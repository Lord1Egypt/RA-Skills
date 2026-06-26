---
name: research-paper-push
description: Create scheduled research-paper alerts using OpenAlex and OpenClaw cron. Use to subscribe to journals, conferences, or research topics; list/update/cancel subscriptions; test real OpenAlex queries; and push concise daily Chinese summaries of newly matched papers. Designed for topic monitoring such as AD/MCI, dynamic functional connectivity, rs-fMRI, graph neural networks, and medical imaging.
---

# Research Paper Push

Create daily paper-alert subscriptions that query OpenAlex, filter real recent papers by topic and preferred venues, and format concise Chinese summaries for delivery.

This skill is for researchers who want an automated “what's new today?” workflow: define journals/conferences, define keywords, choose a time, and let OpenClaw cron run the subscription.

## What it helps with

- Subscribe to new papers by topic, journal, or conference.
- Run one-off test queries before enabling a schedule.
- Maintain local subscription state and last-checked dates.
- Produce short Chinese summaries with title, authors, venue, date, link, matched topics, and relevance.
- Monitor neuroimaging/medical-AI topics such as AD/MCI, dynamic functional connectivity, rs-fMRI, GNNs, and brain networks.

## Use cases

Use this skill when the user wants to:

- Subscribe to new papers in a research area.
- Push papers from selected journals/conferences at a daily time.
- List, update, or cancel paper subscriptions.
- Send a test paper-summary push.
- Run a local scheduled research-monitoring workflow with OpenClaw cron.

Do not use this skill for one-off literature search, DOI lookup, or long literature reviews; use a paper-search/review skill instead.

## Safety and privacy

- Do not store API keys, tokens, cookies, or private channel credentials in the skill folder.
- OpenAlex does not require an API key. Set `OPENALEX_MAILTO` only if the user wants a polite-pool contact email.
- Treat recipient IDs passed with `--to` as local user data; do not include generated `data/*.json` files when publishing the skill.
- Ask before creating or deleting external cron jobs if the user did not explicitly request scheduling changes.
- For QQ or other chat channels, confirm timezone before creating the first scheduled push.

## Bundled script

Run:

```bash
python scripts/manage_papers.py <action> [options]
```

Supported actions:

- `add` — create a subscription and register a cron job.
- `list` — list subscriptions, optionally filtered by recipient.
- `update` — update time, timezone, journals, topics, or lookback days.
- `remove` — remove a subscription and cron job.
- `test` — query OpenAlex once and print a test summary without saving a subscription.
- `run` — execute one subscription by ID and update its `last_checked` date.

Common options:

- `--to "<recipient-id>"`
- `--time "09:00"`
- `--timezone "Asia/Shanghai"`
- `--journals "IEEE TMI,NeuroImage,Medical Image Analysis"`
- `--topics "Alzheimer,MCI,dynamic functional connectivity,graph neural network,rs-fMRI"`
- `--days 3` — look back N days when no `last_checked` date exists.
- `--since YYYY-MM-DD` — override the OpenAlex `from_publication_date` filter.
- `--limit 10` — maximum papers to summarize.

## First-time subscription flow

1. Ask for a clear daily push time if missing.
   - Example: `09:00`, `12:00`, `20:30`.
2. Confirm the user's timezone.
   - Default can be `Asia/Shanghai` when appropriate.
3. Confirm journals/conferences and topics.
4. Create the subscription with the script.
5. Verify the cron registration succeeded.

Example:

```bash
python scripts/manage_papers.py add --to "<recipient-id>" --time "09:00" --timezone "Asia/Shanghai" --journals "IEEE TMI,NeuroImage,Medical Image Analysis" --topics "Alzheimer,MCI,dynamic functional connectivity,graph neural network,rs-fMRI"
```

List subscriptions:

```bash
python scripts/manage_papers.py list --to "<recipient-id>"
```

Update a subscription:

```bash
python scripts/manage_papers.py update --id "1" --time "20:30" --topics "Alzheimer,MCI,dynamic brain network,GNN"
```

Remove a subscription:

```bash
python scripts/manage_papers.py remove --id "1"
```

Run a real OpenAlex test query:

```bash
python scripts/manage_papers.py test --since "2026-01-01" --limit 5 --journals "NeuroImage,Human Brain Mapping" --topics "Alzheimer,MCI,dynamic functional connectivity,rs-fMRI,GNN"
```

Run one saved subscription:

```bash
python scripts/manage_papers.py run --id "1" --limit 10
```

## OpenAlex behavior

The script:

1. Builds English OpenAlex search queries from subscription topics.
2. Uses `from_publication_date` based on `--since`, saved `last_checked`, or `--days`.
3. Queries `https://api.openalex.org/works` sorted by recent publication date.
4. Converts OpenAlex works into paper records with title, authors, venue, date, DOI/link, citation count, and abstract.
5. Scores relevance against subscription topics plus common neuroimaging synonym groups.
6. Prefers requested journals/conferences but keeps highly relevant adjacent results.
7. Deduplicates by DOI, OpenAlex ID, or title.

## Default subscription model

If the user does not specify journals or topics, use the bundled defaults in `scripts/manage_papers.py`:

- Medical imaging and neuroimaging journals/conferences.
- Dynamic brain networks, functional connectivity, neurodegenerative disease, MRI/fMRI, and graph/deep learning topics.

## Output style

Default summaries are concise Chinese bullet points including:

- Title
- Authors/year/venue
- Publication date and citation count
- DOI or OpenAlex link
- Matched topic keywords
- Whether the paper is directly relevant or adjacent
