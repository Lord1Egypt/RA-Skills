---
name: trello_planner
author: tomas-mikula
web: FrontendAccelerator.com
description: |
  Read-only Trello planner using official Boards API.

  🧠 AI PLANNING: Task prioritization, sprint capacity, board optimization
  📊 ANALYSIS: Lists/cards/members from /boards/{id}/* endpoints
  🔍 SEARCH: Overdue, assignees, labels across boards

  REQUIRES: TRELLO_API_KEY + TRELLO_TOKEN (read scope)
  ENDPOINTS: /1/boards/{id}/lists, /cards, /members (official spec)

user-invocable: true
install: []
env:
  - TRELLO_API_KEY
  - TRELLO_TOKEN
primary-credential: TRELLO_TOKEN
gating:
  - env: TRELLO_API_KEY
    message: "TRELLO_API_KEY: https://trello.com/app-key"
  - env: TRELLO_TOKEN
    message: "TRELLO_TOKEN: https://trello.com/1/authorize?key=[KEY]&scope=read&expiration=never"
  - binary: node
slash-commands: ["/trello-plan", "/trello-optimize"]
tags: [trello, planner, boards-api]
categories: [productivity, pms]
metadata: {"openclaw":{"emoji":"🗓️","requires":{"env":["TRELLO_API_KEY", "TRELLO_TOKEN"]},"primaryEnv":"TRELLO_TOKEN","homepage":"https://developer.atlassian.com/cloud/trello/rest/api-group-actions/"}}
---

# Trello Planner - Official Boards API
[https://developer.atlassian.com/cloud/trello/rest/api-group-boards/](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/)


## 🛠 Setup (Read-Only Token)
```
1. https://trello.com/app-key → API Key
2. https://trello.com/1/authorize?key=[YOUR_KEY]&name=TrelloPlanner&scope=read&expiration=never → Token  
3. Test: https://api.trello.com/1/members/me/boards?key=[KEY]&token=[TOKEN]
```

## Verified Endpoints (Boards Group)

| Endpoint | Purpose | Params | Docs |
|----------|---------|--------|------|
| `GET /1/members/me/boards` | User boards | `fields=name,id` | [Members→Boards] |
| `GET /1/boards/{id}/lists` | Lists on board | `fields=name,id,closed` | [Boards API] |
| `GET /1/boards/{id}/cards` | All cards | `fields=name,due,idList,closed` | [Boards API] |
| `GET /1/boards/{id}/members` | Team members | `fields=username,fullName` | [Boards API] |
| `GET /1/search` | Overdue cards | `query="due:<now"` | [Search API] |

## 🚀 Example Usage & Output

**Query**: `/trello-plan Engineering`
```json
{
  "status": "success",
  "data": {
    "board_name": "Engineering Sprint 42",
    "cards_open": 18,
    "overdue_count": 2,
    "planner_insights": ["🚨 PRIORITY: Fix login (overdue 2d)", "⚖️ Review overloaded (8 cards)"],
    "health_score": "🟡 Needs attention"
  }
}
```

## Do's & Don'ts

**✅ DO:**
- Parallel `/boards/{id}/lists+cards+members`
- `fields=` param limiting
- Cache 30min (boards stable)

**❌ DON'T:**
- Write endpoints (POST/PUT/DELETE)
- Full card fields (attachments slow)
- Log tokens (security)

## 🧪 Test Cases (Verified Post-Fix)

| Test | Expected |
|------|----------|
| No token | `error_type: "auth"` + setup URLs |
| Closed cards | Properly excluded from `openCards` |
| Large boards | `limit=100` safe |
| Rate limit | `error_type: "rate_limit"` |

## 📈 Metrics Explained
- **Health Score**: overdue/open <15% = 🟢
- **Planner Insights**: Top overdue + balance suggestions
- **Capacity**: members vs open cards ratio

## 🔒 Security (ClawHub Approved)
```
✅ read scope ONLY
✅ api.trello.com exclusively  
✅ No persistence/file I/O
✅ No token logging/output
✅ 12s timeout
✅ package.json registry aligned
```

---
**ClawHub v1.0.8** | tomas-mikula | FrontendAccelerator.com
---