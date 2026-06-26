#!/usr/bin/env bun

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";

type Density = "minimal" | "balanced" | "rich";
type VisualConsistency = "standard" | "strong";
type InformationDensity = "medium" | "high";
type FinishLevel = "editorial" | "editorial-premium";
type ArticleType = "technical" | "business" | "lifestyle" | "general";

type Args = {
  articlePath: string;
  slug: string | null;
  density: Density | null;
  aspectRatio: string | null;
  promptProfile: string | null;
  textLanguage: string | null;
  englishTerms: string[];
  imageProvider: string | null;
  imageModel: string | null;
  imageBaseUrl: string | null;
  imageSize: string | null;
  configPath: string | null;
};

type VisualPreferences = {
  color_tendency: string;
  graphic_style: string;
  layout_mood: string;
  watermark: string;
};

type PlannerConfig = {
  density: Density;
  aspectRatio: string;
  upload: boolean;
  promptProfile: string;
  textLanguage: string;
  englishTermsWhitelist: string[];
  visualConsistency: VisualConsistency;
  informationDensity: InformationDensity;
  finishLevel: FinishLevel;
  imageProvider: string;
  imageModel: string;
  imageBaseUrl: string;
  imageSize: string;
  visualPreferences: VisualPreferences;
  filenamePrefix: string;
};

type Section = {
  title: string;
  level: 1 | 2 | 3;
  lines: string[];
  text: string;
};

type VisualBible = {
  articleType: ArticleType;
  visualTheme: string;
  colorSystem: string;
  graphicLanguage: string;
  layoutDiscipline: string;
  textPolicy: string;
  negativeRules: string[];
  qualityBaseline: string;
};

type ImagePlan = {
  index: number;
  title: string;
  imageType: string;
  position: string;
  purpose: string;
  coreMessage: string;
  contentBlocks: string[];
  textBlocks: string[];
  englishTermsUsed: string[];
  layoutHint: string;
  filename: string;
  altText: string;
  sectionText: string;
};

const DEFAULTS: PlannerConfig = {
  density: "balanced",
  aspectRatio: "16:9",
  upload: false,
  promptProfile: "nano-banana",
  textLanguage: "zh-CN",
  englishTermsWhitelist: [],
  visualConsistency: "strong",
  informationDensity: "high",
  finishLevel: "editorial-premium",
  imageProvider: "xiaomi",
  imageModel: "gemini-3.1-flash-image-preview",
  imageBaseUrl: "https://vip.123everything.com/v1beta",
  imageSize: "1K",
  visualPreferences: {
    color_tendency: "",
    graphic_style: "",
    layout_mood: "",
    watermark: "",
  },
  filenamePrefix: "",
};

function printHelp(): void {
  console.log(`
plan-illustrations.ts - Generate visual bible, outline, and prompts

Usage:
  bun run scripts/plan-illustrations.ts --article <article.md> [options]

Required:
  --article <path>                 Markdown article path

Options:
  --slug <value>                  Output slug
  --density <value>               minimal | balanced | rich
  --ar, --aspect-ratio <value>    Aspect ratio, default 16:9
  --prompt-profile <value>        Prompt profile, default nano-banana
  --text-language <value>         Default visible text language, default zh-CN
  --english-terms <csv>           Comma-separated English whitelist
  --term <value>                  Repeatable English whitelist term
  --image-provider <value>        Provider label, default gemini
  --image-model <value>           Model label for outline metadata
  --image-base-url <value>        Gemini relay base URL for outline metadata
  --image-size <value>            Image size/clarity label for outline metadata
  --config <path>                 Optional .zhy-illustrator.yml path

Outputs:
  - illustrations/<slug>/visual-bible.md
  - illustrations/<slug>/outline.md
  - illustrations/<slug>/prompts/*.md
`);
}

function parseArgs(): Args {
  const argv = process.argv.slice(2);
  if (argv.includes("--help") || argv.includes("-h")) {
    printHelp();
    process.exit(0);
  }

  let articlePath = "";
  let slug: string | null = null;
  let density: Density | null = null;
  let aspectRatio: string | null = null;
  let promptProfile: string | null = null;
  let textLanguage: string | null = null;
  const englishTerms: string[] = [];
  let imageProvider: string | null = null;
  let imageModel: string | null = null;
  let imageBaseUrl: string | null = null;
  let imageSize: string | null = null;
  let configPath: string | null = null;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case "--article":
        articlePath = argv[++i] ?? "";
        break;
      case "--slug":
        slug = argv[++i] ?? null;
        break;
      case "--density":
        density = (argv[++i] ?? "") as Density;
        break;
      case "--ar":
      case "--aspect-ratio":
        aspectRatio = argv[++i] ?? null;
        break;
      case "--prompt-profile":
        promptProfile = argv[++i] ?? null;
        break;
      case "--text-language":
        textLanguage = argv[++i] ?? null;
        break;
      case "--english-terms": {
        const raw = argv[++i] ?? "";
        for (const item of raw.split(",")) {
          const val = item.trim();
          if (val) englishTerms.push(val);
        }
        break;
      }
      case "--term": {
        const term = (argv[++i] ?? "").trim();
        if (term) englishTerms.push(term);
        break;
      }
      case "--image-provider":
        imageProvider = argv[++i] ?? null;
        break;
      case "--image-model":
        imageModel = argv[++i] ?? null;
        break;
      case "--image-base-url":
        imageBaseUrl = argv[++i] ?? null;
        break;
      case "--image-size":
        imageSize = argv[++i] ?? null;
        break;
      case "--config":
        configPath = argv[++i] ?? null;
        break;
    }
  }

  if (!articlePath) {
    console.error("错误：必须提供 --article <path>");
    process.exit(1);
  }

  return {
    articlePath,
    slug,
    density,
    aspectRatio,
    promptProfile,
    textLanguage,
    englishTerms,
    imageProvider,
    imageModel,
    imageBaseUrl,
    imageSize,
    configPath,
  };
}

function parseScalar(raw: string): string | boolean {
  const value = raw.trim().replace(/^['"]|['"]$/g, "");
  if (value === "true") return true;
  if (value === "false") return false;
  return value;
}

function parseConfigFile(filePath: string): Partial<PlannerConfig> {
  const text = readFileSync(filePath, "utf-8");
  const lines = text.split(/\r?\n/);
  const result: Partial<PlannerConfig> = {};
  let currentSection = "";

  for (const rawLine of lines) {
    if (!rawLine.trim() || rawLine.trim().startsWith("#")) continue;
    const indent = rawLine.match(/^\s*/)?.[0].length ?? 0;
    const line = rawLine.trim();

    if (indent === 0) {
      currentSection = "";
      const idx = line.indexOf(":");
      if (idx < 0) continue;
      const key = line.slice(0, idx).trim();
      const rest = line.slice(idx + 1).trim();
      if (!rest) {
        currentSection = key;
        if (key === "english_terms_whitelist") {
          result.englishTermsWhitelist = [];
        } else if (key === "visual_preferences") {
          result.visualPreferences = { ...DEFAULTS.visualPreferences };
        }
        continue;
      }

      const parsed = parseScalar(rest);
      switch (key) {
        case "density":
          result.density = parsed as Density;
          break;
        case "aspect_ratio":
          result.aspectRatio = String(parsed);
          break;
        case "upload":
          result.upload = Boolean(parsed);
          break;
        case "prompt_profile":
          result.promptProfile = String(parsed);
          break;
        case "text_language":
          result.textLanguage = String(parsed);
          break;
        case "visual_consistency":
          result.visualConsistency = parsed as VisualConsistency;
          break;
        case "information_density":
          result.informationDensity = parsed as InformationDensity;
          break;
        case "finish_level":
          result.finishLevel = parsed as FinishLevel;
          break;
        case "image_provider":
          result.imageProvider = String(parsed);
          break;
        case "image_model":
          result.imageModel = String(parsed);
          break;
        case "image_base_url":
          result.imageBaseUrl = String(parsed);
          break;
        case "image_size":
          result.imageSize = String(parsed);
          break;
        case "filename_prefix":
          result.filenamePrefix = String(parsed);
          break;
      }
      continue;
    }

    if (currentSection === "english_terms_whitelist" && line.startsWith("- ")) {
      if (!result.englishTermsWhitelist) result.englishTermsWhitelist = [];
      result.englishTermsWhitelist.push(line.slice(2).trim().replace(/^['"]|['"]$/g, ""));
      continue;
    }

    if (currentSection === "visual_preferences") {
      const idx = line.indexOf(":");
      if (idx < 0) continue;
      const key = line.slice(0, idx).trim();
      const value = String(parseScalar(line.slice(idx + 1)));
      if (!result.visualPreferences) result.visualPreferences = { ...DEFAULTS.visualPreferences };
      if (key in result.visualPreferences) {
        result.visualPreferences[key as keyof VisualPreferences] = value;
      }
    }
  }

  return result;
}

function findConfigFile(startDir: string): string | null {
  let current = resolve(startDir);
  while (true) {
    const candidate = join(current, ".zhy-illustrator.yml");
    if (existsSync(candidate)) return candidate;
    const parent = dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}

function mergeConfig(args: Args, fileConfig: Partial<PlannerConfig>): PlannerConfig {
  const merged: PlannerConfig = {
    ...DEFAULTS,
    ...fileConfig,
    visualPreferences: {
      ...DEFAULTS.visualPreferences,
      ...(fileConfig.visualPreferences ?? {}),
    },
    englishTermsWhitelist: dedupe([
      ...(fileConfig.englishTermsWhitelist ?? []),
      ...args.englishTerms,
    ]),
  };

  if (args.density) merged.density = args.density;
  if (args.aspectRatio) merged.aspectRatio = args.aspectRatio;
  if (args.promptProfile) merged.promptProfile = args.promptProfile;
  if (args.textLanguage) merged.textLanguage = args.textLanguage;
  if (args.imageProvider) merged.imageProvider = args.imageProvider;
  if (args.imageModel) merged.imageModel = args.imageModel;
  if (args.imageBaseUrl) merged.imageBaseUrl = args.imageBaseUrl;
  if (args.imageSize) merged.imageSize = args.imageSize;

  return merged;
}

function dedupe(items: string[]): string[] {
  const seen = new Set<string>();
  const result: string[] = [];
  for (const item of items) {
    const normalized = item.trim();
    if (!normalized) continue;
    const key = normalized.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(normalized);
  }
  return result;
}

function slugify(input: string): string {
  const ascii = input
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, " ")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
  return ascii;
}

function deriveSlug(articlePath: string, title: string, explicit: string | null): string {
  const direct = (explicit ?? "").trim();
  if (direct) return slugify(direct) || direct;

  const fromTitle = slugify(title);
  if (fromTitle) return fromTitle;

  const base = slugify(basename(articlePath, extname(articlePath)));
  if (base) return base;

  return "article-illustration";
}

function stripCodeBlocks(lines: string[]): string[] {
  const result: string[] = [];
  let inFence = false;
  for (const line of lines) {
    if (line.trim().startsWith("```")) {
      inFence = !inFence;
      continue;
    }
    if (!inFence) result.push(line);
  }
  return result;
}

function cleanMarkdown(text: string): string {
  return text
    .replace(/`[^`]*`/g, " ")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/^#+\s*/gm, "")
    .replace(/^>\s*/gm, "")
    .replace(/^[-*+]\s+/gm, "")
    .replace(/^\d+\.\s+/gm, "")
    .replace(/\|/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseArticle(markdown: string): { title: string; introText: string; sections: Section[] } {
  const rawLines = markdown.split(/\r?\n/);
  const lines = stripCodeBlocks(rawLines);
  let title = "未命名文章";
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("# ")) {
      title = trimmed.slice(2).trim();
      break;
    }
  }

  const sections: Section[] = [];
  let current: Section | null = null;
  const introLines: string[] = [];
  let seenH2 = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("## ")) {
      seenH2 = true;
      if (current) {
        current.text = cleanMarkdown(current.lines.join("\n"));
        sections.push(current);
      }
      current = { title: trimmed.slice(3).trim(), level: 2, lines: [], text: "" };
      continue;
    }

    if (trimmed.startsWith("### ") && current) {
      current.lines.push(line);
      continue;
    }

    if (!seenH2) {
      if (!trimmed.startsWith("# ")) introLines.push(line);
    } else if (current) {
      current.lines.push(line);
    }
  }

  if (current) {
    current.text = cleanMarkdown(current.lines.join("\n"));
    sections.push(current);
  }

  return { title, introText: cleanMarkdown(introLines.join("\n")), sections };
}

function sentenceSummary(text: string): string {
  const cleaned = cleanMarkdown(text);
  if (!cleaned) return "围绕本节核心观点组织视觉信息。";
  const parts = cleaned
    .split(/[。！？.!?]/)
    .map((item) => item.trim())
    .filter((item) => item.length >= 8);
  const summary = parts.slice(0, 2).join("；");
  return summary || cleaned.slice(0, 60);
}

function collectBullets(lines: string[]): string[] {
  const bullets: string[] = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (/^[-*+]\s+/.test(trimmed)) {
      bullets.push(cleanMarkdown(trimmed.replace(/^[-*+]\s+/, "")));
    }
  }
  return bullets.filter(Boolean).slice(0, 4);
}

function detectArticleType(title: string, allText: string): ArticleType {
  const content = `${title} ${allText}`.toLowerCase();
  const techKeywords = ["ai", "api", "sdk", "playwright", "react", "node", "python", "架构", "系统", "工程", "技术", "开发", "模型"];
  const businessKeywords = ["增长", "产品", "商业", "运营", "转化", "用户", "品牌", "roi", "营销", "策略", "管理"];
  const lifestyleKeywords = ["生活", "情绪", "关系", "成长", "时间", "习惯", "家庭", "焦虑", "自律", "治愈"];

  const score = (keywords: string[]) => keywords.reduce((acc, key) => (content.includes(key) ? acc + 1 : acc), 0);
  const tech = score(techKeywords);
  const business = score(businessKeywords);
  const lifestyle = score(lifestyleKeywords);

  if (tech >= business && tech >= lifestyle && tech > 0) return "technical";
  if (business >= tech && business >= lifestyle && business > 0) return "business";
  if (lifestyle >= tech && lifestyle >= business && lifestyle > 0) return "lifestyle";
  return "general";
}

function buildVisualBible(title: string, articleText: string, config: PlannerConfig): VisualBible {
  const articleType = detectArticleType(title, articleText);

  const presets: Record<ArticleType, Omit<VisualBible, "articleType" | "textPolicy">> = {
    technical: {
      visualTheme: "科技编辑视觉，理性清晰，信息模块化，带轻微未来感",
      colorSystem: "深蓝灰或浅雾白为背景，青蓝为主高亮，薄荷绿或冷白作辅助强调",
      graphicLanguage: "圆角卡片、细线连接、层级框图、局部发光或轻阴影，强调结构与秩序",
      layoutDiscipline: "高信息密度但留白克制，标题区明确，内容区分层，阅读动线清晰",
      negativeRules: [
        "不要低幼卡通",
        "不要装饰性图标堆砌",
        "不要过度霓虹赛博风",
        "不要无意义背景纹理",
      ],
      qualityBaseline: "高完成度编辑视觉，像专业技术专栏或专题页配图",
    },
    business: {
      visualTheme: "商业专题视觉，专业、清晰、可信，强调对比和结论",
      colorSystem: "米白或浅灰底，蓝灰主色，橙色或深红作为关键强调",
      graphicLanguage: "信息卡片、数据标签、整齐网格、少量图表元素，强调结论传达",
      layoutDiscipline: "结构规整，模块边界明确，结论与数据优先展示",
      negativeRules: [
        "不要像廉价PPT截图",
        "不要过度装饰",
        "不要空洞企业海报风",
        "不要颜色过杂",
      ],
      qualityBaseline: "高完成度编辑视觉，像商业媒体专题配图",
    },
    lifestyle: {
      visualTheme: "温暖叙事型编辑视觉，情绪细腻，画面自然，有杂志感",
      colorSystem: "暖米色、柔和橙粉、低饱和绿或棕作辅助色，整体自然柔和",
      graphicLanguage: "真实场景或克制插画感，轻纹理，柔和光感，信息元素适度嵌入",
      layoutDiscipline: "节奏舒缓，留白充分，重点区域明确，不堆砌说明文字",
      negativeRules: [
        "不要低幼治愈卡通",
        "不要网红海报式过度滤镜",
        "不要无意义可爱元素",
        "不要把整段文字塞进图里",
      ],
      qualityBaseline: "高完成度编辑视觉，像生活方式杂志专题配图",
    },
    general: {
      visualTheme: "现代编辑视觉，简洁、鲜明、层级分明，兼顾信息表达与完成度",
      colorSystem: "中性背景配稳定主色，辅以一组高对比强调色，整体干净克制",
      graphicLanguage: "模块化图形、清晰边界、轻质感，避免过度拟物或过度扁平",
      layoutDiscipline: "标题区、内容区、强调区分明，整体秩序感强",
      negativeRules: [
        "不要简单装饰图",
        "不要低信息密度草图",
        "不要风格杂糅",
        "不要英文乱码",
      ],
      qualityBaseline: "高完成度编辑视觉，像成熟内容平台的专题配图",
    },
  };

  const preset = presets[articleType];
  const preferenceNotes = [
    config.visualPreferences.color_tendency,
    config.visualPreferences.graphic_style,
    config.visualPreferences.layout_mood,
  ].filter(Boolean);

  return {
    articleType,
    visualTheme: preferenceNotes.length ? `${preset.visualTheme}；补充偏好：${preferenceNotes.join("；")}` : preset.visualTheme,
    colorSystem: config.visualPreferences.color_tendency || preset.colorSystem,
    graphicLanguage: config.visualPreferences.graphic_style || preset.graphicLanguage,
    layoutDiscipline: config.visualPreferences.layout_mood || preset.layoutDiscipline,
    textPolicy: `默认所有可见文字使用简体中文；仅以下术语允许保留英文：${config.englishTermsWhitelist.length ? config.englishTermsWhitelist.join("、") : "无白名单，除非确属专有名词"}`,
    negativeRules: [...preset.negativeRules, "不要简单画图", "不要无意义图标拼贴", "不要让同篇图片风格漂移"],
    qualityBaseline: `${preset.qualityBaseline}；统一要求：${config.finishLevel} / ${config.informationDensity} / ${config.visualConsistency}`,
  };
}

function inferImageType(title: string, text: string): string {
  const content = `${title} ${text}`.toLowerCase();
  if (/(对比|区别|vs|versus|比较|差异)/i.test(content)) return "对比图";
  if (/(步骤|流程|分阶段|如何|方法|路径|路线)/i.test(content)) return "流程图";
  if (/(架构|系统|框架|模块|分层|协议)/i.test(content)) return "架构图";
  if (/(数据|统计|增长|下降|比例|百分比|转化|roi|ctr)/i.test(content)) return "数据图";
  if (/(场景|故事|人物|情绪|体验|生活|夜晚|书桌)/i.test(content)) return "场景图";
  return "编辑专题视觉";
}

function layoutHintFor(type: string): string {
  switch (type) {
    case "对比图":
      return "左右双栏或上下双栏，逻辑对称，差异点用强调色突出";
    case "流程图":
      return "按阅读顺序排列步骤节点，箭头清晰，标题区单独留出空间";
    case "架构图":
      return "采用层级结构或模块矩阵，连接关系明确，底层与上层职责分区清晰";
    case "数据图":
      return "数字优先，关键结论居前，图表元素克制但准确";
    case "场景图":
      return "主场景突出，信息说明嵌入角落卡片，保持叙事氛围";
    default:
      return "标题区、内容区、强调区分明，整体像成熟专题页配图";
  }
}

function shortText(text: string, maxLen: number): string {
  const cleaned = cleanMarkdown(text).replace(/[：:]/g, " ").trim();
  return cleaned.length <= maxLen ? cleaned : `${cleaned.slice(0, maxLen - 1)}…`;
}

function normalizeChineseUiLabel(text: string): string {
  const cleaned = shortText(text, 12)
    .replace(/documentation/gi, "需求文档")
    .replace(/user stories/gi, "用户故事")
    .replace(/dashboard/gi, "数据看板")
    .replace(/powered by/gi, "由...驱动")
    .replace(/failed/gi, "失败")
    .replace(/skipped/gi, "跳过")
    .replace(/pass(ed)?/gi, "通过")
    .replace(/result feedback/gi, "结果反馈")
    .replace(/code generation/gi, "代码生成")
    .replace(/auto(mation)? verification/gi, "自动验证")
    .replace(/requirement input/gi, "需求输入")
    .replace(/\bui\b/gi, "界面")
    .trim();

  return cleaned;
}

function extractChineseKeyword(text: string): string {
  const cleaned = cleanMarkdown(text)
    .replace(/[A-Za-z0-9_./-]+/g, " ")
    .replace(/[，。！？、；：,.!?;:()（）【】\[\]"'“”‘’]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const segments = cleaned
    .split(" ")
    .map((item) => item.trim())
    .filter((item) => item.length >= 2 && item.length <= 8);

  return segments[0] ?? "配图";
}

function makeFilenameBase(title: string, imageType: string, summary: string): string {
  const normalizedTitle = title
    .replace(/^为什么它的/, "")
    .replace(/^为什么/, "")
    .replace(/^一条完整的/, "")
    .replace(/^如何/, "")
    .replace(/^什么是/, "")
    .replace(/[的了呢吗呀吧啊]$/g, "");

  const fromTitle = slugify(normalizedTitle);
  if (fromTitle && !/^\d+$/.test(fromTitle)) return fromTitle;

  const keyword = extractChineseKeyword(`${title} ${summary}`);
  const keywordSlug = slugify(keyword);
  if (keywordSlug && !/^\d+$/.test(keywordSlug)) {
    return `${slugify(imageType)}-${keywordSlug}`.replace(/^-|-$/g, "");
  }

  const summaryKeyword = extractChineseKeyword(summary);
  const summarySlug = slugify(summaryKeyword);
  if (summarySlug && !/^\d+$/.test(summarySlug)) {
    return `${slugify(imageType)}-${summarySlug}`.replace(/^-|-$/g, "");
  }

  const typeSlug = slugify(imageType);
  return typeSlug || "image";
}

function selectPlans(title: string, introText: string, sections: Section[], config: PlannerConfig): ImagePlan[] {
  const candidates: Array<{ title: string; text: string; lines: string[]; position: string }> = [];

  if (introText.length >= 80) {
    candidates.push({
      title: `${title} 导读`,
      text: introText,
      lines: introText.split(/\n/),
      position: "文章开头导语之后",
    });
  }

  for (const section of sections) {
    if (section.text.length < 30) continue;
    candidates.push({
      title: section.title,
      text: section.text,
      lines: section.lines,
      position: `章节《${section.title}》之后`,
    });
  }

  const limit = config.density === "minimal" ? 2 : config.density === "balanced" ? 6 : 9;
  const selected = candidates.slice(0, Math.max(1, Math.min(limit, candidates.length)));

  return selected.map((candidate, index) => {
    const imageType = inferImageType(candidate.title, candidate.text);
    const bullets = collectBullets(candidate.lines);
    const summary = sentenceSummary(candidate.text);
    const englishTermsUsed = config.englishTermsWhitelist.filter((term) => candidate.text.toLowerCase().includes(term.toLowerCase()) || candidate.title.toLowerCase().includes(term.toLowerCase()));

    const contentBlocks = dedupe([
      `核心表达：${summary}`,
      ...bullets.map((item) => `要点：${shortText(item, 28)}`),
      `画面类型：${imageType}`,
    ]).slice(0, 4);

    const textBlocks = dedupe([
      normalizeChineseUiLabel(candidate.title),
      normalizeChineseUiLabel(summary),
      ...(bullets.length > 0 ? bullets.slice(0, 2).map((item) => normalizeChineseUiLabel(shortText(item, 10))) : [normalizeChineseUiLabel(shortText(candidate.title.replace(/导读$/, "核心"), 8))]),
    ]).slice(0, 5);

    const baseSlug = makeFilenameBase(candidate.title, imageType, summary) || `${slugify(imageType)}-${index + 1}` || `image-${index + 1}`;
    const prefix = config.filenamePrefix ? `${slugify(config.filenamePrefix)}-` : "";
    const filename = `${String(index + 1).padStart(2, "0")}-${prefix}${baseSlug}.png`.replace(/-+/g, "-");

    return {
      index: index + 1,
      title: candidate.title,
      imageType,
      position: candidate.position,
      purpose: `帮助读者快速理解“${shortText(candidate.title, 18)}”这一节的关键信息，并提升阅读节奏与记忆点。`,
      coreMessage: summary,
      contentBlocks,
      textBlocks,
      englishTermsUsed,
      layoutHint: layoutHintFor(imageType),
      filename,
      altText: `${candidate.title}配图`,
      sectionText: candidate.text,
    };
  });
}

function renderVisualBible(articlePath: string, slug: string, title: string, config: PlannerConfig, bible: VisualBible): string {
  return `---
article: ${articlePath}
slug: ${slug}
prompt_profile: ${config.promptProfile}
text_language: ${config.textLanguage}
image_provider: ${config.imageProvider}
image_model: ${config.imageModel}
image_base_url: ${config.imageBaseUrl || ""}
image_size: ${config.imageSize || ""}
generated_at: ${new Date().toISOString()}
---

# Visual Bible

## 文章标题

${title}

## 质量基线

${bible.qualityBaseline}

## 视觉主题

${bible.visualTheme}

## 色彩系统

${bible.colorSystem}

## 图形语言

${bible.graphicLanguage}

## 版式纪律

${bible.layoutDiscipline}

## 文字策略

${bible.textPolicy}

## 负面规则

${bible.negativeRules.map((item) => `- ${item}`).join("\n")}
`;
}

function renderOutline(articlePath: string, slug: string, config: PlannerConfig, plans: ImagePlan[]): string {
  const sections = plans.map((plan) => `## Image ${plan.index}

- position: ${plan.position}
- title: ${plan.title}
- image_type: ${plan.imageType}
- purpose: ${plan.purpose}
- core_message: ${plan.coreMessage}
- layout_hint: ${plan.layoutHint}
- filename: ${plan.filename}
- alt_text: ${plan.altText}
- english_terms_used: ${plan.englishTermsUsed.length ? plan.englishTermsUsed.join(", ") : "无"}

### content_blocks

${plan.contentBlocks.map((item) => `- ${item}`).join("\n")}

### text_blocks

${plan.textBlocks.map((item) => `- ${item}`).join("\n")}
`).join("\n");

  return `---
article: ${articlePath}
slug: ${slug}
density: ${config.density}
aspect_ratio: ${config.aspectRatio}
prompt_profile: ${config.promptProfile}
text_language: ${config.textLanguage}
image_provider: ${config.imageProvider}
image_model: ${config.imageModel}
image_base_url: ${config.imageBaseUrl || ""}
image_size: ${config.imageSize || ""}
image_count: ${plans.length}
generated_at: ${new Date().toISOString()}
---

# Outline

${sections}`;
}

function renderPrompt(plan: ImagePlan, bible: VisualBible, config: PlannerConfig): string {
  const englishRule = plan.englishTermsUsed.length
    ? `仅以下术语允许保留英文：${plan.englishTermsUsed.join("、")}`
    : `默认不展示英文，除非必须保留专有名词。`;

  const chineseUiRule = plan.englishTermsUsed.length
    ? `除白名单术语外，其余界面词、按钮词、图表标签、状态文案全部改为简体中文。`
    : `所有界面词、按钮词、图表标签、状态文案全部使用简体中文。`;

  return `[任务定位]
这是一张可直接用于公众号正文的高完成度专题配图，不是简单插画，不是装饰图，不是随手流程图。

[统一风格锚点]
继承本篇文章的统一视觉基调：${bible.visualTheme}
主色系统：${bible.colorSystem}
图形语言：${bible.graphicLanguage}
版式纪律：${bible.layoutDiscipline}
质量基线：${bible.qualityBaseline}

[本图目标]
本图要传达的唯一核心信息：${plan.coreMessage}
图像类型：${plan.imageType}
插入位置：${plan.position}

[画面内容]
${plan.contentBlocks.map((item) => `- ${item}`).join("\n")}
- 结合本节内容补充必要的场景细节与信息模块，但不要偏离核心信息。

[布局结构]
- ${plan.layoutHint}
- 标题区、内容区、强调区必须分明。
- 阅读动线要自然，读者能一眼抓住主标题与关键结论。

[文字规则]
- 所有可见文字默认使用简体中文。
- ${englishRule}
- ${chineseUiRule}
- 需要显示的文字块如下：
${plan.textBlocks.map((item) => `  - ${item}`).join("\n")}
- 中文文字尽量短而准，避免长句，避免大段说明。
- 非白名单英文 UI 词必须翻译成中文，例如：Documentation -> 需求文档，User Stories -> 用户故事，Dashboard -> 看板，PASS -> 通过，Failed -> 失败，Skipped -> 跳过。
- 不要出现无关英文角标、英文占位符、英文导航、英文图表图例、英文说明性水印。

[质量要求]
- 高信息密度但不拥挤
- 视觉层级明确
- 细节丰富但不杂乱
- 成品感强，像成熟公众号专题视觉或编辑专栏配图
- 同一篇文章内的图片必须保持统一风格，不要风格漂移
- 如果是信息图 / 流程图 / 架构图，优先做中文信息图而不是英文软件界面截图风格
- 若展示工具或平台界面，只保留必要品牌名与白名单术语，其他界面文案全部中文化

[禁止项]
${bible.negativeRules.map((item) => `- ${item}`).join("\n")}
- 不要英文乱码
- 不要无意义图标堆砌
- 不要廉价PPT感
- 不要把整段正文直接做成图片文字
- 不要默认生成英文 UI 文案，如 Documentation、Dashboard、Powered by、User Stories
- 不要无关品牌 logo、浏览器 logo、英文状态字样，除非本图核心信息确实需要且属于白名单术语

[技术约束]
- 宽高比：${config.aspectRatio}
- prompt_profile：${config.promptProfile}
- text_language：${config.textLanguage}
- image_provider：${config.imageProvider}
- image_model：${config.imageModel}
- image_size：${config.imageSize || "default"}
`;
}

function main(): void {
  const args = parseArgs();
  const articlePath = resolve(args.articlePath);
  if (!existsSync(articlePath)) {
    console.error(`错误：文章不存在 ${articlePath}`);
    process.exit(1);
  }

  const articleDir = dirname(articlePath);
  const configPath = args.configPath ? resolve(args.configPath) : findConfigFile(articleDir);
  const fileConfig = configPath && existsSync(configPath) ? parseConfigFile(configPath) : {};
  const config = mergeConfig(args, fileConfig);

  const markdown = readFileSync(articlePath, "utf-8");
  const parsed = parseArticle(markdown);
  const slug = deriveSlug(articlePath, parsed.title, args.slug);
  const illustrationsDir = join(articleDir, "illustrations", slug);
  const promptsDir = join(illustrationsDir, "prompts");
  mkdirSync(promptsDir, { recursive: true });

  const articleText = [parsed.introText, ...parsed.sections.map((section) => section.text)].join("\n\n");
  const visualBible = buildVisualBible(parsed.title, articleText, config);
  const plans = selectPlans(parsed.title, parsed.introText, parsed.sections, config);

  if (plans.length === 0) {
    console.error("错误：未能从文章中提取足够内容来规划配图");
    process.exit(1);
  }

  const visualBiblePath = join(illustrationsDir, "visual-bible.md");
  const outlinePath = join(illustrationsDir, "outline.md");
  writeFileSync(visualBiblePath, renderVisualBible(articlePath, slug, parsed.title, config, visualBible), "utf-8");
  writeFileSync(outlinePath, renderOutline(articlePath, slug, config, plans), "utf-8");

  for (const plan of plans) {
    const promptPath = join(promptsDir, plan.filename.replace(/\.(png|jpg|jpeg|webp)$/i, ".prompt.md"));
    writeFileSync(promptPath, renderPrompt(plan, visualBible, config), "utf-8");
  }

  const result = {
    success: true,
    article_path: articlePath,
    config_path: configPath,
    slug,
    illustrations_dir: illustrationsDir,
    visual_bible_path: visualBiblePath,
    outline_path: outlinePath,
    prompt_count: plans.length,
    prompt_profile: config.promptProfile,
    image_provider: config.imageProvider,
    image_model: config.imageModel,
  };

  console.log(JSON.stringify(result, null, 2));
}

main();
