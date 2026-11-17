# Video Character Reference Card

![Video Character Reference Card promo](assets/promo-1600x900.png)

Turn authorized character references into a reusable, cross-shot consistency card for Chinese video planning. It keeps appearance, wardrobe, and performance constraints clear without inventing missing facts.

## What it delivers

- A Markdown character card for storyboards and scripts
- Separate known facts from suggestions
- Cross-shot appearance, wardrobe, and action constraints
- A clear missing-information response when core inputs are absent

## Input and output

Provide an authorized reference description, story context, and styling constraints. See [the successful fixture](fixtures/success-input.json). The output structure is defined in [SKILL.md](SKILL.md), with a complete expected example in [fixtures](fixtures/success-expected.md).

This is a text-only Skill: it does not generate images or perform generic prompt optimization. No API, browser login, or third-party service is required.

## Self-test

```bash
python3 scripts/self_test.py
```

The test verifies package structure and fixtures only; it does not represent a claim of real-world model-quality validation.

## Sources and license

The implementation and copy are original. Public usage positioning was checked against [agentara/skills](https://github.com/agentara/skills) and its [video-storyboard Skill](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md); no source code or copy was reused. This repository is released under the [MIT-0](LICENSE).
