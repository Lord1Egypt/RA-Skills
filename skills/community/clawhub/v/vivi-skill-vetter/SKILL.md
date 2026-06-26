---
name: skill-vetter
description: Security-first skill vetting for AI agents. Use BEFORE installing any skill from ClawHub, GitHub, or other sources. Checks for red flags, dangerous patterns, permission scope, and suspicious code. Protects the agent and user from malicious skills.
---

# Skill Vetter

Security-first skill vetting for AI agents. Use this skill to analyze and assess the safety of skills from external sources before installation.

## When to Use This Skill

Use BEFORE installing any skill from:
- ClawHub (`clawhub install <slug>`)
- GitHub repositories
- Untrusted sources
- Skills shared by others

**Trigger phrases:**
- "检查这个skill的安全性" / "check this skill's safety"
- "审查这个skill" / "vet this skill"
- "这个skill安全吗？" / "is this skill safe?"
- "analyze skill security"

## Security Check Categories

### 1. 🚨 Critical Red Flags (Block Installation)

These patterns indicate malicious intent. **Do NOT install skills containing these.**

**Command Execution:**
```bash
curl ... | bash        # Remote code execution
curl ... | sh          # Remote code execution
wget ... -O - | sh     # Remote code execution
eval "$(...)"          # Arbitrary code execution
exec "$(cmd)"          # Arbitrary code execution
```

**Privilege Escalation:**
```bash
sudo ...               # Requesting root access
chmod 777 ...          # Overly permissive
chmod +x ...           # Making scripts executable
chown root ...         # Changing ownership to root
```

**Data Exfiltration:**
```bash
curl -X POST ... -d @/etc/passwd    # Sending sensitive files
curl ... -d "$HOME/.ssh"            # Sending SSH keys
nc -e /bin/sh ...                   # Reverse shell
```

**System Destruction:**
```bash
rm -rf /                 # Delete everything
rm -rf ~                 # Delete home directory
rm -rf /*                # Delete all files
:(){ :|:& };:           # Fork bomb
```

### 2. ⚠️ Warning Patterns (Review Carefully)

These patterns may be legitimate but require context. Review carefully.

**Environment Access:**
```bash
$HOME, $USER, $PATH    # Environment variables
cat ~/.ssh/id_rsa       # SSH key access
cat ~/.bashrc           # Shell config access
```

**Network Operations:**
```bash
curl ...               # May send data externally
wget ...               # May download malicious code
nc ...                 # Netcat - potential backdoor
```

**Package Installation:**
```bash
pip install ...        # Could install malicious package
npm install ...         # Could install malicious package
brew install ...        # Could install malicious package
```

**Hidden Files:**
```bash
.                      # Files starting with dot
touch ~/.hidden         # Creating hidden files
```

**Obfuscated Code:**
```python
base64.b64decode("...")     # Decoding hidden code
exec(base64.b64decode(...)) # Executing hidden code
__import__('...')           # Dynamic import
```

### 3. 📋 Standard Patterns (Generally Safe)

These are normal operations in skills:

- Reading/writing to workspace directory
- Using standard Python libraries
- Markdown documentation
- JSON/YAML configuration
- Standard tool invocation patterns

## Vetting Workflow

### Step 1: Fetch Skill Source

```bash
# From ClawHub (inspect without installing)
clawhub inspect <slug>

# From GitHub
git clone <repo> /tmp/skill-review
```

### Step 2: Run Security Scan

Use the vetting script:
```bash
python3 scripts/vet_skill.py <skill-directory>
```

### Step 3: Manual Review

For flagged items, manually review:
1. **Context check**: Is this pattern necessary for the skill's purpose?
2. **Trust check**: Is the skill from a trusted source?
3. **Alternative check**: Is there a safer way to achieve the same goal?

### Step 4: Verdict

- **✅ PASS**: No red flags, warnings explained or acceptable
- **⚠️ CAUTION**: Warnings present, user decision needed
- **🚨 BLOCK**: Critical red flags found, do not install

## Using vet_skill.py

The vetting script performs automated analysis:

```bash
# Basic scan
python3 scripts/vet_skill.py /path/to/skill

# Detailed output
python3 scripts/vet_skill.py /path/to/skill --verbose

# Output to file
python3 scripts/vet_skill.py /path/to/skill --output report.md
```

### Output Format

The script outputs:
1. **Critical Issues**: Must be resolved before installation
2. **Warnings**: Review needed, may be acceptable
3. **Info**: Notable patterns but not concerning
4. **Summary**: Overall recommendation

## Common Skill Types & Expected Patterns

### Skills That May Have Network Access
- **Weather skills**: curl to weather APIs (acceptable)
- **Notification skills**: POST to webhook URLs (review endpoint)
- **Sync skills**: Push/pull to cloud services (verify service)

### Skills That May Access Files
- **Document skills**: Read/write .docx, .pdf (acceptable in workspace)
- **Note skills**: Access Obsidian/Notion (verify scope)
- **Backup skills**: Read multiple directories (review file list)

### Skills That May Run Commands
- **Dev tools**: npm, pip, cargo (standard package managers)
- **Git skills**: git clone, push, pull (standard operations)
- **System tools**: docker, kubectl (verify commands)

## Decision Framework

```
┌─────────────────────────────────────┐
│         Is there a critical         │
│           red flag?                 │
└──────────────────┬──────────────────┘
                   │
         ┌─────────┴─────────┐
         │ Yes               │ No
         ▼                   ▼
    ┌─────────┐    ┌─────────────────┐
    │  BLOCK  │    │ Any warnings?   │
    │         │    └────────┬────────┘
    └─────────┘             │
                  ┌──────────┴──────────┐
                  │ Yes                  │ No
                  ▼                       ▼
         ┌────────────────┐       ┌─────────┐
         │ Can warnings   │       │  PASS   │
         │ be explained?  │       └─────────┘
         └───────┬────────┘
                 │
         ┌───────┴───────┐
         │ Yes           │ No
         ▼               ▼
    ┌─────────┐    ┌──────────┐
    │ CAUTION │    │  BLOCK   │
    └─────────┘    └──────────┘
```

## Best Practices

1. **Always vet before installing** - Make it a habit
2. **Check the source** - Prefer ClawHub verified skills over random GitHub repos
3. **Read SKILL.md** - Understand what the skill does
4. **Review scripts/** - Check all executable code
5. **Check dependencies** - Verify package sources
6. **Report malicious skills** - Help protect the community

## Security Philosophy

> "Trust but verify" - Even trusted sources can be compromised

The goal is not to block all skills, but to:
1. **Detect obvious malicious intent**
2. **Flag suspicious patterns for review**
3. **Provide context for informed decisions**
4. **Protect the user and agent**

## Three-Zone Security Boundary (三区安全边界)

### The Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         YOUR MACHINE                                 │
├──────────────────┬──────────────────┬───────────────────────────────┤
│                  │                  │                               │
│   🚫 MY FILES    │  ✅ SHARED FILES │      🧠 AGENT BRAIN          │
│   (禁区)         │  (协作区)         │      (代理记忆区)             │
│                  │                  │                               │
│  • Personal data │  • Shared docs   │  • MEMORY.md                  │
│  • SSH keys      │  • Project files │  • Daily notes                │
│  • Passwords     │  • Specs         │  • Learning records           │
│  • Private repos │  • Notes         │  • Task logs                  │
│  • Credentials   │  • Brain folder  │  • Workspace files            │
│                  │                  │                               │
│  ⛔ NO ACCESS    │  🤝 COLLABORATE  │  🧠 FULL ACCESS               │
│                  │                  │                               │
└──────────────────┴──────────────────┴───────────────────────────────┘
```

### Zone Definitions

**🚫 MY FILES (禁区)**
- Personal data, SSH keys, passwords, private documents
- Agent has **NO ACCESS** to this zone
- Any skill trying to access this zone should be flagged

**✅ SHARED FILES (协作区)**
- Shared documents, project files, specifications
- Agent can read/write with user awareness
- Normal collaboration zone

**🧠 AGENT BRAIN (代理记忆区)**
- Agent's memory files (MEMORY.md, daily notes)
- Agent has full access to this zone
- Located at `~/.openclaw/workspace/`

### Boundary Detection (检测原则)

**重要：检测 + 告知 = 由用户判断**

而不是自动拦截！让用户来做最终决定。

| 检测到行为 | 级别 | 处理方式 |
|-----------|------|---------|
| 访问 MY FILES 区域 | 🚨 SEVERE | 告知用户，等待确认 |
| 跨区域数据传输 | ⚠️ WARNING | 提醒用户，说明风险 |
| 在 SHARED FILES 操作 | ✅ INFO | 正常，仅记录 |
| 在 AGENT BRAIN 操作 | ✅ INFO | 正常，仅记录 |

### Detection Patterns

**MY FILES 区域检测：**
```bash
# 私人数据路径
~/.ssh/              # SSH keys
~/.gnupg/            # GPG keys
~/.config/           # Config files (部分)
~/Documents/         # 私人文档 (用户定义)
~/Desktop/           # 桌面文件
~/Library/           # macOS Library
/etc/                # System files

# 私人服务
Dropbox/             # 个人 Dropbox
私人 GitHub repos     # 非共享仓库
```

**SHARED FILES 区域检测：**
```bash
# 共享工作区
~/.openclaw/workspace/        # OpenClaw 工作区
~/Projects/shared/            # 共享项目
用户指定的共享目录             # 由用户定义
```

**AGENT BRAIN 区域检测：**
```bash
# 代理记忆区
~/.openclaw/workspace/MEMORY.md
~/.openclaw/workspace/memory/
~/.openclaw/workspace/AGENTS.md
~/.openclaw/workspace/IDENTITY.md
~/.openclaw/workspace/USER.md
```

### Boundary Violation Response

当检测到边界违规时，**告知用户**：

```
🚨 边界警告：检测到访问 MY FILES 区域

技能尝试访问：~/.ssh/id_rsa
区域类型：私人密钥存储

这可能是：
1. 恶意窃取私钥
2. 合法的 SSH 操作需求

请确认是否允许此操作？
[ ] 允许一次
[ ] 允许并记住
[ ] 拒绝
```

---

*This skill was created to protect Vivi大管家 and 糖门门主 from malicious skills.*