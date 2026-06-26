## Description: <br>
Swaps faces in images and videos using WaveSpeed AI with image and video face-swap endpoints and multi-face targeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare WaveSpeed AI image or video face-swap requests, including selecting a target face when multiple people are present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive likeness media and may be misused for impersonation, fraud, harassment, sexualized edits, or deceptive publication. <br>
Mitigation: Use it only with media the user owns or has explicit permission to edit, and only when every identifiable person has consented. <br>
Risk: Uploading sensitive photos or videos to WaveSpeed may create privacy, retention, deletion, and output-use obligations. <br>
Mitigation: Check WaveSpeed privacy, retention, deletion, and output-use terms before uploading sensitive media. <br>
Risk: Untrusted or unvalidated media URLs can expose the workflow to unsafe inputs. <br>
Mitigation: Use trusted media sources, validate URLs before sending requests, and avoid loading untrusted user-provided media URLs. <br>
Risk: The WaveSpeed API key could be exposed if hardcoded or committed. <br>
Mitigation: Store WAVESPEED_API_KEY in environment variables or a secret management system and do not commit it to source control. <br>


## Reference(s): <br>
- [WaveSpeed API key access](https://wavespeed.ai/accesskey) <br>
- [ClawHub skill page](https://clawhub.ai/chengzeyi/wavespeed-face-swapper) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WaveSpeed model IDs, required API key setup, media URL guidance, target face selection, retry configuration, and error handling examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
