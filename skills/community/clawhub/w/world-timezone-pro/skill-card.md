## Description: <br>
World timezone converter for looking up current times and comparing supported city time zones for international calls, remote work, travel planning, and global business. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve local times, compare cities, and support timezone-aware planning across global locations. It is most useful for scheduling, travel planning, and remote collaboration where quick timezone context is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises command names and features that do not fully match the shipped script. <br>
Mitigation: Inspect the artifact and invoke the bundled script path directly; validate expected commands before relying on the skill in a workflow. <br>
Risk: Timezone conversion behavior may vary by operating system because the script shells out to the local date command. <br>
Mitigation: Test representative timezone lookups and conversions on the target host, especially before scheduling important meetings or travel. <br>
Risk: Timezone output can be misleading if treated as authoritative for high-impact scheduling decisions. <br>
Mitigation: Use the output as planning assistance and confirm critical times against a trusted calendar or timezone source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON responses from the bundled timezone script plus concise agent guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local execution; no evidence of networking, persistence, hidden data access, or destructive behavior.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
