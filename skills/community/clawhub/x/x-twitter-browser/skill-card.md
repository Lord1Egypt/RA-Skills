## Description:

Log in to X/Twitter via a real browser session and perform actions including posting, replying, reposting, liking, and bookmarking tweets with Playwright browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghanjun2](https://clawhub.ai/user/zhanghanjun2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate authenticated X/Twitter account actions through a saved browser session when they choose browser automation instead of the official X API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable X/Twitter login cookies are stored on disk and could allow account access if exposed.

Mitigation: Keep ~/.openclaw/auth/x-twitter/cookies.json private, do not commit or share it, and revoke the X session if exposure is suspected.

Risk: The skill can perform public account actions such as posting, replying, reposting, liking, and bookmarking.

Mitigation: Verify the session and manually confirm each action and content before execution.

Risk: Browser automation runs with disabled sandbox protections.

Mitigation: Run the automation in a constrained environment and prefer verified x.com URLs or tweet IDs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhanghanjun2/skills/x-twitter-browser)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands that operate a real X/Twitter account through Playwright and a saved browser session.]

## Skill Version(s):

1.0.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
