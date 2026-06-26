## Description: <br>
Build a personal subscription tracker for managing recurring payments, renewals, and cutting waste. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals use this skill to create and maintain a local Markdown tracker for recurring subscriptions, billing dates, payment labels, renewal reminders, spending totals, usage notes, and cancellation savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subscription records can expose private billing details, payment labels, and service usage patterns. <br>
Mitigation: Store only masked payment labels and avoid adding full card numbers, passwords, account credentials, billing documents, or other secrets. <br>
Risk: The local ~/subscriptions/ workspace may be included in device backups or cloud sync. <br>
Mitigation: Review backup and sync settings before adding private subscription details, and keep the tracker in a location appropriate for the user's privacy needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/subscriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local ~/subscriptions/ workspace with active, cancelled, and totals documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
