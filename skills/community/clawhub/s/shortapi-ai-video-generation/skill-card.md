## Description: <br>
Use this skill as an entry point to discover, select, and fetch specific integration parameters for supported AI video generation models through ShortAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsDyh01](https://clawhub.ai/user/IsDyh01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover ShortAPI video model identifiers, fetch the exact model-specific input schema, and construct authenticated video generation requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, media URLs, model arguments, and optional callback URLs are sent to ShortAPI for processing. <br>
Mitigation: Review inputs before submission and avoid sending sensitive content unless the user is comfortable sharing it with ShortAPI. <br>
Risk: The skill requires a ShortAPI credential for authenticated API calls. <br>
Mitigation: Use a dedicated SHORTAPI_KEY when possible, only send it in the ShortAPI Authorization header, and do not include it in callbacks or generated payloads. <br>
Risk: Video generation is asynchronous and status polling can run longer than expected. <br>
Mitigation: Use reasonable polling timeouts or user-visible status updates when tracking generation jobs. <br>


## Reference(s): <br>
- [ShortAPI](https://shortapi.ai) <br>
- [ShortAPI job creation endpoint](https://api.shortapi.ai/api/v1/job/create) <br>
- [ShortAPI model skill document endpoint](https://shortapi.ai/api/skill/<model_id>) <br>
- [ShortAPI job status endpoint](https://api.shortapi.ai/api/v1/job/query?id=$JOB_ID) <br>
- [ClawHub skill page](https://clawhub.ai/IsDyh01/shortapi-ai-video-generation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/IsDyh01) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHORTAPI_KEY and uses model-specific schemas fetched from ShortAPI before request construction.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
