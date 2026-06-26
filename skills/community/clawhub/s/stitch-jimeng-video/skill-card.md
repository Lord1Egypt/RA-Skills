## Description: <br>
Generates 1080P Jimeng image-to-video clips through Volcengine's Jimeng AI API using first-frame and last-frame inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdt328606](https://clawhub.ai/user/sdt328606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to submit prompts plus start and end images to Volcengine's Jimeng API, poll generation status, and optionally download the resulting video file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and first/last-frame images are sent to Volcengine for cloud processing. <br>
Mitigation: Use non-sensitive prompts and media, and confirm the service is appropriate for the user's privacy and compliance requirements. <br>
Risk: The skill requires Volcengine API credentials and may incur API charges. <br>
Mitigation: Store credentials in environment variables, limit credential scope where possible, and monitor API usage and billing. <br>
Risk: Generated video download URLs are returned by the remote service. <br>
Mitigation: Review returned URLs and downloaded files before using them in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdt328606/stitch-jimeng-video) <br>
- [Prompt guide](references/prompt-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI execution and optional MP4 output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VOLC_ACCESS_KEY and VOLC_SECRET_KEY, accepts prompt, first-frame image, last-frame image, seed, output path, and no-poll options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
