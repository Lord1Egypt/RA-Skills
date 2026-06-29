## Description: <br>
Use before making a private repository public, before the first push of a new public repo, or when the user asks "is this safe to publish", "check for leaks", or wants a pre-publication scan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill before publishing a repository to check tracked files, Git history, repository hygiene, and public remote state for secrets or identifying content. It returns a ship-or-fix-first verdict with evidence and concrete remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remediation guidance can include destructive Git operations such as history rewriting, force-pushing, deleting branches or tags, or recreating a repository. <br>
Mitigation: Review proposed commands before running them, keep an external backup of the repository, and verify cleanup from a fresh clone. <br>
Risk: A clean working tree scan can miss secrets or identifying content that remain in Git history or public remote refs. <br>
Mitigation: Run both working-tree and history checks, inspect remote backup branches and tags, and rotate any credential that was ever committed. <br>


## Reference(s): <br>
- [content-guard](https://github.com/solomonneas/content-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with a checklist table, verdict, evidence, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include destructive Git remediation commands for reviewer approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
