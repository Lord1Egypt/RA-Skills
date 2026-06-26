## Description: <br>
Looks up Kuaishou/Kwai creator profile details, including account basics, creator positioning, homepage information, and follower scale, using SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, marketers, and developers use this skill to retrieve read-only Kuaishou creator profile facts by user ID or profile URL. It helps agents report available profile fields while separating factual data from strategic interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SOCIALDATAX_API_KEY and sends creator IDs or profile URLs to an external SocialDataX service. <br>
Mitigation: Use only the documented environment variable, confirm the target profile before lookup, and avoid adding unnecessary sensitive data to command arguments or prompts. <br>
Risk: Returned profile facts can be mixed with strategic interpretation. <br>
Mitigation: Report source fields separately from analysis and label any interpretation as such. <br>


## Reference(s): <br>
- [SocialDataX API access and homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-kuaishou-creator-profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; direct CLI and MCP calls return JSON profile data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY, node, and npm; profile lookups are read-only and should use either user ID or profile URL for a single request.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
