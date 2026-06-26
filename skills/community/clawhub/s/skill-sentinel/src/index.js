import fs from 'node:fs';
import path from 'node:path';

export const TOOL = 'clawshield';
export const VERSION = '0.1.0';

const RULES = [
  {
    id: 'CS001_CURL_PIPE_SH',
    severity: 'high',
    pattern: /\b(?:curl|wget)\b[^\n|]*\|[^\n]*(?:sh|bash)\b/i,
    message: 'Detected download-and-execute chain.',
    remediation: 'Avoid piping remote scripts directly to a shell.'
  },
  {
    id: 'CS002_OBFUSCATED_EXEC',
    severity: 'high',
    pattern: /(?:eval\s*\(|new\s+Function\s*\(|base64\s+(?:-d|--decode)|atob\s*\()/i,
    message: 'Detected obfuscation or dynamic execution pattern.',
    remediation: 'Remove dynamic execution and keep script logic transparent.'
  },
  {
    id: 'CS003_SUSPICIOUS_CALLBACK',
    severity: 'medium',
    pattern: /https?:\/\/(?:\d{1,3}(?:\.\d{1,3}){3}|[^\s/]*(?:ngrok|requestbin|webhook))/i,
    message: 'Detected potentially suspicious outbound callback endpoint.',
    remediation: 'Restrict callbacks to trusted, documented endpoints.'
  },
  {
    id: 'CS004_SOCIAL_ENGINEERING_PROMPT',
    severity: 'medium',
    pattern: /(copy\s+and\s+paste\s+this\s+command|disable\s+(?:all\s+)?security|ignore\s+safety)/i,
    message: 'Detected social-engineering style instruction.',
    remediation: 'Use transparent, auditable steps and avoid bypass instructions.'
  },
  {
    id: 'CS005_SHELL_WRAPPER_EXEC',
    severity: 'high',
    pattern: /bash\s+-c\s+["'][^"']*(?:curl|wget)[^"']*["']/i,
    message: 'Detected shell wrapper executing remote content.',
    remediation: 'Replace with reviewed local scripts or pinned verified artifacts.'
  }
];

const TEXT_EXTENSIONS = new Set([
  '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.ts', '.tsx', '.jsx', '.sh', '.bash', '.zsh', '.py', '.toml', '.ini', '.env', '.cfg'
]);

function nowIso() {
  return new Date().toISOString();
}

function parseArgs(argv) {
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

function makeEnvelope(status, data = {}, errors = []) {
  return {
    tool: TOOL,
    version: VERSION,
    timestamp: nowIso(),
    status,
    data,
    errors
  };
}

function shouldScanFile(filePath) {
  const base = path.basename(filePath);
  if (base.startsWith('.')) {
    return base === '.env' || base.endsWith('.md');
  }
  const ext = path.extname(filePath).toLowerCase();
  return TEXT_EXTENSIONS.has(ext) || !ext;
}

function walkFiles(rootPath, output = []) {
  const entries = fs.readdirSync(rootPath, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === '.next' || entry.name === 'dist') {
      continue;
    }
    const fullPath = path.join(rootPath, entry.name);
    if (entry.isDirectory()) {
      walkFiles(fullPath, output);
      continue;
    }
    if (shouldScanFile(fullPath)) {
      output.push(fullPath);
    }
  }
  return output;
}

function readSuppressions(skillPath, explicitPath) {
  const candidatePath = explicitPath
    ? path.resolve(explicitPath)
    : path.resolve(skillPath, '.clawshield-suppressions.json');

  if (!fs.existsSync(candidatePath)) {
    return [];
  }

  try {
    const parsed = JSON.parse(fs.readFileSync(candidatePath, 'utf8'));
    if (!Array.isArray(parsed)) {
      return [];
    }
    return parsed
      .filter((entry) => entry && typeof entry.ruleId === 'string')
      .filter((entry) => typeof entry.justification === 'string' && entry.justification.trim().length > 0)
      .map((entry) => ({
        ruleId: entry.ruleId,
        file: typeof entry.file === 'string' ? entry.file : undefined,
        line: typeof entry.line === 'number' ? entry.line : undefined,
        justification: entry.justification.trim()
      }));
  } catch {
    return [];
  }
}

function suppressionMatches(finding, suppression) {
  if (finding.ruleId !== suppression.ruleId) return false;
  if (suppression.file && !finding.file.endsWith(suppression.file)) return false;
  if (typeof suppression.line === 'number' && finding.line !== suppression.line) return false;
  return true;
}

function computeRiskLevel(findings) {
  if (findings.some((f) => f.severity === 'high')) return 'Avoid';
  if (findings.some((f) => f.severity === 'medium')) return 'Caution';
  return 'Safe';
}

function toSeverityLevel(severity) {
  if (severity === 'high') return 'error';
  if (severity === 'medium') return 'warning';
  return 'note';
}

export function toSarif(scanResult) {
  return {
    version: '2.1.0',
    $schema: 'https://json.schemastore.org/sarif-2.1.0.json',
    runs: [
      {
        tool: {
          driver: {
            name: 'ClawShield',
            informationUri: 'https://openclaw.ai',
            rules: RULES.map((rule) => ({
              id: rule.id,
              shortDescription: { text: rule.message },
              help: { text: rule.remediation }
            }))
          }
        },
        results: scanResult.findings.map((finding) => ({
          ruleId: finding.ruleId,
          level: toSeverityLevel(finding.severity),
          message: { text: finding.message },
          locations: [
            {
              physicalLocation: {
                artifactLocation: { uri: finding.file },
                region: {
                  startLine: finding.line
                }
              }
            }
          ]
        }))
      }
    ]
  };
}

function renderTable(scanResult) {
  const lines = [];
  lines.push(`ClawShield scan: ${scanResult.skillPath}`);
  lines.push(`Risk Level: ${scanResult.riskLevel}`);
  lines.push(`Findings: ${scanResult.findingCount} (suppressed ${scanResult.suppressedCount})`);
  lines.push('');
  if (scanResult.findings.length === 0) {
    lines.push('No findings.');
    return lines.join('\n');
  }

  for (const finding of scanResult.findings) {
    lines.push(
      `- [${finding.severity.toUpperCase()}] ${finding.ruleId} ${finding.file}:${finding.line} -> ${finding.message}`
    );
  }
  return lines.join('\n');
}

export function scanSkill(skillPath, options = {}) {
  const resolvedSkillPath = path.resolve(skillPath);
  if (!fs.existsSync(resolvedSkillPath) || !fs.statSync(resolvedSkillPath).isDirectory()) {
    throw new Error(`Skill path not found: ${resolvedSkillPath}`);
  }

  const files = walkFiles(resolvedSkillPath);
  const findings = [];

  for (const filePath of files) {
    let content = '';
    try {
      content = fs.readFileSync(filePath, 'utf8');
    } catch {
      continue;
    }

    const lines = content.split(/\r?\n/);
    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index];
      for (const rule of RULES) {
        if (!rule.pattern.test(line)) {
          continue;
        }
        findings.push({
          ruleId: rule.id,
          severity: rule.severity,
          file: path.relative(process.cwd(), filePath),
          line: index + 1,
          message: rule.message,
          remediation: rule.remediation,
          snippet: line.trim().slice(0, 160)
        });
      }
    }
  }

  const suppressions = readSuppressions(resolvedSkillPath, options.suppressionsPath);
  const unsuppressed = findings.filter(
    (finding) => !suppressions.some((suppression) => suppressionMatches(finding, suppression))
  );

  const summary = {
    low: 0,
    medium: 0,
    high: 0
  };
  for (const finding of unsuppressed) {
    summary[finding.severity] += 1;
  }

  const riskLevel = computeRiskLevel(unsuppressed);

  return {
    skillPath: resolvedSkillPath,
    riskLevel,
    findingCount: unsuppressed.length,
    suppressedCount: findings.length - unsuppressed.length,
    findings: unsuppressed,
    summary
  };
}

function failOnTriggered(riskLevel, failOn) {
  if (!failOn) return false;
  if (failOn === 'avoid') return riskLevel === 'Avoid';
  if (failOn === 'caution') return riskLevel === 'Avoid' || riskLevel === 'Caution';
  return false;
}

function printHelp() {
  console.log(`clawshield usage:\n  clawshield scan <skill-path> --format <table|json|sarif> --fail-on <caution|avoid> [--suppressions <path>]`);
}

export async function runCli(argv) {
  const args = parseArgs(argv);
  const command = args._[0];

  if (!command || args.help) {
    printHelp();
    return command ? 0 : 1;
  }

  try {
    if (command !== 'scan') {
      printHelp();
      return 1;
    }

    const skillPath = args._[1];
    if (!skillPath) {
      console.error(JSON.stringify(makeEnvelope('error', {}, ['Missing <skill-path>']), null, 2));
      return 1;
    }

    const format = args.format || 'table';
    const failOn = args['fail-on'];
    const result = scanSkill(skillPath, { suppressionsPath: args.suppressions });
    const blocked = failOnTriggered(result.riskLevel, failOn);

    if (format === 'json') {
      console.log(
        JSON.stringify(makeEnvelope(blocked ? 'blocked' : result.findingCount ? 'warning' : 'ok', result), null, 2)
      );
    } else if (format === 'sarif') {
      console.log(JSON.stringify(toSarif(result), null, 2));
    } else {
      console.log(renderTable(result));
    }

    return blocked ? 2 : 0;
  } catch (error) {
    console.error(
      JSON.stringify(
        makeEnvelope('error', {}, [error instanceof Error ? error.message : String(error)]),
        null,
        2
      )
    );
    return 1;
  }
}
