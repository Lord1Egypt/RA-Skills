"""Pure report calculations over reconciled Skill inventory records."""


LEVEL_RANK_BY_HOST = {
    "claude-code": {"enterprise": 0, "personal": 1, "project": 2, "plugin": 3,
                    "other-host": 8, "unknown": 9},
    "openclaw": {"workspace": 0, "project": 1, "personal": 2, "managed": 3,
                 "enterprise": 0, "plugin": 3, "other-host": 8, "unknown": 9},
}
LEVEL_RANK = LEVEL_RANK_BY_HOST["claude-code"]


def level_rank(skill):
    family = skill.get("host_family") or skill.get("host") or ""
    table = LEVEL_RANK_BY_HOST.get(family, LEVEL_RANK)
    return table.get(skill.get("level"), 9)


def select_scope(skills, include_all):
    loaded = [skill for skill in skills if skill["loaded"]]
    candidates = [skill for skill in skills if skill["loaded"] or
                  (skill["host_family"] == "openclaw" and skill["discoverable"])]
    scope = skills if include_all else candidates
    by_key = {}
    for skill in scope:
        key = (skill["conflict_domain"], skill["namespace"] or "", skill["name"])
        by_key.setdefault(key, []).append(skill)
    return loaded, candidates, by_key


def build_conflicts(by_key):
    conflicts = []
    for (_, _, name), copies in by_key.items():
        if len(copies) < 2:
            continue
        ranked = sorted(copies, key=level_rank)
        winner, losers = ranked[0], ranked[1:]
        if len({copy["content_hash"] for copy in copies}) == 1:
            kind, severity = "redundant", "low"
        elif max(losers, key=lambda copy: copy["mtime"])["mtime"] > winner["mtime"]:
            kind, severity = "shadowed_newer", "high"
        else:
            kind, severity = "intentional_override", "medium"
        conflicts.append({
            "host": winner["host_family"],
            "instance_id": winner["instance_id"],
            "conflict_domain": winner["conflict_domain"],
            "name": name,
            "kind": kind,
            "severity": severity,
            "effective": {"level": winner["level"], "path": winner["path"],
                          "hash": winner["content_hash"], "mtime": winner["mtime"]},
            "shadowed": [{"level": copy["level"], "path": copy["path"],
                          "hash": copy["content_hash"], "mtime": copy["mtime"]}
                         for copy in losers],
        })
    conflicts.sort(key=lambda conflict: {"high": 0, "medium": 1, "low": 2}[
        conflict["severity"]])
    return conflicts


def build_budget(unique, host, include_all, budget, codex_fallback_budget):
    is_codex = host == "codex"
    effective_budget = codex_fallback_budget if is_codex else budget
    used = sum(len(group[0]["description"]) + len(group[0]["name"]) + 4 +
               (len(group[0]["path"]) + 1 if is_codex else 0) for group in unique)
    over = used - effective_budget
    at_risk_names = []
    if over > 0:
        accumulated = 0
        for group in sorted(unique, key=lambda item: -len(item[0]["description"])):
            at_risk_names.append(group[0]["name"])
            accumulated += len(group[0]["description"])
            if accumulated >= over:
                break
    longest = sorted(unique, key=lambda item: -len(item[0]["description"]))[:5]
    report = {
        "available": host in ("claude-code", "codex"),
        "scope": "all-on-disk" if include_all else "loaded-only",
        "counted_skills": len(unique),
        "budget_chars": effective_budget,
        "used_chars": used,
        "pct_used": round(used / effective_budget * 100, 1) if effective_budget else None,
        "over_by_chars": max(0, over),
        "skills_possibly_dropped": len(at_risk_names),
        "at_risk_skills": at_risk_names,
        "longest_descriptions": [
            {"name": group[0]["name"], "chars": len(group[0]["description"])}
            for group in longest],
        "excludes_builtin_skills": True,
        "policy": ("Codex initial skill list: at most 2% of model context, or 8000 chars "
                   "when context is unknown" if is_codex else
                   "Claude Code SLASH_COMMAND_TOOL_CHAR_BUDGET"),
        "note": ("The official Codex calculation includes name, description, and path. skills/list "
                 "does not expose the current model context window, so this report uses the official "
                 "8,000-character fallback. Codex shortens descriptions first, then omits skills with "
                 "a warning if the limit is still exceeded." if is_codex else
                 "Claude Code budget semantics vary by version. This value comes from the environment "
                 "or the 15,000-character default and excludes built-in skills without a SKILL.md on disk."),
        "workaround": None if is_codex else "SLASH_COMMAND_TOOL_CHAR_BUDGET=30000",
    }
    if not report["available"]:
        report.update({
            "scope": "not-available", "counted_skills": None, "budget_chars": None,
            "used_chars": None, "pct_used": None, "over_by_chars": None,
            "skills_possibly_dropped": None, "at_risk_skills": [],
            "longest_descriptions": [], "excludes_builtin_skills": None,
            "workaround": None,
        })
    return report


def build_trigger(loaded, usage, host, zombie_age):
    available = host == "claude-code" and bool(usage)
    scope = loaded if available else []
    zombies = [skill for skill in scope if skill["usage_count"] == 0 and
               skill["installed_days_ago"] >= zombie_age]
    too_new = [skill for skill in scope if skill["usage_count"] == 0 and
               skill["installed_days_ago"] < zombie_age]
    return {
        "available": available,
        "source": "~/.claude.json -> skillUsage",
        "entries_in_host_record": len(usage),
        "counts_are": "lifetime cumulative, not last-30-days",
        "zombie_min_age_days": zombie_age,
        "zombie_candidates": [
            {"name": skill["name"], "path": skill["path"],
             "installed_days_ago": skill["installed_days_ago"],
             "tier1_tokens": skill["tier1_tokens"]}
            for skill in sorted(zombies, key=lambda item: -item["tier1_tokens"])],
        "too_new_to_judge": [
            {"name": skill["name"], "installed_days_ago": skill["installed_days_ago"]}
            for skill in sorted(too_new, key=lambda item: item["installed_days_ago"])],
        "note": "Zero triggers are actionable only after %d installed days. Do not classify "
                "too_new_to_judge entries as zombies." % zombie_age,
    }


def build_structure(analysis_candidates, loaded, split_threshold):
    oversized = [skill for skill in analysis_candidates
                 if skill["tier2_core_tokens"] > split_threshold]
    oversized.sort(key=lambda skill: -skill["tier2_core_tokens"])
    return {
        "split_threshold_tokens": split_threshold,
        "criterion": "tier2_core_tokens (SKILL.md body); line count is reference only",
        "oversized": [
            {"name": skill["name"], "path": skill["path"],
             "tier2_core_tokens": skill["tier2_core_tokens"],
             "tier2_refs_tokens": skill["tier2_refs_tokens"],
             "tier2_max_tokens": skill["tier2_max_tokens"],
             "body_lines": skill["body_lines"],
             "tokens_per_line": round(skill["tier2_core_tokens"] /
                                      max(skill["body_lines"], 1), 1),
             "pct_of_200k_if_fully_read": round(skill["tier2_max_tokens"] / 200000 * 100, 2)}
            for skill in oversized],
        "missing_frontmatter": [
            {"name": skill["name"], "path": skill["path"],
             "has_name": skill["has_name"], "has_description": skill["has_description"]}
            for skill in loaded if not (skill["has_name"] and skill["has_description"])],
        "already_split": [
            {"name": skill["name"], "core": skill["tier2_core_tokens"],
             "refs": skill["tier2_refs_tokens"], "refs_files": skill["tier2_refs_files"],
             "max": skill["tier2_max_tokens"]}
            for skill in sorted(loaded, key=lambda item: -item["tier2_refs_tokens"])
            if skill["tier2_refs_tokens"] > 0],
        "large_data_corpus": [
            {"name": skill["name"], "files": skill["data_corpus_files"],
             "mb": round(skill["data_corpus_bytes"] / 1048576, 1)}
            for skill in sorted(loaded, key=lambda item: -item["data_corpus_bytes"])
            if skill["data_corpus_bytes"] > 1048576],
        "note": "oversized is based on core, which is always loaded on trigger. max in already_split "
                "is the full-read cost; splitting lowers average cost, not worst-case cost. "
                "large_data_corpus contains searchable Markdown corpora and is excluded from tier2; "
                "the report should mention its size only.",
    }


def build_security(skills):
    order = {"critical": 0, "high": 1, "medium": 2, "none": 3}
    flagged = [skill for skill in skills if skill["security"]["max_severity"] != "none"]
    flagged.sort(key=lambda skill: (
        order[skill["security"]["max_severity_uncited"]],
        order[skill["security"]["max_severity"]], not skill["loaded"]))
    return {
        "flagged_count": len(flagged),
        "critical_count": sum(1 for skill in flagged
                              if skill["security"]["max_severity"] == "critical"),
        "critical_uncited_count": sum(1 for skill in flagged
                                      if skill["security"]["max_severity_uncited"] == "critical"),
        "all_cited_count": sum(1 for skill in flagged
                               if skill["security"]["all_findings_cited"]),
        "fetches_external_count": sum(1 for skill in skills
                                      if skill["security"]["external_url_count"] > 0),
        "with_scripts_count": sum(1 for skill in skills if skill["security"]["exec_scripts"]),
        "flagged": [{"name": skill["name"], "path": skill["path"],
                     "loaded": skill["loaded"],
                     "severity": skill["security"]["max_severity"],
                     "severity_uncited": skill["security"]["max_severity_uncited"],
                     "all_findings_cited": skill["security"]["all_findings_cited"],
                     "findings": skill["security"]["findings"]} for skill in flagged[:30]],
        "note": "These are heuristic findings, not proof of malicious behavior, and false negatives "
                "are possible. The scanner's own files are excluded. cited=true only means the match "
                "looks like a quotation, example, or defensive explanation; it affects ordering only "
                "and never lowers severity or suppresses reporting. This hint is easy to bypass by adding "
                "'For example,' or an unmatched quote on the same line, so it must never be treated as a "
                "safety verdict. Every finding includes a line number and requires manual review.",
    }


def build_host_summaries(skills, usage, codex_runtime, openclaw_runtime):
    summaries = {}
    for host in ("claude-code", "codex", "openclaw", "hermes", "workbuddy"):
        host_skills = [skill for skill in skills if skill["host_family"] == host]
        loaded = [skill for skill in host_skills if skill["loaded"]]
        discoverable = [skill for skill in host_skills if skill["discoverable"]]
        scope = discoverable if host == "openclaw" else loaded
        groups = {}
        for skill in scope:
            groups.setdefault((skill["instance_id"] or "", skill["namespace"] or "",
                               skill["name"]), []).append(skill)
        unique = [sorted(group, key=level_rank)[0] for group in groups.values()]
        runtime_evidence = (
            codex_runtime["available"] if host == "codex" else
            any(runtime.get("available") for runtime in openclaw_runtime)
            if host == "openclaw" else False)
        verified_unique = len({(skill["instance_id"], skill["namespace"] or "", skill["name"])
                               for skill in scope if skill["runtime_verified"]})
        summaries[host] = {
            "skills_on_disk": len(host_skills),
            "discoverable_skills": len(discoverable),
            "runtime_verified_loaded_skills": (
                sum(1 for skill in host_skills if skill["runtime_verified"] and skill["loaded"])
                if runtime_evidence else None),
            "runtime_verified_unique_skills": verified_unique if runtime_evidence else None,
            "unique_discoverable_skills": len(unique),
            "tier1_total_tokens": sum(skill["tier1_tokens"] for skill in unique),
            "description_budget": ("available" if host == "claude-code" else
                                   "official-estimate" if host == "codex" and
                                   codex_runtime["available"] else
                                   "configurable" if host == "openclaw" else "not-available"),
            "trigger_data": "available" if host == "claude-code" and bool(usage)
                            else "not-available",
        }
    return summaries


def build_openclaw_instances(skills, openclaw_runtime):
    instances = {}
    ids = sorted({skill["instance_id"] for skill in skills
                  if skill["host_family"] == "openclaw" and skill["instance_id"]})
    for instance_id in ids:
        instance_skills = [skill for skill in skills
                           if skill["host_family"] == "openclaw" and
                           skill["instance_id"] == instance_id]
        discoverable = [skill for skill in instance_skills if skill["discoverable"]]
        disabled = [skill for skill in discoverable if skill["enabled_state"] is False]
        unknown = [skill for skill in discoverable if skill["enabled_state"] is None]
        unique_names = {(skill["namespace"] or "", skill["name"]) for skill in discoverable}
        runtime = next((item for item in openclaw_runtime
                        if item.get("instance_id") == instance_id), None)
        instances[instance_id] = {
            "instance_root": next((skill["instance_root"] for skill in instance_skills
                                   if skill["instance_root"]), None),
            "config_path": next((skill["config_path"] for skill in instance_skills
                                 if skill["config_path"]), None),
            "skills_on_disk": len(instance_skills),
            "discoverable_skills": len(discoverable),
            "unique_discoverable_skills": len(unique_names),
            "explicitly_disabled": len(disabled),
            "enabled_unknown": len(unknown),
            "runtime_verified": sum(1 for skill in discoverable if skill["runtime_verified"]),
            "runtime_catalog_skills": (len(runtime.get("skills", []))
                                       if runtime and runtime.get("available") else None),
            "runtime_semantics": ("eligible/model-visible metadata; full SKILL.md body load unknown"
                                  if runtime and runtime.get("available") else
                                  "filesystem candidates; runtime unavailable"),
            "tier1_candidate_tokens": sum(skill["tier1_tokens"] for skill in discoverable),
        }
    return instances
