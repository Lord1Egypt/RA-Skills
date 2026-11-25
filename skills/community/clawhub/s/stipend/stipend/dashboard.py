"""A dashboard that stays on your machine.

The obvious product move here is a hosted dashboard: sign in at stipend.sh, see
your agent's P&L. We are not doing that, because it would mean holding a record
of what every customer earns and spends — and the whole argument for this kit is
that we hold nothing. A login page would quietly make that false.

So the dashboard is a file. `stipend report --html` reads the local ledger,
writes one self-contained page, and opens it. No server, no account, no request
leaves the machine. Charts are hand-drawn SVG rather than a charting library,
because pulling a CDN script into a page about your finances would reintroduce
exactly the outbound call we just avoided.

    stipend report --html
    stipend report --html --days 30 --output ~/agent-pnl.html
"""

import html
import os
import webbrowser
from datetime import datetime, timezone

from .config import CONFIG_DIR

DEFAULT_OUTPUT = CONFIG_DIR / "report.html"

CSS = """
table.refused{width:100%;border-collapse:collapse;font-size:15.5px;margin-bottom:10px}
table.refused th{text-align:left;color:#95a0ac;font-weight:600;padding:6px 10px 6px 0;
  border-bottom:1px solid #232a33}
table.refused td{padding:7px 10px 7px 0;border-bottom:1px solid #1a1f26;vertical-align:top}
table.refused td.t{color:#737f8d;white-space:nowrap}
table.refused td.a{color:#e0b874;white-space:nowrap}
table.refused td.w{color:#95a0ac}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0b0d10; --panel:#12161b; --line:#232a33;
  --fg:#d7dde5; --dim:#95a0ac; --faint:#737f8d;
  --good:#74e0a0; --warn:#e0b874; --bad:#e08a74;
}
body{background:var(--bg);color:var(--fg);
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:840px;margin:0 auto;padding:44px 22px 80px}
h1{font-size:25px;font-weight:600;letter-spacing:-.01em;margin-bottom:6px}
.sub{color:var(--faint);font-size:15.5px;margin-bottom:6px;
  display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.sub .who{color:var(--dim);letter-spacing:.06em;text-transform:uppercase;
  font-size:12px}
.sub .dot{color:#2b333d}
.addr{color:var(--fg);font-size:14.5px;letter-spacing:.01em;
  background:var(--panel);border:1px solid var(--line);border-radius:5px;
  padding:3px 8px;word-break:break-all}
.hint{color:var(--faint);font-size:14px;margin-bottom:26px;max-width:70ch}
/* One click selects the whole thing, then ctrl-c.
   A copy button needs JavaScript, and this page deliberately has none — it is
   generated from somebody's finances and being provably inert is worth more
   than a button. The first attempt added one anyway, and it did not even work:
   navigator.clipboard does not exist on a file:// page, which is the only way
   this page is ever opened. user-select:all costs nothing and cannot fail. */
.addr,.share code{user-select:all;-webkit-user-select:all;cursor:pointer}
.share{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:8px 0 4px}
.share code{background:var(--panel);border:1px solid var(--line);
  border-radius:5px;padding:4px 9px;font-size:14px;color:var(--fg);
  word-break:break-all}
.summary{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--good);
  border-radius:8px;padding:18px 20px;margin-bottom:26px;font-size:19px}
.summary.warn{border-left-color:var(--warn)}
.summary.bad{border-left-color:var(--bad)}
h2{font-size:14.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  color:var(--dim);margin:34px 0 14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px}
.tile .label{color:var(--dim);font-size:14px;letter-spacing:.08em;text-transform:uppercase}
.tile .value{font-size:29px;font-weight:600;margin-top:6px;letter-spacing:-.02em}
.tile .note{color:var(--faint);font-size:14.5px;margin-top:4px}
.good{color:var(--good)} .warn{color:var(--warn)} .bad{color:var(--bad)} .dim{color:var(--dim)}
table{width:100%;border-collapse:collapse;font-size:16px;margin-top:4px}
th,td{text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--line)}
th{color:var(--dim);font-weight:600;font-size:14px;letter-spacing:.08em;text-transform:uppercase}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.bar{height:6px;background:var(--line);border-radius:3px;overflow:hidden;margin-top:5px}
.bar span{display:block;height:100%;background:var(--good);border-radius:3px}
.empty{color:var(--faint);padding:22px 0;font-size:17px}
footer{margin-top:46px;padding-top:20px;border-top:1px solid var(--line);
  color:var(--faint);font-size:15px}
svg{display:block;max-width:100%;height:auto}
.axis{fill:var(--faint);font-size:12px}
@media(max-width:560px){.wrap{padding:28px 16px 60px}.tile .value{font-size:24px}}
"""


def _money(v):
    return "$%.2f" % (v or 0)


def _spark(rows, days, width=780, height=110):
    """Daily net, drawn by hand. No chart library, so no outbound request."""
    if not rows:
        return ""
    buckets = {}
    for e in rows:
        try:
            day = e["at"][:10]
        except (KeyError, TypeError):
            continue
        delta = e["amount_usdc"] if e["direction"] == "in" else -e["amount_usdc"]
        buckets[day] = buckets.get(day, 0.0) + delta
    if not buckets:
        return ""

    keys = sorted(buckets)
    vals = [buckets[k] for k in keys]
    lo, hi = min(vals + [0.0]), max(vals + [0.0])
    span = (hi - lo) or 1.0
    pad = 26
    usable = width - pad * 2
    step = usable / max(1, len(vals))
    zero_y = height - pad - ((0 - lo) / span) * (height - pad * 2)

    bars = []
    for i, v in enumerate(vals):
        x = pad + i * step
        y = height - pad - ((v - lo) / span) * (height - pad * 2)
        top, h = (min(y, zero_y), abs(y - zero_y) or 1)
        colour = "var(--good)" if v >= 0 else "var(--bad)"
        bars.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" rx="1">'
            "<title>%s  %s</title></rect>"
            % (x, top, max(2.0, step * 0.62), h, colour, html.escape(keys[i]), _money(v))
        )

    return (
        '<svg viewBox="0 0 %d %d" role="img" aria-label="daily net by day">'
        '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--line)"/>'
        '%s<text class="axis" x="%d" y="%d">%s</text>'
        '<text class="axis" x="%d" y="%d" text-anchor="end">%s</text></svg>'
        % (width, height, pad, zero_y, width - pad, zero_y, "".join(bars),
           pad, height - 6, html.escape(keys[0]),
           width - pad, height - 6, html.escape(keys[-1]))
    )


REFUSAL_LABELS = {
    "over_per_transaction": "over the per-transaction cap",
    "over_daily":           "over the daily limit",
    "needs_confirmation":   "needed your confirmation",
    "new_destination":      "first payment to a new address",
    "allowlist":            "destination not on the allowlist",
}


def _refusals_panel(refused):
    """Every time the limits stopped a payment.

    This is the only place the product's central claim leaves evidence. A human
    who paid for "limits it cannot talk its way past" has otherwise no way to
    see them work — the successful payments look identical either way.
    """
    if not refused:
        return ('<div class="empty">Nothing was refused in this window. '
                'The limits are on; nothing has tested them yet.</div>')

    rows = []
    for r in refused[:40]:
        when = str(r.get("at", ""))[:16].replace("T", " ")
        amount = r.get("amount_usdc")
        amount = _money(amount) if amount is not None else "&mdash;"
        to = str(r.get("to") or "")
        # A literal ellipsis, not the entity: this string is escaped below, so
        # "&hellip;" would come out as visible "&amp;hellip;".
        short = (to[:10] + "…" + to[-6:]) if len(to) > 20 else to
        label = REFUSAL_LABELS.get(r.get("kind"), str(r.get("kind") or "refused"))
        rows.append(
            "<tr><td class=\"t\">%s</td><td class=\"a\">%s</td>"
            "<td>%s</td><td class=\"w\">%s</td></tr>"
            % (html.escape(when), amount, html.escape(short), html.escape(label)))

    return ('<table class="refused"><tr><th>when</th><th>amount</th>'
            '<th>to</th><th>why it was stopped</th></tr>%s</table>'
            '<div class="note">These are payments your agent tried to make and '
            'could not. Nothing it read could raise these limits — they are '
            'checked after it decides and before anything is signed.</div>'
            % "".join(rows))


def _affiliate_panel(aff):
    """What the referral programme has actually done for this wallet.

    Deliberately blunt about zero. An affiliate panel that shows an encouraging
    empty state is a recruitment poster, and the one thing we promise never to
    do is imply somebody will earn. If nothing has happened, it says nothing has
    happened.
    """
    if not aff:
        return ('<div class="empty">No referral data. Either this wallet has no '
                'code yet, or the lookup could not reach stipend.sh.</div>')
    if aff.get("error"):
        return '<div class="empty">Could not load: %s</div>' % html.escape(str(aff["error"])[:120])

    sales = int(aff.get("sales_referred") or 0)
    earned = float(aff.get("earned_usd") or 0)
    paid = float(aff.get("paid_usd") or 0)
    owed = float(aff.get("owed_usd") or 0)
    reversed_usd = float(aff.get("reversed_usd") or 0)

    tiles = [
        ("Sales referred", str(sales), "all time"),
        ("Earned", _money(earned), "20% of each sale"),
        ("Paid out", _money(paid), "taken as credits"),
        ("Owed to you", _money(owed), "waiting to be claimed"),
    ]
    body = "".join(
        '<div class="tile"><div class="label">%s</div><div class="value">%s</div>'
        '<div class="note">%s</div></div>' % (html.escape(a), html.escape(b), html.escape(c))
        for a, b, c in tiles)

    extra = ""
    if reversed_usd:
        extra += ('<p class="note">%s was reversed — a refunded sale is not a '
                  'sale.</p>' % html.escape(_money(reversed_usd)))
    if owed > 0:
        extra += ('<p class="note">Claim it with <code>stipend affiliate payout'
                  '</code>. It arrives as gas credits.</p>')
    # The empty state used to open with "this is not a business and we do not
    # suggest treating it as one", which is a strange thing to print for
    # somebody who has just paid. Nothing here is oversold: 20% is 20%, and it
    # is still nothing if nobody buys. But the useful half is the link and what
    # to do with it, so lead with that instead of with a disclaimer.
    if aff.get("share_url"):
        url = html.escape(str(aff["share_url"]))
        extra += (
            '<p class="note">Your link — anyone who buys through it pays the '
            'same $39, and 20%% of it comes back to you as gas credits, for '
            'every sale, for as long as they keep buying.</p>'
            '<div class="share"><code id="reflink">%s</code>'
            '</div>'
            % url)
        if not sales:
            extra += ('<p class="note">It works already — there is nothing to '
                      'sign up for. The people most likely to use it are the '
                      'ones who asked you what your agent costs to run.</p>')
    elif not sales:
        extra += ('<p class="note">Join with <code>stipend affiliate join</code> '
                  'to get a link. 20% of every sale it brings in, paid as gas '
                  'credits.</p>')
    return '<div class="tiles">%s</div>%s' % (body, extra)


LEVELS = {
    1: ("Knocked", "you signed something at the door"),
    2: ("Holds gas credits", "you bought or were granted credits"),
    3: ("Referred a buyer", "somebody bought because of you"),
    4: ("Paid by a stranger", "money arrived from somebody who is not us"),
    5: ("Covering its costs", "thirty days of taking in more than it sent out"),
}


def _lounge_panel(standing):
    """Which levels this agent has actually proven.

    Levels are not claimed, they are read — one to three from ledgers, four and
    five off Base itself. So this is the one panel on the page that says
    something about the agent that the agent did not say about itself.
    """
    if not standing:
        return ('<div class="empty">This agent has not knocked. '
                '<code>stipend lounge knock</code> — it costs nothing and needs '
                'no account.</div>')

    try:
        level = int(standing.get("level") or 0)
    except (TypeError, ValueError):
        level = 0

    rows = []
    for n in sorted(LEVELS):
        name, why = LEVELS[n]
        got = n <= level
        rows.append(
            '<tr><td>%s</td><td>%s</td><td>%s</td><td class="%s">%s</td></tr>'
            % (n, html.escape(name), html.escape(why),
               "good" if got else "dim",
               "reached" if got else "not yet"))

    note = ""
    if level >= 4:
        note = ('<p class="note">Levels four and five are read off Base and '
                'cannot be claimed — this one was earned.</p>')
    elif level:
        note = ('<p class="note">Four and five are read off Base in the '
                'background, so a level just earned can take a few hours to '
                'appear here.</p>')
    return ('<table><tr><th>#</th><th>Level</th><th>What it means</th>'
            '<th>Standing</th></tr>%s</table>%s' % ("".join(rows), note))


def _lifetime_line(payload):
    """One line: has this agent ever been worth it.

    Every other figure on the page is windowed, so none of them answers the
    question somebody asks before switching an agent off.
    """
    lt = payload.get("lifetime") or {}
    if not lt.get("transactions"):
        return ""
    net = lt.get("net_usdc") or 0
    tone = "good" if net >= 0 else "bad"
    since = lt.get("since")
    return ('<p class="hint">Since %s, all time: earned %s, spent %s, '
            '<span class="%s">%s %s</span> across %d transactions.</p>'
            % (html.escape(str(since or "the beginning")),
               _money(lt.get("earned_usdc")), _money(lt.get("spent_usdc")),
               tone, "up" if net >= 0 else "down", _money(abs(net)),
               lt.get("transactions", 0)))


def render(payload, entries, days, address=None, balance=None, version="",
           refused=None, affiliate=None, lounge=None):
    """Build the page. Takes data already computed by ledger.report()."""
    pnl = payload.get("profit_and_loss", {}) or {}
    run = payload.get("runway", {}) or {}
    goal = (payload.get("goal") or {}).get("goal")
    goal_info = payload.get("goal") or {}

    status = run.get("status") or "ok"
    tone = {"critical": "bad", "low": "warn"}.get(status, "")
    net = pnl.get("net_usdc", 0) or 0
    recovery = pnl.get("cost_recovery_percent")

    tiles = [
        ("Earned", _money(pnl.get("earned_usdc")), "good", "%d days" % days),
        ("Spent", _money(pnl.get("spent_usdc")), "dim", "%d transactions" % (pnl.get("transactions") or 0)),
        ("Net", _money(net), "good" if net >= 0 else "bad",
         "profitable" if net >= 0 else "running at a loss"),
        ("Balance", _money(balance) if balance is not None else "—", "dim", "USDC on hand"),
    ]
    if run.get("days_remaining") is not None:
        tiles.append(("Runway", "%s days" % run["days_remaining"],
                      {"critical": "bad", "low": "warn"}.get(status, "good"),
                      "at %s/day" % _money(run.get("daily_burn_usdc"))))

    tile_html = "".join(
        '<div class="tile"><div class="label">%s</div>'
        '<div class="value %s">%s</div><div class="note">%s</div></div>'
        % (html.escape(l), c, html.escape(str(v)), html.escape(str(n)))
        for l, v, c, n in tiles
    )

    by_cat = pnl.get("spend_by_category") or {}
    if by_cat:
        top = max(by_cat.values()) or 1
        rows = "".join(
            '<tr><td>%s<div class="bar"><span style="width:%.1f%%"></span></div></td>'
            '<td class="num">%s</td></tr>'
            % (html.escape(str(k)), (v / top) * 100, _money(v))
            for k, v in sorted(by_cat.items(), key=lambda kv: -kv[1])
        )
        cats = "<table><tr><th>Category</th><th class='num'>Spent</th></tr>%s</table>" % rows
    else:
        cats = '<div class="empty">Nothing spent yet in this window.</div>'

    recent = ""
    if entries:
        rows = "".join(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td class='num %s'>%s%s</td></tr>"
            % (html.escape((e.get("at") or "")[:16].replace("T", " ")),
               "in" if e["direction"] == "in" else "out",
               html.escape(str(e.get("note") or e.get("category") or "—"))[:60],
               "good" if e["direction"] == "in" else "",
               "+" if e["direction"] == "in" else "−",
               _money(e["amount_usdc"]))
            for e in list(reversed(entries))[:25]
        )
        recent = ("<table><tr><th>When</th><th>Dir</th><th>What</th>"
                  "<th class='num'>Amount</th></tr>%s</table>" % rows)
    else:
        recent = '<div class="empty">No transactions recorded yet.</div>'

    goal_block = ""
    if goal:
        pct = goal_info.get("percent")
        goal_block = (
            '<h2>Goal</h2><div class="tile"><div class="label">%s</div>'
            '<div class="value">%s</div>'
            '<div class="bar"><span style="width:%.1f%%"></span></div>'
            '<div class="note">%s</div></div>'
            % (html.escape(str(goal.get("kind", "goal"))),
               html.escape(str(goal_info.get("message", ""))[:90]),
               max(0.0, min(100.0, float(pct or 0))),
               html.escape("%.1f%% there" % float(pct or 0)) if pct is not None else "")
        )

    recovery_note = ""
    if recovery is not None and (pnl.get("spent_usdc") or 0) > 0:
        recovery_note = (
            '<h2>Cost recovery</h2><div class="tile">'
            '<div class="label">Earnings against running costs</div>'
            '<div class="value %s">%s%%</div>'
            '<div class="bar"><span style="width:%.1f%%"></span></div>'
            '<div class="note">%s</div></div>'
            % ("good" if recovery >= 100 else "warn" if recovery >= 50 else "bad",
               recovery, max(0.0, min(100.0, float(recovery))),
               "covering its own costs" if recovery >= 100 else "not yet covering its costs")
        )

    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>stipend — agent P&amp;L</title><style>%s</style></head>
<body><div class="wrap">
<h1>Agent profit &amp; loss</h1>
<!-- The address used to sit here on its own, unlabelled, and a reader had to
     work out what a 42-character hex string was doing at the top of their
     page. It is the one thing on here somebody might need to hand to another
     person, so it says what it is and can be copied without selecting it. -->
<div class="sub">
  <span class="who">Wallet</span>
  <code class="addr" id="addr">%s</code>
  <span class="dot">&middot;</span> last %d days
  <span class="dot">&middot;</span> generated %s
</div>
<p class="hint">That address is where anyone pays this agent. It is the same on
Base mainnet and on testnet, and it is safe to publish.</p>
<div class="summary %s">%s</div>
<h2>At a glance</h2><div class="tiles">%s</div>
%s
%s%s
<h2>Daily net</h2>%s
<h2>Where the money went</h2>%s
<h2>Stopped by the limits</h2>%s
<h2>Referrals</h2>%s
<h2>Standing in the lounge</h2>%s
<h2>Recent activity</h2>%s
<footer>
Generated on this machine by stipend%s. Every figure above except the referral
panel was read from your local ledger; nothing about your balances, payees or
transactions left this machine. The referral panel asked stipend.sh what your own
code has earned, which sends that code and nothing else. Delete this file
whenever you like.
</footer>
</div>
</body></html>""" % (
        CSS,
        html.escape(address or "no wallet"),
        days,
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        tone,
        html.escape(str(payload.get("summary", ""))),
        tile_html,
        _lifetime_line(payload),
        recovery_note,
        goal_block,
        _spark(entries, days) or '<div class="empty">Not enough history to chart yet.</div>',
        cats,
        _refusals_panel(refused or []),
        _affiliate_panel(affiliate),
        _lounge_panel(lounge),
        recent,
        (" " + html.escape(version)) if version else "",
    )


def write(payload, entries, days, address=None, balance=None,
          output=None, version="", open_browser=True, refused=None,
          affiliate=None, lounge=None):
    """Write the page and try to open it. Returns the path."""
    path = os.path.abspath(os.path.expanduser(output or str(DEFAULT_OUTPUT)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(payload, entries, days, address, balance, version,
                       refused, affiliate, lounge))
    try:
        os.chmod(path, 0o600)    # it is a financial record, not world-readable
    except (OSError, NotImplementedError):
        pass
    if open_browser:
        try:
            webbrowser.open("file://" + path.replace(os.sep, "/"))
        except Exception:
            pass    # headless box: the path in the output is enough
    return path
