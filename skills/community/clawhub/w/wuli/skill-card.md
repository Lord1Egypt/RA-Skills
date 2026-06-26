## Description: <br>
Wuli Skill helps agents generate and edit AI images and videos through the Wuli.art open platform API using text prompts and optional reference media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sir1st-inc](https://clawhub.ai/user/sir1st-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to generate images, edit reference images, create videos from text, and animate or transform supplied media through Wuli.art models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images or videos may be sent to Wuli.art and its upload storage for processing. <br>
Mitigation: Use only media appropriate for that service; do not submit private, regulated, or confidential content. <br>
Risk: Remote media URLs may be fetched and re-uploaded, which can expose internal or private URLs. <br>
Mitigation: Use public, intended-for-sharing URLs only, and avoid internal network or access-controlled media links. <br>
Risk: Downloaded outputs are opened automatically by the local OS viewer. <br>
Mitigation: Run the skill only in environments where opening generated media is acceptable, or review this behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sir1st-inc/skills/wuli) <br>
- [Wuli.art](https://wuli.art) <br>
- [Wuli Open Platform API documentation](artifact/references/【呜哩Wuli】开放平台 API 文档.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and WULI_API_TOKEN; selected media may be uploaded to Wuli.art storage and downloaded results may open in the local OS viewer.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
