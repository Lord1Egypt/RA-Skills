## Description: <br>
Automates Twitter/X posting, engagement, direct messages, follows, and profile lookup through the inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Twitter/X automation commands and workflows, including posting text or media, liking, retweeting, sending DMs, following users, and retrieving profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, delete, message, follow, like, or retweet from a connected Twitter/X account. <br>
Mitigation: Require explicit human review before running any command that changes account state. <br>
Risk: The quick start uses a curl-to-shell installer for the inference.sh CLI. <br>
Mitigation: Prefer manual CLI installation and checksum verification when possible, and revoke the connected session when automation is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/twitter-automation) <br>
- [X.com Integration](https://inference.sh/docs/integrations/x) <br>
- [X.com Integration Example](https://inference.sh/docs/examples/x-integration) <br>
- [Apps Overview](https://inference.sh/docs/apps/overview) <br>
- [Manual CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may perform live Twitter/X account actions through inference.sh and should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
