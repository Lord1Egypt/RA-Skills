## Description: <br>
Build, inspect, and extend WP-CLI command code using the documented stable internal API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build or review custom WP-CLI command code against the stable internal API, including command registration, hooks, output helpers, and command composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PHP command skeletons may be loaded into a WordPress project before review. <br>
Mitigation: Inspect generated PHP and adapt it to the target project before registering or executing the command. <br>
Risk: The helper script can write generated PHP to a user-selected path. <br>
Mitigation: Choose an intentional output path and confirm it does not overwrite important project files. <br>
Risk: Untrusted command or class names can produce invalid or unsafe command code. <br>
Mitigation: Use trusted command and class names when running the skeleton generator. <br>


## Reference(s): <br>
- [Stable Internal API](references/stable-internal-api.md) <br>
- [Command Patterns](references/command-patterns.md) <br>
- [WP-CLI Internal API reference](https://make.wordpress.org/cli/handbook/references/internal-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PHP and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a PHP command skeleton and optionally write it to a user-specified path via the helper script.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
