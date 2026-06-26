## Description: <br>
Checks a Docker-based Linux VM over SSH and reports CPU, memory, disk, container, database, Docker cache, and cleanup information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonylnng](https://clawhub.ai/user/tonylnng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for post-deploy VM sanity checks, Docker resource review, database size inspection, disk cleanup planning, and spotting unhealthy or resource-heavy containers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent SSH-based access to the configured VM. <br>
Mitigation: Use a dedicated least-privilege SSH key, keep TOOLS.md private, and verify the saved host before each run. <br>
Risk: The cleanup section can change the remote machine by pruning Docker images and build cache. <br>
Mitigation: Run cleanup only when the user explicitly wants Docker images and build cache pruned on that server. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summary with shell command execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs selected VM health sections: all, system, disk, containers, db, docker-df, or cleanup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
