#!/usr/bin/env node
/**
 * 数据万象（CI）数据集只读工具 CLI（统一 Skill runtime）
 *
 * Usage:
 *   node scripts/ci_api.mjs <command> [options]
 *
 * Commands:
 *   simple-query      POST /datasetquery/simple           元数据条件筛选/排序/聚合（简单检索）
 *   image-search      POST /datasetquery/imagesearch      文搜图 / 图搜图（Templates=ImageSearch）
 *   doc-search        POST /datasetquery/hybridsearch     以文搜文档（Templates=DocSearch, Mode=text）
 *   video-search      POST /datasetquery/hybridsearch     以文搜视频片段（Templates=VideoSearch，仅 text）
 *   face-search       POST /datasetquery/mediafacesearch  人脸粗搜（外部图 → FaceId + UriList）
 *   face-clip-search  POST /datasetquery/mediafaceclipsearch 人脸精搜（FaceId+媒资 → 时间片段/坐标）
 *   get-ai-media-info POST /datasetquery/getaimediainfo   按 URI 拉单文件 AI 详情（标签/ASR/OCR/粗分类/整体描述，视频含片段级信息）
 *   image-analysis    GET  /<ObjectKey>?ci-process=AIImageAnalysis  图片理解（大模型图片打标/自定义 prompt 分析）
 *   image-exif        GET  /<ObjectKey>?exif                获取图片 EXIF 信息（拍摄参数/时间/相机型号等）
 *   list-datasets     GET  /datasets                      列出账号下数据集
 *   list-bindings     GET  /datasetbindings                查询数据集与 COS Bucket 的绑定关系列表
 *   find-datasets-by-bucket  (组合)                        通过存储桶找到关联的数据集（传桶找数据集用此命令，勿逐个找）
 *   ci-service-status (组合)                               查询 CI 总开关及数据处理子服务开通状态
 *   help
 *
 * 说明：
 *   - 复用 lib/ci_client.mjs 的 cosRequest（COS XML 签名），数据集接口挂在桶的 CI 域名下。
 *   - 仅有 R1 只读能力，无创建/修改/删除。
 *   - 各检索接口的请求体字段映射见 references/dataset-search.md；简单检索见 references/dataset-simple-query.md。
 */

import {
  bucketHost,
  ciAccountHost,
  ciHost,
  cosRequest,
  getRuntimeCredentials,
  parseCiRawError,
  runtimeMeta,
} from "./lib/ci_client.mjs";
import { queryCiServiceStatus } from './lib/ci_service_status.mjs';
import { evaluateBillingNotice } from './lib/billing_notice.mjs';

function parseArgs(argv) {
  const positional = [];
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (item.startsWith("--")) {
      const key = item.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        flags[key] = true;
      } else {
        flags[key] = next;
        i += 1;
      }
    } else {
      positional.push(item);
    }
  }
  return { command: positional[0] || "help", flags, positional };
}

function requireFlag(flags, name, hint) {
  const value = flags[name];
  if (!value || value === true) {
    const err = new Error(`missing --${name}${hint ? `; ${hint}` : ""}`);
    err.code = "InvalidArgs";
    throw err;
  }
  return String(value);
}

function print(result) {
  console.log(JSON.stringify(result, null, 2));
}

function fail(error, extra = {}) {
  const payload = {
    ok: false,
    error: {
      code: error && error.code ? error.code : "ScriptError",
      message: error && error.message ? error.message : String(error),
    },
    runtime: runtimeMeta(),
    ...extra,
  };
  print(payload);
  process.exitCode = 1;
}

function summarizeRequest(raw) {
  return {
    method: raw.method,
    host: raw.host,
    pathname: raw.pathname,
    query: raw.query,
    status: raw.status,
    requestId: raw.requestId,
    traceId: raw.traceId,
    elapsedMs: raw.elapsedMs,
    bodySnippet: raw.ok ? undefined : raw.bodySnippet,
  };
}

/** 把成功响应体解析为 JSON；失败则返回统一错误结构。 */
function parseJsonResponse(raw) {
  try {
    return { data: JSON.parse(raw.body) };
  } catch (e) {
    return {
      error: {
        code: "ResponseParseError",
        message: `body is not JSON: ${e.message}`,
      },
    };
  }
}

/** 把字符串解析为 JSON；非法 JSON 抛带 code 的错误。 */
function parseJsonStrict(str, errCode) {
  try {
    return JSON.parse(String(str));
  } catch (e) {
    const err = new Error(`--body is not valid JSON: ${e.message}`);
    err.code = errCode;
    throw err;
  }
}

/** 解析 --body 完整请求体覆盖（可选）；非法 JSON 抛错。 */
function parseBodyOverride(flags) {
  if (!flags.body || flags.body === true) return null;
  return parseJsonStrict(flags.body, "InvalidBody");
}

/** 解析某个 flag 为 JSON（如 --filter）；未传返回 undefined。 */
function parseJsonFlag(flags, name) {
  const v = flags[name];
  if (!v || v === true) return undefined;
  try {
    return JSON.parse(String(v));
  } catch (e) {
    const err = new Error(`--${name} is not valid JSON: ${e.message}`);
    err.code = "InvalidArgs";
    throw err;
  }
}

/** 把可选数值 flag 写入 body（键名大驼峰）。 */
function assignNumberFlag(body, flags, flagName, bodyKey) {
  const value = flags[flagName];
  if (value === undefined) return;
  if (value === true) {
    const error = new Error(`--${flagName} requires a numeric value`);
    error.code = 'InvalidArgs';
    throw error;
  }
  const number = Number(value);
  if (!Number.isFinite(number)) {
    const error = new Error(`--${flagName} must be a finite number`);
    error.code = 'InvalidArgs';
    throw error;
  }
  body[bodyKey] = number;
}

/**
 * 通用：GET 账号级 CI 域名 <AppId>.ci.<Region>.myqcloud.com 下的端点，统一错误解析与 JSON 反序列化。
 * 注意：数据集是 region 级的，region 需与目标数据集所属地域一致。
 * @returns {Promise<{ok:boolean,data?:object,error?:object,request:object}>}
 */
async function ciAccountGet({ appId, region, pathname, query, creds }) {
  const host = ciAccountHost(appId, region);
  const raw = await cosRequest({
    method: "GET",
    host,
    pathname,
    query,
    creds,
    extraHeaders: { Accept: "application/json" },
  });

  if (!raw.ok) {
    return { ok: false, error: parseCiRawError(raw), request: summarizeRequest(raw) };
  }

  const parsed = parseJsonResponse(raw);
  if (parsed.error) {
    return { ok: false, error: parsed.error, request: summarizeRequest(raw) };
  }

  return { ok: true, data: parsed.data, request: summarizeRequest(raw) };
}

/**
 * 通用：POST 到桶 CI 域名下的数据集检索端点，统一错误解析与 JSON 反序列化。
 * @returns {Promise<object>} 结构化结果（ok/tool/bucket/region/datasetName/data|error/request）
 */
async function runDatasetPost({ tool, bucket, region, pathname, body, datasetName }) {
  const creds = getRuntimeCredentials();
  const host = ciHost(bucket, region);

  const raw = await cosRequest({
    method: "POST",
    host,
    pathname,
    query: {},
    creds,
    body: JSON.stringify(body),
    extraHeaders: { Accept: "application/json" },
  });

  const base = { tool, bucket, region, datasetName: datasetName || null };

  if (!raw.ok) {
    return {
      ok: false,
      ...base,
      error: parseCiRawError(raw),
      request: summarizeRequest(raw),
    };
  }

  const parsed = parseJsonResponse(raw);
  if (parsed.error) {
    return { ok: false, ...base, error: parsed.error, request: summarizeRequest(raw) };
  }

  return { ok: true, ...base, data: parsed.data, request: summarizeRequest(raw) };
}

/**
 * 简单查询：POST /datasetquery/simple
 * body 为用户/模型按 references/dataset-simple-query.md 生成的 JSON 请求体。
 */
async function simpleQuery(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const bodyRaw = requireFlag(flags, "body", "JSON string, e.g. --body '{\"DatasetName\":\"example-dataset\",\"Query\":{...}}'");
  const parsedBody = parseJsonStrict(bodyRaw, "InvalidBody");

  return runDatasetPost({
    tool: "simple-query",
    bucket,
    region,
    pathname: "/datasetquery/simple",
    body: parsedBody,
    datasetName: parsedBody.DatasetName || null,
  });
}

/**
 * 组装“文/图搜”类请求体（image-search / video-search 共用）。
 * @param {object} flags CLI flags
 * @param {string} templates "ImageSearch" | "VideoSearch"
 * @returns {object} 请求体
 */
function buildSearchBody(flags, templates) {
  const datasetName = requireFlag(flags, "dataset-name", "e.g. --dataset-name my-image-dataset");
  const mode = (flags.mode && flags.mode !== true) ? String(flags.mode) : "text";
  if (mode !== "text" && mode !== "pic") {
    const err = new Error(`--mode 仅支持 text | pic，收到: ${mode}`);
    err.code = "InvalidArgs";
    throw err;
  }

  const body = { DatasetName: datasetName, Mode: mode, Templates: templates };

  if (mode === "text") {
    const text = requireFlag(flags, "text", "text 模式必填 --text '<自然语言>'");
    // 网关不同版本字段名不一（Text / SearchText），同时下发以兼容。
    body.Text = text;
    body.SearchText = text;
  } else {
    const uri = requireFlag(flags, "uri", "pic 模式必填 --uri 'cos://bucket/key'（逗号分隔多个）");
    const uris = String(uri).split(",").map((s) => s.trim()).filter(Boolean);
    // 网关不同版本字段名不一（URI 单数 / URIs / SearchURIs），同时下发以兼容。
    body.URI = uris[0];
    body.URIs = uris;
    body.SearchURIs = uris;
  }

  assignNumberFlag(body, flags, "limit", "Limit");
  assignNumberFlag(body, flags, "match-threshold", "MatchThreshold");

  const filter = parseJsonFlag(flags, "filter");
  if (filter !== undefined) body.Filter = filter;

  return body;
}

/**
 * 图片检索：POST /datasetquery/imagesearch（Templates=ImageSearch）
 * 支持 text（文搜图）/ pic（图搜图）两种模式。
 */
async function imageSearch(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const override = parseBodyOverride(flags);
  const body = override || buildSearchBody(flags, "ImageSearch");
  return runDatasetPost({
    tool: "image-search",
    bucket,
    region,
    pathname: "/datasetquery/imagesearch",
    body,
    datasetName: body.DatasetName || null,
  });
}

/**
 * 文档检索：POST /datasetquery/hybridsearch（Templates=DocSearch, Mode=text）
 * 以自然语言检索文档，返回命中片段。
 */
async function docSearch(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const override = parseBodyOverride(flags);

  let body;
  if (override) {
    body = override;
  } else {
    const datasetName = requireFlag(flags, "dataset-name", "e.g. --dataset-name my-doc-dataset");
    const text = requireFlag(flags, "text", "必填 --text '<自然语言>'");
    body = {
      DatasetName: datasetName,
      Mode: "text",
      Templates: "DocSearch",
      Text: text,
      SearchText: text,
    };
    assignNumberFlag(body, flags, "limit", "Limit");
    assignNumberFlag(body, flags, "match-threshold", "MatchThreshold");
    const filter = parseJsonFlag(flags, "filter");
    if (filter !== undefined) body.Filter = filter;
  }

  return runDatasetPost({
    tool: "doc-search",
    bucket,
    region,
    pathname: "/datasetquery/hybridsearch",
    body,
    datasetName: body.DatasetName || null,
  });
}

/**
 * 视频检索：POST /datasetquery/hybridsearch（Templates=VideoSearch）
 * 仅支持 text（以文搜视频片段），不支持图搜（Mode=pic 不适用）。
 */
async function videoSearch(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const override = parseBodyOverride(flags);
  const body = override || buildSearchBody(flags, "VideoSearch");
  // 视频检索仅支持以文搜视频片段，强制 text 模式并清掉图搜字段
  if (!override) {
    body.Mode = 'text';
    delete body.URI;
    delete body.URIs;
    delete body.SearchURIs;
  }
  return runDatasetPost({
    tool: "video-search",
    bucket,
    region,
    pathname: "/datasetquery/hybridsearch",
    body,
    datasetName: body.DatasetName || null,
  });
}

/**
 * 人脸粗搜：POST /datasetquery/mediafacesearch
 * 传入一张外部人脸图（URI），返回库内匹配的 FaceId 与命中媒资 UriList。
 */
async function faceSearch(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const override = parseBodyOverride(flags);

  let body;
  if (override) {
    body = override;
  } else {
    body = {
      DatasetName: requireFlag(flags, "dataset-name", "e.g. --dataset-name my-face-dataset"),
      URI: requireFlag(flags, "uri", "必填 --uri 'cos://bucket/face.jpg'"),
    };
    assignNumberFlag(body, flags, "limit", "Limit");
    assignNumberFlag(body, flags, "match-threshold", "MatchThreshold");
  }

  return runDatasetPost({
    tool: "face-search",
    bucket,
    region,
    pathname: "/datasetquery/mediafacesearch",
    body,
    datasetName: body.DatasetName || null,
  });
}

/**
 * 人脸精搜：POST /datasetquery/mediafaceclipsearch
 * 传入 FaceId + 目标媒资 URI，返回该人脸在媒资中出现的时间片段/坐标。
 */
async function faceClipSearch(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const override = parseBodyOverride(flags);

  let body;
  if (override) {
    body = override;
  } else {
    body = {
      DatasetName: requireFlag(flags, "dataset-name", "e.g. --dataset-name my-face-dataset"),
      URI: requireFlag(flags, "uri", "必填 --uri 'cos://bucket/video.mp4'"),
      FaceId: requireFlag(flags, "face-id", "必填 --face-id '<face-search 返回的 FaceId>'"),
    };
  }

  return runDatasetPost({
    tool: "face-clip-search",
    bucket,
    region,
    pathname: "/datasetquery/mediafaceclipsearch",
    body,
    datasetName: body.DatasetName || null,
  });
}

/**
 * 媒资 AI 信息查询：POST /datasetquery/getaimediainfo
 * 仅适用于已加入智能检索，并在 ImageSearch / VideoSearch 数据集中完成入库的图片或视频。
 * 按 URI 拉取 AI 标签 / ASR / OCR / 粗分类与整体描述（AiRoughData.Description，仅视频）；
 * 视频返回更丰富：AsrInfo/OcrInfo/AiLabelInfo 带 From/To/Timestamp、AsrInfo/OcrInfo 带 ClipId，
 * 可按 ClipId 或时间窗聚合出片段描述（该片段说了什么、画面有什么字、出现什么标签）；图片无时间维度。
 */
async function getAiMediaInfo(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const override = parseBodyOverride(flags);

  let body;
  if (override) {
    body = override;
  } else {
    body = {
      URI: requireFlag(flags, "uri", "必填 --uri 'cos://bucket/album/x.mp4'（目标媒资完整路径）"),
      DatasetName: requireFlag(flags, "dataset-name", "必填 --dataset-name '<该媒资所属数据集>'"),
    };
  }

  return runDatasetPost({
    tool: "get-ai-media-info",
    bucket,
    region,
    pathname: "/datasetquery/getaimediainfo",
    body,
    datasetName: body.DatasetName || null,
  });
}

/** 从 XML 片段取首个 <tag>…</tag> 文本（不含子标签递归）。 */
function xmlTag(xml, tag) {
  if (!xml) return null;
  const m = xml.match(new RegExp(`<${tag}>([\\s\\S]*?)</${tag}>`, "i"));
  return m ? m[1].trim() : null;
}

/** UTF-8 → URL 安全 Base64（+→- /→_），供 Custom 模式 prompt 编码。 */
function urlSafeBase64(str) {
  return Buffer.from(String(str), "utf8").toString("base64").replace(/\+/g, "-").replace(/\//g, "_");
}

/** URL 安全/标准 Base64 → UTF-8 文本（Custom 模式返回值解码）。 */
function decodeBase64Utf8(b64) {
  try {
    const norm = String(b64).replace(/-/g, "+").replace(/_/g, "/");
    return Buffer.from(norm, "base64").toString("utf8");
  } catch {
    return null;
  }
}

/**
 * 解析 <ImageLabelsResult> 片段：整体描述 + 分层标签。
 * 真实结构：ImageLabelsResult 下有 Description + 多个 LabelDetail；
 * 每个 LabelDetail = 1 个 Confidence + 多个 LabelInfos（每个 LabelInfos 直接含 labelName/labelValue）。
 */
function parseImageLabelsBlock(block) {
  const description = xmlTag(block, "Description");
  const labels = [];
  const labelDetails = [];
  const detailBlocks = [...block.matchAll(/<LabelDetail>([\s\S]*?)<\/LabelDetail>/gi)];
  for (const d of detailBlocks) {
    const detail = d[1];
    const confidence = xmlTag(detail, "Confidence");
    const infos = {};
    const pairs = [...detail.matchAll(/<LabelInfos>([\s\S]*?)<\/LabelInfos>/gi)];
    for (const p of pairs) {
      const name = xmlTag(p[1], "labelName");
      const value = xmlTag(p[1], "labelValue");
      if (name != null) {
        infos[name] = value;
        labels.push({ name, value, confidence: confidence || null });
      }
    }
    labelDetails.push({ labelInfos: infos, confidence: confidence || null });
  }
  return { description: description || null, labels, labelDetails };
}

/** 兼容网关以 JSON 返回的情形，尽量对齐 XML 解析结构。 */
function normalizeAnalysisJson(json) {
  const r = json.Response || json;
  const ar = r.AnalysisResult || {};
  const data = { type: ar.Type || null, requestId: r.RequestId || null };
  if (ar.ImageLabelsResult) {
    const ir = ar.ImageLabelsResult;
    data.description = ir.Description || null;
    data.labelDetails = ir.LabelDetail || [];
  }
  const customOut = ar.CustomResult && ar.CustomResult.CustomOutput;
  if (customOut != null) {
    data.custom = { outputBase64: customOut, output: decodeBase64Utf8(customOut) };
  }
  return data;
}

/** 解析图片理解响应体（XML 优先，兼容 JSON）。 */
function parseImageAnalysisResponse(body) {
  const text = String(body || "").trim();
  if (!text) return { error: { code: "EmptyResponse", message: "empty response body" } };
  if (text.startsWith("{")) {
    try {
      return { data: normalizeAnalysisJson(JSON.parse(text)) };
    } catch (e) {
      return { error: { code: "ResponseParseError", message: `body is not JSON: ${e.message}` } };
    }
  }
  const type = xmlTag(text, "Type");
  const requestId = xmlTag(text, "RequestId");
  const data = { type: type || null, requestId: requestId || null };
  const labelsBlock = xmlTag(text, "ImageLabelsResult");
  if (labelsBlock != null) {
    Object.assign(data, parseImageLabelsBlock(labelsBlock));
  }
  const customOut = xmlTag(text, "CustomOutput");
  if (customOut != null) {
    data.custom = { outputBase64: customOut, output: decodeBase64Utf8(customOut) };
  }
  return { data };
}

/**
 * 图片理解（AIImageAnalysis · 大模型图片分析）：
 *   GET /<ObjectKey>?ci-process=AIImageAnalysis&type=ImageLabels&label-scenes=General
 * 挂在桶 COS 域名 <bucket>.cos.<region>.myqcloud.com，同步返回 XML。
 *   - type=ImageLabels：返回图片整体描述 + 分层 AI 标签（label-scenes 指定场景）；
 *   - type=Custom：按 --prompt 自定义提问，输出经 Base64 编码的分析文本（已自动解码到 data.custom.output）。
 * 目标图片三选一：--uri 'cos://bucket/key' | --object '<ObjectKey>' | --detect-url '<公网图片URL>'。
 */
async function imageAnalysis(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");

  const detectUrl = flags["detect-url"] && flags["detect-url"] !== true ? String(flags["detect-url"]) : "";
  let objectKey = "";
  if (flags.object && flags.object !== true) {
    objectKey = String(flags.object).replace(/^\/+/, "");
  } else if (flags.uri && flags.uri !== true) {
    objectKey = parseCosUri(flags.uri).path;
  }
  if (!objectKey && !detectUrl) {
    const err = new Error("必填三选一：--uri 'cos://bucket/key' | --object '<ObjectKey>' | --detect-url '<公网图片URL>'");
    err.code = "InvalidArgs";
    throw err;
  }

  const type = flags.type && flags.type !== true ? String(flags.type) : "ImageLabels";
  if (type !== "ImageLabels" && type !== "Custom") {
    const err = new Error(`--type 仅支持 ImageLabels | Custom，收到: ${type}`);
    err.code = "InvalidArgs";
    throw err;
  }

  const query = { "ci-process": "AIImageAnalysis", type };
  if (type === "ImageLabels") {
    query["label-scenes"] = flags["label-scenes"] && flags["label-scenes"] !== true ? String(flags["label-scenes"]) : "General";
  } else {
    const prompt = requireFlag(flags, "prompt", "Custom 模式必填 --prompt '<user prompt>'（≤1024 字符，自动 URL 安全 Base64）");
    query.prompt = urlSafeBase64(prompt);
  }
  if (flags["ai-model"] && flags["ai-model"] !== true) query["ai-model"] = String(flags["ai-model"]);
  if (detectUrl) query["detect-url"] = detectUrl;

  const creds = getRuntimeCredentials();
  const host = bucketHost(bucket, region);
  const pathname = `/${objectKey}`;

  const raw = await cosRequest({
    method: "GET",
    host,
    pathname,
    query,
    creds,
    extraHeaders: { Accept: "application/xml" },
  });

  const base = {
    tool: "image-analysis",
    bucket,
    region,
    objectKey: objectKey || null,
    analysisType: type,
    ...(detectUrl ? { detectUrl } : {}),
  };
  if (!raw.ok) {
    return { ok: false, ...base, error: parseCiRawError(raw), request: summarizeRequest(raw) };
  }
  const parsed = parseImageAnalysisResponse(raw.body);
  if (parsed.error) {
    return { ok: false, ...base, error: parsed.error, request: summarizeRequest(raw) };
  }
  return { ok: true, ...base, data: parsed.data, request: summarizeRequest(raw) };
}

/**
 * 解析 EXIF 响应体：接口返回 JSON，每个字段形如 {"val":"..."}。
 * - 无 EXIF 信息时返回 {"error":"no exif data"}，此处归一化为 error 结构；
 * - 正常时把 {Field:{val}} 摊平为 exif 便捷 map（Field -> val），同时保留原始 raw。
 */
function parseImageExifResponse(body) {
  const text = String(body || "").trim();
  if (!text) return { error: { code: "EmptyResponse", message: "empty response body" } };
  let json;
  try {
    json = JSON.parse(text);
  } catch (e) {
    return { error: { code: "ResponseParseError", message: `body is not JSON: ${e.message}` } };
  }
  if (json && typeof json.error === "string") {
    return { error: { code: "NoExifData", message: json.error } };
  }
  const exif = {};
  for (const [key, entry] of Object.entries(json || {})) {
    if (entry && typeof entry === "object" && "val" in entry) {
      exif[key] = entry.val;
    } else {
      exif[key] = entry;
    }
  }
  return { data: { exif, raw: json } };
}

/**
 * 获取图片 EXIF 信息（EXIF · 基础图片处理）：
 *   GET /<ObjectKey>?exif
 * 挂在桶 COS 域名 <bucket>.cos.<region>.myqcloud.com，返回 JSON（每字段 {"val":"..."}）。
 * 无 EXIF 信息时接口返回 {"error":"no exif data"}，本工具归一化为 error.code=NoExifData。
 * 目标图片二选一：--uri 'cos://bucket/key' | --object '<ObjectKey>'。
 * 支持格式：JPG/PNG/BMP/WebP/TIFF/AVIF/HEIF。
 */
async function imageExif(flags) {
  const bucket = requireFlag(flags, "bucket", "e.g. --bucket example-1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");

  let objectKey = "";
  if (flags.object && flags.object !== true) {
    objectKey = String(flags.object).replace(/^\/+/, "");
  } else if (flags.uri && flags.uri !== true) {
    objectKey = parseCosUri(flags.uri).path;
  }
  if (!objectKey) {
    const err = new Error("必填二选一：--uri 'cos://bucket/key' | --object '<ObjectKey>'");
    err.code = "InvalidArgs";
    throw err;
  }

  const creds = getRuntimeCredentials();
  const host = bucketHost(bucket, region);
  const pathname = `/${objectKey}`;

  const raw = await cosRequest({
    method: "GET",
    host,
    pathname,
    query: { exif: "" },
    creds,
    extraHeaders: { Accept: "application/json" },
  });

  const base = { tool: "image-exif", bucket, region, objectKey };
  if (!raw.ok) {
    return { ok: false, ...base, error: parseCiRawError(raw), request: summarizeRequest(raw) };
  }
  const parsed = parseImageExifResponse(raw.body);
  if (parsed.error) {
    return { ok: false, ...base, error: parsed.error, request: summarizeRequest(raw) };
  }
  return { ok: true, ...base, data: parsed.data, request: summarizeRequest(raw) };
}

/**
 * 列出数据集：GET /datasets?maxresults=&prefix=&nexttoken=
 * 挂在账号级 CI 域名 <AppId>.ci.<Region>.myqcloud.com，返回 JSON。
 */
async function listDatasets(flags) {
  const appId = requireFlag(flags, "appid", "e.g. --appid 1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");

  const query = {};
  if (flags.maxresults && flags.maxresults !== true) {
    query.maxresults = String(flags.maxresults);
  }
  if (flags.prefix && flags.prefix !== true) {
    query.prefix = String(flags.prefix);
  }
  if (flags.nexttoken && flags.nexttoken !== true) {
    query.nexttoken = String(flags.nexttoken);
  }

  const creds = getRuntimeCredentials();
  const res = await ciAccountGet({ appId, region, pathname: "/datasets", query, creds });
  return {
    ok: res.ok,
    tool: "list-datasets",
    appId,
    region,
    ...(res.ok ? { data: res.data } : { error: res.error }),
    request: res.request,
  };
}

/**
 * 查询绑定关系列表：GET /datasetbindings?datasetname=&maxresults=&nexttoken=
 * 挂在账号级 CI 域名 <AppId>.ci.<Region>.myqcloud.com，返回 JSON。
 * 查询某数据集与 COS Bucket 的绑定关系列表。授权 action: ci:DescribeDatasetBindings。
 */
async function listBindings(flags) {
  const appId = requireFlag(flags, "appid", "e.g. --appid 1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou");
  const datasetName = requireFlag(flags, "dataset-name", "e.g. --dataset-name my-dataset");

  const query = { datasetname: datasetName };
  if (flags.maxresults && flags.maxresults !== true) {
    query.maxresults = String(flags.maxresults);
  }
  if (flags.nexttoken && flags.nexttoken !== true) {
    query.nexttoken = String(flags.nexttoken);
  }

  const creds = getRuntimeCredentials();
  const res = await ciAccountGet({ appId, region, pathname: "/datasetbindings", query, creds });
  return {
    ok: res.ok,
    tool: "list-bindings",
    appId,
    region,
    datasetName,
    ...(res.ok ? { data: res.data } : { error: res.error }),
    request: res.request,
  };
}

/** 解析 cos:// URI 为 { bucket, path }；path 为绑定的前缀/子路径（整桶绑定时为空）。 */
function parseCosUri(uri) {
  const s = String(uri || "").trim();
  const m = s.match(/^cos:\/\/([^/]+)(?:\/(.*))?$/i);
  if (!m) return { bucket: null, path: "" };
  return { bucket: m[1], path: m[2] || "" };
}

/** 翻页拉全账号级列表端点的某个数组字段（datasets/bindings 共用）。 */
async function fetchAllPaged({ appId, region, pathname, baseQuery, arrayKey, creds, pageSize }) {
  const items = [];
  let nextToken = "";
  do {
    const query = { ...baseQuery };
    if (pageSize) query.maxresults = String(pageSize);
    if (nextToken) query.nexttoken = nextToken;
    const res = await ciAccountGet({ appId, region, pathname, query, creds });
    if (!res.ok) return { ok: false, error: res.error, request: res.request, items };
    const data = res.data || {};
    for (const it of data[arrayKey] || []) items.push(it);
    nextToken = data.NextToken || "";
  } while (nextToken);
  return { ok: true, items };
}

/**
 * 通过存储桶找到关联的数据集（传入桶要找数据集时用此命令，不要自己一个个找）：
 *   1) 账号级 GET /datasets 翻页列全所有数据集（跨 region）；
 *   2) 对每个数据集用其自身 Region 调 GET /datasetbindings 拉全绑定关系
 *      （BindCount=0 的数据集默认跳过，可用 --scan-all 强制全扫描）；
 *   3) 过滤 URI 桶名 == --bucket 的绑定，输出关联数据集与关联路径。
 */
async function findDatasetsByBucket(flags) {
  const appId = requireFlag(flags, "appid", "e.g. --appid 1250000000");
  const region = requireFlag(flags, "region", "e.g. --region ap-guangzhou（列数据集入口地域，账号级跨地域）");
  const bucket = requireFlag(flags, "bucket", "要反查的完整桶名，e.g. --bucket example-1250000000");
  const scanAll = flags["scan-all"] === true || flags["scan-all"] === "true";
  const pageSize = (flags.maxresults && flags.maxresults !== true) ? String(flags.maxresults) : undefined;
  const creds = getRuntimeCredentials();

  // Step 1: 列全数据集
  const dsRes = await fetchAllPaged({
    appId,
    region,
    pathname: "/datasets",
    baseQuery: {},
    arrayKey: "Datasets",
    creds,
    pageSize,
  });
  const base = { tool: "find-datasets-by-bucket", appId, region, bucket };
  if (!dsRes.ok) {
    return { ok: false, ...base, error: dsRes.error, request: dsRes.request };
  }
  const datasets = dsRes.items;

  // Step 2 + 3: 逐个数据集按其 Region 查绑定并过滤 bucket
  const matched = [];
  const warnings = [];
  let scanned = 0;
  for (const d of datasets) {
    const datasetName = d.DatasetName;
    if (!datasetName) continue;
    // 优化：BindCount 明确为 0 时无绑定，默认跳过（--scan-all 可强制查）
    if (!scanAll && typeof d.BindCount === "number" && d.BindCount === 0) continue;
    const dsRegion = d.Region || region;
    scanned += 1;

    const bRes = await fetchAllPaged({
      appId,
      region: dsRegion,
      pathname: "/datasetbindings",
      baseQuery: { datasetname: datasetName },
      arrayKey: "Bindings",
      creds,
      pageSize,
    });
    if (!bRes.ok) {
      warnings.push({ datasetName, region: dsRegion, error: bRes.error });
      continue;
    }

    for (const b of bRes.items) {
      const parsed = parseCosUri(b.URI);
      if (parsed.bucket === bucket) {
        matched.push({
          datasetName: b.DatasetName || datasetName,
          region: dsRegion,
          uri: b.URI,
          path: parsed.path,
          state: b.State,
          stockState: b.StockState,
          createTime: b.CreateTime,
          updateTime: b.UpdateTime,
        });
      }
    }
  }

  return {
    ok: true,
    ...base,
    data: {
      matched,
      matchedCount: matched.length,
      totalDatasets: datasets.length,
      scannedDatasets: scanned,
    },
    ...(warnings.length ? { warnings } : {}),
  };
}

async function ciServiceStatus(flags) {
  const bucket = requireFlag(flags, 'bucket', 'e.g. --bucket example-1250000000');
  const region = requireFlag(flags, 'region', 'e.g. --region ap-guangzhou');
  const data = await queryCiServiceStatus({ bucket, region, requiredService: flags['required-service'] });
  return {
    ok: true,
    tool: 'ci-service-status',
    ...data,
  };
}

function helpText() {
  return {
    ok: true,
    tool: "help",
    skill: "tencentcloud-cos",
    description: "CI 数据集只读工具，复用 cosRequest COS XML 签名",
    auth: {
      modeDetection: "KIKI=1 时启用严格模式并隐藏部分功能",
      local: ["TENCENT_COS_SECRET_ID", "TENCENT_COS_SECRET_KEY", "TENCENT_COS_TOKEN"],
      runtime: ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY", "TENCENTCLOUD_TOKEN"],
    },
    commands: [
      {
        name: 'ci-service-status',
        usage: 'node scripts/ci_api.mjs ci-service-status --bucket <bucket-appid> --region <region> [--required-service ci|document|media|voice|file|asyncImage|asyncContentRecognition]',
        note: '--required-service 用于处理任务前置检查：已确认未开通时返回 ci_activation v1 interaction；不传此参数仅查询状态，不触发交互。查询 CI 总开关、文档/媒体/语音/文件处理状态，并通过 GET /picbucket 与 GET /ai_bucket 独立查询异步图片处理和异步内容识别；同步图片处理与同步内容识别在 CI 开启时默认可用。',
      },
      {
        name: "simple-query",
        usage: "node scripts/ci_api.mjs simple-query --bucket <bucket-appid> --region <region> --body '<json>'",
        note: "POST /datasetquery/simple；元数据筛选/排序/聚合。body 生成规则见 references/dataset-simple-query.md。",
      },
      {
        name: "image-search",
        usage: "node scripts/ci_api.mjs image-search --bucket <b> --region <r> --dataset-name <d> --mode text|pic (--text <t> | --uri <cos://..>) [--limit N] [--match-threshold N] [--filter '<json>'] [--body '<json>']",
        note: "POST /datasetquery/imagesearch（Templates=ImageSearch）；文搜图 / 图搜图。",
      },
      {
        name: "doc-search",
        usage: "node scripts/ci_api.mjs doc-search --bucket <b> --region <r> --dataset-name <d> --text <t> [--limit N] [--match-threshold N] [--filter '<json>'] [--body '<json>']",
        note: "POST /datasetquery/hybridsearch（Templates=DocSearch, Mode=text）；以文搜文档。",
      },
      {
        name: "video-search",
        usage: "node scripts/ci_api.mjs video-search --bucket <b> --region <r> --dataset-name <d> --text <t> [--limit N] [--match-threshold N] [--filter '<json>'] [--body '<json>']",
        note: "POST /datasetquery/hybridsearch（Templates=VideoSearch）；仅以文搜视频片段，不支持图搜。",
      },
      {
        name: "face-search",
        usage: "node scripts/ci_api.mjs face-search --bucket <b> --region <r> --dataset-name <d> --uri <cos://face.jpg> [--limit N] [--match-threshold N] [--body '<json>']",
        note: "POST /datasetquery/mediafacesearch；人脸粗搜，外部图 → FaceId + 命中媒资 UriList。",
      },
      {
        name: "face-clip-search",
        usage: "node scripts/ci_api.mjs face-clip-search --bucket <b> --region <r> --dataset-name <d> --uri <cos://video.mp4> --face-id <fid> [--body '<json>']",
        note: "POST /datasetquery/mediafaceclipsearch；人脸精搜，FaceId+媒资 → 出现时间片段/坐标。",
      },
      {
        name: "get-ai-media-info",
        usage: "node scripts/ci_api.mjs get-ai-media-info --bucket <b> --region <r> --dataset-name <d> --uri <cos://file> [--body '<json>']",
        note: "POST /datasetquery/getaimediainfo（GetAIMediaInfo）；仅用于智能检索 ImageSearch / VideoSearch 数据集中已完成入库的图片或视频。返回 AI 标签、ASR、OCR、粗分类与整体描述（AiRoughData.Description，仅视频）；视频可按 From~To / ClipId 聚合出片段描述。",
      },
      {
        name: "image-analysis",
        usage: "node scripts/ci_api.mjs image-analysis --bucket <b> --region <r> (--uri <cos://key> | --object <ObjectKey> | --detect-url <url>) [--type ImageLabels|Custom] [--label-scenes General] [--prompt <p>] [--ai-model <m>]",
        note: "GET /<ObjectKey>?ci-process=AIImageAnalysis；图片理解（无需数据集，直接对桶内单张图片）。ImageLabels 打标返回描述+分层标签；Custom 按 --prompt 自定义提问（返回 Base64 已自动解码）。返回 XML 已解析为 JSON。",
      },
      {
        name: "image-exif",
        usage: "node scripts/ci_api.mjs image-exif --bucket <b> --region <r> (--uri <cos://key> | --object <ObjectKey>)",
        note: "GET /<ObjectKey>?exif；获取图片 EXIF 信息（无需数据集）。返回 JSON（每字段 {val}），已摊平为 data.exif（Field->值）+ 保留 data.raw。无 EXIF 时归一化为 error.code=NoExifData。支持 JPG/PNG/BMP/WebP/TIFF/AVIF/HEIF。",
      },
      {
        name: "list-datasets",
        usage: "node scripts/ci_api.mjs list-datasets --appid <AppId> --region <region> [--maxresults N] [--prefix <prefix>] [--nexttoken <token>]",
        note: "GET /datasets；账号级 CI 域名 <AppId>.ci.<Region>.myqcloud.com，Accept: application/json。",
      },
      {
        name: "list-bindings",
        usage: "node scripts/ci_api.mjs list-bindings --appid <AppId> --region <region> --dataset-name <d> [--maxresults N(0~200)] [--nexttoken <token>]",
        note: "GET /datasetbindings；查询数据集与 COS Bucket 的绑定关系列表。授权 action: ci:DescribeDatasetBindings。",
      },
      {
        name: "find-datasets-by-bucket",
        usage: "node scripts/ci_api.mjs find-datasets-by-bucket --appid <AppId> --region <region> --bucket <bucket-appid> [--maxresults N] [--scan-all]",
        note: "通过存储桶找到关联的数据集。传入桶要找数据集时，直接用本命令，不要自己用 list-datasets + list-bindings 一个个找。内部已封装：列全数据集 → 按各数据集所属 Region 查绑定 → 过滤出与 --bucket 关联的数据集及路径；默认跳过 BindCount=0 的数据集，--scan-all 强制全扫描。",
      },
    ],
    notes: [
      "Only R1 read operations. No create/update/delete.",
      "使用 cosRequest（COS XML 签名）访问桶 CI 域名 <bucket>.ci.<region>.myqcloud.com。",
      "各检索接口字段映射详见 references/dataset-search.md；任意命令可用 --body '<json>' 完全覆盖请求体。",
      "DescribeDatasets 等走云 API（CAPI，TC3 签名），不在本工具范围，后续单独提供。",
    ],
  };
}

async function main() {
  const { command, flags } = parseArgs(process.argv.slice(2));
  const started = Date.now();

  try {
    // 严格模式首次使用计费类检索命令时暂停并下发计费提示交互；有效确认回执记录后放行。
    const billingGate = evaluateBillingNotice({
      action: command,
      confirmation: flags['billing-confirmation'],
    });
    if (billingGate && billingGate.billingStatus === 'requires_confirmation') {
      print({
        ok: false,
        command,
        billingStatus: billingGate.billingStatus,
        clientAction: billingGate.clientAction,
        message: '数据万象（CI）与智能检索为按量计费服务，首次使用前需确认已知悉计费规则；确认后原样回填回执并重试原命令。',
        runtime: runtimeMeta(),
        elapsedMs: Date.now() - started,
      });
      return;
    }
    let result;
    switch (command) {
      case "help":
      case "--help":
      case "-h":
        result = helpText();
        break;
      case 'ci-service-status':
        result = await ciServiceStatus(flags);
        break;
      case "simple-query":
        result = await simpleQuery(flags);
        break;
      case "image-search":
        result = await imageSearch(flags);
        break;
      case "doc-search":
        result = await docSearch(flags);
        break;
      case "video-search":
        result = await videoSearch(flags);
        break;
      case "face-search":
        result = await faceSearch(flags);
        break;
      case "face-clip-search":
        result = await faceClipSearch(flags);
        break;
      case "get-ai-media-info":
        result = await getAiMediaInfo(flags);
        break;
      case "image-analysis":
        result = await imageAnalysis(flags);
        break;
      case "image-exif":
        result = await imageExif(flags);
        break;
      case "list-datasets":
        result = await listDatasets(flags);
        break;
      case "list-bindings":
        result = await listBindings(flags);
        break;
      case "find-datasets-by-bucket":
        result = await findDatasetsByBucket(flags);
        break;
      default: {
        const err = new Error(`unknown command: ${command}; run: node scripts/ci_api.mjs help`);
        err.code = "UnknownCommand";
        throw err;
      }
    }

    print({
      ...result,
      runtime: runtimeMeta(),
      elapsedMs: Date.now() - started,
    });
    if (!result.ok) process.exitCode = 1;
  } catch (error) {
    fail(error, { tool: command, elapsedMs: Date.now() - started });
  }
}

main();
