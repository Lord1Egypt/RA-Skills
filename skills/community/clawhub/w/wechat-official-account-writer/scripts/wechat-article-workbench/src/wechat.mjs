import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import sharp from "sharp";
import { config, resolveProjectPath, uploadImagesDir } from "./config.mjs";

const ARTICLE_IMAGE_MAX_BYTES = 1024 * 1024 - 1024;

async function appendFile(form, fieldName, filePath, mimeType) {
  const blob = await fs.openAsBlob(filePath, { type: mimeType });
  form.append(fieldName, blob, path.basename(filePath));
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok || data.errcode) {
    throw new Error(`WeChat API failed: ${JSON.stringify(data)}`);
  }
  return data;
}

export async function getStableAccessToken() {
  if (!config.wechatAppId || !config.wechatAppSecret) {
    throw new Error("WECHAT_APPID and WECHAT_APPSECRET are required");
  }

  const data = await postJson("https://api.weixin.qq.com/cgi-bin/stable_token", {
    grant_type: "client_credential",
    appid: config.wechatAppId,
    secret: config.wechatAppSecret,
    force_refresh: false
  });

  if (!data.access_token) throw new Error(`No access_token in response: ${JSON.stringify(data)}`);
  return data.access_token;
}

export function fileSha1(filePath) {
  const absPath = resolveProjectPath(filePath);
  const stat = fs.statSync(absPath);
  const hash = crypto.createHash("sha1");
  hash.update(path.resolve(absPath));
  hash.update(String(stat.size));
  hash.update(String(Math.trunc(stat.mtimeMs)));
  return hash.digest("hex");
}

export async function uploadPermanentImage(accessToken, filePath) {
  const absPath = resolveProjectPath(filePath);
  if (!fs.existsSync(absPath)) {
    throw new Error(`Cover image not found: ${absPath}`);
  }

  const form = new FormData();
  const mimeType = absPath.toLowerCase().endsWith(".png") ? "image/png" : "image/jpeg";
  await appendFile(form, "media", absPath, mimeType);

  const url = `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${encodeURIComponent(accessToken)}&type=image`;
  const response = await fetch(url, { method: "POST", body: form });
  const data = await response.json();
  if (!response.ok || data.errcode) {
    throw new Error(`WeChat cover upload failed: ${JSON.stringify(data)}`);
  }
  if (!data.media_id) throw new Error(`No media_id in upload response: ${JSON.stringify(data)}`);
  return data.media_id;
}

async function prepareArticleImage(filePath) {
  const absPath = resolveProjectPath(filePath);
  if (!fs.existsSync(absPath)) {
    throw new Error(`Article image not found: ${absPath}`);
  }

  const lower = absPath.toLowerCase();
  const isSupported = lower.endsWith(".png") || lower.endsWith(".jpg") || lower.endsWith(".jpeg");
  const size = fs.statSync(absPath).size;
  if (isSupported && size <= ARTICLE_IMAGE_MAX_BYTES) {
    return {
      path: absPath,
      mimeType: lower.endsWith(".png") ? "image/png" : "image/jpeg"
    };
  }

  fs.mkdirSync(uploadImagesDir, { recursive: true });
  const hash = fileSha1(absPath).slice(0, 16);
  const outputPath = path.join(uploadImagesDir, `${hash}.jpg`);

  await sharp(absPath)
    .resize({ width: 1280, height: 1280, fit: "inside", withoutEnlargement: true })
    .jpeg({ quality: 82, progressive: true, mozjpeg: true })
    .toFile(outputPath);

  if (fs.statSync(outputPath).size > ARTICLE_IMAGE_MAX_BYTES) {
    await sharp(absPath)
      .resize({ width: 960, height: 960, fit: "inside", withoutEnlargement: true })
      .jpeg({ quality: 72, progressive: true, mozjpeg: true })
      .toFile(outputPath);
  }

  if (fs.statSync(outputPath).size > ARTICLE_IMAGE_MAX_BYTES) {
    throw new Error(`Article image remains larger than 1MB after compression: ${outputPath}`);
  }

  return { path: outputPath, mimeType: "image/jpeg" };
}

export async function uploadArticleImage(accessToken, filePath) {
  const prepared = await prepareArticleImage(filePath);
  const form = new FormData();
  await appendFile(form, "media", prepared.path, prepared.mimeType);

  const url = `https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=${encodeURIComponent(accessToken)}`;
  const response = await fetch(url, { method: "POST", body: form });
  const data = await response.json();
  if (!response.ok || data.errcode) {
    throw new Error(`WeChat article image upload failed: ${JSON.stringify(data)}`);
  }
  if (!data.url) throw new Error(`No url in article image upload response: ${JSON.stringify(data)}`);
  return data.url;
}

export async function createDraft(accessToken, article, thumbMediaId) {
  if ([...config.wechatAuthor].length > 8) {
    throw new Error(`WECHAT_AUTHOR is too long for WeChat draft API: ${[...config.wechatAuthor].length}/8 characters`);
  }

  const draftArticle = {
    title: article.title,
    digest: article.digest,
    content: article.contentHtml,
    thumb_media_id: thumbMediaId,
    show_cover_pic: 0,
    need_open_comment: 0,
    only_fans_can_comment: 0
  };

  if (config.wechatAuthor) {
    draftArticle.author = config.wechatAuthor;
  }

  const payload = {
    articles: [draftArticle]
  };

  return await postJson(`https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${encodeURIComponent(accessToken)}`, payload);
}
