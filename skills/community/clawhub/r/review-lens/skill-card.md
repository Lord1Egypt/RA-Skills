## Description: <br>
Finds logical errors, silent edge cases, performance cliffs, implicit assumptions, and other defects that can be missed in human code review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Review Lens to examine code for correctness risks, edge cases, failure paths, state transition problems, performance cliffs, security surfaces, and assumptions that may not be obvious during ordinary review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code review prompts may process sensitive source code or secrets supplied by the user. <br>
Mitigation: Avoid pasting secrets, private keys, regulated data, or proprietary code unless the agent environment is approved for that data. <br>
Risk: Review findings may be incomplete, incorrect, or misleading if applied without engineering judgment. <br>
Mitigation: Treat findings as review guidance and have a developer validate proposed changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jcools1977/review-lens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown code review findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only review guidance; no executable code or external API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
