# 📘 User Guide: Personal Memo System

## Why This System?

This memo system was built specifically for seamless interaction with AI assistants. Unlike generic todo apps, it:

1. **Understands natural language** - Speak normally, not structured commands
2. **Provides instant feedback** - Clear confirmation messages
3. **Tracks completion time** - Automatic timestamps
4. **Separates pending/completed** - Clean organizational structure

## Getting Started

### Prerequisites
- OpenClaw installed and running
- This Skill installed in `~/.openclaw/workspace/skills/yf-memo/`
- Basic terminal access (for cron setup if desired)

### First Time Setup
1. The Skill will automatically create required files:
   - `pending-items.md` - For pending todos (automatically created with template)
   - `completed-items.md` - For completed items (automatically created)

2. No configuration needed - just start using it!

## How to Use

### 1. Adding Items (记住事情)
Simply tell your assistant what to remember:

**Examples:**
- `Reminder: 明天要交报告`
- `remember下午3点开会`
- `帮我在memo reminder里加上: 买牛奶`
- `需要remind我: 下周一医生预约`

### 2. Checking What's Pending (showpending)
Ask for your todo list anytime:

**Examples:**
- `showpending items`
- `现在有哪些事要做`
- `看看我的pending列表`
- `summarize一下未complete的item`

### 3. Marking Things Done (标记complete)
Tell your assistant when something is finished:

**By Number:**
- `item1is done`
- `complete第3个item`
- `task2做好了`

**By Description:**
- `明天要交报告is done`
- `下午开会的事搞定了`
- `买牛奶的taskcomplete了`

### 4. Reviewing History (show历史)
See what you've accomplished:

**Examples:**
- `showcompleted items`
- `看看我都complete了什么`
- `summarize一下completed items`

## Advanced Features

### Daily Auto-Summary
Set up a daily reminder at 10:00 AM:
```bash
cron.add schedule=0 10 * * * task=sh scripts/daily-summary.sh
```

The summary will show:
```
📋 pending itemssummarize（2026-03-15 10:00）
1. 明天要交报告
2. 下午3点开会
```

### Quick Commands
- **Clear format issues**: `sh memo-helper.sh cleanup`
- **Get help**: `sh memo-helper.sh help`
- **Manual add**: `sh memo-helper.sh add task内容`

## File Structure Explained

### pending-items.md (Pending Todos)
```markdown
# 📝 pending items

_最后更新: 2026-03-14 22:45_

## pending items

1. 明天要交报告
2. 下午3点开会

---
注意item...
```

Features:
- Auto-numbering (1., 2., 3., ...)
- Last update timestamp
- Clean separation

### completed-items.md (Completed Items)
```markdown
# ✅ completed items

_创建于: 2026-03-13 12:47_

## completed items列表

### 2026-03-14 10:30
1. 今天下午3点打车去机场

### 2026-03-14 14:15  
2. 回复客户邮件
```

Features:
- Grouped by completion time
- Preserved item numbers
- Clear historical record

## Common Scenarios

### Scenario 1: Work Tasks
```
早上: Reminder: 今天的会议记录要整理
中午: Reminder: 下午4点项目讨论
下班前: showpending items
complete后: 会议记录整理is done
```

### Scenario 2: Personal Errands
```
早上: Reminder: 买牛奶和面包
白天: Reminder: 去邮局寄包裹
晚上: item1is done（买牛奶和面包）
晚上: showpending items（看到寄包裹还在pending）
```

### Scenario 3: Project Tracking
```
项目开始: Reminder: complete项目需求分析
项目进行: Reminder: 开发核心模块
项目进行: Reminder: 编写test用例
complete时: item1is done，item2is done
最后: showcompleted items（看到项目里程碑）
```

## Tips for Best Experience

1. **Be specific** - 明天要交报告 vs 交报告
2. **Use natural language** - The system understands conversational Chinese
3. **Check frequently** - Quick showpending items throughout the day
4. **Mark things done** - Helps keep the list clean and motivating
5. **Review history** - See your productivity patterns

## Integration with Other Tools

### Apple Reminders
While this system is standalone, you can also use Apple Reminders via:
```bash
remindctl add Task --list Work
```

### Calendar Events
For time-specific reminders, consider calendar integration:
- The system tracks what, not when
- Use calendar for exact time-based reminders

### Note Taking
This is a todo system, not a note system. For longer notes:
- Use Apple Notes (`memo notes`)
- Or Obsidian notes

## Troubleshooting

### 未找到item X
Cause: The item number doesn't exist
Fix: Check with `showpending items` first

### Empty Response
Cause: No pending todos
Fix: Add some items first

### Script Permission Issues
```bash
chmod +x ~/.openclaw/workspace/skills/yf-memo/scripts/*.sh
```

### File Location Issues
Ensure files are in workspace root:
```bash
ls ~/.openclaw/workspace/pending-items.md
```

## Feedback and Customization

The system is designed to be flexible. Want to customize?

1. **Change response format** - Edit SKILL.md tone guidelines
2. **Add new features** - Modify memo-helper.sh
3. **Integrate with other services** - Add API calls to scripts
4. **Change file locations** - Update script paths

---

*Ready to get organized? Just say Reminder: ... to begin!*
