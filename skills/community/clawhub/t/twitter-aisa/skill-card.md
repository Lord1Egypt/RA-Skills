## Description: <br>
Twitter/X command center for agent-assisted research, monitoring, watchlists, and OAuth-approved posting through AIsa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research Twitter/X activity, monitor accounts or topics, and publish approved posts with text or media through OAuth-gated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OAuth and posting client may print the AIsa API key in normal command output. <br>
Mitigation: Run authorization and posting only in trusted sessions, avoid sharing captured output, redact exposed keys, and rotate any key that has appeared in logs. <br>
Risk: The skill can post externally to Twitter/X after OAuth approval. <br>
Mitigation: Require explicit user approval for publishing and verify API confirmation before reporting that a post succeeded. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/bibaofeng/twitter-aisa) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa Twitter OAuth guide](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output from bundled Python clients] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; posting sends OAuth requests, post content, and approved media uploads to AIsa.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
