## Description:

Helps agents produce RedNote/Xiaohongshu matrix-account image and text notes at scale by analyzing benchmark accounts, generating product-oriented visuals, assembling covers, and drafting platform-style captions for women's fashion seeding accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and marketing teams use this skill to turn benchmark RedNote/Xiaohongshu accounts and product photos into repeatable image-plus-caption note production workflows. It guides account research, persona confirmation, product-scene prompting, cover generation, copywriting, and final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikHub and Ofox may receive account identifiers, prompts, product images, and persona or reference images during normal use.

Mitigation: Use non-sensitive inputs, review third-party service suitability before use, and keep API keys limited in scope.

Risk: The included scripts perform network requests and write generated or downloaded files into the working project.

Mitigation: Run the scripts in a controlled directory, review output names and paths before execution, and harden the scripts before use in sensitive environments.

Risk: Generated visuals or copy can misrepresent products, personas, or benchmark-account style if not reviewed.

Mitigation: Keep the documented human checkpoints for persona approval, pilot review, product-fidelity checks, and final full-result review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/xiaohongshu-matrix-notes)
- [Lessons](references/lessons.md)
- [Persona and style template](references/persona-and-style.md)
- [TikHub Xiaohongshu app_v2 API](https://api.tikhub.io/api/v1/xiaohongshu/app_v2)
- [Ofox API](https://api.ofox.ai/v1)
- [Noto Sans SC font asset](https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown-style workflow guidance with prompts, captions, shell command examples, configuration notes, and generated file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve generated images, covers, notes JSON, summaries, and downloaded reference covers when the helper scripts are executed.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
