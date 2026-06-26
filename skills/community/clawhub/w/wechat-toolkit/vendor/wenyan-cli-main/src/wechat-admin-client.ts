import type {
    DraftBatchGetResponse,
    DraftCountResponse,
    DraftDeleteResponse,
    DraftGetResponse,
    DraftPublishResponse,
    PublishStatusResponse,
    PublishedArticleGetResponse,
    PublishedBatchGetResponse,
    PublishedDeleteResponse,
} from "./wechat-admin.js";

const DEFAULT_SERVER_URL = "http://localhost:3000";

export interface RemoteWechatOptions {
    server?: string;
    apiKey?: string;
    clientVersion?: string;
}

export interface RemoteWechatListOptions extends RemoteWechatOptions {
    offset?: number;
    count?: number;
    noContent?: boolean;
}

interface ServerErrorPayload {
    code?: number;
    desc?: string;
}

function resolveServerUrl(options: RemoteWechatOptions = {}): string {
    return (options.server || DEFAULT_SERVER_URL).replace(/\/$/, "");
}

function buildHeaders(options: RemoteWechatOptions = {}): Record<string, string> {
    const headers: Record<string, string> = {
        "Content-Type": "application/json",
    };

    if (options.apiKey) {
        headers["x-api-key"] = options.apiKey;
    }

    if (options.clientVersion) {
        headers["x-client-version"] = options.clientVersion;
    }

    return headers;
}

async function postServerJson<T>(
    endpoint: string,
    body: Record<string, unknown>,
    action: string,
    options: RemoteWechatOptions = {},
): Promise<T> {
    const response = await fetch(`${resolveServerUrl(options)}${endpoint}`, {
        method: "POST",
        headers: buildHeaders(options),
        body: JSON.stringify(body),
    });

    let payload: (T & ServerErrorPayload) | null = null;
    try {
        payload = (await response.json()) as T & ServerErrorPayload;
    } catch {
        payload = null;
    }

    if (!response.ok || payload?.code === -1) {
        throw new Error(`${action}失败: ${payload?.desc ?? response.statusText}`);
    }

    if (!payload) {
        throw new Error(`${action}失败: server returned an empty response`);
    }

    return payload;
}

function buildListPayload(options: RemoteWechatListOptions = {}) {
    return {
        offset: options.offset ?? 0,
        count: options.count ?? 20,
        noContent: options.noContent ?? false,
    };
}

export async function getWechatDraftViaServer(
    mediaId: string,
    options: RemoteWechatOptions = {},
): Promise<DraftGetResponse> {
    return await postServerJson<DraftGetResponse>("/draft/get", { mediaId }, "获取草稿", options);
}

export async function listWechatDraftsViaServer(
    options: RemoteWechatListOptions = {},
): Promise<DraftBatchGetResponse> {
    return await postServerJson<DraftBatchGetResponse>(
        "/draft/list",
        buildListPayload(options),
        "获取草稿列表",
        options,
    );
}

export async function countWechatDraftsViaServer(
    options: RemoteWechatOptions = {},
): Promise<DraftCountResponse> {
    return await postServerJson<DraftCountResponse>("/draft/count", {}, "获取草稿总数", options);
}

export async function deleteWechatDraftViaServer(
    mediaId: string,
    options: RemoteWechatOptions = {},
): Promise<DraftDeleteResponse> {
    return await postServerJson<DraftDeleteResponse>("/draft/delete", { mediaId }, "删除草稿", options);
}

export async function submitWechatDraftPublishViaServer(
    mediaId: string,
    options: RemoteWechatOptions = {},
): Promise<DraftPublishResponse> {
    return await postServerJson<DraftPublishResponse>("/draft/publish", { mediaId }, "提交正式发布", options);
}

export async function getWechatPublishStatusViaServer(
    publishId: string,
    options: RemoteWechatOptions = {},
): Promise<PublishStatusResponse> {
    return await postServerJson<PublishStatusResponse>("/publish/status", { publishId }, "查询发布状态", options);
}

export async function listWechatPublishedArticlesViaServer(
    options: RemoteWechatListOptions = {},
): Promise<PublishedBatchGetResponse> {
    return await postServerJson<PublishedBatchGetResponse>(
        "/published/list",
        buildListPayload(options),
        "获取已发布文章列表",
        options,
    );
}

export async function getWechatPublishedArticleViaServer(
    articleId: string,
    options: RemoteWechatOptions = {},
): Promise<PublishedArticleGetResponse> {
    return await postServerJson<PublishedArticleGetResponse>(
        "/published/get",
        { articleId },
        "获取已发布文章",
        options,
    );
}

export async function deleteWechatPublishedArticleViaServer(
    articleId: string,
    index = 0,
    options: RemoteWechatOptions = {},
): Promise<PublishedDeleteResponse> {
    return await postServerJson<PublishedDeleteResponse>(
        "/published/delete",
        { articleId, index },
        "删除已发布文章",
        options,
    );
}
