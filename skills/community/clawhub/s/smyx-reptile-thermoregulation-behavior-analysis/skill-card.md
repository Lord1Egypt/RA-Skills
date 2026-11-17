## Description:

Through fixed enclosure cameras, the system analyzes behavior videos of reptiles (lizards, snakes, turtles) and detects movement frequency and dwell duration between the basking zone (heated area under the basking lamp) and the hiding zone (cave/cool side). | 通过爬宠箱固定摄像头，分析爬行动物（如蜥蜴、蛇、龟）的行为视频，检测宠物在晒点（加热灯下方高温区域）与躲避区（洞穴、冷区）之间的移动频次、停留时长以及活动节律。系统连续监测，生成每日温区利用报告，异常时推送提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers and operators of vivariums or breeding enclosures use this skill to review video-based dwell times, movement between basking and hiding areas, and daily activity patterns. It provides behavioral monitoring guidance and reports for husbandry review, not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says export-only mode may still proceed to account or network activity, so private footage may be uploaded even when analysis is not requested.

Mitigation: Do not use private footage until export-only mode is confirmed to stop before account or network activity.

Risk: The security review says stored account credentials lack adequate protection; authenticated requests and sensitive HTTP logging also need safeguards.

Mitigation: Protect stored tokens, restrict authenticated requests to approved HTTPS destinations, and disable automatic logging of sensitive HTTP data.

Risk: Video leaves the device, and the provider's retention and deletion practices are not verified by this client review.

Mitigation: Confirm retention and deletion practices with the provider before submitting sensitive footage.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-reptile-thermoregulation-behavior-analysis)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured behavior analysis and daily Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include zone dwell ratios, transitions per hour, activity rhythm, thermal preference labels, alerts, and husbandry suggestions.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
