/**
 * 错误处理
 */
export declare class ClawCompanyError extends Error {
    code: string;
    details?: any;
    constructor(message: string, code: string, details?: any);
}
export declare class AgentError extends ClawCompanyError {
    constructor(agent: string, message: string, details?: any);
}
export declare class ConfigError extends ClawCompanyError {
    constructor(message: string, details?: any);
}
export declare class TaskError extends ClawCompanyError {
    constructor(taskId: string, message: string, details?: any);
}
/**
 * 错误处理包装器
 */
export declare function withErrorHandling<T>(operation: string, fn: () => Promise<T>): Promise<T>;
