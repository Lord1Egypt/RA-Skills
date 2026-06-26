# Software Playbooks

## Reliability and Incident Reduction
System starters:
- Stock: unresolved incidents or service risk.
- Flows: incident creation, mitigation, prevention.
- Loops: fire-fighting loop (incident load -> context switching -> more incidents).

Leverage points:
- Rules: incident response policies, SLO error budgets.
- Information flows: real-time telemetry and clear ownership.
- Structure: isolation boundaries and bulkheads.

Argument outline:
- Answer: enforce SLO policy and remove the amplification loop.
- Support 1: reactive work is driving future incidents.
- Support 2: feedback signals are late or unclear.
- Support 3: structural isolation reduces blast radius.

## Performance and Scaling
System starters:
- Stock: queued requests and pending work.
- Flows: arrival rate, processing rate, retries.
- Loops: retry amplification under latency spikes.

Leverage points:
- Rules: retry limits, backpressure, rate limiting.
- Information flows: load-aware routing.
- Structure: autoscaling thresholds and capacity buffers.

Argument outline:
- Answer: reduce amplification and shorten response delay.
- Support 1: retry loop is dominant during peak.
- Support 2: autoscaling lag drives overshoot.
- Support 3: policy changes stabilize the queue.

## Delivery Throughput and Backlog
System starters:
- Stock: WIP and backlog.
- Flows: intake, completion, rework.
- Loops: rework loop (defects -> rework -> delays -> more defects).

Leverage points:
- Buffers: WIP limits and queue design.
- Rules: intake throttles, definition of done.
- Information flows: visibility into bottlenecks.

Argument outline:
- Answer: cap intake and eliminate rework drivers.
- Support 1: system is over capacity.
- Support 2: quality defects dominate delay.
- Support 3: small rule changes produce stable flow.

## Data Quality and Pipeline Stability
System starters:
- Stock: trusted datasets and data freshness.
- Flows: ingestion, validation, correction.
- Loops: silent failure loop (bad data -> bad decisions -> more bad data).

Leverage points:
- Information flows: data lineage and freshness alerts.
- Rules: validation gates and schema contracts.
- Structure: isolation between raw and curated layers.

Argument outline:
- Answer: enforce contracts and improve observability.
- Support 1: data errors are undetected too long.
- Support 2: weak gates allow error propagation.
- Support 3: structure isolates blast radius.

## Technical Debt and Architecture Migration
System starters:
- Stock: legacy code and migration backlog.
- Flows: new features, refactoring, deprecation.
- Loops: feature pressure loop (shortcuts -> debt -> slower delivery -> more shortcuts).

Leverage points:
- Goals: prioritize long-term capability over short-term output.
- Rules: architecture decision records and migration budgets.
- Information flows: dependency mapping and cost of delay.

Argument outline:
- Answer: fund a phased migration with guardrails.
- Support 1: debt is the dominant drag on delivery.
- Support 2: ungoverned changes increase coupling.
- Support 3: staged migration reduces risk and preserves velocity.

## Developer Productivity and Platform Health
System starters:
- Stock: developer time and platform reliability.
- Flows: build time, deploy time, support load.
- Loops: tooling pain loop (slow tools -> context switching -> slower delivery).

Leverage points:
- Information flows: time-to-merge and build metrics.
- Rules: platform reliability targets and support SLAs.
- Structure: shared services and self-service tooling.

Argument outline:
- Answer: invest in platform stability and self-service.
- Support 1: tooling latency dominates cycle time.
- Support 2: support load steals engineering capacity.
- Support 3: self-service reduces recurring toil.

## Security Risk Reduction
System starters:
- Stock: unresolved vulnerabilities and risky dependencies.
- Flows: vulnerability discovery, remediation, new exposure.
- Loops: patch delay loop (backlog -> missed windows -> more backlog).

Leverage points:
- Rules: security SLAs and dependency policies.
- Information flows: asset inventory and risk scoring.
- Structure: segmentation and least-privilege controls.

Argument outline:
- Answer: enforce remediation rules and shrink exposure.
- Support 1: backlog growth is structural, not random.
- Support 2: weak visibility hides high-risk assets.
- Support 3: segmentation limits impact of failures.

## Product Adoption and Retention
System starters:
- Stock: active users.
- Flows: signups, activations, churn, reactivations.
- Loops: activation loop (better onboarding -> higher activation -> referrals).

Leverage points:
- Information flows: activation analytics and cohort visibility.
- Rules: trial-to-paid gates and feature limits.
- Goals: optimize for retention over raw acquisition.

Argument outline:
- Answer: focus on activation and value realization.
- Support 1: activation drop-off drives churn.
- Support 2: promise mismatch increases dissatisfaction.
- Support 3: targeted interventions outperform broad acquisition spend.
