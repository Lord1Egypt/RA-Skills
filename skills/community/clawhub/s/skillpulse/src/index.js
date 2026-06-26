import fs from 'node:fs';
import path from 'node:path';

export const TOOL = 'skill-profiler';
export const VERSION = '0.1.0';

function nowIso() {
  return new Date().toISOString();
}

export function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

export function makeEnvelope(status, data = {}, errors = []) {
  return {
    tool: TOOL,
    version: VERSION,
    timestamp: nowIso(),
    status,
    data,
    errors
  };
}

function toNum(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function percentile(values, p) {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.ceil((p / 100) * sorted.length) - 1;
  return sorted[Math.max(0, Math.min(idx, sorted.length - 1))];
}

export function loadSamples(filePath) {
  const resolved = path.resolve(filePath);
  const parsed = JSON.parse(fs.readFileSync(resolved, 'utf8'));
  if (!Array.isArray(parsed)) throw new Error('Samples file must be a JSON array');
  return parsed;
}

export function collectPerformanceData(samples) {
  const sessions = new Set();
  const bySkill = {};

  for (const sample of samples) {
    sessions.add(sample.sessionId || 'unknown');
    const skill = sample.skill || 'unknown';
    const latencyMs = toNum(sample.latencyMs);
    const cpuMs = toNum(sample.cpuMs);
    const memoryMb = toNum(sample.memoryMb);

    bySkill[skill] = bySkill[skill] || {
      skill,
      runs: 0,
      latency: [],
      cpu: [],
      memory: []
    };

    bySkill[skill].runs += 1;
    bySkill[skill].latency.push(latencyMs);
    bySkill[skill].cpu.push(cpuMs);
    bySkill[skill].memory.push(memoryMb);
  }

  const skills = Object.values(bySkill).map((row) => {
    const avgLatencyMs = row.latency.reduce((a, b) => a + b, 0) / row.latency.length;
    const avgCpuMs = row.cpu.reduce((a, b) => a + b, 0) / row.cpu.length;
    const peakMemoryMb = Math.max(...row.memory, 0);
    return {
      skill: row.skill,
      runs: row.runs,
      avgLatencyMs: Number(avgLatencyMs.toFixed(2)),
      p95LatencyMs: Number(percentile(row.latency, 95).toFixed(2)),
      avgCpuMs: Number(avgCpuMs.toFixed(2)),
      peakMemoryMb: Number(peakMemoryMb.toFixed(2))
    };
  }).sort((a, b) => b.p95LatencyMs - a.p95LatencyMs);

  const allLatency = samples.map((s) => toNum(s.latencyMs));

  return {
    collectedAt: nowIso(),
    totalRuns: samples.length,
    sessions: sessions.size,
    avgLatencyMs: Number((allLatency.reduce((a, b) => a + b, 0) / Math.max(1, allLatency.length)).toFixed(2)),
    p95LatencyMs: Number(percentile(allLatency, 95).toFixed(2)),
    skills
  };
}

export function analyzeBottlenecks(profile, thresholds = {}) {
  const latencyThreshold = toNum(thresholds.latencyMs, 1500);
  const cpuThreshold = toNum(thresholds.cpuMs, 1000);
  const memoryThreshold = toNum(thresholds.memoryMb, 500);

  const bottlenecks = [];
  for (const skill of profile.skills) {
    if (skill.p95LatencyMs > latencyThreshold || skill.avgCpuMs > cpuThreshold || skill.peakMemoryMb > memoryThreshold) {
      bottlenecks.push({
        skill: skill.skill,
        p95LatencyMs: skill.p95LatencyMs,
        avgCpuMs: skill.avgCpuMs,
        peakMemoryMb: skill.peakMemoryMb,
        reasons: [
          skill.p95LatencyMs > latencyThreshold ? `p95 latency > ${latencyThreshold}` : null,
          skill.avgCpuMs > cpuThreshold ? `avg cpu > ${cpuThreshold}` : null,
          skill.peakMemoryMb > memoryThreshold ? `peak memory > ${memoryThreshold}` : null
        ].filter(Boolean)
      });
    }
  }

  return {
    thresholds: { latencyMs: latencyThreshold, cpuMs: cpuThreshold, memoryMb: memoryThreshold },
    bottlenecks,
    level: bottlenecks.length ? 'warning' : 'ok'
  };
}

export function compareSessions(leftProfile, rightProfile) {
  const leftMap = new Map(leftProfile.skills.map((s) => [s.skill, s]));
  const rightMap = new Map(rightProfile.skills.map((s) => [s.skill, s]));
  const allSkills = new Set([...leftMap.keys(), ...rightMap.keys()]);

  const deltas = [];
  for (const skill of allSkills) {
    const l = leftMap.get(skill);
    const r = rightMap.get(skill);
    
    // Determine status: added, removed, changed, unchanged
    let status = 'unchanged';
    if (!l && r) status = 'added';
    else if (l && !r) status = 'removed';
    else if (l && r) {
      const latencyDelta = r.p95LatencyMs - l.p95LatencyMs;
      const cpuDelta = r.avgCpuMs - l.avgCpuMs;
      if (Math.abs(latencyDelta) > 0.01 || Math.abs(cpuDelta) > 0.01) {
        status = 'changed';
      }
    }
    
    // Only calculate deltas when both sides exist
    const deltaP95LatencyMs = l && r ? Number((r.p95LatencyMs - l.p95LatencyMs).toFixed(2)) : null;
    const deltaAvgCpuMs = l && r ? Number((r.avgCpuMs - l.avgCpuMs).toFixed(2)) : null;
    const deltaPercentP95 = l && r && l.p95LatencyMs > 0 
      ? Number((((r.p95LatencyMs - l.p95LatencyMs) / l.p95LatencyMs) * 100).toFixed(1))
      : null;
    
    deltas.push({
      skill,
      status,
      leftP95LatencyMs: l?.p95LatencyMs ?? null,
      rightP95LatencyMs: r?.p95LatencyMs ?? null,
      deltaP95LatencyMs,
      deltaPercentP95,
      leftAvgCpuMs: l?.avgCpuMs ?? null,
      rightAvgCpuMs: r?.avgCpuMs ?? null,
      deltaAvgCpuMs
    });
  }

  // Sort: added/removed first, then by regression severity
  deltas.sort((a, b) => {
    // Status priority: removed > added > changed > unchanged
    const statusOrder = { removed: 0, added: 1, changed: 2, unchanged: 3 };
    if (statusOrder[a.status] !== statusOrder[b.status]) {
      return statusOrder[a.status] - statusOrder[b.status];
    }
    // Within same status, sort by latency regression (most negative delta first)
    const deltaA = a.deltaP95LatencyMs ?? -Infinity;
    const deltaB = b.deltaP95LatencyMs ?? -Infinity;
    return deltaB - deltaA;
  });

  return {
    generatedAt: nowIso(),
    left: { totalRuns: leftProfile.totalRuns, sessions: leftProfile.sessions },
    right: { totalRuns: rightProfile.totalRuns, sessions: rightProfile.sessions },
    added: deltas.filter(d => d.status === 'added').length,
    removed: deltas.filter(d => d.status === 'removed').length,
    changed: deltas.filter(d => d.status === 'changed').length,
    deltas
  };
}

export function renderHtmlReport(report, title = 'Skill Profiler Report') {
  const rows = report.profile.skills
    .map((s) => `<tr><td>${s.skill}</td><td>${s.runs}</td><td>${s.avgLatencyMs}</td><td>${s.p95LatencyMs}</td><td>${s.avgCpuMs}</td><td>${s.peakMemoryMb}</td></tr>`)
    .join('');
  return `<!doctype html>
<html><head><meta charset="utf-8"/><title>${title}</title>
<style>body{font-family:Arial,sans-serif;padding:16px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px;text-align:left}</style>
</head><body>
<h1>${title}</h1>
<p>Total runs: ${report.profile.totalRuns} | Sessions: ${report.profile.sessions} | P95 latency: ${report.profile.p95LatencyMs}ms</p>
<h2>Bottlenecks (${report.analysis.bottlenecks.length})</h2>
<ul>${report.analysis.bottlenecks.map((b) => `<li>${b.skill}: ${b.reasons.join(', ')}</li>`).join('')}</ul>
<h2>Skill metrics</h2>
<table><thead><tr><th>Skill</th><th>Runs</th><th>Avg Latency</th><th>P95 Latency</th><th>Avg CPU</th><th>Peak Memory</th></tr></thead><tbody>${rows}</tbody></table>
</body></html>`;
}

function exportFile(content, outPath) {
  const resolved = path.resolve(outPath);
  fs.mkdirSync(path.dirname(resolved), { recursive: true });
  fs.writeFileSync(resolved, content, 'utf8');
  return resolved;
}

function renderTable(report) {
  const lines = [];
  lines.push('Skill Profiler Report');
  lines.push(`Runs: ${report.profile.totalRuns} | Sessions: ${report.profile.sessions} | P95: ${report.profile.p95LatencyMs}ms`);
  lines.push(`Bottlenecks: ${report.analysis.bottlenecks.length}`);
  lines.push('');
  for (const s of report.profile.skills.slice(0, 5)) {
    lines.push(`- ${s.skill}: p95=${s.p95LatencyMs}ms avgCpu=${s.avgCpuMs}ms peakMem=${s.peakMemoryMb}MB`);
  }
  return lines.join('\n');
}

function printHelp() {
  console.log(`skill-profiler usage:
  skill-profiler run --input <samples.json> [--latency-ms <n>] [--cpu-ms <n>] [--memory-mb <n>] [--format <table|json>]
  skill-profiler report --input <samples.json> --out <file> [--type <json|html>] [--format <table|json>]
  skill-profiler compare --left <samples.json> --right <samples.json> [--format <table|json>]`);
}

export async function runCli(argv) {
  const args = parseArgs(argv);
  const command = args._[0];
  const format = args.format || 'table';

  if (!command || args.help) {
    printHelp();
    return command ? 0 : 1;
  }

  try {
    if (command === 'run' || command === 'report') {
      if (!args.input) {
        console.error(JSON.stringify(makeEnvelope('error', {}, ['--input is required']), null, 2));
        return 1;
      }
      const profile = collectPerformanceData(loadSamples(args.input));
      const analysis = analyzeBottlenecks(profile, {
        latencyMs: args['latency-ms'],
        cpuMs: args['cpu-ms'],
        memoryMb: args['memory-mb']
      });
      const report = { generatedAt: nowIso(), profile, analysis };

      if (command === 'report') {
        if (!args.out) {
          console.error(JSON.stringify(makeEnvelope('error', {}, ['--out is required for report']), null, 2));
          return 1;
        }
        const type = args.type || (args.out.endsWith('.html') ? 'html' : 'json');
        const outPath = exportFile(type === 'html' ? renderHtmlReport(report) : `${JSON.stringify(report, null, 2)}\n`, args.out);
        if (format === 'json') {
          console.log(JSON.stringify(makeEnvelope('ok', { outPath, reportType: type, report }), null, 2));
        } else {
          console.log(`Report exported: ${outPath}`);
        }
        return 0;
      }

      if (format === 'json') {
        console.log(JSON.stringify(makeEnvelope(analysis.level, report), null, 2));
      } else {
        console.log(renderTable(report));
      }
      return analysis.level === 'warning' ? 2 : 0;
    }

    if (command === 'compare') {
      if (!args.left || !args.right) {
        console.error(JSON.stringify(makeEnvelope('error', {}, ['--left and --right are required']), null, 2));
        return 1;
      }
      const left = collectPerformanceData(loadSamples(args.left));
      const right = collectPerformanceData(loadSamples(args.right));
      const comparison = compareSessions(left, right);
      if (format === 'json') {
        console.log(JSON.stringify(makeEnvelope('ok', comparison), null, 2));
      } else {
        console.log('Skill Profiler Compare');
        console.log(`Added: ${comparison.added} | Removed: ${comparison.removed} | Changed: ${comparison.changed}`);
        console.log('');
        for (const d of comparison.deltas.slice(0, 5)) {
          const statusIcon = d.status === 'added' ? '[+]' : d.status === 'removed' ? '[-]' : d.status === 'changed' ? '[~]' : '[=]';
          if (d.status === 'removed') {
            console.log(`${statusIcon} ${d.skill}: removed`);
          } else if (d.status === 'added') {
            console.log(`${statusIcon} ${d.skill}: added (p95=${d.rightP95LatencyMs}ms)`);
          } else if (d.status === 'changed') {
            const sign = (d.deltaP95LatencyMs || 0) > 0 ? '+' : '';
            console.log(`${statusIcon} ${d.skill}: p95 ${sign}${d.deltaP95LatencyMs}ms (${d.deltaPercentP95}%)`);
          }
        }
      }
      return 0;
    }

    printHelp();
    return 1;
  } catch (error) {
    console.error(JSON.stringify(makeEnvelope('error', {}, [error instanceof Error ? error.message : String(error)]), null, 2));
    return 1;
  }
}
