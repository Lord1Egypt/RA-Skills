## Description: <br>
Skill Distributor generates platform-specific marketplace listings, README content, social posts, and publishing commands for an agent skill from its SKILL.md metadata, with optional GitHub publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmf515](https://clawhub.ai/user/gmf515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill creators use this skill to prepare a Skill package for distribution by validating SKILL.md metadata and generating platform-specific marketplace, repository, and social promotion materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional publishing path may handle GitHub credentials and write to a repository. <br>
Mitigation: Use generation-only mode unless publishing is required; if publishing, use a fine-grained token scoped to one repository and remove any tokenized remote URL after use. <br>
Risk: Generated distribution files and README updates may overwrite or introduce misleading project materials. <br>
Mitigation: Verify the destination repository, inspect generated diffs, and back up README.md before applying or publishing changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gmf515/skill-distributor) <br>
- [Platform Format Reference](artifact/references/platform-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, README content, shell command snippets, and platform-specific listing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated distribution materials under a distro/ folder and may provide optional GitHub publishing commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
