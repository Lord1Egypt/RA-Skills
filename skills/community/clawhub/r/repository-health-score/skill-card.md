## Description: <br>
Scores a repository's health across code quality, testing, documentation, CI/CD, security, dependencies, community, and maintainability, then produces a letter grade with improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and technical evaluators use this skill to assess repository maturity, maintenance quality, and adoption risk. It can produce a full score, compare two repositories, or suggest the highest-impact improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository files and local git metadata from the directory where it is run. <br>
Mitigation: Run it only in repositories you intend to inspect, and review the resulting scorecard before relying on it for adoption or investment decisions. <br>
Risk: Optional community metrics may call GitHub through the authenticated GitHub CLI context. <br>
Mitigation: Skip or disable the optional GitHub metric commands if outbound GitHub requests or use of the active GitHub CLI account is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/repository-health-score) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Human-readable scorecards, Markdown reports, JSON summaries, or badge URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores eight repository-health dimensions, assigns an A-F grade, and can suggest prioritized improvements.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
