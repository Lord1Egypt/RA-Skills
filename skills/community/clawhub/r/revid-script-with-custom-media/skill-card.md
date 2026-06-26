## Description: <br>
Render a video from a script using only the media assets the caller provides, with no stock visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to render branded videos from script text and public media URLs while keeping visual selection limited to provided assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scripts, render details, and public media URLs are sent to Revid for processing. <br>
Mitigation: Use only content approved for Revid processing and avoid confidential scripts, private URLs, and long-lived signed links unless Revid data handling has been reviewed. <br>
Risk: The Revid API key is required to render videos. <br>
Mitigation: Store REVID_API_KEY as a secret, keep it scoped where possible, and avoid placing it in prompts, payload files, logs, or committed examples. <br>
Risk: The final video may include unintended stock media if both media restriction flags are not set. <br>
Mitigation: Set both media.useOnlyProvided and options.useOnlyProvidedMedia to true, and review completed renders before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-script-with-custom-media) <br>
- [Revid public render API](https://www.revid.ai/api/public/v3/render) <br>
- [Revid public status API](https://www.revid.ai/api/public/v3/status?pid=$PID) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON configuration, Shell commands] <br>
**Output Format:** [Markdown instructions with HTTP, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY and caller-provided public media URLs; configures Revid media flags to use only provided assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
