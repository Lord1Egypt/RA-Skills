## Description: <br>
Track shipments and manage trackers using Ship24's universal tracking API for 2,500+ couriers and eCommerce platforms worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ship24](https://clawhub.ai/user/ship24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track packages, create and update shipment trackers, retrieve tracking history, and manage webhook-based shipment notifications through Ship24. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Ship24 API key. <br>
Mitigation: Use a revocable or least-privileged Ship24 API key when available and provide it through the SHIP24_API_KEY environment variable. <br>
Risk: Tracker references can contain customer or order identifiers. <br>
Mitigation: Avoid placing sensitive customer or order data in clientTrackerId or other tracker references unless needed for the workflow. <br>
Risk: Webhook subscription and replay features can send shipment event data to an external endpoint. <br>
Mitigation: Verify webhook destinations before subscribing trackers or replaying missed delivery events. <br>
Risk: Bulk tracker creation may partially create trackers when a request is retried after failure. <br>
Mitigation: Check returned created, duplicate, and failed counts, then inspect tracker state before retrying failed bulk operations. <br>
Risk: Some Ship24 operations are rate-limited. <br>
Mitigation: Respect documented rate limits for courier listing and webhook replay operations and retry with backoff when appropriate. <br>


## Reference(s): <br>
- [Ship24 Documentation](https://docs.ship24.com) <br>
- [Ship24](https://ship24.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses with shipment status, tracker metadata, setup configuration snippets, and operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHIP24_API_KEY. Outputs may reference shipment events, tracker identifiers, courier data, and webhook subscription status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
