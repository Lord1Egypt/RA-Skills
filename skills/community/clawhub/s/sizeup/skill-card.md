## Description: <br>
Disk usage analyzer with tree view, large file finder, and extension breakdown. Like `du` but actually readable. Pure Python, zero dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Sizeup to inspect local disk usage, identify large files, summarize extensions, and produce readable or JSON reports for cleanup and scripting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning broad directories can expose local file and directory names, paths, sizes, and extension summaries to the agent. <br>
Mitigation: Scan specific cleanup directories or project folders, and avoid scanning a whole home directory or system root unless intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rogue-agent1/sizeup) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file and directory names, paths, sizes, and extension summaries for the scanned path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
