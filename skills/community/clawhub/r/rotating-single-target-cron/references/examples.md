# Examples

Use these as starting patterns. Replace the roster, schedule, state-file path, and content constraints.

## 1. Heartbreak / lost-youth microfiction

```text
Send exactly one Japanese-light-novel-style heartbreak / lost-youth short piece to the current chat every day at 08:30 (Asia/Shanghai).

Roster: @a, @b, @c
State file: memory/heartbreak-last-target.txt

You must follow these rules exactly:
1. Before writing, read the state file. If the file does not exist, is empty, or contains an ID not in the roster, treat the previous target as "none".
2. Randomly select exactly one person from the roster as the only protagonist for this story.
3. Never select the previous target when any other valid option exists.
4. After choosing the protagonist, immediately overwrite the state file with that target's @ID so the next run can avoid them.
5. Do not mention any other IDs from the roster anywhere in the story.
6. Output only the message body that should be posted to chat. Do not add explanations, titles, or before/after notes.
7. Write in Chinese and keep the length around 200-300 characters.
8. Use second person ("you") and weave the chosen @ID naturally into the beginning.
9. Use a solitary, quiet, ending-scene mood; do not write group-party scenes.
10. Keep it emotional and slightly bittersweet, not comedic, and still acceptable for a public group chat.

Start writing the story directly.
```

## 2. Single-target wake-up message

```text
Send exactly one wake-up message to the current chat every day at 08:30 (Asia/Shanghai).

Roster: @a, @b, @c
State file: memory/wakeup-last-target.txt

You must follow these rules exactly:
1. Read the state file first. If it is invalid, treat the previous target as "none".
2. Randomly select exactly one person from the roster as the only target for this run.
3. Never repeat the previous target unless no other option exists.
4. After choosing the target, overwrite the state file with that target's @ID.
5. Do not mention any other roster members.
6. Output only the final message body that should be posted to chat.
7. Mention the chosen @ID naturally near the beginning.
8. Write a 40-80 character Chinese wake-up message that is light, playful, group-chat safe, and not threatening or explicit.
```

## 3. Single-target teasing / bit post

```text
Send exactly one playful teasing mini-post to the current chat every day at 20:00 (Asia/Shanghai).

Roster: @a, @b, @c
State file: memory/tease-last-target.txt

You must follow these rules exactly:
1. Read the state file first. If it is invalid, treat the previous target as "none".
2. Randomly select exactly one person from the roster as the only target for this run.
3. Do not repeat the previous target unless there is no alternative.
4. After choosing the target, immediately overwrite the state file.
5. Only one @ID may appear in each post.
6. Output only the final message body.
7. Keep it public-chat safe; do not write real violence, privacy violations, harassment, or explicit sexual content.
8. Exaggeration is allowed, but the post must not read like a real threat.
```

## 4. Daily one-person fortune

```text
Send exactly one daily fortune message to the current chat every day at 09:00 (Asia/Shanghai).

Roster: @a, @b, @c
State file: memory/fortune-last-target.txt

You must follow these rules exactly:
1. Read the state file first. If it is invalid, treat the previous target as "none".
2. Randomly select exactly one person from the roster as the only target for today.
3. Do not repeat yesterday's target unless no other option exists.
4. After choosing the target, immediately overwrite the state file.
5. Output only the final message body and mention the chosen @ID naturally near the beginning.
6. Do not mention any other IDs from the roster.
7. Keep the fortune short, light, and suitable for a group chat. Avoid deterministic medical, legal, or investment advice.
```
