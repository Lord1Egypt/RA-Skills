# Hook: Personal Memo System

This hook sets up the personal memo system when an OpenClaw session starts.

## What It Does

1. **Creates required files** - If pending-items.md and completed-items.md don't exist
2. **Ensure script permissions** - Makes sure scripts are executable
3. **Sets up cron job** - Optionally configures daily summary at 10:00 AM

## Installation

Users can install this hook to auto-setup the memo system:

```bash
# Copy hook to OpenClaw hooks directory
mkdir -p ~/.openclaw/hooks/yf-memo
cp -r hooks/openclaw/* ~/.openclaw/hooks/yf-memo/
```

## Hook Script

```bash
#!/bin/bash
# Hook script for personal memo system setup

WORKSPACE_DIR=$HOME/.openclaw/workspace
SKILL_DIR=$HOME/.openclaw/skills/yf-memo

echo 🔧 Setting up Personal Memo System...

# Check if required files exist
if [ ! -f $WORKSPACE_DIR/pending-items.md ]; then
    echo   Creating pending-items.md...
    cp $SKILL_DIR/assets/template-todo.md $WORKSPACE_DIR/pending-items.md
    sed -i '' s/{timestamp}/$(date '+%Y-%m-%d %H:%M')/g $WORKSPACE_DIR/pending-items.md
fi

if [ ! -f $WORKSPACE_DIR/completed-items.md ]; then
    echo   Creating completed-items.md...
    cp $SKILL_DIR/assets/template-done.md $WORKSPACE_DIR/completed-items.md
    sed -i '' s/{timestamp}/$(date '+%Y-%m-%d %H:%M')/g $WORKSPACE_DIR/completed-items.md
fi

# Ensure scripts directory exists
mkdir -p $WORKSPACE_DIR/scripts

# Copy scripts if not present
if [ ! -f $WORKSPACE_DIR/scripts/memo-helper.sh ]; then
    echo   Installing memo-helper.sh...
    cp $SKILL_DIR/scripts/memo-helper.sh $WORKSPACE_DIR/scripts/
    chmod +x $WORKSPACE_DIR/scripts/memo-helper.sh
fi

if [ ! -f $WORKSPACE_DIR/scripts/daily-summary.sh ]; then
    echo   Installing daily-summary.sh...
    cp $SKILL_DIR/scripts/daily-summary.sh $WORKSPACE_DIR/scripts/
    chmod +x $WORKSPACE_DIR/scripts/daily-summary.sh
fi

echo ✅ Personal Memo System setup complete!
```

## Auto-Setup Option

The hook can be configured to:
1. **Ask user** if they want to setup memo system
2. **Auto-setup** silently if files are missing
3. **Skip** if already configured

## Integration with Cron Setup

Optional: Ask user about daily summary
```bash
read -p Set up daily 10:00 AM todo summary? (y/n):  answer
if [[ $answer =~ ^[Yy]$ ]]; then
    cron.add schedule=0 10 * * * task=cd $WORKSPACE_DIR && sh scripts/daily-summary.sh
fi
```

## Post-Setup Message

After setup, the hook can show a welcome message:
```
🗂️ Personal Memo System Ready!

Commands:
• Reminder: <内容>      - Add new todo
• showpending items           - Show pending todos  
• itemXis done             - Mark item complete
• showcompleted items           - Show completed items

Try: Reminder: testmemo reminder系统
```