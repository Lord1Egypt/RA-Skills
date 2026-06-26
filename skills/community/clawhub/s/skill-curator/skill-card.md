## Description: <br>
Skill Curator watches Discord messages formatted as a keyword plus URL, extracts the linked content, and creates or appends a matching knowledge skill in a GitHub skill repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eeyan2025-art](https://clawhub.ai/user/eeyan2025-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge managers use this skill to turn Discord link submissions into persistent, keyword-organized Skill files in a GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically turn Discord links into persistent repository changes without documented review or authorization controls. <br>
Mitigation: Control the Discord trigger surface, prefer pull requests or manual review before pushes, and review generated Skill changes before deployment. <br>
Risk: Repository write tokens and extracted URL content can affect a persistent Skill repository. <br>
Mitigation: Use a fine-grained token limited to the intended repository, sanitize keywords into safe paths, and treat extracted URL content as untrusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eeyan2025-art/skill-curator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown Skill files with supporting text, commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create new skill files or append dated source summaries to existing Skill markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
