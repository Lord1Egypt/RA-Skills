export interface DiffItem {
    field: string;
    today: number;
    yesterday: number;
    change: number;
}
export declare function compareData(todayData: Record<string, unknown>, yesterdayData: Record<string, unknown>): DiffItem[];
//# sourceMappingURL=compare.d.ts.map