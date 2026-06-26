#!/usr/bin/env node

/**
 * Markdown to WeChat-compatible HTML converter
 *
 * Usage:
 *   npx -y tsx scripts/markdown-to-html.ts --input "article.md"
 *   npx -y tsx scripts/markdown-to-html.ts --input "article.md" --output "article.html"
 *   npx -y tsx scripts/markdown-to-html.ts --input "article.md" --css "templates/wechat-theme.css"
 *
 * Output: writes .html file, prints JSON manifest to stdout
 *   { htmlPath, title, contentImages: [{ placeholder, localPath, originalSrc }] }
 *
 * Dependencies: marked, juice (npm install)
 */

import { readFile, writeFile } from 'fs/promises';
import { existsSync } from 'fs';
import path from 'path';
import { execSync } from 'child_process';

// ── Arg parsing ──────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const opts: Record<string, string> = {
    css: path.resolve(__dirname, '../templates/wechat-theme.css'),
  };
  for (let i = 0; i < args.length; i++) {
    const key = args[i].replace(/^--/, '');
    if (args[i].startsWith('--') && args[i + 1] && !args[i + 1].startsWith('--')) {
      opts[key] = args[++i];
    }
  }
  return opts;
}

// ── Frontmatter parser ───────────────────────────────────────────────────────

function parseFrontmatter(content: string): { meta: Record<string, string>; body: string } {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { meta: {}, body: content };
  const meta: Record<string, string> = {};
  for (const line of match[1].split('\n')) {
    const [k, ...v] = line.split(':');
    if (k && v.length) meta[k.trim()] = v.join(':').trim();
  }
  return { meta, body: match[2] };
}

// ── Image placeholder extraction ─────────────────────────────────────────────

interface ContentImage {
  placeholder: string;
  localPath: string;
  originalSrc: string;
}

function extractImages(
  html: string,
  baseDir: string
): { html: string; images: ContentImage[] } {
  const images: ContentImage[] = [];
  let idx = 0;

  // Replace <img src="..."> with data-local-path for local files
  const result = html.replace(/<img([^>]*?)src="([^"]*)"([^>]*?)>/g, (match, pre, src, post) => {
    // Skip remote URLs — leave as-is
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:')) {
      return match;
    }
    idx++;
    const placeholder = `MDTOHTMLIMGPH_${idx}`;
    const localPath = path.resolve(baseDir, src);
    images.push({ placeholder, localPath, originalSrc: src });
    // Keep src, add data-local-path so post-to-wechat.ts can find the file
    return `<img${pre}src="${src}" data-local-path="${localPath}"${post}>`;
  });

  return { html: result, images };
}

// ── HTML wrapper ─────────────────────────────────────────────────────────────

function wrapHtml(title: string, bodyHtml: string, css: string): string {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(title)}</title>
<style>
${css}
</style>
</head>
<body>
<div id="output">
${bodyHtml}
</div>
</body>
</html>`;
}

function escapeHtml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const opts = parseArgs();

  if (!opts.input) {
    console.error('Usage: npx -y tsx scripts/markdown-to-html.ts --input "article.md"');
    process.exit(1);
  }

  const inputPath = path.resolve(opts.input);
  if (!existsSync(inputPath)) {
    console.error(`File not found: ${inputPath}`);
    process.exit(1);
  }

  const baseDir = path.dirname(inputPath);
  const rawContent = await readFile(inputPath, 'utf-8');
  const { meta, body } = parseFrontmatter(rawContent);
  const title = meta.title || path.basename(inputPath, '.md');

  // Dynamic import — auto-install if missing
  let marked: any, juice: any;
  try {
    ({ marked } = await import('marked'));
    juice = (await import('juice')).default;
  } catch {
    console.error('依赖未安装，正在自动安装 marked + juice...');
    const pkgDir = path.resolve(__dirname, '..');
    execSync('npm install', { cwd: pkgDir, stdio: 'inherit' });
    ({ marked } = await import('marked'));
    juice = (await import('juice')).default;
  }

  // Configure marked
  marked.setOptions({ gfm: true, breaks: false });

  // Convert markdown → HTML
  const rawHtml = await marked.parse(body);

  // Load CSS
  const cssPath = path.resolve(opts.css);
  const css = existsSync(cssPath) ? await readFile(cssPath, 'utf-8') : '';

  // Extract local images and add data-local-path attributes
  const { html: htmlWithAttrs, images } = extractImages(rawHtml, baseDir);

  // Wrap in full HTML doc
  const fullHtml = wrapHtml(title, htmlWithAttrs, css);

  // Inline CSS (WeChat strips <style> tags, all CSS must be in style="")
  const inlinedHtml = juice(fullHtml);

  // Write output
  const outputPath = opts.output
    ? path.resolve(opts.output)
    : path.join(baseDir, path.basename(inputPath, '.md') + '.html');

  await writeFile(outputPath, inlinedHtml, 'utf-8');

  // Print JSON manifest to stdout
  const manifest = {
    title,
    author: meta.author || '',
    summary: meta.description || meta.summary || '',
    htmlPath: outputPath,
    contentImages: images,
  };
  console.log(JSON.stringify(manifest, null, 2));
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
