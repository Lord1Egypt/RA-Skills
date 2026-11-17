# Basic Setup — Self-Smarter-Everyday

## Overview

This guide walks you through setting up the self-smarter-everyday skill for a basic agent deployment. By the end of this walkthrough, your agent will have a fully functional nightly self-improvement routine that runs automatically, generates improvement reports, and evolves its behavior over time. The entire setup process takes approximately 15 minutes and requires no external dependencies beyond the base OpenClaw installation.

## Prerequisites

Before beginning, ensure you have the following in place. First, you need a running OpenClaw instance with at least one agent configured. Second, you should have file system access to the agent workspace directory. Third, you need permissions to create cron jobs on the host system. Finally, ensure you have at least 50MB of free disk space for memory storage and logs. No external API keys or services are required for the basic setup — everything runs locally using file-based state management.

## Step 1: Install the Skill

Begin by copying the self-smarter-everyday skill into your workspace skills directory. The skill lives at `~/.openclaw/workspace/skills/self-smarter-everyday/`. If you are installing from the skill registry, use the command `openclaw skills install self-smarter-everyday`. If you are installing manually from a repository, clone the repository into your skills directory and verify that the SKILL.md file is present at the root of the skill folder. After installation, verify the skill is recognized by running `openclaw skills list` and confirming that self-smarter-everyday appears in the output with a status of active.

## Step 2: Create the Initial Configuration

The configuration file lives at `~/self-smarter-everyday/config.json`. Create the directory structure first by running `mkdir -p ~/self-smarter-everyday/{memory,logs,reports,prompts,skills-audit}`. Then create the configuration file with the following content. The configuration uses sensible defaults that work for most agents. The key settings include the reflection time (default 2 AM local time), the memory tier sizes (HOT holds 50 entries, WARM holds 200, COLD is unlimited), and the improvement threshold (the minimum score change before triggering an improvement action).

```json
{
  "version": "1.0.0",
  "agent_name": "my-agent",
  "schedule": {
    "nightly_run": "0 2 * * *",
    "timezone": "UTC"
  },
  "memory": {
    "hot_limit": 50,
    "warm_limit": 200,
    "cold_archive_path": "~/self-smarter-everyday/memory/cold/",
    "promotion_threshold": 0.8,
    "demotion_threshold": 0.3
  },
  "reflection": {
    "prompt_template": "default",
    "max_tokens": 2000,
    "focus_areas": ["task_performance", "error_patterns", "knowledge_gaps"]
  },
  "audit": {
    "metrics": ["response_quality", "token_efficiency", "error_rate", "memory_utilization"],
    "baseline_periods": 7,
    "alert_threshold": 0.15
  },
  "prompt_evolution": {
    "enabled": true,
    "mutation_rate": 0.1,
    "max_versions": 10,
    "fitness_function": "composite_score"
  },
  "skill_gap_analysis": {
    "enabled": true,
    "check_available_skills": true,
    "suggest_new_skills": true
  },
  "reporting": {
    "output_path": "~/self-smarter-everyday/reports/",
    "retain_days": 30,
    "format": "markdown"
  }
}
```

## Step 3: Initialize Memory Tiers

The memory system uses three tiers inspired by human memory. HOT memory contains the 50 most frequently accessed and most recently reinforced patterns. These are the patterns your agent relies on constantly. WARM memory holds up to 200 patterns that are accessed moderately. COLD memory is the archive — patterns that are rarely accessed but preserved for reference. To initialize the memory tiers, run the setup script: `python3 scripts/setup.sh`. This creates the initial memory files with empty state and default seed patterns. The seed patterns include basic operational knowledge like common error recovery strategies, standard response formatting rules, and typical task decomposition approaches.

## Step 4: Configure the Nightly Cron Job

The nightly routine is the heart of self-smarter-everyday. It runs six phases in sequence: reflection, self-audit, memory compaction, prompt evolution, skill gap analysis, and improvement planning. The setup script creates a cron job automatically, but you can also configure it manually. Add the following to your crontab: `0 2 * * * cd ~/self-smarter-everyday && python3 scripts/nightly_routine.py --config config.json >> logs/nightly.log 2>&1`. This runs the routine at 2 AM every day. The routine typically completes in 3 to 5 minutes depending on the amount of accumulated data.

## Step 5: Run the First Nightly Cycle

For testing purposes, you can trigger the first run manually without waiting for the cron schedule. Execute: `python3 scripts/nightly_routine.py --config config.json --dry-run`. The dry-run mode simulates all six phases without writing any changes, so you can verify that everything is configured correctly. Review the output for any errors or warnings. Once you are satisfied, run without the dry-run flag: `python3 scripts/nightly_routine.py --config config.json`. This creates the first improvement report in the reports directory.

## Step 6: Review the First Improvement Report

After the first run, navigate to `~/self-smarter-everyday/reports/` and open the file named with today's date, such as `2026-08-10-improvement-report.md`. The report contains several sections. The Reflection Summary describes what the agent observed about its own performance during the day. The Self-Audit Results show quantitative metrics like response quality score, token efficiency ratio, and error rate. The Memory Health section shows how many entries are in each tier and any promotions or demotions that occurred. The Prompt Evolution section shows any prompt variants that were tested and their fitness scores. The Skill Gap Analysis identifies areas where the agent lacks capabilities. Finally, the Improvement Plan lists prioritized actions for the coming days.

## Step 7: Iterate and Tune

After the first week of operation, you will have enough data to start tuning the configuration. If the agent is generating too many low-value improvement suggestions, increase the improvement threshold from 0.1 to 0.2. If memory compaction is too aggressive and losing useful patterns, increase the demotion threshold from 0.3 to 0.4. If prompt evolution is not producing meaningful improvements, try adjusting the mutation rate from 0.1 to 0.15. The key is to observe the reports for at least seven days before making changes. Premature tuning based on insufficient data leads to suboptimal configurations.

## Expected Timeline

Here is what you can expect in the first month of operation. During week one, the system establishes baselines for all metrics. The first few reports may show large swings as the system calibrates. During week two, patterns begin to stabilize. The memory tiers start showing meaningful differentiation between HOT and WARM entries. During week three, prompt evolution begins producing measurable improvements in response quality. You should see a five to ten percent improvement in composite scores by the end of this week. During week four, the system enters steady-state operation. Improvements become incremental rather than dramatic. This is normal and healthy — the agent is now fine-tuning rather than overhauling.

## Troubleshooting Common Issues

If the nightly routine fails silently, check the log file at `~/self-smarter-everyday/logs/nightly.log` for error messages. The most common issue is incorrect file permissions on the memory directory. Ensure the agent user has read-write access to all subdirectories. If memory compaction produces empty tiers, verify that the agent is actually logging interactions during normal operation. The self-smarter system depends on interaction data to function. If no data flows in, there is nothing to improve upon. Consider adding interaction logging hooks to your agent's main loop if they are not already present. If prompt evolution produces degraded results, use the rollback feature to revert to the previous prompt version. The system keeps the last ten versions of each prompt, and you can restore any of them by copying the versioned file back to the active prompt path.

## Next Steps

Once your basic setup is running smoothly, consider exploring advanced configuration options. The advanced-config example covers custom reflection prompts, multi-tier memory tuning, custom evaluation metrics, and integration with external monitoring systems. You can also explore team deployment if you are running multiple agents that should share improvement insights.
