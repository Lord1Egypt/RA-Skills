#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const DEFAULT_AGENTS_DIR = path.join(os.homedir(), '.openclaw', 'agents');

function parseArgs(argv) {
  const args = {
    path: null,
    agent: null,
    offset: null,
    format: 'text',
    details: false,
    detailsSessionId: null,
    provider: null,
    table: false,
    help: false
  };
  let i = 0;

  while (i < argv.length) {
    if (argv[i] === '--help' || argv[i] === '-h') {
      args.help = true;
    } else if (argv[i] === '--offset' && i + 1 < argv.length) {
      args.offset = argv[++i];
    } else if (argv[i] === '--format' && i + 1 < argv.length) {
      args.format = argv[++i];
    } else if (argv[i] === '--json') {
      args.format = 'json';  // backwards compat
    } else if (argv[i] === '--path' && i + 1 < argv.length) {
      args.path = argv[++i];
    } else if (argv[i] === '--provider' && i + 1 < argv.length) {
      args.provider = argv[++i].toLowerCase();
    } else if (argv[i] === '--agent' && i + 1 < argv.length) {
      args.agent = argv[++i].toLowerCase();
    } else if (argv[i] === '--table') {
      args.table = true;
    } else if (argv[i] === '--details') {
      args.details = true;
      if (i + 1 < argv.length && !argv[i + 1].startsWith('-')) {
        args.detailsSessionId = argv[++i];
      }
    }
    i++;
  }

  return args;
}

function parseTimeOffset(offsetStr) {
  if (!offsetStr) return null;

  const match = offsetStr.match(/^(\d+)([mhd])$/);
  if (!match) {
    console.error('Invalid time format. Use: 30m, 2h, 7d');
    process.exit(1);
  }

  const value = parseInt(match[1]);
  const unit = match[2];

  let ms;
  switch (unit) {
    case 'm': ms = value * 60 * 1000; break;
    case 'h': ms = value * 60 * 60 * 1000; break;
    case 'd': ms = value * 24 * 60 * 60 * 1000; break;
  }

  return Date.now() - ms;
}

function discoverAgents(agentsDir) {
  if (!fs.existsSync(agentsDir)) return [];
  const agents = [];
  try {
    const entries = fs.readdirSync(agentsDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const sessionsPath = path.join(agentsDir, entry.name, 'sessions');
      if (fs.existsSync(sessionsPath)) {
        agents.push({ name: entry.name, sessionsPath });
      }
    }
  } catch (err) {
    // Permission errors, etc.
  }
  return agents;
}

function agentNameFromPath(dirPath) {
  const normalized = path.resolve(dirPath);
  const parts = normalized.split(path.sep);
  // Detect .../agents/<name>/sessions pattern
  for (let i = 0; i < parts.length; i++) {
    if (parts[i] === 'agents' && i + 2 < parts.length && parts[i + 2] === 'sessions') {
      return parts[i + 1];
    }
  }
  if (parts[parts.length - 1] === 'sessions' && parts.length >= 2) {
    return parts[parts.length - 2];
  }
  return path.basename(normalized);
}

function findJsonlFiles(dirPath) {
  const files = [];

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile()
                 && entry.name.endsWith('.jsonl')
                 && !entry.name.endsWith('.trajectory.jsonl')) {
        files.push(fullPath);
      }
    }
  }

  walk(dirPath);
  return files;
}

function analyzeSession(filePath, cutoffTime, agentName) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n').filter(l => l.trim());

  const usage = {
    input: 0,
    output: 0,
    cacheRead: 0,
    cacheWrite: 0,
    totalTokens: 0,
    costInput: 0,
    costOutput: 0,
    costCacheRead: 0,
    costCacheWrite: 0,
    costTotal: 0
  };

  let api = null;
  let model = null;
  let provider = null;
  let sessionId = null;
  let firstTimestamp = null;
  let lastTimestamp = null;
  let assistantMessageCount = 0;

  for (const line of lines) {
    try {
      const record = JSON.parse(line);

      if (record.type === 'session') {
        sessionId = record.id;
      }

      if (record.timestamp) {
        const ts = new Date(record.timestamp).getTime();
        if (!firstTimestamp || ts < firstTimestamp) firstTimestamp = ts;
        if (!lastTimestamp || ts > lastTimestamp) lastTimestamp = ts;
      }

      if (record.type === 'message' && record.message?.usage) {
        const msg = record.message;

        const u = msg.usage;
        usage.input += u.input || 0;
        usage.output += u.output || 0;
        usage.cacheRead += u.cacheRead || 0;
        usage.cacheWrite += u.cacheWrite || 0;
        usage.totalTokens += u.totalTokens || 0;

        if (u.cost) {
          usage.costInput += u.cost.input || 0;
          usage.costOutput += u.cost.output || 0;
          usage.costCacheRead += u.cost.cacheRead || 0;
          usage.costCacheWrite += u.cost.cacheWrite || 0;
          usage.costTotal += u.cost.total || 0;
        }

        // Capture model/provider from any message with usage; prefer non-zero cost if available
        if (msg.api) api = msg.api;
        if (msg.model) model = msg.model;
        if (msg.provider) provider = msg.provider;

        if (msg.role === 'assistant') {
          assistantMessageCount++;
        }
      }
    } catch (err) {
      // Skip malformed lines
    }
  }

  if (cutoffTime && firstTimestamp && firstTimestamp < cutoffTime) {
    return null;
  }

  return {
    file: path.basename(filePath),
    fullPath: filePath,
    agent: agentName || 'unknown',
    sessionId,
    api: api || 'unknown',
    provider: provider || 'unknown',
    model: model || 'unknown',
    usage,
    assistantMessageCount,
    firstTimestamp: firstTimestamp ? new Date(firstTimestamp).toISOString() : null,
    lastTimestamp: lastTimestamp ? new Date(lastTimestamp).toISOString() : null,
    durationMin: firstTimestamp && lastTimestamp ?
      Math.round((lastTimestamp - firstTimestamp) / 1000 / 60) : 0
  };
}

function sumUsage(sessions) {
  return sessions.reduce((acc, r) => ({
    input: acc.input + r.usage.input,
    output: acc.output + r.usage.output,
    cacheRead: acc.cacheRead + r.usage.cacheRead,
    cacheWrite: acc.cacheWrite + r.usage.cacheWrite,
    totalTokens: acc.totalTokens + r.usage.totalTokens,
    costInput: acc.costInput + r.usage.costInput,
    costOutput: acc.costOutput + r.usage.costOutput,
    costCacheRead: acc.costCacheRead + r.usage.costCacheRead,
    costCacheWrite: acc.costCacheWrite + r.usage.costCacheWrite,
    costTotal: acc.costTotal + r.usage.costTotal,
    assistantMessageCount: acc.assistantMessageCount + (r.assistantMessageCount || 0)
  }), {
    input: 0, output: 0, cacheRead: 0, cacheWrite: 0, totalTokens: 0,
    costInput: 0, costOutput: 0, costCacheRead: 0, costCacheWrite: 0, costTotal: 0,
    assistantMessageCount: 0
  });
}

function groupByModel(results) {
  const groups = {};
  for (const r of results) {
    const key = `${r.provider}/${r.model}`;
    if (!groups[key]) groups[key] = [];
    groups[key].push(r);
  }
  return groups;
}

function groupByAgent(results) {
  const groups = {};
  for (const r of results) {
    if (!groups[r.agent]) groups[r.agent] = [];
    groups[r.agent].push(r);
  }
  return groups;
}

function formatTokens(tokens) {
  if (tokens >= 1000000) {
    return (tokens / 1000000).toFixed(1) + 'M';
  } else if (tokens >= 1000) {
    return (tokens / 1000).toFixed(1) + 'K';
  }
  return tokens.toString();
}

function printTableHeader(multiAgent) {
  if (multiAgent) {
    console.log('Agent'.padEnd(15) + 'Model'.padEnd(35) + 'Duration'.padEnd(12) + 'Tokens'.padEnd(14) + 'Cache'.padEnd(20) + 'Cost'.padEnd(12) + 'Session');
    console.log('─'.repeat(140));
  } else {
    console.log('Model'.padEnd(35) + 'Duration'.padEnd(12) + 'Tokens'.padEnd(14) + 'Cache'.padEnd(20) + 'Cost'.padEnd(12) + 'Session');
    console.log('─'.repeat(125));
  }
}

function printTableRow(result, multiAgent) {
  const session = (result.sessionId || 'unknown').slice(0, 32);
  const model = `${result.provider}/${result.model}`.slice(0, 32);
  const duration = `${result.durationMin} min`;
  const tokens = formatTokens(result.usage.totalTokens);
  const cache = `${formatTokens(result.usage.cacheRead)} / ${formatTokens(result.usage.cacheWrite)}`;
  const cost = `$${result.usage.costTotal.toFixed(4)}`;

  if (multiAgent) {
    const agent = result.agent.slice(0, 12);
    console.log(
      agent.padEnd(15) +
      model.padEnd(35) +
      duration.padEnd(12) +
      tokens.padEnd(14) +
      cache.padEnd(20) +
      cost.padEnd(12) +
      session
    );
  } else {
    console.log(
      model.padEnd(35) +
      duration.padEnd(12) +
      tokens.padEnd(14) +
      cache.padEnd(20) +
      cost.padEnd(12) +
      session
    );
  }
}

function printModelSummary(label, sessions, totals, indent) {
  const p = indent || '';
  const tokensUnreported =
    totals.totalTokens === 0 && totals.assistantMessageCount > 0;
  const suffix = tokensUnreported ? ' (not reported by model)' : '';
  console.log(`\n${p}${label}`);
  console.log(p + '-'.repeat(80));
  console.log(`${p}  Sessions: ${sessions.length}`);
  console.log(`${p}  Tokens:   ${totals.totalTokens.toLocaleString()}${suffix} (input: ${totals.input.toLocaleString()}, output: ${totals.output.toLocaleString()})`);
  console.log(`${p}  Cache:    read: ${totals.cacheRead.toLocaleString()} tokens, write: ${totals.cacheWrite.toLocaleString()} tokens${suffix}`);
  console.log(`${p}  Cost:     $${totals.costTotal.toFixed(4)}`);
  console.log(`${p}    Input:       $${totals.costInput.toFixed(4)}`);
  console.log(`${p}    Output:      $${totals.costOutput.toFixed(4)}`);
  console.log(`${p}    Cache read:  $${totals.costCacheRead.toFixed(4)}  (included in total, discounted rate)`);
  console.log(`${p}    Cache write: $${totals.costCacheWrite.toFixed(4)}  (included in total)`);
}

function buildUsageSummary(sessions, totals) {
  return {
    sessions: sessions.length,
    tokens: { input: totals.input, output: totals.output, total: totals.totalTokens },
    cache: { read: totals.cacheRead, write: totals.cacheWrite },
    cost: {
      total: round4(totals.costTotal),
      input: round4(totals.costInput),
      output: round4(totals.costOutput),
      cacheRead: round4(totals.costCacheRead),
      cacheWrite: round4(totals.costCacheWrite)
    }
  };
}

function buildJsonOutput(results, offset) {
  const agentGroups = groupByAgent(results);
  const agentNames = Object.keys(agentGroups);

  const agents = {};
  for (const [agentName, agentSessions] of Object.entries(agentGroups)) {
    const models = groupByModel(agentSessions);
    const modelSummaries = {};
    for (const [model, sessions] of Object.entries(models)) {
      const totals = sumUsage(sessions);
      modelSummaries[model] = buildUsageSummary(sessions, totals);
    }
    const agentTotals = sumUsage(agentSessions);
    agents[agentName] = {
      models: modelSummaries,
      totals: buildUsageSummary(agentSessions, agentTotals)
    };
  }

  const output = { agents };

  const totalModels = Object.values(agentGroups)
    .reduce((sum, sessions) => sum + Object.keys(groupByModel(sessions)).length, 0);
  if (agentNames.length > 1 || totalModels > 1) {
    const grandTotals = sumUsage(results);
    output.grandTotal = buildUsageSummary(results, grandTotals);
  }

  if (offset) output.offset = offset;

  return output;
}

function round4(n) {
  return Math.round(n * 10000) / 10000;
}

function formatDiscord(results, offset) {
  const lines = [];

  // Header with emoji
  lines.push('💰 **Usage Summary**');
  if (offset) {
    lines.push(`(last ${offset})`);
  }
  lines.push('');

  // Grand totals
  const grandTotals = sumUsage(results);
  lines.push(`**Total Cost:** $${grandTotals.costTotal.toFixed(2)}`);
  lines.push(`**Total Tokens:** ${formatTokens(grandTotals.totalTokens)}`);
  lines.push(`**Sessions:** ${results.length}`);

  // Group by agent
  const byAgent = groupByAgent(results);
  if (Object.keys(byAgent).length > 1) {
    lines.push('');
    lines.push('**By Agent:**');
    for (const [agent, sessions] of Object.entries(byAgent)) {
      const totals = sumUsage(sessions);
      lines.push(`• ${agent}: $${totals.costTotal.toFixed(2)} (${sessions.length} sessions)`);
    }
  }

  // Group by provider
  const byProvider = {};
  for (const r of results) {
    const p = r.provider;
    if (!byProvider[p]) {
      byProvider[p] = [];
    }
    byProvider[p].push(r);
  }

  if (Object.keys(byProvider).length > 1) {
    lines.push('');
    lines.push('**By Provider:**');
    for (const [provider, sessions] of Object.entries(byProvider)) {
      const totals = sumUsage(sessions);
      lines.push(`• ${provider}: $${totals.costTotal.toFixed(2)} (${formatTokens(totals.totalTokens)} tokens)`);
    }
  }

  // Top models (limit to 5)
  const modelGroups = groupByModel(results);
  const modelEntries = Object.entries(modelGroups)
    .map(([model, sessions]) => ({
      model,
      totals: sumUsage(sessions)
    }))
    .sort((a, b) => b.totals.costTotal - a.totals.costTotal)
    .slice(0, 5);

  if (modelEntries.length > 0) {
    lines.push('');
    lines.push('**Top Models:**');
    for (const entry of modelEntries) {
      lines.push(`• ${entry.model}: $${entry.totals.costTotal.toFixed(2)} (${formatTokens(entry.totals.totalTokens)} tokens)`);
    }
  }

  return lines.join('\n');
}

function printHelp() {
  console.log('Usage: node session-cost.js [options]');
  console.log('');
  console.log('Analyze OpenClaw session logs for token usage, costs, and performance metrics.');
  console.log('By default, scans all agents in ~/.openclaw/agents/.');
  console.log('');
  console.log('Options:');
  console.log('  --path <dir>         Directory to scan for .jsonl files (overrides agent discovery)');
  console.log('  --agent <name>       Filter by agent name (e.g., main, codegen)');
  console.log('  --offset <time>      Only include sessions from the last N units (30m, 2h, 7d)');
  console.log('  --provider <name>    Filter by model provider (anthropic, openai, ollama, etc.)');
  console.log('  --details [id]       Show per-session details. Optionally specify a session ID');
  console.log('                       to show only that session (searches across all agents)');
  console.log('  --table              Show details in compact table format (use with --details)');
  console.log('  --format <type>      Output format: text (default), json, or discord');
  console.log('  --json               Shorthand for --format json (backwards compat)');
  console.log('  --help, -h           Show this help message');
  console.log('');
  console.log('Examples:');
  console.log('  node session-cost.js                          # Summary across all agents');
  console.log('  node session-cost.js --agent main             # Only main agent sessions');
  console.log('  node session-cost.js --details --table        # All sessions in table format');
  console.log('  node session-cost.js --details abc123         # Details for one session');
  console.log('  node session-cost.js --offset 24h             # Last 24 hours summary');
  console.log('  node session-cost.js --provider anthropic     # Only Anthropic sessions');
  console.log('  node session-cost.js --path /other/dir --json # Custom path, JSON output');
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const cutoffTime = parseTimeOffset(args.offset);

  // Determine scan sources
  let agents;
  if (args.path) {
    // Explicit --path: scan exactly that directory
    if (!fs.existsSync(args.path)) {
      console.error(`Error: Path does not exist: ${args.path}`);
      process.exit(1);
    }
    const agentName = agentNameFromPath(args.path);
    agents = [{ name: agentName, sessionsPath: args.path }];
  } else {
    // Auto-discover all agents
    agents = discoverAgents(DEFAULT_AGENTS_DIR);
    if (agents.length === 0) {
      console.error(`Error: No agents found in ${DEFAULT_AGENTS_DIR}`);
      process.exit(1);
    }
  }

  // Apply --agent filter
  if (args.agent) {
    agents = agents.filter(a => a.name.toLowerCase() === args.agent);
    if (agents.length === 0) {
      console.error(`Error: No agent found matching: ${args.agent}`);
      process.exit(1);
    }
  }

  // Single session mode: search across agents for <id>.jsonl
  if (args.detailsSessionId) {
    let sessionFile = null;
    let agentName = null;

    for (const agent of agents) {
      const candidate = path.join(agent.sessionsPath, `${args.detailsSessionId}.jsonl`);
      if (fs.existsSync(candidate)) {
        sessionFile = candidate;
        agentName = agent.name;
        break;
      }
    }

    if (!sessionFile) {
      console.error(`Error: Session file not found: ${args.detailsSessionId}.jsonl`);
      process.exit(1);
    }

    const result = analyzeSession(sessionFile, cutoffTime, agentName);
    if (!result) {
      console.log('Session did not match the time criteria.');
      return;
    }

    if (args.format === 'json') {
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    const unreported = result.usage.totalTokens === 0 && (result.assistantMessageCount || 0) > 0;
    const sfx = unreported ? ' (not reported by model)' : '';
    console.log(`Session: ${result.sessionId || 'unknown'}`);
    console.log(`Agent: ${result.agent}`);
    console.log(`Model: ${result.provider}/${result.model} (${result.api})`);
    console.log(`Duration: ${result.durationMin} minutes`);
    console.log(`Timestamps: ${result.firstTimestamp || 'N/A'} → ${result.lastTimestamp || 'N/A'}`);
    console.log(`Tokens: input=${result.usage.input.toLocaleString()}, output=${result.usage.output.toLocaleString()}, total=${result.usage.totalTokens.toLocaleString()}${sfx}`);
    console.log(`Cache: read=${result.usage.cacheRead.toLocaleString()}, write=${result.usage.cacheWrite.toLocaleString()}`);
    console.log(`Cost: $${result.usage.costTotal.toFixed(4)} (input=$${result.usage.costInput.toFixed(4)}, output=$${result.usage.costOutput.toFixed(4)})`);
    return;
  }

  // Collect all session files across agents
  let totalFiles = 0;
  let results = [];

  for (const agent of agents) {
    const files = findJsonlFiles(agent.sessionsPath);
    totalFiles += files.length;
    for (const file of files) {
      const result = analyzeSession(file, cutoffTime, agent.name);
      if (result) results.push(result);
    }
  }

  if (results.length === 0) {
    if (args.format === 'json') {
      console.log(JSON.stringify({ agents: {}, sessions: 0 }));
    } else {
      console.log('No sessions matched the criteria.');
    }
    return;
  }

  // Filter by provider if specified
  if (args.provider) {
    const originalCount = results.length;
    results = results.filter(r => r.provider.toLowerCase() === args.provider);
    if (results.length === 0 && args.format !== 'json') {
      console.log(`No sessions matched provider filter: ${args.provider}`);
      console.log(`(Found ${originalCount} sessions total, but none matched the provider)`);
      return;
    }
  }

  // Sort by timestamp (newest first)
  results.sort((a, b) => {
    const aTime = a.lastTimestamp || a.firstTimestamp || 0;
    const bTime = b.lastTimestamp || b.firstTimestamp || 0;
    return new Date(bTime) - new Date(aTime);
  });

  const agentGroups = groupByAgent(results);
  const agentNames = Object.keys(agentGroups);
  const multiAgent = agentNames.length > 1;

  // JSON output
  if (args.format === 'json') {
    console.log(JSON.stringify(buildJsonOutput(results, args.offset), null, 2));
    return;
  }

  // Discord output
  if (args.format === 'discord') {
    console.log(formatDiscord(results, args.offset));
    return;
  }

  // Text output
  const filters = [];
  if (args.offset && cutoffTime) {
    filters.push(`sessions from the last ${args.offset} (since ${new Date(cutoffTime).toISOString()})`);
  }
  if (args.provider) {
    filters.push(`provider=${args.provider}`);
  }
  if (args.agent) {
    filters.push(`agent=${args.agent}`);
  }
  if (filters.length > 0) {
    console.log(`Filtering: ${filters.join(', ')}\n`);
  }

  if (multiAgent) {
    console.log(`Found ${totalFiles} .jsonl files across ${agentNames.length} agents, ${results.length} matched\n`);
  } else {
    console.log(`Found ${totalFiles} .jsonl files, ${results.length} matched\n`);
  }

  // Per-session details (only when --details is used)
  if (args.details) {
    console.log('SESSION DETAILS');
    console.log('='.repeat(multiAgent ? 140 : 125));

    if (args.table) {
      printTableHeader(multiAgent);
      for (const r of results) {
        printTableRow(r, multiAgent);
      }
    } else {
      for (const r of results) {
        const unreported = r.usage.totalTokens === 0 && (r.assistantMessageCount || 0) > 0;
        const sfx = unreported ? ' (not reported by model)' : '';
        console.log(`\nSession: ${r.sessionId || 'unknown'}`);
        if (multiAgent) console.log(`Agent: ${r.agent}`);
        console.log(`Model: ${r.provider}/${r.model} (${r.api})`);
        console.log(`Duration: ${r.durationMin} minutes`);
        console.log(`Timestamps: ${r.firstTimestamp || 'N/A'} → ${r.lastTimestamp || 'N/A'}`);
        console.log(`Tokens: input=${r.usage.input.toLocaleString()}, output=${r.usage.output.toLocaleString()}, total=${r.usage.totalTokens.toLocaleString()}${sfx}`);
        console.log(`Cache: read=${r.usage.cacheRead.toLocaleString()}, write=${r.usage.cacheWrite.toLocaleString()}`);
        console.log(`Cost: $${r.usage.costTotal.toFixed(4)} (input=$${r.usage.costInput.toFixed(4)}, output=$${r.usage.costOutput.toFixed(4)})`);
      }
    }
  }

  // Summary grouped by agent, then by model within each agent
  console.log('\n' + '='.repeat(100));
  console.log('SUMMARY BY AGENT');
  console.log('='.repeat(100));

  for (const [agentName, agentSessions] of Object.entries(agentGroups)) {
    console.log(`\nAgent: ${agentName}`);

    const modelGroups = groupByModel(agentSessions);
    for (const [model, sessions] of Object.entries(modelGroups)) {
      const totals = sumUsage(sessions);
      printModelSummary(model, sessions, totals, '  ');
    }
  }

  // Grand total
  const totalModels = Object.values(agentGroups)
    .reduce((sum, sessions) => sum + Object.keys(groupByModel(sessions)).length, 0);
  if (multiAgent || totalModels > 1) {
    console.log('\n' + '='.repeat(100));
    console.log('GRAND TOTAL');
    console.log('='.repeat(100));

    if (multiAgent) {
      for (const [agentName, agentSessions] of Object.entries(agentGroups)) {
        const totals = sumUsage(agentSessions);
        console.log(`  ${agentName.padEnd(20)} — ${agentSessions.length} sessions, $${totals.costTotal.toFixed(4)}`);
      }
      console.log('');
    }

    const grandTotals = sumUsage(results);
    const grandLabel = multiAgent
      ? `All agents (${agentNames.length})`
      : `All models (${totalModels})`;
    printModelSummary(grandLabel, results, grandTotals);
  }
}

main();
