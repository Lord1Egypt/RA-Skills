## Description: <br>
Record, search, and analyze your wine collection and tasting notes. Use when logging tastings, searching vintages, comparing ratings, or tracking inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log wine-related notes, search prior entries, review recent activity, and export locally stored records. The implementation primarily behaves as a command-line plaintext logger for arbitrary input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool saves arbitrary command input in plaintext under ~/.local/share/wine. <br>
Mitigation: Avoid entering secrets or unrelated sensitive information, and review local logs and exports before sharing or backing them up. <br>
Risk: The advertised wine-specific functionality is underdeveloped compared with the implementation's generic logging behavior. <br>
Mitigation: Validate that the command behavior meets the intended wine tracking workflow before relying on it for inventory or tasting records. <br>
Risk: The executable name wine can conflict with other software named wine on a user's system. <br>
Mitigation: Verify which wine command is on PATH before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/wine) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and local JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command input and activity history locally under ~/.local/share/wine.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
