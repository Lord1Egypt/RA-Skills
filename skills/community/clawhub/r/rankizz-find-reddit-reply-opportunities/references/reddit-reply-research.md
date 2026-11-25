# Reddit reply research contract

## Rankizz tool

Use `search_social_research` with `platform: "reddit"`.

Relevant inputs:

- `projectId`: required Rankizz project
- `queries`: 1 to 20 terms combined into one provider request
- `sort`: `relevance`, `new`, `top`, or `comment_count`
- `timeframe`: `all`, `day`, `week`, `month`, or `year`
- `cursor`: continuation cursor from a prior response
- `runId`: saved run to append when loading another page

One provider request costs one credit. The output includes the saved run, query, search date, next cursor, credits charged, and result items. Items can include URL, title, description, author, community, publication date, score, comments, likes, and views. Some metrics may be null.

Use `list_social_research_history` to reuse recent saved searches when appropriate. Do not call `delete_social_research_history` unless the user explicitly asks to remove saved data.

## Primary platform references

- [Reddit Rules](https://redditinc.com/policies/reddit-rules)
- [Reddit Help: spam](https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam)
- [Reddit Pro organic engagement playbook](https://redditinc.com/hubfs/Reddit%20Inc/Content/Reddit%20Pros%20organic%20playbook.pdf)
- [FTC endorsement guidance](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)
- [FTC social media disclosure guidance](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)

## Hard boundaries

- Follow current site-wide and subreddit rules.
- Do not automate posting, replies, voting, account creation, private messages, or repetitive engagement.
- Do not evade a ban, removal, promotion restriction, or moderator instruction.
- Do not conceal ownership, employment, payment, affiliate benefit, free access, or another material relationship.
- Do not infer private or sensitive traits from a user's history.
- Do not promise that a reply will remain live, receive engagement, or generate customers.
