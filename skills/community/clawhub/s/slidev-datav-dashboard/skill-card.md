## Description:

Build large-screen DataV dashboards as Slidev presentations with reusable layouts, design rules, component references, an example deck, and a scaffold script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to create command-center dashboards, monitoring screens, and visualization decks in Slidev with DataV components. It helps scaffold the project, choose dashboard layouts and palettes, wire DataV into Slidev, and troubleshoot common rendering issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold script refreshes setup, layout, style, component, Vite, package, and example deck files, which can overwrite local project changes.

Mitigation: Run the scaffold only in a fresh or version-controlled directory and review the generated diff before using the files.

Risk: The package template uses unpinned or range-based npm dependencies and the scaffold runs npm install.

Mitigation: Pin dependency versions, generate and review a lockfile, and prefer npm ci or reviewed install flags for production use.

Risk: Dashboard font configuration may fetch Google Fonts from a third-party service.

Mitigation: Remove the external font import or self-host approved fonts when third-party font requests are not acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/junwugit/skills/slidev-datav-dashboard)
- [DataV Component Catalog](references/components.md)
- [Large-Screen Dashboard Design Rules](references/design-rules.md)
- [Slidev Integration Guide](references/slidev-integration.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Example Dashboard Deck](templates/slides.example.md)
- [DataV Vue3 Documentation](https://datav-vue3.netlify.app)
- [DataV Vue3 Live Demos](https://datav-vue3-demo.netlify.app)
- [Original DataV Documentation](http://datav.jiaminghi.com/)
- [Slidev Vue App Configuration](https://sli.dev/custom/config-vue)
- [Slidev Components in Slides](https://sli.dev/guide/component)
- [Slidev Vite Configuration](https://sli.dev/custom/config-vite)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and scaffolded Slidev project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for a Vue 3 and Slidev dashboard project and may include file-copy scaffolding plus npm dependency installation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
