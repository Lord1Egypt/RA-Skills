## Description: <br>
Queries SPX Express and CAINIAO Malaysia shipment tracking numbers through SPX and returns structured JSON, human-readable text, or a one-line status summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WizisCool](https://clawhub.ai/user/WizisCool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check SPX Express or CAINIAO Malaysia delivery status from a tracking number, including ETA, timeline, route, and delay details. <br>

### Deployment Geography for Use: <br>
Malaysia <br>

## Known Risks and Mitigations: <br>
Risk: Tracking requests send user-provided SPX or CAINIAO tracking numbers to spx.com.my and may return shipment details such as recipient, route, and timing. <br>
Mitigation: Use the skill only for intended SPX or CAINIAO shipments and share the minimum tracking details needed for the user's request. <br>
Risk: The optional cookie can contain browser session data. <br>
Mitigation: Avoid using the cookie unless necessary; never log it, echo it, or paste broad browser session cookies into shared or untrusted environments. <br>
Risk: The skill depends on the external SPX API and network availability. <br>
Mitigation: Handle request and parse failures explicitly, and avoid treating unavailable or stale API results as confirmed delivery status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WizisCool/spx-tracking) <br>
- [SPX Express tracking site](https://spx.com.my/) <br>
- [SPX tracking API endpoint](https://spx.com.my/shipment/order/open/order/get_order_info) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands] <br>
**Output Format:** [JSON, human-readable text report, or one-line summary selected by --format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 or python and requests; optional cookie input can contain session data and should not be logged.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
