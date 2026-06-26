#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { buildArticleHtml, readOptionalText } from "../lib/style.mjs";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        args[arg.slice(2)] = true;
      } else {
        args[arg.slice(2)] = next;
        i += 1;
      }
    }
  }
  return args;
}

function stripHtml(html) {
  return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function resolveAccounts(config, args) {
  const accounts = config.wechat?.accounts || {};
  if (args["all-enabled"]) {
    return Object.entries(accounts)
      .filter(([, account]) => account.enabled !== false)
      .map(([id]) => id);
  }

  const raw = args.accounts || args.account || config.wechat?.defaultAccount || "default";
  return String(raw)
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function resolvePublishingConfig(config, account) {
  return {
    ...(config.publishing || {}),
    ...(account?.publishing || {})
  };
}

async function loadConfig(configPath) {
  const resolved = path.resolve(configPath);
  const raw = await fs.readFile(resolved, "utf8");
  return JSON.parse(raw);
}

async function loadTemplateVariable(configDir, publishing, templateName, registryArg) {
  if (!templateName) {
    return null;
  }
  const registryPath = registryArg || publishing.templateVariablesFile || "";
  if (!registryPath) {
    throw new Error("Template variable requested but no registry file configured");
  }
  const resolved = path.resolve(configDir, registryPath);
  const raw = await fs.readFile(resolved, "utf8");
  const parsed = JSON.parse(raw);
  const template = parsed?.templates?.[templateName];
  if (!template) {
    throw new Error(`Template variable not found: ${templateName}`);
  }
  return template;
}

async function getAccessToken(config, accountId, tokenCacheDir) {
  const account = config.wechat.accounts[accountId];
  if (!account) {
    throw new Error(`Unknown account: ${accountId}`);
  }

  await fs.mkdir(tokenCacheDir, { recursive: true });
  const cacheFile = path.join(tokenCacheDir, `token_cache_${accountId.replace(/[^\w\u4e00-\u9fff-]+/g, "_")}.json`);

  try {
    const raw = await fs.readFile(cacheFile, "utf8");
    const cached = JSON.parse(raw);
    if (Date.now() / 1000 < Number(cached.expires_at || 0) - 300) {
      return cached.access_token;
    }
  } catch {}

  const params = new URLSearchParams({
    grant_type: "client_credential",
    appid: account.appId,
    secret: account.appSecret
  });
  const url = `${config.wechat.apiBaseUrl || "https://api.weixin.qq.com"}/cgi-bin/token?${params.toString()}`;
  const response = await fetch(url);
  const result = await response.json();

  if (result.errcode) {
    throw new Error(`Get access token failed for ${accountId}: ${result.errcode} - ${result.errmsg}`);
  }

  const expiresAt = Math.floor(Date.now() / 1000) + Number(result.expires_in || 7200);
  await fs.writeFile(cacheFile, JSON.stringify({ access_token: result.access_token, expires_at: expiresAt }, null, 2), "utf8");
  return result.access_token;
}

async function uploadImage(config, accessToken, imagePath, isThumb = false) {
  const resolved = path.resolve(imagePath);
  const fileName = path.basename(resolved);
  const type = isThumb ? "thumb" : "image";
  const url = `${config.wechat.apiBaseUrl || "https://api.weixin.qq.com"}/cgi-bin/material/add_material?access_token=${accessToken}&type=${type}`;
  const data = await fs.readFile(resolved);
  const form = new FormData();
  form.append("media", new Blob([data]), fileName);

  const response = await fetch(url, {
    method: "POST",
    body: form
  });
  const result = await response.json();
  if (result.errcode && result.errcode !== 0) {
    throw new Error(`Upload image failed: ${result.errcode} - ${result.errmsg}`);
  }
  return result;
}

async function processContentImages(config, accessToken, html, baseDir) {
  const srcMatches = [...html.matchAll(/<img[^>]*src=["']([^"']+)["'][^>]*>/gi)];
  let processed = html;

  for (const match of srcMatches) {
    const src = match[1];
    if (/^https?:\/\//i.test(src) || src.startsWith("data:")) {
      continue;
    }
    const imagePath = path.isAbsolute(src) ? src : path.resolve(baseDir, src);
    const uploaded = await uploadImage(config, accessToken, imagePath, false);
    if (uploaded.url) {
      processed = processed.replaceAll(`src="${src}"`, `src="${uploaded.url}"`);
      processed = processed.replaceAll(`src='${src}'`, `src='${uploaded.url}'`);
    }
  }

  return processed;
}

async function createDraft(config, accessToken, account, title, content, thumbMediaId = "") {
  const url = `${config.wechat.apiBaseUrl || "https://api.weixin.qq.com"}/cgi-bin/draft/add?access_token=${accessToken}`;
  const publishing = resolvePublishingConfig(config, account);
  const plainText = stripHtml(content);
  const digestBase = plainText.slice(0, 120).trim();
  const digestSuffix = account.digestSuffix ? ` ${account.digestSuffix}` : "";
  const payload = {
    articles: [
      {
        title,
        author: account.author || "OpenClaw",
        digest: `${digestBase}${digestSuffix}`.trim(),
        content,
        content_source_url: "",
        thumb_media_id: thumbMediaId,
        need_open_comment: publishing.needOpenComment ?? 1,
        only_fans_can_comment: publishing.onlyFansCanComment ?? 0,
        show_cover_pic: thumbMediaId && publishing.showCoverPic !== false ? 1 : 0
      }
    ]
  };

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const result = await response.json();
  if (result.errcode && result.errcode !== 0) {
    throw new Error(`Create draft failed: ${result.errcode} - ${result.errmsg}`);
  }
  return result.media_id;
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.config || !args.title || (!args["content-file"] && !args.content)) {
    throw new Error("Usage: node scripts/publish-node.mjs --config config.json --title 标题 --content-file article.html [--accounts a,b]");
  }

  const config = await loadConfig(args.config);
  const configDir = path.dirname(path.resolve(args.config));
  const accounts = resolveAccounts(config, args);
  const html = args["content-file"]
    ? await fs.readFile(path.resolve(args["content-file"]), "utf8")
    : String(args.content || "");

  const results = [];
  const tokenCacheDir = path.resolve(configDir, config.wechat?.tokenCacheDir || "./.tokens");
  for (const accountId of accounts) {
    const account = config.wechat?.accounts?.[accountId];
    if (!account) {
      throw new Error(`Account not found: ${accountId}`);
    }
    const publishing = resolvePublishingConfig(config, account);
    const templateVariable = await loadTemplateVariable(configDir, publishing, args["template-name"], args.registry);
    const introHtml = templateVariable?.introHtml
      || await readOptionalText(args["intro-template"] || publishing.introTemplate ? path.resolve(configDir, args["intro-template"] || publishing.introTemplate || "") : "");
    const outroHtml = templateVariable?.outroHtml
      || await readOptionalText(args["outro-template"] || publishing.outroTemplate ? path.resolve(configDir, args["outro-template"] || publishing.outroTemplate || "") : "");
    const cssFile = templateVariable?.customCss ? "" : (args["css-file"] || publishing.customCssFile ? path.resolve(configDir, args["css-file"] || publishing.customCssFile || "") : "");
    const styledHtml = await buildArticleHtml({
      html,
      theme: args.theme || publishing.defaultTheme || "modern-minimal",
      cssFile,
      customCss: [templateVariable?.customCss || "", args["custom-css"] || ""].filter(Boolean).join("\n"),
      introHtml,
      outroHtml
    });
    const accessToken = await getAccessToken(config, accountId, tokenCacheDir);
    const contentBaseDir = args["content-dir"] ? path.resolve(args["content-dir"]) : path.dirname(path.resolve(args["content-file"] || "."));
    const processedContent = await processContentImages(config, accessToken, styledHtml, contentBaseDir);
    let thumbMediaId = "";
    if (args.thumb) {
      const thumb = await uploadImage(config, accessToken, args.thumb, false);
      thumbMediaId = thumb.media_id || "";
    }
    const mediaId = await createDraft(config, accessToken, account, args.title, processedContent, thumbMediaId);
    const result = { accountId, accountName: account.name || accountId, mediaId };
    results.push(result);
    process.stdout.write(`${result.accountId}\t${result.accountName}\t${result.mediaId}\n`);
  }

  if (args["output-json"]) {
    await fs.writeFile(path.resolve(args["output-json"]), JSON.stringify(results, null, 2), "utf8");
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
