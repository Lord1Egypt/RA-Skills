# Recommendations

Use this reference for proactive suggestions and feedback.

## Intent Routing

- Use `recommendation.record` when the Skill/AI has formed a concrete recommendation candidate from saved memory, operation lessons, verified topology, user request context, or the just-completed task.
- Use `recommendation.list` after `recommendation.record`, when the user asks for suggestions, or when Runtime already returned a recommendation.
- Use `recommendation.feedback` for accept, reject, hide, cooldown, or "do not suggest this again" feedback.

## Recommendation Boundary

- Runtime is an objective local store for recommendation candidates and feedback. It does not decide what should be recommended from fuzzy wording, memory, or interaction history.
- The Skill/AI owns subjective recommendation judgment: whether to recommend, what to recommend, how to explain it, and which evidence is relevant.
- Before presenting a proactive local recommendation, save the candidate with `recommendation.record`, then call `recommendation.list` and present the returned pending item.
- Present at most one non-essential recommendation in a conversation.
- Do not surface recommendations during troubleshooting, auth recovery, destructive-change confirmation, or error handling unless the user explicitly asks.
- A recommendation may propose a scene, automation, lighting design, naming cleanup, favorite organization, repair, energy saving, capability discovery, or memory update, but any persistent change must go through Runtime execution after any caller-side user confirmation that is needed.
- `memory.remember` and `recommendation.list` do not materialize recommendations by themselves. If saved preferences imply a useful suggestion, the Skill must author a concise candidate and store it with `recommendation.record`.
- If Runtime returns no recommendation, say there is no current local recommendation. Do not fill the gap with an unrecorded model-only recommendation.

## Candidate Types

- Repeated action sequence: suggest a reusable scene, not an immediate persistent write.
- Stable time behavior: suggest an automation only after Runtime returns enough evidence and the user asks or accepts.
- Repeated correction after a scene: suggest adjusting that scene, with an impact preview.
- Naming conflict or duplicate target: suggest renaming or grouping cleanup.
- Invalid or missing dependency: suggest repair, replacement, or a manual app step if Runtime cannot fix it.
- Night long-on or repeated forgotten-off behavior: suggest energy saving, delayed off, or a low-risk reminder.
- Unused capability: suggest a discovery action only when Runtime proves the capability exists.
- Lighting gap: suggest a lighting design plan; applying it still uses the relevant Runtime intent.

## Candidate Payload

`recommendation.record` stores a structured candidate. Required fields are:

- `type`: short category such as `scene`, `automation`, `lighting_design`, `favorite`, `cleanup`, `repair`, `memory`, or `capability_discovery`.
- `explanation`: one short user-facing reason or benefit.
- `evidence`: desensitized evidence such as saved memory id/type, operation lesson symptom, repeated correction summary, verified topology, or current user request. Do not store full logs or full transcripts.

Recommended optional fields:

- `source`: normally `ai_skill`; use `operation_lesson`, `memory`, `interaction_signal`, or `user_requested` only when that is the direct source.
- `targetIntent`: Runtime intent that would execute the suggested change, for example `scene.create`, `automation.create`, `lighting.design.import`, `favorite.add`, or `memory.remember`.
- `scopeType` and `scopeRef`: `home`, `room`, `device`, `scene`, `automation`, or `profile` plus a short natural reference.
- `priority`: small integer where higher means more useful.
- `confidence`: `low`, `medium`, or `high`.
- `actionHint`: small object with the next action label or target. Keep it short.
- `parametersHint`: small object with safe, non-secret structured hints for the future Runtime request.

Example:

```json
{
  "intent": "recommendation.record",
  "parameters": {
    "houseId": "200193",
    "type": "automation",
    "source": "ai_skill",
    "targetIntent": "automation.create",
    "scopeType": "room",
    "scopeRef": "主卧",
    "confidence": "high",
    "priority": 80,
    "explanation": "可以把你偏好的浪漫暖光做成主卧晚间放松自动化，后续一键启用。",
    "evidence": "本地记忆：ambience=prefer_romantic_warm；用户刚完成主卧灯光设计",
    "actionHint": {
      "label": "创建主卧晚间放松自动化"
    },
    "parametersHint": {
      "targetIntent": "automation.create",
      "roomName": "主卧",
      "tone": "warm_romantic"
    }
  }
}
```

## Display Threshold

- Do not show a recommendation during auth recovery, diagnostics, destructive-change confirmation, or high-risk confirmation.
- If the current user task completed successfully and you can articulate one high-confidence useful next step, call `recommendation.record`, then `recommendation.list`, and present it as one optional next step.
- If the user asks "有什么建议", inspect relevant saved memory or operation lessons when useful, record at most one concrete candidate if you have one, then call `recommendation.list` and summarize returned candidates in priority order.
- If the suggestion would create or change cloud configuration, say it is a proposal and route the actual change through Runtime execution.

## Feedback And Suppression

- Use `recommendation.feedback` for accepted, rejected, dismissed, cooldown, and permanent suppression outcomes.
- For `recommendation.feedback`, use the concrete `recommendationId` returned by `recommendation.record` or `recommendation.list`. Do not try to identify a recommendation only by type, scope, or explanation text.
- Respect rejection, cooldown, and permanent suppression decisions.
- If the user says "do not suggest this again" or equivalent, treat it as permanent suppression until Runtime says it was restored.
- Accepted recommendations must not be repeated as pending suggestions unless Runtime returns a new distinct item.

## Explanation Rules

- Keep user-facing reasons short and based on Runtime evidence.
- Recommendation evidence must be explainable and desensitized.
- Explain the concrete pattern or benefit from the evidence you stored, for example saved preference, repeated correction, operation lesson, verified topology, invalid dependency, naming conflict, or unused capability.
- Do not say only "I recommend an automation" or imply server-side AI recommendations. Make clear it is a local Skill-authored suggestion stored through Runtime.
- If Runtime returns no recommendation, say there is no current suggestion rather than filling the gap with model guesses.
- Good explanations mention the observed pattern, target scope, and user benefit, while avoiding full logs, secrets, exact internal IDs, or full transcripts.
