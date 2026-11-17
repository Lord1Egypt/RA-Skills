## Description:

A local, offline scanner that checks source code, configuration, environment files, logs, and Git history for suspected secrets, then reports findings as text, JSON, or CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to check authorized code, configuration, and Git history for suspected credentials before committing, releasing, or sharing material. It can also inspect a single value or redact text; findings need human verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can contain complete secrets even when masking is enabled.

Mitigation: Keep reports private until masking has been corrected and verified; inspect output before sharing.

Risk: Scanning paths without authorization or with an unnecessarily broad scope can expose sensitive material.

Mitigation: Limit scans to authorized paths and data.

Risk: Installing or updating the skill can change files in the chosen destination.

Mitigation: Pin the reviewed package version, choose one installation destination, and back up an existing installation before updating.

## Reference(s):

- [Rules and detection categories](artifact/references/rules.md)
- [Entropy and verification](artifact/references/entropy-and-verification.md)
- [FAQ and troubleshooting](artifact/references/faq.md)
- [Integration guidance](artifact/references/integration.md)
- [Project homepage](https://github.com/YottaMeta/yotta-secret)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-secret)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Security analysis, Guidance]

**Output Format:** [Text, JSON, or CSV scan reports, with findings summarized for an agent in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are suspected secrets and require human verification. Reports may expose complete secrets despite masking.]

## Skill Version(s):

0.2.4 (source: frontmatter, package.json, changelog, released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
