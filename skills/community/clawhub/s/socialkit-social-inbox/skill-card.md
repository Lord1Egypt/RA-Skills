## Description:

Gathers comments and replies on the user's published YouTube videos and Facebook, Instagram and Threads posts into one inbox, drafts replies in the user's voice, and sends only the replies the user approved. Use when the user wants to read or answer comments across their social accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Social account owners use this skill to collect comments from supported social posts, prepare useful reply drafts, and review them before sending. It also lists YouTube comments for manual replies in YouTube Studio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval does not lock all reply destinations and sending account details.

Mitigation: Before sending, confirm approval covers the reply text, platform, destination, and sending account.

Risk: The script supports additional platforms beyond those advertised.

Mitigation: Require explicit opt-in for each additional platform before enabling sends. Use a dedicated posts folder, keep the inbox private, and delete it when finished.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-social-inbox)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON comment and reply files with human-readable review guidance and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply drafts are prepared for review; YouTube comments are listed for manual response.]

## Skill Version(s):

0.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
