## Description: <br>
Handle tasks that arrive from StageWhisper live calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piotraleksander](https://clawhub.ai/user/piotraleksander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams using StageWhisper live-call workflows can use this skill to turn in-call follow-up tasks into concise research, drafting, scheduling, lookup, or notification responses while the call context is still current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to act immediately on live-call follow-ups that may involve calendars, messages, internal records, or documents without clear approval boundaries. <br>
Mitigation: Install it only where connected tools can be restricted, and require human review or policy checks before sending messages, creating calendar events, updating records, or accessing sensitive systems. <br>
Risk: Ambiguous call context could lead to incorrect follow-up content or actions. <br>
Mitigation: Have the agent choose the safe version of ambiguous tasks, state assumptions briefly, and call out missing access or other blockers before taking externally visible action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piotraleksander/stagewhisper-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Short text or Markdown responses with task results, assumptions, and blockers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include draft messages, summaries, lookup results, scheduling proposals, and blocker notes depending on available connected tools.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
