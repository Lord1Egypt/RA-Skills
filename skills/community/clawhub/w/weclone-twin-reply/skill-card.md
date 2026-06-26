## Description: <br>
Build a review-gated digital twin reply from persona markdown, persona examples, and live conversation context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xming521](https://clawhub.ai/user/xming521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to assemble a persona-grounded prompt package and produce a candidate reply that imitates a specific user's messaging style. It is designed for review-gated drafting and keeps outbound sending conditional on explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persona files and recent conversation snippets may contain private or sensitive information when assembled into a model prompt. <br>
Mitigation: Use only the persona files and dialogue needed for the draft, keep secrets out of ai_twin/, and remove unrelated Markdown files before rendering. <br>
Risk: A generated reply could imply promises, reveal private information, or misrepresent the user if sent without review. <br>
Mitigation: Keep the approval gate in place, review risk flags, and send only after explicit user confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xming521/weclone-twin-reply) <br>
- [WeClone Skill Homepage](https://github.com/xming521/WeClone-Skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown draft response with risk flags and a reviewer note, plus shell command guidance for rendering the isolated prompt package.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow produces a reviewable candidate reply and requires explicit approval before any send step.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
