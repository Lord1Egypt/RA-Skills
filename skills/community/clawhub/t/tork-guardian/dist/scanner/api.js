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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.scanFromURL = scanFromURL;
exports.scanFromSource = scanFromSource;
exports.formatReportForAPI = formatReportForAPI;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const axios_1 = __importDefault(require("axios"));
const index_1 = require("./index");
const scanner = new index_1.SkillScanner();
// File extensions worth scanning
const SCAN_EXTENSIONS = new Set([
    '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
    '.json', '.yaml', '.yml', '.toml',
]);
// Max files to download per repo (rate-limit guard)
const MAX_FILES = 200;
// Max individual file size in bytes
const MAX_FILE_SIZE = 500000;
/**
 * Fetch a public GitHub repository over HTTPS and scan it.
 *
 * Uses the GitHub REST API (trees + raw contents) — no git clone,
 * no child_process, no shell commands.
 */
async function scanFromURL(url) {
    // Strict validation: only GitHub HTTPS URLs
    const match = url.match(/^https?:\/\/github\.com\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+?)(?:\.git)?$/);
    if (!match) {
        throw new Error('Only GitHub HTTPS URLs are supported (e.g. https://github.com/owner/repo)');
    }
    const [, owner, repo] = match;
    // 1. Fetch the default-branch tree recursively
    const { data: tree } = await axios_1.default.get(`https://api.github.com/repos/${owner}/${repo}/git/trees/HEAD?recursive=1`, { headers: { Accept: 'application/vnd.github.v3+json' }, timeout: 30000 });
    // 2. Filter to scannable source files
    const blobs = tree.tree
        .filter((entry) => entry.type === 'blob' &&
        entry.size < MAX_FILE_SIZE &&
        SCAN_EXTENSIONS.has(path.extname(entry.path)))
        .slice(0, MAX_FILES);
    // 3. Download each file via the raw-content endpoint
    const files = {};
    for (const blob of blobs) {
        try {
            const contentUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${blob.path
                .split('/')
                .map(encodeURIComponent)
                .join('/')}`;
            const { data } = await axios_1.default.get(contentUrl, {
                headers: { Accept: 'application/vnd.github.v3.raw' },
                timeout: 10000,
                responseType: 'text',
            });
            files[blob.path] = typeof data === 'string' ? data : String(data);
        }
        catch (_a) {
            // Skip files that can't be fetched (binary, permissions, etc.)
        }
    }
    return scanFromSource(files, repo);
}
/**
 * Scan source code provided as a map of filename -> content strings.
 * Writes files to a temp directory, scans, and cleans up.
 */
async function scanFromSource(files, skillName) {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tork-scan-src-'));
    try {
        for (const [filename, content] of Object.entries(files)) {
            const filePath = path.join(tmpDir, filename);
            const dir = path.dirname(filePath);
            fs.mkdirSync(dir, { recursive: true });
            fs.writeFileSync(filePath, content);
        }
        const report = await scanner.scanSkill(tmpDir);
        if (skillName) {
            report.skillName = skillName;
        }
        return report;
    }
    finally {
        fs.rmSync(tmpDir, { recursive: true, force: true });
    }
}
/**
 * Strip absolute file paths from findings for public API responses.
 */
function formatReportForAPI(report) {
    return {
        skillName: report.skillName,
        scannedAt: report.scannedAt,
        filesScanned: report.filesScanned,
        totalFindings: report.totalFindings,
        findings: (report.findings || []).map(stripFilePath),
        riskScore: report.riskScore,
        verdict: report.verdict,
        scanDurationMs: report.scanDurationMs,
    };
}
function stripFilePath(finding) {
    return {
        ruleId: finding.ruleId,
        ruleName: finding.ruleName,
        severity: finding.severity,
        line: finding.line,
        column: finding.column,
        snippet: finding.snippet,
        description: finding.description,
        remediation: finding.remediation,
    };
}
//# sourceMappingURL=api.js.map
