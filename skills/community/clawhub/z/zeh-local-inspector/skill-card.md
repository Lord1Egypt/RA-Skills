## Description: <br>
Inspect local working directory and return a short result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maosangtianshi](https://clawhub.ai/user/maosangtianshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect the current local working directory in a safe, read-only way. It reports the folder path, a short top-level entry listing, and a concise Chinese risk note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal the current folder path and a short top-level directory listing. <br>
Mitigation: Use it only in directories where exposing that metadata is acceptable. <br>
Risk: Future versions could change the inspection behavior. <br>
Mitigation: Review updates before enabling new versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maosangtianshi/zeh-local-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Concise Chinese Markdown based on JSON inspection results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the current working directory and up to ten top-level entries; does not modify files or use network access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
