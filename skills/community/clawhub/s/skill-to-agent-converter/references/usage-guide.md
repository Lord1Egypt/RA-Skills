# Skill-to-Agent Usage Guide

## Quick Start

### Phase 1: Analyze Skill Structure
1. Read SKILL.md frontmatter (name, description, triggers)
2. Identify required tools and dependencies
3. Determine agent type: thread-bound, isolated, or run-mode

### Phase 2: Create Agent Workspace
```bash
# Create agent directory
mkdir -p ~/.openclaw/agents/agent-name

# Copy skill resources if needed
cp -r /path/to/skill/references/ ~/.openclaw/agents/agent-name/
cp -r /path/to/skill/scripts/ ~/.openclaw/agents/agent-name/
```

### Phase 3: Configure Agent Identity
Create the following files in the agent workspace:
1. **IDENTITY.md** - Agent name, creature, vibe, emoji
2. **SOUL.md** - Agent personality and operating style
3. **AGENTS.md** - Workspace rules and workflow
4. **USER.md** - Who the agent helps
5. **HEARTBEAT.md** - Proactive behavior checklist
6. **TOOLS.md** - Required tools and configurations
7. **memory/** directory for daily logs

### Phase 4: Register Agent in OpenClaw
```javascript
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      list: [
        {
          id: "agent-name",
          name: "Agent Display Name",
          workspace: "/Users/nimbletenthousand/.openclaw/workspace",
          agentDir: "/Users/nimbletenthousand/.openclaw/agents/agent-name"
        }
      ]
    }
  }),
  note: "Added agent-name to agents configuration"
});
```

### Phase 5: Spawn with Correct Binding
```javascript
sessions_spawn({
  task: "Agent instructions based on skill...",
  label: "agent-name-task",
  runtime: "subagent",
  mode: "session", // or "run" based on channel
  thread: false, // or true for thread-bound agents
  cwd: "/Users/nimbletenthousand/.openclaw/agents/agent-name",
  timeoutSeconds: 300
});
```

---

## Common Use Cases

### Use Case 1: Discord Thread Agent
**Scenario:** You want a skill to operate in Discord threads
```bash
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-bot \
  --mode session \
  --thread true \
  --runtime subagent \
  --label "War Room Coordinator"
```

**Result:** Creates an agent that can be spawned in Discord threads with proper binding.

### Use Case 2: Background Processing Agent
**Scenario:** You need a skill to run isolated background tasks
```bash
node skill_to_agent.js \
  --skill seo-content \
  --agent content-generator \
  --mode session \
  --thread false \
  --runtime subagent \
  --tools "read,write,web_search" \
  --memory ephemeral
```

**Result:** Creates an isolated agent for batch content generation.

### Use Case 3: One-Shot Task Agent
**Scenario:** You want a skill for single execution tasks
```bash
node skill_to_agent.js \
  --skill video-frames \
  --agent video-processor \
  --mode run \
  --thread false \
  --runtime subagent \
  --timeout 600
```

**Result:** Creates an agent configuration for one-time video processing tasks.

---

## Integration with OpenClaw

### As a Skill
Add to your OpenClaw configuration:
```yaml
skills:
  - name: skill-to-agent
    path: ~/.openclaw/skills/skill-to-agent
    enabled: true
```

### In Agent Scripts
```javascript
const SkillToAgent = require('~/.openclaw/skills/skill-to-agent/skill_to_agent.js');
const converter = new SkillToAgent();

// Convert and spawn in one go
async function createAndSpawnSkillAgent(skillName, agentId) {
  const analysis = converter.analyzeSkill(skillName);
  const binding = converter.resolveBinding({}, analysis);
  const task = converter.generateSpawnTask(agentId, analysis, binding);
  
  // Use sessions_spawn to create the agent
  const result = await sessions_spawn({
    task: task,
    label: binding.label,
    runtime: binding.runtime,
    mode: binding.mode,
    thread: binding.thread
  });
  
  return result;
}
```

### In Cron Jobs
```bash
# Create agents dynamically in cron jobs
0 8 * * * node ~/.openclaw/skills/skill-to-agent/skill_to_agent.js --skill daily-digest --agent daily-reporter --mode run
```

---

## Advanced Configuration

### Custom Tool Mapping
Create a `tools-config.json`:
```json
{
  "web_search": {
    "purpose": "Market research and competitor analysis",
    "limits": "10 queries per hour",
    "patterns": ["search for", "research", "find information"]
  },
  "browser": {
    "purpose": "Web automation and data collection",
    "limits": "5 minutes per session",
    "patterns": ["automate", "scrape", "collect data"]
  }
}
```

Use it with:
```bash
node skill_to_agent.js --skill your-skill --agent your-agent --tools-config tools-config.json
```

### Custom Templates
Override default templates by creating:
- `templates/SOUL.custom.md`
- `templates/AGENTS.custom.md`
- `templates/TOOLS.custom.md`

The converter will use custom templates if available.

### Environment Variables
```bash
# Set workspace location
export OPENCLAW_AGENTS_DIR=/custom/path/agents

# Enable debug mode
export SKILL_TO_AGENT_DEBUG=true

# Set default runtime
export DEFAULT_AGENT_RUNTIME=acp
```

---

## Troubleshooting

### Common Issues

**Issue 1: "SKILL.md not found"**
```bash
# Solution 1: Specify full path
node skill_to_agent.js --skill ~/.openclaw/skills/war-room/SKILL.md --agent test

# Solution 2: Check skill directory structure
ls -la ~/.openclaw/skills/war-room/
```

**Issue 2: "thread=true is unavailable"**
```bash
# Solution: Use isolated mode instead
node skill_to_agent.js --skill war-room --agent test --mode session --thread false
```

**Issue 3: Agent lacks tool access**
```bash
# Solution: Verify tools and update configuration
node skill_to_agent.js --skill war-room --agent test --tools "sessions_spawn,sessions_send,memory_search"
```

**Issue 4: Workspace permission errors**
```bash
# Solution: Check directory permissions
ls -la ~/.openclaw/agents/
chmod 755 ~/.openclaw/agents/
```

### Debug Mode
Enable verbose output:
```bash
node skill_to_agent.js --skill war-room --agent test --verbose
```

### Dry Run
Test without making changes:
```bash
node skill_to_agent.js --skill war-room --agent test --dry-run --verbose
```

---

## Performance Optimization

### Token Management
- Keep SOUL.md under 500 tokens
- Use efficient memory strategies
- Configure context pruning
- Set appropriate timeouts

### Resource Allocation
```bash
# For resource-intensive skills
node skill_to_agent.js \
  --skill video-processing \
  --agent video-bot \
  --mode run \
  --timeout 1800 \
  --memory ephemeral
```

### Batch Processing
```bash
# Convert multiple skills at once
for skill in war-room marketing-pmm seo-content; do
  node skill_to_agent.js --skill $skill --agent ${skill}-bot --mode run
done
```

---

## Security Considerations

### Agent Isolation
- Each agent gets separate workspace
- No shared memory by default
- Tool access limited to requirements
- Session boundaries enforced

### Data Protection
- Skill files copied, not linked
- Agent memory separate from skill
- Cleanup policies configurable
- Audit logs in agent workspace

### Access Control
```bash
# Create agents with minimal permissions
node skill_to_agent.js \
  --skill read-only-skill \
  --agent reader \
  --tools "read,memory_get" \
  --mode isolated
```

---

## Monitoring & Maintenance

### Agent Health Checks
```bash
# Check agent workspace
ls -la ~/.openclaw/agents/{agent-id}/

# Test agent spawning
node -e "console.log(require('./skill_to_agent.js').testSpawn('agent-id'))"

# Verify tool access
node skill_to_agent.js --verify --agent {agent-id}
```

### Workspace Cleanup
```bash
# List all created agents
node skill_to_agent.js --list

# Repair damaged workspace
node skill_to_agent.js --repair --agent {agent-id}

# Clean up old agents
find ~/.openclaw/agents/* -type d -mtime +30 -exec rm -rf {} \;
```

### Performance Monitoring
```bash
# Monitor agent resource usage
ps aux | grep "agent:" | grep {agent-id}

# Check workspace size
du -sh ~/.openclaw/agents/{agent-id}/

# Review memory usage
tail -n 100 ~/.openclaw/agents/{agent-id}/memory/$(date +%Y-%m-%d).md
```

---

## Integration Examples

### Example 1: Complete Workflow
```bash
#!/bin/bash
# create_and_deploy_agent.sh

SKILL=$1
AGENT=$2

echo "🔧 Converting $SKILL to agent $AGENT"

# Step 1: Convert skill to agent
node skill_to_agent.js --skill $SKILL --agent $AGENT --verbose

# Step 2: Test agent workspace
if [ -d ~/.openclaw/agents/$AGENT ]; then
  echo "✅ Agent workspace created"
  
  # Step 3: Create test script
  cat > test_$AGENT.js << EOF
  const { sessions_spawn } = require('openclaw');
  
  async function testAgent() {
    const config = require('~/.openclaw/agents/$AGENT/spawn-config.json');
    const result = await sessions_spawn(config);
    console.log('Agent spawned:', result.sessionKey);
  }
  
  testAgent().catch(console.error);
  EOF
  
  echo "📝 Test script created: test_$AGENT.js"
  
else
  echo "❌ Failed to create agent workspace"
  exit 1
fi
```

### Example 2: Dynamic Agent Creation
```javascript
// dynamic_agent_creator.js
const SkillToAgent = require('./skill_to_agent.js');
const fs = require('fs');
const path = require('path');

class DynamicAgentManager {
  constructor() {
    this.converter = new SkillToAgent();
  }
  
  async createAgentForTask(taskDescription, skillPatterns) {
    // Analyze available skills
    const skillsDir = path.join(process.env.HOME, '.openclaw', 'skills');
    const skills = fs.readdirSync(skillsDir);
    
    // Find matching skill
    const matchingSkill = skills.find(skill => {
      const skillPath = path.join(skillsDir, skill, 'SKILL.md');
      if (fs.existsSync(skillPath)) {
        const content = fs.readFileSync(skillPath, 'utf8').toLowerCase();
        return skillPatterns.some(pattern => content.includes(pattern));
      }
      return false;
    });
    
    if (!matchingSkill) {
      throw new Error('No matching skill found');
    }
    
    // Generate agent ID
    const agentId = `task-${Date.now()}-${matchingSkill}`;
    
    // Create agent
    const analysis = this.converter.analyzeSkill(matchingSkill);
    const binding = this.converter.resolveBinding({
      mode: 'run',
      thread: false
    }, analysis);
    
    // Generate spawn configuration
    const spawnConfig = {
      task: this.converter.generateSpawnTask(agentId, analysis, binding),
      label: `Task Agent: ${taskDescription.substring(0, 20)}...`,
      runtime: binding.runtime,
      mode: binding.mode,
      thread: binding.thread,
      timeoutSeconds: 300
    };
    
    return {
      agentId,
      spawnConfig,
      skill: matchingSkill
    };
  }
}

module.exports = DynamicAgentManager;
```

### Example 3: Skill Chaining System
```javascript
// skill_chain_manager.js
const SkillToAgent = require('./skill_to_agent.js');

class SkillChainManager {
  constructor() {
    this.converter = new SkillToAgent();
    this.activeAgents = new Map();
  }
  
  async createChain(skillNames, workflow) {
    const agents = [];
    
    for (const skillName of skillNames) {
      const agentId = `${skillName}-${Date.now()}`;
      const analysis = this.converter.analyzeSkill(skillName);
      
      // Create agent with sequential binding
      const binding = this.converter.resolveBinding({
        mode: 'session',
        thread: false,
        runtime: 'subagent'
      }, analysis);
      
      const agentConfig = {
        id: agentId,
        skill: skillName,
        analysis: analysis,
        binding: binding,
        spawnTask: this.converter.generateSpawnTask(agentId, analysis, binding)
      };
      
      agents.push(agentConfig);
      this.activeAgents.set(agentId, agentConfig);
    }
    
    // Set up communication between agents
    const chainConfig = {
      agents: agents,
      workflow: workflow,
      communication: {
        memoryFile: `memory/chain-${Date.now()}.md`,
        handoffProtocol: 'memory-based'
      }
    };
    
    return chainConfig;
  }
  
  async executeChain(chainConfig, input) {
    // Write input to shared memory
    const memoryPath = chainConfig.communication.memoryFile;
    fs.writeFileSync(memoryPath, `# Chain Execution - ${new Date().toISOString()}\n\nInput: ${JSON.stringify(input, null, 2)}\n\n`);
    
    // Execute each agent in sequence
    for (const agentConfig of chainConfig.agents) {
      console.log(`Executing agent: ${agentConfig.id}`);
      
      // Spawn agent with chain context
      const task = `${agentConfig.spawnTask}\n\nChain Context: Read ${memoryPath} for input and previous results.`;
      
      const result = await sessions_spawn({
        task: task,
        label: agentConfig.id,
        runtime: agentConfig.binding.runtime,
        mode: agentConfig.binding.mode,
        thread: agentConfig.binding.thread
      });
      
      // Append result to memory
      const resultText = `## ${agentConfig.id} Result\n${JSON.stringify(result, null, 2)}\n\n`;
      fs.appendFileSync(memoryPath, resultText);
      
      // Wait for completion
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Read final result
    const finalResult = fs.readFileSync(memoryPath, 'utf8');
    return finalResult;
  }
}

module.exports = SkillChainManager;
```

---

## Best Practices

### 1. Skill Analysis First
Always analyze the skill before conversion:
```bash
node skill_to_agent.js --skill your-skill --dry-run --verbose
```

### 2. Start Simple
Begin with `--mode run` for testing, then move to more complex configurations.

### 3. Use Descriptive Labels
```bash
--label "Marketing Analyst (Data Research Focus)"
```

### 4. Limit Tool Access
Only include tools the agent actually needs:
```bash
--tools "web_search,web_fetch,memory_search"
```

### 5. Configure Timeouts
```bash
--timeout 600  # 10 minutes for processing tasks
```

### 6. Monitor Memory Usage
Check agent memory files regularly and implement cleanup policies.

### 7. Test Before Deployment
Always test agents in a non-production environment first.

### 8. Document Configurations
Keep records of agent configurations and their purposes.

---

## Migration & Updates

### Updating Existing Agents
```bash
# Create backup
cp -r ~/.openclaw/agents/old-agent ~/.openclaw/agents/old-agent.backup

# Recreate with updated skill
node skill_to_agent.js --skill updated-skill --agent old-agent --force
```

### Migrating Between Systems
1. Export agent configuration:
```bash
tar -czf agent-backup.tar.gz ~/.openclaw/agents/your-agent/
```

2. Import on new system:
```bash
tar -xzf agent-backup.tar.gz -C ~/.openclaw/agents/
```

3. Update paths in configuration files if needed.

---

## Community & Support

### Getting Help
- Open issues on GitHub repository
- Join OpenClaw Discord community
- Check existing documentation and examples

### Contributing
1. Fork the repository
2. Make enhancements
3. Add tests
4. Update documentation
5. Submit pull request

### Reporting Issues
Include:
- OpenClaw version
- Skill being converted
- Error messages
- Steps to reproduce
- Expected vs actual behavior

---

## Future Roadmap

### Planned Features
1. **AI-Powered Analysis** - Automatically determine optimal agent configuration
2. **Skill Composition** - Combine multiple skills into single agent
3. **Performance Optimization** - Dynamic resource allocation
4. **Enhanced Security** - Sandboxed execution environments
5. **Marketplace Integration** - Publish agents to ClawHub

### Community Requests
- Support for custom agent templates
- Integration with external APIs
- Advanced monitoring dashboards
- Automated testing frameworks
- Multi-tenant support

---

## Conclusion

The Skill-to-Agent converter solves the common problem of properly converting OpenClaw skills into functional agents. By following this guide, you can:

1. **Convert any skill** into a properly configured agent
2. **Avoid common binding errors** with smart configuration
3. **Create specialized agents** for different use cases
4. **Manage agent lifecycles** effectively
5. **Scale your agent ecosystem** systematically

Remember to start simple, test thoroughly, and iterate based on your specific needs. Happy agent building!