## Description: <br>
Tracks packages across USPS, UPS, FedEx, DHL, Amazon, OnTrac, and LaserShip by reading a markdown shipments file, detecting carriers from tracking-number patterns, and checking status with direct HTTP or an optional browser-use fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to track active shipments, detect carriers from tracking numbers, generate carrier tracking URLs, and obtain status output from a local markdown shipments table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional browser-use fallback may send tracking numbers, order information, package details, and carrier URLs to cloud browser and LLM services. <br>
Mitigation: Use manual tracking for sensitive packages and run the browser-use fallback only after reviewing the link fields and command. <br>
Risk: The skill prints an executable browser-use command built from shipment-file links. <br>
Mitigation: Do not let an agent automatically run the printed command; inspect the shipment file links and generated command before execution. <br>
Risk: Shipment and order data are kept in a local markdown file. <br>
Mitigation: Install only where storing shipment data locally is acceptable, and remove delivered or sensitive entries when no longer needed. <br>


## Reference(s): <br>
- [Shipment Tracker on ClawHub](https://clawhub.ai/pfrederiksen/shipment-tracker) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON status summaries, with optional shell commands for browser-use fallback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local markdown shipments table and may make outbound HTTPS carrier lookups.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
