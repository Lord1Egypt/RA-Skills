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
exports.SkillScanner = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const rules_1 = require("./rules");
const SEVERITY_WEIGHTS = {
    critical: 25,
    high: 15,
    medium: 8,
    low: 3,
};
const SCANNABLE_EXTENSIONS = new Set([
    '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.json', '.yaml', '.yml', '.md',
]);
class SkillScanner {
    constructor(rules) {
        this.rules = rules ?? rules_1.SCAN_RULES;
    }
    async scanSkill(skillPath) {
        const start = Date.now();
        const resolvedPath = path.resolve(skillPath);
        const skillName = path.basename(resolvedPath);
        const files = this.collectFiles(resolvedPath);
        const allFindings = [];
        for (const file of files) {
            const findings = await this.scanFile(file);
            allFindings.push(...findings);
        }
        const riskScore = this.calculateRiskScore(allFindings);
        return {
            skillName,
            scannedAt: new Date().toISOString(),
            filesScanned: files.length,
            totalFindings: allFindings.length,
            findings: allFindings,
            riskScore,
            verdict: this.assignVerdict(riskScore),
            scanDurationMs: Date.now() - start,
        };
    }
    async scanFile(filePath) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const lines = content.split('\n');
        const findings = [];
        for (const rule of this.rules) {
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                // Reset regex state for global patterns
                const pattern = new RegExp(rule.pattern.source, rule.pattern.flags);
                const match = pattern.exec(line);
                if (match) {
                    findings.push({
                        ruleId: rule.id,
                        ruleName: rule.name,
                        severity: rule.severity,
                        file: filePath,
                        line: i + 1,
                        column: match.index + 1,
                        snippet: line.trim(),
                        description: rule.description,
                        remediation: rule.remediation,
                    });
                }
            }
        }
        return findings;
    }
    calculateRiskScore(findings) {
        if (findings.length === 0)
            return 0;
        let raw = 0;
        for (const f of findings) {
            raw += SEVERITY_WEIGHTS[f.severity];
        }
        return Math.min(100, raw);
    }
    assignVerdict(riskScore) {
        if (riskScore < 30)
            return 'verified';
        if (riskScore < 50)
            return 'reviewed';
        return 'flagged';
    }
    collectFiles(dir) {
        const results = [];
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.isDirectory()) {
                if (entry.name === 'node_modules' || entry.name === 'dist' || entry.name === '.git') {
                    continue;
                }
                results.push(...this.collectFiles(fullPath));
            }
            else if (entry.isFile()) {
                const ext = path.extname(entry.name);
                if (SCANNABLE_EXTENSIONS.has(ext)) {
                    results.push(fullPath);
                }
            }
        }
        return results;
    }
}
exports.SkillScanner = SkillScanner;
//# sourceMappingURL=index.js.map