#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (!arg.startsWith("--")) {
      continue;
    }
    if (!next || next.startsWith("--")) {
      args[arg.slice(2)] = true;
    } else {
      args[arg.slice(2)] = next;
      i += 1;
    }
  }
  return args;
}

function getArg(args, ...names) {
  for (const name of names) {
    if (typeof args[name] !== "undefined") {
      return args[name];
    }
  }
  return undefined;
}

function cleanHtml(html) {
  return html.replace(/<script\b[\s\S]*?<\/script>/gi, "");
}

function extractStyleBlocks(html) {
  return [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)]
    .map((match) => match[1].trim())
    .filter(Boolean)
    .join("\n");
}

function extractArticleHtml(html) {
  const patterns = [
    /<div[^>]+id=["']js_content["'][^>]*>([\s\S]*?)<\/div>/i,
    /<section[^>]+id=["']js_content["'][^>]*>([\s\S]*?)<\/section>/i,
    /<div[^>]+class=["'][^"']*rich_media_content[^"']*["'][^>]*>([\s\S]*?)<\/div>/i,
    /<article[^>]*>([\s\S]*?)<\/article>/i,
    /<body[^>]*>([\s\S]*?)<\/body>/i
  ];

  for (const pattern of patterns) {
    const match = html.match(pattern);
    if (match?.[1]) {
      return match[1];
    }
  }
  return html;
}

function extractBlocks(html) {
  const blockPattern = /<(p|section|blockquote|h1|h2|h3|h4|h5|h6|ul|ol|pre|table|figure|div)[^>]*>[\s\S]*?<\/\1>/gi;
  const blocks = [];
  for (const match of html.matchAll(blockPattern)) {
    const block = match[0].trim();
    const textOnly = block.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
    if (textOnly) {
      blocks.push(block);
    }
  }
  return blocks;
}

function getAttributeStyle(htmlTag) {
  const match = htmlTag.match(/style=["']([^"']+)["']/i);
  return match?.[1]?.trim() || "";
}

function selectorRule(selector, style) {
  return style ? `${selector} { ${style} }\n` : "";
}

function extractStyleProfile(articleHtml, styleBlocks) {
  const titleTag = articleHtml.match(/<h1\b[^>]*>/i)?.[0] || "";
  const h2Tag = articleHtml.match(/<h2\b[^>]*>/i)?.[0] || "";
  const paragraphTag = articleHtml.match(/<p\b[^>]*>/i)?.[0] || "";
  const titleStyle = getAttributeStyle(titleTag);
  const h2Style = getAttributeStyle(h2Tag);
  const paragraphStyle = getAttributeStyle(paragraphTag);

  const extractedCss = [
    selectorRule(".wechat-content h1", titleStyle),
    selectorRule(".wechat-content h2", h2Style),
    selectorRule(".wechat-content p", paragraphStyle)
  ].join("");

  return {
    titleStyle,
    headingStyle: h2Style,
    paragraphStyle,
    customCss: [extractedCss.trim(), styleBlocks.trim()].filter(Boolean).join("\n")
  };
}

function findEdgeImage(blocks, side) {
  const windowBlocks = side === "start" ? blocks.slice(0, 5) : blocks.slice(Math.max(0, blocks.length - 5));
  for (const block of windowBlocks) {
    const match = block.match(/<img[^>]*src=["']([^"']+)["'][^>]*>/i);
    if (match?.[1]) {
      return {
        src: match[1],
        html: block
      };
    }
  }
  return null;
}

function wrapTemplate(name, blocks) {
  const klass = name === "intro" ? "wechat-intro" : "wechat-outro";
  return `<section class="${klass}">\n${blocks.join("\n")}\n</section>\n`;
}

async function loadHtml(args) {
  const input = getArg(args, "input", "html-file", "file");
  const url = getArg(args, "url", "article-url", "link");
  if (input) {
    return fs.readFile(path.resolve(input), "utf8");
  }
  if (url) {
    const response = await fetch(String(url));
    if (!response.ok) {
      throw new Error(`Fetch failed: ${response.status} ${response.statusText}`);
    }
    return response.text();
  }
  throw new Error("Provide --input <html-file> or --url <wechat-article-url>");
}

async function loadRegistry(registryPath) {
  if (!registryPath) {
    return { templates: {} };
  }
  try {
    const raw = await fs.readFile(path.resolve(registryPath), "utf8");
    const parsed = JSON.parse(raw);
    return parsed?.templates ? parsed : { templates: {} };
  } catch {
    return { templates: {} };
  }
}

async function saveRegistry(registryPath, registry) {
  if (!registryPath) {
    return;
  }
  await fs.writeFile(path.resolve(registryPath), JSON.stringify(registry, null, 2), "utf8");
}

async function main() {
  const args = parseArgs(process.argv);
  const mode = getArg(args, "extract-mode", "mode") || "heuristic";
  const introCount = Number(getArg(args, "intro-count", "header-blocks") || (mode === "ai" ? 5 : 3));
  const outroCount = Number(getArg(args, "outro-count", "footer-blocks") || (mode === "ai" ? 5 : 3));
  const rawHtml = await loadHtml(args);
  const cleanedHtml = cleanHtml(rawHtml);
  const styleBlocks = extractStyleBlocks(cleanedHtml);
  const articleHtml = extractArticleHtml(cleanedHtml);
  const blocks = extractBlocks(articleHtml);

  if (blocks.length === 0) {
    throw new Error("No article blocks found");
  }

  const introBlocks = blocks.slice(0, introCount);
  const outroBlocks = blocks.slice(Math.max(0, blocks.length - outroCount));
  const introHtml = wrapTemplate("intro", introBlocks);
  const outroHtml = wrapTemplate("outro", outroBlocks);
  const styleProfile = extractStyleProfile(articleHtml, styleBlocks);
  const headerImage = findEdgeImage(blocks, "start");
  const footerImage = findEdgeImage(blocks, "end");
  const styleOutput = styleProfile.customCss || "";

  const introOutput = getArg(args, "intro-output", "header-template-output");
  const outroOutput = getArg(args, "outro-output", "footer-template-output");
  const styleOutputPath = getArg(args, "style-output", "css-output", "layout-style-output");
  const registryPath = getArg(args, "registry", "template-registry");
  const templateName = getArg(args, "name", "template-name", "save-name");
  const analysisOutput = getArg(args, "analysis-output", "ai-analysis-output");

  if (introOutput) {
    await fs.writeFile(path.resolve(introOutput), introHtml, "utf8");
  } else {
    process.stdout.write(introHtml);
  }

  if (outroOutput) {
    await fs.writeFile(path.resolve(outroOutput), outroHtml, "utf8");
  } else {
    process.stdout.write(`\n${outroHtml}`);
  }

  if (styleOutputPath) {
    await fs.writeFile(path.resolve(styleOutputPath), styleOutput, "utf8");
  }

  const analysis = {
    mode,
    source: getArg(args, "url", "article-url", "link") || getArg(args, "input", "html-file", "file") || "",
    introCandidateBlocks: blocks.slice(0, Math.min(8, blocks.length)),
    outroCandidateBlocks: blocks.slice(Math.max(0, blocks.length - 8)),
    styleProfile,
    headerImage,
    footerImage
  };

  if (analysisOutput) {
    await fs.writeFile(path.resolve(analysisOutput), JSON.stringify(analysis, null, 2), "utf8");
  }

  if (templateName) {
    const registry = await loadRegistry(registryPath);
    registry.templates[templateName] = {
      name: templateName,
      importedAt: new Date().toISOString(),
      source: analysis.source,
      introHtml,
      outroHtml,
      customCss: styleOutput,
      titleStyle: styleProfile.titleStyle,
      headingStyle: styleProfile.headingStyle,
      paragraphStyle: styleProfile.paragraphStyle,
      headerImage,
      footerImage,
      extractionMode: mode,
      analysis
    };
    await saveRegistry(registryPath, registry);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
