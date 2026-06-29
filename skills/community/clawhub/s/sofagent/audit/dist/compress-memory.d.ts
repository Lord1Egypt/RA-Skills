/**
 * 归档 60 天前的反思条目
 * @returns 移动的条目数
 */
export declare function archiveOldEntries(dataBase?: string): number;
/**
 * 备份 think.md，仅保留最近 3 份备份
 */
export declare function rotateBackups(dataBase?: string): string | null;
/**
 * 提取 think.md 摘要——最近 N 条反思的标签和结论
 */
export declare function extractSummary(dataBase?: string, limit?: number): {
    label: string;
    conclusion: string;
    date: string;
}[];
//# sourceMappingURL=compress-memory.d.ts.map