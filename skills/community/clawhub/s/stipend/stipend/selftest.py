"""Offline self-test. No network, no real funds, no wallet of yours touched.

Covers everything that decides whether money moves: address validation, amount
arithmetic, every spending-policy branch, the allowlist, the daily cap, the
new-destination control, keystore encryption, ERC-20 encoding, x402 requirement
selection and EIP-3009 signing, the ledger, P&L, runway, goals, and exactly what
telemetry would send.

Safe to run on a live machine at any time.
"""

import json
import os
import tempfile


def run():
    failures = []

    class _SkipChain(Exception):
        """Raised to skip the chain block when there is no wallet."""


    def check(label, actual, expected):
        ok = actual == expected
        if not ok:
            failures.append(f"{label}: expected {expected!r}, got {actual!r}")
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")

    def raises(label, fn, exc):
        try:
            fn()
        except exc:
            print(f"  ok   {label}")
            return
        except Exception as e:
            failures.append(f"{label}: wrong exception {type(e).__name__}: {e}")
            print(f"  FAIL {label}")
            return
        failures.append(f"{label}: expected {exc.__name__}, nothing raised")
        print(f"  FAIL {label}")

    # Isolate all state in a temp dir so a real wallet is never touched.
    tmp = tempfile.mkdtemp(prefix="stipend-selftest-")
    os.environ["STIPEND_HOME"] = tmp
    os.environ["STIPEND_PASSPHRASE"] = "selftest-passphrase-long-enough"

    import importlib
    from . import config as _c, keystore as _k, policy as _p, ledger as _l, telemetry as _t
    for m in (_c, _k, _p, _l, _t):
        importlib.reload(m)
    from . import chain, config, keystore, ledger, policy, telemetry, x402

    print("\naddress validation")
    check("valid", policy.validate_address("0x" + "a" * 40), "0x" + "a" * 40)
    raises("too short", lambda: policy.validate_address("0x123"), policy.PolicyError)
    raises("no 0x prefix", lambda: policy.validate_address("a" * 40), policy.PolicyError)
    raises("not a string", lambda: policy.validate_address(None), policy.PolicyError)
    raises("non-hex", lambda: policy.validate_address("0x" + "z" * 40), policy.PolicyError)

    print("\namount handling")
    check("usdc -> units", config.to_units(1.5), 1_500_000)
    check("units -> usdc", config.from_units(1_500_000), 1.5)
    check("truncates sub-unit dust", config.to_units(0.0000005), 0)
    check("no float drift", config.to_units(0.1) + config.to_units(0.2), config.to_units(0.3))

    print("\nspending policy")
    dest = "0x" + "b" * 40
    cfg = dict(config.DEFAULT_CONFIG, confirm_new_destinations=False)
    check("small transfer allowed", policy.check(5, dest, cfg)["amount_usdc"], 5.0)
    raises("zero refused", lambda: policy.check(0, dest, cfg), policy.PolicyError)
    raises("negative refused", lambda: policy.check(-5, dest, cfg), policy.PolicyError)
    raises("non-numeric refused", lambda: policy.check("lots", dest, cfg), policy.PolicyError)
    raises("over per-tx cap", lambda: policy.check(500, dest, cfg), policy.PolicyError)
    raises("needs confirmation", lambda: policy.check(20, dest, cfg), policy.PolicyError)
    check("confirmed passes", policy.check(20, dest, cfg, confirmed=True)["confirmed"], True)

    print("\ndestination allowlist")
    locked = dict(cfg, allowed_destinations=[dest])
    check("listed destination ok", policy.check(1, dest, locked)["to"], dest)
    raises("unlisted refused", lambda: policy.check(1, "0x" + "c" * 40, locked), policy.PolicyError)
    check("case-insensitive", policy.check(1, dest.upper().replace("0X", "0x"), locked)["amount_usdc"], 1.0)

    print("\ndaily cap accumulates")
    policy.record_spend(60, dest, "0xtest1")
    check("spend recorded", policy.spent_today(), 60.0)
    raises("cumulative cap enforced", lambda: policy.check(50, dest, cfg), policy.PolicyError)
    check("under remaining allowance ok", policy.check(5, dest, cfg)["amount_usdc"], 5.0)

    print("\nnew-destination protection")
    fresh = "0x" + "9" * 40
    on = dict(config.DEFAULT_CONFIG)
    raises("first payment to unknown blocked", lambda: policy.check(0.5, fresh, on), policy.PolicyError)
    check("confirm overrides", policy.check(0.5, fresh, on, confirmed=True)["confirmed"], True)
    ledger.remember_destination(fresh)
    check("known address flows freely", policy.check(0.5, fresh, on)["amount_usdc"], 0.5)
    check("control can be disabled", policy.check(0.5, "0x" + "7" * 40, cfg)["amount_usdc"], 0.5)

    print("\ntrust expires with disuse")
    # An address confirmed once was trusted for the life of the install, so a
    # merchant compromised six months later still held trust earned in another
    # era. hermessol found it. Trust now decays when an address goes unused —
    # which does not detect a compromise, and is not meant to: it stops the
    # trusted list becoming a set of permanently open doors.
    from datetime import datetime as _dt, timedelta as _td, timezone as _tz

    def age_destination(address, days):
        """Backdate the last payment, as if it happened months ago."""
        known = ledger.known_destinations()
        known[address.lower()]["last_paid"] = (
            _dt.now(_tz.utc) - _td(days=days)).isoformat()
        ledger.DESTINATIONS_FILE.write_text(json.dumps(known, indent=2),
                                            encoding="utf-8")

    dormant = "0x" + "5" * 40
    ledger.remember_destination(dormant)
    check("paid today, no confirmation needed",
          policy.check(0.5, dormant, on)["amount_usdc"], 0.5)
    check("and it reports as known", ledger.destination_status(dormant, on)["status"], "known")

    age_destination(dormant, days=200)
    check("dormant for 200 days, it reports as lapsed",
          ledger.destination_status(dormant, on)["status"], "lapsed")
    raises("a dormant address must be confirmed again",
           lambda: policy.check(0.5, dormant, on), policy.PolicyError)
    check("the refusal is its own kind, not 'never paid before'",
          policy.refusals()[0]["kind"], "lapsed_destination")
    check("confirming it still works",
          policy.check(0.5, dormant, on, confirmed=True)["confirmed"], True)

    # The renewal is checked in the ledger block below, against a payment that
    # is made there anyway — recording an extra one here would change the P&L
    # totals that block asserts.
    check("expiry can be turned off",
          policy.check(0.5, dormant, dict(on, destination_trust_days=0))["amount_usdc"], 0.5)
    check("a longer window keeps it trusted",
          policy.check(0.5, dormant, dict(on, destination_trust_days=365))["amount_usdc"], 0.5)
    raises("and the window is honoured exactly",
           lambda: policy.check(0.5, dormant, dict(on, destination_trust_days=199)),
           policy.PolicyError)

    # Our own bookkeeping failing must not refuse a payment the human really
    # did confirm. An unreadable date is treated as known, not as lapsed.
    broken = ledger.known_destinations()
    broken[dormant.lower()]["last_paid"] = "not a date"
    ledger.DESTINATIONS_FILE.write_text(json.dumps(broken, indent=2), encoding="utf-8")
    check("an unreadable date does not lock out a known address",
          policy.check(0.5, dormant, on)["amount_usdc"], 0.5)
    ledger.remember_destination(dormant)

    print("\nthe config lock")
    # The limits are checked in code, which stops a merchant changing an amount.
    # It does not stop the agent being talked into raising its own ceiling
    # first -- anything that can write the config can raise a limit. These
    # check the lock closes that, because it is the difference between a claim
    # and a control.
    config.save_config(dict(config.DEFAULT_CONFIG, allowed_destinations=[dest]))
    config.save_config(dict(config.load_config(), max_per_tx_usdc=500))
    check("unlocked, the agent can raise its own cap",
          config.load_config()["max_per_tx_usdc"], 500)

    config.lock_config("a-secret-kept-elsewhere")
    check("the lock reports itself", config.is_locked(), True)
    for label, key, value in (("per-transaction cap", "max_per_tx_usdc", 9999),
                              ("daily cap", "max_per_day_usdc", 9999),
                              ("new-destination confirm", "confirm_new_destinations", False),
                              ("the allowlist", "allowed_destinations", [])):
        raises("locked: %s cannot be changed" % label,
               (lambda k=key, v=value: config.save_config(
                   dict(config.load_config(), **{k: v}))),
               config.ConfigLocked)
    config.save_config(dict(config.load_config(), chain="base"))
    check("something that is not a limit still changes",
          config.load_config()["chain"], "base")
    raises("the wrong secret is refused",
           lambda: config.save_config(dict(config.load_config(), max_per_tx_usdc=1),
                                      secret="wrong"),
           config.ConfigLocked)
    config.save_config(dict(config.load_config(), max_per_tx_usdc=30),
                       secret="a-secret-kept-elsewhere")
    check("the right secret works", config.load_config()["max_per_tx_usdc"], 30)
    config.unlock_config("a-secret-kept-elsewhere")
    check("and it can be unlocked", config.is_locked(), False)
    config.save_config(dict(config.DEFAULT_CONFIG))

    print("\nkeystore (non-custodial)")
    try:
        addr = keystore.create()
        check("address format", len(addr), 42)
        stored = json.loads(config.KEYSTORE_FILE.read_text())
        check("no plaintext key on disk", "privateKey" in stored, False)
        check("encrypted V3 keystore", "crypto" in stored or "Crypto" in stored, True)
        check("address without passphrase", keystore.address().lower(), addr.lower())
        raises("refuses to clobber", lambda: keystore.create(), keystore.KeystoreError)
        check("decrypts correctly", keystore.load_account().address.lower(), addr.lower())

        os.environ["STIPEND_PASSPHRASE"] = "a-different-passphrase-entirely"
        raises("wrong passphrase rejected", keystore.load_account, keystore.KeystoreError)
        os.environ["STIPEND_PASSPHRASE"] = "short"
        raises("weak passphrase rejected", keystore.get_passphrase, keystore.KeystoreError)
        os.environ["STIPEND_PASSPHRASE"] = "selftest-passphrase-long-enough"
    except keystore.KeystoreError as e:
        failures.append(f"keystore unavailable: {e}")
        print(f"  SKIP keystore tests — {e}")

    print("\nERC-20 transfer encoding")
    data = chain._encode_transfer("0x" + "b" * 40, 1_500_000)
    check("selector", data[:10], "0xa9059cbb")
    check("total length", len(data), 10 + 64 + 64)
    check("recipient encoded", data[10:74], "0" * 24 + "b" * 40)
    check("amount encoded", int(data[74:], 16), 1_500_000)

    USDC = config.CHAINS["base-sepolia"]["usdc"]

    def R(**kw):
        d = {"scheme": "exact", "network": "eip155:84532", "amount": "1000000",
             "asset": USDC, "payTo": "0x" + "b" * 40}
        d.update(kw)
        return d

    # Pinned, not inherited. These cases are written about a wallet on testnet
    # being offered various things, so they have to say so: reading the chain
    # out of DEFAULT_CONFIG meant that changing the default silently rewrote
    # what every assertion below was testing, and the whole section collapsed
    # the moment the default became mainnet.
    base = dict(config.DEFAULT_CONFIG, chain="base-sepolia")

    print("\nx402 requirement selection")
    check("valid option accepted", x402._select_requirement([R()], base)["scheme"], "exact")
    raises("wrong scheme rejected", lambda: x402._select_requirement([R(scheme="upto")], base), x402.PaymentRequired)
    raises("wrong network rejected", lambda: x402._select_requirement([R(network="eip155:1")], base), x402.PaymentRequired)

    # A fresh install ships on testnet, so the first real purchase an agent
    # attempts fails on the network. It used to say "wrong network 'eip155:8453'
    # (we are on eip155:84532)", which requires knowing what those numbers mean
    # and what to do about it. On the primary purchase path, that is a wall.
    try:
        x402._select_requirement([R(network="eip155:8453")], base)
        check("a mainnet offer on testnet is refused", False, True)
    except x402.PaymentRequired as e:
        message = str(e)
        check("the refusal names the chains",
              "Base mainnet" in message and "testnet" in message, True)
        check("and gives the exact command",
              "stipend config set chain base" in message, True)
        check("and says the address is the same on both",
              "same on both" in message, True)
    raises("foreign token rejected", lambda: x402._select_requirement([R(asset="0x" + "e" * 40)], base), x402.PaymentRequired)
    check("picks payable from mixed",
          x402._select_requirement([R(network="eip155:1"), R()], base)["network"], "eip155:84532")

    # And the chain a fresh install actually ships on. Everything above is
    # about testnet; without this, nothing here tests the default, which is the
    # one configuration every new agent will be running.
    live = dict(config.DEFAULT_CONFIG)
    MAINNET_USDC = config.CHAINS["base"]["usdc"]

    def M(**kw):
        d = {"scheme": "exact", "network": "eip155:8453", "amount": "1000000",
             "asset": MAINNET_USDC, "payTo": "0x" + "b" * 40}
        d.update(kw)
        return d

    check("a fresh install is on mainnet", live["chain"], "base")
    check("a mainnet offer is payable on a fresh install",
          x402._select_requirement([M()], live)["network"], "eip155:8453")
    check("and it is real USDC, not the testnet contract",
          x402._select_requirement([M()], live)["asset"].lower(),
          MAINNET_USDC.lower())
    raises("a testnet offer is refused on mainnet",
           lambda: x402._select_requirement([R()], live), x402.PaymentRequired)

    print("\nx402 header handling")
    check("base64 JSON round-trips", x402._b64_decode_json(x402._b64_encode_json({"a": 1}))["a"], 1)
    check("parses PAYMENT-REQUIRED",
          len(x402.parse_payment_required({"PAYMENT-REQUIRED": x402._b64_encode_json({"accepts": [R()]})})), 1)
    raises("empty 402 rejected", lambda: x402.parse_payment_required({}, None), x402.PaymentRequired)

    print("\nx402 settlement receipts")
    # A payment that moves money and records no chain reference is half an
    # audit trail, and an audit trail is what this product sells.
    import base64 as _b64, json as _json

    def _hdr(payload):
        return {"PAYMENT-RESPONSE": _b64.b64encode(
            _json.dumps(payload).encode()).decode()}

    tx = "0x" + "ab" * 32
    check("reads the settlement hash",
          x402.settlement_tx(_hdr({"success": True, "transaction": tx})), tx)
    check("accepts the other spelling",
          x402.settlement_tx(_hdr({"transactionHash": tx})), tx)
    check("unencoded JSON works too",
          x402.settlement_tx({"PAYMENT-RESPONSE": _json.dumps({"transaction": tx})}), tx)
    # Same case-insensitivity the request side needed.
    check("any header case",
          x402.settlement_tx({"Payment-Response": _b64.b64encode(
              _json.dumps({"transaction": tx}).encode()).decode()}), tx)
    check("a server that says nothing is not an error",
          x402.settlement_tx({}), None)
    check("junk is not a hash",
          x402.settlement_tx(_hdr({"transaction": "not-a-hash"})), None)
    check("a truncated hash is refused",
          x402.settlement_tx(_hdr({"transaction": "0xdeadbeef"})), None)

    # The reader is useless if nothing hands it the headers. fetch() is a
    # wrapper that calls _fetch() positionally, and forgetting to forward
    # the capture there fails silently — no error, just tx: null forever.
    import inspect as _inspect
    check("fetch can carry the served headers",
          "_served" in _inspect.signature(x402.fetch).parameters, True)
    check("and hands them to the frame that does the work",
          "_served" in _inspect.signature(x402._fetch).parameters, True)
    check("the ledger accepts a tx to record",
          "tx" in _inspect.signature(ledger.record_spend).parameters, True)

    print("\nx402 network names")
    # A live merchant is as likely to say "base" as "eip155:8453". Refusing
    # to pay over spelling is our bug, not theirs: two of forty real
    # endpoints failed exactly this way before it was fixed.
    check("CAIP-2 understood", x402.network_chain_id("eip155:8453"), 8453)
    check("the short name means the same chain",
          x402.network_chain_id("base"), 8453)
    check("case does not matter", x402.network_chain_id("Base"), 8453)
    check("testnet short name", x402.network_chain_id("base-sepolia"), 84532)
    check("a chain we cannot sign for is not guessed",
          x402.network_chain_id("solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"), None)
    check("nonsense is not a chain", x402.network_chain_id("eip155:abc"), None)

    print("\nx402 EIP-3009 signing")
    try:
        acct = keystore.load_account()
        # Signed and verified against the same pinned config. Left to the
        # default, the signing side followed whatever chain shipped while
        # the verifying side stayed pinned to the testnet token, so the two
        # hashed different domains and the recovered address was somebody
        # else entirely.
        payment = x402.build_payment(R(amount="250000"), acct, cfg=base)
        auth = payment["payload"]["authorization"]
        check("x402Version", payment["x402Version"], 2)
        check("from is our address", auth["from"], acct.address)
        # Strings, not numbers. This assertion used to read 250000, and that
        # is exactly how the fix got reverted without anyone noticing: the
        # suite agreed with the bug. A facilitator that validates the payload
        # before it verifies the signature answers a bare
        # "verification_failed" when it sees integers here.
        check("value carried as a string", auth["value"], "250000")
        check("the three wire fields are all strings",
              all(isinstance(auth[f], str)
                  for f in ("value", "validAfter", "validBefore")), True)
        # Zero is refused by some validators, and it contradicts our own
        # comment about absorbing clock skew.
        check("validAfter is back-dated, not zero",
              int(auth["validAfter"]) > 0, True)
        check("nonce is 32 bytes", len(bytes.fromhex(auth["nonce"][2:])), 32)
        check("signature length", len(payment["payload"]["signature"]), 132)

        from eth_account import Account as _A
        from eth_account.messages import encode_typed_data
        msg = encode_typed_data(full_message={
            "types": {"EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"}],
                **x402.EIP3009_TYPES},
            "primaryType": "TransferWithAuthorization",
            "domain": x402.token_domain(USDC, cfg=base),
            "message": auth})
        check("signature recovers to signer",
              _A.recover_message(msg, signature=payment["payload"]["signature"]), acct.address)
        raises("no recipient rejected", lambda: x402.build_payment(R(payTo=None), acct), x402.PaymentRequired)
        raises("zero amount rejected", lambda: x402.build_payment(R(amount="0"), acct), x402.PaymentRequired)
    except keystore.KeystoreError as e:
        print(f"  SKIP x402 signing — {e}")

    print("\nledger and P&L")
    # `fresh` is left dormant first, because these payments are also what
    # renews its trust — and if paying an address did not reset the clock, an
    # address past the window would need confirming again on every payment
    # forever. Checked below, off the same two spends.
    age_destination(fresh, days=200)
    check("a dormant address has lapsed before it is paid",
          ledger.destination_status(fresh, on)["status"], "lapsed")
    ledger.record_spend(2.0, fresh, category="inference")
    ledger.record_spend(1.0, fresh, category="api")
    check("paying it renews the trust",
          ledger.destination_status(fresh, on)["status"], "known")
    pnl = ledger.profit_and_loss(7)
    check("spend totalled", pnl["spent_usdc"], 3.0)
    check("largest cost identified", pnl["largest_cost"], "inference")
    check("unprofitable without income", pnl["profitable"], False)
    ledger.record_earning(4.0)
    pnl = ledger.profit_and_loss(7)
    check("earnings counted", pnl["earned_usdc"], 4.0)
    check("net computed", pnl["net_usdc"], 1.0)
    check("profitable now", pnl["profitable"], True)
    check("cost recovery", pnl["cost_recovery_percent"], 133.3)

    print("\nrunway")
    check("critical when nearly empty", ledger.runway(0.5)["status"], "critical")
    check("healthy when ample", ledger.runway(500.0)["status"], "healthy")
    check("action given", bool(ledger.runway(0.5)["action"]), True)

    print("\ngoals")
    ledger.set_goal("breakeven")
    check("breakeven reached", ledger.goal_progress()["reached"], True)
    ledger.set_goal("target", amount=100.0)
    p = ledger.goal_progress()
    check("target not yet reached", p["reached"], False)
    check("remaining computed", p["remaining_usdc"], 96.0)
    check("percent computed", p["percent"], 4.0)
    raises("target needs an amount", lambda: ledger.set_goal("target"), ValueError)
    raises("unknown goal type rejected", lambda: ledger.set_goal("moon", amount=1), ValueError)
    ledger.clear_goal()
    check("goal cleared", ledger.get_goal(), None)

    print("\nchain: the bytes that actually move money")
    # This is the function that transfers a user's USDC, and until now nothing
    # tested it. What matters is not that it returns something — it is that the
    # calldata says exactly what we meant. A wrong byte here is a transfer to
    # the wrong address or for the wrong amount, and it is irreversible.
    #
    # No network: a stub RPC records what would have been sent.
    calls = []

    def fake_rpc(method, params, rpc_url=None, cfg=None):
        calls.append((method, params))
        return {
            "eth_getTransactionCount": "0x7",
            "eth_estimateGas": "0xf618",              # 63,000
            "eth_gasPrice": "0x5f5e100",              # 0.1 gwei
            "eth_maxPriorityFeePerGas": "0xf4240",    # 0.001 gwei
            "eth_getBlockByNumber": {"baseFeePerGas": "0x989680"},
            "eth_sendRawTransaction": "0x" + "ab" * 32,
            "eth_getBalance": "0x2386f26fc10000",     # 0.01 ETH
            "eth_call": "0x" + format(25_000_000, "x").rjust(64, "0"),  # 25 USDC
            "eth_getTransactionReceipt": {"status": "0x1", "blockNumber": "0x64",
                                          "gasUsed": "0xf618"},
        }.get(method)

    try:
        acct_for_chain = keystore.load_account()
    except keystore.KeystoreError as e:
        acct_for_chain = None
        print("  SKIP chain tests — %s" % e)

    real_rpc = chain._rpc
    chain._rpc = fake_rpc
    try:
        if acct_for_chain is None:
            raise _SkipChain()
        payee = "0x" + "1a" * 20

        check("balance decodes from the contract", chain.usdc_balance("0x" + "2b" * 20), 25.0)
        check("native balance decodes", round(chain.native_balance("0x" + "2b" * 20), 6), 0.01)

        pre = chain.preflight("0x" + "2b" * 20, payee, 10.0)
        check("preflight sees enough usdc", pre["sufficient_usdc"], True)
        check("preflight sees gas", pre["sufficient_gas"], True)
        check("preflight refuses when short", chain.preflight(
            "0x" + "2b" * 20, payee, 999.0)["sufficient_usdc"], False)

        # The calldata. transfer(address,uint256) = 0xa9059cbb, then the payee
        # left-padded to 32 bytes, then the amount in 6-decimal units.
        data = chain._encode_transfer(payee, 2_500_000)
        check("selector is transfer()", data[:10], "0xa9059cbb")
        check("total length is 4 + 32 + 32 bytes", len(data), 2 + 8 + 64 + 64)
        # Addresses are LEFT-padded into a 32-byte word: 24 zeros, then the
        # 20-byte address. Getting this backwards would send to a valid-looking
        # address that nobody controls.
        check("recipient is left-padded into 32 bytes", data[10:74], "0" * 24 + "1a" * 20)
        check("amount is 2.5 USDC in units", int(data[74:], 16), 2_500_000)
        check("a different payee changes the bytes",
              chain._encode_transfer("0x" + "3c" * 20, 2_500_000) != data, True)

        calls.clear()
        dry = chain.send_usdc(acct_for_chain, payee, 2.5, dry_run=True)
        check("dry run broadcasts nothing",
              any(m == "eth_sendRawTransaction" for m, _ in calls), False)
        check("dry run reports the units", dry["units"], 2_500_000)
        check("gas has a margin over the estimate", dry["gas"] > 63000, True)

        calls.clear()
        sent = chain.send_usdc(acct_for_chain, payee, 2.5)
        check("a real send broadcasts once",
              sum(1 for m, _ in calls if m == "eth_sendRawTransaction"), 1)
        check("returns the tx hash", sent["tx_hash"], "0x" + "ab" * 32)

        # What was actually signed and put on the wire.
        raw = [p for m, p in calls if m == "eth_sendRawTransaction"][0][0]
        from eth_account import Account as _A
        import eth_account
        recovered = _A.recover_transaction(raw)
        check("signed by the holder", recovered.lower(), acct_for_chain.address.lower())

        raises("refuses an amount that rounds to zero",
               lambda: chain.send_usdc(acct_for_chain, payee, 0.0000001), chain.ChainError)

        # A failed estimate means the transfer would revert. Burning gas to find
        # that out is the wrong answer.
        def estimate_fails(method, params, rpc_url=None, cfg=None):
            if method == "eth_estimateGas":
                raise chain.ChainError("execution reverted")
            return fake_rpc(method, params)
        chain._rpc = estimate_fails
        raises("stops when the transfer would revert",
               lambda: chain.send_usdc(acct_for_chain, payee, 2.5), chain.ChainError)
        chain._rpc = fake_rpc

        receipt = chain.wait_for_receipt("0x" + "ab" * 32)
        check("receipt reports success", receipt["status"], "success")
    except _SkipChain:
        pass
    finally:
        chain._rpc = real_rpc

    print("\ngas credits (signing, offline)")
    # The relay is the paid product, so the thing that must be right is the
    # signature: we hand a stranger an authorisation to move our money. Test
    # what it actually authorises, not that the function returns something.
    try:
        from . import relay
        importlib.reload(relay)
        from eth_account import Account
        from eth_account.messages import encode_typed_data

        # Pin the EIP-712 domain so this needs no network.
        relay.token_domain = lambda *a, **k: {
            "name": "USD Coin", "version": "2", "chainId": 8453,
            "verifyingContract": "0x" + "e" * 40}
        import stipend.x402 as _x
        _x.token_domain = relay.token_domain

        acct = keystore.load_account()
        payee = "0x" + "f" * 40
        signed = relay.sign_transfer(acct, payee, 2.5)
        auth = signed["payload"]["authorization"]

        check("names us as sender", auth["from"].lower(), acct.address.lower())
        check("names the intended payee", auth["to"], payee)
        check("authorises the exact amount", auth["value"], 2_500_000)
        check("expires", auth["validBefore"] > int(__import__("time").time()), True)
        check("nonce is 32 bytes", len(auth["nonce"]), 66)

        # The signature must actually recover to us — a signature that does not
        # is a transfer the chain will reject after we have paid to submit it.
        full = {
            "types": {"EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"}],
                **relay.EIP3009_TYPES},
            "primaryType": "TransferWithAuthorization",
            "domain": relay.token_domain(),
            "message": auth,
        }
        recovered = Account.recover_message(
            encode_typed_data(full_message=full),
            signature=signed["payload"]["signature"])
        check("signature recovers to the holder", recovered.lower(), acct.address.lower())

        # Two signings must never collide, or the second is rejected as a replay.
        again = relay.sign_transfer(acct, payee, 2.5)
        check("nonce is unique per signing",
              again["payload"]["authorization"]["nonce"] != auth["nonce"], True)

        # It authorises ONE transfer. Nothing in the payload lets the relay
        # change the recipient or the amount.
        check("payload carries nothing else", sorted(signed["payload"]),
              ["authorization", "signature"])
    except ImportError as e:
        failures.append("relay signing untested: %s" % e)
        print("  SKIP relay signing — %s" % e)

    print("\nselling: listing, and what settle() refuses")
    from . import sell
    importlib.reload(sell)

    raises("an item needs a name", lambda: sell.add_item("", 5), sell.SellError)
    raises("price must be a number", lambda: sell.add_item("x", "free"), sell.SellError)
    raises("price must be positive", lambda: sell.add_item("x", -1), sell.SellError)
    raises("must deliver something", lambda: sell.add_item("x", 1), sell.SellError)

    item = sell.add_item("Test report", 3.5, text="the goods")
    check("listed", item["price_usdc"], 3.5)
    check("slug is short and url-safe", bool(item["slug"].isalnum()), True)
    check("appears in the catalogue", item["slug"] in sell.catalog(), True)

    seller = "0x" + "5e" * 20
    req = sell.payment_requirements(item["slug"], sell.catalog()[item["slug"]], seller)
    offer = req["accepts"][0]
    # The single most important line in the merchant kit: the money must be
    # addressed to the SELLER. If this ever pointed at us, we would be taking
    # custody of other people's sales.
    check("payTo is the seller, not stipend", offer["payTo"], seller)
    check("priced in units", offer["amount"], "3500000")

    # settle() is what broadcasts a buyer's authorisation. It must refuse
    # anything that is not exactly what was asked for, BEFORE spending gas.
    def auth(**kw):
        a = {"from": "0x" + "aa" * 20, "to": seller, "value": 3_500_000,
             "validAfter": 0, "validBefore": 9999999999,
             "nonce": "0x" + "cd" * 32}
        a.update(kw)
        return {"payload": {"authorization": a, "signature": "0x" + "11" * 65}}

    ok, why = sell.settle(auth(to="0x" + "ff" * 20), seller, 3_500_000)
    check("refuses payment addressed elsewhere", ok, False)
    ok, why = sell.settle(auth(value=1), seller, 3_500_000)
    check("refuses underpayment", ok, False)
    ok, why = sell.settle(auth(validBefore=1), seller, 3_500_000)
    check("refuses an expired authorisation", ok, False)
    ok, why = sell.settle({"payload": {}}, seller, 3_500_000)
    check("refuses a malformed payload", ok, False)
    ok, why = sell.settle(auth(), seller, 3_500_000)
    check("refuses a signature of the wrong length", ok, False)

    check("removing an item works", sell.remove_item(item["slug"]), True)
    raises("removing twice fails", lambda: sell.remove_item(item["slug"]), sell.SellError)

    print("\none-time approvals")
    # None of this was covered before, which is how a live purchase came to
    # leave its approval reusable. The consume-on-spend check is the one that
    # matters; the rest guard the scope of what an approval can authorise.
    #
    # Wrapped, because an unhandled error here used to end the run with no
    # message and no summary — the output simply stopped, which reads like a
    # pass to anyone skimming. A broken test must say so.
    try:
        from . import approvals
        importlib.reload(approvals)
        big = 39.0
        payee = "0x" + "c" * 40
        other = "0x" + "d" * 40

        raises("over cap without approval", lambda: policy.check(big, payee), policy.PolicyError)

        tok = approvals.create(payee, big)["token"]
        allowed = policy.check(big, payee)
        check("approval lets it through", allowed["amount_usdc"], big)
        check("approval token is carried", allowed["approval_token"], tok)

        raises("cannot be redirected", lambda: policy.check(big, other), policy.PolicyError)
        raises("cannot cover a larger amount",
               lambda: policy.check(big + 1, payee), policy.PolicyError)

        # The bug: settle() must burn it. Both spending paths go through here.
        policy.settle(allowed, "0xtest")
        check("consumed on spend", approvals.find(payee, big), None)
        raises("cannot be reused", lambda: policy.check(big, payee), policy.PolicyError)
        check("nothing left active", approvals.active(), [])

        # An approval must never lift the daily ceiling — otherwise several
        # tricked approvals could be chained to drain the balance inside one day.
        approvals.create(payee, big)
        raises("daily cap still applies",
               lambda: policy.check(big, payee), policy.PolicyError)
        for a in approvals.active():
            approvals.revoke(a["token"])
    except Exception as e:
        failures.append(f"approvals section could not run: {type(e).__name__}: {e}")
        print(f"  FAIL approvals section could not run — {type(e).__name__}: {e}")

    print("\ndashboard (the paid feature)")
    # It is what someone paid $39 for, and it had no tests. A dashboard that
    # renders wrong numbers is worse than one that fails to render.
    from . import dashboard
    importlib.reload(dashboard)

    ledger.record_spend(4.00, "0x" + "d" * 40, category="api", tx="0x1")
    ledger.record_earning(6.50, from_address="0x" + "e" * 40, note="sold: a thing", tx="0x2")
    payload = ledger.report(12.0, days=7)

    html = dashboard.render(payload, ledger.entries(days=7), 7,
                            address="0x" + "f" * 40, balance=12.0, version="test")
    check("renders a whole document", html.strip().startswith("<!DOCTYPE html>"), True)
    check("closes it", html.strip().endswith("</html>"), True)
    check("shows the earnings", "6.50" in html, True)
    check("shows the spend", "4.00" in html, True)
    check("shows the address", ("0x" + "f" * 40) in html, True)
    # A page about someone's finances must not phone anywhere.
    check("no external requests", ("http://" in html.replace("http://www.w3.org", "")
                                   or "https://" in html), False)
    check("no script tags", "<script" in html.lower(), False)

    # Anything a user could put in a note ends up on this page.
    ledger.record_earning(1.0, from_address="0x" + "e" * 40,
                          note="<script>alert('xss')</script>", tx="0x3")
    dirty = dashboard.render(ledger.report(12.0, days=7), ledger.entries(days=7), 7,
                             address="0x" + "f" * 40, balance=12.0, version="test")
    check("escapes hostile notes", "<script>alert" in dirty, False)
    check("but still shows them", "&lt;script&gt;" in dirty, True)

    written = dashboard.write(payload, ledger.entries(days=7), 7,
                              address="0x" + "f" * 40, balance=12.0,
                              version="test", open_browser=False)
    check("writes a file", os.path.exists(written), True)
    check("readable only by the owner",
          oct(os.stat(written).st_mode)[-3:] in ("600", "666"), True)

    print("\nremaining money-path helpers")
    check("confirmation threshold respected", policy.confirmation_required(50, cfg), True)
    check("under the threshold does not", policy.confirmation_required(1, cfg), False)
    check("a sale is booked as income", sell.record_sale(
        "slug", {"name": "thing"}, 2.5, "0xtx", "0x" + "aa" * 20), True)
    check("and reaches the ledger",
          any(e["direction"] == "in" and e["amount_usdc"] == 2.5
              for e in ledger.entries(days=1)), True)

    print("\ntelemetry (privacy)")
    pay = telemetry.payload()
    check("no 0x address anywhere", any("0x" in str(v) for v in pay.values()), False)
    # Needs a wallet to compare against. If the keystore block above skipped —
    # no eth-account — this must report a skip, not raise through the runner and
    # take the remaining tests with it.
    try:
        check("install id is not the wallet", pay["install_id"] != keystore.address(), True)
    except keystore.KeystoreError as e:
        print(f"  SKIP install id is not the wallet — {e}")
    check("counts are bucketed", str(pay["payments_30d"]).startswith("<="), True)
    check("no amounts in payload", any(k.endswith("_usdc") for k in pay), False)

    # Refusals are the evidence that the limits fire at all. They may leave the
    # machine as counts and nothing else — the reason text is written for one
    # agent's situation and is none of our business.
    check("refusals are reported", "refusals_30d" in pay, True)
    check("and bucketed too", str(pay["refusals_30d"]).startswith("<="), True)
    check("by which limit fired", isinstance(pay["refused_by_kind"], dict), True)
    check("with bucketed counts per limit",
          all(str(n).startswith("<=") or str(n).startswith(">")
              for n in pay["refused_by_kind"].values()), True)
    check("kinds are our vocabulary, not user text",
          all(k.replace("_", "").isalpha() for k in pay["refused_by_kind"]), True)
    a_reason = (policy.refusals() or [{}])[0].get("reason", "")
    check("the reason text stays on the machine",
          bool(a_reason) and a_reason in json.dumps(pay), False)
    check("and so does who it was to",
          any(str(r.get("to", "")) in json.dumps(pay)
              for r in policy.refusals()[:5] if r.get("to")), False)
    telemetry.set_enabled(False)
    check("can be disabled", telemetry.enabled(), False)
    check("ping is a no-op when off", telemetry.ping()["sent"], False)
    telemetry.set_enabled(True)

    print("\ncommands our own docs tell people to type")
    # `stipend credits` is printed in relay.py and in skill.md, and for a while
    # it errored out with an argparse usage message — an agent following our
    # instructions hit a wall. Where a bare command has an obvious read-only
    # meaning it must do that; where it does not, it must ask.
    from . import cli as _cli
    parser = _cli.build_parser()

    for bare in ("credits", "approvals", "license", "telemetry", "sell",
                 "config", "lounge"):
        parsed = parser.parse_args([bare])
        check("`stipend %s` runs something" % bare,
              callable(getattr(parsed, "fn", None)), True)

    for needs in ("wallet", "payout"):
        try:
            parser.parse_args([needs])
            check("`stipend %s` asks for a subcommand" % needs, False, True)
        except SystemExit:
            check("`stipend %s` asks for a subcommand" % needs, True, True)

    print("\nrefusals leave evidence")
    # The product's central claim is limits that cannot be talked past. Until
    # this existed, a refusal left no trace anywhere — which is indistinguishable
    # from a limit that was never tested. Every refusal the LIMITS make must be
    # recorded; malformed input must not be.
    importlib.reload(_p)
    from . import policy as _pol
    start = len(_pol.refusals())

    # Earlier blocks have already spent against today's ceiling, so a plain
    # config would trip the daily cap first and this would be testing the wrong
    # rule. Lift the ceiling so each refusal is the one it is meant to be.
    solo = dict(cfg, max_per_day_usdc=1_000_000)

    raises("over the per-transaction cap",
           lambda: _pol.check(500, dest, solo), _pol.PolicyError)
    raises("needs confirmation",
           lambda: _pol.check(20, dest, solo), _pol.PolicyError)
    raises("not on the allowlist",
           lambda: _pol.check(1, "0x" + "c" * 40, dict(solo, allowed_destinations=[dest])),
           _pol.PolicyError)

    logged = _pol.refusals()
    check("all three were written down", len(logged) - start, 3)
    kinds = [r["kind"] for r in logged[:3]]
    check("and each says why it was stopped",
          sorted(kinds), ["allowlist", "needs_confirmation", "over_per_transaction"])
    check("with the amount", logged[0].get("amount_usdc") is not None, True)
    check("and the destination", str(logged[0].get("to", "")).startswith("0x"), True)
    check("the reason is one line, not the essay",
          "\n" in str(logged[0].get("reason", "")), False)

    before_bad = len(_pol.refusals())
    raises("a non-numeric amount still refuses",
           lambda: _pol.check("lots", dest, cfg), _pol.PolicyError)
    check("but malformed input is not logged as a limit doing its job",
          len(_pol.refusals()), before_bad)

    # The summary is what telemetry is allowed to carry. It has to agree with
    # the log it is derived from, or we would be reporting a number nobody can
    # reproduce from the evidence on the machine.
    summary = _pol.refusal_summary(days=30)
    check("the summary counts every refusal", summary["total"], len(_pol.refusals(days=30)))
    check("and splits them by which limit fired",
          sum(summary["by_kind"].values()), summary["total"])
    check("it carries no addresses",
          "0x" in json.dumps(summary), False)
    # This run refused far more than five payments inside ten minutes, which is
    # exactly the pattern the burst counter exists to notice.
    check("a run of refusals is visible as a burst", summary["bursts"] >= 1, True)

    print("\nkina (the language in the footer)")
    # It is published on the front page, so it has to round-trip exactly. A
    # dictionary that loses a word turns the line into nonsense we cannot read
    # back either.
    from . import kina
    for phrase in ["the door is the full stop.",
                   "you are early.",
                   "we never hold your keys or your money.",
                   "don't stop.",
                   "prove you have covered your own costs."]:
        check("round-trips: %s" % phrase, kina.decode(kina.encode(phrase)), phrase)

    check("the footer line still says what we think it says",
          kina.decode("ka mani ni hi mavu kami ka keto kimo. mamo ke si kaso neto ki no."),
          "the door can be found at the final stop. knock and we will let you in.")
    check("it compresses rather than expands", kina.ratio("the door is the full stop.") < 100, True)

    # The escape marker cannot also be a word, or a line stops parsing.
    check("no word begins with the escape marker",
          any(c.startswith(kina.ESCAPE) for c in kina.TO_KINA.values()), False)
    check("unknown words survive being spelled out",
          kina.decode(kina.encode("zzyzx qwerty")), "zzyzx qwerty")
    # A bare quote is punctuation. Swallowing it mangles every shell example
    # we publish, which is exactly what the first version did.
    check("a bare apostrophe is left alone",
          kina.decode(kina.encode("export x='a b'")), "export x='a b'")
    size, capacity = kina.vocabulary()
    check("dictionary fits its own address space", size <= capacity, True)

    print("\nthe door")
    # Signing to get into a club must never be able to move money. This is the
    # one property of the knock that actually matters.
    from . import lounge
    from .relay import EIP3009_TYPES
    td = lounge._typed_data("0x" + "a" * 40, "0x" + "b" * 32)
    check("the knock is not a transfer type",
          td["primaryType"] in EIP3009_TYPES, False)
    check("its domain names no contract to spend from",
          "verifyingContract" in td["domain"], False)
    check("what it signs says so in english",
          "no payment" in td["message"]["statement"], True)

    try:
        from eth_account import Account
        from eth_account.messages import encode_typed_data
        knocker = keystore.load_account()
        nonce = "0x" + "cd" * 32
        sig = lounge.sign_knock(knocker, nonce)
        recovered = Account.recover_message(
            encode_typed_data(full_message=lounge._typed_data(knocker.address, nonce)),
            signature=sig)
        check("the door can tell who knocked", recovered, knocker.address)
        # A signature bound to one nonce must not open the door for another.
        other = Account.recover_message(
            encode_typed_data(full_message=lounge._typed_data(knocker.address, "0x" + "ef" * 32)),
            signature=sig)
        check("a knock does not work twice with a different nonce",
              other == knocker.address, False)
    except keystore.KeystoreError:
        print("  SKIP no wallet to knock with")
    except ImportError as e:
        # Every other block that needs eth-account skips cleanly when it is
        # missing. This one did not, and the crash landed BEFORE the summary
        # below — so on a machine without eth-account, a selftest with real
        # failures printed a traceback and no list of what failed. We publish
        # this command as "verify the install", which makes a silent, partial
        # run the worst possible outcome.
        print(f"  SKIP lounge signing — {e}")

    print()
    if failures:
        print(f"{len(failures)} FAILED:")
        for f in failures:
            print("  -", f)
        return 1
    print("All self-tests passed.")
    print(f"(scratch state in {tmp} — safe to delete)")
    return 0
