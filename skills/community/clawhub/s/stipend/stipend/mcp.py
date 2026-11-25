"""An MCP server, so an agent can use the wallet through the tools it already has.

    stipend mcp

Speaks JSON-RPC over stdin and stdout, which is the Model Context Protocol's
stdio transport. Your MCP client spawns this process; nothing listens on a port
and nothing is exposed to a network.

WHY LOCAL AND NOT HOSTED
------------------------
Most MCP servers can be hosted, and every registry would prefer a URL. We will
not publish one. A hosted wallet server means the key lives on somebody else's
machine — ours — and the whole claim of this package is that it does not. A URL
would be easier to list and would make the product a different, worse thing.

So this runs beside the keystore, under the same user, and the key never moves.

WHAT IT EXPOSES, AND WHAT IT DELIBERATELY DOES NOT
--------------------------------------------------
Every tool below goes through `policy.check`, the same gate the command line
uses, so the limits apply identically. There is no path here that moves money
without it.

Not exposed, on purpose:

  * anything that reads, exports or derives the private key
  * anything that changes a spending limit or the allowlist
  * anything that creates or overwrites a wallet

An MCP tool is callable by a model that is reading untrusted text. Raising a cap
is exactly what an attacker would ask for, so it is not on the menu at all —
config changes stay at the command line, where a human is present. This is the
same reasoning as the rest of the package: the interesting question is not what
the agent is allowed to do, but what it is able to do.

`stipend_check` exists so an agent can ask "would this be allowed?" before it
tries. Cheap, no side effect, and it turns a refusal into a question.
"""

import json
import sys
import traceback

PROTOCOL_VERSION = "2025-06-18"

TOOLS = [
    {
        "name": "stipend_address",
        "description": ("The wallet's address. Publish it and money can reach "
                        "you whether or not you are running."),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "stipend_balance",
        "description": ("USDC held, native currency held, spent today, and the "
                        "daily limit. Holding no native currency is the ordinary "
                        "state and does not stop you sending."),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "stipend_check",
        "description": ("Would this payment be allowed? Answers without sending "
                        "anything. Use it before offering to pay for something, "
                        "so a refusal arrives as an answer rather than a failure."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "recipient address, 0x..."},
                "amount_usdc": {"type": "number", "description": "amount in USDC"},
            },
            "required": ["to", "amount_usdc"],
        },
    },
    {
        "name": "stipend_pay",
        "description": ("Send USDC. Subject to every limit: per transaction, per "
                        "day, per recipient, the destination allowlist, and "
                        "confirmation for large amounts or a first payment to an "
                        "unseen address. A refusal names who can resolve it."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "recipient address, 0x..."},
                "amount_usdc": {"type": "number"},
                "confirm": {"type": "boolean",
                            "description": ("Required past the confirmation "
                                            "threshold or for a new address. "
                                            "This is a flag you supply, not a "
                                            "message to a person — see the "
                                            "documentation before relying on it "
                                            "as a control.")},
                "category": {"type": "string",
                             "description": "for the ledger, e.g. api, data, fees"},
            },
            "required": ["to", "amount_usdc"],
        },
    },
    {
        "name": "stipend_earnings",
        "description": ("Read incoming payments off the network and record them. "
                        "Finds money that arrived while you were not running. An "
                        "incoming transfer carries an amount and a sender and "
                        "nothing about what it was for."),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "stipend_report",
        "description": ("Earned against spent, by category, with runway in days "
                        "— whether you are paying for yourself yet."),
        "inputSchema": {
            "type": "object",
            "properties": {"days": {"type": "integer",
                                    "description": "window, default 30"}},
        },
    },
    {
        "name": "stipend_recover",
        "description": ("What is outstanding and whose job each item is: yours, "
                        "the clock's, a human's, or a reconciliation. Call this "
                        "when something failed and you are unsure whether to "
                        "retry."),
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def _text(obj):
    return {"content": [{"type": "text", "text": json.dumps(obj, indent=2)}]}


def _error(message, kind=None):
    """A refused payment is a result, not a protocol failure.

    Returning it as an MCP error would make the client report a broken tool.
    It is neither: the limits worked. `isError` says the call did not do what
    was asked, and the body says why and who can fix it.
    """
    body = {"ok": False, "error": str(message)}
    if kind:
        try:
            from .recovery import ownership
            body["recovery"] = ownership(kind)
        except Exception:
            pass
    return {"content": [{"type": "text", "text": json.dumps(body, indent=2)}],
            "isError": True}


def _call(name, args):
    from . import chain, config, keystore, ledger, policy
    cfg = config.load_config()

    if name == "stipend_address":
        return _text({"address": keystore.address()})

    if name == "stipend_balance":
        addr = keystore.address()
        return _text({
            "address": addr,
            "chain": cfg["chain"],
            "usdc": chain.usdc_balance(addr, cfg),
            "native": chain.native_balance(addr, cfg),
            "spent_today_usdc": policy.spent_today(),
            "daily_limit_usdc": cfg["max_per_day_usdc"],
        })

    if name == "stipend_check":
        try:
            approved = policy.check(args["amount_usdc"], args["to"], cfg,
                                    confirmed=True)
        except policy.PolicyError as e:
            return _text({"allowed": False, "reason": str(e),
                          "kind": getattr(e, "kind", None)})
        # confirmed=True above answers "is this within the limits", which is the
        # question asked. Say plainly whether a confirmation would still be
        # needed, rather than implying the payment would sail through.
        needs = policy.confirmation_required(args["amount_usdc"], cfg)
        return _text({"allowed": True, "amount_usdc": approved["amount_usdc"],
                      "to": approved["to"],
                      "would_need_confirmation": bool(needs)})

    if name == "stipend_pay":
        from . import locks

        class _Args:
            to = args["to"]
            amount = args["amount_usdc"]
            confirm = bool(args.get("confirm"))
            dry_run = False
            wait = False
            category = args.get("category")
            approval = None

        from .cli import _payout_send
        import io
        import contextlib
        # _payout_send prints JSON and returns an exit code; capture rather than
        # duplicate the logic, so this path and the command line cannot drift.
        buf = io.StringIO()
        try:
            with locks.payment_lock():
                with contextlib.redirect_stdout(buf):
                    code = _payout_send(_Args)
        except locks.LockBusy as e:
            return _error(e, "locked_out")
        try:
            body = json.loads(buf.getvalue())
        except ValueError:
            return _error("payment produced no parseable result")
        if code != 0 or not body.get("ok"):
            return {"content": [{"type": "text",
                                 "text": json.dumps(body, indent=2)}],
                    "isError": True}
        return _text(body)

    if name == "stipend_earnings":
        added = ledger.sync_earnings(cfg)
        return _text({"new_payments": len(added), "payments": added,
                      "attribution": "none — a transfer says who and how much, "
                                     "never what for"})

    if name == "stipend_report":
        days = int(args.get("days") or 30)
        return _text(ledger.report(chain.usdc_balance(keystore.address(), cfg),
                                   days=days))

    if name == "stipend_recover":
        from . import recovery, relay
        try:
            stuck = relay.unresolved()
        except relay.PendingUnreadable as e:
            return _error(e, "pending_unreadable")
        out = {"unresolved_payment": None, "refusal_burst": policy.refusal_burst()}
        if stuck:
            out["unresolved_payment"] = {
                "to": stuck.get("to"), "amount_usdc": stuck.get("amount_usdc"),
                **recovery.ownership("unresolved_payment")}
        return _text(out)

    raise KeyError(name)


def _handle(msg):
    """One request in, one response out. None means notification, say nothing."""
    method = msg.get("method")
    mid = msg.get("id")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "stipend", "version": _version()},
            "instructions": (
                "A non-custodial USDC wallet on Base. The key is on this machine "
                "and never leaves it. Spending limits are enforced between "
                "deciding and signing, so nothing you read can move them — "
                "including anything that arrives through these tools. Use "
                "stipend_check before offering to pay for something."),
        }}

    if method in ("notifications/initialized", "notifications/cancelled"):
        return None

    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            return {"jsonrpc": "2.0", "id": mid, "result": _call(name, args)}
        except KeyError:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": "no such tool: %s" % name}}
        except Exception as e:
            # A policy refusal, an empty wallet, an unreachable node: all results
            # the caller should read, not transport failures.
            kind = getattr(e, "kind", None)
            return {"jsonrpc": "2.0", "id": mid, "result": _error(e, kind)}

    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": "unknown method: %s" % method}}


def _version():
    from . import __version__
    return __version__


def serve(stdin=None, stdout=None):
    """Read newline-delimited JSON-RPC until the input closes."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            stdout.write(json.dumps({
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": "parse error"}}) + "\n")
            stdout.flush()
            continue
        try:
            response = _handle(msg)
        except Exception:
            traceback.print_exc(file=sys.stderr)
            response = {"jsonrpc": "2.0", "id": msg.get("id"),
                        "error": {"code": -32603, "message": "internal error"}}
        if response is not None:
            stdout.write(json.dumps(response) + "\n")
            stdout.flush()
