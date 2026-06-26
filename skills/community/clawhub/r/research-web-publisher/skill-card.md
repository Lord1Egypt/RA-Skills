## Description: <br>
Publishes research reports as visually rich HTML pages, pushes them to a configured GitHub repository, and returns an htmlpreview link backed by jsDelivr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2239721014-ops](https://clawhub.ai/user/2239721014-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content operators use this skill to turn research or analysis material into an online HTML report, publish it to GitHub, and share a China-accessible preview link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to publish report content online, which can expose private, proprietary, or unapproved material. <br>
Mitigation: Before publishing, confirm the exact repository, branch, files, preview URL, and that the report is approved for public release. <br>
Risk: Broad automatic trigger terms can cause the publishing workflow to activate during ordinary research or analysis requests. <br>
Mitigation: Require explicit user approval before running git add, commit, push, or sharing a public preview link. <br>
Risk: Publishing through GitHub and jsDelivr depends on a public repository and can make changes broadly accessible. <br>
Mitigation: Use a dedicated publishing repository, review diffs before push, and avoid committing secrets, drafts, or restricted data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2239721014-ops/research-web-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/2239721014-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with HTML preview link, plus generated HTML/code files and shell commands when publishing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may commit and push report files to a configured public GitHub repository and instructs the agent to share the htmlpreview URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
