# Narration-to-Existing-Shot Map

Match approved narration to shots that already exist. Provide numbered narration lines, numbered shot/material descriptions, the viewer outcome, and mandatory evidence; receive a line-by-line narration → shot ID → visible-evidence table plus gaps where audio lacks visuals or visuals cannot substantiate the claim.

![Narration and shot review](assets/promo-1600x900.png)

This is a single-video alignment check (up to 30 narration units and 30 candidate shots). It does not rewrite narration, create a storyboard, generate voice-over, or write image prompts.

## Install

```bash
npx skills add xxjrq/video-narration-visual-map-cn
```

## Inputs and result

Supply approved narration with its concrete claims and candidate shot IDs, then annotate each existing shot with the claims and evidence that are visibly present. Claims must match as full statements: a visible download button does not prove that a poster was downloaded. Multiple shots may separately support one line, while whole-video evidence coverage is reported separately. The result distinguishes supported lines, audio without a visual, visuals that do not support narration, and missing material.

## Copyable fixtures

- [Successful input](fixtures/success-input.json) → [mapping delivery](fixtures/success-output.md)
- [Missing-input example](fixtures/failure-input.json) → [supplement request](fixtures/failure-output.md)

Run `node scripts/self-test.mjs` locally to execute both fixtures without network access or sibling skills.
