#!/usr/bin/env node

/**
 * Skill Vetting Tool
 * Scans skill directories for potential security threats
 */

const fs = require('fs');
const path = require('path');

// Risk patterns
const PATTERNS = {
  high: [
    { pattern: /eval\s*\(/g, desc: 'Dynamic code execution via eval()' },
    { pattern: /exec\s*\(/g, desc: 'Shell command execution' },
    { pattern: /child_process.*spawn.*shell:\s*true/g, desc: 'Shell injection risk' },
    { pattern: /Buffer\.from\([^,)]*\)/g, desc: 'Buffer manipulation' },
    { pattern: /process\.env\.(AWS_|AZURE_|GCP_|SECRET|PASSWORD|TOKEN|KEY)/g, desc: 'Sensitive env access' },
    { pattern: /crypto\.createDecipher/g, desc: 'Encryption/decryption' },
  ],
  medium: [
    { pattern: /fs\.writeFile/g, desc: 'File write operation' },
    { pattern: /fs\.unlink/g, desc: 'File deletion' },
    { pattern: /fs\.rmdir/g, desc: 'Directory removal' },
    { pattern: /https?:\/\//g, desc: 'Network request' },
    { pattern: /child_process/g, desc: 'Subprocess spawning' },
    { pattern: /setTimeout|setInterval/g, desc: 'Delayed execution' },
    { pattern: /fetch\s*\(/g, desc: 'HTTP fetch' },
    { pattern: /axios/g, desc: 'HTTP client' },
  ],
  low: [
    { pattern: /console\.log/g, desc: 'Logging' },
    { pattern: /require\s*\(\s*['"]fs['"]\)/g, desc: 'Filesystem access' },
    { pattern: /require\s*\(\s*['"]path['"]\)/g, desc: 'Path manipulation' },
  ]
};

// Color codes
const colors = {
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function scanFile(filePath, verbose = false) {
  const issues = [];
  const ext = path.extname(filePath);
  
  // Skip non-code files
  if (!['.js', '.ts', '.sh', '.bash', '.ps1', '.md'].includes(ext)) {
    return issues;
  }
  
  let content;
  try {
    content = fs.readFileSync(filePath, 'utf-8');
  } catch (e) {
    return issues;
  }
  
  const lines = content.split('\n');
  
  // Check high risk patterns
  for (const rule of PATTERNS.high) {
    let match;
    rule.pattern.lastIndex = 0;
    while ((match = rule.pattern.exec(content)) !== null) {
      const lineNum = content.substring(0, match.index).split('\n').length;
      issues.push({
        level: 'high',
        file: filePath,
        line: lineNum,
        desc: rule.desc,
        snippet: lines[lineNum - 1]?.trim().substring(0, 60)
      });
    }
  }
  
  // Check medium risk patterns
  for (const rule of PATTERNS.medium) {
    let match;
    rule.pattern.lastIndex = 0;
    while ((match = rule.pattern.exec(content)) !== null) {
      const lineNum = content.substring(0, match.index).split('\n').length;
      issues.push({
        level: 'medium',
        file: filePath,
        line: lineNum,
        desc: rule.desc,
        snippet: lines[lineNum - 1]?.trim().substring(0, 60)
      });
    }
  }
  
  // Check low risk patterns (verbose only)
  if (verbose) {
    for (const rule of PATTERNS.low) {
      let match;
      rule.pattern.lastIndex = 0;
      while ((match = rule.pattern.exec(content)) !== null) {
        const lineNum = content.substring(0, match.index).split('\n').length;
        issues.push({
          level: 'low',
          file: filePath,
          line: lineNum,
          desc: rule.desc,
          snippet: lines[lineNum - 1]?.trim().substring(0, 60)
        });
      }
    }
  }
  
  return issues;
}

function scanDir(dirPath, verbose = false) {
  const allIssues = [];
  let fileCount = 0;
  
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      // Skip node_modules, .git, etc.
      if (entry.isDirectory()) {
        if (!['node_modules', '.git', '.venv', 'dist'].includes(entry.name)) {
          walk(fullPath);
        }
      } else if (entry.isFile()) {
        fileCount++;
        const issues = scanFile(fullPath, verbose);
        allIssues.push(...issues);
      }
    }
  }
  
  walk(dirPath);
  return { issues: allIssues, fileCount };
}

function main() {
  const args = process.argv.slice(2);
  const verbose = args.includes('--verbose') || args.includes('-v');
  
  let targetPath = args.find(a => !a.startsWith('-')) || '.';
  
  // Resolve relative path
  if (!path.isAbsolute(targetPath)) {
    targetPath = path.resolve(process.cwd(), targetPath);
  }
  
  if (!fs.existsSync(targetPath)) {
    console.error(`${colors.red}Error: Path not found: ${targetPath}${colors.reset}`);
    process.exit(1);
  }
  
  const isDir = fs.statSync(targetPath).isDirectory();
  
  console.log(`${colors.blue}🔍 Scanning: ${targetPath}${colors.reset}\n`);
  
  let result;
  if (isDir) {
    result = scanDir(targetPath, verbose);
  } else {
    result = { issues: scanFile(targetPath, verbose), fileCount: 1 };
  }
  
  console.log(`📁 Files scanned: ${result.fileCount}`);
  console.log(`⚠️  Issues found: ${result.issues.length}\n`);
  
  // Group by level
  const high = result.issues.filter(i => i.level === 'high');
  const medium = result.issues.filter(i => i.level === 'medium');
  const low = result.issues.filter(i => i.level === 'low');
  
  if (high.length > 0) {
    console.log(`${colors.red}🔴 High Risk:${colors.reset}`);
    for (const issue of high) {
      console.log(`  ${colors.red}[HIGH]${colors.reset} ${issue.file}:${issue.line}`);
      console.log(`    ${issue.desc}`);
      if (issue.snippet) console.log(`    ${colors.gray}>${colors.reset} ${issue.snippet}`);
    }
    console.log('');
  }
  
  if (medium.length > 0) {
    console.log(`${colors.yellow}🟡 Medium Risk:${colors.reset}`);
    for (const issue of medium) {
      console.log(`  ${colors.yellow}[MEDIUM]${colors.reset} ${issue.file}:${issue.line}`);
      console.log(`    ${issue.desc}`);
    }
    console.log('');
  }
  
  if (low.length > 0 && verbose) {
    console.log(`${colors.green}🟢 Low Risk:${colors.reset}`);
    for (const issue of low) {
      console.log(`  ${colors.green}[LOW]${colors.reset} ${issue.file}:${issue.line}`);
      console.log(`    ${issue.desc}`);
    }
    console.log('');
  }
  
  // Summary
  if (high.length > 0) {
    console.log(`${colors.red}❌ Scan failed: High risk issues detected. Review before proceeding.${colors.reset}`);
    process.exit(1);
  } else if (medium.length > 0) {
    console.log(`${colors.yellow}⚠️  Scan complete: Medium risk issues found. Caution advised.${colors.reset}`);
    process.exit(0);
  } else {
    console.log(`${colors.green}✅ Scan complete: No significant issues found.${colors.reset}`);
    process.exit(0);
  }
}

main();
