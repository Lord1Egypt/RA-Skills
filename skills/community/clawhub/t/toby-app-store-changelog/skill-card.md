## Description: <br>
Create user-facing App Store release notes by collecting and summarizing all user-impacting changes since the last git tag or a specified ref. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to turn local git history into concise, user-facing App Store release notes. It helps collect changes since a tag or ref, filter out internal-only work, and draft benefit-focused bullets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local commit messages and file paths, which may contain private project details. <br>
Mitigation: Run it only on repositories whose history can be summarized, and review generated notes before sharing them outside the project. <br>
Risk: Release notes may misclassify ambiguous or internal-only changes as user-visible. <br>
Mitigation: Validate every bullet against the selected git range and ask for clarification when the user impact is unclear. <br>


## Reference(s): <br>
- [App Store Release Notes Guidelines](references/release-notes-guidelines.md) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-app-store-changelog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown bullet list with optional title and supporting shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers 5 to 10 concise, user-facing bullets and filters internal-only changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
