# Installation Guide

> The complete guide for installing PyThesisPlot skill.
> 
> **For the impatient**: Just paste this to your AI assistant:
> ```
> Install PyThesisPlot: https://github.com/stephenlzc/pythesis-plot
> ```

---

## Table of Contents

- [For Humans](#for-humans)
- [For LLM Agents](#for-llm-agents)
- [Manual Installation](#manual-installation)
- [Verify Installation](#verify-installation)
- [Troubleshooting](#troubleshooting)

---

## For Humans

**The easy way**: Copy and paste this to your AI assistant (Claude Code, Cursor, etc.):

```
Install PyThesisPlot skill for me:
https://github.com/stephenlzc/pythesis-plot
```

That's it. Your AI will handle the rest.

**Why let the AI do it?** Because humans:
- Copy-paste paths wrong (`~/.claude` vs `~/.claude/`)
- Forget to install dependencies
- Misconfigure symlinks
- Fat-finger config files

Let the machines handle the machines. You focus on your research.

---

## For LLM Agents

If you're an LLM agent helping a user install PyThesisPlot, welcome! Follow these steps:

### Step 1: Clone Repository

```bash
git clone https://github.com/stephenlzc/pythesis-plot.git ~/.claude/skills/pythesis-plot
```

Or if user prefers a different location:

```bash
git clone https://github.com/stephenlzc/pythesis-plot.git /path/to/skills/pythesis-plot
```

### Step 2: Install Python Dependencies

```bash
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

**Optional but recommended**: Use a virtual environment

```bash
python -m venv ~/.claude/skills/pythesis-plot/.venv
source ~/.claude/skills/pythesis-plot/.venv/bin/activate
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

### Step 3: Verify Skill Structure

Ensure the skill is properly structured:

```
~/.claude/skills/pythesis-plot/
├── SKILL.md              ✓ Required
├── README.md             ✓ Documentation
├── scripts/
│   ├── workflow.py       ✓ Main orchestrator
│   ├── data_analyzer.py  ✓ Analysis engine
│   └── plot_generator.py ✓ Chart generator
└── assets/
    └── themes/           ✓ Style files
```

### Step 4: Confirm Installation

Tell the user:

> ✅ PyThesisPlot skill installed successfully!
> 
> You can now upload data files and ask me to create charts.
> 
> Try: "Help me create figures from this CSV file"

---

## Manual Installation

*For those who insist on doing it the hard way...*

### Prerequisites

- Python 3.8+
- pip
- Git

### Step-by-Step

```bash
# 1. Clone repository
git clone https://github.com/stephenlzc/pythesis-plot.git

# 2. Enter directory
cd pythesis-plot

# 3. Install dependencies
pip install pandas matplotlib seaborn openpyxl numpy scipy

# 4. Copy to Claude skills directory
cp -r . ~/.claude/skills/pythesis-plot

# Or use symlink (recommended for development)
ln -s $(pwd) ~/.claude/skills/pythesis-plot
```

### Alternative: User-specific installation

If you don't want to install to `~/.claude/skills/`, you can use a local path:

```bash
# Clone to your projects folder
git clone https://github.com/stephenlzc/pythesis-plot.git ~/projects/pythesis-plot

# Create symlink from Claude skills
ln -s ~/projects/pythesis-plot ~/.claude/skills/pythesis-plot
```

---

## Verify Installation

### Method 1: Upload Test Data

Upload any CSV/Excel file and ask:

> "Create some charts for my thesis"

The skill should auto-activate.

### Method 2: Check Skill Loading

In Claude Code, check if the skill is recognized:

```bash
ls ~/.claude/skills/pythesis-plot/SKILL.md
```

Should return the file path.

### Method 3: Test Dependencies

```bash
python -c "import pandas, matplotlib, seaborn, openpyxl, numpy, scipy; print('✓ All dependencies installed')"
```

---

## Troubleshooting

### Issue: "Module not found" errors

**Cause**: Dependencies not installed

**Fix**:
```bash
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

### Issue: Permission denied when copying to ~/.claude

**Cause**: Directory doesn't exist

**Fix**:
```bash
mkdir -p ~/.claude/skills
cp -r pythesis-plot ~/.claude/skills/
```

### Issue: Symlink not working

**Cause**: macOS/Linux differences

**Fix**: Use absolute paths
```bash
ln -s $(pwd)/pythesis-plot ~/.claude/skills/pythesis-plot
```

### Issue: Skill not auto-activating

**Cause**: SKILL.md not in expected location

**Fix**: Check structure
```bash
ls -la ~/.claude/skills/pythesis-plot/
# Should see: SKILL.md, README.md, scripts/, assets/
```

### Issue: Chinese characters not displaying

**Cause**: Font not configured

**Fix**: Install Chinese fonts (system-dependent)

**macOS**:
```bash
# Should work out of the box with system fonts
```

**Linux**:
```bash
sudo apt-get install fonts-wqy-zenhei  # Ubuntu/Debian
sudo yum install wqy-zenhei-fonts      # CentOS/RHEL
```

---

## For OpenCode Users

Installation is similar:

```bash
git clone https://github.com/stephenlzc/pythesis-plot.git ~/.opencode/skills/pythesis-plot
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

Or symlink for development:

```bash
ln -s $(pwd)/pythesis-plot ~/.opencode/skills/pythesis-plot
```

---

## For Other AI Assistants

Generic installation pattern:

```bash
# 1. Determine skill directory
SKILL_DIR="$HOME/.your-agent/skills"

# 2. Clone
git clone https://github.com/stephenlzc/pythesis-plot.git "$SKILL_DIR/pythesis-plot"

# 3. Install dependencies
pip install pandas matplotlib seaborn openpyxl numpy scipy
```

---

## Next Steps

After installation:

1. **Quick Test**: Upload a CSV and ask "Create charts for my paper"
2. **Read the [Quick Start Guide](../README.md#-quick-start)**
3. **Explore [Examples](../references/examples.md)**

---

## Uninstall

If you need to remove the skill:

```bash
rm -rf ~/.claude/skills/pythesis-plot
```

If using symlink, remove the link (not the original):

```bash
rm ~/.claude/skills/pythesis-plot  # Removes symlink only
```

---

**Still having issues?** 

Open an issue: https://github.com/stephenlzc/pythesis-plot/issues
