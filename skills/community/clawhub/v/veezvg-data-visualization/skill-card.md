## Description: <br>
Generates runnable Python matplotlib chart code by selecting chart types from the input data and applying BCG, The Economist, or McKinsey-style visualization templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veezvg](https://clawhub.ai/user/veezvg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, consultants, content creators, and developers use this skill to turn datasets or chart requests into professional report-style matplotlib code for research reports, consulting decks, industry analysis, and article graphics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python may create PNG chart files in the working directory when run. <br>
Mitigation: Review output paths and filenames before execution and run the script in an appropriate working directory. <br>
Risk: Generated examples may reference a macOS Chinese font path that is unavailable on other systems. <br>
Mitigation: Adjust FontProperties font paths or labels for the target environment before running generated code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veezvg/veezvg-data-visualization) <br>
- [Chart Selection Guide](references/chart_selection.md) <br>
- [Visualization Specification](references/visualization_spec.md) <br>
- [Making Economist-Style Plots in Matplotlib](https://medium.com/data-science/making-economist-style-plots-in-matplotlib-e7de6d679739) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown containing runnable Python matplotlib code and concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts may save PNG chart files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
