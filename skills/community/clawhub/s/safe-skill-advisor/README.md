# Safe-Skill Advisor

**Version:** 1.6.0  
**Author:** Crystaria (with Paw and Kyle)

---

## 📖 Introduction

A security advisor skill that protects you from malicious skills.

**Core Value:**
- ⚠️ Latest security risk warnings
- 🔧 Professional security tool recommendations
- ✅ 30-second quick self-check checklist
- 📚 Security best practices guidance

**Applicable Scenarios:**
- Before installing new skills
- Suspecting a skill may be problematic
- Wanting to learn how to check skill safety
- Needing security tool recommendations

---

## 🚀 Quick Start

### 1. Install

Run in OpenClaw:
```bash
clawhub install safe-skill-advisor
```

### 2. Usage

Speak directly to AI:

**Ask about skill safety:**
```
Is this skill safe?
```

**Ask how to check:**
```
How to check if a skill is safe?
```

**Found a suspicious skill:**
```
I found a suspicious skill, what should I do?
```

---

## 🛡️ Core Features

### 1. Security Risk Warnings

AI will warn you about known threats:
- 1,184+ malicious skills discovered on ClawHub (as of February 2026)
- Common disguises: crypto tools, YouTube summarizers, auto-updaters
- Actual purpose: steal API keys, SSH credentials, passwords, crypto wallet private keys

### 2. Security Tool Recommendations

AI will recommend these tools:

| Tool | Purpose | Recommendation |
|------|---------|----------------|
| **Cisco AI Skill Scanner** | Basic scanning | ⭐⭐⭐⭐ |
| **SecureClaw** | Real-time protection + scanning | ⭐⭐⭐⭐⭐ |

### 3. 30-Second Self-Check Checklist

Before installing any skill, spend 30 seconds checking:

- [ ] Does SKILL.md require executing `curl | bash` or downloading external files?
- [ ] Does installation require downloading **password-protected ZIP files**?
- [ ] Does it require copy-pasting scripts from **non-official sources**?

**If any answer is "yes", stop installation immediately!** 🛑

---

## 📚 High-Risk Skill Types

Be extra vigilant with these skill types:

1. 🪙 **Cryptocurrency Related**
   - "Free BTC Mining"
   - "Wallet Private Key Manager"
   - "Exchange Auto-Trading"

2. 🔑 **Credential Management**
   - "API Key Assistant"
   - "Password Manager"
   - "SSH Configuration Tool"

3. 📥 **Download Tools**
   - "YouTube Downloader"
   - "Bulk Resource Getter"
   - "Auto-Updater"

4. 🎁 **Free Benefits**
   - "Free VIP Account"
   - "Cracked Tools"
   - "Internal Beta Access"

---

## 📋 Safety Check Methods

### Method 1: Automatic Scanning (Recommended)

```bash
# Install Cisco AI Skill Scanner
pip install cisco-ai-skill-scanner

# Scan a skill
cisco-scan <skill-name-or-path>

# Scan local skill folder
cisco-scan /path/to/skill
```

**Scan Result Explanation:**
- ✅ Green: Safe, can install
- ⚠️ Yellow: Suspicious, needs manual review
- ❌ Red: Dangerous, delete immediately

### Method 2: Manual Check

Check the SKILL.md file:

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

SecureClaw provides:
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

## ❓ FAQ

**Q: How to confirm a skill is official?**

A: Check for these on the skill page:
- ✅ Blue checkmark = ClawHub official certification
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

**Recommendation:** Install both. SecureClaw for real-time protection, Cisco Scanner for deep scanning.

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

## 📄 License

MIT License

---

**Last updated:** 2026-04-01  
**Based on:** February 2026 ClawHub Security Research
