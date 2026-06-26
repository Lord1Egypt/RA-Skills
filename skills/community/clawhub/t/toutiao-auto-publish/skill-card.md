## Description: <br>
Automates publishing short text posts and optional images to the Toutiao micro-posting platform through a logged-in browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devilsbibble](https://clawhub.ai/user/devilsbibble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators can use this skill to prepare and publish Toutiao micro-posts with text, topics, and optional images from an agent workflow. It is intended for accounts where the operator can review the final content and publication settings before posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content through a logged-in Toutiao browser session without a built-in final approval gate. <br>
Mitigation: Require manual review of the exact final text, image, topics, and publication settings before allowing the browser action that posts content. <br>
Risk: Remote browser debugging can expose an authenticated browser session if left open or reused broadly. <br>
Mitigation: Use a dedicated Toutiao browser profile for this skill and close the remote debugging port immediately after use. <br>
Risk: File-based content and image inputs may unintentionally include sensitive or incorrect material. <br>
Mitigation: Avoid passing sensitive files and verify any file or image path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devilsbibble/toutiao-auto-publish) <br>
- [Toutiao creator platform](https://mp.toutiao.com) <br>
- [Toutiao micro-post publish page](https://mp.toutiao.com/profile_v4/weitoutiao/publish?from=toutiao_pc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Command-line arguments and browser automation actions, with success or error screenshots written to the desktop] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts post content, optional topic tags, optional image paths, file-based content input, and browser mode flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
