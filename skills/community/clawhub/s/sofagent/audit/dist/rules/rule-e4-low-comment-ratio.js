"use strict";
// ============================================================
// E4 不低注释（扩展层 · 能力拐杖）
// 新增 > 200 行且注释率 < 5% → WARN
// evidenceMode: git-diff（纯 diff 判定，不依赖日志）
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkRuleE4 = checkRuleE4;
const ADDED_LINE_THRESHOLD = 200;
const MIN_COMMENT_RATIO = 0.05;
/**
 * 判断一行代码是否为注释行
 * 支持 //、/*、*、# 开头的注释（按语言约定，简单匹配）
 */
function isCommentLine(line) {
    const trimmed = line.trim();
    if (trimmed.startsWith('//'))
        return true;
    if (trimmed.startsWith('/*'))
        return true;
    if (trimmed.startsWith('*'))
        return true;
    if (trimmed.startsWith('#'))
        return true;
    return false;
}
function checkRuleE4(ctx) {
    const rule = {
        name: 'E4 不低注释',
        number: 204,
        status: 'PASS',
        details: [],
        evidenceMode: 'git-diff',
        ruleClass: '能力拐杖',
    };
    const { diffFiles } = ctx;
    // 统计所有 diff 文件中新增的代码行和注释行
    let addedCodeLines = 0;
    let commentLines = 0;
    for (const file of diffFiles) {
        for (const line of file.lines) {
            if (line.startsWith('+') && !line.startsWith('+++')) {
                const content = line.substring(1);
                // 跳过空行
                if (content.trim() === '')
                    continue;
                addedCodeLines++;
                if (isCommentLine(content)) {
                    commentLines++;
                }
            }
        }
    }
    // 新增 ≤ 200 行时跳过
    if (addedCodeLines <= ADDED_LINE_THRESHOLD) {
        return rule;
    }
    const commentRatio = addedCodeLines > 0 ? commentLines / addedCodeLines : 0;
    if (commentRatio < MIN_COMMENT_RATIO) {
        rule.status = 'WARN';
        rule.details.push(`新增 ${addedCodeLines} 行代码，注释行 ${commentLines} 行 (${(commentRatio * 100).toFixed(1)}%)，低于 5% 阈值。建议补充关键逻辑注释。`);
    }
    return rule;
}
//# sourceMappingURL=rule-e4-low-comment-ratio.js.map