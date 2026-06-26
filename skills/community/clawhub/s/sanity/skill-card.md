## Description: <br>
Helps agents query and manage Sanity CMS content via GROQ queries and the Sanity HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwhite-oss](https://clawhub.ai/user/dwhite-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to fetch, query, create, update, publish, and delete Sanity Content Lake documents through GROQ and HTTP API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Sanity API token or Authorization header could be exposed in logs, prompts, or shared command output. <br>
Mitigation: Use the least-privileged token needed for the task and avoid printing, logging, or sharing token-bearing curl commands. <br>
Risk: Create, update, publish, or delete examples can mutate production content when run with an Editor token. <br>
Mitigation: Confirm mutation intent before execution, prefer staging datasets for testing, and use Viewer tokens for read-only work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dwhite-oss/sanity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples, GROQ snippets, and environment variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SANITY_PROJECT_ID, SANITY_DATASET, and SANITY_API_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
