## Description: <br>
Generate install commands, GitHub README snippets, website cards, and copy text for a published ClawHub or Codex skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill publishers use this skill to generate consistent install commands, README snippets, landing-page cards, metadata, and launch copy for published ClawHub or Codex skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated install snippets or launch copy can be misleading if placeholder or incorrect skill metadata is supplied. <br>
Mitigation: Provide real slug, owner, version, and URL values, then review the generated Markdown, HTML, JSON, and social text before publishing. <br>
Risk: The --force option can replace existing generated output files. <br>
Mitigation: Use --force only when intentionally replacing prior snippets, or write to a separate output directory. <br>


## Reference(s): <br>
- [Skill Install Bridge on ClawHub](https://clawhub.ai/zack-dev-cm/skill-install-bridge) <br>
- [source-manifest.json](references/source-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown, HTML, JSON, and plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local install-copy files and prints generated metadata; existing outputs are overwritten only when --force is supplied.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
