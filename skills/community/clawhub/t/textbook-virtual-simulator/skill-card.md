## Description: <br>
Textbook Virtual Simulator helps agents turn textbook content in text, PDF, or JSON formats into interactive educational simulation web applications with 3D scenes, quizzes, progress tracking, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erich1566](https://clawhub.ai/user/erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and learning-technology teams use this skill to parse teaching materials and generate deployable virtual simulation web applications for experiments, operational training, knowledge visualization, and other instructional scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated apps can persist learner activity, quiz results, progress, and session data in browser storage. <br>
Mitigation: Disclose tracking before learner use, define retention expectations, and provide a clear way to export or clear stored data. <br>
Risk: Generated web templates load third-party JavaScript, fonts, and icons from public CDNs. <br>
Mitigation: Pin dependency versions, review CDN integrity and availability requirements, or vendor dependencies before deployment. <br>
Risk: The skill generates deployable web application code from instructional materials. <br>
Mitigation: Inspect generated code, test browser behavior, and review content rights before publishing or using the app in a learner-facing setting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erich1566/skills/textbook-virtual-simulator) <br>
- [Publisher profile](https://clawhub.ai/user/erich1566) <br>
- [Metadata homepage](https://github.com/your-username/textbook-virtual-simulator) <br>
- [3D Technologies Guide](references/3d_technologies.md) <br>
- [Educational Simulation Best Practices](references/best_practices.md) <br>
- [Simulation Types Guide](references/simulation_types.md) <br>
- [Web Templates Guide](references/web_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, JavaScript, CSS, HTML, and deployable web application files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated web applications may include 3D scenes, interactive components, quiz logic, learner progress tracking, analytics dashboards, and deployment notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
