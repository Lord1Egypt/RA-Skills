---
name: yoooclaw-meeting-preparations-en
description: Preparation before the meeting - Generate a "preparation briefing" for users before the meeting. News from relevant people in mobile phone notifications, as well as external developments searched on the Internet, are organized around the theme of the meeting into a global overview, key findings and suggested focus points. This skill is used when the user mentions meetings, pre-meeting preparations, war preparations, meeting briefings, "start preparations", or gives "people/things to follow" and wants to sort out information before the meeting. Even if the user does not explicitly say the word "briefing", this skill should be used as long as it is necessary to quickly grasp the latest status of a certain topic before the meeting.
Compatibility: Internet search depends on the byted-web-search skill; if it is missing, press "Prerequisites" below to handle it.
---

# Meeting Prep

Generate pre-meeting preparation briefings for users. Follow the sequence below strictly and do not skip steps.

## User input

- Following: `{{who}}`
- Focus on: `{{what}}`

## Core Principles

"Things of concern" is the main line of this briefing, and all searches, screening, and summarization are centered around it.
"Following people" is an observation perspective - used to see what these people have said and done recently around the main line.
News that is irrelevant to the main story, even if it comes from people who follow it, should not appear in the briefing.

## Pre-dependency: Internet search capability

The second step may require Internet search, relying on the `byted-web-search` skill. Check it once before starting, no need to confirm again with the user:

1. Execute `openclaw skills list` and check whether `byted-web-search` is included in the output.
2. Installed: Continue normally.
3. Not installed: execute
   `npx skills add https://skills.volces.com/skills/bytedance/agentkit-samples -s byted-web-search --agent openclaw`
   - Installation successful: continue normally.
   - Installation failed: **Do not abort the entire briefing**. Make a note of "Internet search is not available", skip the networking part directly in the second step, generate a briefing using only the notification information, and prompt "Unable to search for external information online this time" at the end of the briefing.

>Design note: Purely internal meetings do not require Internet search, so if the Internet capability is missing, it will only be downgraded and not blocked.

---

## Step 1: Search from phone notificationsExtract 1-3 short keywords from "Things of Interest". When extracting, remove the modifiers such as "weekly meeting", "monthly meeting", "review", "focus" and "key points", and only retain the core nouns.

Extraction example (reference):
- "Project A weekly meeting, focusing on budget approval" → Project A, budget approval
- "Q2 Planning Review" → Q2 Planning
- "Discuss cooperation plans with customers" → Customers, cooperation plans
- "Team Weekly Meeting" → Team

Notifications for the last 7 days for each keyword search. If "Following People" is not empty, the notifications of the last 7 days will also be searched for each person's name.

Summarize all results for later use. If there are no results, write down "No relevant information found in the notification" and continue to the next step.

## Step 2: Determine whether you need to search online

Judgment based on "matters of concern" (search if any one of them is met):
- Involving industry dynamics and market trends
- Involving competing products, friendly merchants, and external partners
- Involving changes in policies, regulations and standards
- Involving the latest developments in a certain technology
- Involving external customers or suppliers

**No need to connect to the Internet**: purely internal weekly meetings/stand-up meetings/progress synchronization, internal review/review, only discussing internal processes and division of labor.

Judgment example (reference):
- "Customer A Cooperation Plan Discussion" → Search "Customer A Company Latest News"
- "Project A Internal Weekly Meeting" → Do not search
- "AI large model technology selection meeting" → Search for "AI large model latest progress"
- "Team Monthly Review" → Do not search
- "Preparation for Industry Summit Participation" → Search for "[Industry Name] Summit Latest Topics"

Need to search: Generate 1-2 search terms by yourself, use `byted-web-search` to perform Internet search, set the time range to the last week, and record the results for later use.
There is no need to search, or the "People Following" and "Things Following" are all empty, or the networking capability is unavailable: Skip this step and go to the third step.

## Step 3: Organize theme dimensions

Put together all the information collected in the first and second steps (notifications + networking), and sort out 2-4 theme dimensions around "things of concern":

1. Find recurring topics or directions around the main thread.
2. Group information with similar content into the same dimension (regardless of source).
3. Use a short title to summarize each dimension (such as "Product experience and quality", "Market channel progress", "Functional planning direction").
4. Information irrelevant to the topic is directly discarded in this step.

Example - When the topic is "YoooClaw App", it is possible to sort out: product experience and stability, market and channels, functions and hardware direction.

## Step 4: Output war preparation briefing

The output is session text, no file is generated. Strictly follow the following template:

```
📋 [Use one sentence to summarize the key points of this briefing around "matters of concern", ≤30 words]

## 🎯Conference theme
{{what}}

## 📊 Global overview[3-5 sentences, integrating all the information from notifications and Internet searches, and giving an overall judgment around the "matter of concern":
At what stage has it progressed, what is the overall situation, and what are the noteworthy changes? This section is the most important,
Users may enter the conference room just after watching this paragraph. ]

## 🔍 Key findings
[Output one by one according to the subject dimensions in the third step. Information under the dimensions does not distinguish between sources and is presented in a mixed manner. ]

### [Dimension 1 title]
[1-2 sentences summarizing the main points. ]
- [Source Marking] [Message content, can be simplified but retain the original meaning]
- [Source label] [Message content]

### [Dimension 2 Title]
[1-2 sentence summary. ]
- [Source label] [Message content]

### [Dimension 3 Title] (if any)
...

## ❓ Suggested points of concern
- [Issue]: [Why it deserves attention, 1 sentence]
- [Issue]: [Why it deserves attention, 1 sentence]
```

Source labeling rules:
- Notification message: `[Source App · Name · Date]`, such as `[Feishu · Shi Dongbo · 4/18]`
- Internet search: `[Source website · Date]`, such as `[China.com · 5/9]`

Constraints: Each dimension can list up to 4 most relevant messages; 2-4 dimensions, no more than 4.

If both notifications and Internet searches yield no results at all, the "Key Findings" section reads:
> No information found for "{{what}}".

If there is little or empty information, write in the "Suggested Focus" section:
- Information is limited. It is recommended to communicate directly with relevant personnel before the meeting to understand the latest situation.

## Secret rules

- Only fill in "Things of concern" but not "People of concern" → Skip the name search, only search for notifications by subject keywords, and do not include the name of the person in the source tag.
- Fill in only "people you are following" but not "things you are following" → Search only for notifications related to the person's name and skip online searches; write "unspecified" in the "meeting topic" in the template, and sort out the dimensions around the recent common topics of these people.
- Fill in neither → Output "Please fill in at least one item of concern and try again", and do not generate a briefing.
- The total number of search results exceeds 15 → Filter by relevance to the topic and then sort out the dimensions.