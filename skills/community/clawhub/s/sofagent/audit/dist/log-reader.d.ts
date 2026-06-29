/**
 * 日志读取器统一接口
 * 不同格式（Markdown / JSONL）实现此接口，实现格式无关的日志解析
 */
export interface LogReader {
    /** 从日志内容中提取操作类型（read/write/execute/other） */
    extractOperation(content: string): string;
    /** 从日志内容中提取被操作的文件路径列表 */
    extractFileReferences(content: string): string[];
}
/**
 * Markdown 日志读取器
 * 迁移自 log-checker.ts 原有的 extractOperation / extractFileReferences
 */
export declare class MarkdownLogReader implements LogReader {
    /**
     * 从 Markdown 日志内容中提取操作类型
     * 结构化操作上下文检查（逐行匹配）+ 否定语义过滤
     */
    extractOperation(content: string): string;
    /**
     * 从 Markdown 日志内容中提取被操作的文件路径
     */
    extractFileReferences(content: string): string[];
}
/**
 * JSONL 日志读取器
 * 解析 { ts, op, file, context } 格式的结构化日志
 */
export declare class JSONLLogReader implements LogReader {
    /**
     * 解析 JSONL 提取操作类型
     * 统计 op 出现频率，按优先级返回（read > write > execute > other）
     */
    extractOperation(content: string): string;
    /**
     * 解析 JSONL 提取文件引用列表
     */
    extractFileReferences(content: string): string[];
}
/**
 * 根据文件扩展名选择日志读取器
 * .jsonl → JSONLLogReader，其他 → MarkdownLogReader
 */
export declare function pickLogReader(filePath: string): LogReader;
//# sourceMappingURL=log-reader.d.ts.map