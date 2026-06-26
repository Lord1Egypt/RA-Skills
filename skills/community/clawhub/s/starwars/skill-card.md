## Description: <br>
Starwars is a CLI skill that lets agents look up Star Wars characters, planets, films, species, and starships using SWAPI without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and external users use Starwars to answer routine Star Wars universe lookup questions from SWAPI, including lookups for people, planets, films, species, and starships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup terms may be sent to swapi.dev. <br>
Mitigation: Use Star Wars entity names or film terms as queries, and avoid submitting private or sensitive text. <br>
Risk: Manual installation instructions reference cloning an external repository, changing script permissions, and creating a /usr/local/bin symlink. <br>
Mitigation: Prefer the ClawHub install path for this release, or inspect the external repository and script before following manual clone, chmod, or symlink commands. <br>
Risk: SWAPI coverage is limited to the original and prequel films and does not cover sequel trilogy, TV shows, or extended universe material. <br>
Mitigation: Use the skill for Episodes 1-6 lookups and verify answers against another source when users ask about material outside that coverage. <br>


## Reference(s): <br>
- [Starwars on ClawHub](https://clawhub.ai/jeffaf/starwars) <br>
- [SWAPI](https://swapi.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text CLI output with entity summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq; uses SWAPI and no API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
