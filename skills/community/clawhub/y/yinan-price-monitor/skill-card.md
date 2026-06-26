## Description: <br>
Monitor website prices, inventory, and content changes using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and commerce teams use this skill to check product pages, monitor competitor or inventory changes, and keep local price history for alerts or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-listed webpages and may be scheduled to revisit them. <br>
Mitigation: Review the product CSV before running, use only sites you are authorized to access, and configure schedules and request pacing deliberately. <br>
Risk: Price-history files can retain product URLs, prices, timestamps, and inventory observations. <br>
Mitigation: Store generated history logs in an appropriate location and protect or delete retained files according to the user's data handling needs. <br>
Risk: Future email, Discord, or webhook alert configuration could send monitored data outside local files. <br>
Mitigation: Manually review alert destinations, credentials, and payload contents before enabling any external notification channel. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinanping-CPU/yinan-price-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script writes local price-history CSV files when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
