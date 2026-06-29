"use strict";
// ============================================================
// skill-safety-engine.ts · Skill 安全审查——文件扫描引擎
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.findFiles = findFiles;
exports.scanFile = scanFile;
const fs_1 = require("fs");
const path_1 = require("path");
const skill_safety_rules_1 = require("./skill-safety-rules");
/**
 * 递归找出所有需扫描的文件。
 * 跳过隐藏目录和 node_modules。
 */
function findFiles(target) {
    if (!(0, fs_1.existsSync)(target))
        return [];
    const stat = (0, fs_1.statSync)(target);
    if (stat.isFile()) {
        const ext = (0, path_1.extname)(target).toLowerCase();
        if (skill_safety_rules_1.SCANNABLE_EXTENSIONS.has(ext))
            return [target];
        if (ext === '')
            return [target]; // 无扩展名（Makefile、Dockerfile 等）
        return [];
    }
    if (stat.isDirectory()) {
        const files = [];
        try {
            for (const entry of (0, fs_1.readdirSync)(target, { withFileTypes: true })) {
                const fullPath = (0, path_1.join)(target, entry.name);
                if (entry.isDirectory()) {
                    if (entry.name.startsWith('.') || entry.name === 'node_modules')
                        continue;
                    files.push(...findFiles(fullPath));
                }
                else if (entry.isFile()) {
                    const ext = (0, path_1.extname)(entry.name).toLowerCase();
                    if (skill_safety_rules_1.SCANNABLE_EXTENSIONS.has(ext) || ext === '')
                        files.push(fullPath);
                }
            }
        }
        catch { /* 跳过无法读取的目录 */ }
        return files;
    }
    return [];
}
/**
 * 扫描单个文件，返回命中列表。
 */
function scanFile(filePath) {
    const hits = [];
    let lines;
    try {
        lines = (0, fs_1.readFileSync)(filePath, 'utf-8').split('\n');
    }
    catch {
        return hits;
    }
    for (const rule of skill_safety_rules_1.COMPILED_RULES) {
        const re = rule.regex;
        for (let lineNum = 0; lineNum < lines.length; lineNum++) {
            const lineText = lines[lineNum];
            if (lineText !== undefined && re && re.test(lineText)) {
                hits.push({
                    file: filePath,
                    line: lineNum + 1,
                    category: rule.category,
                    severity: rule.severity,
                    pattern: rule.pattern.source,
                    description: rule.description,
                });
            }
        }
    }
    return hits;
}
//# sourceMappingURL=skill-safety-engine.js.map