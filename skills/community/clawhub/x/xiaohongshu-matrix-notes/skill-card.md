## Description: <br>
Supports Xiaohongshu/RedNote matrix-account image-and-text note production by collecting benchmark-account examples, generating product lifestyle or try-on images, building covers, and drafting style-matched captions for women's fashion seeding accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, content operators, and developers use this skill to create Xiaohongshu/RedNote seeding-account notes from benchmark account analysis and product images, including generated visuals, cover layouts, captions, and self-check guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large-scale benchmark-account style mimicry or real-person likeness reuse can confuse audiences or copy a creator's identity. <br>
Mitigation: Use licensed or consented references, avoid impersonation, require approval for persona and pilot images, and review generated content before publication. <br>
Risk: Third-party platform scraping and reuse of account, product, model, or face-reference data may exceed account rights or platform rules. <br>
Mitigation: Confirm rights to every dataset and image input, review Xiaohongshu/RedNote and provider terms, and define retention and deletion practices for collected notes and generated assets. <br>
Risk: Sensitive credentials are required for TikHub and Ofox API access. <br>
Mitigation: Keep TIKHUB_TOKEN and OFOX_API_KEY out of generated outputs and shared artifacts, rotate exposed keys, and use scoped credentials where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/xiaohongshu-matrix-notes) <br>
- [Lessons and operational notes](artifact/references/lessons.md) <br>
- [Persona and style template](artifact/references/persona-and-style.md) <br>
- [Ofox image API endpoint](https://api.ofox.ai/v1) <br>
- [TikHub Xiaohongshu API endpoint](https://api.tikhub.io/api/v1/xiaohongshu/app_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python utility scripts; generated working outputs may include JSON summaries, downloaded cover images, generated PNG images, and captions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided TikHub and Ofox credentials, product images, benchmark-account inputs, and human review of persona, pilot, likeness, product fidelity, platform compliance, and final publishing choices.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
