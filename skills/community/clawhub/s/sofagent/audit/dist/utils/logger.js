"use strict";
// ============================================================
// logger.ts · 基础日志函数
// 给未来的 TypeScript 脚本用（bash→TS 迁移的前置基础设施）
// 替代 bash 脚本中重复定义的 echo颜色/日志格式函数
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.log = log;
exports.info = info;
exports.warn = warn;
exports.error = error;
exports.success = success;
exports.title = title;
exports.separator = separator;
const colors_1 = require("./colors");
/** 日志级别前缀 */
const LEVEL_PREFIX = {
    info: `${colors_1.Colors.BLUE}[INFO]${colors_1.Colors.RESET}`,
    warn: `${colors_1.Colors.YELLOW}[WARN]${colors_1.Colors.RESET}`,
    error: `${colors_1.Colors.RED}[ERROR]${colors_1.Colors.RESET}`,
    success: `${colors_1.Colors.GREEN}[OK]${colors_1.Colors.RESET}`,
};
/**
 * 输出带级别标签的日志消息
 */
function log(level, message) {
    const prefix = LEVEL_PREFIX[level];
    console.log(`${prefix} ${message}`);
}
/** 信息级日志（蓝色） */
function info(message) {
    log('info', message);
}
/** 警告级日志（黄色） */
function warn(message) {
    log('warn', message);
}
/** 错误级日志（红色） */
function error(message) {
    log('error', message);
}
/** 成功级日志（绿色） */
function success(message) {
    log('success', message);
}
/**
 * 输出带标签的标题行
 */
function title(text) {
    console.log(`\n${colors_1.color.bold(colors_1.color.cyan('=== ' + text + ' ==='))}\n`);
}
/**
 * 输出分隔线
 */
function separator(char = '-', length = 60) {
    console.log(char.repeat(length));
}
//# sourceMappingURL=logger.js.map