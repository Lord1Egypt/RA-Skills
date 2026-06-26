#!/usr/bin/env python3
"""
Settlement Predictor — Real-time on-chain settlement prediction for EVM chains & Bitcoin.

Supported chains: Ethereum, Arbitrum, Optimism, Base, Polygon, Bitcoin
Zero API keys required for core features (gas, settlement, mempool, tx tracking).
Optional: ETHERSCAN_API_KEY (contract verification, token metadata, internal txs, revert reasons)
Optional: TENDERLY_API_KEY (transaction simulation)
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# ── third-party ──────────────────────────────────────────────────────────────
try:
    import requests
except ImportError:
    sys.stderr.write("Error: `requests` is required. Install via: pip install requests\n")
    sys.exit(1)

try:
    from web3 import Web3
    from web3.exceptions import BlockNotFound, TransactionNotFound
except ImportError:
    sys.stderr.write("Error: `web3` is required (>=6.0.0). Install via: pip install web3\n")
    sys.exit(1)

# ── constants ─────────────────────────────────────────────────────────────────

CACHE_DIR = Path.home() / ".cache" / "settlement-predictor"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = CACHE_DIR / "gas_history.db"

# Public RPC endpoints (rate-limit friendly)
RPC_ENDPOINTS: Dict[str, str] = {
    "ethereum":   "https://eth.llamarpc.com",
    "arbitrum":   "https://arb1.arbitrum.io/rpc",
    "optimism":   "https://mainnet.optimism.io",
    "base":       "https://mainnet.base.org",
    "polygon":    "https://polygon-rpc.com",
}

# Chain metadata: (chain_id, symbol, block_time_sec, explorer_base)
CHAIN_META: Dict[str, Tuple[int, str, float, str]] = {
    "ethereum":   (1,     "ETH",  12.0,  "https://etherscan.io"),
    "arbitrum":   (42161, "ETH",   0.25,  "https://arbiscan.io"),
    "optimism":   (10,    "ETH",   2.0,   "https://optimistic.etherscan.io"),
    "base":       (8453,  "ETH",   2.0,   "https://basescan.org"),
    "polygon":    (137,   "MATIC", 2.0,   "https://polygonscan.com"),
}

# mempool.space public endpoints (no key needed)
MEMPOOL_ENDPOINTS = [
    "https://mempool.space/api/v1",
    "https://mempool.space/api",
]

# Etherscan-style base URLs (for optional API calls)
ETHERSCAN_BASE: Dict[str, str] = {
    "ethereum":   "https://api.etherscan.io/api",
    "arbitrum":   "https://api.arbiscan.io/api",
    "optimism":   "https://api-optimistic.etherscan.io/api",
    "base":       "https://api.basescan.org/api",
    "polygon":    "https://api.polygonscan.com/api",
}

BTC_RELAY = "https://mempool.space/api"


# ── enums ─────────────────────────────────────────────────────────────────────

class Urgency(str, Enum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"
    INSTANT = "instant"


class OutputFormat(str, Enum):
    JSON  = "json"
    TABLE = "table"


# ── dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class GasPrediction:
    chain: str
    timestamp: str
    current_gas_gwei: float
    estimated_gas_gwei: Dict[str, float]  # slow/standard/fast/instant
    base_fee_gwei: Optional[float]
    priority_fee_gwei: Optional[float]
    pending_block: Optional[int]
    network_congestion: str  # low/medium/high/severe
    confidence: str  # low/medium/high
    source: str  # rpc/mempool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SettlementPrediction:
    chain: str
    timestamp: str
    input_gas_gwei: float
    deadline_blocks: int
    estimated_blocks_to_finality: int
    estimated_time_seconds: float
    estimated_settlement_time: str
    confidence: str
    risk_level: str  # low/medium/high
    cost_wei: Optional[float] = None
    cost_usd_approx: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OptimalWindow:
    chain: str
    timestamp: str
    urgency: str
    target_minutes: Optional[float]
    recommended_fee_gwei: float
    wait_blocks: int
    estimated_time_seconds: float
    estimated_finality_time: str
    confidence: str
    warning: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PendingPoolAnalysis:
    chain: str
    timestamp: str
    pool_address: str
    direction: str  # buy/sell
    amount_usd: float
    gas_environment: str
    pool_congestion_score: float  # 0-1
    sandwich_risk: str  # none/low/medium/high
    price_impact_bps: float
    net_cost_usd: float
    recommendation: str
    confidence: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TxTracker:
    chain: str
    timestamp: str
    tx_hash: str
    status: str  # pending/confirmed/failed/not_found
    block_number: Optional[int]
    confirmations: int
    gas_used: Optional[int]
    gas_limit: Optional[int]
    effective_gas_price_gwei: Optional[float]
    base_fee_gwei: Optional[float]
    priority_fee_gwei: Optional[float]
    settled_in_blocks: Optional[int]
    settled_in_seconds: Optional[float]
    settlement_time: Optional[str]
    nonce: Optional[int]
    from_address: Optional[str]
    to_address: Optional[str]
    value_eth: Optional[float]
    explorer_url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ContractVerification:
    chain: str
    address: str
    timestamp: str
    is_verified: bool
    contract_name: Optional[str]
    compiler_version: Optional[str]
    optimizer_enabled: Optional[bool]
    optimization_runs: Optional[int]
    abi: Optional[List[Dict]]
    source_code_available: bool
    license: Optional[str]
    verified_at: Optional[str]
    explorer_url: str
    note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TokenInfo:
    chain: str
    address: str
    timestamp: str
    symbol: str
    name: str
    decimals: int
    total_supply: Optional[str]
    contract_type: Optional[str]
    price_usd: Optional[float]
    holder_count: Optional[int]
    transfer_count_24h: Optional[int]
    is_verified: bool
    explorer_url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InternalTx:
    tx_hash: str
    chain: str
    timestamp: str
    block_number: int
    from_address: str
    to_address: Optional[str]
    value_wei: str
    call_type: str
    gas_used: Optional[int]
    success: bool
    error: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BtcFeeEstimate:
    timestamp: str
    urgency: str
    sat_per_vbyte: Dict[str, float]  # fastest/half_hour/hour/two_hours/economical
    estimated_blocks: Dict[str, int]
    mempool_depth_mb: Optional[float]
    congestion_level: str  # low/normal/high/extreme
    confidence: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BtcSettlementPrediction:
    timestamp: str
    sat_per_vbyte: float
    urgency: str
    estimated_blocks: int
    estimated_minutes: float
    estimated_settlement_time: str
    confidence: str
    risk_level: str
    cost_sats: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BtcOptimalWindow:
    timestamp: str
    urgency: str
    recommended_sat_vb: float
    estimated_blocks: int
    estimated_minutes: float
    estimated_settlement_time: str
    confidence: str
    warning: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BtcTxTracker:
    txid: str
    timestamp: str
    status: str  # unconfirmed/confirmed/not_found
    confirmed: bool
    block_height: Optional[int]
    confirmations: int
    fee_sats: Optional[int]
    fee_rate_sat_vb: Optional[float]
    vsize: Optional[int]
    weight_units: Optional[int]
    estimated_broadcast_time: Optional[str]
    first_seen_unix: Optional[int]
    settled_in_blocks: Optional[int]
    settled_in_minutes: Optional[float]
    settlement_time: Optional[str]
    mempool_url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GasTrendAnalysis:
    chain: str
    timestamp: str
    window_hours: int
    current_gas_gwei: float
    avg_gas_gwei: float
    min_gas_gwei: float
    max_gas_gwei: float
    std_dev: float
    volatility: str  # low/medium/high
    trend_direction: str  # rising/falling/stable
    trend_pct_change: float
    data_points: int
    forecast_1h_gwei: Optional[float]
    forecast_4h_gwei: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BtcTrendAnalysis:
    timestamp: str
    window_hours: int
    current_fee_sat_vb: float
    avg_fee_sat_vb: float
    min_fee_sat_vb: float
    max_fee_sat_vb: float
    std_dev: float
    mempool_txs: int
    mempool_size_mb: float
    volatility: str
    trend_direction: str
    trend_pct_change: float
    data_points: int
    forecast_1h_sat_vb: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SimulatedTx:
    chain: str
    timestamp: str
    to_address: str
    value_eth: float
    success: bool
    gas_used: Optional[int]
    gas_limit: Optional[int]
    return_value: Optional[str]
    revert_reason: Optional[str]
    state_changes: List[Dict[str, Any]]
    logs: List[Dict[str, Any]]
    explorer_url: str
    note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ── database ─────────────────────────────────────────────────────────────────

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    _init_db(conn)
    return conn


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gas_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chain       TEXT NOT NULL,
            timestamp   TEXT NOT NULL,
            slow        REAL,
            standard    REAL,
            fast        REAL,
            instant     REAL,
            base_fee    REAL,
            block_num   INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS btc_fee_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            fastest     REAL,
            half_hour   REAL,
            hour        REAL,
            two_hours   REAL,
            economical  REAL,
            mempool_mb  REAL,
            mempool_txs INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            expires_at REAL NOT NULL
        )
    """)
    # indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_gas_chain_time ON gas_history(chain, timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_btc_time ON btc_fee_history(timestamp)")
    conn.commit()


def cache_get(key: str) -> Optional[str]:
    try:
        conn = get_db()
        cur = conn.execute(
            "SELECT value FROM cache WHERE key=? AND expires_at>?",
            (key, time.time())
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception:
        return None


def cache_set(key: str, value: str, ttl_seconds: int = 60) -> None:
    try:
        conn = get_db()
        conn.execute(
            "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
            (key, value, time.time() + ttl_seconds)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


# ── helpers ───────────────────────────────────────────────────────────────────

def _http_get(url: str, params: Optional[Dict] = None, timeout: int = 10) -> Optional[Dict]:
    try:
        r = requests.get(url, params=params, timeout=timeout, headers={
            "Accept": "application/json",
            "User-Agent": "settlement-predictor/1.0"
        })
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _post_json(url: str, data: Dict, timeout: int = 10) -> Optional[Dict]:
    try:
        r = requests.post(url, json=data, timeout=timeout, headers={
            "Accept": "application/json",
            "User-Agent": "settlement-predictor/1.0"
        })
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def gwei_to_wei(gwei: float) -> int:
    return int(gwei * 1e9)


def wei_to_gwei(wei: float) -> float:
    return wei / 1e9


def format_time(ts: Optional[float] = None) -> str:
    if ts is None:
        ts = time.time()
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_table(headers: List[str], rows: List[List[str]]) -> str:
    if not rows:
        return "No data available."
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    lines = []
    lines.append("  ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)))
    lines.append("  ".join("-" * w for w in col_widths))
    for row in rows:
        lines.append("  ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(row)))
    return "\n".join(lines)


def congestion_level(blocks_in_mempool: Optional[int] = None,
                     base_fee_gwei: Optional[float] = None,
                     priority_fee_gwei: Optional[float] = None) -> str:
    if blocks_in_mempool is None and base_fee_gwei is None:
        return "unknown"
    score = 0
    if blocks_in_mempool is not None:
        if blocks_in_mempool > 5000:
            score += 3
        elif blocks_in_mempool > 2000:
            score += 2
        elif blocks_in_mempool > 500:
            score += 1
    if priority_fee_gwei is not None:
        if priority_fee_gwei > 50:
            score += 2
        elif priority_fee_gwei > 20:
            score += 1
    if score >= 4:
        return "severe"
    elif score >= 3:
        return "high"
    elif score >= 2:
        return "medium"
    elif score >= 1:
        return "low"
    return "low"


def confidence_score(blocks_in_mempool: Optional[int] = None) -> str:
    if blocks_in_mempool is None:
        return "low"
    if blocks_in_mempool > 2000:
        return "high"
    elif blocks_in_mempool > 500:
        return "medium"
    return "low"


# ── EVM utilities ─────────────────────────────────────────────────────────────

def get_web3(chain: str) -> Optional[Web3]:
    rpc = RPC_ENDPOINTS.get(chain)
    if not rpc:
        return None
    try:
        w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))
        if w3.is_connected():
            return w3
        return None
    except Exception:
        return None


def get_etherscan_api_key() -> Optional[str]:
    return os.environ.get("ETHERSCAN_API_KEY")


def get_tenderly_api_key() -> Optional[str]:
    return os.environ.get("TENDERLY_API_KEY")


def _eth_get_gas_prices(chain: str) -> Optional[GasPrediction]:
    w3 = get_web3(chain)
    if not w3:
        return None
    try:
        latest = w3.eth.get_block("latest")
        base_fee = wei_to_gwei(latest.get("baseFeePerGas", 0))
        pending_block = latest.get("number")

        # get recent txs count as congestion proxy
        block_count = 20
        recent_txs = 0
        for i in range(max(1, pending_block - block_count), pending_block + 1):
            try:
                b = w3.eth.get_block(i)
                recent_txs += len(b.get("transactions", []))
            except Exception:
                pass

        avg_txs_per_block = recent_txs / block_count if block_count > 0 else 1

        # estimate priority fees via suggested tips
        try:
            priority_fee = w3.eth.max_priority_fee
            priority_fee_gwei = wei_to_gwei(priority_fee) if priority_fee else None
        except Exception:
            priority_fee_gwei = None

        # congestion estimate
        if avg_txs_per_block > 150:
            congestion = "severe"
        elif avg_txs_per_block > 100:
            congestion = "high"
        elif avg_txs_per_block > 50:
            congestion = "medium"
        else:
            congestion = "low"

        # fee tiers (gwei)
        pf = priority_fee_gwei if priority_fee_gwei else 2.0
        slow = max(base_fee * 0.8 + pf * 0.5, base_fee + 0.5)
        standard = base_fee + pf
        fast = base_fee + pf * 2
        instant = base_fee + pf * 4

        pred = GasPrediction(
            chain=chain,
            timestamp=format_time(),
            current_gas_gwei=standard,
            estimated_gas_gwei={
                "slow": round(slow, 2),
                "standard": round(standard, 2),
                "fast": round(fast, 2),
                "instant": round(instant, 2),
            },
            base_fee_gwei=round(wei_to_gwei(base_fee), 2) if base_fee else None,
            priority_fee_gwei=round(priority_fee_gwei, 2) if priority_fee_gwei else None,
            pending_block=pending_block,
            network_congestion=congestion,
            confidence=confidence_score(avg_txs_per_block * 10),
            source="rpc",
        )
        _store_gas_history(chain, pred)
        return pred
    except Exception as e:
        sys.stderr.write(f"get_eth_gas_prices error ({chain}): {e}\n")
        return None


def _store_gas_history(chain: str, pred: GasPrediction) -> None:
    try:
        conn = get_db()
        conn.execute(
            """INSERT INTO gas_history (chain, timestamp, slow, standard, fast, instant, base_fee, block_num)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                chain,
                pred.timestamp,
                pred.estimated_gas_gwei.get("slow"),
                pred.estimated_gas_gwei.get("standard"),
                pred.estimated_gas_gwei.get("fast"),
                pred.estimated_gas_gwei.get("instant"),
                pred.base_fee_gwei,
                pred.pending_block,
            )
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_gas_trend_data(chain: str, window_hours: int = 24) -> List[Tuple[float, str]]:
    try:
        conn = get_db()
        cutoff = format_time(time.time() - window_hours * 3600)
        rows = conn.execute(
            """SELECT standard, timestamp FROM gas_history
               WHERE chain=? AND timestamp>=? ORDER BY timestamp ASC""",
            (chain, cutoff)
        ).fetchall()
        conn.close()
        return [(r[0], r[1]) for r in rows]
    except Exception:
        return []


def predict_settlement_eth(chain: str, gas_price_gwei: float,
                           deadline_blocks: int) -> Optional[SettlementPrediction]:
    w3 = get_web3(chain)
    if not w3:
        return None
    try:
        chain_id, symbol, block_time, _ = CHAIN_META[chain]
        latest = w3.eth.get_block("latest")
        base_fee = wei_to_gwei(latest.get("baseFeePerGas", 0))

        # estimate how many blocks will fit within deadline
        recent_avg = 1.0
        block_count = 10
        pending = latest.get("number", 0)
        total_txs = 0
        for i in range(max(1, pending - block_count), pending + 1):
            try:
                b = w3.eth.get_block(i)
                total_txs += len(b.get("transactions", []))
            except Exception:
                pass
        recent_avg = total_txs / block_count if block_count > 0 else 1

        # blocks to finality estimate based on congestion
        if recent_avg > 150:
            blocks_to_finality = max(1, deadline_blocks // 3)
            risk = "high"
        elif recent_avg > 80:
            blocks_to_finality = max(1, deadline_blocks // 2)
            risk = "medium"
        else:
            blocks_to_finality = max(1, deadline_blocks)
            risk = "low"

        blocks_to_finality = min(blocks_to_finality, deadline_blocks)
        est_seconds = blocks_to_finality * block_time
        finality_time = format_time(time.time() + est_seconds)

        cost_wei = gwei_to_wei(gas_price_gwei) * 21000
        conf = "high" if recent_avg < 80 else "medium" if recent_avg < 150 else "low"

        return SettlementPrediction(
            chain=chain,
            timestamp=format_time(),
            input_gas_gwei=gas_price_gwei,
            deadline_blocks=deadline_blocks,
            estimated_blocks_to_finality=blocks_to_finality,
            estimated_time_seconds=est_seconds,
            estimated_settlement_time=finality_time,
            confidence=conf,
            risk_level=risk,
            cost_wei=cost_wei,
        )
    except Exception as e:
        sys.stderr.write(f"predict_settlement_eth error: {e}\n")
        return None


def _optimal_window_eth(chain: str, urgency: str,
                        target_minutes: Optional[float] = None) -> Optional[OptimalWindow]:
    w3 = get_web3(chain)
    if not w3:
        return None
    try:
        chain_id, symbol, block_time, _ = CHAIN_META[chain]
        latest = w3.eth.get_block("latest")
        base_fee = wei_to_gwei(latest.get("baseFeePerGas", 0))
        try:
            priority_fee_gwei = wei_to_gwei(w3.eth.max_priority_fee)
        except Exception:
            priority_fee_gwei = 2.0

        urgency_multipliers = {
            "low": 1.0, "medium": 1.5, "high": 2.5, "instant": 5.0
        }
        mult = urgency_multipliers.get(urgency, 1.5)

        if target_minutes:
            target_blocks = max(1, int(target_minutes / block_time))
            wait_blocks = target_blocks
        else:
            wait_blocks = max(1, int(mult))

        # estimate fee that gets into next N blocks
        rec_fee = base_fee + priority_fee_gwei * mult
        est_seconds = wait_blocks * block_time
        finality_time = format_time(time.time() + est_seconds)

        congestion_vals = {"low": "low", "medium": "medium", "high": "high", "instant": "severe"}
        congestion = congestion_vals.get(urgency, "medium")

        warning = None
        if urgency == "instant" and base_fee > 100:
            warning = "Network extremely congested. Instant may still take several minutes."

        return OptimalWindow(
            chain=chain,
            timestamp=format_time(),
            urgency=urgency,
            target_minutes=target_minutes,
            recommended_fee_gwei=round(rec_fee, 2),
            wait_blocks=wait_blocks,
            estimated_time_seconds=est_seconds,
            estimated_finality_time=finality_time,
            confidence="medium",
            warning=warning,
        )
    except Exception as e:
        sys.stderr.write(f"_optimal_window_eth error: {e}\n")
        return None


# ── Bitcoin utilities ─────────────────────────────────────────────────────────

def _mempool_get(endpoint: str, path: str, timeout: int = 10) -> Optional[Dict]:
    url = f"{endpoint}{path}"
    try:
        r = requests.get(url, timeout=timeout, headers={
            "Accept": "application/json",
            "User-Agent": "settlement-predictor/1.0"
        })
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _mempool_get_fee_estimates() -> Optional[Dict]:
    for ep in MEMPOOL_ENDPOINTS:
        data = _mempool_get(ep, "/v1/fees/recommended")
        if data:
            return data
    return None


def _mempool_get_mempool_info() -> Optional[Dict]:
    for ep in MEMPOOL_ENDPOINTS:
        data = _mempool_get(ep, "/v1/mempool")
        if data:
            return data
    return None


def btc_fee_estimate(urgency: str) -> Optional[BtcFeeEstimate]:
    try:
        fees = _mempool_get_fee_estimates()
        mempool_info = _mempool_get_mempool_info()

        urgency_map = {
            "low": "economical",
            "medium": "hour",
            "high": "halfHour",
            "instant": "fastest",
        }
        key = urgency_map.get(urgency, "hour")

        sat_vb = {
            "fastest":    round(fees.get("fastestFee", 10), 2),
            "half_hour":  round(fees.get("halfHourFee", 5), 2),
            "hour":       round(fees.get("hourFee", 3), 2),
            "two_hours":  round(fees.get("twoHourFee", 2), 2),
            "economical": round(fees.get("economyFee", 1), 2),
        }

        blocks_map = {
            "fastest":    1,
            "half_hour":  3,
            "hour":       6,
            "two_hours":  12,
            "economical": 24,
        }

        mempool_mb = None
        mempool_txs = None
        if mempool_info:
            mempool_mb = round(mempool_info.get("vsize_mb", 0), 2)
            mempool_txs = mempool_info.get("count", 0)

        # congestion level
        if mempool_mb:
            if mempool_mb > 100:
                congestion = "extreme"
            elif mempool_mb > 50:
                congestion = "high"
            elif mempool_mb > 10:
                congestion = "normal"
            else:
                congestion = "low"
        else:
            congestion = "normal"

        # confidence
        conf = "high" if mempool_info and mempool_info.get("count", 0) > 500 else "medium"

        est = BtcFeeEstimate(
            timestamp=format_time(),
            urgency=urgency,
            sat_per_vbyte=sat_vb,
            estimated_blocks=blocks_map,
            mempool_depth_mb=mempool_mb,
            congestion_level=congestion,
            confidence=conf,
        )
        _store_btc_fee_history(est)
        return est
    except Exception as e:
        sys.stderr.write(f"btc_fee_estimate error: {e}\n")
        return None


def _store_btc_fee_history(est: BtcFeeEstimate) -> None:
    try:
        conn = get_db()
        conn.execute(
            """INSERT INTO btc_fee_history (timestamp, fastest, half_hour, hour, two_hours, economical, mempool_mb, mempool_txs)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                est.timestamp,
                est.sat_per_vbyte.get("fastest"),
                est.sat_per_vbyte.get("half_hour"),
                est.sat_per_vbyte.get("hour"),
                est.sat_per_vbyte.get("two_hours"),
                est.sat_per_vbyte.get("economical"),
                est.mempool_depth_mb,
                est.mempool.get("count") if est.mempool_depth_mb is not None else None,
            )
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def btc_predict_settlement(sat_per_vbyte: float, urgency: str) -> Optional[BtcSettlementPrediction]:
    try:
        fees = _mempool_get_fee_estimates()
        mempool_info = _mempool_get_mempool_info()

        # find nearest block estimate
        fee_map = {
            "fastest":    (fees.get("fastestFee", 10), 1),
            "half_hour":  (fees.get("halfHourFee", 5), 3),
            "hour":       (fees.get("hourFee", 3), 6),
            "two_hours":  (fees.get("twoHourFee", 2), 12),
            "economical": (fees.get("economyFee", 1), 24),
        }

        urgency_blocks = {
            "low": 24, "medium": 6, "high": 3, "instant": 1
        }
        est_blocks = urgency_blocks.get(urgency, 6)

        # scale blocks by relative fee
        if sat_per_vbyte > 0:
            # find which tier this sat/vb falls near
            for tier_name, (tier_fee, tier_blocks) in sorted(fee_map.items(), key=lambda x: x[1][0]):
                if sat_per_vbyte >= tier_fee * 0.8:
                    est_blocks = tier_blocks
                    break

        est_minutes = est_blocks * 10  # ~10 min per BTC block
        finality_time = format_time(time.time() + est_minutes * 60)

        risk = "low"
        if est_blocks <= 1:
            risk = "medium"
        if mempool_info and mempool_info.get("vsize_mb", 0) > 100:
            risk = "high"

        # cost estimate for a typical 250vB tx
        cost_sats = int(sat_per_vbyte * 250)

        return BtcSettlementPrediction(
            timestamp=format_time(),
            sat_per_vbyte=sat_per_vbyte,
            urgency=urgency,
            estimated_blocks=est_blocks,
            estimated_minutes=est_minutes,
            estimated_settlement_time=finality_time,
            confidence="medium",
            risk_level=risk,
            cost_sats=cost_sats,
        )
    except Exception as e:
        sys.stderr.write(f"btc_predict_settlement error: {e}\n")
        return None


def btc_optimal_window(urgency: str) -> Optional[BtcOptimalWindow]:
    try:
        fees = _mempool_get_fee_estimates()
        mempool_info = _mempool_get_mempool_info()

        urgency_recs = {
            "low":      ("economyFee", 24, "medium"),
            "medium":   ("hourFee", 6, "medium"),
            "high":     ("halfHourFee", 3, "high"),
            "instant":  ("fastestFee", 1, "high"),
        }

        fee_key, blocks, conf = urgency_recs.get(urgency, ("hourFee", 6, "medium"))
        sat_vb = round(fees.get(fee_key, 3), 2)
        est_minutes = blocks * 10
        finality_time = format_time(time.time() + est_minutes * 60)

        warning = None
        if mempool_info and mempool_info.get("vsize_mb", 0) > 80:
            warning = f"Mempool very full ({mempool_info['vsize_mb']:.0f} MB). Consider higher fees."
        elif mempool_info and mempool_info.get("vsize_mb", 0) > 40:
            warning = f"Mempool moderately full ({mempool_info['vsize_mb']:.0f} MB)."

        return BtcOptimalWindow(
            timestamp=format_time(),
            urgency=urgency,
            recommended_sat_vb=sat_vb,
            estimated_blocks=blocks,
            estimated_minutes=est_minutes,
            estimated_settlement_time=finality_time,
            confidence=conf,
            warning=warning,
        )
    except Exception as e:
        sys.stderr.write(f"btc_optimal_window error: {e}\n")
        return None


def track_btc_tx(txid: str) -> Optional[BtcTxTracker]:
    try:
        for ep in MEMPOOL_ENDPOINTS:
            data = _mempool_get(ep, f"/tx/{txid}")
            if not data:
                continue

            status = data.get("status", {})
            confirmed = status.get("confirmed", False)
            block_height = status.get("block_height") if confirmed else None
            confirmations = 0
            if confirmed and block_height:
                # get current height
                current = _mempool_get(ep, "/v1/blocks/tip/height")
                if current:
                    confirmations = int(current) - block_height + 1

            fee = data.get("fee")
            vin_count = len(data.get("vin", []))
            vout_count = len(data.get("vout", []))
            weight = data.get("weight", 0)
            vsize = data.get("vsize", weight // 4)
            fee_rate = round(fee / vsize * 1000, 2) if fee and vsize else None

            first_seen = data.get("status", {}).get("block_time")
            settled_in_blocks = None
            settled_in_minutes = None
            settlement_time = None
            if confirmed and first_seen:
                settled_in_minutes = (data["status"]["block_time"] - data["status"].get("first_seen", data["status"]["block_time"])) * 60
                settlement_time = datetime.fromtimestamp(
                    data["status"]["block_time"], tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")

            tx_status = "confirmed" if confirmed else "unconfirmed"
            if not data:
                tx_status = "not_found"

            return BtcTxTracker(
                txid=txid,
                timestamp=format_time(),
                status=tx_status,
                confirmed=confirmed,
                block_height=block_height,
                confirmations=confirmations,
                fee_sats=int(fee * 1e8) if fee else None,
                fee_rate_sat_vb=fee_rate,
                vsize=vsize,
                weight_units=weight,
                estimated_broadcast_time=datetime.fromtimestamp(
                    data["status"].get("first_seen", 0), tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ") if data.get("status", {}).get("first_seen") else None,
                first_seen_unix=data.get("status", {}).get("first_seen"),
                settled_in_blocks=settled_in_blocks,
                settled_in_minutes=settled_in_minutes,
                settlement_time=settlement_time,
                mempool_url=f"https://mempool.space/tx/{txid}",
            )
        return None
    except Exception as e:
        sys.stderr.write(f"track_btc_tx error: {e}\n")
        return None


# ── pending pool analysis ─────────────────────────────────────────────────────

def analyze_pending_pool(chain: str, pool_address: str, direction: str,
                          amount_usd: float) -> Optional[PendingPoolAnalysis]:
    """
    Rough pending pool analysis based on gas environment and pool heuristics.
    No MEV API required — uses public RPC + fee data.
    """
    w3 = get_web3(chain)
    if not w3:
        return None
    try:
        # basic gas environment check
        latest = w3.eth.get_block("latest")
        base_fee = wei_to_gwei(latest.get("baseFeePerGas", 0))
        pending_block = latest.get("number")

        recent_txs = 0
        block_count = 5
        for i in range(max(1, pending_block - block_count), pending_block + 1):
            try:
                b = w3.eth.get_block(i)
                recent_txs += len(b.get("transactions", []))
            except Exception:
                pass

        avg_txs = recent_txs / block_count
        congestion_score = min(avg_txs / 200, 1.0)

        # simple pool heuristics
        direction_lower = direction.lower()
        is_buy = direction_lower in ("buy", "swap_in", "add")
        is_sell = direction_lower in ("sell", "swap_out", "remove")

        # price impact rough estimate
        if is_buy:
            price_impact_bps = max(1, min(50, amount_usd / 10000 * 15))
        elif is_sell:
            price_impact_bps = max(1, min(30, amount_usd / 10000 * 10))
        else:
            price_impact_bps = 5.0

        # sandwich risk based on gas + amount
        sandwich_risk = "none"
        if amount_usd > 10000 and base_fee > 50:
            sandwich_risk = "high"
        elif amount_usd > 5000 and base_fee > 20:
            sandwich_risk = "medium"
        elif amount_usd > 2000:
            sandwich_risk = "low"

        # gas environment
        if congestion_score > 0.7:
            gas_env = "congested"
        elif congestion_score > 0.4:
            gas_env = "moderate"
        else:
            gas_env = "healthy"

        # net cost rough estimate
        gas_cost_usd = base_fee * 21000 / 1e9 * _eth_usd_price(chain)
        net_cost = gas_cost_usd + (amount_usd * 0.003 if amount_usd > 1000 else 0)

        # recommendation
        if sandwich_risk == "high":
            rec = f"High sandwich risk. Split into smaller chunks or use flashbots."
        elif gas_env == "congested":
            rec = f"Gas high ({base_fee:.1f} gwei). Wait for lower base fee or use layer-2."
        elif is_buy and price_impact_bps > 30:
            rec = f"Large price impact ({price_impact_bps:.0f} bps). Consider splitting order."
        else:
            rec = "Proceed. Monitor for unfavorable slippage."

        conf = "medium" if congestion_score < 0.7 else "low"

        return PendingPoolAnalysis(
            chain=chain,
            timestamp=format_time(),
            pool_address=pool_address,
            direction=direction,
            amount_usd=amount_usd,
            gas_environment=gas_env,
            pool_congestion_score=round(congestion_score, 3),
            sandwich_risk=sandwich_risk,
            price_impact_bps=round(price_impact_bps, 2),
            net_cost_usd=round(net_cost, 4),
            recommendation=rec,
            confidence=conf,
        )
    except Exception as e:
        sys.stderr.write(f"analyze_pending_pool error: {e}\n")
        return None


def _eth_usd_price(chain: str) -> float:
    """Very rough ETH/USD from coingecko public API."""
    cache_key = f"eth_price_{chain}"
    cached = cache_get(cache_key)
    if cached:
        try:
            return float(cached)
        except Exception:
            pass
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
            timeout=5,
        )
        price = r.json().get("ethereum", {}).get("usd", 2500.0)
        cache_set(cache_key, str(price), ttl_seconds=60)
        return price
    except Exception:
        return 2500.0  # fallback


# ── tx tracker ────────────────────────────────────────────────────────────────

def track_tx(chain: str, tx_hash: str) -> Optional[TxTracker]:
    w3 = get_web3(chain)
    if not w3:
        return None
    try:
        chain_id, symbol, block_time, explorer = CHAIN_META[chain]
        explorer_url = f"{explorer}/tx/{tx_hash}"

        receipt = None
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            pass

        if receipt:
            status = "confirmed" if receipt.get("status") == 1 else "failed"
            block_num = receipt.get("blockNumber")
            gas_used = receipt.get("gasUsed")
            gas_limit = None
            try:
                tx = w3.eth.get_transaction(tx_hash)
                gas_limit = tx.get("gas")
            except Exception:
                pass

            effective_gas_price = wei_to_gwei(receipt.get("effectiveGasPrice", 0))
            latest_block = w3.eth.get_block("latest")
            current_block = latest_block.get("number", 0)
            confirmations = max(0, current_block - block_num) if block_num else 0

            settled_seconds = confirmations * block_time
            settlement_time_str = format_time(time.time() - settled_seconds) if confirmations else None

            tx_from = receipt.get("from", "")
            tx_to = receipt.get("to", "")
            tx_value_wei = receipt.get("value", 0)
            tx_value_eth = wei_to_gwei(tx_value_wei) / 1e9

            return TxTracker(
                chain=chain,
                timestamp=format_time(),
                tx_hash=tx_hash,
                status=status,
                block_number=int(block_num) if block_num else None,
                confirmations=confirmations,
                gas_used=int(gas_used) if gas_used else None,
                gas_limit=int(gas_limit) if gas_limit else None,
                effective_gas_price_gwei=round(effective_gas_price, 2),
                base_fee_gwei=None,
                priority_fee_gwei=None,
                settled_in_blocks=confirmations,
                settled_in_seconds=settled_seconds,
                settlement_time=settlement_time_str,
                nonce=receipt.get("nonce"),
                from_address=tx_from,
                to_address=tx_to,
                value_eth=round(tx_value_eth, 8),
                explorer_url=explorer_url,
            )
        else:
            # pending
            try:
                tx = w3.eth.get_transaction(tx_hash)
                pending_block = w3.eth.get_block("latest").get("number", 0)
                gas_limit = tx.get("gas")
                gas_price = wei_to_gwei(tx.get("gasPrice", 0))
                nonce = tx.get("nonce")
                tx_from = tx.get("from", "")
                tx_to = tx.get("to", "")
                tx_value = wei_to_gwei(tx.get("value", 0)) / 1e9

                return TxTracker(
                    chain=chain,
                    timestamp=format_time(),
                    tx_hash=tx_hash,
                    status="pending",
                    block_number=None,
                    confirmations=0,
                    gas_used=None,
                    gas_limit=int(gas_limit) if gas_limit else None,
                    effective_gas_price_gwei=round(gas_price, 2),
                    base_fee_gwei=None,
                    priority_fee_gwei=None,
                    settled_in_blocks=None,
                    settled_in_seconds=None,
                    settlement_time=None,
                    nonce=nonce,
                    from_address=tx_from,
                    to_address=tx_to,
                    value_eth=round(tx_value, 8),
                    explorer_url=explorer_url,
                )
            except TransactionNotFound:
                return TxTracker(
                    chain=chain,
                    timestamp=format_time(),
                    tx_hash=tx_hash,
                    status="not_found",
                    block_number=None,
                    confirmations=0,
                    gas_used=None,
                    gas_limit=None,
                    effective_gas_price_gwei=None,
                    base_fee_gwei=None,
                    priority_fee_gwei=None,
                    settled_in_blocks=None,
                    settled_in_seconds=None,
                    settlement_time=None,
                    nonce=None,
                    from_address=None,
                    to_address=None,
                    value_eth=None,
                    explorer_url=explorer_url,
                )
    except Exception as e:
        sys.stderr.write(f"track_tx error: {e}\n")
        return None


# ── contract verification ─────────────────────────────────────────────────────

def verify_contract(chain: str, address: str) -> Optional[ContractVerification]:
    api_key = get_etherscan_api_key()
    explorer_base = ETHERSCAN_BASE.get(chain, "")
    explorer_url = f"{CHAIN_META[chain][3]}/address/{address}"

    if not api_key or not explorer_base:
        return ContractVerification(
            chain=chain,
            address=address,
            timestamp=format_time(),
            is_verified=False,
            contract_name=None,
            compiler_version=None,
            optimizer_enabled=None,
            optimization_runs=None,
            abi=None,
            source_code_available=False,
            license=None,
            verified_at=None,
            explorer_url=explorer_url,
            note="ETHERSCAN_API_KEY not set. Contract verification unavailable.",
        )

    try:
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": api_key,
        }
        data = _http_get(explorer_base, params)
        result = data.get("result", [{}])
        if isinstance(result, list):
            result = result[0] if result else {}
        elif isinstance(result, str):
            return ContractVerification(
                chain=chain, address=address, timestamp=format_time(),
                is_verified=False, contract_name=None, compiler_version=None,
                optimizer_enabled=None, optimization_runs=None, abi=None,
                source_code_available=False, license=None, verified_at=None,
                explorer_url=explorer_url,
                note=f"API error: {result[:200]}",
            )

        is_verified = bool(result.get("SourceCode"))
        contract_name = result.get("ContractName")
        compiler_version = result.get("CompilerVersion")
        optimizer = result.get("OptimizationUsed") == "1"
        optimization_runs = int(result.get("Runs", 0))
        license_type = result.get("LicenseType")

        # fetch ABI
        abi_params = {
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": api_key,
        }
        abi_data = _http_get(explorer_base, abi_params)
        abi_str = abi_data.get("result", "")
        abi = None
        if abi_str and not abi_str.startswith("Max rate"):
            try:
                abi = json.loads(abi_str)
            except Exception:
                pass

        return ContractVerification(
            chain=chain,
            address=address,
            timestamp=format_time(),
            is_verified=is_verified,
            contract_name=contract_name,
            compiler_version=compiler_version,
            optimizer_enabled=optimizer,
            optimization_runs=optimization_runs if optimizer else None,
            abi=abi,
            source_code_available=is_verified,
            license=license_type,
            verified_at=result.get("VerificationDate"),
            explorer_url=explorer_url,
        )
    except Exception as e:
        return ContractVerification(
            chain=chain, address=address, timestamp=format_time(),
            is_verified=False, contract_name=None, compiler_version=None,
            optimizer_enabled=None, optimization_runs=None, abi=None,
            source_code_available=False, license=None, verified_at=None,
            explorer_url=explorer_url,
            note=f"Error: {str(e)[:200]}",
        )


# ── token info ────────────────────────────────────────────────────────────────

def get_token_info(chain: str, address: str) -> Optional[TokenInfo]:
    w3 = get_web3(chain)
    if not w3:
        return None
    explorer_base = CHAIN_META[chain][3]

    # ERC-20 token metadata via public RPC (no API key needed for basic info)
    try:
        address = w3.to_checksum_address(address)
    except Exception:
        pass

    try:
        # Try to call token URI if this is a721
        # We'll use the RPC to call erc20 functions
        # Minimal ERC-20 ABI
        ERC20_ABI = [
            {"name": "decimals", "outputs": [{"type": "uint8"}], "type": "function", "stateMutability": "view"},
            {"name": "symbol", "outputs": [{"type": "string"}], "type": "function", "stateMutability": "view"},
            {"name": "name", "outputs": [{"type": "string"}], "type": "function", "stateMutability": "view"},
            {"name": "totalSupply", "outputs": [{"type": "uint256"}], "type": "function", "stateMutability": "view"},
        ]
        contract = w3.eth.contract(address=w3.to_checksum_address(address), abi=ERC20_ABI)

        symbol = "???"
        name = "???"
        decimals = 18
        total_supply = None

        try:
            symbol = contract.functions.symbol().call(block_identifier="latest")
        except Exception:
            pass
        try:
            name = contract.functions.name().call(block_identifier="latest")
        except Exception:
            pass
        try:
            decimals = contract.functions.decimals().call(block_identifier="latest")
        except Exception:
            pass
        try:
            supply_wei = contract.functions.totalSupply().call(block_identifier="latest")
            total_supply = str(supply_wei)
        except Exception:
            pass

        # Try Etherscan for price + holder count if key available
        price_usd = None
        holder_count = None
        transfer_count_24h = None

        api_key = get_etherscan_api_key()
        if api_key:
            params = {
                "module": "token",
                "action": "tokeninfo",
                "address": address,
                "apikey": api_key,
            }
            explorer_url_base = ETHERSCAN_BASE.get(chain, "")
            if explorer_url_base:
                info_data = _http_get(explorer_url_base, params)
                result = info_data.get("result", {})
                if isinstance(result, list):
                    result = result[0] if result else {}

        return TokenInfo(
            chain=chain,
            address=address,
            timestamp=format_time(),
            symbol=symbol,
            name=name,
            decimals=decimals,
            total_supply=total_supply,
            contract_type="ERC-20",
            price_usd=price_usd,
            holder_count=holder_count,
            transfer_count_24h=transfer_count_24h,
            is_verified=True,
            explorer_url=f"{explorer_base}/token/{address}",
        )
    except Exception as e:
        return TokenInfo(
            chain=chain,
            address=address,
            timestamp=format_time(),
            symbol="???",
            name="???",
            decimals=18,
            total_supply=None,
            contract_type="???",
            price_usd=None,
            holder_count=None,
            transfer_count_24h=None,
            is_verified=False,
            explorer_url=f"{explorer_base}/token/{address}",
        )


# ── internal txs ──────────────────────────────────────────────────────────────

def get_internal_txs(chain: str, tx_hash: str) -> List[InternalTx]:
    api_key = get_etherscan_api_key()
    if not api_key:
        return []

    explorer_base = ETHERSCAN_BASE.get(chain, "")
    if not explorer_base:
        return []

    try:
        params = {
            "module": "account",
            "action": "txlistinternal",
            "txhash": tx_hash,
            "apikey": api_key,
        }
        data = _http_get(explorer_base, params)
        results = data.get("result", [])
        if isinstance(results, str):
            return []

        txs = []
        for r in results:
            txs.append(InternalTx(
                tx_hash=tx_hash,
                chain=chain,
                timestamp=format_time(),
                block_number=int(r.get("blockNumber", 0)),
                from_address=r.get("from", ""),
                to_address=r.get("to"),
                value_wei=r.get("value", "0"),
                call_type=r.get("type", "call"),
                gas_used=int(r.get("gasUsed", 0)) if r.get("gasUsed") else None,
                success=r.get("isError") != "1",
                error=r.get("error") if r.get("isError") == "1" else None,
            ))
        return txs
    except Exception:
        return []


# ── gas trend analysis ────────────────────────────────────────────────────────

def analyze_gas_trend(chain: str, window_hours: int = 24) -> Optional[GasTrendAnalysis]:
    rows = get_gas_trend_data(chain, window_hours)
    if not rows:
        return None
    try:
        gas_values = [r[0] for r in rows if r[0] and r[0] > 0]
        if not gas_values:
            return None

        current = gas_values[-1]
        avg = sum(gas_values) / len(gas_values)
        mn = min(gas_values)
        mx = max(gas_values)

        # std dev
        variance = sum((x - avg) ** 2 for x in gas_values) / len(gas_values)
        std = variance ** 0.5

        # volatility
        if std / avg > 0.5:
            volatility = "high"
        elif std / avg > 0.2:
            volatility = "medium"
        else:
            volatility = "low"

        # trend
        if len(gas_values) >= 4:
            recent = gas_values[-4:]
            older = gas_values[-8:-4] if len(gas_values) >= 8 else gas_values[:4]
            recent_avg = sum(recent) / len(recent)
            older_avg = sum(older) / len(older)
            pct_change = (recent_avg - older_avg) / older_avg * 100 if older_avg else 0
            if pct_change > 10:
                trend = "rising"
            elif pct_change < -10:
                trend = "falling"
            else:
                trend = "stable"
        else:
            pct_change = 0.0
            trend = "stable"

        # simple forecast (linear extrapolation)
        forecast_1h = None
        forecast_4h = None
        if len(gas_values) >= 2:
            delta = gas_values[-1] - gas_values[-2]
            # hours represented by data points
            pts_per_hour = len(gas_values) / window_hours if window_hours > 0 else 1
            if pts_per_hour > 0:
                forecast_1h = max(0.1, gas_values[-1] + delta * (1 / pts_per_hour))
                forecast_4h = max(0.1, gas_values[-1] + delta * (4 / pts_per_hour))

        return GasTrendAnalysis(
            chain=chain,
            timestamp=format_time(),
            window_hours=window_hours,
            current_gas_gwei=round(current, 2),
            avg_gas_gwei=round(avg, 2),
            min_gas_gwei=round(mn, 2),
            max_gas_gwei=round(mx, 2),
            std_dev=round(std, 4),
            volatility=volatility,
            trend_direction=trend,
            trend_pct_change=round(pct_change, 2),
            data_points=len(gas_values),
            forecast_1h_gwei=round(forecast_1h, 2) if forecast_1h else None,
            forecast_4h_gwei=round(forecast_4h, 2) if forecast_4h else None,
        )
    except Exception as e:
        sys.stderr.write(f"analyze_gas_trend error: {e}\n")
        return None


# ── BTC trend analysis ────────────────────────────────────────────────────────

def analyze_btc_trend(window_hours: int = 24) -> Optional[BtcTrendAnalysis]:
    try:
        conn = get_db()
        cutoff = format_time(time.time() - window_hours * 3600)
        rows = conn.execute(
            """SELECT fastest, half_hour, hour, two_hours, economical, mempool_mb, mempool_txs, timestamp
               FROM btc_fee_history WHERE timestamp>=? ORDER BY timestamp ASC""",
            (cutoff,)
        ).fetchall()
        conn.close()

        if not rows:
            return None

        fastest_vals = [r[0] for r in rows if r[0] and r[0] > 0]
        if not fastest_vals:
            return None

        current = fastest_vals[-1]
        avg = sum(fastest_vals) / len(fastest_vals)
        mn = min(fastest_vals)
        mx = max(fastest_vals)

        variance = sum((x - avg) ** 2 for x in fastest_vals) / len(fastest_vals)
        std = variance ** 0.5

        if std / avg > 0.5:
            volatility = "high"
        elif std / avg > 0.2:
            volatility = "medium"
        else:
            volatility = "low"

        # trend
        if len(fastest_vals) >= 4:
            recent = fastest_vals[-4:]
            older = fastest_vals[-8:-4] if len(fastest_vals) >= 8 else fastest_vals[:4]
            recent_avg = sum(recent) / len(recent)
            older_avg = sum(older) / len(older)
            pct_change = (recent_avg - older_avg) / older_avg * 100 if older_avg else 0
            if pct_change > 10:
                trend = "rising"
            elif pct_change < -10:
                trend = "falling"
            else:
                trend = "stable"
        else:
            pct_change = 0.0
            trend = "stable"

        mempool_vals = [r[5] for r in rows if r[5]]
        mempool_txs_vals = [r[6] for r in rows if r[6]]

        forecast_1h = None
        if len(fastest_vals) >= 2:
            delta = fastest_vals[-1] - fastest_vals[-2]
            pts_per_hour = len(fastest_vals) / window_hours if window_hours > 0 else 1
            if pts_per_hour > 0:
                forecast_1h = max(0.1, fastest_vals[-1] + delta * (1 / pts_per_hour))

        return BtcTrendAnalysis(
            timestamp=format_time(),
            window_hours=window_hours,
            current_fee_sat_vb=round(current, 2),
            avg_fee_sat_vb=round(avg, 2),
            min_fee_sat_vb=round(mn, 2),
            max_fee_sat_vb=round(mx, 2),
            std_dev=round(std, 4),
            mempool_txs=mempool_txs_vals[-1] if mempool_txs_vals else 0,
            mempool_size_mb=round(mempool_vals[-1], 2) if mempool_vals else 0.0,
            volatility=volatility,
            trend_direction=trend,
            trend_pct_change=round(pct_change, 2),
            data_points=len(fastest_vals),
            forecast_1h_sat_vb=round(forecast_1h, 2) if forecast_1h else None,
        )
    except Exception as e:
        sys.stderr.write(f"analyze_btc_trend error: {e}\n")
        return None


# ── simulate tx ───────────────────────────────────────────────────────────────

def simulate_tx(chain: str, to_address: str, value_eth: float = 0.0) -> Optional[SimulatedTx]:
    """
    Simulate a transaction. Uses Tenderly if TENDERLY_API_KEY is set,
    otherwise falls back to local eth_call.
    """
    w3 = get_web3(chain)
    if not w3:
        return None

    api_key = get_tenderly_api_key()
    explorer_base = CHAIN_META[chain][3]

    try:
        to_checksum = w3.to_checksum_address(to_address)
        value_wei = int(value_eth * 1e18)

        if api_key:
            # Tenderly simulation
            return _simulate_tenderly(chain, to_checksum, value_wei, api_key, explorer_base)

        # Fallback: local eth_call (no state changes returned)
        try:
            tx_data = {
                "to": to_checksum,
                "value": value_wei,
                "data": "0x",
            }
            result = w3.eth.call(tx_data)
            return_value = result.hex() if result else "0x"

            # Try to estimate gas
            try:
                gas_estimate = w3.eth.estimate_gas(tx_data)
            except Exception:
                gas_estimate = None

            return SimulatedTx(
                chain=chain,
                timestamp=format_time(),
                to_address=to_checksum,
                value_eth=value_eth,
                success=True,
                gas_used=gas_estimate,
                gas_limit=gas_estimate,
                return_value=return_value,
                revert_reason=None,
                state_changes=[],
                logs=[],
                explorer_url=f"{explorer_base}/tx/new",
                note="Local eth_call simulation (no state changes). Set TENDERLY_API_KEY for full simulation.",
            )
        except Exception as e:
            err_msg = str(e)
            revert = None
            if "revert" in err_msg.lower():
                revert = err_msg[:500]
            return SimulatedTx(
                chain=chain,
                timestamp=format_time(),
                to_address=to_checksum,
                value_eth=value_eth,
                success=False,
                gas_used=None,
                gas_limit=None,
                return_value=None,
                revert_reason=revert,
                state_changes=[],
                logs=[],
                explorer_url=f"{explorer_base}/tx/new",
                note="Simulation failed.",
            )
    except Exception as e:
        return SimulatedTx(
            chain=chain,
            timestamp=format_time(),
            to_address=to_address,
            value_eth=value_eth,
            success=False,
            gas_used=None,
            gas_limit=None,
            return_value=None,
            revert_reason=str(e)[:500],
            state_changes=[],
            logs=[],
            explorer_url="",
            note=f"Error: {str(e)[:200]}",
        )


def _simulate_tenderly(chain: str, to: str, value_wei: int,
                       api_key: str, explorer_base: str) -> Optional[SimulatedTx]:
    tenderly_slug = {
        "ethereum": "mainnet",
        "arbitrum": "arbitrum-one",
        "optimism": "optimism",
        "base": "base",
        "polygon": "polygon",
    }
    network = tenderly_slug.get(chain, "mainnet")

    payload = {
        "network_id": network,
        "from": "0x0000000000000000000000000000000000000000",
        "to": to,
        "value": str(value_wei),
        "input": "0x",
        "gas": 5000000,
        "gas_price": "0",
        "simulation_type": "full",
    }
    headers = {
        "X-Access-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(
            "https://api.tenderly.co/api/v1/simulate",
            json=payload,
            headers=headers,
            timeout=15,
        )
        if r.status_code == 200:
            data = r.json()
            sim = data.get("simulation", {})
            status = sim.get("status", False)
            revert_reason = None
            if not status:
                revert_reason = sim.get("error_message", "Transaction would fail")

            logs = []
            for log in sim.get("logs", []):
                logs.append({
                    "address": log.get("address"),
                    "topics": log.get("topics", []),
                    "data": log.get("data"),
                })

            return SimulatedTx(
                chain=chain,
                timestamp=format_time(),
                to_address=to,
                value_eth=wei_to_gwei(value_wei) / 1e9,
                success=status,
                gas_used=sim.get("gas_used"),
                gas_limit=sim.get("gas_limit"),
                return_value=sim.get("return"),
                revert_reason=revert_reason,
                state_changes=[],
                logs=logs,
                explorer_url=f"{explorer_base}/tx/new",
                note="Tenderly simulation.",
            )
        else:
            return SimulatedTx(
                chain=chain,
                timestamp=format_time(),
                to_address=to,
                value_eth=wei_to_gwei(value_wei) / 1e9,
                success=False,
                gas_used=None,
                gas_limit=None,
                return_value=None,
                revert_reason=f"Tenderly API error {r.status_code}: {r.text[:200]}",
                state_changes=[],
                logs=[],
                explorer_url=f"{explorer_base}/tx/new",
                note="Tenderly simulation failed.",
            )
    except Exception as e:
        return SimulatedTx(
            chain=chain,
            timestamp=format_time(),
            to_address=to,
            value_eth=wei_to_gwei(value_wei) / 1e9,
            success=False,
            gas_used=None,
            gas_limit=None,
            return_value=None,
            revert_reason=str(e)[:500],
            state_changes=[],
            logs=[],
            explorer_url=f"{explorer_base}/tx/new",
            note="Tenderly simulation error.",
        )


# ── formatter ─────────────────────────────────────────────────────────────────

def _format_json(obj: Any) -> str:
    if hasattr(obj, "to_dict"):
        return json.dumps(obj.to_dict(), indent=2, default=str)
    return json.dumps(obj, indent=2, default=str)


def _format_result_table(obj: Any) -> str:
    if isinstance(obj, GasPrediction):
        rows = []
        for tier, val in obj.estimated_gas_gwei.items():
            rows.append([tier.capitalize(), f"{val} gwei"])
        rows.append(["Base Fee", f"{obj.base_fee_gwei} gwei"])
        rows.append(["Priority Fee", f"{obj.priority_fee_gwei} gwei"])
        rows.append(["Congestion", obj.network_congestion.capitalize()])
        rows.append(["Confidence", obj.confidence.capitalize()])
        rows.append(["Block", str(obj.pending_block)])
        header = f"Gas Prediction — {obj.chain.upper()}"
        sub = f"Timestamp: {obj.timestamp}  |  Source: {obj.source}"
        return f"\n{header}\n{sub}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, SettlementPrediction):
        rows = [
            ["Input Gas", f"{obj.input_gas_gwei} gwei"],
            ["Deadline", f"{obj.deadline_blocks} blocks"],
            ["Est. Blocks to Finality", str(obj.estimated_blocks_to_finality)],
            ["Est. Time", f"{obj.estimated_time_seconds:.1f}s"],
            ["Est. Settlement", obj.estimated_settlement_time],
            ["Confidence", obj.confidence.capitalize()],
            ["Risk Level", obj.risk_level.capitalize()],
        ]
        if obj.cost_wei:
            rows.append(["Cost (wei)", str(obj.cost_wei)])
        header = f"Settlement Prediction — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, OptimalWindow):
        rows = [
            ["Urgency", obj.urgency.upper()],
            ["Recommended Fee", f"{obj.recommended_fee_gwei} gwei"],
            ["Wait Blocks", str(obj.wait_blocks)],
            ["Est. Time", f"{obj.estimated_time_seconds:.1f}s"],
            ["Est. Finality", obj.estimated_finality_time],
            ["Confidence", obj.confidence.capitalize()],
        ]
        if obj.warning:
            rows.append(["Warning", obj.warning])
        header = f"Optimal Window — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, PendingPoolAnalysis):
        rows = [
            ["Pool", obj.pool_address],
            ["Direction", obj.direction.upper()],
            ["Amount (USD)", f"${obj.amount_usd:,.2f}"],
            ["Gas Environment", obj.gas_environment.capitalize()],
            ["Congestion Score", f"{obj.pool_congestion_score:.3f}"],
            ["Sandwich Risk", obj.sandwich_risk.upper()],
            ["Price Impact", f"{obj.price_impact_bps:.1f} bps"],
            ["Net Cost (USD)", f"${obj.net_cost_usd:.4f}"],
            ["Confidence", obj.confidence.capitalize()],
            ["Recommendation", obj.recommendation],
        ]
        header = f"Pending Pool Analysis — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, TxTracker):
        rows = [
            ["Hash", obj.tx_hash],
            ["Status", obj.status.upper()],
            ["Block", str(obj.block_number)],
            ["Confirmations", str(obj.confirmations)],
            ["Gas Used", str(obj.gas_used)],
            ["Gas Limit", str(obj.gas_limit)],
            ["Effective Gas", f"{obj.effective_gas_price_gwei} gwei"],
            ["Settled In", f"{obj.settled_in_seconds:.1f}s ({obj.settled_in_blocks} blocks)"],
            ["From", obj.from_address],
            ["To", obj.to_address],
            ["Value (ETH)", str(obj.value_eth)],
            ["Explorer", obj.explorer_url],
        ]
        header = f"Transaction Tracker — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, ContractVerification):
        rows = [
            ["Address", obj.address],
            ["Verified", "✅ Yes" if obj.is_verified else "❌ No"],
            ["Contract Name", str(obj.contract_name)],
            ["Compiler Version", str(obj.compiler_version)],
            ["Optimizer", "Enabled" if obj.optimizer_enabled else "Disabled"],
            ["Optimization Runs", str(obj.optimization_runs)],
            ["License", str(obj.license)],
            ["Source Code", "Available" if obj.source_code_available else "Not Available"],
            ["Explorer", obj.explorer_url],
        ]
        if obj.note:
            rows.append(["Note", obj.note])
        header = f"Contract Verification — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, TokenInfo):
        rows = [
            ["Address", obj.address],
            ["Symbol", obj.symbol],
            ["Name", obj.name],
            ["Decimals", str(obj.decimals)],
            ["Total Supply", str(obj.total_supply)],
            ["Contract Type", str(obj.contract_type)],
            ["Price (USD)", f"${obj.price_usd}" if obj.price_usd else "N/A"],
            ["Holders", str(obj.holder_count)],
            ["24h Transfers", str(obj.transfer_count_24h)],
            ["Verified", "Yes" if obj.is_verified else "No"],
            ["Explorer", obj.explorer_url],
        ]
        header = f"Token Info — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, list) and obj and isinstance(obj[0], InternalTx):
        rows = [[
            str(t.block_number), t.from_address[:10] + "...",
            (t.to_address[:10] + "..." if t.to_address else "?"),
            t.call_type, str(t.value_wei),
            "✅" if t.success else "❌", t.error or ""
        ] for t in obj]
        header = f"Internal Transactions — {obj[0].chain.upper()}"
        return f"\n{header}\n\n{format_table(['Block', 'From', 'To', 'Type', 'Value (wei)', 'OK', 'Error'], rows)}\n"

    if isinstance(obj, BtcFeeEstimate):
        rows = [
            ["Urgency", obj.urgency.upper()],
            ["Fastest", f"{obj.sat_per_vbyte.get('fastest', 'N/A')} sat/vB"],
            ["~30 min", f"{obj.sat_per_vbyte.get('half_hour', 'N/A')} sat/vB"],
            ["~1 hour", f"{obj.sat_per_vbyte.get('hour', 'N/A')} sat/vB"],
            ["~2 hours", f"{obj.sat_per_vbyte.get('two_hours', 'N/A')} sat/vB"],
            ["Economical", f"{obj.sat_per_vbyte.get('economical', 'N/A')} sat/vB"],
            ["Mempool Depth", f"{obj.mempool_depth_mb} MB" if obj.mempool_depth_mb else "N/A"],
            ["Congestion", obj.congestion_level.capitalize()],
            ["Confidence", obj.confidence.capitalize()],
        ]
        header = "Bitcoin Fee Estimate"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, BtcSettlementPrediction):
        rows = [
            ["Fee Rate", f"{obj.sat_per_vbyte} sat/vB"],
            ["Urgency", obj.urgency.upper()],
            ["Est. Blocks", str(obj.estimated_blocks)],
            ["Est. Minutes", str(obj.estimated_minutes)],
            ["Est. Settlement", obj.estimated_settlement_time],
            ["Confidence", obj.confidence.capitalize()],
            ["Risk Level", obj.risk_level.capitalize()],
            ["Cost (250vB tx)", f"{obj.cost_sats} sats" if obj.cost_sats else "N/A"],
        ]
        header = "Bitcoin Settlement Prediction"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, BtcOptimalWindow):
        rows = [
            ["Urgency", obj.urgency.upper()],
            ["Recommended Fee", f"{obj.recommended_sat_vb} sat/vB"],
            ["Est. Blocks", str(obj.estimated_blocks)],
            ["Est. Minutes", str(obj.estimated_minutes)],
            ["Est. Settlement", obj.estimated_settlement_time],
            ["Confidence", obj.confidence.capitalize()],
        ]
        if obj.warning:
            rows.append(["Warning", obj.warning])
        header = "Bitcoin Optimal Fee Window"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, BtcTxTracker):
        rows = [
            ["TXID", obj.txid],
            ["Status", obj.status.upper()],
            ["Confirmed", "Yes" if obj.confirmed else "No"],
            ["Block Height", str(obj.block_height)],
            ["Confirmations", str(obj.confirmations)],
            ["Fee (sats)", str(obj.fee_sats)],
            ["Fee Rate", f"{obj.fee_rate_sat_vb} sat/vB" if obj.fee_rate_sat_vb else "N/A"],
            ["VSize", f"{obj.vsize} vB" if obj.vsize else "N/A"],
            ["Weight", f"{obj.weight_units} WU" if obj.weight_units else "N/A"],
            ["Settled In", f"{obj.settled_in_minutes:.1f} min" if obj.settled_in_minutes else "Pending"],
            ["Settlement Time", obj.settlement_time or "Pending"],
            ["Mempool URL", obj.mempool_url],
        ]
        header = "Bitcoin Transaction Tracker"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, GasTrendAnalysis):
        rows = [
            ["Chain", obj.chain.upper()],
            ["Window", f"{obj.window_hours}h"],
            ["Data Points", str(obj.data_points)],
            ["Current Gas", f"{obj.current_gas_gwei} gwei"],
            ["Average Gas", f"{obj.avg_gas_gwei} gwei"],
            ["Min Gas", f"{obj.min_gas_gwei} gwei"],
            ["Max Gas", f"{obj.max_gas_gwei} gwei"],
            ["Std Dev", f"{obj.std_dev:.4f}"],
            ["Volatility", obj.volatility.capitalize()],
            ["Trend", f"{obj.trend_direction.upper()} ({obj.trend_pct_change:+.1f}%)"],
            ["Forecast 1h", f"{obj.forecast_1h_gwei} gwei" if obj.forecast_1h_gwei else "N/A"],
            ["Forecast 4h", f"{obj.forecast_4h_gwei} gwei" if obj.forecast_4h_gwei else "N/A"],
        ]
        header = f"Gas Trend Analysis — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, BtcTrendAnalysis):
        rows = [
            ["Window", f"{obj.window_hours}h"],
            ["Data Points", str(obj.data_points)],
            ["Current Fee", f"{obj.current_fee_sat_vb} sat/vB"],
            ["Average Fee", f"{obj.avg_fee_sat_vb} sat/vB"],
            ["Min Fee", f"{obj.min_fee_sat_vb} sat/vB"],
            ["Max Fee", f"{obj.max_fee_sat_vb} sat/vB"],
            ["Std Dev", f"{obj.std_dev:.4f}"],
            ["Mempool Txs", f"{obj.mempool_txs:,}"],
            ["Mempool Size", f"{obj.mempool_size_mb:.1f} MB"],
            ["Volatility", obj.volatility.capitalize()],
            ["Trend", f"{obj.trend_direction.upper()} ({obj.trend_pct_change:+.1f}%)"],
            ["Forecast 1h", f"{obj.forecast_1h_sat_vb} sat/vB" if obj.forecast_1h_sat_vb else "N/A"],
        ]
        header = "Bitcoin Trend Analysis"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    if isinstance(obj, SimulatedTx):
        rows = [
            ["Chain", obj.chain.upper()],
            ["To", obj.to_address],
            ["Value (ETH)", str(obj.value_eth)],
            ["Success", "✅ Yes" if obj.success else "❌ No"],
            ["Gas Used", str(obj.gas_used)],
            ["Gas Limit", str(obj.gas_limit)],
            ["Return Value", obj.return_value or "N/A"],
            ["Revert Reason", obj.revert_reason or "None"],
            ["Explorer", obj.explorer_url],
        ]
        if obj.note:
            rows.append(["Note", obj.note])
        header = f"Transaction Simulation — {obj.chain.upper()}"
        return f"\n{header}\n\n{format_table(['Metric', 'Value'], rows)}\n"

    return str(obj)


# ── CLI commands ──────────────────────────────────────────────────────────────

def cmd_get_gas_prediction(chain: str, urgency: str, fmt: OutputFormat) -> int:
    pred = _eth_get_gas_prices(chain)
    if not pred:
        sys.stderr.write(f"Error: Could not fetch gas data for {chain}.\n")
        return 1
    print(_format_json(pred) if fmt == OutputFormat.JSON else _format_result_table(pred))
    return 0


def cmd_predict_settlement(chain: str, gas_price: float,
                           deadline_blocks: int, fmt: OutputFormat) -> int:
    pred = predict_settlement_eth(chain, gas_price, deadline_blocks)
    if not pred:
        sys.stderr.write(f"Error: Could not predict settlement for {chain}.\n")
        return 1
    print(_format_json(pred) if fmt == OutputFormat.JSON else _format_result_table(pred))
    return 0


def cmd_get_optimal_window(chain: str, urgency: str,
                           target_minutes: Optional[float], fmt: OutputFormat) -> int:
    win = _optimal_window_eth(chain, urgency, target_minutes)
    if not win:
        sys.stderr.write(f"Error: Could not determine optimal window for {chain}.\n")
        return 1
    print(_format_json(win) if fmt == OutputFormat.JSON else _format_result_table(win))
    return 0


def cmd_analyze_pending_pool(chain: str, pool_address: str,
                              direction: str, amount_usd: float,
                              fmt: OutputFormat) -> int:
    result = analyze_pending_pool(chain, pool_address, direction, amount_usd)
    if not result:
        sys.stderr.write(f"Error: Could not analyze pending pool for {chain}.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_track_tx(chain: str, tx_hash: str, fmt: OutputFormat) -> int:
    tracker = track_tx(chain, tx_hash)
    if not tracker:
        sys.stderr.write(f"Error: Could not track tx on {chain}.\n")
        return 1
    print(_format_json(tracker) if fmt == OutputFormat.JSON else _format_result_table(tracker))
    return 0


def cmd_verify_contract(chain: str, address: str, fmt: OutputFormat) -> int:
    result = verify_contract(chain, address)
    if not result:
        sys.stderr.write(f"Error: Could not verify contract on {chain}.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_get_token_info(chain: str, address: str, fmt: OutputFormat) -> int:
    result = get_token_info(chain, address)
    if not result:
        sys.stderr.write(f"Error: Could not get token info for {chain}.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_get_internal_txs(chain: str, tx_hash: str, fmt: OutputFormat) -> int:
    txs = get_internal_txs(chain, tx_hash)
    print(_format_json(txs) if fmt == OutputFormat.JSON else _format_result_table(txs))
    return 0


def cmd_btc_fee_estimate(urgency: str, fmt: OutputFormat) -> int:
    result = btc_fee_estimate(urgency)
    if not result:
        sys.stderr.write("Error: Could not fetch BTC fee estimate.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_btc_predict_settlement(sat: float, urgency: str, fmt: OutputFormat) -> int:
    result = btc_predict_settlement(sat, urgency)
    if not result:
        sys.stderr.write("Error: Could not predict BTC settlement.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_btc_optimal_window(urgency: str, fmt: OutputFormat) -> int:
    result = btc_optimal_window(urgency)
    if not result:
        sys.stderr.write("Error: Could not determine BTC optimal window.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_track_btc_tx(tx: str, fmt: OutputFormat) -> int:
    result = track_btc_tx(tx)
    if not result:
        sys.stderr.write("Error: Could not track BTC transaction.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_analyze_gas_trend(chain: str, fmt: OutputFormat, window: int = 24) -> int:
    result = analyze_gas_trend(chain, window)
    if not result:
        sys.stderr.write(f"Error: Could not analyze gas trend for {chain}. No cached data.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_analyze_btc_trend(fmt: OutputFormat, window: int = 24) -> int:
    result = analyze_btc_trend(window)
    if not result:
        sys.stderr.write("Error: Could not analyze BTC trend. No cached data.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


def cmd_simulate_tx(chain: str, to: str, value: float, fmt: OutputFormat) -> int:
    result = simulate_tx(chain, to, value)
    if not result:
        sys.stderr.write(f"Error: Could not simulate tx on {chain}.\n")
        return 1
    print(_format_json(result) if fmt == OutputFormat.JSON else _format_result_table(result))
    return 0


# ── argparse ──────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="settlement-predictor",
        description="Real-time on-chain settlement prediction for EVM chains & Bitcoin.",
    )
    parser.add_argument("--format", "-f", dest="format", choices=["json", "table"],
                        default="table", help="Output format (default: table)")

    sub = parser.add_subparsers(dest="command", required=True)

    # 1. get-gas-prediction
    p1 = sub.add_parser("get-gas-prediction", help="Get current gas prediction for a chain")
    p1.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"],
                    help="EVM chain")
    p1.add_argument("--urgency", default="medium",
                    choices=["low", "medium", "high", "instant"],
                    help="Urgency level (affects recommended tier)")

    # 2. predict-settlement
    p2 = sub.add_parser("predict-settlement", help="Predict settlement time for a given gas price")
    p2.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p2.add_argument("--gas-price", type=float, required=True, help="Gas price in gwei")
    p2.add_argument("--deadline-blocks", type=int, required=True,
                    help="Maximum blocks until deadline")

    # 3. get-optimal-window
    p3 = sub.add_parser("get-optimal-window", help="Get optimal fee window")
    p3.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p3.add_argument("--urgency", default="medium",
                    choices=["low", "medium", "high", "instant"])
    p3.add_argument("--target-minutes", type=float,
                    help="Target time to settlement in minutes")

    # 4. analyze-pending-pool
    p4 = sub.add_parser("analyze-pending-pool",
                        help="Analyze pending pool for sandwich risk / price impact")
    p4.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p4.add_argument("--pool-address", required=True, help="Pool contract address")
    p4.add_argument("--direction", required=True,
                    help="Direction: buy/sell (or add/remove liquidity)")
    p4.add_argument("--amount-usd", type=float, required=True, help="Amount in USD")

    # 5. track-tx
    p5 = sub.add_parser("track-tx", help="Track an EVM transaction")
    p5.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p5.add_argument("--tx-hash", required=True, help="Transaction hash (0x...)")

    # 6. verify-contract
    p6 = sub.add_parser("verify-contract", help="Verify a smart contract on block explorer")
    p6.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p6.add_argument("--address", required=True, help="Contract address")

    # 7. get-token-info
    p7 = sub.add_parser("get-token-info", help="Get ERC-20 token information")
    p7.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p7.add_argument("--address", required=True, help="Token contract address")

    # 8. get-internal-txs
    p8 = sub.add_parser("get-internal-txs",
                        help="Get internal transactions for an EVM tx (requires ETHERSCAN_API_KEY)")
    p8.add_argument("--chain", required=True,
                    choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p8.add_argument("--tx-hash", required=True, help="Transaction hash")

    # 9. btc-fee-estimate
    p9 = sub.add_parser("btc-fee-estimate", help="Get Bitcoin fee estimate from mempool.space")
    p9.add_argument("--urgency", default="medium",
                    choices=["low", "medium", "high", "instant"])

    # 10. btc-predict-settlement
    p10 = sub.add_parser("btc-predict-settlement",
                         help="Predict Bitcoin settlement for a given sat/vB fee rate")
    p10.add_argument("--sat", type=float, required=True,
                     help="Fee rate in satoshis per vbyte")
    p10.add_argument("--urgency", default="medium",
                     choices=["low", "medium", "high", "instant"])

    # 11. btc-optimal-window
    p11 = sub.add_parser("btc-optimal-window",
                          help="Get optimal Bitcoin fee window based on urgency")
    p11.add_argument("--urgency", default="medium",
                     choices=["low", "medium", "high", "instant"])

    # 12. track-btc-tx
    p12 = sub.add_parser("track-btc-tx", help="Track a Bitcoin transaction via mempool.space")
    p12.add_argument("--tx", required=True, help="Bitcoin transaction ID")

    # 13. analyze-gas-trend
    p13 = sub.add_parser("analyze-gas-trend",
                          help="Analyze historical gas trend for an EVM chain")
    p13.add_argument("--chain", required=True,
                     choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])

    # 14. analyze-btc-trend
    p14 = sub.add_parser("analyze-btc-trend",
                          help="Analyze historical Bitcoin fee trend from cached mempool data")

    # 15. simulate-tx
    p15 = sub.add_parser("simulate-tx",
                          help="Simulate an EVM transaction (uses Tenderly if key set)")
    p15.add_argument("--chain", required=True,
                     choices=["ethereum", "arbitrum", "optimism", "base", "polygon"])
    p15.add_argument("--to", required=True, help="Destination address")
    p15.add_argument("--value", type=float, default=0.0, help="Value in ETH (default: 0)")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    fmt = OutputFormat(args.format)

    # Route commands
    cmd = args.command
    if cmd == "get-gas-prediction":
        return cmd_get_gas_prediction(args.chain, args.urgency, fmt)
    elif cmd == "predict-settlement":
        return cmd_predict_settlement(args.chain, args.gas_price, args.deadline_blocks, fmt)
    elif cmd == "get-optimal-window":
        return cmd_get_optimal_window(args.chain, args.urgency,
                                      getattr(args, "target_minutes", None), fmt)
    elif cmd == "analyze-pending-pool":
        return cmd_analyze_pending_pool(args.chain, args.pool_address,
                                        args.direction, args.amount_usd, fmt)
    elif cmd == "track-tx":
        return cmd_track_tx(args.chain, args.tx_hash, fmt)
    elif cmd == "verify-contract":
        return cmd_verify_contract(args.chain, args.address, fmt)
    elif cmd == "get-token-info":
        return cmd_get_token_info(args.chain, args.address, fmt)
    elif cmd == "get-internal-txs":
        return cmd_get_internal_txs(args.chain, args.tx_hash, fmt)
    elif cmd == "btc-fee-estimate":
        return cmd_btc_fee_estimate(args.urgency, fmt)
    elif cmd == "btc-predict-settlement":
        return cmd_btc_predict_settlement(args.sat, args.urgency, fmt)
    elif cmd == "btc-optimal-window":
        return cmd_btc_optimal_window(args.urgency, fmt)
    elif cmd == "track-btc-tx":
        return cmd_track_btc_tx(args.tx, fmt)
    elif cmd == "analyze-gas-trend":
        return cmd_analyze_gas_trend(args.chain, fmt)
    elif cmd == "analyze-btc-trend":
        return cmd_analyze_btc_trend(fmt)
    elif cmd == "simulate-tx":
        return cmd_simulate_tx(args.chain, args.to, args.value, fmt)
    else:
        sys.stderr.write(f"Unknown command: {cmd}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
