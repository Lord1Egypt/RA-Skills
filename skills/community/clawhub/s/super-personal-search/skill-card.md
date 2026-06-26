## Description: <br>
Build, debug, and extend the Connectify founder network platform, including its React/Vite frontend, Express backend, Redis cache, OpenAI ranking, and Apify ingestion adapter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deonmenezes](https://clawhub.ai/user/deonmenezes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run, modify, debug, and deploy the Connectify network analytics app. It is especially relevant when preserving the `/api/query` response contract, tuning OpenAI-based relevance scoring, managing Redis-backed connection data, or replacing placeholder ingestion with Apify actor calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The app sends contact details and free-form notes to OpenAI when AI ranking and suggested-action features run. <br>
Mitigation: Avoid entering sensitive relationship notes or confidential contact data unless the deployment has appropriate consent, data-processing controls, and OpenAI configuration. <br>
Risk: The app stores network contact records and query-context data in Redis. <br>
Mitigation: Use an appropriately secured Redis deployment, restrict access to stored contact data, and review retention behavior before using real network records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deonmenezes/super-personal-search) <br>
- [Artifact README](README.md) <br>
- [Artifact skill guide](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is scoped to the Connectify app and its local development, API, Redis, OpenAI, and Apify integration workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
