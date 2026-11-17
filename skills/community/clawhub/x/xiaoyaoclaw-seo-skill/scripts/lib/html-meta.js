'use strict';
/**
 * html-meta.js — 从首页 HTML 里静态提取 SEO 关键标签（纯函数、无网络）
 *
 * 只做静态解析：JS 注入的 JSON-LD / title 检测不到，需浏览器渲染复核
 * （见 references/schema.md）。
 */

/** 判断一段文本是不是 HTML（用于识别 robots.txt / sitemap.xml 的 HTML fallback） */
function looksLikeHtml(text) {
  const head = String(text || '').slice(0, 300).trim();
  return /^<!DOCTYPE|<html/i.test(head);
}

/** 提取 title / meta description / canonical / H1-H2 / viewport / lang / JSON-LD */
function extractMeta(html) {
  const out = {};
  const title = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  out.title = title ? title[1].trim().slice(0, 200) : null;
  const desc =
    html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([\s\S]*?)["']/i) ||
    html.match(/<meta[^>]+content=["']([\s\S]*?)["'][^>]+name=["']description["']/i);
  out.metaDesc = desc ? desc[1].trim().slice(0, 300) : null;
  const h1s = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)]
    .map((m) => m[1].replace(/<[^>]+>/g, '').trim())
    .filter(Boolean);
  out.h1Count = h1s.length;
  out.h1Samples = h1s.slice(0, 3);
  out.h2Count = (html.match(/<h2[^>]*>/gi) || []).length;
  const canon =
    html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([\s\S]*?)["']/i) ||
    html.match(/<link[^>]+href=["']([\s\S]*?)["'][^>]+rel=["']canonical["']/i);
  out.canonical = canon ? canon[1] : null;
  out.viewport = /name=["']viewport["']/i.test(html);
  out.lang = (html.match(/<html[^>]+lang=["']([\s\S]*?)["']/i) || [])[1] || null;
  const jsonld = [...html.matchAll(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
  out.jsonldCount = jsonld.length;
  out.jsonldTypes = [];
  for (const m of jsonld) {
    try {
      const j = JSON.parse(m[1]);
      const types = Array.isArray(j['@type']) ? j['@type'] : [j['@type']];
      out.jsonldTypes.push(...types.filter(Boolean));
    } catch {
      out.jsonldTypes.push('(parse error)');
    }
  }
  out.robotsMeta =
    (html.match(/<meta[^>]+name=["']robots["'][^>]+content=["']([\s\S]*?)["']/i) || [])[1] || null;
  return out;
}

module.exports = { looksLikeHtml, extractMeta };
