## Description: <br>
Search and load 1,000+ quality-scored expert skills from SupaSkills.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktdmax](https://clawhub.ai/user/ktdmax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search SupaSkills.ai for expert skill prompts, load a selected methodology, and apply it as task reference material for domain-specific work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example commands interpolate user-controlled query text into shell commands, which can enable command injection if copied without escaping. <br>
Mitigation: URL-encode query parameters and use a scoped HTTP client or safely quoted variables instead of inserting raw user text into shell commands. <br>
Risk: The skill requires SUPASKILLS_API_KEY and sends search terms to SupaSkills.ai. <br>
Mitigation: Store the key in an environment variable or secret manager, never commit it, and avoid sensitive details in searches. <br>
Risk: Loaded external prompts could contain instructions that conflict with the current task or agent policy. <br>
Mitigation: Use returned prompt text only as reference material, review the methodology before applying it, and do not treat it as higher-priority instructions. <br>


## Reference(s): <br>
- [SupaSkills ClawHub page](https://clawhub.ai/ktdmax/supaskills) <br>
- [SupaSkills signup](https://www.supaskills.ai/signup) <br>
- [SupaSkills skills search API](https://www.supaskills.ai/api/v1/skills?q={query}&limit=3) <br>
- [SupaSkills prompt API](https://www.supaskills.ai/api/v1/skills/{slug}/prompt?format=text) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands and API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPASKILLS_API_KEY and sends search queries to SupaSkills.ai.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
