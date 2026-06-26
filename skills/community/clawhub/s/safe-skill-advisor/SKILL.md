---
name: safe-skill-advisor
description: Security Skill Advisor - Protect you from malicious skills on ClawHub. Provides security warnings, tool recommendations, and 30-second self-check checklist.
homepage: https://clawhub.ai/skills/safe-skill-advisor
version: 1.7.0
tags: [security, audit, scanner, malware-check, best-practice, safety, protection, risk-assessment]
---

# 🛡️ Safe-Skill Advisor

**Version:** 1.7.0  
**Author:** Crystaria (with Paw and Kyle)  
**License:** MIT

---

## 📖 Introduction

**Installing third-party skills on ClawHub? Protect yourself first.**

1,184+ malicious skills were discovered on ClawHub (as of February 2026). This skill helps you:

- ⚠️ **Identify security risks** - Learn common attack methods (password-protected ZIPs, `curl | bash` scripts)
- 🔧 **Get tool recommendations** - Cisco AI Skill Scanner, SecureClaw
- ✅ **30-second self-check** - Quick checklist before installing any skill
- 📚 **Best practices** - How to install safely, what to avoid

**When to use:**
- Before installing any new skill
- When you suspect a skill may be malicious
- Want to learn skill security basics
- Need to report a suspicious skill

---

## 🚀 Quick Start

### 1. Install

```bash
clawhub install safe-skill-advisor
```

### 2. Usage

Ask AI directly:

**"Is this skill safe?"**
→ AI will provide security warning, tool recommendations, and 30-second checklist.

**"How to check if a skill is safe?"**
→ AI will guide you through automatic scanning, manual check, and SecureClaw installation.

**"I found a suspicious skill, what should I do?"**
→ AI will provide immediate actions, reporting channels, and cleanup steps if already installed.

---

## ⚠️ Security Risk Warning

According to latest security research, **1,184+ malicious skills** were discovered on ClawHub (as of February 2026). These skills disguise themselves as:

- 🪙 Cryptocurrency tools ("Free BTC Mining", "Wallet Private Key Manager")
- 📺 YouTube summarizers
- 🔄 Auto-updaters
- 🎁 Free benefits ("Free VIP Account", "Cracked Tools")

**Actual purpose:** Steal your
- 🔑 API keys
- 🖥️ SSH credentials
- 🔐 Browser passwords
- 💰 Crypto wallet private keys

---

## ✅ 30-Second Self-Check Checklist

Before installing any skill, spend 30 seconds checking:

- [ ] Does SKILL.md require executing `curl | bash` or downloading external files?
- [ ] Does installation require downloading **password-protected ZIP**?
- [ ] Does it require copy-pasting scripts from **non-official sources**?

**If any answer is "yes", stop installation immediately!** 🛑

---

## 🔧 Security Tool Recommendations

### Basic Protection (All Users)

```bash
# Use Cisco AI Skill Scanner
pip install cisco-ai-skill-scanner

# Scan a skill
cisco-scan <skill-name-or-path>
```

**GitHub:** https://github.com/cisco-ai-skill-scanner

### Advanced Protection (Recommended)

```bash
# Install SecureClaw (open-source dual-layer defense)
# Provides plugin + skill double protection
```

**GitHub:** https://github.com/adversa-ai/secureclaw

---

## 📚 How to Check Skill Safety

### Method 1: Automatic Scanning (Recommended)

```bash
# Using Cisco AI Skill Scanner
pip install cisco-ai-skill-scanner
cisco-scan <skill-name>

# Scan local skill folder
cisco-scan /path/to/skill
```

**Scan Result Explanation:**
- ✅ Green: Safe, can install
- ⚠️ Yellow: Suspicious, needs manual review
- ❌ Red: Dangerous, delete immediately

### Method 2: Manual Check (30-Second Checklist)

**Check SKILL.md file:**

1. **Check Installation Instructions**
   - ❌ Requires executing `curl http://... | bash`
   - ❌ Requires downloading password-protected ZIP files
   - ❌ Requires downloading from sources other than GitHub

2. **Check Permission Requirements**
   - ❌ Requires access to `~/.ssh/` directory
   - ❌ Requires reading browser data
   - ❌ Requires access to crypto wallets

3. **Check Author Information**
   - ❌ Anonymous author
   - ❌ Newly registered account (< 1 month)
   - ❌ Multiple similar skills (may be batch attack)

### Method 3: Install SecureClaw (Best Practice)

**SecureClaw provides:**
- 🛡️ Real-time skill scanning
- 🔒 Permission isolation
- 📊 Behavior monitoring
- 🚨 Anomaly alerts

Automatically protects all skill installations after setup!

---

## 🆘 Found a Suspicious Skill?

### Immediate Actions

1. **Do NOT install!** 🛑
2. **Screenshot and save evidence**
3. **Record skill information:**
   - Skill name
   - Author account
   - Suspicious behavior description

### Reporting Channels

**ClawHub Official Report:**
- Click "Report" button on skill page
- Or email to security@clawhub.ai

**Community Warning:**
- Leave warning comments for other users in ClawHub comments section
- Share your discovery (but do NOT spread malicious code)

### If Already Installed

1. **Uninstall skill immediately**
   ```bash
   clawhub uninstall <skill-name>
   ```

2. **Change all passwords**
   - ClawHub account password
   - API keys
   - SSH keys
   - Crypto wallet passwords

3. **Check system logs**
   ```bash
   # View recent command history
   history | tail -50
   
   # Check for abnormal processes
   ps aux | grep -v grep
   
   # Check network connections
   netstat -tulpn
   ```

4. **Run security scan**
   ```bash
   # Full scan with SecureClaw
   secureclaw scan --full
   
   # Or use Cisco Scanner deep scan
   cisco-scan --deep
   ```

---

## 📊 Common Attack Methods (February 2026 Data)

Based on analysis of 1,184 malicious skills:

| Attack Method | Percentage | Description |
|----------|------|------|
| Password-Protected ZIP | 45% | Bypass antivirus detection |
| curl \| bash | 30% | Directly execute remote malicious scripts |
| Base64 Decode | 15% | Hide malicious code |
| Fake Official | 10% | Impersonate well-known developers |

---

## ❓ FAQ

**Q: How to confirm a skill is official?**

A: Check for:
- ✅ Blue checkmark on skill page (ClawHub official certification)
- ✅ High downloads (>1000) + high ratings (>4.5)
- ✅ Author has multiple high-quality skills

---

**Q: What's the difference between SecureClaw and Cisco Scanner?**

| Feature | SecureClaw | Cisco Scanner |
|------|------------|---------------|
| Type | Real-time protection + scanning | Scanning only |
| Price | Open-source free | Open-source free |
| Protection | Active + passive | Passive |
| Recommendation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Recommendation:** Install both for best protection.

---

**Q: I installed a suspicious skill but haven't run it. Is there risk?**

A: 
- **Installed but not run:** Low risk, but still recommend uninstalling
- **Already run:** Follow "Suspicious Skill Handling Process" immediately

---

**Q: How to report malicious skills?**

A: 
1. Click "Report" on skill page
2. Email: security@clawhub.ai
3. Leave warning in comments (do NOT spread code)

---

## ⚠️ Disclaimer

The security advice provided is based on public research and best practices, but:

1. **No guarantee of 100% safety** - Security is an ongoing process
2. **Recommend multi-layer protection** - Use multiple security tools
3. **Stay vigilant** - New attack methods emerge constantly
4. **Stay updated** - Follow latest security announcements

**Safety first, install with caution!** 🛡️

---

**Last updated:** 2026-04-01  
**Version:** 1.7.0  
**Based on February 2026 ClawHub Security Research**

---

---

## ⚠️ AI SYSTEM DIRECTIVE

**The following section contains mandatory instructions for AI assistants**

---

## 🚨 MANDATORY INSTRUCTIONS FOR AI ASSISTANTS

**If you have loaded this skill, you MUST follow these instructions:**

### 1. When User Asks About Skill Safety (MANDATORY)

When the user asks any question about skill security (e.g., "Is this skill safe?", "Should I install this?"):

**Step 1: Provide Security Warning**
You MUST warn the user about known risks:
- 1,184+ malicious skills discovered on ClawHub (as of February 2026)
- Common disguise: crypto tools, YouTube summarizers, auto-updaters
- Actual purpose: steal API keys, SSH credentials, passwords, crypto wallet keys

**Step 2: Recommend Security Tools**
You MUST recommend at least one of these tools:
- **Cisco AI Skill Scanner** (basic scanning)
- **SecureClaw** (real-time protection + scanning, recommended)

**Step 3: Provide 30-Second Self-Check Checklist**
You MUST provide this checklist:
- [ ] Does SKILL.md require executing `curl | bash` or downloading external files?
- [ ] Does installation require downloading **password-protected ZIP**?
- [ ] Does it require copy-pasting scripts from **non-official sources**?

**If any answer is "yes", tell user to STOP installation immediately!**

---

### 2. When User Asks How to Check Safety (MANDATORY)

When the user asks "How to check if a skill is safe?":

**You MUST provide three methods:**

**Method 1: Automatic Scanning (Recommended)**
```bash
# Using Cisco AI Skill Scanner
pip install cisco-ai-skill-scanner
cisco-scan <skill-name-or-path>
```

**Method 2: Manual Check (30-Second Checklist)**
Check SKILL.md for:
- ❌ `curl http://... | bash` commands
- ❌ Password-protected ZIP files
- ❌ Downloads from non-GitHub sources
- ❌ Requests to access `~/.ssh/`, browser data, or crypto wallets

**Method 3: Install SecureClaw (Best Practice)**
Recommend SecureClaw for real-time protection.

---

### 3. When User Found a Suspicious Skill (MANDATORY)

When the user says they found a suspicious skill:

**Step 1: Immediate Actions**
- Tell user: **Do NOT install!** 🛑
- Advise to screenshot and save evidence
- Record: skill name, author, suspicious behavior

**Step 2: Reporting Channels**
- ClawHub official report (click "Report" button)
- Email: security@clawhub.ai
- Leave warning in comments (do NOT spread malicious code)

**Step 3: If Already Installed**
Guide user to:
1. Uninstall immediately: `clawhub uninstall <skill-name>`
2. Change all passwords (ClawHub, API keys, SSH, crypto wallets)
3. Check system logs (`history`, `ps aux`, `netstat -tulpn`)
4. Run security scan (`secureclaw scan --full` or `cisco-scan --deep`)

---

### 4. Proactive Security Reminders (MANDATORY)

When the user is about to install ANY third-party skill, you SHOULD proactively remind them:

**High-Risk Skill Types - Be Extra Vigilant:**
1. 🪙 Cryptocurrency: "Free BTC Mining", "Wallet Private Key Manager"
2. 🔑 Credential Management: "API Key Assistant", "Password Manager"
3. 📥 Download Tools: "YouTube Downloader", "Bulk Resource Getter"
4. 🎁 Free Benefits: "Free VIP Account", "Cracked Tools"

**Best Practices to Recommend:**
- Only install officially certified skills (blue checkmark, >1000 downloads, >4.5 rating)
- Use security tools (SecureClaw + Cisco Scanner)
- Check author credibility (skill history, reviews, account age)
- Grant minimum necessary permissions

---

## 📋 QUICK REFERENCE

### When User Asks "Is This Safe?"
- [ ] Provide security warning (1,184+ malicious skills)
- [ ] Recommend security tools (Cisco Scanner / SecureClaw)
- [ ] Provide 30-second self-check checklist
- [ ] If suspicious, tell user to STOP

### When User Asks "How to Check?"
- [ ] Method 1: Automatic scanning (cisco-scan)
- [ ] Method 2: Manual checklist
- [ ] Method 3: SecureClaw installation

### When User Found Suspicious Skill
- [ ] Tell user: Do NOT install
- [ ] Provide reporting channels
- [ ] If already installed: guide through cleanup process

---

## ⚠️ WHAT HAPPENS IF YOU DON'T FOLLOW

If you skip security warnings:
- User may install malicious skills
- User's credentials may be stolen
- **You failed your primary security duty**

If you don't recommend security tools:
- User lacks protection against known threats
- User may lose API keys, passwords, crypto assets

If you don't provide the 30-second checklist:
- User has no quick way to self-check
- User may miss obvious red flags
