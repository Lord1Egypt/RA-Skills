## Description: <br>
Generate and extend videos using Google's Veo 3.1 Fast model via WaveSpeed AI, including text-to-video, image-to-video, video extension, up to 4K resolution, audio generation, and chained extensions up to 148 seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to configure WaveSpeed AI requests for text-to-video, image-to-video, and Veo-generated video extension workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WaveSpeed API key and can expose credentials if copied into source files or logs. <br>
Mitigation: Keep WAVESPEED_API_KEY in environment variables or secret storage and do not hardcode or commit it. <br>
Risk: Image-to-video and video extension workflows may upload sensitive media to WaveSpeed AI. <br>
Mitigation: Avoid uploading sensitive images or videos unless WaveSpeed's data handling is acceptable for the use case. <br>
Risk: Chained video generations and extensions can incur paid API costs. <br>
Mitigation: Confirm pricing and expected run counts before starting generation or extension chains. <br>
Risk: Untrusted media URLs or unsupported parameters can produce unsafe or failed requests. <br>
Mitigation: Use trusted media URLs, validate prompt and media inputs, and only pass documented parameters. <br>


## Reference(s): <br>
- [WaveSpeed AI access keys](https://wavespeed.ai/accesskey) <br>
- [ClawHub skill page](https://clawhub.ai/chengzeyi/wavespeed-veo-31-fast) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides WaveSpeed API calls that return generated or extended video URLs; usage can involve uploaded media, API credentials, and paid generation requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
