## Description: <br>
Creates and pushes date-based GitHub release tags, and matching GitHub Releases, for one or more configured microservice repositories from a selected branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyang777](https://clawhub.ai/user/sunyang777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to prepare and execute release tagging for configured service repositories, including selecting services, branches, date-based or explicit tag names, and optional dry-run review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled credentials and unrelated Feishu/Jenkins configuration may expose secrets or enable unintended access. <br>
Mitigation: Remove bundled credentials, rotate any exposed GitHub, Feishu, and Jenkins secrets, and require user-supplied least-privilege credentials before installation or use. <br>
Risk: The skill can create remote tags and GitHub Releases, and its script can operate across all configured repositories when no service scope is supplied. <br>
Mitigation: Confirm the exact repositories, branch, tag, and release behavior before execution; use dry-run mode for review when the user has not explicitly authorized the final write. <br>
Risk: Release creation or backfill behavior may surprise users who only expect tag creation. <br>
Mitigation: State that matching GitHub Releases are created or backfilled as part of the operation before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunyang777/tag-release) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include processed service names, branch, tag name, dry-run status, tag links, release links, PR metadata, and failure reasons.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
