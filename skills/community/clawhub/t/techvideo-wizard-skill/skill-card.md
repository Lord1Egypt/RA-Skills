## Description:

Interactive video script wizard that guides users through a structured 6-step process to collect product video requirements and generate a professional video script in Markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neshoir](https://clawhub.ai/user/neshoir)

### License/Terms of Use:

MIT-0

## Use Case:

Product, technical marketing, and GIS content teams use this skill to turn product or feature ideas into concise Chinese video scripts. The skill collects requirements step by step, checks for similar published content, applies terminology constraints, and produces a Markdown script for production handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow automatically searches external video platforms using the topic supplied after Step 1.

Mitigation: Do not enter confidential product names, unreleased campaign ideas, client details, or roadmap terms unless external search disclosure is acceptable.

Risk: The workflow saves the generated script as a Markdown file in the current working directory.

Mitigation: Run the skill in an appropriate workspace and review the generated file before sharing or publishing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neshoir/skills/techvideo-wizard-skill)
- [Video List Document](https://doc.weixin.qq.com/sheet/e3_AbEABwZhAOEELyAyNqUQ4urnvazrm?scode=AEwAawe0AAgC6L3AHYADQA7AahAB0&tab=BB08J2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown video script with structured sections and input records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first workflow; preserves configured SuperMap GIS terminology; writes a Markdown script file in the current working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
