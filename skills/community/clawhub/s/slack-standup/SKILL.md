# slack-standup SKILL.md

## Skill Identity
- Name: slack-standup
- Version: 1.0.0
- License: MIT
- Category: Productivity / Team Collaboration

## Description
Automated daily standup bot for Slack. Collects updates at scheduled times, aggregates responses, posts summaries.

## Business Value
- Problem: Remote teams waste time scheduling standup meetings
- Solution: Async standup via Slack bot
- ROI: Saves 15-30 min/day per team member

## Capabilities
1. collect_standup - Prompt team for daily updates
2. aggregate_responses - Compile into formatted summary
3. post_summary - Post to designated channel
4. schedule_reminder - Set recurring daily prompts

## Tools Required
- Slack Bot API (xoxb-* token)
- Cron scheduling
- Text formatting (Slack MRKDWN)

## Installation
1. `clawhub install slack-standup`
2. Configure Slack bot token
3. Set standup time (9:00 AM default)
4. Test: `/standup test`

## Pricing
- One-time: $25
- Subscription: $5/month
- Team: $50 (up to 10 members)
