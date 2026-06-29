/** ANSI 颜色码枚举 */
export declare const Colors: {
    readonly RESET: "\u001B[0m";
    readonly BOLD: "\u001B[1m";
    readonly DIM: "\u001B[2m";
    readonly UNDERSCORE: "\u001B[4m";
    readonly BLACK: "\u001B[30m";
    readonly RED: "\u001B[31m";
    readonly GREEN: "\u001B[32m";
    readonly YELLOW: "\u001B[33m";
    readonly BLUE: "\u001B[34m";
    readonly MAGENTA: "\u001B[35m";
    readonly CYAN: "\u001B[36m";
    readonly WHITE: "\u001B[37m";
    readonly BG_RED: "\u001B[41m";
    readonly BG_GREEN: "\u001B[42m";
    readonly BG_YELLOW: "\u001B[43m";
    readonly BG_BLUE: "\u001B[44m";
};
/** 颜色辅助函数 */
export declare const color: {
    red: (text: string) => string;
    green: (text: string) => string;
    yellow: (text: string) => string;
    blue: (text: string) => string;
    cyan: (text: string) => string;
    bold: (text: string) => string;
    dim: (text: string) => string;
};
//# sourceMappingURL=colors.d.ts.map