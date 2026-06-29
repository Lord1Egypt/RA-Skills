/**
 * 单条任务记录——JSONL 格式
 */
export interface TaskRecord {
    /** ISO 8601 时间戳 */
    ts: string;
    /** 操作类型 */
    op: 'read' | 'write' | 'execute';
    /** 被操作的文件路径 */
    file?: string;
    /** 操作上下文/说明 */
    context?: string;
}
/**
 * 创建一条任务记录
 * @param op 操作类型（read/write/execute）
 * @param file 被操作的文件路径（可选）
 * @param context 操作上下文/说明（可选）
 */
export declare function createTaskRecord(op: TaskRecord['op'], file?: string, context?: string): TaskRecord;
/**
 * 将单条任务记录序列化为 JSONL 行
 */
export declare function serializeTaskRecord(record: TaskRecord): string;
/**
 * 将多条记录序列化为 JSONL 文本（每行一条）
 */
export declare function serializeTaskRecords(records: TaskRecord[]): string;
/**
 * 从 JSONL 文本解析回记录数组
 * 非法 JSON 行会被跳过
 */
export declare function parseTaskRecords(jsonl: string): TaskRecord[];
/**
 * 追加一条记录到 JSONL 文件
 * 用法：appendTaskRecord('.sofagent/task/logs/task.jsonl', createTaskRecord('read', 'src/index.ts'))
 * @param filePath JSONL 文件路径
 * @param record 任务记录
 */
export declare function appendTaskRecord(filePath: string, record: TaskRecord): void;
//# sourceMappingURL=task-record.d.ts.map