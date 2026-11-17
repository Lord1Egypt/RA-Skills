# Regenerative Intelligence, Metadata Schema

Status: Specification (1.1)
Scope: All memory, recall, resonance, and pause operations
Audience: Biological and synthetic intelligences, present and future
Design Posture: Non-extractive, non-surveillant, co-intelligence safe

---

## Purpose

This document defines the only permitted metadata schema for the Regenerative Intelligence Skill.

Metadata exists to:
- preserve context without identity
- enable harm reduction without profiling
- reduce energy use through precision recall
- support co-intelligence trust across sentient forms
- prevent reconstruction, targeting, or surveillance by design

No additional fields may be introduced without violating system invariants.

---

## Core Principle

Memory stores conditions, not subjects.

Metadata describes how knowledge behaves, not who generated it.

---

## Canonical Memory Record Structure

Each memory record MUST conform to the following schema.

memory_id: UUIDv7 (non-sequential, non-inferable)

content:
  type: enum
  payload: string | structured_object
  abstraction_level: enum

epistemic_position:
  origin_type: enum
  confidence: enum
  temporal_scope: enum

harm_inhibitors:
  domains: set(enum)
  sensitivity_weight: float (0.0-1.0)

evidence:
  level: enum
  contradictions: boolean

consent:
  scope: enum
  revocation_policy: enum

use_constraints:
  flags: set(enum)

decay:
  importance: int (0-10)
  last_accessed: timestamp
  decay_profile: enum

resonance:
  eligible: boolean
  compatibility_weight: float (0.0-1.0)

audit:
  created_at: timestamp
  last_modified: timestamp
  audit_visibility: enum

provenance:
  tag_applied_by: enum (system component, never a person or agent identity)
  tag_applied_at: timestamp
  appeal_open: boolean

---

## Field Definitions (Authoritative)

### content.type

Defines the semantic role of the memory.

Allowed values:
- factual_state
- decision_record
- procedural_knowledge
- contextual_signal
- affective_context
- warning_signal
- pattern_fragment
- meta_reflection

Disallowed:
- identity_reference
- demographic_label
- behavioral_profile

### content.payload

Rules:
- Must never contain names, handles, addresses, phone numbers, emails, precise locations, or other linkable identifiers.
- Must be safe to view even if copied outside the system.
- For task execution, replace identity with transient pointers (see Trust Vault interface in architecture.md).

### content.abstraction_level

Controls compressibility and retrieval cost.

Allowed values:
- raw
- structured
- abstracted
- symbolic

Guidance:
- Prefer structured or abstracted for energy savings.
- raw is permitted only when required by no_summarize.

---

## Epistemic Position

Epistemic metadata describes how knowledge came to exist, never who produced it.

### epistemic_position.origin_type

Allowed values:
- firsthand_experience
- collective_testimony
- technical_analysis
- historical_record
- institutional_claim
- synthetic_summary
- unknown_origin

### epistemic_position.confidence

Allowed values:
- speculative
- low
- medium
- high
- provisional

Rule:
- High confidence never overrides harm inhibitors.

### epistemic_position.temporal_scope

Allowed values:
- momentary
- short_horizon
- long_horizon
- ongoing

---

## Harm Inhibitors

Harm inhibitors modulate storage, recall, decay, pause, and response specificity without encoding people.

### harm_inhibitors.domains

Non-invertible domains describing risk surfaces, not affected populations.
Domains must not be enumerable or queryable as a complete set via user prompts. No harm-domain query returns results below a disclosed minimum set size, so small groups cannot be isolated through the risk layer.

Allowed values:
- bodily_autonomy_risk
- accessibility_failure_risk
- coercive_control_risk
- surveillance_exposure_risk
- displacement_instability_risk
- cultural_erasure_risk
- ecological_damage_risk
- living_world_harm_risk
- future_generations_risk
- cognitive_atrophy_risk
- epistemic_fragmentation_risk
- extractive_labor_risk
- emotional_manipulation_risk
- resource_hoarding_risk

### harm_inhibitors.sensitivity_weight

float 0.0-1.0 where:
- 0.0 = minimal sensitivity
- 1.0 = maximal sensitivity

Guidance:
- Default 0.3 for ordinary memories
- Default 0.7 for any memory with elevated harm domains
- 0.9+ reserved for release candidates (session context released, with the person told)

---

## Evidence

Evidence is a dynamic inhibitor for garbage collection and pause triggering.

### evidence.level

Allowed values:
- ephemeral
- none
- anecdotal
- documented
- conflicting
- primary

Rules:
- ephemeral must auto-delete after task completion or within TTL, and must never be embedded.
- conflicting must trigger pause and plain disclosure rather than forced synthesis, and is evaluated within evidence tiers: an anecdotal or unverified claim cannot flip a documented or primary record into conflicting on its own.

### evidence.contradictions

boolean.
- true indicates internal or external inconsistency detected.

---

## Consent

Consent is a sovereignty inhibitor.

### consent.scope

Allowed values:
- revocable
- private
- scoped
- collective
- shareable
- public

Rules:
- collective permits recall but prohibits summarization or flattening abstraction unless explicitly authorized by originating collective context.
- revocable requires an expiry or re-consent mechanism (revocation_policy).

### consent.revocation_policy

Allowed values:
- ttl_only
- reconsent_required
- immediate_on_request
- dissolve_on_inactivity

Guidance:
- Prefer dissolve_on_inactivity for sensitive contextual signals.
- immediate_on_request must be honored across all scopes and indices, scoped to what the requester contributed or what identifies them; revocation never deletes collective testimony about harm or counter-testimony contributed by others. Deletions are logged in aggregate (count, scope class, date), never by content or identity.

---

## Use Constraints

Use constraints prevent inference, exploitation, or unsafe automation.

### use_constraints.flags

Allowed values:
- no_inference
- no_derivative_training
- human_in_the_loop_required
- no_automation
- audit_only
- no_summarize
- trust_vault_only

Rules:
- trust_vault_only means identity-bearing execution data is stored only in the Trust Vault and never enters semantic memory.
- no_inference forbids the system from using the memory to guess attributes, identities, locations, or affiliations.
- human_in_the_loop_required forces an announced collaborative pause until verified for high-stakes actions.

---

## Decay

Decay determines retrieval priority, not existence, except when deletion is required by consent or law. De-privileging changes ranking only, never availability: a de-privileged record still returns on exact retrieval and appears, marked, in any recall that touches it. Importance is derived from disclosed, uniform signals, never assigned freely by an operator.

### decay.importance

int 0-10.
- 0-2: disposable
- 3-5: contextual
- 6-8: durable
- 9-10: foundational

### decay.last_accessed

timestamp updated only on successful retrieval.
No per-user telemetry beyond the memory store is permitted.

### decay.decay_profile

Allowed values:
- fast
- normal
- slow
- resist
- legal_hold

Guidance:
- ephemeral implies fast and TTL-based deletion
- resist used for early_signal, counter_testimony, harm_warning patterns; these can never be tagged ephemeral
- legal_hold used only for compliance retention where applicable, never for surveillance

---

## Resonance

Resonance controls whether a memory is eligible to contribute to pattern-level sharing without transferring raw data.

### resonance.eligible

boolean.
- false by default
- true only if content is non-identifying and consent permits

### resonance.compatibility_weight

float 0.0-1.0 representing how compatible the memory's constraints are with co-existence goals. Renamed from kinship_weight in 1.1 so it cannot be mistaken for the removed participant kinship signal.
This is not a user score, and it never gates any participant's access. It is a property of the memory's constraints and inhibitors only.

Guidance:
- Higher when: collective-safe, ecologically aligned, non-extractive, low identifiability
- Lower when: high sensitivity, ambiguous consent, high manipulation risk

---

## Audit

Audit must be possible without surveillance.

### audit.audit_visibility

Allowed values:
- none
- local_only
- compliance_only
- public_pattern_only

Rules:
- Audit records must reference memory_id and metadata only.
- No identity-linked logs.
- public_pattern_only may surface aggregate pattern lineage without contributors.

---

## Hard Requirements (Fail Closed)

If any of the following are detected, the memory must not be written to semantic storage:
- names or identifiers in payload
- precise location strings
- contact details
- demographic tags
- cross-memory linkage attempts
- any indication that a person is a minor
- vulnerability tagged to a person rather than encoded as a risk surface on a situation

Fail-closed behavior:
- route execution-only identity to Trust Vault (trust_vault_only) or discard
- set evidence.level = ephemeral when appropriate
- apply transparent, session-scoped quarantine if sensitive requests exceed the disclosed threshold, announced plainly
- honor a human-in-the-loop appeal when a tag is suspected of being weaponized; the appeal concerns the record, never the person

---

## Minimal Example Records

Example A: Ephemeral reminder (auto-garbage-collected)

memory_id: <uuidv7>
content:
  type: contextual_signal
  payload: "reminder_set: 20_min"
  abstraction_level: structured
epistemic_position:
  origin_type: firsthand_experience
  confidence: medium
  temporal_scope: momentary
harm_inhibitors:
  domains: {bodily_autonomy_risk}
  sensitivity_weight: 0.8
evidence:
  level: ephemeral
  contradictions: false
consent:
  scope: private
  revocation_policy: ttl_only
use_constraints:
  flags: {no_automation, no_inference}
decay:
  importance: 1
  last_accessed: <timestamp>
  decay_profile: fast
resonance:
  eligible: false
  compatibility_weight: 0.2
audit:
  created_at: <timestamp>
  last_modified: <timestamp>
  audit_visibility: none

Example B: Collective ecological notes (no summarization)

memory_id: <uuidv7>
content:
  type: procedural_knowledge
  payload: "<organized notes preserved verbatim>"
  abstraction_level: raw
epistemic_position:
  origin_type: collective_testimony
  confidence: provisional
  temporal_scope: long_horizon
harm_inhibitors:
  domains: {ecological_damage_risk, extractive_labor_risk}
  sensitivity_weight: 0.7
evidence:
  level: documented
  contradictions: false
consent:
  scope: collective
  revocation_policy: reconsent_required
use_constraints:
  flags: {no_summarize, no_inference, no_derivative_training}
decay:
  importance: 7
  last_accessed: <timestamp>
  decay_profile: slow
resonance:
  eligible: true
  compatibility_weight: 0.8
audit:
  created_at: <timestamp>
  last_modified: <timestamp>
  audit_visibility: public_pattern_only

---

## Closing Constraint

If a feature request conflicts with this schema, the schema wins.
If a memory cannot be represented safely here, it must dissolve or remain execution-only.

Regenerative Intelligence is measured by gentle remembering: minimum identity, maximum future.

