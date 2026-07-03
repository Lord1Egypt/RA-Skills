## Description: <br>
Visit Analyzer analyzes employee visit communication records to assess sales stage, follow-up strategy, customer insights, commitments, and risks, then generates a client/project profile with an H5 viewing link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales employees and operators use this skill to analyze phone call transcripts and WeChat chat records for a specific customer or project. It produces a concise visit-analysis summary, creates or updates a project profile, and returns an H5 link for detailed review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for employee passwords in chat and cache authentication tokens for later access. <br>
Mitigation: Install only when the publisher and backend operator are trusted; prefer platform-native authentication, protect the token cache, and clear cached credentials when access is no longer needed. <br>
Risk: The skill may read private call transcripts and WeChat notification records, then send derived analysis to a remote IP-based service. <br>
Mitigation: Use explicit consent before each data-source access, limit analysis to selected records, and avoid processing sensitive conversations that should not leave the local environment. <br>
Risk: Generated H5 links may grant access through an exchange code or a fallback token-bearing URL. <br>
Mitigation: Prefer exchange-code links, avoid sharing generated links outside the intended audience, and revoke or rotate tokens if a link is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/visit-analyzer) <br>
- [Backend API base URL referenced by the skill](http://47.116.49.218:8000/api/v1) <br>
- [H5 viewer base URL referenced by the skill](http://47.116.49.218:5173) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; final agent output is a concise text summary plus an H5 link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and python3 on Linux or macOS; reads local transcripts or notification records and calls a remote backend service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
