## Description:

Extract and cite management guidance from SEC filings, then compare consecutive filings to summarize graded changes in the outlook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinghao0724](https://clawhub.ai/user/tinghao0724)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts and developers use the skill to find, cite, and compare management outlook statements in public SEC filings. It returns quoted filing passages and a retrieval coverage check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence because filing text is passed to an agent-capable CLI without explicit tool restrictions, creating prompt-injection risk.

Mitigation: Treat retrieved filings as untrusted input; review whether the Claude CLI fallback is needed and inspect the tools and local resources it can access.

Risk: Custom questions may be sent to a model provider, and dependency versions are not pinned.

Mitigation: Review provider data handling before sending sensitive questions and pin dependency versions for controlled deployments.

Risk: The security scan is incomplete because several referenced local paths were missing.

Mitigation: Review the missing paths and complete a full package security review before relying on the scan.

## Reference(s):

- [Project repository](https://github.com/TINGHAO0724/sec-guidance-skill)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Cited text or structured JSON with filing quotes and source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes retrieval coverage information; diff mode reports graded guidance changes with quotes from both filings.]

## Skill Version(s):

0.5.1 (source: frontmatter, changelog, released 2026-11-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
