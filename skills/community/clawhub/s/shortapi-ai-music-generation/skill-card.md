## Description: <br>
Helps agents discover ShortAPI music generation models, fetch model-specific input schemas, create music generation jobs, and poll for results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsDyh01](https://clawhub.ai/user/IsDyh01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to integrate ShortAPI-backed music generation into agent workflows. It guides the agent to retrieve the selected model schema, submit a generation job with SHORTAPI_KEY, poll for completion, and present returned media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, and job metadata are sent to ShortAPI. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid placing secrets or sensitive data in prompts or callback URLs. <br>
Risk: A leaked SHORTAPI_KEY could allow unauthorized use of the ShortAPI account. <br>
Mitigation: Keep SHORTAPI_KEY in the environment and include it only in the Authorization header for ShortAPI requests. <br>
Risk: Rendering returned media URLs inline could expose users to unsafe or unexpected content if URLs are not checked. <br>
Mitigation: Verify returned URLs point to authorized shortapi.ai or known CDN domains before rendering media markup. <br>
Risk: Long-running generation jobs could lead to excessive polling. <br>
Mitigation: Stop polling after the documented 5-minute limit and notify the user if the job has not completed. <br>


## Reference(s): <br>
- [ShortAPI Homepage](https://shortapi.ai) <br>
- [ShortAPI Music Job Creation Endpoint](https://api.shortapi.ai/api/v1/job/create) <br>
- [ShortAPI Suno V5 Model Skill Document](https://shortapi.ai/api/skill/suno/suno-v5/generate) <br>
- [ClawHub Skill Page](https://clawhub.ai/IsDyh01/shortapi-ai-music-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, Markdown] <br>
**Output Format:** [Markdown with JSON payloads, shell commands, and inline media markup when results are available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHORTAPI_KEY and may produce audio preview markup for returned ShortAPI media URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
