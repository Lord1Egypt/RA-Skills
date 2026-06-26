#!/usr/bin/env python3
"""ShieldBot OpenClaw Skill — Format API responses into agent-readable text."""


def _risk_label(score):
    if score is None:
        return "UNKNOWN"
    if score <= 20:
        return "SAFE"
    if score <= 40:
        return "LOW RISK"
    if score <= 60:
        return "MEDIUM RISK"
    if score <= 80:
        return "HIGH RISK"
    return "CRITICAL"


def _trunc(addr, n=10):
    if not addr or len(addr) <= n + 4:
        return addr or "N/A"
    return f"{addr[:n]}...{addr[-4:]}"


def format_scan(data):
    score = data.get("risk_score", "N/A")
    level = data.get("risk_level", "unknown").upper()
    address = data.get("address", "N/A")
    chain = data.get("chain_id", "N/A")
    network = data.get("network", "N/A")
    verified = data.get("is_verified", "N/A")
    warnings = data.get("warnings", [])
    checks = data.get("checks", {})

    lines = []
    lines.append(f"Contract Scan: {address}")
    lines.append(f"Chain: {network} ({chain})")
    lines.append(f"Risk: {score}/100 ({_risk_label(score)})")
    lines.append(f"Risk Level: {level}")
    lines.append(f"Verified: {verified}")

    honeypot = checks.get("is_honeypot")
    if honeypot is True:
        lines.append("HONEYPOT: YES — Cannot sell tokens after buying!")
    elif honeypot is False:
        lines.append("Honeypot: No")

    ownership = checks.get("ownership_renounced")
    if ownership is not None:
        lines.append(f"Ownership Renounced: {ownership}")

    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for w in warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)


def format_simulate(data):
    classification = data.get("classification", "UNKNOWN")
    score = data.get("risk_score", "N/A")
    verdict = data.get("verdict", "")
    plain = data.get("plain_english", "")
    decoded = data.get("decoded_action", "")
    signals = data.get("danger_signals", [])
    deltas = data.get("asset_delta", [])

    lines = []
    lines.append(f"Transaction Analysis: {classification}")
    lines.append(f"Risk: {score}/100 ({_risk_label(score)})")
    if decoded:
        lines.append(f"Action: {decoded}")
    if verdict:
        lines.append(f"Verdict: {verdict}")
    if plain:
        lines.append(f"Recommendation: {plain}")

    if signals:
        lines.append("")
        lines.append("Danger Signals:")
        for s in signals:
            lines.append(f"  - {s}")

    if deltas:
        lines.append("")
        lines.append("Asset Changes:")
        for d in deltas:
            lines.append(f"  {d}")

    shield = data.get("shield_score", {})
    if shield:
        threat = shield.get("threat_type", "")
        confidence = shield.get("confidence", "")
        critical = shield.get("critical_flags", [])
        if threat:
            lines.append(f"Threat Type: {threat}")
        if confidence:
            lines.append(f"Confidence: {confidence}%")
        if critical:
            lines.append("Critical Flags:")
            for f in critical:
                lines.append(f"  - {f}")

    return "\n".join(lines)


def format_deployer(data):
    address = data.get("address", "N/A")
    deployer = data.get("deployer", "N/A")
    campaign = data.get("campaign", {})
    cross_chain = data.get("cross_chain_contracts", [])
    funder_cluster = data.get("funder_cluster", [])

    is_campaign = campaign.get("is_campaign", False)
    severity = campaign.get("severity", "NONE")
    total = campaign.get("total_contracts", 0)
    high_risk = campaign.get("high_risk_contracts", 0)
    indicators = campaign.get("indicators", [])
    chains = campaign.get("chains_involved", [])

    lines = []
    lines.append(f"Deployer Investigation: {address}")
    if deployer and deployer != address:
        lines.append(f"Deployed by: {deployer}")
    lines.append(f"Campaign Detected: {'YES' if is_campaign else 'No'}")
    lines.append(f"Severity: {severity}")
    lines.append(f"Total Contracts: {total}")
    lines.append(f"High Risk: {high_risk}")
    if chains:
        lines.append(f"Chains: {', '.join(str(c) for c in chains)}")

    if indicators:
        lines.append("")
        lines.append("Campaign Indicators:")
        for i in indicators:
            lines.append(f"  - {i}")

    if cross_chain:
        lines.append("")
        lines.append("Cross-Chain Contracts:")
        for c in cross_chain[:10]:
            risk = c.get("risk_score")
            arch = c.get("archetype", "")
            label = f"{_trunc(c.get('contract', ''))} chain:{c.get('chain_id', '?')}"
            if risk is not None:
                label += f" risk:{risk}"
            if arch:
                label += f" ({arch})"
            lines.append(f"  {label}")

    if funder_cluster:
        lines.append("")
        lines.append("Funder Cluster (same funder):")
        for f in funder_cluster[:10]:
            lines.append(
                f"  {_trunc(f.get('deployer', ''))} — "
                f"{f.get('contract_count', 0)} contracts, "
                f"{f.get('high_risk_contracts', 0)} high risk"
            )

    return "\n".join(lines)


def format_threats(data):
    threats = data.get("threats", [])
    count = data.get("count", 0)
    chain_filter = data.get("chain_id")

    lines = []
    header = "Threat Feed"
    if chain_filter:
        header += f" (chain {chain_filter})"
    lines.append(f"{header}: {count} threats")
    lines.append("")

    if not threats:
        lines.append("No threats found.")
        return "\n".join(lines)

    for t in threats:
        ttype = t.get("type", "unknown")
        chain = t.get("chain_id", "?")

        if ttype.startswith("mempool_"):
            severity = t.get("severity", "?")
            desc = t.get("description", "")
            attacker = _trunc(t.get("attacker_addr", ""))
            line = f"[{severity}] {ttype} — chain {chain}"
            if attacker and attacker != "N/A":
                line += f" | attacker: {attacker}"
            lines.append(line)
            if desc:
                lines.append(f"  {desc}")
        else:
            addr = _trunc(t.get("address", ""))
            risk = t.get("risk_score", "?")
            level = t.get("risk_level", "?")
            arch = t.get("archetype", "")
            line = f"[{level}] {ttype} — {addr} (chain {chain}, risk {risk})"
            if arch:
                line += f" [{arch}]"
            lines.append(line)

    return "\n".join(lines)


def format_phishing(data):
    is_phishing = data.get("is_phishing", False)
    confidence = data.get("confidence", "unknown")
    source = data.get("source", "N/A")

    lines = []
    if is_phishing:
        lines.append("PHISHING DETECTED")
        lines.append(f"Confidence: {confidence}")
        lines.append(f"Source: {source}")
        lines.append("Do NOT connect your wallet to this site.")
    else:
        lines.append("No phishing detected.")
        lines.append(f"Confidence: {confidence}")

    return "\n".join(lines)


def format_campaigns(data):
    campaigns = data.get("campaigns", [])
    count = data.get("count", 0)

    lines = []
    lines.append(f"Top Scam Campaigns: {count} deployers")
    lines.append("")

    if not campaigns:
        lines.append("No campaigns found.")
        return "\n".join(lines)

    for c in campaigns:
        deployer = _trunc(c.get("deployer", ""))
        contracts = c.get("contract_count", 0)
        chains = c.get("chain_count", 0)
        funder = _trunc(c.get("funder"))
        risk_profile = c.get("risk_profile", {})
        high = risk_profile.get("HIGH", 0)

        line = f"{deployer} — {contracts} contracts across {chains} chains"
        if high > 0:
            line += f", {high} HIGH risk"
        if funder and funder != "N/A":
            line += f" (funded by {funder})"
        lines.append(line)

    return "\n".join(lines)


def format_approvals(data):
    wallet = data.get("wallet", "N/A")
    chain = data.get("chain_id", "N/A")
    total = data.get("total_approvals", 0)
    high = data.get("high_risk", 0)
    medium = data.get("medium_risk", 0)
    value = data.get("total_value_at_risk_usd", 0)
    approvals = data.get("approvals", [])
    alerts = data.get("alerts", [])

    lines = []
    lines.append(f"Approval Audit: {wallet}")
    lines.append(f"Chain: {chain}")
    lines.append(f"Total Approvals: {total}")
    lines.append(f"High Risk: {high} | Medium Risk: {medium}")
    if value > 0:
        lines.append(f"Value at Risk: ${value:,.2f}")

    if alerts:
        lines.append("")
        lines.append("Alerts:")
        for a in alerts:
            sev = a.get("severity", "")
            title = a.get("title", "")
            desc = a.get("description", "")
            lines.append(f"  [{sev}] {title}")
            if desc:
                lines.append(f"    {desc}")

    risky = [a for a in approvals if a.get("risk_level") in ("HIGH", "MEDIUM")]
    if risky:
        lines.append("")
        lines.append("Risky Approvals:")
        for a in risky:
            symbol = a.get("token_symbol", "?")
            spender = _trunc(a.get("spender", ""))
            label = a.get("spender_label", "")
            level = a.get("risk_level", "")
            reason = a.get("risk_reason", "")
            allowance = a.get("allowance", "?")
            line = f"  [{level}] {symbol} → {spender}"
            if label:
                line += f" ({label})"
            line += f" | allowance: {allowance}"
            lines.append(line)
            if reason:
                lines.append(f"    Reason: {reason}")

    revokes = data.get("revoke_txs", [])
    if revokes:
        lines.append("")
        lines.append(f"Recommended Revocations: {len(revokes)}")
        for r in revokes:
            symbol = r.get("token_symbol", "?")
            spender = _trunc(r.get("spender", ""))
            label = r.get("spender_label", "")
            lines.append(f"  Revoke {symbol} from {spender} ({label})")

    return "\n".join(lines)


def format_ask(data):
    response = data.get("response", "No response.")
    scan_data = data.get("scan_data")

    lines = []
    lines.append(response)

    if scan_data:
        lines.append("")
        lines.append("--- Scan Data ---")
        addr = scan_data.get("address", "")
        score = scan_data.get("risk_score")
        level = scan_data.get("risk_level", "")
        arch = scan_data.get("archetype", "")
        flags = scan_data.get("flags", [])
        lines.append(f"Address: {addr}")
        if score is not None:
            lines.append(f"Risk: {score}/100 ({_risk_label(score)})")
        if level:
            lines.append(f"Level: {level}")
        if arch:
            lines.append(f"Archetype: {arch}")
        if flags:
            lines.append(f"Flags: {', '.join(flags)}")

    return "\n".join(lines)


FORMATTERS = {
    "scan": format_scan,
    "simulate": format_simulate,
    "deployer": format_deployer,
    "threats": format_threats,
    "phishing": format_phishing,
    "campaigns": format_campaigns,
    "approvals": format_approvals,
    "ask": format_ask,
}


def format_result(action, data):
    formatter = FORMATTERS.get(action)
    if not formatter:
        import json
        return json.dumps(data, indent=2)
    return formatter(data)
