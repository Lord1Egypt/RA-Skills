#!/usr/bin/env node
/**
 * WeChat Article Parser → Clean Markdown for Obsidian
 *
 * Usage: node parse.mjs <html_file> [--json]
 *   --json  Output metadata as JSON instead of Markdown
 *
 * Output: Clean Markdown with images, merged PART headings,
 *         promotional tail stripped, and WeChat decoration removed.
 */

import { readFileSync } from "fs";

const htmlFile = process.argv[2];
const jsonMode = process.argv.includes("--json");

if (!htmlFile) {
  console.error("Usage: node parse.mjs <html_file> [--json]");
  process.exit(1);
}

const html = readFileSync(htmlFile, "utf-8");

// --- Metadata extraction ---

function extractMeta(html) {
  const get = (pattern) => {
    const m = html.match(pattern);
    return m ? m[1].trim() : "";
  };

  const title =
    get(/var msg_title = '([^']*)'/) ||
    get(/<h1[^>]*class="rich_media_title[^"]*"[^>]*>([\s\S]*?)<\/h1/) ||
    "";
  const cleanTitle = title.replace(/<[^>]+>/g, "").trim();

  const author =
    get(/var nickname = htmlDecode\('(.*?)'\)/) ||
    get(/var nickname = "(.*?)"/) ||
    get(/id="js_name"[^>]*>([\s\S]*?)<\//) ||
    "";

  const ctStr = get(/var ct = "(\d+)"/) || get(/var create_time = "(\d+)"/);
  let publishDate = "";
  if (ctStr) {
    const d = new Date(parseInt(ctStr) * 1000);
    const bj = new Date(d.getTime() + 8 * 3600 * 1000);
    publishDate = bj.toISOString().replace("T", " ").replace(/\.\d+Z$/, "");
  }
  if (!publishDate) {
    publishDate =
      get(/<div[^>]*id="publish_time"[^>]*>([\s\S]*?)<\//) ||
      get(/<span[^>]*id="publish_time"[^>]*>([\s\S]*?)<\//) ||
      "";
    publishDate = publishDate.replace(/<[^>]+>/g, "").trim();
  }

  const desc = get(/var msg_desc = htmlDecode\("([\s\S]*?)"\)/) || "";
  const sourceUrl = get(/var msg_link = "(.*?)"/) || "";

  return { title: cleanTitle, author, publishDate, description: desc, sourceUrl };
}

// --- Content extraction ---

function extractContent(html) {
  const startIdx = html.indexOf('id="js_content"');
  if (startIdx === -1) return "";

  const tagEnd = html.indexOf(">", startIdx);
  if (tagEnd === -1) return "";

  let depth = 1;
  let i = tagEnd + 1;
  while (i < html.length && depth > 0) {
    if (html[i] === "<") {
      if (html.substring(i, i + 4) === "<div") {
        depth++;
      } else if (html.substring(i, i + 6) === "</div>") {
        depth--;
        if (depth === 0) break;
      }
    }
    i++;
  }

  const contentHtml = html.substring(tagEnd + 1, i);
  return htmlToMarkdown(contentHtml);
}

function htmlToMarkdown(html) {
  let md = html;

  // Remove script/style tags
  md = md.replace(/<script[\s\S]*?<\/script>/gi, "");
  md = md.replace(/<style[\s\S]*?<\/style>/gi, "");

  // Images: prefer data-src (WeChat lazy-load), fallback to src
  md = md.replace(/<img[^>]*?(?:data-src|src)="([^"]*)"[^>]*>/gi, (match, src) => {
    const dataSrc = match.match(/data-src="([^"]*)"/);
    const actualSrc = dataSrc ? dataSrc[1] : src;
    if (!actualSrc || actualSrc.startsWith("data:")) return "";
    return `\n![](${actualSrc})\n`;
  });

  // Headings
  md = md.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, (_, c) => `\n# ${stripTags(c).trim()}\n\n`);
  md = md.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, (_, c) => `\n## ${stripTags(c).trim()}\n\n`);
  md = md.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, (_, c) => `\n### ${stripTags(c).trim()}\n\n`);
  md = md.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, (_, c) => `\n#### ${stripTags(c).trim()}\n\n`);

  // Bold
  md = md.replace(/<(?:strong|b)(?:\s[^>]*)?>([\s\S]*?)<\/(?:strong|b)>/gi, (_, c) => {
    const text = stripTags(c).trim();
    return text ? `**${text}**` : "";
  });

  // Italic
  md = md.replace(/<(?:em|i)(?:\s[^>]*)?>([\s\S]*?)<\/(?:em|i)>/gi, (_, c) => {
    const text = stripTags(c).trim();
    return text ? `*${text}*` : "";
  });

  // Code blocks
  md = md.replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, (_, c) => {
    const code = stripTags(c).trim();
    return `\n\`\`\`\n${code}\n\`\`\`\n\n`;
  });

  // Inline code
  md = md.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, (_, c) => `\`${stripTags(c)}\``);

  // Links
  md = md.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, (_, href, text) => {
    if (!href || href.startsWith("javascript:")) return stripTags(text);
    return `[${stripTags(text).trim()}](${href})`;
  });

  // Blockquote
  md = md.replace(/<blockquote[^>]*>([\s\S]*?)<\/blockquote>/gi, (_, c) => {
    const text = stripTags(c).trim();
    return `\n> ${text.replace(/\n/g, "\n> ")}\n\n`;
  });

  // List items
  md = md.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, (_, c) => `- ${stripTags(c).trim()}\n`);

  // BR
  md = md.replace(/<br\s*\/?>/gi, "\n");

  // Paragraphs and sections
  md = md.replace(/<\/(?:p|section|div)>/gi, "\n\n");

  // HR
  md = md.replace(/<hr[^>]*>/gi, "\n---\n\n");

  // Strip remaining tags
  md = stripTags(md);

  // Clean up entities
  md = md.replace(/&nbsp;/g, " ");
  md = md.replace(/&lt;/g, "<");
  md = md.replace(/&gt;/g, ">");
  md = md.replace(/&amp;/g, "&");
  md = md.replace(/&quot;/g, '"');
  md = md.replace(/&#39;/g, "'");

  // --- Post-processing: clean WeChat decoration ---

  // Remove standalone THUMB / STOPPING lines (WeChat CSS decoration text)
  md = md.replace(/^\s*THUMB\s*$/gm, "");
  md = md.replace(/^\s*STOPPING\s*$/gm, "");

  // Merge "PART.XX\n\nTitle" into "## PART.XX Title"
  md = md.replace(/\n*PART\.(\d+)\s*\n+([^\n]+)/g, (_, num, title) => {
    return `\n## PART.${num} ${title.trim()}`;
  });

  // Strip promotional tail: everything after common ending patterns
  const tailPatterns = [
    /\n\s*感谢[您你]的[观阅]看[\s\S]*$/,
    /\n\s*(?:求各位|喜欢的话|觉得不错).{0,20}(?:点赞|关注|在看|转发|三连)[\s\S]*$/,
    /\n\s*PS[：:]?\s*欢迎加我[\s\S]*$/,
    /\n\s*PS[：:]?\s*公众号后台回复[\s\S]*$/,
  ];
  for (const pattern of tailPatterns) {
    md = md.replace(pattern, "");
  }

  // Clean up whitespace
  md = md.replace(/[ \t]+\n/g, "\n");
  md = md.replace(/\n{3,}/g, "\n\n");
  md = md.trim();

  return md;
}

function stripTags(html) {
  return html.replace(/<[^>]+>/g, "");
}

// --- Main ---

const meta = extractMeta(html);
const content = extractContent(html);

if (jsonMode) {
  console.log(JSON.stringify({ ...meta, contentLength: content.length }, null, 2));
} else {
  const lines = [
    "---",
    `title: "${meta.title.replace(/"/g, '\\"')}"`,
    `author: "${meta.author}"`,
    `publish_date: "${meta.publishDate}"`,
    `saved_date: "${new Date().toISOString().split("T")[0]}"`,
    `source: "wechat"`,
    meta.sourceUrl ? `url: "${meta.sourceUrl}"` : null,
    "---",
    "",
    `# ${meta.title}`,
    "",
    content,
    "",
  ].filter(Boolean);
  console.log(lines.join("\n"));
}
