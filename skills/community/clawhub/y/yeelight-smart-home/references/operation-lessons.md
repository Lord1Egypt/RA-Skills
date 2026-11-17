# Operation Lessons

Use this reference for reusable Skill/Runtime usage experience discovered during real operation.

Operation lessons are not user taste memory, cloud topology, diagnostics transcripts, or recommendations. They are compact local notes that help future agents avoid known Skill/Runtime pitfalls and choose faster, more reliable paths.

## Intent Routing

- Use `operation.lesson.list` before a complex, previously failed, or parameter-heavy operation when a known lesson could avoid wasted turns.
- Use `operation.lesson.record` after a failed, blocked, unsupported, confusing, slow, or workaround-based actual operation attempt only when the cause is confirmed reusable Runtime behavior, a stable cloud boundary, a payload-shape rule, a fallback, or a fast path. This is not limited to lighting design. If the next attempt succeeds because the Skill changed target resolution, payload shape, fallback intent, or fast path, record the reusable lesson before the final user response. Do not record one-off failures, guesses, or cases where the current Runtime response already gives the clear supported path.
- Do not use operation lessons for normal user preferences. Use `memory.remember` for preferences such as ambience, product positioning, room purpose, or recommendation suppression.
- Do not use operation lessons for a one-off current state result, full chat transcript, secret, token, Runtime internal request detail, or private account data.

## Lesson Types

Use one of these `lessonType` values when possible:

| Type | Meaning |
| --- | --- |
| `fast_path` | A faster way to complete a common user goal. |
| `resource_resolution` | How to resolve names, rooms, devices, scenes, automations, or aliases reliably. |
| `parameter_shape` | A precise nested JSON or payload-shape requirement learned from Runtime responses. |
| `failure_pattern` | A repeated error pattern with cause and recovery path. |
| `fallback` | A safer or more reliable alternative intent when the first path is unavailable. |
| `capability_gap` | A confirmed unsupported or not-yet-registered capability that should not be retried blindly. |

## Record Shape

Preferred request:

```json
{
  "contractVersion": "1.0",
  "requestId": "operation-lesson-scene-update-001",
  "locale": "zh-CN",
  "utterance": "记录 scene.update 参数经验",
  "intent": "operation.lesson.record",
  "parameters": {
    "lesson": {
      "intent": "scene.update",
      "lessonType": "parameter_shape",
      "symptom": "invalid_scene_update_payload when guessing nested scene actions",
      "cause": "acceptedFields lists top-level fields but does not define the nested action rows",
      "recommendedPath": "Call scene.detail.get first, use editablePayload/updateShape, then read-modify-send the complete action list.",
      "avoid": "Do not invent nested action rows from acceptedFields alone.",
      "fallbackIntent": "scene.create",
      "evidence": "Runtime returned invalid_scene_update_payload during update attempt.",
      "source": "runtime_response",
      "confidence": "high",
      "status": "confirmed",
      "stale": false,
      "lastValidatedAt": 1780000000
    }
  }
}
```

Required fields:

- lesson `intent`: the target capability that future agents should learn about, not `operation.lesson.record`.
- lesson `lessonType`: use the taxonomy above.
- lesson `symptom`: short observed symptom or error.
- lesson `recommendedPath`: concise action path to use next time.

Optional fields:

- `cause`: why the issue happens, only if known.
- `avoid`: what future agents should not do.
- `parametersHint`: minimal payload-shape note or compact JSON hint.
- `fallbackIntent`: Runtime intent to try when the primary path is unavailable.
- `evidence`: short, sanitized evidence such as an error code or result summary.
- `source`: one of `ai_skill`, `runtime_response`, `validated_cli`, or another short objective source tag.
- `confidence`: `low`, `medium`, or `high`. Use `high` only for actual Runtime behavior or source-backed code review, not guesses.
- `status`: usually `confirmed`; use `candidate` only for a lesson that still needs more evidence, `deprecated` for a superseded path, and `rejected` for a bad lesson.
- `stale`: set `true` when a newer Runtime response or code review shows the lesson should not guide normal execution.
- `lastValidatedAt`: Unix seconds when this lesson was last verified by Runtime behavior, tests, or source-backed review.

## Query Shape

Before a complex operation, query by intent or symptom:

```json
{
  "contractVersion": "1.0",
  "requestId": "operation-lesson-list-scene-update-001",
  "locale": "zh-CN",
  "utterance": "查询 scene.update 的实操经验",
  "intent": "operation.lesson.list",
  "parameters": {
    "intent": "scene.update",
    "status": "confirmed",
    "minConfidence": "medium",
    "limit": 5
  }
}
```

Useful filters:

- `intent`: exact Runtime intent such as `scene.update`, `lighting.design.import`, or `light.power.set`.
- `lessonType`: one of the lesson types above.
- `query`: text search across symptom, cause, recommended path, avoid, parameters hint, fallback, and evidence.
- `status`: optional exact status filter: `candidate`, `confirmed`, `deprecated`, or `rejected`.
- `source`: optional source filter.
- `minConfidence`: optional threshold: `low`, `medium`, or `high`.
- `includeStale`: default is false. Set true only during cleanup, debugging, or when you need to inspect superseded knowledge.
- `includeRejected`: default is false. Set true only during cleanup or audit.
- `limit`: default is 10; keep small for fast context.

## Trigger Policy

After every non-successful or surprising attempt, run this check before the final answer:

1. Does the current Runtime response already give a clear supported path, or is the issue a one-off failure or unverified guess? If yes, do not record a user lesson; follow the current Runtime response instead.
2. Did the attempt reveal a reusable way to avoid future failure, extra turns, wrong target resolution, bad payload shape, unsupported intent retry, or unreliable path that cannot be fixed in the current flow?
3. Is the evidence from actual Runtime behavior, validated CLI behavior, or a Runtime response?
4. Can the lesson be summarized without secrets, internal request headers, full transcripts, private unrelated data, or cloud topology snapshots?

If answers 2-4 are yes and answer 1 is no, call `operation.lesson.record` before finalizing. Do not skip this just because the user goal eventually succeeded; the exact purpose of lessons is to prevent the next agent from repeating the failed path first.

Record a lesson when all are true:

- The issue or path is reusable for future users or future turns.
- The lesson was learned from actual Runtime use, a Runtime response, or validated CLI behavior.
- The lesson can be expressed without secrets, tokens, internal request headers, full transcripts, or private unrelated data.
- The lesson is more specific than the public reference text.

## Must-Consider Capture Matrix

Use this matrix after any non-success, partial, surprising success, extra-turn workaround, or user-reported failed AI attempt. If the row matches and the evidence is from Runtime/CLI behavior, record a lesson before the final answer.

| Observed pattern | Lesson type | Scope guidance | Record when |
| --- | --- | --- | --- |
| A request fails or asks clarification until the Skill adds a room, home, entity type, target qualifier, alias, or exact name. | `resource_resolution` | House-specific when it depends on current topology or naming; profile-global for a reusable resolver rule. | The added qualifier is what made the next attempt succeed or avoid ambiguity. |
| A write fails because nested action lists, ordered item lists, room design blocks, condition blocks, object detail blocks, parameter objects, button events, or design slots were guessed. | `parameter_shape` | Usually profile-global unless one home's current scene/automation content is the cause. | `intent.explain`, `payloadShape`, `editablePayload`, `updateShape`, or a Runtime clarification reveals the correct shape. |
| A read-modify-send flow is required before update, or detail read proves the object cannot safely be updated. | `parameter_shape` or `fallback` | House-specific if tied to one scene/automation/device; profile-global for a stable adapter rule. | The successful path uses detail/readback first, or switches to create/replace because update is not safe. |
| An intent is blocked, unsupported, backend-refused, or returns `safeToRetry=false`, and another intent or manual/design-only path is the reliable answer. | `fallback` or `capability_gap` | Profile-global for stable Runtime/cloud boundary; house-specific when missing gateway/sensor/capability is local topology. | Retrying the same payload would waste turns or risk confusion. |
| A write returns `partial`, write verification mismatch, or a post-write readback changes what the Skill should say or do next. | `failure_pattern` | House-specific if tied to live topology; profile-global if the verification rule is general. | Future agents need the verification/readback rule to avoid claiming too much. |
| Product words, SKU names, series aliases, or product pedia terms were mistaken for installed devices, or the fix was to treat them as candidate products/design slots. | `resource_resolution` | Profile-global unless a specific home has a custom alias causing the confusion. | The boundary between installed device, future slot, and product knowledge affected the successful path. |
| A missing dependency such as sensor, gateway, capability, room, area, or automation trigger changes execution into a design note, recommendation, or safe alternative. | `capability_gap` or `fallback` | House-specific when the dependency is missing only in this home. | The agent must not invent the dependency and should reuse the same safe alternative later. |
| A high-risk action only becomes acceptable after dry-run, preview, explicit confirmation, or a different lower-risk lane. | `fast_path` or `failure_pattern` | Profile-global for safety-lane rules; house-specific if tied to one resource. | The safer flow is reusable and prevents accidental destructive or permission-sensitive action. |
| A common user goal took extra calls because the agent preflighted with broad lists or used an over-complex path, then a direct intent succeeded. | `fast_path` | Profile-global. | The direct Runtime intent is confirmed and materially reduces turns without reducing safety. |
| A current public reference exists but a real host agent still missed it due to ambiguous trigger wording. | Usually do not record; update Skill/reference wording. | N/A | Record only when there is also a concrete Runtime-backed symptom and a reusable path, not merely because a prompt was ignored. |

Common must-record cases:

- `clarification_required`, `blocked`, `not_supported`, or `error` exposes a reusable payload/field/target mistake.
- A first attempt fails and a second attempt succeeds because the Skill switched to a different confirmed intent, payload shape, read-modify-send flow, target qualifier, or fallback path.
- An intent is unavailable and a known fallback should be used next time.
- A direct user goal took multiple Runtime calls only because the target resolution path was unclear.
- A new-home import accidentally used the current selected home or a named-home reference incorrectly.
- A Runtime response proves a documented path is stale, incomplete, or misleading.
- A dependency gap, product-vs-installed-device confusion, safety-lane change, write-verification mismatch, or backend `safeToRetry=false` result changes the path future agents should use.

Do not record:

- Ordinary successful one-off commands.
- User preferences or style choices.
- Cloud topology snapshots such as current device lists or scene IDs.
- Temporary test data, transient request IDs, or full payload dumps.
- Guesses that were not verified by Runtime behavior or validated CLI behavior.

When the current Runtime contract already handles the behavior directly, do not record another operation lesson. When the behavior is a stable cloud/runtime boundary or a reusable fallback that remains true across normal use, record the lesson.

## Applying Lessons

- Treat returned lessons as local operational guidance, not proof that the current cloud state still exists.
- If a lesson says an intent is unsupported, do not retry it blindly. Use the recommended fallback or explain the current limitation.
- If a lesson gives a fast path, prefer it only when the user's current request matches the same scope and risk.
- If a lesson describes a payload shape, still respect the current Runtime clarification, `payloadShape`, `editablePayload`, and `updateShape`.
- If a lesson is stale or contradicted by a newer Runtime response, record a corrected lesson with better evidence.
- When a lesson is no longer reliable, record the same target/symptom with `status=deprecated` or `stale=true` and better evidence instead of leaving it as active guidance.
- Prefer active `confirmed` lessons with `medium` or `high` confidence. Treat `candidate` lessons as hints to verify, not as instructions.

## Boundaries

- Runtime stores caller-structured lessons only. It does not infer subjective experience from user utterances.
- Operation lessons are profile-global when no `houseId` is supplied. Prefer profile-global lessons for reusable capability behavior, payload shapes, fastest paths, supported-intent fallbacks, safety-lane rules, and general resource-resolution patterns. This is the right scope when the rule should help future homes.
- Include `houseId` only when the lesson depends on one home's current topology, naming conflict, device capability, scene content, automation content, or other house-specific state. Do not attach reusable lessons to disposable test homes; otherwise future agents in normal homes may not find them.
- Querying with a house context can return both house-specific and profile-global lessons.
- Operation lessons must never replace Runtime execution, validation, or write verification.

## Known Runtime Boundaries

Keep only stable cloud/runtime limits here. If Runtime already returns a public `clarification`, `partialState`, `editablePayload`, `updateShape`, or safe fallback, use that contract instead of recording another operation lesson.

- A design-import sandbox with no effective bound gateway can expose readable rooms, slots, groups, scenes, and automations while still blocking live control or execution. First check Runtime evidence such as gateway `bind` and device slot binding; use read-only detail/list validation for design metadata, and do not retry direct control when Runtime returns `safeToRetry=false`.
- Imported design automations can be enabled, disabled, listed, and inspected, but `automation.update` can return backend `403 禁止访问` for an automation created by `lighting.design.import` even when the same complete rule shape succeeds for an automation created through `automation.create`. For an imported design automation edit, report the backend refusal and prefer creating a replacement live automation with `automation.create`; only delete or disable the imported rule after the user explicitly confirms the persistent change.
- After a partial design-slot import, treat residual slots, groups, and scenes as planning metadata until Runtime proves they are valid execution resources. A readable `scene.detail.get` or `editablePayload` is not proof that `scene.update`, `scene.execute`, or `scene.test` will work.
- `scene.test` or `scene.execute` can return backend business code `1611` with message `当前情景无有效网关` in homes without an effective gateway, even when `scene.detail.get` returns a readable action list. Treat Runtime `safeToRetry=false` as final for the same payload; report that the scene needs a valid executable gateway/home instead of retrying or changing sibling scene intents.
- `home.sort.configure` accepts public sort items such as `items[].entityType` plus `items[].id`/`targetId` and Runtime translates them before writing. Dev cloud can still return backend `500 服务器内部错误` for the actual sort write after validation. When this happens, report the backend failure and do not retry equivalent payloads with internal numeric sort fields.
- For direct light control, `state.query` is the reliable live read. If `light.power.set`, `light.brightness.set`, `light.color_temperature.set`, or `light.color.set` reaches Runtime but returns a backend business error, report the execution failure and do not retry sibling light intents or fall back to a legacy behavior-execution path.
