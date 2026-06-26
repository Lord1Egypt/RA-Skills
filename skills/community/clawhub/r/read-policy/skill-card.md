## Description: <br>
Read OpenClaw policies from PostgreSQL through the local Supabase Docker stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EcosincronIA](https://clawhub.ai/user/EcosincronIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw policy keys and values from a local Supabase PostgreSQL database, such as auto_approve, priority_routing, and available_skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper reads policy values from a local database container, which may expose operational policy contents to the user running it. <br>
Mitigation: Run it only in trusted local environments and limit use to users authorized to inspect OpenClaw policies. <br>
Risk: The command depends on the local supabase-db Docker container and public.openclaw_policies table being the intended database target. <br>
Mitigation: Confirm the active Docker context and database container before running list or get commands. <br>


## Reference(s): <br>
- [ClawHub Read Policy release](https://clawhub.ai/EcosincronIA/read-policy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local policy data through docker exec against the supabase-db container.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
