"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.main = main;
const rebateAssistantRouter_1 = require("./rebateAssistantRouter");
const CASES = [
    ["返利", "auth_guide", "start_auth"],
    ["返利宝", "auth_guide", "start_auth"],
    ["返利助手", "auth_guide", "start_auth"],
    ["教程", "auth_guide", "start_auth"],
    ["返利教程", "auth_guide", "start_auth"],
    ["返利。", "auth_guide", "start_auth"],
    ["返利宝。", "auth_guide", "start_auth"],
    ["返利！", "auth_guide", "start_auth"],
    ["返利宝！", "auth_guide", "start_auth"],
    ["返利?", "auth_guide", "start_auth"],
    ["返利宝?", "auth_guide", "start_auth"],
    ["返利，", "auth_guide", "start_auth"],
    ["返利宝，", "auth_guide", "start_auth"],
    ["教程。", "auth_guide", "start_auth"],
    ["教程！", "auth_guide", "start_auth"],
    ["返利宝如何使用", "auth_guide", "detailed_tutorial"],
    ["返利助手如何使用", "auth_guide", "detailed_tutorial"],
    ["返利如何使用", "auth_guide", "detailed_tutorial"],
    ["如何使用返利助手", "auth_guide", "detailed_tutorial"],
    ["如何使用返利宝", "auth_guide", "detailed_tutorial"],
    ["教程如何使用", "auth_guide", "detailed_tutorial"],
    ["怎么使用返利助手", "auth_guide", "detailed_tutorial"],
    ["返利助手是什么", "auth_guide", "detailed_tutorial"],
    ["返利宝怎么用", "auth_guide", "detailed_tutorial"],
    ["返利助手使用说明", "auth_guide", "detailed_tutorial"],
    ["详细教程", "auth_guide", "detailed_tutorial"],
    ["提现教程", "auth_guide", "withdraw_tutorial"],
    ["怎么提现", "auth_guide", "withdraw_tutorial"],
    ["提现规则", "auth_guide", "withdraw_tutorial"],
    ["返利宝怎么提现", "auth_guide", "withdraw_tutorial"],
    ["提现10元", "auth_guide", "withdraw_prepare"],
    ["我要提现", "auth_guide", "withdraw_prepare"],
    ["申请提现10元", "auth_guide", "withdraw_prepare"],
    ["全部提现", "auth_guide", "withdraw_prepare"],
    ["确认提现", "auth_guide", "withdraw_confirm"],
    ["确定提现", "auth_guide", "withdraw_confirm"],
    ["余额", "auth_guide", "account_balance"],
    ["账户余额", "auth_guide", "account_balance"],
    ["可提现余额", "auth_guide", "account_balance"],
    ["返利宝余额", "auth_guide", "account_balance"],
    ["查一下余额", "auth_guide", "account_balance"],
    ["订单", "auth_guide", "rebate_details"],
    ["订单明细", "auth_guide", "rebate_details"],
    ["返利明细", "auth_guide", "rebate_details"],
    ["我的订单", "auth_guide", "rebate_details"],
    ["查看返利记录", "auth_guide", "rebate_details"],
    ["我登录了吗", "auth_guide", "binding_status"],
    ["我授权了吗", "auth_guide", "binding_status"],
    ["当前绑定状态", "auth_guide", "binding_status"],
    ["有没有登录返利宝", "auth_guide", "binding_status"],
    ["授权完成", "auth_guide", "confirm_auth"],
    ["我已授权", "auth_guide", "confirm_auth"],
];
function main() {
    const failures = [];
    for (const [message, expectedScene, expectedAction] of CASES) {
        const actual = (0, rebateAssistantRouter_1.classifyScene)(message);
        if (actual.scene !== expectedScene || actual.action !== expectedAction) {
            failures.push([message, expectedScene, expectedAction, actual]);
        }
    }
    if (failures.length) {
        for (const [message, expectedScene, expectedAction, actual] of failures) {
            process.stdout.write(`FAIL: ${JSON.stringify(message)} expected scene=${expectedScene} action=${expectedAction}, got ${JSON.stringify(actual)}\n`);
        }
        return 1;
    }
    process.stdout.write(`OK: ${CASES.length} S01 routing cases passed\n`);
    return 0;
}
