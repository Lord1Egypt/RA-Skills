import { type SafetyResult } from './rules/skill-safety-rules';
/**
 * 扫描指定目标的安全性。
 */
export declare function scanSkillSafety(target: string, options?: {
    mode?: 'terminal' | 'json' | 'quiet';
}): SafetyResult;
/**
 * CLI 入口函数。
 */
export declare function main(): void;
export { findFiles, scanFile } from './rules/skill-safety-engine';
export { type SafetyHit, type SafetyRule, type SafetyResult } from './rules/skill-safety-rules';
//# sourceMappingURL=skill-safety-check.d.ts.map