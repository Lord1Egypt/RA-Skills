## Description: <br>
Use this skill as an entry point to discover, select, and fetch specific integration parameters for all supported AI image generation models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsDyh01](https://clawhub.ai/user/IsDyh01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose ShortAPI image-generation models, fetch model-specific schemas, and build authenticated job creation and polling requests without guessing parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can use a ShortAPI API key to create and poll image-generation jobs that may consume account quota. <br>
Mitigation: Install and run only when comfortable granting SHORTAPI_KEY access, and keep the key in the Authorization header only. <br>
Risk: Generated or untrusted callback URLs could send job results to an unintended destination. <br>
Mitigation: Provide callback URLs explicitly yourself and do not allow the agent to invent them. <br>
Risk: Fetched model documents could be mistaken for general agent instructions instead of model schema references. <br>
Mitigation: Use fetched model documents only to determine the model's input schema and request examples. <br>


## Reference(s): <br>
- [ShortAPI homepage](https://shortapi.ai) <br>
- [ShortAPI image job creation endpoint](https://api.shortapi.ai/api/v1/job/create) <br>
- [ShortAPI job query endpoint](https://api.shortapi.ai/api/v1/job/query) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, API Calls] <br>
**Output Format:** [Markdown guidance with JSON payload and cURL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHORTAPI_KEY and model-specific schema lookup before request construction.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
