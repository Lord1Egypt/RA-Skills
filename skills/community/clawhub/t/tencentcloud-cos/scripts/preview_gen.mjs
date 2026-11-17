#!/usr/bin/env node
/**
 * 检索结果预览 HTML 一键生成器。
 *
 * 目的：把「逐个 sign-url → 手写填充 HTML」压缩为一条命令，显著降低场景耗时。
 * - 入参格式**固化且极简**：只需 uri 列表 + 少量元信息，其余字段脚本自动补全；
 * - 签名在**本地纯计算**（lib/presign.mjs），零网络请求，N 个文件也是毫秒级；
 * - 视频自动用数据万象 snapshot 截帧作封面；文档自动用 doc-preview 首页图；
 * - 输出完整单文件 HTML（模板 references/preview/search-results.html），可直接交给 exportFile。
 *
 * 用法：
 *   # 1) 直接传 JSON 字符串
 *   node scripts/preview_gen.mjs --spec '{"bucket":"b-125","region":"ap-guangzhou","query":"海边日落","items":[{"uri":"cos://b-125/a.jpg"}]}'
 *
 *   # 2) 从文件读（推荐，避免 shell 转义）
 *   node scripts/preview_gen.mjs --spec-file /tmp/spec.json --out /tmp/search-results.html
 *
 *   # 3) 从 stdin 读
 *   echo '<spec json>' | node scripts/preview_gen.mjs --out /tmp/search-results.html
 *
 * Spec（固化入参）：
 * {
 *   "bucket":   "example-1250000000",   // 必填（items[].uri 已含 bucket 时可省略）
 *   "region":   "ap-guangzhou",         // 必填
 *   "query":    "海边日落",              // 可选：展示用检索条件（填用户原话）
 *   "datasetName": "example-dataset",      // 可选：无数据集（GetBucket 列举）时省略
 *   "tool":     "image-search",         // 可选
 *   "total":    128,                    // 可选：命中总数，缺省取 items.length
 *   "expires":  3600,                   // 可选：签名有效期秒，默认 3600
 *   "items": [                          // 必填：命中文件，建议 <=20
 *     { "uri":"cos://b/a.jpg" },                             // 最简：只给 uri，类型由后缀推断
 *     { "uri":"cos://b/v.mp4", "snapshotTime": 3 },          // 视频：可指定截帧秒（默认 1）
 *     { "uri":"cos://b/d.pdf", "text":"命中片段", "page":3 },  // 文档：命中文本与页码（缩略图取该页）
 *     { "uri":"cos://b/t.xlsx", "sheet":2 },                 // 表格：第几张表，可加 excelPaperDirection:1 横向
 *     { "uri":"cos://b/noext", "srcType":"docx" },           // 无后缀对象：必须显式给 srcType
 *     { "uri":"cos://b/v.mp4", "from":12.5, "to":18.2 }      // 视频片段：命中起止秒
 *   ]
 * }
 *
 * 文档预览缩略图参数对齐官方文档（doc-preview 同步转码）：
 *   https://cloud.tencent.com/document/product/436/121090
 * 注意该接口**没有 width/height 参数**，宽度通过 ImageParams=imageMogr2/thumbnail/240x 控制。
 *
 * 输出：stdout 打印 JSON 结果（含 htmlPath / html 字节数 / 统计）；--out 指定落盘路径。
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { getRuntimeCredentials } from "./lib/ci_client.mjs";
import {
  parseCosUri,
  presignUrl,
  presignVideoSnapshot,
  presignDocPreview,
  docSrcTypeOf,
} from "./lib/presign.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATE_PATH = path.resolve(__dirname, "../references/preview/search-results.html");

const IMAGE_EXT = new Set(["jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff", "tif", "avif", "heif", "heic"]);
const VIDEO_EXT = new Set(["mp4", "mov", "avi", "mkv", "flv", "wmv", "webm", "m4v", "mpg", "mpeg", "ts", "m3u8"]);
const AUDIO_EXT = new Set(["mp3", "wav", "flac", "aac", "m4a", "ogg", "wma", "amr"]);

/**
 * doc-preview 支持的输入格式（对齐 https://cloud.tencent.com/document/product/436/121090）
 * 演示 / 文字 / 表格 / 其他（含纯文本与代码类）
 */
const DOC_EXT = new Set([
  // 演示
  "pptx", "ppt", "pot", "potx", "pps", "ppsx", "dps", "dpt", "pptm", "potm", "ppsm",
  // 文字
  "doc", "dot", "wps", "wpt", "docx", "dotx", "docm", "dotm",
  // 表格
  "xls", "xlt", "et", "ett", "xlsx", "xltx", "csv", "xlsb", "xlsm", "xltm", "ets",
  // 其他
  "pdf", "lrc", "c", "cpp", "h", "asm", "s", "java", "asp", "bat", "bas", "prg",
  "cmd", "rtf", "txt", "log", "xml", "htm", "html",
]);

/** 表格类：需用 sheet 参数，且列多时建议横向输出 */
const SHEET_EXT = new Set(["xls", "xlt", "et", "ett", "xlsx", "xltx", "csv", "xlsb", "xlsm", "xltm", "ets"]);

function extOf(key) {
  const base = String(key || "").split("?")[0];
  const idx = base.lastIndexOf(".");
  return idx >= 0 ? base.slice(idx + 1).toLowerCase() : "";
}

/**
 * 推断展示类型。
 * 优先级：显式 type > 显式 srcType（无后缀对象场景，视为文档）> 扩展名。
 */
function guessType(key, item = {}) {
  if (item.type) return item.type;
  const ext = extOf(key);
  // 无后缀对象若显式给了 srcType，按该源类型判定（doc-preview 要求无后缀必须带 srcType）
  const probe = ext || String(item.srcType || "").toLowerCase();
  if (IMAGE_EXT.has(probe)) return "image";
  if (VIDEO_EXT.has(probe)) return "video";
  if (DOC_EXT.has(probe)) return "doc";
  if (AUDIO_EXT.has(probe)) return "audio";
  return "other";
}

function fileNameOf(key) {
  const parts = String(key || "").split("?")[0].split("/");
  return parts[parts.length - 1] || String(key || "");
}

function fmtClock(sec) {
  if (sec == null || Number.isNaN(Number(sec))) return "";
  const n = Math.max(0, Math.floor(Number(sec)));
  return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, "0")}`;
}

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (!a.startsWith("--")) continue;
    const k = a.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      out[k] = next;
      i += 1;
    } else {
      out[k] = true;
    }
  }
  return out;
}

function readStdin() {
  try {
    return fs.readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

function fail(code, message, extra = {}) {
  process.stdout.write(`${JSON.stringify({ ok: false, tool: "preview-gen", error: { code, message }, ...extra }, null, 2)}\n`);
  process.exit(1);
}

/** 把固化 spec 展开为模板所需的 result-data */
function buildResultData(spec, creds) {
  const region = spec.region;
  const expires = Number(spec.expires) || 3600;
  const items = Array.isArray(spec.items) ? spec.items.slice(0, 40) : [];

  const stats = { image: 0, video: 0, doc: 0, audio: 0, other: 0, signed: 0 };
  const thumbs = [];
  const extra = {};
  const warnings = [];

  for (const raw of items) {
    const item = typeof raw === "string" ? { uri: raw } : raw || {};
    const parsed = parseCosUri(item.uri);
    const bucket = item.bucket || parsed.bucket || spec.bucket;
    const key = item.key || parsed.key;
    if (!bucket || !key) continue;

    const type = guessType(key, item);
    stats[type] = (stats[type] || 0) + 1;

    const base = {
      secretId: creds.secretId,
      secretKey: creds.secretKey,
      token: creds.token,
      bucket,
      region,
      key,
      expires,
    };

    // 源文件签名地址（点击图片新标签打开）
    const signedUrl = presignUrl(base);
    stats.signed += 1;

    // 缩略图展示地址：图片直接用源图；视频走 snapshot 截帧；文档走 doc-preview 首页图
    let url = "";
    if (type === "image") {
      url = signedUrl;
    } else if (type === "video") {
      url = presignVideoSnapshot({
        ...base,
        time: item.snapshotTime != null ? item.snapshotTime
            : (item.from != null ? Math.max(0, Math.floor(Number(item.from))) : 1),
        width: 240,
      });
    } else if (type === "doc") {
      // 文档预览缩略图：doc-preview 无 width 参数，宽度靠 ImageParams(imageMogr2) 控制
      const ext = docSrcTypeOf(key);
      // 对象无后缀名时必须显式给 srcType（item.srcType），否则 doc-preview 无法识别源格式
      const srcType = item.srcType || "";
      if (!ext && !srcType) {
        warnings.push(
          `${key}: 对象无后缀名且未指定 srcType，doc-preview 可能无法识别源格式（缩略图将降级为占位图标）`,
        );
      }
      const docExt = ext || srcType.toLowerCase();
      url = presignDocPreview({
        ...base,
        page: item.page || 1,
        width: 240,
        dstType: item.dstType || "jpg",
        ...(srcType ? { srcType } : {}),
        // 表格类：指定第几张表；列多时可用 excelPaperDirection=1 横向输出
        ...(SHEET_EXT.has(docExt)
          ? {
              sheet: item.sheet != null ? item.sheet : 1,
              ...(item.excelPaperDirection != null
                ? { excelPaperDirection: item.excelPaperDirection }
                : {}),
            }
          : {}),
        ...(item.password ? { password: item.password } : {}),
        ...(item.comment != null ? { comment: item.comment } : {}),
        ...(item.imageParams ? { imageParams: item.imageParams } : {}),
      });
    }

    // 角标：视频优先显示命中时间点 / 时长位置，其余用显式 label
    let label = item.label;
    if (label == null && type === "video") {
      label = item.from != null ? fmtClock(item.from)
            : (item.snapshotTime != null ? fmtClock(item.snapshotTime) : "视频");
    }
    if (label == null && type === "doc" && item.page) label = `P.${item.page}`;

    thumbs.push({
      url,
      signedUrl,
      uri: `cos://${bucket}/${key}`,
      name: item.name || fileNameOf(key),
      type: type === "video" ? "video" : (type === "image" ? "image" : type),
      ...(label ? { label: String(label) } : {}),
    });

    // 首个带命中详情的项目提升到 extra（模板顶部 chips / 片段展示）
    if (extra.text == null && item.text) {
      extra.text = String(item.text);
      if (item.page != null) extra.textPage = item.page;
    }
    if (extra.from == null && item.from != null && item.to != null) {
      extra.from = Number(item.from);
      extra.to = Number(item.to);
    }
    if (extra.faceId == null && item.faceId) extra.faceId = String(item.faceId);
  }

  if (!thumbs.length) {
    const err = new Error("no valid items: 每项需可解析出 bucket + key（uri 形如 cos://bucket/key）");
    err.code = "EmptyItems";
    throw err;
  }

  const first = thumbs[0];
  return {
    data: {
      ...(spec.tool ? { tool: spec.tool } : {}),
      region,
      uri: first.uri,
      ...(spec.datasetName ? { datasetName: spec.datasetName } : {}),
      bucket: spec.bucket || parseCosUri(first.uri).bucket,
      ...(spec.query ? { query: spec.query } : {}),
      total: spec.total != null ? Number(spec.total) : thumbs.length,
      signedUrl: first.signedUrl,
      thumbs,
      extra,
    },
    stats,
    warnings,
  };
}

function renderHtml(resultData) {
  const tpl = fs.readFileSync(TEMPLATE_PATH, "utf8");
  const json = JSON.stringify(resultData, null, 2);
  // 只替换 <script id="result-data"> 内的 JSON，模板结构 / 样式保持原样
  const re = /(<script id="result-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
  if (!re.test(tpl)) {
    const err = new Error(`template placeholder not found in ${TEMPLATE_PATH}`);
    err.code = "BadTemplate";
    throw err;
  }
  // 防止数据里的 </script> 提前闭合脚本标签
  const safe = json.replace(/<\/script/gi, "<\\/script");
  return tpl.replace(re, `$1\n${safe}\n$3`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || args.h) {
    process.stdout.write(
      [
        "用法：",
        "  node scripts/preview_gen.mjs --spec-file <spec.json> [--out <out.html>]",
        "  node scripts/preview_gen.mjs --spec '<json>' [--out <out.html>]",
        "  cat spec.json | node scripts/preview_gen.mjs [--out <out.html>]",
        "",
        "Spec 必填：region + items[]（每项 uri，形如 cos://bucket/key）；bucket 可由 uri 推断。",
        "Spec 可选：query / datasetName / tool / total / expires。",
        "视频自动 snapshot 截帧作封面，文档自动 doc-preview 首页图。",
        "",
      ].join("\n"),
    );
    return;
  }

  let rawSpec = "";
  if (args["spec-file"]) {
    try {
      rawSpec = fs.readFileSync(String(args["spec-file"]), "utf8");
    } catch (e) {
      fail("SpecFileUnreadable", `无法读取 --spec-file: ${e.message}`);
    }
  } else if (typeof args.spec === "string") {
    rawSpec = args.spec;
  } else {
    rawSpec = readStdin();
  }

  if (!String(rawSpec).trim()) {
    fail("MissingSpec", "缺少 spec：用 --spec-file / --spec 或 stdin 传入固化 JSON");
  }

  let spec;
  try {
    spec = JSON.parse(rawSpec);
  } catch (e) {
    fail("BadSpecJson", `spec JSON 解析失败: ${e.message}`);
  }

  if (!spec.region) fail("MissingRegion", "spec.region 必填（如 ap-guangzhou）");
  if (!Array.isArray(spec.items) || !spec.items.length) fail("MissingItems", "spec.items 必填且非空");

  const creds = getRuntimeCredentials();
  if (!creds.secretId || !creds.secretKey) {
    fail("MissingCredentials", "缺少当前运行模式所需的 COS 凭证");
  }

  let built;
  let html;
  try {
    built = buildResultData(spec, creds);
    html = renderHtml(built.data);
  } catch (e) {
    fail(e.code || "BuildFailed", e.message);
  }

  const outPath = args.out
    ? path.resolve(String(args.out))
    : path.resolve(process.cwd(), "search-results.html");

  try {
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, html, "utf8");
  } catch (e) {
    fail("WriteFailed", `写入 HTML 失败: ${e.message}`);
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        ok: true,
        tool: "preview-gen",
        htmlPath: outPath,
        bytes: Buffer.byteLength(html, "utf8"),
        fileCount: built.data.thumbs.length,
        total: built.data.total,
        typeStats: built.stats,
        expiresIn: Number(spec.expires) || 3600,
        ...(built.warnings && built.warnings.length ? { warnings: built.warnings } : {}),
        nextStep:
          "用 sandbox-export 的 exportFile 导出该 HTML，取 artifactId 后输出：" +
          "[iframe:artifact|{artifactId}|maxWidth=720|maxHeight=186|title=检索结果]",
      },
      null,
      2,
    )}\n`,
  );
}

main();
