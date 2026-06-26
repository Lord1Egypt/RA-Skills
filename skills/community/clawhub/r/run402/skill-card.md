## Description: <br>
Provision Postgres databases, deploy static sites, generate images, and build full-stack webapps on Run402 using x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MajorTal](https://clawhub.ai/user/MajorTal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to build, deploy, and operate Run402-hosted apps, databases, static sites, serverless functions, image generation, and billing or wallet workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned global CLI package. <br>
Mitigation: Verify the npm package name and version before installation. <br>
Risk: The skill can create persistent wallet or payment authority and trigger paid cloud actions. <br>
Mitigation: Start on testnet or with minimal funds, use idempotency keys where applicable, and require explicit approval before paid or mainnet actions. <br>
Risk: The skill handles service keys, wallet files, project configuration, and deployed secrets. <br>
Mitigation: Keep service keys server-side, avoid exposing secret values, and rotate wallet files or service credentials if they may have been exposed. <br>
Risk: The skill includes destructive project, storage, and data operations. <br>
Mitigation: Require explicit user confirmation before deletion, archival, or irreversible administrative operations. <br>


## Reference(s): <br>
- [Run402 API](https://api.run402.com) <br>
- [ClawHub run402 skill page](https://clawhub.ai/MajorTal/run402) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, SQL, JavaScript, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid deployment steps, project manifests, API requests, and secret-handling instructions.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
