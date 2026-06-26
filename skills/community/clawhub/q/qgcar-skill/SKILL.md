---
name: qgcar-skill
description: Use when the user wants help with Qiguan campus bus tickets using the local qg CLI, including listing schedules, choosing Zhuhai/South/East campus routes, generating WeChat order-entry links, copying links, or troubleshooting qg/qg-list commands. The skill should help prepare a booking link, but must not auto-submit passenger information, create orders, or pay.
---

# QG Car

Use the local `qg` CLI to help the user query Qiguan campus bus schedules and generate WeChat `BusOrderWrite` order-entry links.

## Core Workflow

1. List available schedules first unless the user already provides a valid list code:

```bash
qg list --today --available
```

2. Narrow the list with the user's route, date, and Zhuhai station:

```bash
qg list --start zhuhai --to south --station zhuhai --today --available
qg list --start zhuhai --to east --station boya --tomorrow --available
qg list --start south --to zhuhai --date 2026-04-10 --available
```

3. Prefer the `Code` column from the latest list result when generating the link:

```bash
qg link 1
qg link 1 --copy
```

4. If no list code is available, generate by exact route and time:

```bash
qg link --start zhuhai --to south --station zhuhai --time 16:00
```

5. Return the generated WeChat link and tell the user to open it in WeChat to complete passenger selection, order confirmation, and payment.

Do not call hidden order-save or payment APIs directly. The safe boundary for this skill is schedule lookup plus WeChat order-entry link generation.

## Route Mapping

Campus keys:

```text
zhuhai = Zhuhai campus side
south  = South Campus
east   = East Campus
```

Zhuhai station keys:

```text
zhuhai = 珠海中大岐关服务点
boya   = 博雅苑
fifth  = 中大五院正门
```

Default route behavior:

```text
qg list                       -> zhuhai to south, today
qg --start zhuhai             -> zhuhai to south, today
qg list --start south         -> south to zhuhai, today
qg list --start east          -> east to zhuhai, today
qg list --start zhuhai --all  -> zhuhai to both south and east
```

Use one side as `zhuhai`; direct `south` to `east` routes are not supported by this CLI.

## User Intent Handling

If the user says "珠海去南校区", use:

```bash
qg list --start zhuhai --to south --available
```

If the user says "南校区回珠海", use:

```bash
qg list --start south --to zhuhai --available
```

If the user says "珠海去东校区", use:

```bash
qg list --start zhuhai --to east --available
```

If the user says "东校区回珠海", use:

```bash
qg list --start east --to zhuhai --available
```

If the user specifies "博雅苑" or "中大五院", add `--station boya` or `--station fifth`. Otherwise use the default Zhuhai station, `--station zhuhai`.

Dates default to today. The CLI supports `--today`, `--tomorrow`, and `--date YYYY-MM-DD` within one week.

## Output Guidance

When listing schedules, summarize the useful rows with code, line time, boarding time, arrival time, station, price, seats, directness, and status.

When generating a link, include the link in a plain copyable block. Mention that the link is an order-entry link, not a completed booking.

If `qg link CODE` says there is no cached list, run `qg list ... --available` again and use the new code. If a link is stale or fails in WeChat, re-run `qg list` and `qg link` to refresh `priceMark`.

For detailed command behavior and troubleshooting, read `references/qg-cli.md`.
