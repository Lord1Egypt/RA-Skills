## Description:

Content Catcher helps agents capture web pages and media, convert content to Markdown, PDF, or JSON, extract structured page elements, translate content, and download video when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to collect web content, media assets, structured page data, translations, and downloadable video into reusable local outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed command-injection paths in shell-based execution.

Mitigation: Replace shell-based execSync calls with argument-array APIs, validate inputs, and run the skill in a sandbox until patched.

Risk: Under-disclosed media and key-handling behavior.

Mitigation: Disable or remove key capture, Cookie header rewriting, and page-to-background pass-through unless explicitly required and reviewed.

Risk: Webpage and media downloads can expose users to untrusted sources or unauthorized media capture.

Mitigation: Use trusted URLs only, review media download legality before use, and keep network/file access constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/xia-zhua-zhua)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Markdown, PDF, JSON, text summaries, downloaded media files, and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local files and download webpage or media content.]

## Skill Version(s):

4.0.1 (source: server release metadata; artifact frontmatter says 4.0.0 and package.json says 2.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
