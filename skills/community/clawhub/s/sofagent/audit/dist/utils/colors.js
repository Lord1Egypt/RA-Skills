"use strict";
// ============================================================
// colors.ts · ANSI 颜色码常量
// 给未来的 TypeScript 脚本用（bash→TS 迁移的前置基础设施）
// bash 侧的颜色定义保持不变——这是已知技术债，将在迁移时统一消除
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.color = exports.Colors = void 0;
/** ANSI 颜色码枚举 */
exports.Colors = {
    RESET: '\x1b[0m',
    BOLD: '\x1b[1m',
    DIM: '\x1b[2m',
    UNDERSCORE: '\x1b[4m',
    BLACK: '\x1b[30m',
    RED: '\x1b[31m',
    GREEN: '\x1b[32m',
    YELLOW: '\x1b[33m',
    BLUE: '\x1b[34m',
    MAGENTA: '\x1b[35m',
    CYAN: '\x1b[36m',
    WHITE: '\x1b[37m',
    BG_RED: '\x1b[41m',
    BG_GREEN: '\x1b[42m',
    BG_YELLOW: '\x1b[43m',
    BG_BLUE: '\x1b[44m',
};
/** 颜色辅助函数 */
exports.color = {
    red: (text) => `${exports.Colors.RED}${text}${exports.Colors.RESET}`,
    green: (text) => `${exports.Colors.GREEN}${text}${exports.Colors.RESET}`,
    yellow: (text) => `${exports.Colors.YELLOW}${text}${exports.Colors.RESET}`,
    blue: (text) => `${exports.Colors.BLUE}${text}${exports.Colors.RESET}`,
    cyan: (text) => `${exports.Colors.CYAN}${text}${exports.Colors.RESET}`,
    bold: (text) => `${exports.Colors.BOLD}${text}${exports.Colors.RESET}`,
    dim: (text) => `${exports.Colors.DIM}${text}${exports.Colors.RESET}`,
};
//# sourceMappingURL=colors.js.map