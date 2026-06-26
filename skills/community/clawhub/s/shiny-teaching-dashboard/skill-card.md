## Description: <br>
Helps agents create single-file R Shiny classroom dashboards that replace slide decks with interactive lessons, component guidance, color schemes, and reusable teaching templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, instructional designers, and developers use this skill to turn course material into interactive R Shiny dashboards for classroom presentation and local distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad interactive-lesson requests may be steered toward R Shiny even when another stack would be preferable. <br>
Mitigation: State the desired language, framework, or delivery format when Shiny is not the intended target. <br>
Risk: Generated work may include local file creation plus package installation and run commands. <br>
Mitigation: Review generated R code and package installation commands before running them in managed or shared environments. <br>
Risk: The skill may default to Chinese phrasing. <br>
Mitigation: Specify the desired output language when requesting teaching content or app text. <br>


## Reference(s): <br>
- [Layout Patterns](references/layout-patterns.md) <br>
- [Color Schemes](references/color-schemes.md) <br>
- [Components](references/components.md) <br>
- [Setup and Run](references/setup-and-run.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/junwugit/shiny-teaching-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Single-file R Shiny app.R plus concise Markdown response with installation and run commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated source is expected to be written to disk rather than pasted in full in chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
