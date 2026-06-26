## Description: <br>
Track all your subscriptions, get alerts before renewals, identify forgotten services, and calculate total spend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kilusha](https://clawhub.ai/user/kilusha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track recurring subscriptions, review upcoming renewals, and summarize monthly or yearly subscription spend from locally stored records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subscription and spending details are stored locally in JSON. <br>
Mitigation: Install only when local storage of these records is acceptable and protect or back up the local data directory according to the user's privacy needs. <br>
Risk: Canceling a subscription in the tracker may be mistaken for canceling the real service. <br>
Mitigation: Treat cancel actions as local record updates only and cancel the actual subscription directly with the provider. <br>
Risk: Permanent deletion can remove records the user may later need. <br>
Mitigation: Back up records before using permanent deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kilusha/subscription-manager-pro) <br>
- [Publisher profile](https://clawhub.ai/user/kilusha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and local JSON or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-entered subscription records locally and can export tracked records as CSV or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
