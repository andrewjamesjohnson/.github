"""Tiny SVG kit for the portfolio exhibits.

The look is a research report exhibit: white page, a thin rule under the title, dark navy ink, grey notes,
square corners, and one blue used only for things that feed back. No gradients, no glows, no pastel fills,
no dotted paths. Text uses the reader's system font, because GitHub shows an SVG as an image and cannot load
web fonts.
"""
from xml.sax.saxutils import escape

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
PAPER = "#FFFFFF"
EDGE = "#D0D7DE"
INK = "#0B1F33"
MUTED = "#4A5565"
FAINT = "#7A8594"
LINE = "#B8C0CC"
FILL = "#FFFFFF"
SHADE = "#F3F5F8"
BLUE = "#1A4E9A"
BLUE_FILL = "#FFFFFF"
HUMAN = "#0B2545"


def w(text, size, weight=400):
    """Rough text width in px for the system sans at this size."""
    k = 0.55 if weight < 600 else 0.59
    return len(text) * size * k


class SVG:
    def __init__(self, width, height, title, desc=""):
        self.W, self.H = width, height
        self.parts = []
        self.title, self.desc = title, desc
        self.marker_ids = set()

    def add(self, s):
        self.parts.append(s)

    # ---- primitives -------------------------------------------------------
    def card(self, pad=0):
        self.add(f'<rect x="{pad+0.5}" y="{pad+0.5}" width="{self.W-2*pad-1}" height="{self.H-2*pad-1}" '
                 f'rx="6" fill="{PAPER}" stroke="{EDGE}"/>')

    def text(self, x, y, s, size=14, weight=400, color=INK, anchor="start", spacing=0, italic=False):
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" '
                 f'text-anchor="{anchor}"{ls}{st}>{escape(s)}</text>')

    def lines(self, x, y, rows, size=13, gap=None, color=MUTED, weight=400, anchor="start"):
        gap = gap or round(size * 1.38)
        for i, r in enumerate(rows):
            self.text(x, y + i * gap, r, size, weight, color, anchor)

    def kicker(self, x, y, s, color=FAINT):
        self.text(x, y, s, 12.5, 600, color)

    def rect(self, x, y, wd, ht, fill=FILL, stroke=LINE, rx=3, sw=1):
        self.add(f'<rect x="{x}" y="{y}" width="{wd}" height="{ht}" rx="{min(rx, 3)}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, x1, y1, x2, y2, color=LINE, sw=1.2):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>')

    def source(self, s):
        self.text(40, self.H - 18, s, 11.5, 400, FAINT)

    def _marker(self, color):
        mid = "m" + color.strip("#")
        if mid not in self.marker_ids:
            self.marker_ids.add(mid)
            self.parts.insert(0, f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
                                 f'markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">'
                                 f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker></defs>')
        return mid

    def arrow(self, x1, y1, x2, y2, color=INK, sw=1.3):
        m = self._marker(color)
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" '
                 f'marker-end="url(#{m})"/>')

    def path_arrow(self, d, color=BLUE, sw=1.5):
        m = self._marker(color)
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
                 f'stroke-linejoin="miter" marker-end="url(#{m})"/>')

    # ---- composites -------------------------------------------------------
    def node(self, x, y, wd, ht, head, rows=(), human=False, loop=False, num=None, head_size=14.5):
        fill, stroke, hc, rc, sw = FILL, LINE, INK, MUTED, 1
        if human:
            fill, stroke, hc, rc = HUMAN, HUMAN, "#FFFFFF", "#C9D3E0"
        elif loop:
            stroke, hc, sw = BLUE, BLUE, 1.5
        self.rect(x, y, wd, ht, fill, stroke, sw=sw)
        tx, ty = x + 14, y + 26
        if num is not None:
            self.text(tx, ty, f"{num}", 12, 700, "#9FB0C4" if human else FAINT)
            tx2 = tx + 18
        else:
            tx2 = tx
        self.text(tx2, ty, head, head_size, 700, hc)
        self.lines(tx, ty + 21, rows, 12.5, color=rc)

    def render(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" '
                f'viewBox="0 0 {self.W} {self.H}" font-family="{FONT}" role="img" '
                f'aria-labelledby="t d"><title id="t">{escape(self.title)}</title>'
                f'<desc id="d">{escape(self.desc)}</desc>')
        return head + "".join(self.parts) + "</svg>\n"

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.render())
        return path
