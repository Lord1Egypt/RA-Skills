"use strict";
// ============================================================
// audit-log.ts · 审计日志引擎
// v0.97: 从 audit.sh 迁移到 TS，零外部依赖
// ============================================================
// 功能：追加审计日志到 MD 表格。
// 读取 .sofagent/task/logs/ → 提取关键字段 → 追加到 audit.md
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.appendAuditLog = appendAuditLog;
exports.extractLogEntries = extractLogEntries;
exports.syncLogsToAudit = syncLogsToAudit;
const fs_1 = require("fs");
const path_1 = require("path");
const os_1 = require("os");
const VERSION = '0.97';
function getDataBase() {
    return process.env.SOFAGENT_DATA || (0, path_1.join)((0, os_1.homedir)(), '.sofagent');
}
function getAuditEnabled() {
    return process.env.SOFA_AUDIT_ENABLED === 'true';
}
function escapePipe(s) {
    return s.replace(/\|/g, '\\|');
}
/**
 * 追加一条审计记录到 audit.md
 */
function appendAuditLog(entry, dataBase) {
    if (!getAuditEnabled())
        return false;
    const base = dataBase || getDataBase();
    const now = new Date();
    const month = now.toISOString().slice(0, 7);
    const date = now.toISOString().slice(0, 10);
    const auditDir = (0, path_1.join)(base, 'task', 'audit', month);
    const auditFile = (0, path_1.join)(auditDir, `${date}.md`);
    (0, fs_1.mkdirSync)(auditDir, { recursive: true });
    if (!(0, fs_1.existsSync)(auditFile)) {
        const header = `# ${date} 审计记录

| 时间 (UTC) | 操作 | 对象 | 结果 | 用户 | 主机 | 详情 |
|------------|------|------|------|------|------|------|
`;
        (0, fs_1.writeFileSync)(auditFile, header);
    }
    const utcTime = now.toISOString().slice(11, 19);
    const user = entry.user || process.env.USER || process.env.USERNAME || 'unknown';
    const host = entry.host || (() => { try {
        return require('os').hostname();
    }
    catch {
        return 'unknown';
    } })();
    const row = `| ${utcTime} | ${escapePipe(entry.operation)} | ${escapePipe(entry.target || '-')} | ${escapePipe(entry.result || '-')} | ${user} | ${host} | |\n`;
    (0, fs_1.appendFileSync)(auditFile, row);
    return true;
}
/**
 * 从 task/logs 提取关键字段
 */
function extractLogEntries(dataBase) {
    const base = dataBase || getDataBase();
    const logDir = (0, path_1.join)(base, 'task', 'logs');
    if (!(0, fs_1.existsSync)(logDir))
        return [];
    const entries = [];
    for (const monthDir of (0, fs_1.readdirSync)(logDir, { withFileTypes: true })) {
        if (!monthDir.isDirectory())
            continue;
        const monthPath = (0, path_1.join)(logDir, monthDir.name);
        for (const logFile of (0, fs_1.readdirSync)(monthPath)) {
            if (!logFile.endsWith('.md'))
                continue;
            const filePath = (0, path_1.join)(monthPath, logFile);
            try {
                const content = (0, fs_1.readFileSync)(filePath, 'utf-8');
                // 提取任务名
                const taskMatch = content.match(/\*\*任务\*\*\s*\|\s*([^|\n]+)/);
                const target = taskMatch ? taskMatch[1].trim() : logFile;
                // 提取状态
                const statusMatch = content.match(/\*\*状态\*\*\s*\|\s*([^|\n]+)/);
                const result = statusMatch ? statusMatch[1].trim() : 'unknown';
                // 提取时间
                const dateMatch = logFile.match(/^(\d{4}-\d{2}-\d{2})/);
                const timestamp = dateMatch ? dateMatch[1] : '';
                entries.push({
                    operation: 'task-record',
                    target,
                    result,
                    timestamp,
                });
            }
            catch {
                // 跳过无法解析的文件
            }
        }
    }
    return entries;
}
/**
 * 将 task/logs 批量同步到 audit.md
 */
function syncLogsToAudit(dataBase) {
    if (!getAuditEnabled())
        return { total: 0, synced: 0 };
    const entries = extractLogEntries(dataBase);
    let synced = 0;
    for (const entry of entries) {
        if (appendAuditLog(entry, dataBase))
            synced++;
    }
    return { total: entries.length, synced };
}
// ── CLI ──
function main() {
    const args = process.argv.slice(2);
    if (args.includes('--help')) {
        console.log(`sofagent audit-log v${VERSION}`);
        console.log('  审计日志引擎——从 task/logs 提取关键字段追加到 audit.md');
        console.log('');
        console.log('  用法:');
        console.log('    node audit-log.js --operation install --target "开始" --result "成功"');
        console.log('    node audit-log.js --sync               批量同步 task/logs → audit.md');
        console.log('');
        console.log('  配置:');
        console.log('    SOFA_AUDIT_ENABLED=true 启用（默认关闭）');
        process.exit(0);
    }
    // 解析参数
    let operation = '';
    let target = '';
    let result = '';
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--operation':
                operation = args[++i];
                break;
            case '--target':
                target = args[++i];
                break;
            case '--result':
                result = args[++i];
                break;
            case '--sync':
                const stats = syncLogsToAudit();
                console.log(`同步完成: ${stats.synced}/${stats.total} 条`);
                process.exit(0);
        }
    }
    if (!operation) {
        console.error('错误: --operation 为必填参数');
        process.exit(1);
    }
    const success = appendAuditLog({ operation, target, result });
    if (!success) {
        console.log('审计未启用（SOFA_AUDIT_ENABLED != true）');
    }
}
if (require.main === module) {
    main();
}
//# sourceMappingURL=audit-log.js.map