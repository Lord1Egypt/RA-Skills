## Description: <br>
Uses a seven-step method to analyze China A-share stocks and produce financial analysis covering ROE decomposition, profit model identification, industry comparison, and investment insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request remote financial analysis for Shanghai and Shenzhen listed stocks and receive investment-oriented summaries or HTML report content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock-analysis prompts to a remote Prana/Claw service. <br>
Mitigation: Install only if you trust the Prana/Claw service, are comfortable sending the prompts to it, and have verified the configured base URL. <br>
Risk: API credentials may be stored in config/api_key.txt by default. <br>
Mitigation: Keep config/api_key.txt private, avoid committing it, or set PRANA_SKILL_SKIP_WRITE_API_KEY=1 and provide credentials through environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokeer52/stock-analysis-7step) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML reports, JSON, shell commands, configuration] <br>
**Output Format:** [Remote service response printed as JSON, with stock-analysis text or generated HTML report content depending on the service result.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python and Node clients accept a message, optional thread ID, and optional base URL; long-running requests may be recovered through result polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
