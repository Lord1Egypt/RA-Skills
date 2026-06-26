#!/usr/bin/env node
"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const path = __importStar(require("path"));
const index_1 = require("./index");
const badge_1 = require("./badge");
function parseArgs(argv) {
    const args = argv.slice(2);
    const flags = {
        json: false,
        verbose: false,
        strict: false,
        skillPath: '.',
    };
    const positional = [];
    for (const arg of args) {
        if (arg === '--json')
            flags.json = true;
        else if (arg === '--verbose')
            flags.verbose = true;
        else if (arg === '--strict')
            flags.strict = true;
        else if (arg === '--help' || arg === '-h') {
            printUsage();
            process.exit(0);
        }
        else
            positional.push(arg);
    }
    if (positional.length > 0) {
        flags.skillPath = positional[0];
    }
    return flags;
}
function printUsage() {
    console.log(`
tork-scan — Scan OpenClaw skills for security vulnerabilities

Usage:
  tork-scan [path] [flags]

Arguments:
  path              Path to skill directory (default: current directory)

Flags:
  --json            Output results as JSON
  --verbose         Show all findings with details
  --strict          Exit 1 on any high or critical finding
  -h, --help        Show this help message

Examples:
  tork-scan .
  tork-scan ./my-skill --verbose
  tork-scan ./my-skill --json --strict
`);
}
const SEVERITY_ICON = {
    critical: 'CRIT',
    high: 'HIGH',
    medium: 'MED ',
    low: 'LOW ',
};
function printFinding(f, verbose) {
    const relFile = path.relative(process.cwd(), f.file);
    console.log(`  [${SEVERITY_ICON[f.severity]}] ${f.ruleId}: ${f.ruleName}`);
    console.log(`         ${relFile}:${f.line}:${f.column}`);
    if (verbose) {
        console.log(`         ${f.snippet}`);
        console.log(`         → ${f.description}`);
        console.log(`         ✓ ${f.remediation}`);
    }
}
async function main() {
    const flags = parseArgs(process.argv);
    const resolvedPath = path.resolve(flags.skillPath);
    const scanner = new index_1.SkillScanner();
    const report = await scanner.scanSkill(resolvedPath);
    const badge = (0, badge_1.generateBadge)(report);
    if (flags.json) {
        console.log(JSON.stringify({ report, badge }, null, 2));
    }
    else {
        console.log('');
        console.log('╔══════════════════════════════════════════╗');
        console.log('║          Tork Security Scanner           ║');
        console.log('╚══════════════════════════════════════════╝');
        console.log('');
        console.log(`  Skill:          ${report.skillName}`);
        console.log(`  Files scanned:  ${report.filesScanned}`);
        console.log(`  Scan duration:  ${report.scanDurationMs}ms`);
        console.log(`  Findings:       ${report.totalFindings}`);
        console.log(`  Risk score:     ${report.riskScore}/100`);
        console.log(`  Verdict:        ${report.verdict.toUpperCase()}`);
        console.log(`  Badge:          ${badge.label} (${badge.tier})`);
        console.log('');
        if (report.findings.length > 0) {
            // Group by severity
            const critical = report.findings.filter(f => f.severity === 'critical');
            const high = report.findings.filter(f => f.severity === 'high');
            const medium = report.findings.filter(f => f.severity === 'medium');
            const low = report.findings.filter(f => f.severity === 'low');
            console.log('── Findings ────────────────────────────────');
            console.log('');
            for (const [label, group] of [['Critical', critical], ['High', high], ['Medium', medium], ['Low', low]]) {
                if (group.length > 0) {
                    console.log(`  ${label} (${group.length}):`);
                    for (const f of group) {
                        printFinding(f, flags.verbose);
                    }
                    console.log('');
                }
            }
        }
        else {
            console.log('  No security issues found.');
            console.log('');
        }
        console.log(`  ${(0, badge_1.generateBadgeMarkdown)(badge)}`);
        console.log('');
    }
    // Exit code logic
    const hasHighPlus = report.findings.some(f => f.severity === 'critical' || f.severity === 'high');
    if (report.verdict === 'flagged') {
        process.exit(1);
    }
    if (flags.strict && hasHighPlus) {
        process.exit(1);
    }
    process.exit(0);
}
main().catch((err) => {
    console.error('tork-scan error:', err.message);
    process.exit(2);
});
//# sourceMappingURL=cli.js.map