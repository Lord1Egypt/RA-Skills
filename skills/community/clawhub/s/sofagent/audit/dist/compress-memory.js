"use strict";
// ============================================================
// compress-memory.ts · think.md 合并压缩 + 日志归档
// v0.97: 从 compress-memory.sh 迁移到 TS，零外部依赖
// ============================================================
// 功能：
//   1. 归档 think.md 中 60 天前的旧反思条目到 think.archive.md
//   2. 备份当前 think.md，仅保留最近 3 份备份
//   3. 提取 think.md 摘要（最近 N 条的标签和结论）
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.archiveOldEntries = archiveOldEntries;
exports.rotateBackups = rotateBackups;
exports.extractSummary = extractSummary;
const fs_1 = require("fs");
const path_1 = require("path");
const os_1 = require("os");
const VERSION = '0.97';
/** think.md 路径 */
function getThinkPath(dataBase) {
    const base = dataBase || process.env.SOFAGENT_DATA || (0, path_1.join)((0, os_1.homedir)(), '.sofagent');
    return (0, path_1.join)(base, 'think.md');
}
/** think.archive.md 路径 */
function getArchivePath(dataBase) {
    const base = dataBase || process.env.SOFAGENT_DATA || (0, path_1.join)((0, os_1.homedir)(), '.sofagent');
    return (0, path_1.join)(base, 'think.archive.md');
}
/** 数据目录路径 */
function getDataBase() {
    return process.env.SOFAGENT_DATA || (0, path_1.join)((0, os_1.homedir)(), '.sofagent');
}
/**
 * 归档 60 天前的反思条目
 * @returns 移动的条目数
 */
function archiveOldEntries(dataBase) {
    const thinkPath = getThinkPath(dataBase);
    if (!(0, fs_1.existsSync)(thinkPath))
        return 0;
    const archivePath = getArchivePath(dataBase);
    const content = (0, fs_1.readFileSync)(thinkPath, 'utf-8');
    const sixtyDaysAgo = new Date(Date.now() - 60 * 24 * 3600 * 1000);
    const lines = content.split('\n');
    const active = [];
    const archive = [];
    let currentBlock = [];
    let currentDateStr = '';
    let moved = 0;
    for (const line of lines) {
        const dateMatch = line.match(/^##\s+(20\d{2}-\d{2}-\d{2})/);
        if (dateMatch) {
            // Output previous block
            if (currentBlock.length > 0 && currentDateStr) {
                const blockDate = new Date(currentDateStr);
                if (blockDate < sixtyDaysAgo) {
                    archive.push(...currentBlock, '');
                    moved++;
                }
                else {
                    active.push(...currentBlock, '');
                }
            }
            currentDateStr = dateMatch[1];
            currentBlock = [line];
        }
        else {
            currentBlock.push(line);
        }
    }
    // Last block
    if (currentBlock.length > 0 && currentDateStr) {
        const blockDate = new Date(currentDateStr);
        if (blockDate < sixtyDaysAgo) {
            archive.push(...currentBlock);
            moved++;
        }
        else {
            active.push(...currentBlock);
        }
    }
    if (moved > 0 && archive.length > 0) {
        (0, fs_1.writeFileSync)(thinkPath, active.join('\n'));
        const archiveContent = (0, fs_1.existsSync)(archivePath)
            ? (0, fs_1.readFileSync)(archivePath, 'utf-8') + '\n' + archive.join('\n')
            : archive.join('\n');
        (0, fs_1.writeFileSync)(archivePath, archiveContent);
    }
    return moved;
}
/**
 * 备份 think.md，仅保留最近 3 份备份
 */
function rotateBackups(dataBase) {
    const thinkPath = getThinkPath(dataBase);
    if (!(0, fs_1.existsSync)(thinkPath))
        return null;
    const base = dataBase || getDataBase();
    const dateStr = new Date().toISOString().slice(0, 10);
    const backupPath = (0, path_1.join)(base, `think.${dateStr}.bak`);
    (0, fs_1.copyFileSync)(thinkPath, backupPath);
    // 删除超过 3 份的旧备份
    const backupFiles = (0, fs_1.readdirSync)(base)
        .filter(f => f.startsWith('think.') && f.endsWith('.bak'))
        .map(f => ({ name: f, path: (0, path_1.join)(base, f), mtime: (0, fs_1.statSync)((0, path_1.join)(base, f)).mtimeMs }))
        .sort((a, b) => b.mtime - a.mtime);
    for (let i = 3; i < backupFiles.length; i++) {
        try {
            (0, fs_1.unlinkSync)(backupFiles[i].path);
        }
        catch { /* */ }
    }
    return backupPath;
}
/**
 * 提取 think.md 摘要——最近 N 条反思的标签和结论
 */
function extractSummary(dataBase, limit = 10) {
    const thinkPath = getThinkPath(dataBase);
    if (!(0, fs_1.existsSync)(thinkPath))
        return [];
    const content = (0, fs_1.readFileSync)(thinkPath, 'utf-8');
    const entries = [];
    const dateRegex = /^##\s+(20\d{2}-\d{2}-\d{2})/;
    const labelRegex = /-?\s*#([^\s#]+)/;
    const blocks = content.split(/\n(?=## 20\d{2})/);
    for (const block of blocks) {
        if (entries.length >= limit)
            break;
        const dateMatch = block.match(dateRegex);
        if (!dateMatch)
            continue;
        const labels = block.match(labelRegex);
        const label = labels ? '#' + labels[1] : '未分类';
        // 提取第一段非标题内容作为结论摘要
        const bodyLines = block.split('\n').filter(l => !l.startsWith('##') && l.trim());
        const conclusion = bodyLines.length > 0
            ? bodyLines[0].trim().slice(0, 100)
            : '无结论';
        entries.push({ label, conclusion, date: dateMatch[1] });
    }
    return entries;
}
// ── CLI ──
function main() {
    const args = process.argv.slice(2);
    const dryRun = args.includes('--dry-run');
    const summaryOnly = args.includes('--summary');
    if (args.includes('--help')) {
        console.log(`sofagent compress-memory v${VERSION}`);
        console.log('  压缩 think.md 反思区 + 日志归档');
        console.log('');
        console.log('  用法:');
        console.log('    node compress-memory.js              正常压缩');
        console.log('    node compress-memory.js --dry-run    仅预览');
        console.log('    node compress-memory.js --summary    提取摘要');
        process.exit(0);
    }
    const dataBase = getDataBase();
    (0, fs_1.mkdirSync)(dataBase, { recursive: true });
    if (summaryOnly) {
        const summary = extractSummary(dataBase);
        console.log(JSON.stringify(summary, null, 2));
        process.exit(0);
    }
    if (dryRun) {
        const thinkPath = getThinkPath(dataBase);
        if (!(0, fs_1.existsSync)(thinkPath)) {
            console.log('think.md 不存在，无需压缩');
            process.exit(0);
        }
        const stats = (0, fs_1.statSync)(thinkPath);
        console.log(`think.md: ${stats.size} bytes`);
        const entries = extractSummary(dataBase, 100);
        console.log(`反思条目: ${entries.length}`);
        console.log('--dry-run 完成。不加参数执行压缩。');
        process.exit(0);
    }
    const moved = archiveOldEntries(dataBase);
    const backup = rotateBackups(dataBase);
    console.log(`压缩完成。`);
    if (moved > 0)
        console.log(`  已归档 ${moved} 条 60 天前反思 → think.archive.md`);
    if (backup)
        console.log(`  已备份: ${backup}`);
}
// CLI 入口
if (require.main === module) {
    main();
}
//# sourceMappingURL=compress-memory.js.map