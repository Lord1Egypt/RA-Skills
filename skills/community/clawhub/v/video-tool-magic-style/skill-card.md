## Description: <br>
Apply WeryAI magic style transfer to an existing HTTPS video (video-magic). Use when the user wants preset visual restyling of a video URL, not text-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to restyle an existing public HTTPS video through WeryAI's magic-style workflow. It is intended for preset video restyling, not text-to-video generation or local file upload workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends the selected public video URL and style option to WeryAI's API for paid processing. <br>
Mitigation: Confirm the video URL and any non-default style with the user before submission, and use dry-run validation when checking inputs. <br>
Risk: The skill requires WERYAI_API_KEY for API access. <br>
Mitigation: Keep the API key out of files and use a scoped key where available. <br>
Risk: Public video URLs may expose sensitive content or embedded access tokens to the external API. <br>
Mitigation: Avoid URLs containing private tokens or sensitive media, and only submit content the user is comfortable sending to WeryAI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-magic-style) <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and final video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit and poll WeryAI video-magic tasks; dry-run mode validates JSON without a paid submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
