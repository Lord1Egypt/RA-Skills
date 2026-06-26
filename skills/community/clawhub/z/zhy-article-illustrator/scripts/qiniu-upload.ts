#!/usr/bin/env bun
/**
 * qiniu-upload.ts — 七牛云文件上传（零依赖实现）
 *
 * 使用七牛云 HTTP 上传 API，通过 HMAC-SHA1 签名生成 uploadToken，
 * multipart/form-data POST 上传文件到指定 bucket。
 *
 * 用法:
 *   bun run scripts/qiniu-upload.ts --file <本地路径> --key <远程路径>
 *   bun run scripts/qiniu-upload.ts --file img.png --key illustrations/demo/01.png
 *   bun run scripts/qiniu-upload.ts --dir ./images --prefix illustrations/demo/
 *
 * 环境变量（从技能根目录 .env 读取）:
 *   QINIU_ACCESS_KEY  — AK
 *   QINIU_SECRET_KEY  — SK
 *   QINIU_BUCKET      — 存储空间名
 *   QINIU_DOMAIN      — CDN 域名（含 https://）
 *   QINIU_REGION      — 区域代码（z0=华东, z1=华北, z2=华南, na0=北美, as0=东南亚）
 */

import { createHmac } from "crypto";
import { readFileSync, readdirSync, statSync, existsSync } from "fs";
import { join, basename, resolve, extname } from "path";

// ─── 类型 ────────────────────────────────────────────────────────────

interface UploadResult {
  success: boolean;
  file: string;
  key: string;
  url?: string;
  error?: string;
}

interface QiniuConfig {
  accessKey: string;
  secretKey: string;
  bucket: string;
  domain: string;
  region: string;
}

// ─── 配置加载 ─────────────────────────────────────────────────────────

function loadEnvFile(filePath: string): Record<string, string> {
  const vars: Record<string, string> = {};
  if (!existsSync(filePath)) return vars;
  const content = readFileSync(filePath, "utf-8");
  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    let val = trimmed.slice(eqIdx + 1).trim();
    // 去掉引号
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    vars[key] = val;
  }
  return vars;
}

function loadConfig(): QiniuConfig {
  // 优先从环境变量读取，否则从技能根目录 .env
  const envFile = resolve(process.cwd(), ".env");
  const fileVars = loadEnvFile(envFile);

  const get = (key: string): string => process.env[key] || fileVars[key] || "";

  const accessKey = get("QINIU_ACCESS_KEY");
  const secretKey = get("QINIU_SECRET_KEY");
  const bucket = get("QINIU_BUCKET");
  const domain = get("QINIU_DOMAIN").replace(/\/+$/, "");
  const region = get("QINIU_REGION") || "z0";

  if (!accessKey || !secretKey || !bucket || !domain) {
    console.error("Error: 七牛云配置不完整");
    console.error(`请在 ${envFile} 中配置以下变量：`);
    console.error("  QINIU_ACCESS_KEY=<你的 AK>");
    console.error("  QINIU_SECRET_KEY=<你的 SK>");
    console.error("  QINIU_BUCKET=<存储空间名>");
    console.error("  QINIU_DOMAIN=<CDN 域名，如 https://cdn.example.com>");
    console.error("  QINIU_REGION=<区域，如 z0>（可选，默认 z0）");
    process.exit(1);
  }

  return { accessKey, secretKey, bucket, domain, region };
}

// ─── 七牛云上传核心 ───────────────────────────────────────────────────

/**
 * 上传区域对应的 host
 * 参考：https://developer.qiniu.com/kodo/1671/region-endpoint-fq
 */
function getUploadHost(region: string): string {
  const hosts: Record<string, string> = {
    "z0": "https://up-z0.qiniup.com",
    "cn-east-2": "https://up-cn-east-2.qiniup.com",
    "z1": "https://up-z1.qiniup.com",
    "z2": "https://up-z2.qiniup.com",
    "na0": "https://up-na0.qiniup.com",
    "as0": "https://up-as0.qiniup.com",
    "ap-southeast-2": "https://up-ap-southeast-2.qiniup.com",
    "ap-southeast-3": "https://up-ap-southeast-3.qiniup.com",
  };
  return hosts[region] || hosts["z0"];
}

/**
 * 生成七牛云上传凭证（upload token）
 *
 * 算法：
 * 1. 构建 put policy JSON（scope, deadline）
 * 2. Base64 URL-safe 编码
 * 3. HMAC-SHA1 签名
 * 4. 拼接为 AK:sign:encodedPolicy
 */
function generateUploadToken(config: QiniuConfig, key: string): string {
  const deadline = Math.floor(Date.now() / 1000) + 3600; // 1 小时有效

  const putPolicy = JSON.stringify({
    scope: `${config.bucket}:${key}`,  // 覆盖上传
    deadline,
    returnBody: '{"key":"$(key)","hash":"$(etag)","fsize":$(fsize)}',
  });

  const encodedPolicy = base64UrlSafe(Buffer.from(putPolicy));
  const sign = base64UrlSafe(
    createHmac("sha1", config.secretKey).update(encodedPolicy).digest()
  );

  return `${config.accessKey}:${sign}:${encodedPolicy}`;
}

function base64UrlSafe(buf: Buffer): string {
  return buf.toString("base64").replace(/\+/g, "-").replace(/\//g, "_");
}

/**
 * 上传单个文件到七牛云
 */
async function uploadFile(
  config: QiniuConfig,
  localPath: string,
  remoteKey: string
): Promise<UploadResult> {
  const absPath = resolve(localPath);

  if (!existsSync(absPath)) {
    return { success: false, file: localPath, key: remoteKey, error: `文件不存在: ${absPath}` };
  }

  const token = generateUploadToken(config, remoteKey);
  const fileData = readFileSync(absPath);
  const fileName = basename(absPath);

  // 构建 multipart/form-data
  const formData = new FormData();
  formData.append("token", token);
  formData.append("key", remoteKey);

  // 根据扩展名推断 MIME 类型
  const mimeTypes: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".bmp": "image/bmp",
    ".ico": "image/x-icon",
  };
  const mime = mimeTypes[extname(absPath).toLowerCase()] || "application/octet-stream";
  const blob = new Blob([fileData], { type: mime });
  formData.append("file", blob, fileName);

  const uploadHost = getUploadHost(config.region);

  try {
    const resp = await fetch(`${uploadHost}/`, {
      method: "POST",
      body: formData,
    });

    if (!resp.ok) {
      const errorText = await resp.text();
      return {
        success: false,
        file: localPath,
        key: remoteKey,
        error: `HTTP ${resp.status}: ${errorText}`,
      };
    }

    const body = await resp.json();
    const url = `${config.domain}/${remoteKey}`;
    return { success: true, file: localPath, key: body.key || remoteKey, url };
  } catch (err: any) {
    return {
      success: false,
      file: localPath,
      key: remoteKey,
      error: `网络错误: ${err.message}`,
    };
  }
}

// ─── CLI 参数解析 ──────────────────────────────────────────────────────

function parseArgs(): {
  mode: "file" | "dir";
  file?: string;
  key?: string;
  dir?: string;
  prefix?: string;
} {
  const args = process.argv.slice(2);
  const map: Record<string, string> = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--") && i + 1 < args.length) {
      map[args[i].slice(2)] = args[i + 1];
      i++;
    }
  }

  if (map["dir"]) {
    return { mode: "dir", dir: map["dir"], prefix: map["prefix"] || "" };
  }

  if (map["file"]) {
    if (!map["key"]) {
      // 默认 key 就是文件名
      map["key"] = basename(map["file"]);
    }
    return { mode: "file", file: map["file"], key: map["key"] };
  }

  console.error("用法:");
  console.error("  单文件上传: bun run scripts/qiniu-upload.ts --file <路径> --key <远程路径>");
  console.error("  目录批量:   bun run scripts/qiniu-upload.ts --dir <目录> --prefix <远程前缀>");
  process.exit(1);
}

// ─── 主流程 ───────────────────────────────────────────────────────────

async function main() {
  const opts = parseArgs();
  const config = loadConfig();

  const results: UploadResult[] = [];

  if (opts.mode === "file") {
    console.log(`上传: ${opts.file} → ${opts.key}`);
    const result = await uploadFile(config, opts.file!, opts.key!);
    results.push(result);
  } else {
    const dirPath = resolve(opts.dir!);
    if (!existsSync(dirPath)) {
      console.error(`目录不存在: ${dirPath}`);
      process.exit(1);
    }

    const imageExts = new Set([".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"]);
    const files = readdirSync(dirPath).filter((f) => {
      const ext = extname(f).toLowerCase();
      return imageExts.has(ext) && statSync(join(dirPath, f)).isFile();
    });

    if (files.length === 0) {
      console.log("目录中没有找到图片文件");
      process.exit(0);
    }

    console.log(`找到 ${files.length} 个图片文件，开始上传...\n`);

    for (const file of files) {
      const localPath = join(dirPath, file);
      const remoteKey = opts.prefix ? `${opts.prefix.replace(/\/+$/, "")}/${file}` : file;
      console.log(`  上传: ${file} → ${remoteKey}`);
      const result = await uploadFile(config, localPath, remoteKey);
      results.push(result);
    }
  }

  // 输出汇总
  console.log("\n" + "─".repeat(60));
  console.log("上传结果汇总:");
  console.log("─".repeat(60));

  const succeeded = results.filter((r) => r.success);
  const failed = results.filter((r) => !r.success);

  for (const r of succeeded) {
    console.log(`  ✓ ${r.key} → ${r.url}`);
  }
  for (const r of failed) {
    console.log(`  ✗ ${r.key} — ${r.error}`);
  }

  console.log(`\n成功: ${succeeded.length}  失败: ${failed.length}  总计: ${results.length}`);

  // 输出 JSON 到 stdout（方便脚本调用时解析）
  if (process.env["QINIU_OUTPUT_JSON"] === "1") {
    console.log("\n---JSON---");
    console.log(JSON.stringify(results, null, 2));
  }

  if (failed.length > 0) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
