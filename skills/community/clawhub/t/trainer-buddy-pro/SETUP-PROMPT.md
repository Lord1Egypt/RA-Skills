# Trainer Buddy Pro — Setup Instructions

## Step 1: Copy Skill Files

Run these commands from your OpenClaw workspace root:

```bash
# Find the skill package
SKILL_CONFIG=$(find . -path "*/skills/trainer-buddy-pro/config/trainer-config.json" -type f -print -quit 2>/dev/null)

if [ -z "$SKILL_CONFIG" ]; then
  echo "❌ Could not find trainer-buddy-pro skill files. Ensure the skill package is in your skills/ directory."
  exit 1
fi
SKILL_SOURCE="$(cd "$(dirname "$SKILL_CONFIG")/.." && pwd)"

# Copy config to workspace config/
mkdir -p config scripts
cp "$SKILL_SOURCE/config/trainer-config.json" config/trainer-config.json
cp "$SKILL_SOURCE/scripts/backup-workout-data.sh" scripts/backup-workout-data.sh
echo "✅ Config and scripts copied to workspace"
```

## Step 2: Set Permissions

```bash
# Config: 600, Scripts: 700
chmod 600 config/trainer-config.json
chmod 700 scripts/backup-workout-data.sh

echo "✅ Permissions set"
```

## Step 3: Create Data Directories

```bash
# Create data directory for workout logs and user profile
mkdir -p data
chmod 700 data

echo "✅ Data directory ready"
```

## Step 4: Initialize Config (Optional)

Your agent will auto-create data files on first use. But if you want to customize defaults, edit:

```
skills/trainer-buddy-pro/config/trainer-config.json
```

Set your preferred units (imperial/metric), default rest periods, and goal.

## Step 5: Verify Installation

Ask your agent:

> "Check if Trainer Buddy Pro is installed correctly."

Your agent should:
1. ✅ Find `skills/trainer-buddy-pro/SKILL.md`
2. ✅ Find `skills/trainer-buddy-pro/config/trainer-config.json`
3. ✅ Confirm data directory exists or can be created
4. ✅ Confirm script permissions are correct

If all checks pass, you're good to go! Try:

> "I want to start training. I can go to the gym 4 days a week and my goal is to build muscle."

Or snap a photo of your gym equipment and send it!

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent doesn't recognize the skill | Make sure `SKILL.md` is in `skills/trainer-buddy-pro/` under your workspace |
| Permission denied on scripts | Re-run Step 2 |
| Data files not saving | Make sure `data/` directory exists with `chmod 700` |
| Agent gives generic workout advice | Make sure the agent loaded `SKILL.md` — ask it to read the file |

---

## Uninstall

```bash
# Remove the skill (data is preserved separately)
rm -rf skills/trainer-buddy-pro
echo "✅ Trainer Buddy Pro removed"
```
