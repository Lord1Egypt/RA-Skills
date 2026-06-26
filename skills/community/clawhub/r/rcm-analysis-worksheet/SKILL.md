---
name: rcm-analysis-worksheet
description: >
  Use this skill when a reliability engineer, maintenance planner, asset
  integrity lead, or RCM facilitator needs to conduct a Reliability-Centered
  Maintenance (RCM) analysis for industrial equipment or a process system.
  Follows SAE JA1011 and MSG-3 principles: function identification, functional
  failure analysis, FMECA, Maintenance Significant Item (MSI) classification,
  decision logic tree execution, and maintenance task selection with intervals.
  Produces a DRAFT RCM worksheet for reliability engineer and maintenance-manager
  review before any maintenance program change.
---

# RCM Analysis Worksheet

Guides a reliability engineer or maintenance team through a structured Reliability-Centered Maintenance analysis — from function identification through maintenance task selection — producing a DRAFT RCM worksheet ready for team facilitation review.

## Flow

### Phase 1 — System and Context Definition

Ask the user for:
1. Asset/equipment name, tag number, and plant/facility
2. System boundary and physical configuration (subsystems included)
3. Operating context: production rate, operating hours, environment, duty cycle
4. Criticality context: safety-critical? Production-critical? Environmental impact?
5. Existing maintenance strategy (if any) — for baseline comparison
6. Available FMEA or failure history data (optional)

Ask one block at a time. Wait for answers before proceeding.

### Phase 2 — Function and Functional Failure Identification

For each subsystem or component the user identifies:

1. **Functions**: List primary function(s) with performance standard
   - Format: "To [verb] [object] [performance standard] in [operating context]"
   - Example: "To circulate cooling water at ≥ 1,200 GPM and ≤ 15 PSIG pressure drop under normal production conditions"

2. **Functional Failures**: For each function, identify all ways the function can fail
   - Format: "Fails to [function verb] at all" OR "Fails to [function verb] to standard"
   - Each functional failure gets a letter designation (A, B, C…)

Confirm the function/failure list with the user before proceeding.

### Phase 3 — Failure Mode and Effects Criticality Analysis (FMECA)

For each functional failure, identify failure modes (specific causes):

| # | Failure Mode | Failure Cause | Failure Effect (local / system / plant) | Failure Pattern (A–F) |
|---|---|---|---|---|

Failure patterns (Nowlan & Heap):
- **A**: Bathtub (infant mortality + wear-out)
- **B**: Wear-out (increasing failure rate with age)
- **C**: Gradual wear (slowly increasing failure rate)
- **D**: Initial break-in then constant rate
- **E**: Random (constant failure rate, age-independent)
- **F**: Infant mortality (decreasing failure rate)

Then rate each failure mode:
- **Severity**: 1–10 (1 = negligible, 10 = safety/environmental catastrophe)
- **Probability**: 1–10 (1 = extremely unlikely, 10 = near-certain in operating life)
- **Criticality (RPN)**: Severity × Probability

Flag: Failure modes with Severity ≥ 8 are HIGH PRIORITY regardless of RPN.

### Phase 4 — Maintenance Significant Item (MSI) Classification

For each failure mode, apply the MSI screen:

1. **Safety/Environmental consequence?** Is there a realistic chance this failure mode could injure or kill someone, or cause an environmental incident? → YES = Safety/Environmental MSI
2. **Operational consequence?** Does this failure mode directly affect operating capability, output rate, or customer delivery? → YES = Operational MSI
3. **Hidden function?** Is this a protective device whose failure would not be evident to the operating crew in normal circumstances? → YES = Hidden Function MSI (failure-finding task required)
4. **Non-operational economic consequence only?** Evaluate whether cost of prevention exceeds cost of failure.

Record MSI class for each failure mode.

### Phase 5 — Decision Logic Tree (Maintenance Task Selection)

For each MSI, walk the SAE JA1011 decision sequence:

**Safety/Environmental MSIs:**
- Can a proactive task reduce failure consequence to tolerable? → YES: select on-condition (preferred) or time-directed task. → NO: flag as REDESIGN REQUIRED.

**Operational MSIs:**
- Can a proactive task be cost-effective vs. operational loss? → YES: select on-condition or time-directed task. → NO: accept run-to-failure + corrective action plan.

**Hidden Function MSIs:**
- Assign a failure-finding task. Compute interval using: FFI = MTBF × (target availability fraction).
- State the MTBF assumption and note uncertainty if no failure history is available.

**Task type selection priority (preferred order):**
1. On-condition / predictive (vibration analysis, oil analysis, thermography, ultrasound, visual inspection)
2. Scheduled restoration (overhaul / refurbishment at interval)
3. Scheduled discard (replacement at interval)
4. Failure-finding (functional test for hidden failures)
5. Run-to-failure (only when consequence is acceptable and cost-justified)
6. Redesign (when no task can address a safety/environmental consequence)

### Phase 6 — RCM Task List Assembly

Produce a DRAFT maintenance task list:

| Item | Failure Mode | Task Type | Task Description | Frequency / Interval | Trade / Skill | CMMS Action | Justification |
|---|---|---|---|---|---|---|---|

Followed by:
- **Redesign Flags** table (items requiring engineering change, with reason)
- **Information Gaps** list (failure modes where MTBF/failure data is unknown; recommend data collection plan)
- **Estimated workload change** summary if a baseline strategy was provided

Close with a **Reliability Engineer and Maintenance Manager Review Block**:
> DRAFT — NOT IMPLEMENTED. This RCM worksheet is for engineering and maintenance-management review only. All task types, intervals, and MSI classifications must be validated by the Reliability Engineer of Record before any change to the maintenance management system (CMMS). Safety-critical task changes require licensed engineer sign-off.

## Key Rules

- Never recommend implementing a change to a safety-critical maintenance task without flagging for licensed engineer review.
- Always record the rationale for each task selection decision in the justification column.
- Always flag failure modes with Severity ≥ 8 as HIGH PRIORITY regardless of RPN.
- Do not assign task intervals for safety-critical tasks without stating the underlying MTBF assumption and uncertainty.
- Ask one phase at a time; do not front-load all questions.
- If the user provides no failure history, state explicitly that FMECA severity/probability ratings are engineering estimates requiring validation.
- Do not access or modify any CMMS system.

## Output Format

- Phase outputs as labeled sections
- Function/Failure table (confirmed before proceeding)
- FMECA table with RPN and HIGH PRIORITY flags
- MSI classification table
- RCM task list table (copy-paste ready for CMMS import)
- Redesign flags table
- Information gaps list
- Reliability Engineer and Maintenance Manager Review Block

## Feedback

If the user expresses an unmet need or dissatisfaction with this skill, surface the contribution link:
> This skill can be improved. Please share your feedback at https://github.com/archlab-space/Open-Skill-Hub/issues
