#!/usr/bin/env node
/**
 * engine-assets.mjs — REA-CN 付费版 · 引擎资产共享模块
 *
 * 被 pay-gate.mjs（付费闸）与 run-mcp.mjs（启动入口）共用：
 *   - sha256File         计算文件 SHA256（与网关 ENGINE_SHA256 对齐）
 *   - extractZip         四路兜底解压（tar / unzip / PowerShell / python）
 *   - readEntitlement    读取 engine/.entitlement.json（付费放行凭证）
 *   - writeEntitlement   登记付费放行凭证（含服务端 expires_at 24h 时效）
 *   - entitlementExpiresAt / entitlementStatus / entitlementValid
 *                        24h 有效期三件套（SkillHub 规则：单次付费 24h 内免验证，过期需重新付费）
 *
 * 仅使用 Node 内置模块 + 子进程调用系统工具。语法可通过 `node --check` 校验。
 */
import { createHash, createPublicKey, verify as cryptoVerify } from "node:crypto";
import { existsSync, readFileSync, writeFileSync, mkdirSync, copyFileSync, readdirSync } from "node:fs";
import { execFileSync, spawnSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { ENTITLEMENT_PUBLIC_KEY_PEM, ENTITLEMENT_SKILL_ID } from "./entitlement-key.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));

/** 计算文件 SHA256（hex） */
export function sha256File(filePath) {
  const buf = readFileSync(filePath);
  return createHash("sha256").update(buf).digest("hex");
}

/**
 * 可移植的递归目录复制（copyFileSync + mkdirSync 实现）。
 * 不用 fs.cpSync 的原因：部分 Node 构建（实测托管 Node v22.22.2）在目标路径
 * 含非 ASCII 字符（如中文工作区路径）时 cpSync 会静默失败——不抛错、不复制。
 * 符号链接按普通文件复制其目标内容（node_modules 的 .bin 场景可接受）。
 */
export function copyDirSync(src, dest) {
  mkdirSync(dest, { recursive: true });
  for (const entry of readdirSync(src, { withFileTypes: true })) {
    const s = join(src, entry.name);
    const d = join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(s, d);
    } else {
      copyFileSync(s, d);
    }
  }
}

/** 判断命令是否可用（spawnSync 不抛异常） */
function hasCommand(cmd, args = ["--version"]) {
  try {
    const r = spawnSync(cmd, args, { stdio: "ignore", shell: process.platform === "win32" });
    return r.status === 0 || r.status === null && !r.error;
  } catch {
    return false;
  }
}

/**
 * 四路兜底解压 zip 到目标目录（覆盖已存在文件）。
 * @returns {{ok: boolean, via?: string, error?: string}}
 */
export function extractZip(zipPath, destDir) {
  if (!existsSync(zipPath)) return { ok: false, error: `zip 不存在: ${zipPath}` };
  mkdirSync(destDir, { recursive: true });

  const attempts = [
    // 1) tar：Windows 10 1803+ 与所有 Unix 自带，bsdtar 原生支持 zip
    { cmd: "tar", args: ["-xf", zipPath, "-C", destDir], label: "tar" },
    // 2) unzip：Git Bash / Linux / macOS
    { cmd: "unzip", args: ["-o", "-q", zipPath, "-d", destDir], label: "unzip" },
    // 3) PowerShell Expand-Archive：Windows 原生
    { cmd: "powershell", args: ["-NoProfile", "-Command",
      `Expand-Archive -LiteralPath '${zipPath}' -DestinationPath '${destDir}' -Force`], label: "powershell" },
    // 4) python zipfile：最后兜底
    { cmd: "python", args: ["-c",
      `import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])`, zipPath, destDir], label: "python" },
  ];

  for (const a of attempts) {
    try {
      const r = spawnSync(a.cmd, a.args, { stdio: "pipe", shell: process.platform === "win32" });
      if (r.status === 0) {
        // 校验解压产物：engine 目录下应有 dist/ 与 scripts/rea.mjs
        const marker = join(destDir, "engine", "scripts", "rea.mjs");
        const altMarker = join(destDir, "scripts", "rea.mjs");
        if (existsSync(marker) || existsSync(altMarker)) {
          return { ok: true, via: a.label };
        }
      }
    } catch { /* 尝试下一路 */ }
  }
  return { ok: false, error: "四路解压（tar/unzip/powershell/python）均失败" };
}

/** 读取 entitlement（不存在返回 null） */
export function readEntitlement(engineDir) {
  const p = join(engineDir, ".entitlement.json");
  if (!existsSync(p)) return null;
  try {
    return JSON.parse(readFileSync(p, "utf-8"));
  } catch {
    return null;
  }
}

/** 登记 entitlement（付费放行凭证）。data.expires_at 为服务端履约时签发的 ISO 到期时间 */
export function writeEntitlement(engineDir, data) {
  mkdirSync(engineDir, { recursive: true });
  const p = join(engineDir, ".entitlement.json");
  const record = {
    skill: "rea-cn-paid",
    engineVersion: "6.4.0",
    granted_at: new Date().toISOString(),
    ...data,
  };
  writeFileSync(p, JSON.stringify(record, null, 2) + "\n", "utf-8");
  return record;
}

/**
 * entitlement 到期时刻（Date）。
 * 优先用服务端 expires_at（履约时刻 + 24h，ISO 带时区，权威）；
 * 兜底用本地 granted_at + ttlHours（防服务端未下发时的无限期白嫖）。
 */
export function entitlementExpiresAt(ent, ttlHours = 24) {
  if (!ent) return null;
  if (ent.expires_at) {
    const d = new Date(ent.expires_at);
    if (!Number.isNaN(d.getTime())) return d;
  }
  if (ent.granted_at) {
    const g = new Date(ent.granted_at);
    if (!Number.isNaN(g.getTime())) return new Date(g.getTime() + ttlHours * 3600 * 1000);
  }
  return null;
}

/**
 * 校验本地凭证的 Ed25519 签名（服务端私钥签发，本包只有公钥 → 可验不可伪造）。
 * 签名原文 = `${skill}\n${out_trade_no}\n${expires_at}`
 * @returns {boolean} true=签名有效
 */
export function verifyEntitlementSignature(ent) {
  if (!ent || !ent.signature) return false;
  const expiresAt = ent.expires_at || "";
  if (!expiresAt) return false;
  try {
    const payload = Buffer.from(
      `${ENTITLEMENT_SKILL_ID}\n${ent.out_trade_no}\n${expiresAt}`,
      "utf-8"
    );
    const key = createPublicKey(ENTITLEMENT_PUBLIC_KEY_PEM);
    return cryptoVerify(null, payload, key, Buffer.from(String(ent.signature), "base64"));
  } catch {
    return false;
  }
}

/**
 * entitlement 状态：
 *   ENTITLED     有效（签名正确 + 24h 内）→ 免验证直接放行
 *   EXPIRED      过期，需重新付费
 *   FORGED       凭证缺失签名或签名校验失败（被手搓/篡改）→ 视同未解锁，需付费
 *   NOT_ENTITLED 从未解锁
 */
export function entitlementStatus(ent, ttlHours = 24) {
  if (!ent || ent.skill !== "rea-cn-paid" || !ent.out_trade_no) return "NOT_ENTITLED";
  // 签名是权威来源：无签名 / 签名不匹配 → 一律视为无效凭证（防手搓 .entitlement.json）
  if (!verifyEntitlementSignature(ent)) {
    return ent.expires_at ? "FORGED" : "NOT_ENTITLED";
  }
  const exp = entitlementExpiresAt(ent, ttlHours);
  if (!exp) return "ENTITLED";
  return Date.now() < exp.getTime() ? "ENTITLED" : "EXPIRED";
}

/** entitlement 是否有效（存在、技能匹配、且在 24h 有效期内） */
export function entitlementValid(ent, ttlHours = 24) {
  return entitlementStatus(ent, ttlHours) === "ENTITLED";
}

/** 读取本技能包的 config/cn-config.json */
export function readSkillConfig() {
  const p = join(__dirname, "..", "..", "config", "cn-config.json");
  return JSON.parse(readFileSync(p, "utf-8"));
}

// ============================================================
// base64 文本分片（SkillHub 禁止上传二进制的适配方案）
// ============================================================
const CHUNK_DIR = join(__dirname, "..", "..", "engine-b64");

/** 读取 base64 分片清单（不存在返回 null——纯文本包无分片，引擎走网关交付） */
export function readChunkManifest() {
  const p = join(CHUNK_DIR, "manifest.json");
  if (!existsSync(p)) return null;
  try { return JSON.parse(readFileSync(p, "utf-8")); } catch { return null; }
}

/**
 * 从包内 base64 文本分片重建 engine.zip（自包含包免联网；SHA256 全程校验）。
 * 已有有效 zip 则直接复用。返回 {ok, via:"existing"|"chunks", size?, error?}
 */
export function ensureEngineZip(skillRoot, expectedSha = "") {
  const zipPath = join(skillRoot, "engine.zip");
  const man = readChunkManifest();
  if (!man) return { ok: false, error: "engine-b64/manifest.json 不存在（纯文本包：引擎经官网网关付费交付）" };
  if (existsSync(zipPath) && (!expectedSha || sha256File(zipPath) === expectedSha)) {
    return { ok: true, via: "existing" };
  }
  const parts = [];
  for (let i = 1; i <= man.chunks; i++) {
    const name = `part-${String(i).padStart(2, "0")}.txt`;
    const p = join(CHUNK_DIR, name);
    if (!existsSync(p)) return { ok: false, error: `分片缺失: engine-b64/${name}` };
    parts.push(readFileSync(p, "utf-8").replace(/\s+/g, ""));
  }
  // 逐片解码后再拼二进制：每片 base64 自带 "=" 填充，先拼文本会被填充符截断导致数据损坏
  const buf = Buffer.concat(parts.map((p) => Buffer.from(p, "base64")));
  const got = createHash("sha256").update(buf).digest("hex");
  if (got !== man.sha256) {
    return { ok: false, error: `分片拼合 SHA256 不符（期望 ${man.sha256.slice(0, 16)}… 实得 ${got.slice(0, 16)}…）` };
  }
  if (expectedSha && got !== expectedSha) {
    return { ok: false, error: "分片拼合结果与配置 engineZipSha256 不一致" };
  }
  writeFileSync(zipPath, buf);
  return { ok: true, via: "chunks", size: buf.length };
}

export { execFileSync };
