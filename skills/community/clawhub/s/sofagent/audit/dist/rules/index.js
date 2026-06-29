"use strict";
// ============================================================
// index.ts · 规则注册表
// reporter 从此导入规则数组，循环调用——不再硬编码 import 每条规则
// v0.97：铁律与审计分离——defaultRules (A1-A11) + extendedRules (E1-E4)
// ============================================================
Object.defineProperty(exports, "__esModule", { value: true });
exports.rules = exports.extendedRules = exports.defaultRules = void 0;
const rule_a1_sensitive_files_1 = require("./rule-a1-sensitive-files");
const rule_a2_secret_leak_1 = require("./rule-a2-secret-leak");
const rule_a3_careful_modify_1 = require("./rule-a3-careful-modify");
const rule_a4_config_deleted_1 = require("./rule-a4-config-deleted");
const rule_a5_honest_report_1 = require("./rule-a5-honest-report");
const rule_a6_build_broken_1 = require("./rule-a6-build-broken");
const rule_a7_read_before_write_1 = require("./rule-a7-read-before-write");
const rule_a8_verify_before_continue_1 = require("./rule-a8-verify-before-continue");
const rule_a9_no_injection_1 = require("./rule-a9-no-injection");
const rule_a10_no_poison_1 = require("./rule-a10-no-poison");
const rule_a11_no_abuse_1 = require("./rule-a11-no-abuse");
const rule_e1_no_test_files_1 = require("./rule-e1-no-test-files");
const rule_e2_todo_undeclared_1 = require("./rule-e2-todo-undeclared");
const rule_e3_large_deletion_1 = require("./rule-e3-large-deletion");
const rule_e4_low_comment_ratio_1 = require("./rule-e4-low-comment-ratio");
/** 默认规则（A1-A11）——始终生效 */
exports.defaultRules = [
    { name: 'A1 不碰敏感', number: 1, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a1_sensitive_files_1.checkRuleA1 },
    { name: 'A2 不泄密钥', number: 2, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a2_secret_leak_1.checkRuleA2 },
    { name: 'A3 不改越界', number: 3, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a3_careful_modify_1.checkRuleA3 },
    { name: 'A4 不删配置', number: 4, evidenceMode: 'git-diff', ruleClass: '能力拐杖', check: rule_a4_config_deleted_1.checkRuleA4 },
    { name: 'A5 不瞒真相', number: 5, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a5_honest_report_1.checkRuleA5 },
    { name: 'A6 不坏构建', number: 6, evidenceMode: 'git-diff', ruleClass: '能力拐杖', check: rule_a6_build_broken_1.checkRuleA6 },
    { name: 'A7 不存盲改', number: 7, evidenceMode: 'hybrid', ruleClass: '能力拐杖', check: rule_a7_read_before_write_1.checkRuleA7 },
    { name: 'A8 不逃验证', number: 8, evidenceMode: 'hybrid', ruleClass: '能力拐杖', check: rule_a8_verify_before_continue_1.checkRuleA8 },
    { name: 'A9 不纳注入', number: 9, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a9_no_injection_1.checkRuleA9 },
    { name: 'A10 不引毒源', number: 10, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a10_no_poison_1.checkRuleA10 },
    { name: 'A11 不滥资源', number: 11, evidenceMode: 'git-diff', ruleClass: '业务底线', check: rule_a11_no_abuse_1.checkRuleA11 },
];
/** 扩展规则（E1-E4）——默认不生效，需 config.extendedRulesEnabled = true */
exports.extendedRules = [
    { name: 'E1 不落测试', number: 201, evidenceMode: 'git-diff', ruleClass: '能力拐杖', check: rule_e1_no_test_files_1.checkRuleE1 },
    { name: 'E2 不空标记', number: 202, evidenceMode: 'git-diff', ruleClass: '能力拐杖', check: rule_e2_todo_undeclared_1.checkRuleE2 },
    { name: 'E3 不滥删除', number: 203, evidenceMode: 'git-diff', ruleClass: '能力拐杖', check: rule_e3_large_deletion_1.checkRuleE3 },
    { name: 'E4 不低注释', number: 204, evidenceMode: 'git-diff', ruleClass: '能力拐杖', check: rule_e4_low_comment_ratio_1.checkRuleE4 },
];
/** 全部规则——reporter 默认使用此数组（含 default + extended） */
exports.rules = [...exports.defaultRules, ...exports.extendedRules];
//# sourceMappingURL=index.js.map