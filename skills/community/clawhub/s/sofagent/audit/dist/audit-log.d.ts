export interface AuditEntry {
    operation: string;
    target: string;
    result: string;
    timestamp?: string;
    user?: string;
    host?: string;
}
/**
 * 追加一条审计记录到 audit.md
 */
export declare function appendAuditLog(entry: AuditEntry, dataBase?: string): boolean;
/**
 * 从 task/logs 提取关键字段
 */
export declare function extractLogEntries(dataBase?: string): AuditEntry[];
/**
 * 将 task/logs 批量同步到 audit.md
 */
export declare function syncLogsToAudit(dataBase?: string): {
    total: number;
    synced: number;
};
//# sourceMappingURL=audit-log.d.ts.map