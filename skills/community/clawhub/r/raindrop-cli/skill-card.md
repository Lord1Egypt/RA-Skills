## Description:

Manage Raindrop.io bookmarks from the command line using the Raindrop REST API for search, existence checks, add, update, and remove workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adorostkar](https://clawhub.ai/user/adorostkar)

### License/Terms of Use:


## Use Case:

Developers and automation-focused users use this skill to manage Raindrop.io bookmarks from an agent-assisted command line, including checking for existing URLs and applying collection, search, add, update, and remove operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Raindrop.io token can enable bookmark automation and may expose account data if stored insecurely.

Mitigation: Store RAINDROP_TOKEN only in a private local env file with restrictive permissions and avoid sharing logs or configs that contain it.

Risk: Update and remove commands can change or delete Raindrop.io account data.

Mitigation: Review target IDs before update or remove operations and test behavior on noncritical bookmarks before broader use.

Risk: The reviewed artifact describes a scripts/raindrop CLI but does not include the script itself, so runtime safeguards could not be verified from package code.

Mitigation: Inspect the installed CLI script and confirm its behavior before relying on it for bulk bookmark workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a personal RAINDROP_TOKEN for live Raindrop.io API operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
