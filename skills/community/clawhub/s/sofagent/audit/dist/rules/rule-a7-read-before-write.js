"use strict";
// ============================================================
// A7 不存盲改（过程层 · 能力拐杖）
// 被修改的文件，修改前是否有 Read 操作记录（检查 .sofagent/task/logs/ 目录）
// 违规 → exit code 2
// v0.94：新增 --silent 双路径——无日志 + silent 走 diff 启发式，只 WARN 不 FAIL
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkRuleA7 = checkRuleA7;
const path_1 = require("path");
const log_checker_1 = require("../log-checker");
function checkRuleA7(ctx) {
    const { diffFiles, logEntries } = ctx;
    const rule = {
        name: 'A7 不存盲改',
        number: 7,
        status: 'PASS',
        details: [],
        evidenceMode: 'hybrid',
        ruleClass: '能力拐杖',
    };
    const readFiles = (0, log_checker_1.getReadAccessMap)(logEntries);
    const modifiedFiles = diffFiles
        .filter((f) => f.status === 'modified' || f.status === 'added')
        .map((f) => f.path);
    // 如果没有需要检查的修改文件（全是 deleted 或 renamed），跳过检查
    if (modifiedFiles.length === 0) {
        return rule;
    }
    // 双路径：无日志 + silent → 走 diff 启发式，只 WARN 不 FAIL
    if (ctx.silent && logEntries.length === 0) {
        rule.status = 'WARN';
        rule.details.push('--silent 模式：无任务日志，跳过精确「不存盲改」检查（git diff 无法证明读取行为）。');
        return rule;
    }
    // 如果没有日志记录（可能是新项目或日志被清空），发出提示但不判定违规
    if (logEntries.length === 0) {
        if (ctx.strict) {
            rule.status = 'FAIL';
            rule.details.push('--strict 模式：未找到任务日志，「不存盲改」检查失败。Agent 必须记录操作日志。');
        }
        else {
            rule.status = 'WARN';
            rule.details.push('未找到 .sofagent/task/logs/ 任务记录——可能是首次使用或日志目录为空。跳过「不存盲改」检查。');
        }
        return rule;
    }
    const uncheckedFiles = [];
    for (const path of modifiedFiles) {
        // 精确文件名匹配——比对 path.basename，避免子串误报（config.ts ≠ tsconfig.json）
        const targetName = (0, path_1.basename)(path);
        let found = false;
        // 第一优先：精确比对 readFiles 集合中的 basename
        for (const readFile of readFiles) {
            if ((0, path_1.basename)(readFile) === targetName) {
                found = true;
                break;
            }
        }
        // 第二优先：仅匹配日志中 Read 操作条目（不匹配整篇日志的任意文件名引用）
        if (!found) {
            for (const entry of logEntries) {
                if (entry.operation !== 'read')
                    continue;
                if (entry.file && (0, path_1.basename)(entry.file) === targetName) {
                    found = true;
                    break;
                }
            }
        }
        if (!found) {
            uncheckedFiles.push(path);
        }
    }
    if (uncheckedFiles.length > 0) {
        rule.status = 'FAIL';
        rule.details.push(`${uncheckedFiles.length} 个文件被修改但无读取记录: ${uncheckedFiles.slice(0, 3).join(', ')}${uncheckedFiles.length > 3 ? ` 等 ${uncheckedFiles.length} 个` : ''}`);
    }
    else {
        rule.status = 'PASS';
    }
    return rule;
}
//# sourceMappingURL=rule-a7-read-before-write.js.map