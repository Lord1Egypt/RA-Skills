## Description: <br>
Generate videos with the NanoPhoto.AI Sora 2 API in text-to-video or image-to-video mode, with support for submission, status checks, and optional in-process polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit NanoPhoto.AI Sora 2 text-to-video or image-to-video generation requests, poll task status, and return resulting video URLs and generation metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, public image URLs, task IDs, and generation metadata are sent to the NanoPhoto.AI service. <br>
Mitigation: Use the skill only for content you are authorized to submit and avoid confidential, regulated, client-owned, or private media unless third-party processing is approved. <br>
Risk: The skill requires a NanoPhoto.AI API key. <br>
Mitigation: Store NANOPHOTO_API_KEY in the platform's secure environment-variable setting and do not paste the key into chat. <br>
Risk: Image-to-video mode requires public image URLs and does not support local or base64 image input. <br>
Mitigation: Provide only public image URLs that are safe to share with NanoPhoto.AI and avoid private image links. <br>


## Reference(s): <br>
- [Sora 2 Video Generation API Reference](references/api.md) <br>
- [NanoPhoto.AI homepage](https://nanophoto.ai) <br>
- [NanoPhoto.AI API key settings](https://nanophoto.ai/settings/apikeys) <br>
- [ClawHub skill page](https://clawhub.ai/nanophotohq/sora-2-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task IDs, status responses, video URLs, generation time, credits used, and error guidance from the NanoPhoto.AI API.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
