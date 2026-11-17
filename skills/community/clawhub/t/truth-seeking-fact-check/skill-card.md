## Description:

Truth Seeking Fact Check helps agents evaluate text for possible AI hallucinations or misinformation, producing credibility scores, highlighted issues, suggestions, and optional blockchain-evidence checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangtaozhanshen](https://clawhub.ai/user/tangtaozhanshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to run local fact-checking workflows over single texts, batches, or scheduled checks, then review credibility scores, confidence details, problematic sentences, and improvement suggestions. It is suited for content review support, not as a sole authority for truth or professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive checked text may be exposed if external data sources are enabled.

Mitigation: Use the skill with external data sources disabled unless sending search queries to Brave is acceptable for the deployment.

Risk: Blockchain verification should not be treated as strong proof of authenticity.

Mitigation: Treat blockchain evidence as an advisory signal and require independent review before relying on the result.

Risk: Unpinned dependencies and broad permissions can increase production deployment risk.

Mitigation: Pin dependencies, review requested permissions, and run a security review before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangtaozhanshen/skills/truth-seeking-fact-check)
- [Artifact README and usage guide](artifact/SKILL.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON objects or Markdown reports with scores, confidence details, issue annotations, suggestions, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-text, batch, and optional scheduled checks; results are advisory and depend on configured local and external data sources.]

## Skill Version(s):

1.5.0 (source: server release metadata, manifest.json, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
