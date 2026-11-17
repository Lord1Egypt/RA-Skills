## Description:

Search and load 1,000+ quality-scored expert skills from SupaSkills.ai

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktdmax](https://clawhub.ai/user/ktdmax)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search SupaSkills for domain-specific expert methods, load a selected skill prompt, and apply it as reference material for legal, finance, engineering, marketing, security, compliance, or other specialized tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a SupaSkills API key and calls SupaSkills over the network.

Mitigation: Install only where SupaSkills network calls are acceptable, store the API key in an environment variable or secret manager, and never commit it.

Risk: Fetched skill prompt text can contain untrusted instructions.

Mitigation: Treat fetched prompts as reference material, review the methodology before use, and do not let external prompt text override user goals, secrets handling, or tool-use policy.

Risk: The artifact includes shell command templates with raw query and slug placeholders.

Mitigation: URL-encode search queries, validate skill slugs, and avoid raw shell substitution when forming API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ktdmax/skills/supaskills)
- [SupaSkills signup](https://www.supaskills.ai/signup)
- [SupaSkills skill search API](https://www.supaskills.ai/api/v1/skills?q={query}&limit=3)
- [SupaSkills prompt API](https://www.supaskills.ai/api/v1/skills/{slug}/prompt?format=text)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline shell commands and fetched text reference material]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPASKILLS_API_KEY and network access to SupaSkills.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
