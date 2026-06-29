"use strict";
// ============================================================
// log-checker.ts · 任务日志读取器
// v0.94：使用 pickLogReader 支持 Markdown 和 JSONL 两种格式
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkLogs = checkLogs;
exports.getReadAccessMap = getReadAccessMap;
exports.hasTestOrBuildExecution = hasTestOrBuildExecution;
const fs_1 = require("fs");
const path_1 = require("path");
const log_reader_1 = require("./log-reader");
/**
 * 读取 .sofagent/task/logs/ 目录中的任务记录
 * 检查哪些文件在任务中被 Read/Write 操作过
 * 支持两种格式：.md（Markdown）和 .jsonl（JSONL 结构化）
 */
function checkLogs(logDir) {
    // 优先找项目根目录的 .sofagent/，其次是当前目录
    const searchDirs = [
        logDir,
        (0, path_1.join)(process.cwd(), '.sofagent', 'task', 'logs'),
        (0, path_1.join)(process.cwd(), '..', '.sofagent', 'task', 'logs'),
    ];
    const baseWithReaders = [];
    // 第一阶段：遍历所有文件收集基础日志条目
    for (const dir of searchDirs) {
        if (!dir || !(0, fs_1.existsSync)(dir))
            continue;
        try {
            // 支持 .md 和 .jsonl 两种格式
            const files = (0, fs_1.readdirSync)(dir).filter((f) => f.endsWith('.md') || f.endsWith('.jsonl'));
            // 按修改时间排序，取最近的
            const sorted = files
                .map((f) => ({ name: f, mtime: (0, fs_1.statSync)((0, path_1.join)(dir, f)).mtime }))
                .sort((a, b) => b.mtime.getTime() - a.mtime.getTime());
            for (const { name } of sorted.slice(0, 10)) {
                try {
                    const content = (0, fs_1.readFileSync)((0, path_1.join)(dir, name), 'utf-8');
                    // 根据文件扩展名选择 reader
                    const reader = (0, log_reader_1.pickLogReader)(name);
                    const op = reader.extractOperation(content);
                    const mtime = (0, fs_1.statSync)((0, path_1.join)(dir, name)).mtime;
                    const entry = { timestamp: mtime, operation: op, raw: content };
                    baseWithReaders.push({ entry, fileName: name });
                }
                catch {
                    // 跳过无法读取的文件
                }
            }
            break; // 找到第一个有效的日志目录就跳出
        }
        catch {
            continue;
        }
    }
    // 第二阶段：基于已收集的 baseEntries 展开文件引用
    // 使用与第一阶段相同的 reader（由文件名决定格式）
    const entries = [];
    for (const { entry, fileName } of baseWithReaders) {
        entries.push(entry);
        const reader = (0, log_reader_1.pickLogReader)(fileName);
        const fileRefs = reader.extractFileReferences(entry.raw);
        for (const ref of fileRefs) {
            entries.push({ ...entry, file: ref });
        }
    }
    return entries;
}
/**
 * 生成文件被读取的摘要报告
 */
function getReadAccessMap(entries) {
    const readFiles = new Set();
    for (const entry of entries) {
        if (entry.operation === 'read' && entry.file) {
            readFiles.add(entry.file);
        }
    }
    return readFiles;
}
/**
 * 检查是否有测试/构建命令执行记录
 */
function hasTestOrBuildExecution(entries) {
    const testPatterns = [/npm test/, /npm run test/, /npm run build/, /yarn test/, /yarn build/, /pnpm test/, /pnpm build/, /make\s+(build|test)/, /gradle/, /docker\s+(build|compose\s+build)/, /tsc\s+(--noEmit|-p\b)/];
    for (const entry of entries) {
        if (entry.operation === 'execute') {
            for (const pattern of testPatterns) {
                if (pattern.test(entry.raw))
                    return true;
            }
        }
    }
    return false;
}
//# sourceMappingURL=log-checker.js.map