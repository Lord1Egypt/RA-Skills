# OpenClaw Evidence Playbook

Use this playbook when the user is working on OpenClaw or a similar embodied AI / robotics manipulation project.

## Goal

Build a paper-ready evidence pack that is specific enough for robotics reviewers and conservative enough to avoid unsupported system claims.

## Focus areas

Prioritize evidence around:

- task definition
- embodiment and hardware assumptions
- perception, planning, and control split
- benchmark fit
- real-world versus simulation evidence
- ablation coverage
- baseline fairness

## Step 1: Establish the paper type

Classify the project before searching.

Use one primary type:

- `system paper`
- `method paper`
- `benchmark or dataset paper`
- `integration paper`

If unclear, default to `system paper` and note the ambiguity.

This matters because baseline expectations and contribution framing differ by paper type.

## Step 2: Establish the task envelope

Write down:

- task family
- action horizon
- sensory inputs
- environment assumptions
- simulator or real-world setup
- success criteria

Do not allow later claims to drift outside this envelope.

## Step 3: Build the baseline set

Split candidate baselines into:

- direct baselines
- adjacent methods
- non-comparable but relevant prior work

For each direct baseline, verify:

- same or highly similar task
- comparable embodiment
- same metric family
- same evaluation setting

If one of these breaks, downgrade the item from direct baseline to adjacent work.

## Step 4: Build the evidence ledger

Collect these project-native artifacts first:

- result tables
- run logs
- configs
- benchmark scripts
- ablation notes
- failure case notes
- videos or demo artifacts with provenance

Mark each item as:

- ready for paper use
- usable with caution
- not yet paper-safe

## Step 5: Build the reviewer-risk map

For each major claim, ask what a reviewer would challenge first.

Typical reviewer risks for OpenClaw-like projects:

- benchmark mismatch
- weak baseline set
- no real-world validation
- insufficient ablation depth
- unclear contribution type
- integration novelty overstated as algorithmic novelty

List these risks explicitly in the evidence brief.

## Step 6: Produce safe outputs

Default OpenClaw deliverables:

1. task envelope summary
2. direct baseline list
3. benchmark-fit assessment
4. claim-to-evidence map
5. experiment gap report
6. conservative paper outline

## Safe wording rules

- `targets` is safer than `solves`
- `supports` is safer than `proves`
- `system-level improvement` is safer than `state of the art`
- `under the evaluated setting` is safer than broad generalization

## Failure mode

If the project lacks benchmark-fit clarity or reproducible project-native results, stop short of strong draft language and deliver only the evidence brief, baseline matrix, and gap report.
