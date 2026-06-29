export type LogLevel = 'info' | 'warn' | 'error' | 'success';
/**
 * 输出带级别标签的日志消息
 */
export declare function log(level: LogLevel, message: string): void;
/** 信息级日志（蓝色） */
export declare function info(message: string): void;
/** 警告级日志（黄色） */
export declare function warn(message: string): void;
/** 错误级日志（红色） */
export declare function error(message: string): void;
/** 成功级日志（绿色） */
export declare function success(message: string): void;
/**
 * 输出带标签的标题行
 */
export declare function title(text: string): void;
/**
 * 输出分隔线
 */
export declare function separator(char?: string, length?: number): void;
//# sourceMappingURL=logger.d.ts.map