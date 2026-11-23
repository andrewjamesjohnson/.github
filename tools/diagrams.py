"""Builds every portfolio diagram (SVG) into each repo's docs/ folder.

Run from anywhere:  python3 .github/tools/diagrams.py
Every diagram is 880 px wide, so GitHub shows it at about full size and the
smallest text stays readable on a laptop.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import SVG, INK, MUTED, FAINT, LINE, BLUE, BLUE_FILL, FILL, PAPER, w

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
W = 880


def out(repo, name):
    d = os.path.join(ROOT, repo, "profile" if repo == ".github" else "docs")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def header(s, kicker, title, sub=None, y=48):
    s.kicker(40, y, kicker)
    s.text(40, y + 38, title, 30, 700)
    if sub:
        s.text(40, y + 66, sub, 15, 400, MUTED)


# ---------------------------------------------------------------------------
# Front page: who I am
# ---------------------------------------------------------------------------
def hero():
    s = SVG(W, 330, "Andrew James Johnson",
            "I build systems that run themselves. Finance student, applied AI builder.")
    s.card()
    s.kicker(40, 52, "Andrew James Johnson")
    s.text(40, 104, "I build systems that run", 40, 700)
    s.text(40, 152, "themselves.", 40, 700)
    s.text(40, 190, "Finance student and applied AI builder. I map a job as data in, a decision,", 15.5, 400, MUTED)
    s.text(40, 212, "data out and a check, then build the loop that does it every day.", 15.5, 400, MUTED)
    s.line(40, 240, W - 40, 240, LINE, 1)
    stats = [("1,435", "commits in 5 weeks"), ("6,222", "tests on one system"),
             ("51", "jobs on timers"), ("1", "human in the loop: me")]
    cw = (W - 80) / 4
    for i, (n, l) in enumerate(stats):
        x = 40 + i * cw
        s.text(x, 284, n, 30, 700, BLUE if i == 3 else INK)
        s.text(x, 308, l, 13.5, 400, MUTED)
    return s.save(out(".github", "hero.svg"))


def how_i_build():
    s = SVG(W, 470, "How I build anything",
            "Six steps that repeat: map, build the smallest loop, gate it in code, run in shadow, measure, keep or roll back.")
    s.card()
    header(s, "How I build", "The same six steps, every project",
           "Built once, then improved every day by its own results.")
    steps = [
        ("Map it", ["Data in, a decision,", "data out, a check.", "Where do parts meet?"]),
        ("Smallest loop", ["One path that runs end", "to end today, even", "if it is ugly."]),
        ("Gate it in code", ["Every rule is a check", "that answers in fixed", "words. Never vibes."]),
        ("Run in shadow", ["It decides, nothing", "ships. I compare its", "calls to mine."]),
        ("Measure", ["Real results only.", "Views, fills, returns,", "errors caught."]),
        ("Keep or roll back", ["Every change ends", "KEEP, NO EFFECT", "or ROLL BACK."]),
    ]
    cols, gx, gy = 3, 20, 20
    bw = (W - 80 - gx * (cols - 1)) / cols
    bh = 108
    for i, (h, rows) in enumerate(steps):
        r, c = divmod(i, cols)
        x = 40 + c * (bw + gx)
        y = 140 + r * (bh + gy)
        s.node(x, y, bw, bh, h, rows, num=i + 1, loop=(i == 5))
        if c < cols - 1:
            s.arrow(x + bw + 2, y + bh / 2, x + bw + gx - 2, y + bh / 2, INK)
    # row 1 end drops to row 2 start
    x3 = 40 + 2 * (bw + gx) + bw / 2
    x1 = 40 + bw / 2
    s.path_arrow(f"M{x3},{140+bh+2} L{x3},{140+bh+10} L{x1},{140+bh+10} L{x1},{140+bh+gy-2}", INK, 1.4)
    # the loop back from step 6 to step 1
    yb = 140 + 2 * bh + gy + 22
    x6 = 40 + 2 * (bw + gx) + bw / 2
    s.path_arrow(f"M{x6},{140+2*bh+gy+2} L{x6},{yb} L{20},{yb} L{20},{140+bh/2} L{38},{140+bh/2}", BLUE, 1.6)
    s.text(W / 2, yb + 22, "The loop runs again with what it learned.", 13.5, 600, BLUE, anchor="middle")
    return s.save(out(".github", "how-i-build.svg"))


# ---------------------------------------------------------------------------
# Clip Factory
# ---------------------------------------------------------------------------
CF_STEPS = [
    ("Find", "every hour", ["Scouts read news channels, hearings and live streams every hour. A breaking",
                            "desk checks the news every 15 minutes. A hunt digs up past hearings."]),
    ("Pick", "15:00 board", ["A daily board ranks every moment by who is in it, the video, the moment",
                               "and how fresh it is. The best clips go first. Formats are picked after."]),
    ("Make", "21:00 night shift", ["Claude agents cut the night's clips: the hook, the cut points, captions,",
                                   "framing, title and cover. A render engine draws every frame."]),
    ("Check", "every clip", ["Code gates read each clip. Every caption word is really said, the face",
                             "matches the name, no dead air, no loading screens, swears muted."]),
    ("Me", "one tap", ["I watch each clip in Clip Review and approve it. Nothing posts that I have",
                       "not seen, or that changed after I saw it."]),
    ("Dress", "at the upload door", ["Overlays go on last, on a copy: stickers, sounds, a flash on the hit.",
                                     "Only where the moment earns it. Best clip first, overlays last."]),
    ("Post", "at its slot", ["Official APIs only: YouTube Data API, Meta Graph for Facebook and",
                             "Instagram Reels. TikTok by hand. A post that may be up is looked up, never resent."]),
    ("Measure", "every 30 min", ["Views, watch time and drop off for every clip on every platform.",
                                 "Second by second retention from the YouTube Analytics API."]),
    ("Learn", "05:20 + 12:20", ["A coach agent reads the numbers and writes tomorrow's lessons. Every",
                                "rule change is replayed on past nights, then KEEP, NO EFFECT or ROLL BACK."]),
]


def cf_loop():
    top, bh, gap = 150, 74, 12
    H = top + len(CF_STEPS) * (bh + gap) + 30
    s = SVG(W, H, "The Clip Factory loop",
            "Nine steps: find, pick, make, check, me, dress, post, measure, learn, and back to find.")
    s.card()
    header(s, "The Clip Factory", "One loop, running 24/7",
           "Nine steps. Code and agents do eight of them. I do one.")
    x0, x1 = 40, W - 96
    for i, (name, when, rows) in enumerate(CF_STEPS):
        y = top + i * (bh + gap)
        human, loop = name == "Me", name == "Learn"
        fill = INK if human else (BLUE_FILL if loop else FILL)
        stroke = INK if human else (BLUE if loop else LINE)
        hc = "#FFFFFF" if human else (BLUE if loop else INK)
        rc = "#D9D9D4" if human else ("#3D4F86" if loop else MUTED)
        s.rect(x0, y, x1 - x0, bh, fill, stroke)
        s.text(x0 + 18, y + 31, f"{i+1:02d}", 12, 700, "#A9A9A4" if human else FAINT, spacing=1)
        s.text(x0 + 46, y + 31, name, 17, 700, hc)
        s.text(x0 + 18, y + 53, when, 12.5, 400, rc)
        s.lines(x0 + 170, y + 31, rows, 13.2, gap=19, color=hc if human else INK if not loop else "#22336B")
        if i < len(CF_STEPS) - 1:
            s.arrow(x0 + 60, y + bh + 1, x0 + 60, y + bh + gap - 1, INK, 1.3)
    # the loop: from Learn back up to Find
    yl = top + 8 * (bh + gap) + bh / 2
    yf = top + bh / 2
    xr = W - 50
    s.path_arrow(f"M{x1},{yl} L{xr},{yl} L{xr},{yf} L{x1+3},{yf}", BLUE, 1.8)
    ym = top + 2 * (bh + gap) + bh / 2
    s.path_arrow(f"M{xr},{ym} L{x1+3},{ym}", BLUE, 1.4)
    s.add(f'<text x="{xr+18}" y="{(yl+yf)/2}" font-size="12.5" font-weight="700" fill="{BLUE}" '
          f'text-anchor="middle" letter-spacing="1.4" transform="rotate(90 {xr+18} {(yl+yf)/2})">'
          f'LESSONS FEED THE NEXT NIGHT</text>')
    return s.save(out("clip-factory", "loop.svg"))


def cf_day():
    H = 500
    s = SVG(W, H, "A day in the Clip Factory",
            "24 hours of timers: night shift, posting window, scouts, breaking desk, stats, coach and fixer.")
    s.card()
    header(s, "A day in the factory", "Nobody presses start",
           "Every job below runs on a timer. Times are Mountain.")
    ax0, ax1 = 130, W - 40
    hx = lambda h: ax0 + (ax1 - ax0) * h / 24
    for h in range(0, 25, 3):
        x = hx(h)
        s.text(x, 142, f"{h:02d}:00", 11.5, 400, FAINT, anchor="middle")
        s.line(x, 150, x, 440, "#ECECE8", 1)
    rows = {"Find": 160, "Make": 218, "Check": 276, "Post": 334, "Learn": 392}
    for name, y in rows.items():
        s.text(40, y + 26, name, 15, 700)

    def bar(h0, h1, y, label="", kind="plain"):
        x0, x1 = hx(h0), hx(h1)
        fill, stroke, col = {"plain": ("#E9E9E5", "#CFCFCB", INK), "solid": (INK, INK, "#FFFFFF"),
                             "loop": (BLUE_FILL, BLUE, BLUE)}[kind]
        s.rect(x0, y + 10, x1 - x0, 24, fill, stroke, rx=6)
        if label:
            s.text(x0 + 9, y + 27, label, 12, 600, col)

    def mark(h, y, label, kind="ink"):
        x = hx(h)
        c = BLUE if kind == "loop" else INK
        s.line(x, y + 6, x, y + 38, c, 2)
        s.text(x + 6, y + 50, label, 11.5, 700 if kind == "loop" else 400, c)

    y = rows["Find"]
    for h in range(5, 23):
        for m in (5, 40):
            x = hx(h + m / 60)
            s.line(x, y + 2, x, y + 9, INK, 1.4)
    bar(5 + 5 / 60, 20 + 50 / 60, y + 4, "Breaking desk every 15 min, plus scouts at :05 and :40")
    y = rows["Make"]
    bar(0, 5, y, "Night shift", "solid")
    bar(21, 24, y, "Night", "solid")
    mark(8, y, "08:00 make-up run")
    mark(15, y, "15:00 prep")
    y = rows["Check"]
    bar(0, 5, y, "Gates, every clip")
    bar(21, 24, y, "Gates")
    mark(7 + 20 / 60, y, "07:20 fixer")
    mark(16 + 20 / 60, y, "16:20 fixer")
    y = rows["Post"]
    bar(7, 21, y, "Posting slots, 07:00 to 21:00, each clip at its own time")
    mark(6 + 26 / 60, y - 2, "")
    s.text(hx(6 + 26 / 60) - 6, y + 48, "06:26 bench fill", 11.5, 400, INK, anchor="end")
    y = rows["Learn"]
    bar(0, 24, y, "Stats read every 30 minutes, every platform", "loop")
    mark(5 + 20 / 60, y, "05:20 coach", "loop")
    mark(12 + 20 / 60, y, "12:20 coach", "loop")
    s.text(40, 478, "34 launchd timers and 17 scheduled Claude jobs run this day, every day.", 13, 400, MUTED)
    return s.save(out("clip-factory", "day.svg"))


# ---------------------------------------------------------------------------
# Job Bot
# ---------------------------------------------------------------------------
def jb_funnel():
    rows = [
        ("93,000", "open jobs", "on 1,801 public company boards (Greenhouse, Lever, Ashby)", 1.00),
        ("3,300", "fit", "entry level, US or remote, the kind of job I actually want", 0.62),
        ("150", "a day", "best score against my five resumes, every link opened first", 0.36),
        ("10", "tabs", "forms filled in my own Chrome: name, school, resume, yes and no questions", 0.18),
        ("1", "click", "mine. The bot never presses Submit. That part is still a person.", 0.05),
    ]
    top, rh = 150, 72
    H = top + len(rows) * rh + 20
    s = SVG(W, H, "The Job Bot funnel",
            "93,000 open jobs down to 150 a day, 10 filled tabs, and one human click.")
    s.card()
    header(s, "The Job Bot", "From 93,000 jobs to one click",
           "Every morning at 06:30, before I am awake.")
    bx, bmax = 250, W - 40 - 250
    for i, (n, unit, note, frac) in enumerate(rows):
        y = top + i * rh
        last = i == len(rows) - 1
        s.text(40, y + 34, n, 28, 700, INK)
        s.text(40 + w(n, 28, 700) + 10, y + 34, unit, 15, 600, MUTED)
        s.rect(bx, y + 8, max(14, bmax * frac), 14, INK if last else LINE, INK if last else LINE, rx=4)
        s.text(bx, y + 46, note, 13.2, 400, MUTED)
        if not last:
            s.line(40, y + rh - 8, W - 40, y + rh - 8, "#E6E6E2", 1)
    return s.save(out("job-bot", "funnel.svg"))


def jb_form():
    H = 560
    s = SVG(W, H, "What the form filler does to an application",
            "A job form with every field filled by the bot, two questions left yellow for me, and a Submit button the bot never presses.")
    s.card()
    header(s, "The form filler", "It fills the boring parts. I do the honest parts.",
           "A real application form, after the bot has been through it.")
    fx, fy, fw = 40, 140, 520
    s.rect(fx, fy, fw, 390, FILL, LINE, rx=12)
    s.text(fx + 24, fy + 36, "Finance Data Analyst Intern, 2027", 16, 700)
    fields = [
        ("First name", "Andrew", "ok"), ("Last name", "Johnson", "ok"),
        ("School", "University of Utah", "ok"), ("Resume", "Quant resume.pdf", "ok"),
        ("Authorized to work in the US?", "Yes", "ok"),
        ("Why this company?", "", "yellow"), ("Anything else we should know?", "", "yellow"),
    ]
    y = fy + 62
    for label, val, kind in fields:
        s.text(fx + 24, y + 14, label, 12, 600, MUTED)
        if kind == "ok":
            s.rect(fx + 230, y, fw - 254, 24, "#FFFFFF", "#CFCFCB", rx=5)
            s.text(fx + 240, y + 17, val, 13, 400, INK)
        else:
            s.rect(fx + 230, y - 2, fw - 254, 28, "#FFF6CC", "#E8B600", rx=5, sw=2.2)
            s.text(fx + 240, y + 17, "yellow: this one is mine", 13, 600, "#8A6A00")
        y += 40
    s.rect(fx + 24, y + 6, 130, 36, INK, INK, rx=8)
    s.text(fx + 89, y + 30, "Submit", 14, 700, "#FFFFFF", anchor="middle")
    s.text(fx + 170, y + 30, "never pressed by the bot", 13, 600, INK)
    # the notes on the right
    nx = 600
    notes = [
        ("Filled by the bot", ["Name, contact, links, school,", "degree, the right resume,", "work status, EEO answers."]),
        ("Left yellow", ["Essays and anything it is", "not sure about. It never", "guesses. Wrong school once,", "so the rules are strict now."]),
        ("Never done", ["Submit, CAPTCHAs, LinkedIn", "Easy Apply. Those stay", "with a human."]),
    ]
    ny = 150
    for h, rows in notes:
        s.text(nx, ny, h, 15, 700, INK if h != "Left yellow" else "#8A6A00")
        s.lines(nx, ny + 22, rows, 13, color=MUTED)
        ny += 34 + 19 * len(rows) + 26
    return s.save(out("job-bot", "form.svg"))


# ---------------------------------------------------------------------------
# Congress Stock Scorecard
# ---------------------------------------------------------------------------
def cs_morning():
    H = 330
    s = SVG(W, H, "A Congress Scorecard morning",
            "02:30 prices, 06:00 estimates and slides, 06:05 my phone, 06:30 posted, 09:30 cut off.")
    s.card()
    header(s, "Congress Stock Scorecard", "One market morning, by itself",
           "Public filings in. Eight slides out. One tap from me in between.")
    steps = [
        ("02:30", "Prices", ["Streams IEX's daily", "file, 10 to 15 GB,", "keeps last trades."], False),
        ("06:00", "Estimates", ["Every member's gain,", "SEC earnings since", "the close, slides."], False),
        ("06:05", "My phone", ["Every slide on one", "picture: Post it", "or No."], True),
        ("06:30", "Posted", ["Only on Post it.", "A changed slide", "is refused."], False),
        ("09:30", "Cut off", ["No answer means", "nothing goes out", "that day."], False),
    ]
    gx = 14
    bw = (W - 80 - gx * 4) / 5
    for i, (t, h, rows, human) in enumerate(steps):
        x = 40 + i * (bw + gx)
        s.node(x, 148, bw, 132, h, rows, human=human)
        s.text(x + 16, 140, t, 12.5, 700, FAINT)
        if i < 4:
            s.arrow(x + bw + 1, 214, x + bw + gx - 1, 214, INK)
    s.text(40, 310, "Next market morning it runs again. Weekends and holidays it stays quiet.", 13, 400, MUTED)
    return s.save(out("congress-stock-scorecard", "morning.svg"))


if __name__ == "__main__":
    for f in (hero, how_i_build, cf_loop, cf_day, jb_funnel, jb_form, cs_morning):
        print(f())
