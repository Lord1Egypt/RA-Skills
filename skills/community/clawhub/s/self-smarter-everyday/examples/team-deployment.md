# Team Deployment — Self-Smarter-Everyday

## Overview

This guide covers deploying the self-smarter-everyday skill across a team of multiple agents that operate in coordination. Team deployment introduces several new considerations beyond single-agent setup: shared memory spaces where agents can learn from each other's experiences, coordinated improvement schedules that prevent conflicting changes, conflict resolution mechanisms for when agents propose contradictory improvements, centralized monitoring dashboards for oversight, per-agent customization that allows each agent to specialize while still benefiting from team-wide insights, and team-wide metrics that measure collective improvement rather than individual agent performance. This guide assumes you have already deployed self-smarter-everyday on at least one agent using the basic setup guide.

## Architecture Overview

A team deployment consists of a shared coordination directory, individual agent workspaces, and a centralized monitoring hub. The shared directory lives at `~/self-smarter-team/` and contains shared memory, team-wide configuration, conflict resolution logs, and aggregated reports. Each agent maintains its own workspace at `~/self-smarter-everyday/` as in the single-agent setup, but with additional configuration that links it to the team coordination layer. The monitoring hub is a lightweight web dashboard that aggregates metrics from all team members and provides a unified view of team health and improvement trajectory.

## Shared Memory Configuration

The shared memory system allows agents to contribute insights to a common knowledge base. When one agent discovers a better approach to a task, that insight can be promoted to shared memory where all team members can access it. The shared memory uses the same three-tier structure as individual agent memory, but with an additional layer of access control.

```json
{
  "team": {
    "shared_memory": {
      "enabled": true,
      "path": "~/self-smarter-team/shared-memory/",
      "contribution_policy": "review_required",
      "auto_promote_threshold": 0.95,
      "access_control": {
        "read": "all_team_members",
        "write": "all_team_members",
        "promote_to_shared": "coordinator_only"
      },
      "categories": [
        "error_recovery",
        "task_patterns",
        "domain_knowledge",
        "communication_templates",
        "tool_usage"
      ],
      "max_shared_entries": 500,
      "ttl_days": 90
    }
  }
}
```

The `contribution_policy` setting controls how entries enter shared memory. With `review_required`, any agent can propose an entry, but it must be reviewed by the coordinator agent before becoming accessible to the team. With `auto_contribute`, entries that exceed the `auto_promote_threshold` confidence score are immediately available to all team members. The coordinator-only promotion model is safest for production environments where incorrect shared knowledge could cause widespread issues.

## Coordinated Improvement Schedule

When multiple agents run their nightly routines simultaneously, they can interfere with each other by modifying shared resources concurrently. The coordinated schedule staggers agent runs and implements locking on shared resources.

```json
{
  "team": {
    "schedule": {
      "coordination_mode": "staggered",
      "agents": [
        {"name": "agent-alpha", "run_time": "02:00", "priority": 1},
        {"name": "agent-beta", "run_time": "02:15", "priority": 2},
        {"name": "agent-gamma", "run_time": "02:30", "priority": 3},
        {"name": "agent-delta", "run_time": "02:45", "priority": 4}
      ],
      "lock_timeout_minutes": 10,
      "shared_resource_lock": "file_based",
      "conflict_detection": "semantic"
    }
  }
}
```

The staggered mode ensures that each agent starts its nightly routine fifteen minutes after the previous one. This prevents file locking conflicts on shared memory files. The priority field determines the order of access to shared resources when two agents need to write simultaneously. The coordinator agent (priority 1) always has first access. The `conflict_detection` setting uses semantic comparison to identify when two agents propose contradictory improvements, such as one agent suggesting a prompt change that another agent's data shows would be detrimental.

## Conflict Resolution Between Agents

Conflicts arise when agents propose incompatible improvements. The conflict resolution system detects these situations and applies a resolution strategy automatically. There are three types of conflicts: resource conflicts where two agents try to modify the same file, logic conflicts where agents propose contradictory behavioral changes, and metric conflicts where agents optimize for different objectives.

```json
{
  "team": {
    "conflict_resolution": {
      "strategy": "evidence_weighted",
      "methods": {
        "resource_conflict": "queue_with_priority",
        "logic_conflict": "evidence_weighted",
        "metric_conflict": "team_objective_alignment"
      },
      "escalation": {
        "auto_resolve_threshold": 0.8,
        "human_escalation": true,
        "escalation_webhook": "https://your-system.example.com/escalations"
      },
      "resolution_log": "~/self-smarter-team/conflict-log/"
    }
  }
}
```

The `evidence_weighted` strategy resolves logic conflicts by comparing the evidence supporting each agent's proposal. The agent with stronger supporting data (more data points, higher confidence scores, more recent observations) wins the conflict. The `team_objective_alignment` method resolves metric conflicts by evaluating which proposal better aligns with the team-wide objectives defined in the team configuration. When the confidence of either side exceeds the `auto_resolve_threshold`, the conflict is resolved automatically. Otherwise, it is escalated to a human operator via the configured webhook.

## Centralized Monitoring

The monitoring hub provides a unified dashboard for observing the health and improvement trajectory of all team members. The hub reads from each agent's report directory and the shared team directory to produce aggregated views.

```json
{
  "team": {
    "monitoring": {
      "enabled": true,
      "hub_path": "~/self-smarter-team/monitoring/",
      "refresh_interval_minutes": 60,
      "dashboard": {
        "type": "markdown",
        "output_path": "~/self-smarter-team/monitoring/dashboard.md",
        "sections": [
          "team_health_summary",
          "individual_agent_status",
          "shared_memory_stats",
          "conflict_summary",
          "improvement_trajectory",
          "alerts_and_anomalies"
        ]
      },
      "alerts": {
        "enabled": true,
        "channels": ["webhook", "file_log"],
        "rules": [
          {
            "name": "agent_degradation",
            "condition": "composite_score_delta < -0.1",
            "window_days": 3,
            "severity": "warning"
          },
          {
            "name": "shared_memory_overflow",
            "condition": "shared_entries > max_shared_entries * 0.9",
            "severity": "info"
          },
          {
            "name": "conflict_spike",
            "condition": "conflicts_per_day > 5",
            "severity": "warning"
          }
        ]
      }
    }
  }
}
```

The dashboard is generated as a markdown file that can be viewed directly or converted to HTML for web serving. It includes a team health summary showing the average composite score across all agents, individual agent status cards showing each agent's current metrics and trend direction, shared memory statistics showing utilization and recent contributions, a conflict summary listing recent conflicts and their resolutions, an improvement trajectory chart rendered in ASCII or Mermaid format, and an alerts section highlighting any active warnings or anomalies.

## Per-Agent Customization

While agents share a team configuration for coordination settings, each agent maintains its own specialized configuration for its improvement routine. This allows agents to specialize in different areas while still participating in the team improvement process.

```json
{
  "agent_profile": {
    "name": "agent-alpha",
    "role": "customer_support",
    "specialization": {
      "focus_metrics": ["response_quality", "customer_satisfaction", "resolution_time"],
      "reflection_focus": ["interaction_patterns", "knowledge_gaps", "empathy_accuracy"],
      "skill_priorities": ["communication", "domain_knowledge", "tool_usage"],
      "prompt_evolution_scope": ["system_prompt", "response_templates", "escalation_criteria"]
    },
    "team_contribution": {
      "share_all_insights": false,
      "share_categories": ["error_recovery", "communication_templates"],
      "contribution_frequency": "daily"
    }
  }
}
```

The specialization block defines which metrics, reflection areas, skills, and prompt scopes this particular agent focuses on. The team contribution block controls what insights this agent shares with the team and how frequently. Setting `share_all_insights` to false and specifying categories allows you to control information flow — for example, a research agent might share domain knowledge but not communication templates, while a support agent does the opposite.

## Team-Wide Metrics

Team-wide metrics aggregate individual agent metrics into collective measurements that reflect the team's overall improvement trajectory. These metrics are computed during the coordinator agent's nightly run after all other agents have completed their routines.

The key team-wide metrics include: collective composite score which is the weighted average of all agent composite scores with weights proportional to each agent's task volume, knowledge sharing ratio which measures how effectively insights flow between agents, conflict resolution rate which tracks the percentage of conflicts resolved automatically versus escalated, improvement velocity which measures the rate of meaningful improvements across the team per week, and redundancy detection which identifies when multiple agents are learning the same lesson independently instead of sharing.

```json
{
  "team": {
    "metrics": {
      "collective_composite": {
        "weighting": "task_volume_proportional",
        "target_improvement_per_week": 0.02
      },
      "knowledge_sharing": {
        "target_ratio": 0.6,
        "measurement": "shared_contributions / total_new_insights"
      },
      "improvement_velocity": {
        "unit": "improvements_per_week",
        "target": 5,
        "minimum": 2
      }
    }
  }
}
```

## Deployment Checklist

Before going live with a team deployment, verify the following items. First, ensure all agents have completed at least one week of individual operation before linking them into a team. This prevents unstable agents from contaminating shared memory. Second, verify that file permissions allow all agent processes to read and write to the shared directory. Third, test the staggered schedule with dry-run mode on all agents to confirm there are no timing conflicts. Fourth, run the conflict resolution system in log-only mode for the first three days to observe what kinds of conflicts arise before enabling automatic resolution. Fifth, set up the monitoring dashboard and verify it is updating correctly after the first coordinated nightly run. Finally, establish a weekly review cadence where a human operator reviews the team dashboard, examines escalated conflicts, and adjusts team-wide objectives as needed.

## Scaling Considerations

The team deployment model scales well up to approximately ten agents with the file-based coordination approach described here. Beyond ten agents, consider switching to a database-backed coordination layer for shared memory and conflict resolution. The skill's architecture is designed to support pluggable coordination backends through the `team.coordination_backend` configuration key. Supported backends include `file` for the default file-based approach, `sqlite` for single-host multi-agent deployments, and `redis` for distributed multi-host deployments. Each backend provides the same interface but with different performance characteristics and concurrency guarantees.
