## Description: <br>
Generate high-quality images on demand via the Runware.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeekLord](https://clawhub.ai/user/GeekLord) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn text prompts into locally saved images through their own Runware account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Runware and may consume the user's Runware API credits. <br>
Mitigation: Use the skill only with an approved Runware account, review prompts before generation, and follow Runware's terms and content policies. <br>
Risk: The skill requires a Runware API key. <br>
Mitigation: Provide RUNWARE_API_KEY through the environment or a secret manager, and do not store API keys in skill-config.json or committed files. <br>
Risk: Generated files are saved locally and the last output directory is remembered in skill-config.json. <br>
Mitigation: Review or clear skill-config.json's last_output_dir before sharing or publishing the skill package. <br>
Risk: Dependencies are not fully pinned in requirements.txt. <br>
Mitigation: Install with pinned, current dependency versions in production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GeekLord/runware-image) <br>
- [Runware API documentation](https://runware.ai/docs/getting-started/introduction) <br>
- [Runware task API endpoint](https://api.runware.ai/v1/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API calls, Configuration] <br>
**Output Format:** [Generated image files saved locally with CLI status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RUNWARE_API_KEY from the environment, sends prompts to Runware, and remembers the last output directory in skill-config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
