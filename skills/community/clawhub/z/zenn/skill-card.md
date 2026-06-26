## Description: <br>
Publish Zenn articles by managing Markdown in a GitHub-connected repository (push/PR -> merge) and previewing with Zenn CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tachi-koma-x](https://clawhub.ai/user/tachi-koma-x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical writers use this skill to draft, preview, review, and publish Zenn articles through a GitHub-connected repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing with published: true or merging without review can expose draft content or confidential information. <br>
Mitigation: Review diffs and PRs before merging, keep drafts unpublished until ready, and verify content before changing published to true. <br>
Risk: Running npm or npx commands in the wrong repository, or with an untrusted Zenn CLI version, can make unintended local changes. <br>
Mitigation: Run Zenn CLI commands only in the intended repository and use a trusted or pinned zenn-cli version where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tachi-koma-x/zenn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell command blocks and article front matter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance expects users to review PR diffs and publishing flags before merging.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
