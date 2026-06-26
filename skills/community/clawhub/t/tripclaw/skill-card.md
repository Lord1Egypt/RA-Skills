## Description: <br>
将 OpenClaw 生成的自驾行程导入到 TripClaw 应用。当用户说"导入行程到 TripClaw"、"同步到 TripClaw"、"发送到 TripClaw"、"推送到 TripClaw" 或提及 TripClaw 行程同步时触发。支持将行程数据（途经点、住宿、活动、预算等）通过 API 同步到用户的 TripClaw 账户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tripclaws](https://clawhub.ai/user/tripclaws) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to structure OpenClaw-generated road trip itineraries and sync them into a user's TripClaw account. It supports importing waypoints, lodging, activities, dates, traveler counts, and budget details through the TripClaw API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Itinerary data can include routes, lodging, activities, dates, traveler counts, and budget details that are sent to TripClaw. <br>
Mitigation: Ask to review the itinerary JSON before syncing and use the skill only when the user wants those details sent to TripClaw. <br>
Risk: The TripClaw API key grants access to the user's TripClaw account. <br>
Mitigation: Keep the API key private, store it locally, avoid exposing it in shared logs or screenshots, and prefer a revocable or scoped key when available. <br>


## Reference(s): <br>
- [TripClaw API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tripclaws/tripclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON itinerary data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces TripClaw import instructions and command invocations; the bundled script returns JSON responses from the TripClaw API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
