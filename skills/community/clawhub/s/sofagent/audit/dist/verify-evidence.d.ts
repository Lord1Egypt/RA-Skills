/**
 * 扫描日志文件中的客观证据（测试/lint/build 关键词）。
 * @param filePath - 日志文件路径，默认 `${cwd}/.sofagent/task/logs/${YYYY-MM}/${YYYY-MM-DD}.md`
 * @param daemonMode - 静默模式，不输出 console
 * @returns 0 = 已验证（有证据），1 = 未验证（无证据或无日志）
 */
export declare function verifyEvidence(filePath?: string, daemonMode?: boolean): number;
/**
 * CLI 入口函数，处理 process.argv。
 */
export declare function main(): void;
//# sourceMappingURL=verify-evidence.d.ts.map