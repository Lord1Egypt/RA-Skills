## Description: <br>
打车助手 helps agents estimate prices, request or schedule rides, book airport transfers, and manage car-service orders for enterprise travel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs200809](https://clawhub.ai/user/cs200809) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business travelers use this skill to arrange immediate or scheduled car service, airport transfers, charter rides, and related order tasks through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking, scheduling, sharing, invoicing, and cancellation actions can affect real travel plans or costs without a clearly documented confirmation boundary. <br>
Mitigation: Require explicit user approval before any action that creates, changes, shares, invoices, or cancels a ride. <br>
Risk: Ride locations, flight numbers, contacts, and invoice details are sensitive and may be sent to external car-service platforms. <br>
Mitigation: Collect only necessary details, disclose external sharing before submission, and avoid retaining sensitive travel or billing data longer than needed. <br>
Risk: The artifact includes simulated price, distance, driver, and vehicle data that could be mistaken for confirmed platform results. <br>
Mitigation: Use real car-service platform APIs for availability, prices, driver assignment, and order status, and label estimates as non-final until confirmed by the provider. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cs200809/ride-hailing-helper) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/cs200809) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [JSON responses and human-readable trip summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; handles ride locations, schedules, flight details, order IDs, contacts, and invoice-related inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
