## Description: <br>
Zapier Recipe helps agents design Zapier and Make automation recipes, including triggers, action chains, conditions, templates, and efficiency analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to draft practical Zapier or Make workflow recipes and command-line recipe templates for common automation scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command arguments and local helper history may expose private workflow notes or secrets. <br>
Mitigation: Do not pass secrets or private notes as command arguments; set ZAPIER_RECIPE_DIR to a controlled location when command history should be isolated or deleted. <br>
Risk: The bundled documentation and helper scripts expose somewhat different command sets. <br>
Mitigation: Treat generated recipes and command output as drafting aids, and review the specific helper help text before relying on a command in a workflow. <br>


## Reference(s): <br>
- [Zapier Recipe on ClawHub](https://clawhub.ai/bytesagain-lab/zapier-recipe) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Text and Markdown with command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper output is written to stdout; one helper can also write local command history under the configured data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
