---
name: yoooclaw-personal-daily-en
description: Used when users need to generate a personalized daily news report based on the topics they care about; typical trigger sentences: 'Help me read today's news', 'Run the daily report', 'What's new today', 'Personalized daily report', 'Help me organize today's information', 'News express', 'What happened today', 'What's worth paying attention to'.
---

# Personal Daily News V2

The input is a list of topics that the user is interested in. The source is the interest topics carried in the `interests.md` configuration file or the scheduled task message.

Users can set topics of interest through the "What to follow" field in the installation pop-up window, such as: AI large models, new energy vehicles, entrepreneurial financing, humanoid robots, and a specific company or product.

The goal is to use a daily report to explain:
- What important things happened under each topic today?
- Which developments deserve in-depth attention?
- Overall trends and key signals

## Workflow

1. Read the interest-topic configuration at `/Users/xinyu/.openclaw/个性化日报/interests.md`; if the scheduled-task message contains interest topics, use those instead.
2. If there is no following topic in both places, output "The following topic has not been configured yet, please configure it in the scene settings first", and then stop.
3. Extract search keywords from the topic list and sort out 5-8 groups of search terms.
4. Use `byted-web-search` to perform targeted searches for each set of keywords (once for Chinese + once for English).
5. Strictly filter non-daily news and discard old news, advertisements, soft articles, and headlines.
6. Only the best sources of multiple reports on the same event will be retained, and no reports will be piled up one by one.
7. Organize into groups by topic and output structured daily reports.

## Search rules

### Search Tools

All searches are performed using `byted-web-search` (Volcan Engine Web Search).

### Search strategy

Each group of keywords is searched twice (Chinese + English), and the total number of searches does not exceed 15 times.

Search term construction:
- Chinese: `{Keyword} {M month D day}`, such as `AI large model May 13`, `OpenAI May 13`
- English: `{keyword} {Month Day, Year}`, such as `AI model May 13, 2026`
- No need for fuzzy words such as "today", "today", "recently", etc., and the specific date matching is more accurate
- When the quality of the first search results is poor, try again with more specific keywords.

## Timeliness filtering rulesEach search result must pass the timeliness check, and those that fail will be discarded directly:

- The title, abstract, and URL contain the current date (such as `2026-05-13`, `May 13`, `May 13`) → Reserved
- The abstract contains time words ("today", "just now", "today", "hours ago", "hours ago", "just now") → Keep
- Specific dates that are not the current day ("May 10th", "last week", "last week") → discarded
- Without any time signal → discard

Only the first occurrence of the same URL is retained.

## Source filtering rules

- Priority retention: domestic mainstream media (Xinhua News Agency, The Paper, 36Kr, Huxiu, Heart of the Machine, Qubit, etc.), overseas authoritative media (TechCrunch, The Verge, Reuters, Bloomberg, etc.), official blogs, and well-known technology media.
- Prioritize discarding: soft-text advertisements, SEO content, headlines, and marketing account content.
- Among multiple reports on the same event, only the one with the most complete information and the most authoritative source will be retained.
- If you can't find the news of the day under the topic, skip the topic directly and don't make up the count.

## Output requirements

The output is session text, no file is generated. The structure is as follows:

```text
☀️ Personalized daily report (YYYY-MM-DD)

One-sentence overview: Use 1 sentence to summarize today’s most noteworthy developments.

Today’s focus: {Topic 1}, {Topic 2}, {Topic 3}...

---

1. {Topic name}

  1. {News Title}
     {2-3 sentence summary explaining what happened and why it’s important}
     Source: {Source URL}

  2. {News Title}
     {2-3 sentence summary}
     Source: {Source URL}

---

2. {Topic name}

  1. ...

---

📌 Today’s summary

{3-5 sentences, summarize today’s most critical developments, highlight trends and signals worthy of continued attention}

---

💬 Which news are you interested in? Tell me to help you understand more.
```

If there is not enough valid news of the day after searching, it must be output:

```text
☀️ Personalized daily report (YYYY-MM-DD)

There is no major news on the topics you are interested in today. I wish you a good day.
```

## Output style

- High information density, suitable for quick reading in the morning.
- Tone soberly, concisely, and directly.
- Each abstract should be no more than 3 sentences, and the full text should be no more than 1,500 words.
- For news from English sources, the abstracts are uniformly presented in Chinese.
- Key data, person names, and product names remain in their original text.

## Decision Criteria

- Do not keep a running account, and give priority to outputting information that can affect judgment and action.- Do not make up news or URLs without an exact source.
- When the same event is updated before and after, the latest status shall prevail.
- When the information is sparse, it is better to type out the bottom-line copy instead of making up daily reports just to make up for the organization.
- Do not search for pan-news that is not related to topics that users care about.
