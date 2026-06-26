## Description: <br>
Generate talking head videos from a portrait image and audio using WaveSpeed AI's InfiniteTalk model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate lip-synced talking avatar videos from consented portrait images and audio. It provides JavaScript examples for WaveSpeed AI uploads, model invocation, optional face masks, prompt guidance, resolution selection, retries, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portraits, voice/audio, prompts, and mask images are sent to WaveSpeed AI for processing. <br>
Mitigation: Use consented media only and avoid uploading sensitive content unless the user accepts WaveSpeed AI processing. <br>
Risk: Untrusted media URLs could expose private data or trigger unwanted remote fetch behavior. <br>
Mitigation: Use trusted image and audio URLs or validate URLs before submitting them to the service. <br>
Risk: The WaveSpeed API key can grant access to paid generation resources. <br>
Mitigation: Store the API key in an environment variable or secret manager and do not hardcode or commit it. <br>


## Reference(s): <br>
- [WaveSpeed AI Access Keys](https://wavespeed.ai/accesskey) <br>
- [ClawHub Skill Page](https://clawhub.ai/chengzeyi/wavespeed-infinitetalk-avatar) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers portrait image, audio, optional mask image, prompt, resolution, seed, retry settings, error handling, expected processing time, and pricing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
