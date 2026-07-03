# Memory And Personalization

Use this reference for local memory, preferences, and personalization.

## Intent Routing

- Use `memory.remember` only for an explicit preference the user wants saved.
- Use `memory.list` when the user asks what is remembered.
- Use `memory.pause` or `memory.resume` for learning controls.
- Use `memory.forget` with `preferenceIds[]` and/or `recommendationIds[]` when the user asks to remove specific remembered preferences or recommendations. Use broad `memory.forget` without IDs only when the user explicitly asks to forget/export-and-delete all local memory for the current profile and house.
- For single-preference `memory.remember`, pass structured fields `scopeType`, `scopeRef`, `preferenceType`, `preferenceValue`, optional `kind`, optional `status`, and `evidence`; do not wrap the preference inside a nested free-form object.
- For multi-preference memory from one utterance, prefer one `memory.remember` request with `parameters.preferences[]`. Each item has the same fields as a single preference. This is the preferred shape for "浪漫色调还有高端奢华" because it avoids multiple Runtime calls while keeping each memory atomic.
- When the user clearly says "remember", "use this by default later", "I prefer", or "I dislike", the Skill must structure the preference before calling `memory.remember`. Runtime will not interpret subjective natural language into preference types or values.

## Runtime Memory Is Primary

- Yeelight Runtime memory is the source of truth for Yeelight-domain preferences. Host memory such as WorkBuddy, Codex, or another assistant's generic memory file is only auxiliary and must not replace Runtime `memory.remember`.
- If a user asks to remember a Yeelight lighting, product, room, scene, automation, recommendation, or home-design preference, save it through Runtime first. Only say "已记录/已保存" after Runtime returns `success` or `partial`.
- If the host platform also wants to save a generic memory, write it only after Runtime succeeds and keep the response clear that the Yeelight Runtime memory was saved.
- In hosts with their own memory tool, treat Yeelight-domain phrases such as "记住主卧偏暖", "以后儿童房夜里别太亮", "我不喜欢彩光动效", or "别再推荐这个自动化" as Runtime-memory requests, not host-memory-only requests. Calling only the host memory tool is an incomplete Skill execution.
- Runtime is not the memory judge. It accepts structured `preferenceType` and `preferenceValue`, validates and stores them, merges exact same structured preferences, and returns the saved record. Deciding what should be remembered and how to split subjective wording happens before the Runtime call.
- Runtime handles local memory storage and migration. Do not instruct users to inspect internal files; use `memory.list`, `memory.remember`, `memory.pause`, `memory.resume`, or `memory.forget`.

## Memory Classes

- Profile-level preferences: stable user tastes that should influence future design recommendations when the same Runtime profile and region are active, such as "喜欢高端奢华", "不要彩光", or "偏好暖色舒适氛围". Save them with `scopeType:"profile"` and empty `scopeRef` in the current `profile + region + houseId` shard. Do not assume Runtime automatically merges profile memories across different homes; if cross-home reuse matters, the Skill must deliberately query/write the current home scope.
- Home-level preferences: tastes or policies for one family/home, such as "这个家走温馨浪漫路线", "这个家不要自动推荐派对动效".
- Room-level preferences: room-specific defaults such as "孩子屋夜里别太亮", "主卧偏暖一点".
- Scene/task-level preferences: recurring activity preferences such as "观影时不要开主灯", "阅读模式要亮一点".
- Entity alias/purpose memories: user-defined names, room purposes, and preference-shaped labels that help future targeting, for example "粒粒的房间就是孩子屋".
- Explicit preferences are direct user instructions such as preferred ambience, disliked color modes, aliases, room purposes, or "do not recommend" choices.
- Strong memory signals are explicit phrases such as "记住", "记一下", "帮我记", "以后默认", "以后都", "以后帮我", "我喜欢", "我偏好", "我不喜欢", "别再", "不要推荐", "use this by default later", "I prefer", or "I dislike". Route these to `memory.remember`.
- Medium memory signals are repeated corrections or repeated preference-shaped behavior observed by the assistant. Treat them as suggestions to ask the user whether to remember, not as saved Runtime memory.
- Weak interaction signals are ordinary one-off operations. Runtime may keep coarse interaction counters for local diagnostics, but the Skill must not claim they became memory.
- Single behavior observations, one correction, one undo, one failed write, one diagnostic result, or one temporary command are not long-term memory by themselves.
- Current-turn instructions override saved preferences. Explicit dislikes override explicit likes, accepted personalization, and generic recipes.

## Trigger Policy

Use this trigger order instead of relying on vague intuition:

1. Direct save: user explicitly asks to remember, set future defaults, avoid future recommendations, or states a stable preference with "我喜欢/我不喜欢/我偏好/以后". Structure and call `memory.remember`.
2. Ask before saving: user repeatedly corrects the same dimension across turns, reacts strongly to a recommendation, or says something preference-shaped without an explicit save verb. Ask one concise question such as "要把这个作为以后设计的默认偏好吗？".
3. Do not save: one-time controls, current-scene instructions, device state, current topology, product search results, error logs, execution transcripts, low-level ids, and temporary tests.
4. Never save: tokens, secrets, account data, cookies, authorization material, full chat transcripts, or private data unrelated to Yeelight personalization.

The trigger is an AI/Skill decision, not Runtime inference. Runtime should receive only the final structured memory payload.

## Preference Extraction

- Save only useful preference assertions: preferred brightness/色温/彩光 policy, room purpose, friendly alias, recommendation suppression, or recurring comfort rules.
- Scope the memory as narrowly as the user says. "卧室晚上" is not "全屋全天"; "客厅观影" is not every scene.
- Preserve negative preferences exactly enough to act on them later, for example "不要彩光", "夜里别太亮", "别再推荐自动化".
- Do not save factual cloud state such as current device list, member list, product data, one-time commands, diagnostic errors, dry-run previews, or execution transcripts as memory.
- If the user's wording is a correction to the last result, the Skill must decide whether it is an explicit memory request, a current-turn instruction, or ordinary feedback. Route only explicit saved preferences to `memory.remember`.

## Trigger Mapping

| User wording | Preference type | Normalized value guidance | Notes |
| --- | --- | --- | --- |
| "记住我喜欢浪漫色调", "温馨浪漫", "有氛围感", "有情调" | `ambience` | `prefer_romantic_warm` | Treat as a profile/home/room ambience preference depending on wording. It can influence lighting-design recipes and scene tone. |
| "高端奢华", "旗舰", "预算充足", "Pro/M20/E+/S/P 系列优先" | `product_preference` | `prefer_premium_luxury` | Treat as product positioning, not a lighting color preference. It can influence product candidate selection. |
| "柔和暖光", "偏暖一点", "暖白" | `color_temperature` | `prefer_warm` | Same-meaning warm preferences should merge. |
| "夜里别太亮", "不要刺眼", "暗一点" | `brightness` | `prefer_dimmer` | Keep separate from color temperature. |
| "不要彩光", "不喜欢彩色灯效" | `color` | `avoid_colorful` | Explicit dislike overrides generic colorful recipes. |
| "这个房间是孩子屋/老人房/书房/电竞房" | `room_purpose` | concise purpose value such as `child_room`, `elder_room`, `study`, `gaming_room` | Helps future lighting design and targeting. |
| "这个灯以后叫阅读灯", "粒粒房间就是孩子屋" | `alias` | stable alias text | Helps future entity/room resolution. |
| "别再推荐自动化", "不要推荐情景" | `recommendation` | concise suppression value | Respect future recommendation filtering. |

When one utterance contains multiple independent dimensions, save each dimension as a separate item in `parameters.preferences[]`. Example: "浪漫色调还有高端奢华" is two memory items: ambience and product preference.

## Safety And Privacy

- Memory is scoped by local profile, region, and house; never merge or reveal another account, region, or house's preferences.
- Keep profile, region, and house isolation strict. Do not combine memories across accounts, regions, homes, hosts, or families.
- Never save secrets, account data, low-level identifiers, auth material, cookies, full chat logs, or token-like values.
- Do not treat all conversation turns as memory. Runtime memory is preference state, not a transcript store.
- Local memory and recommendations are enabled by default. Treat `memory.pause` as the user's explicit opt-out and `memory.resume` as opt-in again.
- Runtime stores preferences in local memory directly when `memory.remember` succeeds. Do not recover or infer memory yourself.
- First saved memory requires Runtime consent handling. Do not claim consent, consent version, retention, export, or deletion state was recorded unless Runtime confirms it.
- Default retention: explicit preferences stay until the user forgets or deletes them; recommendation evidence and coarse interaction evidence last about 90 days. Do not claim event-history retention is implemented unless Runtime returns event-history data.
- Runtime interaction signals are coarse local counters. They store objective `intent` and response `status` evidence only, not the user's original utterance. Do not treat these weak signals as saved preference memory.
- Export results are local Runtime snapshots for the current scope. Do not promise encrypted import/export or cross-device restore unless Runtime explicitly returns that support.

## Execution Rules

- Before saving a new memory, call or consider `memory.list` when context is available. If an existing preference has the same or near-identical meaning, the Skill should map it to the same canonical `preferenceValue` instead of creating a duplicate; call `memory.remember` only to refresh the same preference with better evidence.
- Treat memory as compact preference state, not a note archive. Do not create separate records for wording variants such as "柔和暖光", "偏暖一点", and "暖白"; the Skill should normalize them into one actionable preference before calling Runtime. Keep separate records only when the action dimension is different, for example one color-temperature preference plus one brightness preference.
- Evidence should be short and additive. Summarize the useful new signal, avoid copying full conversation turns, and do not repeat evidence already present in `memory.list`.
- Prefer canonical values over prose when the value will drive behavior: `prefer_romantic_warm`, `prefer_premium_luxury`, `prefer_warm`, `prefer_dimmer`, `avoid_colorful`. Use short prose only when no stable canonical value exists yet.
- `memory.remember` is a direct local upsert. Runtime does not perform subjective synonym extraction. The Skill must pass the same canonical `preferenceValue` for same-meaning memories, for example `prefer_romantic_warm` or `prefer_premium_luxury`. Runtime then merges exact same structured preferences and evidence. If a single utterance contains distinct preferences, such as ambience plus product positioning, save each distinct preference once.
- For multiple distinct preferences in one utterance, prefer:
  ```json
  {
    "parameters": {
      "houseId": "<current-house-id>",
      "preferences": [
        {
          "scopeType": "profile",
          "preferenceType": "ambience",
          "preferenceValue": "prefer_romantic_warm",
          "evidence": "用户明确要求记住喜欢浪漫色调"
        },
        {
          "scopeType": "profile",
          "preferenceType": "product_preference",
          "preferenceValue": "prefer_premium_luxury",
          "evidence": "用户明确要求记住高端奢华产品定位"
        }
      ]
    }
  }
  ```
- `memory.forget` with `preferenceIds[]` and/or `recommendationIds[]` exports and deletes only those local records. Without IDs it exports the current scope snapshot and deletes local consent, preferences, and recommendations for that scope; use that broad form only for an explicit "forget all local Yeelight memory for this home" request.
- `memory.pause` and `memory.resume` affect local learning only; they do not change cloud devices or home configuration.
- Persistent home changes suggested by memory still require Runtime execution and any caller-side user confirmation appropriate to the operation.
- Unsaved preference guesses must not directly create room, group, scene, automation, device, gateway, or favorite configuration.
- Low-risk personalization may adjust wording or suggested defaults only when Runtime returns saved memory or recommendation evidence; still explain that it is a preference-based local suggestion, not an applied home change.
- After Runtime confirms `memory.remember`, Runtime stores memory only. If the saved preference implies a useful future suggestion, the Skill may create a structured candidate with `recommendation.record`, then call `recommendation.list` before presenting it.
- Recommendation feedback such as reject, cooldown, or permanent suppression must be respected.
- If the user asks why a suggestion appeared, cite Runtime's returned memory/recommendation evidence, not hidden reasoning or full history.

## Cleaning And Compression

- The memory file should stay compact because Runtime upserts exact same structured preferences. The Skill is responsible for preference consolidation by using the same canonical value for same-meaning preferences.
- When `memory.list` shows several records that are equivalent but use different values, do not add another duplicate. Save one canonical replacement with better evidence and, if needed, tell the user you consolidated future behavior around that preference.
- Do not preserve every wording variant. Evidence can mention the latest useful phrase, but `preferenceValue` should remain stable.
- Prefer narrow scopes. A room-level correction should not overwrite profile/home taste unless the user says it is global.
- Review stale or conflicting memories conversationally. If the user says "我现在不喜欢浪漫风了", save the new explicit preference or recommendation suppression; do not silently delete old records unless the user asks to forget.
- Use targeted `memory.forget` only for explicit delete/export-and-delete requests for known records. Normal cleanup should be structured consolidation through canonical values, not broad deletion.

## Examples

User: "记住我喜欢喜欢浪漫的色调还有高端奢华"

Preferred single Runtime call:

```json
{
  "contractVersion": "1.0",
  "requestId": "memory-romantic-premium-001",
  "locale": "zh-CN",
  "utterance": "记住我喜欢喜欢浪漫的色调还有高端奢华",
  "intent": "memory.remember",
  "parameters": {
    "houseId": "<current-house-id>",
    "preferences": [
      {
        "scopeType": "profile",
        "preferenceType": "ambience",
        "preferenceValue": "prefer_romantic_warm",
        "evidence": "用户明确要求记住喜欢浪漫色调"
      },
      {
        "scopeType": "profile",
        "preferenceType": "product_preference",
        "preferenceValue": "prefer_premium_luxury",
        "evidence": "用户明确要求记住高端奢华产品定位"
      }
    ]
  }
}
```

If the assistant cannot confidently split the utterance, ask one concise clarification question or save only the dimension it can structure safely. Do not send an unstructured natural-language memory and expect Runtime to infer subjective meaning.

Expected assistant response after Runtime success:

```text
已写入 Yeelight 本地记忆 2 条：浪漫暖色氛围偏好、高端奢华产品偏好。以后做照明设计和产品选型时会优先参考这两条。
```

Do not say it was saved if only host memory was updated or Runtime returned `clarification_required`, `blocked`, or `auth_required`.
