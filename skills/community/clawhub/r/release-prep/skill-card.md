## Description: <br>
Deep code audit + documentation sync + release preparation for Python packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morozsm](https://clawhub.ai/user/morozsm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers of Python packages use this skill to audit tests, lint, dead code, documentation, version consistency, and release readiness, then optionally prepare fixes, changelogs, version bumps, tags, builds, and PyPI publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify repository files during fix and release workflows. <br>
Mitigation: Run audit mode first, work on a clean branch, and review diffs before applying fixes. <br>
Risk: Release mode can bump versions, create commits and tags, publish packages to PyPI, and push tags. <br>
Mitigation: Require explicit approval before version bumps, commits, tags, PyPI uploads, or pushing tags, and use scoped PyPI tokens. <br>
Risk: The security review notes broader triggers and incomplete confirmation safeguards. <br>
Mitigation: Install only when an agent should help prepare Python package releases, and avoid running it on untrusted repositories. <br>


## Reference(s): <br>
- [Release Prep ClawHub page](https://clawhub.ai/morozsm/release-prep) <br>
- [Publisher profile](https://clawhub.ai/user/morozsm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown release-readiness report with shell commands, changelog text, and proposed code or documentation changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports audit, fix, and release modes; release mode may propose or perform version updates, commits, tags, package builds, PyPI uploads, and tag pushes after confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
