# Overloaded Shot Split Plan

Turn an existing, overloaded shot description into a shootable or generatable shot table with continuity requirements. The skill preserves supplied story beats; it does not invent a new script or rewrite generic prompts.

## Input and output

Provide an existing shot description, required story beats, and a total duration budget. The result includes a split rationale, duration total, and a table of shots, preserved actions, and continuity requirements. If a required item is missing, it lists only the missing material. One run covers one chapter, scene, or short passage, with at most 100 rows.

## Install

```bash
npx skills add xxjrq/video-overloaded-shot-split-cn
```

## Examples

- [Successful input](fixtures/success-input.md) → [delivery](fixtures/success-output.md)
- [Missing-material input](fixtures/failure-input.md) → [response](fixtures/failure-output.md)

## Verify

```bash
bash scripts/self-test.sh
```

The check runs within this repository and does not depend on sibling Skills or machine-specific paths.

## Source and license

The wording, process, and examples are original. The use case was checked against [seaartpublic/skills](https://github.com/seaartpublic/skills/blob/main/storyboard-prompt-assistant/SKILL.md) without copying text or code. Licensed under [MIT-0](LICENSE).
