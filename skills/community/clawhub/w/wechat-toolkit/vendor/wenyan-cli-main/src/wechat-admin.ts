import { tokenStore } from "@wenyan-md/core/wrapper";

const WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin";
const DEFAULT_POLL_INTERVAL_MS = 5_000;
const DEFAULT_WAIT_TIMEOUT_MS = 120_000;
const DEFAULT_LIST_COUNT = 20;
const MAX_LIST_COUNT = 20;
const TOKEN_REFRESH_ERROR_CODES = new Set([40001, 40014, 42001]);

interface WechatApiErrorPayload {
    errcode?: number;
    errmsg?: string;
    rid?: string;
}

interface WechatAccessTokenResponse extends WechatApiErrorPayload {
    access_token?: string;
    expires_in?: number;
}

export interface WechatCredentialOptions {
    appId?: string;
    appSecret?: string;
}

export interface WechatListOptions extends WechatCredentialOptions {
    offset?: number;
    count?: number;
    noContent?: boolean;
}

export interface WaitForPublishOptions extends WechatCredentialOptions {
    intervalMs?: number;
    timeoutMs?: number;
}

export interface WechatArticle {
    title?: string;
    author?: string;
    digest?: string;
    content?: string;
    content_source_url?: string;
    thumb_media_id?: string;
    thumb_url?: string;
    show_cover_pic?: number;
    need_open_comment?: number;
    only_fans_can_comment?: number;
    url?: string;
    is_deleted?: boolean;
}

export interface DraftGetResponse extends WechatApiErrorPayload {
    news_item?: WechatArticle[];
    create_time?: number;
    update_time?: number;
}

export interface DraftCountResponse extends WechatApiErrorPayload {
    total_count: number;
}

export interface DraftBatchContent {
    news_item?: WechatArticle[];
    create_time?: number;
    update_time?: number;
}

export interface DraftBatchItem {
    media_id: string;
    content?: DraftBatchContent;
    update_time?: number;
}

export interface DraftBatchGetResponse extends WechatApiErrorPayload {
    total_count: number;
    item_count: number;
    item: DraftBatchItem[];
}

export interface DraftDeleteResponse extends WechatApiErrorPayload {
    errcode: number;
    errmsg: string;
}

export interface DraftPublishResponse extends WechatApiErrorPayload {
    errcode: number;
    errmsg: string;
    publish_id: string;
    msg_data_id?: string;
}

export interface PublishArticleDetailItem {
    idx: number;
    article_url: string;
}

export interface PublishArticleDetail {
    count?: number;
    item?: PublishArticleDetailItem[];
}

export interface PublishStatusResponse extends WechatApiErrorPayload {
    publish_id: string;
    publish_status: number;
    article_id?: string;
    article_detail?: PublishArticleDetail;
    fail_idx?: number[];
}

export interface PublishedArticleGetResponse extends WechatApiErrorPayload {
    news_item?: WechatArticle[];
}

export interface PublishedBatchContent {
    news_item?: WechatArticle[];
    create_time?: number;
    update_time?: number;
}

export interface PublishedBatchItem {
    article_id: string;
    content?: PublishedBatchContent;
    update_time?: number;
}

export interface PublishedBatchGetResponse extends WechatApiErrorPayload {
    total_count: number;
    item_count: number;
    item: PublishedBatchItem[];
}

export interface PublishedDeleteResponse extends WechatApiErrorPayload {
    errcode: number;
    errmsg: string;
}

function resolveCredentials(options: WechatCredentialOptions = {}) {
    const appId = options.appId ?? process.env.WECHAT_APP_ID;
    const appSecret = options.appSecret ?? process.env.WECHAT_APP_SECRET;

    if (!appId || !appSecret) {
        throw new Error("请通过环境变量 WECHAT_APP_ID / WECHAT_APP_SECRET 提供公众号凭据");
    }

    return { appId, appSecret };
}

function assertIdentifier(value: string, label: string) {
    if (!value.trim()) {
        throw new Error(`缺少必要参数：${label}`);
    }
}

function assertNonNegativeInteger(value: number, label: string) {
    if (!Number.isInteger(value) || value < 0) {
        throw new Error(`${label} 必须是大于等于 0 的整数`);
    }
}

function assertListCount(value: number) {
    if (!Number.isInteger(value) || value < 1 || value > MAX_LIST_COUNT) {
        throw new Error(`count 必须是 1 到 ${MAX_LIST_COUNT} 之间的整数`);
    }
}

function buildWechatErrorMessage(payload: WechatApiErrorPayload, action: string) {
    const detail = payload.errmsg ?? "unknown error";
    const rid = payload.rid ? ` rid: ${payload.rid}` : "";
    return `${action}失败 (${payload.errcode}): ${detail}${rid}`;
}

function assertWechatSuccess(payload: WechatApiErrorPayload, action: string) {
    if (typeof payload.errcode === "number" && payload.errcode !== 0) {
        throw new Error(buildWechatErrorMessage(payload, action));
    }
}

async function fetchWechatAccessToken(appId: string, appSecret: string, forceRefresh = false): Promise<string> {
    const cachedToken = !forceRefresh ? tokenStore.getToken(appId) : null;
    if (cachedToken) {
        return cachedToken;
    }

    const url = `${WECHAT_API_BASE}/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`;
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`获取 access_token 失败: HTTP ${response.status} ${response.statusText}`);
    }

    const payload = (await response.json()) as WechatAccessTokenResponse;
    assertWechatSuccess(payload, "获取 access_token");

    if (!payload.access_token || !payload.expires_in) {
        throw new Error(`获取 access_token 失败: ${JSON.stringify(payload)}`);
    }

    await tokenStore.setToken(appId, payload.access_token, payload.expires_in);
    return payload.access_token;
}

async function requestWechatJson<T extends WechatApiErrorPayload>(
    method: "GET" | "POST",
    endpoint: string,
    action: string,
    options: WechatCredentialOptions = {},
    body?: Record<string, unknown>,
    forceRefreshToken = false,
): Promise<T> {
    const { appId, appSecret } = resolveCredentials(options);
    const accessToken = await fetchWechatAccessToken(appId, appSecret, forceRefreshToken);
    const url = `${WECHAT_API_BASE}${endpoint}?access_token=${accessToken}`;

    const response = await fetch(url, {
        method,
        headers:
            method === "POST"
                ? {
                      "Content-Type": "application/json",
                  }
                : undefined,
        body: method === "POST" ? JSON.stringify(body ?? {}) : undefined,
    });

    if (!response.ok) {
        throw new Error(`${action}失败: HTTP ${response.status} ${response.statusText}`);
    }

    const payload = (await response.json()) as T;
    if (
        !forceRefreshToken &&
        typeof payload.errcode === "number" &&
        TOKEN_REFRESH_ERROR_CODES.has(payload.errcode)
    ) {
        return await requestWechatJson<T>(method, endpoint, action, options, body, true);
    }

    assertWechatSuccess(payload, action);
    return payload;
}

async function postWechatJson<T extends WechatApiErrorPayload>(
    endpoint: string,
    body: Record<string, unknown>,
    action: string,
    options: WechatCredentialOptions = {},
): Promise<T> {
    return await requestWechatJson<T>("POST", endpoint, action, options, body);
}

async function getWechatJson<T extends WechatApiErrorPayload>(
    endpoint: string,
    action: string,
    options: WechatCredentialOptions = {},
): Promise<T> {
    return await requestWechatJson<T>("GET", endpoint, action, options);
}

function resolveListOptions(options: WechatListOptions = {}) {
    const offset = options.offset ?? 0;
    const count = options.count ?? DEFAULT_LIST_COUNT;

    assertNonNegativeInteger(offset, "offset");
    assertListCount(count);

    return {
        offset,
        count,
        no_content: options.noContent ? 1 : 0,
    };
}

export async function getWechatDraft(
    mediaId: string,
    options: WechatCredentialOptions = {},
): Promise<DraftGetResponse> {
    assertIdentifier(mediaId, "media_id");
    return await postWechatJson<DraftGetResponse>("/draft/get", { media_id: mediaId }, "获取草稿", options);
}

export async function listWechatDrafts(
    options: WechatListOptions = {},
): Promise<DraftBatchGetResponse> {
    return await postWechatJson<DraftBatchGetResponse>(
        "/draft/batchget",
        resolveListOptions(options),
        "获取草稿列表",
        options,
    );
}

export async function countWechatDrafts(
    options: WechatCredentialOptions = {},
): Promise<DraftCountResponse> {
    return await getWechatJson<DraftCountResponse>("/draft/count", "获取草稿总数", options);
}

export async function deleteWechatDraft(
    mediaId: string,
    options: WechatCredentialOptions = {},
): Promise<DraftDeleteResponse> {
    assertIdentifier(mediaId, "media_id");
    return await postWechatJson<DraftDeleteResponse>("/draft/delete", { media_id: mediaId }, "删除草稿", options);
}

export async function submitWechatDraftPublish(
    mediaId: string,
    options: WechatCredentialOptions = {},
): Promise<DraftPublishResponse> {
    assertIdentifier(mediaId, "media_id");
    return await postWechatJson<DraftPublishResponse>(
        "/freepublish/submit",
        { media_id: mediaId },
        "提交正式发布",
        options,
    );
}

export async function getWechatPublishStatus(
    publishId: string,
    options: WechatCredentialOptions = {},
): Promise<PublishStatusResponse> {
    assertIdentifier(publishId, "publish_id");
    return await postWechatJson<PublishStatusResponse>(
        "/freepublish/get",
        { publish_id: publishId },
        "查询发布状态",
        options,
    );
}

export async function listWechatPublishedArticles(
    options: WechatListOptions = {},
): Promise<PublishedBatchGetResponse> {
    return await postWechatJson<PublishedBatchGetResponse>(
        "/freepublish/batchget",
        resolveListOptions(options),
        "获取已发布文章列表",
        options,
    );
}

export async function getWechatPublishedArticle(
    articleId: string,
    options: WechatCredentialOptions = {},
): Promise<PublishedArticleGetResponse> {
    assertIdentifier(articleId, "article_id");
    return await postWechatJson<PublishedArticleGetResponse>(
        "/freepublish/getarticle",
        { article_id: articleId },
        "获取已发布文章",
        options,
    );
}

export async function deleteWechatPublishedArticle(
    articleId: string,
    index = 0,
    options: WechatCredentialOptions = {},
): Promise<PublishedDeleteResponse> {
    assertIdentifier(articleId, "article_id");
    assertNonNegativeInteger(index, "index");
    return await postWechatJson<PublishedDeleteResponse>(
        "/freepublish/delete",
        { article_id: articleId, index },
        "删除已发布文章",
        options,
    );
}

export function getPublishStatusText(status: number) {
    switch (status) {
        case 0:
            return "发布成功";
        case 1:
            return "发布中";
        case 2:
            return "原创校验失败";
        case 3:
            return "常规发布失败";
        case 4:
            return "平台审核不通过";
        case 5:
            return "发布成功后用户删除全部文章";
        case 6:
            return "发布成功后系统封禁全部文章";
        default:
            return `未知状态 (${status})`;
    }
}

export function isTerminalPublishStatus(status: number) {
    return status !== 1;
}

function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function waitForWechatPublishResult(
    publishId: string,
    options: WaitForPublishOptions = {},
): Promise<PublishStatusResponse> {
    const intervalMs = options.intervalMs ?? DEFAULT_POLL_INTERVAL_MS;
    const timeoutMs = options.timeoutMs ?? DEFAULT_WAIT_TIMEOUT_MS;
    const startedAt = Date.now();

    while (true) {
        const status = await getWechatPublishStatus(publishId, options);
        if (isTerminalPublishStatus(status.publish_status)) {
            return status;
        }

        if (Date.now() - startedAt >= timeoutMs) {
            throw new Error(
                `等待正式发布结果超时（${Math.ceil(timeoutMs / 1000)} 秒），请稍后使用 publish-status 命令继续查询`,
            );
        }

        await sleep(intervalMs);
    }
}

function formatTimestamp(timestamp?: number) {
    if (typeof timestamp !== "number" || Number.isNaN(timestamp)) {
        return "未知";
    }

    return new Date(timestamp * 1000).toLocaleString("zh-CN", {
        hour12: false,
    });
}

function summarizeArticle(article: WechatArticle, index: number) {
    const lines = [`第${index + 1} 篇: ${article.title ?? "(无标题)"}`];

    if (article.author) {
        lines.push(`作者: ${article.author}`);
    }
    if (article.digest) {
        lines.push(`摘要: ${article.digest}`);
    }
    if (article.url) {
        lines.push(`链接: ${article.url}`);
    }
    if (article.content_source_url) {
        lines.push(`原文: ${article.content_source_url}`);
    }
    if (typeof article.content === "string") {
        lines.push(`正文长度: ${article.content.length} 字符`);
    }
    if (article.thumb_url) {
        lines.push(`封面图: ${article.thumb_url}`);
    }

    return lines.join("\n");
}

export function formatDraft(draft: DraftGetResponse, mediaId?: string) {
    const articles = draft.news_item ?? [];
    const lines = [
        `草稿 Media ID: ${mediaId ?? "(未知)"}`,
        `创建时间: ${formatTimestamp(draft.create_time)}`,
        `更新时间: ${formatTimestamp(draft.update_time)}`,
        `文章数: ${articles.length}`,
    ];

    if (articles.length === 0) {
        lines.push("暂无文章内容");
        return lines.join("\n");
    }

    for (const [index, article] of articles.entries()) {
        lines.push("");
        lines.push(summarizeArticle(article, index));
    }

    return lines.join("\n");
}

export function formatDraftCount(result: DraftCountResponse) {
    return `草稿总数: ${result.total_count}`;
}

export function formatDraftList(result: DraftBatchGetResponse, offset = 0) {
    const lines = [`草稿总数: ${result.total_count}`, `本次返回: ${result.item_count}`];

    if (!result.item.length) {
        lines.push("暂无草稿");
        return lines.join("\n");
    }

    for (const [index, item] of result.item.entries()) {
        const label = `#${offset + index + 1} ${item.media_id}`;
        lines.push("");
        lines.push(label);
        lines.push(`更新时间: ${formatTimestamp(item.content?.update_time ?? item.update_time)}`);

        const articles = item.content?.news_item ?? [];
        if (!articles.length) {
            lines.push("未返回文章内容");
            continue;
        }

        lines.push(`文章数: ${articles.length}`);
        lines.push(`首篇标题: ${articles[0]?.title ?? "(无标题)"}`);
        if (articles[0]?.author) {
            lines.push(`作者: ${articles[0].author}`);
        }
    }

    return lines.join("\n");
}

export function formatPublishStatus(status: PublishStatusResponse) {
    const lines = [
        `发布任务: ${status.publish_id}`,
        `状态: ${getPublishStatusText(status.publish_status)} (${status.publish_status})`,
    ];

    if (status.article_id) {
        lines.push(`文章 ID: ${status.article_id}`);
    }

    const articleItems = status.article_detail?.item ?? [];
    for (const item of articleItems) {
        lines.push(`文章链接 #${item.idx}: ${item.article_url}`);
    }

    if (status.fail_idx?.length) {
        lines.push(`失败文章序号: ${status.fail_idx.join(", ")}`);
    }

    return lines.join("\n");
}

export function formatPublishedArticle(result: PublishedArticleGetResponse, articleId?: string) {
    const articles = result.news_item ?? [];
    const lines = [`已发布文章 ID: ${articleId ?? "(未知)"}`, `文章数: ${articles.length}`];

    if (!articles.length) {
        lines.push("暂无文章内容");
        return lines.join("\n");
    }

    for (const [index, article] of articles.entries()) {
        lines.push("");
        lines.push(summarizeArticle(article, index));
    }

    return lines.join("\n");
}

export function formatPublishedList(result: PublishedBatchGetResponse, offset = 0) {
    const lines = [`已发布总数: ${result.total_count}`, `本次返回: ${result.item_count}`];

    if (!result.item.length) {
        lines.push("暂无已发布文章");
        return lines.join("\n");
    }

    for (const [index, item] of result.item.entries()) {
        const label = `#${offset + index + 1} ${item.article_id}`;
        lines.push("");
        lines.push(label);
        lines.push(`更新时间: ${formatTimestamp(item.content?.update_time ?? item.update_time)}`);

        const articles = item.content?.news_item ?? [];
        if (!articles.length) {
            lines.push("未返回文章内容");
            continue;
        }

        lines.push(`文章数: ${articles.length}`);
        lines.push(`首篇标题: ${articles[0]?.title ?? "(无标题)"}`);
        if (articles[0]?.url) {
            lines.push(`文章链接: ${articles[0].url}`);
        }
    }

    return lines.join("\n");
}
