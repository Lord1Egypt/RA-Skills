#!/usr/bin/env python3
"""Deterministic build, validation, rendering and maintenance primitives.

The agent supplies researched facts and proposed operations. This module owns every mutation and
output invariant. It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

PROFILES = ("light", "medium", "heavy", "max")
PROFILE_INDEX = {name: index for index, name in enumerate(PROFILES)}
ROLES = {
    "BENCHMARK",
    "ANCHOR",
    "THEME_LEADER",
    "QUALITY_LEADER",
    "BETA_SATELLITE",
    "INDEPENDENT_SENSOR",
    "BREADTH_PROXY",
    "LIQUIDITY_SENSOR",
    "NEW_LISTING",
}
BUCKET_BY_ROLE = {
    "BENCHMARK": "core",
    "ANCHOR": "core",
    "THEME_LEADER": "core",
    "QUALITY_LEADER": "core",
    "BETA_SATELLITE": "satellite",
    "INDEPENDENT_SENSOR": "satellite",
    "BREADTH_PROXY": "satellite",
    "LIQUIDITY_SENSOR": "tactical",
    "NEW_LISTING": "tactical",
}
CORE_ROLES = frozenset(role for role, bucket in BUCKET_BY_ROLE.items() if bucket == "core")
ROLE_ORDER = {
    "BENCHMARK": 1100,
    "ANCHOR": 1000,
    "THEME_LEADER": 900,
    "QUALITY_LEADER": 800,
    "INDEPENDENT_SENSOR": 700,
    "BETA_SATELLITE": 600,
    "BREADTH_PROXY": 500,
    "LIQUIDITY_SENSOR": 400,
    "NEW_LISTING": 300,
}
# Roles whose members are admitted for structural reasons rather than for carrying independent
# information, so the factor-redundancy statistic is not asked of them.
FACTOR_EXEMPT_ROLES = frozenset({"BENCHMARK", "ANCHOR", "NEW_LISTING"})


@dataclass(frozen=True)
class MarketSpec:
    """Everything that is true of one market and of no other.

    Every market-specific rule lives in a row of this table, so adding a market is a registry
    entry plus a policy entry plus an overlay document — not an edit spread across the validator,
    the identity rule and the candidate gate, where a fourth market would have gone unchecked in
    two of the three.
    """

    code: str
    label: str
    venues: frozenset[str]
    symbol_pattern: re.Pattern[str]
    symbol_hint: str
    # The language the human-readable report is written in unless the caller overrides it. A
    # universe is read by the people who trade that market, so the default follows the market
    # rather than the tool: an A-share report is Simplified Chinese the same way it is six digits.
    language: str = "en"
    # Whether two venues listing the same symbol are the same economic asset. CN dual listings
    # are distinct instruments; a US symbol is the company wherever it prints.
    venue_in_asset_id: bool = False
    # Suffixes stripped in order to reach the economic identity: a perpetual and its spot pair
    # are one information source, so BTCUSDT.P and BTCUSDT both reduce to BTC.
    asset_id_strip: tuple[str, ...] = ()
    # Markets driven by one factor complex have to state how redundant each member is with it.
    factor_r2_required: bool = False
    # Adverse flags this market's regime issues and no other's does. They are added to
    # QUALITY_FLAG_CODES, never substituted for it: the scoring rule stays general — every flag
    # costs the same QUALITY_FLAG_PENALTY — while what counts as a flag follows the regulator.
    # Without this the choice is a vocabulary too coarse to record an ST designation or a core
    # that knows what an NT 10-K is, and the second is how a general tool becomes three tools.
    quality_flags: frozenset[str] = frozenset()
    # `registered` means this row shipped with the skill and was reviewed. `declared` means a
    # snapshot supplied it at run time, which is a weaker claim and is reported as one.
    origin: str = "registered"


MARKET_SPECS: dict[str, MarketSpec] = {
    spec.code: spec
    for spec in (
        MarketSpec(
            code="cn",
            label="China A-shares",
            venues=frozenset({"SSE", "SZSE", "BSE"}),
            symbol_pattern=re.compile(r"\d{6}"),
            symbol_hint="six digits",
            language="zh-Hans",
            venue_in_asset_id=True,
            quality_flags=frozenset({
                "special_treatment", "share_pledge_risk", "exchange_inquiry",
            }),
        ),
        MarketSpec(
            code="us",
            label="US equities and ETFs",
            venues=frozenset({"NASDAQ", "NYSE", "AMEX", "NYSEARCA", "ARCA", "CBOE", "IEX", "OTC"}),
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9.\-]{0,14}"),
            symbol_hint="one to fifteen characters starting with a letter",
            quality_flags=frozenset({
                "late_filing", "listing_deficiency", "material_weakness",
            }),
        ),
        MarketSpec(
            code="crypto",
            label="Crypto spot and perpetuals",
            venues=frozenset({"BINANCE", "OKX"}),
            symbol_pattern=re.compile(r"[A-Z0-9]{1,15}USDT(\.P)?"),
            symbol_hint="a USDT-quoted spot or perpetual symbol",
            asset_id_strip=(".P", "USDT"),
            factor_r2_required=True,
            quality_flags=frozenset({
                "unlock_overhang", "supply_concentration", "unaudited_contract",
            }),
        ),
        MarketSpec(
            code="jp",
            label="Japan equities",
            venues=frozenset({"TSE"}),
            symbol_pattern=re.compile(r"\d{3}[0-9A-Z]"),
            symbol_hint="four characters: three digits then a digit or a letter",
            language="ja",
            quality_flags=frozenset({
                "security_on_alert", "supervision_post", "listing_criteria_shortfall",
            }),
        ),
        MarketSpec(
            code="hk",
            label="Hong Kong equities",
            venues=frozenset({"HKEX"}),
            symbol_pattern=re.compile(r"\d{1,5}"),
            symbol_hint="one to five digits, unpadded",
            language="zh-Hant",
            quality_flags=frozenset({
                "prolonged_suspension", "cancellation_procedure", "shell_activity_concern",
            }),
        ),
        MarketSpec(
            code="in",
            label="India equities",
            venues=frozenset({"NSE", "BSE"}),
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9&\-]{0,19}"),
            symbol_hint="an alphanumeric code, ampersand and hyphen allowed",
            quality_flags=frozenset({
                "asm_surveillance", "gsm_surveillance", "promoter_pledge",
            }),
        ),
        MarketSpec(
            code="kr",
            label="Korea equities",
            venues=frozenset({"KRX"}),
            symbol_pattern=re.compile(r"\d{6}"),
            symbol_hint="six digits",
            language="ko",
            quality_flags=frozenset({
                "administrative_issue", "investment_alert", "trading_halt_review",
            }),
        ),
        MarketSpec(
            code="tw",
            label="Taiwan equities",
            venues=frozenset({"TWSE", "TPEX"}),
            symbol_pattern=re.compile(r"\d{4,6}[A-Z]?"),
            symbol_hint="four to six digits, optionally one trailing letter",
            language="zh-Hant",
            quality_flags=frozenset({
                "disposition_stock", "altered_trading_method", "full_delivery",
            }),
        ),
        MarketSpec(
            code="uk",
            label="UK equities",
            venues=frozenset({"LSE"}),
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9.]{0,5}"),
            symbol_hint="two to six characters starting with a letter",
            quality_flags=frozenset({
                "offer_period", "cancellation_notice", "listing_category_transfer",
            }),
        ),
        MarketSpec(
            code="de",
            label="Germany equities",
            venues=frozenset({"XETR", "FWB"}),
            # Xetra codes may open with a digit -- 4GLD, 1U1 -- so the shape is alphanumeric
            # rather than letter-led. Found by a real listing, not by reading the rule.
            symbol_pattern=re.compile(r"[A-Z0-9][A-Z0-9]{0,5}"),
            symbol_hint="one to six alphanumeric characters",
            language="de",
            quality_flags=frozenset({
                "squeeze_out", "delisting_offer", "prime_standard_breach",
            }),
        ),
        MarketSpec(
            code="fr",
            label="Euronext Paris equities",
            venues=frozenset({"EURONEXT"}),
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9]{0,4}"),
            symbol_hint="one to five characters starting with a letter",
            language="fr",
            quality_flags=frozenset({
                "tender_offer_period", "amf_injunction", "transfer_to_growth",
            }),
        ),
        MarketSpec(
            code="ca",
            label="Canada equities",
            venues=frozenset({"TSX", "TSXV"}),
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9.]{0,9}"),
            symbol_hint="one to ten characters starting with a letter",
            quality_flags=frozenset({
                "cease_trade_order", "management_cto", "delisting_review",
            }),
        ),
        MarketSpec(
            code="au",
            label="Australia equities",
            venues=frozenset({"ASX"}),
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9]{2,5}"),
            symbol_hint="three to six characters starting with a letter",
            quality_flags=frozenset({
                "asx_price_query", "voluntary_administration", "capital_raising_halt",
            }),
        ),
        MarketSpec(
            code="br",
            label="Brazil equities",
            venues=frozenset({"BMFBOVESPA"}),
            # Four characters then the class digits. The four are usually letters but need not
            # be -- B3SA3 is the exchange itself -- so only the first character is pinned.
            symbol_pattern=re.compile(r"[A-Z][A-Z0-9]{3}\d{1,2}"),
            symbol_hint="four characters starting with a letter, then one or two digits",
            language="pt-BR",
            quality_flags=frozenset({
                "judicial_recovery", "cvm_inquiry", "segment_downgrade",
            }),
        ),
    )
}
MARKETS = frozenset(MARKET_SPECS)

# A market this skill has not reviewed is not a market the user may not observe. The general
# logic — roles, quotas, evidence tiers, measurement, turnover budgets, hashing — is the same
# everywhere; what a registry row adds is the handful of facts that are true of one market and
# of no other. Those are facts, so a snapshot can carry them the way it carries any other fact:
# researched, evidence-backed, recorded, and visibly marked as researched rather than reviewed.
DECLARED_SPEC_FIELDS = frozenset({
    "code", "label", "language", "venues", "symbol_pattern", "symbol_hint",
    "venue_in_asset_id", "asset_id_strip", "factor_r2_required", "quality_flags",
    "breadth", "guidance", "evidence",
})
MARKET_CODE_RE = re.compile(r"[a-z][a-z0-9_]{1,15}")
VENUE_RE = re.compile(r"[A-Z][A-Z0-9_.\-]{1,15}")
# A symbol is at most a few characters, so a pattern long enough to be pathological is a pattern
# that is wrong. The cap is a guard rail, not a security boundary.
MAX_SYMBOL_PATTERN = 120


SCORE_WEIGHTS = {
    "core": {"liquidity": 0.35, "quality": 0.4, "independence": 0.15, "heat": 0.1},
    "satellite": {"liquidity": 0.25, "quality": 0.2, "independence": 0.4, "heat": 0.15},
    "tactical": {"liquidity": 0.45, "independence": 0.15, "heat": 0.4},
}
BETA_SCORE_WEIGHTS = {
    "liquidity": 0.25,
    "beta_strength": 0.35,
    "beta_stability": 0.25,
    "heat": 0.15,
}

METRIC_FIELDS = (
    "liquidity",
    "quality",
    "independence",
    "heat",
    "factor_r2",
    "beta_strength",
    "beta_stability",
)
# Window-dependent statistics. A model cannot know these without computing them, so the snapshot
# has to say which window and which source produced them; declaring them as judgement is refused.
MEASURED_ONLY_METRICS = {
    "liquidity", "factor_r2", "independence", "beta_strength", "beta_stability",
}
# Metrics that are a rank rather than a level. A percentile is a statement about a population,
# and the population here is whatever bench got researched -- sixty to a hundred and twenty
# names in a seed. 0.9 against a hundred researched names may be 0.4 against the market, so the
# declaration has to say what it was ranked against or the number is not comparable to anything.
CROSS_SECTIONAL_METRICS = {"liquidity"}
# `quality` is the heaviest weight in the core bucket and the least checkable thing in the file.
# It stays a judgement — durability is not a statistic — but where checkable facts exist they
# carry half of it, so the score cannot drift on opinion alone.
BLENDABLE_METRICS = {"quality"}
MEASUREMENT_BASES = {"measured", "judged", "blended"}
QUALITY_RULE_WEIGHT = 0.5
QUALITY_FLAG_PENALTY = 25
# Closed vocabulary, same reasoning as the exclusion codes: a flag that can be counted is worth
# more than a sentence that cannot. These seven are the ones every market states in some form,
# which is why they live here; the ones only one regulator issues live on that market's spec.
QUALITY_FLAG_CODES = {
    "risk_warning",
    "going_concern",
    "regulatory_action",
    "audit_qualification",
    "monitoring_tag",
    "restructuring",
    "loss_making",
}
QUALITY_FACT_FIELDS = ("listing_age_days", "size_rank_pct", "adverse_flags")
QUALITY_FLAG_RE = re.compile(r"[a-z][a-z0-9_]{2,31}")
# A market with a dozen flags of its own has stopped keeping a vocabulary and started keeping
# notes. The cap is what forces the researcher to name the few that change a decision.
MAX_MARKET_QUALITY_FLAGS = 6
# Survival is the one quality signal every market states the same way. The bands are coarse on
# purpose: the difference between four and five years of listing is not information.
LISTING_AGE_BANDS = ((1825, 100), (1095, 85), (730, 70), (365, 50), (180, 30))

# Closed vocabulary. Free text hides the reason a candidate lost its slot inside prose nobody
# aggregates; a code can be counted across rounds.
EXCLUSION_CODES = {
    "not_listed",
    "delisted_or_halted",
    "risk_warning_status",
    "wrong_venue",
    "excluded_instrument_type",
    "insufficient_liquidity",
    "insufficient_history",
    "redundant_with_member",
    "unverifiable_fact",
    "duplicate_asset",
    "other",
}
# Reasons this module writes into the selection audit itself.
AUDIT_CODES = {
    "outside_profile_coverage",
    "not_selected_under_budget",
    "removed_by_maintenance",
    "removed_by_downgrade",
    "not_in_seed_universe",
}
DECISION_OPS = {"ADD", "REMOVE", "REPLACE"}
THEME_OPS = {"ADD_THEME", "REMOVE_THEME", "UPDATE_THEME"}
# Theme structure is resolved before membership, so a MOVE or ADD can target a theme this same
# round created, and a theme can only be retired once its members have been placed elsewhere.
OP_ORDER = {
    "ADD_THEME": 0,
    "UPDATE_THEME": 0,
    "REMOVE": 1,
    "MOVE": 2,
    "REPLACE": 3,
    "ADD": 4,
    "REFRESH": 4,
    "REMOVE_THEME": 5,
    "NO_CHANGE": 6,
}
# Display weights allocate seats only in explicit legacy replay. Coverage-first uses the
# economic plan; Max freezes Heavy's distribution, independent of these display weights.
DEFAULT_THEME_WEIGHT = 1.0
# The range is a guard rail, not a judgement. Below a quarter a theme is not worth a row in the
# table; above four the apportionment is being used to hand-pick the universe, which is what the
# roles and the buckets are for.
MIN_THEME_WEIGHT = 0.25
MAX_THEME_WEIGHT = 4.0
# One theme holding more than this share of a universe is not an error — it may be exactly what
# the market looks like — but it is worth saying out loud, in the report and in the taxonomy check.
THEME_CONCENTRATION_NOTICE = 0.15
# Past this share of the target spent on the breadth floor, a table's weights order so little of
# the universe that saying so is worth an author's attention. The reviewed tables sit at 38-66%.
FLOOR_COST_NOTICE = 0.75
# What counts as a pool that walked away from its own table. Deliberately loose: a build hands
# unfilled slots to whichever theme still has candidates, so the honest reading of a busy theme
# is usually that its neighbours were thin, not that anything is wrong.
THEME_DRIFT_RATIO = 2.5
# A floor, because a ratio alone would fire on a theme holding two against an expectation of
# nought-point-seven, which is rounding, not drift. It sat at 5 while required seats were still
# counted against apportioned expectation — it was the only thing stopping that error from
# surfacing. With required seats out of the comparison it can come down to where it is useful:
# at Light most themes expect one to five members, so a floor of 5 made a theme at four times
# its share invisible in the tier most people build.
THEME_DRIFT_FLOOR = 3
# How far a bucket may sit above its profile target before the drift is reported.
BUCKET_DRIFT_TOLERANCE = 0.10
# Shake the ruler. Every measured number is an estimate, and the question index construction asks
# first is how much of the membership survives the estimate being slightly wrong. Nudge each
# measured metric by this much, in a direction drawn per ticker so the shift is a perturbation
# and not a rescaling, and report how many members come back. Two draws, because one draw that
# happens to flatter the pool is an anecdote.
STABILITY_SHIFT = 0.01
STABILITY_DRAWS = 2
STRONG_EVIDENCE_TIERS = {1, 2}

_THEME_RE = re.compile(r"^\d{2}_[A-Z]$")


class UniverseError(ValueError):
    pass


def read_json(path: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UniverseError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise UniverseError(f"{path} must contain a JSON object")
    return value


def default_policy_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "default-policy.json"


def load_policy(path: str | Path | None = None) -> dict[str, Any]:
    return read_json(path or default_policy_path())


def check_taxonomy(
    raw: Any,
    market: str,
    policy: dict[str, Any] | None = None,
    target: int | None = None,
    profile: str | None = None,
) -> dict[str, Any]:
    """Check display-table structure; economic feasibility belongs to the coverage plan.

    An explicit legacy policy additionally checks its theme floors and weighted allocation.
    """
    policy = policy or load_policy()
    errors: list[str] = []
    warnings: list[str] = []
    items = raw.get("taxonomy") if isinstance(raw, dict) else raw
    try:
        taxonomy = normalize_taxonomy(items or [])
    except UniverseError as exc:
        return {"passed": False, "errors": [str(exc)], "warnings": [], "stats": {}}
    if not taxonomy:
        return {"passed": False, "errors": ["taxonomy is empty"], "warnings": [], "stats": {}}

    names: dict[str, str] = {}
    for item in taxonomy:
        first = names.setdefault(item["l1_code"], item["l1_name"])
        if first != item["l1_name"]:
            errors.append(
                f"{item['theme_code']}: l1_code {item['l1_code']} is called both "
                f"{first!r} and {item['l1_name']!r}"
            )
        if not item["theme_name"].isascii():
            # It becomes a `###00_A_NAME` section header in the TradingView export, and what a
            # third-party importer does with non-ASCII there is not something to find out later.
            warnings.append(
                f"{item['theme_code']}: theme_name {item['theme_name']!r} is not ASCII; it is "
                "a TradingView section header. Put the local-language label in l1_name"
            )
    by_level = Counter(item["coverage_level"] for item in taxonomy)
    if not by_level[1]:
        errors.append("no theme at coverage_level 1; a Light universe would have nothing to hold")
    for l1_code in sorted(names):
        levels = {item["coverage_level"] for item in taxonomy if item["l1_code"] == l1_code}
        if 1 not in levels:
            warnings.append(
                f"{l1_code} {names[l1_code]!r} first appears at level {min(levels)}; "
                "this part of the market is invisible to a Light universe"
            )

    stats: dict[str, Any] = {
        "themes": len(taxonomy),
        "l1_groups": len(names),
        "weight_total": round(sum(theme_weight(item) for item in taxonomy), 3),
        "by_level": {str(level): by_level[level] for level in (1, 2, 3)},
        "capacity": {},
    }
    if profile is not None and profile not in PROFILES:
        raise UniverseError(f"profile must be one of {', '.join(PROFILES)}")
    if policy.get("selection_model") == "coverage_first":
        for name in (profile,) if profile else PROFILES:
            level = int(policy["profiles"][name]["coverage_level"])
            stats["capacity"][name] = {
                "themes": sum(item["coverage_level"] <= level for item in taxonomy),
                "target": target,
            }
        return {
            "passed": not errors,
            "scope": "display_structure_only",
            "errors": sorted(set(errors)),
            "warnings": sorted(set(warnings)),
            "stats": stats,
        }
    try:
        guidance = market_guidance(str(market).strip().lower(), policy, None)
    except UniverseError:
        guidance = None
    for name in (profile,) if profile else PROFILES:
        level = int(policy["profiles"][name]["coverage_level"])
        in_level = [item for item in taxonomy if int(item["coverage_level"]) <= level]
        reachable = len(in_level)
        want = target if target is not None else (
            int(guidance[name]["target"]) if guidance else None
        )
        stats["capacity"][name] = {
            "themes": reachable,
            "target": want,
            # What the breadth floor costs: every reachable theme takes a seat before weight is
            # consulted, so this share of the universe is settled by the table's shape and only
            # the rest is ordered by its weights. Not a defect — it is what makes the instrument
            # a survey rather than a shortlist — but an author about to tune `weight` should see
            # how much of the budget weight still reaches, and this is the command they run
            # before any research starts.
            "floor_share": round(reachable / want, 2) if want else None,
            "weight_total": round(sum(theme_weight(item) for item in in_level), 3),
            "expected": {
                code: round(share, 1)
                for code, share in sorted(expected_members(in_level, want or 0).items())
            } if want else {},
        }
        if want is None:
            continue
        if reachable > want:
            # Every theme inside the coverage level must hold at least one member, so this is not
            # a tight fit — it is a build that cannot validate.
            errors.append(
                f"{name}: {reachable} themes against a target of {want}; every theme must "
                "hold a member, so widen the target or raise some themes' coverage_level"
            )
        elif reachable > FLOOR_COST_NOTICE * want:
            # Disclosed always (`floor_share` above), warned about only here. The design called
            # for a warning at half the target, but the fourteen reviewed tables spend 38-66%
            # of Light on the floor — a warning that fires on ten of fourteen correct inputs is
            # a miscalibrated threshold, and the fastest way to teach an author to stop reading
            # warnings. The number is the disclosure; this is the point past which weight has
            # almost nothing left to order.
            warnings.append(
                f"{name}: the breadth floor spends {reachable} of {want} seats "
                f"({reachable / want:.0%}) giving every theme its first member, leaving "
                f"{want - reachable} for weight to order; the table's weights barely apply "
                "at this target"
            )
        for code, share in sorted(expected_members(in_level, want).items()):
            if share / want > THEME_CONCENTRATION_NOTICE:
                warnings.append(
                    f"{name}: {code} is weighted to about {share:.0f} of {want} members "
                    f"({share / want:.0%} of the universe); that is the table saying so, not a "
                    "limit — check it is what you meant"
                )
        if reachable + want > 1000:
            warnings.append(
                f"{name}: {reachable} themes + {want} tickers exceeds the 1000-token "
                "TradingView cap"
            )
    if target is None and not guidance:
        warnings.append(
            f"no size guidance for market {market!r}; pass --target to check capacity"
        )
    return {
        "passed": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "stats": stats,
    }


def theme_weight(item: dict[str, Any]) -> float:
    return float(item.get("weight") or DEFAULT_THEME_WEIGHT)


def theme_priority(weight: float, held: int) -> float:
    """Sainte-Laguë: the claim a theme has on the next free slot.

    A theme holding `held` members and carrying `weight` divides by `2 x held + 1`, so the first
    slot is cheap and each further one costs more. Run to convergence this apportions the
    universe to weight — three times the weight, about three times the members — without ever
    naming a ceiling, and a theme whose bench is empty drops out of the race instead of holding
    slots the way a quota would.
    """
    return float(weight) / float(2 * int(held) + 1)


def largest_remainder(target: int, shares: dict[str, Any]) -> dict[str, int]:
    """Hand out whole seats so that the parts add up to the whole.

    Flooring each share drops up to one seat per bucket, and the fill pass that picks them up
    gives them to `core` every time — core is 80% of the bench and sorts first — so the rounding
    loss is not noise, it is a standing transfer to the largest bucket. Nine of the fourteen
    markets lose a seat this way at Light. Largest remainder gives each leftover seat to the
    bucket with the most seat left over, which is the same discipline the themes already get
    from Sainte-Laguë: one apportionment method, used at both levels.
    """
    exact = {bucket: target * float(share) for bucket, share in shares.items()}
    seats = {bucket: math.floor(value) for bucket, value in exact.items()}
    # Sorted by remainder, then by name, so a tie between two buckets resolves the same way on
    # every machine — this decides a real seat.
    order = sorted(exact, key=lambda bucket: (-(exact[bucket] - seats[bucket]), bucket))
    leftover = max(0, min(target - sum(seats.values()), len(order)))
    for bucket in order[:leftover]:
        seats[bucket] += 1
    return seats


def expected_members(taxonomy: list[dict[str, Any]], target: int) -> dict[str, float]:
    """What apportionment converges on, if every theme had candidates enough to take its share."""
    total = sum(theme_weight(item) for item in taxonomy)
    if total <= 0:
        return {}
    return {
        item["theme_code"]: float(target) * theme_weight(item) / total for item in taxonomy
    }


def tier_guidance(breadth: float, policy: dict[str, Any]) -> dict[str, dict[str, int]]:
    """How big this market's Light, Medium and Heavy are.

    One number per market. A tier is a base size — 60, 160, 400 — scaled by the market's breadth:
    how much investable, liquid, separately-moving stock it actually lists. The US and the A-share
    market carry more distinguishable names than Brazil does, so the same depth of observation
    costs more tickers there, and pretending otherwise gave Brazil a Heavy universe it had to
    pad and the US a Light one that left whole sectors unwatched. The band around the target is
    the same everywhere: plus or minus a quarter, rounded to ten.
    """
    band = float(policy.get("guidance_band", 0.25))
    guidance: dict[str, dict[str, int]] = {}
    for profile in PROFILES:
        base = float(policy["tiers"][profile])
        target = max(5, int(round(base * float(breadth) / 5.0)) * 5)
        low = min(target, max(10, int(round(target * (1 - band) / 10.0)) * 10))
        high = max(target, int(round(target * (1 + band) / 10.0)) * 10)
        guidance[profile] = {"min": low, "target": target, "max": high}
    return guidance


def locales_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "locales"


def languages() -> tuple[str, ...]:
    return tuple(sorted(path.stem for path in locales_path().glob("*.json")))


def load_lexicon(language: str) -> dict[str, str]:
    """The words a report is written in, as data.

    Only the chrome is translated — headings, labels and the closed vocabularies. Those are
    finite, so a lexicon can be complete and a test can prove it. Human content comes from the
    snapshot and its authored report_translations, not from this fixed vocabulary file.
    """
    path = locales_path() / f"{language}.json"
    if not path.is_file():
        raise UniverseError(f"unknown language {language!r}; available: {', '.join(languages())}")
    return {key: str(value) for key, value in read_json(path).items()}


def normalize_report_translations(raw: Any) -> dict[str, dict[str, str]]:
    """Authored display text, kept separate from research facts and selection inputs."""
    if not isinstance(raw, dict):
        raise UniverseError("report_translations must be a language-keyed object")
    result = {}
    for language, entries in raw.items():
        if language not in languages() or not isinstance(entries, dict):
            raise UniverseError("report_translations requires a supported language and text map")
        if any(not isinstance(k, str) or not k.strip()
               or not isinstance(v, str) or not v.strip() for k, v in entries.items()):
            raise UniverseError("report_translations entries must be non-empty text pairs")
        result[language] = dict(entries)
    return result


def starter_taxonomy(market: str, profile: str | None = None) -> list[dict[str, Any]]:
    """The published theme table for a market, optionally cut to one profile's coverage level.

    Designing the taxonomy is the first step of a build and the one with no help in it: it needs
    domain judgement before any ticker has been looked at, and a taxonomy invented per run is why
    two universes of the same market turn out incomparable. This is a starting point to edit, not
    a fixed schema — but starting from an edit is a different task from starting from nothing.
    """
    spec = market_spec(market)
    taxonomy = normalize_taxonomy(resolve_taxonomy_file(taxonomy_path(spec.code)))
    if profile is None:
        return taxonomy
    if profile not in PROFILES:
        raise UniverseError(f"profile must be one of {', '.join(PROFILES)}")
    level = int(load_policy()["profiles"][profile]["coverage_level"])
    return [item for item in taxonomy if item["coverage_level"] <= level]


def taxonomy_path(name: str) -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "taxonomy" / f"{name}.json"


def resolve_taxonomy_file(path: Path, _seen: frozenset[str] = frozenset()) -> list[dict[str, Any]]:
    """Read a theme table, resolving the one inheritance step a market table is allowed.

    Fourteen markets do not have fourteen unrelated sector structures. Banks, semiconductors,
    pharma and utilities are the same idea in Frankfurt and in Toronto, and copying the shared
    skeleton into every file would mean a correction landing in one of them and not the other
    thirteen. So the shared part lives in `_equity.json` and a market file states only its
    delta: the groups it renames into its own language, the themes it does not have, the ones it
    has and nobody else does, and the weights that say which of them its market is actually
    about. A table that inherits nothing — crypto — just carries `taxonomy` and is read as is.
    """
    document = read_json(path)
    parent = document.get("extends")
    if not parent:
        return list(document.get("taxonomy") or [])
    parent = str(parent)
    if parent in _seen or parent == path.stem:
        raise UniverseError(f"taxonomy {path.stem}: extends cycle through {parent!r}")
    rows = {
        str(item.get("theme_code")): dict(item)
        for item in resolve_taxonomy_file(taxonomy_path(parent), _seen | {path.stem})
    }
    for code in document.get("drop") or []:
        if str(code) not in rows:
            raise UniverseError(f"taxonomy {path.stem}: drop names unknown theme {code}")
        rows.pop(str(code))
    for item in document.get("add") or []:
        rows[str(item.get("theme_code"))] = dict(item)
    for group, label in (document.get("groups") or {}).items():
        touched = [row for row in rows.values() if row.get("l1_code") == str(group)]
        if not touched:
            raise UniverseError(f"taxonomy {path.stem}: groups names unknown l1_code {group}")
        for row in touched:
            row["l1_name"] = label
    for code, patch in (document.get("rename") or {}).items():
        if str(code) not in rows:
            raise UniverseError(f"taxonomy {path.stem}: rename names unknown theme {code}")
        rows[str(code)].update(patch)
    for code, level in (document.get("level") or {}).items():
        if str(code) not in rows:
            raise UniverseError(f"taxonomy {path.stem}: level names unknown theme {code}")
        rows[str(code)]["coverage_level"] = level
    for code, weight in (document.get("weight") or {}).items():
        if str(code) not in rows:
            raise UniverseError(f"taxonomy {path.stem}: weight names unknown theme {code}")
        rows[str(code)]["weight"] = weight
    return list(rows.values())


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def universe_hash(universe: dict[str, Any]) -> str:
    """Hash membership and taxonomy, not run metadata or review history."""
    canonical = {
        "market": universe.get("market"),
        # Two universes built under different identity rules are not the same universe, so a
        # declared spec is part of what the hash protects rather than run metadata beside it.
        "market_spec": universe.get("market_spec"),
        "profile": universe.get("profile"),
        "taxonomy": universe.get("taxonomy") or [],
        "members": [
            {
                "ticker": item.get("ticker"),
                "asset_id": item.get("asset_id"),
                "theme_code": item.get("theme_code"),
                "role": item.get("role"),
                "required": bool(item.get("required", False)),
            }
            for item in universe.get("members") or []
        ],
    }
    if universe.get("selection_model") == "coverage_first":
        canonical["coverage_plan"] = universe.get("coverage_plan")
        canonical["admissions"] = [c.get("admission") for c in universe.get("members", [])]
    return canonical_hash(canonical)


def content_hash(universe: dict[str, Any]) -> str:
    """Fact/provenance integrity, separate from the stable membership version."""
    return canonical_hash({k: v for k, v in universe.items() if k != "content_hash"})


def market_spec(market: str) -> MarketSpec:
    spec = MARKET_SPECS.get(str(market).strip().lower())
    if spec is None:
        raise UniverseError(
            f"unsupported market {market!r}; registered: {', '.join(sorted(MARKETS))}. "
            "An unregistered market is buildable by declaring market_spec in the snapshot — "
            "see references/markets/adding-a-market.md"
        )
    return spec


def normalize_market_declaration(raw: Any, market: str) -> dict[str, Any]:
    """Check a snapshot-supplied market spec as hard as any other researched fact.

    This is the surface where invention is cheapest: a venue code and a symbol shape are easier
    to make up than a ticker and, unlike a ticker, a wrong one silently changes what counts as
    the same asset for every member at once. So it needs strong evidence, it is recorded in the
    universe rather than being resolved again next round, and it is covered by `version_hash` —
    two universes built under different identity rules are not the same universe.
    """
    if market in MARKET_SPECS:
        raise UniverseError(
            f"market {market!r} is registered; its rules are not snapshot-supplied"
        )
    if not isinstance(raw, dict):
        raise UniverseError(
            f"unsupported market {market!r}; registered: {', '.join(sorted(MARKETS))}. "
            "To build it anyway, declare market_spec in the snapshot — "
            "see references/markets/adding-a-market.md"
        )
    unknown = sorted(set(raw) - DECLARED_SPEC_FIELDS)
    if unknown:
        raise UniverseError(f"market_spec: unknown fields: {', '.join(unknown)}")
    code = str(raw.get("code", "")).strip().lower()
    if not MARKET_CODE_RE.fullmatch(code):
        raise UniverseError(f"market_spec: code {code!r} must be 2-16 lowercase letters or digits")
    if code != str(market).strip().lower():
        raise UniverseError(f"market_spec code {code!r} does not match the snapshot market")
    label = str(raw.get("label", "")).strip()
    if not label:
        raise UniverseError("market_spec: label is required")
    venues = sorted({str(item).strip().upper() for item in raw.get("venues") or []})
    if not venues:
        raise UniverseError("market_spec: at least one venue is required")
    for venue in venues:
        if not VENUE_RE.fullmatch(venue):
            raise UniverseError(f"market_spec: {venue!r} is not a TradingView venue code")
    pattern = str(raw.get("symbol_pattern", ""))
    if not pattern or len(pattern) > MAX_SYMBOL_PATTERN:
        raise UniverseError(
            f"market_spec: symbol_pattern is required and at most {MAX_SYMBOL_PATTERN} characters"
        )
    if ":" in pattern:
        raise UniverseError("market_spec: symbol_pattern matches the symbol, not the venue prefix")
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        raise UniverseError(
            f"market_spec: symbol_pattern is not a regular expression: {exc}"
        ) from exc
    if compiled.fullmatch(""):
        raise UniverseError("market_spec: symbol_pattern must not match an empty symbol")
    hint = str(raw.get("symbol_hint", "")).strip()
    if not hint:
        raise UniverseError("market_spec: symbol_hint is required; it is the error a user reads")
    language = str(raw.get("language") or "en").strip()
    if language not in languages():
        raise UniverseError(
            f"market_spec: no locale for {language!r}; ship one or omit the field to use en. "
            f"Available: {', '.join(languages())}"
        )
    strip = [str(item).strip().upper() for item in raw.get("asset_id_strip") or []]
    flags = sorted({str(item).strip().lower() for item in raw.get("quality_flags") or []})
    if len(flags) > MAX_MARKET_QUALITY_FLAGS:
        raise UniverseError(
            f"market_spec: at most {MAX_MARKET_QUALITY_FLAGS} quality_flags; "
            "a longer list is notes, not a vocabulary"
        )
    for flag in flags:
        if not QUALITY_FLAG_RE.fullmatch(flag):
            raise UniverseError(f"market_spec: quality flag {flag!r} must be a lowercase code")
        if flag in QUALITY_FLAG_CODES:
            # Redeclaring a universal code is how one market quietly gives it a second meaning,
            # and the counts in every report stop being comparable across markets.
            raise UniverseError(
                f"market_spec: quality flag {flag!r} is already universal; declare only the "
                "ones this market's regime issues and no other's does"
            )
    # Size is not optional for a declared market. The deeper tiers are defined relative to the
    # shallower ones, so a build with no stated Light size has no way to reach Medium except by
    # inventing one — and an invented range reports nothing when a universe is wrong. State it
    # the way a registered market does, as one breadth factor, or state the nine numbers.
    breadth = raw.get("breadth")
    guidance = raw.get("guidance")
    if (breadth is None) == (guidance is None):
        raise UniverseError(
            "market_spec: declare exactly one of breadth (a scale on the 60/160/400 tier bases, "
            "like every registered market) or guidance (min, target and max per tier)"
        )
    clean_breadth: float | None = None
    clean_guidance: dict[str, dict[str, int]] | None = None
    if breadth is not None:
        if isinstance(breadth, bool) or not isinstance(breadth, (int, float)):
            raise UniverseError("market_spec: breadth must be a number")
        if not 0.1 <= float(breadth) <= 3.0:
            raise UniverseError("market_spec: breadth must be between 0.1 and 3.0")
        clean_breadth = float(breadth)
    else:
        if not isinstance(guidance, dict) or set(guidance) != set(PROFILES):
            raise UniverseError(
                "market_spec: guidance must carry " + ", ".join(PROFILES) +
                " (min, target and max for each)"
            )
        clean_guidance = {}
        for profile in PROFILES:
            row = guidance[profile]
            if not isinstance(row, dict) or set(row) != {"min", "target", "max"}:
                raise UniverseError(f"market_spec: guidance.{profile} needs min, target and max")
            values = {key: int(row[key]) for key in ("min", "target", "max")}
            if not 0 < values["min"] <= values["target"] <= values["max"]:
                raise UniverseError(
                    f"market_spec: guidance.{profile} must be 0 < min <= target <= max"
                )
            clean_guidance[profile] = values
    subject = f"market_spec {code}"
    evidence = validate_evidence(raw.get("evidence") or [], subject)
    require_strong_evidence(evidence, subject)
    return {
        "code": code,
        "label": label,
        "language": language,
        "venues": venues,
        "symbol_pattern": pattern,
        "symbol_hint": hint,
        "venue_in_asset_id": bool(raw.get("venue_in_asset_id", False)),
        "asset_id_strip": strip,
        "factor_r2_required": bool(raw.get("factor_r2_required", False)),
        "quality_flags": flags,
        "breadth": clean_breadth,
        "guidance": clean_guidance,
        "evidence": evidence,
    }


def spec_from_declaration(declaration: dict[str, Any]) -> MarketSpec:
    return MarketSpec(
        code=declaration["code"],
        label=declaration["label"],
        venues=frozenset(declaration["venues"]),
        symbol_pattern=re.compile(declaration["symbol_pattern"]),
        symbol_hint=declaration["symbol_hint"],
        language=declaration["language"],
        venue_in_asset_id=declaration["venue_in_asset_id"],
        asset_id_strip=tuple(declaration["asset_id_strip"]),
        factor_r2_required=declaration["factor_r2_required"],
        quality_flags=frozenset(declaration.get("quality_flags") or ()),
        origin="declared",
    )


def resolve_market(market: str, declaration: Any = None) -> tuple[MarketSpec, dict | None]:
    """The registry row for a registered market, the snapshot's own for anything else."""
    if str(market).strip().lower() in MARKET_SPECS and not declaration:
        return market_spec(market), None
    clean = normalize_market_declaration(declaration, str(market).strip().lower())
    return spec_from_declaration(clean), clean


def _spec(value: str | MarketSpec) -> MarketSpec:
    return value if isinstance(value, MarketSpec) else market_spec(value)


def market_guidance(
    market: str, policy: dict[str, Any], declaration: dict[str, Any] | None
) -> dict[str, Any]:
    """How big this market's tiers are, derived from its breadth or stated outright.

    A registered market carries one number, its breadth, and the three tiers follow from it. A
    declared market may do the same, or state the nine numbers itself when it knows better than
    a scale factor can say.
    """
    if declaration:
        if declaration.get("guidance"):
            return declaration["guidance"]
        return tier_guidance(declaration["breadth"], policy)
    row = (policy.get("markets") or {}).get(market)
    if not row:
        raise UniverseError(f"policy carries no size guidance for market {market!r}")
    if "breadth" not in row:
        raise UniverseError(f"policy markets.{market} carries no breadth")
    return tier_guidance(row["breadth"], policy)


def declared_market_warnings(declaration: dict[str, Any] | None) -> list[str]:
    """Say, every time, that these rules were researched rather than reviewed.

    A declared market builds under exactly the same invariants as a registered one — that is the
    point of keeping the general logic general. What it does not carry is a second pair of eyes
    on the venue list and the symbol shape, and a report that did not say so would be claiming
    more than it knows.
    """
    if not declaration:
        return []
    warnings = [
        f"market {declaration['code']} is not registered; its venues "
        f"({', '.join(declaration['venues'])}), symbol shape and size guidance were declared in "
        "the snapshot and have not been reviewed by this skill"
    ]
    if declaration.get("quality_flags"):
        warnings.append(
            "market_spec declares the adverse flags "
            f"{', '.join(declaration['quality_flags'])}; they cost the same as any other flag "
            "and no locale translates them, so they print as codes"
        )
    return warnings


def split_ticker(ticker: str) -> tuple[str, str]:
    value = str(ticker).strip().upper()
    if ":" not in value:
        raise UniverseError(f"ticker must include TradingView venue: {ticker}")
    venue, symbol = value.split(":", 1)
    if not venue or not symbol:
        raise UniverseError(f"invalid ticker: {ticker}")
    return venue, symbol


def default_asset_id(market: str | MarketSpec, ticker: str) -> str:
    spec = _spec(market)
    venue, symbol = split_ticker(ticker)
    for suffix in spec.asset_id_strip:
        symbol = symbol.removesuffix(suffix)
    return f"{venue}:{symbol}" if spec.venue_in_asset_id else symbol


def validate_ticker(market: str | MarketSpec, ticker: str) -> list[str]:
    try:
        spec = _spec(market)
        venue, symbol = split_ticker(ticker)
    except UniverseError as exc:
        return [str(exc)]
    errors: list[str] = []
    if venue not in spec.venues:
        errors.append(
            f"{ticker}: unsupported {spec.code} venue; "
            f"expected one of {', '.join(sorted(spec.venues))}"
        )
    if not spec.symbol_pattern.fullmatch(symbol):
        errors.append(f"{ticker}: {spec.code} symbol must be {spec.symbol_hint}")
    elif spec.code == "cn":
        matches = {
            "SSE": symbol.startswith(("5", "6", "9", "000")),
            "SZSE": symbol.startswith(("0", "1", "2", "3")),
            "BSE": symbol.startswith(("4", "8", "92")),
        }
        if venue in matches and not matches[venue]:
            errors.append(f"{ticker}: venue does not match the CN code range")
    return errors


def normalize_taxonomy(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    taxonomy: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise UniverseError(f"taxonomy #{index} must be an object")
        theme_code = str(item.get("theme_code", "")).strip().upper()
        if not _THEME_RE.fullmatch(theme_code):
            raise UniverseError(f"taxonomy #{index} has invalid theme_code {theme_code!r}")
        if theme_code in seen:
            raise UniverseError(f"duplicate taxonomy theme {theme_code}")
        seen.add(theme_code)
        level = item.get("coverage_level")
        if level not in (1, 2, 3):
            raise UniverseError(f"{theme_code}: coverage_level must be 1, 2, or 3")
        l1_code = str(item.get("l1_code", "")).strip()
        if theme_code.split("_", 1)[0] != l1_code:
            raise UniverseError(f"{theme_code}: l1_code does not match theme prefix")
        l1_name = str(item.get("l1_name", "")).strip()
        theme_name = str(item.get("theme_name", "")).strip()
        if not l1_name or not theme_name:
            raise UniverseError(f"{theme_code}: l1_name and theme_name are required")
        if any(char in l1_name + theme_name for char in (",", "\n", "\r")):
            raise UniverseError(f"{theme_code}: taxonomy names cannot contain commas or newlines")
        raw_weight = item.get("weight", DEFAULT_THEME_WEIGHT)
        if isinstance(raw_weight, bool) or not isinstance(raw_weight, (int, float)):
            raise UniverseError(f"{theme_code}: weight must be a number")
        weight = float(raw_weight)
        if not MIN_THEME_WEIGHT <= weight <= MAX_THEME_WEIGHT:
            raise UniverseError(
                f"{theme_code}: weight {weight} is outside "
                f"{MIN_THEME_WEIGHT}-{MAX_THEME_WEIGHT}"
            )
        taxonomy.append({
            "l1_code": l1_code,
            "l1_name": l1_name,
            "theme_code": theme_code,
            "theme_name": theme_name,
            "coverage_level": level,
            "weight": weight,
        })
        if "purpose" in item:
            if not isinstance(item["purpose"], str) or not item["purpose"].strip():
                raise UniverseError(f"{theme_code}: purpose must be a non-empty sentence")
            taxonomy[-1]["purpose"] = item["purpose"].strip()
        if "representative_roles" in item:
            roles = item["representative_roles"]
            if (not isinstance(roles, list) or not roles
                    or any(not isinstance(r, str) or r not in CORE_ROLES for r in roles)):
                raise UniverseError(f"{theme_code}: representative_roles must name core roles")
            if not taxonomy[-1].get("purpose"):
                raise UniverseError(f"{theme_code}: representative_roles requires purpose")
            taxonomy[-1]["representative_roles"] = sorted(set(roles))
    return sorted(taxonomy, key=lambda item: item["theme_code"])


def _score_value(value: Any, field: str, ticker: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise UniverseError(f"{ticker}: metric {field} must be numeric or null")
    number = float(value)
    if not 0 <= number <= 100:
        raise UniverseError(f"{ticker}: metric {field} must be between 0 and 100")
    return number


def validate_evidence(evidence: Any, subject: str) -> list[dict[str, Any]]:
    if not isinstance(evidence, list) or not evidence:
        raise UniverseError(f"{subject}: at least one evidence item is required")
    for item in evidence:
        url = str(item.get("url", "")) if isinstance(item, dict) else ""
        if not url.startswith(("http://", "https://")):
            raise UniverseError(f"{subject}: every evidence item needs an http(s) URL")
        if _parse_date(item.get("as_of")) is None:
            raise UniverseError(f"{subject}: every evidence item needs an ISO as_of date")
        if type(item.get("tier")) is not int or item["tier"] not in (1, 2, 3):
            raise UniverseError(f"{subject}: every evidence item needs tier 1, 2, or 3")
    return deepcopy(evidence)


def require_strong_evidence(evidence: list[dict[str, Any]], subject: str) -> None:
    """Admission and removal need a primary or auditable source, never market narrative alone."""
    if not any(int(item["tier"]) in STRONG_EVIDENCE_TIERS for item in evidence):
        raise UniverseError(f"{subject}: needs at least one tier 1 or tier 2 evidence item")


def _parse_date(value: Any) -> date | None:
    try:
        parsed = date.fromisoformat(value)
        return parsed if parsed.isoformat() == value else None
    except (TypeError, ValueError):
        return None


def staleness_warnings(
    as_of: str, evidence_groups: list[tuple[str, list[dict[str, Any]]]], policy: dict[str, Any]
) -> list[str]:
    """Evidence that predates the snapshot by more than the policy window is reported, not trusted
    silently. An `as_of` in the future is always wrong and is reported the same way."""
    reference = _parse_date(as_of)
    limit = int((policy.get("freshness") or {}).get("evidence_warning_days", 180))
    if reference is None:
        return [f"as_of {as_of!r} is not an ISO date"]
    warnings: list[str] = []
    for subject, evidence in evidence_groups:
        for item in evidence:
            stamped = _parse_date(item.get("as_of"))
            if stamped is None:
                stale = item.get("as_of")
                warnings.append(f"{subject}: evidence as_of {stale!r} is not an ISO date")
            elif stamped > reference:
                warnings.append(f"{subject}: evidence as_of {stamped} is after the snapshot")
            elif (reference - stamped).days > limit:
                warnings.append(
                    f"{subject}: evidence is {(reference - stamped).days} days older than the "
                    f"snapshot (limit {limit})"
                )
    return sorted(set(warnings))


def normalize_measurement(
    raw: Any, used_fields: set[str], blended: set[str] | None = None
) -> dict[str, dict[str, Any]]:
    """Every populated metric must say how it was produced.

    `measured` carries a window and a source; `judged` carries a method and nothing else;
    `blended` means a rule component computed from declared facts plus a judged remainder, and
    carries the source those facts were read from. The window-dependent statistics cannot be
    declared `judged` — a model that has not run the regression does not have the number, and a
    filled-in guess is indistinguishable from one.

    `blended` is not optional where it applies: if the candidates carry `quality_facts`, the
    declaration has to say so, and if they do not, it may not claim they do.
    """
    blended = set(blended or ())
    if not isinstance(raw, dict):
        raise UniverseError("measurement must be an object keyed by metric name")
    declared: dict[str, dict[str, Any]] = {}
    for field, entry in raw.items():
        if field not in METRIC_FIELDS:
            raise UniverseError(f"measurement: unknown metric {field!r}")
        if not isinstance(entry, dict):
            raise UniverseError(f"measurement {field}: must be an object")
        basis = str(entry.get("basis", "")).strip().lower()
        if basis not in MEASUREMENT_BASES:
            raise UniverseError(
                f"measurement {field}: basis must be {', '.join(sorted(MEASUREMENT_BASES))}"
            )
        method = str(entry.get("method", "")).strip()
        if not method:
            raise UniverseError(f"measurement {field}: method is required")
        if basis == "judged" and field in MEASURED_ONLY_METRICS:
            raise UniverseError(f"measurement {field}: this metric cannot be judged, only measured")
        if basis == "blended" and field not in BLENDABLE_METRICS:
            raise UniverseError(f"measurement {field}: this metric cannot be blended")
        if field in blended and basis != "blended":
            raise UniverseError(
                f"measurement {field}: candidates carry quality_facts, so declare it as blended"
            )
        if basis == "blended" and field not in blended:
            raise UniverseError(
                f"measurement {field}: declared blended but no candidate carries quality_facts"
            )
        item = {"basis": basis, "method": method}
        if basis in {"measured", "blended"}:
            source = str(entry.get("source", "")).strip()
            if not source.startswith(("http://", "https://")):
                raise UniverseError(f"measurement {field}: {basis} metrics need a source URL")
            item["source"] = source
        if basis == "measured":
            window = str(entry.get("window", "")).strip()
            if not window:
                raise UniverseError(f"measurement {field}: measured metrics need a window")
            item["window"] = window
        if "population" in entry:
            population = entry["population"]
            if not isinstance(population, int) or isinstance(population, bool) or population < 1:
                raise UniverseError(
                    f"measurement {field}: population must be a positive whole number of tickers"
                )
            item["population"] = population
        declared[field] = item
    missing = sorted(used_fields - set(declared))
    if missing:
        raise UniverseError("metrics used without a measurement declaration: " + ", ".join(missing))
    return dict(sorted(declared.items()))


def measurement_warnings(measurement: dict[str, dict[str, Any]]) -> list[str]:
    """A rank without its population is a number nobody can compare to another universe's."""
    return [
        f"measurement {field}: a cross-sectional percentile with no population; "
        "state how many tickers it was ranked against"
        for field in sorted(CROSS_SECTIONAL_METRICS & set(measurement))
        if "population" not in measurement[field]
    ]


def quality_flag_codes(rules: Any = None) -> frozenset[str]:
    """The adverse flags this market can record: the universal ones plus its own."""
    if rules is None:
        return frozenset(QUALITY_FLAG_CODES)
    return frozenset(QUALITY_FLAG_CODES) | _spec(rules).quality_flags


def normalize_quality_facts(raw: Any, ticker: str, rules: Any = None) -> dict[str, Any] | None:
    """Checkable inputs to `quality`, or None when the candidate offers none.

    Every field here is something a person can look up and disagree with by citing a source,
    which is the difference between it and the judged half of the score.
    """
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise UniverseError(f"{ticker}: quality_facts must be an object")
    unknown = sorted(set(raw) - set(QUALITY_FACT_FIELDS))
    if unknown:
        raise UniverseError(f"{ticker}: unknown quality_facts fields: {', '.join(unknown)}")
    facts: dict[str, Any] = {}
    age = raw.get("listing_age_days")
    if age is not None:
        if isinstance(age, bool) or not isinstance(age, (int, float)) or age < 0:
            raise UniverseError(f"{ticker}: listing_age_days must be a non-negative number")
        facts["listing_age_days"] = int(age)
    size = raw.get("size_rank_pct")
    if size is not None:
        facts["size_rank_pct"] = _score_value(size, "size_rank_pct", ticker)
    flags = raw.get("adverse_flags") or []
    if not isinstance(flags, list):
        raise UniverseError(f"{ticker}: adverse_flags must be a list")
    known = quality_flag_codes(rules)
    codes = sorted({str(flag).strip() for flag in flags if str(flag).strip()})
    for code in codes:
        if code not in known:
            # A flag another market issues is named separately, because a CN snapshot carrying
            # `late_filing` is not a typo — it is a researcher reaching for the wrong regime.
            elsewhere = sorted(
                spec.code for spec in MARKET_SPECS.values() if code in spec.quality_flags
            )
            hint = (
                f"; {code!r} belongs to {', '.join(elsewhere)}"
                if elsewhere else ""
            )
            raise UniverseError(
                f"{ticker}: unknown adverse flag {code!r}{hint}; "
                f"known: {', '.join(sorted(known))}"
            )
    facts["adverse_flags"] = codes
    if "listing_age_days" not in facts and "size_rank_pct" not in facts:
        raise UniverseError(
            f"{ticker}: quality_facts needs listing_age_days or size_rank_pct; "
            "adverse flags alone do not make a score"
        )
    return facts


def quality_rule_score(facts: dict[str, Any] | None) -> float | None:
    if not facts:
        return None
    parts: list[float] = []
    age = facts.get("listing_age_days")
    if age is not None:
        parts.append(float(next((score for days, score in LISTING_AGE_BANDS if age >= days), 10)))
    size = facts.get("size_rank_pct")
    if size is not None:
        parts.append(float(size))
    if not parts:
        return None
    penalty = QUALITY_FLAG_PENALTY * len(facts.get("adverse_flags") or [])
    return min(100.0, max(0.0, sum(parts) / len(parts) - penalty))


def blended_metrics(candidates: list[dict[str, Any]]) -> set[str]:
    """Which metrics actually carry a rule component in this universe."""
    if any(item.get("quality_facts") for item in candidates):
        return {"quality"}
    return set()


def metrics_in_use(candidates: list[dict[str, Any]]) -> set[str]:
    return {
        field
        for candidate in candidates
        for field in METRIC_FIELDS
        if candidate.get("metrics", {}).get(field) is not None
    }


def normalize_candidate(
    market: str | MarketSpec,
    raw: dict[str, Any],
    taxonomy_by_code: dict[str, dict[str, Any]],
    *,
    coverage_first: bool = False,
) -> dict[str, Any]:
    ticker = str(raw.get("ticker", "")).strip().upper()
    ticker_errors = validate_ticker(market, ticker)
    if ticker_errors:
        raise UniverseError("; ".join(ticker_errors))
    theme_code = str(raw.get("theme_code", "")).strip().upper()
    if theme_code not in taxonomy_by_code:
        raise UniverseError(f"{ticker}: unknown theme {theme_code}")
    role = str(raw.get("role", "")).strip().upper()
    if role not in ROLES:
        raise UniverseError(f"{ticker}: invalid role {role!r}")
    evidence = validate_evidence(raw.get("evidence") or [], ticker)
    raw_metrics = raw.get("metrics") or {}
    if not isinstance(raw_metrics, dict):
        raise UniverseError(f"{ticker}: metrics must be an object")
    unknown = sorted(set(raw_metrics) - set(METRIC_FIELDS))
    if unknown:
        raise UniverseError(f"{ticker}: unknown metric fields: {', '.join(unknown)}")
    metrics = {
        field: _score_value(raw_metrics.get(field), field, ticker) for field in METRIC_FIELDS
    }
    if metrics["factor_r2"] is not None:
        derived_independence = 100 - metrics["factor_r2"]
        if metrics["independence"] is not None and abs(
            metrics["independence"] - derived_independence
        ) > 5:
            raise UniverseError(
                f"{ticker}: independence must equal 100 - factor_r2 within five points"
            )
        metrics["independence"] = derived_independence
    eligible = bool(raw.get("eligible", False))
    if not isinstance(raw.get("eligible", False), bool):
        raise UniverseError(f"{ticker}: eligible must be a boolean")
    exclusion_reasons = [
        str(item).strip() for item in raw.get("exclusion_reasons", []) if str(item).strip()
    ]
    for reason in exclusion_reasons:
        code = reason.split(":", 1)[0].strip()
        if code not in EXCLUSION_CODES:
            raise UniverseError(
                f"{ticker}: exclusion reason must start with one of "
                f"{', '.join(sorted(EXCLUSION_CODES))}; got {code!r}"
            )
    if not eligible and not exclusion_reasons:
        raise UniverseError(f"{ticker}: ineligible candidate requires exclusion_reasons")
    if eligible and metrics["liquidity"] is None and role not in {"BENCHMARK", "ANCHOR"}:
        raise UniverseError(f"{ticker}: non-anchor candidate requires a liquidity score")
    spec = _spec(market)
    # Coverage satellites describe supplementary businesses, not a price amplifier.
    # The admission contract is checked independently; legacy roles retain their gates.
    supplementary_beta = (coverage_first and role == "BETA_SATELLITE"
                          and isinstance(raw.get("admission"), dict)
                          and raw["admission"].get("kind") == "satellite")
    if (
        eligible
        and spec.factor_r2_required
        and role not in FACTOR_EXEMPT_ROLES
        and not supplementary_beta
    ):
        if metrics["factor_r2"] is None:
            raise UniverseError(
                f"{ticker}: established {spec.code} candidates require factor_r2"
            )
    if eligible and role == "INDEPENDENT_SENSOR" and (
        metrics["independence"] is None or metrics["independence"] < 50
    ):
        raise UniverseError(f"{ticker}: INDEPENDENT_SENSOR requires independence >= 50")
    if eligible and role == "BETA_SATELLITE" and not supplementary_beta and (
        metrics["beta_strength"] is None or metrics["beta_stability"] is None
    ):
        raise UniverseError(f"{ticker}: BETA_SATELLITE requires beta_strength and beta_stability")
    if eligible and metrics["independence"] is not None and metrics["factor_r2"] is None:
        raise UniverseError(f"{ticker}: independence requires measured factor_r2")
    if eligible and role == "BETA_SATELLITE" and not supplementary_beta and (
        metrics["factor_r2"] is None or metrics["factor_r2"] < 30
        or metrics["beta_strength"] < 55 or metrics["beta_stability"] < 50
    ):
        raise UniverseError(
            f"{ticker}: BETA_SATELLITE requires R2 >= 30, positive beta strength >= 55 "
            "and stability >= 50"
        )
    if eligible and role in {"LIQUIDITY_SENSOR", "NEW_LISTING"} and metrics["heat"] is None:
        raise UniverseError(f"{ticker}: tactical roles require a heat score")
    reason = str(raw.get("reason", "")).strip()
    listing = deepcopy(raw.get("listing"))
    if eligible:
        require_strong_evidence(evidence, ticker)
        if not isinstance(raw.get("reason"), str) or not reason:
            raise UniverseError(f"{ticker}: eligible candidate requires a reason")
        if not isinstance(listing, dict) or listing.get("status") != "active":
            raise UniverseError(f"{ticker}: eligible candidate requires an active listing check")
        if _parse_date(listing.get("as_of")) is None:
            raise UniverseError(f"{ticker}: listing as_of must be an ISO date")
        strong_urls = {item["url"] for item in evidence if item["tier"] in (1, 2)}
        if listing.get("source") not in strong_urls:
            raise UniverseError(f"{ticker}: listing source must be present in strong evidence")
    asset_id = str(raw.get("asset_id") or default_asset_id(market, ticker)).strip().upper()
    if not asset_id:
        raise UniverseError(f"{ticker}: asset_id is empty")
    quality_facts = normalize_quality_facts(raw.get("quality_facts"), ticker, spec)
    rule_score = quality_rule_score(quality_facts)
    if quality_facts is not None and metrics["quality"] is None:
        raise UniverseError(
            f"{ticker}: quality_facts supply half the score; the judged half is still required"
        )
    # Derived, never stored back into metrics: `metrics.quality` stays the judged input, so
    # re-normalizing an already-built member reaches the same blend instead of compounding it.
    quality_score = metrics["quality"] if rule_score is None else round(
        QUALITY_RULE_WEIGHT * rule_score + (1 - QUALITY_RULE_WEIGHT) * float(metrics["quality"]), 1
    )
    taxonomy = taxonomy_by_code[theme_code]
    candidate = {
        "ticker": ticker,
        "asset_id": asset_id,
        "name": str(raw.get("name", "")).strip() or asset_id,
        "theme_code": theme_code,
        "l1_code": taxonomy["l1_code"],
        "role": role,
        "required": bool(raw.get("required", False)),
        "eligible": eligible,
        "exclusion_reasons": exclusion_reasons,
        "metrics": metrics,
        "quality_facts": quality_facts,
        "quality_rule_score": rule_score,
        "quality_score": quality_score,
        "evidence": evidence,
        "reason": reason,
        "listing": listing,
        "measurement_record": deepcopy(raw.get("measurement_record")),
        "tags": sorted({str(tag).strip() for tag in raw.get("tags", []) if str(tag).strip()}),
    }
    if "admission" in raw:
        candidate["admission"] = deepcopy(raw["admission"])
    if "reason_summary" in raw:
        summary = raw["reason_summary"]
        if not isinstance(summary, str) or not summary.strip() or len(summary) > 160 \
                or "\n" in summary or "\r" in summary:
            raise UniverseError(f"{ticker}: reason_summary must be one line of 1–160 characters")
        candidate["reason_summary"] = summary.strip()
    candidate["scored_on"] = score_coverage(candidate)
    return candidate


def normalize_snapshot(snapshot: dict[str, Any], *, coverage_first: bool = False) -> dict[str, Any]:
    rules, declaration = resolve_market(
        snapshot.get("market", ""), snapshot.get("market_spec")
    )
    market = rules.code
    if snapshot.get("schema_version") != 1:
        raise UniverseError("snapshot schema_version must be 1")
    if snapshot.get("complete") is not True:
        raise UniverseError("snapshot is incomplete; refusing a formal build")
    if not snapshot.get("as_of"):
        raise UniverseError("snapshot as_of is required")
    sources = validate_evidence(snapshot.get("sources") or [], "snapshot")
    require_strong_evidence(sources, "snapshot")
    taxonomy = normalize_taxonomy(snapshot.get("taxonomy") or [])
    if not taxonomy:
        raise UniverseError("snapshot taxonomy is empty")
    taxonomy_by_code = {item["theme_code"]: item for item in taxonomy}
    candidates = [
        normalize_candidate(rules, item, taxonomy_by_code, coverage_first=coverage_first)
        for item in snapshot.get("candidates") or []
    ]
    fact_errors = candidate_date_errors(candidates, str(snapshot["as_of"]))
    reference = _parse_date(snapshot["as_of"])
    if reference and any(
        _parse_date(e.get("as_of")) and _parse_date(e["as_of"]) > reference
        for e in sources
    ):
        fact_errors.append("snapshot source evidence is future-dated")
    if fact_errors:
        raise UniverseError("; ".join(fact_errors))
    seen_tickers: set[str] = set()
    seen_assets: set[str] = set()
    for candidate in candidates:
        if candidate["ticker"] in seen_tickers:
            raise UniverseError(f"duplicate ticker in snapshot: {candidate['ticker']}")
        if candidate["asset_id"] in seen_assets:
            raise UniverseError(f"duplicate economic asset in snapshot: {candidate['asset_id']}")
        seen_tickers.add(candidate["ticker"])
        seen_assets.add(candidate["asset_id"])
    measurement = normalize_measurement(
        snapshot.get("measurement") or {},
        metrics_in_use(candidates),
        blended_metrics(candidates),
    )
    return {
        "schema_version": 1,
        "market": market,
        "market_spec": declaration,
        "as_of": str(snapshot["as_of"]),
        "complete": True,
        "sources": deepcopy(sources),
        "measurement": measurement,
        "measurement_audit": deepcopy(snapshot.get("measurement_audit") or {}),
        "taxonomy": taxonomy,
        "candidates": candidates,
        "notes": deepcopy(snapshot.get("notes") or []),
        "coverage": deepcopy(snapshot.get("coverage") or {}),
        **({"report_translations": normalize_report_translations(snapshot["report_translations"])}
           if "report_translations" in snapshot else {}),
    }


def candidate_date_errors(candidates: list[dict], as_of: str) -> list[str]:
    reference = _parse_date(as_of)
    if reference is None:
        return ["snapshot as_of must be an ISO date"]
    errors = []
    for item in candidates:
        if not item.get("eligible"):
            continue
        checked = _parse_date((item.get("listing") or {}).get("as_of"))
        if checked and not 0 <= (reference - checked).days <= 30:
            errors.append(f"{item['ticker']}: listing check is future-dated or older than 30 days")
        record = item.get("measurement_record") or {}
        if not record and any(item["metrics"].get(k) is not None for k in MEASURED_ONLY_METRICS):
            errors.append(f"{item['ticker']}: measured metrics require a measurement_record")
        if record and not isinstance(record, dict):
            errors.append(f"{item['ticker']}: measurement_record must be an object")
            continue
        if record:
            if not re.fullmatch(r"[a-f0-9]{64}", str(record.get("data_sha256", ""))):
                errors.append(f"{item['ticker']}: measurement_record needs an input SHA-256")
            first = _parse_date(record.get("first_session"))
            last = _parse_date(record.get("last_session"))
            measured_at = _parse_date(record.get("as_of"))
            if (not first or not last or not measured_at
                    or not first <= last <= measured_at <= reference):
                errors.append(f"{item['ticker']}: invalid measurement_record date boundaries")
            if not str(record.get("source", "")).startswith(("http://", "https://")):
                errors.append(f"{item['ticker']}: measurement_record requires a source URL")
            if item["metrics"].get("liquidity") is not None and (
                not isinstance(record.get("liquidity_observations"), int)
                or record["liquidity_observations"] < 1
            ):
                errors.append(f"{item['ticker']}: liquidity record requires observations")
            if any(item["metrics"].get(k) is not None
                   for k in ("factor_r2", "beta_strength", "beta_stability")) and (
                not isinstance(record.get("observations"), int)
                or record["observations"] < 30 or not record.get("benchmarks")
            ):
                errors.append(
                    f"{item['ticker']}: factor record requires 30 observations and gauge legs"
                )
        if any(_parse_date(e.get("as_of")) and _parse_date(e["as_of"]) > reference
               for e in item.get("evidence", [])):
            errors.append(f"{item['ticker']}: evidence is future-dated")
        end = _parse_date(record.get("last_session"))
        if end and end > reference:
            errors.append(f"{item['ticker']}: measurement includes observations after as_of")
        if end and (reference - end).days > 10:
            errors.append(f"{item['ticker']}: measured quote is stale (over 10 days)")
    return errors


def candidate_bucket(candidate: dict[str, Any]) -> str:
    return BUCKET_BY_ROLE[candidate["role"]]


def _score_inputs(candidate: dict[str, Any]) -> tuple[dict[str, float], dict[str, float]]:
    """The weights this candidate is judged on, and the values it actually brought to them."""
    values = dict(candidate["metrics"])
    if candidate.get("quality_score") is not None:
        values["quality"] = candidate["quality_score"]
    weights = (
        BETA_SCORE_WEIGHTS
        if candidate["role"] == "BETA_SATELLITE"
        else SCORE_WEIGHTS[candidate_bucket(candidate)]
    )
    return weights, values


def metric_score(candidate: dict[str, Any]) -> float:
    """Score against the full denominator, so an absent field costs exactly what it weighs.

    Renormalizing over the fields that happen to be present rewards silence: a candidate
    carrying only `liquidity` at 0.95 would beat one carrying 0.90 / 0.85 / 0.80 / 0.75 across
    all four. And the silence is manufactured on purpose -- measurement.md requires that a
    ticker with no usable volume gets no liquidity score rather than a guessed one -- so the
    honesty rule was feeding the scoring rule exactly the input it paid for. A metric nobody
    measured does not earn a seat here, and it does not get out of the way either.
    """
    weights, values = _score_inputs(candidate)
    earned = sum(
        float(values[field]) * weight
        for field, weight in weights.items()
        if values.get(field) is not None
    )
    return earned / sum(weights.values())


def score_coverage(candidate: dict[str, Any]) -> dict[str, int]:
    """How many of the fields this candidate was scored on carried a value.

    A bare score cannot be read without it: 0.62 from four fields and 0.62 from two are not the
    same claim, and only the second one is partly a statement about missing research.
    """
    weights, values = _score_inputs(candidate)
    return {
        "present": sum(1 for field in weights if values.get(field) is not None),
        "of": len(weights),
    }


def _is_partially_scored(candidate: dict[str, Any]) -> bool:
    coverage = score_coverage(candidate)
    return coverage["present"] < coverage["of"]


def rank_key(candidate: dict[str, Any]) -> tuple[float, float, str]:
    return (-ROLE_ORDER[candidate["role"]], -metric_score(candidate), candidate["ticker"])


def _add_candidate(
    selected: list[dict[str, Any]],
    selected_assets: set[str],
    theme_counts: Counter[str],
    candidate: dict[str, Any],
) -> bool:
    if candidate["asset_id"] in selected_assets:
        return False
    selected.append(candidate)
    selected_assets.add(candidate["asset_id"])
    theme_counts[candidate["theme_code"]] += 1
    return True


def _select_stage(
    *,
    candidates: list[dict[str, Any]],
    taxonomy: list[dict[str, Any]],
    profile: str,
    target: int,
    profile_policy: dict[str, Any],
    seed: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    coverage_level = int(profile_policy["coverage_level"])
    allowed_themes = [
        item for item in taxonomy if int(item["coverage_level"]) <= coverage_level
    ]
    allowed_codes = {item["theme_code"] for item in allowed_themes}
    eligible = [
        candidate for candidate in candidates
        if candidate["eligible"] and candidate["theme_code"] in allowed_codes
    ]
    by_theme: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in eligible:
        by_theme[candidate["theme_code"]].append(candidate)
    for values in by_theme.values():
        values.sort(key=rank_key)

    missing = [item["theme_code"] for item in allowed_themes if not by_theme[item["theme_code"]]]
    if missing:
        raise UniverseError(
            f"{profile}: no eligible candidate for required themes: {', '.join(missing)}"
        )
    missing_representatives = [t["theme_code"] for t in allowed_themes
                              if t.get("representative_roles") and not any(
                                  c["role"] in t["representative_roles"]
                                  for c in by_theme[t["theme_code"]])]
    if missing_representatives:
        raise UniverseError(f"{profile}: no qualified representative for duties: "
                            + ", ".join(missing_representatives))

    selected = list(seed)
    selected_assets = {item["asset_id"] for item in selected}
    theme_counts = Counter(item["theme_code"] for item in selected)
    warnings: list[str] = []

    required = sorted(
        (item for item in eligible if item["required"]),
        key=lambda item: (item["theme_code"], rank_key(item)),
    )
    for candidate in required:
        _add_candidate(selected, selected_assets, theme_counts, candidate)

    # Breadth first, and only one deep. Every theme inside the coverage level holds a member
    # before any theme holds a second, so the instrument still looks at the whole market no
    # matter how lopsided the weights are.
    for theme in allowed_themes:
        roles = theme.get("representative_roles")
        represented = any(c["theme_code"] == theme["theme_code"] and
                          (not roles or c["role"] in roles) for c in selected)
        if not represented:
            _add_candidate(
                selected, selected_assets, theme_counts,
                next(c for c in by_theme[theme["theme_code"]] if not roles or c["role"] in roles),
            )

    if len(selected) > target:
        raise UniverseError(
            f"{profile}: anchors and required theme coverage need {len(selected)} slots, "
            f"target is {target}"
        )

    quotas = largest_remainder(target, profile_policy["bucket_targets"])
    bucket_counts = Counter(candidate_bucket(item) for item in selected)

    # Max extends the inherited Heavy instrument. Spend the incremental beta budget first,
    # across themes by the same weighted apportionment; never relabel weak candidates to fill it.
    beta_goal = math.ceil(max(0, target - len(seed)) * float(
        profile_policy.get("incremental_beta_share", 0)
    )) if seed else 0
    added_beta = 0
    for _ in range(beta_goal):
        choices = [c for c in eligible
                   if c["role"] == "BETA_SATELLITE" and c["asset_id"] not in selected_assets]
        if not choices or len(selected) >= target:
            break
        weights = {t["theme_code"]: theme_weight(t) for t in allowed_themes}
        best = min(choices, key=lambda c: (
            -theme_priority(weights[c["theme_code"]], theme_counts[c["theme_code"]]), rank_key(c),
        ))
        _add_candidate(selected, selected_assets, theme_counts, best)
        bucket_counts["satellite"] += 1
        added_beta += 1
    if added_beta < beta_goal:
        warnings.append(
            f"{profile}: qualified beta additions filled {added_beta} of {beta_goal}; "
            "remaining slots follow ordinary gates"
        )

    def next_in(theme_code: str, respect_quota: bool) -> dict[str, Any] | None:
        for candidate in by_theme[theme_code]:
            if candidate["asset_id"] in selected_assets:
                continue
            bucket = candidate_bucket(candidate)
            if respect_quota and bucket_counts[bucket] >= quotas.get(bucket, 0):
                continue
            return candidate
        return None

    # Two passes over the same apportionment. The first respects the bucket quotas, so the
    # core/satellite/tactical shape of the tier is what steers which candidate a theme offers;
    # the second fills what the first could not place, since a quota is an entitlement and not
    # a promise that the bench can meet it. By then the shape is already set.
    for respect_quota in (True, False):
        while len(selected) < target:
            best_key: tuple[Any, ...] | None = None
            best_candidate: dict[str, Any] | None = None
            for theme in allowed_themes:
                code = theme["theme_code"]
                candidate = next_in(code, respect_quota)
                if candidate is None:
                    continue
                key = (
                    -theme_priority(theme_weight(theme), theme_counts[code]),
                    rank_key(candidate),
                    code,
                )
                if best_key is None or key < best_key:
                    best_key, best_candidate = key, candidate
            if best_candidate is None:
                break
            _add_candidate(selected, selected_assets, theme_counts, best_candidate)
            bucket_counts[candidate_bucket(best_candidate)] += 1

    if len(selected) < target:
        warnings.append(
            f"qualified universe filled {len(selected)} of {target}; "
            "eligibility was not relaxed"
        )
    return selected, warnings


def _jitter(candidates: list[dict[str, Any]], draw: int) -> list[dict[str, Any]]:
    """The same bench with every measured number nudged, to see whether the seats move.

    The direction is drawn per ticker and per field from a hash, which matters more than it
    looks: shifting every number the same way is a rescaling, and `metric_score` is linear, so
    a uniform shift reorders nothing and would report perfect stability on any input. Real
    measurement error is independent per number, so the draw is too — and taken from a digest
    rather than an RNG, so the number a build reports is the number it reports on any machine,
    in any order, forever.

    Judged fields are left alone. A judgement is not an estimate with an error bar, and nudging
    one would measure how sensitive the pool is to the author's opinion, which is a different
    question and not one a ±1% shift can ask.
    """
    shifted = []
    for candidate in candidates:
        metrics = dict(candidate["metrics"])
        for field in sorted(MEASURED_ONLY_METRICS & set(metrics)):
            if field == "independence":
                continue
            value = metrics[field]
            if value is None:
                continue
            seed = f"{draw}:{candidate['asset_id']}:{field}".encode()
            sign = 1 if hashlib.sha256(seed).digest()[0] & 1 else -1
            # Metrics are 0..100, the range `_score_value` enforces, and a nudge may not walk
            # a value out of it.
            metrics[field] = min(100.0, max(0.0, float(value) * (1 + sign * STABILITY_SHIFT)))
        if metrics.get("factor_r2") is not None:
            metrics["independence"] = 100 - metrics["factor_r2"]
        shifted.append({**candidate, "metrics": metrics})
    return shifted


def _seed_members(
    snapshot: dict[str, Any], previous: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """Resolve an existing universe's members against the new snapshot.

    Changing tier is a move along a nesting, not a rebuild: rebuilding from scratch would churn
    every slot of a pool whose whole point is low turnover. Any incumbent the new snapshot no
    longer carries as an eligible candidate stops the build and is named, because dropping it is
    a decision the operator has to make, not one this function can make quietly.
    """
    if previous is None:
        return []
    if previous.get("market") != snapshot["market"]:
        raise UniverseError("seed universe and snapshot markets differ")
    by_ticker = {item["ticker"]: item for item in snapshot["candidates"] if item["eligible"]}
    missing = sorted(
        item["ticker"] for item in previous.get("members") or [] if item["ticker"] not in by_ticker
    )
    if missing:
        raise UniverseError(
            "seed members absent or ineligible in the new snapshot: " + ", ".join(missing)
        )
    return [deepcopy(by_ticker[item["ticker"]]) for item in previous.get("members") or []]


def build_universe(
    spec: dict[str, Any],
    snapshot_raw: dict[str, Any],
    policy: dict[str, Any],
    previous: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if policy.get("selection_model") == "coverage_first" or "coverage_plan" in snapshot_raw:
        from coverage_core import build
        return build(spec, snapshot_raw, policy, previous)
    if spec.get("schema_version") != 1:
        raise UniverseError("build spec schema_version must be 1")
    market = str(spec.get("market", "")).lower()
    profile = str(spec.get("profile", "")).lower()
    if profile not in PROFILES:
        raise UniverseError(f"build spec profile must be one of {', '.join(PROFILES)}")
    snapshot = normalize_snapshot(snapshot_raw)
    if snapshot["market"] != market:
        raise UniverseError("build spec and snapshot markets differ")
    if spec.get("as_of") and spec["as_of"] != snapshot["as_of"]:
        raise UniverseError("build spec as_of must match the researched snapshot")
    declaration = snapshot["market_spec"]

    market_policy = market_guidance(market, policy, declaration)
    final_guide = market_policy[profile]
    target = int(spec.get("target_count") or final_guide["target"])
    hard_cap = min(int(spec.get("hard_ticker_cap", 1000)), 1000)
    token_cap = min(int(spec.get("tradingview_token_cap", 1000)), 1000)
    if target > hard_cap:
        raise UniverseError(f"target_count {target} exceeds hard_ticker_cap {hard_cap}")
    if not spec.get("allow_outside_guidance", False):
        if not int(final_guide["min"]) <= target <= int(final_guide["max"]):
            raise UniverseError(
                f"{market}/{profile} target {target} is outside guidance "
                f"{final_guide['min']}..{final_guide['max']}"
            )

    warnings: list[str] = (
        declared_market_warnings(declaration)
        + measurement_warnings(snapshot["measurement"])
        + staleness_warnings(
            snapshot["as_of"],
            [("snapshot", snapshot["sources"])]
            + [(item["ticker"], item["evidence"]) for item in snapshot["candidates"]],
            policy,
        )
    )
    incumbents = _seed_members(snapshot, previous)
    seed_profile = str(previous.get("profile", "")).lower() if previous else ""
    # Widening extends the seed; narrowing reselects inside it. Both beat a rebuild, which would
    # churn a pool whose whole point is low turnover — and narrowing by rebuilding would drop
    # incumbents for reasons that have nothing to do with the smaller target.
    narrowing = bool(incumbents) and PROFILE_INDEX.get(seed_profile, -1) > PROFILE_INDEX[profile]
    pool = snapshot["candidates"]
    selected: list[dict[str, Any]] = []
    if narrowing:
        pool = incumbents
        warnings.append(
            f"narrowed universe {previous.get('version_hash')} from {seed_profile} to {profile}; "
            f"its {len(incumbents)} members were the only candidates"
        )
    elif incumbents:
        selected = incumbents
        warnings.append(
            f"seeded {len(selected)} members from universe "
            f"{previous.get('version_hash')} ({seed_profile})"
        )
    # Walk every intermediate tier when widening, including a Medium -> Max jump. Otherwise
    # the beta preference would spend the Heavy budget too and nesting would depend on the route.
    if (incumbents and seed_profile in PROFILE_INDEX
            and PROFILE_INDEX[seed_profile] < PROFILE_INDEX[profile]):
        stages = PROFILES[PROFILE_INDEX[seed_profile] + 1: PROFILE_INDEX[profile] + 1]
    else:
        stages = (profile,) if incumbents else PROFILES[: PROFILE_INDEX[profile] + 1]

    def run_stages(
        stage_pool: list[dict[str, Any]], record: list[str] | None
    ) -> list[dict[str, Any]]:
        """One full pass of the tier ladder. Run again on a nudged bench to measure stability.

        `record` collects the warnings on the real pass and is None on a rehearsal, because a
        perturbed run's warnings are about a universe nobody is being shipped.
        """
        held = list(seed_members)
        for stage in stages:
            guide = market_policy[stage]
            stage_target = target if stage == profile else int(guide["target"])
            stage_theme_count = sum(
                1 for item in snapshot["taxonomy"]
                if item["coverage_level"] <= policy["profiles"][stage]["coverage_level"]
            )
            stage_effective = min(stage_target, token_cap - stage_theme_count, hard_cap)
            if stage_effective <= 0:
                raise UniverseError(f"{stage}: TradingView token cap leaves no ticker slots")
            if record is not None and stage_effective < stage_target:
                record.append(
                    f"{stage}: target reduced from {stage_target} to {stage_effective} "
                    "by token cap"
                )
            held, stage_warnings = _select_stage(
                candidates=stage_pool,
                taxonomy=snapshot["taxonomy"],
                profile=stage,
                target=stage_effective,
                profile_policy=policy["profiles"][stage],
                seed=held,
            )
            if record is not None:
                record.extend(stage_warnings)
        return held

    seed_members = selected
    selected = run_stages(pool, warnings)
    survivors = set(item["asset_id"] for item in selected)
    for draw in range(STABILITY_DRAWS):
        try:
            shaken = run_stages(_jitter(pool, draw), None)
        except UniverseError:
            # A perturbed bench that cannot fill the universe says nothing about the one that
            # can, and it is not a reason to fail a build that already passed.
            survivors = set()
            break
        survivors &= {item["asset_id"] for item in shaken}
    stability = {
        "shift": STABILITY_SHIFT,
        "draws": STABILITY_DRAWS,
        "survived": len(survivors),
        "of": len(selected),
        "share": round(len(survivors) / len(selected), 4) if selected else None,
    }

    selected.sort(key=lambda item: (item["theme_code"], rank_key(item)))
    selected_assets = {item["asset_id"] for item in selected}
    final_level = int(policy["profiles"][profile]["coverage_level"])
    selection_audit = []
    taxonomy_by_code = {item["theme_code"]: item for item in snapshot["taxonomy"]}
    incumbent_tickers = {item["ticker"] for item in incumbents}
    for candidate in snapshot["candidates"]:
        if candidate["asset_id"] in selected_assets:
            continue
        if not candidate["eligible"]:
            reasons = candidate["exclusion_reasons"]
        elif taxonomy_by_code[candidate["theme_code"]]["coverage_level"] > final_level:
            reasons = ["outside_profile_coverage"]
        elif narrowing:
            # A narrowing run never considered the rest of the snapshot, and saying they lost on
            # budget would be a different claim from the true one.
            reasons = [
                "removed_by_downgrade"
                if candidate["ticker"] in incumbent_tickers
                else "not_in_seed_universe"
            ]
        else:
            reasons = ["not_selected_under_budget"]
        selection_audit.append({
            "ticker": candidate["ticker"],
            "asset_id": candidate["asset_id"],
            "theme_code": candidate["theme_code"],
            "reasons": reasons,
        })
    universe_base = {
        "schema_version": 1,
        "market": market,
        "market_spec": declaration,
        "profile": profile,
        "as_of": str(spec.get("as_of") or snapshot["as_of"]),
        "source_as_of": snapshot["as_of"],
        "policy_version": canonical_hash(policy),
        "limits": {
            "hard_ticker_cap": hard_cap,
            "tradingview_token_cap": token_cap,
            "target_count": target,
        },
        "taxonomy": snapshot["taxonomy"],
        "sources": snapshot["sources"],
        "measurement": snapshot["measurement"],
        "measurement_audit": snapshot["measurement_audit"],
        "notes": snapshot["notes"],
        "coverage": snapshot["coverage"],
        **({"report_translations": snapshot["report_translations"]}
           if "report_translations" in snapshot else {}),
        "members": selected,
        "selection_audit": selection_audit,
        "history": [],
    }
    universe = {**universe_base}
    universe["version_hash"] = universe_hash(universe)
    universe["content_hash"] = content_hash(universe)
    report = validate_universe(universe, policy)
    # Build-time only, and deliberately not part of the universe. Answering it needs the whole
    # bench — the candidates that lost, with their metrics — and a stored universe keeps only
    # the members and the reasons the rest were turned down. `validate` on a file therefore
    # cannot recompute it, and every reader of the report has to treat it as absent.
    report["stats"]["stability"] = stability
    report["warnings"] = sorted(set(report["warnings"] + warnings))
    if not report["passed"]:
        raise UniverseError("built universe failed validation: " + "; ".join(report["errors"]))
    return universe, report


def validate_universe(
    universe: dict[str, Any], policy: dict[str, Any] | None = None
) -> dict[str, Any]:
    policy = policy or load_policy()
    errors: list[str] = []
    warnings: list[str] = []
    if "report_translations" in universe:
        try:
            normalize_report_translations(universe["report_translations"])
        except UniverseError as exc:
            errors.append(str(exc))
    market = str(universe.get("market", "")).lower()
    profile = str(universe.get("profile", "")).lower()
    declaration = universe.get("market_spec")
    rules: MarketSpec | None = None
    try:
        # Re-resolved from the record rather than from the registry, so a stored universe of an
        # unregistered market still validates — and so an edited declaration is caught here as
        # well as by the hash.
        rules, declaration = resolve_market(market, declaration)
    except UniverseError as exc:
        errors.append(str(exc))
    if profile not in PROFILES:
        errors.append("invalid profile")
    warnings.extend(declared_market_warnings(declaration))
    try:
        taxonomy = normalize_taxonomy(universe.get("taxonomy") or [])
    except UniverseError as exc:
        errors.append(str(exc))
        taxonomy = []
    taxonomy_by_code = {item["theme_code"]: item for item in taxonomy}
    members = universe.get("members") or []
    seen_tickers: set[str] = set()
    seen_assets: set[str] = set()
    normalized: list[dict[str, Any]] = []
    try:
        require_strong_evidence(
            validate_evidence(universe.get("sources"), "universe"), "universe"
        )
    except UniverseError as exc:
        errors.append(str(exc))
    for index, raw in enumerate(members):
        try:
            item = normalize_candidate(
                rules or market,
                raw,
                taxonomy_by_code,
                coverage_first=universe.get("selection_model") == "coverage_first",
            )
        except UniverseError as exc:
            errors.append(f"member #{index}: {exc}")
            continue
        if not item["eligible"]:
            errors.append(f"{item['ticker']}: selected member is not eligible")
        if item["ticker"] in seen_tickers:
            errors.append(f"duplicate ticker: {item['ticker']}")
        if item["asset_id"] in seen_assets:
            errors.append(f"duplicate economic asset: {item['asset_id']}")
        seen_tickers.add(item["ticker"])
        seen_assets.add(item["asset_id"])
        normalized.append(item)
    errors.extend(candidate_date_errors(normalized, str(universe.get("source_as_of", ""))))
    concentration: dict[str, Any] | None = None
    duties = {"declared": 0, "represented": 0, "missing": [], "undeclared": []}
    coverage_model = universe.get("selection_model") == "coverage_first"
    if rules is not None and profile in PROFILES and not coverage_model:
        level = policy["profiles"][profile]["coverage_level"]
        required_themes = {
            item["theme_code"] for item in taxonomy if item["coverage_level"] <= level
        }
        held_themes = {item["theme_code"] for item in normalized}
        missing = sorted(required_themes - held_themes)
        if missing:
            errors.append("uncovered required themes: " + ", ".join(missing))
        undeclared = [t["theme_code"] for t in taxonomy if t["theme_code"] in required_themes
                      and not (t.get("purpose") and t.get("representative_roles"))]
        declared = [t for t in taxonomy if t["theme_code"] in required_themes
                    and t.get("representative_roles")]
        missing_duties = [t["theme_code"] for t in declared if not any(
            c["theme_code"] == t["theme_code"] and c["role"] in t["representative_roles"]
            for c in normalized)]
        errors.extend(f"unrepresented observation duty: {code}" for code in missing_duties)
        duties = {"declared": len(declared), "represented": len(declared) - len(missing_duties),
                  "missing": missing_duties, "undeclared": sorted(undeclared)}
        if undeclared:
            warnings.append(f"{len(undeclared)} themes have no declared observation duty; "
                            "legacy presence-only coverage applies")
        disallowed = sorted({
            item["theme_code"] for item in normalized
            if taxonomy_by_code[item["theme_code"]]["coverage_level"] > level
        })
        if disallowed:
            errors.append("themes exceed profile coverage level: " + ", ".join(disallowed))
        # No cap to check. What is worth saying is where the universe actually concentrated,
        # measured against what the taxonomy's own weights asked for — a build apportions to
        # weight, but maintenance adds and removes one name at a time and nothing re-checks the
        # shape, so a pool can walk a long way from its table without anyone being told.
        counts = Counter(item["theme_code"] for item in normalized)
        in_level = [item for item in taxonomy if int(item["coverage_level"]) <= level]
        # Required seats never went through apportionment. A benchmark is in the universe
        # because the market spec names it, not because its theme won a slot, so counting it
        # against the theme's weighted share compares a seat that was assigned to a seat that
        # was earned. Every market carries two or three of them and they all sit in benchmark
        # themes, so left in they skew the same theme in the same direction everywhere — Korea's
        # 00_A holds three against an expectation of one, and two of the three are required.
        # Out of both sides, and the remaining comparison is apportioned against apportioned.
        required_counts = Counter(
            item["theme_code"] for item in normalized if item.get("required")
        )
        apportioned = len(normalized) - sum(required_counts.values())
        expected = expected_members(in_level, apportioned)
        top = counts.most_common(1)
        if top:
            code, held = top[0]
            concentration = {
                "theme_code": code,
                "members": held,
                "share": round(held / len(normalized), 4) if normalized else 0.0,
                # Stated on the same basis as `members`, so the two are readable side by side:
                # what the weights asked for, plus the seats the spec spent before weighing.
                "expected": round(expected.get(code, 0.0) + required_counts[code], 1),
            }
        for code, held in sorted(counts.items()):
            want = expected.get(code)
            earned = held - required_counts[code]
            # Generous on purpose. A build already apportions to weight, and a theme whose
            # neighbours ran out of eligible candidates legitimately absorbs their slots — that
            # is the behaviour a cap could not produce. What this catches is the other thing:
            # a pool that maintenance walked into one theme, one evidence-backed op at a time.
            if want and earned >= THEME_DRIFT_FLOOR and earned > THEME_DRIFT_RATIO * want:
                held_note = (
                    f"{earned} apportioned members (of {held})"
                    if required_counts[code] else f"{earned} members"
                )
                warnings.append(
                    f"{code} holds {held_note} against a weighted share of {want:.0f}; "
                    "either the weight in the taxonomy is stale or maintenance drifted"
                )
    try:
        normalize_measurement(
            universe.get("measurement") or {},
            metrics_in_use(normalized),
            blended_metrics(normalized),
        )
    except UniverseError as exc:
        errors.append(str(exc))
    if normalized and any(item["metrics"]["quality"] is not None for item in normalized):
        with_facts = sum(1 for item in normalized if item.get("quality_facts"))
        if not with_facts:
            warnings.append(
                f"quality rests on judgement alone for all {len(normalized)} members; "
                "no candidate carries quality_facts"
            )
    if rules is not None and profile in PROFILES and normalized and not coverage_model:
        # Quotas steer the build; nothing re-checked them afterwards, so a maintenance round could
        # walk a pool from 5% tactical to 30% one evidence-backed op at a time and never be told.
        targets = policy["profiles"][profile]["bucket_targets"]
        counts = Counter(candidate_bucket(item) for item in normalized)
        for bucket, share in sorted(targets.items()):
            actual = counts[bucket] / len(normalized)
            if actual - float(share) > BUCKET_DRIFT_TOLERANCE:
                warnings.append(
                    f"{bucket} bucket holds {actual:.0%} of the pool against a "
                    f"{float(share):.0%} target"
                )
    quality = None
    references = []
    if coverage_model:
        try:
            from coverage_core import quality_check
            quality = quality_check(universe, policy)
            references = universe["coverage_plan"].get("references", [])
            if quality["status"] == "partial":
                warnings.append(
                    "PARTIAL Max: qualified members, but required expansion is not met; "
                    f"shortfall={universe['delivery']['shortfall']}"
                )
        except (UniverseError, KeyError, TypeError, ValueError) as exc:
            errors.append(str(exc))
    else:
        warnings.append(
            "Legacy artifact: structural validation is not coverage-first certification")
    exported = normalized + references
    from display_core import theme_groups
    display = theme_groups(universe["coverage_plan"], profile) if quality else {}
    token_count = len(exported) + len({display.get(item["theme_code"], item["theme_code"])
                                      for item in exported})
    limits = universe.get("limits") or {}
    hard_ticker_cap = min(int(limits.get("hard_ticker_cap", 1000)), 1000)
    tradingview_token_cap = min(int(limits.get("tradingview_token_cap", 1000)), 1000)
    if len(exported) > hard_ticker_cap:
        errors.append(f"ticker count exceeds {hard_ticker_cap}")
    if token_count > tradingview_token_cap:
        errors.append(f"TradingView token count exceeds {tradingview_token_cap}")
    if rules is not None and profile in PROFILES and not coverage_model:
        guide = market_guidance(market, policy, declaration)[profile]
        if len(normalized) < int(guide["min"]):
            warnings.append(
                f"member count {len(normalized)} is below "
                f"{market}/{profile} guidance {guide['min']}"
            )
        if len(normalized) > int(guide["max"]):
            warnings.append(
                f"member count {len(normalized)} is above "
                f"{market}/{profile} guidance {guide['max']}"
            )
    expected = universe.get("version_hash")
    if not expected or not universe.get("content_hash"):
        errors.append("universe requires both version_hash and content_hash")
    if expected and universe_hash(universe) != expected:
        errors.append("version_hash does not match universe content")
    if universe.get("content_hash") and content_hash(universe) != universe["content_hash"]:
        errors.append("content_hash does not match facts or provenance")
    return {
        "passed": not errors,
        **({"qualified": not errors and quality is not None and quality["status"] == "qualified"}
           if coverage_model else {}),
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "tickers": len(normalized),
            "exported_tickers": len(exported),
            "quality": quality,
            "themes": len({display.get(item["theme_code"], item["theme_code"])
                           for item in normalized}),
            **({"research_themes": len({item["theme_code"] for item in normalized})}
               if coverage_model else {}),
            **({"partially_scored": sum(_is_partially_scored(item) for item in normalized)}
               if not coverage_model else {}),
            "concentration": concentration,
            "duties": duties,
            "tradingview_tokens": token_count,
            "roles": dict(sorted(Counter(item["role"] for item in normalized).items())),
            "buckets": dict(sorted(Counter(candidate_bucket(item) for item in normalized).items())),
            "rejections": dict(audit_summary(universe.get("selection_audit") or [])),
        },
    }


def audit_summary(selection_audit: list[dict[str, Any]]) -> list[tuple[str, int]]:
    """Count rejections by code, largest first.

    This is the payoff of the closed vocabulary: free text cannot be counted, and a count is what
    turns "some candidates were dropped" into a statement about where the universe is constrained.
    """
    counts: Counter[str] = Counter()
    for item in selection_audit:
        for reason in item.get("reasons") or []:
            counts[str(reason).split(":", 1)[0].strip()] += 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def adverse_flag_summary(members: list[dict[str, Any]]) -> list[tuple[str, int]]:
    """Count adverse flags across the members, largest first.

    The flags are the most consequential checkable fact in the file — each one costs a quarter of
    the rule half of `quality` — and until now they were only visible by reading the JSON. A
    count is also the only way a reader sees that a market-specific vocabulary was used at all.
    """
    counts: Counter[str] = Counter()
    for item in members:
        for flag in (item.get("quality_facts") or {}).get("adverse_flags") or []:
            counts[str(flag)] += 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))


def render_txt(universe: dict[str, Any]) -> str:
    from display_core import display_view
    labels, grouped = display_view(universe)
    tokens: list[str] = []
    for code in sorted(grouped):
        tokens.append(f"###{code}_{labels[code]}")
        tokens.extend(item["ticker"] for item in sorted(grouped[code], key=(lambda c: c["ticker"])
                              if universe.get("selection_model") == "coverage_first" else rank_key))
    return ",".join(tokens) + "\n"


_SECTION_RE = re.compile(r"^(\d{2})_([A-Z])_(.+)$")
_NAME_SAFE_RE = re.compile(r"[^A-Z0-9]+")
IMPORT_NOT_RESEARCHED = "unverifiable_fact: imported from a watchlist, not yet researched"


def parse_watchlist(text: str) -> list[tuple[str, list[str]]]:
    """Read a TradingView watchlist back into (section, tickers) pairs.

    Comma separated on one line is what TradingView exports; one per line is what people keep by
    hand. Both are the same file as far as this is concerned.
    """
    sections: list[tuple[str, list[str]]] = []
    current = ""
    for token in (part.strip() for line in text.splitlines() for part in line.split(",")):
        if not token:
            continue
        if token.startswith("###"):
            current = token[3:].strip()
            if not any(name == current for name, _ in sections):
                sections.append((current, []))
            continue
        if not sections:
            sections.append((current, []))
        for name, tickers in sections:
            if name == current:
                tickers.append(token.upper())
                break
    return [(name, tickers) for name, tickers in sections if tickers]


def watchlist_to_snapshot(text: str, market: str, as_of: str) -> dict[str, Any]:
    """Turn a watchlist into a snapshot skeleton that is honest about what it does not know.

    A txt file carries tickers and section names. It does not carry roles, liquidity, evidence or
    whether anything is still listed, so this writes none of those: every candidate arrives
    ineligible, `complete` is false, and the build refuses it until someone does the research.
    What it saves is the transcription — which is the part that is tedious rather than the part
    that is hard.
    """
    spec = market_spec(market)
    taxonomy: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    notes: list[str] = []
    seen: set[str] = set()
    for index, (section, tickers) in enumerate(parse_watchlist(text)):
        match = _SECTION_RE.fullmatch(section)
        if match:
            # Our own output round-trips: the codes it already carries are kept.
            l1_code, letter, theme_name = match.groups()
            theme_code = f"{l1_code}_{letter}"
        else:
            if index >= 100:
                raise UniverseError("a watchlist with more than 100 sections needs manual sorting")
            l1_code = f"{index:02d}"
            theme_code = f"{l1_code}_A"
            theme_name = _NAME_SAFE_RE.sub("_", (section or "UNSORTED").upper()).strip("_")
        taxonomy.append({
            "l1_code": l1_code,
            "l1_name": theme_name.replace("_", " ").title(),
            "theme_code": theme_code,
            "theme_name": theme_name or "UNSORTED",
            "coverage_level": 1,
        })
        for ticker in tickers:
            problems = validate_ticker(spec.code, ticker)
            if problems:
                notes.append(f"{ticker}: not imported; {problems[0]}")
                continue
            if ticker in seen:
                notes.append(f"{ticker}: listed more than once, kept the first section")
                continue
            seen.add(ticker)
            candidates.append({
                "ticker": ticker,
                "name": "",
                "theme_code": theme_code,
                "role": "",
                "eligible": False,
                "exclusion_reasons": [IMPORT_NOT_RESEARCHED],
                "metrics": {},
                "evidence": [],
            })
    if not candidates:
        raise UniverseError(f"no {spec.code} tickers found in the watchlist")
    return {
        "schema_version": 1,
        "market": spec.code,
        "as_of": as_of,
        "complete": False,
        "sources": [],
        "measurement": {},
        "taxonomy": normalize_taxonomy(taxonomy),
        "candidates": candidates,
        "notes": sorted(set(notes)),
    }


def report_language(universe: dict[str, Any] | str) -> str:
    """The report language a universe defaults to: its declared one, or its registry row's."""
    if isinstance(universe, dict):
        declared = (universe.get("market_spec") or {}).get("language")
        if declared:
            return str(declared)
        market = str(universe.get("market", ""))
    else:
        market = universe
    spec = MARKET_SPECS.get(market.strip().lower())
    return spec.language if spec else "en"


def report_languages(
    universe: dict[str, Any] | str, language: str | None = None
) -> tuple[str, ...]:
    """Every language this universe's report is written in: its own, and English beside it.

    English is not a fallback here, it is a second reader. A jp universe is read by the people
    who trade Tokyo, and also by someone allocating across six markets who reads none of their
    six languages — and a ticker universe is exactly the artifact that reader needs, because the
    reasons and the evidence are the whole point of it. Writing only the market's language served
    the first reader and handed the second a table of headings they cannot parse.

    So both, always, and the language goes in the filename rather than only one of them getting
    a suffix. Asymmetric naming would mean "where is the English report" has two answers — the
    plain `.md` in five markets and the suffixed one in nine — which is the question this is
    supposed to stop anyone asking.
    """
    primary = language or report_language(universe)
    return (primary,) if primary == "en" else (primary, "en")


def _glossed(lexicon: dict[str, str], domain: str, code: str) -> str:
    """`BENCHMARK` in English, `基准 (BENCHMARK)` in Chinese.

    The code is the vocabulary this skill documents and the string a reader greps for, so the
    translation is added beside it rather than in place of it.
    """
    label = lexicon.get(f"{domain}.{code}", code)
    return label if label == code else f"{label} ({code})"


def _brief_reason(member: dict[str, Any]) -> str:
    """A presentation excerpt; never replace the admission reasoning in the record."""
    text = " ".join(str(member.get("reason_summary") or member.get("reason") or "").split())
    if not member.get("reason_summary"):
        first = re.split(r"(?<=[。！？])|(?<=[.!?])\s+(?=[A-Z])", text, maxsplit=1)[0]
        if len(first) >= 12 or re.search(r"[\u3400-\u9fff]", first):
            # Short Chinese sentences are useful; an initialism such as U.S. alone is not.
            text = first
    if len(text) > 160:
        cut = text[:159]
        if " " in cut and not re.search(r"[\u3400-\u9fff]", cut):
            cut = cut.rsplit(" ", 1)[0]
        text = cut.rstrip(" ,;，；") + "…"
    return text.replace("|", "\\|")


def _measurement_diagnostic(note: str) -> bool:
    return bool(re.fullmatch(
        r"\S+: (?:no factor statistics, \d+ sessions overlap a usable gauge"
        r"|not covered by the price table)", str(note),
    ))


def render_markdown(
    universe: dict[str, Any], report: dict[str, Any], language: str | None = None
) -> str:
    language = language or report_language(universe)
    lex = load_lexicon(language)
    translations = universe.get("report_translations", {}).get(language, {})

    def text(value: str) -> str:
        return translations.get(value, value).replace("|", "\\|").replace("\n", " ")

    def reason(member: dict[str, Any]) -> str:
        brief = _brief_reason(member)
        original = member.get("reason_summary") or brief
        # Reapply the normal brief limit to authored translations; never change the member.
        return (_brief_reason({"reason_summary": translations[original]})
                if original in translations else brief)

    taxonomy = {item["theme_code"]: item for item in universe["taxonomy"]}
    per_theme = Counter(member["theme_code"] for member in universe["members"])
    from display_core import display_view, theme_groups
    labels, groups = display_view(universe)
    mapping = theme_groups(universe.get("coverage_plan", {}), universe["profile"])
    limits = universe.get("limits", {})
    profile = universe["profile"]
    colon = lex["punct.colon"]
    declaration = universe.get("market_spec")
    # Only ever shown when the rules were declared rather than reviewed. The presence of the line
    # is the signal; printing "registered" on every other report would bury it.
    declared_line = [
        f"- {lex['label.market_rules']}{colon}{_glossed(lex, 'origin', 'declared')} · "
        f"{text(declaration['label'])} · {', '.join(declaration['venues'])}"
    ] if declaration else []
    partial_notice = []
    if universe.get("delivery", {}).get("status") == "partial":
        delivery = universe["delivery"]
        filled = len(universe["members"])
        if (language or report_language(universe)) == "zh-Hans":
            held = len(universe["heavy_base"]["members"])
            partial_notice = [
                f"- 交付状态：部分完成（PARTIAL），{filled} / "
                f"{delivery['required_entities']} 个实体，缺 {delivery['shortfall']} 个；"
                f"实际扩增 {(filled - held) / held:.2%}。标的与覆盖检查通过，扩增目标未达标；"
                "可使用当前版或继续补充。"
            ]
        else:
            partial_notice = [
                f"- PARTIAL: {filled} / {delivery['required_entities']} "
                f"entities; missing {delivery['shortfall']}. Max growth target is not met; "
                "member/coverage checks passed. Deliver with disclosure or resume research."
            ]
    lines = [
        "# " + lex["title"].format(market=universe["market"].upper()),
        "",
        *declared_line,
        f"- {lex['label.profile']}{colon}{lex.get('profile.' + profile, profile)}",
        f"- {lex['label.facts_as_of']}{colon}{universe['source_as_of']}",
        f"- {lex['label.version']}{colon}`{universe['version_hash']}`",
        f"- {lex['label.tickers']}{colon}{report['stats']['tickers']}",
        *partial_notice,
        *([f"- PARTIAL: {len(universe['members'])} / {limits['target_count']} "
           "— requested size is not filled; continue research before calling this complete."]
          if len(universe['members']) < limits.get('target_count', 0)
          and universe.get('selection_model') != 'coverage_first' else []),
        f"- {lex['label.themes']}{colon}{report['stats']['themes']}",
        # Absent when a stored universe is re-validated rather than built — the bench it needs
        # is not in the file — so the line goes where it can simply not appear.
        *([
            f"- {lex['label.stability']}{colon}"
            f"{report['stats']['stability']['share']:.2f} · "
            f"{report['stats']['stability']['survived']} / {report['stats']['stability']['of']} · "
            f"±{report['stats']['stability']['shift']:.0%}"
        ] if (report["stats"].get("stability") or {}).get("share") is not None else []),
        # Only when it happened. A line reading "0" on every clean build teaches a reader to
        # stop reading the lines.
        *([
            f"- {lex['label.partially_scored']}{colon}"
            f"{report['stats']['partially_scored']} / {report['stats']['tickers']}"
        ] if report["stats"].get("partially_scored")
          and universe.get("selection_model") != "coverage_first" else []),
        # Where the universe concentrated, beside what its own table asked for. Nothing caps a
        # theme any more, so this line is how a reader tells a market that really is one theme
        # deep from a taxonomy whose weights were never revisited.
        *([
            f"- {lex['label.largest_theme']}{colon}"
            f"{report['stats']['concentration']['theme_code']} · "
            f"{report['stats']['concentration']['members']} · "
            f"{report['stats']['concentration']['share']:.0%} · "
            f"{lex['label.weighted_share']} "
            f"{report['stats']['concentration']['expected']:.0f}"
        ] if report["stats"].get("concentration") else []),
        f"- {lex['label.tv_tokens']}{colon}{report['stats']['tradingview_tokens']} / "
        f"{limits.get('tradingview_token_cap', 1000)}",
        f"- {lex['label.rejected']}{colon}{len(universe.get('selection_audit', []))}",
        f"- {lex['label.validation']}{colon}"
        f"{lex['value.pass'] if report['passed'] else lex['value.fail']}",
        "",
        lex["note.audit_record"].format(
            universe=f"{artifact_stem(universe)}.json",
            validation=f"{artifact_stem(universe)}.validation.json",
        ),
        "",
        *[f"- {text(note)}" for note in universe.get("notes", [])
          if not _measurement_diagnostic(note)],
        "",
        f"## {lex['section.roles']}",
        "",
        f"| {lex['column.role']} | {lex['column.count']} |",
        "|---|---:|",
    ]
    for role, count in report["stats"]["roles"].items():
        lines.append(f"| {_glossed(lex, 'role', role)} | {count} |")
    # The theme table is where a reader sees the shape of the instrument: which parts of the
    # market are covered, at what depth, and which theme is carrying more weight than it should.
    # Human labels may have authored translations; economic codes and duties stay unchanged.
    lines.extend([
        "",
        f"## {lex['section.themes']}",
        "",
        f"| {lex['column.code']} | {lex['column.group']} | {lex['column.theme']} "
        f"| {lex['column.level']} | {lex['column.weight']} | {lex['column.count']} |",
        "|---|---|---|---:|---:|---:|",
    ])
    for code in sorted(taxonomy):
        if mapping.get(code, code) != code:
            continue
        theme = taxonomy[code]
        merged = [k for k in taxonomy if mapping.get(k, k) == code]
        count = sum(per_theme[k] for k in merged)
        lines.append(
            f"| {code} | {text(theme['l1_name'])} | {text(labels[code])} | "
            f"{theme['coverage_level']} | {theme_weight(theme):g} | {count} |"
        )
    duties = [t for t in taxonomy.values() if t.get("purpose")]
    if duties:
        lines.extend(["", f"| {lex['column.theme']} | {lex['column.purpose']} | "
                      f"{lex['column.representatives']} |", "|---|---|---|"])
        for theme in sorted(duties, key=lambda t: t["theme_code"]):
            purpose = text(theme["purpose"])
            lines.append(f"| {theme['theme_code']} | {purpose} | "
                         f"{', '.join(theme.get('representative_roles', []))} |")
    measurement = universe.get("measurement") or {}
    if measurement:
        lines.extend([
            "",
            f"## {lex['section.measurement']}",
            "",
            f"| {lex['column.metric']} | {lex['column.basis']} | {lex['column.method']} "
            f"| {lex['column.window']} |",
            "|---|---|---|---|",
        ])
        for field, entry in measurement.items():
            window = entry.get("window") or lex["value.na"]
            basis = _glossed(lex, "basis", entry["basis"])
            lines.append(f"| {field} | {basis} | {text(entry['method'])} | {text(window)} |")
        with_facts = sum(1 for item in universe["members"] if item.get("quality_facts"))
        if with_facts:
            lines.extend([
                "",
                lex["note.quality_blend"].format(
                    rule=f"{QUALITY_RULE_WEIGHT:.0%}",
                    judged=f"{1 - QUALITY_RULE_WEIGHT:.0%}",
                    with_facts=with_facts,
                    total=len(universe["members"]),
                ),
            ])
        flags = adverse_flag_summary(universe["members"])
        if flags:
            lines.extend([
                "",
                f"| {lex['column.flag']} | {lex['column.count']} |",
                "|---|---:|",
            ])
            lines.extend(
                f"| {_glossed(lex, 'flag', code)} | {count} |" for code, count in flags
            )
    rejections = audit_summary(universe.get("selection_audit") or [])
    if rejections:
        # The detail stays in universe.json. What belongs in a document a person reads is the
        # shape of the rejections: a universe losing most of its candidates to unverifiable facts
        # has a research problem, and one losing them to theme caps has a budget problem.
        lines.extend([
            "",
            f"## {lex['section.rejections']}",
            "",
            f"| {lex['column.reason']} | {lex['column.count']} |",
            "|---|---:|",
        ])
        lines.extend(
            f"| {_glossed(lex, 'reason', code)} | {count} |" for code, count in rejections
        )
    if report["warnings"]:
        lines.extend(["", f"## {lex['section.warnings']}", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
        # Diagnostics name policy fields and code paths and are worth grepping for verbatim, so
        # they stay in one language and the report says so rather than half-translating them.
        if lex.get("note.diagnostics_language"):
            lines.extend(["", lex["note.diagnostics_language"]])
    if report.get("maintenance"):
        maintenance = report["maintenance"]
        depth = maintenance["review_depth"]
        lines.extend([
            "",
            f"## {lex['section.review']}",
            "",
            f"- {lex['review.depth']}{colon}{lex.get('depth.' + depth, depth)}",
            f"- {lex['review.turnover']}{colon}{maintenance['turnover']:.1%}",
            f"- {lex['review.added']}{colon}"
            f"{', '.join(maintenance['added']) or lex['value.none']}",
            f"- {lex['review.removed']}{colon}"
            f"{', '.join(maintenance['removed']) or lex['value.none']}",
            f"- {lex['review.deferred']}{colon}{len(maintenance['deferred'])}",
        ])
    lines.extend([
        "",
        f"## {lex['section.members']}",
        "",
        f"| {lex['column.ticker']} | {lex['column.name']} "
        f"| {lex['column.role']} | {lex['column.reason']} |",
        "|---|---|---|---|",
    ])
    if universe.get("selection_model") == "coverage_first":
        # Group headings carry the theme; full economic duties and evidence stay in JSON.
        lines = lines[:-2]
        for code in sorted(groups):
            members = [c for c in groups[code] if "asset_id" in c]
            if not members:
                continue
            lines.extend(
                [
                    f"### {code} · {text(labels[code])} ({len(members)})",
                    "",
                    f"| {lex['column.ticker']} | {lex['column.name']} | "
                    f"{lex['column.role']} | {lex['column.reason']} |",
                    "|---|---|---|---|",
                ]
            )
            for member in sorted(members, key=lambda c: c["ticker"]):
                lines.append(f"| {member['ticker']} | {text(member['name'])} | "
                             f"{_glossed(lex, 'role', member['role'])} | "
                             f"{reason(member)} |")
            lines.append("")
    else:
        for member in universe["members"]:
            lines.append(
                f"| {member['ticker']} | {text(member['name'])} | "
                f"{_glossed(lex, 'role', member['role'])} | {reason(member)} |"
            )
    if universe.get("selection_model") == "coverage_first":
        quality = report["stats"].get("quality") or {}
        lines.extend(["", "## Coverage-first audit", "",
                      f"- Quality: {quality.get('status', 'unverified')}",
                      f"- Reviewed leader coverage: {quality.get('leader_coverage')}",
                      f"- Entity ceiling (not a fill target): {limits['target_count']}",
                      f"- Unused capacity: {quality.get('unused_capacity')}",
                      f"- Admission roles: {quality.get('roles')}",
                      f"- Economic sector counts: {quality.get('sectors')}",
                      "- Evidence boundary: validates declared research, not leadership truth."])
        if expansion := quality.get("expansion"):
            lines.extend([
                f"- Heavy entities: {expansion['heavy_entities']}; "
                f"added Beta: {expansion['added_beta']} ({expansion['growth']:.1%})",
                f"- Required Max entities: at least {expansion['min_entities']}; "
                f"entity ceiling {expansion['max_entities']} (references excluded)",
            ])
            if expansion.get("shortfall"):
                lines.append("- Partial group ceilings retain the planned growth allocation; "
                             "unfilled places are not transferred to other groups.")
            lines.extend(["", "### Heavy → Max distribution", "",
                          "| Group | Heavy | Added Beta | Rounding ceiling |",
                          "|---|---:|---:|---:|"])
            for code, row in expansion["distribution"].items():
                lines.append(f"| {code} {text(labels[code])} | {row['heavy']} | "
                             f"{row['added']} | {row['added_cap']} |")
        lines.extend(["", "### Reference instruments", ""])
        for ref in universe["coverage_plan"].get("references", []):
            lines.append(f"- {ref['ticker']} ({ref['kind']}): {text(ref['observes'])}"
                         + (f"; proxy for {text(ref['proxy_for'])}{colon}{text(ref['limitation'])}"
                            if ref.get("proxy_for") else ""))
    return "\n".join(lines).rstrip() + "\n"


def _write_atomic(output: str | Path, files: dict[str, str]) -> Path:
    destination = Path(output).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and any(destination.iterdir()):
        raise UniverseError(f"output directory is not empty: {destination}")
    scratch = Path(tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent))
    try:
        for name, content in files.items():
            (scratch / name).write_text(content, encoding="utf-8")
        if destination.exists():
            destination.rmdir()
        os.replace(scratch, destination)
    except Exception:
        shutil.rmtree(scratch, ignore_errors=True)
        raise
    return destination


def artifact_stem(universe: dict[str, Any]) -> str:
    """`crypto-light-2026-09-17`.

    The watchlist leaves this directory the moment it is useful — it gets imported, mailed,
    dropped in a downloads folder next to last quarter's. A file called `universe.txt` says
    nothing about which universe or when; the name has to carry that on its own.
    """
    suffix = "-partial" if universe.get("delivery", {}).get("status") == "partial" else ""
    return f"{universe['market']}-{universe['profile']}-{universe['as_of']}{suffix}"


def write_artifacts(
    universe: dict[str, Any],
    report: dict[str, Any],
    output: str | Path,
    language: str | None = None,
) -> dict[str, Any]:
    from report_html import render_html

    stem = artifact_stem(universe)
    written = report_languages(universe, language)
    files = {
        f"{stem}.json": json.dumps(universe, ensure_ascii=False, indent=2) + "\n",
        f"{stem}.validation.json": json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        f"{stem}.txt": render_txt(universe),
    }
    for code in written:
        files[f"{stem}.{code}.md"] = render_markdown(universe, report, code)
        files[f"{stem}.{code}.html"] = render_html(universe, report, code)
    destination = _write_atomic(output, files)
    return {
        "directory": destination,
        "universe": destination / f"{stem}.json",
        "validation": destination / f"{stem}.validation.json",
        "watchlist": destination / f"{stem}.txt",
        # Keyed by language, so a caller that wants the English one asks for it by name instead
        # of reconstructing a filename.
        "reports": {code: destination / f"{stem}.{code}.md" for code in written},
        "html_reports": {code: destination / f"{stem}.{code}.html" for code in written},
    }


DRIFT_REPORT_LIMIT = 20


def diff_universes(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """What changed between two universes, whoever produced them.

    `maintain` reports the turnover of one review. This answers the question a review cannot:
    two universes of the same market built in different sessions, months apart, or by two people
    — did they converge? For a declared market that is not a nicety, because the venue list and
    the symbol shape were researched at run time and a session that researched them differently
    built something that is not comparable at all. That comparison comes first in the output for
    exactly that reason.
    """
    def members(universe: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {str(item["ticker"]): item for item in universe.get("members") or []}

    def themes(universe: dict[str, Any]) -> dict[str, str]:
        return {
            str(item["theme_code"]): str(item["theme_name"])
            for item in universe.get("taxonomy") or []
        }

    old_members, new_members = members(before), members(after)
    old_themes, new_themes = themes(before), themes(after)
    shared = sorted(set(old_members) & set(new_members))
    added = sorted(set(new_members) - set(old_members))
    removed = sorted(set(old_members) - set(new_members))

    header: dict[str, Any] = {}
    for field in ("market", "profile", "as_of", "source_as_of", "policy_version", "version_hash",
                  "content_hash"):
        if before.get(field) != after.get(field):
            header[field] = {"before": before.get(field), "after": after.get(field)}

    # Two universes built under different identity rules are not two versions of one universe.
    rules = "unchanged"
    if before.get("market_spec") != after.get("market_spec"):
        rules = {"before": before.get("market_spec"), "after": after.get("market_spec")}

    drift: list[dict[str, Any]] = []
    for ticker in shared:
        old_metrics = old_members[ticker].get("metrics") or {}
        new_metrics = new_members[ticker].get("metrics") or {}
        for metric in sorted(set(old_metrics) | set(new_metrics)):
            was, now = old_metrics.get(metric), new_metrics.get(metric)
            if was == now or was is None or now is None:
                continue
            drift.append({
                "ticker": ticker, "metric": metric,
                "before": was, "after": now, "delta": round(float(now) - float(was), 1),
            })
    drift.sort(key=lambda item: (-abs(item["delta"]), item["ticker"], item["metric"]))

    return {
        "identical": not (
            header or rules != "unchanged" or added or removed
            or old_themes != new_themes or drift
            or before.get("taxonomy") != after.get("taxonomy")
            or content_hash(before) != content_hash(after)
            or any(old_members[t]["theme_code"] != new_members[t]["theme_code"] for t in shared)
            or any(old_members[t]["role"] != new_members[t]["role"] for t in shared)
        ),
        "market_spec": rules,
        "coverage_plan": {
            "changed": before.get("coverage_plan") != after.get("coverage_plan"),
            "before_hash": canonical_hash(before.get("coverage_plan")),
            "after_hash": canonical_hash(after.get("coverage_plan")),
        },
        "references": {
            "before": before.get("coverage_plan", {}).get("references", []),
            "after": after.get("coverage_plan", {}).get("references", []),
        },
        "admissions_changed": [t for t in shared
                               if old_members[t].get("admission") !=
                               new_members[t].get("admission")],
        "header": header,
        "turnover": round((len(added) + len(removed)) / max(len(old_members), 1), 4),
        "added": added,
        "removed": removed,
        "moved": [
            {
                "ticker": ticker,
                "before": old_members[ticker]["theme_code"],
                "after": new_members[ticker]["theme_code"],
            }
            for ticker in shared
            if old_members[ticker]["theme_code"] != new_members[ticker]["theme_code"]
        ],
        "rerolled": [
            {
                "ticker": ticker,
                "before": old_members[ticker]["role"],
                "after": new_members[ticker]["role"],
            }
            for ticker in shared
            if old_members[ticker]["role"] != new_members[ticker]["role"]
        ],
        "themes": {
            "added": sorted(set(new_themes) - set(old_themes)),
            "removed": sorted(set(old_themes) - set(new_themes)),
            "renamed": [
                {"theme_code": code, "before": old_themes[code], "after": new_themes[code]}
                for code in sorted(set(old_themes) & set(new_themes))
                if old_themes[code] != new_themes[code]
            ],
        },
        "metric_drift": {
            "fields": len(drift),
            # A full drift list on a 250-member universe is not something anyone reads, and the
            # tail of it is noise. The largest moves are the ones worth a question.
            "largest": drift[:DRIFT_REPORT_LIMIT],
        },
    }


def apply_change_set(
    universe_raw: dict[str, Any],
    changes: dict[str, Any],
    policy: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    universe = deepcopy(universe_raw)
    current_report = validate_universe(universe, policy)
    if not current_report["passed"]:
        raise UniverseError("current universe is invalid: " + "; ".join(current_report["errors"]))
    if changes.get("schema_version") != 1:
        raise UniverseError("changes schema_version must be 1")
    if changes.get("market") != universe.get("market"):
        raise UniverseError("changes and universe markets differ")
    if changes.get("market_spec"):
        # The rules a universe was built under are part of its identity. A review that wanted
        # different ones is a new universe, not a change set against this one.
        raise UniverseError("a change set cannot redeclare market_spec; rebuild instead")
    rules, _ = resolve_market(universe["market"], universe.get("market_spec"))
    if changes.get("base_version_hash") != universe.get("version_hash"):
        raise UniverseError("stale change set: base_version_hash does not match")
    if (changes.get("base_content_hash")
            and changes["base_content_hash"] != universe.get("content_hash")):
        raise UniverseError("stale change set: base_content_hash does not match refreshed facts")
    if changes.get("complete") is not True:
        raise UniverseError("maintenance facts are incomplete; refusing to update")
    if not changes.get("as_of"):
        raise UniverseError("maintenance as_of is required")
    sources = validate_evidence(changes.get("sources") or [], "maintenance")
    require_strong_evidence(sources, "maintenance")
    depth = str(changes.get("review_depth", ""))
    if depth not in policy["maintenance"]:
        raise UniverseError("review_depth must be routine, deep, or event")
    coverage_level = int(policy["profiles"][universe["profile"]]["coverage_level"])
    taxonomy_by_code = {item["theme_code"]: item for item in universe["taxonomy"]}
    members = universe["members"]
    before_members = {item["ticker"]: deepcopy(item) for item in members}
    before = set(before_members)

    def locate(ticker: str) -> tuple[int, dict[str, Any]]:
        normalized = str(ticker).strip().upper()
        for index, member in enumerate(members):
            if member["ticker"] == normalized:
                return index, member
        raise UniverseError(f"ticker is not in the universe: {ticker}")

    raw_ops = changes.get("ops") or []
    if not isinstance(raw_ops, list):
        raise UniverseError("changes ops must be a list")
    if not raw_ops:
        raise UniverseError("maintenance requires at least one op; use NO_CHANGE explicitly")
    ops = sorted(
        enumerate(raw_ops),
        key=lambda pair: (OP_ORDER.get(str(pair[1].get("op", "")).upper(), 99), pair[0]),
    )
    op_evidence: list[tuple[str, list[dict[str, Any]]]] = []
    for original_index, op in ops:
        name = str(op.get("op", "")).upper()
        if name not in OP_ORDER:
            raise UniverseError(f"op #{original_index}: unsupported op {name}")
        if name == "NO_CHANGE":
            if not str(op.get("reason", "")).strip():
                raise UniverseError(f"op #{original_index}: NO_CHANGE requires reason")
            continue
        evidence = op.get("evidence") or []
        reason = str(op.get("reason", "")).strip()
        subject = f"op #{original_index} {name}"
        if name in DECISION_OPS | THEME_OPS | {"REFRESH"}:
            if not evidence or not reason:
                raise UniverseError(f"{subject}: requires reason and evidence")
            evidence = validate_evidence(evidence, subject)
            require_strong_evidence(evidence, subject)
            op_evidence.append((subject, evidence))
        if name == "ADD_THEME":
            theme = {
                "l1_code": str(op.get("l1_code", "")).strip(),
                "l1_name": str(op.get("l1_name", "")).strip(),
                "theme_code": str(op.get("theme_code", "")).strip().upper(),
                "theme_name": str(op.get("theme_name", "")).strip(),
                "coverage_level": op.get("coverage_level"),
                "weight": op.get("weight", DEFAULT_THEME_WEIGHT),
            }
            theme.update({k: op[k] for k in ("purpose", "representative_roles") if k in op})
            if theme["theme_code"] in taxonomy_by_code:
                raise UniverseError(f"{subject}: theme {theme['theme_code']} already exists")
            level = theme["coverage_level"]
            if level not in (1, 2, 3) or int(level) > coverage_level:
                raise UniverseError(
                    f"{subject}: coverage_level must be 1..{coverage_level} for this profile"
                )
            universe["taxonomy"] = normalize_taxonomy(universe["taxonomy"] + [theme])
            taxonomy_by_code = {item["theme_code"]: item for item in universe["taxonomy"]}
        elif name == "UPDATE_THEME":
            code = str(op.get("theme", "")).strip().upper()
            if code not in taxonomy_by_code:
                raise UniverseError(f"{subject}: unknown theme {code}")
            changes_to_theme = {k: op[k] for k in (
                "weight", "theme_name", "purpose", "representative_roles") if k in op}
            if not changes_to_theme:
                raise UniverseError(
                    f"{subject}: provide weight, theme_name, purpose or representative_roles"
                )
            taxonomy_by_code[code].update(changes_to_theme)
            universe["taxonomy"] = normalize_taxonomy(list(taxonomy_by_code.values()))
            taxonomy_by_code = {item["theme_code"]: item for item in universe["taxonomy"]}
        elif name == "REFRESH":
            index, old = locate(op.get("ticker", ""))
            refreshed = normalize_candidate(
                rules,
                op.get("candidate") or {},
                taxonomy_by_code,
                coverage_first=universe.get("selection_model") == "coverage_first",
            )
            keys = ("ticker", "asset_id", "theme_code", "role", "required")
            if any(refreshed[k] != old[k] for k in keys) or not refreshed["eligible"]:
                raise UniverseError(f"{subject}: REFRESH must preserve membership and role")
            members[index] = refreshed
        elif name == "REMOVE_THEME":
            code = str(op.get("theme", "")).strip().upper()
            if code not in taxonomy_by_code:
                raise UniverseError(f"{subject}: unknown theme {code}")
            holders = [item["ticker"] for item in members if item["theme_code"] == code]
            if holders:
                raise UniverseError(
                    f"{subject}: move or remove its members first: {', '.join(holders)}"
                )
            universe["taxonomy"] = [
                item for item in universe["taxonomy"] if item["theme_code"] != code
            ]
            taxonomy_by_code = {item["theme_code"]: item for item in universe["taxonomy"]}
        elif name == "REMOVE":
            index, member = locate(op.get("ticker", ""))
            if member["role"] in {"BENCHMARK", "ANCHOR"} or member["required"]:
                raise UniverseError(f"op #{original_index}: anchor removal requires REPLACE")
            members.pop(index)
        elif name == "MOVE":
            _, member = locate(op.get("ticker", ""))
            destination = str(op.get("to_theme", "")).upper()
            if destination not in taxonomy_by_code:
                raise UniverseError(f"{subject}: unknown destination theme {destination}")
            member["theme_code"] = destination
            member["l1_code"] = taxonomy_by_code[destination]["l1_code"]
        elif name in {"ADD", "REPLACE"}:
            candidate_input = deepcopy(op.get("candidate") or {})
            candidate_input["evidence"] = deepcopy(evidence)
            candidate = normalize_candidate(
                rules,
                candidate_input,
                taxonomy_by_code,
                coverage_first=universe.get("selection_model") == "coverage_first",
            )
            if not candidate["eligible"]:
                raise UniverseError(f"op #{original_index}: candidate is not eligible")
            candidate["reason"] = reason or candidate["reason"]
            if name == "REPLACE":
                index, old = locate(op.get("ticker", ""))
                if (old["role"] in {"BENCHMARK", "ANCHOR"} or old["required"]) and not (
                    candidate["role"] in {"BENCHMARK", "ANCHOR"} or candidate["required"]
                ):
                    raise UniverseError(
                        f"op #{original_index}: anchor replacement must remain an anchor"
                    )
                members.pop(index)
            if any(item["asset_id"] == candidate["asset_id"] for item in members):
                raise UniverseError(f"{subject}: duplicate asset {candidate['asset_id']}")
            members.append(candidate)

    members.sort(key=lambda item: (
        item["theme_code"],
        item["ticker"] if universe.get("selection_model") == "coverage_first" else rank_key(item),
    ))
    after = {item["ticker"] for item in members}
    added = sorted(after - before)
    removed = sorted(before - after)
    audit = [
        item for item in universe.get("selection_audit", [])
        if item.get("ticker") not in set(added)
    ]
    audited_tickers = {item.get("ticker") for item in audit}
    for ticker in removed:
        if ticker not in audited_tickers:
            audit.append({
                "ticker": ticker,
                "asset_id": before_members[ticker]["asset_id"],
                "theme_code": before_members[ticker]["theme_code"],
                "reasons": ["removed_by_maintenance"],
            })
    universe["selection_audit"] = audit
    turnover = (len(added) + len(removed)) / max(len(before), 1)
    threshold = float(policy["maintenance"][depth]["turnover_warning"])
    extra_warnings: list[str] = []
    extra_errors: list[str] = []
    if turnover > threshold * 2:
        extra_errors.append(
            f"turnover {turnover:.1%} exceeds hard limit {threshold * 2:.1%} for {depth}"
        )
    elif turnover > threshold:
        extra_warnings.append(
            f"turnover {turnover:.1%} exceeds warning {threshold:.1%} for {depth}"
        )
    recently_removed = {
        asset
        for item in universe.get("history", [])[-4:]
        for asset in item.get("removed", [])
    }
    flip_flops = sorted(set(added) & recently_removed)
    if flip_flops:
        extra_warnings.append("recently removed tickers re-added: " + ", ".join(flip_flops))

    history_entry = {
        "as_of": str(changes.get("as_of", "")),
        "review_depth": depth,
        "summary": str(changes.get("summary", "")),
        "added": added,
        "removed": removed,
        "turnover": turnover,
        "deferred": deepcopy(changes.get("deferred") or []),
    }
    universe["as_of"] = history_entry["as_of"] or universe["as_of"]
    universe["source_as_of"] = str(changes["as_of"])
    universe["sources"] = sources
    if "measurement_audit" in changes:
        universe["measurement_audit"] = deepcopy(changes["measurement_audit"])
    universe["measurement"] = normalize_measurement(
        changes.get("measurement") or universe.get("measurement") or {},
        metrics_in_use(members),
        blended_metrics(members),
    )
    extra_warnings.extend(
        staleness_warnings(
            str(changes["as_of"]), [("maintenance", sources)] + op_evidence, policy
        )
    )
    universe.setdefault("history", []).append(history_entry)
    universe["version_hash"] = universe_hash(universe)
    universe["content_hash"] = content_hash(universe)
    report = validate_universe(universe, policy)
    report["errors"] = report["errors"] + extra_errors
    report["warnings"] = report["warnings"] + extra_warnings
    report["passed"] = not report["errors"]
    report["maintenance"] = history_entry
    if not report["passed"]:
        raise UniverseError("maintenance failed validation: " + "; ".join(report["errors"]))
    return universe, report
