# Advanced Configuration — Self-Smarter-Everyday

## Overview

This guide covers advanced configuration options for the self-smarter-everyday skill. These settings are intended for users who have already completed the basic setup and have at least one week of operational data. Advanced configuration allows you to customize every aspect of the self-improvement pipeline, from the specific prompts used during reflection to the mathematical formulas used for evaluating prompt fitness. Each section includes the configuration syntax, an explanation of the underlying mechanics, and practical guidance on when to adjust each parameter.

## Custom Reflection Prompts

The default reflection prompt covers general performance areas, but you can create domain-specific reflection prompts that focus on the aspects of performance that matter most to your agent's role. To create a custom reflection prompt, add a new file to `~/self-smarter-everyday/prompts/` with a descriptive name such as `customer-support-reflection.md`. The prompt file should contain a Jinja2 template that receives context variables from the nightly routine. Available variables include `{{ task_summary }}` for the day's task list, `{{ error_log }}` for errors encountered, `{{ memory_stats }}` for memory tier statistics, and `{{ previous_reflection }}` for the prior day's reflection text.

Here is an example custom reflection prompt designed for a customer support agent. The prompt instructs the agent to analyze interaction quality, identify recurring customer issues, evaluate response empathy and accuracy, and flag knowledge gaps that were exposed during customer interactions. The prompt also asks the agent to rate its own performance on a scale from one to ten across five dimensions: accuracy, empathy, resolution speed, knowledge coverage, and customer satisfaction signals.

```markdown
# Nightly Reflection — Customer Support Agent

## Context
Date: {{ date }}
Tasks handled: {{ task_summary | length }}
Errors encountered: {{ error_log | length }}

## Reflection Instructions

Analyze today's performance across these dimensions:

### 1. Interaction Quality
Review each customer interaction from today. For each interaction, consider:
- Was the customer's actual problem identified correctly?
- Was the response accurate and complete?
- Did the tone match the customer's emotional state?
- Was the resolution achieved in a reasonable number of exchanges?

### 2. Recurring Issues
Identify patterns in customer questions. Are there topics that came up
repeatedly? These represent either product issues that need escalation
or knowledge gaps that need documentation updates.

### 3. Knowledge Gaps
List every instance where you were uncertain about an answer or had to
defer to another source. Each gap should be documented with:
- The topic area
- Why the knowledge was missing
- Suggested source for filling the gap
- Priority (high/medium/low)

### 4. Performance Self-Rating
Rate yourself 1-10 on each dimension:
- Accuracy: {{ accuracy_rating }}/10
- Empathy: {{ empathy_rating }}/10
- Resolution Speed: {{ speed_rating }}/10
- Knowledge Coverage: {{ coverage_rating }}/10
- Customer Satisfaction: {{ satisfaction_rating }}/10

### 5. Tomorrow's Focus
Based on today's reflection, identify the top three areas to focus on
improving tomorrow. Be specific — not "be better at responses" but
"reduce average resolution time for billing questions by checking the
billing FAQ before responding."
```

To activate a custom prompt, update the configuration file to reference it: set `reflection.prompt_template` to the filename without the extension, such as `customer-support-reflection`. The nightly routine automatically loads the template from the prompts directory and renders it with the current day's context variables before passing it to the reflection phase.

## Multi-Tier Memory Tuning

The three-tier memory system (HOT, WARM, COLD) can be finely tuned to match your agent's access patterns. The default configuration works well for general-purpose agents, but specialized agents may benefit from adjusted tier sizes and promotion/demotion thresholds.

The promotion algorithm uses an access frequency score combined with a recency decay factor. Each memory entry has an access count and a last-accessed timestamp. The composite score is calculated as `score = access_count * recency_decay`, where `recency_decay = exp(-lambda * days_since_access)`. The lambda parameter controls how quickly old accesses lose relevance. A higher lambda means only very recent accesses matter; a lower lambda gives more weight to historical access patterns.

```json
{
  "memory": {
    "hot_limit": 30,
    "warm_limit": 150,
    "cold_archive_path": "~/self-smarter-everyday/memory/cold/",
    "promotion_threshold": 0.85,
    "demotion_threshold": 0.25,
    "recency_lambda": 0.05,
    "merge_similarity_threshold": 0.9,
    "compaction_strategy": "score_based",
    "semantic_dedup": true,
    "semantic_model": "local-embeddings"
  }
}
```

The `merge_similarity_threshold` controls when two memory entries are considered similar enough to merge. A threshold of 0.9 means entries must be 90 percent similar in semantic space before merging is attempted. Lower this to 0.8 for more aggressive compaction, or raise it to 0.95 for conservative merging that preserves more distinct entries. The `semantic_dedup` flag enables embedding-based deduplication, which catches semantically similar entries that exact string matching would miss. This requires a local embeddings model, which is bundled with the skill.

## Custom Evaluation Metrics

Beyond the built-in metrics (response quality, token efficiency, error rate, memory utilization), you can define custom metrics that track aspects of performance specific to your domain. Custom metrics are defined in the configuration under the `audit.custom_metrics` array.

Each metric definition includes a name, a description, a data source, a calculation formula, and a target range. The data source can be a log file pattern, a database query, or a computed value from other metrics. The formula uses a simple expression language that supports basic arithmetic, aggregation functions like mean and percentile, and comparison operators.

```json
{
  "audit": {
    "custom_metrics": [
      {
        "name": "first_response_time",
        "description": "Time from user message to first agent response",
        "source": "interaction_log",
        "filter": "event_type == 'message_received'",
        "formula": "percentile(values, 50)",
        "unit": "seconds",
        "target_range": [0, 30],
        "weight": 0.2
      },
      {
        "name": "knowledge_reuse_rate",
        "description": "Percentage of responses that reused cached knowledge",
        "source": "memory_access_log",
        "filter": "access_type == 'cache_hit'",
        "formula": "hits / (hits + misses) * 100",
        "unit": "percent",
        "target_range": [60, 100],
        "weight": 0.15
      },
      {
        "name": "escalation_rate",
        "description": "Percentage of tasks escalated to human or higher-tier agent",
        "source": "task_log",
        "filter": "outcome == 'escalated'",
        "formula": "escalated / total * 100",
        "unit": "percent",
        "target_range": [0, 10],
        "weight": 0.15
      }
    ]
  }
}
```

Custom metrics are included in the nightly audit report and contribute to the composite improvement score based on their assigned weights. The weights are normalized automatically, so they do not need to sum to one.

## Skill Evolution Rules

The skill gap analysis phase can be configured with custom rules that define how the agent should respond to identified gaps. By default, the system suggests installing available skills from the registry. You can override this behavior with custom evolution rules that specify different actions based on the gap category.

```json
{
  "skill_gap_analysis": {
    "evolution_rules": [
      {
        "category": "data_processing",
        "action": "suggest_skill",
        "priority": "high",
        "preferred_sources": ["clawhub", "github"]
      },
      {
        "category": "communication",
        "action": "internal_improvement",
        "method": "prompt_augmentation",
        "description": "Add communication patterns to prompt templates"
      },
      {
        "category": "domain_knowledge",
        "action": "memory_injection",
        "method": "seed_memory",
        "source_path": "~/self-smarter-everyday/knowledge-base/"
      }
    ]
  }
}
```

## Prompt Mutation Strategies

Prompt evolution uses mutation strategies to generate variant prompts for fitness testing. The default strategy applies random word substitutions and structural rearrangements. You can define custom mutation strategies that are more targeted.

Available built-in strategies include `synonym_swap` which replaces words with synonyms from a built-in thesaurus, `constraint_add` which adds new constraints to the prompt, `constraint_relax` which removes overly restrictive constraints, `example_inject` which adds new few-shot examples, `example_prune` which removes low-performing examples, and `structure_shuffle` which reorders sections of the prompt. You can combine multiple strategies in a pipeline:

```json
{
  "prompt_evolution": {
    "strategies": ["synonym_swap", "constraint_add", "example_inject"],
    "pipeline_order": "sequential",
    "mutations_per_generation": 5,
    "survival_rate": 0.4,
    "elitism_count": 2
  }
}
```

The `survival_rate` controls what fraction of mutated variants are kept for the next generation. A rate of 0.4 means only the top 40 percent of variants survive. The `elitism_count` ensures that the best-performing variants from the previous generation are always preserved regardless of the survival rate, preventing regression.

## Integration with External Monitoring

For production deployments, you may want to integrate self-smarter-everyday with external monitoring and alerting systems. The skill supports webhook notifications, metrics export in Prometheus format, and structured JSON logging for ingestion by log aggregation systems.

```json
{
  "integrations": {
    "webhook": {
      "enabled": true,
      "url": "https://your-monitoring-system.example.com/webhooks/self-smarter",
      "events": ["imvement_plan_created", "alert_threshold_exceeded", "prompt_rolled_back"],
      "headers": {
        "Authorization": "Bearer YOUR_WEBHOOK_TOKEN"
      }
    },
    "prometheus": {
      "enabled": true,
      "port": 9090,
      "path": "/metrics",
      "prefix": "self_smarter_"
    },
    "json_logging": {
      "enabled": true,
      "output_path": "~/self-smarter-everyday/logs/structured.jsonl",
      "fields": ["timestamp", "phase", "metric_name", "value", "delta"]
    }
  }
}
```

The Prometheus integration exposes all metrics with the configured prefix, allowing you to build dashboards and alerting rules in Grafana or compatible tools. The webhook integration sends structured JSON payloads to your monitoring system whenever significant events occur. The JSON logging mode writes one JSON object per line to the specified file, making it easy to ingest with tools like Filebeat, Fluentd, or Logstash.

## Performance Considerations

Advanced configurations can increase the runtime of the nightly routine. Semantic deduplication with embeddings adds approximately thirty seconds to the memory compaction phase. Custom metrics with complex formulas may add ten to twenty seconds to the audit phase. Prompt evolution with multiple mutation strategies and large survival rates can add one to two minutes if many variants need fitness evaluation. Plan your cron schedule accordingly, and monitor the log file for phase durations. If the routine is taking too long, consider disabling expensive features like semantic deduplication on weeknights and running them only on weekends.
