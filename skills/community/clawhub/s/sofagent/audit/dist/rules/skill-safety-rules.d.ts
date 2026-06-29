export declare const VERSION = "0.97";
export declare const SCANNABLE_EXTENSIONS: Set<string>;
/** 安全检查规则 */
export interface SafetyRule {
    pattern: RegExp;
    regex?: RegExp;
    category: string;
    severity: 'DANGEROUS' | 'SUSPICIOUS' | 'INFO';
    description: string;
}
/** 单条命中记录 */
export interface SafetyHit {
    file: string;
    line: number;
    category: string;
    severity: 'DANGEROUS' | 'SUSPICIOUS' | 'INFO';
    pattern: string;
    description: string;
}
/** 扫描结果 */
export interface SafetyResult {
    version: string;
    scannedAt: string;
    filesScanned: number;
    verdict: 'SAFE' | 'DANGEROUS' | 'SUSPICIOUS';
    exitCode: number;
    results: Array<{
        file: string;
        verdict: 'SAFE' | 'DANGEROUS' | 'SUSPICIOUS';
        hits: SafetyHit[];
    }>;
}
/** 预编译规则（去除 g flag，避免 lastIndex 状态问题） */
export declare const COMPILED_RULES: SafetyRule[];
//# sourceMappingURL=skill-safety-rules.d.ts.map