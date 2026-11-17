## Description:

元鉴 performs offline static triage of files and directories, producing hashes, file-type and entropy details, classified strings, PE/ELF header findings, risk clues, and IOC reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Security analysts and developers can use the skill to inspect authorized samples locally before deeper investigation. It computes hashes, identifies file types, measures entropy, extracts and classifies strings, parses PE/ELF headers, and exports preliminary risk clues and IOCs for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static risk scores and extracted strings are preliminary clues and may be misleading.

Mitigation: Treat findings as untrusted evidence and corroborate them through analyst review or other authorized analysis.

Risk: Scanning a directory that contains symlinks or writing reports alongside samples can create avoidable analysis ambiguity.

Mitigation: Use a dedicated sample directory, check file symlinks, and save reports separately from samples.

Risk: Installers can overwrite this skill's installed files, and an npm installation may fetch a release beyond the bundled files assessed here.

Mitigation: Choose a specific agent or installation directory, preview changes with --dry-run, and pin and verify npm releases.

## Reference(s):

- [Triage specification](references/triage-spec.md)
- [Risk model](references/risk-model.md)
- [Project repository](https://github.com/YottaMeta/yotta-triage)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-triage)
- [ClawHub release](https://clawhub.ai/yottameta/skills/yotta-triage)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Text, JSON, or Markdown triage reports; IOC data can be emitted as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-file and aggregate static findings; risk levels are preliminary clues, not verdicts.]

## Skill Version(s):

0.1.6 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
