## Description: <br>
Logs into TGA (hortorgames), parses projectId and dashboardId from panel URL, downloads report zip via API, unzips to tga-downloads/, and analyzes all xlsx files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xifengxi](https://clawhub.ai/user/xifengxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to download authorized TGA dashboard reports, extract the report archive, and summarize metrics from the resulting xlsx files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TGA credentials and browser cookies in local configuration and stores a reusable token in plaintext. <br>
Mitigation: Use only authorized TGA accounts, keep the skill directory private, never commit .env or .tga-token, and delete or rotate stored tokens after use. <br>
Risk: Downloaded TGA reports may contain sensitive business data. <br>
Mitigation: Store downloaded reports in controlled locations, limit access to authorized users, and remove report archives and extracted files when no longer needed. <br>


## Reference(s): <br>
- [TGA web application](https://tga-web.hortorgames.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a token cache, downloaded zip archive, extracted report directory, and structured analysis of xlsx files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
