## Description: <br>
A travel assistant skill that guides an agent in using the tuniu CLI to search, book, and manage flights, hotels, attraction tickets, trains, cruises, and vacation products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardoooooo](https://clawhub.ai/user/leonardoooooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to turn travel requests into tuniu CLI commands for searching availability, reviewing details, creating orders, and handling cancellations across Tuniu travel services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and running the tuniu CLI/package. <br>
Mitigation: Install it only in trusted environments and only when the user intends to use Tuniu travel services. <br>
Risk: TUNIU_API_KEY is a sensitive credential used by the CLI. <br>
Mitigation: Store it in a protected secret or environment variable and avoid exposing the full value in chat, logs, or shell history. <br>
Risk: Booking flows can send traveler personal data such as names, phone numbers, and identity document numbers to Tuniu. <br>
Mitigation: Collect only data needed for the booking, avoid echoing personal data in responses or logs, and make clear that the data is sent to Tuniu for order creation. <br>
Risk: The skill can create or cancel travel orders. <br>
Mitigation: Require explicit user confirmation before running any booking or cancellation command. <br>


## Reference(s): <br>
- [ClawHub listing for tuniu-cli](https://clawhub.ai/leonardoooooo/tuniu-cli) <br>
- [Tuniu Open Platform API key registration](https://open.tuniu.com/mcp/login) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose tuniu CLI calls that query services, create travel orders, or cancel orders after user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
