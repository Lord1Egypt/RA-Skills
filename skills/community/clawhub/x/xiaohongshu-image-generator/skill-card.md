## Description: <br>
Generates Xiaohongshu-style vertical card images from prompts using HTML/CSS templates and browser screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Parker-Y](https://clawhub.ai/user/Parker-Y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to create 800x1000 Xiaohongshu-style note covers, share cards, and marketing visuals from prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local HTML files and starts a temporary local web server. <br>
Mitigation: Run it only in an empty working directory, bind the server to 127.0.0.1, and stop the server immediately after screenshotting. <br>
Risk: Untrusted prompt content could be rendered into generated HTML. <br>
Mitigation: Avoid rendering untrusted prompt content as raw HTML; review or sanitize prompt-derived text before opening the page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Parker-Y/xiaohongshu-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/Parker-Y) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with HTML/CSS code, local server commands, and screenshot instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated visual cards target an 800x1000px vertical layout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
