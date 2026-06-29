# Recommendations

Use this reference for proactive suggestions and feedback.

## Intent Routing

- Use `recommendation.list` only when the user asks for suggestions or Runtime already returned a recommendation.
- Use `recommendation.feedback` for accept, reject, hide, cooldown, or "do not suggest this again" feedback.

## Recommendation Boundary

- Do not add, invent, rank, or queue a recommendation that Runtime did not return.
- Present at most one non-essential recommendation in a conversation, and only the item returned by Runtime.
- Do not surface recommendations during troubleshooting, auth recovery, safety confirmation, deletion approval, or error handling unless the user explicitly asks.
- A recommendation may propose a scene, automation, lighting design, naming cleanup, favorite organization, repair, energy saving, capability discovery, or memory update, but any persistent change must go through Runtime confirmation.
- Preference-based local recommendations may be returned after `memory.remember` or when `recommendation.list` materializes saved preferences. They can suggest defaults or next-step plans, but they must not create room, group, scene, automation, favorite, device, gateway, or member configuration directly.
- If Runtime returns no recommendation, say there is no current local recommendation. Do not fill the gap with model-generated advice.

## Feedback And Suppression

- Use `recommendation.feedback` for accepted, rejected, dismissed, cooldown, and permanent suppression outcomes.
- Respect rejection, cooldown, and permanent suppression decisions.
- If the user says "do not suggest this again" or equivalent, treat it as permanent suppression until Runtime says it was restored.
- Accepted recommendations must not be repeated as pending suggestions unless Runtime returns a new distinct item.

## Explanation Rules

- Keep user-facing reasons short and based on Runtime evidence.
- Recommendation evidence must be explainable and desensitized.
- Explain the concrete pattern or benefit when Runtime provides it, for example repeated time window, repeated correction, invalid dependency, naming conflict, or unused capability.
- Do not say only "I recommend an automation" or imply server-side AI recommendations.
- If Runtime returns no recommendation, say there is no current suggestion rather than filling the gap with model guesses.
