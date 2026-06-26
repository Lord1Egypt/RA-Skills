## Description: <br>
Bria AI helps agents generate, edit, enhance, and remove backgrounds from images through Bria.ai APIs using local Bria credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and marketing or design teams use this skill to create image assets, edit photos, remove or replace backgrounds, upscale images, and automate visual asset pipelines with Bria.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Bria credentials in ~/.bria/credentials. <br>
Mitigation: Use only a Bria key appropriate for local storage and keep the credentials file private. <br>
Risk: Selected images are uploaded to Bria.ai for processing. <br>
Mitigation: Avoid processing sensitive images unless the user is comfortable uploading them to Bria.ai. <br>
Risk: API calls can consume Bria account quota or credits. <br>
Mitigation: Confirm intended use before batch or high-volume operations. <br>


## Reference(s): <br>
- [Bria.ai](https://bria.ai) <br>
- [Bria API reference for agents](https://docs.bria.ai/llms.txt) <br>
- [API Endpoints Reference](references/api-endpoints.md) <br>
- [Shell Client](references/code-examples/bria_client.sh) <br>
- [ClawHub skill page](https://clawhub.ai/galbria/test-should-be-removed) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with bash snippets and API result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bria credentials and may upload selected images to Bria.ai for processing.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata; artifact metadata version 1.2.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
