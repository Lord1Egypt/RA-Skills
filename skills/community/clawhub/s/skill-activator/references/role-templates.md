# Role Templates — Skill Activator

Personalized automation recommendations by role. After scanning the user's environment, match their identity to the closest role and recommend specific automations.

## Product Manager / 产品经理

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Competitive monitoring is manual | Daily auto-scan competitor updates → generate briefing | agent-reach + content-shapeshifter + feishu-doc |
| Meeting notes scattered, action items lost | Meeting transcript → auto-extract todos + calendar events | feishu-doc + wecom-edit-todo + wecom-schedule |
| PRD writing from scratch every time | Voice/text input → structured PRD document | feishu-doc |
| Data metrics require manual checking | Scheduled data summary → push to chat | feishu-doc + wecom-msg |

## Software Developer / 程序员

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Onboarding to unfamiliar codebases | Repo scan → architecture doc + key file guide | coding-agent + github |
| GitHub issues pile up | Auto-triage issues → suggest fixes → open PRs | gh-issues + coding-agent |
| Release process is tedious | Version bump + changelog + tag + publish | release-skills + github |
| Documentation drifts from code | Code change detection → doc update reminder | github + feishu-doc |

## Content Creator / 自媒体博主

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Finding trending topics takes hours | Auto-scan trending content across platforms | agent-reach |
| Adapting one post for multiple platforms | Write once → auto-adapt for XHS/WeChat/Twitter | content-shapeshifter |
| Cover images are time-consuming | Auto-generate cover images from title | baoyu-cover-image + baoyu-image-gen |
| Publishing to multiple platforms manually | One-click multi-platform publish | xhs-publish + baoyu-post-to-wechat |
| Analyzing post quality before publishing | Auto-audit content quality + suggestions | xiaohongshu-note-analyzer |

## Operations / 运营

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Daily reports assembled manually | Auto-aggregate data → formatted report | feishu-doc + wecom-msg |
| Social media monitoring is fragmented | Unified monitoring across platforms → alerts | agent-reach + feishu-doc |
| Event/campaign tracking in spreadsheets | Auto-update tracking sheets from multiple sources | feishu-doc |
| Customer feedback scattered | Aggregate feedback → categorize → summary | agent-reach + content-shapeshifter |

## Team Lead / Manager / 团队管理者

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Scheduling meetings across busy calendars | Check availability → find common slots → book | wecom-schedule + wecom-meeting-create |
| Following up on delegated tasks | Track todo completion → nudge reminders | wecom-get-todo-list + wecom-edit-todo |
| Weekly team summary takes hours | Auto-generate weekly summary from activity | feishu-doc + github |
| Forgetting 1-on-1 prep | Pre-meeting briefing auto-generated | wecom-schedule + wecom-msg |

## Student / Researcher / 学生研究者

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Literature review is overwhelming | Auto-search papers/articles → summarize trends | agent-reach |
| Notes scattered across tools | Aggregate notes → structured knowledge base | feishu-doc |
| Presentation slides from scratch | Content → auto-generate slide outline | feishu-doc |
| Study schedule not followed | Smart reminders based on exam dates | wecom-schedule + wecom-edit-todo |

## Freelancer / 自由职业者

| Pain Point | Automation | Skills Needed |
|------------|-----------|---------------|
| Client communication across platforms | Unified inbox summary + auto-reply drafts | wecom-msg + feishu-doc |
| Invoice and project tracking | Time tracking → invoice generation | feishu-doc |
| Portfolio updates manual | Auto-update portfolio from completed work | content-shapeshifter |
| Finding new leads | Monitor relevant discussions → alert opportunities | agent-reach |

---

## How to Use This File

1. Run `scripts/scan_environment.sh` to get the user's installed skills and identity
2. Match user's SOUL.md / USER.md role to the closest template above
3. Cross-reference "Skills Needed" with actually installed skills
4. Generate personalized report:
   - ✅ Already have: skills installed and applicable
   - 📦 Recommend install: skills available on ClawHub but not installed
   - 🔧 Can build: automation achievable by fusing existing skills
   - ❌ Gap: no existing skill covers this, suggest creating one
