/**
 * XHS API Client
 *
 * Handles all HTTP requests to edith.xiaohongshu.com and creator.xiaohongshu.com
 * with proper signing, headers, and error handling.
 */

import { signMainApi, USER_AGENT, buildGetUri, extractUri } from "./signing.js";
import { signCreator } from "./creator-signing.js";
import { cookiesToString, type XhsCookies } from "./cookies.js";

const EDITH_HOST = "https://edith.xiaohongshu.com";
const CREATOR_HOST = "https://creator.xiaohongshu.com";
const HOME_URL = "https://www.xiaohongshu.com";
const UPLOAD_HOST = "https://ros-upload.xiaohongshu.com";

export class XhsApiError extends Error {
  constructor(
    message: string,
    public code?: number | string,
    public response?: unknown
  ) {
    super(message);
    this.name = "XhsApiError";
  }
}

export class NeedVerifyError extends XhsApiError {
  constructor(
    public verifyType: string,
    public verifyUuid: string
  ) {
    super(`Captcha required: type=${verifyType}, uuid=${verifyUuid}`);
    this.name = "NeedVerifyError";
  }
}

export class XhsClient {
  private cookies: XhsCookies;

  constructor(cookies: XhsCookies) {
    this.cookies = cookies;
  }

  private baseHeaders(): Record<string, string> {
    return {
      "user-agent": USER_AGENT,
      "content-type": "application/json",
      cookie: cookiesToString(this.cookies),
      origin: HOME_URL,
      referer: `${HOME_URL}/`,
    };
  }

  private async mainApiGet(
    uri: string,
    params?: Record<string, string | number | string[]>
  ): Promise<unknown> {
    const signHeaders = signMainApi("GET", uri, this.cookies, params);
    const fullUri = buildGetUri(uri, params);
    const url = `${EDITH_HOST}${fullUri}`;

    const res = await fetch(url, {
      method: "GET",
      headers: { ...this.baseHeaders(), ...signHeaders },
    });

    return this.handleResponse(res);
  }

  private async mainApiPost(
    uri: string,
    data: Record<string, unknown>
  ): Promise<unknown> {
    const signHeaders = signMainApi("POST", uri, this.cookies, undefined, data);
    const url = `${EDITH_HOST}${uri}`;

    const res = await fetch(url, {
      method: "POST",
      headers: { ...this.baseHeaders(), ...signHeaders },
      body: JSON.stringify(data),
    });

    return this.handleResponse(res);
  }

  // /web_api/ endpoints → edith host; /api/galaxy/ → creator host
  private creatorHost(uri: string): string {
    return uri.startsWith("/api/galaxy/") ? CREATOR_HOST : EDITH_HOST;
  }

  private async creatorGet(
    uri: string,
    params?: Record<string, string | number>
  ): Promise<unknown> {
    let apiStr = `url=${uri}`;
    if (params) {
      const qs = Object.entries(params)
        .map(([k, v]) => `${k}=${v}`)
        .join("&");
      apiStr = `url=${uri}?${qs}`;
    }

    const sign = signCreator(apiStr, null, this.cookies.a1);
    const fullUri = params
      ? `${uri}?${Object.entries(params).map(([k, v]) => `${k}=${v}`).join("&")}`
      : uri;

    const host = this.creatorHost(uri);
    const res = await fetch(`${host}${fullUri}`, {
      method: "GET",
      headers: {
        ...this.baseHeaders(),
        "x-s": sign["x-s"],
        "x-t": sign["x-t"],
        origin: CREATOR_HOST,
        referer: `${CREATOR_HOST}/`,
      },
    });

    return this.handleResponse(res);
  }

  private async creatorPost(
    uri: string,
    data: Record<string, unknown>
  ): Promise<unknown> {
    const sign = signCreator(`url=${uri}`, data, this.cookies.a1);

    const host = this.creatorHost(uri);
    const res = await fetch(`${host}${uri}`, {
      method: "POST",
      headers: {
        ...this.baseHeaders(),
        "x-s": sign["x-s"],
        "x-t": sign["x-t"],
        origin: CREATOR_HOST,
        referer: `${CREATOR_HOST}/`,
      },
      body: JSON.stringify(data),
    });

    return this.handleResponse(res);
  }

  private async handleResponse(res: Response): Promise<unknown> {
    if (res.status === 461 || res.status === 471) {
      throw new NeedVerifyError(
        res.headers.get("verifytype") ?? "unknown",
        res.headers.get("verifyuuid") ?? "unknown"
      );
    }

    const text = await res.text();
    if (!text) return null;

    let data: Record<string, unknown>;
    try {
      data = JSON.parse(text);
    } catch {
      throw new XhsApiError(`Non-JSON response: ${text.substring(0, 200)}`);
    }

    if (data.success) {
      return data.data ?? data.success;
    }

    const code = data.code as string | number | undefined;
    if (code === 300012) {
      throw new XhsApiError("IP blocked by XHS", code, data);
    }
    if (code === 300015) {
      throw new XhsApiError("Signature verification failed", code, data);
    }
    if (code === -100) {
      throw new XhsApiError("Session expired — please re-login", code, data);
    }
    if (code === -101) {
      const hint = process.platform === "win32"
        ? ' Use --cookie-string "a1=VALUE; web_session=VALUE" (from Chrome DevTools > Application > Cookies).'
        : " Try logging out and back in on xiaohongshu.com.";
      throw new XhsApiError(
        `Missing or incomplete login cookies — the 'web_session' cookie may not have been extracted.${hint}`,
        code,
        data
      );
    }

    throw new XhsApiError(
      `API error: ${JSON.stringify(data).substring(0, 300)}`,
      code,
      data
    );
  }

  // ─── Reading Endpoints ──────────────────────────────────────────────────

  async getSelfInfo(): Promise<unknown> {
    return this.mainApiGet("/api/sns/web/v2/user/me");
  }

  async getUserInfo(userId: string): Promise<unknown> {
    return this.mainApiGet("/api/sns/web/v1/user/otherinfo", {
      target_user_id: userId,
    });
  }

  async getUserNotes(
    userId: string,
    cursor: string = ""
  ): Promise<unknown> {
    return this.mainApiGet("/api/sns/web/v1/user_posted", {
      num: 30,
      cursor,
      user_id: userId,
      image_scenes: "FD_WM_WEBP",
    });
  }

  async searchNotes(
    keyword: string,
    page: number = 1,
    pageSize: number = 20,
    sort: "general" | "popularity_descending" | "time_descending" = "general",
    noteType: 0 | 1 | 2 = 0
  ): Promise<unknown> {
    const searchId = generateSearchId();
    return this.mainApiPost("/api/sns/web/v1/search/notes", {
      keyword,
      page,
      page_size: pageSize,
      search_id: searchId,
      sort,
      note_type: noteType,
    });
  }

  async getNoteById(
    noteId: string,
    xsecToken: string,
    xsecSource: string = "pc_feed"
  ): Promise<unknown> {
    return this.mainApiPost("/api/sns/web/v1/feed", {
      source_note_id: noteId,
      image_formats: ["jpg", "webp", "avif"],
      extra: { need_body_topic: 1 },
      xsec_source: xsecSource,
      xsec_token: xsecToken,
    });
  }

  async getHomeFeed(
    category: string = "homefeed_recommend"
  ): Promise<unknown> {
    return this.mainApiPost("/api/sns/web/v1/homefeed", {
      cursor_score: "",
      num: 40,
      refresh_type: 1,
      note_index: 0,
      unread_begin_note_id: "",
      unread_end_note_id: "",
      unread_note_count: 0,
      category,
      search_key: "",
      need_num: 40,
      image_scenes: ["FD_PRV_WEBP", "FD_WM_WEBP"],
    });
  }

  async getComments(
    noteId: string,
    cursor: string = "",
    xsecToken: string = ""
  ): Promise<unknown> {
    return this.mainApiGet("/api/sns/web/v2/comment/page", {
      note_id: noteId,
      cursor,
      image_formats: "jpg,webp,avif",
      xsec_token: xsecToken,
    });
  }

  // ─── Favorites / Collect Endpoints ────────────────────────────────────

  async getUserCollectedNotes(
    userId: string,
    num: number = 30,
    cursor: string = ""
  ): Promise<unknown> {
    return this.mainApiGet("/api/sns/web/v2/note/collect/page", {
      user_id: userId,
      num,
      cursor,
    });
  }

  async collectNote(noteId: string): Promise<unknown> {
    return this.mainApiPost("/api/sns/web/v1/note/collect", {
      note_id: noteId,
    });
  }

  async uncollectNote(noteId: string): Promise<unknown> {
    return this.mainApiPost("/api/sns/web/v1/note/uncollect", {
      note_ids: noteId,
    });
  }

  async getSubComments(
    noteId: string,
    rootCommentId: string,
    num: number = 30,
    cursor: string = ""
  ): Promise<unknown> {
    return this.mainApiGet("/api/sns/web/v2/comment/sub/page", {
      note_id: noteId,
      root_comment_id: rootCommentId,
      num,
      cursor,
    });
  }

  async postComment(
    noteId: string,
    content: string
  ): Promise<unknown> {
    return this.mainApiPost("/api/sns/web/v1/comment/post", {
      note_id: noteId,
      content,
      at_users: [],
    });
  }

  async replyComment(
    noteId: string,
    targetCommentId: string,
    content: string
  ): Promise<unknown> {
    return this.mainApiPost("/api/sns/web/v1/comment/post", {
      note_id: noteId,
      content,
      target_comment_id: targetCommentId,
      at_users: [],
    });
  }

  // ─── HTML Fallback ────────────────────────────────────────────────────

  async getNoteFromHtml(
    noteId: string,
    xsecToken: string
  ): Promise<unknown> {
    const url = `${HOME_URL}/explore/${noteId}?xsec_token=${xsecToken}&xsec_source=pc_feed`;
    const res = await fetch(url, {
      headers: {
        "user-agent": USER_AGENT,
        referer: `${HOME_URL}/`,
        cookie: cookiesToString(this.cookies),
      },
    });

    const html = await res.text();
    const match = html.match(
      /window\.__INITIAL_STATE__=({.*})<\/script>/
    );
    if (!match) {
      throw new XhsApiError("Could not parse __INITIAL_STATE__ from HTML");
    }

    // Replace bare `undefined` values (not inside strings) with ""
    const stateStr = match[1].replace(/:\s*undefined/g, ':""').replace(/,\s*undefined/g, ',""');
    const state = JSON.parse(stateStr);

    const detailMap = state.note?.noteDetailMap;
    if (detailMap) {
      // Try exact noteId first, then fall back to first entry
      const entry = detailMap[noteId] ?? Object.values(detailMap)[0];
      if (entry && (entry as Record<string, unknown>).note) {
        return (entry as Record<string, unknown>).note;
      }
    }

    throw new XhsApiError("Note not found in HTML state");
  }

  // ─── Creator/Posting Endpoints ────────────────────────────────────────

  async getUploadPermit(
    fileType: "image" | "video",
    count: number = 1
  ): Promise<{ fileId: string; token: string }> {
    const data = (await this.creatorGet("/api/media/v1/upload/web/permit", {
      biz_name: "spectrum",
      scene: fileType,
      file_count: count,
      version: 1,
      source: "web",
    })) as { uploadTempPermits: Array<{ fileIds: string[]; token: string }> };

    const permit = data.uploadTempPermits[0];
    return { fileId: permit.fileIds[0], token: permit.token };
  }

  async uploadFile(
    fileId: string,
    token: string,
    filePath: string,
    contentType: string = "image/jpeg"
  ): Promise<void> {
    const fs = await import("node:fs");
    const fileData = fs.readFileSync(filePath);
    const url = `${UPLOAD_HOST}/${fileId}`;

    const res = await fetch(url, {
      method: "PUT",
      headers: {
        "X-Cos-Security-Token": token,
        "Content-Type": contentType,
      },
      body: fileData,
    });

    if (!res.ok) {
      throw new XhsApiError(`Upload failed: ${res.status} ${res.statusText}`);
    }
  }

  async createImageNote(
    title: string,
    desc: string,
    imageFileIds: string[],
    options: {
      topics?: Array<{ id: string; name: string; type: string }>;
      ats?: Array<{ userId: string; nickname: string }>;
      postTime?: string;
      isPrivate?: boolean;
    } = {}
  ): Promise<unknown> {
    const images = imageFileIds.map((fileId) => ({
      file_id: fileId,
      metadata: { source: -1 },
    }));

    const businessBinds = {
      version: 1,
      noteId: 0,
      noteOrderBind: {},
      notePostTiming: { postTime: options.postTime ? new Date(options.postTime).getTime() : null },
      noteCollectionBind: { id: "" },
    };

    const data = {
      common: {
        type: "normal",
        title,
        note_id: "",
        desc,
        source: '{"type":"web","ids":"","extraInfo":"{\\"subType\\":\\"official\\"}"}',
        business_binds: JSON.stringify(businessBinds),
        ats: options.ats ?? [],
        hash_tag: options.topics ?? [],
        post_loc: {},
        privacy_info: { op_type: 1, type: options.isPrivate ? 1 : 0 },
      },
      image_info: { images },
      video_info: null,
    };

    return this.creatorPost("/web_api/sns/v2/note", data);
  }

  async searchTopics(keyword: string): Promise<unknown> {
    return this.creatorPost("/web_api/sns/v1/search/topic", {
      keyword,
      suggest_topic_request: { title: "", desc: "" },
      page: { page_size: 20, page: 1 },
    });
  }

  async searchUsers(keyword: string): Promise<unknown> {
    return this.creatorPost("/web_api/sns/v1/search/user_info", {
      keyword,
      search_id: String(Date.now()),
      page: { page_size: 20, page: 1 },
    });
  }

  async getCreatorNoteList(
    tab: number = 0,
    page: number = 0
  ): Promise<unknown> {
    return this.creatorGet("/api/galaxy/creator/note/user/posted", {
      tab,
      page,
    });
  }
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function generateSearchId(): string {
  const e = BigInt(Date.now()) << 64n;
  const t = BigInt(Math.floor(Math.random() * 2147483646));
  return base36Encode(e + t);
}

function base36Encode(num: bigint): string {
  const alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  if (num === 0n) return "0";
  let result = "";
  let n = num;
  while (n > 0n) {
    result = alphabet[Number(n % 36n)] + result;
    n = n / 36n;
  }
  return result;
}
