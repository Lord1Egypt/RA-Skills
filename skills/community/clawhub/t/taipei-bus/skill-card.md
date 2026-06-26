## Description: <br>
查詢台北市、新北市公車及公路客運動態資訊、路線圖及預估到站時間。當用戶詢問公車動態、特定公車路線、或提供台北市公車動態網址（pda5284.gov.taipei）或公路客運網址（taiwanbus.tw）時使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dabendan2](https://clawhub.ai/user/dabendan2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Taipei, New Taipei, and Taiwan highway bus routes, live arrival estimates, route maps, and current vehicle-position details from public transit websites. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: Route numbers or transit questions may be sent to public transportation websites during lookup. <br>
Mitigation: Use the skill only for non-sensitive transit queries and tell users when public transit sites are being consulted. <br>
Risk: Arrival times can be misstated if the agent rounds, converts, or paraphrases the source website's live status text. <br>
Mitigation: Report the exact displayed values such as station names, arrival minutes, and live status labels without converting them into broader estimates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dabendan2/taipei-bus) <br>
- [Taipei City Bus Dynamic Information System](https://pda5284.gov.taipei/MQS/routelist.jsp) <br>
- [TaiwanBus real-time route query](https://www.taiwanbus.tw/eBUSPage/Query/QueryResult.aspx?rno=[route_number]&lan=C) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text transit lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Arrival estimates should preserve the exact wording and precision shown by the source transit website.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
