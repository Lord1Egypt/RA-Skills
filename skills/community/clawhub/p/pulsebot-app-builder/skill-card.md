## Description: <br>
Build real-time Timeplus data processing and analysis applications in Pulsebot as single-file HTML/JavaScript apps that connect to Timeplus Proton, visualize streaming data with Vistral, and follow the Timeplus UI style guide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtao](https://clawhub.ai/user/gangtao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to build browser-based Timeplus Proton dashboards, pipeline visualizers, and streaming analytics apps in Pulsebot. The skill guides requirement clarification, SQL/query setup, chart selection, Timeplus styling, and delivery of a self-contained HTML app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may run SQL against the local Timeplus Proton proxy at localhost:8001. <br>
Mitigation: Review the SQL query and target streams before opening or sharing generated apps. <br>
Risk: Generated apps load React, Vistral, Proton driver, and peer dependencies from third-party unpkg script tags. <br>
Mitigation: Use trusted, pinned, or locally hosted dependencies when working with sensitive Proton data or controlled environments. <br>


## Reference(s): <br>
- [Pulsebot App Builder release page](https://clawhub.ai/gangtao/pulsebot-app-builder) <br>
- [Proton JavaScript Driver Reference](references/PROTON_DRIVER.md) <br>
- [Vistral API Reference](references/VISTRAL_API.md) <br>
- [Timeplus Application Style Guide](references/STYLE_GUIDE.md) <br>
- [Timeplus Proton JavaScript Driver](https://github.com/timeplus-io/proton-javascript-driver) <br>
- [Timeplus Vistral](https://github.com/timeplus-io/vistral) <br>
- [Timeplus style guide source](https://gist.github.com/gangtao/5307e8bbb84384804c7fb9480a515925) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, CSS, SQL, and shell command snippets; final app output is a single self-contained HTML file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated apps load browser dependencies from CDN and connect to a local Timeplus Proton proxy at localhost:8001.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
