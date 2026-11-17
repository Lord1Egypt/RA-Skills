/**
 * TikTok 链接归一。
 * 作品只接受主页或整段 sec_uid。评论只接受 /video/数字id 或纯数字 aweme_id。
 * 采集端用精确字符串匹配任务，这里产出的值会同时用于创建和查询。
 */

const PROFILE_MESSAGE =
  "无法识别博主主页。支持 https://www.tiktok.com/@用户名 、@用户名，或整段 MS4w 开头的 sec_uid。视频链接请交给评论命令。vm、vt、/t/ 短链请先换成标准主页链接";
const VIDEO_MESSAGE =
  "无法识别视频。支持 https://www.tiktok.com/@用户名/video/数字id ，或纯数字 aweme_id。主页和 sec_uid 请交给作品命令。vm、vt、/t/ 短链请先换成标准视频链接或数字 id";
const SHORT_MESSAGE =
  "短链无法在本地解析，采集端也不接受。请换成 https://www.tiktok.com/@用户名 或 /video/数字id";
const PHOTO_MESSAGE =
  "图文 /photo/ 链接当前不支持。请换 /video/数字id ，或把数字 aweme_id 交给评论命令";

const SEC_UID_RE = /^MS4w[A-Za-z0-9_\-=+]{8,}$/;
const BARE_UNIQUE_ID_RE = /^@?[A-Za-z0-9._]{2,24}$/;
const PATH_UNIQUE_ID_RE = /^[A-Za-z0-9._]{1,64}$/;
const AWEME_ID_RE = /^\d{1,64}$/;
const TRAILING_PUNCT = /[\/.,;:!?"'，。！？；：、）】》>]+$/u;

function codePointLength(value) {
  return Array.from(value).length;
}

function invalid(message) {
  const error = new Error(message);
  error.code = "INVALID_URL";
  throw error;
}

function tidy(raw) {
  if (typeof raw !== "string") return "";
  let text = raw.trim();
  text = text.replace(/^[<("'`“”‘’【\[]+/, "");
  text = text.replace(TRAILING_PUNCT, "");
  return text.trim();
}

function maybeDecode(text) {
  if (!text.includes("%")) return text;
  try {
    return decodeURIComponent(text);
  } catch (_) {
    return text;
  }
}

/**
 * @param {string} text
 * @returns {URL|null}
 */
function toUrl(text) {
  let value = text;
  if (!/^https?:\/\//i.test(value)) {
    if (/^(?:www\.|m\.|vm\.|vt\.)?tiktok\.com\//i.test(value)) {
      value = "https://" + value;
    } else {
      return null;
    }
  }
  value = value.replace(/^http:\/\//i, "https://");
  let parsed;
  try {
    parsed = new URL(value);
  } catch (_) {
    return null;
  }
  parsed.protocol = "https:";
  let host = parsed.hostname.toLowerCase();
  if (host === "tiktok.com" || host === "m.tiktok.com") host = "www.tiktok.com";
  parsed.hostname = host;
  return parsed;
}

function isShortHost(host) {
  return host === "vm.tiktok.com" || host === "vt.tiktok.com";
}

function rejectLength(value, label) {
  if (codePointLength(value) > 255) {
    invalid(`${label}长度不能超过 255 个字符`);
  }
}

/**
 * 用搜索或评论结果里的 unique_id 补主页。不像入参那样要求至少 2 位。
 * @param {string} uniqueId
 * @returns {string}
 */
function profileUrl(uniqueId) {
  if (typeof uniqueId !== "string" || !PATH_UNIQUE_ID_RE.test(uniqueId)) return "";
  if (!hasLetterOrDigit(uniqueId)) return "";
  return "https://www.tiktok.com/@" + uniqueId;
}

function hasLetterOrDigit(value) {
  return /[A-Za-z0-9]/.test(value);
}

function canonicalProfile(uniqueId) {
  return "https://www.tiktok.com/@" + uniqueId;
}

function canonicalVideo(uniqueId, awemeId) {
  return `https://www.tiktok.com/@${uniqueId}/video/${awemeId}`;
}

/**
 * @param {string} raw
 * @returns {string}
 */
function resolveProfileUrl(raw) {
  const text = maybeDecode(tidy(raw));
  if (!text || /\s/.test(text)) invalid(PROFILE_MESSAGE);
  if (AWEME_ID_RE.test(text)) {
    invalid("纯数字是作品 aweme_id，请交给评论命令。博主请用主页链接、@用户名或 MS4w 开头的 sec_uid");
  }
  if (text.startsWith("MS4w")) {
    if (!SEC_UID_RE.test(text)) {
      invalid("sec_uid 必须是整段、以 MS4w 开头，后面只含字母、数字、下划线、连字符或等号");
    }
    rejectLength(text, "sec_uid");
    return text;
  }

  const bareUniqueId = text.replace(/^@/, "");
  if (
    BARE_UNIQUE_ID_RE.test(text) &&
    hasLetterOrDigit(bareUniqueId) &&
    !/tiktok\.com/i.test(text)
  ) {
    const url = canonicalProfile(bareUniqueId);
    rejectLength(url, "博主主页链接");
    return url;
  }

  const parsed = toUrl(text);
  if (!parsed) invalid(PROFILE_MESSAGE);
  if (isShortHost(parsed.hostname) || /^\/t\//i.test(parsed.pathname)) {
    invalid(SHORT_MESSAGE);
  }
  if (parsed.hostname !== "www.tiktok.com") {
    invalid("这不是 TikTok 主页链接。" + PROFILE_MESSAGE);
  }
  if (/\/photo\//i.test(parsed.pathname)) invalid(PHOTO_MESSAGE);
  if (/\/video\//i.test(parsed.pathname)) {
    invalid("这是视频链接，请交给评论命令");
  }

  const matched = parsed.pathname.match(/^\/@([^/]+)\/?$/);
  if (!matched || !PATH_UNIQUE_ID_RE.test(matched[1]) || !hasLetterOrDigit(matched[1])) {
    invalid(PROFILE_MESSAGE);
  }
  const url = canonicalProfile(matched[1]);
  rejectLength(url, "博主主页链接");
  return url;
}

/**
 * @param {string} raw
 * @returns {string}
 */
function resolveVideoUrl(raw) {
  const text = maybeDecode(tidy(raw));
  if (!text || /\s/.test(text)) invalid(VIDEO_MESSAGE);
  if (text.startsWith("MS4w")) {
    invalid("这是博主 sec_uid，请交给作品命令");
  }
  if (AWEME_ID_RE.test(text)) {
    rejectLength(text, "作品 id");
    return text;
  }
  if (BARE_UNIQUE_ID_RE.test(text) && !/tiktok\.com/i.test(text)) {
    invalid("这是用户名或主页，请交给作品命令");
  }

  const parsed = toUrl(text);
  if (!parsed) invalid(VIDEO_MESSAGE);
  if (isShortHost(parsed.hostname) || /^\/t\//i.test(parsed.pathname)) {
    invalid(SHORT_MESSAGE);
  }
  if (parsed.hostname !== "www.tiktok.com") {
    invalid("这不是 TikTok 视频链接。" + VIDEO_MESSAGE);
  }
  if (/\/photo\//i.test(parsed.pathname)) invalid(PHOTO_MESSAGE);

  const matched = parsed.pathname.match(/^\/@([^/]+)\/video\/([^/]+)\/?$/i);
  if (!matched) {
    if (/^\/@[^/]+\/?$/.test(parsed.pathname)) {
      invalid("这是博主主页，请交给作品命令");
    }
    invalid(VIDEO_MESSAGE);
  }
  const uniqueId = matched[1];
  const awemeId = matched[2];
  if (!AWEME_ID_RE.test(awemeId)) {
    invalid("视频 id 必须是数字。请换 /video/数字id ，或只传数字 aweme_id");
  }
  if (PATH_UNIQUE_ID_RE.test(uniqueId) && hasLetterOrDigit(uniqueId)) {
    const url = canonicalVideo(uniqueId, awemeId);
    rejectLength(url, "视频链接");
    return url;
  }
  return awemeId;
}

function url2Name(url) {
  if (typeof url !== "string" || url === "") return "unknown";
  const name = url
    .replace(/^https?:\/\//, "")
    .replace("www.tiktok.com/@", "user_")
    .replace("/video/", "_video_")
    .replace(/[\/?=&@.]+/g, "_");
  return name || "unknown";
}

module.exports = {
  resolveProfileUrl,
  resolveVideoUrl,
  profileUrl,
  url2Name,
};
