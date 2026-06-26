## Description: <br>
Generates Xiaohongshu-style draft content and a local semi-automated HTML publishing page with copy, content switching, timing suggestions, and publish-status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShiXiangYu2](https://clawhub.ai/user/ShiXiangYu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and personal-brand builders use this skill to draft themed Xiaohongshu posts and manage a local publishing workflow with copy actions, scheduling suggestions, and status tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Xiaohongshu posts may contain inaccurate, unsuitable, or off-brand content if copied without review. <br>
Mitigation: Review and edit generated posts before copying them to Xiaohongshu or publishing them elsewhere. <br>
Risk: Broad activation phrases could trigger the workflow in contexts where content generation is not intended. <br>
Mitigation: Use clear requests when invoking the skill and avoid relying on broad auto-activation phrases for sensitive workflows. <br>
Risk: The generated browser page can leave publish-status history in LocalStorage. <br>
Mitigation: Clear the browser LocalStorage for the generated page if local status history should not remain in the browser profile. <br>
Risk: The bundled ClawHub publishing script can publish the skill through the user's ClawHub account. <br>
Mitigation: Run publish_to_clawhub.sh only when intentionally publishing this skill through an authenticated ClawHub account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ShiXiangYu2/xiaohongshu-hot-publish) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets, generated Xiaohongshu post text, and local HTML output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages may store publish-status history in browser LocalStorage.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; changelog released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
