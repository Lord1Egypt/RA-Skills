# QG CLI Reference

The source project is `https://github.com/qybaihe/qg-skill`. The globally linked commands are `qg` and `qg-list`.

## Commands

```bash
qg --help
qg routes
qg list --today --available
qg list --tomorrow --start south --available
qg list --today --start zhuhai --to east --station boya --available
qg list --today --start zhuhai --all --available
qg link 1
qg link --code 1
qg link 1 --copy
qg link --today --start zhuhai --to south --station zhuhai --time 16:00
```

`qg-list` is an alias for listing schedules:

```bash
qg-list --start zhuhai --today --available
```

## Route And Station Keys

Campus keys:

```text
zhuhai: Zhuhai
south: South Campus
east: East Campus
```

Zhuhai station keys:

```text
zhuhai: 珠海中大岐关服务点
boya: 博雅苑
fifth: 中大五院正门
```

One side of a route must be `zhuhai`. The CLI rejects `south -> east`.

## Date And Time

No date option means today.

Supported date options:

```bash
--today
--tomorrow
--date 2026-04-10
--date today
--date tomorrow
--date fri
```

Dates must be within one week. `--time` must use `HH:mm` and can match either the line time or the actual boarding time. The generated link uses the actual boarding time for the selected station.

## List Code Flow

`qg list` writes the latest table to `~/.qiguan-cli/last-list.json`. `qg link CODE` reads that cache, re-fetches the matched schedule to get a fresh `priceMark`, and prints a WeChat order-entry link.

Use the code flow when possible:

```bash
qg list --start zhuhai --to south --station zhuhai --today --available
qg link 1
```

Use direct time matching when there is no cache or when the user asks for a specific time:

```bash
qg link --start zhuhai --to south --station boya --time 16:00
```

## Safety Boundary

The CLI intentionally supports schedule queries and WeChat order-entry link generation. It should not submit orders, store passenger identity data, or trigger payment.

If the user asks to complete the order, generate the WeChat link and tell them to finish passenger and payment steps in WeChat. If the user asks to automate order submission or payment, pause and explain that this crosses into passenger PII and payment authorization.

## Troubleshooting

If `qg` is missing:

```bash
npm install -g qg-skill
```

For local development:

```bash
cd /Users/baihe/Documents/岐关车cli
npm install
npm run build
npm link
```

If `qg link CODE` fails because the cache is missing, run `qg list ... --available` again and use a new code.

If the WeChat link fails, rerun `qg list` and `qg link` to refresh schedule availability and `priceMark`.

If no matching schedule is found, show `qg list` for that route/date and ask the user which visible code they want.
