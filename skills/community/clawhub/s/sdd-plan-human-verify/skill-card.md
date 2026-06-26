## Description: <br>
Generates a human verification checklist from a completed spec-plan.md, with [A] automated and [H] human substeps covering all verification items for AI-driven acceptance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn SDD plan and design documents into a detailed Chinese acceptance checklist. It separates shell-checkable steps from human visual or interaction checks so a follow-on verifier can execute automated preparation and ask focused yes/no questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated checklist commands may later be run automatically by another verifier, including installs, long-running services, database migrations, or other workspace-changing commands. <br>
Mitigation: Review the generated spec-human-verify.md before running a follow-on verifier, especially all [AUTO] and [AUTO/SERVICE] entries that install packages, migrate data, delete files, use sudo, touch secrets, or affect cloud or account resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/sdd-plan-human-verify) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown checklist with inline shell commands and yes/no human verification prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated checklist is written in Chinese and uses [AUTO], [AUTO/SERVICE], [MANUAL], [A], and [H] tags to distinguish automated execution from human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
