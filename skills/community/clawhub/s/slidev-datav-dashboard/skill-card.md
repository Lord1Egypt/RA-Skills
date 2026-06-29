## Description: <br>
Build large-screen data-visualization dashboards as Slidev presentations using the datav-vue3 DataV component library, with ready-to-use layouts, panel components, design rules, an example deck, and a scaffold script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to scaffold and customize Slidev-based monitoring, command-center, or data visualization dashboards with DataV components and a 1920x1080 large-screen layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold installs third-party npm dependencies and uses unpinned or range-based versions in the generated package template. <br>
Mitigation: Use the skill in projects where npm installation is acceptable, review dependency changes, pin dependency versions, and keep a lockfile for production builds. <br>
Risk: The dashboard stylesheet imports Google Fonts, which can require network access during development or build and may be unsuitable for offline or restricted environments. <br>
Mitigation: Replace the remote font import with local or system fonts when building for production, offline, or restricted deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/junwugit/skills/slidev-datav-dashboard) <br>
- [DataV Vue3 docs](https://datav-vue3.netlify.app) <br>
- [DataV Vue3 demos](https://datav-vue3-demo.netlify.app) <br>
- [Original DataV docs](http://datav.jiaminghi.com/) <br>
- [DataV component catalog](references/components.md) <br>
- [Large-screen dashboard design rules](references/design-rules.md) <br>
- [Slidev integration guide](references/slidev-integration.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Vue, TypeScript, CSS, JSON, and bash snippets plus scaffolded project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Slidev dashboard scaffold and reference material; the scaffold runs npm install and may load Google Fonts unless adapted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
