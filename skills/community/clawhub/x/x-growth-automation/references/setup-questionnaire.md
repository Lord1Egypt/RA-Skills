# Setup Questionnaire

Use this to install a reusable X growth automation system for a new user.
Ask only what is still missing.

## 1. Strategy
- What is the account about?
- What niche(s) should the system focus on?
- What language or languages should posts use?
- Is there one primary language and one secondary language?
- Should the tone be more technical, more casual, more founder-like, or more educational?

## 2. Cadence
- Ideal daily post range?
- Hard monthly cap?
- Should replies be automated?
- If yes, max replies per day?

## 3. Sources
- Is Bird CLI available?
- Is X API available?
- Should an external source feed be used as a source channel, a CTA destination, or both?
- What is that source/feed/platform? (Telegram, Discord, newsletter, RSS, blog, other)
- Any existing content cron/job that should branch into X?

## 4. CTA / Community
- Should replies include a community CTA?
- If yes, what link should be used?
- Which platform is that community on?
- Should CTA appear only in reply automation, or also in normal posts?
- Should replies prefer mentions only, or may they also target search-discovered tweets?
- If a reply fails because of target restrictions, should the system skip the slot or try another reply candidate?

## 5. Live vs Dry-run
- Start in dry-run or live mode?
- If live: when should live publishing begin?
- Any blocked hours or preferred posting windows?

## 6. Safety / Filtering
- Any banned topics?
- Any banned accounts or sources?
- Any tone/style examples to imitate or avoid?
- How aggressive should the system be: cautious, balanced, aggressive?

## 7. Credentials / Delivery
- Where will `.env` live?
- Are X credentials ready?
- Are Bird cookies/session ready?
- If source branching is wanted, where does source content come from?

## Suggested defaults
- dry-run first
- Bird for discovery
- X API for publishing
- daily range 2-5 for initial rollout
- reply automation off by default unless explicitly requested
- CTA only in dedicated reply automation
- short-to-medium post length
- one primary language unless the user explicitly wants multilingual output

## Aggressive profile template (explicit opt-in)
- daily total: 10
- structure: 1 news/source crosspost + 1 special crosspost + 8 core
- reply lane: disabled (unless user explicitly insists)
- anti-repetition: enable recent-post similarity checks + source de-dup
