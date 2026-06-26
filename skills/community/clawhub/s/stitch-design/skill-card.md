## Description: <br>
Official Google Stitch SDK wrapper for OpenClaw that lets agents generate UI screens from text, apply targeted edits, branch variants, export HTML and images, and track design lineage with screen aliases and append-only event history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rasimme](https://clawhub.ai/user/rasimme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to create, iterate on, review, and export Google Stitch UI concepts from an agent workflow. It is suited for rapid screen and component ideation, visual variants, screenshot delivery, and local design lineage tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google Stitch API key. <br>
Mitigation: Provide STITCH_API_KEY only through the agent or shell environment and avoid committing credentials to prompts, design-system files, or local artifacts. <br>
Risk: Design prompts and optional design-system markdown are sent to Google Stitch, and generated HTML, screenshots, aliases, and event history are retained locally. <br>
Mitigation: Avoid confidential or regulated content unless that external processing and local retention are acceptable for the project. <br>
Risk: Generated UI output can contain inaccurate or unrequested labels, copy, layout details, or design elements. <br>
Mitigation: Review screenshots and exported HTML before using generated designs in product work. <br>


## Reference(s): <br>
- [Skill Homepage](https://github.com/rasimme/stitch-design) <br>
- [Google Stitch](https://stitch.withgoogle.com) <br>
- [@google/stitch-sdk](https://www.npmjs.com/package/@google/stitch-sdk) <br>
- [Prompt Guide](references/prompt-guide.md) <br>
- [SDK / CLI API Reference](references/sdk-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Code, Files] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON command output, screenshot URLs, and exported HTML/PNG artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses STITCH_API_KEY, calls Google Stitch endpoints, and writes local runs, state, and latest-screen artifacts.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
