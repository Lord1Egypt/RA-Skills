# Tklr Tasks, Scheduling, & Reminders for Hermes Agent

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill that turns your agent into a personal schedule assistant: appointments, events, tasks, reminders, and the questions people typically ask about them.

You talk to it in plain language. It works out the commands, and it delivers reminder alerts to whatever channels you use (Matrix, Telegram, Signal, email, SMS, desktop notifications) at the lead times you asked for.

**It currently requires Hermes Agent.** A port to OpenClaw is planned; see [Portability](references/how-it-works.md#portability) for the details.

Six kinds of reminder cover everything you'd ask for. You don't need to know them when using: you say what you want and the agent picks. But they are what the skill is made of, so here is each one as a conversation.

**Event**: something that happens at a particular time. It goes on the calendar, it can hold travel time either side, and it is the only type that really needs a clock.

```
You:    Lunch with Ed Friday at noon, an hour and a half, nudge me 15
        minutes before
Agent:  Added: Lunch with Ed, Friday 12:00–13:30. Reminder at 11:45.

You:    It's across town, hold half an hour either side
Agent:  Updated: 30 minutes of travel before and after, so Friday now
        blocks 11:30–14:00. The reminder is unchanged.

You:    Am I free Tuesday at 3? Sam wants to get coffee
Agent:  Tuesday's clear from 1pm, but you have a 1:1 with Dana at 4:30.
        A 3pm coffee fits with room to spare.

You:    Book it, 45 minutes, at Cafe Ambrosia, nudge me 15 before
Agent:  Added: Coffee with Sam, Tuesday 15:00–15:45 at Cafe Ambrosia.
        Reminder at 14:45.

You:    Standup every weekday at 9, ten minutes ahead is plenty
Agent:  Added: Standup, weekdays at 09:00, reminder at 08:50.

You:    What's on Tuesday?
Agent:  Three things: Standup 09:00, Coffee with Sam 15:00 at Cafe
        Ambrosia, 1:1 with Dana 16:30.

You:    Move that 1:1 to Wednesday afternoon
Agent:  Moved: Wednesday at 16:30. Only this week's; the series carries
        on as before.

You:    Skip next Monday's standup, keep the rest
Agent:  Done: next Monday is off. The rest of the series is untouched.
```

**Task**: something that requires an action to complete. A date is optional; what matters is that it stays on the list until it's done.

```
You:    Remind me to pick up milk
Agent:  Added: Pick up milk. No date on it, so it just sits in your list
        until you tell me it's done.

You:    Renew my passport by September 1st. It's important, and start
        warning me a month out
Agent:  Added: Renew passport, due 1 September, top priority. It starts
        showing as pending on 1 August, and I'll remind you a week
        before and again the day before.

You:    Water the plants every Tuesday
Agent:  Added: Water the plants, every Tuesday. It comes back on
        schedule whether or not you got to last week's.

You:    Change the furnace filter every 90 days, counting from when I
        actually do it
Agent:  Added: Change the furnace filter. This one repeats from
        completion instead: mark it done and the next lands 90 days from
        that day, so a late one can't drift the rest.

You:    What do I need to get done?
Agent:  Pick up milk, and Water the plants by Tuesday. Renew passport
        isn't pending yet; that starts warning you on 1 August. Nothing
        overdue.

You:    Got the milk
Agent:  Done: Pick up milk is complete.
```

**Project**: a collection of related tasks, tracked together, where some steps can wait on others.

```
You:    Build the dog house: pick up materials, cut the panels, then
        assemble it. Each one needs the one before it
Agent:  Added: Build dog house, with three steps: Pick up materials,
        Cut the panels, Assemble. They're chained, so only Pick up
        materials is available right now.

You:    Materials are in the truck
Agent:  Done: Pick up materials is complete. Cut the panels is next up.

You:    How's the dog house going?
Agent:  One of three done. Cut the panels is available now; Assemble is
        waiting on it.

You:    Jordan's cutting the panels
Agent:  Noted: Cut the panels is on Jordan's list now, still part of the
        project.
```

**Goal**: a target rate rather than a date, meaning *n* completions per period. Nothing is ever overdue, you're just ahead or behind.

```
You:    I want to do interval training three times a week
Agent:  Added: Interval training, 3 times a week. No fixed days on this
        one; I count completions against the target and tell you where
        you stand.

You:    Did a session this morning
Agent:  Logged one against Interval training. That's it recorded, not
        finished. The goal keeps running.

You:    Show me the interval training goal
Agent:  Interval training, target 3 a week, one completion recorded.
        Nothing is ever late on this one; a goal can only be ahead or
        behind.
```

**Note**: information for future reference. No schedule, no alerts; it's there so you can find it later.

```
You:    Remember that the wifi password is on the back of the router
Agent:  Noted: Wifi password is on the back of the router. It won't
        remind you of anything; it'll just be there when you search.

You:    Keep this: "Give me a pig! He looks you in the eye and treats you
        as an equal." Churchill
Agent:  Saved, with #Churchill on it so it turns up when you search.

You:    What was that quote about pigs?
Agent:  "Give me a pig! He looks you in the eye and treats you as an
        equal." Churchill.
```

**Jot**: a few words dashed off while something is happening, stamped with the time so you can make sense of it later. Tklr's own description is "in the heat of battle when every second counts, jot down just enough to trigger your memory later when things have calmed down."

```
You:    Jot down that I'm taking a walk
Agent:  Logged at 13:14: taking a walk.

You:    That walk was an hour and a quarter, count it as exercise
Agent:  Updated: taking a walk at 13:14, 1h15m, filed under
        exercise.walking.

You:    Note that the well pump was making a grinding noise
Agent:  Logged at 15:20: well pump making a grinding noise.

You:    Spent two hours on the Henderson invoices
Agent:  Logged: Henderson invoices, 2h, filed under billing.henderson.

You:    Where did my time go this month?
Agent:  4 hours logged. Billing 2h, all Henderson. Exercise 2h, split
        1h15m walking and 40m interval training.
```

Capture first, fill in the detail afterwards: that two-step is the whole point of a jot, and what separates it from a note. A note is information you file because you'll want it later; a jot is a record that at 13:14 this happened. Categories nest, so `exercise.walking` and `exercise.interval_training` total together under `exercise` without mixing into your billing hours.

Behind the scenes is [tklr](https://github.com/dagraham/tklr-dgraham) ([documentation](https://dagraham.github.io/tklr-dgraham/)). You don't need to learn its syntax. Just talk to your agent in natural language and let it use the tool.

You can learn it if you want to, though. The skill sits alongside ordinary tklr use rather than replacing it. It uses tklr's normal workspace at `~/.config/tklr`, so you and the agent share one database: anything you add with `tklr` or its UI shows up for the agent, and anything the agent adds shows up for you. [`references/tklr-syntax.md`](references/tklr-syntax.md) documents the grammar.

## Install

Register the repo as a skill source, then install from it:

```bash
hermes skills tap add 37Rb/hermes-skills
hermes skills install 37Rb/hermes-skills/skills/tklr-reminders --category productivity
```

`--category productivity` files it under `~/.hermes/skills/productivity/`. Leave the flag off and it installs flat at `~/.hermes/skills/tklr-reminders`. The skill works either way, since Hermes only uses the category for grouping.

Then run this, exactly as written:

> `/tklr-reminders setup`

That loads the skill and it takes it from there: installs tklr, creates the workspace, installs the alert dispatcher, creates the cron job, points alerts at the chat you are already talking in, and sends you a test reminder to confirm delivery works.

**On Matrix and Slack, type `!tklr-reminders setup` instead.** Those clients reserve `/` for their own commands, so a typed `/` never reaches Hermes; their adapters accept `!` and rewrite it. Every other platform uses `/`.

**Include the word `setup`; it does real work.** Anything you type after the command is passed through to the agent as your instruction, and it is placed at the very end of the message, after the skill and after the file listing Hermes appends. That last position is the one the agent acts on most reliably. A bare `/tklr-reminders` gives it a document and no task, and smaller local models tend to respond by describing the skill or offering you a menu instead of setting it up. One word fixes it.

Use the explicit invocation for the first run rather than asking in your own words. Every skill is registered as `/<skill-name>`, and invoking it loads the skill directly, with no guessing about whether your phrasing matched. Something like "set up my reminders" relies on the agent picking this skill out of ~65 others from a one-line description, which it may not do, especially if you have used a different calendar tool with it before. Once setup is done, plain language works fine for everyday use.

The same trick helps later on. `/tklr-reminders what can you do?` or `/tklr-reminders add my dentist appointment` both reload the skill *and* give it the task, which is more reliable on a small model than the command alone.

<details>
<summary>What the installer does</summary>

```bash
bash ~/.hermes/skills/productivity/tklr-reminders/scripts/install.sh
```

Idempotent, so it doubles as a readiness check if something drifts. It:

1. installs `tklr-dgraham` via `uv` (Hermes ships its own `uv`)
2. creates the tklr workspace at `~/.config/tklr` (`config.toml` + `tklr.db`)
3. copies the alert dispatcher into `~/.hermes/scripts/`
4. reports whether any alert channels are defined yet

It deliberately does **not** invent alert channels, and does **not** create the cron job. Both need to know your actual delivery targets.
</details>

## What setup involves

The agent handles all of this. It's documented here so you know what landed on your machine, and so you can fix it if something drifts.

**1. Alert channels.** The `[alerts]` section of `~/.config/tklr/config.toml` *is* the routing table. Each key is one lowercase letter naming a (person, channel) pair, and its value is the command that performs the delivery:

```toml
[alerts]
r = 'hermes send --to telegram:YOUR_CHAT_ID --quiet "⏰ Reminder: {name} — starts {when} ({start}). {description}"'
a = 'hermes send --to matrix:!YOUR_ROOM_ID:matrix.org --quiet "⏰ Reminder: {name} — starts {when} ({start})"'
```

A letter's value is a plain shell command, so anything this machine can send with works. Chat goes through `hermes send` (Matrix, Telegram, Signal, Discord, Slack, SMS, or a bare platform name for its home channel), and email goes through `himalaya`, which is how Hermes reaches email. Desktop notifications are just `notify-send`. Nothing in the skill prefers one platform over another; whatever `hermes send --list` and `himalaya account list` report is what you can use.

A reminder then picks offsets and channels: `@a 1h, 15m: r` fires an hour before and again 15 minutes before, both to `r`. See [`templates/alerts-config-example.toml`](templates/alerts-config-example.toml) for a fully commented example including email, SMS, and group chats, and for the several ways this file can bite you (an apostrophe in any value silently erases the whole section two commands later).

Get valid delivery targets with `hermes send --list`. **Use exactly what it prints.** A wrong target is a silent black hole: the send reports success, the alert is marked delivered and deleted, and the message reaches nobody.

**2. The dispatcher cron job.** Tklr normally only fires alerts while its interactive UI is running. This skill replaces that with a once-a-minute job:

```bash
hermes cron create '* * * * *' --script tklr_alert_poller.py \
  --no-agent --name tklr-alert-poller --deliver local
```

`--script` takes a **bare filename**. The scheduler rejects any path outside `~/.hermes/scripts/`, which is why `install.sh` copies the dispatcher there. The skill also ships a daily blueprint health check (06:37) that recreates the job if it goes missing and re-generates any alerts left stranded by stale derived state.

## How it works

```
you → agent → scripts/tklr_agent_wrapper.py → tklr → tklr.db
                                                       │
                          Alerts table (one row per offset × channel)
                                                       │
        hermes cron (every minute) → scripts/tklr_alert_poller.py
                                                       │
                            hermes send (chat) / himalaya (email) / notify-send
```

The dispatcher reads due alerts, runs each one's command, and deletes the row on success, so one row per (offset, channel) gives exact once-only delivery with no separate send ledger. Undelivered rows are retried until they're an hour late, then reported and dropped rather than retried forever.

## Layout

```
SKILL.md                              agent instructions (the skill itself)
README.md                             this file
references/setup.md                   the setup procedure, start to finish
references/using-the-wrapper.md       every command the agent runs day to day
references/how-it-works.md            delivery, healing, SQLite, troubleshooting
references/tklr-syntax.md             underlying tklr grammar, only needed for --raw
scripts/tklr_agent_wrapper.py         the one interface: add edit list show find
                                        free done delete move uses channels
                                        status setup email welcome
scripts/tklr_alert_poller.py          the every-minute dispatcher
scripts/set_alert_channel.py          safely edit [alerts]; validates targets
scripts/tklr_mutate.py                low-level record edits
scripts/install.sh                    idempotent setup / readiness check
scripts/reset.sh                      undo the setup, back to a pristine state
templates/alerts-config-example.toml  commented [alerts] reference
```

## Caveats

- Tklr's own logs grow in `~/.config/tklr/logs/` and are not rotated, yet.
- If you leave `tklr ui` open, it delivers due alerts itself every 6 seconds, from the same table the dispatcher reads. Both delete each row once it's sent, so you normally still get exactly one alert, but a duplicate is possible if the two fire in the same instant.

## License

This skill is published on ClawHub, which licenses every skill it hosts under [MIT-0](https://opensource.org/license/mit-0): use it, modify it, redistribute it, commercially or otherwise, with no attribution required.

Tklr itself is a separate program, installed from PyPI as `tklr-dgraham`, and is licensed GPL-3.0-or-later. This skill invokes the `tklr` command; it does not include or link against its code.
