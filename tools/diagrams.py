"""Builds every portfolio diagram (SVG) into each repo's docs/ folder.

Run from anywhere:  python3 .github/tools/diagrams.py
Every diagram is 880 px wide, so GitHub shows it at about full size and the
smallest text stays readable on a laptop.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import SVG, INK, MUTED, FAINT, LINE, BLUE, BLUE_FILL, FILL, PAPER, SHADE, HUMAN, w

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
W = 880


def out(repo, name):
    d = os.path.join(ROOT, repo, "profile" if repo == ".github" else "docs")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def header(s, label, title, sub=None, y=40):
    s.kicker(40, y, label)
    s.text(40, y + 30, title, 21, 700)
    if sub:
        s.text(40, y + 54, sub, 13.5, 400, MUTED)
    s.line(40, y + 72, W - 40, y + 72, INK, 1)


# ---------------------------------------------------------------------------
# Front page: who I am
# ---------------------------------------------------------------------------
def hero():
    s = SVG(W, 330, "Andrew James Johnson",
            "Finance first, AI as leverage. Finance student building the systems a fund runs on.")
    s.card()
    s.kicker(40, 52, "Andrew James Johnson")
    s.text(40, 104, "Finance first.", 40, 700)
    s.text(40, 152, "AI as leverage.", 40, 700, MUTED)
    s.text(40, 190, "Finance student at the University of Utah. I build the systems a fund runs on:", 15.5, 400, MUTED)
    s.text(40, 212, "research, risk, operations and compliance, with a person making every call.", 15.5, 400, MUTED)
    s.line(40, 240, W - 40, 240, LINE, 1)
    stats = [("109", "agents on a fund desk"), ("52", "coverage and research desks"),
             ("13,000+", "tests across my systems"), ("1", "human in the loop: me")]
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
    header(s, "Method", "How each system gets built",
           "The same six steps on every project, repeated as results come in.")
    steps = [
        ("Map the process", ["What comes in, what gets", "decided, what goes out", "and what checks it."]),
        ("Build one path", ["One working path, end", "to end, before adding", "anything else."]),
        ("Rules become checks", ["Each rule is a test in", "code with a fixed pass", "or fail answer."]),
        ("Run in shadow", ["It makes the call,", "nothing ships, and I", "compare it with mine."]),
        ("Measure", ["Real outcomes only:", "returns, views, errors", "caught, time saved."]),
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
    s.text(W / 2, yb + 22, "Results go into the next round of changes.", 13.5, 600, BLUE, anchor="middle")
    return s.save(out("loop-engineering", "method.svg"))


# ---------------------------------------------------------------------------
# Loop Engineering: the overview at the top of the front page
# ---------------------------------------------------------------------------
def le_loops():
    H = 624
    s = SVG(W, H, "Loop Engineering: how my systems run",
            "Sources, agents, checks, a person's sign off, output and results, with a fix loop, a day loop and a "
            "week loop sending results back, and the five parts that keep every step on track.")
    s.card()
    header(s, "Loop Engineering", "How my systems run",
           "The loop under The Clip Factory and Mac Studio Prepared, from the first source to the measured result.")
    steps = [
        ("Sources", "code", ["Filings, prices,", "news, streams", "and hearings."]),
        ("Agents", "AI agents", ["Each role", "follows its own", "written workflow."]),
        ("Checks", "code", ["Every rule is", "a test in code,", "pass or fail."]),
        ("Approval", "a person", ["Signs off on", "anything that", "matters."]),
        ("Output", "code", ["Clips, research", "notes and", "trade plans."]),
        ("Results", "code", ["Real outcomes:", "views, returns,", "time saved."]),
    ]
    n, gx = len(steps), 16
    bw = (W - 80 - gx * (n - 1)) / n
    top, bh = 176, 118
    xs = [40 + i * (bw + gx) for i in range(n)]

    def cx(i, f=0.5):
        return round(xs[i] + bw * f, 1)

    for i, (head, who, rows) in enumerate(steps):
        x, human = xs[i], head == "Approval"
        s.rect(x, top, bw, bh, HUMAN if human else FILL, HUMAN if human else LINE)
        s.text(x + 14, top + 26, str(i + 1), 12, 700, "#9FB0C4" if human else FAINT)
        s.text(x + 30, top + 26, head, 14.5, 700, "#FFFFFF" if human else INK)
        s.text(x + 14, top + 45, who, 12, 400, "#9FB0C4" if human else FAINT)
        s.lines(x + 14, top + 70, rows, 12.5, gap=17, color="#C9D3E0" if human else MUTED)
        if i < n - 1:
            s.arrow(x + bw + 1, top + bh / 2, x + bw + gx - 1, top + bh / 2, INK, 1.3)
    bot = top + bh
    # week loop: results go back over the top to the checks, where the rules live
    yw = top - 26
    s.path_arrow(f"M{cx(5)},{top-2} L{cx(5)},{yw} L{cx(2)},{yw} L{cx(2)},{top-3}", BLUE, 1.6)
    s.text((cx(2) + cx(5)) / 2, yw - 9, "Week loop", 12.5, 700, BLUE, anchor="middle")
    # fix loop: a failed check goes back to the agents
    yf = bot + 24
    s.path_arrow(f"M{cx(2,0.35)},{bot+2} L{cx(2,0.35)},{yf} L{cx(1,0.65)},{yf} L{cx(1,0.65)},{bot+3}", BLUE, 1.6)
    s.text((cx(2, 0.35) + cx(1, 0.65)) / 2, yf + 18, "Fix loop", 12.5, 700, BLUE, anchor="middle")
    # day loop: results become the lessons the next run starts from
    yd = bot + 54
    s.path_arrow(f"M{cx(5)},{bot+2} L{cx(5)},{yd} L{cx(1,0.3)},{yd} L{cx(1,0.3)},{bot+3}", BLUE, 1.6)
    s.text((cx(3) + cx(5)) / 2, yd - 9, "Day loop", 12.5, 700, BLUE, anchor="middle")
    # what each loop does
    legend = [
        ("Fix loop", "minutes", ["A failed check goes back to be", "fixed, with the reason it failed."]),
        ("Day loop", "daily", ["Results become the lessons the", "next run reads first."]),
        ("Week loop", "weekly", ["Rule changes are replayed on past", "runs, then KEEP, NO EFFECT or ROLL BACK."]),
    ]
    cw = (W - 80) / 3
    ly = 394
    for i, (name, when, rows) in enumerate(legend):
        x = 40 + i * cw
        s.add(f'<text x="{x}" y="{ly}" font-size="13" font-weight="700" fill="{BLUE}">{name}'
              f'<tspan font-weight="400" fill="{FAINT}">  ·  {when}</tspan></text>')
        s.lines(x, ly + 21, rows, 12.2, gap=17, color=MUTED)
    # the parts that keep every step on track
    s.line(40, 462, W - 40, 462, LINE, 1)
    s.kicker(40, 488, "What keeps every step on track")
    parts = [
        ("Memory", ["One shared board every", "step reads first and", "writes last."]),
        ("Gates", ["Code checks each rule", "and answers in fixed", "words."]),
        ("Journal", ["Every run leaves a line,", "so a crash picks up", "where it fell."]),
        ("Replay", ["Real past jobs rerun", "before any engine", "change ships."]),
        ("Undo", ["Every live change", "ships with a way back."]),
    ]
    pw = (W - 80) / len(parts)
    for i, (name, rows) in enumerate(parts):
        x = 40 + i * pw
        s.text(x, 514, name, 13.5, 700)
        s.lines(x, 535, rows, 12.2, gap=17, color=MUTED)
    s.source("Source: The Clip Factory and Mac Studio Prepared, November 2026. Blue: results going back in. "
             "Dark: a person.")
    return s.save(out("loop-engineering", "loops.svg"))


# ---------------------------------------------------------------------------
# Clip Factory
# ---------------------------------------------------------------------------
CF_STEPS = [
    ("Find", "every hour", ["Scouts read news channels, hearings and live streams every hour. A breaking",
                            "desk checks the news every 15 minutes. A hunt digs up past hearings."]),
    ("Pick", "15:00 board", ["A daily board ranks every moment by who is in it, the video, the moment",
                               "and how fresh it is. The best clips go first. Formats are picked after."]),
    ("Make", "21:00 night shift", ["AI agents cut the night's clips: the hook, the cut points, captions,",
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
    header(s, "The Clip Factory", "From source video to posted clip",
           "Nine stages. Eight run on their own. One is my approval.")
    x0, x1 = 40, W - 96
    for i, (name, when, rows) in enumerate(CF_STEPS):
        y = top + i * (bh + gap)
        human, loop = name == "Me", name == "Learn"
        fill = INK if human else (BLUE_FILL if loop else FILL)
        stroke = INK if human else (BLUE if loop else LINE)
        hc = "#FFFFFF" if human else (BLUE if loop else INK)
        rc = "#C9D3E0" if human else (MUTED if loop else MUTED)
        s.rect(x0, y, x1 - x0, bh, fill, stroke)
        s.text(x0 + 18, y + 31, f"{i+1:02d}", 12, 700, "#9FB0C4" if human else FAINT, spacing=1)
        s.text(x0 + 46, y + 31, name, 17, 700, hc)
        s.text(x0 + 18, y + 53, when, 12.5, 400, rc)
        s.lines(x0 + 170, y + 31, rows, 13.2, gap=19, color=hc if human else INK if not loop else INK)
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
          f'Lessons go to the next night</text>')
    return s.save(out("clip-factory", "loop.svg"))


def cf_day():
    H = 500
    s = SVG(W, H, "A day in the Clip Factory",
            "24 hours of timers: night shift, posting window, scouts, breaking desk, stats, coach and fixer.")
    s.card()
    header(s, "The Clip Factory", "Daily schedule",
           "Every job runs on a timer. Mountain time.")
    ax0, ax1 = 130, W - 40
    hx = lambda h: ax0 + (ax1 - ax0) * h / 24
    for h in range(0, 25, 3):
        x = hx(h)
        s.text(x, 142, f"{h:02d}:00", 11.5, 400, FAINT, anchor="middle")
        s.line(x, 150, x, 440, "#EEF1F5", 1)
    rows = {"Find": 160, "Make": 218, "Check": 276, "Post": 334, "Learn": 392}
    for name, y in rows.items():
        s.text(40, y + 26, name, 15, 700)

    def bar(h0, h1, y, label="", kind="plain"):
        x0, x1 = hx(h0), hx(h1)
        fill, stroke, col = {"plain": (SHADE, "#C3CAD4", INK), "solid": (INK, INK, "#FFFFFF"),
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
    s.text(40, 478, "34 launchd timers and 17 scheduled AI jobs run this day, every day.", 13, 400, MUTED)
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
            s.line(40, y + rh - 8, W - 40, y + rh - 8, "#E3E7ED", 1)
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
            s.rect(fx + 230, y, fw - 254, 24, "#FFFFFF", "#C3CAD4", rx=5)
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
    header(s, "Congress Stock Scorecard", "A market morning",
           "Public filings in, eight slides out, and my approval in between.")
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


# ---------------------------------------------------------------------------
# Mac Studio Prepared
# ---------------------------------------------------------------------------
def msp_firm():
    H = 760
    s = SVG(W, H, "The firm: Mac Studio Prepared",
            "109 AI agent seats organised like a fund: research, 52 coverage desks, risk, operations, compliance, clients and the platform, under a PM who signs every decision.")
    s.card()
    header(s, "Mac Studio Prepared", "A fund desk of 109 agents",
           "Organised the way a real fund runs. Every decision goes to a person.")
    # people at the top
    s.node(300, 140, 280, 64, "The PM and me", ["Approve, trade, send. Nobody else can."], human=True)
    s.arrow(440, 206, 440, 226, INK)
    s.node(280, 228, 320, 64, "Head of the floor", ["Routes every task to the right seats."])
    s.line(440, 294, 440, 312, INK, 1.4)
    s.line(110, 312, 770, 312, INK, 1.4)
    depts = [
        ("Research", 14, ["Reader, watcher, analyst,", "checker, transcriber,", "earnings, quant research,", "forecaster, librarian"]),
        ("Coverage", 48, ["Rates, credit, FX, macro,", "energy, tech, banks,", "biotech, M&A, shorts,", "China, Japan, Europe..."]),
        ("Risk and book", 6, ["Risk manager, execution,", "derivatives quant,", "P&L explainer, tax,", "corporate actions"]),
        ("Operations", 3, ["Reconciler (three ways,", "every morning), shadow", "NAV controller,", "treasury guard"]),
    ]
    depts2 = [
        ("Compliance", 10, ["Legal, restricted list,", "pre-clearance, trade", "surveillance, sanctions,", "MNPI wall, filings clock"]),
        ("Data", 8, ["Licences, data quality,", "alt data, power grid,", "shipping, weather,", "public record, social"]),
        ("Clients and IR", 3, ["Client book, DDQs and", "the letter, allocator", "flows"]),
        ("Discipline", 4, ["Devil's advocate,", "scorekeeper, costs,", "retro coach", ""]),
    ]
    bw, bh, gx = 190, 150, 20
    for row, (dl, y) in enumerate(((depts, 326), (depts2, 500))):
        for i, (name, n, rows) in enumerate(dl):
            x = 40 + i * (bw + gx)
            if row == 0:
                s.line(x + bw / 2, 312, x + bw / 2, y, INK, 1.4)
            s.rect(x, y, bw, bh, FILL, LINE)
            s.text(x + 16, y + 30, name, 15, 700)
            s.text(x + bw - 16, y + 30, str(n), 15, 700, FAINT, anchor="end")
            s.lines(x + 16, y + 56, [r for r in rows if r], 12.5, color=MUTED)
    s.text(40, 690, "Plus 5 platform seats (model lab, model scout, coder, frontier desk, postmaster), a 6 seat public", 13, 400, MUTED)
    s.text(40, 710, "media studio, and a chief of staff. Each seat has a written role, a data clearance and an owner.", 13, 400, MUTED)
    s.text(40, 740, "Counts are seats per group. Built and tested on a fictional market ahead of the hardware.", 12, 400, FAINT)
    return s.save(out("mac-studio-prepared", "firm.svg"))


MSP_MORNING = [
    ("03:15", "Integrity check", "Verify the audit chain. Prove a fake private file cannot reach the cloud."),
    ("04:00", "Broker digest", "Sell side notes on our names, read and summarised. Licensed research stays inside."),
    ("04:15", "Risk report", "VaR, stress tests, limits and liquidity, with an optimizer proposal."),
    ("04:30", "Thesis monitor", "Every new filing and call checked against each thesis's own sell if rules."),
    ("05:00", "Morning brief", "Positions, watchlist, overnight news through the impact map. Checked, then filed."),
    ("06:22", "Morning call", "The early read, held until risk, the books, NAV and the P&L explanation are in."),
    ("06:30", "Middle office", "Corporate actions, three way reconciliation, cash ladder, P&L attribution, NAV check."),
    ("06:55", "Ops and compliance", "One page for the COO and CCO: breaks, payee changes, pre-clearance, MNPI flags."),
    ("06:58", "Ready to open?", "Eight checks in code. One answer: yes, or no with what is missing and who acts."),
    ("07:30", "PM meeting", "The PM reviews the late edition. Trades are placed by people only."),
]


def msp_morning():
    top, rh = 150, 54
    H = top + len(MSP_MORNING) * rh + 30
    s = SVG(W, H, "The trading morning",
            "From the 03:15 integrity check to the 07:30 PM meeting, with the 06:58 ready to open gate.")
    s.card()
    header(s, "Mac Studio Prepared", "The trading morning, New York time",
           "Each step waits for the one before it. At 06:58 a gate decides whether the desk is ready.")
    for i, (t, name, note) in enumerate(MSP_MORNING):
        y = top + i * rh
        human = name == "PM meeting"
        gate = name == "Ready to open?"
        if human or gate:
            s.rect(40, y + 2, W - 80, rh - 8, INK if human else BLUE_FILL, INK if human else BLUE, rx=8)
        c1 = "#FFFFFF" if human else (BLUE if gate else INK)
        c2 = "#C9D3E0" if human else (INK if gate else MUTED)
        s.text(58, y + 30, t, 14, 700, "#9FB0C4" if human else FAINT)
        s.text(130, y + 30, name, 15, 700, c1)
        s.text(310, y + 30, note, 12.8, 400, c2)
        if not (human or gate) and i < len(MSP_MORNING) - 1 and MSP_MORNING[i + 1][1] != "Ready to open?":
            s.line(58, y + rh - 3, W - 58, y + rh - 3, "#E3E7ED", 1)
    return s.save(out("mac-studio-prepared", "morning.svg"))


def msp_event():
    steps = [
        ("Screen", "code", "PUBLIC", "Instructions hidden in a headline are quarantined."),
        ("Triage", "fast model", "PUBLIC", "Which hub, which direction, is it new, how sure."),
        ("Gate", "code", "PUBLIC", "Duplicates and unsure calls go to a second read."),
        ("Basket", "code", "INTERNAL", "The impact map ranks suppliers, customers, rivals."),
        ("Overlap", "code", "RESTRICTED", "Which of those names we hold, and which side."),
        ("Brief", "analyst", "RESTRICTED", "Written only from the facts the code passed it."),
        ("Number check", "code", "RESTRICTED", "Every number traced. A made up $61bn was caught."),
        ("Inbox", "a person", "RESTRICTED", "Pending review. Nothing is sent or traded by an agent."),
    ]
    top, rh = 176, 50
    H = top + len(steps) * rh + 40
    s = SVG(W, H, "Headline to brief",
            "The event alert workflow: eight steps from a newswire headline to a checked brief in the inbox, with the data class rising as private data joins.")
    s.card()
    header(s, "Mac Studio Prepared", "Event alert: from headline to checked brief",
           "The newswire is read every 30 seconds. About three minutes from headline to brief.")
    for x, h in ((58, "Step"), (230, "Who"), (360, "Data class"), (490, "What happens")):
        s.kicker(x, 160, h)
    for i, (name, who, cls, note) in enumerate(steps):
        y = top + i * rh
        last = i == len(steps) - 1
        s.rect(40, y + 4, W - 80, rh - 8, INK if last else FILL, INK if last else LINE, rx=8)
        c1 = "#FFFFFF" if last else INK
        c2 = "#C9D3E0" if last else MUTED
        s.text(58, y + 30, f"{i+1}  {name}", 14, 700, c1)
        s.text(230, y + 30, who, 13, 400, c2)
        shade = {"PUBLIC": "#FFFFFF", "INTERNAL": SHADE, "RESTRICTED": "#C3CAD4"}[cls]
        if not last:
            s.rect(360, y + 15, 100, 22, shade, "#B8C0CC", rx=5)
            s.text(410, y + 30, cls, 10.5, 700, INK, anchor="middle", spacing=0.8)
        else:
            s.text(360, y + 30, cls, 10.5, 700, "#C9D3E0", spacing=0.8)
        s.text(490, y + 30, note if len(note) < 58 else note[:57].rsplit(" ", 1)[0] + "...", 12.5, 400, c2)
    s.text(40, H - 18, "Anything built from private inputs is private. Unknown sources count as RESTRICTED.", 12.5, 400, MUTED)
    return s.save(out("mac-studio-prepared", "event.svg"))


def msp_strategy():
    steps = [
        ("Idea", ["A factor or a thesis,", "written down first."]),
        ("Walk forward", ["12 months train,", "3 months test, costs in."]),
        ("Trial ledger", ["Every try counted.", "Deflated Sharpe."]),
        ("Holdout", ["Last 6 months stay shut.", "Opened once, by name."]),
        ("Paper book", ["New days only, real", "fills, borrow, halts."]),
        ("PM decides", ["Tracked against the", "backtest. A person signs."]),
    ]
    H = 530
    s = SVG(W, H, "An idea's path to a paper book",
            "Idea, walk forward backtest, trial ledger with deflated Sharpe, holdout opened once, paper trading on new days, PM decides.")
    s.card()
    header(s, "Mac Studio Prepared", "Strategy validation",
           "A strategy reaches a paper portfolio only after every test below.")
    cols, gx, gy = 3, 20, 20
    bw = (W - 80 - gx * (cols - 1)) / cols
    bh = 92
    for i, (h, rows) in enumerate(steps):
        r, c = divmod(i, cols)
        x = 40 + c * (bw + gx)
        y = 140 + r * (bh + gy)
        s.node(x, y, bw, bh, h, rows, num=i + 1, human=(i == 5))
        if c < cols - 1:
            s.arrow(x + bw + 2, y + bh / 2, x + bw + gx - 2, y + bh / 2, INK)
    x3 = 40 + 2 * (bw + gx) + bw / 2
    x1 = 40 + bw / 2
    s.path_arrow(f"M{x3},{140+bh+2} L{x3},{140+bh+10} L{x1},{140+bh+10} L{x1},{140+bh+gy-2}", INK, 1.4)
    y = 140 + 2 * bh + gy + 30
    s.line(40, y, W - 40, y, LINE, 1)
    s.kicker(40, y + 28, "What the PM sees")
    s.text(40, y + 60, "Before", 13, 700, MUTED)
    s.text(140, y + 60, "Sharpe +1.62", 15, 700)
    s.text(40, y + 90, "Now", 13, 700, INK)
    s.text(140, y + 90, "Sharpe +1.62, standard error 0.81, 391 sessions, 6 trials.", 13, 400)
    s.text(140, y + 110, "Deflated Sharpe 0.52 against a 0.95 line: not significant yet.", 13, 400)
    return s.save(out("mac-studio-prepared", "strategy.svg"))


def msp_wall():
    H = 520
    s = SVG(W, H, "The privacy wall",
            "Private zone on four Mac Studios with local open weight models; one public route out to cloud models for public data only, enforced three times.")
    s.card()
    header(s, "Mac Studio Prepared", "Where the data is allowed to go",
           "Private data stays on the four Studios. The rule is enforced three times and tested every night.")
    # private zone
    s.rect(40, 140, 560, 330, "#FFFFFF", INK, rx=12, sw=1.4)
    s.kicker(60, 168, "Private zone: four Mac Studios")
    macs = [("Studio 1", "Watcher + services", "fast reads, alerts"), ("Studio 2", "Analyst", "every brief"),
            ("Studio 3", "Checker", "numbers, speech, vision"), ("Studio 4", "Lab", "candidate models")]
    for i, (a, b, c) in enumerate(macs):
        x = 60 + (i % 2) * 265
        y = 186 + (i // 2) * 84
        s.rect(x, y, 250, 70, SHADE, LINE, rx=8)
        s.text(x + 14, y + 26, a, 12, 700, FAINT, spacing=1)
        s.text(x + 14, y + 47, b, 14, 700)
        s.text(x + 14, y + 63, c, 12, 400, MUTED)
    s.text(60, 386, "Positions, theses, client data, expert calls, broker research.", 12.5, 400, MUTED)
    s.text(60, 406, "Open weight models only, on hardware the fund owns.", 12.5, 400, MUTED)
    s.rect(60, 422, 520, 32, INK, INK, rx=7)
    s.text(320, 443, "Everything lands in one inbox. A person approves.", 13, 700, "#FFFFFF", anchor="middle")
    # cloud
    s.rect(660, 200, 180, 120, SHADE, LINE, rx=12)
    s.kicker(678, 228, "Cloud")
    s.text(678, 254, "Frontier models", 14, 700)
    s.lines(678, 276, ["public data only:", "filings, news, transcripts"], 12, color=MUTED)
    s.arrow(602, 260, 656, 260, INK)
    s.text(629, 248, "1 route", 11, 700, INK, anchor="middle")
    layers = ["1  The router refuses", "2  The gateway refuses", "3  One network route out", "Canary test every night"]
    s.kicker(660, 352, "Enforced three times")
    s.lines(660, 378, layers, 12.5, gap=21, color=INK)
    return s.save(out("mac-studio-prepared", "wall.svg"))


def msp_learning():
    H = 400
    s = SVG(W, H, "The learning loop",
            "Code measures every call, the coach proposes at most three fixes a week, a person applies them in a reviewed commit.")
    s.card()
    header(s, "Mac Studio Prepared", "Weekly review",
           "Code measures every call, the coach proposes, and a person approves any change.")
    nodes = [
        (40, "Code measures", ["Latency on every call,", "fallback ladder, the", "bake off, calibration."], False, False),
        (325, "Coach proposes", ["Fridays 17:30. At most", "three fixes, every", "number checked by code."], False, True),
        (610, "A person applies", ["In a reviewed commit,", "by name. Or says no.", "Nothing changes itself."], True, False),
    ]
    for x, h, rows, human, loop in nodes:
        s.node(x, 150, 230, 112, h, rows, human=human, loop=loop)
    s.arrow(272, 206, 323, 206, INK)
    s.arrow(557, 206, 608, 206, INK)
    s.path_arrow("M725,264 L725,300 L155,300 L155,266", BLUE, 1.6)
    s.text(440, 322, "Next week runs on what was approved.", 13, 600, BLUE, anchor="middle")
    s.text(40, 362, "Calibration: a model that says 0.95 but is right 73 times in 100 is mapped to about 0.73,", 12.5, 400, MUTED)
    s.text(40, 382, "so the gate sends that headline to a second read instead of acting on it.", 12.5, 400, MUTED)
    return s.save(out("mac-studio-prepared", "learning.svg"))


def msp_seat():
    H = 560
    s = SVG(W, H, "How one seat files a report",
            "Code computes every number, a local model writes a few sentences, code checks each number, an unsupported one bounces once, then the inbox and a person.")
    s.card()
    header(s, "Mac Studio Prepared", "How a seat files a report",
           "The same five steps for all 94 reports, from the rates note to the risk report.")
    steps = [
        ("Pull", "code", ["Only the data the seat is cleared", "for: PUBLIC, INTERNAL or RESTRICTED."], False, False),
        ("Compute", "code", ["Every figure: curve, spreads, VaR, P&L,", "estimates. Units and windows stated."], False, False),
        ("Write", "local model", ["A few sentences on top of the numbers.", "No arithmetic. No advice language."], False, False),
        ("Check", "code", ["Every number traced to the item. One that", "is not there sends the draft back once."], False, True),
        ("Inbox", "a person", ["Read, approve, edit or reject. The verdict", "feeds the credibility scoreboard."], True, False),
    ]
    top, bh, gap = 150, 64, 12
    for i, (h, who_, rows, human, loop) in enumerate(steps):
        y = top + i * (bh + gap)
        fill = INK if human else (BLUE_FILL if loop else FILL)
        stroke = INK if human else (BLUE if loop else LINE)
        hc = "#FFFFFF" if human else (BLUE if loop else INK)
        rc = "#C9D3E0" if human else (INK if loop else MUTED)
        s.rect(40, y, 720, bh, fill, stroke)
        s.text(58, y + 28, f"{i+1:02d}", 12, 700, "#9FB0C4" if human else FAINT, spacing=1)
        s.text(86, y + 28, h, 16, 700, hc)
        s.text(58, y + 48, who_, 12.5, 400, rc)
        s.lines(230, y + 27, rows, 13, gap=19, color="#FFFFFF" if human else (INK if loop else INK))
        if i < len(steps) - 1:
            s.arrow(100, y + bh + 1, 100, y + bh + gap - 1, INK, 1.3)
    y3 = top + 3 * (bh + gap) + bh / 2
    y2 = top + 2 * (bh + gap) + bh / 2
    s.path_arrow(f"M760,{y3} L800,{y3} L800,{y2} L763,{y2}", BLUE, 1.6)
    s.text(812, (y2 + y3) / 2 + 4, "once", 12, 700, BLUE)
    s.text(40, H - 22, "A second unsupported number goes to a person, flagged. A model never grades its own draft.", 12.5, 400, MUTED)
    return s.save(out("mac-studio-prepared", "seat.svg"))


def msp_company():
    H = 752
    s = SVG(W, H, "How work moves through the desk",
            "The desk's 120 seats in the groups its own app draws: command, intake, data, the research floor, risk and quant, compliance, reports and clients, the investment team, operations, and the seats alongside.")
    s.card()
    header(s, "Mac Studio Prepared", "How work moves through the desk",
           "120 seats, grouped the way the desk's own app draws them. Numbers are seats.")
    def box(x, y, wd, ht, num, head, count, rows, human=False):
        s.rect(x, y, wd, ht, HUMAN if human else FILL, HUMAN if human else LINE)
        hc = "#FFFFFF" if human else INK
        rc = "#C9D3E0" if human else MUTED
        s.text(x + 12, y + 24, str(num), 12, 700, "#9FB0C4" if human else FAINT)
        s.text(x + 28, y + 24, head, 14, 700, hc)
        if count:
            s.text(x + wd - 12, y + 24, str(count), 14, 700, "#9FB0C4" if human else FAINT, anchor="end")
        s.lines(x + 12, y + 46, rows, 12.2, gap=17, color=rc)
    # 1 command across the top
    s.rect(40, 126, 800, 52, FILL, INK, sw=1.2)
    s.text(52, 150, "1", 12, 700, FAINT)
    s.text(68, 150, "Command", 14, 700)
    s.text(828, 150, "5", 14, 700, FAINT, anchor="end")
    s.text(68, 168, "The head of the floor routes every task to the seat that owns it. Staff: chief of staff, devil's advocate, scorekeeper, costs.", 12.2, 400, MUTED)
    A, B, C, D = (40, 180), (234, 226), (474, 196), (684, 156)
    top = 222
    # distribution line from command to the columns
    s.line(440, 178, 440, 196, INK, 1.2)
    s.line(A[0] + A[1] / 2, 196, C[0] + C[1] / 2, 196, INK, 1.2)
    for x0, wd in (A, B, C):
        s.arrow(x0 + wd / 2, 196, x0 + wd / 2, top - 2, INK)
    s.arrow(D[0] + D[1] / 2, 178, D[0] + D[1] / 2, top - 2, INK)
    s.text(D[0] + D[1] / 2 + 6, 205, "reports", 11, 400, FAINT)
    # column A: what comes in
    box(A[0], top, A[1], 172, 2, "Intake and watch", 8, ["News, filings, mail", "and calls, screened", "as they arrive.", "Sanctions and the", "security watch."])
    box(A[0], top + 200, A[1], 172, 3, "Data team", 4, ["Whole public files,", "checked and dated.", "Licences, quality", "and the model", "scout."])
    # column B: the research floor
    bx, bw = B
    s.rect(bx, top, bw, 372, FILL, INK, sw=1.2)
    s.text(bx + 12, top + 24, "4", 12, 700, FAINT)
    s.text(bx + 28, top + 24, "Research floor", 14, 700)
    s.text(bx + bw - 12, top + 24, "61", 14, 700, FAINT, anchor="end")
    s.lines(bx + 12, top + 46, ["The analyst leads. Each", "note is checked before", "it leaves the floor."], 12.2, gap=17, color=MUTED)
    pits = [("Markets pit", 17, "macro, rates, FX, energy"), ("Companies pit", 18, "banks, tech, biotech, legal"),
            ("Third pit", 18, "M&A, credit, Asia, Europe"), ("On the glass", 8, "checker, grid, shipping")]
    for i, (name, n, desc) in enumerate(pits):
        y = top + 104 + i * 66
        s.rect(bx + 12, y, bw - 24, 54, SHADE, "#D5DBE3")
        s.text(bx + 24, y + 22, name, 13, 700)
        s.text(bx + bw - 24, y + 22, str(n), 13, 700, FAINT, anchor="end")
        s.text(bx + 24, y + 41, desc, 11.8, 400, MUTED)
    # arrows A -> B
    for y in (top + 86, top + 286):
        s.arrow(A[0] + A[1] + 1, y, bx - 2, y, INK)
    # column C: checked notes go three ways
    cx, cw = C
    cy = [top, top + 132, top + 264]
    box(cx, cy[0], cw, 108, 5, "Risk and quant", 7, ["Estimates, backtests,", "risk and the paper book."])
    box(cx, cy[1], cw, 108, 6, "Compliance", 9, ["Filings, controls and", "the restricted list."])
    box(cx, cy[2], cw, 108, 7, "Reports, clients", 9, ["Reports, client replies", "and investor letters."])
    s.line(bx + bw + 1, top + 186, bx + bw + 9, top + 186, INK, 1.2)
    s.line(bx + bw + 9, cy[0] + 54, bx + bw + 9, cy[2] + 54, INK, 1.2)
    for y in cy:
        s.arrow(bx + bw + 9, y + 54, cx - 2, y + 54, INK)
    # column D: people, then operations
    dx, dw = D
    box(dx, top, dw, 160, 8, "Investment team", "", ["PM, CIO, risk and", "compliance approve,", "send and trade.", "Nobody else can."], human=True)
    box(dx, top + 212, dw, 160, 9, "Operations", 7, ["After the trade:", "reconciled,", "explained, cash", "and tax."])
    s.line(cx + cw + 1, cy[0] + 54, cx + cw + 9, cy[0] + 54, INK, 1.2)
    s.line(cx + cw + 1, cy[1] + 54, cx + cw + 9, cy[1] + 54, INK, 1.2)
    s.line(cx + cw + 1, cy[2] + 54, cx + cw + 9, cy[2] + 54, INK, 1.2)
    s.line(cx + cw + 9, cy[0] + 54, cx + cw + 9, cy[2] + 54, INK, 1.2)
    s.arrow(cx + cw + 9, top + 80, dx - 2, top + 80, INK)
    s.arrow(dx + dw / 2, top + 162, dx + dw / 2, top + 210, INK)
    s.text(dx + dw / 2 + 6, top + 190, "trades", 11, 400, FAINT)
    s.path_arrow(f"M{dx+dw},{top+292} L{dx+dw+14},{top+292} L{dx+dw+14},{top+120} L{dx+dw+3},{top+120}", BLUE, 1.5)
    # 10: alongside
    yb = top + 400
    s.rect(40, yb, 800, 72, FILL, LINE)
    s.text(52, yb + 24, "10", 12, 700, FAINT)
    s.text(74, yb + 24, "Alongside", 14, 700)
    s.text(74, yb + 44, "Lab and coach (3) test models and propose fixes. Public windows (2) are the only route to the cloud,", 12.2, 400, MUTED)
    s.text(74, yb + 62, "for public data only. The studio (5) drafts public media. Everything here is a draft or a proposal.", 12.2, 400, MUTED)
    s.source("Source: Mac Studio Prepared floor plan, November 2026. 109 agents and 11 always on engines. Blue: work that needs a person goes back.")
    return s.save(out("mac-studio-prepared", "company.svg"))


def lib_flow():
    steps = [
        ("Question", "you", "In plain words. Optional: a subject, like banking, or the books to use."),
        ("Find the books", "code", "Subject search on Project Gutenberg. The Internet Archive as a backup."),
        ("Public domain only", "code", "Gutenberg's own flag, or published in 1930 or earlier for the Archive."),
        ("Pull them", "code", "One book at a time, two seconds apart, cached here, never redistributed."),
        ("Read every paragraph", "code", "Header and licence removed. Each paragraph numbered, with its chapter."),
        ("Rank", "code", "BM25 over every paragraph. The six that best answer the question."),
        ("Answer", "local model", "From those six passages only, every sentence cited."),
        ("Check the citations", "code", "A citation that does not exist, or a sentence without one, fails the answer."),
    ]
    top, rh = 150, 50
    H = top + len(steps) * rh + 44
    s = SVG(W, H, "How the Library Agent answers a question",
            "Eight steps from a question to an answer with book, chapter and paragraph citations, checked in code.")
    s.card()
    header(s, "The Library Agent", "From a question to a cited answer",
           "Public domain books only. Everything runs on this machine.")
    for i, (name, who_, note) in enumerate(steps):
        y = top + i * rh
        last = i == len(steps) - 1
        s.rect(40, y + 4, W - 80, rh - 8, FILL, BLUE if last else LINE, sw=1.5 if last else 1)
        s.text(56, y + 30, str(i + 1), 12, 700, FAINT)
        s.text(78, y + 30, name, 14, 700, BLUE if last else INK)
        s.text(270, y + 30, who_, 12.5, 400, MUTED)
        s.text(370, y + 30, note, 12.4, 400, INK)
    s.source("Sources: Project Gutenberg through the Gutendex catalog, and the Internet Archive's advanced search.")
    return s.save(out("library-agent", "flow.svg"))


def echo_flow():
    top, rh = 150, 50
    steps = [
        ("Sources", "you", "YouTube, podcasts, live TV, PDFs, articles and earnings calls."),
        ("Pull", "code", "Downloads the media or the text. Articles are stripped to readable text."),
        ("Transcribe", "local model", "whisper.cpp on this Mac. No per hour cost and nothing uploaded."),
        ("Speaker turns", "local model", "A second pass marks where the speaker changes."),
        ("Store", "code", "SQLite with full text search. The database never leaves the machine."),
        ("Search and read", "you", "Search everything at once, or open a transcript that jumps to the moment."),
    ]
    H = top + len(steps) * rh + 104
    s = SVG(W, H, "How Project Echo works",
            "From sources to a searchable, speaker-labelled library of transcripts on your own machine, with briefs as the next phase.")
    s.card()
    header(s, "Project Echo", "From a podcast or an earnings call to searchable text",
           "A local research tool for investors. Code is shared; your data and keys stay on your machine.")
    for i, (name, who_, note) in enumerate(steps):
        y = top + i * rh
        human = who_ == "you"
        s.rect(40, y + 4, W - 80, rh - 8, HUMAN if human else FILL, HUMAN if human else LINE)
        s.text(56, y + 30, str(i + 1), 12, 700, "#9FB0C4" if human else FAINT)
        s.text(78, y + 30, name, 14, 700, "#FFFFFF" if human else INK)
        s.text(250, y + 30, who_, 12.5, 400, "#C9D3E0" if human else MUTED)
        s.text(370, y + 30, note, 12.2, 400, "#FFFFFF" if human else INK)
    y = top + len(steps) * rh + 10
    s.rect(40, y, W - 80, 48, SHADE, "#D5DBE3")
    s.text(56, y + 20, "Next phase", 13.5, 700)
    s.text(56, y + 38, "Briefs and unanswered questions from each call, written by a local model from the transcript. Not built yet.", 12.2, 400, MUTED)
    s.source("Built for my brother. Speed: an 80 minute podcast transcribes in about six minutes on an M2 Max.")
    return s.save(out("project-echo", "flow.svg"))


if __name__ == "__main__":
    for f in (le_loops, how_i_build, cf_loop, cf_day, jb_funnel, jb_form, cs_morning,
              msp_morning, msp_event, msp_strategy, msp_wall, msp_learning, msp_seat, lib_flow, echo_flow):
        print(f())
