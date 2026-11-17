## Description:

Helps an agent create Chinese-language, single-file R Shiny classroom dashboards that replace static slide decks with interactive teaching apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, instructional developers, and agents assisting them use this skill to turn lesson material into runnable R Shiny teaching dashboards with templates for lectures, parameter exploration, data stories, concept comparison, stepwise reveals, and quizzes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated app.R files may contain lesson-specific code that is run locally.

Mitigation: Review generated app.R files before running them.

Risk: The generated app may require installing R packages or deploying to hosted Shiny services.

Mitigation: Install only the listed packages and deploy only when the project and account or network implications are trusted.

Risk: Classroom apps that depend on live network resources can fail during instruction.

Mitigation: Prefer local runApp execution and package required data with the app when preparing classroom materials.

## Reference(s):

- [Skill page](https://clawhub.ai/junwugit/skills/shiny-teaching-dashboard)
- [Layout patterns](references/layout-patterns.md)
- [Shiny components for teaching](references/components.md)
- [Color schemes](references/color-schemes.md)
- [Setup, run, deploy, and Chinese fonts](references/setup-and-run.md)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Single-file R Shiny app.R plus concise Markdown run instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated apps may require local R packages such as shiny, bslib, ggplot2, plotly, DT, thematic, showtext, bsicons, or shinydashboard depending on the selected template.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
