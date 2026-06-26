## Description: <br>
Check wind and weather conditions for wind sports (kitesurfing, wingfoiling, surfing). Get forecasts, find spots nearby, view session history, and request new spots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jumptrnr](https://clawhub.ai/user/jumptrnr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to check wind-sports forecasts, compare nearby spots, review personal session data, and request calendar blocks for rideable forecast windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated features use a WindSensei API key. <br>
Mitigation: Store the key in WINDSENSEI_API_KEY and prefer Bearer-token authentication instead of putting keys in URLs. <br>
Risk: Calendar actions can reserve incorrect times, time zones, or locations if forecast details are misunderstood. <br>
Mitigation: Review proposed calendar events, times, time zones, and locations before allowing the agent to create them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jumptrnr/windsensei) <br>
- [WindSensei](https://windsensei.com) <br>
- [WindSensei API Key Manager](https://windsensei.com/dashboard/profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls, configuration] <br>
**Output Format:** [Markdown with concise natural-language summaries and occasional JSON or shell-style configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use optional WINDSENSEI_API_KEY for personalized forecasts, favorites, history, and social features.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
