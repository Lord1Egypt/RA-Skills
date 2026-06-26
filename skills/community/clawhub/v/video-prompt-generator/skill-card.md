## Description: <br>
Generates polished Sora 2 text-to-video and image-to-video prompts through the NanoPhoto.AI Prompt Generator API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a topic or public image-guided scene idea into a production-ready Sora 2 prompt with configurable mode, technique, duration, and locale. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted topics and public image URLs are sent to NanoPhoto's API. <br>
Mitigation: Use only topics and public image URLs you are authorized and comfortable sharing with NanoPhoto. <br>
Risk: The NanoPhoto API key can be exposed if pasted into chat or command-line history. <br>
Mitigation: Store NANOPHOTO_API_KEY in the platform's secure skill environment. <br>
Risk: Prompt generation may consume NanoPhoto credits. <br>
Mitigation: Confirm that the account has sufficient credits and that the generation request is intentional before running the skill. <br>


## Reference(s): <br>
- [Sora 2 Prompt Generator API Reference](references/api.md) <br>
- [NanoPhoto.AI Homepage](https://nanophoto.ai) <br>
- [NanoPhoto API Key Settings](https://nanophoto.ai/settings/apikeys) <br>
- [ClawHub Skill Listing](https://clawhub.ai/nanophotohq/video-prompt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text prompt output with Markdown usage guidance and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The API returns streaming text; the bundled script prints the final assembled prompt text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
