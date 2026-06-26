# Test Instructions

Before running the cases below, verify that every command listed in `SKILL.md` has a one-to-one match with the corresponding command in `src/cli.js`.

Then run the following commands and verify that the output matches the expectation.

## 1) Default invocation

### Command

```bash
node ./bin/signal-track.js
```

### Expected output

Show the usage text (the output starts with `Usage`).

## 2) `--help` flag

### Command

```bash
node ./bin/signal-track.js --help
```

### Expected output

Show the usage text (the output starts with `Usage`).

## 3) `-h` short flag

### Command

```bash
node ./bin/signal-track.js -h
```

### Expected output

Show the usage text (the output starts with `Usage`).

## 4) `-help` short alias

### Command

```bash
node ./bin/signal-track.js -help
```

### Expected output

Show the usage text (the output starts with `Usage`).

## 5) Login command

### Command

```bash
node ./bin/signal-track.js login --api-key <api_key>
```

### Expected output

For a valid key, print a success payload:

```json
{
  "status": "SUCCESS",
  "message": "Login success"
}
```

If `--api-key` is missing, print a validation error and usage text.

## 6) Topic show command

### Command

```bash
node ./bin/signal-track.js topic show --topic-id <topic_id> [--cursor <cursor>] [--page-size <page_size>]
```

### Expected output

Return topic details payload.

## 7) Topics list

### Command

```bash
node ./bin/signal-track.js topics my
node ./bin/signal-track.js topics list
```

### Expected output

Return topic list payloads.

## 8) Topics follow/unfollow

### Command

```bash
node ./bin/signal-track.js topics follow --topic-id <topic_id>
node ./bin/signal-track.js topics unfollow --topic-id <topic_id>
```

### Expected output

Return backend operation payload for each command.

## 9) Topics search

### Command

```bash
node ./bin/signal-track.js topics search --scope my --query <keyword> [--page-size <page_size>] [--page-number <page_number>]
node ./bin/signal-track.js topics search --scope square --query <keyword> [--page-size <page_size>] [--page-number <page_number>]
```

### Expected output

Return search payload for the selected scope.

## 10) News cards feed

### Command

```bash
node ./bin/signal-track.js news_cards feed my [--cursor <cursor>] [--page-size <page_size>]
node ./bin/signal-track.js news_cards feed [--cursor <cursor>] [--page-size <page_size>]
node ./bin/signal-track.js news_cards feed --topic-id a7ba7b790631f637 [--cursor <cursor>] [--page-size <page_size>]
```

### Expected output

- `news_cards feed my` and `news_cards feed` should return the default my feed payload.
- `news_cards feed --topic-id ...` should return topic feed payload.

## 11) News cards get

### Command

```bash
node ./bin/signal-track.js news_cards get --news-id 78a9ef8644bc29ecdcfb344ba44b6045
node ./bin/signal-track.js news_cards get 78a9ef8644bc29ecdcfb344ba44b6045
```

### Expected output

Return card detail payload.

Without `--json`, if the payload contains `data.cards`, print the first card object directly.

## 12) News cards search

### Command

```bash
node ./bin/signal-track.js news_cards search --query <keyword>
```

### Expected output

Return matching card search payload.

## 13) Article content

### Command

```bash
node ./bin/signal-track.js articles content --article-id ffcac7a9ccc1302d1a132ddb4d17387d
```

### Expected output

Return article detail payload.

## 14) Not logged in behavior

### Command

```bash
node ./bin/signal-track.js topics my
node ./bin/signal-track.js topic show --topic-id a7ba7b790631f637
```

### Expected output

If not authenticated, output:

```text
Error: You have not logged in yet. Run: signal-track login --api-key <api_key>
```
