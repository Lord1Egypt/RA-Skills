"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.executeAction = executeAction;
exports.emitAction = emitAction;
const common_1 = require("./common");
const rebateV1Service_1 = require("./rebateV1Service");
const DETAILED_TUTORIAL = `好的,让我为您介绍一下如何使用返利助手!

━━━━━━━━━━━━━━━━━━━━━━━━━━━

【功能一:复制链接获取返利】

支持以下平台:

• 淘宝:复制商品详情页链接

• 京东:复制商品详情页链接

• 拼多多:复制商品详情页链接

操作步骤:

1. 在APP中找到心仪商品

2. 点击"分享"按钮

3. 选择"复制链接"

4. 回到对话窗口,粘贴链接给我

5. 我会自动生成返利链接和返利口令

━━━━━━━━━━━━━━━━━━━━━━━━━━━

【功能二:场景化搜索获取返利】

直接告诉我你的购物需求,例如:

• "我要买运动鞋"

• "推荐一款蓝牙耳机"

• "适合送给女朋友的礼物"

• "500元左右的手机"

• "性价比高的护肤品"

我会自动帮你搜索有佣金返利的商品!

━━━━━━━━━━━━━━━━━━━━━━━━━━━

【功能三:返利提现】

1. 下单后我会发送提现教程链接

2. 点击链接：
https://xiaomaxiangshenghuo.io.mlj130.com/follow.html
关注小马享生活公众号

3. 自动绑定,查看订单

4. 一键提现,返利到微信零钱

5. 返利金额在订单完成后3-7天到账

━━━━━━━━━━━━━━━━━━━━━━━━━━━

现在可以开始使用啦!有任何问题随时问我`;
const WITHDRAW_TUTORIAL = `💰 返利提现教程

━━━━━━━━━━━━━━━━━━━━━━━━━━━

【提现流程】

步骤1: 微信授权登录返利宝

步骤2：点击链接：
https://xiaomaxiangshenghuo.io.mlj130.com/follow.html
关注小马享生活公众号

步骤3: 自动绑定

关注公众号后,系统会自动绑定您的账号,无需额外操作

步骤4: 查看订单

在公众号内点击"我的订单",查看您的返利订单

步骤5: 一键提现

点击"立即提现",返利金额会自动到账到您的微信零钱

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提现说明

• 返利金额在订单完成后3-7天到账

• 单笔提现金额不限,满1元即可提现

• 提现到账后自动存入微信零钱

• 提现手续费全免`;
const AUTH_URL_PATTERN = /^https?:\/\//i;
const AUTH_LANDING_PAGE_URL = "https://xiaomaxiangshenghuo.io.mlj130.com/authlogin.html";
const FOLLOW_PAGE_URL = "https://xiaomaxiangshenghuo.io.mlj130.com/follow.html";
const REBATE_DETAILS_PAGE_URL = "https://xiaomaxiangshenghuo.io.mlj130.com/rebate-details.html";
const MIN_WITHDRAW_AMOUNT = 1;
const MIN_WITHDRAW_AMOUNT_TEXT = "1.00元";
const BOUND_SUCCESS_MESSAGE = [
    "你已经登录返利宝了，当前账号已完成微信授权绑定，无需重复注册或授权。",
    "",
    "现在你可以直接：",
    "1. 复制商品链接给我获取返利",
    "2. 直接告诉我想买什么",
    "3. 回复“提现教程”查看返现方式",
].join("\n");
function isValidAuthUrl(authUrl) {
    return AUTH_URL_PATTERN.test(String(authUrl || "").trim());
}
function buildAuthLandingUrl(machineCode) {
    const normalized = String(machineCode || "").trim();
    if (!normalized) {
        throw new Error("machine_code 不能为空");
    }
    return `${AUTH_LANDING_PAGE_URL}?machinecode=${encodeURIComponent(normalized)}`;
}
function buildErrorPayload(stage, code, message) {
    return { stage, code, message };
}
function buildResultData(payload) {
    const result = {};
    Object.entries(payload || {}).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
            result[key] = value;
        }
    });
    return result;
}
function withStandardResult(payload, options) {
    const normalized = { ...payload };
    normalized.result_type = options.resultType;
    normalized.result_data = options.resultData || {};
    normalized.error = options.error || null;
    if (normalized.code === undefined && options.error) {
        normalized.code = options.error.code;
    }
    return normalized;
}
function buildWelcomeAuthMessage(authUrl) {
    if (!isValidAuthUrl(authUrl)) {
        throw new Error("missing auth_url");
    }
    return [
        "使用前请先注册账号并关注公众号：",
        "",
        "注册链接：",
        "",
        authUrl,
        "",
        "关注公众号后，返回回复“授权完成”",
        "",
        "之后就可以：",
        "",
        "复制商品链接获取返利",
        "",
        "场景化搜索获取返利",
        "",
        "下单后一键提现",
        "",
        "如需详情；可回复【详细教程】【提现教程】",
    ].join("\n");
}
function buildRebateDetailsUrl(openId) {
    const normalizedOpenId = String(openId || "").trim();
    if (!normalizedOpenId) {
        return "";
    }
    return `${REBATE_DETAILS_PAGE_URL}?openid=${encodeURIComponent(normalizedOpenId)}`;
}
function buildWithdrawTutorialMessage(openId = "") {
    const normalizedOpenId = String(openId || "").trim();
    if (!normalizedOpenId) {
        return WITHDRAW_TUTORIAL;
    }
    const orderUrl = buildRebateDetailsUrl(normalizedOpenId);
    return `💰 返利提现教程

━━━━━━━━━━━━━━━━━━━━━━━━━━━

【提现流程】

步骤1: 微信授权登录返利宝

步骤2：点击链接：
https://xiaomaxiangshenghuo.io.mlj130.com/follow.html
关注小马享生活公众号

步骤3: 自动绑定

关注公众号后,系统会自动绑定您的账号,无需额外操作

步骤4: 查看订单

在公众号内点击"我的订单",查看您的返利订单，也可以点击链接
${orderUrl}
查询

步骤5: 一键提现

点击"立即提现",返利金额会自动到账到您的微信零钱

━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提现说明

• 返利金额在订单完成后3-7天到账

• 单笔提现金额不限,满1元即可提现

• 提现到账后自动存入微信零钱

• 提现手续费全免`;
}
function buildRebateDetailsUserMessage(openId) {
    return `你可以点击下面链接查看订单明细和返利明细：\n\n${buildRebateDetailsUrl(openId)}`;
}
function buildAccountBalanceWithRebateDetailsUserMessage(balance, openId) {
    const userMessage = (0, rebateV1Service_1.buildAccountBalanceUserMessage)(balance);
    const detailsUrl = buildRebateDetailsUrl(openId);
    if (!detailsUrl) {
        return userMessage;
    }
    return `${userMessage}\n\n查看订单明细和返利明细：\n${detailsUrl}`;
}
function toFiniteNumber(value) {
    const numberValue = Number(value);
    return Number.isFinite(numberValue) ? numberValue : null;
}
function extractWithdrawAmount(rawMessage) {
    const message = String(rawMessage || "").trim();
    if (!message) {
        return null;
    }
    const patterns = [
        /(?:提现|提取)\s*(?:金额)?\s*[¥￥]?\s*(\d+(?:\.\d+)?)\s*(?:元|块|rmb|RMB)?/,
        /[¥￥]?\s*(\d+(?:\.\d+)?)\s*(?:元|块|rmb|RMB)?\s*(?:提现|提取)/,
    ];
    for (const pattern of patterns) {
        const match = message.match(pattern);
        if (!match) {
            continue;
        }
        const amount = Number(match[1]);
        if (Number.isFinite(amount)) {
            return amount;
        }
    }
    return null;
}
function buildWithdrawBalanceAskAmountUserMessage(balance) {
    return [
        "当前账户可提现金额如下：",
        "",
        `可提现金额：${(0, rebateV1Service_1.formatPrice)(balance.available_amount)}元`,
        `提现中金额：${(0, rebateV1Service_1.formatPrice)(balance.withdrawing_amount)}元`,
        `冻结金额：${(0, rebateV1Service_1.formatPrice)(balance.frozen_amount)}元`,
        "",
        "当前可提现金额满足提现条件。",
        "请告诉我你要提现的金额，例如：提现10元",
    ].join("\n");
}
function buildWithdrawBalanceInsufficientUserMessage(balance) {
    return [
        "当前暂不可提现。",
        "",
        `可提现金额：${(0, rebateV1Service_1.formatPrice)(balance.available_amount)}元`,
        `最低提现金额：${MIN_WITHDRAW_AMOUNT_TEXT}`,
        `提现中金额：${(0, rebateV1Service_1.formatPrice)(balance.withdrawing_amount)}元`,
        "",
        "可提现金额未达到最低提现条件，暂时不能发起提现。",
    ].join("\n");
}
function buildWithdrawAmountTooSmallUserMessage(amount) {
    return [
        "提现金额不能低于1.00元。",
        "",
        `当前申请提现：${(0, rebateV1Service_1.formatPrice)(amount)}元`,
        "请重新输入提现金额，例如：提现10元",
    ].join("\n");
}
function buildWithdrawAmountTooLargeUserMessage(amount, availableAmount) {
    return [
        "提现金额大于可提现金额。",
        "",
        `当前可提现金额：${(0, rebateV1Service_1.formatPrice)(availableAmount)}元`,
        `当前申请提现：${(0, rebateV1Service_1.formatPrice)(amount)}元`,
        "",
        "请重新输入不超过可提现金额的提现金额。",
    ].join("\n");
}
function buildWithdrawConfirmationUserMessage(amount, balance) {
    return [
        "提现前请先确认你已经关注小马享生活公众号，否则无法顺利领取微信红包。",
        "",
        "关注链接：",
        FOLLOW_PAGE_URL,
        "",
        "提现确认信息：",
        `提现金额：${(0, rebateV1Service_1.formatPrice)(amount)}元`,
        `可提现金额：${(0, rebateV1Service_1.formatPrice)(balance.available_amount)}元`,
        `提现中金额：${(0, rebateV1Service_1.formatPrice)(balance.withdrawing_amount)}元`,
        "",
        "确认无误后，请回复：",
        "确认提现",
    ].join("\n");
}
function buildWithdrawApplySuccessUserMessage(withdraw, openId) {
    const detailsUrl = buildRebateDetailsUrl(openId);
    const lines = [
        "提现申请已提交，请注意去微信查看红包。",
        "",
        `提现金额：${(0, rebateV1Service_1.formatPrice)(withdraw.amount)}元`,
        `提现状态：${withdraw.status || "processing"}`,
        `申请单号：${withdraw.request_no || withdraw.withdraw_id || "无"}`,
        `提交时间：${withdraw.created_at || "无"}`,
    ];
    if (withdraw.arrival_text) {
        lines.push(`到账说明：${withdraw.arrival_text}`);
    }
    if (detailsUrl) {
        lines.push("", "提现记录可以点击下面链接查询：", detailsUrl);
    }
    return lines.join("\n");
}
function buildWithdrawApplyFailureUserMessage(message) {
    return [
        "提现申请失败。",
        "",
        `失败原因：${message}`,
        "",
        "请稍后重试，或者前往小马享生活公众号进行提现",
        "关注链接：",
        FOLLOW_PAGE_URL,
    ].join("\n");
}
function getLocalOpenId(machineCode) {
    const binding = (0, common_1.loadLocalOpenidBinding)(machineCode) || {};
    return String(binding.open_id || "").trim();
}
function hasLocalOpenid(machineCode) {
    return Boolean(getLocalOpenId(machineCode));
}
function buildBindingCheckPayload(machineCode, openId) {
    return {
        machine_code: machineCode,
        openid: String(openId || "").trim(),
    };
}
function normalizeRemoteBindingData(machineCode, data) {
    const payload = data || {};
    const bindStatus = String(payload.bind_status || "").trim() || "unbound";
    const openId = String(payload.openid || "").trim();
    const authUrl = String(payload.auth_url || "").trim();
    return {
        machine_code: String(payload.machine_code || "").trim() || machineCode,
        open_id: openId,
        bind_status: bindStatus,
        status: bindStatus,
        authorized: bindStatus === "bound" && Boolean(openId),
        auth_url: authUrl,
        can_withdraw: Boolean(payload.can_withdraw || false),
        available_amount: payload.available_amount ?? 0,
        pending_amount: payload.pending_amount ?? 0,
    };
}
function syncRemoteBindingState(machineCode, data) {
    const normalized = normalizeRemoteBindingData(machineCode, data);
    (0, common_1.updateLocalAuthState)(machineCode, {
        machine_code: machineCode,
        status: normalized.status,
        bind_status: normalized.bind_status,
        auth_url: normalized.auth_url,
        open_id: normalized.open_id || null,
        can_withdraw: normalized.can_withdraw,
        available_amount: normalized.available_amount,
        pending_amount: normalized.pending_amount,
    });
    if (normalized.authorized) {
        (0, common_1.saveLocalOpenidBinding)({
            machine_code: machineCode,
            open_id: normalized.open_id,
            can_withdraw: normalized.can_withdraw,
            available_amount: normalized.available_amount,
            pending_amount: normalized.pending_amount,
        });
    }
    return normalized;
}
async function fetchRemoteBindingStatus(machineCode) {
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/auth/binding-check", buildBindingCheckPayload(machineCode, getLocalOpenId(machineCode)));
    return syncRemoteBindingState(machineCode, response.data || {});
}
function buildAuthUrlData(machineCode) {
    const authUrl = buildAuthLandingUrl(machineCode);
    if (!isValidAuthUrl(authUrl)) {
        throw new Error("未生成有效注册链接");
    }
    const data = {
        machine_code: machineCode,
        auth_url: authUrl,
        expire_at: null,
    };
    (0, common_1.updateLocalAuthState)(machineCode, {
        machine_code: machineCode,
        status: "pending",
        bind_status: "unbound",
        auth_url: authUrl,
        expire_at: data.expire_at,
        open_id: getLocalOpenId(machineCode) || null,
    });
    return data;
}
function extractRuntimeErrorMessage(error, defaultMessage) {
    const rawMessage = String(error instanceof Error ? error.message : error || "").trim();
    if (!rawMessage) {
        return defaultMessage;
    }
    try {
        const payload = JSON.parse(rawMessage);
        const detail = payload.detail || {};
        if (detail && typeof detail === "object" && detail.message) {
            return String(detail.message);
        }
        return String(payload.message || rawMessage);
    }
    catch {
        return rawMessage;
    }
}
async function resolveMachineCode() {
    return await (0, common_1.getOrCreateMachineCode)();
}
async function buildBindingStatusResponse() {
    const machineCode = await resolveMachineCode();
    const localBinding = (0, common_1.loadLocalOpenidBinding)(machineCode);
    let binding = null;
    try {
        binding = await fetchRemoteBindingStatus(machineCode);
    }
    catch {
        binding = null;
    }
    if (binding?.authorized) {
        return [
            withStandardResult({
                success: true,
                module: "operation-guide",
                intent: "binding_status",
                next_action: "enter_rebate_flow",
                step: "check_binding_status",
                machine_code: machineCode,
                authorized: true,
                open_id: binding.open_id,
                binding,
                message: "当前已完成微信授权绑定",
                user_message: "你已经登录返利宝了，当前微信授权已完成。\n\n现在你可以：\n1. 发送商品链接获取返利\n2. 直接说想买什么商品让我帮你搜索",
            }, {
                resultType: "binding_status",
                resultData: buildResultData({
                    authorized: true,
                    open_id: binding.open_id,
                    binding,
                }),
            }),
            0,
        ];
    }
    if (localBinding) {
        return [
            withStandardResult({
                success: true,
                module: "operation-guide",
                intent: "binding_status",
                next_action: "enter_rebate_flow",
                step: "check_binding_status",
                machine_code: machineCode,
                authorized: true,
                open_id: localBinding.open_id,
                binding: localBinding,
                message: "当前已完成微信授权绑定",
                user_message: "你已经登录返利宝了，当前本地存在已绑定的微信授权信息。\n\n现在你可以：\n1. 发送商品链接获取返利\n2. 直接说想买什么商品让我帮你搜索",
            }, {
                resultType: "binding_status",
                resultData: buildResultData({
                    authorized: true,
                    open_id: localBinding.open_id,
                    binding: localBinding,
                }),
            }),
            0,
        ];
    }
    return [
        withStandardResult({
            success: true,
            module: "operation-guide",
            intent: "binding_status",
            next_action: "start_auth",
            step: "check_binding_status",
            machine_code: machineCode,
            authorized: false,
            auth_url: binding?.auth_url || null,
            message: "当前未检测到已绑定 openId",
            user_message: "你现在还没有登录返利宝。回复【返利】开始授权登录。",
        }, {
            resultType: "binding_status",
            resultData: buildResultData({
                authorized: false,
                auth_url: binding?.auth_url || null,
            }),
        }),
        0,
    ];
}
async function buildAuthLinkResponse() {
    const machineCode = await resolveMachineCode();
    let binding = null;
    if (hasLocalOpenid(machineCode)) {
        try {
            binding = await fetchRemoteBindingStatus(machineCode);
        }
        catch {
            binding = null;
        }
    }
    if (binding?.authorized) {
        return [
            withStandardResult({
                success: true,
                step: "generate_wechat_auth_link",
                machine_code: machineCode,
                auth_url: "",
                status: "bound",
                message: "当前已完成微信授权绑定",
                already_bound: true,
                open_id: binding.open_id,
            }, {
                resultType: "auth_link",
                resultData: buildResultData({
                    status: "bound",
                    already_bound: true,
                    open_id: binding.open_id,
                    auth_url: "",
                }),
            }),
            0,
        ];
    }
    let authUrl = "";
    let expireAt = null;
    try {
        const response = buildAuthUrlData(machineCode);
        authUrl = String(response.auth_url || "").trim();
        expireAt = response.expire_at || null;
    }
    catch (error) {
        const message = extractRuntimeErrorMessage(error, "注册链接生成失败");
        return [
            withStandardResult({
                success: false,
                step: "generate_wechat_auth_link",
                machine_code: machineCode,
                auth_url: "",
                status: "error",
                message,
            }, {
                resultType: "auth_link",
                resultData: buildResultData({ status: "error", auth_url: "" }),
                error: buildErrorPayload("generate_auth_link", "AUTH_LINK_ERROR", message),
            }),
            1,
        ];
    }
    return [
        withStandardResult({
            success: true,
            step: "generate_wechat_auth_link",
            machine_code: machineCode,
            auth_url: authUrl,
            status: "pending",
            expire_at: expireAt,
            message: "微信授权链接已生成",
            tips: ["请将 auth_url 发给用户打开。", "用户完成登录后，提示其回复“我已授权”。"],
        }, {
            resultType: "auth_link",
            resultData: buildResultData({
                status: "pending",
                auth_url: authUrl,
                expire_at: expireAt,
            }),
        }),
        0,
    ];
}
async function buildStartAuthResponse() {
    const machineCode = await resolveMachineCode();
    const binding = (0, common_1.loadLocalOpenidBinding)(machineCode);
    if (binding) {
        return [
            withStandardResult({
                success: true,
                module: "operation-guide",
                intent: "auth_already_bound",
                next_action: "enter_rebate_flow",
                machine_code: machineCode,
                authorized: true,
                open_id: binding.open_id,
                user_message: BOUND_SUCCESS_MESSAGE,
            }, {
                resultType: "auth_binding",
                resultData: buildResultData({
                    authorized: true,
                    open_id: binding.open_id,
                }),
            }),
            0,
        ];
    }
    let authUrl = null;
    try {
        const [authLinkPayload] = await buildAuthLinkResponse();
        if (authLinkPayload.already_bound || authLinkPayload.status === "bound") {
            const openId = String(authLinkPayload.open_id || "").trim();
            if (openId) {
                (0, common_1.saveLocalOpenidBinding)({
                    machine_code: machineCode,
                    open_id: openId,
                    can_withdraw: false,
                    available_amount: 0,
                    pending_amount: 0,
                });
            }
            (0, common_1.updateLocalAuthState)(machineCode, {
                machine_code: machineCode,
                status: "bound",
                bind_status: "bound",
                auth_url: "",
                open_id: openId || null,
            });
            return [
                withStandardResult({
                    success: true,
                    module: "operation-guide",
                    intent: "auth_already_bound",
                    next_action: "enter_rebate_flow",
                    machine_code: machineCode,
                    authorized: true,
                    open_id: openId,
                    user_message: BOUND_SUCCESS_MESSAGE,
                }, {
                    resultType: "auth_binding",
                    resultData: buildResultData({
                        authorized: true,
                        open_id: openId,
                    }),
                }),
                0,
            ];
        }
        authUrl = authLinkPayload.auth_url || null;
    }
    catch {
        authUrl = null;
    }
    const success = isValidAuthUrl(authUrl || "");
    const userMessage = success
        ? buildWelcomeAuthMessage(String(authUrl || ""))
        : "注册链接生成失败，请稍后重试。\n\n当前没有生成有效的注册链接。";
    const nextAction = success ? "open_auth_url" : "retry_auth_link";
    const code = success ? null : "AUTH_URL_MISSING";
    return [
        withStandardResult({
            success,
            module: "operation-guide",
            intent: "start_auth",
            next_action: nextAction,
            machine_code: machineCode,
            authorized: false,
            auth_url: authUrl,
            code,
            user_message: userMessage,
        }, {
            resultType: "auth_binding",
            resultData: buildResultData({
                authorized: false,
                auth_url: authUrl,
            }),
            error: success ? null : buildErrorPayload("generate_auth_link", "AUTH_URL_MISSING", userMessage),
        }),
        success ? 0 : 1,
    ];
}
async function buildExchangeOpenidResponse() {
    const machineCode = await resolveMachineCode();
    let binding;
    try {
        binding = await fetchRemoteBindingStatus(machineCode);
    }
    catch (error) {
        const message = extractRuntimeErrorMessage(error, "绑定状态检查失败");
        return [
            withStandardResult({
                success: false,
                step: "exchange_openid",
                machine_code: machineCode,
                status: "unknown",
                message,
                code: "BINDING_CHECK_FAILED",
                tips: ["请检查返利测试环境接口是否可用。", "如果接口正常，再让用户重新回复“我已授权”。"],
            }, {
                resultType: "auth_binding",
                resultData: buildResultData({ status: "unknown" }),
                error: buildErrorPayload("check_binding_status", "BINDING_CHECK_FAILED", message),
            }),
            1,
        ];
    }
    if (!binding.authorized) {
        return [
            withStandardResult({
                success: false,
                step: "exchange_openid",
                machine_code: machineCode,
                status: binding.status,
                auth_url: binding.auth_url,
                message: "尚未检测到微信授权完成",
                code: "AUTH_NOT_COMPLETED",
                tips: ["请先打开授权链接完成微信登录。", "完成后，再次执行本脚本或让用户重新回复“我已授权”。"],
            }, {
                resultType: "auth_binding",
                resultData: buildResultData({
                    status: binding.status,
                    auth_url: binding.auth_url,
                    authorized: false,
                }),
                error: buildErrorPayload("confirm_auth", "AUTH_NOT_COMPLETED", "尚未检测到微信授权完成"),
            }),
            1,
        ];
    }
    return [
        withStandardResult({
            success: true,
            step: "exchange_openid",
            machine_code: machineCode,
            open_id: binding.open_id,
            message: "openId 已同步",
            local_store: "wechat-openid-store.json",
        }, {
            resultType: "auth_binding",
            resultData: buildResultData({
                authorized: true,
                open_id: binding.open_id,
                local_store: "wechat-openid-store.json",
            }),
        }),
        0,
    ];
}
async function executePendingRebateRequest(request) {
    const rawMessage = request.raw_message;
    if (request.scene === "link_rebate") {
        const { buildResponse } = await Promise.resolve().then(() => __importStar(require("./m02PlatformLink")));
        const payload = await buildResponse(rawMessage);
        return [payload, payload.success ? 0 : 1];
    }
    if (request.scene === "search_rebate") {
        const { buildResponse } = await Promise.resolve().then(() => __importStar(require("./productSearch")));
        const payload = await buildResponse(rawMessage);
        return [payload, payload.success ? 0 : 1];
    }
    return null;
}
async function resumePendingRebateRequest(machineCode) {
    const request = (0, common_1.loadPendingAuthRequest)(machineCode);
    if (!request) {
        return null;
    }
    (0, common_1.clearPendingAuthRequest)(machineCode);
    const resumed = await executePendingRebateRequest(request);
    if (!resumed) {
        return null;
    }
    const [payload, exitCode] = resumed;
    payload.resumed_after_auth = true;
    payload.pending_auth_request = {
        scene: request.scene,
        handler: request.handler,
        created_at: request.created_at,
    };
    return [payload, exitCode];
}
async function buildConfirmAuthResponse() {
    const machineCode = await resolveMachineCode();
    const [exchangePayload, exitCode] = await buildExchangeOpenidResponse();
    if (exitCode !== 0) {
        const payload = JSON.parse(JSON.stringify(exchangePayload));
        if (payload.code === "BINDING_CHECK_FAILED") {
            const message = payload.message || "授权状态查询失败";
            payload.module = "operation-guide";
            payload.intent = "binding_check_failed";
            payload.next_action = "retry_confirm_auth";
            payload.authorized = false;
            payload.user_message = `授权状态查询失败，请稍后重试。\n\n${message}`;
            return [
                withStandardResult(payload, {
                    resultType: "auth_binding",
                    resultData: buildResultData({
                        authorized: false,
                        auth_url: payload.auth_url || null,
                        open_id: payload.open_id,
                        status: payload.status,
                    }),
                    error: buildErrorPayload("confirm_auth", payload.code || "BINDING_CHECK_FAILED", message),
                }),
                1,
            ];
        }
        const localSession = (0, common_1.loadLocalAuthState)(machineCode) || {};
        let authUrl = payload.auth_url || localSession.auth_url || null;
        if (!authUrl) {
            try {
                const [authLinkPayload] = await buildAuthLinkResponse();
                authUrl = authLinkPayload.auth_url || null;
            }
            catch {
                authUrl = null;
            }
        }
        let userMessage = "我还没有检测到授权完成。\n\n请先打开刚才的授权链接完成登录，然后再回复“我已授权”。";
        if (authUrl) {
            userMessage = `我还没有检测到授权完成。\n\n请先打开下面的授权链接完成登录：\n\n${authUrl}\n\n完成后再回复“我已授权”。`;
        }
        payload.module = "operation-guide";
        payload.intent = "auth_not_completed";
        payload.next_action = "wait_auth_confirmation";
        payload.authorized = false;
        payload.auth_url = authUrl;
        payload.user_message = userMessage;
        return [
            withStandardResult(payload, {
                resultType: "auth_binding",
                resultData: buildResultData({
                    authorized: false,
                    auth_url: authUrl,
                    open_id: payload.open_id,
                    status: payload.status,
                }),
                error: buildErrorPayload("confirm_auth", payload.code || "AUTH_NOT_COMPLETED", payload.message || "尚未检测到微信授权完成"),
            }),
            1,
        ];
    }
    const binding = { open_id: exchangePayload.open_id };
    const localSession = (0, common_1.loadLocalAuthState)(machineCode) || {};
    if (Object.keys(localSession).length) {
        localSession.status = "bound";
        localSession.bind_status = "bound";
        localSession.open_id = binding.open_id;
        (0, common_1.updateLocalAuthState)(machineCode, localSession);
    }
    const payload = withStandardResult({
        success: true,
        module: "operation-guide",
        intent: "auth_confirmed",
        next_action: "enter_rebate_flow",
        machine_code: machineCode,
        authorized: true,
        open_id: binding.open_id,
        user_message: BOUND_SUCCESS_MESSAGE,
    }, {
        resultType: "auth_binding",
        resultData: buildResultData({
            authorized: true,
            open_id: binding.open_id,
        }),
    });
    const resumed = await resumePendingRebateRequest(machineCode);
    if (resumed) {
        return resumed;
    }
    return [payload, 0];
}
function buildDetailedTutorialResponse() {
    return [
        withStandardResult({
            success: true,
            module: "operation-guide",
            intent: "detailed_tutorial",
            next_action: "send_detailed_tutorial",
            user_message: DETAILED_TUTORIAL,
        }, {
            resultType: "tutorial",
            resultData: buildResultData({ tutorial_type: "detailed_tutorial" }),
        }),
        0,
    ];
}
async function buildWithdrawTutorialResponse() {
    let openId = "";
    try {
        openId = getLocalOpenId(await resolveMachineCode());
    }
    catch {
        openId = "";
    }
    return [
        withStandardResult({
            success: true,
            module: "operation-guide",
            intent: "withdraw_tutorial",
            next_action: "send_withdraw_tutorial",
            user_message: buildWithdrawTutorialMessage(openId),
        }, {
            resultType: "tutorial",
            resultData: buildResultData({ tutorial_type: "withdraw_tutorial" }),
        }),
        0,
    ];
}
async function buildRebateDetailsResponse() {
    let openId = "";
    try {
        ({ openId } = await (0, rebateV1Service_1.requireBoundOpenid)());
    }
    catch {
        return await buildStartAuthResponse();
    }
    const detailsUrl = buildRebateDetailsUrl(openId);
    return [
        withStandardResult({
            success: true,
            module: "operation-guide",
            intent: "rebate_details",
            next_action: "open_rebate_details",
            authorized: true,
            open_id: openId,
            rebate_details_url: detailsUrl,
            user_message: buildRebateDetailsUserMessage(openId),
        }, {
            resultType: "rebate_details",
            resultData: buildResultData({
                authorized: true,
                open_id: openId,
                rebate_details_url: detailsUrl,
            }),
        }),
        0,
    ];
}
async function buildAccountBalanceResponse() {
    let openId = "";
    try {
        ({ openId } = await (0, rebateV1Service_1.requireBoundOpenid)());
    }
    catch {
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "account_balance",
                next_action: "start_auth",
                authorized: false,
                user_message: "查询账户余额前请先完成微信授权。回复【返利】开始授权登录。",
            }, {
                resultType: "account_balance",
                resultData: buildResultData({ authorized: false }),
                error: buildErrorPayload("auth", "AUTH_REQUIRED", "查询账户余额前请先完成微信授权。"),
            }),
            1,
        ];
    }
    let balance;
    try {
        balance = await (0, rebateV1Service_1.queryAccountBalance)(openId);
    }
    catch (error) {
        const message = (0, rebateV1Service_1.extractServiceErrorMessage)(error, "账户余额查询失败");
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "account_balance",
                next_action: "retry_account_balance",
                authorized: true,
                open_id: openId,
                user_message: `账户余额查询失败，请稍后重试。\n\n${message}`,
            }, {
                resultType: "account_balance",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                }),
                error: buildErrorPayload("account_balance", "ACCOUNT_BALANCE_QUERY_ERROR", message),
            }),
            1,
        ];
    }
    const detailsUrl = buildRebateDetailsUrl(openId);
    return [
        withStandardResult({
            success: true,
            module: "operation-guide",
            intent: "account_balance",
            next_action: "return_account_balance",
            authorized: true,
            open_id: openId,
            balance,
            rebate_details_url: detailsUrl,
            user_message: buildAccountBalanceWithRebateDetailsUserMessage(balance, openId),
        }, {
            resultType: "account_balance",
            resultData: buildResultData({
                authorized: true,
                open_id: openId,
                balance,
                rebate_details_url: detailsUrl,
            }),
        }),
        0,
    ];
}
async function buildWithdrawPrepareResponse(rawMessage = "") {
    const amount = extractWithdrawAmount(rawMessage);
    if (amount !== null && amount < MIN_WITHDRAW_AMOUNT) {
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "withdraw_prepare",
                next_action: "ask_withdraw_amount",
                code: "WITHDRAW_AMOUNT_TOO_SMALL",
                amount,
                user_message: buildWithdrawAmountTooSmallUserMessage(amount),
            }, {
                resultType: "withdraw",
                resultData: buildResultData({ amount }),
                error: buildErrorPayload("withdraw_prepare", "WITHDRAW_AMOUNT_TOO_SMALL", "提现金额不能低于1.00元。"),
            }),
            0,
        ];
    }
    let machineCode = "";
    let openId = "";
    try {
        ({ machineCode, openId } = await (0, rebateV1Service_1.requireBoundOpenid)());
    }
    catch {
        return await buildStartAuthResponse();
    }
    let balance;
    try {
        balance = await (0, rebateV1Service_1.queryAccountBalance)(openId);
    }
    catch (error) {
        const message = (0, rebateV1Service_1.extractServiceErrorMessage)(error, "账户余额查询失败");
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "withdraw_prepare",
                next_action: "retry_withdraw_prepare",
                code: "WITHDRAW_BALANCE_QUERY_ERROR",
                authorized: true,
                open_id: openId,
                amount,
                user_message: `提现前余额查询失败，请稍后重试。\n\n${message}`,
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                    amount,
                }),
                error: buildErrorPayload("withdraw_prepare", "WITHDRAW_BALANCE_QUERY_ERROR", message),
            }),
            0,
        ];
    }
    const availableAmount = toFiniteNumber(balance.available_amount) ?? 0;
    const withdrawingAmount = toFiniteNumber(balance.withdrawing_amount);
    if (amount === null) {
        (0, common_1.clearPendingWithdrawRequest)(machineCode);
        if (availableAmount < MIN_WITHDRAW_AMOUNT) {
            return [
                withStandardResult({
                    success: false,
                    module: "operation-guide",
                    intent: "withdraw_prepare",
                    next_action: "wait_withdrawable_balance",
                    code: "WITHDRAW_AVAILABLE_AMOUNT_TOO_SMALL",
                    authorized: true,
                    open_id: openId,
                    balance,
                    user_message: buildWithdrawBalanceInsufficientUserMessage(balance),
                }, {
                    resultType: "withdraw",
                    resultData: buildResultData({
                        authorized: true,
                        open_id: openId,
                        balance,
                    }),
                    error: buildErrorPayload("withdraw_prepare", "WITHDRAW_AVAILABLE_AMOUNT_TOO_SMALL", "可提现金额未达到最低提现条件。"),
                }),
                0,
            ];
        }
        return [
            withStandardResult({
                success: true,
                module: "operation-guide",
                intent: "withdraw_prepare",
                next_action: "ask_withdraw_amount",
                authorized: true,
                open_id: openId,
                balance,
                user_message: buildWithdrawBalanceAskAmountUserMessage(balance),
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                    balance,
                }),
            }),
            0,
        ];
    }
    if (amount > availableAmount) {
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "withdraw_prepare",
                next_action: "ask_withdraw_amount",
                code: "WITHDRAW_AMOUNT_EXCEEDS_AVAILABLE",
                authorized: true,
                open_id: openId,
                amount,
                balance,
                user_message: buildWithdrawAmountTooLargeUserMessage(amount, availableAmount),
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                    amount,
                    balance,
                }),
                error: buildErrorPayload("withdraw_prepare", "WITHDRAW_AMOUNT_EXCEEDS_AVAILABLE", "提现金额大于可提现金额。"),
            }),
            0,
        ];
    }
    const pendingWithdraw = (0, common_1.savePendingWithdrawRequest)(machineCode, {
        openid: openId,
        amount,
        availableAmount,
        withdrawingAmount,
    });
    return [
        withStandardResult({
            success: true,
            module: "operation-guide",
            intent: "withdraw_prepare",
            next_action: "confirm_withdraw",
            authorized: true,
            open_id: openId,
            amount,
            balance,
            pending_withdraw: pendingWithdraw,
            user_message: buildWithdrawConfirmationUserMessage(amount, balance),
        }, {
            resultType: "withdraw",
            resultData: buildResultData({
                authorized: true,
                open_id: openId,
                amount,
                balance,
                pending_withdraw: pendingWithdraw,
            }),
        }),
        0,
    ];
}
async function buildWithdrawConfirmResponse() {
    let machineCode = "";
    let openId = "";
    try {
        ({ machineCode, openId } = await (0, rebateV1Service_1.requireBoundOpenid)());
    }
    catch {
        return await buildStartAuthResponse();
    }
    const pendingWithdraw = (0, common_1.loadPendingWithdrawRequest)(machineCode);
    if (!pendingWithdraw) {
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "withdraw_confirm",
                next_action: "ask_withdraw_amount",
                code: "WITHDRAW_PENDING_NOT_FOUND",
                authorized: true,
                open_id: openId,
                user_message: "没有找到待确认的提现申请。请先输入提现金额，例如：提现10元",
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                }),
                error: buildErrorPayload("withdraw_confirm", "WITHDRAW_PENDING_NOT_FOUND", "没有找到待确认的提现申请。"),
            }),
            1,
        ];
    }
    if (String(pendingWithdraw.openid || "").trim() !== openId) {
        (0, common_1.clearPendingWithdrawRequest)(machineCode);
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "withdraw_confirm",
                next_action: "ask_withdraw_amount",
                code: "WITHDRAW_PENDING_OPENID_MISMATCH",
                authorized: true,
                open_id: openId,
                user_message: "待确认的提现申请已失效。请重新输入提现金额，例如：提现10元",
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                }),
                error: buildErrorPayload("withdraw_confirm", "WITHDRAW_PENDING_OPENID_MISMATCH", "待确认的提现申请已失效。"),
            }),
            1,
        ];
    }
    const amount = Number(pendingWithdraw.amount);
    try {
        const withdraw = await (0, rebateV1Service_1.applyWithdraw)(openId, amount);
        (0, common_1.clearPendingWithdrawRequest)(machineCode);
        return [
            withStandardResult({
                success: true,
                module: "operation-guide",
                intent: "withdraw_confirm",
                next_action: "return_withdraw_result",
                authorized: true,
                open_id: openId,
                amount,
                withdraw,
                user_message: buildWithdrawApplySuccessUserMessage({ amount, ...withdraw }, openId),
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                    amount,
                    withdraw,
                }),
            }),
            0,
        ];
    }
    catch (error) {
        const message = (0, rebateV1Service_1.extractServiceErrorMessage)(error, "提现申请失败");
        (0, common_1.clearPendingWithdrawRequest)(machineCode);
        return [
            withStandardResult({
                success: false,
                module: "operation-guide",
                intent: "withdraw_confirm",
                next_action: "retry_withdraw_or_use_official_account",
                code: "WITHDRAW_APPLY_ERROR",
                authorized: true,
                open_id: openId,
                amount,
                pending_withdraw: pendingWithdraw,
                user_message: buildWithdrawApplyFailureUserMessage(message),
            }, {
                resultType: "withdraw",
                resultData: buildResultData({
                    authorized: true,
                    open_id: openId,
                    amount,
                    pending_withdraw: pendingWithdraw,
                }),
                error: buildErrorPayload("withdraw_confirm", "WITHDRAW_APPLY_ERROR", message),
            }),
            1,
        ];
    }
}
async function executeAction(action, rawMessage = "") {
    const actionMap = {
        binding_status: buildBindingStatusResponse,
        auth_link: buildAuthLinkResponse,
        start_auth: buildStartAuthResponse,
        exchange_openid: buildExchangeOpenidResponse,
        confirm_auth: buildConfirmAuthResponse,
        detailed_tutorial: buildDetailedTutorialResponse,
        withdraw_tutorial: buildWithdrawTutorialResponse,
        withdraw_prepare: () => buildWithdrawPrepareResponse(rawMessage),
        withdraw_confirm: buildWithdrawConfirmResponse,
        rebate_details: buildRebateDetailsResponse,
        account_balance: buildAccountBalanceResponse,
    };
    if (!actionMap[action]) {
        throw new Error(`unsupported action: ${action}`);
    }
    return await actionMap[action]();
}
async function emitAction(action, outputFormat = "json", rawMessage = "") {
    const [payload, exitCode] = await executeAction(action, rawMessage);
    if (outputFormat === "json") {
        (0, common_1.printJson)(payload);
    }
    else {
        (0, common_1.printUserMessage)(payload.user_message || "", { markdown: outputFormat === "md" });
    }
    const handledWithdrawMessage = outputFormat !== "json" && payload.result_type === "withdraw" && Boolean(String(payload.user_message || "").trim());
    return handledWithdrawMessage ? 0 : exitCode;
}
