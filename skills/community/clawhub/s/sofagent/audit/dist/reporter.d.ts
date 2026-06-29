import type { DiffFile } from './diff-parser';
import type { LogEntry } from './log-checker';
import type { AuditConfig } from './config-loader';
import type { RuleCheck } from './rules/types';
export type { RuleCheck } from './rules/types';
export interface AuditResult {
    rules: RuleCheck[];
    exitCode: number;
}
/**
 * 运行全部审计规则（注册表模式）
 * @param diffFiles git diff 解析出的文件变更列表
 * @param logEntries 任务日志条目
 * @param task 任务描述（--task 参数）
 * @param strict 严格模式
 * @param silent 沉默模式（跳过日志依赖规则，走 diff 启发式）
 * @param commitMsg commit message（用于 E2/A5 规则及 #10 回退）
 * @param config 审计配置（.sofagent/config.yml 加载，三级 fallback）
 */
export declare function runRules(diffFiles: DiffFile[], logEntries: LogEntry[], task?: string, strict?: boolean, silent?: boolean, commitMsg?: string, config?: AuditConfig): AuditResult;
//# sourceMappingURL=reporter.d.ts.map