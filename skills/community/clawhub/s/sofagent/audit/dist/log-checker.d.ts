export interface LogEntry {
    timestamp: Date;
    operation: string;
    file?: string;
    raw: string;
}
/**
 * 读取 .sofagent/task/logs/ 目录中的任务记录
 * 检查哪些文件在任务中被 Read/Write 操作过
 * 支持两种格式：.md（Markdown）和 .jsonl（JSONL 结构化）
 */
export declare function checkLogs(logDir?: string): LogEntry[];
/**
 * 生成文件被读取的摘要报告
 */
export declare function getReadAccessMap(entries: LogEntry[]): Set<string>;
/**
 * 检查是否有测试/构建命令执行记录
 */
export declare function hasTestOrBuildExecution(entries: LogEntry[]): boolean;
//# sourceMappingURL=log-checker.d.ts.map