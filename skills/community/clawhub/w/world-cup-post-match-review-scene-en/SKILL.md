---
name: yoooclaw-world-cup-post-match-review-scene-en
description: Used to generate post-match reviews of World Cup football matches, and supports standardized scene input, post-match information retrieval and fan group notification extraction. It is used when the user needs to summarize the game in one sentence, how the game was played, who played the best, the hot topic after the game, or when the user explicitly requests a full review. The final answer only presents the review content without adding additional paragraphs.
---

# World Cup Post-Match Review Scene

Generate practical post-match reviews of World Cup football matches to help users quickly understand the game, organize hot discussions in group chats, and accumulate post-match opinions that can be forwarded. Prioritize the output of content with clear facts, clear judgment after review, and content that can be forwarded directly.

This skill v1 is only for World Cup football matches. Do not generalize to other sports unless the user explicitly requests extension.

## Scene input

At least one of the following information is required:

- Match sides, e.g. `Argentina vs Algeria`
- Match name, for example `World Cup Group J Argentina Algeria`
- Post-match events such as `Messi hat-trick Argentina 3-0 Algeria`

Users set three types of attention dimensions through the installation pop-up window or this request:

- Who to follow: The subject of the game to follow can be both parties, teams, players, coaches or national teams. Used to locate games, teams and key figures.
- What to focus on: The desired review content and level of detail: a one-sentence summary, match analysis, best performer, post-match talking points, a full report, or a short/standard/detailed version. Used to determine the output type.
- Which groups and applications to focus on: fan groups, game viewing groups, WeChat groups, Feishu groups, sports apps, social media apps, or "no limit" that need to be retrieved first. Used for notification queries and result filtering.

If `who to follow' is not enough to uniquely determine the match, use the available information to infer first; if there are still multiple candidate matches, only ask for confirmation once.

If `What to focus on` is empty, no output type is specified, or it only says "partial output" but does not list specific directions, just ask: `Which pieces do you want: summarizing the game in one sentence, how the ball was played, who played the best, and the hot topic after the game? It can also be said that the full amount. `

If `Which groups and applications to follow` is empty, post-match reviews can still be generated; when news notifications are needed for hot discussions, relevant fan group notifications can be queried without limiting the scope of groups and applications.

## Output type

Users can choose from the following 4 short sentence types:

- `Summary the game in one sentence`: Combines a quick overview of the game and a one-sentence summary, suitable for quick forwarding.
- `How the ball was played`: Combine the game review and goal timeline, focusing on how the game changed.
- `Who played the best`: Merges full-game data and star performance, focusing on who played well and what the data shows.- `Hot Topics After the Game': Merges hot comments from fans, hot comments from news notifications, and opinions of celebrities, focusing on refining controversies, emotions, and high-frequency topics.

If the user explicitly says `full`, `complete`, `all`, all 4 types will be output.

Each output type only outputs the corresponding content. Do not append extra paragraphs.

## Workflow

### 1. Confirm the game and game status

Standardize the Chinese and English names of the team. Confirm the match date, World Cup stage, group, match location and, if the match is over, confirm the final score. If there is an ambiguity in the date, the specific date adopted must be stated.

**Must do: Determine the game status. ** This is a mandatory step and cannot be skipped. First classify this game into one of the following three states, and then step 4 will take different branches according to the state:

- `Ended`: A clear end signal appears, such as final, full time, end of game, end, post-game, Full Time, FT, 90'+, 120'+, penalty shootout has been decided, or the search results have given the official final score of the game.
- `In Progress': Signals such as live broadcast, first half, halftime, second half, overtime, penalty shootout in progress, X minute, injury time, HT, etc., and there is no full-time end signal. Note: Intermission (HT, half-time) is `in progress`, not the end.
- `Not started`: The game has not kicked off yet. There are only signals such as pre-match preview, starting list, upcoming start, start at XX o'clock Beijing time, etc., without any real-time score.

Determine the conservative principle (important):

- Only when there is a clear end signal or it can be confirmed that the official final score is obtained, it can be judged as `over'.
- As long as it is not possible to confirm that the game has ended, it will be treated as `in progress' and will never default to the fact that the game has been played.
- If you can't distinguish between "in progress" and "not yet started", if there is any score, press `in progress', if there is no score, press `not yet started'.
- If the event text provided by the user contains a clear full-time score (such as `Argentina 3-0 Algeria Final`), it can be directly judged as `Ended`.

### 2. Collect post-match information

If necessary, search relevant battle reports, technical statistics, post-match discussions and comment directions for this game for internal verification and content organization.

Key points to complete when searching internally:

- Scores, match dates, stages, groups, locations
- Goal timeline, red and yellow cards, penalties, substitutions, starting lineup
- Shot, shot on target, possession, corner kick, foul, yellow card, red card, xG or key chance
- Key player performance, coaching adjustments, tactical changes
- Controversial points after the game, hot discussions among fans, and commentators’ opinions

Processing rules:

- The score, goal time, red and yellow cards, technical statistics, and records must be checked before being written into the text.
- Weakly relevant, expired or insufficient content pages are only used as clues for continued retrieval.- Before any material enters the text, it must be filtered for relevance to the target competition.
- Do not write inferences as facts; omit any revelations without sufficient basis.

Stratify each important piece of information:

- `Facts`: scores, goals, lineups, statistics, official records
- `Public opinion`: fan comments, media headline tendencies, social media hot discussions
- `Inference`: tactical review, winner and loser, player status judgment
- `Omitted`: Injury rumors, locker room news, revelations without sufficient basis

### 3. Retrieve and refine fan group notifications

If the user's request involves message notifications, fan groups, game viewing groups, group chat hot discussions, mobile phone reminders, or the user explicitly requests full/select `post-match hot topics', the notification must be queried first, and then notification-related content is generated.

Use local notification retrieval capabilities. If the user provides a time range, the user time range is strictly used. If no time range is provided, the default query is 2 hours before the start of the game to 24 hours after the game. If the match time has not been confirmed yet, confirm the match time first; if the match time still cannot be confirmed, query the local time from 00:00 yesterday to the current time.

Reusing old notification results is strictly prohibited. Each time a notification context is required, it must be queried again.

If local notification retrieval is unavailable or fails, write `Currently unable to query related fan group notifications. `, and continue to generate other modules.

Extract only content relevant to the target match or World Cup post-match discussion from all return notifications. Screening clues include:

- Event words: World Cup, World Cup, group stage, knockout round, battle report, post-match, review
- Team name, alias, country name, abbreviation
- Player names, common nicknames, coach names
- Scores, goals, red cards, penalties, hat tricks, buzzers, upsets, records
- Fan group/chat signals: group announcement, group chat, brothers, gathering, staying up late, halftime, post-game, review, breaking defense, becoming a god, laughing to death, refunding money
- User scenario scope: Teams/players/players in `Follow Who', output types in `What to Follow', groups, applications, channels or viewing locations in `Which Groups and Applications to Follow'

Ignore irrelevant notifications: takeout, express delivery, bank, system reminders, advertisements, work reminders, calendar noise, ordinary app push, non-football chat, etc.

The priority will be increased when the following content is hit: Who to follow, what to follow, which groups and applications to follow, repeated discussions, @users, direct inquiries, score discussions, controversial points, post-match reviews, famous scenes, player evaluations.

Only use notifications that actually exist. Do not simulate, fabricate, fill, or recreate missing notifications. If there are no relevant notifications, write: `No fan group notifications related to this game were found. `

The notification signals can be summarized as:

- Group emotions: excitement, defense breaking, controversy, jokes, nostalgia
- High-frequency topics: scores, goals, players, records, referees, tactics, substitutions
- Controversial points: star performance, coaching decisions, penalties, whether it is an upset, whether it is over-reliance on a certain player- Available words: must be based on real notifications for natural conversion
- Noise Ignored: List the main irrelevant categories

Do not expose irrelevant sensitive notifications. Only use short, relevant snippets when necessary.

### 4. Generate post-match review

**First select the branch according to the game status judged in step 1. This is a hard rule and cannot be skipped: **

- Branch A - Game status = `Ended`: It is generated normally according to the output type templates below this section, and the `Final Score` field is filled with the real full-time score as usual.
- Branch B - Game status = `in progress` or `not started`: **Do not apply the post-match review template and do not write "final score" anywhere. ** Jump directly to the "Unfinished Game Handling Rules" at the end of this section and follow the prompts and templates there to generate it.

Contents of branch A (closed) below:

The output goal is not to "stack data", but to help users quickly understand the game, retell key nodes, and refine post-game opinions. The wording should be clear, natural, and replicable.

Generates the output type selected by the user. When the user makes multiple selections, the corresponding templates are spliced ​​in the following order: `Summary of the game in one sentence`, `How the ball was played`, `Who played the best`, `The focus of hot discussion after the game`. When the user explicitly requests `full quantity`, all 4 templates will be output in this order. In multi-select or full selection, only the top title, game date, event/stage, final score and user scenario are retained once, and subsequent templates start from the second-level title.

`Summary this game in one sentence` Output structure:

```markdown
# {Team A} vs {Team B} Post-match review

Competition date:
Event/stage:
Final score:
User scenario:

## Summarize this game in one sentence
{A natural, replicable post-game summary. }

## Quick Facts
- Final score:
- The biggest highlights:
- Key players:
- Key turning point:
- Conclusion after the game:
```

`How the ball was played` Output structure:

```markdown
# {Team A} vs {Team B} Post-match review

Competition date:
Event/stage:
Final score:
User scenario:

## How was the ball played?
### First Half
### Second half
### Key turning point
### Winner and Loser and Tactical Observation

## Goal timeline
- Minute X: {Goal Process}
- Minute X: {Goal Process}
```

`Who played the best` output structure:

```markdown
# {Team A} vs {Team B} Post-match review

Competition date:
Event/stage:
Final score:
User scenario:

## Who plays the best
### {player}
Performance tags:
Key contributions:
Worth discussing:
Review skills:

## Key data
- Shot:
- Shots on target:
- Ball possession:
- Corner kick:- Foul/yellow card/red card:
- xG or critical opportunity:
- Data conclusion:
```

`Hot talk after the game` Output structure:

```markdown
# {Team A} vs {Team B} Post-match review

Competition date:
Event/stage:
Final score:
User scenario:

## Hot topics after the game
Hot discussion directions:
Disputed points:
Group sentiment:
High frequency topics:

## Message notification hot discussion
Related notification signals:
High frequency topics:
Group sentiment:
Disputed points:
Transformable words:
If not found: No fan group notification related to this game was found.

## Famous mouth opinions
Only organize comments that can be reproduced. It is not allowed to make up the original words of specific famous people.
Media/Commentator Views:
Safe to paraphrase:
Omitted:
```

### Rules for handling unfinished games (Branch B: in progress/not yet started)

As long as the first step is judged to be `in progress` or `not yet started`, go here and **do not follow the post-game review template above**. Core principles: First truthfully inform that the game is not over, the data may be inaccurate, and it is recommended to use it after the end, and then give the information that can be confirmed so far. Never write the real-time/halftime score as the "final score", and never write the half-time performance as the final conclusion.

General hard rules (applicable to both states):

- Do not write "Post-match review" in the output title. For `in progress`, write `real-time results`, for `not yet started`, write `pre-game overview`.
- The words "Final Score" do not appear anywhere. The score is always written as "Current Score" with status and minutes.
- Only write what has happened and can be verified (goals scored, cards played, substitutions made, current statistics). If it hasn’t happened or you’re not sure about it, just don’t write it down and don’t guess.
- All judgmental content (who played well, winner or loser, tactical conclusion, who will win) must be written as tentative. Words such as "at present", "temporarily" and "if the current situation is maintained" must not be written as final.
- Regardless of the requested output type or a request for a "full report," use only the relevant template below before the match ends. Defer detailed post-match analysis by type until the final whistle.

If status = `in progress`, output according to this template:

```markdown
# {Team A} vs {Team B} real-time results

> ⚠️ Real-time reminder: This game is not over yet (currently {first half/halftime/second half/overtime/penalty shootout}, it has reached the {X} minute). The following content is based on real-time information. Scores, data and conclusions may change with the game and be inaccurate. For a complete post-game review, it is recommended to run this skill after the end of the game.

Competition date:
Event/stage:
Current score: {Team A} {X}-{X} {Team B} (in progress·{X} minute)
User scenario:

## Current progress
- Reached: {X} minute ({stage})- The biggest highlights so far:
- Players who are currently outstanding:

## Confirmed key events (only write those that have already occurred)
- Minute X: {goal/red and yellow cards/substitution/penalty kick}
-…

## Current technical statistics (real-time, may continue to change)
- If there are existing data such as shots/shots on target/possession rate/corner kicks/fouls, write "None" if you don't have them.

## Tentative observation (not conclusive)
{Use "currently", "temporarily" and "if the current situation is maintained" to give a temporary judgment, and explain that it will change with the game. }
```

If status = `Not started`, output according to this template:

```markdown
# {Team A} vs {Team B} Pre-match overview

> ⚠️ Real-time reminder: This game has not kicked off yet, and there is no game data yet. The following is only information that can be confirmed before the game. Please run this skill after the game for a complete post-game review.

Kick-off time:
Event/stage:
Current score: None (no kickoff yet)
User scenario:

## Information can be confirmed before the game
- Playing against both sides:
- Time and place:
- Event/Stage/Group:
- Starter/Injury: If it has been officially announced, fill in it; if it has not been announced, write "Official has not announced yet"
- Highlights before the game:
```

If the user selects `Post-match Hot Discussions` or requires `Full Volume`, and there is indeed relevant real-time discussion in the local notification, a `## Real-time Group Chat Hot Discussions` section can be added to the end of the above template, which will still be treated as real-time and undecided, and indicate "The following is a group chat discussion in progress during the game, not a post-match conclusion." If there is no relevant notice, no additional information will be added.

## Style rules

- Chinese output is used by default unless the user specifies other languages.
- Give conclusions first, then details.
- Reviews should be like content that people can send to their friends and should not be written as database reports.
- Don’t pile up jargon; tactical points should fall into game details that users can observe.
- Do not write offensive, insulting, geographical, racial or identity offensive jokes.
- Don’t turn star rivalries into mutual insults among fans.
- Do not write fan comments, group chat opinions or tactical inferences as facts.
- Do not make up the original words of famous speakers; if there is no original words that can be directly quoted, only organize the "comment direction".
- When there is a clear date and time, the specific date and time must be written.
- Use: `more like`, `could be understood as` for inferential content, do not write as confirmed facts.
- Only if the game is `over`, the "final score" and post-game conclusion are allowed to be used; for `in progress` / `not yet started`, the "current score" will be used and the status will be indicated. It will first prompt that the data may be inaccurate.
- When the game is not over, the midfield or real-time score will never be written as the final score, and the half-time performance will never be written as the conclusion of the game.
- Simulation notification is prohibited for official operation; simulation is only allowed when the user explicitly requests samples or tests, and must be explicitly marked.- The final answer only presents the content of the review requested, without adding additional paragraphs.

## Quality Check

Confirm item by item before output:

- The match is a World Cup soccer match, or the user explicitly requests an extension.
- The game status (Ended/In Progress/Not Started) has been determined, and if the end cannot be confirmed, press "In Progress".
- When the game is not over: the title is not "Post-match review", "Final score" does not appear, real-time prompts are added, and all conclusions are marked as tentative.
- Scores, goals, and key data have been checked.
- The retrieved materials are filtered by the relevance of the target competition before entering the text.
- When the context needs to be notified, the new query results are used, not the old results.
- There are no simulated notifications or fabricated group messages; if the user requests a simulated sample, it is clearly marked "simulated".
- The opinions expressed in the notice are not written as facts.
- Fan comments are not written as facts.
- Tactical judgment is marked as inferred unless the material explicitly states it.
- There are no fictional famous quotes.
- The output type required by the user has been adhered to.
- The final answer contains only the requested review content.
- Do not make up when notification data is missing; when query fails, write `Currently unable to query relevant fan group notifications. `;If the query is successful but there are no relevant results, write `No fan group notification related to this game was found. `
