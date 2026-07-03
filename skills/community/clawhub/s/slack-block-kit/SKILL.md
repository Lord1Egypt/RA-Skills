---
name: "slack-block-kit"
description: "Create and send native Slack Block Kit messages, including tables, code cards, structured layouts, buttons, inputs, and rich Slack blocks."
---

# Slack Block Kit

Use this skill when Slack needs formatting beyond plain mrkdwn.

Use OpenClaw `message(..., presentation=...)` for portable rich replies:

- Text, context, dividers, buttons, and selects
- Cross-channel degradation when the same reply may be reused outside Slack

Use native Slack Block Kit samples or Slack API calls for Slack-specific layouts:

- Native tables and dashboards
- Syntax-highlighted code cards
- Structured layouts with headers, fields, images, inputs, and actions
- New Slack layout blocks such as containers with nested `child_blocks`
- Raw or experimental Slack blocks that are not part of OpenClaw portable `presentation.blocks`
- Local sample validation before publishing or sharing

## Rule

Use plain Slack mrkdwn for ordinary prose. Use native Block Kit when structure matters.

Use the OpenClaw `message` tool with `presentation` for portable rich messages: text, context, dividers, buttons, and selects. Slack renders those as Block Kit where supported, and other channels can degrade them.

Do not put raw Slack Block Kit JSON inside OpenClaw portable `presentation.blocks`. The `presentation` schema is semantic and only accepts `text`, `context`, `divider`, `buttons`, and `select` blocks; it is not a Slack block pass-through. For raw or experimental Slack blocks such as tables, containers, charts, rich code cards, Markdown blocks, images, inputs, and agent-only blocks, call Slack `chat.postMessage` directly or use a Slack-specific plugin path.

Always include `text` as the notification/accessibility fallback when posting `blocks`.

## Samples

Copy from the smallest matching sample first, then customize.

- `samples/blocks/header.json`
- `samples/blocks/section.json`
- `samples/blocks/divider.json`
- `samples/blocks/image.json`
- `samples/blocks/context.json`
- `samples/blocks/actions.json`
- `samples/blocks/input.json`
- `samples/blocks/markdown.json`
- `samples/blocks/agents/plan.json`
- `samples/blocks/agents/task_card.json`
- `samples/blocks/agents/message_feedback.json`
- `samples/blocks/rich_text.json`
- `samples/blocks/table.json`
- `samples/blocks/data_table/basic.json`
- `samples/blocks/data_table/paginated.json`
- `samples/blocks/data_table/numeric_sort.json`
- `samples/blocks/data_visualization/line_single.json`
- `samples/blocks/data_visualization/line_multi.json`
- `samples/blocks/data_visualization/line_negative.json`
- `samples/blocks/data_visualization/bar_single.json`
- `samples/blocks/data_visualization/bar_multi.json`
- `samples/blocks/data_visualization/bar_negative.json`
- `samples/blocks/data_visualization/area_single.json`
- `samples/blocks/data_visualization/area_multi.json`
- `samples/blocks/data_visualization/area_negative.json`
- `samples/blocks/data_visualization/pie_multi_segment.json`
- `samples/blocks/data_visualization/pie_dominant_segment.json`
- `samples/blocks/video.json`
- `samples/blocks/callout.json`
- `samples/blocks/contact_card.json`
- `samples/blocks/container/standard.json`
- `samples/blocks/container/full_width.json`
- `samples/blocks/container/collapsible.json`
- `samples/blocks/container/icon_subtitle.json`
- `samples/blocks/container/media_preview.json`
- `samples/blocks/container/with_callout.json`
- `samples/blocks/container/with_image.json`
- `samples/elements/button.json`
- `samples/elements/selects.json`
- `samples/elements/overflow.json`
- `samples/elements/date_time.json`
- `samples/elements/checkboxes_radios.json`
- `samples/elements/plain_text_input.json`

For complete Slack API details, prefer the official docs for the specific block or element after choosing a local sample.

## Validation

After adding or editing samples, run:

```bash
node <skill_dir>/scripts/validate-samples.mjs
```

This walks `samples/**/*.json`, parses each file, and runs lightweight local checks for common mistakes: malformed `raw_text` and `rich_text`, table/data-table row shape, minimum data-visualization fields, duplicate `block_id`/`action_id`, wrapped or HTML-encoded URL fields, and missing container/image essentials. It is not a full Slack schema validator.

## Markdown Blocks

Use `type: "markdown"` for Slack's newer Markdown block when the content needs common Markdown features such as headings, horizontal rules, fenced code blocks, tables, blockquotes, and inline formatting.

This is distinct from legacy `mrkdwn` text objects used inside `section` and `context` blocks. Use `samples/blocks/markdown.json` for a compact mixed example.

## Agent Blocks

Use `samples/blocks/agents/` for agent-facing Slack blocks such as plans, task cards, and feedback controls.

Common blocks:

- `plan`: groups multiple task steps under a shared goal
- `task_card`: shows one task with status, details, output, and sources
- `message_feedback`: compact feedback controls; the underlying Slack block type is `context_actions`

Normalize source and link URLs to plain strings before posting.

## Containers

Containers are wrapper blocks with `child_blocks`. Use them for grouped layouts that need a title, subtitle, icon, width control, or collapsible body.

Common fields:

- `type: "container"`
- `title`: plain text title
- `subtitle`: optional plain text subtitle
- `icon`: optional image icon
- `width`: `standard` or `full`
- `is_collapsible`: true when the container can collapse
- `default_collapsed`: initial collapsed state
- `child_blocks`: nested Slack blocks

Nested child blocks still need valid `block_id` values when they are referenced by interactions or diagnostics.

## Data Visualization

Use `data_visualization` for native Slack charts.

Common fields:

- `type: "data_visualization"`
- `block_id`: stable chart block id
- `title`: chart title string
- `chart.type`: chart type, such as `line`, `bar`, `area`, or `pie`
- `chart.series`: one or more named series for axis-based charts
- `chart.series[].data`: label/value points for axis-based charts
- `chart.axis_config.categories`: x-axis category order for axis-based charts
- `chart.axis_config.x_label` and `chart.axis_config.y_label`: axis labels for axis-based charts
- `chart.segments`: label/value segments for pie charts

Use separate samples for single-series, multi-series, and negative-value charts. Negative values are valid for line, bar, and area examples. Pie charts use `segments`, not `series` or `axis_config`.

## Posting

For portable rich replies, use `message(action="send", presentation=...)`. Current OpenClaw docs describe Slack `message` tool sends with `presentation` as Slack-rendered Block Kit sends.

For raw Slack Block Kit JSON, use Slack `chat.postMessage` directly. The OpenClaw `message` tool schema accepts `presentation`, not a top-level raw `blocks` array.

```bash
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg channel "$CHANNEL_ID" \
    --arg thread "$THREAD_TS" \
    --arg text "JavaScript code block" \
    --argjson blocks "$(cat samples/blocks/rich_text.json)" \
    '{
      channel: $channel,
      thread_ts: $thread,
      text: $text,
      blocks: $blocks
    }')"
```

Resolve the Slack bot token from the configured Slack account. OpenClaw supports `channels.slack.botToken`, per-account `channels.slack.accounts.<accountId>.botToken`, SecretRefs, and the default-account `SLACK_BOT_TOKEN` env fallback. The token needs `chat:write`, and the bot must be in the channel.

Do not print token values while copying or debugging the curl sample.

For portable Slack thread replies through the `message` tool, pass `threadId` or `replyTo`. Add `replyBroadcast: true` only when the thread reply should also appear in the parent channel; it maps to Slack `reply_broadcast` and is not supported for media uploads. Use `topLevel: true` or `threadId: null` to opt out of inherited Slack thread routing. For raw `chat.postMessage`, use Slack's `thread_ts` and `reply_broadcast` fields directly.

After sending, verify with Slack readback when this is a test or incident investigation. Prefer the OpenClaw `message` action `read` when available; otherwise use Slack API readback with the same channel and thread identifiers.

## Tables

- Tabular data in Slack: financial summaries, comparison grids, status dashboards
- Markdown tables render poorly or not at all in Slack
- Use `scripts/table.mjs` for non-trivial tables
- Use `table` for compact rich-text tables
- Use `data_table` for larger datasets, paginated-style tables, or typed numeric values
- Use `raw_number` cells inside `data_table` when Slack should sort numbers by value instead of text

### Generate

Generate table JSON from headers + rows:

```bash
node <skill_dir>/scripts/table.mjs \
  --headers '["Source","Amount","Status"]' \
  --rows '[["Mochary","$11K","Pending"],["MHC","$13.4K","Invoiced"]]' \
  --align '1:right' \
  --compact --blocks-only
```

Options:

- `--headers '["H1","H2"]'` - first row, bold by default
- `--rows '[["a","b"],["c","d"]]'` - data rows
- `--json '{"headers":[...],"rows":[...]}'` - single JSON input
- `--stdin` - read JSON from stdin
- `--align '<col>:<left|center|right>,...'` - column alignment, 0-indexed
- `--wrap '<col>,...'` - columns to wrap text
- `--bold-headers` - bold headers; this is the default
- `--no-bold-headers` - plain text headers
- `--compact` - minified JSON
- `--blocks-only` - output just the blocks array for API calls

Generated empty cells are converted to zero-width space automatically. For manual JSON, `raw_text.text` must be non-empty.

### Constraints

- `scripts/table.mjs` emits 1 table block per payload
- Max 100 rows, max 20 columns; the generator enforces these limits
- Rows must all have the same column count
- Cells: `raw_text` plain cells or `rich_text` rich cells
- Empty text is not allowed; use zero-width space automatically
- `data_table` rows can mix `raw_text`, `rich_text`, and typed values such as `raw_number`

### Combining Text + Table

Post your text message first via the `message` tool, then post the table in the same thread via Slack API. Or include a `section` block before the table in the native blocks array.

## Gotchas

- Block Kit caps messages at 50 blocks; big tables/layouts may need splitting across multiple messages.
- `chat.postMessage.text` is the notification/accessibility fallback; always include it even when sending `blocks`.
- Rich-text approximations do not scale to real columns; use `table`, `data_table`, or `scripts/table.mjs` for non-trivial tables.
- For thread replies after subagent completion or session resume, pass the original `thread_ts` explicitly; do not rely on inherited routing.
- Actions and inputs need unique `block_id` and `action_id` values when interactivity matters.
- Confirm destructive or externally visible interactive workflows before wiring live buttons.
- Slack examples sometimes wrap URLs in mrkdwn angle brackets or encode `&amp;`; JSON payloads should use plain URL strings.

## Manual Block Kit JSON

For non-table blocks or custom layouts, construct the JSON directly from the samples.

Cell with bold text:

```json
{"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"text","text":"Bold","style":{"bold":true}}]}]}
```

Plain text cell:

```json
{"type":"raw_text","text":"Plain"}
```
