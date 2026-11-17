"""Coverage-first selection. Economic obligations are independent of display taxonomy.

The research plan is an auditable assertion, not machine proof of business leadership.
No network access, inferred identities, silent substitutions or capacity padding.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from copy import deepcopy

from display_core import theme_groups
from universe_core import (
    PROFILES,
    UniverseError,
    canonical_hash,
    content_hash,
    normalize_snapshot,
    parse_watchlist,
    require_strong_evidence,
    universe_hash,
    validate_evidence,
    validate_universe,
)

MODEL = "coverage_first"
CORE_KINDS = {"leader", "peer"}
REFERENCE_KINDS = {"index", "yield", "fx", "commodity", "etf", "spot", "future", "ratio"}
MAX_PARTIAL_GAP_RATIO = 0.05


def need(condition, message):
    if not condition:
        raise UniverseError("coverage: " + message)


def sentence(value):
    return isinstance(value, str) and bool(value.strip())


def integer(value, minimum=0):
    return type(value) is int and value >= minimum


def evidence(items, subject, as_of):
    from datetime import date

    rows = validate_evidence(items, subject)
    require_strong_evidence(rows, subject)
    for row in rows:
        try:
            age = (date.fromisoformat(as_of) - date.fromisoformat(row["as_of"])).days
        except (ValueError, TypeError) as exc:
            raise UniverseError(f"coverage: {subject}: invalid evidence date") from exc
        need(0 <= age <= 180, f"{subject}: evidence must be dated within 180 days")
    return rows


def keyed(rows, key, subject):
    need(isinstance(rows, list), f"{subject} must be a list")
    need(
        all(isinstance(r, dict) and sentence(r.get(key)) for r in rows),
        f"{subject} needs nonempty {key}",
    )
    result = {r[key]: r for r in rows}
    need(len(result) == len(rows), f"duplicate {subject} {key}")
    return result


def plan_check(plan, as_of, taxonomy):
    need(
        isinstance(plan, dict) and plan.get("schema_version") == 1,
        "coverage_plan schema_version 1 is required; research the Core before rebuilding",
    )
    need(plan.get("origin") in {"new", "migration"}, "plan origin must be new or migration")
    need(sentence(plan.get("scope")), "plan needs an explicit market/instrument scope")
    evidence(plan.get("evidence", []), "market structure", as_of)
    budgets = plan.get("budgets", {})
    need(
        isinstance(budgets, dict)
        and set(budgets) == set(PROFILES)
        and all(integer(n, 1) for n in budgets.values()),
        "budgets must give positive entity ceilings for all four profiles",
    )
    need([budgets[p] for p in PROFILES] == sorted(budgets.values()), "budgets must be nested")
    keyed(plan.get("roster"), "asset_id", "core roster")
    sectors = keyed(plan.get("sectors"), "id", "sectors")
    need(bool(sectors), "at least one economic sector is required")
    for key, row in sectors.items():
        weight = row.get("weight")
        need(
            type(weight) in (int, float) and math.isfinite(weight) and weight > 0,
            f"{key}: positive stable weight required",
        )
        need(sentence(row.get("rationale")), f"{key}: market-structure rationale required")
        caps = row.get("caps", {})
        need(
            isinstance(caps, dict)
            and set(caps) == set(PROFILES)
            and all(integer(n) for n in caps.values()),
            f"{key}: four absolute sector caps required",
        )
        need([caps[p] for p in PROFILES] == sorted(caps.values()), f"{key}: caps must be nested")
    branches = keyed(plan.get("branches"), "id", "branches")
    need(bool(branches), "economic branches are required")
    representatives = set()
    for key, row in branches.items():
        need(
            row.get("sector") in sectors and sentence(row.get("purpose")),
            f"{key}: sector and economic purpose required",
        )
        need(row.get("min_profile") in PROFILES[:3], f"{key}: branches must enter by Heavy")
        ids = row.get("representatives")
        need(
            isinstance(ids, list) and ids and all(sentence(x) for x in ids),
            f"{key}: necessary representative asset_ids required",
        )
        need(
            len(ids) == len(set(ids)) and not representatives.intersection(ids),
            f"{key}: an entity may represent only one primary economic branch",
        )
        representatives.update(ids)
    need(
        {r["sector"] for r in branches.values()} == set(sectors),
        "every sector needs an economic branch",
    )
    refs = keyed(plan.get("references", []), "id", "references")
    themes = {t["theme_code"] for t in taxonomy}
    presentation = plan.get("display_groups", {})
    need(isinstance(presentation, dict), "display_groups must be a profile-keyed object")
    if presentation:
        need(set(presentation) == set(PROFILES), "display_groups needs all four profiles")
        need(presentation["max"] == presentation["heavy"], "Max must retain Heavy display groups")
        for profile, rows in presentation.items():
            groups = keyed(rows, "id", profile + " display groups")
            mapped = set()
            for key, row in groups.items():
                source = row.get("themes")
                need(isinstance(source, list) and len(source) >= 2
                     and all(sentence(x) for x in source)
                     and set(source) <= themes and len(source) == len(set(source))
                     and key in source and not mapped.intersection(source),
                     f"{key}: display groups need unique known themes and a constituent id")
                need(sentence(row.get("name"))
                     and re.fullmatch(r"[A-Z0-9_]+", row["name"])
                     and sentence(row.get("reason")),
                     f"{key}: display group name and economic-similarity reason required")
                mapped.update(source)
    symbols = set()
    for key, row in refs.items():
        ticker = row.get("ticker", "")
        need(
            isinstance(ticker, str) and re.fullmatch(r"[A-Z0-9_]+:[A-Z0-9_.!/-]+", ticker),
            f"{key}: reference needs a full verified symbol",
        )
        need(ticker not in symbols, f"duplicate reference ticker {ticker}")
        symbols.add(ticker)
        need(row.get("theme_code") in themes, f"{key}: unknown display theme")
        need(
            row.get("kind") in REFERENCE_KINDS and sentence(row.get("observes")),
            f"{key}: reference kind and exact observation required",
        )
        # A proxy is explicit and never earns the direct reference's identity.
        if row.get("proxy_for"):
            need(sentence(row.get("limitation")), f"{key}: proxy limitation required")
        evidence(row.get("evidence", []), key, as_of)
    baseline = plan.get("baseline")
    need(
        plan["origin"] != "migration" or isinstance(baseline, dict),
        "migration requires the original Core and complete decisions",
    )
    if baseline is not None:
        need(
            isinstance(baseline, dict) and sentence(baseline.get("watchlist")),
            "baseline needs original watchlist text",
        )
        need(
            hashlib.sha256(baseline["watchlist"].encode()).hexdigest() == baseline.get("sha256"),
            "baseline SHA-256 does not match original text",
        )
        originals = [t for _, ts in parse_watchlist(baseline["watchlist"]) for t in ts]
        need(
            originals and len(originals) == len(set(originals)), "Core has duplicate/empty symbols"
        )
        decisions = keyed(baseline.get("decisions"), "ticker", "baseline decisions")
        need(
            set(decisions) == set(originals),
            "every original Core symbol needs exactly one decision",
        )
        for ticker, row in decisions.items():
            need(
                row.get("action") in {"retain", "replace", "remove", "pending"},
                f"{ticker}: invalid Core decision",
            )
            if row["action"] != "pending":
                need(sentence(row.get("reason")), f"{ticker}: Core decision needs a reason")
                evidence(row.get("evidence", []), ticker, as_of)
                if row["action"] != "remove":
                    need(
                        bool(row.get("asset_id")) != bool(row.get("reference_id")),
                        f"{ticker}: bind one asset_id or reference_id",
                    )
    return sectors, branches, refs


def admission_check(candidate, plan, branches, as_of, market):
    need(
        candidate["metrics"].get("liquidity") is not None,
        f"{candidate['ticker']}: entities need measured liquidity",
    )
    a = candidate.get("admission")
    ticker = candidate["ticker"]
    need(isinstance(a, dict), f"{ticker}: missing researched admission (old role is insufficient)")
    kind = a.get("kind")
    need(kind in CORE_KINDS | {"satellite"}, f"{ticker}: unknown admission kind")
    branch = a.get("branch")
    need(branch in branches, f"{ticker}: unknown economic branch")
    minimum = a.get("min_profile")
    need(minimum in PROFILES, f"{ticker}: admission min_profile required")
    need(
        sentence(a.get("business")) and (kind == "satellite" or sentence(a.get("quality"))),
        f"{ticker}: business representation required; core also needs domain-specific quality",
    )
    evidence(a.get("evidence", []), ticker + " admission", as_of)
    if market == "crypto":
        need(
            sentence(a.get("ecosystem_id")) and sentence(a.get("token_role")),
            f"{ticker}: crypto ecosystem_id and token_role required",
        )
    expected = set(branches[branch]["representatives"])
    if kind in CORE_KINDS:
        need(
            candidate["asset_id"] in expected, f"{ticker}: core admission absent from branch roster"
        )
        need(minimum != "max", f"{ticker}: necessary representative delayed to Max")
        need(
            kind == "leader" or minimum == "heavy",
            f"{ticker}: peers enter at Heavy, not Light/Medium",
        )
        need(
            candidate["role"] in {"ANCHOR", "THEME_LEADER", "QUALITY_LEADER", "BENCHMARK"},
            f"{ticker}: core admission contradicts observation role",
        )
    else:
        need(
            candidate["asset_id"]
            not in {x for b in branches.values() for x in b["representatives"]},
            f"{ticker}: necessary representative cannot be relabelled satellite",
        )
        need(
            minimum in {"heavy", "max"} and candidate["role"] == "BETA_SATELLITE",
            f"{ticker}: satellites need the supplementary Beta role and cannot enter Light/Medium",
        )
        distinct = a.get("distinct_from")
        roster = {x for b in branches.values() for x in b["representatives"]}
        need(
            isinstance(distinct, list)
            and distinct
            and all(sentence(x) for x in distinct)
            and set(distinct) <= roster
            and sentence(a.get("incremental_value")),
            f"{ticker}: explain incremental value relative to named core representatives",
        )
    # The tool is explicit; economic identity cannot silently change with a venue or contract.
    binding = a.get("instrument", {})
    need(
        isinstance(binding, dict)
        and binding.get("kind") in {"equity", "spot", "perpetual", "etf"}
        and sentence(binding.get("quote_currency"))
        and type(binding.get("units")) in (int, float)
        and math.isfinite(binding["units"])
        and binding["units"] > 0,
        f"{ticker}: instrument kind, quote_currency and contract units required",
    )
    if kind == "satellite":
        market_cap_check(a, ticker, as_of, market)
    return a


def market_cap_check(admission, ticker, as_of, market):
    """Sourced equity/circulating capitalization; no FDV or inferred quality score."""
    from datetime import date

    cap = admission.get("market_cap", {})
    need(isinstance(cap, dict), f"{ticker}: market_cap object required")
    value = cap.get("value")
    need(type(value) in (int, float) and math.isfinite(value) and value > 0,
         f"{ticker}: positive sourced market cap required")
    currency = "USD" if market == "crypto" else admission["instrument"]["quote_currency"]
    need(cap.get("currency") == currency, f"{ticker}: market cap must use {currency}")
    need(cap.get("basis") == ("circulating" if market == "crypto" else "equity"),
         f"{ticker}: equity/circulating market cap required, not FDV")
    try:
        age = (date.fromisoformat(as_of) - date.fromisoformat(cap.get("as_of", ""))).days
    except (ValueError, TypeError) as exc:
        raise UniverseError(f"coverage: {ticker}: invalid market cap date") from exc
    need(0 <= age <= 30, f"{ticker}: market cap must be dated within 30 days")
    need(any(e.get("url") == cap.get("source") and e.get("as_of") == cap["as_of"]
             and e.get("tier") in (1, 2) for e in admission.get("evidence", [])),
         f"{ticker}: market cap source must match dated tier 1/2 admission evidence")


def comparable_caps(candidates):
    currencies = {c["admission"]["market_cap"]["currency"] for c in candidates
                  if c["admission"]["kind"] == "satellite"}
    need(len(currencies) <= 1, "Beta market caps must use one comparable currency")


def core_decisions(plan, members, refs, profile):
    baseline = plan.get("baseline")
    if not baseline:
        return
    held = {c["asset_id"]: c for c in members}
    for row in baseline["decisions"]:
        ticker, action = row["ticker"], row["action"]
        if profile in {"heavy", "max"}:
            need(action != "pending", f"unresolved Core decision: {ticker}")
        if action == "remove":
            need(
                ticker not in {c["ticker"] for c in members} | {r["ticker"] for r in refs.values()},
                f"Core removal still exported: {ticker}",
            )
        if action in {"pending", "remove"}:
            continue
        obj = held.get(row.get("asset_id")) or refs.get(row.get("reference_id"))
        if profile in {"heavy", "max"}:
            need(obj is not None, f"Core {action} target missing: {ticker}")
        if obj and action == "retain":
            need(
                obj["ticker"] == ticker,
                f"{ticker}: changed instrument requires replace, not retain",
            )


def expansion_minimum(heavy_count, policy):
    """Entity-only minimum growth; existing capacity gates provide the ceilings."""
    rule = policy.get("coverage", {}).get("max_expansion")
    need(
        isinstance(rule, dict) and set(rule) == {"min"},
        "policy needs max_expansion min only",
    )
    minimum = rule["min"]
    need(
        type(minimum) in (int, float) and math.isfinite(minimum) and minimum >= 0.3,
        "Max expansion minimum must be at least 30%",
    )
    return heavy_count + math.ceil(heavy_count * minimum - 1e-9)


def expansion_distribution(seed, added_count):
    """Heavy proportions, with at most the one-seat integer rounding remainder per group."""
    mapping = theme_groups(seed["coverage_plan"])
    counts = Counter(mapping.get(c["theme_code"], c["theme_code"]) for c in seed["members"])
    total = len(seed["members"])
    return mapping, counts, {k: math.ceil(n * added_count / total - 1e-9)
                             for k, n in counts.items()}


def partial_delivery(heavy_count, selected_count, policy):
    required = expansion_minimum(heavy_count, policy)
    missing = required - selected_count
    need(selected_count > heavy_count and 0 < missing <= required * MAX_PARTIAL_GAP_RATIO,
         "Max partial delivery requires positive growth and a gap within 5% of required entities")
    return {"status": "partial", "reason": "max_growth_shortfall",
            "required_entities": required, "shortfall": missing,
            "allowed_gap_ratio": MAX_PARTIAL_GAP_RATIO}


def quality_check(universe, policy, *, assembling=False):
    """Recompute the same gates for build, maintenance and stored-file validation."""
    p, profile = universe.get("coverage_plan"), universe["profile"]
    need("delivery" not in universe or profile == "max", "partial delivery is Max-only")
    settings = policy.get("coverage", {})
    limits = settings.get("satellite_max", {})
    need(set(limits) == set(PROFILES), "policy needs four satellite ceilings")
    for name, maximum in zip(PROFILES, (0, 0, 0.2, 0.35), strict=True):
        value = limits[name]
        need(
            type(value) in (int, float) and math.isfinite(value) and 0 <= value <= maximum,
            f"{name}: satellite ceiling may only tighten the coverage-first maximum",
        )
    medium_min = settings.get("medium_leader_min")
    need(
        type(medium_min) in (int, float) and 0.7 <= medium_min <= 1,
        "Medium leader coverage must be at least 70%",
    )
    sectors, branches, refs = plan_check(p, universe["source_as_of"], universe["taxonomy"])
    need(profile in PROFILES, "invalid profile")
    members = universe["members"]
    by_asset = {c["asset_id"]: c for c in members}
    need(len(by_asset) == len(members), "duplicate economic identity")
    need(
        not {r["ticker"] for r in refs.values()} & {c["ticker"] for c in members},
        "reference and entity layers duplicate the same instrument",
    )
    stage = PROFILES.index(profile)
    counts, kinds = Counter(), Counter()
    for c in members:
        a = admission_check(c, p, branches, universe["source_as_of"], universe["market"])
        need(PROFILES.index(a["min_profile"]) <= stage, f"{c['ticker']}: outside admission depth")
        counts[branches[a["branch"]]["sector"]] += 1
        kinds[a["kind"]] += 1
    comparable_caps(members)
    for branch in branches.values():
        if PROFILES.index(branch["min_profile"]) <= stage:
            representatives = [by_asset[x] for x in branch["representatives"] if x in by_asset]
            need(
                any(c["admission"]["kind"] in CORE_KINDS for c in representatives),
                f"uncovered economic branch: {branch['id']}",
            )
        if profile in {"heavy", "max"}:
            missing = set(branch["representatives"]) - set(by_asset)
            need(not missing, "missing necessary representatives: " + ", ".join(sorted(missing)))
    roster = p.get("roster", [])
    # Persist the entire reviewed core roster, so validation sees omitted leaders too.
    entries = keyed(roster, "asset_id", "core roster")
    expected = {x for b in branches.values() for x in b["representatives"]}
    need(set(entries) == expected, "core roster must match all branch representatives")
    for asset, a in entries.items():
        need(
            a.get("kind") in CORE_KINDS and a.get("min_profile") in PROFILES[:3],
            f"{asset}: invalid core roster",
        )
        need(a["kind"] == "leader" or a["min_profile"] == "heavy", f"{asset}: peer before Heavy")
        if PROFILES.index(a["min_profile"]) <= stage:
            need(asset in by_asset, f"necessary representative omitted at {profile}: {asset}")
        if asset in by_asset:
            held = by_asset[asset]["admission"]
            need(all(held[k] == a[k] for k in ("kind", "min_profile")), f"{asset}: roster mismatch")
    leaders = {a for a, row in entries.items() if row["kind"] == "leader"}
    need(bool(leaders), "no researched leaders in the core roster")
    share = len(leaders & set(by_asset)) / len(leaders)
    if profile == "medium":
        need(
            share >= policy["coverage"]["medium_leader_min"], "Medium misses most reviewed leaders"
        )
    need(
        len(members) <= universe["limits"]["target_count"] <= p["budgets"][profile],
        "entity budget exceeded or inconsistent with coverage plan",
    )
    for sector, n in counts.items():
        need(n <= sectors[sector]["caps"][profile], f"economic sector cap exceeded: {sector}")
    ceiling = policy["coverage"]["satellite_max"][profile]
    need(
        kinds["satellite"] <= len(members) * ceiling + 1e-9,
        f"{profile}: satellite share exceeds {ceiling:.0%}",
    )
    core_decisions(p, members, refs, profile)
    expansion = {}
    if profile == "max":
        seed = universe.get("heavy_base")
        need(
            isinstance(seed, dict) and seed.get("profile") == "heavy",
            "Max requires a Heavy base",
        )
        need(seed.get("selection_model") == MODEL, "legacy Heavy has no coverage certification")
        need(
            seed["market"] == universe["market"]
            and seed["source_as_of"] == universe["source_as_of"]
            and seed["coverage_plan"] == p,
            "Heavy base must share market, date and coverage plan",
        )
        checked = validate_universe(seed, policy)
        need(checked["passed"], "Heavy base failed validation: " + "; ".join(checked["errors"]))
        old = {c["asset_id"]: c for c in seed["members"]}
        need(set(old) <= set(by_asset), "Max dropped Heavy economic entities")
        need(
            all(by_asset[k] == c for k, c in old.items()),
            "Max changed Heavy facts/bindings; rebuild Heavy first",
        )
        need(
            all(c["admission"]["kind"] == "satellite" for k, c in by_asset.items() if k not in old),
            "Max cannot repair a missing Heavy core representative",
        )
        minimum = expansion_minimum(len(old), policy)
        maximum = universe["limits"]["target_count"]
        added_count = len(members) - len(old)
        delivery = universe.get("delivery")
        if "delivery" in universe:
            need(isinstance(delivery, dict)
                 and integer(delivery.get("required_entities"), 1)
                 and integer(delivery.get("shortfall"), 1)
                 and delivery == partial_delivery(len(old), len(members), policy),
                 "partial delivery metadata does not match the actual Max shortfall")
        # Vacancies retain their original target-group allocation; partial delivery cannot
        # move them to groups with plentiful candidates or change Heavy facts.
        distribution_basis = minimum - len(old) if delivery else added_count
        mapping, heavy_groups, group_caps = expansion_distribution(seed, distribution_basis)
        additions = Counter(mapping.get(c["theme_code"], c["theme_code"])
                            for k, c in by_asset.items() if k not in old)
        if not assembling:
            need(
                len(members) >= minimum or bool(delivery),
                f"Max expansion needs research: Heavy={len(old)}, selected={len(members)}, "
                f"required>={minimum}, entity_ceiling={maximum}, "
                f"missing={max(0, minimum - len(members))}; "
                "research more qualified Beta; do not weaken admission gates",
            )
        for group, n in additions.items():
            need(n <= group_caps.get(group, 0),
                 f"Max Heavy distribution exceeded: {group}, added={n}, "
                 f"proportional_cap={group_caps.get(group, 0)}; research other groups")
        expansion = {
            "heavy_entities": len(old),
            "added_beta": len(members) - len(old),
            "growth": (len(members) - len(old)) / len(old),
            "min_entities": minimum,
            "max_entities": maximum,
            **({"shortfall": minimum - len(members),
                "distribution_basis_added": distribution_basis} if delivery else {}),
            "distribution": {k: {"heavy": n, "added": additions[k],
                                 "added_cap": group_caps[k]}
                             for k, n in sorted(heavy_groups.items())},
        }
    return {
        "status": "partial" if universe.get("delivery") else "qualified",
        "leader_coverage": round(share, 4),
        "roles": dict(kinds),
        "sectors": dict(sorted(counts.items())),
        "entity_count": len(members),
        "references": len(refs),
        "unused_capacity": universe["limits"]["target_count"] - len(members),
        "plan_hash": canonical_hash(p),
        "evidence_boundary": "Checks declared research, not independent proof of leadership.",
        **({"expansion": expansion} if expansion else {}),
    }


def build(spec, raw, policy, previous=None):
    need(spec.get("schema_version") == 1, "build spec schema_version must be 1")
    snap = normalize_snapshot(raw, coverage_first=True)
    market, profile = snap["market"], spec.get("profile")
    need(spec.get("market") == market and profile in PROFILES, "spec market/profile mismatch")
    shortfall_action = spec.get("shortfall_action", "auto")
    need(isinstance(shortfall_action, str) and shortfall_action in {"auto", "deliver", "retry"},
         "unknown shortfall_action")
    need(not spec.get("as_of") or spec["as_of"] == snap["as_of"], "spec/snapshot dates differ")
    plan = deepcopy(raw.get("coverage_plan"))
    sectors, branches, refs = plan_check(plan, snap["as_of"], snap["taxonomy"])
    stage = PROFILES.index(profile)
    candidates = snap["candidates"]
    admitted = []
    audit = []
    for c in candidates:
        if not c["eligible"] or not c.get("admission"):
            audit.append(
                {
                    "ticker": c["ticker"],
                    "asset_id": c["asset_id"],
                    "theme_code": c["theme_code"],
                    "reasons": c["exclusion_reasons"]
                    or ["unverifiable_fact: admission not researched"],
                }
            )
            continue
        admission_check(c, plan, branches, snap["as_of"], market)
        admitted.append(c)
    comparable_caps(admitted)
    pool = {c["asset_id"]: c for c in admitted}
    roster = {x for b in branches.values() for x in b["representatives"]}
    need(
        roster <= set(pool),
        "research missing necessary representatives: " + ", ".join(sorted(roster - set(pool))),
    )
    # Roster is a contract, not inferred from liquid candidates or legacy ordering.
    for row in plan.get("roster", []):
        if row.get("asset_id") in pool:
            a = pool[row["asset_id"]]["admission"]
            need(
                all(row.get(k) == a[k] for k in ("kind", "min_profile")),
                "researched core roster mismatch",
            )
    target = spec.get("target_count", plan["budgets"][profile])
    need(
        integer(target, 1) and target <= plan["budgets"][profile],
        "target must respect plan entity ceiling",
    )
    if profile == "max":
        need(
            previous is not None and previous.get("profile") == "heavy",
            "Max requires --seed with a qualified Heavy",
        )
        selected = deepcopy(previous.get("members", []))
        need(
            all(pool.get(c["asset_id"]) == c for c in selected),
            "Heavy facts or eligibility changed; rebuild Heavy first",
        )
    else:
        selected = [
            c
            for c in admitted
            if c["admission"]["kind"] in CORE_KINDS
            and PROFILES.index(c["admission"]["min_profile"]) <= stage
        ]
        if previous:
            checked = validate_universe(previous, policy)
            need(
                checked["passed"] and previous.get("selection_model") == MODEL,
                "seed must be a qualified coverage-first universe",
            )
            need(
                previous.get("coverage_plan") == plan
                and previous["source_as_of"] == snap["as_of"]
                and previous["market"] == market,
                "seed plan/date/market differ",
            )
            need(PROFILES.index(previous["profile"]) <= stage, "narrow by rebuilding the same plan")
            for c in previous["members"]:
                need(pool.get(c["asset_id"]) == c, "seed facts changed; rebuild the base")
                if c["asset_id"] not in {s["asset_id"] for s in selected}:
                    selected.append(c)
    if profile == "heavy" and plan.get("baseline"):
        retained_ids = {
            r.get("asset_id")
            for r in plan["baseline"]["decisions"]
            if r["action"] in {"retain", "replace"}
        }
        for c in admitted:
            if c["asset_id"] in retained_ids and c not in selected:
                selected.append(c)
    for key in ("hard_ticker_cap", "tradingview_token_cap"):
        need(integer(spec.get(key, 1000), 1), f"{key} must be a positive integer")
    base = {
        "schema_version": 1,
        "selection_model": MODEL,
        "market": market,
        "market_spec": snap["market_spec"],
        "profile": profile,
        "as_of": snap["as_of"],
        "source_as_of": snap["as_of"],
        "policy_version": canonical_hash(policy),
        "coverage_plan": plan,
        "limits": {
            "target_count": target,
            "hard_ticker_cap": min(spec.get("hard_ticker_cap", 1000), 1000),
            "tradingview_token_cap": min(spec.get("tradingview_token_cap", 1000), 1000),
        },
        **{
            k: snap[k]
            for k in (
                "taxonomy",
                "sources",
                "measurement",
                "measurement_audit",
                "notes",
                "coverage",
            )
        },
        "members": selected,
        **({"report_translations": snap["report_translations"]}
           if "report_translations" in snap else {}),
        "selection_audit": audit,
        "history": [],
    }
    need(
        all(integer(base["limits"][k], 1) for k in ("hard_ticker_cap", "tradingview_token_cap")),
        "hard caps must be positive integers",
    )
    if profile == "max":
        base["heavy_base"] = deepcopy(previous)
    # Validate the skeleton BEFORE optional Beta; no candidate can conceal its absence.
    quality_check(base, policy, assembling=True)
    if profile == "max":
        minimum = expansion_minimum(len(selected), policy)
        need(
            minimum <= target,
            f"Max growth needs at least {minimum} entities; plan/spec ceiling {target} "
            "cannot meet it; review capacity before researching additions",
        )
        retained_beta = sum(c["admission"]["kind"] == "satellite" for c in selected)
        ceiling = policy["coverage"]["satellite_max"][profile]
        need(
            retained_beta + minimum - len(selected) <= minimum * ceiling + 1e-9,
            "Max growth conflicts with the satellite-share ceiling of this Heavy; "
            "review the Heavy plan without relabelling or dropping protected members",
        )

    def fits_export(items):
        exported = items + list(refs.values())
        display = theme_groups(plan, profile)
        return (
            len(exported) <= base["limits"]["hard_ticker_cap"]
            and len(exported) + len({display.get(c["theme_code"], c["theme_code"])
                                     for c in exported})
            <= base["limits"]["tradingview_token_cap"]
        )

    need(fits_export(selected), "necessary backbone exceeds TradingView/export cap")
    held = {c["asset_id"] for c in selected}
    counts = Counter(branches[c["admission"]["branch"]]["sector"] for c in selected)
    satellites = sum(c["admission"]["kind"] == "satellite" for c in selected)
    ceiling = policy["coverage"]["satellite_max"][profile]
    mapping, heavy_groups, group_caps = ({}, Counter(), {})
    added_groups = Counter()
    selection_target = target
    if profile == "max":
        selection_target = expansion_minimum(len(selected), policy)
        mapping, heavy_groups, group_caps = expansion_distribution(
            previous, selection_target - len(selected))
    while len(selected) < selection_target:
        choices = []
        for c in admitted:
            a = c["admission"]
            sector = branches[a["branch"]]["sector"]
            group = mapping.get(c["theme_code"], c["theme_code"])
            if (
                c["asset_id"] in held
                or a["kind"] != "satellite"
                or PROFILES.index(a["min_profile"]) > stage
                or counts[sector] >= sectors[sector]["caps"][profile]
                or satellites + 1 > (len(selected) + 1) * ceiling + 1e-9
                or (profile == "max" and added_groups[group] >= group_caps.get(group, 0))
                or not fits_export(selected + [c])
            ):
                continue
            # Max follows the frozen Heavy distribution; small groups gain no inverse bonus.
            choices.append(
                (
                    -(heavy_groups[group] / (2 * added_groups[group] + 1)
                      if profile == "max" else
                      sectors[sector]["weight"] / (2 * counts[sector] + 1)),
                    -a["market_cap"]["value"],
                    c["ticker"],
                    c,
                )
            )
        if not choices:
            break
        c = min(choices, key=lambda x: x[:3])[3]
        selected.append(c)
        held.add(c["asset_id"])
        counts[branches[c["admission"]["branch"]]["sector"]] += 1
        satellites += 1
        added_groups[mapping.get(c["theme_code"], c["theme_code"])] += 1
    selected.sort(key=lambda c: (c["theme_code"], c["ticker"]))
    for c in admitted:
        if c["asset_id"] not in held:
            audit.append(
                {
                    "ticker": c["ticker"],
                    "asset_id": c["asset_id"],
                    "theme_code": c["theme_code"],
                    "reasons": ["not_selected_under_budget: depth, sector or satellite ceiling"],
                }
            )
    if profile == "max" and len(selected) < selection_target and shortfall_action != "retry":
        missing = selection_target - len(selected)
        if missing <= selection_target * MAX_PARTIAL_GAP_RATIO and len(selected) > len(
            previous["members"]
        ):
            base["delivery"] = partial_delivery(len(previous["members"]), len(selected), policy)
    base["version_hash"] = universe_hash(base)
    base["content_hash"] = content_hash(base)
    report = validate_universe(base, policy)
    need(report["passed"], "; ".join(report["errors"]))
    return base, report


def audit_core(text, universe=None):
    """Exact-code migration queue. Identity equivalence requires subsequent human research."""
    grouped = parse_watchlist(text)
    current = {c["ticker"]: c for c in (universe or {}).get("members", [])}
    current.update(
        {r["ticker"]: r for r in (universe or {}).get("coverage_plan", {}).get("references", [])}
    )
    originals = [t for _, ts in grouped for t in ts]
    entries = [
        {
            "ticker": t,
            "original_group": group,
            "present_exactly": t in current,
            "current_theme": current[t]["theme_code"] if t in current else None,
            "action": "pending",
            "reason": "",
            "evidence": [],
        }
        for group, ts in grouped
        for t in ts
    ]
    return {
        "schema_version": 1,
        "kind": "core_migration_audit",
        "baseline": {"watchlist": text, "sha256": hashlib.sha256(text.encode()).hexdigest()},
        "comparison_version": (universe or {}).get("version_hash"),
        "original_count": len(originals),
        "exact_retained": sum(t in current for t in originals),
        "missing_exact": sorted(set(originals) - set(current)),
        "added_exact": sorted(set(current) - set(originals)),
        "decisions": entries,
        "status": "needs_research",
        "limitations": [
            "Exact codes are not economic identities or verified leaders.",
            "Core membership never auto-approves an admission or instrument substitution.",
        ],
    }
