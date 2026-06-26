## Description: <br>
RegexVisualizer renders Regulex-style railroad diagrams for JavaScript regular expressions and exports SVG or PNG output matching the Regulex-Plus web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PipeDream941](https://clawhub.ai/user/PipeDream941) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and documentation authors use this skill to turn JavaScript regular expressions into railroad diagrams for debugging, documentation, sharing, or embedding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs npm dependencies in the skill directory. <br>
Mitigation: Install dependencies only when comfortable running npm install for this skill. <br>
Risk: The skill launches a local Chrome or Edge browser through Puppeteer. <br>
Mitigation: Use only trusted browser paths, including any value passed through --chrome or browser-related environment variables. <br>
Risk: The --out path writes SVG and PNG files and may affect existing filenames. <br>
Mitigation: Write output to a project or temporary directory and avoid important existing basenames. <br>


## Reference(s): <br>
- [RegexVisualizer on ClawHub](https://clawhub.ai/PipeDream941/regex-visualizer) <br>
- [README.md](artifact/README.md) <br>
- [Regulex-Plus web UI copy](artifact/assets/regulex.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [SVG and PNG files with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs .svg and/or .png files from a JavaScript regular expression; supported flags are limited to i, m, and g.] <br>

## Skill Version(s): <br>
1.0.0 (source: manifest.yaml, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
