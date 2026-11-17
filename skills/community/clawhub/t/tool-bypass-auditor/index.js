const fs = require('fs');
const path = require('path');

function auditWorkspace(root) {
  const results = {
    workspace: root,
    time: new Date().toISOString(),
    totalFindings: 0,
    bypassLikely: 0,
    execOveruse: 0,
    findings: [],
    recommendations: []
  };

  const files = collectJsonl(root);
  for (const file of files) {
    const lines = readJsonl(file);
    for (const line of lines) {
      if (!line || typeof line !== 'object') continue;
      const text = JSON.stringify(line);

      if (/tool_bypass|toolbypass|bypass/.test(text)) {
        results.findings.push({ file, type: 'bypass_likely', signal: 'tool_bypass' });
        results.bypassLikely++;
      }

      if (/exec/.test(text) || /shell/.test(text) || /cmd /.test(text)) {
        const execCount = (text.match(/exec|shell|cmd /g) || []).length;
        if (execCount > 2) {
          results.findings.push({ file, type: 'exec_overuse', count: execCount });
          results.execOveruse++;
        }
      }

      if (/sudo|--force|unsafe|chmod 777|rm -rf/.test(text)) {
        results.findings.push({ file, type: 'unsafe_execution' });
      }
    }
  }

  results.totalFindings = results.findings.length;
  if (results.bypassLikely > 0) {
    results.recommendations.push('Prefer registered tools over exec/shell workarounds for bypassed actions.');
  }
  if (results.execOveruse > 0) {
    results.recommendations.push('Review exec-heavy flows for possible skill/tool replacements.');
  }
  if (results.totalFindings === 0) {
    results.recommendations.push('No bypass patterns detected in scanned artifacts.');
  }
  return results;
}

function collectJsonl(root) {
  const out = [];
  const visited = new Set();
  function walk(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      if (e.name.startsWith('.') && e.name !== '.env') continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (visited.has(full)) continue;
        visited.add(full);
        walk(full);
      } else if (e.isFile() && e.name.endsWith('.jsonl')) {
        out.push(full);
      }
    }
  }
  walk(root);
  return out;
}

function readJsonl(file) {
  const content = fs.readFileSync(file, 'utf8');
  return content.split(/\r?\n/).filter(Boolean).map((line, idx) => {
    try { return JSON.parse(line); } catch (e) { return { _parse_error: true, file, line: idx + 1 }; }
  });
}

module.exports = { auditWorkspace };

if (require.main === module) {
  const root = process.argv[2] || process.cwd();
  const report = auditWorkspace(root);
  console.log(JSON.stringify(report, null, 2));
}
