## Description: <br>
Look up snooker rankings, results, player profiles, live matches and head-to-head records via api.snooker.org. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rgstephens](https://clawhub.ai/user/rgstephens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to query professional snooker data, including rankings, results, player profiles, live matches, schedules, tournaments, events, and head-to-head records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional setup command can store the Snooker API key in ~/.nanobot/workspace/snooker/config.json. <br>
Mitigation: Prefer SNOOKER_API_KEY for credentials; if the setup command is used, restrict local access to the config file. <br>
Risk: Direct script execution may require uv even though release metadata lists python3. <br>
Mitigation: Confirm uv availability before invoking snooker.py directly, or run the Python script in an environment that supports its script header. <br>


## Reference(s): <br>
- [Snooker API](https://api.snooker.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/rgstephens/snooker-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/rgstephens) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with documented shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SNOOKER_API_KEY for authenticated api.snooker.org requests.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
