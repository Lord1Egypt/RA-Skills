## Description: <br>
Create, edit, and share AI-generated videos using tellers.ai, including media upload, AI-assisted generation, subtitles, overlays, music, exports, and public previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxdunc](https://clawhub.ai/user/yxdunc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and video creators use this skill to operate the Tellers CLI for uploading footage, generating videos, exporting projects, and sharing previews. It is suited for news summaries, highlight reels, promotional edits, and client video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload user media to Tellers. <br>
Mitigation: Upload only media the user is allowed to send to Tellers and verify the destination before running upload commands. <br>
Risk: Tellers actions can spend credits for uploads, exports, and generation. <br>
Mitigation: Confirm credit-spending actions with the user before running commands that upload, generate, or export media. <br>
Risk: Assets or previews can be made public. <br>
Mitigation: Explicitly confirm before using commands that enable anonymous read access or share public preview links. <br>
Risk: The workflow requires a Tellers API key. <br>
Mitigation: Use a dedicated API key, avoid storing it where unrelated tools can read it, and verify the Homebrew tap before installing the CLI. <br>


## Reference(s): <br>
- [Tellers API Documentation](https://www.tellers.ai/docs/dev/api) <br>
- [Tellers CLI Source](https://github.com/tellers-ai/tellers-cli) <br>
- [Tellers App](https://app.tellers.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/yxdunc/tellers) <br>
- [Publisher Profile](https://clawhub.ai/user/yxdunc) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Tellers asset IDs, project IDs, chat IDs, app URLs, public preview URLs, and export guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
