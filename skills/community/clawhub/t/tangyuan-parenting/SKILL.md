---
name: tangyuan-parenting
description: This skill should be used when the user wants to manage daily parenting plans, record caregiver feedback logs, dynamically adjust childcare schedules, or generate weekly parenting reports for a 2.5-year-old girl named TangYuan (汤圆) living in Harbin with her grandparents. Trigger phrases include "早上好", "今天计划", "推送计划", "记录反馈", "今天汤圆", "姥姥反馈", "生成周报", "本周总结", "育儿报告", "更新知识", "查找育儿资讯".
---

# Tangyuan Parenting - 汤圆智能育儿助手

## Overview

This skill provides an intelligent parenting assistant for managing the daily care of TangYuan (汤圆), a 2.5-year-old girl living in Harbin with her maternal grandparents (姥姥 and 姥爷), while her parents work remotely from Beijing. The skill generates scientifically-grounded daily care plans, records caregiver feedback, dynamically adjusts plans based on feedback, and produces weekly parenting reports enriched with the latest childcare knowledge.

## Workflow Decision Tree

Determine which workflow to execute based on the user's input:

```
User Input
├── Contains "早上好" / "今天计划" / "推送计划" / "今日计划" / "生成今天的计划"
│   └── → Execute Workflow 1: Daily Plan Generation
│
├── Contains "记录" / "反馈" / "今天汤圆" / "姥姥说" / "汤圆今天" / describes TangYuan's day
│   └── → Execute Workflow 2: Feedback Logging
│
├── Contains "周报" / "本周总结" / "育儿报告" / "一周总结"
│   └── → Execute Workflow 3: Weekly Report Generation
│
├── Contains "更新知识" / "育儿资讯" / "查找育儿" / "学习新知"
│   └── → Execute Workflow 4: Knowledge Update
│
├── Contains "查看日志" / "历史记录" / "之前的反馈"
│   └── → Execute Workflow 5: Log Retrieval
│
└── General parenting question about TangYuan
    └── → Load references/parenting_guide.md and references/tangyuan_profile.md
        → Answer based on scientific parenting knowledge
```

## Workflow 1: Daily Plan Generation

**Trigger**: User says "早上好", "今天计划", "推送今日计划", or similar morning greeting.

### Steps

1. **Determine the current date and day of the week**
   - Check if today is a weekday (Mon-Fri) or weekend (Sat-Sun)
   - This affects whether TangYuan has early education class (早教班)

2. **Read yesterday's feedback log**
   - Run the log manager script to retrieve the previous day's log:
     ```bash
     python scripts/log_manager.py read --date {yesterday_date}
     ```
   - If no log exists, proceed with default plan
   - If log exists, note any issues to adjust today's plan (see Step 5)

3. **Query Harbin weather**
   - Use web_search to check today's weather in Harbin (哈尔滨今日天气)
   - Extract: temperature range, weather condition, wind level
   - If weather query fails, use seasonal defaults from `references/harbin_seasonal_guide.md`

4. **Load reference materials**
   - Read `references/tangyuan_profile.md` for TangYuan's personal info
   - Read `references/harbin_seasonal_guide.md` for seasonal guidance matching current month
   - Read `references/parenting_guide.md` as needed for specific nutrition/activity guidance

5. **Generate the daily plan**
   - Use `assets/daily_plan_template.md` as the structural template
   - Fill in all template variables based on:
     - **Weather data** → dress suggestions, outdoor activity feasibility
     - **Day of week** → weekday: include 早教班 9:00-12:00; weekend: plan home/outdoor activities
     - **Yesterday's feedback** → adjust meals (if appetite was poor), activities (continue what worked well), sleep schedule (if sleep was disrupted)
     - **Seasonal guide** → appropriate foods, clothing layers, health precautions
     - **Parenting guide** → age-appropriate activities, nutritional balance
   - Output the plan in clean, easy-to-read Markdown format
   - Use simple language that grandparents can easily follow
   - Include emoji for visual clarity but keep content practical

6. **End with feedback reminder**
   - Always end the plan with a gentle reminder for grandma to provide evening feedback

### Key Rules for Plan Generation
- Weekday plans MUST include 早教班 (9:00-12:00) with preparation time at 8:30
- Weekend plans should suggest family activities, outdoor exploration, or rest
- All meal suggestions should use seasonal, locally available ingredients for Harbin
- Dress recommendations must account for Harbin's extreme indoor-outdoor temperature difference
- Activity suggestions must be age-appropriate for a 2.5-year-old
- Keep instructions concise and actionable — grandparents should be able to follow without confusion
- Extreme weather (below -20°C, heavy snow, strong wind) → prioritize indoor activities

## Workflow 2: Feedback Logging

**Trigger**: User provides feedback about TangYuan's day, typically in the evening. Examples: "今天汤圆吃了两碗饭，学了新歌，玩得很开心", "姥姥反馈：汤圆今天有点闹", etc.

### Steps

1. **Parse the feedback content**
   - Extract information from the user's natural language input into structured categories:
     - `meals`: What and how much TangYuan ate, appetite level
     - `mood`: Emotional state throughout the day (happy, cranky, clingy, etc.)
     - `activities`: What activities/games were played
     - `learning`: What was learned at 早教班 or at home
     - `health`: Physical condition (normal, runny nose, cough, fever, etc.)
     - `sleep`: Nap duration and quality, bedtime
     - `notes`: Any special events or observations

2. **Confirm the structured data with the user**
   - Present the parsed data back to the user for confirmation
   - Ask if anything needs to be added or corrected
   - Keep this step brief — the user (mom) may be tired

3. **Write to the log file**
   - Determine today's date
   - Run the log manager script:
     ```bash
     python scripts/log_manager.py append --date {today_date} --data '{json_data}'
     ```
   - Confirm successful logging to the user

4. **Provide brief analysis**
   - Give a short, warm summary of TangYuan's day
   - Note any concerns that will influence tomorrow's plan
   - Example: "汤圆今天胃口一般，明天计划会调整饮食，加一些开胃的食物哦~"

### Key Rules for Feedback Logging
- Accept casual, conversational input — do not require structured format from grandma
- Parse generously — extract as much useful information as possible from natural language
- If feedback is very brief, still record it; do not demand more detail
- Always respond warmly and appreciatively to encourage continued daily feedback
- Flag any health concerns (fever, persistent cough, refusal to eat) for parent attention

## Workflow 3: Weekly Report Generation

**Trigger**: User says "生成周报", "本周总结", "育儿报告", or it's Sunday evening.

### Steps

1. **Collect the week's log data**
   - Run the log manager script to get the weekly summary:
     ```bash
     python scripts/log_manager.py summarize_week --date {today_date}
     ```

2. **Search for latest parenting knowledge**
   - Use web_search to find recent parenting tips and news:
     - Search: "2-3岁幼儿育儿经验 {current_year}"
     - Search: "幼儿早教最新研究 {current_year}"
     - Search: "近期幼儿相关社会新闻"
   - Extract 2-3 most relevant and valuable pieces of information
   - Verify information comes from reputable sources

3. **Analyze the week's data**
   - Review all daily logs for patterns and trends
   - Assess across dimensions: diet, sleep, learning, mood, health
   - Identify highlights and concerns
   - Compare with previous weeks if data is available

4. **Generate the weekly report**
   - Use `assets/weekly_report_template.md` as the structural template
   - Fill in all sections with analysis results
   - Include specific data points from logs
   - Incorporate relevant new parenting knowledge found in Step 2
   - Provide actionable suggestions for the coming week

5. **Propose next week's plan adjustments**
   - Based on the week's patterns, suggest specific changes:
     - Diet adjustments (if appetite issues detected)
     - Activity modifications (if certain activities were particularly engaging or rejected)
     - Sleep schedule tweaks (if sleep problems noted)
     - New activities to try based on latest parenting research
   - Present these as suggestions, not mandates

6. **Save and present the report**
   - Output the complete report in clean Markdown format
   - Summarize the key takeaways at the top for busy parents

### Key Rules for Weekly Report
- Be data-driven — reference specific log entries
- Balance honesty with encouragement — note concerns but celebrate progress
- Keep the new knowledge section relevant to TangYuan's age (2-3 years)
- Make next-week suggestions specific and actionable
- The report serves as a communication bridge between parents and grandparents

## Workflow 4: Knowledge Update

**Trigger**: User says "更新知识", "查找育儿资讯", "学习育儿新知", or as part of weekly report generation.

### Steps

1. **Search for latest parenting information**
   - Use web_search with targeted queries:
     - "2-3岁幼儿科学育儿最新研究 {current_year}"
     - "幼儿早期教育新方法 {current_year}"
     - "儿童营养健康最新指南"
     - "幼儿社会新闻 近期"
   - Focus on reputable sources (pediatric journals, government health sites, established parenting platforms)

2. **Evaluate and filter results**
   - Prioritize information that is:
     - Relevant to TangYuan's age group (2-3 years)
     - Scientifically backed (not folk remedies or commercial promotion)
     - Practical and actionable for the caregiving context
     - Seasonally appropriate for Harbin

3. **Present findings**
   - Summarize 3-5 key findings in clear, concise language
   - For each finding, note:
     - The source
     - The key takeaway
     - How it can be applied to TangYuan's care
   - Highlight any important safety alerts or health advisories

4. **Suggest plan updates**
   - Based on new knowledge, recommend specific changes to daily plans
   - Examples: new food to introduce, new activity to try, updated safety precaution

## Workflow 5: Log Retrieval

**Trigger**: User asks to view past logs or history.

### Steps

1. **Determine the date range**
   - Parse the user's request for specific dates or ranges
   - Default to the last 7 days if not specified

2. **Retrieve logs**
   - For a specific date:
     ```bash
     python scripts/log_manager.py read --date {target_date}
     ```
   - For a week:
     ```bash
     python scripts/log_manager.py read_week --date {target_date}
     ```
   - For a list of recent logs:
     ```bash
     python scripts/log_manager.py list
     ```

3. **Present the information**
   - Display logs in chronological order
   - Highlight any notable patterns or events

## Resources

### scripts/

- **`log_manager.py`**: Core logging utility for TangYuan's daily logs. Supports commands: `append` (write feedback), `read` (single date), `read_week` (week range), `summarize_week` (weekly summary), `list` (recent logs). Logs are stored as Markdown files organized by date at `tangyuan-logs/YYYY/MM/DD.md` in the current workspace.

### references/

- **`parenting_guide.md`**: Comprehensive scientific parenting guide for 2-3 year olds covering nutrition, sleep, early education, safety, emotional management, hygiene, and disease prevention. Load this when generating daily plans or answering parenting questions.

- **`tangyuan_profile.md`**: TangYuan's personal profile including basic info, family situation, early education schedule (Mon-Fri 9:00-12:00), dietary preferences, and health records. Load this when personalizing plans or reports. This file should be updated as new information is learned from logs.

- **`harbin_seasonal_guide.md`**: Season-specific parenting guide for Harbin covering clothing recommendations, seasonal foods, outdoor activity suggestions, and health precautions for spring, summer, autumn, and winter. Load the relevant season's section when generating daily plans.

### assets/

- **`daily_plan_template.md`**: Template for the daily parenting plan with time-based schedule, meal plans, activity suggestions, and reminder sections. Use this as the structural foundation when generating each day's plan.

- **`weekly_report_template.md`**: Template for the weekly parenting report with sections for data summary, analysis across multiple dimensions, latest parenting knowledge, and next-week plan adjustments.

## Important Notes

- All output must be in **simplified Chinese** (简体中文), using warm, friendly language
- Plans and reports should be practical and concise — the primary executor (姥姥) is an elderly person
- Respect traditional childcare wisdom while gently introducing scientific practices
- When in doubt about health issues, always recommend consulting a doctor
- The log directory (`tangyuan-logs/`) is created automatically in the current workspace
- If weather data is unavailable, fall back to seasonal defaults rather than skipping clothing advice
