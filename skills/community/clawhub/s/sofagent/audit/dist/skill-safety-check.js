"use strict";
// ============================================================
// skill-safety-check.ts · Skill 安全审查（入口）
// ============================================================
// 扫描 Skill 文件中的安全威胁——恶意命令/密钥泄露/危险API/Prompt注入/数据外泄。
// 纯 TypeScript + Node.js 内置模块，零外部依赖。
//
// 用法：
//   npx ts-node src/skill-safety-check.ts <skill-file-or-dir>
//   npx ts-node src/skill-safety-check.ts --json <path>
//   npx ts-node src/skill-safety-check.ts --quiet <path>
//   npx ts-node src/skill-safety-check.ts --help
//
// 退出码：
//   0 = SAFE       / 1 = DANGEROUS  / 2 = SUSPICIOUS
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.scanFile = exports.findFiles = void 0;
exports.scanSkillSafety = scanSkillSafety;
exports.main = main;
const fs_1 = require("fs");
const skill_safety_rules_1 = require("./rules/skill-safety-rules");
const skill_safety_engine_1 = require("./rules/skill-safety-engine");
const skill_safety_reporter_1 = require("./rules/skill-safety-reporter");
/**
 * 扫描指定目标的安全性。
 */
function scanSkillSafety(target, options) {
    const mode = options?.mode ?? 'terminal';
    if (!(0, fs_1.existsSync)(target)) {
        const result = {
            version: skill_safety_rules_1.VERSION,
            scannedAt: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
            filesScanned: 0,
            verdict: 'SUSPICIOUS',
            exitCode: 2,
            results: [],
        };
        if (mode === 'terminal')
            (0, skill_safety_reporter_1.printError)(`错误：目标不存在：${target}`);
        else if (mode === 'json')
            (0, skill_safety_reporter_1.printJsonOutput)(result);
        else if (mode === 'quiet')
            (0, skill_safety_reporter_1.printQuietOutput)('SUSPICIOUS');
        return result;
    }
    const files = (0, skill_safety_engine_1.findFiles)(target);
    const fileResults = [];
    let safeCount = 0, dangerousCount = 0, suspiciousCount = 0;
    let overallVerdict = 'SAFE';
    for (const file of files) {
        const hits = (0, skill_safety_engine_1.scanFile)(file);
        if (hits.length === 0) {
            safeCount++;
            if (mode === 'terminal')
                (0, skill_safety_reporter_1.printFileResult)(file, [], 'SAFE');
            fileResults.push({ file, verdict: 'SAFE', hits: [] });
        }
        else {
            const hasDangerous = hits.some(h => h.severity === 'DANGEROUS');
            const verdict = hasDangerous ? 'DANGEROUS' : 'SUSPICIOUS';
            if (verdict === 'DANGEROUS') {
                dangerousCount++;
                overallVerdict = 'DANGEROUS';
            }
            else {
                suspiciousCount++;
                if (overallVerdict !== 'DANGEROUS')
                    overallVerdict = 'SUSPICIOUS';
            }
            if (mode === 'terminal')
                (0, skill_safety_reporter_1.printFileResult)(file, hits, verdict);
            fileResults.push({ file, verdict, hits });
        }
    }
    const exitCode = overallVerdict === 'DANGEROUS' ? 1 : overallVerdict === 'SUSPICIOUS' ? 2 : 0;
    const result = {
        version: skill_safety_rules_1.VERSION,
        scannedAt: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
        filesScanned: files.length,
        verdict: overallVerdict,
        exitCode,
        results: fileResults,
    };
    if (mode === 'json')
        (0, skill_safety_reporter_1.printJsonOutput)(result);
    else if (mode === 'terminal')
        (0, skill_safety_reporter_1.printTerminalSummary)(result, safeCount, dangerousCount, suspiciousCount);
    else if (mode === 'quiet')
        (0, skill_safety_reporter_1.printQuietOutput)(overallVerdict);
    return result;
}
/**
 * CLI 入口函数。
 */
function main() {
    const args = process.argv.slice(2);
    let mode = 'terminal';
    let target = '';
    for (const arg of args) {
        switch (arg) {
            case '--help':
            case '-h':
                (0, skill_safety_reporter_1.showHelp)(skill_safety_rules_1.VERSION);
                process.exit(0);
            case '--json':
                mode = 'json';
                break;
            case '--quiet':
                mode = 'quiet';
                break;
            case '--version':
                console.log(`skill-safety-check v${skill_safety_rules_1.VERSION}`);
                process.exit(0);
            default: target = arg;
        }
    }
    if (!target) {
        (0, skill_safety_reporter_1.printError)('错误：缺少扫描目标。用法：skill-safety-check <file-or-dir>');
        process.exit(2);
    }
    const result = scanSkillSafety(target, { mode });
    process.exit(result.exitCode);
}
if (require.main === module) {
    main();
}
// 重新导出子模块（保持向后兼容）
var skill_safety_engine_2 = require("./rules/skill-safety-engine");
Object.defineProperty(exports, "findFiles", { enumerable: true, get: function () { return skill_safety_engine_2.findFiles; } });
Object.defineProperty(exports, "scanFile", { enumerable: true, get: function () { return skill_safety_engine_2.scanFile; } });
//# sourceMappingURL=skill-safety-check.js.map