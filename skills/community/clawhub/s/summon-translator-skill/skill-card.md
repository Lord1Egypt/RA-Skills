## Description:

Translate safety procedures, supplier documents, and Articulate Rise 360 eLearning content into 137+ languages using AI for supply chain, HSE, and L&D teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikirun2017-phache](https://clawhub.ai/user/nikirun2017-phache)

### License/Terms of Use:

MIT-0

## Use Case:

Supply chain managers, HSE professionals, and L&D teams use this skill to submit local compliance or training files to Summon Translator, poll jobs, and download translated files while preserving supported document structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen documents are sent to Summon Translator's external translation service.

Mitigation: Use the skill only for documents approved for external processing and review organizational handling requirements before upload.

Risk: A crafted local file path could cause unintended shell command execution in the sample upload command.

Mitigation: Avoid untrusted file paths and prefer a fixed script or API client that passes file paths as arguments instead of substituting them into shell text.

Risk: Safety-critical or legally binding translations may be inaccurate without domain review.

Mitigation: Have a qualified human reviewer validate regulatory submissions and safety-critical translated content before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikirun2017-phache/skills/summon-translator-skill)
- [Summon Translator API Docs](https://summontranslator.com/llms.txt)
- [Summon Translator Homepage](https://summontranslator.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUMMON_API_KEY and produces commands for submitting, polling, and downloading translation jobs.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
