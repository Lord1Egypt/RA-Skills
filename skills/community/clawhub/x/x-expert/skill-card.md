## Description: <br>
X Expert is a conversational X (Twitter) publishing assistant that helps users gather context, draft posts, generate images, review content, and publish tweets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thousandsky2024](https://clawhub.ai/user/thousandsky2024) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, social media operators, marketers, founders, and developers use this skill to plan X posts, generate draft copy and images, preview publication settings, and publish or delete tweets through a guided workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish posts and delete tweets using live X account credentials. <br>
Mitigation: Use revocable, least-privilege tokens and install only for accounts where these actions are acceptable. <br>
Risk: Direct publishing or deletion can change a live account without enough review. <br>
Mitigation: Keep manual review enabled and require confirmation before publishing, scheduling, media posting, thread posting, or deletion. <br>
Risk: Search queries, tweet drafts, and image prompts may expose sensitive material to external services. <br>
Mitigation: Do not include confidential information in search or image prompts, and review generated content before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thousandsky2024/x-expert) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thousandsky2024) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown, with optional shell commands, generated prompts, publication summaries, and post URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured X API credentials and optional search or image-generation service credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
