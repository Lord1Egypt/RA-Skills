# Single-Shot Execution Card

Turn one approved live-action shot into an on-set execution card that a camera operator and performer can follow. Provide the shot, location/people/props, available equipment, action start and end, and delivery requirement. The result covers blocking, framing, spoken cues, an end marker, and on-set checks. Missing critical actions, location constraints, or equipment are listed first; unknown exposure and focal length stay marked for a test take.

![Single-shot execution card promo](assets/promo-1600x900.png)

## Install

```bash
npx skills add xxjrq/video-single-shot-execution-card-cn
```

This skill handles one approved live-action shot only. It does not write a story, schedule multiple shots, or generate AI video.

## Usage

Invoke `$video-single-shot-execution-card-cn` with the approved shot, location constraints, equipment, action start/end and delivery requirements. Missing, blank or pending approval returns missing information instead of an execution card. The script checks required fields and subject/prop anchors only; before drafting, the agent must compare the approved shot with action start/end, location, people and props. Stop for clarification if they conflict; field validation is not semantic review.

## Examples and self-test

- [Successful input](fixtures/success-input.json) → [execution card](fixtures/success-output.md)
- [Missing-information input](fixtures/failure-input.json) → [requested details](fixtures/failure-output.md)


- [Additional approved shot](fixtures/approved-shot-input.json) and [missing approved shot](fixtures/missing-approved-shot-input.json): [offline validation report](fixtures/approval-check-report.md). Approval is a user-provided prerequisite; the tool does not approve shots.

```bash
node scripts/self-test.mjs
```

The test runs locally in this repository and exercises both the valid and missing-information input branches.

## Source and license

The use case was checked against [agentara/skills video-storyboard](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md). This repository contains original wording, examples, and code. Licensed under [MIT-0](LICENSE).
