## Description:

Audits whether AI search systems can read a website and identify its business, applies safe visibility fixes, and opens a reviewable pull request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[searchiz](https://clawhub.ai/user/searchiz)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and developers use this skill to check whether AI search systems can access and understand a site's public information, apply safe visibility fixes, and prepare them for review in a pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the audit executes searchiz-audit@1.1.0, whose package code was unavailable for verification.

Mitigation: Review the pull request, especially crawler permissions and server-header changes, before merging.

## Reference(s):

- [searchiz-audit source repository](https://github.com/searchiz/searchiz-audit)
- [Searchiz](https://searchiz.com)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Code, Configuration instructions, Files, Shell commands]

**Output Format:** [JSON audit report, repository changes, and pull request description]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changes that require business facts or owner confirmation are left for review.]

## Skill Version(s):

1.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
