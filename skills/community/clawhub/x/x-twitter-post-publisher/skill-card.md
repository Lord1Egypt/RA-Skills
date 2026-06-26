## Description: <br>
Publish posts to X/Twitter from plain text or markdown post banks using OpenCLI with an already logged-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish prepared X/Twitter posts from direct text or markdown post banks through an existing logged-in browser session. It supports workflows that need reliable X composer activation, character checks, and post verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post publicly from an already logged-in X/Twitter account. <br>
Mitigation: Require the agent to show the exact post text, selected markdown label, and active account, then obtain explicit approval before clicking Post. <br>
Risk: The artifact references scripts/publish-x-post.ps1, but that script is not included in the artifact. <br>
Mitigation: Verify or replace the missing PowerShell script before running any publishing command. <br>
Risk: X's Draft.js composer can show text visually while the Post button remains disabled or the internal editor state is stale. <br>
Mitigation: Use native clipboard paste, verify the Post button is enabled, and verify publication through search or the author's timeline before claiming success. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Release Page](https://clawhub.ai/jinhuadeng/x-twitter-post-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with inline PowerShell and OpenCLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational posting guidance and command examples; the skill itself does not include the referenced publish-x-post.ps1 script in this artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
