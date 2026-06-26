## Description: <br>
Remove watermarks from Sora 2 generated videos via the NanoPhoto.AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process Sora share-link videos through NanoPhoto.AI and receive a clean downloadable video URL. Users should confirm they are authorized to modify the media and that watermark removal is allowed for their use case. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Sora share links to NanoPhoto.AI as a third-party processor. <br>
Mitigation: Install only if third-party processing by NanoPhoto.AI is acceptable for the media being handled. <br>
Risk: The skill requires a NanoPhoto API key. <br>
Mitigation: Store NANOPHOTO_API_KEY in the skill environment or other secure runtime configuration, not in chat. <br>
Risk: Watermark removal can be inappropriate or unlawful for unauthorized media. <br>
Mitigation: Use the skill only on content the user is authorized to process and only when watermark removal is lawful and allowed. <br>


## Reference(s): <br>
- [Sora Watermark Removal API Reference](references/api.md) <br>
- [NanoPhoto.AI](https://nanophoto.ai) <br>
- [NanoPhoto API Key Management](https://nanophoto.ai/settings/apikeys) <br>
- [ClawHub Skill Page](https://clawhub.ai/nanophotohq/sora-watermark-remover) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a clean video URL from NanoPhoto.AI when processing succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
