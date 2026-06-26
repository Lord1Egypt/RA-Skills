## Description: <br>
Queries a Traditional Chinese Medicine prescription REST API for formula search, formula details, category browsing, and symptom-based recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slamw](https://clawhub.ai/user/slamw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to look up TCM prescription data, retrieve formula details, browse categories, and request symptom-based formula recommendations through the publisher's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends health-related symptom text to an external raw-IP API service. <br>
Mitigation: Use only if the API operator is trusted, avoid identifying medical details, and treat returned formula information as reference material rather than medical advice. <br>
Risk: The artifact documents an API-key query-parameter flow. <br>
Mitigation: Prefer the documented X-API-Key header and environment variable workflow, and avoid placing API keys in URLs, logs, or chat messages. <br>


## Reference(s): <br>
- [TCM Prescription API Reference](references/api-reference.md) <br>
- [Skill README](README.md) <br>
- [ClawHub Release Page](https://clawhub.ai/slamw/tcm-prescription-api) <br>
- [Publisher Profile](https://clawhub.ai/user/slamw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON API results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TCM_API_KEY for authenticated recommendation and full-data requests.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
