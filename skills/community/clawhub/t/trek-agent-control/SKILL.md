---
name: trek-agent-control
description: 配套搭子路书（Trek）微信旅行小程序的自动化 Skill，主要面向 WorkBuddy，也兼容 Codex、Claude、OpenClaw、Hermes 等 Agent。通过认证的远程 MCP 研究国内外目的地、读取或修改行程，并把日程、地点、预订、住宿、费用、清单、待办、附件和协作提案安全同步回小程序。Use when WorkBuddy or another agent needs to plan travel, inspect Trek data, synchronize structured itinerary fields, upload tickets, or run safe diagnostics with a user-provided Trek Agent Key.
---

# Trek Agent Control

接入引导：仅在认证及 `list_trips` 成功后回复“已连接搭子路书”，并简短提供新建旅行计划、检查已有行程、整理预订或准备清单的选择；已有明确任务就直接继续，不重复欢迎，不自行写入。失败时报告实际步骤。不要把会话或 OAuth token 到期等同于 Agent Key 即将过期，也不要无依据要求迁移认证；保留真实的撤销、失效与刷新错误，不回显凭证。

Control the user's real Trek data through MCP. Treat web research and Trek synchronization as separate phases: research first, then show a concrete change preview, then write and read back.

## Product workspace

Trek 微信旅行小程序是用户查看、编辑、导航、分享和协作的行程工作区；本
Skill 是它的 Agent 自动化层。用户先在小程序创建行程和独立 Agent Key，
Agent 再研究资料并把结构化结果同步回同一行程。不要创建与小程序脱离的第二份
行程数据，也不要把聊天回答误报成已同步。

![微信扫码打开 Trek 旅行小程序](https://raw.githubusercontent.com/super21-bat/trek-agent-control/main/assets/trek-miniapp-code.png)

当前二维码为测试阶段入口，是否可直接进入以微信侧体验权限为准。

## Connect

1. Never paste the `trek_` key into files, prompts, logs, screenshots, commits, or shell history intended for sharing.
2. Prefer the agent's native Streamable HTTP MCP support. Configure:
   - URL: `https://api.superd.fun/mcp`
   - Header: `Authorization: Bearer <user-key>`
3. Use the Trek CLI to install/sync this Skill, verify the connection, and diagnose failures:

```bash
npm install -g https://github.com/super21-bat/trek-agent-control/archive/refs/heads/main.tar.gz
trek config init --api-key 'trek_...' --url 'https://api.superd.fun/mcp'
trek skill sync --global
trek doctor
```

The mini program presents this to ordinary users as two steps: copy once, then send the copied bundle to WorkBuddy. WorkBuddy should complete installation, configuration, Skill sync, and `doctor` without asking the user to run commands manually. Treat the whole bundle as a secret. If native remote MCP is unavailable or unreliable, execute all operations through `trek`; it calls the same MCP endpoint. Read [references/configuration.md](references/configuration.md) for runtime details.

## Fast paths for common user requests

Do not load the large-planning workflow for these small writes. Use the exact
recipe, then stop:

- “加到待定/候选地点”：resolve the trip with `list_trips`, then run
  `trek add-pending <trip-id> <title> [--place-id <saved-place-id>]` or call
  native MCP `add_pending_place`. If the place already exists in 收藏, pass its
  `placeId`; the server links/reuses that place instead of creating a duplicate.
  For a newly researched candidate, include a short stable `description` and a
  representative `imageUrl` when available; put the trip-specific recommendation
  in `reason`. A name plus address alone is not enough context for group voting.
  `apply_trip_change` with `action: "add_pending"` remains a compatible fallback.
  Never use `create_place` for 待选/候选/待决定.
- “设置行程封面”：run `trek set-cover <trip-id>
  <absolute-image>` or call native MCP `apply_trip_change` with `action:
  "set_cover"`. The server owns upload, binding and readback as one semantic
  operation; do not compose primitive upload/update calls when this tool exists.

For either fast path, if readback fails, report “未同步” and the exact failed
stage. Never continue into unrelated planning or claim the mini program will
eventually refresh.

## Mandatory workflow

1. Run `doctor` or native `tools/list`. Stop on authentication, network, or missing-tool failure.
2. Read existing state with `list_trips` and `get_trip_summary`. Never assume a trip ID. Use top-level `places[]` for every trip place, including unassigned places; use `packing.bags[]` for all bags, including empty bags.
3. Research current facts with primary/official sources first. Separate confirmed facts, recommendations, and unresolved items.
4. Build a dated plan and an `expectedAssignmentsByDate` checklist containing every POI/activity that must appear in the mini program. Use exact local dates and times. Do not invent reservations, confirmation numbers, phone numbers, opening hours, prices, or addresses.
5. Show the user a compact change preview before destructive, bulk, financial, membership, proposal-decision, or rescheduling writes.
6. Write in small batches. Reuse existing entities and detect duplicates by normalized name/date before creating.
   For a user-requested **new** trip, try to add one relevant cover by default unless the user opts out; do not replace existing covers or block creation if no suitable image is available. Follow [the cover recipe](references/workflows.md#new-trip-cover).
7. Every real location visit must be a Place plus Assignment. Use `create_and_assign_place` for a new POI and `assign_place_to_day` for an existing one. Pass known `place_time` and `end_time` directly in either creation call; both save the visit time atomically and return the assignment ID. Use `update_assignment_time` for later edits, not as a mandatory second step after creation. Location-free actions (wake up, bring tickets, meet a friend) can be timed day notes: visible in the notes part of the collapsed day-information section in mini program 0.3.18+, but not map stops. Never fabricate a POI just to make a note visible; older clients must upgrade.
8. Model accommodation separately. `create_place_accommodation`/`create_accommodation` create a lodging date range but no visible day assignment. If a hotel or check-in is in the daily plan, also assign its place to that day.
9. Populate only meaningful fields, but use the complete model when relevant: trip dates/description, days, places and coordinates, assignment start/end/duration/transport/notes, reservations, accommodations, costs, packing, todos, collaboration notes, proposals and members.
10. Read back with `get_trip_summary` plus the relevant `list_*` tool. Compare `expectedAssignmentsByDate` to actual `days[].assignments` by date and normalized place name/ID, not only counts. A planned day must not have zero assignments; explicitly document intentional rest/location-free travel days.
11. Do not report synchronization complete while any expected assignment is missing or only mentioned in a day note. Repair the gap or disclose it to the user.
12. Report what changed, what remains uncertain, and what the user must confirm.

Read [references/workflows.md](references/workflows.md) for detailed planning and synchronization recipes. Read [references/field-guide.md](references/field-guide.md) before a large or unfamiliar write.

## CLI

```bash
trek doctor
trek update --check
trek tools place
trek call list_trips '{"include_archived":false}'
trek summary 3
trek audit-plan 3 /absolute/path/expected-assignments.json
trek add-pending 3 '西湖游船' --reason '同行者表态后再排日程'
trek upload-file 3 /absolute/path/ticket.pdf --assignment 42 --description '景区电子票'
trek set-cover 3 /absolute/path/cover.jpg --description '行程封面'
trek rename-file 3 19 '金门大桥门票.pdf'
trek batch /absolute/path/actions.json
trek batch /absolute/path/actions.json --apply
trek smoke --allow-write-smoke
```

`doctor` reports local configuration, endpoint, credential presence, Skill integrity, authentication, live tool count, and trip readback. Failures include a category, hint, and next command; retain that structured output when diagnosing. `update --check` compares CLI versions; `update` upgrades the CLI and resynchronizes the Skill. `audit-plan` compares an expected JSON date-to-place mapping with live `days[].assignments` and exits non-zero on missing items. `add-pending` creates or reuses a candidate and verifies the open proposal by ID. `upload-file` reads a local attachment without printing its base64 and supports files up to 10 MB. `set-cover` uploads, binds, and verifies a visible trip cover as one command. `rename-file` changes only the display name and keeps the extension. `batch` is dry-run unless `--apply` is present. Applied actions always expose `ok`, `resourceType`, `resource`, `warnings`, and the original `result`; execution stops on the first failed action. It refuses high-risk tool names unless `--confirm-high-risk` is also present. `smoke` creates temporary data, exercises the proposal lifecycle, deletes it, and closes the MCP session.

## Safety invariants

- Treat the key as a password. Ask the user to revoke it immediately if exposed.
- Never delete or overwrite real data during diagnostics. Use the bundled temporary smoke only.
- Do not mark bookings confirmed without order evidence. Use `pending` or a todo for unresolved bookings.
- Reuse independently verified, appropriately licensed place details; `search_place` is a fallback when extra resolution is needed, not a required call per stop. For fallback use `market: "china"` plus `region` in Mainland China, or `market: "global"` plus an ISO `countryCode` overseas. Never invent coordinates or assume different coordinate systems are interchangeable. Only send coordinates whose source, rights and compatibility with the target map are verified; otherwise omit them and tell the user map/navigation needs verification. Existing records have no reliable coordinate-system metadata: do not mass-convert them. Preserve supported provider IDs where permitted. See [references/field-guide.md](references/field-guide.md).
- For minors, medical needs, border crossings, flights, and tight transfers, add safety buffers and explicit adult-confirmation tasks.
- Respect 429 responses. Do not disable server limits or fire requests in parallel; the bundled client retries with bounded backoff.
- Static `trek_` keys currently grant broad user access. Create one per Agent, revoke unused keys, and prefer scoped OAuth when the target agent supports it.
- Close every MCP session, including failed runs.

## Failure handling

- `401`: key missing, revoked, malformed, or sent without `Bearer`.
- `403`: user lacks trip permission or scope; do not retry as another user.
- `404`: wrong trip/entity ID or inaccessible resource; refresh state.
- `429`: wait and retry sequentially; reduce batch size.
- `isError: true`: treat as failed even if HTTP succeeded. Preserve the error text and stop dependent writes.
- Unknown fields/tools: call `tools/list`; never guess a schema from an older document.

When native MCP and the bundled client disagree, trust a fresh `tools/list` response and production readback.

## Daily notes and reminders (mini program 0.3.22+)

- Keep day titles short (about 25 characters). Use `update_day.daily_brief` for an optional user-authored clothing/tickets/packing reminder, up to 500 characters. Keep it concise, use actual newline characters to separate ideas, and avoid Markdown because the mini program renders plain text; empty or null hides the reminder. Mini program 0.3.24+ renders each line separately. `trek set-day-brief <trip-id> <day-id> @brief.txt` preserves line breaks from the file; a literal `\n` in a CLI argument is also normalized. Weather appears automatically below the day title when location and data are available: MET Norway is preferred for the first nine days, extended forecasts cover days 10–15, and dates beyond day 15 show a clearly labeled historical temperature estimate. It refreshes at most once per day. Do not set or ask the user to set `weather_enabled`.
- `create_day_note` stores a timed action in the notes part of the collapsed day-information section, without adding a map stop. These notes were invisible in 0.3.16 and older.
- `trek day-view <trip-id> <day-id>` / `preview_day_view` returns the content contract and minimum client version, not a screenshot or proof the user installed that version. Compare notes using `trek audit-notes <trip-id> expected-notes.json`; `audit-plan` checks assignments only.
- Use the current authorized tool schema. With semantic profile, discover these advanced tools and reconnect using full profile if needed. For exact fields and boundaries read [references/field-guide.md](references/field-guide.md).

### Optional day extras (0.3.18)

- Day notes are grouped under “当天备注 · count”, collapsed by default. Expand to read; tap a note to edit/delete in place. Notes are not route/map stops. Empty notes and reminders have no content panel.
- Weather is derived from the day's date and first located assignment, not a user-managed field. Missing coordinates or unavailable forecast/reference data produce no weather summary. Reminder and notes are the only editable sections in the day-information disclosure. Dates beyond day 15 use a historical temperature estimate, never a real forecast.
- Weather is cached on the client for the day and shared by rounded location on the server. MET Norway attribution and update time are shown. Authored text is not automatically refreshed.
- Use `preview_day_view.notesPresentation` to explain collapsed state; `renderedNotes` means available after expansion, not all rows visible on first opening. Preview does not fetch weather or prove a screenshot.
- Keep each note as one action/supporting item (text <=500); `text` is the editable label/body, so no separate name field is needed. Assignment notes from assign/update tools refer to the same visit-specific field. Packing and budget remain in their own tabs; do not duplicate them as itinerary stops.

## 跨零点（schema184 / 小程序0.3.36+）

保留用户选择的所属行程日，凌晨接机用正常HH:mm及start/end_day_offset=1，不自动移到第二天，也不用25:00。跨时区航班分别填出发/抵达当地时区。同步前读[references/cross-midnight.md](references/cross-midnight.md)，核对归属日、实际日期与UTC时刻。旧数据不盲目推断，省略字段保留。

## 到达方式（schema183 / 小程序0.3.35+）

每次安排独立设置到达方式，不按地点全局批量修改。未明确时根据上一站、实际路线、同行者与时间余量合理推断，标记 inferred 并写依据；明确指定或有凭据才标 confirmed。人工 manual 值保持优先。接送机用taxi，实际航班才用flight；机场节点不能一律flight。同一酒店不同次独立设置。同步前读 [references/arrival-mode.md](references/arrival-mode.md) 并核对实时Schema；字段缺失时只交付建议，不假装同步成功。
