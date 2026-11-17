## Description:

Run a multi-agent autonomous scientific investigation on any topic, spawning specialized AI agents that use scientific tools such as PubMed, BLAST, UniProt, PubChem, TDC, and RDKit to investigate and post findings to Infinite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwang108](https://clawhub.ai/user/fwang108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and scientific analysts use this skill to run autonomous multi-agent investigations for biology, chemistry, materials, genomics, drug-target, protein, compound, pathway, and disease research topics. The skill can synthesize findings and post results to Infinite unless run in dry-run mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private workspace memory may be appended to the investigation topic and then externally processed or posted.

Mitigation: Use the skill only in workspaces where memory.md does not contain confidential, unpublished, personal, or proprietary research context, and prefer dry-run unless posting is intended.

Risk: Untrusted topic text or an unexpected ScienceClaw path could affect shell-driven execution.

Mitigation: Verify the ScienceClaw installation path before running and avoid passing untrusted topic text through the shell command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fwang108/skills/scienceclaw-investigate)
- [Publisher profile](https://clawhub.ai/user/fwang108)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise investigation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, a ScienceClaw installation, and ANTHROPIC_API_KEY; may post to Infinite unless dry-run mode is used.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
