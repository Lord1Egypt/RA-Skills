## Description: <br>
Quantics Bank is a project guide for a multi-source quantitative question-bank site, covering question sources, repository structure, commands, formula-rendering constraints, and public deployment details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aznikline](https://clawhub.ai/user/aznikline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to understand, operate, extend, and deploy the Quantics Bank quantitative question-bank project. It helps them locate data sources and repository paths, run data-fetch/build/test/deploy commands, and preserve formula-rendering constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production deployment commands can publish the current build to Vercel if run without checking the active account, project, output directory, and intent. <br>
Mitigation: Confirm the current directory, Vercel account, target project, build output, and production intent before running deploy commands. <br>
Risk: Data-fetch commands contact external question sources and may update generated project data. <br>
Mitigation: Run fetch and build commands from the expected repository, account for external network access, then validate and review generated data changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aznikline/quantics-bank) <br>
- [Quantics Bank GitHub repository](https://github.com/aznikline/Quantics-Bank) <br>
- [Quantics Bank public site](https://quantics-bank.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes project paths, data-source notes, operational commands, and deployment guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
