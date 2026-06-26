## Description: <br>
Automates ZLQA game GM tool API testing by helping manage test cases, execute interface tests, and view generated reports after binding a local project path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gerburmsidep7](https://clawhub.ai/user/gerburmsidep7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to initialize a local ZLQA project path, discover GM API interfaces, run selected or grouped test cases, and view generated HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes local Python test scripts from the bound ZLQA project, which may use API secrets or test credentials. <br>
Mitigation: Install and run it only for trusted ZLQA repositories, use least-privilege test credentials, and avoid production GM secrets. <br>
Risk: The runner writes configuration and edits target project test files when selecting cases. <br>
Mitigation: Review project diffs after runs and keep secret-bearing configuration files out of version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gerburmsidep7/zlqa-gmt-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Plain text summaries with command examples and generated HTML test reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write skill configuration, edit target project test selection, and open generated HTML reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
