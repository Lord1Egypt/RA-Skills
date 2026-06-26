#!/usr/bin/env node
/**
 * pwsh-encoding-fix.js — PowerShell 编码损坏检测与修复工具 v2
 * 在任何有 Node.js 的 Windows 机器上可用。
 *
 * 用法:
 *   node pwsh-encoding-fix.js <file>          # 诊断
 *   node pwsh-encoding-fix.js <file> --fix     # 诊断 + 修复
 *   node pwsh-encoding-fix.js --help           # 帮助
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================
// 诊断
// ============================================================

function diagnose(filePath) {
  const absPath = path.resolve(filePath);
  if (!fs.existsSync(absPath)) {
    console.error('File not found: ' + absPath);
    process.exit(1);
  }

  const stat = fs.statSync(absPath);
  const raw = fs.readFileSync(absPath);
  const text = raw.toString('utf8');
  var linesArr = text.split('\n');
  const issues = [];

  // --- 1. BOM check ---
  if (raw[0] === 0xEF && raw[1] === 0xBB && raw[2] === 0xBF) {
    issues.push({ type: 'BOM', severity: 'low',
      detail: 'File has UTF-8 BOM header. Non-critical, but may cause issues cross-platform.' });
  }

  // --- 2. Backtick loss ---
  const backtickCount = (text.match(/`/g) || []).length;
  const templateDollar = (text.match(/\$\{/g) || []).length;

  // Line-level: find code lines (not comments, not string content) that use ${} without backticks
  var suspiciousLines = 0;
  var totalDollarLines = 0;
  for (var li = 0; li < linesArr.length; li++) {
    var l = linesArr[li].trim();
    if (l.indexOf('${') === -1) continue;
    // Skip comments and string definitions (tool source code patterns)
    if (l.indexOf('//') === 0) continue;
    if (l.indexOf('*') === 0) continue;
    if (l.indexOf('detail:') >= 0) continue;
    if (l.indexOf('h += ') >= 0) continue;
    totalDollarLines++;
    if (l.indexOf('`') === -1) {
      suspiciousLines++;
    }
  }

  if (suspiciousLines > 0 && backtickCount < templateDollar * 0.3) {
    issues.push({ type: 'BACKTICK_LOST', severity: 'critical',
      detail: suspiciousLines + ' lines use ${} without backticks. '
        + 'Found ' + backtickCount + ' backticks vs ' + totalDollarLines + ' lines with ${}. '
        + 'Template literals likely stripped by PowerShell.' });
  } else if (suspiciousLines > 0) {
    issues.push({ type: 'BACKTICK_PARTIAL', severity: 'warning',
      detail: suspiciousLines + ' lines use ${} without backticks. Some templates may be damaged.' });
  }

  // --- 3. Empty templates (dollar expanded to empty) ---
  var emptyTemplates = 0;
  for (var ei = 0; ei < linesArr.length; ei++) {
    var el = linesArr[ei];
    // Skip tool source patterns that use `` in regex or docs
    if (el.indexOf('/``/') >= 0) continue;
    if (el.indexOf('(``)') >= 0) continue;
    if (el.indexOf('empty template') >= 0) continue;
    // Real empty template detection
    if (el.indexOf('``') >= 0) {
      var stripped = el.replace(/'[^']*'/g, '').replace(/"[^"]*"/g, '');
      if (stripped.indexOf('``') >= 0) {
        emptyTemplates++;
      }
    }
  }
  if (emptyTemplates > 1) {
    issues.push({ type: 'DOLLAR_EXPANDED', severity: 'critical',
      detail: emptyTemplates + ' empty template literals found. Dollar-brace variables likely expanded to empty.' });
  }

  // --- 4. GBK corruption ---
  let gbkChars = 0;
  let hanChars = 0;
  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);
    if (code >= 0x4E00 && code <= 0x9FFF) hanChars++;
    if ((code >= 0x00C0 && code <= 0x024F) || code === 0x00AB || code === 0x00BB) {
      gbkChars++;
    }
  }

  const ratio = hanChars > 0 ? gbkChars / hanChars : Infinity;
  if (gbkChars > 20 && ratio > 0.5) {
    issues.push({ type: 'GBK_CORRUPT', severity: 'critical',
      detail: 'GBK residual: ' + gbkChars + ' chars / valid Chinese: ' + hanChars
        + ' (ratio ' + ratio.toFixed(1) + '). Chinese text is heavily corrupted.' });
  } else if (gbkChars > 10 && ratio > 0.2) {
    issues.push({ type: 'GBK_CORRUPT', severity: 'warning',
      detail: 'GBK residual: ' + gbkChars + ' chars / valid Chinese: ' + hanChars
        + ' (ratio ' + ratio.toFixed(1) + '). Some Chinese may be corrupted.' });
  }

  // --- 5. Syntax check (JS files only) ---
  let syntaxOk = true;
  let syntaxMsg = '';
  try {
    if (filePath.endsWith('.js')) {
      execSync('node --check "' + absPath + '"', { stdio: 'pipe' });
    }
  } catch (e) {
    syntaxOk = false;
    syntaxMsg = e.stderr ? e.stderr.toString().split('\n')[0] : e.message;
    issues.push({ type: 'SYNTAX_ERROR', severity: 'critical',
      detail: syntaxMsg.substring(0, 200) });
  }

  return {
    file: absPath, size: stat.size, lines: linesArr.length,
    backtickCount, templateDollar, suspiciousLines,
    totalDollarLines, hanChars, gbkChars,
    syntaxOk, syntaxMsg, issues
  };
}

// ============================================================
// 报告
// ============================================================

function printReport(d) {
  var sevOrder = { critical: 0, warning: 1, low: 2 };
  var hasCritical = false;

  console.log('');
  console.log('========================================================');
  console.log('  PowerShell Encoding Damage Report');
  console.log('========================================================');
  console.log('  File:    ' + d.file);
  console.log('  Size:    ' + (d.size / 1024).toFixed(1) + ' KB  (' + d.lines + ' lines)');
  console.log('  Backtick: ' + d.backtickCount);
  console.log('  Dollar{}: ' + d.templateDollar + ' total');
  console.log('  Suspicious lines: ' + d.suspiciousLines + ' / ' + d.totalDollarLines);
  console.log('  Chinese: ' + d.hanChars + ' valid / ' + d.gbkChars + ' GBK residual');
  console.log('  Syntax:  ' + (d.syntaxOk ? 'PASS' : 'FAIL'));
  console.log('--------------------------------------------------------');

  if (d.issues.length === 0) {
    console.log('  No encoding issues detected.');
    return true;
  }

  d.issues.sort(function(a, b) { return sevOrder[a.severity] - sevOrder[b.severity]; });
  console.log('  Found ' + d.issues.length + ' issue(s):');
  console.log('');

  d.issues.forEach(function(iss) {
    var icon = iss.severity === 'critical' ? '!!' : iss.severity === 'warning' ? 'WW' : 'II';
    console.log('  ' + icon + ' [' + iss.severity.toUpperCase() + '] ' + iss.type);
    console.log('     ' + iss.detail);
    if (iss.severity === 'critical') hasCritical = true;
  });

  console.log('--------------------------------------------------------');
  if (hasCritical) {
    console.log('  Critical issues found. Use --fix to attempt repair.');
  }
  console.log('');

  return !hasCritical;
}

// ============================================================
// 修复
// ============================================================

function fixFile(filePath) {
  var absPath = path.resolve(filePath);
  var d = diagnose(filePath);
  var critical = d.issues.filter(function(i) { return i.severity === 'critical'; });

  if (critical.length === 0) {
    console.log('No critical issues found. Nothing to fix.');
    return;
  }

  console.log('');
  console.log('Attempting repair...');
  console.log('');

  critical.forEach(function(iss) {
    if (iss.type === 'GBK_CORRUPT') {
      var raw = fs.readFileSync(absPath);
      try {
        var fixed;
        // Try iconv-lite first
        try {
          var iconv = require('iconv-lite');
          fixed = iconv.decode(raw, 'gbk');
        } catch (e1) {
          // Fallback: Node.js TextDecoder
          try {
            var buf = (raw[0] === 0xEF && raw[1] === 0xBB && raw[2] === 0xBF) ? raw.slice(3) : raw;
            var td = new (require('util').TextDecoder)('gbk');
            fixed = td.decode(buf);
          } catch (e2) {
            throw new Error('GBK decoder unavailable. Install: npm install iconv-lite');
          }
        }

        // Backup original
        var bakPath = absPath + '.bak';
        if (!fs.existsSync(bakPath)) {
          fs.copyFileSync(absPath, bakPath);
          console.log('  Backup saved: ' + path.basename(bakPath));
        }

        // Check decode quality
        var suspectCount = 0;
        for (var i = 0; i < fixed.length; i++) {
          var c = fixed.charAt(i);
          if (c === '\uFFFD' || c === '\uFFFE' || c === '\uFFFF') suspectCount++;
        }
        if (suspectCount > 10) {
          console.log('  Warning: ' + suspectCount + ' replacement characters. Decode quality may be poor.');
        }

        fs.writeFileSync(absPath, fixed, 'utf8');
        console.log('  GBK encoding repaired to UTF-8.');
        console.log('  Original backed up as: ' + path.basename(bakPath));
      } catch (e) {
        console.log('  GBK repair FAILED: ' + e.message);
      }
    }

    if (iss.type === 'BACKTICK_LOST' || iss.type === 'DOLLAR_EXPANDED') {
      console.log('  Cannot auto-repair backtick/dollar expansion.');
      console.log('  Options:');
      console.log('    1. Rewrite from original source with safe write method');
      console.log('    2. Git restore: git checkout -- ' + path.basename(absPath));
      console.log('    3. Hex transfer from clean machine');
    }
  });

  // Re-diagnose
  console.log('');
  console.log('Re-diagnosing after fix...');
  var after = diagnose(filePath);
  printReport(after);
}

// ============================================================
// 帮助
// ============================================================

function printHelp() {
  var h = '';
  h += 'pwsh-encoding-fix.js - PowerShell File Encoding Fix Tool\n';
  h += '\n';
  h += 'Detects and repairs file corruption caused by PowerShell file writes on Windows.\n';
  h += '\n';
  h += 'Usage:\n';
  h += '  node pwsh-encoding-fix.js <file>          Diagnose only\n';
  h += '  node pwsh-encoding-fix.js <file> --fix     Diagnose + auto-repair\n';
  h += '  node pwsh-encoding-fix.js --help           This help\n';
  h += '\n';
  h += 'Issue types:\n';
  h += '  !! BACKTICK_LOST    - Template backticks eaten by PowerShell\n';
  h += '  !! DOLLAR_EXPANDED  - Dollar-brace vars expanded to empty\n';
  h += '  !! GBK_CORRUPT      - Chinese UTF-8 re-encoded as GBK (auto-fixable)\n';
  h += '  WW SYNTAX_ERROR    - JS syntax broken by encoding damage\n';
  h += '  II BOM             - UTF-8 BOM header (non-critical)\n';
  h += '\n';
  h += 'Examples:\n';
  h += '  node pwsh-encoding-fix.js server.js\n';
  h += '  node pwsh-encoding-fix.js server.js --fix\n';
  console.log(h);
}

// ============================================================
// 主入口
// ============================================================

function main() {
  var args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    return;
  }

  if (args[1] === '--fix') {
    fixFile(args[0]);
  } else {
    var d = diagnose(args[0]);
    printReport(d);
  }
}

main();
