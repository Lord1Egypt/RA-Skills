# Recommendation Rubric

## When the user provides a current goal
Weight approximately:
- 60% goal fit
- 40% history fit

Examples:
- "我最近想系统学 AI Agent"
- "我想补创业管理"
- "我想读几本建立世界史框架的书"

## When the user provides no goal
Weight approximately:
- 70% history fit
- 20% recency
- 10% exploration/diversity

## What to look at in normalized data
### Strong positive signals
- high `engagement_score`
- finished books
- books with many notes/bookmarks/reviews
- recently active books
- repeated categories among high-engagement books

### Weak signals
- unread books with zero interaction
- imported/archive items with no progress
- books present only because they were added long ago

## Recommended reply structure
### 1. Reading profile
Summarize:
- dominant themes
- likely preferred style (framework / practical / narrative / theoretical)
- recency shift

### 2. Recommendations
For each book, explain:
- why it matches the goal or history
- which prior books it resembles
- what new angle it adds
- whether it is a safe pick or exploration pick

### 3. Why now
State why the recommendation fits the user's current stage.

### 4. Skip for now (optional)
Call out books that may be good later but are not the best next read.

## Avoid
- empty similarity claims
- recommending near-duplicate editions/translations as if they were new discoveries
- recommending only because a book is famous
