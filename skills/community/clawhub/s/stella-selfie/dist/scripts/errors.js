"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.localActionHint = localActionHint;
exports.normalizeNativeError = normalizeNativeError;
const LOCAL_ACTION_HINTS = {
    INPUT_INVALID: "请检查请求字段、分辨率和画幅。",
    CONFIG_INVALID: "请检查 Stella 的模型、参考图数量及授权目录配置。",
    AGENT_NOT_FOUND: "请检查绑定的 Agent ID 是否存在。",
    IDENTITY_UNREADABLE: "请检查绑定 Agent 的工作区与 IDENTITY.md。",
    NO_VALID_REFERENCE: "请在授权目录中提供至少一张有效的 JPEG、PNG 或 WebP 参考图。",
    OUTPUT_INVALID: "请由调用方决定是否重新请求；不要假定结果未生成。",
};
/** Local validation hints. Do not reuse upstream provider/network classification. */
function localActionHint(code) {
    return Object.hasOwn(LOCAL_ACTION_HINTS, code)
        ? LOCAL_ACTION_HINTS[code]
        : "请检查请求、Agent 绑定及参考图配置。";
}
/** Safe workflow errors. Never return upstream response text or credentials. */
function normalizeNativeError(error) {
    const value = error && typeof error === "object" ? error : {};
    if (value.code === "HOST_QUERY_FAILED")
        return {
            code: "HOST_QUERY_FAILED", message: "无法读取 OpenClaw 宿主元数据。",
            actionHint: "请检查宿主配置、支持的 Node 版本及 CLI 访问权限；必要时设置 OPENCLAW_CLI_PATH 指向已安装的 openclaw.mjs。",
        };
    const nested = value.error && typeof value.error === "object" ? value.error : {};
    const rawStatus = value.status ?? value.statusCode ?? nested.code;
    const status = typeof rawStatus === "string" ? Number(rawStatus) : rawStatus;
    const message = String(value.message ?? nested.message ?? error).toLowerCase();
    let code = "UNKNOWN", text = "原生图片请求未成功完成。", hint = "请检查宿主原生图片 provider、模型及网络配置。";
    if (/safety|blockedreason|block_reason/.test(message)) {
        code = "SAFETY_BLOCKED";
        text = "请求触发了模型的内容安全限制。";
        hint = "请调整提示词后由调用方重新请求。";
    }
    else if (status === 401 || /no api.?key|unauthenticated|api.?key.*(invalid|missing|not set|not configured)|auth.*profile|credential/.test(message)) {
        code = "AUTH_FAILED";
        text = "宿主原生图片认证不可用。";
        hint = "请配置绑定 Agent 的宿主原生图片认证。";
    }
    else if (status === 403 || /permission.denied|blocked.*private|network.*policy/.test(message)) {
        code = "PERMISSION_DENIED";
        text = "请求被权限或网络策略拒绝。";
        hint = "请检查模型权限和官方 API 域名的网络解析。";
    }
    else if (status === 429 || /rate.?limit|resource_exhausted/.test(message)) {
        code = "RATE_LIMITED";
        text = "宿主生图服务限流。";
        hint = "请等待后由调用方决定是否重新请求。";
    }
    else if (status === 408 || status === 504 || /timeout|timed out|deadline_exceeded/.test(message)) {
        code = "TIMEOUT";
        text = "生成等待超时，结果尚无法确认。";
        hint = "请由调用方决定是否重新请求；重新请求可能产生额外生成。";
    }
    else if (status === 400) {
        code = "INPUT_INVALID";
        text = "原生模型不接受本次参数。";
        hint = "请检查提示词、参考图及模型参数。";
    }
    else if (status === 404 || /not_found/.test(message)) {
        code = "RESOURCE_NOT_FOUND";
        text = "模型或请求资源不存在。";
        hint = "请检查宿主支持的图片模型及引用文件。";
    }
    else if (/no (images|image data|content parts)/.test(message)) {
        code = "NO_OUTPUT";
        text = "模型没有返回有效图片。";
    }
    else if (status === 500 || status === 502 || status === 503 || /unavailable|network|fetch failed|econn|enotfound|eai_again/.test(message)) {
        code = "UPSTREAM_UNAVAILABLE";
        text = "网络或原生生图服务暂不可用。";
    }
    return { code, message: text, actionHint: hint };
}
//# sourceMappingURL=errors.js.map