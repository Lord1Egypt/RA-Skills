import fs from "node:fs";
import { resolveProjectPath } from "./config.mjs";

function htmlLength(html) {
  return Buffer.byteLength(String(html || ""), "utf8");
}

function validateLocalImagePath(errors, fieldName, filePath) {
  if (!filePath || typeof filePath !== "string") {
    errors.push(`${fieldName} must be a string path`);
    return;
  }
  const absPath = resolveProjectPath(filePath);
  if (!fs.existsSync(absPath)) {
    errors.push(`${fieldName} not found: ${filePath}`);
  }
  if (!/\.(png|jpe?g)$/i.test(filePath)) {
    errors.push(`${fieldName} must be a PNG or JPG image: ${filePath}`);
  }
}

export function validateGeneratedArticle(article) {
  const errors = [];
  if (!article || typeof article !== "object") errors.push("article must be an object");
  if (!article?.sourceId) errors.push("sourceId is required");
  if (!article?.title) errors.push("title is required");
  if (!article?.digest) errors.push("digest is required");
  if (!article?.contentHtml) errors.push("contentHtml is required");
  if (String(article?.author || "").includes("AIHOT")) errors.push("author must not contain internal source labels");
  if (String(article?.contentHtml || "").includes("AIHOT 自动精选")) errors.push("contentHtml must not contain internal source labels");
  if (/个人观点\s*仅供参考/.test(article?.contentHtml || "")) errors.push("contentHtml must not include 个人观点 仅供参考");
  if (/来源[:：]/.test(article?.contentHtml || "")) errors.push("contentHtml must not include 来源");
  if (/原文链接[:：]/.test(article?.contentHtml || "")) errors.push("contentHtml must not include 原文链接");
  if (/参考链接/.test(article?.contentHtml || "")) errors.push("contentHtml must not include 参考链接");
  if (String(article?.title || "").length > 64) errors.push("title should be <= 64 characters");
  if (String(article?.digest || "").length > 120) errors.push("digest should be <= 120 characters");
  if (htmlLength(article?.contentHtml) > 900 * 1024) errors.push("contentHtml should be below 900KB");
  if (/<script[\s>]/i.test(article?.contentHtml || "")) errors.push("script tags are not allowed");
  if (/<img[^>]+src=['"]https?:\/\//i.test(article?.contentHtml || "")) {
    errors.push("external img tags are not allowed; upload images to WeChat first");
  }
  if (article?.coverImagePath) {
    validateLocalImagePath(errors, "coverImagePath", article.coverImagePath);
  }
  if (article?.inlineImages !== undefined) {
    if (!Array.isArray(article.inlineImages)) {
      errors.push("inlineImages must be an array");
    } else {
      const placeholders = new Set();
      for (const [index, image] of article.inlineImages.entries()) {
        const prefix = `inlineImages[${index}]`;
        if (!image || typeof image !== "object") {
          errors.push(`${prefix} must be an object`);
          continue;
        }
        if (!image.placeholder || typeof image.placeholder !== "string") {
          errors.push(`${prefix}.placeholder is required`);
        } else {
          if (placeholders.has(image.placeholder)) errors.push(`${prefix}.placeholder is duplicated`);
          placeholders.add(image.placeholder);
          if (!String(article?.contentHtml || "").includes(image.placeholder)) {
            errors.push(`${prefix}.placeholder is not present in contentHtml`);
          }
        }
        validateLocalImagePath(errors, `${prefix}.path`, image.path);
      }
    }
  }
  return errors;
}
