## Description: <br>
Post and reply to X/Twitter and Farcaster with text and images, including multi-account posting, draft previews, character validation, threads, replies, image uploads, and optional text variation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Callmedas69](https://clawhub.ai/user/Callmedas69) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to draft, preview, publish, and reply to posts across X/Twitter and Farcaster from command-line workflows. It is suited for social posting workflows that need platform selection, multi-account support, image handling, thread splitting, link shortening, dry runs, and cost visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public posts and replies to X/Twitter and Farcaster. <br>
Mitigation: Use dry-run previews and confirmation prompts first, and run it only with dedicated low-risk social accounts. <br>
Risk: Farcaster posting can spend funds from a custody wallet. <br>
Mitigation: Keep only a small Farcaster wallet balance and check the balance before enabling automated posting. <br>
Risk: The --vary option is designed to avoid duplicate-content detection. <br>
Mitigation: Do not use --vary for platform-evasion or spam workflows; reserve it only for legitimate copy variation that complies with platform rules. <br>
Risk: Link shortening and image upload paths may share URLs or media with third-party services. <br>
Mitigation: Do not shorten private URLs or upload sensitive images through these workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Callmedas69/social-post) <br>
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) <br>
- [X API pricing](https://developer.twitter.com/#pricing) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce dry-run previews, public social posts, replies, thread splits, shortened links, and image-upload workflows when the scripts are executed.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
