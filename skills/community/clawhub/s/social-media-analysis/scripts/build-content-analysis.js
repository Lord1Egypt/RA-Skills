#!/usr/bin/env node
/**
 * 内容解析生成器（统一版）
 *
 * 目标：
 * 1) 保证每条记录都有“内容解析”
 * 2) 优先输出与品牌相关且有证据的信息
 * 3) 严格控制在 100 字以内
 *
 * 用法：
 * node build-content-analysis.js \
 *   --title "标题" \
 *   --text "正文" \
 *   --platform "微博" \
 *   --media-type "视频" \
 *   --visual "画面中出现小米手机开箱，桌面有小爱音箱"
 *
 * 输出：
 * {
 *   "analysis": "100字以内内容解析",
 *   "evidence": { ... },
 *   "score": 0.86
 * }
 */

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const cur = argv[i];
    if (!cur.startsWith("--")) continue;
    const key = cur.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      args[key] = next;
      i++;
    } else {
      args[key] = "true";
    }
  }
  return args;
}

function normalizeText(input) {
  return String(input || "")
    .replace(/<[^>]*>/g, " ")
    .replace(/https?:\/\/\S+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function splitSentences(text) {
  return normalizeText(text)
    .split(/[。！？!?；;\n]/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function truncateByChars(text, maxChars) {
  const src = String(text || "");
  if (src.length <= maxChars) return src;
  return `${src.slice(0, maxChars - 1)}…`;
}

function pickTopSentence(sentences, keywords) {
  if (!sentences.length) return "";
  let best = sentences[0];
  let bestScore = -1;

  for (const s of sentences) {
    let score = 0;
    const lower = s.toLowerCase();
    for (const kw of keywords) {
      if (lower.includes(kw.toLowerCase())) score += 2;
    }
    if (s.length >= 12 && s.length <= 60) score += 1;
    if (/[发布|体验|测评|开箱|对比|评测|升级|更新|功能]/.test(s)) score += 1;
    if (score > bestScore) {
      bestScore = score;
      best = s;
    }
  }
  return best;
}

function buildAnalysis({
  title,
  text,
  platform,
  mediaType,
  visual,
  maxChars = 100,
}) {
  const BRAND_KWS = ["小米", "小爱", "小爱同学", "Xiaomi", "Mi", "Redmi"];
  const titleText = normalizeText(title);
  const bodyText = normalizeText(text);
  const visualText = normalizeText(visual);
  const sents = splitSentences(`${titleText}。${bodyText}`);

  const core = pickTopSentence(sents, BRAND_KWS) || titleText || bodyText;
  const visualCore = pickTopSentence(splitSentences(visualText), BRAND_KWS);

  const hasBrand =
    BRAND_KWS.some((kw) => titleText.includes(kw) || bodyText.includes(kw) || visualText.includes(kw));
  const hasVisual = visualText.length > 0;

  let analysis = "";
  if (hasBrand) {
    analysis = `该内容与小米/小爱相关，核心信息：${core}`;
    if (hasVisual) {
      analysis += `；画面显示：${visualCore || truncateByChars(visualText, 28)}`;
    }
  } else if (hasVisual) {
    analysis = `该内容未明显提及小米/小爱，核心信息：${core || "文本信息有限"}；画面显示：${visualCore || truncateByChars(visualText, 28)}`;
  } else {
    analysis = `该内容核心信息：${core || "文本信息有限，建议补充原文或媒体素材后复核"}`;
  }

  const evidence = {
    title_used: !!titleText,
    text_used: !!bodyText,
    visual_used: !!visualText,
    brand_related: hasBrand,
    platform: normalizeText(platform) || "未知平台",
    media_type: normalizeText(mediaType) || "未知",
  };

  // 评分用于判定“准确性风险”，可在批处理时做复核阈值
  let score = 0.4;
  if (evidence.title_used) score += 0.2;
  if (evidence.text_used) score += 0.2;
  if (evidence.visual_used) score += 0.1;
  if (evidence.brand_related) score += 0.1;
  if (score > 0.98) score = 0.98;

  return {
    analysis: truncateByChars(analysis, maxChars),
    evidence,
    score: Number(score.toFixed(2)),
  };
}

function main() {
  const args = parseArgs(process.argv);
  const maxChars = Number(args["max-chars"] || 100);
  const result = buildAnalysis({
    title: args.title || "",
    text: args.text || "",
    platform: args.platform || "",
    mediaType: args["media-type"] || "",
    visual: args.visual || "",
    maxChars: Number.isFinite(maxChars) ? maxChars : 100,
  });
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (require.main === module) {
  main();
}

module.exports = {
  buildAnalysis,
  normalizeText,
  splitSentences,
};

