## Description:

Sets up and launches three AI workflows—creative production, US market research, and lead research—on Windows 10/11, with a reviewable PowerShell setup, launcher, and health check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US small-business users and developers use the Windows kit to install, launch, and verify creative, market-research, and lead-research agent skills. The suite prepares research and outreach for human review; it does not place trades or send messages on the user's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags misleading Windows security assurances and broad script-unblocking advice for review.

Mitigation: Verify each script before unblocking it, and preserve Defender and workplace security policies.

Risk: The optional unsigned desktop app is separate from this skill and outside this inspection; a matching publisher-supplied hash does not establish safety.

Mitigation: Assess the separate app independently before use; do not treat its supplied hash as proof that it is safe.

Risk: The setup installs three separately distributed agent skills.

Mitigation: Review those skills independently before using them.

## Reference(s):

- [Install and Verify](references/install-and-verify.md)
- [FAQ](references/faq.md)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)
- [Publisher homepage](https://github.com/rapidworker1)
- [AI Creative Studio skill](https://clawhub.ai/rapidworker1/skills/ai-creative-studio)
- [AI Trading skill](https://clawhub.ai/rapidworker1/skills/ai-trading)
- [B2B Lead Research Agent skill](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent)
- [Separate Windows app download (unsigned; outside this inspection)](https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [PowerShell scripts, Markdown instructions, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 10/11 setup, launcher, and health-check workflow; installed agent skills produce their own outputs.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
