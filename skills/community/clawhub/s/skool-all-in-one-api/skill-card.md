## Description: <br>
Provides full read and write access for agents to manage Skool members, posts, comments, mentions, events, and community administration workflows through an Apify actor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctala](https://clawhub.ai/user/ctala) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External community operators and agents use this skill to administer Skool communities through an Apify actor, including posts, comments, member approvals, member rejections, bans, events, and mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad Skool community write and moderation actions through a third-party Apify actor. <br>
Mitigation: Require explicit confirmation before creating, editing, deleting, approving, rejecting, or banning. <br>
Risk: The workflow depends on APIFY_TOKEN, Skool credentials, and reusable cookies. <br>
Mitigation: Treat tokens, passwords, and cookies as secrets, use the least-privileged Skool account available, and re-authenticate only when needed. <br>
Risk: Server security evidence reports insufficient safety guidance for broad administration and reusable-session access. <br>
Mitigation: Verify the Apify actor and publisher before installation and review each requested administrative action before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ctala/skool-all-in-one-api) <br>
- [Apify Actor Page](https://apify.com/cristiantala/skool-all-in-one-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and action parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include action names, JSON-like parameter examples, curl commands, and result formatting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
