## Description: <br>
Tracks Qantas Freight shipments by air waybill number and returns origin, destination, shipper, consignee, pieces, weight, ETD, and latest shipment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sicl](https://clawhub.ai/user/sicl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to format Qantas Freight air waybill tracking results into readable shipment summaries, including support for multiple AWBs and common missing-data cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment results may include business contact names such as shipper and consignee. <br>
Mitigation: Use the skill only for AWBs the user is authorized to check and avoid sharing returned shipment details unnecessarily. <br>
Risk: Missing or empty tracking responses can lead to incomplete shipment summaries. <br>
Mitigation: Return the documented not-found or fallback status instead of inventing missing shipment events. <br>


## Reference(s): <br>
- [Qantas Freight Tracking on ClawHub](https://clawhub.ai/sicl/qantas-freight-tracking) <br>
- [Publisher profile: sicl](https://clawhub.ai/user/sicl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary tables with expandable details blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles up to 10 AWBs and may include shipment business contact names such as shipper and consignee.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
