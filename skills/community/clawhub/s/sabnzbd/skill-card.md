## Description: <br>
Manage Usenet downloads with SABnzbd through queue, history, speed, category, script, and status commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage SABnzbd downloads from an agent by checking status, adding NZBs, changing queue state, and reviewing history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script has unsafe URL handling that could allow crafted add-command input to run local code. <br>
Mitigation: Avoid untrusted or unusual URL strings for add commands until the URL encoding bug is fixed. <br>
Risk: Queue delete, purge, and delete-history commands can remove SABnzbd jobs or associated files. <br>
Mitigation: Confirm destructive actions before allowing an agent to run them. <br>
Risk: The skill requires access to a SABnzbd instance and API key. <br>
Mitigation: Use only SABnzbd instances and API keys you control, and keep the credential file private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jmagar/sabnzbd) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses from SABnzbd] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SABnzbd URL and API key via config file or environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
