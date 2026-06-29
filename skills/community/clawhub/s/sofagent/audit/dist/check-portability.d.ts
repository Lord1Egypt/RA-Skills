export interface PortabilityReport {
    os: string;
    arch: string;
    release: string;
    bashVersion: string | null;
    gitVersion: string | null;
    nodeVersion: string | null;
    hasShasum: boolean;
    hasSha256sum: boolean;
    statType: 'gnu' | 'bsd' | 'unknown';
    issues: string[];
}
/**
 * 执行跨平台兼容性检查
 */
export declare function checkPortability(): PortabilityReport;
/**
 * 打印格式化的可移植性报告
 */
export declare function printReport(report: PortabilityReport): string;
/**
 * 快速验证 shasum/sha256sum 回退机制
 */
export declare function testHashFallback(input: string): {
    slug: string;
    ok: boolean;
    error?: string;
};
//# sourceMappingURL=check-portability.d.ts.map