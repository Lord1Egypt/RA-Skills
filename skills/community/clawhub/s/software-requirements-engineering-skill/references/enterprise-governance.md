# Enterprise Governance Reference

Use this for high-complexity, production-grade, enterprise requirements work: multiple departments, external integrations, compliance duties, privacy/security risk, operational SLAs, data migration, high concurrency, financial impact, audit, or mission-critical workflows.

## Table of Contents

- Enterprise Lens
- Cross-Cutting Requirement Areas
- Governance Roles
- Enterprise Quality Attributes
- Integration and Interface Control
- Data Quality and Migration
- Security, Privacy, and Compliance
- Operations and Support
- Rollout and Adoption
- Enterprise Quality Gate

## Enterprise Lens

Enterprise requirements must cover more than feature behavior:

- business value and process ownership
- user classes across departments and geographies
- decision rights and conflict resolution
- data ownership, lineage, quality, retention
- integration with existing systems
- security, privacy, compliance, audit
- operational reliability, support, monitoring, recovery
- migration, rollout, adoption, training
- change governance and traceability

## Cross-Cutting Requirement Areas

| Area | Questions |
|---|---|
| Organization | Which departments own decisions, approvals, exceptions, and funding? |
| Process | What as-is/to-be workflows, handoffs, controls, and KPIs must be represented? |
| User classes | Which classes differ by authority, frequency, skill, geography, risk, or accessibility? |
| Data | What is the source of truth? What data is stale, duplicated, incomplete, regulated, or sensitive? |
| Integration | Which systems send/receive data? What happens when they fail, delay, or disagree? |
| Security | Who can see, create, change, approve, export, mask, archive, or delete each data class? |
| Compliance | What policies, laws, certifications, audit trails, retention periods, and approvals apply? |
| Operations | Who monitors, supports, restores, escalates, and communicates incidents? |
| Rollout | Pilot, migration, cutover, rollback, training, support readiness, adoption metrics |
| Analytics | Metric definitions, data lineage, reconciliation, report owners, decision use |

## Governance Roles

Add these roles when relevant:

| Role | Requirement responsibility |
|---|---|
| Business process owner | Owns process rules, KPIs, exceptions, and approvals |
| Data owner/steward | Owns definitions, quality, source of truth, retention |
| Security officer | Owns access control, least privilege, audit, threat concerns |
| Privacy/compliance officer | Owns regulatory, consent, retention, and reporting needs |
| Operations/SRE | Owns availability, monitoring, incident response, recovery |
| Integration owner | Owns interface contracts, error handling, versioning |
| Support/training owner | Owns adoption, help, training, support workflows |
| Release/cutover manager | Owns migration, pilot, cutover, rollback |
| Enterprise architect | Owns architecture constraints, standards, reuse, interoperability |

## Enterprise Quality Attributes

Use a quality attribute register:

| ID | Attribute | Requirement | Scale/metric | Target | Conditions | Verification | Owner |
|---|---|---|---|---|---|---|---|

Consider:

- availability by business-critical window
- performance under peak and degraded conditions
- throughput and batch completion time
- reliability and mean time between failures
- robustness under invalid input, network failures, partial outages
- recovery time objective and recovery point objective
- scalability by users, transactions, data volume, tenants, locations
- security and privacy controls by data classification
- integrity/reconciliation of financial or regulated data
- interoperability and interface compatibility
- usability/accessibility for critical user classes
- installability/configurability for enterprise environments
- modifiability for volatile business rules
- auditability and verifiability

Prioritize attributes because they conflict. Record trade-off decisions explicitly.

## Integration and Interface Control

For each integration:

| Interface ID | Systems | Direction | Data/messages | Protocol | Frequency | Failure handling | Owner |
|---|---|---|---|---|---|---|---|

Elicit:

- message formats, schemas, codes, and units
- data mappings and transformations
- authentication/authorization
- encryption and privacy controls
- retry, timeout, idempotency, and duplicate handling
- ordering and synchronization needs
- versioning and backward compatibility
- monitoring and alerting
- support ownership across both sides
- change-control path for interface changes

## Data Quality and Migration

Data requirements:

- source of truth and authoritative owner
- definition, type, allowed values, units, format
- completeness, accuracy, timeliness, uniqueness, consistency
- reconciliation rules
- retention, disposal, archiving, legal hold
- lineage and auditability
- migration mapping, cleansing, conversion, validation, fallback
- access restrictions by role/data class
- reporting and analytics definitions

Migration table:

| Legacy field/entity | Target field/entity | Transformation | Quality rule | Owner | Validation evidence |
|---|---|---|---|---|---|

## Security, Privacy, and Compliance

Capture:

- identity, authentication, authorization, session requirements
- role/permission model
- segregation of duties
- data classification and masking
- consent, retention, deletion, portability, and legal hold
- audit trail events and tamper resistance
- encryption in transit and at rest
- regulatory reports and certifications
- breach/incident notification obligations
- security logging, monitoring, and review
- threat or abuse cases for high-risk systems

Make compliance requirements traceable to policies, laws, standards, contracts, or audit findings.

## Operations and Support

Operational requirements:

- monitoring signals and dashboards
- alert thresholds and escalation paths
- backup/restore
- disaster recovery
- maintenance windows
- runbooks and admin capabilities
- support roles and service levels
- log retention and observability
- capacity planning
- configuration and feature toggles
- startup, shutdown, degraded mode, rollback

Do not hide operational needs under "other requirements"; make them verifiable.

## Rollout and Adoption

For enterprise adoption:

- pilot population and success criteria
- migration waves
- training requirements
- support readiness
- cutover checklist
- rollback/fallback triggers
- communication plan
- adoption KPIs
- legacy system retirement criteria
- business continuity constraints

Separate software requirements from project rollout tasks, but trace them when product behavior depends on rollout or migration.

## Enterprise Quality Gate

Before baseline or release:

- all critical business processes have owners and success metrics
- user classes across departments are represented
- data ownership, definitions, quality, retention, and migration are explicit
- integrations include failure handling and ownership
- security/privacy/compliance requirements trace to sources
- operational requirements are measurable and testable
- rollout, support, training, cutover, and rollback needs are visible
- quality attribute trade-offs are documented
- audit and traceability needs are met
- enterprise risks have mitigations and owners
