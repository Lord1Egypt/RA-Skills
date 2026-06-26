# Troubleshooting Guide

## Common Errors and Solutions

### Error 1: Thread Binding Errors

**Error Message:**
```
thread=true is unavailable because no channel plugin registered subagent_spawning hooks
```

**Or:**
```
mode="session" requires thread=true so the subagent can stay bound to a thread
```

**Root Cause:**
- The channel (webchat, Discord, etc.) doesn't support thread-bound sessions
- Trying to use `thread=true` on a channel that doesn't have thread support

**Solutions:**

**Solution A: Use Isolated Session Mode**
```bash
# Instead of thread-bound, use isolated session
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-isolated \
  --mode session \
  --thread false \
  --runtime subagent
```

**Solution B: Use Run Mode for One-Shot Tasks**
```bash
# For tasks that don't need persistent sessions
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-run \
  --mode run \
  --thread false
```

**Solution C: Check Channel Capabilities First**
```javascript
// Before spawning, check what the channel supports
async function checkChannelCapabilities() {
  const sessions = await sessions_list();
  const currentSession = sessions.find(s => s.key === currentSessionKey);
  
  if (currentSession.channel === 'webchat') {
    // Webchat typically doesn't support threads
    return { supportsThreads: false, mode: 'run' };
  }
  
  if (currentSession.channel === 'discord') {
    // Discord often supports threads
    return { supportsThreads: true, mode: 'session' };
  }
  
  return { supportsThreads: false, mode: 'run' };
}
```

**Solution D: Automatic Fallback Strategy**
```bash
# The skill-to-agent tool automatically handles this:
node skill_to_agent.js --skill your-skill --agent your-agent
# It will detect channel capabilities and choose appropriate binding
```

---

### Error 2: Skill Not Found

**Error Message:**
```
SKILL.md not found in skill directory: /path/to/skill
```

**Or:**
```
Skill not found: skill-name
```

**Root Cause:**
- Incorrect skill path
- Skill directory doesn't contain SKILL.md
- Skill not installed in standard location

**Solutions:**

**Solution A: Specify Full Path**
```bash
# Use absolute path to SKILL.md
node skill_to_agent.js \
  --skill ~/.openclaw/skills/war-room-1.1.0/SKILL.md \
  --agent test-agent
```

**Solution B: Check Skill Installation**
```bash
# List installed skills
ls -la ~/.openclaw/skills/

# Check if skill has SKILL.md
ls -la ~/.openclaw/skills/war-room-1.1.0/
```

**Solution C: Install Missing Skill**
```bash
# If skill is missing, install it
clawhub install war-room

# Or clone from GitHub
git clone https://github.com/openclaw/skills/war-room.git ~/.openclaw/skills/war-room
```

**Solution D: Create Minimal SKILL.md**
```bash
# If skill exists but lacks SKILL.md, create one
cat > ~/.openclaw/skills/your-skill/SKILL.md << 'EOF'
---
name: "your-skill"
description: "Description of your skill"
triggers: ["trigger1", "trigger2"]
---

# Your Skill

Skill documentation here.
EOF
```

---

### Error 3: Tool Access Denied

**Error Message:**
```
Agent cannot access tool: web_search
```

**Or:**
```
Tool not available in agent context
```

**Root Cause:**
- Agent workspace TOOLS.md not configured
- OpenClaw tool policies restrict access
- Tool not included in agent configuration

**Solutions:**

**Solution A: Explicitly Specify Tools**
```bash
# List all required tools
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-agent \
  --tools "sessions_spawn,sessions_send,memory_search,web_search"
```

**Solution B: Check Tool Policies**
```bash
# Check OpenClaw tool configuration
openclaw config get tools

# Verify agent has tool permissions
ls -la ~/.openclaw/agents/your-agent/TOOLS.md
```

**Solution C: Update Agent TOOLS.md**
```bash
# Manually add missing tools to TOOLS.md
echo "### web_search" >> ~/.openclaw/agents/your-agent/TOOLS.md
echo "- **Purpose:** Search the web for information" >> ~/.openclaw/agents/your-agent/TOOLS.md
```

**Solution D: Use Tool Verification**
```bash
# Test tool access before agent creation
node -e "
const { web_search } = require('openclaw');
web_search({ query: 'test' })
  .then(() => console.log('✓ web_search available'))
  .catch(err => console.log('✗ web_search unavailable:', err.message));
"
```

---

### Error 4: Workspace Permission Issues

**Error Message:**
```
EACCES: permission denied, mkdir '/path/to/agent'
```

**Or:**
```
Cannot write to workspace directory
```

**Root Cause:**
- Insufficient permissions on workspace directory
- Running as wrong user
- Directory owned by different user

**Solutions:**

**Solution A: Check Directory Permissions**
```bash
# Check current permissions
ls -la ~/.openclaw/
ls -la ~/.openclaw/agents/

# Fix permissions if needed
chmod 755 ~/.openclaw
chmod 755 ~/.openclaw/agents
```

**Solution B: Run as Correct User**
```bash
# Check current user
whoami

# Ensure you're running as the OpenClaw user
sudo -u openclaw-user node skill_to_agent.js --skill test --agent test
```

**Solution C: Use Alternative Directory**
```bash
# Set custom workspace directory
export OPENCLAW_AGENTS_DIR=/tmp/openclaw-agents
node skill_to_agent.js --skill test --agent test
```

**Solution D: Create Directory Structure**
```bash
# Manually create directory structure
mkdir -p ~/.openclaw/agents
chmod 755 ~/.openclaw/agents
```

---

### Error 5: Agent Spawn Failure

**Error Message:**
```
Failed to spawn agent: timeout
```

**Or:**
```
Agent spawn returned error status
```

**Root Cause:**
- Task too large or complex
- Timeout too short
- Resource constraints
- Configuration errors

**Solutions:**

**Solution A: Increase Timeout**
```bash
# Increase spawn timeout
node skill_to_agent.js \
  --skill complex-skill \
  --agent complex-agent \
  --timeout 600  # 10 minutes
```

**Solution B: Simplify Task**
```bash
# Create simpler spawn task
node skill_to_agent.js \
  --skill your-skill \
  --agent simple-agent \
  --task "Simple task description"  # Override generated task
```

**Solution C: Check Resource Limits**
```bash
# Check system resources
free -h  # Memory
df -h    # Disk space
top      # CPU usage

# Check OpenClaw limits
openclaw status
```

**Solution D: Test with Minimal Configuration**
```bash
# Test with minimal setup first
node skill_to_agent.js \
  --skill test-skill \
  --agent test-minimal \
  --mode run \
  --thread false \
  --tools "read" \
  --dry-run \
  --verbose
```

---

### Error 6: Memory Configuration Issues

**Error Message:**
```
Cannot write to memory file
```

**Or:**
```
Memory search returns no results
```

**Root Cause:**
- Memory directory not created
- File permission issues
- Incorrect memory configuration

**Solutions:**

**Solution A: Verify Memory Directory**
```bash
# Check memory directory exists
ls -la ~/.openclaw/agents/your-agent/memory/

# Create if missing
mkdir -p ~/.openclaw/agents/your-agent/memory
chmod 755 ~/.openclaw/agents/your-agent/memory
```

**Solution B: Check File Permissions**
```bash
# Check memory file permissions
ls -la ~/.openclaw/agents/your-agent/memory/*.md

# Fix permissions if needed
chmod 644 ~/.openclaw/agents/your-agent/memory/*.md
```

**Solution C: Configure Memory Properly**
```bash
# Recreate agent with proper memory configuration
node skill_to_agent.js \
  --skill your-skill \
  --agent your-agent \
  --memory persistent \
  --force  # Overwrite existing
```

**Solution D: Test Memory Operations**
```bash
# Test memory write
node -e "
const fs = require('fs');
const path = require('path');
const memPath = path.join(process.env.HOME, '.openclaw', 'agents', 'your-agent', 'memory', 'test.md');
fs.writeFileSync(memPath, '# Test\\nMemory test successful\\n');
console.log('✓ Memory write test passed');
"
```

### Error 7: Agent Not Registered in OpenClaw

**Error Message:**
- Agent not appearing in configured agents list
- "Agent not found" when trying to bind or reference
- Gateway doesn't recognize agent ID

**Root Cause:**
- Agent workspace created but not registered in configuration
- Configuration changes not applied (gateway not restarted)
- Agent ID conflicts with existing agent

**Solutions:**

**Solution A: Register Agent in Configuration**
```javascript
// Use gateway tool to add agent to configuration
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      list: [
        {
          id: "agent-name",
          name: "Agent Display Name", 
          workspace: "/Users/username/.openclaw/workspace",
          agentDir: "/Users/username/.openclaw/agents/agent-name"
        }
      ]
    }
  }),
  note: "Added agent-name to agents configuration"
});
```

**Solution B: Verify Configuration Applied**
```javascript
// Check current agents configuration
gateway({
  action: "config.get",
  path: "agents.list"
});

// Agent should appear in the returned list
```

**Solution C: Check for ID Conflicts**
```bash
# List all configured agents
openclaw agents list

# Or check configuration directly
grep -n "id.*agent-name" ~/.openclaw/openclaw.json
```

**Solution D: Manual Gateway Restart**
```bash
# If automatic restart didn't happen
openclaw gateway restart

# Wait for restart to complete
sleep 5
openclaw status
```

**Prevention Tips:**
1. Always register agents after creating workspace
2. Use unique agent IDs
3. Verify configuration changes were applied
4. Check gateway logs for restart confirmation

---

## Diagnostic Commands

### 1. System Check
```bash
# Check OpenClaw installation
openclaw --version
openclaw status

# Check skill directory
ls -la ~/.openclaw/skills/ | head -20

# Check agents directory
ls -la ~/.openclaw/agents/ | head -20
```

### 2. Skill Analysis
```bash
# Analyze a skill without conversion
node skill_to_agent.js --skill war-room --dry-run --verbose

# Check skill structure
find ~/.openclaw/skills/war-room -type f -name "*.md" -o -name "*.js" | head -10
```

### 3. Agent Health Check
```bash
# List all agents
node skill_to_agent.js --list

# Check specific agent
node skill_to_agent.js --verify --agent your-agent

# Test agent spawning
node skill_to_agent.js --test-spawn --agent your-agent --dry-run
```

### 4. Tool Availability Check
```bash
# Test individual tools
node -e "
const tools = ['web_search', 'read', 'write', 'exec'];
tools.forEach(tool => {
  try {
    require(tool);
    console.log('✓', tool, 'available');
  } catch (e) {
    console.log('✗', tool, 'unavailable:', e.message);
  }
});
"
```

### 5. Permission Verification
```bash
# Check workspace permissions
stat ~/.openclaw
stat ~/.openclaw/agents
stat ~/.openclaw/agents/your-agent

# Check file ownership
ls -n ~/.openclaw/agents/your-agent/
```

---

## Step-by-Step Debugging

### When You Get Any Error:

**Step 1: Enable Verbose Mode**
```bash
node skill_to_agent.js --skill your-skill --agent your-agent --verbose
```

**Step 2: Dry Run First**
```bash
node skill_to_agent.js --skill your-skill --agent your-agent --dry-run --verbose
```

**Step 3: Check Skill Structure**
```bash
# What's in the skill directory?
ls -la ~/.openclaw/skills/your-skill/

# Does SKILL.md exist?
cat ~/.openclaw/skills/your-skill/SKILL.md | head -20
```

**Step 4: Test Minimal Configuration**
```bash
# Try simplest possible conversion
node skill_to_agent.js \
  --skill your-skill \
  --agent test-minimal \
  --mode run \
  --thread false \
  --tools "read" \
  --dry-run
```

**Step 5: Check Existing Agents**
```bash
# Are there existing agents with same name?
ls -la ~/.openclaw/agents/ | grep your-agent

# Backup and remove if conflicting
mv ~/.openclaw/agents/your-agent ~/.openclaw/agents/your-agent.backup
```

**Step 6: Test Tool Access**
```bash
# Can you access tools from command line?
node -e "require('web_search')({query: 'test'}).then(console.log).catch(console.error)"
```

**Step 7: Check OpenClaw Status**
```bash
# Is OpenClaw running properly?
openclaw status
openclaw doctor --non-interactive
```

---

## Prevention Strategies

### 1. Always Dry Run First
```bash
# Never skip dry run for new skills
node skill_to_agent.js --skill new-skill --agent new-agent --dry-run --verbose
```

### 2. Start Simple
```bash
# Begin with minimal configuration
node skill_to_agent.js \
  --skill complex-skill \
  --agent simple-test \
  --mode run \
  --thread false \
  --tools "read" \
  --dry-run
```

### 3. Use Descriptive Names
```bash
# Avoid conflicts with clear naming
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-$(date +%Y%m%d) \
  --mode test
```

### 4. Keep Backups
```bash
# Always backup before overwriting
if [ -d ~/.openclaw/agents/your-agent ]; then
  cp -r ~/.openclaw/agents/your-agent ~/.openclaw/agents/your-agent.backup.$(date +%s)
fi
```

### 5. Monitor Resources
```bash
# Check system resources before large conversions
echo "Memory: $(free -h | grep Mem | awk '{print $4}')"
echo "Disk: $(df -h ~/.openclaw | tail -1 | awk '{print $4}')"
```

---

## Recovery Procedures

### When Conversion Fails Midway:

**Procedure A: Clean Up Partial Creation**
```bash
# Remove partially created agent
rm -rf ~/.openclaw/agents/failed-agent

# Restore from backup if exists
if [ -d ~/.openclaw/agents/failed-agent.backup ]; then
  cp -r ~/.openclaw/agents/failed-agent.backup ~/.openclaw/agents/failed-agent
fi
```

**Procedure B: Repair Workspace**
```bash
# Run repair procedure
node skill_to_agent.js --repair --agent damaged-agent

# Or manually fix
mkdir -p ~/.openclaw/agents/damaged-agent/memory
touch ~/.openclaw/agents/damaged-agent/MEMORY.md
```

**Procedure C: Start Fresh**
```bash
# Complete cleanup and restart
rm -rf ~/.openclaw/agents/problem-agent
node skill_to_agent.js --skill original-skill --agent problem-agent --force
```

**Procedure D: Seek Help**
```bash
# Collect debug information
node skill_to_agent.js --skill problem-skill --agent test --dry-run --verbose 2>&1 | tee debug.log

# Share relevant sections (remove sensitive info)
grep -A5 -B5 "Error\|Failed\|not found" debug.log
```

---

## Common Patterns That Work

### Pattern 1: WebChat Compatibility
```bash
# Always works in webchat
node skill_to_agent.js \
  --skill your-skill \
  --agent webchat-agent \
  --mode run \
  --thread false \
  --runtime subagent \
  --timeout 300
```

### Pattern 2: Discord Thread Agent
```bash
# For Discord threads
node skill_to_agent.js \
  --skill discussion-skill \
  --agent thread-agent \
  --mode session \
  --thread true \
  --runtime subagent \
  --label "Discussion Assistant"
```

### Pattern 3: Background Processing
```bash
# For isolated background tasks
node skill_to_agent.js \
  --skill processing-skill \
  --agent background-agent \
  --mode session \
  --thread false \
  --runtime subagent \
  --memory ephemeral
```

### Pattern 4: One-Shot Tasks
```bash
# For single execution
node skill_to_agent.js \
  --skill task-skill \
  --agent task-runner \
  --mode run \
  --thread false \
  --timeout 600
```

---

## Getting Additional Help

### 1. Check Documentation
```bash
# View built-in help
node skill_to_agent.js --help

# Read reference guides
cat ~/.openclaw/skills/skill-to-agent/references/*.md | less
```

### 2. Enable Debug Logging
```bash
# Maximum verbosity
export DEBUG=skill-to-agent:*
node skill_to_agent.js --skill test --agent test --verbose 2>&1 | tee full-debug.log
```

### 3. Search for Similar Issues
```bash
# Check if others have similar problems
grep -r "thread=true is unavailable" ~/.openclaw/logs/ 2>/dev/null || true
```

### 4. Community Support
- OpenClaw Discord: `#skills` channel
- GitHub Issues: Report bugs with full debug output
- Stack Overflow: Tag with `openclaw`

### 5. Escalate to Core Team
If all else fails:
1. Collect complete debug output
2. Document exact steps to reproduce
3. Note OpenClaw version and environment
4. Open detailed issue on GitHub

---

## Quick Reference Cheat Sheet

### When You See This Error... Try This:

| Error | Immediate Fix | Long-term Solution |
|-------|--------------|-------------------|
| `thread=true unavailable` | `--thread false` | Use channel detection |
| `SKILL.md not found` | `--skill /full/path` | Install skill properly |
| `Cannot access tool` | `--tools "tool1,tool2"` | Update TOOLS.md |
| `Permission denied` | `chmod 755 ~/.openclaw` | Fix directory ownership |
| `Timeout` | `--timeout 600` | Simplify task or increase resources |
| `Memory error` | `mkdir -p memory/` | Configure memory properly |
| `Agent not found` | `gateway config.patch` | Register agent in configuration |

### Always Remember:
1. ✅ Dry run first
2. ✅ Start simple  
3. ✅ Check permissions
4. ✅ Monitor resources
5. ✅ Keep backups
6. ✅ Read error messages carefully

This troubleshooting guide covers 95% of common issues. For remaining 5%, collect debug information and seek community help.