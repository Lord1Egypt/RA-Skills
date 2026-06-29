export interface BenchConfig {
    /** 运行次数 */
    runs: number;
    /** 超时时间（ms），超时后计为失败 */
    timeout: number;
    /** 命令 */
    command: string;
    /** 参数 */
    args?: string[];
    /** 工作目录 */
    cwd?: string;
}
export interface BenchResult {
    /** 总运行次数 */
    total: number;
    /** 成功次数 */
    success: number;
    /** 失败次数 */
    failed: number;
    /** 成功率 */
    successRate: number;
    /** 平均耗时（ms）——仅成功运行 */
    avgMs: number;
    /** 最快耗时（ms） */
    minMs: number;
    /** 最慢耗时（ms） */
    maxMs: number;
    /** 标准差（ms） */
    stdMs: number;
    /** 每次运行的耗时数组（ms）——与 total 一一对应，失败为 0 */
    durations: number[];
    /** 失败运行次数 */
    failures: {
        run: number;
        error: string;
    }[];
}
/**
 * 运行基准测试
 */
export declare function runBenchmark(config: BenchConfig): BenchResult;
/**
 * 生成 Markdown 格式的基准测试报告
 */
export declare function formatMarkdownReport(name: string, config: BenchConfig, result: BenchResult): string;
/**
 * 运行一组基准测试并汇总
 */
export declare function runSuite(tests: {
    name: string;
    config: BenchConfig;
}[]): {
    results: Record<string, BenchResult>;
    summary: string;
};
/**
 * 快速 ping 测试（验证框架可用）
 */
export declare function quickPing(iterations?: number): BenchResult;
//# sourceMappingURL=benchmark.d.ts.map