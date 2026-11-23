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
    ("04:15", "Risk report", "VaR, stress tests, limits, exposures, liquidity. An optimizer proposal inside the same limits."),
    ("04:30", "Thesis monitor", "Every new filing and call checked against each thesis's own sell if rules."),
    ("05:00", "Morning brief", "Positions, watchlist, overnight news through the impact map. Checked, then filed."),
    ("06:22", "Morning call", "The early read, held until risk, the books, NAV and the P&L explanation are in."),
    ("06:30", "Middle office", "Corporate actions, three way reconciliation, cash ladder, P&L attribution, NAV check."),
    ("06:55", "Ops and compliance", "One page for the COO and CCO: breaks, payee changes, pre-clearance, MNPI flags."),
    ("06:58", "Ready to open?", "Eight checks in code. One answer: yes, or no with what is missing and who acts."),
    ("07:30", "PM meeting", "The PM reads the late edition and decides. People trade. Agents never do."),
]


def msp_morning():
    top, rh = 150, 54
    H = top + len(MSP_MORNING) * rh + 30
    s = SVG(W, H, "The trading morning",
            "From the 03:15 integrity check to the 07:30 PM meeting, with the 06:58 ready to open gate.")
    s.card()
    header(s, "The trading morning", "Ready to open by 06:58",
           "Every weekday, New York time. Agents read and draft. Code checks. People decide.")
    for i, (t, name, note) in enumerate(MSP_MORNING):
        y = top + i * rh
        human = name == "PM meeting"
        gate = name == "Ready to open?"
        if human or gate:
            s.rect(40, y + 2, W - 80, rh - 8, INK if human else BLUE_FILL, INK if human else BLUE, rx=8)
        c1 = "#FFFFFF" if human else (BLUE if gate else INK)
        c2 = "#D9D9D4" if human else ("#22336B" if gate else MUTED)
        s.text(58, y + 30, t, 14, 700, "#A9A9A4" if human else FAINT)
        s.text(130, y + 30, name, 15, 700, c1)
        s.text(310, y + 30, note, 12.8, 400, c2)
        if not (human or gate) and i < len(MSP_MORNING) - 1 and MSP_MORNING[i + 1][1] != "Ready to open?":
            s.line(58, y + rh - 3, W - 58, y + rh - 3, "#E6E6E2", 1)
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
    header(s, "Workflow: event alert", "A headline to a checked brief in about 3 minutes",
           "The newswire is read every 30 seconds. The data class only ever goes up.")
    for x, h in ((58, "Step"), (230, "Who"), (360, "Data class"), (490, "What happens")):
        s.kicker(x, 160, h)
    for i, (name, who, cls, note) in enumerate(steps):
        y = top + i * rh
        last = i == len(steps) - 1
        s.rect(40, y + 4, W - 80, rh - 8, INK if last else FILL, INK if last else LINE, rx=8)
        c1 = "#FFFFFF" if last else INK
        c2 = "#D9D9D4" if last else MUTED
        s.text(58, y + 30, f"{i+1}  {name}", 14, 700, c1)
        s.text(230, y + 30, who, 13, 400, c2)
        shade = {"PUBLIC": "#FFFFFF", "INTERNAL": "#E9E9E5", "RESTRICTED": "#CFCFCB"}[cls]
        if not last:
            s.rect(360, y + 15, 100, 22, shade, "#BDBDB8", rx=5)
            s.text(410, y + 30, cls, 10.5, 700, INK, anchor="middle", spacing=0.8)
        else:
            s.text(360, y + 30, cls, 10.5, 700, "#D9D9D4", spacing=0.8)
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
    header(s, "Workflow: strategy validation", "Is the Sharpe real?",
           "An idea earns a paper book only after the tests that kill most ideas.")
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
    s.text(140, y + 90, "Sharpe +1.62, standard error 0.81, 391 sessions, 6 trials, deflated Sharpe 0.52 against a", 13, 400)
    s.text(140, y + 110, "line of 0.95. Same number, honest context: not good enough yet.", 13, 400)
    return s.save(out("mac-studio-prepared", "strategy.svg"))


def msp_wall():
    H = 520
    s = SVG(W, H, "The privacy wall",
            "Private zone on four Mac Studios with local open weight models; one public route out to cloud models for public data only, enforced three times.")
    s.card()
    header(s, "Guardrails", "Private data never leaves the building",
           "The same rule is enforced three times, and tested every night.")
    # private zone
    s.rect(40, 140, 560, 330, "#FFFFFF", INK, rx=12, sw=1.4)
    s.kicker(60, 168, "Private zone: four Mac Studios")
    macs = [("Studio 1", "Watcher + services", "fast reads, alerts"), ("Studio 2", "Analyst", "every brief"),
            ("Studio 3", "Checker", "numbers, speech, vision"), ("Studio 4", "Lab", "candidate models")]
    for i, (a, b, c) in enumerate(macs):
        x = 60 + (i % 2) * 265
        y = 186 + (i // 2) * 84
        s.rect(x, y, 250, 70, "#F7F7F4", LINE, rx=8)
        s.text(x + 14, y + 26, a, 12, 700, FAINT, spacing=1)
        s.text(x + 14, y + 47, b, 14, 700)
        s.text(x + 14, y + 63, c, 12, 400, MUTED)
    s.text(60, 386, "Positions, theses, client data, expert calls, broker research.", 12.5, 400, MUTED)
    s.text(60, 406, "Open weight models only. No meter, no outside copy.", 12.5, 400, MUTED)
    s.rect(60, 422, 520, 32, INK, INK, rx=7)
    s.text(320, 443, "Everything lands in one inbox. A person approves.", 13, 700, "#FFFFFF", anchor="middle")
    # cloud
    s.rect(660, 200, 180, 120, "#F7F7F4", LINE, rx=12)
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
    header(s, "The learning loop", "The agent proposes. Code measures. A person changes it.",
           "That is the only safe shape for a system that improves itself.")
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
    header(s, "How a seat works", "Code does the math. The model writes. Code checks.",
           "The same five steps for every one of the 94 reports, from the rates note to the risk report.")
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
        rc = "#D9D9D4" if human else ("#22336B" if loop else MUTED)
        s.rect(40, y, 720, bh, fill, stroke)
        s.text(58, y + 28, f"{i+1:02d}", 12, 700, "#A9A9A4" if human else FAINT, spacing=1)
        s.text(86, y + 28, h, 16, 700, hc)
        s.text(58, y + 48, who_, 12.5, 400, rc)
        s.lines(230, y + 27, rows, 13, gap=19, color="#FFFFFF" if human else ("#22336B" if loop else INK))
        if i < len(steps) - 1:
            s.arrow(100, y + bh + 1, 100, y + bh + gap - 1, INK, 1.3)
    y3 = top + 3 * (bh + gap) + bh / 2
    y2 = top + 2 * (bh + gap) + bh / 2
    s.path_arrow(f"M760,{y3} L800,{y3} L800,{y2} L763,{y2}", BLUE, 1.6)
    s.text(812, (y2 + y3) / 2 + 4, "once", 12, 700, BLUE)
    s.text(40, H - 22, "A second unsupported number goes to a person, flagged. A model never grades its own draft.", 12.5, 400, MUTED)
    return s.save(out("mac-studio-prepared", "seat.svg"))


if __name__ == "__main__":
    for f in (hero, how_i_build, cf_loop, cf_day, jb_funnel, jb_form, cs_morning,
              msp_firm, msp_morning, msp_event, msp_strategy, msp_wall, msp_learning, msp_seat):
        print(f())
