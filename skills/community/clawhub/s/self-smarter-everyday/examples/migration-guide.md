# Migration Guide — From Self-Improving to Self-Smarter-Everyday

## Overview

This guide provides a comprehensive walkthrough for migrating from the existing self-improving skill to the self-smarter-everyday skill. The new skill is a complete redesign that addresses limitations in the original architecture while maintaining backward compatibility with existing data formats where possible. This guide covers what changes, what stays the same, step-by-step migration procedures, data migration strategies, configuration mapping from old format to new format, rollback procedures if the migration does not go as planned, and compatibility notes for hybrid operation during the transition period. The migration is designed to be non-destructive — your existing self-improving data is preserved throughout the process, and you can roll back at any point before completing the final cutover.

## What's New in Self-Smarter-Everyday

The self-smarter-everyday skill introduces several architectural improvements over the original self-improving skill. Understanding these changes helps you map your existing configuration and expectations to the new system.

The first major change is the three-tier memory system. The original self-improving skill used a flat memory file where all patterns were stored with equal priority. The new skill introduces HOT, WARM, and COLD tiers with automatic promotion and demotion based on access frequency and recency. This means frequently-used patterns are always quickly accessible while rarely-used patterns are archived but preserved. Your existing memory entries will be migrated into the appropriate tier based on their access frequency metadata.

The second major change is the prompt evolution engine. The original skill had a basic prompt update mechanism that replaced prompts wholesale based on reflection output. The new skill uses a genetic algorithm approach where multiple prompt variants are generated, evaluated for fitness, and the best performers are selected for the next generation. This produces more stable and measurable prompt improvements over time. Your existing prompts are preserved as the initial generation in the new system.

The third major change is the structured nightly routine. The original skill ran improvement as a single monolithic process. The new skill breaks the nightly routine into six distinct phases: reflection, self-audit, memory compaction, prompt evolution, skill gap analysis, and improvement planning. Each phase produces its own output and can be configured, enabled, or disabled independently. This gives you much finer control over the improvement process.

The fourth major change is the custom metrics framework. The original skill tracked a fixed set of metrics. The new skill allows you to define arbitrary custom metrics with custom data sources, formulas, and alerting thresholds. This enables domain-specific improvement tracking that was not possible in the original system.

## What Stays the Same

Several aspects of the original self-improving skill are preserved in the new system to minimize migration friction. The core improvement loop of observe, reflect, plan, act, verify remains the same. The file-based storage approach is maintained — no external database is required. The markdown report format is preserved for human readability. The cron-based scheduling mechanism is unchanged. The skill's integration points with the parent agent remain compatible — the nightly routine is still triggered the same way and produces output in the same location structure.

## Pre-Migration Checklist

Before starting the migration, complete the following checklist. First, ensure you are running self-improving skill version 2.0 or later. If you are running an earlier version, upgrade to 2.0 first and run at least one nightly cycle to ensure your data is in the expected format. Second, back up your entire self-improving directory by copying it to a safe location: `cp -r ~/self-improving/ ~/self-improving-backup-$(date +%Y%m%d)/`. Third, verify that you have at least 100MB of free disk space for the new skill's data structures. Fourth, review your current configuration file and note any custom settings you have made — these will need to be mapped to the new configuration format. Fifth, ensure no nightly routine is currently running by checking for active processes: `ps aux | grep nightly_routine`.

## Migration Steps

### Step 1: Install the New Skill

Install self-smarter-everyday alongside the existing self-improving skill. Do not remove the old skill yet — both will run in parallel during the transition period. Copy the new skill to your skills directory: `cp -r self-smarter-everyday/ ~/.openclaw/workspace/skills/self-smarter-everyday/`. Verify installation with `openclaw skills list`.

### Step 2: Create the New Directory Structure

Run the setup script to create the new directory structure: `bash ~/.openclaw/workspace/skills/self-smarter-everyday/scripts/setup.sh`. This creates `~/self-smarter-everyday/` with all required subdirectories. The old `~/self-improving/` directory remains untouched.

### Step 3: Migrate Configuration

Map your old configuration to the new format. The configuration mapping tool automates this process: `python3 scripts/migrate_config.py --input ~/self-improving/config.json --output ~/self-smarter-everyday/config.json`. The mapping tool reads your old configuration, translates each setting to the equivalent new-format setting, and writes the result. Settings that have no direct equivalent are documented in the migration log for manual review.

Here is the complete configuration mapping table showing how each old setting maps to the new format:

| Old Setting | New Setting | Notes |
|-------------|-------------|-------|
| `reflection_time` | `schedule.nightly_run` | Format changed from `2:00` to cron `0 2 * * *` |
| `memory_file` | `memory.hot_path` + `memory.warm_path` | Split into tiers |
| `max_memory_entries` | `memory.hot_limit` + `memory.warm_limit` | Distributed across tiers |
| `prompt_path` | `prompt_evolution.base_prompt_path` | Same, nested under prompt_evolution |
| `report_path` | `reporting.output_path` | Same concept, new location |
| `improvement_threshold` | `audit.alert_threshold` | Semantics slightly different |
| `log_level` | `logging.level` | Direct mapping |
| `custom_prompts` | `reflection.prompt_template` | Now a template reference |
| N/A | `memory.cold_archive_path` | New in self-smarter |
| N/A | `prompt_evolution.mutation_rate` | New in self-smarter |
| N/A | `audit.custom_metrics` | New in self-smarter |
| N/A | `skill_gap_analysis` | New in self-smarter |

### Step 4: Migrate Memory Data

The memory migration tool reads your existing flat memory file and distributes entries across the three tiers based on access frequency metadata. Run: `python3 scripts/migrate_memory.py --input ~/self-improving/memory.json --output-dir ~/self-smarter-everyday/memory/`. The tool analyzes each entry's `access_count` and `last_accessed` fields to determine tier placement. Entries with high access counts and recent access dates go to HOT. Entries with moderate access go to WARM. Everything else goes to COLD. If your old memory file lacks access metadata, all entries default to WARM tier, and the compaction phase will sort them out over the first few nightly cycles.

### Step 5: Migrate Prompt History

If you have prompt version history from the old skill, migrate it to seed the new prompt evolution engine: `python3 scripts/migrate_prompts.py --input ~/self-improving/prompts/ --output-dir ~/self-smarter-everyday/prompts/versions/`. This preserves your prompt evolution history so the new system can build on it rather than starting from scratch.

### Step 6: Parallel Operation Period

Run both skills in parallel for seven days. During this period, the old self-improving skill continues its nightly routine as before, and the new self-smarter-everyday skill runs its routine independently. Compare the reports from both systems to verify that the new system is producing sensible output. The reports directory for the new skill is at `~/self-smarter-everyday/reports/`. Check that memory tiers are populating correctly, that prompt evolution is generating variants, and that the improvement plan is producing actionable items.

### Step 7: Cutover

After seven days of successful parallel operation, disable the old skill's cron job and make the new skill the sole improvement system. Remove the old cron entry: `crontab -e` and delete the self-improving nightly line. The new skill's cron job should already be active from the setup script. Do not delete the old skill files or data yet — keep them as a fallback for at least thirty days.

## Rollback Procedure

If the migration does not go as planned, rollback is straightforward at any stage. During the parallel operation period, simply re-enable the old skill's cron job and disable the new one. The old skill's data was never modified — it continued running independently throughout the transition. If you have already completed the cutover and need to roll back, restore the old cron job, copy the backup directory back if needed: `cp -r ~/self-improving-backup-YYYYMMDD/ ~/self-improving/`, and verify the old nightly routine runs successfully. The new skill's data in `~/self-smarter-everyday/` can be archived or deleted at your discretion — it has no impact on the old skill.

## Compatibility Notes

During the transition period, be aware of these compatibility considerations. Both skills write to separate directories and do not interfere with each other's data. However, if both skills are configured to modify the same agent prompts, there is a risk of conflicting changes. To avoid this, configure the new skill's prompt evolution to operate on a copy of the prompts during the parallel period, not the live prompts. Set `prompt_evolution.live_mode` to `false` in the new skill's configuration during parallel operation. Switch to `true` only after cutover is complete.

The new skill reads interaction logs from the same location as the old skill if configured to do so. Set `data_collection.interaction_log.source_path` to point to the old skill's log directory if you want the new skill to have access to historical interaction data. This is optional — the new skill can start collecting its own interaction data from scratch.

## Post-Migration Verification

After completing the migration and cutover, verify the following. Check that the nightly routine runs successfully for three consecutive nights by reviewing the log file. Verify that memory tiers are populating with appropriate entries by examining the memory directory. Confirm that prompt evolution is generating and evaluating variants by checking the prompt versions directory. Review the improvement reports for actionability and relevance. Finally, compare the new skill's composite score trajectory against the old skill's historical scores to ensure continuity in improvement measurement.
