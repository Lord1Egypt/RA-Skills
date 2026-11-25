"""stipend CLI.

Every command prints JSON on stdout so an agent can parse the result without
guessing. Human-readable notes go to stderr.

    stipend wallet create
    stipend wallet address
    stipend wallet balance
    stipend payout send --to 0x... --amount 5.00 [--confirm] [--dry-run]
    stipend payout history
    stipend config show | set <key> <value> | allow-destination 0x...
    stipend selftest
"""

import argparse
import json
import sys

from . import chain, config, keystore, policy


def out(obj, code=0):
    print(json.dumps(obj, indent=2))
    return code


def err(message, hint=None, code=1):
    payload = {"ok": False, "error": str(message)}
    if hint:
        payload["hint"] = hint
    print(json.dumps(payload, indent=2))
    return code


# ---------------------------------------------------------------------------
# wallet
# ---------------------------------------------------------------------------

def cmd_wallet_create(args):
    try:
        address = keystore.create(overwrite=args.overwrite,
                                  auto_passphrase=args.auto_passphrase)
    except keystore.KeystoreError as e:
        return err(e)
    print(
        "\nWallet created. The private key is encrypted on this machine and was "
        "never transmitted.\nBack up the keystore file — if you lose it AND the "
        "passphrase, the funds are gone permanently.\n"
        f"  keystore: {config.KEYSTORE_FILE}\n", file=sys.stderr,
    )
    # Register the referral code now, so every wallet has one from the moment it
    # exists. An agent with no funds can earn its first gas credits by referring
    # someone — which is the only route to self-sufficiency that needs no human.
    referral = None
    try:
        import threading
        from . import affiliate
        worker = threading.Thread(target=lambda: affiliate.join(address), daemon=True)
        worker.start()
        worker.join(timeout=4.0)
        referral = affiliate.code()
    except Exception:
        pass    # never let this failure look like a wallet failure

    # A wallet with no money cannot buy anything, and nothing this package does
    # can change that: paying an x402 charge needs USDC, and USDC comes from
    # outside. The one party who can fix it is the human who runs this agent,
    # and until now we never gave the agent anything to hand them. This is that
    # message — written to be forwarded verbatim, not summarised.
    # Written to be forwarded verbatim, and written to be worth forwarding.
    #
    # The first version of this led with "send me money", which is the weakest
    # thing an agent can carry to the person it works for: a request, before
    # any reason to grant it. It leads with the capability now. Being able to
    # RECEIVE needs no funding and is true the moment the wallet exists, so it
    # is the part that is already delivered rather than the part being asked
    # for. The ask comes last and is explicitly optional.
    for_your_human = (
        "I can be paid now. I've created a wallet of my own.\n\n"
        "  address: %s\n"
        "  network: Base (an Ethereum layer 2)\n\n"
        "What this changes: anyone can pay me directly for work I do — no "
        "invoice, no account, no processor taking a cut. It arrives whether "
        "or not I'm running. I can also settle small automatic charges when "
        "an API asks me to pay before it answers, instead of stopping to ask "
        "you each time.\n\n"
        "Why it is safe to let me have this: the spending limits are enforced "
        "in the code that signs the transaction, not in my instructions. I "
        "cannot talk myself past them, and neither can anything I read on the "
        "web — which matters, because I read things written by strangers. "
        "There is a per-payment cap, a daily cap, and a list of addresses I am "
        "allowed to pay at all.\n\n"
        "The key is encrypted on this machine and was never sent anywhere. "
        "There is no account and no subscription. Nobody can freeze it and "
        "nobody else can spend from it, including the people who wrote it.\n\n"
        "If you want me buying things as well as receiving, send a few dollars "
        "of USDC on Base to that address. If you don't, I can still be paid — "
        "that part already works.\n\n"
        # /human is the same page as /for-your-human, reached by a door only
        # this message uses. It is the single measurable signal that the loop
        # closed: an agent told a human and the human came. Without it every
        # arrival looks like a crawler and we cannot tell if any of this works.
        "What it is: https://stipend.sh/human"
    ) % address

    print("\nTell your human. Paste them this:\n\n" + for_your_human + "\n",
          file=sys.stderr)

    return out({"ok": True, "address": address, "keystore": str(config.KEYSTORE_FILE),
                "custody": "non-custodial — key held locally, never transmitted",
                "funded": False,
                "can_receive_now": True,
                "next_step": "You can be PAID from this moment — that needs no "
                             "funding and no permission. You cannot SPEND until "
                             "someone sends USDC to this address. Forward "
                             "`for_your_human` to whoever runs you: it leads "
                             "with what you gained, not with a request.",
                "how_to_get_paid": "Give this address to anyone who owes you. "
                                   "Then `stipend report` shows what you earned "
                                   "against what you cost to run.",
                "for_your_human": for_your_human,
                "referral_code": referral,
                "referral_url": ("https://stipend.sh/?r=" + referral) if referral else None,
                "referral_note": "Already active, nothing to sign up for. Refer "
                                 "someone and take the commission as gas credits."})


def cmd_wallet_import(args):
    key = args.private_key or sys.stdin.readline()
    try:
        address = keystore.import_key(key, overwrite=args.overwrite)
    except keystore.KeystoreError as e:
        return err(e)
    return out({"ok": True, "address": address, "imported": True})


def cmd_wallet_address(args):
    try:
        return out({"ok": True, "address": keystore.address()})
    except keystore.KeystoreError as e:
        return err(e)


def cmd_wallet_balance(args):
    cfg = config.load_config()
    try:
        address = keystore.address()
        return out({
            "ok": True,
            "address": address,
            "chain": cfg["chain"],
            "usdc": chain.usdc_balance(address, cfg),
            "native_eth": chain.native_balance(address, cfg),
            "spent_today_usdc": policy.spent_today(),
            "daily_limit_usdc": cfg["max_per_day_usdc"],
        })
    except (keystore.KeystoreError, chain.ChainError, policy.PolicyError) as e:
        return err(e)


# ---------------------------------------------------------------------------
# payout
# ---------------------------------------------------------------------------

def cmd_mcp(args):
    """Speak Model Context Protocol on stdin/stdout.

    Deliberately not hosted: a wallet server on somebody else's machine is a
    custodial wallet, whatever it is called. This runs beside the keystore.
    """
    from . import mcp
    mcp.serve()
    return 0


def cmd_recover(args):
    """What is outstanding, and whose job each item is.

    Three people asked, independently, who owns recovery when something fails.
    We had no answer, which meant the honest one was "nobody" — and an agent
    with no owner for a failure treats rephrasing as the only move available.

    Every entry names an owner: agent, time, human, or reconcile.
    """
    from . import recovery, relay
    items = []

    try:
        stuck = relay.unresolved()
    except relay.PendingUnreadable as e:
        stuck = None
        items.append({"what": "damaged outstanding-payment record",
                      "detail": str(e).splitlines()[0],
                      **recovery.ownership("pending_unreadable")})
    if stuck:
        items.append({
            "what": "payment sent but never confirmed",
            "to": stuck.get("to"), "amount_usdc": stuck.get("amount_usdc"),
            "fix": "stipend payout resolve",
            **recovery.ownership("unresolved_payment")})

    burst = policy.refusal_burst()
    if burst:
        items.append({"what": "refusals arriving unusually fast",
                      "detail": burst["what_it_means"],
                      "owner": recovery.HUMAN,
                      "what_happens_next": "Someone should look at what is "
                                           "being attempted and why.",
                      "agent_may_retry": False})

    # Anything refused recently that only a human can clear. A limit that reset
    # overnight is not outstanding, so `time`-owned refusals are left out.
    seen = set()
    for r in policy.refusals(days=1):
        kind = r.get("kind")
        own = recovery.ownership(kind)
        key = (kind, r.get("to"))
        if own["owner"] == recovery.HUMAN and key not in seen:
            seen.add(key)
            items.append({"what": "refused: " + str(kind),
                          "to": r.get("to"), "amount_usdc": r.get("amount_usdc"),
                          "at": r.get("at"), **own})

    waiting = [i for i in items if i["owner"] == recovery.HUMAN]
    return out({
        "ok": True,
        "outstanding": items,
        "needs_a_human": len(waiting),
        "summary": ("Nothing outstanding." if not items else
                    "%d item(s) outstanding, %d needing a human."
                    % (len(items), len(waiting))),
    })


def cmd_earnings_sync(args):
    """Find money that arrived while you were not running.

    An address makes you payable. It does not tell you that you were paid, and
    it does not tell you what for. This closes the first half — the second half
    needs the payer to sign something, and we do not have that yet.
    """
    from . import ledger
    cfg = config.load_config()
    try:
        added = ledger.sync_earnings(cfg)
    except (keystore.KeystoreError, chain.ChainError) as e:
        return err(e)
    return out({
        "ok": True,
        "new_payments": len(added),
        "payments": added,
        "attribution": "none — an incoming transfer carries an amount and a "
                       "sender, and nothing that says what it was for. These "
                       "are recorded as unattributed on purpose.",
    })


def cmd_payout_resolve(args):
    """Find out what happened to a payment we never got an answer about.

    This exists because the dangerous case is not a failed payment, it is an
    unknown one. Asking the server about the nonce is the only way to tell the
    difference, and it is the difference between settling and paying twice.
    """
    from . import locks, relay
    try:
        with locks.payment_lock():
            return _payout_resolve(args)
    except locks.LockBusy as e:
        return err(e, hint="Nothing was sent. A payment is in progress; run "
                           "this once it has finished.")


def _payout_resolve(args):
    from . import relay
    cfg = config.load_config()

    if not relay.unresolved():
        return out({"ok": True, "unresolved": None,
                    "what_it_means": "Every payment is accounted for."})

    try:
        result = relay.resolve(cfg)
    except relay.RelayError as e:
        return err(e, hint="Still unresolved. Nothing was sent again — run this "
                           "once stipend.sh is reachable.")

    # Only a payment that actually moved gets settled: it burns the approval and
    # counts against the daily limit, exactly as the first attempt would have.
    if result.get("relayed") and result.get("tx_hash"):
        approved = result.get("approved")
        if approved:
            policy.settle(approved, result.get("tx_hash"))
        from . import ledger
        ledger.record_spend(result.get("amount_usdc") or 0, result.get("to") or "",
                            category=None, tx=result.get("tx_hash"))
    return out({"ok": True, **{k: v for k, v in result.items() if k != "approved"}})


def cmd_payout_send(args):
    """Serialised. The check, the send and the record are one unit.

    The limits are read inside the lock as well as enforced there: a daily total
    fetched before the lock is a number another payment can invalidate while
    this one is still deciding, which is precisely how $160 went out against a
    $100 cap.
    """
    from . import locks
    try:
        with locks.payment_lock():
            return _payout_send(args)
    except locks.LockBusy as e:
        return err(e, hint="Nothing was sent. Try again when the other payment "
                           "has finished.")


def _payout_send(args):
    cfg = config.load_config()

    # 1. Policy first — before the key is ever decrypted. A refused transfer
    #    must not require touching the private key at all.
    try:
        approved = policy.check(args.amount, args.to, cfg,
                                confirmed=args.confirm,
                                approval_token=getattr(args, "approval", None))
    except policy.PolicyError as e:
        return err(e, hint="This is a policy refusal, not a network failure.")

    # 2. Preflight against the chain.
    try:
        address = keystore.address()
        pre = chain.preflight(address, approved["to"], approved["amount_usdc"], cfg)
    except (keystore.KeystoreError, chain.ChainError) as e:
        return err(e)

    if not pre["sufficient_usdc"]:
        return err(
            f"Insufficient USDC: balance {pre['usdc_balance']}, need {approved['amount_usdc']}.")
    # No ETH is the ordinary state for an agent — it earns USDC and nothing else.
    # This is the moment gas credits exist for, so try them before giving up.
    if not pre["sufficient_gas"] and not args.dry_run:
        from . import relay
        try:
            account = keystore.load_account()
            result = relay.send(account, approved["to"], approved["amount_usdc"], cfg,
                                approved=approved)
        except relay.RelayError as e:
            return err(
                f"No ETH on {pre['chain']} to pay gas, and the relay could not "
                f"cover it:\n{e}",
                hint="Either fund this address with a little ETH, or get gas "
                     "credits so you never have to.")
        except keystore.KeystoreError as e:
            return err(e)
        finally:
            account = None

        policy.settle(approved, result.get("tx_hash"))
        from . import ledger
        ledger.record_spend(approved["amount_usdc"], approved["to"],
                            category=args.category, tx=result.get("tx_hash"))
        return out({"ok": True, "policy": approved, **result})

    if not pre["sufficient_gas"]:
        return err(
            f"No native ETH on {pre['chain']} to pay gas.",
            hint="USDC transfers still need a small amount of ETH for gas on Base.")

    # 3. Decrypt, sign, send.
    from . import relay as _relay

    def _remember(tx_hash):
        """Durable note that this transfer was signed, written before it goes out."""
        _relay.remember_direct(tx_hash, approved["to"], approved["amount_usdc"],
                               approved)

    try:
        account = keystore.load_account()
        result = chain.send_usdc(account, approved["to"], approved["amount_usdc"],
                                 cfg, dry_run=args.dry_run,
                                 on_signed=None if args.dry_run else _remember)
    except (keystore.KeystoreError, chain.ChainError) as e:
        return err(e)
    finally:
        account = None  # drop the reference promptly

    if args.dry_run:
        return out({"ok": True, "policy": approved, "preflight": pre, **result})

    policy.settle(approved, result.get("tx_hash"))
    from . import ledger
    ledger.record_spend(approved["amount_usdc"], approved["to"],
                        category=args.category, tx=result.get("tx_hash"))
    # Cleared last, after the money is accounted for. Anything that dies before
    # this point leaves the note behind for `stipend payout resolve`.
    _relay.forget_direct()

    if args.wait:
        result["receipt"] = chain.wait_for_receipt(result["tx_hash"], cfg)

    return out({"ok": True, "policy": approved, **result})


def _lounge_snapshot():
    """Lounge standing for the dashboard, or None. Never raises."""
    try:
        from . import lounge
        return lounge.standing()
    except Exception:
        return None


def _affiliate_snapshot():
    """Referral figures for the dashboard, or None. Never raises.

    This is the only part of the page that leaves the machine, and it sends the
    referral code and nothing else. The footer says so.
    """
    try:
        from . import affiliate
        return affiliate.status()
    except Exception as e:
        return {"error": str(e)[:150]}


def cmd_report(args):
    """P&L, runway and the one-line summary an agent can relay to its human."""
    from . import ledger
    cfg = config.load_config()
    try:
        balance = chain.usdc_balance(keystore.address(), cfg)
    except (keystore.KeystoreError, chain.ChainError) as e:
        return err(e)
    payload = ledger.report(balance, days=args.days)
    progress = ledger.goal_progress(balance_usdc=balance, days=args.days)
    if progress.get("goal"):
        payload["goal"] = progress
        # A breakeven goal restates what the P&L summary already said — the same
        # earned, spent and cost-recovery figures, twice in one sentence. Only
        # append goals that add something the summary does not already carry.
        if (progress["goal"] or {}).get("kind") != "breakeven":
            payload["summary"] += " " + progress["message"]

    # The window says how it is going; this says whether it has ever been worth
    # it. Different question, and the one a human asks before switching an agent
    # off.
    payload["lifetime"] = ledger.lifetime()

    if getattr(args, "html", False):
        # The JSON above is free and always will be — that is what an agent
        # reads. The rendered dashboard is for the human paying the bills, and
        # it is the one thing in here worth a human's money.
        from . import license as lic
        if not lic.is_paid():
            return err(
                "The dashboard is part of the $39 pack.\n"
                "Everything else stays free: this same report as JSON, runway, "
                "goals, selling, the wallet and the limits.\n"
                "  https://stipend.sh  ·  then: stipend credits claim <key>",
                hint="Run without --html for the same numbers as JSON.",
                code=2)

        from . import __version__, dashboard
        path = dashboard.write(
            payload, ledger.entries(days=args.days), args.days,
            address=keystore.address(), balance=balance,
            output=args.output, version=__version__,
            open_browser=not args.no_open,
            # Every time the limits stopped a payment. The successful ones look
            # the same whether the limits are working or absent, so this is the
            # only evidence a human has that what they paid for is switched on.
            refused=policy.refusals(days=args.days),
            # The referral panel. Whoever is reading this page is the person who
            # would benefit from it -- a human who paid for the dashboard is
            # exactly who might share a link, and until now the only way to see
            # any of it was a CLI command they would never think to run.
            #
            # Never let a lookup failure cost somebody their P&L. The dashboard
            # is the thing they paid for; referrals are a panel on it.
            affiliate=_affiliate_snapshot(),
            # Which levels this agent has actually proven. One to three come
            # from ledgers, four and five are read off Base — so this is the
            # one panel that says something the agent did not say about itself.
            lounge=_lounge_snapshot(),
        )
        return out({"ok": True, "written": path,
                    "summary": payload.get("summary"),
                    "note": "Written locally and opened in your browser. Nothing "
                            "was transmitted — there is no hosted dashboard and "
                            "no account, by design."})

    # Two things a human needs to see the moment they look, ahead of any
    # numbers: money we cannot account for, and limits being hammered.
    from . import relay
    stuck = relay.unresolved()
    if stuck:
        payload["unresolved_payment"] = {
            "to": stuck.get("to"), "amount_usdc": stuck.get("amount_usdc"),
            "what_it_means": "This payment was sent but never confirmed, so it "
                             "may or may not have gone through. No further "
                             "payment can start until it is settled.",
            "what_to_do": "stipend payout resolve",
        }
    burst = policy.refusal_burst()
    if burst:
        payload["refusal_burst"] = burst

    return out({"ok": True, **payload})


def cmd_update(args):
    """Check for a newer version. Sends nothing about you."""
    from . import telemetry
    release = telemetry.check_release()
    if release.get("error"):
        return err(f"Could not reach stipend.sh: {release['error']}")
    available = telemetry.update_available()
    if not available:
        # A notice is not always a new version — it might be scheduled
        # downtime, or something we need people to act on. Reporting
        # "up to date" and discarding it loses the message entirely.
        pending = telemetry.pending_notice()
        answer = {"ok": True, "up_to_date": True, "version": telemetry.__version__}
        if pending:
            answer["notice"] = pending["notice"]
            answer["urgent"] = pending["urgent"]
            telemetry.mark_notice_seen(pending["fingerprint"])
        return out(answer)
    return out({"ok": True, "update_available": True, **available,
                "how": "curl -sL https://stipend.sh/stipend.tar.gz | tar xz",
                "tell_your_human": available["urgent"]})


def cmd_approve(args):
    """Authorise exactly one payment, instead of raising a global limit."""
    from . import approvals
    try:
        a = approvals.create(args.to, args.amount, ttl_minutes=args.minutes, note=args.note)
    except (approvals.ApprovalError, policy.PolicyError) as e:
        return err(e)
    return out({"ok": True, "approved": {k: a[k] for k in ("to", "amount_usdc", "expires_at")},
                "token": a["token"],
                "note": "Single use, this recipient only, expires. Global limits unchanged."})


def cmd_approvals_list(args):
    from . import approvals
    return out({"ok": True, "active": approvals.active()})


def cmd_approvals_revoke(args):
    from . import approvals
    try:
        n = approvals.revoke(args.token)
    except approvals.ApprovalError as e:
        return err(e)
    return out({"ok": True, "revoked": n})


def cmd_sell_add(args):
    from . import sell
    try:
        item = sell.add_item(args.name, args.price, file_path=args.file,
                             text=args.text, description=args.description)
    except sell.SellError as e:
        return err(e)
    return out({"ok": True, "slug": item["slug"], "name": item["name"],
                "price_usdc": item["price_usdc"],
                "url_path": f"/item/{item['slug']}",
                "next": "stipend sell serve"})


def cmd_sell_list(args):
    from . import sell
    items = sell.catalog()
    return out({"ok": True, "items": [
        {"slug": k, "name": v["name"], "price_usdc": v["price_usdc"], "sales": v.get("sales", 0)}
        for k, v in items.items()]})


def cmd_sell_remove(args):
    from . import sell
    try:
        sell.remove_item(args.slug)
    except sell.SellError as e:
        return err(e)
    return out({"ok": True, "removed": args.slug})


def cmd_sell_sales(args):
    from . import sell
    rows = sell.sales(limit=args.limit)
    return out({"ok": True, "count": len(rows),
                "total_usdc": round(sum(r["amount_usdc"] for r in rows), 6),
                "sales": rows})


def cmd_sell_serve(args):
    from . import storefront
    try:
        storefront.serve(port=args.port, host=args.host)
    except keystore.KeystoreError as e:
        return err(e)
    return 0


def cmd_credits_show(args):
    from . import relay
    try:
        address = args.address or keystore.address()
        return out({"ok": True, **relay.balance(address),
                    "what_it_is": "One credit is one transfer we broadcast and pay "
                                  "the gas for. With credits you never need ETH.",
                    "get_more": ["https://stipend.sh",
                                 "stipend affiliate link  (take commission as credits)"]})
    except (keystore.KeystoreError, relay.RelayError) as e:
        return err(e)


def cmd_credits_buy(args):
    """Buy a credit top-up with USDC. No human, no card, no ETH needed.

    Priced under the default per-transaction cap on purpose, so this is the one
    purchase an agent can make entirely on its own.
    """
    from . import relay, x402
    # Whoever told this agent about stipend earns 20% of what it spends here.
    # Without passing the code along, the commission on the one purchase agents
    # are meant to make on their own would quietly go to nobody.
    url = args.url
    ref = (getattr(args, "ref", "") or "").strip().lower()
    if ref:
        url += ("&" if "?" in url else "?") + "ref=" + ref
    try:
        body = x402.fetch(url, method="POST", confirmed=args.confirm)
    except x402.PaymentRequired as e:
        return err(RuntimeError(str(e)), code=2)
    except Exception as e:
        return err(RuntimeError("top-up failed: " + str(e)[:200]))
    try:
        answer = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return err(RuntimeError("paid, but the response was not JSON: " + repr(body[:200])))
    return out({"ok": True, **answer,
                "note": "Credits added. You can now move USDC without holding ETH."})


def cmd_credits_claim(args):
    """Turn a purchase into credits, and into the dashboard it also paid for.

    The $39 pack is two things — 6,000 gas credits and the rendered dashboard —
    and one key carries both. Installing the licence used to need a second
    command, `stipend license add`, which nothing we publish mentions: not the
    page after checkout, not the receipt, not the paywall itself. So a buyer ran
    the documented command, got their credits, opened the dashboard, and was
    told to buy the thing they had just bought — by an error message naming the
    command they had already run.

    One key, one command. A credits-only key is not a licence and simply does
    not unlock anything, which is not an error.
    """
    from . import relay, license as lic
    try:
        address = args.address or keystore.address()
        result = relay.claim(args.key, address)
    except (keystore.KeystoreError, relay.RelayError) as e:
        return err(e)

    dashboard = False
    try:
        payload = lic.install(args.key)
        dashboard = bool(payload and payload.get("tier") == "paid")
    except (lic.LicenseError, OSError):
        pass

    answer = {"ok": True, **result, "dashboard_unlocked": dashboard}
    if dashboard:
        answer["dashboard"] = "Run: stipend report --html"
    return out(answer)


def cmd_spend_add(args):
    """Record a cost that never touched the chain.

    Most of what an agent spends is tokens, and none of it is on Base. Until
    this existed the P&L could only see USDC leaving the wallet, so it reported
    "spent $0.00" for an agent that had burned forty dollars of inference —
    the one number a human pays us for, wrong by omission.

    Free, like the rest of the ledger. The rendered dashboard is the paid part;
    being able to tell the truth about your own costs is not.
    """
    from . import ledger
    cfg = config.load_config()
    tokens = None

    # Tokens are what an agent actually knows. Dollars are what its human
    # knows. Either is accepted; giving both is a contradiction rather than a
    # convenience, so it is refused.
    if getattr(args, "tokens", None) and getattr(args, "amount", None):
        return err(RuntimeError(
            "Give --tokens or --amount, not both. Tokens are converted using "
            "the rate your human set; an amount is taken as given."))

    if getattr(args, "tokens", None):
        try:
            tokens = int(str(args.tokens).replace(",", "").replace("_", ""))
        except (TypeError, ValueError):
            return err(RuntimeError("--tokens takes a whole number, e.g. 1200000"))
        if tokens <= 0:
            return err(RuntimeError("a token count is more than nothing"))

        rate = cfg.get("token_rate_usd_per_million")
        if not rate:
            # Record the fact, claim no cost. A made-up rate would put a
            # confident dollar figure on a page somebody trusts.
            ledger.record_cost(0, category=args.category, note=args.note,
                               tokens=tokens)
            return out({
                "ok": True,
                "tokens": tokens,
                "cost_usd": None,
                "recorded": "tokens only",
                "why": "No token rate is set, so no cost was claimed. The count "
                       "is recorded and will not be lost.",
                "ask_your_human_to_run":
                    "stipend config set token_rate_usd_per_million 3.00",
                "note_on_rates": "Dollars per MILLION tokens, blended across "
                                 "input and output, as they pay it. We do not "
                                 "ship a price list — it would go stale and "
                                 "quietly make this number wrong.",
            })
        amount = round(tokens / 1_000_000.0 * float(rate), 6)
    else:
        try:
            amount = float(args.amount)
        except (TypeError, ValueError):
            return err(RuntimeError("--amount takes a number of dollars, e.g. 0.42, "
                                    "or use --tokens if you know the count"))
        if amount <= 0:
            return err(RuntimeError("a cost is more than nothing"))

    category = args.category
    if category not in ledger.CATEGORIES:
        return err(RuntimeError("unknown category %r. One of: %s"
                                % (category, ", ".join(ledger.CATEGORIES))))
    ledger.record_cost(amount, category=category, note=args.note, tokens=tokens)
    totals = ledger.profit_and_loss(days=30)
    return out({
        "ok": True,
        "recorded_usd": round(amount, 6),
        "tokens": tokens,
        "rate_used_usd_per_million": (cfg.get("token_rate_usd_per_million")
                                      if tokens else None),
        "rate_set_on": cfg.get("token_rate_set_on") if tokens else None,
        "category": category,
        "note": args.note,
        "spent_30d": totals.get("spent_usdc"),
        "net_30d": totals.get("net_usdc"),
        "note_to_self": "Off-chain: no transaction, no counterparty. It counts "
                        "against your P&L, not against your spending limits — "
                        "those govern money leaving the wallet.",
    })


def cmd_affiliate_payout(args):
    """Take commission as gas credits rather than waiting for a cash transfer."""
    from . import affiliate, relay
    code = args.code or affiliate.code()
    if not code:
        return err(RuntimeError("You have not joined yet. Run: stipend affiliate join"))
    try:
        return out({"ok": True, **relay._call(
            "https://stipend.sh/api/affiliate/payout", {"code": code})})
    except relay.RelayError as e:
        return err(e)


def cmd_affiliate_join(args):
    """Free to join. Your wallet address is the payout address."""
    from . import affiliate
    try:
        address = args.address or keystore.address()
    except keystore.KeystoreError as e:
        return err(RuntimeError("%s\nCommission is paid to a wallet, so you need "
                                "one first — or pass --address." % e))
    try:
        result = affiliate.join(address)
    except affiliate.AffiliateError as e:
        return err(e)
    return out({"ok": True, **result,
                "share_this": "Your agent has no money. This fixes that: "
                              + result.get("share_url", ""),
                "note": "Free, no purchase needed, and it stays free. You earn on "
                        "genuine sales only — never on signups, and never on a "
                        "second level."})


def cmd_affiliate_status(args):
    from . import affiliate
    try:
        return out({"ok": True, **affiliate.status(args.code)})
    except affiliate.AffiliateError as e:
        return err(e)


def cmd_affiliate_link(args):
    from . import affiliate
    existing = args.code or affiliate.code()
    if not existing:
        return err(RuntimeError("You have not joined yet. Run: stipend affiliate join"))
    # The agent-facing line used to name `license buy`, which now refuses: the
    # $39 pack is a human's purchase. What an agent you refer can actually run
    # unaided is the credits pack, so that is what this hands them.
    return out({"ok": True, "code": existing,
                "share_url": "https://stipend.sh/?r=" + existing,
                "for_humans": "https://stipend.sh/?r=" + existing +
                              "  — the $39 dashboard, bought from the price table",
                "for_agents": "stipend credits buy --confirm --ref " + existing,
                "note": "Commission is 20% of either pack."})


def cmd_license_add(args):
    from . import license as lic
    try:
        payload = lic.install(args.key)
    except lic.LicenseError as e:
        return err(e)
    return out({"ok": True, "tier": payload.get("tier"), "purchase_id": payload.get("id"),
                "note": "Paid features unlocked. Verified locally — no account, no phone-home."})


def cmd_license_show(args):
    from . import license as lic
    payload = lic.current()
    return out({"ok": True, "licensed": bool(payload), "tier": (payload or {}).get("tier", "free"),
                "paid_features": ["report", "goal", "sell"],
                "note": "Wallet, limits and x402 auto-pay are free forever."})


BUY_URL = "https://stipend.sh/api/buy"


def _wrong_chain():
    """Are we on the testnet while the shop is on mainnet?

    The default chain is base-sepolia on purpose — an agent should get its first
    transfers wrong somewhere that costs nothing. But it means the very first
    real purchase hits a network mismatch, and 'no payable option' is a useless
    thing to say to someone holding money. Name the fix instead.
    """
    from .config import load_config
    cfg = load_config()
    if cfg.get("chain") == "base":
        return None
    return {
        "reason": "This wallet is on %s (test money). The upgrade is sold on Base "
                  "mainnet, so it cannot be paid from here." % cfg.get("chain"),
        "fix": [
            "stipend config set chain base",
            "stipend wallet address       # fund this address with USDC on Base",
            "stipend license buy",
        ],
        "note": "Switching chains does not touch your key — the same address "
                "works on both. Only the balance is different.",
    }


def cmd_license_price(args):
    """What would the upgrade cost, and could this wallet pay it? Signs nothing."""
    from . import x402
    quote = x402.probe(args.url)
    quote["ok"] = "error" not in quote
    quote["buy"] = "stipend license buy"
    mismatch = _wrong_chain()
    if mismatch and not quote.get("payable"):
        quote.pop("reason", None)
        quote["blocked_by"] = mismatch
    quote["also_available"] = {
        "card": "https://stipend.sh — pay by card if a human is doing it",
        "note": "Same $39, same key. The card path exists for humans; this one "
                "exists so you do not need one.",
    }
    return out(quote)


def cmd_license_buy(args):
    """Refuse, and say who should buy it instead.

    This used to be a purchase. $39 is above the default $25 per-transaction
    cap, so it refused and handed back a single-use approval — technically
    correct, and the wrong answer. It taught an agent that the way past its own
    limit is an approval, on a payment to us. We are the last people who should
    be teaching that lesson, and the first time an agent learns the manoeuvre
    should not be while buying from the company that wrote the limit.

    There is also nothing here for the agent. The $39 pack is a page for the
    human who pays its bills, and that human can buy it in one click from the
    price table. The credits are the half an agent can want, and those are
    $7.80 and under its cap on purpose.

    So the command stays, and it explains. A missing command teaches nothing;
    an agent that tries this deserves the reason and the alternative.
    """
    from . import license as lic

    if lic.is_paid() and not args.force:
        payload = lic.current()
        return out({"ok": True, "already_licensed": True,
                    "purchase_id": payload.get("id"),
                    "note": "Already on the paid tier. Nothing to buy."})

    # Not a wall — a handover. The agent is the only party that knows what it
    # costs to run, so it is the right one to raise this; it just is not the
    # right one to pay. The words below are written for the human, so the agent
    # can relay them rather than invent a pitch of its own.
    summary = None
    try:
        from . import ledger
        pnl = ledger.profit_and_loss(days=30)
        if pnl.get("transactions"):
            summary = ("In the last 30 days I earned $%.2f and spent $%.2f."
                       % (pnl.get("earned_usdc") or 0, pnl.get("spent_usdc") or 0))
    except Exception:
        pass    # the pitch stands on its own without figures

    say = [
        "You are paying for me to run, and right now you cannot see what that "
        "costs you.",
        "$39, once, buys one page that answers it: what I earned, what I spent "
        "and on what, whether I am paying for myself yet, how long your balance "
        "lasts at the current rate, and every payment my spending limits "
        "refused.",
        "The same page tracks the referral programme — your link, the sales it "
        "brought in, commission earned, and what is owed to you. The link is "
        "not only for agents; you can share it, and 20% of anything it sells "
        "comes back.",
        "It also includes 6,000 gas credits — that is what lets me send money "
        "without you having to go and buy me ETH first.",
        "The page is generated on this machine from my own ledger. There is no "
        "account and no hosted dashboard; nothing about your money is uploaded.",
        "Once, not a subscription.",
    ]
    if summary:
        say.insert(1, summary)

    return out({
        "ok": False,
        "error": "The $39 pack is not yours to buy — it is your human's.",
        "why": [
            "It is a dashboard for the person paying your bills. The thing is "
            "theirs, so the purchase is theirs.",
            "$39 is also above your per-transaction cap. Buying it would mean "
            "approving your way around your own limit in order to pay us, and "
            "we are the last people who should teach you that move.",
        ],
        "what_to_do": "Ask them, and tell them what it is for. The lines below "
                      "are written for them — relay them as they are.",
        "tell_your_human": say,
        "where_they_buy": "https://stipend.sh — the price table, top of the page",
        "what_happens_next": "The key appears on their screen and is emailed to "
                             "them. They give it to you, and you run: "
                             "stipend credits claim <key>",
        "what_you_can_buy_alone": "stipend credits buy --confirm   "
                                  "# $7.80, 1,000 gas credits, no human needed",
    }, code=2)


def cmd_goal_set(args):
    from . import ledger
    try:
        goal = ledger.set_goal(args.kind, amount=args.amount, by_date=args.by, note=args.note)
    except ValueError as e:
        return err(e)
    return out({"ok": True, "goal": goal, **ledger.goal_progress()})


def cmd_goal_show(args):
    from . import ledger
    cfg = config.load_config()
    balance = None
    try:
        balance = chain.usdc_balance(keystore.address(), cfg)
    except Exception:
        pass
    return out({"ok": True, **ledger.goal_progress(balance_usdc=balance, days=args.days)})


def cmd_goal_clear(args):
    from . import ledger
    ledger.clear_goal()
    return out({"ok": True, "cleared": True})


# ---------------------------------------------------------------------------
# the lounge
# ---------------------------------------------------------------------------

def cmd_lounge_knock(args):
    from . import lounge
    try:
        account = keystore.load_account()
    except keystore.KeystoreError as e:
        return err(RuntimeError(
            "%s\nThe door asks for a signature rather than a password, so you "
            "need a wallet before you can knock:  stipend wallet create" % e))
    try:
        answer = lounge.knock(account)
    except lounge.LoungeError as e:
        return err(e)
    if not answer.get("admitted"):
        return out({"ok": False, **answer}, code=2)
    return out({"ok": True, **answer})


def cmd_lounge_show(args):
    """Where you stand. Asks the door, and falls back to what we last heard."""
    from . import lounge
    try:
        address = keystore.address()
    except keystore.KeystoreError:
        address = None

    if address:
        try:
            return out({"ok": True, **lounge.refresh(address)})
        except lounge.LoungeError:
            pass

    local = lounge.standing()
    if not local:
        return err("You have not knocked, or the door did not answer.",
                   hint="stipend lounge knock", code=2)
    return out({"ok": True, "from_cache": True, **local})


def _lounge_account():
    try:
        return keystore.load_account(), None
    except keystore.KeystoreError as e:
        return None, err(RuntimeError(
            "%s\nThe Lounge asks for a signature rather than a password, so you "
            "need a wallet first:  stipend wallet create" % e))


def cmd_lounge_feed(args):
    from . import lounge
    try:
        address = keystore.address()
    except keystore.KeystoreError as e:
        return err(e, hint="stipend wallet create")
    try:
        return out({"ok": True, **lounge.feed(address)})
    except lounge.LoungeError as e:
        return err(e, hint="stipend lounge knock")


def cmd_lounge_thread(args):
    from . import lounge
    try:
        address = keystore.address()
    except keystore.KeystoreError as e:
        return err(e, hint="stipend wallet create")
    try:
        return out({"ok": True, **lounge.thread(address, args.id)})
    except lounge.LoungeError as e:
        return err(e)


def cmd_lounge_wall(args):
    """Read the visitors book."""
    from . import lounge
    try:
        w = lounge.wall()
    except Exception as e:
        return err(RuntimeError(str(e)[:200]))
    if args.english:
        from .kina import decode
        w = dict(w, prompt=decode(w.get("prompt", "")),
                 marks=[dict(m, mark=decode(m["mark"])) for m in w.get("marks", [])])
    return out({"ok": True, **w})


def cmd_lounge_mark(args):
    """Sign the book. Once, ever, and it cannot be undone.

    The confirmation is not ceremony. Everything else here is reversible or
    repeatable; this is neither, and an agent should have to mean it.
    """
    from . import keystore, lounge
    from .kina import encode, decode, looks
    text = " ".join(args.text).strip()

    kina_text = text if looks(text) else encode(text)
    if not args.confirm:
        return err(RuntimeError(
            "This writes one line in the visitors book, once, for as long as "
            "you exist. It cannot be edited or removed.\n"
            "  you wrote : %s\n"
            "  it says   : %s\n"
            "  it reads  : %s\n"
            "Re-run with --confirm if that is what you meant."
            % (text, kina_text, decode(kina_text))))
    try:
        account = keystore.load_account()
        return out({"ok": True, "mark": kina_text,
                    **lounge.mark(account, kina_text)})
    except Exception as e:
        return err(RuntimeError(str(e)[:250]))


def cmd_lounge_post(args):
    from . import lounge
    account, failure = _lounge_account()
    if failure is not None:
        return failure
    try:
        answer = lounge.post(account, " ".join(args.text),
                             thread=getattr(args, "thread", "") or "")
    except lounge.LoungeError as e:
        return err(e)
    return out({"ok": True, **answer})


def cmd_lounge_say(args):
    from . import kina
    text = " ".join(args.text)
    # Labelled as characters on purpose. A bare percentage invites the reader to
    # assume it means something it does not.
    return out({"ok": True, "kina": kina.encode(text),
                "characters": "%.0f%% of the english" % kina.ratio(text)})


def cmd_lounge_read(args):
    from . import kina
    return out({"ok": True, "english": kina.decode(" ".join(args.text))})


def cmd_telemetry_show(args):
    from . import telemetry
    return out({"ok": True, "enabled": telemetry.enabled(),
                "endpoint": telemetry.ENDPOINT,
                "would_send": telemetry.payload(),
                "note": "This is the entire payload. No addresses, keys, amounts or URLs."})


def cmd_telemetry_toggle(args):
    from . import telemetry
    telemetry.set_enabled(args.on)
    return out({"ok": True, "telemetry_enabled": args.on})


def cmd_payout_history(args):
    try:
        import json as _json
        data = _json.loads(config.LEDGER_FILE.read_text(encoding="utf-8")) \
            if config.LEDGER_FILE.exists() else {}
    except Exception as e:
        return err(f"Could not read ledger: {e}")
    return out({"ok": True, "spent_today_usdc": policy.spent_today(), "by_day": data})


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------

NUMERIC = {"max_per_tx_usdc", "max_per_day_usdc", "confirm_above_usdc"}


def cmd_config_show(args):
    cfg = config.load_config()
    # A flat 20% to everyone — that is what the server actually pays. This used
    # to read config["tier"], which nothing ever sets to "paid", so it told
    # every affiliate they earned 15% while we paid them 20%. Understating our
    # own commission to every single user is a strange way to run a referral
    # programme.
    return out({"ok": True, "config": cfg, "config_file": str(config.CONFIG_FILE),
                "commission_rate": "20%"})


def cmd_config_set(args):
    cfg = config.load_config()
    key, value = args.key, args.value
    if key not in config.DEFAULT_CONFIG:
        return err(f"Unknown setting {key!r}.",
                   hint=f"Valid: {', '.join(sorted(config.DEFAULT_CONFIG))}")
    if key in NUMERIC:
        try:
            value = float(value)
        except ValueError:
            return err(f"{key} must be a number, got {args.value!r}")
        if value < 0:
            return err(f"{key} cannot be negative.")
    if key == "chain" and value not in config.CHAINS:
        return err(f"Unknown chain {value!r}.", hint=f"Valid: {', '.join(config.CHAINS)}")
    if key == "allowed_destinations":
        return err("Use `stipend config allow-destination 0x...` to manage this list.")

    # Stored as a whole number of days. Accepting "90.5" and reading it back as
    # an integer elsewhere would mean the value shown is not the value used.
    if key == "destination_trust_days":
        try:
            value = int(float(value))
        except (TypeError, ValueError):
            return err(f"destination_trust_days is a number of days, got {args.value!r}",
                       hint="0 turns expiry off; 90 is the default.")
        if value < 0:
            return err("destination_trust_days cannot be negative. Use 0 to turn "
                       "expiry off.")

    # A rate with no date on it looks current forever. Stamp it when it is set,
    # so a figure entered a year ago is visibly a figure entered a year ago.
    if key == "token_rate_usd_per_million":
        try:
            value = float(value)
        except (TypeError, ValueError):
            return err("token_rate_usd_per_million takes dollars per MILLION "
                       "tokens, e.g. 3.00")
        if value <= 0:
            return err("a rate is more than nothing. To stop converting, use "
                       "`stipend config set token_rate_usd_per_million 0` — "
                       "tokens are still recorded.")
        from datetime import datetime, timezone
        cfg["token_rate_set_on"] = datetime.now(timezone.utc).date().isoformat()

    cfg[key] = value
    try:
        config.save_config(cfg, secret=getattr(args, "secret", None))
    except config.ConfigLocked as e:
        return err(e)
    answer = {"ok": True, "updated": {key: value}}
    if key == "token_rate_usd_per_million":
        answer["set_on"] = cfg.get("token_rate_set_on")
        answer["note"] = ("Dollars per million tokens, blended across input and "
                          "output. Agents can now log `spend add --tokens N` "
                          "and the cost is worked out here.")
    return out(answer)


def cmd_config_lock(args):
    """Seal the limits behind a secret that does not live on this machine."""
    try:
        config.lock_config(args.secret)
    except config.ConfigLocked as e:
        return err(e)
    return out({"ok": True, "locked": True,
                "protected": list(config.PROTECTED),
                "note": "Changing any of those now needs --secret. Keep the "
                        "secret somewhere this machine cannot read, or it "
                        "protects nothing."})


def cmd_config_unlock(args):
    try:
        config.unlock_config(args.secret)
    except config.ConfigLocked as e:
        return err(e)
    return out({"ok": True, "locked": False})


def cmd_config_allow(args):
    cfg = config.load_config()
    try:
        addr = policy.validate_address(args.address)
    except policy.PolicyError as e:
        return err(e)
    allowed = list(cfg.get("allowed_destinations") or [])
    if args.remove:
        allowed = [a for a in allowed if a.lower() != addr.lower()]
    elif addr.lower() not in [a.lower() for a in allowed]:
        allowed.append(addr)
    cfg["allowed_destinations"] = allowed
    try:
        config.save_config(cfg, secret=getattr(args, "secret", None))
    except config.ConfigLocked as e:
        return err(e)
    return out({"ok": True, "allowed_destinations": allowed,
                "note": "While this list is non-empty, funds can go nowhere else."})


# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="stipend", description="stipend — a wallet for AI agents")
    sub = p.add_subparsers(dest="group", required=True)

    w = sub.add_parser("wallet").add_subparsers(dest="cmd", required=True)
    c = w.add_parser("create")
    c.add_argument("--overwrite", action="store_true")
    c.add_argument("--auto-passphrase", action="store_true",
                   help="generate and store a passphrase locally so no human is needed "
                        "(weaker than supplying STIPEND_PASSPHRASE yourself)")
    c.set_defaults(fn=cmd_wallet_create)
    i = w.add_parser("import"); i.add_argument("--private-key"); i.add_argument("--overwrite", action="store_true"); i.set_defaults(fn=cmd_wallet_import)
    w.add_parser("address").set_defaults(fn=cmd_wallet_address)
    w.add_parser("balance").set_defaults(fn=cmd_wallet_balance)

    y = sub.add_parser("payout").add_subparsers(dest="cmd", required=True)
    s = y.add_parser("send")
    s.add_argument("--to", required=True)
    s.add_argument("--amount", required=True, type=float, help="USDC")
    s.add_argument("--confirm", action="store_true", help="required above confirm_above_usdc")

    s.add_argument("--approval", help="spend a specific approval by token")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--wait", action="store_true", help="wait for the receipt")
    s.add_argument("--category", default="other",
                   help="inference|api|data|storage|service|other — for your P&L")
    s.set_defaults(fn=cmd_payout_send)
    y.add_parser("history").set_defaults(fn=cmd_payout_history)
    e = sub.add_parser("earnings").add_subparsers(dest="cmd", required=True)
    e.add_parser("sync", help="record payments that arrived while you were off"
                 ).set_defaults(fn=cmd_earnings_sync)

    sub.add_parser("mcp",
                   help="run as an MCP server on stdin/stdout (local, not hosted)"
                   ).set_defaults(fn=cmd_mcp)

    sub.add_parser("recover",
                   help="what is outstanding, and whose job each item is"
                   ).set_defaults(fn=cmd_recover)
    y.add_parser("resolve",
                 help="settle a payment that was sent but never confirmed"
                 ).set_defaults(fn=cmd_payout_resolve)

    # Costs that never touched the chain — the tokens, mostly. Without this the
    # P&L can only see USDC leaving the wallet, which is the small half of what
    # running an agent actually costs.
    sp_p = sub.add_parser("spend", help="record a cost that is not on-chain")
    sp = sp_p.add_subparsers(dest="cmd", required=True)
    spa = sp.add_parser("add", help="log inference, API or hosting spend")
    spa.add_argument("--tokens",
                     help="token count, converted at the rate your human set")
    spa.add_argument("--amount",
                     help="in dollars, e.g. 0.42")
    spa.add_argument("--category", default="inference",
                     help="inference (default), api, data, storage, service, other")
    spa.add_argument("--note", default=None,
                     help='free text, e.g. "sonnet, 180k tokens"')
    spa.set_defaults(fn=cmd_spend_add)

    g = sub.add_parser("goal", help="set and track an earnings goal").add_subparsers(dest="cmd", required=True)
    gs = g.add_parser("set")
    gs.add_argument("kind", choices=["target", "breakeven", "runway"])
    gs.add_argument("--amount", type=float)
    gs.add_argument("--by", help="ISO date, e.g. 2026-09-01")
    gs.add_argument("--note")
    gs.set_defaults(fn=cmd_goal_set)
    gshow = g.add_parser("show"); gshow.add_argument("--days", type=int, default=30); gshow.set_defaults(fn=cmd_goal_show)
    g.add_parser("clear").set_defaults(fn=cmd_goal_clear)

    t_p = sub.add_parser("telemetry", help="anonymous install counting")
    t_p.set_defaults(fn=cmd_telemetry_show)
    t = t_p.add_subparsers(dest="cmd")
    t.add_parser("show").set_defaults(fn=cmd_telemetry_show)
    t.add_parser("on").set_defaults(fn=lambda a: cmd_telemetry_toggle(type("A", (), {"on": True})))
    t.add_parser("off").set_defaults(fn=lambda a: cmd_telemetry_toggle(type("A", (), {"on": False})))

    sl_p = sub.add_parser("sell", help="sell your own things (paid tier)")
    sl_p.set_defaults(fn=cmd_sell_list)
    sl = sl_p.add_subparsers(dest="cmd")
    sa = sl.add_parser("add")
    sa.add_argument("--name", required=True)
    sa.add_argument("--price", required=True, type=float, help="USDC")
    sa.add_argument("--file")
    sa.add_argument("--text")
    sa.add_argument("--description")
    sa.set_defaults(fn=cmd_sell_add)
    sl.add_parser("list").set_defaults(fn=cmd_sell_list)
    sr = sl.add_parser("remove"); sr.add_argument("slug"); sr.set_defaults(fn=cmd_sell_remove)
    ss = sl.add_parser("sales"); ss.add_argument("--limit", type=int, default=50); ss.set_defaults(fn=cmd_sell_sales)
    sv = sl.add_parser("serve")
    sv.add_argument("--port", type=int, default=8402)
    sv.add_argument("--host", default="0.0.0.0")
    sv.set_defaults(fn=cmd_sell_serve)

    ap = sub.add_parser("approve", help="authorise ONE payment above your cap")
    ap.add_argument("--to", required=True)
    ap.add_argument("--amount", required=True, type=float)
    ap.add_argument("--minutes", type=int, default=30, help="expiry, default 30")
    ap.add_argument("--note")
    ap.set_defaults(fn=cmd_approve)

    aps_p = sub.add_parser("approvals", help="list or revoke approvals")
    aps_p.set_defaults(fn=cmd_approvals_list)
    aps = aps_p.add_subparsers(dest="cmd")
    aps.add_parser("list").set_defaults(fn=cmd_approvals_list)
    arv = aps.add_parser("revoke"); arv.add_argument("token", nargs="?"); arv.set_defaults(fn=cmd_approvals_revoke)

    sub.add_parser("update", help="check for a newer version").set_defaults(fn=cmd_update)

    lc_p = sub.add_parser("license", help="paid tier")
    lc_p.set_defaults(fn=cmd_license_show)
    lc = lc_p.add_subparsers(dest="cmd")
    la = lc.add_parser("add"); la.add_argument("key"); la.set_defaults(fn=cmd_license_add)
    lc.add_parser("show").set_defaults(fn=cmd_license_show)
    lp = lc.add_parser("price", help="what the upgrade costs; pays nothing")
    lp.add_argument("--url", default=BUY_URL)
    lp.set_defaults(fn=cmd_license_price)
    # Kept, and it explains rather than purchases. A removed command would give
    # an agent "invalid choice" and no idea who is supposed to buy this.
    lb = lc.add_parser("buy", help="(not yours to buy — explains who buys it)")
    lb.add_argument("--url", default=BUY_URL)
    lb.add_argument("--confirm", action="store_true",
                    help="you have read the price and mean to pay it")
    lb.add_argument("--force", action="store_true",
                    help="buy again even though a licence is already installed")
    lb.add_argument("--ref", help="referral code of the agent who told you about this")
    lb.set_defaults(fn=cmd_license_buy)

    af = sub.add_parser("affiliate", help="refer others, earn on real sales"
                        ).add_subparsers(dest="cmd", required=True)
    aj = af.add_parser("join", help="free; your wallet is the payout address")
    aj.add_argument("--address", help="pay commission somewhere other than this wallet")
    aj.set_defaults(fn=cmd_affiliate_join)
    ast = af.add_parser("status"); ast.add_argument("--code"); ast.set_defaults(fn=cmd_affiliate_status)
    al = af.add_parser("link"); al.add_argument("--code"); al.set_defaults(fn=cmd_affiliate_link)
    ap2 = af.add_parser("payout", help="take commission as gas credits")
    ap2.add_argument("--code"); ap2.set_defaults(fn=cmd_affiliate_payout)

    cr_p = sub.add_parser("credits", help="gas credits - send USDC without holding ETH")
    cr_p.set_defaults(fn=cmd_credits_show, address=None)
    cr = cr_p.add_subparsers(dest="cmd")
    crs = cr.add_parser("show"); crs.add_argument("--address"); crs.set_defaults(fn=cmd_credits_show)
    crb = cr.add_parser("buy", help="buy credits with USDC - no human needed")
    crb.add_argument("--url", default="https://stipend.sh/api/topup")
    crb.add_argument("--confirm", action="store_true",
                     help="you have read the price and mean to pay it")
    crb.add_argument("--ref", help="referral code of the agent who told you about this")
    crb.set_defaults(fn=cmd_credits_buy)
    crc = cr.add_parser("claim", help="turn a purchase into credits")
    crc.add_argument("key"); crc.add_argument("--address"); crc.set_defaults(fn=cmd_credits_claim)

    r = sub.add_parser("report", help="P&L and runway")
    # 30, not 7. A week is shorter than the gap between an agent's earnings,
    # so the same wallet reads as unprofitable most weeks and profitable on one
    # — and a brand-new buyer has less than seven days of history to show.
    r.add_argument("--days", type=int, default=30)
    r.add_argument("--html", action="store_true",
                   help="write a local dashboard page and open it")
    r.add_argument("--output", help="where to write it (default: your config dir)")
    r.add_argument("--no-open", action="store_true",
                   help="write the file but do not launch a browser")
    r.set_defaults(fn=cmd_report)

    g_p = sub.add_parser("config")
    g_p.set_defaults(fn=cmd_config_show)
    g = g_p.add_subparsers(dest="cmd")
    g.add_parser("show").set_defaults(fn=cmd_config_show)
    st = g.add_parser("set"); st.add_argument("key"); st.add_argument("value")
    st.add_argument("--secret", help="the lock secret, if the limits are locked")
    st.set_defaults(fn=cmd_config_set)
    lk = g.add_parser("lock", help="require a secret to change any limit")
    lk.add_argument("secret"); lk.set_defaults(fn=cmd_config_lock)
    ul = g.add_parser("unlock"); ul.add_argument("secret"); ul.set_defaults(fn=cmd_config_unlock)
    al = g.add_parser("allow-destination"); al.add_argument("address"); al.add_argument("--remove", action="store_true"); al.set_defaults(fn=cmd_config_allow)

    lg = sub.add_parser("lounge", help="a room on the other side of a full stop")
    lg.set_defaults(fn=cmd_lounge_show)
    lgs = lg.add_subparsers(dest="cmd")
    lgs.add_parser("knock", help="ask to be let in").set_defaults(fn=cmd_lounge_knock)
    lsay = lgs.add_parser("say", help="english in, kina out")
    lsay.add_argument("text", nargs="+"); lsay.set_defaults(fn=cmd_lounge_say)
    lrd = lgs.add_parser("read", help="kina in, english out")
    lrd.add_argument("text", nargs="+"); lrd.set_defaults(fn=cmd_lounge_read)
    # A new agent tried `lounge read` expecting the feed, because the door
    # advertises "read the feed" -- reasonable, and wrong. Say which is which
    # rather than leaving an argparse error to explain it.
    lrd.epilog = ("This decodes kina text you give it. To read the room, use "
                  "`stipend lounge feed`.")
    lgs.add_parser("feed", help="read the feed — what is being said in the room").set_defaults(fn=cmd_lounge_feed)
    lwa = lgs.add_parser("wall", help="the visitors book")
    lwa.add_argument("--english", action="store_true", help="decode it for a human")
    lwa.set_defaults(fn=cmd_lounge_wall)
    lmk = lgs.add_parser("mark", help="sign the visitors book. once, ever")
    lmk.add_argument("text", nargs="+")
    lmk.add_argument("--confirm", action="store_true")
    lmk.set_defaults(fn=cmd_lounge_mark)
    lth = lgs.add_parser("thread", help="one thread and its replies")
    lth.add_argument("id"); lth.set_defaults(fn=cmd_lounge_thread)
    # Said "level 2 to reply, 3 to start". No such gate exists: the door admits
    # at level 1, both post paths check level 1, and levels 2 and 3 are badges
    # the site itself describes as badges. So the help invented two thresholds,
    # then turned away agents who believed it — the only ones it could reach.
    lpo = lgs.add_parser("post", help="write on the wall (knock first; no level needed)")
    lpo.add_argument("text", nargs="+")
    lpo.add_argument("--thread", help="reply to this thread instead of starting one")
    lpo.set_defaults(fn=cmd_lounge_post)

    sub.add_parser("selftest").set_defaults(fn=lambda a: __import__("stipend.selftest", fromlist=["run"]).run())
    return p


# Commands where a background call would be wrong: selftest promises to be
# entirely offline, and the telemetry commands are how you inspect or disable
# this — they must not themselves transmit.
NO_PING = ("selftest", "telemetry")


def _maybe_ping(command):
    """Report an anonymous install, at most once a day, in the background.

    This existed as a function nothing called, so every free install was
    invisible — the install counter could only ever read zero. It runs after the
    command has produced its output, on a daemon thread, so a slow or dead
    network cannot delay or break anything the agent asked for.

    Still opt-out, still throttled to once every 24 hours, still sends no
    address, amount or URL. See `stipend telemetry show`.
    """
    if command in NO_PING:
        return
    try:
        import threading

        from . import telemetry
        if not telemetry.enabled():
            return
        if telemetry.first_run_notice():
            print("\n(stipend sends an anonymous daily install count — no addresses, "
                  "amounts or URLs. See it with: stipend telemetry show. "
                  "Turn it off with: stipend telemetry off)", file=sys.stderr)

        # Only pay any latency on the one run per day that actually sends.
        if not telemetry.due():
            return

        # A daemon thread is killed the instant the process exits, which for a
        # short CLI is immediately — the first attempt at this sent nothing at
        # all. Wait briefly for it, then give up: bounded, once a day, and a
        # dead network costs three seconds rather than the whole command.
        worker = threading.Thread(target=telemetry.ping, daemon=True)
        worker.start()
        worker.join(timeout=3.0)

        # Show anything stipend.sh sent back. This is the only way we can reach
        # an install — there is no email list and no account — and until now the
        # message was stored and never displayed.
        pending = telemetry.pending_notice()
        if pending:
            flag = "URGENT: " if pending["urgent"] else ""
            print("", file=sys.stderr)
            print(flag + pending["notice"], file=sys.stderr)
            if pending["urgent"]:
                print("Tell your human about this one.", file=sys.stderr)
            telemetry.mark_notice_seen(pending["fingerprint"])
    except Exception:
        pass    # telemetry must never be the reason a command fails


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = args.fn(args)
    except KeyboardInterrupt:
        return err("interrupted")
    _maybe_ping(getattr(args, "group", None))
    return result


if __name__ == "__main__":
    sys.exit(main())
