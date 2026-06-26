## Description: <br>
Deploy Umami analytics avoiding data loss, tracking failures, and integration issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill as an Umami deployment and integration checklist to avoid analytics data loss, missing pageviews, tracking-script failures, and self-hosting mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the checklist to a real Umami instance can affect analytics privacy, consent handling, stored event data, and service continuity. <br>
Mitigation: Apply normal analytics privacy and consent review, back up the database before changes, protect deployment secrets, and test tracking behavior before relying on production data. <br>
Risk: Changing HASH_SALT, using an unsupported database, or misconfiguring website IDs can cause data loss or silent tracking gaps. <br>
Mitigation: Keep HASH_SALT stable, use PostgreSQL or MySQL, verify each site uses the correct tracking script, and confirm pageviews and events in browser network and console tools after deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/umami) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code is produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
