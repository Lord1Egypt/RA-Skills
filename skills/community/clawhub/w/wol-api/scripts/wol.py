#!/usr/bin/env python3
"""WOL API client used by the wol-api agent skill.

Stdlib only. Handles credentials, base-URL pinning, confirmation of state-changing
calls, error mapping and output formatting, so the agent does not have to.

Security properties:
  * The API token is never printed, never passed on a command line and never
    written anywhere except the token file created by `set-token`.
  * Requests only go to an allowlisted base URL; redirects are never followed.
  * State-changing commands (order, register, unregister, seat) only preview
    unless --yes is given.
"""

import argparse
import getpass
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://wollan.nl"
ALLOWED_BASE_URLS = {"https://wollan.nl", "https://www.wollan.nl"}
# Local development hosts. Plain http is allowed only for these.
LOCAL_HOST_RE = re.compile(r"^https?://(localhost|127\.0\.0\.1)(:\d{1,5})?$")
TOKEN_RE = re.compile(r"^wol_[0-9a-f]{64}$")
TIMEOUT = 20

EXIT_OK = 0
EXIT_API_ERROR = 1
EXIT_CONFIG_ERROR = 2
EXIT_USAGE = 3

ORDER_STATUS = {
    "accepted": "received, being prepared",
    "waiting": "queued behind other orders",
    "ready": "READY for pick-up",
    "complete": "picked up / done",
    "cancelled": "cancelled, not fulfilled",
    "rejected": "rejected, not fulfilled",
}

ERROR_HINTS = {
    400: "The request was malformed. Check the command arguments.",
    401: "The API token is invalid, expired or revoked. The user must create a new token at "
         "{base}/user/api-tokens and store it with `set-token` (or WOL_API_TOKEN).",
    403: "The user is not registered for, or has not paid for, the active event. "
         "Registering and paying happens on the WOL website.",
    404: "Not found. Check the event/seat ID (run `events` to list events).",
    429: "Rate limit hit (60 requests/minute). Wait a minute before retrying; do not retry in a loop.",
    500: "Server error. Nothing the user can fix; tell them to contact the WOL crew/site admin.",
    502: "The WOL site is unreachable right now. Try again later.",
    503: "No active catering event is configured. Tell the user to contact the site admin.",
    504: "The WOL site timed out. Try again later.",
}


class WolError(Exception):
    def __init__(self, message, exit_code=EXIT_API_ERROR, hint=None):
        super().__init__(message)
        self.exit_code = exit_code
        self.hint = hint


# --------------------------------------------------------------------------- config

def config_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "wol")


def token_file():
    return os.path.join(config_dir(), "token")


def resolve_base_url():
    raw = os.environ.get("WOL_BASE_URL", "").strip()
    if not raw:
        return DEFAULT_BASE_URL, "default"
    url = raw.rstrip("/")
    if url in ALLOWED_BASE_URLS or LOCAL_HOST_RE.match(url):
        return url, "WOL_BASE_URL"
    raise WolError(
        "Refusing to send WOL credentials to untrusted base URL from WOL_BASE_URL.",
        EXIT_CONFIG_ERROR,
        "Unset WOL_BASE_URL (production is https://wollan.nl). Only wollan.nl and "
        "localhost/127.0.0.1 are allowed.",
    )


def resolve_token():
    """Return (token, source). Never log the returned token."""
    env = os.environ.get("WOL_API_TOKEN", "").strip()
    if env:
        return env, "WOL_API_TOKEN environment variable"
    path = token_file()
    if os.path.isfile(path):
        mode = os.stat(path).st_mode
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            print(f"warning: {path} is readable by other users; run: chmod 600 {path}", file=sys.stderr)
        with open(path, encoding="utf-8") as fh:
            tok = fh.read().strip()
        if tok:
            return tok, f"token file {path}"
    return None, None


def require_token():
    tok, source = resolve_token()
    if not tok:
        raise WolError(
            "No WOL API token configured.",
            EXIT_CONFIG_ERROR,
            "Ask the user to create a token at https://wollan.nl/user/api-tokens and then run "
            f"`python3 {os.path.abspath(__file__)} set-token` themselves in a terminal "
            "(or export WOL_API_TOKEN). The user must NOT paste the token into the chat.",
        )
    if any(c in tok for c in "\r\n\0"):
        raise WolError(f"The token from {source} contains control characters.", EXIT_CONFIG_ERROR,
                       "Re-create it with `set-token`.")
    if not TOKEN_RE.match(tok):
        print(f"warning: token from {source} does not look like a WOL token "
              "(expected 'wol_' followed by 64 hex characters).", file=sys.stderr)
    return tok, source


# --------------------------------------------------------------------------- http

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise WolError(
            f"The API answered with a redirect ({code}); refusing to follow it with credentials.",
            EXIT_API_ERROR,
            "Check WOL_BASE_URL. Do not work around this.",
        )


_opener = urllib.request.build_opener(_NoRedirect())


def api(method, path, body=None):
    base, _ = resolve_base_url()
    tok, _ = require_token()
    data = None
    headers = {
        "Authorization": f"Bearer {tok}",
        "Accept": "application/json",
        "User-Agent": "wol-api-skill/2.0",
    }
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base + path, data=data, method=method, headers=headers)
    try:
        with _opener.open(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise _http_error(e.code, e.read(), base) from None
    except urllib.error.URLError as e:
        raise WolError(f"Could not reach {base}: {e.reason}", EXIT_API_ERROR,
                       "Check the network connection; try again later.") from None
    except TimeoutError:
        raise WolError(f"Request to {base} timed out.", EXIT_API_ERROR, "Try again later.") from None
    if not raw:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        raise WolError("The API returned a non-JSON response.", EXIT_API_ERROR, ERROR_HINTS[500]) from None


def _http_error(code, raw, base):
    message = None
    try:
        payload = json.loads(raw)
        if isinstance(payload, dict):
            parts = [payload.get("error"), payload.get("message"), payload.get("detail")]
            message = " - ".join(str(p) for p in parts if p)
    except ValueError:
        pass
    message = message or "(no error message)"
    hint = ERROR_HINTS.get(code, "")
    if code == 422:
        low = message.lower()
        if "disabled by the crew" in low:
            hint = "Ordering is temporarily paused by the crew. Tell the user to try again later."
        elif "out of stock" in low:
            hint = "Tell the user which product is out of stock and suggest an in-stock product from the same category (run `menu`)."
        elif "no event configured" in low:
            hint = ERROR_HINTS[503]
        elif "profile incomplete" in low:
            hint = "The user must fill in name, address, postcode and city in their profile on the WOL website."
        else:
            hint = "Show this message to the user."
    return WolError(f"HTTP {code}: {message}", EXIT_API_ERROR, hint.format(base=base))


# --------------------------------------------------------------------------- helpers

def euro(cents):
    cents = int(cents or 0)
    sign = "-" if cents < 0 else ""
    return f"{sign}€{abs(cents) / 100:.2f}"


def stock_mode(product):
    mode = product.get("stockMode")
    if isinstance(mode, dict):
        mode = mode.get("value") or mode.get("name")
    return mode


def active_event_id():
    data = api("GET", "/api/v1/events/zijn-de-inschrijvingen-al-open-of-nie")
    if not data.get("eventId"):
        raise WolError("There is no active WOL event.", EXIT_API_ERROR,
                       "Nothing to register for yet. Run `events` to see all events.")
    return int(data["eventId"])


def event_id_from(args):
    return args.event if args.event else active_event_id()


def event_detail(event_id):
    return api("GET", f"/api/v1/events/{int(event_id)}")


def event_line(ev):
    return (f"[{ev['id']}] {ev.get('name')} ({ev.get('nameShort')}) - starts {ev.get('startDate')} - "
            f"registrations {'OPEN' if ev.get('open') else 'closed'} - {ev.get('totalSeats')} seats"
            f"{' - seat selection enabled' if ev.get('chooseSeatEnabled') else ''}")


def emit(args, data, text_fn):
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        text_fn(data)


def confirm_hint(argv_hint):
    print()
    print("PREVIEW ONLY - nothing was changed.")
    print("Show this to the user and ask for explicit confirmation. Only after a clear yes, run:")
    print(f"  python3 {os.path.abspath(__file__)} {argv_hint} --yes")


# --------------------------------------------------------------------------- commands

def cmd_auth(args):
    base, base_src = resolve_base_url()
    tok, tok_src = resolve_token()
    print(f"Base URL : {base} ({base_src})")
    if not tok:
        print("Token    : NOT CONFIGURED")
        require_token()  # raises with the setup instructions
    print(f"Token    : configured via {tok_src} (value hidden)")
    api("GET", "/api/v1/events/zijn-de-inschrijvingen-al-open-of-nie")
    print("Check    : OK - the API accepted the token")


def cmd_set_token(args):
    if sys.stdin.isatty():
        tok = getpass.getpass("Paste your WOL API token (input hidden): ").strip()
    else:
        tok = sys.stdin.readline().strip()
    if not tok:
        raise WolError("No token entered.", EXIT_USAGE)
    if not TOKEN_RE.match(tok):
        raise WolError("That does not look like a WOL token (expected 'wol_' followed by 64 hex characters).",
                       EXIT_USAGE, "Copy the token shown once after creating it at /user/api-tokens.")
    os.makedirs(config_dir(), mode=0o700, exist_ok=True)
    path = token_file()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(tok + "\n")
    os.chmod(path, 0o600)
    print(f"Token saved to {path} (mode 600).")
    if os.environ.get("WOL_API_TOKEN"):
        print("Note: WOL_API_TOKEN is also set and takes precedence over the file.")


def cmd_menu(args):
    categories = api("GET", "/api/v1/catering/products")

    def text(cats):
        for cat in cats:
            products = cat.get("activeProducts") or []
            if not products:
                continue
            print(f"== {cat.get('name')}")
            for p in products:
                stock = int(p.get("calculatedStock") or 0)
                if stock <= 0:
                    avail = "OUT OF STOCK"
                elif stock_mode(p) == "Auto":
                    avail = f"in stock ({stock} left)"
                else:
                    avail = "in stock"
                print(f"  id {p['id']:>4}  {euro(p.get('price')):>7}  {p.get('name')}  [{avail}]")
        print()
        print("Prices in euro. Order with: order <productId>[:<quantity>] ...")

    emit(args, categories, text)


def parse_items(specs):
    items = {}
    for spec in specs:
        for part in spec.split(","):
            part = part.strip()
            if not part:
                continue
            m = re.fullmatch(r"(\d+)(?:[:x*](\d+))?", part)
            if not m:
                raise WolError(f"Invalid item '{part}'. Use productId or productId:quantity, e.g. 12:2",
                               EXIT_USAGE)
            pid, qty = int(m.group(1)), int(m.group(2) or 1)
            if qty < 1:
                raise WolError(f"Quantity must be at least 1 (item '{part}').", EXIT_USAGE)
            items[pid] = items.get(pid, 0) + qty
    if not items:
        raise WolError("No items given. Example: order 12:2 7", EXIT_USAGE)
    return [{"productId": pid, "quantity": qty} for pid, qty in items.items()]


def cmd_order(args):
    items = parse_items(args.items)
    argv_hint = "order " + " ".join(f"{i['productId']}:{i['quantity']}" for i in items)

    if not args.yes:
        products = {}
        for cat in api("GET", "/api/v1/catering/products"):
            for p in cat.get("activeProducts") or []:
                products[int(p["id"])] = (p, cat.get("name"))
        total, problems = 0, []
        print("Order preview:")
        for it in items:
            entry = products.get(it["productId"])
            if not entry:
                problems.append(f"product id {it['productId']} does not exist or is not available")
                continue
            p, cat = entry
            line = int(p.get("price") or 0) * it["quantity"]
            total += line
            flag = "" if int(p.get("calculatedStock") or 0) > 0 else "  <-- OUT OF STOCK"
            print(f"  {it['quantity']} x {p.get('name')} ({cat}) @ {euro(p.get('price'))} = {euro(line)}{flag}")
            if flag:
                problems.append(f"{p.get('name')} is out of stock")
        print(f"  Total: {euro(total)}")
        if problems:
            print()
            for pr in problems:
                print(f"PROBLEM: {pr}")
            print("Fix the item list (run `menu`) before asking the user to confirm.")
            return EXIT_USAGE
        confirm_hint(argv_hint)
        return EXIT_OK

    order = api("POST", "/api/v1/catering/orders", {"items": items})

    def text(o):
        total = sum(int(i.get("productPrice") or 0) * int(i.get("quantity") or 0) for i in o.get("items", []))
        print(f"Order placed: #{o.get('id')} - status {o.get('status')} ({ORDER_STATUS.get(o.get('status'), '')})")
        for i in o.get("items", []):
            print(f"  {i.get('quantity')} x {i.get('productName')} @ {euro(i.get('productPrice'))}")
        print(f"  Total: {euro(total)}")

    emit(args, order, text)


def cmd_orders(args):
    query = urllib.parse.urlencode({"page": args.page, "limit": args.limit})
    data = api("GET", f"/api/v1/catering/orders?{query}")

    def text(d):
        acc = d.get("account", {})
        print("Catering account (active event):")
        print(f"  Total spent (completed orders) : {euro(acc.get('totalSpent'))}")
        print(f"  Total paid                     : {euro(acc.get('totalPaid'))}")
        bal = int(acc.get("balance") or 0)
        label = "still owed" if bal > 0 else ("credit" if bal < 0 else "settled")
        print(f"  Balance                        : {euro(bal)} ({label})")
        print(f"  Pending (orders in progress)   : {euro(acc.get('pendingTotal'))}")
        pag = d.get("pagination", {})
        orders = d.get("orders", [])
        print(f"  Orders                         : {pag.get('total', len(orders))}")
        if not args.details:
            return
        print()
        if not orders:
            print("No orders on this page.")
        for o in orders:
            items = o.get("items", [])
            total = sum(int(i.get("productPrice") or 0) * int(i.get("quantity") or 0) for i in items)
            status = o.get("status")
            print(f"#{o.get('id')}  {o.get('dateCreated')}  {status} ({ORDER_STATUS.get(status, '?')})  {euro(total)}")
            for i in items:
                print(f"    {i.get('quantity')} x {i.get('productName')} @ {euro(i.get('productPrice'))}")
        if pag.get("pages", 1) > 1:
            print(f"\nPage {pag.get('page')} of {pag.get('pages')} (use --page N for more)")

    emit(args, data, text)


def cmd_open(args):
    data = api("GET", "/api/v1/events/zijn-de-inschrijvingen-al-open-of-nie")

    def text(d):
        if not d.get("eventId"):
            print("There is no active WOL event.")
        elif d.get("open"):
            print(f"Registrations are OPEN for the active event (event id {d['eventId']}).")
        else:
            print(f"Registrations are CLOSED for the active event (event id {d['eventId']}).")

    emit(args, data, text)


def cmd_events(args):
    events = api("GET", "/api/v1/events/")

    def text(evs):
        if not evs:
            print("No events.")
        for ev in evs:
            print(event_line(ev))

    emit(args, events, text)


def _seat_counts(detail):
    plan = detail.get("seatPlan") or {}
    seats = plan.get("seats") or []
    free = [s for s in seats if not s.get("reserved") and not s.get("taken")]
    return seats, free


def cmd_event(args):
    detail = event_detail(event_id_from(args))

    def text(d):
        print(event_line(d))
        seats, free = _seat_counts(d)
        if d.get("seatPlan"):
            print(f"Seat plan: {len(seats)} seats, {len(free)} free. Use `seats` for the list of free seats.")
        else:
            print("No seat plan configured.")

    emit(args, detail, text)


def cmd_seats(args):
    detail = event_detail(event_id_from(args))
    seats, free = _seat_counts(detail)
    data = {"eventId": detail.get("id"), "chooseSeatEnabled": detail.get("chooseSeatEnabled"),
            "free": [{"id": s["id"], "seatNumber": s.get("seatNumber")} for s in free]}

    def text(d):
        if not detail.get("seatPlan"):
            print("This event has no seat plan.")
            return
        print(f"Event {d['eventId']}: {len(free)} of {len(seats)} seats free"
              f"{'' if d['chooseSeatEnabled'] else ' (seat selection is currently DISABLED)'}")
        print("Free seat numbers: " + ", ".join(str(s["seatNumber"]) for s in d["free"]))

    emit(args, data, text)


def cmd_registration(args):
    event_id = event_id_from(args)
    data = api("GET", f"/api/v1/events/{event_id}/registration-status")
    data["eventId"] = event_id

    def text(d):
        if not d.get("registered"):
            print(f"Not registered for event {event_id}.")
        else:
            print(f"Registered for event {event_id}; payment: {'PAID' if d.get('payed') else 'NOT paid yet'}.")

    emit(args, data, text)


def cmd_register(args):
    event_id = event_id_from(args)
    if not args.yes:
        detail = event_detail(event_id)
        print("Register for: " + event_line(detail))
        if not detail.get("open"):
            print("PROBLEM: registrations for this event are closed.")
            return EXIT_USAGE
        status = api("GET", f"/api/v1/events/{event_id}/registration-status")
        if status.get("registered"):
            print("PROBLEM: the user is already registered for this event.")
            return EXIT_USAGE
        confirm_hint(f"register --event {event_id}")
        return EXIT_OK
    data = api("POST", f"/api/v1/events/{event_id}/register")
    emit(args, data, lambda d: print(f"Registered for event {event_id}. "
                                     "Payment is done via the WOL website."))


def cmd_unregister(args):
    event_id = event_id_from(args)
    if not args.yes:
        detail = event_detail(event_id)
        print("CANCEL registration for: " + event_line(detail))
        status = api("GET", f"/api/v1/events/{event_id}/registration-status")
        if not status.get("registered"):
            print("PROBLEM: the user is not registered for this event.")
            return EXIT_USAGE
        if status.get("payed"):
            print("WARNING: this registration is already PAID. Make sure the user understands this.")
        if args.reason:
            print(f"Reason: {args.reason}")
        reason = f" --reason {json.dumps(args.reason)}" if args.reason else ""
        confirm_hint(f"unregister --event {event_id}{reason}")
        return EXIT_OK
    body = {"reason": args.reason} if args.reason else None
    data = api("POST", f"/api/v1/events/{event_id}/unregister", body)
    emit(args, data, lambda d: print(f"Registration for event {event_id} cancelled."))


def cmd_seat(args):
    event_id = event_id_from(args)
    seat_id = args.id
    if args.number is not None or not args.yes:
        detail = event_detail(event_id)
        seats = (detail.get("seatPlan") or {}).get("seats") or []
        if args.number is not None:
            match = [s for s in seats if str(s.get("seatNumber")) == str(args.number)]
        else:
            match = [s for s in seats if int(s["id"]) == int(seat_id)]
        if not match:
            raise WolError(f"Seat not found in the seat plan of event {event_id}.", EXIT_USAGE,
                           "Run `seats` to list free seat numbers.")
        seat = match[0]
        seat_id = int(seat["id"])
        if not args.yes:
            print(f"Choose seat number {seat.get('seatNumber')} (seat id {seat_id}) for: " + event_line(detail))
            problems = []
            if not detail.get("chooseSeatEnabled"):
                problems.append("seat selection is disabled for this event")
            if seat.get("reserved") or seat.get("taken"):
                problems.append("this seat is not available")
            if problems:
                for pr in problems:
                    print(f"PROBLEM: {pr}")
                return EXIT_USAGE
            confirm_hint(f"seat --event {event_id} --id {seat_id}")
            return EXIT_OK
    data = api("POST", f"/api/v1/events/{event_id}/seat", {"seatId": int(seat_id)})
    emit(args, data, lambda d: print(f"Seat (id {seat_id}) assigned for event {event_id}."))


# --------------------------------------------------------------------------- cli

def build_parser():
    p = argparse.ArgumentParser(prog="wol.py", description="WOL (Wake-up On LAN) API client.")
    p.add_argument("--json", action="store_true", help="print the raw API JSON instead of text")
    sub = p.add_subparsers(dest="command", required=True, metavar="COMMAND")

    def add(name, fn, help_):
        sp = sub.add_parser(name, help=help_, description=help_)
        sp.set_defaults(fn=fn)
        sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        return sp

    def add_event(sp):
        sp.add_argument("--event", type=int, help="event id (default: the active event)")

    def add_yes(sp):
        sp.add_argument("--yes", action="store_true", help="actually perform the change (after user confirmation)")

    add("auth", cmd_auth, "show which credentials are used (never the token itself) and verify them")
    add("set-token", cmd_set_token, "store a token in ~/.config/wol/token (for the USER to run in a terminal)")
    add("menu", cmd_menu, "list catering products with ids, prices and stock")

    sp = add("order", cmd_order, "preview (or with --yes: place) a catering order")
    sp.add_argument("items", nargs="+", help="productId or productId:quantity (quantity defaults to 1)")
    add_yes(sp)

    sp = add("orders", cmd_orders, "catering account balance; --details lists the orders")
    sp.add_argument("--details", action="store_true", help="also list individual orders")
    sp.add_argument("--page", type=int, default=1)
    sp.add_argument("--limit", type=int, default=20, help="orders per page (max 100)")

    add("open", cmd_open, "are registrations open for the active event?")
    add("events", cmd_events, "list all events")

    sp = add("event", cmd_event, "details of an event (default: active event)")
    add_event(sp)

    sp = add("seats", cmd_seats, "list free seats of an event")
    add_event(sp)

    sp = add("registration", cmd_registration, "is the user registered for / paid for an event?")
    add_event(sp)

    sp = add("register", cmd_register, "preview (or with --yes: perform) registration for an event")
    add_event(sp)
    add_yes(sp)

    sp = add("unregister", cmd_unregister, "preview (or with --yes: perform) cancelling a registration")
    add_event(sp)
    sp.add_argument("--reason", help="optional cancellation reason")
    add_yes(sp)

    sp = add("seat", cmd_seat, "preview (or with --yes: perform) choosing a seat")
    add_event(sp)
    g = sp.add_mutually_exclusive_group(required=True)
    g.add_argument("--number", help="seat number as shown on the seat plan")
    g.add_argument("--id", type=int, help="seat id from the API")
    add_yes(sp)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args) or EXIT_OK
    except WolError as e:
        sys.stdout.flush()
        print(f"ERROR: {e}", file=sys.stderr)
        if e.hint:
            print(f"ACTION: {e.hint}", file=sys.stderr)
        return e.exit_code
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
