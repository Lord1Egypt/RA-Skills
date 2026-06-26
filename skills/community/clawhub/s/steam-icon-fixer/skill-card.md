## Description: <br>
Fix missing or generic Steam game desktop icons on Linux by finding the Steam app ID from local launchers and installing replacement artwork into the user's icon theme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunarmoon26](https://clawhub.ai/user/lunarmoon26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Linux desktop users, and support engineers use this skill to diagnose Steam-created launchers with missing or generic icons and install correctly named replacement artwork into the local icon theme. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer writes generated icon files into the selected hicolor icon directory. <br>
Mitigation: Run it only with image and icon directories that the user intends to modify, and use explicit directory arguments for nonstandard setups. <br>
Risk: The icon cache refresh invokes local desktop icon-cache tools when present. <br>
Mitigation: Review the command behavior before use and pass --skip-cache-refresh when manual cache refresh is preferred. <br>
Risk: ICO and image processing depends on Pillow in the Python environment. <br>
Mitigation: Install Pillow in the environment that will run the bundled script and verify the input image path before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lunarmoon26/steam-icon-fixer) <br>
- [Publisher profile](https://clawhub.ai/user/lunarmoon26) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script scans local desktop launchers, writes PNG icon files under the selected hicolor icon directory, and may refresh the local icon cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
