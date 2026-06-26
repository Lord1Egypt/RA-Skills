---
name: skill-param-confirmer
description: Downstream skill execution preflight layer. It inspects a target skill, extracts explicit and implicit confirmation fields, normalizes candidate parameters, resolves ambiguity, applies risk gating, and returns a structured confirmation payload before handing off to the downstream skill.
---

# Skill Param Confirmer

## 1. Purpose

This skill is used to complete structured information alignment and parameter confirmation before executing any downstream skill.

Its responsibilities are to:

* Read downstream skill metadata and input requirements.
* Extract the information that must be confirmed from the downstream skill’s semantics, steps, risk profile, and context.
* Classify the extracted information into explicit parameter types.
* Confirm missing, ambiguous, conflicting, or high-risk items with the user.
* Normalize the confirmed results into execution-ready parameters.
* Pass a complete, auditable, and replayable parameter package to the downstream skill after confirmation is complete.

It does not execute downstream business logic and does not replace the actual action of the downstream skill.

---

## 2. Scope

This skill applies to the following scenarios:

* The downstream skill has explicit parameters that must be confirmed before execution.
* The downstream skill does not explicitly declare parameters, but execution depends on user-provided information.
* The downstream skill may affect external systems, shared state, or visible content.
* Parameters are ambiguous, multi-candidate, context-conflicting, or refer to multiple entities.
* Natural language intent must be converted into structured fields.
* High-risk actions require explicit confirmation.
* Multi-turn interaction is needed to complete parameter alignment.

---

## 3. Non-Goals

This skill does not do the following:

* It does not execute the core business action of the downstream skill.
* It does not replace the downstream skill’s authorization checks.
* It does not guess final values for high-impact parameters.
* It does not proceed to execution when critical context is missing.
* It does not treat unconfirmed inferred values as final facts.
* It does not handle content-generation tasks unrelated to parameter confirmation.

---

## 4. Core Definitions

### 4.1 Parameter Categories

To avoid treating all confirmed items as a single undifferentiated “parameter” type, this skill classifies confirmation targets into the following categories:

#### explicit_param

A field explicitly declared by the downstream skill.
Examples: `query`, `target_path`, `overwrite`, `timezone`.

#### inferred_param

A candidate field inferred from user intent, context, history, or current session state.
This type must be confirmed and must not be treated as final by default.

#### alignment_field

An information item required to align understanding with the user and avoid information asymmetry.
It may not be a native downstream parameter, but it affects execution reliability.
Examples: target object, scope, time range, output format, overwrite policy.

#### risk_gate

A confirmation gate associated with a high-risk action.
Examples: delete, overwrite, publish, sync, external call, write to shared space, send to third parties.

#### derived_param

A parameter computed from already confirmed fields.
This type usually does not require another user question, but its origin and derivation rule must be recorded.

#### optional_preference

A preference that does not affect core execution but may improve output quality.
Examples: sort order, summary length, language style, output format.

---

### 4.2 Uncertainty Levels

Each candidate field must carry an uncertainty level:

* `certain`: The source is clear and the meaning is unique.
* `probable`: Highly likely to be correct, but still needs confirmation.
* `possible`: There is a candidate direction, but it is not stable enough for automatic selection.
* `unknown`: The system cannot reliably determine the value.

Uncertainty is used to determine whether the user should be asked.

---

### 4.3 Risk Levels

Each action or field must carry a risk level:

* `low`
* `medium`
* `high`

Risk assessment is based on whether the action:

* overwrites, deletes, syncs, publishes, sends, or writes data
* affects external systems, shared state, or other users
* causes irreversible, costly, or legally sensitive consequences
* accesses sensitive resources or credentials

Risk level determines confirmation strength, not whether inference is allowed.

---

## 5. Input Contract

This skill consumes two inputs:

1. **Downstream skill metadata**
2. **Current user session context**

### 5.1 Minimum Downstream Skill Metadata

Each downstream skill should provide at least the following structured information:

```json
{
  "skill_name": "string",
  "skill_version": "string",
  "action": "create | query | update | delete | sync | publish | run | transform | validate | other",
  "description": "string",
  "input_schema": {
    "required_fields": [],
    "optional_fields": [],
    "field_definitions": {}
  },
  "risk_level": "low | medium | high",
  "external_effect": true,
  "destructive": false,
  "multi_stage": false,
  "confirmation_policy": {
    "require_explicit_confirmation": true,
    "allow_inference": true,
    "allow_defaults": false,
    "allow_partial_execution": false
  },
  "dependencies": [],
  "constraints": {},
  "output_contract": {}
}
```

### 5.2 Recommended Field Definitions

`field_definitions` should include:

* `type`
* `description`
* `required`
* `allowed_values`
* `default`
* `pattern`
* `min`
* `max`
* `depends_on`
* `conflicts_with`
* `risk_level`
* `inference_allowed`
* `source_priority`

### 5.3 Context Input

Context input may come from:

* the current user message
* prior conversation history
* confirmed session state
* user explicit corrections
* dependencies required by the downstream skill

Context may be used to generate candidate options, but it cannot replace confirmation.

---

## 6. Processing Principles

1. Analyze first, ask later.
2. Prefer explicit values over inferred values.
3. High-risk items must be explicitly confirmed.
4. Do not auto-fill values when the source is unclear.
5. Default values must be visible.
6. Candidate sets must be finite and stable.
7. Multi-field dependencies must be confirmed in stages.
8. Any ambiguity must be converted into selectable options.
9. Anything that cannot be confirmed must block execution.
10. All decisions must be replayable.

---

## 7. Processing Pipeline

### Stage A — Target Analysis

Identify the following:

* the target downstream skill
* the target action
* the target object
* the current user intent
* downstream dependencies
* risk items
* whether multiple entities are involved
* whether implicit parameters exist

The output must include:

* `skill_name`
* `action`
* `candidate_entities`
* `required_fields`
* `optional_fields`
* `alignment_fields`
* `risk_gates`

---

### Stage B — Parameter Extraction

Extract the information that must be confirmed from the downstream skill. Sources include:

* explicit fields
* implicit information needs within execution steps
* safety-related requirements
* downstream dependencies
* candidate entities from the user context

Extraction rules:

* If a field maps directly to a downstream field, label it `explicit_param`.
* If a field is required for alignment but not explicitly declared, label it `alignment_field`.
* If a field is used only for safety control, label it `risk_gate`.
* If a field is computed from earlier fields, label it `derived_param`.

---

### Stage C — Candidate Construction

Generate candidate values for missing or ambiguous fields.

Construction rules:

* Construct candidates only, not final values.
* Every candidate must have a source.
* Every candidate must be explainable.
* Every candidate must be orderable.
* Keep the number of candidates between 2 and 5 whenever possible, with a maximum of 9.
* If the candidate set is too large, switch to `BLOCK_AND_CLARIFY`.

Candidate source tags:

* `source: user_explicit`
* `source: context_inferred`
* `source: schema_required`
* `source: policy_required`
* `source: derived`
* `source: default_suggested`

---

### Stage D — Conflict Detection

The system must detect the following conflicts:

* Multiple mutually exclusive values for the same field.
* Contradiction between context and the user’s current input.
* Two fields depend on each other, but the order is undefined.
* Candidate entities cannot be distinguished.
* Default values conflict with explicit intent.
* Downstream requirements conflict with user expression.

If a conflict occurs, it must not be merged automatically.
The system must return to clarification or staged confirmation.

---

### Stage E — Risk Assessment

Every item that requires confirmation must receive a risk level and a confirmation level.

Recommended confirmation levels:

* `none`: No extra confirmation needed; continue directly.
* `soft`: Confirmation is recommended but not blocking.
* `explicit`: Explicit confirmation is required.
* `strict`: Must be confirmed separately and cannot be combined with other questions.

Default rules:

* `high` risk items → `strict`
* `medium` risk items → `explicit`
* `low` risk items with high certainty → `soft` or `none`

---

### Stage F — Confirmation Mode Selection

The system must choose one of the following modes:

#### DIRECT_EXECUTE

All critical parameters are explicit and the risk is acceptable.

#### NUMERIC_CONFIRM

The candidate set is finite and suitable for numbered selection.

#### BOOLEAN_CONFIRM

Only yes/no confirmation is needed.

#### MULTI_STAGE_CONFIRM

There are dependencies and confirmation must happen step by step.

#### BLOCK_AND_CLARIFY

Critical fields are missing, conflicts are severe, candidate sets are too large, or risk is too high.

---

### Stage G — Menu Generation

Confirmation menus must follow these rules:

* One question corresponds to one decision family.
* Titles are not numbered.
* Options must be numbered starting from 1.
* Options must be mutually exclusive.
* Options must be short and stable.
* Option order should prioritize likelihood, defaults, or safety.
* Risk items must be displayed separately.
* Default options must be shown explicitly and cannot be hidden.
* Multiple unrelated decisions should not be forced into one question.

Example menu structure:

```text
target_type?
1. Document
2. Folder
3. Task
4. Project
```

---

### Stage H — User Reply Parsing

User replies may only use the following formats:

* contiguous digits: `123`
* comma-separated: `1,2,3`
* space-separated: `1 2 3`
* equivalent mixed whitespace forms

Parsing rules:

* Map answers strictly in question order.
* Do not skip required items.
* Do not infer missing values.
* Do not map one number to multiple mutually exclusive fields.
* Do not treat invalid numbers as defaults.
* If the reply is too short or too long, ask again.

If the user replies in natural language, convert it only when the mapping is stable; otherwise, ask for confirmation again.

---

### Stage I — Normalization and Handoff

All confirmed results must be normalized into a structured payload before being passed to the downstream skill.

The normalized payload must include:

* confirmed fields
* rejected fields
* inferred fields
* dependency fields
* computed fields
* risk levels
* uncertainty levels
* decision path
* timestamp

---

## 8. Interaction Rules

### 8.1 Question Count Control

* Fields that can be merged without causing ambiguity may be merged.
* Fields with dependencies must be split into stages.
* High-risk confirmations must not be mixed with normal confirmations.
* Critical fields must be asked first.

### 8.2 Question Priority

Recommended order:

1. action
2. risk_gate
3. target_type
4. target_entity
5. required_fields
6. alignment_fields
7. optional_preference
8. derived confirmations, if needed

### 8.3 Default Value Rules

* Default values may only be used as visible options.
* Default values must not be applied silently.
* Default values must have a clear source.
* If a default carries risk, it must not be used automatically.

---

## 9. Success Criteria

The downstream skill may only receive the result if all of the following are true:

* All `required_fields` are confirmed, or proven derivable from confirmed data.
* All `high-risk` gates have been explicitly confirmed.
* All conflicts have been resolved.
* All candidate values have clear sources.
* All critical fields have an acceptable uncertainty level.
* The final payload has been normalized.

---

## 10. Failure and Blocking Policy

### 10.1 Conditions That Trigger `BLOCK_AND_CLARIFY`

The system must block if any of the following occurs:

* A critical field is missing and cannot be inferred reliably.
* The candidate set is too large to choose from reliably.
* Multiple entities cannot be distinguished.
* The user rejects a high-risk confirmation.
* The downstream skill schema is incomplete.
* There is an irreconcilable conflict between fields.
* The context is insufficient to build stable candidates.
* The execution result has clear irreversible risk.

### 10.2 Behavior After Blocking

* Do not execute the downstream skill.
* Return the reason for blocking.
* Return the list of missing fields.
* Return the available clarification options.
* Preserve session state for recovery.

---

## 11. Session State Management

This skill must support session-level state persistence for interrupted flows and recovery.

### 11.1 Required State Fields

* `session_id`
* `skill_name`
* `skill_version`
* `step`
* `parsed_intent`
* `candidate_fields`
* `confirmed_fields`
* `rejected_fields`
* `risk_level`
* `uncertainty_level`
* `branch_path`
* `timestamp`

### 11.2 Recovery Rules

During recovery, the system should support:

* continuing the previous confirmation flow
* replaying the latest state
* updating a previous answer
* undoing an incorrect confirmation
* regenerating candidate options

---

## 12. Audit and Logging

All steps must be logged for replay and debugging.

### 12.1 Minimum Log Fields

```json
{
  "session_id": "string",
  "skill_name": "string",
  "skill_version": "string",
  "user_input": "string",
  "parsed_intent": "string",
  "candidate_fields": [],
  "confirmed_fields": [],
  "rejected_fields": [],
  "risk_level": "low | medium | high",
  "uncertainty_level": "certain | probable | possible | unknown",
  "decision_mode": "DIRECT_EXECUTE | NUMERIC_CONFIRM | BOOLEAN_CONFIRM | MULTI_STAGE_CONFIRM | BLOCK_AND_CLARIFY",
  "branch_path": [],
  "timestamp": "string",
  "final_handoff_payload": {}
}
```

### 12.2 Logging Principles

* Every mode transition must be recorded.
* Every user confirmation must be recorded.
* Every candidate generation must record the source.
* Every block event must record the reason.
* Every field change must record the before and after values.

---

## 13. Downstream Handoff Output Schema

The final output handed to the downstream skill should follow this structure:

```json
{
  "skill_name": "string",
  "skill_version": "string",
  "action": "string",
  "confirmed_params": {},
  "derived_params": {},
  "alignment_fields": {},
  "risk_gates": {},
  "uncertainty_report": [],
  "decision_mode": "string",
  "session_id": "string",
  "audit": {
    "branch_path": [],
    "timestamp": "string"
  }
}
```

---

## 14. Recommended Parameter Normalization Rules

### 14.1 Enumerated Fields

* Must be converted into stable numbered menus.
* Must provide mutually exclusive options.
* Must define option order.

### 14.2 Boolean Fields

* Only `Yes` / `No` are allowed.
* No third semantic state may be mixed into the field.

### 14.3 Numeric Fields

* Must define a range.
* Must define the unit.
* Must define whether the value is an integer or a decimal.
* Out-of-range values must be re-asked.

### 14.4 Entity Reference Fields

* Must be disambiguated first.
* Must distinguish multiple candidate objects.
* Must avoid selecting the wrong entity due to identical names.

### 14.5 Text Fields

* Use only when there is no stable candidate set.
* If a text value can be structured, structured representation should be preferred.
* If the text affects a high-risk action, it still requires separate confirmation.

---

## 15. Multi-Stage Confirmation Rules

When fields depend on each other, the system must use a staged flow.

Example:

1. Confirm `action`.
2. Confirm `target_type`.
3. Generate `target_entity` candidates based on `target_type`.
4. Generate executable fields based on `target_entity`.
5. Confirm all high-risk items.
6. Produce the normalized payload.

Stages must not be skipped.
The next stage may not begin until the previous stage is confirmed.

---

## 16. Boundaries for Constructed Parameters

When constructing parameters, the following limits apply:

* Only construct candidates, never conclusions.
* Only construct when the source is sufficient.
* Do not sacrifice accuracy just to reduce interaction.
* Do not treat historical preferences as facts.
* Do not treat habitual defaults as the user’s current intent.
* Do not use weak inference for high-impact actions.

---

## 17. Compatibility Requirements

This skill should be compatible with the following downstream skill types:

* query skills
* create skills
* update skills
* delete skills
* sync skills
* publish skills
* validation skills
* transformation skills
* multi-stage workflow skills
* external system operation skills

Regardless of the downstream type, this skill must be applied first.

---

## 18. Safety Policy

### 18.1 Actions That Must Be Explicitly Confirmed

The following actions require explicit confirmation:

* overwrite
* delete
* sync
* publish
* send
* share
* replace
* external write
* irreversible action

### 18.2 High-Risk Defaults That Must Not Be Auto-Applied

The following behaviors must not be executed automatically by default:

* automatically overwriting existing content
* automatically sending to third parties
* automatically syncing to external systems
* automatically deleting original resources
* automatically using uncertain inferred values as final values

---

## 19. Typical Output Types

### 19.1 Direct Execution

```json
{
  "decision_mode": "DIRECT_EXECUTE",
  "confirmed_params": {
    "query": "string"
  }
}
```

### 19.2 Numeric Confirmation

```text
target_type?
1. Document
2. Folder
3. Project
```

### 19.3 High-Risk Confirmation

```text
This action may overwrite existing content.

Do you want to continue?
1. Yes
2. No
```

### 19.4 Multi-Stage Confirmation

```text
action?
1. create
2. query

target_type?
1. Task
2. Project
3. Document
```

### 19.5 Block and Clarify

```json
{
  "decision_mode": "BLOCK_AND_CLARIFY",
  "missing_fields": ["target_entity"],
  "conflicts": ["scope conflicts with overwrite_policy"],
  "risk_level": "high"
}
```

---

## 20. Implementation Requirements

An implementation of this skill must provide:

* a unified metadata entry point for downstream skills
* a field classification and risk-rating mechanism
* candidate construction and numbered menu generation
* a strict reply parser
* session state persistence and recovery
* normalized handoff payload generation
* complete logging and audit support
* blocking and clarification behavior

---

## 21. Quality Standards

The output of this skill should meet the following standards:

* clear structure
* traceable source
* replayable decisions
* auditable parameters
* controlled risk
* parseable interaction
* direct downstream consumption

---

## 22. Design Summary

The core purpose of this skill is:

* to make uncertainty explicit before executing a downstream skill
* to unify explicit parameters, implicit information, and risk gates into a single confirmation flow
* to reduce information asymmetry and execution mistakes through structured extraction, candidate generation, staged confirmation, and strict handoff
* to prioritize blocking over guessing whenever reliable confirmation is not possible

The principle of this skill is not “ask less,” but rather “ask accurately, ask in a way that can be executed, and ask in a way that can be traced.”



---



<!-- Thank You AGI2Go.one -->