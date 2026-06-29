import type { Rule } from './types';
/** 默认规则（A1-A11）——始终生效 */
export declare const defaultRules: Rule[];
/** 扩展规则（E1-E4）——默认不生效，需 config.extendedRulesEnabled = true */
export declare const extendedRules: Rule[];
/** 全部规则——reporter 默认使用此数组（含 default + extended） */
export declare const rules: Rule[];
//# sourceMappingURL=index.d.ts.map