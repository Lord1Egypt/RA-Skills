---
name: yoooclaw-world-cup-match-talk-scene-en
description: Use to generate World Cup football conversation kits from standardized match input and notification retrieval. It supports prep for fan-group chats, in-person viewing, social posts, or selected modules such as "understand the match in 30 seconds," "main match highlights," "what everyone is discussing," "expert-sounding match lines," and "generate a Moments post." It can retrieve Chinese public sports sources and, when notifications or fan groups are relevant, use `openclaw ntf search` to extract matching mobile-notification signals.
---

# World Cup Match Conversation Kit

Generate a practical World Cup football game conversation package to help users speak naturally in group chats, offline watching games, social media posts and ordinary chats. Produce content based on five things: understand the game in 30 seconds, understand the main highlights of the game, know what everyone is talking about, prepare the pretense of the game, and write copy that can be sent directly to Moments. Prioritize the output of content that can be spoken directly and forwarded directly.

This skill v1 is only for World Cup football matches. Do not generalize to other sports unless the user explicitly requests extension.

## Scene input

At least one of the following information is required:

- Match sides, e.g. `Portugal vs Uzbekistan`
- Match name, for example `World Cup Group K Portugal Uzbekistan`

Users set three types of attention dimensions through the installation pop-up window or this request:

- Who to follow: The subject of the game to follow, which can be the two sides of the game, the name of the game, the team, the player or the national team, such as `Portugal vs Uzbekistan`. Used to position matches.
- What to focus on: the content you want to generate, usage scenarios and output depth. It can be a full discussion package, designated modules, group chat version, offline viewing, social media copywriting, commentary preparation, short/standard/detailed, etc. Used to determine output mode and module.
- Which groups and applications to follow: Notifications and information source range, which can be fan groups, game viewing groups, WeChat groups, Feishu groups, Weibo, Qiqiudi, Live Broadcast Bar, exported notification files, or "check recent notifications" instructions. Used for notification queries, notification filters, and source preferences.

If `who to follow' is not enough to uniquely determine the match, public information will be used to infer it first; if there are still multiple candidate matches, only one confirmation will be asked.

If `what to focus on` is empty, no output mode is specified, or it only says "module output" but does not list specific modules, directly use `full` to output in full without asking.If `Which groups and applications to follow` is empty, you can still generate a discussion package based only on public information; when notification context is needed, query recent notifications without limiting the scope of groups and applications. Users are not required to provide fan group notifications. Notification refinement is only performed when the user requests a notification/group chat context, provides a notification file, or includes a notification scope in Groups and Apps to Follow.

## Output mode

### Full output

When generating a complete discussion package, splice the following five templates in order; do not use a single full template.

### Module output

Only user-specified modules are output. If the specified module uses mobile phone notifications or tactical inference, be sure to mark the necessary uncertainty and do not write the inference as fact.

Optional modules (combined according to chat scenarios for easy understanding and selection):

- `Understand this game in 30 seconds` — Quick reading at the beginning, catch the most worth talking about this game at a glance
- `The main highlights of this game` — the three major highlights, the playing styles of both sides, and the hot players, together you can understand the whole game
- `What are everyone talking about during this game` — Internet hot discussions, comparison topics, and fan group notifications on your phone to know what everyone is talking about
- `Pretentious talk for this game` — a list of chats while watching, talk skills for knowing the game but not pretending, and group chat skills that can be directly copied
- `Generate the Moments copywriting of this game` — different styles of social media copywriting

Users can also name only one of the sub-items (such as "hot players", "comparison topics", "can be copied directly") and press the corresponding sub-module to output.

## Workflow

### 1. Confirm the match

Standardize the Chinese and English names of the team. Confirm match times, World Cup stages, groups, context with public sources. If there is an ambiguity in the date, the specific date adopted must be stated.

### 2. Collect Chinese public information

First use web-search to find relevant pages and latest discussions for this game. web-search is responsible for relevance and timeliness; script is responsible for structured crawling and extraction.

Prioritize these targeted searches:

- `{Team A} {Team B} World Cup Pre-match`
- `{Team A} {Team B} Match Time World Cup`
- `site:news.zhibo8.com {Team A} {Team B} World Cup`
- `site:m.dongqiudi.com {Team A} {Team B} {Key Players}`
- `site:sports.sina.com.cn {Team A} {Team B} World Cup`

After finding relevant pages or strongly related query terms, if there is a source detection script in the skill package, use it to obtain structured crawling diagnosis:

```bash
python3 scripts/probe_cn_football_sources.py \--query "{Team A} {Team B} World Cup Pre-match Hot Players" \
  --limit 1 \
  --out /tmp/world_cup_match_sources.json
```

Use script output to identify accessible pages, titles, times, summaries, sample facts, and source failures. Scripts are only structuring and crawling aids, not the only factual layer.

If the script does not exist, is not runnable, or the results are weak, continue using web-search or direct browser retrieval.

Priority is given to using these Chinese public channels:

- Understand the football emperor: pre-match analysis, player/team articles, tactical analysis, tags
- Live broadcast: news, game reports, player data, schedule and group situation
- Sina Sports: Battle reports, records, event background, cross-validation
- Hupu: fan controversies, community opinions, comparison topics
- CCTV Sports: event description, video/news summary, competition narrative
- Chinese Football Association/Official Chinese Football Channel: Official notices when it comes to Chinese football

Weibo is only available through web-search snippets, accessible browser pages, Playwright or authenticated browsing environments. Don’t treat ordinary non-login scripts to capture Weibo as a stable source.

Known script behavior:

- Detection was relatively stable before: Qiqiudi, Live Bar, Sina Sports, Hupu, CCTV Sports, Chinese Football Association pages
- Previous detection section available: Chinese Football Association/Chinese Super League dynamic schedule page
- Often blocked without login/browser context: Weibo hot page

When reading script JSON, these fields take precedence:

- `source`
- `url`
- `status`
- `title`
- `published_at`
- `author_or_source`
- `summary`
- `sample_facts`
- `raw_text_length`
- `error`

Records with `status: ok` are preferred. `partial` is only used as a clue to continue browsing. `blocked` is used only to illustrate source restrictions, not to generate factual content.

Before using any script results into the main text, relevance filtering must be done: the title, summary or sample facts must at least hit the target team, key players, World Cup context or this game. If the script result is technically successfully captured but has nothing to do with the target competition, it can only be used as a capture diagnosis and cannot be written into the discussion package.

Selective cross-validation:

- Key facts must be cross-verified: game time, score, points, injuries, starts, records, official statements
- For `partial`, `blocked`, expired or weakly relevant pages, use web-search/browser to find out

Stratify each important piece of information:- `Facts`: schedule, scores, points, official statements, reported data
- `Public Opinion`: Hupu, Weibo, comment trends, group chat sentiments
- `Inference`: tactical judgment, possible matchups, trend interpretation
- `Unverified`: Injury rumors, starting lineup leaks, transfer rumours

Do not write inferences or unverified content as fact.

### 3. Retrieve and refine relevant mobile phone notifications

If the user's request involves notifications, fan groups, game viewing groups, mobile phone reminders or notification-derived discussions, the notifications must be queried first and then the notification-related modules are generated.

Use `exec` to execute `openclaw ntf search`. If the user provides a time range, the user time range is strictly used. If no time range is provided, the query ranges from 00:00 yesterday local time to the current time by default.

```text
command: openclaw ntf search --from start time --to end time
yieldMs: 30000
```

Example:

```text
command: openclaw ntf search --from 2026-06-17T00:00:00+08:00 --to 2026-06-18T15:00:00+08:00
yieldMs: 30000
```

Reusing old notification results is strictly prohibited. Each time a notification context is required, it must be queried again.

If `openclaw ntf search` is unavailable or fails to execute, it means that the notification cannot be queried at this time, and other modules will continue to be generated based on the public information. If the user provides a notification file, the file is read directly.

Extract only content relevant to the target match or World Cup discussion from all return notifications. Screening clues include:

- Event words: World Cup, World Cup, group stage, knockout round, schedule, live broadcast
- Team name, alias, country name, abbreviation
- Player names and common nicknames
- Words for watching the game: watching the game, watching football, bar, offline, gathering, live broadcast source, prediction, score, lineup
- Fan group/chat signals: group announcement, group chat, brothers, assembly, start of game, stay up late, midfield, after game, @
- User scenario scope: Teams/players/game subjects in `Who to follow', output scenarios/modules in `What to follow', groups, applications, channels or viewing locations in `Which groups and applications to follow'

Ignore irrelevant notifications: takeout, express delivery, bank, system reminders, advertisements, work reminders, calendar noise, ordinary app push, non-football chat, etc.

The priority is increased when the following content is hit: who to follow, what to follow, which groups and applications to follow, repeated reminders, @users, direct inquiries, live broadcast links, offline gatherings, score predictions, and game time reminders.Only use command results or notifications that actually exist in the user file. Do not simulate, fabricate, fill, or recreate missing notifications. If there is no relevant notification, write: `No relevant mobile phone notification/fan group notification found. ` Then continue to output the public information module.

The notification signals can be summarized as:

- Watching organization: time, location, live broadcast source, reminder
- Group emotions: excitement, anxiety, opposition, fun
- High-frequency topics: players, records, tactics, score predictions
- Available words: must be based on real notifications for natural conversion
- Noise Ignored: Brief description of the main irrelevant categories

Do not expose irrelevant sensitive notifications. Only quote short relevant snippets when necessary.

### 4. Generate discussion package

The output goal is not to "stack information", but to allow users to get five things from this game: understand the whole scene in 30 seconds, grasp the main points of interest, know what everyone is talking about, have ready-made pretense skills, and be able to directly post to Moments. The wording should be concise, natural, and replicable.

Output corresponding modules according to user selection. `full` full output only splices five templates in sequence; when the user only specifies one or a few modules, only the corresponding templates are read and output, and other modules are not brought out.

Read the following reference files as needed:

- `Understand this game in 30 seconds`: read `references/template-30s.md`
- `The main points of this game`: read `references/template-main-points.md`
- `What are everyone talking about during this game`: read `references/template-discussion.md`
- `The talk of this game`: read `references/template-talk-lines.md`
- `Generate the Moments copy for this game`: read `references/template-social-post.md`

If the user only names the minor items, read the template files they belong to: `Three major points`, `Recent play styles of both sides`, `Hot players` belong to `template-main-points.md`; `Online discussions`, `Comparative topics`, `Fans group in your mobile phone` belong to `template-discussion.md`; `Chat while watching list`, `Talk skills of knowing football but not pretending`, `Can be copied directly` belong to `template-talk-lines.md`.

When outputting in full, read the five reference files in the order above and splice them for output. Do not pre-read unrequested template files.

When outputting a specified submodule, the superior module title and related subtitles of the submodule are retained, and only other modules not requested by the user are omitted. The "What is this" description written in italics under each title should be retained to help users understand what this section is about; you can fine-tune the wording according to the game, but do not delete it.## Style rules

- Chinese output is used by default unless the user specifies other languages.
- The sentences should be natural and suitable for speaking directly.
- Don’t pile up jargon; tactical points should fall into game details that users can observe.
- Do not write offensive, insulting or identity-attacking jokes.
- Don’t turn star rivalries into mutual insults among fans.
- When there is a clear date and time, the specific date and time must be written.
- Use natural expressions for uncertain content, such as: `at the moment`, `more like`, `can be understood as`, `waiting for confirmation of the pre-match roster`.

## Quality Check

Confirm item by item before output:

- The match is a World Cup soccer match, or the user explicitly requests an extension.
- When notification context is required, use fresh `openclaw ntf search` results or user-supplied files, not old results.
- The content of the mobile phone notification used actually comes from the command results or user files.
- No simulated notifications or made-up group messages.
- The script results are filtered by the target competition relevance before entering the text.
- The opinions expressed in the notice are not written as facts.
- User-required output modes and modules have been adhered to.
- The reproducible words are short enough and suitable for group posting or social media.
- Do not fabricate when notification data is missing; omit the notification module when the notification module is not required and the notification scope is not provided; write `No relevant mobile phone notifications/fan group notifications found when there are no relevant notifications in the query or file. `.
