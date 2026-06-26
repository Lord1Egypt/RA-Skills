## Description: <br>
Exhaustive Google Places search using grid-based scanning to find places beyond the standard surfaced results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foeken](https://clawhub.ai/user/foeken) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use spots to run dense Google Places searches over named areas or coordinates, filter results, fetch reviews, and export results as JSON, CSV, or map files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google API key for Places and Geocoding access. <br>
Mitigation: Use a Google API key restricted to the required APIs, set quotas or billing alerts, and keep the key out of shared logs or artifacts. <br>
Risk: Installing the CLI with an unpinned latest version can change behavior between runs. <br>
Mitigation: Verify the source repository before installing and pin a known version for repeatable or production workflows. <br>
Risk: Exact secret-manager paths can disclose sensitive operational details. <br>
Mitigation: Avoid publishing exact secret-manager item paths and expose credentials only through intentional local CLI setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foeken/spots) <br>
- [Publisher-provided source link](https://github.com/foeken/spots) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides use of a CLI that can produce JSON, CSV, or map files.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata, released 2026-01-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
