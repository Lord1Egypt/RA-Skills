"""Pure assembly of the stable public Skill Vitals JSON report."""

from .analysis import (
    build_budget,
    build_conflicts,
    build_host_summaries,
    build_openclaw_instances,
    build_security,
    build_structure,
    build_trigger,
    select_scope,
)


def _under_home(home_n, relative):
    return home_n.rstrip("/") + "/" + relative.lstrip("/")


def build_report(inventory, *, host, include_all, budget, codex_fallback_budget,
                 zombie_age, split_threshold, schema_version, home_n):
    """Return the complete unredacted report without performing any I/O."""
    skills = inventory["skills"]
    usage = inventory["usage"]
    codex_runtime = inventory["codex_runtime"]
    openclaw_runtime = inventory["openclaw_runtime"]
    loaded, candidates, by_key = select_scope(skills, include_all)
    unique = list(by_key.values())
    tier1_total = sum(group[0]["tier1_tokens"] for group in unique)
    budget_report = build_budget(
        unique, host, include_all, budget, codex_fallback_budget)
    trigger_report = build_trigger(loaded, usage, host, zombie_age)
    structure_report = build_structure(candidates, loaded, split_threshold)
    security_report = build_security(skills)
    workbuddy_roots = inventory["workbuddy_roots"]

    return {
        "schema_version": schema_version,
        "scanned_roots": inventory["scanned_roots"],
        "host_selection": host,
        "host_summaries": build_host_summaries(
            skills, usage, codex_runtime, openclaw_runtime),
        "openclaw_runtime": openclaw_runtime,
        "unreadable_skills": inventory["unreadable_skills"],
        "total_skills_on_disk": len(skills),
        "loaded_skills": len(loaded),
        "unique_skills": len(unique),
        "plugin_state": {
            "host_config_read": inventory["plugins_known"],
            "enabled_plugins": sorted(inventory["enabled_plugins"] or ()),
            "note": "Disabled plugin copies remain on disk but do not enter context or count toward the budget. "
                    "When host_config_read=false, plugin state is unknown and copies are treated as not loaded.",
        },
        "codex_runtime": {
            "available": codex_runtime["available"],
            "source": codex_runtime["source"],
            "cwd": codex_runtime.get("cwd"),
            "catalog_skills": len(codex_runtime.get("skills", [])),
            "errors": codex_runtime["errors"],
            "note": "When available=true, Codex discovery, scope, enabled state, interface, and dependencies "
                    "come from the official app-server. No public per-skill trigger-count API is available.",
        },
        "workbuddy_discovery": {
            "source": "manifest-selected top-level packages resolved in plugins/cache/workbuddy-builtin",
            "user_root": _under_home(home_n, ".workbuddy/skills"),
            "builtin_root": _under_home(
                home_n, ".workbuddy/plugins/marketplaces/workbuddy-builtin"),
            "cache_root": _under_home(
                home_n, ".workbuddy/plugins/cache/workbuddy-builtin"),
            "excluded_roots": ["~/.workbuddy/connectors-marketplace (catalog only)",
                               "non-top-level builtin-plugin content such as role definitions under experts/"],
            "welcome_mode": inventory["workbuddy_mode"],
            "orphaned_packages": sorted(inventory["workbuddy_orphaned"]),
            "top_level_manifest_packages": len({
                metadata.get("workbuddy_package") for _, metadata in workbuddy_roots
                if metadata.get("workbuddy_package")}),
            "skill_roots_from_manifest": len(workbuddy_roots),
            "enabled_state": "mode-filtered manifest evidence; no public per-skill runtime API",
            "trigger_data": "not-available",
        },
        "openclaw_instances": build_openclaw_instances(skills, openclaw_runtime),
        "description_budget": budget_report,
        "trigger_data": trigger_report,
        "structure": structure_report,
        "security": security_report,
        "tier1_total_tokens": tier1_total,
        "tier1_pct_of_200k": round(tier1_total / 200000 * 100, 2),
        "conflicts": build_conflicts(by_key),
        "precedence_note": "Overrides are compared only within one host. Claude Code: enterprise > personal > "
                           "project > plugin; OpenClaw: workspace > project > personal > managed. Plugin skills "
                           "are isolated by <plugin>:<name>, so equal bare names are not conflicts.",
        "cross_host_note": "Hosts do not share context. Use host_summaries or --host for one runtime; do not "
                           "interpret top-level Tier1 or description-budget values as a cross-host total.",
        "skills": sorted(skills, key=lambda skill: (not skill["loaded"],
                                                    -skill["tier1_tokens"])),
    }
