import { type SafetyHit, type SafetyResult } from './skill-safety-rules';
/** 单文件终端输出 */
export declare function printFileResult(file: string, hits: SafetyHit[], verdict: 'SAFE' | 'DANGEROUS' | 'SUSPICIOUS'): void;
/** 终端模式总结输出 */
export declare function printTerminalSummary(result: SafetyResult, safeCount: number, dangerousCount: number, suspiciousCount: number): void;
export declare function printJsonOutput(result: SafetyResult): void;
export declare function printQuietOutput(verdict: string): void;
export declare function printError(msg: string): void;
export declare function showHelp(version: string): void;
//# sourceMappingURL=skill-safety-reporter.d.ts.map