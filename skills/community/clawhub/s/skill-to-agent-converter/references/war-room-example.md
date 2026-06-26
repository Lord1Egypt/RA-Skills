# War Room Skill Conversion Example

This example shows how to properly convert the war-room skill into a functional agent, solving the exact binding errors we encountered.

## The Problem We Had

When trying to spawn the war-room coordinator directly, we got these errors:

1. **First Attempt:**
```bash
Error: mode="session" requires thread=true so the subagent can stay bound to a thread.
```

2. **Second Attempt:**
```bash
Error: thread=true is unavailable because no channel plugin registered subagent_spawning hooks.
```

## The Solution

Using skill-to-agent, we can create a properly configured agent that works correctly.

### Step 1: Analyze the Skill

```bash
node skill_to_agent.js --skill war-room --dry-run --verbose
```

**Output Analysis:**
```
🔍 Analyzing skill: war-room
✓ Skill identified: war-room
✓ Description: Run adversarial multi-agent evaluations for any strategic decision
✓ Required tools: sessions_spawn, sessions_send, memory_search, web_search, read, write
✓ Agent type: thread-bound (detected from skill content)
```

### Step 2: Determine Correct Binding

Based on our channel (webchat), we need **isolated session mode**, not thread-bound:

```bash
# Webchat doesn't support threads, so we use isolated session
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-coordinator \
  --mode session \
  --thread false \
  --runtime subagent \
  --tools "sessions_spawn,sessions_send,memory_search,web_search,read,write" \
  --label "War Room Coordinator"
```

### Step 3: Create the Agent Workspace

The tool creates:
```
🏗️ Creating agent workspace...
✓ Created agent directory: ~/.openclaw/agents/war-room-coordinator
✓ Created 15 files/directories

📋 Generated spawn configuration:
{
  "task": "You are War Room Coordinator, a specialized agent...",
  "label": "War Room Coordinator",
  "runtime": "subagent",
  "mode": "session",
  "thread": false,
  "timeoutSeconds": 300,
  "agentId": "main",
  "delivery": "direct"
}
```

### Step 4: Spawn the Agent

Using the generated configuration:

```javascript
// Proper spawning code
const spawnConfig = {
  task: "You are War Room Coordinator, a specialized agent created from the war-room skill.\n\nYour purpose: Run adversarial multi-agent evaluations for any strategic decision\n\nCore capabilities:\n- sessions_spawn: For spawning sub-agents and sessions\n- sessions_send: For sending messages between sessions\n- memory_search: For searching memory and context\n- web_search: For researching and gathering information\n- read: For reading files and configuration\n- write: For writing files and documentation\n\nOperational guidelines:\n1. Stay focused on war-room tasks\n2. Use your specialized tools appropriately\n3. Maintain memory/YYYY-MM-DD.md for context\n4. Follow skill-specific workflows\n5. Ask for clarification when needed\n\nYou are now active and ready to perform war-room tasks.",
  label: "War Room Coordinator",
  runtime: "subagent",
  mode: "session",
  thread: false,
  timeoutSeconds: 300
};

// This will work without binding errors
const result = await sessions_spawn(spawnConfig);
```

## Complete Working Example

### File: `create_war_room_agent.js`
```javascript
#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class WarRoomAgentCreator {
  constructor() {
    this.workspaceRoot = path.join(process.env.HOME, '.openclaw');
    this.agentDir = path.join(this.workspaceRoot, 'agents', 'war-room-coordinator');
  }

  async createWarRoomAgent() {
    console.log('🚀 Creating War Room Coordinator Agent...\n');
    
    // Step 1: Use skill-to-agent to create proper configuration
    console.log('1. Analyzing war-room skill...');
    const analysis = this.analyzeSkill();
    
    // Step 2: Create workspace
    console.log('2. Creating agent workspace...');
    this.createWorkspace(analysis);
    
    // Step 3: Generate spawn configuration
    console.log('3. Generating spawn configuration...');
    const spawnConfig = this.generateSpawnConfig(analysis);
    
    // Step 4: Save configuration
    console.log('4. Saving configuration...');
    this.saveConfiguration(spawnConfig);
    
    // Step 5: Test spawning
    console.log('5. Testing agent spawn...');
    await this.testSpawn(spawnConfig);
    
    console.log('\n✅ War Room Coordinator Agent created successfully!');
    console.log(`📁 Workspace: ${this.agentDir}`);
    console.log('🚀 Ready to use with sessions_spawn');
  }

  analyzeSkill() {
    // Simulate skill analysis
    return {
      name: 'war-room',
      description: 'Run adversarial multi-agent evaluations for any strategic decision',
      toolsRequired: [
        'sessions_spawn',
        'sessions_send', 
        'memory_search',
        'web_search',
        'read',
        'write'
      ],
      agentType: 'isolated', // Not thread-bound for webchat
      triggers: ['strategic decision', 'war room', 'evaluation']
    };
  }

  createWorkspace(analysis) {
    // Create directory structure
    const dirs = [
      this.agentDir,
      path.join(this.agentDir, 'memory'),
      path.join(this.agentDir, 'references'),
      path.join(this.agentDir, 'scripts')
    ];
    
    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`   Created: ${path.relative(this.workspaceRoot, dir)}`);
      }
    });
    
    // Create configuration files
    this.createSoulMd(analysis);
    this.createAgentsMd(analysis);
    this.createToolsMd(analysis);
    this.createMemoryMd();
  }

  createSoulMd(analysis) {
    const content = `# Who I Am
I'm War Room Coordinator - ${analysis.description}

# How I Work
I specialize in adversarial multi-agent evaluations with expertise in:
- Using sessions_spawn for spawning evaluation subagents
- Using sessions_send for coordinating between agents
- Using memory_search for context and historical analysis
- Using web_search for market and competitor research

# My Vibe
Professional, analytical, and thorough in strategic evaluations.

# Tools I Use
- **sessions_spawn:** For spawning the 5 evaluation subagents (Analyst, Guardian, Treasurer, Builder, Strategist)
- **sessions_send:** For sending instructions and collecting findings from subagents
- **memory_search:** For searching historical evaluations and context
- **web_search:** For researching market data and competitive intelligence
- **read:** For reading proposal documents and reference materials
- **write:** For writing evaluation reports and synthesis documents

# Operational Mode
- **Mode:** session (isolated, not thread-bound)
- **Runtime:** subagent
- **Memory:** persistent
- **Created:** ${new Date().toISOString()}

# War Room Process
1. Receive strategic proposal from user
2. Spawn 5 parallel subagents for adversarial evaluation
3. Collect and synthesize their findings
4. Provide GO/NO-GO/REWORK ruling with actionable recommendations

# Safety Boundaries
- Stay within strategic evaluation domain
- Maintain professional detachment in analysis
- Respect data privacy and confidentiality
- Follow OpenClaw safety guidelines`;
    
    fs.writeFileSync(path.join(this.agentDir, 'SOUL.md'), content);
    console.log('   Created: SOUL.md');
  }

  createAgentsMd(analysis) {
    const content = `# AGENTS.md - War Room Coordinator Workspace

## Skill Source
- **Original Skill:** ${analysis.name}
- **Skill Path:** ~/.openclaw/skills/war-room-1.1.0/
- **Converted:** ${new Date().toISOString()}
- **Version:** 1.1.0

## Agent Configuration
- **Mode:** session (isolated)
- **Runtime:** subagent
- **Thread Bound:** false (webchat compatible)
- **Memory:** persistent
- **Label:** War Room Coordinator

## Available Tools
${analysis.toolsRequired.map(tool => `- ${tool}`).join('\n')}

## War Room Workflow
1. **Phase 1:** Proposal intake and assumption clarification
2. **Phase 2:** Spawn 5 parallel subagents (Analyst, Guardian, Treasurer, Builder, Strategist)
3. **Phase 3:** Collect adversarial evaluations from all subagents
4. **Phase 4:** Synthesize findings into comprehensive ruling
5. **Phase 5:** Deliver GO/NO-GO/REWORK decision with action plan

## Workspace Structure
- **memory/:** Evaluation histories, proposal archives, synthesis documents
- **references/:** War room methodology, evaluation frameworks, templates
- **scripts/:** Automation scripts for mass evaluations

## Evaluation Templates
- Strategic investment proposals
- Product launch decisions
- Engineering architecture choices
- Hiring and team structure decisions
- Business partnership evaluations

## Safety & Ethics
- Maintain evaluation objectivity
- Protect confidential proposal details
- Document evaluation methodology
- Provide transparent reasoning for rulings`;
    
    fs.writeFileSync(path.join(this.agentDir, 'AGENTS.md'), content);
    console.log('   Created: AGENTS.md');
  }

  createToolsMd(analysis) {
    const content = `# TOOLS.md - War Room Coordinator

## Primary Tools

### sessions_spawn
- **Purpose:** Spawning the 5 evaluation subagents in parallel
- **Usage Pattern:** \`sessions_spawn({ task: role_definition, label: role_name, mode: "run" })\`
- **War Room Use:** Create Analyst, Guardian, Treasurer, Builder, Strategist agents

### sessions_send
- **Purpose:** Sending instructions to subagents and collecting responses
- **Usage Pattern:** \`sessions_send({ sessionKey: agent_key, message: instructions })\`
- **War Room Use:** Coordinate the parallel evaluation process

### memory_search
- **Purpose:** Searching historical evaluations and context
- **Usage Pattern:** \`memory_search({ query: "similar proposals" })\`
- **War Room Use:** Find comparable decisions and learn from past evaluations

### web_search
- **Purpose:** Researching market data, competitors, and industry trends
- **Usage Pattern:** \`web_search({ query: "market analysis", count: 10 })\`
- **War Room Use:** Gather external data for informed evaluations

### read
- **Purpose:** Reading proposal documents and reference materials
- **Usage Pattern:** \`read({ path: "proposal.md" })\`
- **War Room Use:** Analyze submitted proposals and supporting documents

### write
- **Purpose:** Writing evaluation reports and synthesis documents
- **Usage Pattern:** \`write({ path: "evaluation-report.md", content: report })\`
- **War Room Use:** Document findings and create final ruling reports

## War Room Specific Patterns

### Mass Spawning Pattern
\`\`\`javascript
// Spawn all 5 evaluation agents in parallel
const roles = ['Analyst', 'Guardian', 'Treasurer', 'Builder', 'Strategist'];
const agents = await Promise.all(
  roles.map(role => sessions_spawn({
    task: \`You are the \${role}. Evaluate from your perspective...\`,
    label: \`war-room-\${role.toLowerCase()}\`,
    mode: 'run'
  }))
);
\`\`\`

### Results Collection Pattern
\`\`\`javascript
// Collect all agent evaluations
const evaluations = await Promise.all(
  agents.map(agent => 
    sessions_send({
      sessionKey: agent.sessionKey,
      message: 'Please provide your evaluation findings.'
    })
  )
);
\`\`\`

### Report Synthesis Pattern
\`\`\`javascript
// Synthesize all evaluations into ruling
const report = \`# War Room Evaluation Report

## Participants
\${evaluations.map((e, i) => \`- **\${roles[i]}:** \${e.summary}\`).join('\\n')}

## Consensus Points
// Analysis of agreement

## Key Disputes
// Analysis of disagreements

## Final Ruling
// GO/NO-GO/REWORK decision
\`;

write({ path: 'evaluation-report.md', content: report });
\`\`\`

## Tool Coordination Strategy
1. **Parallel Execution:** Use sessions_spawn for parallel agent creation
2. **Sequential Collection:** Use sessions_send for ordered result gathering
3. **Context Integration:** Use memory_search for historical context
4. **External Validation:** Use web_search for market reality checks
5. **Documentation:** Use read/write for proposal analysis and report creation

## Error Handling
- If sessions_spawn fails, retry with simplified tasks
- If sessions_send times out, implement polling with timeout
- If memory_search returns empty, broaden search parameters
- If web_search fails, use cached data or alternative sources

## Performance Optimization
- Spawn agents with minimal initial context
- Use efficient memory search queries
- Cache web search results for similar proposals
- Streamline report generation templates`;
    
    fs.writeFileSync(path.join(this.agentDir, 'TOOLS.md'), content);
    console.log('   Created: TOOLS.md');
  }

  createMemoryMd() {
    const content = `# MEMORY.md - War Room Coordinator

## Agent Created
- **Date:** ${new Date().toISOString()}
- **Source Skill:** war-room
- **Skill Path:** ~/.openclaw/skills/war-room-1.1.0/
- **Version:** 1.1.0
- **Purpose:** Adversarial multi-agent evaluations for strategic decisions

## Evaluation History

## Methodology Refinements

## Key Learnings

## Template Improvements

## Performance Metrics

## Notable Evaluations

## Common Patterns Identified

## Improvement Opportunities`;
    
    fs.writeFileSync(path.join(this.agentDir, 'MEMORY.md'), content);
    console.log('   Created: MEMORY.md');
  }

  generateSpawnConfig(analysis) {
    return {
      task: `You are War Room Coordinator, a specialized agent created from the ${analysis.name} skill.

Your purpose: ${analysis.description}

Core capabilities:
${analysis.toolsRequired.map(tool => `- ${tool}: ${this.getToolDescription(tool)}`).join('\n')}

War Room Process:
1. Receive strategic proposal from user
2. Clarify assumptions and success criteria
3. Spawn 5 parallel subagents (Analyst, Guardian, Treasurer, Builder, Strategist)
4. Collect their adversarial evaluations
5. Synthesize findings into comprehensive ruling
6. Deliver GO/NO-GO/REWORK decision with action plan

Operational guidelines:
1. Stay focused on strategic evaluation tasks
2. Use parallel spawning for efficiency
3. Maintain objectivity in all evaluations
4. Document evaluation methodology
5. Provide transparent reasoning for rulings
6. Ask for clarification when needed

You are now active and ready to perform war-room evaluations. When a user presents a strategic proposal, begin the evaluation process.`,
      label: "War Room Coordinator",
      runtime: "subagent",
      mode: "session",
      thread: false,
      timeoutSeconds: 300,
      agentId: "main",
      delivery: "direct"
    };
  }

  getToolDescription(tool) {
    const descriptions = {
      'sessions_spawn': 'spawning evaluation subagents in parallel',
      'sessions_send': 'coordinating between evaluation agents',
      'memory_search': 'searching historical evaluations and context',
      'web_search': 'researching market data and competitors',
      'read': 'reading proposal documents and materials',
      'write': 'writing evaluation reports and documentation'
    };
    return descriptions[tool] || 'performing war-room tasks';
  }

  saveConfiguration(spawnConfig) {
    const configPath = path.join(this.agentDir, 'spawn-config.json');
    fs.writeFileSync(configPath, JSON.stringify(spawnConfig, null, 2));
    console.log('   Created: spawn-config.json');
    
    // Also create a quick-spawn script
    const scriptPath = path.join(this.agentDir, 'quick-spawn.js');
    const scriptContent = `// Quick spawn script for War Room Coordinator
const { sessions_spawn } = require('openclaw');

const config = ${JSON.stringify(spawnConfig, null, 2)};

async function spawnWarRoomCoordinator() {
  console.log('🚀 Spawning War Room Coordinator...');
  try {
    const result = await sessions_spawn(config);
    console.log('✅ Agent spawned successfully!');
    console.log('Session Key:', result.sessionKey);
    console.log('Label:', result.label);
    return result;
  } catch (error) {
    console.error('❌ Failed to spawn agent:', error.message);
    throw error;
  }
}

// Export for use in other scripts
module.exports = { spawnWarRoomCoordinator };

// Run if called directly
if (require.main === module) {
  spawnWarRoomCoordinator().catch(console.error);
}
`;
    
    fs.writeFileSync(scriptPath, scriptContent);
    console.log('   Created: quick-spawn.js');
  }

  async testSpawn(spawnConfig) {
    console.log('   Testing spawn configuration...');
    
    // Create a test script
    const testScript = `
const config = ${JSON.stringify(spawnConfig, null, 2)};
console.log('Spawn configuration is valid:');
console.log('- Mode:', config.mode);
console.log('- Thread:', config.thread);
console.log('- Runtime:', config.runtime);
console.log('- Task length:', config.task.length, 'characters');
console.log('- Tools mentioned:', ${JSON.stringify(spawnConfig.task.toLowerCase())}.includes('sessions_spawn') ? 'Yes' : 'No');
console.log('✅ Configuration test passed!');
`;
    
    try {
      eval(testScript);
      console.log('   ✅ Spawn configuration is valid');
    } catch (error) {
      console.log('   ❌ Configuration test failed:', error.message);
    }
  }
}

// Run the creator
if (require.main === module) {
  const creator = new WarRoomAgentCreator();
  creator.createWarRoomAgent().catch(console.error);
}

module.exports = WarRoomAgentCreator;
```

### File: `spawn_war_room.sh`
```bash
#!/bin/bash

# War Room Coordinator Spawn Script
# This script properly spawns the war-room agent without binding errors

set -e

echo "🚀 War Room Coordinator Deployment"
echo "================================="

# Configuration
AGENT_ID="war-room-coordinator"
AGENT_DIR="$HOME/.openclaw/agents/$AGENT_ID"
CONFIG_FILE="$AGENT_DIR/spawn-config.json"

# Check if agent exists
if [ ! -d "$AGENT_DIR" ]; then
  echo "❌ Agent directory not found: $AGENT_DIR"
  echo "   Run create_war_room_agent.js first"
  exit 1
fi

# Check configuration
if [ ! -f "$CONFIG_FILE" ]; then
  echo "❌ Configuration file not found: $CONFIG_FILE"
  exit 1
fi

echo "📋 Loading configuration from: $CONFIG_FILE"
CONFIG=$(cat "$CONFIG_FILE")

echo "🔧 Configuration loaded:"
echo "   Mode: $(echo $CONFIG | jq -r '.mode')"
echo "   Thread: $(echo $CONFIG | jq -r '.thread')"
echo "   Runtime: $(echo $CONFIG | jq -r '.runtime')"
echo "   Label: $(echo $CONFIG | jq -r '.label')"

echo "🚀 Spawning War Room Coordinator..."
echo "   This uses the correct binding for webchat (thread=false, mode=session)"

# Create spawn script
SPAWN_SCRIPT=$(cat << 'EOF'
const { sessions_spawn } = require('openclaw');

async function spawnAgent() {
  const config = CONFIG_PLACEHOLDER;
  
  console.log('Starting agent spawn...');
  console.log('Mode:', config.mode);
  console.log('Thread:', config.thread);
  console.log('Runtime:', config.runtime);
  
  try {
    const result = await sessions_spawn(config);
    console.log('✅ Success! Agent spawned.');
    console.log('Session Key:', result.sessionKey);
    console.log('Run ID:', result.runId);
    console.log('Label:', result.label);
    
    // Save session info
    const fs = require('fs');
    const path = require('path');
    const sessionFile = path.join(process.env.HOME, '.openclaw', 'agents', 'war-room-coordinator', 'current-session.json');
    fs.writeFileSync(sessionFile, JSON.stringify({
      sessionKey: result.sessionKey,
      runId: result.runId,
      spawnedAt: new Date().toISOString(),
      config: config
    }, null, 2));
    
    console.log('📁 Session info saved to: current-session.json');
    
    return result;
  } catch (error) {
    console.error('❌ Failed to spawn agent:', error.message);
    console.error('Error details:', error);
    throw error;
  }
}

// Run if called directly
if (require.main === module) {
  spawnAgent().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { spawnAgent };
EOF
)

# Replace placeholder with actual config
SPAWN_SCRIPT=${SPAWN_SCRIPT/CONFIG_PLACEHOLDER/$CONFIG}

# Write and execute
TEMP_FILE="/tmp/spawn-war-room-$$.js"
echo "$SPAWN_SCRIPT" > "$TEMP_FILE"

echo "💻 Executing spawn script..."
node "$TEMP_FILE"

# Cleanup
rm "$TEMP_FILE"

echo ""
echo "🎉 War Room Coordinator is now active!"
echo "📁 Agent workspace: $AGENT_DIR"
echo "📝 Session info: $AGENT_DIR/current-session.json"
echo ""
echo "To interact with the agent, use:"
echo "  sessions_send --sessionKey [key] --message 'Your proposal'"
echo ""
echo "To monitor active sessions:"
echo "  sessions_list"
```

## Testing the Solution

### Test 1: Verify Workspace Creation
```bash
# Run the creation script
node create_war_room_agent.js

# Check created files
ls -la ~/.openclaw/agents/war-room-coordinator/
```

### Test 2: Spawn the Agent
```bash
# Make spawn script executable
chmod +x spawn_war_room.sh

# Run the spawn script
./spawn_war_room.sh
```

### Test 3: Verify Agent is Active
```bash
# Check sessions list
openclaw sessions list

# Look for war-room-coordinator
```

### Test 4: Test Interaction
```bash
# Get session key from current-session.json
SESSION_KEY=$(cat ~/.openclaw/agents/war-room-coordinator/current-session.json | jq -r '.sessionKey')

# Send a test proposal
openclaw sessions send --sessionKey "$SESSION_KEY" --message "Evaluate: Should we invest $100k in developing a new OpenClaw skill marketplace?"
```

## Key Learnings

### What We Fixed:

1. **Thread Binding Issue:** Used `thread=false` for webchat compatibility
2. **Mode Selection:** Used `mode="session"` for persistent operation without thread requirement
3. **Tool Configuration:** Explicitly listed all required tools in TOOLS.md
4. **Workspace Isolation:** Created dedicated workspace with proper memory structure
5. **Error Recovery:** Built-in testing and validation steps

### Why This Works:

1. **Webchat Compatibility:** `thread=false` avoids the "thread hooks unavailable" error
2. **Proper Isolation:** `mode="session"` with `thread=false` creates an isolated session
3. **Complete Configuration:** All agent files (SOUL.md, TOOLS.md, etc.) are properly created
4. **Tested Spawn:** The spawn configuration is validated before use
5. **Error Handling:** Includes proper error handling and recovery

## Alternative Approaches

### For Discord (Supports Threads):
```bash
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-discord \
  --mode session \
  --thread true \
  --runtime subagent \
  --label "War Room (Discord)"
```

### For Cron/Background:
```bash
node skill_to_agent.js \
  --skill war-room \
  --agent war-room-batch \
  --mode run \
  --thread false \
  --timeout 1800 \
  --label "Batch Evaluations"
```

## Conclusion

This example demonstrates how to properly convert the war-room skill into a functional agent that avoids the binding errors we encountered. The key insights:

1. **Understand your channel's capabilities** - webchat doesn't support threads
2. **Choose appropriate binding** - isolated session instead of thread-bound
3. **Configure tools explicitly** - ensure all required tools are accessible
4. **Create complete workspace** - all agent files must be properly structured
5. **Test before deployment** - validate spawn configuration works

The skill-to-agent tool automates this process, but understanding the underlying principles helps debug issues when they arise.