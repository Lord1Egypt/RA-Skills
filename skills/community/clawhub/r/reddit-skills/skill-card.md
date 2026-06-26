## Description: <br>
Reddit automation skill collection for authentication, content publishing, search and discovery, social interactions, and compound Reddit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1146345502](https://clawhub.ai/user/1146345502) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to operate Reddit through a logged-in browser session, including browsing, searching, posting, commenting, voting, saving, and multi-step content operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives a local browser extension and Python bridge control over a logged-in Reddit browser session. <br>
Mitigation: Install only when comfortable with that control, use a dedicated browser profile or secondary Reddit account, and keep the bridge server closed when not actively using the skill. <br>
Risk: The skill can perform account actions such as posting, commenting, voting, saving, and logging out. <br>
Mitigation: Review every post, comment, vote, and save action before execution, and keep operation frequency low to reduce rate-limit or account-restriction risk. <br>
Risk: Untrusted local processes could try to interact with the local bridge while it is running. <br>
Mitigation: Avoid leaving the extension and bridge enabled around untrusted local processes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/1146345502/reddit-skills) <br>
- [Project homepage](https://github.com/1146345502/reddit-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON results from the local CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing workflows route through a Python CLI and may summarize Reddit page data, post/comment drafts, and operation results.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
