---
name: qwen-portal-auth-helper
description: Automate qwen-portal OAuth authentication - solves the interactive TTY problem with tmux, provides monitoring and recovery tools.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["tmux", "openclaw"] },
        "category": "authentication",
        "tags": ["qwen-portal", "oauth", "automation", "troubleshooting"],
        "version": "1.0.0",
        "author": "Bessent (based on 2026-03-09 practical experience)"
      },
  }
---

# Qwen Portal Auth Helper

> **Battle-tested solution for qwen-portal OAuth automation**  
> Solves the "interactive TTY required" problem, prevents cron task failures, and provides full monitoring.

## 🚨 The Problem

qwen-portal provides free models (2,000 requests/day) but **OAuth expires every 1-2 weeks**. When it expires:

1. Cron tasks fail with: `Qwen OAuth refresh token expired or invalid`
2. `openclaw models auth login --provider qwen-portal` fails: `requires an interactive TTY`
3. Manual intervention required, breaking automation
4. Tasks remain in error state even after authentication fix

## 💡 The Solution

This skill provides a complete solution:

- **Automated OAuth link extraction** using tmux (bypasses TTY requirement)
- **Health monitoring** for qwen-portal tasks
- **Self-healing scripts** to fix task states
- **Documented best practices** from real-world experience

## 📦 Installation

```bash
# Via ClawHub (recommended)
clawhub install qwen-portal-auth-helper

# Or manually
cd ~/.openclaw/skills/
git clone <repository>
```

## 🛠️ Quick Start

### Get OAuth Link (when authentication expired)
```bash
~/.openclaw/skills/qwen-portal-auth-helper/scripts/get-qwen-oauth-link.sh
```
Outputs:
```
🔗 OAuth Link: https://chat.qwen.ai/authorize?user_code=M17WU0SC
📱 Device Code: M17WU0SC
```

### Check Authentication Health
```bash
~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh
```
Checks all qwen-portal tasks, reports errors, generates actionable report.

### Setup Weekly Monitoring
```bash
# Add to crontab (runs every Monday at 9 AM)
0 9 * * 1 ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh
```

## 🔧 Core Features

### 1. OAuth Link Automation
```bash
# Traditional way (fails in automation):
openclaw models auth login --provider qwen-portal  # ❌ Error: requires interactive TTY

# Our solution:
./scripts/get-qwen-oauth-link.sh  # ✅ Works in cron, AI assistants, etc.
```

**How it works**: Uses tmux to create virtual terminal, captures output before command hangs.

### 2. Health Monitoring
- Scans all cron tasks using qwen-portal models
- Detects error states and consecutive failures
- Generates detailed reports with actionable advice
- Early warning before complete failure

### 3. Recovery Tools
- Resets task error states after authentication fix
- Provides step-by-step recovery checklist
- Validates fixes actually work

### 4. Best Practices Documentation
- Complete workflow from diagnosis to recovery
- Common pitfalls and how to avoid them
- Maintenance schedule recommendations

## 📋 Complete Workflow

### When tasks start failing:
```
1. Run: check-qwen-auth.sh
   → Identifies failing tasks, shows error details

2. Run: get-qwen-oauth-link.sh  
   → Provides OAuth link and device code

3. User: Click link, authenticate in browser
   → Authorization completes automatically

4. Test: openclaw cron run <task-id>
   → Verifies authentication works

5. Reset: Scripts help reset task state
   → Tasks return to normal operation
```

### Weekly Maintenance:
```
Monday 9 AM: check-qwen-auth.sh runs automatically
If issues detected: Email/notification sent
Preventative action: Re-authenticate before expiry
```

## 🎯 Use Cases

### 1. AI Assistants & Automation
AI assistants can't provide interactive TTY. This skill enables them to:
- Automatically detect qwen-portal auth issues
- Get OAuth links for user approval
- Complete the recovery process

### 2. Cron Task Reliability
Ensure scheduled tasks don't fail due to expired OAuth:
- Weekly health checks
- Early detection of impending expiry
- Automated recovery procedures

### 3. Team Collaboration
Standardized approach for teams:
- Everyone uses same proven method
- Documentation prevents repeated mistakes
- Shared monitoring and alerting

### 4. New User Onboarding
New OpenClaw users inevitably hit this issue. This skill provides:
- Immediate solution without trial-and-error
- Complete documentation
- Community-validated approach

## 🔍 Technical Details

### How OAuth Link Extraction Works
```bash
# The core technique:
tmux new-session -d -s qwen-oauth "openclaw models auth login --provider qwen-portal"
sleep 5
tmux capture-pane -t qwen-oauth -p | grep -E "(http|https)://"
```

**Key discoveries from real-world testing**:
- Link format is always: `https://chat.qwen.ai/authorize?user_code=XXXXXXX&client=qwen-code`
- Device code: 7 uppercase alphanumeric characters (e.g., M17WU0SC)
- Command hangs after showing link (`◑ Waiting for Qwen OAuth approval...`)
- Must capture output actively, not wait for completion

### Task State Management
Even after successful authentication, cron tasks may remain in error state:
```json
// Before fix:
"state": {"lastStatus": "error", "consecutiveErrors": 10}

// After fix (manual reset needed):
"state": {"lastStatus": "pending", "consecutiveErrors": 0}
```

This skill includes scripts to reset these states automatically.

## 📊 Monitoring & Alerting

### What We Monitor
1. **Task Status**: Error vs OK
2. **Consecutive Errors**: >3 triggers warning
3. **Last Success Time**: Tasks not running recently
4. **OAuth Expiry Estimate**: Based on 1-2 week pattern

### Alert Thresholds
- **Warning**: 3+ consecutive errors
- **Critical**: Task in error state + OAuth-related error message
- **Recovery Needed**: Manual intervention required

### Reports Generated
- Weekly health report
- Error analysis with suggested fixes
- Maintenance checklist
- Historical trends

## 🚀 Advanced Usage

### Integration with Other Skills
```bash
# Combine with system-maintenance skill
~/.openclaw/skills/system-maintenance/scripts/daily-maintenance.sh
~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh

# Use with agent-team-orchestration
# Assign OAuth recovery as a specialized team task
```

### Custom Monitoring Schedule
```bash
# Daily quick check (lightweight)
0 9 * * * ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh --quick

# Weekly comprehensive check
0 9 * * 1 ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh --full

# Alert on critical issues immediately
*/30 * * * * ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh --alert-only
```

### Extending for Other OAuth Providers
The pattern works for other services with similar issues:
1. GitHub OAuth
2. Google OAuth  
3. Other AI model providers with device-code flow

## 📝 Examples

### Example 1: Quick Recovery
```bash
# 1. Check what's wrong
./check-qwen-auth.sh

# 2. Get new OAuth link  
./get-qwen-oauth-link.sh
# Output: Link and code to give to user

# 3. After user authenticates, verify
openclaw cron run 71628635-03e3-414b-865b-e427af4e804f
openclaw cron runs --id 71628635-03e3-414b-865b-e427af4e804f

# 4. Reset task states if needed
./scripts/reset-task-state.py 71628635-03e3-414b-865b-e427af4e804f
```

### Example 2: Proactive Maintenance
```bash
# Add to crontab for Monday morning checks
crontab -l | grep -q "check-qwen-auth" || echo "0 9 * * 1 ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh >> ~/.openclaw/logs/qwen-check.log" | crontab -

# Review weekly reports
cat /tmp/qwen-auth-report-*.md | less
```

### Example 3: Integration with AI Assistant
```markdown
When user reports news tasks failing:
1. Run check-qwen-auth.sh to confirm qwen-portal issue
2. Run get-qwen-oauth-link.sh to get authentication link
3. Provide link and code to user
4. Guide user through browser authentication
5. Verify fix with test run
6. Reset task states if needed
```

## ⚠️ Common Pitfalls & Solutions

### Pitfall 1: Command hangs indefinitely
**Solution**: Use timeout and active output capture (implemented in scripts)

### Pitfall 2: ANSI escape codes break parsing
**Solution**: Robust regex that handles colored output (included)

### Pitfall 3: Task state doesn't reset automatically
**Solution**: Manual state reset scripts (provided)

### Pitfall 4: Multiple qwen-portal tasks failing
**Solution**: Batch processing in monitoring script

### Pitfall 5: OAuth expires at inconvenient times
**Solution**: Weekly monitoring catches it early

## 🔄 Maintenance Schedule

### Weekly (Essential)
- Run health check script
- Review error reports
- Prepare for potential re-authentication

### Monthly (Recommended)
- Review OAuth expiry patterns
- Update scripts if qwen-portal changes
- Clean up old log files

### Quarterly (Optional)
- Test complete recovery workflow
- Update documentation
- Check for new best practices

## 🤝 Community & Support

### Based on Real Experience
This skill was developed from solving actual production issues on 2026-03-09:
- Two critical news collection tasks failing
- 9-10 consecutive errors before detection
- Multiple failed attempts before finding tmux solution
- Documented in `.learnings/` system

### Contributing
Found a better way? Have another OAuth provider with similar issues?
1. Fork the repository
2. Add your improvements  
3. Submit pull request
4. Help others avoid the same pitfalls

### Getting Help
- Check `examples/` directory for common scenarios
- Review `docs/troubleshooting.md` for known issues
- Open issue on repository for new problems

## 📈 Benefits

### For Individual Users
- No more manual OAuth link hunting
- Prevent task failures before they happen
- Standardized recovery process
- Less time spent on maintenance

### For Teams
- Shared knowledge and tools
- Consistent monitoring approach
- Reduced support requests
- Faster onboarding for new members

### For Community
- Open source solution to common problem
- Continuously improved by users
- Foundation for other OAuth automation
- Knowledge sharing prevents repeated mistakes

## 🎉 Getting Started

### Installation
```bash
# Install from ClawHub
clawhub install qwen-portal-auth-helper

# Or clone directly
cd ~/.openclaw/skills
git clone https://github.com/your-username/qwen-portal-auth-helper.git
```

### First-Time Setup
```bash
# 1. Test the scripts
cd ~/.openclaw/skills/qwen-portal-auth-helper
./scripts/get-qwen-oauth-link.sh --test-only
./scripts/check-qwen-auth.sh

# 2. Set up monitoring
echo "0 9 * * 1 $(pwd)/scripts/check-qwen-auth.sh" | crontab -

# 3. Document your qwen-portal tasks
# Update examples/your-tasks.md with your task IDs
```

### Verify It Works
```bash
# Simulate a failure scenario
openclaw cron run <your-qwen-portal-task-id>

# Check monitoring catches it
./scripts/check-qwen-auth.sh

# Practice recovery workflow
./scripts/get-qwen-oauth-link.sh --dry-run
```

---

**Remember**: qwen-portal OAuth expires every 1-2 weeks.  
**Solution**: Weekly monitoring + this skill = no more surprises.

*Skill version: 1.0.0 | Based on 2026-03-09 battle-tested experience*