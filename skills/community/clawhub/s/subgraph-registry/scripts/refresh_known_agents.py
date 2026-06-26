#!/usr/bin/env python3
"""Rebuild query 7507131 ('Identified agent payers') with a fresh
wallet → agent-identity directory.

Driven by actual payer wallets, not enumeration of registries.
For every wallet that has ever paid The Graph's x402 gateway on
Base, hit each registry by exact wallet — covering:

  • owner_address matches via 8004scan ?search=<wallet>
  • owner / agentWallet / operator matches via the agent0
    base-mainnet subgraph (graph.network)
  • static operator seed (Paul / GA wallets)
  • graphadvocate.com/bazaar/active (active x402 services)

Why payer-driven: 8004scan has 282k+ agents across many chains and
its default paginated listing surfaces Ethereum / BNB / Abstract
agents long before Base mainnet, so enumeration missed every Base
x402 payer. Searching by the payer wallet returns exact matches in
one round-trip each and works for both owner-paid and operator-paid
flows.

Optional env:
  BASE_RPC_URL   — Base RPC endpoint (defaults to https://mainnet.base.org)
  GRAPH_API_KEY  — used by the agent0 subgraph lookup; if missing, that
                   source is skipped (8004scan + seed + bazaar still work)
  PAYER_LOOKBACK_BLOCKS — how far back to scan for payers (default 1_500_000
                          blocks ≈ 35 days at Base's 2s block time)
  OUTPUT_PATH    — where to write SQL (default /tmp/known_agents_directory.sql)
"""

from __future__ import annotations
import json
import os
import sys
import time
import urllib.request
import urllib.error
from typing import Iterable

QUERY_ID = 7507131
GATEWAY_PAYTO = "0x79DC34E41B2b591078d3dE222C43EcaaBD52FcCB"
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
AGENT0_BASE_SUBGRAPH_ID = "43s9hQRurMGjuYnC1r2ZwS6xSQktbFyXMPMqGKUFJojb"

def _basescan(wallet: str) -> str:
    return f"https://basescan.org/address/{wallet}"


# 8004scan URL pattern is /agents/<chain-slug>/<token_id>, NOT the composite
# agent_id. Map known chain IDs to the slug their app uses (sniffed from the
# 8004scan home page link list).
_CHAIN_SLUG = {
    1: "ethereum",
    8453: "base",
    42161: "arbitrum",
    10: "optimism",
    56: "bsc",
    137: "polygon",
    42220: "celo",
    130: "unichain",
    1923: "swellchain",
    2741: "abstract",
    5042002: "ronin",
    84532: "base-sepolia",
    11155111: "sepolia",
}


def _scan8004(agent_id: str | None) -> str:
    """8004scan agent detail URL — translates the composite chain:contract:tokenId
    to /agents/<chain-slug>/<tokenId>. Falls back to the home page if the chain
    isn't mapped (rare; add to _CHAIN_SLUG when a new chain shows up)."""
    if not agent_id:
        return "https://8004scan.io"
    parts = agent_id.split(":")
    if len(parts) == 3 and parts[0].isdigit() and parts[2].isdigit():
        chain_id, _contract, token_id = parts
        slug = _CHAIN_SLUG.get(int(chain_id))
        if slug:
            return f"https://8004scan.io/agents/{slug}/{token_id}"
    return "https://8004scan.io"


# Graph Advocate's ERC-8004 identity on Base — agent #41034 on contract
# 0x8004a169fb4a3325136eb29fa0ceb6d2e539a432 (chain 8453).
# The same agent is also registered on Arbitrum as #734.
GA_8004_BASE_AGENT_ID = "8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:41034"

OPERATOR_SEED = [
    # (wallet, name, source, link)
    # All three GA-controlled wallets present as the same agent identity
    # — same name, same 8004scan link — to match the single-name format
    # the other identified agents use (Michaelgent, Clarabotagent, etc.).
    # graphadvocate.eth — identity wallet, holds GRT on Arbitrum, signs A2A
    ("0x575267eed09c338fae5716a486a7b58a5749a292", "graphadvocate", "operator",
     _scan8004(GA_8004_BASE_AGENT_ID)),
    # GA x402 outbound — pays bazaar endpoints
    ("0xe121e3a8611e1f44f7cc52892ee1117fddc8f734", "graphadvocate", "operator",
     _scan8004(GA_8004_BASE_AGENT_ID)),
    # GA x402 inbound — receives /route payments
    ("0x0ff5a6ecef783bba35463ec2f8403b9b5e9e7c86", "graphadvocate", "operator",
     _scan8004(GA_8004_BASE_AGENT_ID)),
]


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def fetch_json(url: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "x402-graph-dune-refresh/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def post_json(url: str, body: dict, timeout: int = 20) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "User-Agent": "x402-graph-dune-refresh/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


# ── Payer discovery (on-chain) ────────────────────────────────────────────────

def fetch_payers_from_chain() -> list[str]:
    """Pull distinct payer wallets to the gateway via Base RPC.

    Uses eth_getLogs over the last PAYER_LOOKBACK_BLOCKS blocks (default
    ~35 days). Public Base RPC works; set BASE_RPC_URL for a paid endpoint
    with higher limits.
    """
    rpc = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org")
    lookback = int(os.environ.get("PAYER_LOOKBACK_BLOCKS", "1500000"))
    try:
        tip_hex = post_json(rpc, {
            "jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": [],
        })["result"]
    except Exception as e:
        print(f"  eth_blockNumber failed: {e}", file=sys.stderr)
        return []
    tip = int(tip_hex, 16)
    from_block = max(0, tip - lookback)
    recv_topic = "0x" + "0" * 24 + GATEWAY_PAYTO[2:].lower()
    # Chunk into windows the RPC will accept (most caps at ~10k blocks).
    chunk = 10_000
    payers: set[str] = set()
    cur = from_block
    while cur <= tip:
        end = min(cur + chunk - 1, tip)
        try:
            res = post_json(rpc, {
                "jsonrpc": "2.0", "id": 1, "method": "eth_getLogs",
                "params": [{
                    "fromBlock": hex(cur),
                    "toBlock": hex(end),
                    "address": USDC_BASE,
                    "topics": [USDC_TRANSFER_TOPIC, None, recv_topic],
                }],
            }, timeout=30)
            for log in (res.get("result") or []):
                t = log.get("topics") or []
                if len(t) >= 2:
                    from_topic = t[1]
                    if isinstance(from_topic, str) and len(from_topic) >= 26:
                        payers.add("0x" + from_topic[-40:].lower())
        except Exception as e:
            print(f"  getLogs [{cur},{end}] failed: {e}", file=sys.stderr)
            # Continue past transient errors; small gaps are tolerable.
            time.sleep(1)
        cur = end + 1
    return sorted(payers)


# ── Identity registries ───────────────────────────────────────────────────────

def from_bazaar() -> list[tuple[str, str, str, str]]:
    """Pull active x402 services from GA's bazaar proxy."""
    try:
        d = fetch_json("https://graphadvocate.com/bazaar/active")
    except Exception as e:
        print(f"  bazaar fetch failed: {e}", file=sys.stderr)
        return []
    rows = []
    for it in d.get("results") or []:
        pay_to = (it.get("pay_to") or "").lower()
        resource = it.get("resource") or ""
        e8 = it.get("erc8004_agent") or {}
        name = e8.get("name") or e8.get("ens") or _hostname(resource) or "?"
        agent_id_full = e8.get("agent_id")  # e.g. "8453:0x8004…:47143"
        link = _scan8004(agent_id_full) if agent_id_full else _basescan(pay_to)
        if pay_to and pay_to.startswith("0x"):
            rows.append((pay_to, str(name), "bazaar", link))
        owner = (e8.get("owner") or "").lower()
        if owner and owner.startswith("0x") and owner != pay_to:
            rows.append((
                owner,
                f"ERC-8004 #{agent_id_full}" if agent_id_full else str(name),
                "erc8004",
                _scan8004(agent_id_full),
            ))
    return rows


def enrich_from_8004scan(wallet: str) -> tuple[str, str, str, str] | None:
    """Exact wallet → 8004scan agent lookup. Returns (wallet, name, source, link)
    only when 8004scan has an agent whose owner_address matches.
    """
    try:
        d = fetch_json(
            f"https://8004scan.io/api/v1/public/agents?search={wallet}", timeout=8,
        )
    except Exception as e:
        print(f"  8004scan search for {wallet[:10]}… failed: {e}", file=sys.stderr)
        return None
    for a in (d.get("data") or []):
        if (a.get("owner_address") or "").lower() != wallet.lower():
            continue  # search is fuzzy; pin to exact owner match
        name = a.get("name") or ""
        if not name or name.startswith("Agent #"):
            name = a.get("owner_ens") or ""
            if not name:
                continue
        chain = a.get("chain_id")
        agent_id_full = a.get("agent_id")  # "8453:0x8004…:47143"
        label = f"{name}" if chain == 8453 else f"{name} (chain {chain})"
        return (wallet.lower(), label, "8004scan", _scan8004(agent_id_full))
    return None


def enrich_from_agent0(wallet: str, api_key: str) -> tuple[str, str, str, str] | None:
    """Query the agent0-base-mainnet subgraph for any agent where the wallet
    is owner, agentWallet, OR an operator. Catches the operator-paid case
    that 8004scan's owner-only response misses.
    """
    import base64
    url = f"https://gateway.thegraph.com/api/{api_key}/subgraphs/id/{AGENT0_BASE_SUBGRAPH_ID}"
    # Schema note: the agent0 subgraph has NO top-level `operators` query.
    # `operators` is a [Bytes!]! field on the Agent type. Earlier versions of
    # this script queried `operators(first: 5, where: {address: $w})` and
    # silently failed every time with `Type Query has no field operators`,
    # so the agent0 source contributed 0 matches indefinitely. Use
    # `operators_contains` on the Agent filter instead — this captures the
    # operator-paid case 8004scan misses without needing a separate query.
    query = """
    query($w: Bytes!) {
      agents(first: 5, where: {or: [
        {owner: $w},
        {agentWallet: $w},
        {operators_contains: [$w]}
      ]}) {
        agentId owner agentWallet agentURI operators
      }
    }
    """
    try:
        d = post_json(url, {"query": query, "variables": {"w": wallet.lower()}}, timeout=15)
    except Exception as e:
        print(f"  agent0 query for {wallet[:10]}… failed: {e}", file=sys.stderr)
        return None
    # Surface GraphQL errors that come back as HTTP 200 — otherwise the
    # whole agent0 source silently no-ops (the bug we just fixed).
    if isinstance(d, dict) and d.get("errors"):
        msg = (d["errors"][0] or {}).get("message", "unknown")
        print(f"  agent0 query for {wallet[:10]}… GraphQL error: {msg[:120]}", file=sys.stderr)
        return None
    data = d.get("data") or {}
    agents = data.get("agents") or []
    for a in agents:
        if not a:
            continue
        agent_id = a.get("agentId")
        name = f"ERC-8004 #{agent_id}"
        uri = a.get("agentURI") or ""
        if uri.startswith("data:application/json;base64,"):
            try:
                meta = json.loads(base64.b64decode(uri.split(",", 1)[1]))
                if meta.get("name"):
                    name = meta["name"]
            except Exception:
                pass
        is_owner = (a.get("owner") or "").lower() == wallet.lower()
        is_agent_wallet = (a.get("agentWallet") or "").lower() == wallet.lower()
        if not (is_owner or is_agent_wallet):
            name = f"{name} (operator)"
        # Build the 8004scan composite ID for the link, since agent0 surfaces
        # the same agents but doesn't host its own per-agent UI.
        agent_id_full = f"8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:{agent_id}" if agent_id else None
        return (wallet.lower(), name, "agent0", _scan8004(agent_id_full))
    return None


def _hostname(url: str) -> str | None:
    try:
        from urllib.parse import urlparse
        h = urlparse(url).hostname
        return h.replace("www.", "") if h else None
    except Exception:
        return None


def dedupe(rows: Iterable[tuple[str, str, str, str]]) -> list[tuple[str, str, str, str]]:
    """Keep first occurrence per wallet (source order is priority)."""
    seen: dict[str, tuple[str, str, str, str]] = {}
    for wallet, name, source, link in rows:
        wallet_l = wallet.lower()
        if wallet_l in seen:
            continue
        # Escape single quotes in name/link for SQL.
        name_clean = name.replace("'", "''")
        link_clean = (link or "").replace("'", "''")
        seen[wallet_l] = (wallet_l, name_clean, source, link_clean)
    return list(seen.values())


SQL_TEMPLATE = """-- Payers to The Graph's x402 gateway with a confirmed identity in
-- 8004scan, the agent0 Base subgraph, the x402 Bazaar, or a manually
-- seeded operator list.
-- This SQL is regenerated daily by scripts/refresh_known_agents.py;
-- do not hand-edit the VALUES block — edit the script's OPERATOR_SEED
-- or extend its sources instead.
--
-- Directory size: {count} wallets ({sources})
-- Regenerated: {regenerated}
WITH payers AS (
  SELECT
    "from"          AS payer,
    COUNT(*)        AS payments,
    MAX(block_time) AS last_seen
  FROM tokens_base.transfers
  WHERE contract_address = {usdc}
    AND "to" = {gateway}
  GROUP BY 1
),
known_agents (wallet, agent_name, source, agent_link) AS (
  VALUES
{values}
)
SELECT
  -- Markdown-formatted clickable link; Dune table viz renders inline links.
  '[' || ka.agent_name || '](' || ka.agent_link || ')' AS agent,
  p.payer       AS wallet,
  p.payments,
  p.last_seen,
  ka.source     AS registry,
  ka.agent_link AS agent_link
FROM payers p
INNER JOIN known_agents ka
  ON LOWER(CAST(ka.wallet AS varchar)) = LOWER(CAST(p.payer AS varchar))
ORDER BY p.payments DESC
"""


def build_sql(rows: list[tuple[str, str, str, str]]) -> str:
    from datetime import datetime, timezone
    values_lines = []
    for wallet, name, source, link in rows:
        values_lines.append(f"    ({wallet}, '{name}', '{source}', '{link}')")
    values_sql = ",\n".join(values_lines) if values_lines else "    (NULL, NULL, NULL, NULL)"
    by_source: dict[str, int] = {}
    for _, _, src, _ in rows:
        by_source[src] = by_source.get(src, 0) + 1
    src_summary = ", ".join(f"{c} {s}" for s, c in sorted(by_source.items())) or "0"
    return SQL_TEMPLATE.format(
        count=len(rows),
        sources=src_summary,
        regenerated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        usdc=USDC_BASE,
        gateway=GATEWAY_PAYTO,
        values=values_sql,
    )


def main() -> None:
    print("Refreshing known-agent directory…")
    print(f"[1] Operator seed: {len(OPERATOR_SEED)} entries")

    print("[2] Bazaar /active fetch…")
    bazaar_rows = from_bazaar()
    print(f"    → {len(bazaar_rows)} rows")

    print("[3] Discovering payers via Base RPC…")
    payers = fetch_payers_from_chain()
    print(f"    → {len(payers)} distinct payer wallets in lookback window")

    print("[4] Enriching each payer via 8004scan + agent0 (per-wallet exact match)…")
    graph_key = os.environ.get("GRAPH_API_KEY", "").strip()
    if not graph_key:
        print("    GRAPH_API_KEY not set — agent0 subgraph source disabled")
    enriched: list[tuple[str, str, str, str]] = []
    n_8004 = n_agent0 = 0
    for wallet in payers:
        # Skip the gateway itself if it ever appears as payer (it shouldn't, but be safe).
        if wallet == GATEWAY_PAYTO.lower():
            continue
        row = enrich_from_8004scan(wallet)
        if row:
            enriched.append(row)
            n_8004 += 1
            continue
        if graph_key:
            row = enrich_from_agent0(wallet, graph_key)
            if row:
                enriched.append(row)
                n_agent0 += 1
    print(f"    → 8004scan matches: {n_8004}; agent0 matches: {n_agent0}")

    deduped = dedupe(OPERATOR_SEED + bazaar_rows + enriched)
    print(f"[5] Deduped union: {len(deduped)} wallets")

    sql = build_sql(deduped)
    output_path = os.environ.get("OUTPUT_PATH", "/tmp/known_agents_directory.sql")
    with open(output_path, "w") as f:
        f.write(sql)
    print(f"[6] SQL written to {output_path} ({len(sql)} chars)")
    print(f"[7] Caller: dune query update {QUERY_ID} --sql \"$(cat {output_path})\"")


if __name__ == "__main__":
    main()
