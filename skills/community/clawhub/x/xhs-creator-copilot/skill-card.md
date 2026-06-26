## Description: <br>
Local assistant for Xiaohongshu futures and finance creators that drafts posts, replies, comment triage, cover images, compliance checks, and local files while keeping publishing and messaging manual. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujietech](https://clawhub.ai/user/yujietech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Xiaohongshu creators in futures and finance use this skill to prepare compliant draft notes, response candidates, comment triage, cover images, and local output files. The user remains responsible for reviewing content, applying required AI disclosures, and manually publishing or sending any final material. <br>

### Deployment Geography for Use: <br>
Global, subject to Xiaohongshu platform rules and applicable AI-content labeling requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Humanizer workflows could be misused to hide AI authorship. <br>
Mitigation: Require explicit AI content labels, preserve required AI statements and cover-image badges, and refuse requests to remove or bypass those disclosures. <br>
Risk: Finance drafts may become misleading if treated as investment advice or if they invent personal trading experience. <br>
Mitigation: Require human review, investment-risk disclaimers, and rejection of fabricated experience, guaranteed returns, calls, or account-opening inducements. <br>
Risk: Pasted DMs, screenshots, notification pages, and FAQ examples may contain personal data that is retained locally. <br>
Mitigation: Ask users to redact sensitive details before use, keep generated outputs and FAQ examples local, and periodically review or delete retained files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujietech/xhs-creator-copilot) <br>
- [README](README.md) <br>
- [Skill entrypoint](SKILL.md) <br>
- [Content drafting workflow](references/content.md) <br>
- [Humanizer workflow](references/humanizer.md) <br>
- [Compliance guide](references/compliance-guide.md) <br>
- [Local output specification](references/local-output.md) <br>
- [Cover image workflow](references/cover-image.md) <br>
- [Reply draft workflow](references/faq-draft.md) <br>
- [Comment triage workflow](references/reply-triage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, SVG, PNG, and local file paths depending on the requested workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local review and manual copy or upload; the skill does not publish to Xiaohongshu or send messages automatically.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
