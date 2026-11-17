## Description:

Safely triage and remediate GitHub dependency hygiene issues with explicit guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrummler17](https://clawhub.ai/user/mrummler17)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use RepoMedic to triage failing Dependabot updates, lockfile drift, transitive vulnerabilities, and dependency-related CI or Vercel failures while keeping remediation tightly scoped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency remediation may change lockfiles or package versions and affect build or runtime behavior.

Mitigation: Review planned file and version changes, prefer targeted patch or minor updates, and run install, build, test, lint, and audit checks where available before merging.

Risk: Medium- or high-risk remediation may expand into major upgrades, framework migrations, or uncertain dependency-tree changes.

Mitigation: Require explicit approval before non-trivial edits, present options with risk labels, and stop when the blast radius is unclear.

Risk: Repository write permissions can exceed the least privilege needed for dependency remediation.

Mitigation: Use a branch and PR workflow, avoid direct pushes to main or master, limit workspace changes to the target repository, and do not use unverified credentials.

## Reference(s):

- [RepoMedic on ClawHub](https://clawhub.ai/mrummler17/skills/repomedic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown sections with concise prose, file and version change summaries, validation results, and command snippets when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Low, Medium, or High risk level and requests approval for non-trivial or higher-risk dependency changes.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
