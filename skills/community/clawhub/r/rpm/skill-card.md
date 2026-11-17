## Description:

RPM Package Management provides RPM packaging guidance for spec files, rpmbuild and mock workflows, rpmlint checks, macro expansion, dependency handling, and common build-system templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and packaging engineers use this Chinese-language skill as a reference for creating, reviewing, building, linting, and updating RPM packages across RPM-based distributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes some RPM guidance may be overconfident or stale.

Mitigation: Verify distro-specific packaging rules and current macro behavior against the target distribution before applying recommendations.

Risk: RPM build or package installation commands can modify host systems when run directly.

Mitigation: Run builds in mock, containers, or other unprivileged isolated environments, and avoid install or remove commands on a main system unless that change is intended.

Risk: Dependency installation guidance can introduce unreviewed or nondeterministic inputs.

Mitigation: Prefer reviewed package sources, deterministic dependency inputs, and clean rebuilds when converting guidance into build steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidongkl/skills/rpm)
- [Publisher profile](https://clawhub.ai/user/weidongkl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with RPM spec snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language RPM packaging reference; no hidden code, persistence, credential access, or automatic execution identified in security evidence.]

## Skill Version(s):

4.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
