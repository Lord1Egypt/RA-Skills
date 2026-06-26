## Description: <br>
Automatically colors Telegram bot choice buttons as default, destructive, or secondary based on action criticality and reversibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandysuper](https://clawhub.ai/user/dandysuper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Telegram or Openclaw bot flows use this skill to classify choice buttons and generate inline or reply keyboard payloads whose visual style reflects recommended, low-priority, or high-stakes actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bot tokens may be exposed or misused if copied into shared files or logs. <br>
Mitigation: Keep BOT_TOKEN private, prefer environment variables or a local .env file, and use a test bot token while evaluating the skill. <br>
Risk: The setup script writes scaffold files into the selected project directory and can overwrite files with the same names. <br>
Mitigation: Run setup in a fresh directory or review the target path before execution. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Pin dependency versions before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandysuper/telegram-colored-choices-buttons) <br>
- [Publisher profile](https://clawhub.ai/user/dandysuper) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [Telegram Bot API changelog](https://core.telegram.org/bots/api-changelog) <br>
- [Telegram blog announcement](https://telegram.org/blog/crafting-android-design-and-more) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, Python, and Bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper behavior that can call the Telegram Bot API and a setup script that scaffolds local bot project files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
