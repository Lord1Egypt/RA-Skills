#!/usr/bin/env node
/**
 * COS 预签名 URL 生成（本地纯计算，无网络请求）。
 *
 * 用于「检索结果预览」场景：批量把 cos://bucket/key 转成带签名的可直接访问地址，
 * 避免逐个调用 sign-url 子进程（N 次进程启动是主要耗时来源）。
 *
 * 规则说明（对齐 cos-js-sdk-v5 getObjectUrl 行为）：
 * - 业务 query（如 ci-process=snapshot&time=1）**参与签名**并列入 q-url-param-list；
 * - headers 不参与签名（q-header-list 为空），使浏览器直接访问不受 header 限制；
 * - 临时密钥的 x-cos-security-token **附加在签名之后、不参与签名计算**。
 */

import crypto from "node:crypto";

function hmacSha1(key, data) {
  return crypto.createHmac("sha1", key).update(data).digest("hex");
}

function sha1(data) {
  return crypto.createHash("sha1").update(data).digest("hex");
}

function camSafeUrlEncode(value) {
  return encodeURIComponent(value)
    .replace(/[!'()*]/g, (char) => `%${char.charCodeAt(0).toString(16).toUpperCase()}`);
}

/** 签名串：key 需 lowercase，value 保留原始大小写（含大写值如 AIImageAnalysis 不可小写化） */
function objectToSignString(obj) {
  return Object.keys(obj)
    .sort()
    .map((key) => `${camSafeUrlEncode(key).toLowerCase()}=${camSafeUrlEncode(String(obj[key]))}`)
    .join("&");
}

/** 实际 URL 上的 query 串，顺序与签名串一致 */
function buildQueryString(obj) {
  return Object.keys(obj)
    .sort()
    .map((key) => `${camSafeUrlEncode(key)}=${camSafeUrlEncode(String(obj[key]))}`)
    .join("&");
}

/** ObjectKey 逐段编码，保留路径分隔符 */
function encodeKey(key) {
  return String(key)
    .replace(/^\/+/, "")
    .split("/")
    .map((seg) => camSafeUrlEncode(seg))
    .join("/");
}

/** 解析 cos://bucket/key → { bucket, key } */
export function parseCosUri(uri) {
  const m = /^cos:\/\/([^/]+)\/(.+)$/.exec(String(uri || "").trim());
  if (!m) return { bucket: "", key: "" };
  return { bucket: m[1], key: m[2] };
}

export function cosBucketHost(bucket, region) {
  return `${bucket}.cos.${region}.myqcloud.com`;
}

/**
 * 生成预签名 URL。
 * @param {object} opts
 * @param {string} opts.secretId
 * @param {string} opts.secretKey
 * @param {string} [opts.token]      临时密钥 token（可选）
 * @param {string} opts.bucket
 * @param {string} opts.region
 * @param {string} opts.key          ObjectKey（不含前导 /）
 * @param {object} [opts.query]      业务参数，如 { "ci-process":"snapshot", time:1 }
 * @param {number} [opts.expires]    有效期秒数，默认 3600
 * @param {string} [opts.method]     默认 GET
 * @returns {string} 完整签名 URL
 */
export function presignUrl({
  secretId,
  secretKey,
  token = "",
  bucket,
  region,
  key,
  query = {},
  expires = 3600,
  method = "GET",
}) {
  if (!secretId || !secretKey) {
    const err = new Error('missing credentials for the current runtime mode');
    err.code = "MissingCredentials";
    throw err;
  }

  const now = Math.floor(Date.now() / 1000) - 60; // 容忍轻微时钟偏差
  const keyTime = `${now};${now + Math.max(60, Number(expires) || 3600)}`;
  const signKey = hmacSha1(secretKey, keyTime);

  const pathname = `/${String(key).replace(/^\/+/, "")}`;
  const signedQuery = objectToSignString(query);

  const formatString = [method.toLowerCase(), pathname, signedQuery, "", ""].join("\n");
  const stringToSign = ["sha1", keyTime, sha1(formatString), ""].join("\n");
  const signature = hmacSha1(signKey, stringToSign);

  const authorization = [
    "q-sign-algorithm=sha1",
    `q-ak=${secretId}`,
    `q-sign-time=${keyTime}`,
    `q-key-time=${keyTime}`,
    "q-header-list=",
    `q-url-param-list=${Object.keys(query).sort().map((k) => camSafeUrlEncode(k).toLowerCase()).join(";")}`,
    `q-signature=${signature}`,
  ].join("&");

  const bizQs = buildQueryString(query);
  const host = cosBucketHost(bucket, region);

  return [
    `https://${host}/${encodeKey(key)}?`,
    bizQs ? `${bizQs}&` : "",
    authorization,
    token ? `&x-cos-security-token=${camSafeUrlEncode(token)}` : "",
  ].join("");
}

/** 视频截帧封面（数据万象 snapshot）：GET /<key>?ci-process=snapshot&time=..&format=jpg&width=.. */
export function presignVideoSnapshot(opts) {
  const { time = 1, width = 240, format = "jpg", ...rest } = opts;
  return presignUrl({
    ...rest,
    query: {
      "ci-process": "snapshot",
      time: String(time),
      format,
      width: String(width),
    },
  });
}

/** 文档首页预览图（数据万象 doc-preview）：GET /<key>?ci-process=doc-preview&page=1&dstType=jpg */
/**
 * 文档预览缩略图（数据万象文档转码同步请求 doc-preview）。
 * 文档：https://cloud.tencent.com/document/product/436/121090
 *
 *   GET /<ObjectKey>?ci-process=doc-preview&page=1&dstType=jpg&ImageParams=imageMogr2/thumbnail/240x
 *
 * 要点（对齐官方文档）：
 * - 该接口**没有 width / height 参数**，输出尺寸只能通过 ImageParams（imageMogr2）或 scale / imageDpi 控制；
 * - 每次请求**只返回一页**；page 默认从 1 开始；
 * - Excel 类用 sheet 指定第几张表，可配合 excelPaperDirection 横向输出；
 * - 对象**无后缀名**时必须显式给 srcType，否则无法识别源格式；
 * - 加密 Office 文档需带 password；
 * - 同步接口 10 秒超时、建议 100 页以内，仅适合做缩略图预览。
 *
 * @param {object} opts
 * @param {number} [opts.page=1]       页码（表格文件表示该 sheet 的第几张图）
 * @param {string} [opts.dstType=jpg]  输出格式 jpg / png
 * @param {number} [opts.width=240]    期望缩略图宽度（等比），转成 ImageParams
 * @param {number} [opts.quality]      图片质量 1~100
 * @param {number} [opts.scale]        缩放比例 10~200
 * @param {string} [opts.srcType]      源文件后缀（无后缀对象必填）
 * @param {number} [opts.sheet]        表格文件：第几张表
 * @param {number} [opts.excelPaperDirection] 表格纸张方向 0 垂直 / 1 水平
 * @param {string} [opts.password]     加密文档密码
 * @param {number} [opts.comment]      0 隐藏批注（默认）/ 1 显示
 * @param {string} [opts.imageParams]  完全自定义 ImageParams（给了则忽略 width）
 */
export function presignDocPreview(opts) {
  const {
    page = 1,
    dstType = "jpg",
    width = 240,
    quality,
    scale,
    srcType,
    sheet,
    excelPaperDirection,
    password,
    comment,
    imageParams,
    ...rest
  } = opts;

  const query = {
    "ci-process": "doc-preview",
    page: String(page),
    dstType,
  };

  // 缩略图尺寸只能靠 imageMogr2（接口本身无 width/height 参数）
  const params = imageParams || (width ? `imageMogr2/thumbnail/${width}x` : "");
  if (params) query.ImageParams = params;

  if (quality != null) query.quality = String(quality);
  if (scale != null) query.scale = String(scale);
  if (srcType) query.srcType = String(srcType);
  if (sheet != null) query.sheet = String(sheet);
  if (excelPaperDirection != null) query.excelPaperDirection = String(excelPaperDirection);
  if (password) query.password = String(password);
  if (comment != null) query.comment = String(comment);

  return presignUrl({ ...rest, query });
}

/** 无后缀名时需显式指定 srcType，这里按扩展名给出 doc-preview 可识别的源类型 */
export function docSrcTypeOf(key) {
  const base = String(key || "").split("?")[0];
  const idx = base.lastIndexOf(".");
  return idx >= 0 ? base.slice(idx + 1).toLowerCase() : "";
}
