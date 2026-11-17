## Description:

Assesses post-grooming pet images for mat residue, dandruff coverage, and coat smoothness, then returns a grooming score and targeted re-grooming suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and groomers use this skill to assess post-grooming cat, dog, or other pet images and receive a grooming score, visual observations, and follow-up grooming suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags account creation, identity, and credential handling as unexplained for this grooming skill.

Mitigation: Ask the publisher to clarify these behaviors before installing or supplying credentials.

Risk: Images and videos may be transferred to a remote analysis service, and report history or exports may be accessed through that service.

Mitigation: Confirm the service's data handling before submitting media, and avoid images you do not want processed remotely.

Risk: The security assessment reports that analysis may still run with the export-only option; its scan was partial and does not establish malicious intent.

Mitigation: Do not rely on that option to prevent analysis or media transfer; review the complete package and clarify behavior with the publisher before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-grooming-effect-assessment-analysis)
- [API reference](references/api_doc.md)
- [Skill usage demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis text with JSON result content, grooming suggestions, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save report output to a file.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
