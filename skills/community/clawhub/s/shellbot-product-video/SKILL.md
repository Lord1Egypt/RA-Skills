---
name: shellbot-product-video
description: "Create conversion-focused product marketing videos with Remotion + React using the AIDA framework (Attention, Interest, Desire, Action). Use when building launch videos, paid social ads, app promos, SaaS explainers, or product teasers that must follow this arc: (1) establish the problem, (2) introduce the solution, (3) show use cases instead of feature lists, and (4) end with a call-to-action that includes an incentive. Use Freepik only for ancillary assets (for example Nano Banana 2 stills, Kling inserts/transitions, and ElevenLabs voiceover/music), while core storytelling, timing, and final assembly stay in Remotion code."
---

# Shellbot Product Video

## Overview

Build one thing well: product marketing videos that convert.
Keep Remotion as the source of truth for pacing, layout, animation, and render output. Use external generation tools only to enrich scenes.
Built by the [ShellBot Team](https://getshell.ai).

## Non-Negotiable Story Structure (AIDA)

Follow this structure in order:

1. Establish the problem being solved.
2. Introduce the solution.
3. Show use cases, not feature lists.
4. End with a CTA that includes an incentive.

Reject drafts that skip any step.

## Workflow

### 1) Bootstrap the Remotion Base Project

List bundled templates:

```bash
./scripts/bootstrap_template.sh --list
```

Bootstrap the chosen template:

```bash
./scripts/bootstrap_template.sh --template cinematic-product-16x9 ./my-product-video
cd ./my-product-video
npm install
```

To also copy official Remotion rule asset snippets into the project:

```bash
./scripts/bootstrap_template.sh --template cinematic-product-16x9 --include-rule-assets ./my-product-video
```

Template bundle:

- `assets/remotion-product-template` (`aida-classic-16x9`)
- `assets/templates/cinematic-product-16x9`
- `assets/templates/saas-metrics-16x9`
- `assets/templates/mobile-ugc-9x16`
- `references/remotion-rules/assets` (official-style reusable snippet assets)

Then adapt scene content/components and composition metadata in `src/Root.tsx` for the brief.

### 2) Capture Brief Inputs

Collect these fields before writing scenes:

- Product name
- Audience
- Core pain/problem
- Value proposition (one sentence)
- 2 to 4 use cases
- CTA
- Incentive for CTA (discount, trial extension, bonus, etc.)
- Visual style direction

If use cases are missing and only features are present, ask for use-case phrasing.

### 3) Build AIDA Narrative and Timing

Use this duration allocation as a starting point:

- Attention: 0% to 20%
- Interest: 20% to 45%
- Desire: 45% to 80%
- Action: 80% to 100%

Generate a structured plan with:

```bash
python3 scripts/brief_to_aida_plan.py --in brief.json --out plan.json --duration-sec 45 --fps 30
```

### 4) Map Story to Remotion Scenes

Implement scenes as React components and sequence them using `Sequence`.
Keep transitions purposeful and short (usually 8-18 frames).

Load [references/remotion-product-video-playbook.md](references/remotion-product-video-playbook.md) when writing or reviewing Remotion code.
Load [references/remotion-rules-index.md](references/remotion-rules-index.md) and then only the specific files needed from `references/remotion-rules/`.

### 5) Add Ancillary Assets (Optional but Useful)

Use Freepik-generated assets only to support scenes:

- Nano Banana 2 or Freepik image models for hero stills/background art.
- Kling for short inserts or transition clips.
- ElevenLabs voiceover and music endpoints for narration and soundtrack.

Do not let generated clips replace the whole narrative structure.

Load [references/freepik-ancillary-assets.md](references/freepik-ancillary-assets.md) when planning asset generation.

### 6) Assemble, QA, and Render

Run this QA gate before rendering:

- Problem is clear in first 3-5 seconds.
- Solution is introduced before midpoint.
- Use cases are concrete scenarios, not feature bullets.
- CTA includes an explicit incentive.
- Audio levels keep voiceover intelligible over music.

Then render via Remotion CLI or renderer API.

## Creative Rules

- Prefer visual metaphors and outcomes over UI tours.
- Keep one message per scene.
- Use motion to direct attention, not decorate.
- Show benefits in context: who uses the product, when, and what changes.
- Keep CTA simple and singular.

## Deliverables

Produce these outputs for each request:

1. AIDA script draft.
2. Scene plan JSON (`plan.json`).
3. Remotion project from the selected bundled template customized for the brief.
4. Asset manifest listing generated inputs and their intended scene usage.
5. Final render command(s).

## References

- Remotion implementation details: [references/remotion-product-video-playbook.md](references/remotion-product-video-playbook.md)
- Remotion rules navigator: [references/remotion-rules-index.md](references/remotion-rules-index.md)
- Freepik ancillary generation recipes: [references/freepik-ancillary-assets.md](references/freepik-ancillary-assets.md)
- Template chooser: [references/template-showcase.md](references/template-showcase.md)
- Packaging and publishing: [references/publishing-clawhub.md](references/publishing-clawhub.md)
- ShellBot Team: [getshell.ai](https://getshell.ai)

Use this skill for product marketing videos only. For other video categories, use a different skill.
