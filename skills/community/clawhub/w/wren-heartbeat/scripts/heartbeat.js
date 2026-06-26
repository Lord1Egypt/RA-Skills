#!/usr/bin/env node
/**
 * Agent Heartbeat — Parallel health checks and data collection for AI agents.
 * 
 * Reads heartbeat.yaml, runs all checks in parallel, writes an LLM-optimized summary.
 * Exit 0 = all clear, Exit 1 = error, Exit 2 = action needed.
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Simple YAML parser (handles the subset we need — no dependency required)
function parseYaml(text) {
  // Use JSON via a quick transform for simple YAML
  // For production, agents can install js-yaml, but this works for our config format
  try {
    // Try native YAML parsing if available
    const yaml = require('yaml');
    return yaml.parse(text);
  } catch {
    // Fallback: simple line-based parser for flat configs
    return simpleYamlParse(text);
  }
}

function simpleYamlParse(text) {
  const result = { collectors: [], health: [], settings: {} };
  let currentSection = null;
  let currentItem = null;

  for (const line of text.split('\n')) {
    const raw = line.trimEnd();
    if (!raw || raw.trimStart().startsWith('#')) continue;

    const indent = raw.length - raw.trimStart().length;
    const trimmed = raw.trimStart();

    if (indent === 0 && trimmed.endsWith(':')) {
      currentSection = trimmed.slice(0, -1);
      currentItem = null;
      continue;
    }

    if (indent === 2 && trimmed.startsWith('- name:')) {
      currentItem = { name: trimmed.slice(7).trim().replace(/^["']|["']$/g, '') };
      if (currentSection === 'collectors') result.collectors.push(currentItem);
      else if (currentSection === 'health') result.health.push(currentItem);
      continue;
    }

    if (indent >= 4 && currentItem) {
      const match = trimmed.match(/^(\w[\w-]*)\s*:\s*(.+)/);
      if (match) {
        let val = match[2].trim();
        // Only strip outer quotes if they form a complete quoted string
        if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
          val = val.slice(1, -1);
        }
        if (match[1] !== 'command') {
          if (val === 'true') val = true;
          else if (val === 'false') val = false;
          else if (/^\d+$/.test(val)) val = parseInt(val);
        }
        currentItem[match[1]] = val;
      }
      continue;
    }

    if (indent === 2 && currentSection === 'settings') {
      const match = trimmed.match(/^(\w[\w-]*)\s*:\s*(.+)/);
      if (match) {
        let val = match[2].trim().replace(/^["']|["']$/g, '');
        if (val === 'true') val = true;
        else if (val === 'false') val = false;
        else if (/^\d+$/.test(val)) val = parseInt(val);
        result.settings[match[1]] = val;
      }
    }
  }
  return result;
}

// Run a single check
function runCheck(check, timeoutMs) {
  return new Promise((resolve) => {
    const start = Date.now();
    try {
      const output = execSync(check.command, {
        encoding: 'utf8',
        timeout: timeoutMs,
        stdio: ['ignore', 'pipe', 'pipe'],
        shell: true,
        env: { ...process.env },
      }).trim();
      resolve({ ...check, ok: true, output, ms: Date.now() - start });
    } catch (err) {
      const output = (err.stdout || err.stderr || err.message || '').trim();
      resolve({ ...check, ok: false, output, ms: Date.now() - start, error: true });
    }
  });
}

// Evaluate alert condition against output
function evalAlert(condition, output, format) {
  if (!condition) return false;
  
  let value = output;
  let parsed = null;
  
  if (format === 'json') {
    try { parsed = JSON.parse(output); } catch { return false; }
  }

  // JSON field access: .field > N, .field == 'str', .field != null
  const jsonMatch = condition.match(/^\.(\w+)\s*(>|<|>=|<=|==|!=)\s*(.+)$/);
  if (jsonMatch && parsed) {
    const field = parsed[jsonMatch[1]];
    const op = jsonMatch[2];
    let compare = jsonMatch[3].trim().replace(/^["']|["']$/g, '');
    
    if (compare === 'null') {
      if (op === '!=') return field != null;
      if (op === '==') return field == null;
    }
    
    const numCompare = parseFloat(compare);
    const numField = typeof field === 'number' ? field : parseFloat(field);
    
    if (!isNaN(numCompare) && !isNaN(numField)) {
      switch (op) {
        case '>': return numField > numCompare;
        case '<': return numField < numCompare;
        case '>=': return numField >= numCompare;
        case '<=': return numField <= numCompare;
        case '==': return numField === numCompare;
        case '!=': return numField !== numCompare;
      }
    }
    
    switch (op) {
      case '==': return String(field) === compare;
      case '!=': return String(field) !== compare;
    }
  }

  // OR conditions: .field < -20 || .field > 20
  if (condition.includes('||')) {
    return condition.split('||').some(c => evalAlert(c.trim(), output, format));
  }

  // Simple comparisons on raw output
  if (condition.startsWith('!= ')) {
    const compare = condition.slice(3).replace(/^['"]|['"]$/g, '');
    return value !== compare;
  }
  if (condition.startsWith('== ')) {
    const compare = condition.slice(3).replace(/^['"]|['"]$/g, '');
    return value === compare;
  }
  if (condition.startsWith('contains ')) {
    const compare = condition.slice(9).replace(/^['"]|['"]$/g, '');
    return value.includes(compare);
  }
  
  // Numeric comparisons
  const numMatch = condition.match(/^(>|<|>=|<=)\s*(\d+\.?\d*)$/);
  if (numMatch) {
    const num = parseFloat(value);
    const compare = parseFloat(numMatch[2]);
    if (isNaN(num)) return false;
    switch (numMatch[1]) {
      case '>': return num > compare;
      case '<': return num < compare;
      case '>=': return num >= compare;
      case '<=': return num <= compare;
    }
  }

  // Changed detection
  if (condition === 'changed') {
    // Handled separately in the main loop
    return false;
  }

  return false;
}

// Render summary template
function renderSummary(template, output, format) {
  if (!template) return output.substring(0, 200);
  
  let result = template.replace(/\{\{output\}\}/g, output);
  
  if (format === 'json') {
    try {
      const parsed = JSON.parse(output);
      result = result.replace(/\{\{\.([\w.]+)\}\}/g, (_, key) => {
        const val = key.split('.').reduce((o, k) => o?.[k], parsed);
        return val !== undefined ? String(val) : '';
      });
    } catch {}
  }
  
  return result;
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const brief = args.includes('--brief');
  const json = args.includes('--json');
  const quiet = args.includes('--quiet');
  const dryRun = args.includes('--dry-run');
  const singleRun = args.includes('--run') ? args[args.indexOf('--run') + 1] : null;
  
  const configIdx = args.indexOf('--config');
  const configPath = configIdx !== -1 ? args[configIdx + 1] : 'heartbeat.yaml';
  
  // Find config
  const fullConfigPath = path.resolve(configPath);
  if (!fs.existsSync(fullConfigPath)) {
    console.error(`Config not found: ${fullConfigPath}`);
    console.error('Create heartbeat.yaml in your workspace root. See SKILL.md for examples.');
    process.exit(1);
  }

  const configText = fs.readFileSync(fullConfigPath, 'utf8');
  const config = parseYaml(configText);
  
  const timeoutMs = (config.settings?.timeout || 30) * 1000;
  const outputPath = config.settings?.output || 'research/latest.md';
  const cacheDir = config.settings?.cache_dir || '.heartbeat-cache';

  // Merge collectors and health checks
  let checks = [
    ...(config.collectors || []).map(c => ({ ...c, type: 'collector' })),
    ...(config.health || []).map(h => ({ ...h, type: 'health' })),
  ].filter(c => c.enabled !== false);

  if (singleRun) {
    checks = checks.filter(c => c.name === singleRun);
    if (checks.length === 0) {
      console.error(`Check "${singleRun}" not found in config.`);
      process.exit(1);
    }
  }

  if (dryRun) {
    console.log('Would run:');
    checks.forEach(c => console.log(`  [${c.type}] ${c.name}: ${c.command}`));
    process.exit(0);
  }

  // Run all checks in parallel
  const startAll = Date.now();
  const results = await Promise.all(checks.map(c => runCheck(c, timeoutMs)));
  const totalMs = Date.now() - startAll;

  // Evaluate alerts
  const alerts = [];
  const summaryLines = [];

  for (const r of results) {
    const condition = r.alert || r.warn || r.critical;
    let triggered = false;
    let level = 'ok';

    // Handle "changed" alert
    if (r.alert === 'changed' && r.cache) {
      const cachePath = path.resolve(cacheDir, path.basename(r.cache));
      fs.mkdirSync(path.dirname(cachePath), { recursive: true });
      const prev = fs.existsSync(cachePath) ? fs.readFileSync(cachePath, 'utf8') : null;
      if (prev !== null && prev !== r.output) {
        triggered = true;
        level = 'action';
      }
      fs.writeFileSync(cachePath, r.output);
    } else {
      if (r.critical && evalAlert(r.critical, r.output, r.format)) {
        triggered = true;
        level = 'critical';
      } else if (r.warn && evalAlert(r.warn, r.output, r.format)) {
        triggered = true;
        level = 'warn';
      } else if (r.alert && evalAlert(r.alert, r.output, r.format)) {
        triggered = true;
        level = 'action';
      }
    }

    if (r.error) {
      level = 'error';
      triggered = true;
    }

    const summary = r.ok ? renderSummary(r.summary, r.output, r.format) : `ERROR: ${r.output.substring(0, 100)}`;
    
    const entry = {
      name: r.name,
      type: r.type,
      level,
      triggered,
      summary: triggered ? summary : null,
      ms: r.ms,
    };

    if (triggered) alerts.push(entry);
    summaryLines.push(entry);
  }

  const needsAction = alerts.some(a => a.level !== 'ok');

  // JSON output
  if (json) {
    console.log(JSON.stringify({
      status: needsAction ? 'action_needed' : 'all_clear',
      checks: summaryLines,
      alerts,
      totalMs,
    }, null, 2));
    process.exit(needsAction ? 2 : 0);
  }

  // Brief output
  if (brief) {
    if (!needsAction) {
      console.log('HEARTBEAT_OK');
    } else {
      const items = alerts.map(a => `${a.name}: ${a.summary}`).join('; ');
      console.log(`NEEDS ATTENTION: ${items}`);
    }
    process.exit(needsAction ? 2 : 0);
  }

  // Quiet output
  if (quiet) {
    process.exit(needsAction ? 2 : 0);
  }

  // Full summary — write to file
  const now = new Date().toISOString();
  let md = `# Heartbeat Summary\n_${now}_ (${totalMs}ms)\n\n`;

  if (needsAction) {
    md += `## ⚠️ Action Needed\n\n`;
    for (const a of alerts) {
      const icon = a.level === 'critical' ? '🔴' : a.level === 'error' ? '❌' : a.level === 'warn' ? '🟡' : '🔵';
      md += `- ${icon} **${a.name}**: ${a.summary}\n`;
    }
    md += '\n';
  } else {
    md += `All clear. ${summaryLines.length} checks passed.\n\n`;
  }

  md += `## Details\n\n`;
  for (const s of summaryLines) {
    const icon = s.triggered ? (s.level === 'critical' ? '🔴' : s.level === 'error' ? '❌' : '🟡') : '✅';
    md += `- ${icon} ${s.name} (${s.ms}ms)${s.summary ? ': ' + s.summary : ''}\n`;
  }

  // Write summary
  const outDir = path.dirname(path.resolve(outputPath));
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.resolve(outputPath), md);

  // Also print to stdout
  if (needsAction) {
    console.log(`NEEDS ATTENTION (${alerts.length} alert${alerts.length > 1 ? 's' : ''})`);
    alerts.forEach(a => console.log(`  ${a.name}: ${a.summary}`));
  } else {
    console.log(`HEARTBEAT_OK (${summaryLines.length} checks, ${totalMs}ms)`);
  }

  process.exit(needsAction ? 2 : 0);
}

main().catch(err => {
  console.error('Heartbeat error:', err.message);
  process.exit(1);
});
