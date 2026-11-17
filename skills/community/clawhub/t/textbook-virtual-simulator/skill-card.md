## Description:

Textbook Virtual Simulator converts textbook materials in text, PDF, or JSON formats into interactive educational simulation web applications with 3D scenes, learning components, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and educators use this skill to turn textbook or training materials into deployable interactive simulation web apps for virtual experiments, operations training, knowledge graphs, and other instructional scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated web apps may process learner data and untrusted textbook content.

Mitigation: Review and sanitize source materials, avoid sensitive or student-identifying content, and make analytics and progress storage explicit before deployment.

Risk: Generated apps may rely on external dependencies or CDN-hosted assets.

Mitigation: Review, pin, and host dependencies according to the deployment environment's security requirements.

Risk: The release security verdict is suspicious because generated apps need careful review before production use.

Mitigation: Harden and test the generated app before deployment, including privacy, dependency, and content-handling review.

## Reference(s):

- [Simulation Types Guide](references/simulation_types.md)
- [3D Technology Selection Guide](references/3d_technologies.md)
- [Web Templates Guide](references/web_templates.md)
- [Educational Simulation Best Practices](references/best_practices.md)
- [Basic Web Template README](assets/web-template/README.md)
- [Project homepage from ClawHub metadata](https://github.com/your-username/textbook-virtual-simulator)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, markdown, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated web application source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate deployable web app files with 3D scene, interactive component, progress tracking, and analytics modules.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
