"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildResponse = buildResponse;
exports.emitResponse = emitResponse;
const common_1 = require("./common");
const m01OperationGuide_1 = require("./m01OperationGuide");
const recognizePlatformLink_1 = require("./recognizePlatformLink");
const rebateV1Service_1 = require("./rebateV1Service");
function buildErrorPayload(stage, code, message) {
    return { stage, code, message: String(message || "").trim() };
}
function buildResultData(response, resolvedLink, searchResult, item, lease, rebateResult) {
    return {
        platform: response.platform,
        original_link: response.original_link,
        resolved_link: resolvedLink || null,
        search_result: searchResult || null,
        selected_item: item || null,
        lease: lease || null,
        rebate_result: rebateResult || null,
    };
}
async function normalizeLinkSearchInput(platform, originalLink) {
    let searchInput = String(originalLink || "").trim();
    let resolvedLink = null;
    let host = "";
    try {
        host = new URL(originalLink || "").hostname.trim().toLowerCase();
    }
    catch {
        host = "";
    }
    if (platform === "taobao" && host === "e.tb.cn") {
        resolvedLink = await (0, common_1.resolveTaobaoShortLink)(originalLink);
        searchInput = resolvedLink || searchInput;
    }
    return { searchInput, resolvedLink };
}
async function buildStartAuthResponseForLink(rawMessage) {
    try {
        (0, common_1.savePendingAuthRequest)(await (0, common_1.getOrCreateMachineCode)(), {
            scene: "link_rebate",
            handler: "m02_platform_link",
            rawMessage,
            reason: "链接返利场景执行时发现未授权",
        });
    }
    catch {
        // Best-effort only. Failing to persist pending request should not block auth link generation.
    }
    const [payload] = await (0, m01OperationGuide_1.executeAction)("start_auth");
    return payload;
}
async function buildResponse(rawMessage) {
    const response = (0, recognizePlatformLink_1.recognizeRawMessage)(rawMessage);
    if (!response.success) {
        return {
            ...response,
            module: "platform-link-rebate",
            intent: "create_rebate_link",
            next_action: "ask_for_supported_link",
            result_type: "link_rebate",
            result_data: buildResultData(response),
            error: buildErrorPayload("recognize_link", response.code || "UNSUPPORTED_LINK", "当前链接暂不支持返利识别，仅支持淘宝、京东、拼多多商品链接。"),
        };
    }
    if (response.platform === "multiple") {
        return {
            ...response,
            success: false,
            code: "MULTIPLE_LINKS_FOUND",
            next_action: "ask_for_single_link",
            result_type: "link_rebate",
            result_data: buildResultData(response),
            error: buildErrorPayload("recognize_link", "MULTIPLE_LINKS_FOUND", "检测到多个商品链接，请一次只发一个。"),
            user_message: `${String(response.user_message || "").trim()}\n\n请一次只发一个商品链接，我再帮你生成返利链接。`,
        };
    }
    let openId = "";
    try {
        ({ openId } = await (0, rebateV1Service_1.requireBoundOpenid)());
    }
    catch {
        return await buildStartAuthResponseForLink(rawMessage);
    }
    const platform = response.platform;
    const originalLink = response.original_link || rawMessage;
    let rawTextForLinkSearch = originalLink;
    let resolvedLink = null;
    try {
        const normalized = await normalizeLinkSearchInput(platform, originalLink);
        rawTextForLinkSearch = normalized.searchInput;
        resolvedLink = normalized.resolvedLink;
    }
    catch (error) {
        return {
            ...response,
            success: false,
            code: "TAOBAO_SHORT_LINK_RESOLVE_ERROR",
            next_action: "retry_link_search",
            result_type: "link_rebate",
            result_data: buildResultData(response),
            error: buildErrorPayload("resolve_short_link", "TAOBAO_SHORT_LINK_RESOLVE_ERROR", (0, rebateV1Service_1.extractServiceErrorMessage)(error, "短链解析失败")),
            user_message: `淘宝短链识别成功，但最终商品链接解析失败，请稍后重试或直接发送商品详情页链接。\n\n${(0, rebateV1Service_1.extractServiceErrorMessage)(error, "短链解析失败")}`,
        };
    }
    let searchResult;
    try {
        searchResult = await (0, rebateV1Service_1.searchProductByLink)(openId, platform, rawTextForLinkSearch);
    }
    catch (error) {
        return {
            ...response,
            success: false,
            code: "LINK_SEARCH_API_ERROR",
            next_action: "retry_link_search",
            result_type: "link_rebate",
            result_data: buildResultData(response, resolvedLink, null),
            error: buildErrorPayload("search_product", "LINK_SEARCH_API_ERROR", (0, rebateV1Service_1.extractServiceErrorMessage)(error, "商品查询失败")),
            search_result: null,
            user_message: `链接识别成功，但商品查询失败，请稍后重试。\n\n${(0, rebateV1Service_1.extractServiceErrorMessage)(error, "商品查询失败")}`,
        };
    }
    const items = Array.isArray(searchResult.items) ? searchResult.items : [];
    if (!items.length) {
        return {
            ...response,
            success: false,
            code: "LINK_PRODUCT_NOT_FOUND",
            next_action: "ask_for_supported_link",
            result_type: "link_rebate",
            result_data: buildResultData(response, resolvedLink, searchResult),
            error: buildErrorPayload("search_product", "LINK_PRODUCT_NOT_FOUND", "暂时没查到这个链接对应的返利商品。"),
            search_result: searchResult,
            user_message: "暂时没查到这个链接对应的返利商品，请换一个商品详情页链接再试。",
        };
    }
    const item = items[0];
    let lease;
    let convertResult;
    try {
        lease = await (0, rebateV1Service_1.applyAdzoneLease)(openId, item.platform || platform);
        convertResult = await (0, rebateV1Service_1.createRebateLink)(openId, lease.lease_id, item.platform || platform, item.item_id, rawTextForLinkSearch);
    }
    catch (error) {
        return {
            ...response,
            success: false,
            code: "REBATE_LINK_CREATE_ERROR",
            next_action: "retry_rebate_link_create",
            result_type: "link_rebate",
            result_data: buildResultData(response, resolvedLink, searchResult, item, typeof lease !== "undefined" ? lease : null),
            error: buildErrorPayload("create_rebate_link", "REBATE_LINK_CREATE_ERROR", (0, rebateV1Service_1.extractServiceErrorMessage)(error, "返利链接生成失败")),
            search_result: searchResult,
            selected_item: item,
            user_message: `商品已识别，但返利链接生成失败，请稍后重试。\n\n${(0, rebateV1Service_1.extractServiceErrorMessage)(error, "返利链接生成失败")}`,
        };
    }
    return {
        ...response,
        success: true,
        module: "platform-link-rebate",
        intent: "create_rebate_link",
        next_action: "return_rebate_link",
        result_type: "link_rebate",
        result_data: buildResultData(response, resolvedLink, searchResult, item, lease, convertResult),
        error: null,
        resolved_link: resolvedLink,
        search_result: searchResult,
        selected_item: item,
        lease,
        rebate_result: convertResult,
        user_message: (0, rebateV1Service_1.buildConvertResultUserMessage)(convertResult),
    };
}
async function emitResponse(rawMessage, outputFormat) {
    const response = await buildResponse(rawMessage);
    if (outputFormat === "json") {
        (0, common_1.printJson)(response);
    }
    else {
        (0, common_1.printUserMessage)(response.user_message || "", { markdown: outputFormat === "md" });
    }
    return response.success ? 0 : 1;
}
