import fs from "node:fs/promises";
import path from "node:path";
import { DEFAULT_REFLECTION_DIR, reflectionFilePath, slugify } from "./book-utils.mjs";

const DEFAULT_OUTPUT_DIR = "output/obsidian";

function parseArgs(argv) {
  const args = {
    shelf: "",
    book: "",
    outputDir: DEFAULT_OUTPUT_DIR,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--shelf") args.shelf = argv[index + 1];
    if (token === "--book") args.book = argv[index + 1];
    if (token === "--output-dir") args.outputDir = argv[index + 1];
  }

  if (!args.shelf && !args.book) {
    throw new Error("Provide at least one of --shelf or --book");
  }

  return args;
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function writeFile(filePath, content) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, "utf8");
}

async function readJsonIfExists(filePath, fallback = null) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    if (error?.code === "ENOENT") {
      return fallback;
    }
    throw error;
  }
}

function fenceYaml(value) {
  return `---\n${value}\n---\n`;
}

function cleanLine(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

function uniqueLines(values, limit = 20) {
  const result = [];
  const seen = new Set();

  for (const value of values || []) {
    const cleaned = cleanLine(value);
    if (!cleaned) continue;
    if (seen.has(cleaned)) continue;
    seen.add(cleaned);
    result.push(cleaned);
    if (result.length >= limit) break;
  }

  return result;
}

function shorten(value, max = 220) {
  const cleaned = cleanLine(value);
  if (cleaned.length <= max) return cleaned;
  return `${cleaned.slice(0, max - 1)}…`;
}

function normalizeSnippet(value) {
  return cleanLine(value)
    .replace(/^[,，。；:：、■\-\s]+/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function stripChapterPrefix(value) {
  return normalizeSnippet(value)
    .replace(/^\d+(?:\.\d+)+\s*/, "")
    .replace(/^第[一二三四五六七八九十百零两0-9]+[章节卷篇部]\s*/, "")
    .replace(/^[上中下]篇\s*/, "")
    .trim();
}

function extractPhraseCandidates(value, { title = "" } = {}) {
  const cleaned = stripChapterPrefix(value).replace(title, "").trim();
  if (!cleaned) return [];

  const candidates = [];
  const push = (item) => {
    const normalized = normalizeSnippet(item);
    if (!normalized) return;
    if (normalized.length < 2 || normalized.length > 18) return;
    if (/已读到|条笔记|时长|公开发|赞 评论|点评此书|推荐一般/.test(normalized)) return;
    if (!candidates.includes(normalized)) candidates.push(normalized);
  };

  if (cleaned.includes("趋势") && cleaned.includes("盘整")) push("趋势与盘整");
  if (cleaned.includes("级别") && cleaned.includes("判断")) push("同级别判断");
  if (cleaned.includes("假设条件")) push("假设条件");
  if (cleaned.includes("中枢")) push("中枢");
  if (cleaned.includes("背驰")) push("背驰");
  if (cleaned.includes("买卖点")) push("买卖点");
  if (cleaned.includes("陷阱式") || cleaned.includes("反转式") || cleaned.includes("中继式")) push("模式分类");

  for (const segment of cleaned.split(/[，。；：！？,.!?\n■]/)) {
    const part = normalizeSnippet(segment);
    if (!part) continue;

    const directMatches = part.match(/[\u4e00-\u9fa5]{3,12}/g) || [];
    directMatches.forEach(push);

    const howMatch = part.match(/如何([\u4e00-\u9fa5]{2,10})/);
    if (howMatch) push(howMatch[1]);

    const judgmentMatch = part.match(/([\u4e00-\u9fa5]{2,8})判断/);
    if (judgmentMatch) push(`${judgmentMatch[1]}判断`);
  }

  return candidates;
}

function pickIdeaLabel(value, { title = "", max = 16, fallback = "核心观点" } = {}) {
  const cleaned = stripChapterPrefix(value).replace(title, "").trim();
  if (!cleaned) return fallback;

  const phraseCandidates = extractPhraseCandidates(cleaned, { title }).filter((part) => part.length >= 3);
  const parts = [
    ...phraseCandidates,
    ...cleaned
      .split(/[，。；：！？,.!?:]/)
      .map((part) => normalizeSnippet(part))
      .filter(Boolean)
      .filter((part) => part.length >= 3 && part.length <= 24)
      .filter((part) => !/已读到|条笔记|时长|公开发|赞 评论|点评此书|推荐一般/.test(part)),
  ];

  const best = parts.find((part) => part.length >= 4 && part.length <= max) || parts[0] || cleaned;
  const normalized = normalizeSnippet(best).replace(/^[的地得]/, "");

  if (!normalized) return fallback;
  if (normalized.length <= max) return normalized;
  return shorten(normalized, max);
}

function parseReadingStats(book) {
  const source = [book.metadata?.intro, ...(book.notes || [])].map(cleanLine).join(" ");
  const progress = source.match(/已读到\s*([0-9]{1,3}%)/)?.[1] || "";
  const noteCount = source.match(/共\s*([0-9]+)\s*条笔记/)?.[1] || "";
  const duration = source.match(/时长\s*([0-9天小时分钟]+)/)?.[1] || "";

  return {
    progress,
    noteCount,
    duration,
  };
}

function renderBulletList(items, emptyText) {
  if (!items.length) {
    return [`- ${emptyText}`];
  }

  return items.map((item) => `- ${item}`);
}

function renderQuoteSections(items, headingPrefix) {
  if (!items.length) {
    return ["暂无可展示内容。"];
  }

  const lines = [];
  items.forEach((item, index) => {
    lines.push(`### ${headingPrefix} ${index + 1}`);
    lines.push("");
    lines.push(`> ${item}`);
    lines.push("");
  });
  return lines;
}

function pickCurrentChapter(book) {
  const pools = [
    ...(book.notes || []),
    ...(book.content?.blocks || []),
    ...(book.page?.headings || []),
    ...(book.toc || []).map((item) => item.title),
  ].map(cleanLine);

  const patterns = [
    /第[一二三四五六七八九十百零两0-9]+[章节卷篇部][^。；,\n]{0,30}/,
    /\d+(?:\.\d+)+\s*[^\s，。；:\n]{1,30}/,
    /[上中下]篇[^。；,\n]{0,20}/,
  ];

  for (const text of pools) {
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) return cleanLine(match[0]);
    }
  }

  return cleanLine(book.page?.headings?.[0] || "");
}

function filterQuoteCandidates(book) {
  const title = cleanLine(book.metadata?.title || "");
  const seen = new Set();
  const candidates = [];

  for (const raw of uniqueLines(book.notes || [], 50)) {
    const item = normalizeSnippet(raw);
    if (!item) continue;
    if (item === title) continue;
    if (/已读到|条笔记|时长|公开发|赞 评论|点评此书|推荐一般/.test(item)) continue;
    if (item.length < 18 || item.length > 220) continue;
    if (seen.has(item)) continue;
    seen.add(item);
    candidates.push(item);
  }

  if (candidates.length) {
    return candidates.slice(0, 6);
  }

  return uniqueLines(
    (book.content?.blocks || [])
      .map((item) => normalizeSnippet(shorten(item, 180)))
      .filter((item) => item.length >= 18),
    6
  );
}

function inferThemes(book, quoteCandidates) {
  const title = cleanLine(book.metadata?.title || "");
  const candidates = [
    pickCurrentChapter(book),
    ...(book.page?.headings || []),
    ...quoteCandidates,
    ...(book.content?.blocks || []),
  ];

  const themes = [];
  const seen = new Set();

  for (const item of candidates) {
    const cleaned = shorten(
      stripChapterPrefix(item),
      28
    );
    if (!cleaned || cleaned.length < 4) continue;
    if (cleaned === title) continue;
    if (cleaned.includes(title) && title) continue;
    if (seen.has(cleaned)) continue;
    seen.add(cleaned);
    themes.push(cleaned);
    if (themes.length >= 4) break;
  }

  return themes;
}

function buildQuestionCards(currentChapter, themes, quoteCandidates) {
  const themeA = pickIdeaLabel(themes[0] || currentChapter, { fallback: "当前章节" });
  const themeB = pickIdeaLabel(themes[1] || quoteCandidates[0], { fallback: "作者观点" });
  const quote = shorten(quoteCandidates[0] || "当前摘录", 60);

  return [
    `这个章节最想解决的核心问题是什么，作者给出的答案为什么成立？ 线索：${themeA}`,
    `这条观点和我已有的经验或认知，最一致和最冲突的地方分别是什么？ 线索：${themeB}`,
    `如果把这条观点放到真实场景里，哪些前提成立时它有效，哪些情况下会失效？ 线索：${quote}`,
  ];
}

function buildPermanentNoteSeeds({ currentChapter, themes, quoteCandidates, title }) {
  const chapterLabel = pickIdeaLabel(currentChapter || themes[0], { title, fallback: "核心原则" });
  const conceptA = pickIdeaLabel(quoteCandidates[0] || themes[1], { title, fallback: chapterLabel });
  const conceptB = pickIdeaLabel(quoteCandidates[1] || themes[2] || quoteCandidates[0], { title, fallback: "模式分类" });
  const quote = quoteCandidates[0] || "";

  return [
    {
      title: `${chapterLabel}可以作为判断原则`,
      prompt: `把“${chapterLabel}”改写成一句脱离原书也能成立的判断，并补上适用边界。`,
      support: quote,
    },
    {
      title: `判断${conceptA}前要先明确边界`,
      prompt: `解释为什么判断“${conceptA}”前要先明确边界，再补一个容易误判的例子。`,
      support: quoteCandidates[1] || quote,
    },
    {
      title: `${conceptB}可以迁移到别的场景`,
      prompt: `把“${conceptB}”迁移到工作、投资、学习或写作中的一个具体情境。`,
      support: quoteCandidates[2] || quote,
    },
  ];
}

function renderReflectionEntries(reflections) {
  if (!reflections.length) {
    return [
      "> [!tip] 写法建议",
      "> 可以直接补三行：",
      "> 1. 这本书最打动我的观点是什么",
      "> 2. 它改变了我对什么问题的理解",
      "> 3. 我接下来准备怎么做",
      "",
      "- 暂无读后感，可让 OpenClaw 先帮你起草一版再同步回来。",
    ];
  }

  return reflections.flatMap((item, index) => [
    `### 读后感 ${index + 1}`,
    "",
    `- 时间：${item.updatedAt || item.createdAt || "未知"}`,
    `- 风格：${item.mode || "polished"}`,
    "",
    item.content || "",
    "",
  ]);
}

function buildShelfMarkdown(shelf) {
  const books = shelf.books || [];
  const lines = books.slice(0, 50).map((book, index) => {
    const title = book.title || `Untitled ${index + 1}`;
    const href = book.href || "";
    const bookId = book.bookId || "unknown";
    return `| ${index + 1} | ${title} | ${bookId} | [打开](${href}) |`;
  });

  const yaml = [
    "source: weread",
    `captured_at: ${shelf.capturedAt || ""}`,
    `book_count: ${books.length}`,
    "type: weread-shelf",
    "tags:",
    "  - weread",
    "  - bookshelf",
  ].join("\n");

  return [
    fenceYaml(yaml),
    "# 微信读书书架",
    "",
    "> [!summary] 本次同步",
    `> - 时间：${shelf.capturedAt || "unknown"}`,
    `> - 书籍数量：${books.length}`,
    `> - 页面：${shelf.page?.title || "微信读书"}`,
    "",
    "## 使用方式",
    "",
    "> [!tip] 下一步",
    "> 1. 从下表挑一本书，复制链接后运行 `weread:fetch-book`。",
    "> 2. 导出书籍 Markdown 后，让 OpenClaw 基于单书笔记做总结和卡片化整理。",
    "> 3. 把最终整理结果沉淀到永久笔记或日报中。",
    "",
    "## 书架总览",
    "",
    "| # | 书名 | Book ID | 链接 |",
    "| --- | --- | --- | --- |",
    ...(lines.length ? lines : ["| - | 未识别到书籍 | - | - |"]),
    "",
    "## OpenClaw Prompt",
    "",
    "请基于这份书架快照，帮我挑选下一本最值得深读的书，并给出理由、预期收获、以及建议的阅读顺序。",
    "",
  ].join("\n");
}

function buildBookMarkdown(book, { reflections = [] } = {}) {
  const metadata = book.metadata || {};
  const title = metadata.title || book.page?.title || "Untitled";
  const stats = parseReadingStats(book);
  const currentChapter = pickCurrentChapter(book);
  const headings = uniqueLines(book.page?.headings || [], 8);
  const tocLines = uniqueLines((book.toc || []).map((item) => item.title), 20);
  const quoteCandidates = filterQuoteCandidates(book);
  const noteLines = uniqueLines(book.notes || [], 12);
  const contentLines = uniqueLines((book.content?.blocks || []).map((item) => shorten(item, 800)), 10);
  const themes = inferThemes(book, quoteCandidates);
  const questionCards = buildQuestionCards(currentChapter, themes, quoteCandidates);
  const permanentNotes = buildPermanentNoteSeeds({
    currentChapter,
    themes,
    quoteCandidates,
    title,
  });
  const intro = shorten(metadata.intro || "", 320);
  const yaml = [
    "source: weread",
    `captured_at: ${book.capturedAt || ""}`,
    `title: ${JSON.stringify(title)}`,
    `author: ${JSON.stringify(metadata.author || "")}`,
    `source_url: ${JSON.stringify(book.sourceUrl || "")}`,
    `progress: ${JSON.stringify(stats.progress || "")}`,
    `note_count: ${JSON.stringify(stats.noteCount || "")}`,
    `reading_duration: ${JSON.stringify(stats.duration || "")}`,
    `current_chapter: ${JSON.stringify(currentChapter || "")}`,
    "type: weread-book",
    "tags:",
    "  - weread",
    "  - reading-note",
    "  - zettelkasten",
  ].join("\n");

  return [
    fenceYaml(yaml),
    `# ${title}`,
    "",
    "> [!info] 读书进度面板",
    `> - 作者：${metadata.author || "未知"}`,
    `> - 进度：${stats.progress || "未知"}`,
    `> - 当前章节：${currentChapter || "未知"}`,
    `> - 笔记数：${stats.noteCount || "未知"}`,
    `> - 阅读时长：${stats.duration || "未知"}`,
    `> - 最近同步：${book.capturedAt || "未知"}`,
    `> - 来源：${book.sourceUrl || "未知"}`,
    "",
    "## 本轮待办",
    "",
    "- [ ] 用自己的话复述当前章节的核心观点",
    "- [ ] 从下面的金句卡片里选 1 条做重点展开",
    "- [ ] 至少补完 1 条永久笔记草稿",
    "- [ ] 回答 1 个问题卡片并记录新的疑问",
    "",
    "## 内容概览",
    "",
    ...(intro ? [intro, ""] : []),
    ...(headings.length
      ? ["### 页面标题线索", "", ...renderBulletList(headings, "暂无标题线索"), ""]
      : []),
    "## 章节定位",
    "",
    ...renderBulletList(
      [currentChapter, ...tocLines].filter(Boolean),
      "未识别到目录项"
    ),
    "",
    "## 金句卡片",
    "",
    "> [!quote] 使用建议",
    "> 先挑最有触动的一句，补上“为什么打动我”和“它能指导什么行动”。",
    "",
    ...(quoteCandidates.length
      ? quoteCandidates.flatMap((item, index) => [
          `### 金句 ${index + 1}`,
          "",
          `> ${item}`,
          "",
          "- 我的理解：",
          "- 能连接到哪条旧笔记：",
          "- 可以指导什么行动：",
          "",
        ])
      : ["- 当前页面未识别到适合做金句卡片的内容", ""]),
    "",
    "## 问题卡片",
    "",
    ...(questionCards.length
      ? questionCards.flatMap((item, index) => [
          `### 问题 ${index + 1}`,
          "",
          `- 问题：${item}`,
          "- 为什么值得追问：",
          "- 下次阅读时重点留意：",
          "",
        ])
      : ["- 暂无问题卡片。", ""]),
    "",
    "## 永久笔记草稿",
    "",
    ...(permanentNotes.length
      ? permanentNotes.flatMap((item, index) => [
          `### 永久笔记 ${index + 1}`,
          "",
          `- 标题：${item.title}`,
          `- 论点：${item.prompt}`,
          `- 证据：${item.support || "待补充"}`,
          "- 我的例子：",
          "- 可链接到：",
          "",
        ])
      : ["- 暂无永久笔记草稿。", ""]),
    "",
    "## 读后感与我的卡片",
    "",
    ...renderReflectionEntries(reflections),
    "",
    "## 划线与想法候选",
    "",
    "> [!note] 待清洗原料",
    "> 这一节保留抓取到的原始划线和想法候选，方便 OpenClaw 二次清洗。",
    "",
    ...renderBulletList(noteLines, "当前页面未识别到划线或想法"),
    "",
    "## 正文摘录",
    "",
    ...renderQuoteSections(contentLines, "摘录"),
    "",
    "## OpenClaw Prompt",
    "",
    "> [!tip] 直接可用",
    "> 请把这份笔记整理成卡片笔记输出，要求：",
    "> 1. 先更新读书进度面板",
    "> 2. 从金句卡片里挑出最值得保留的 3 条",
    "> 3. 回答问题卡片中的至少 2 个问题",
    "> 4. 完成 2 到 3 条真正可复用的永久笔记",
    "",
  ]
    .filter(Boolean)
    .join("\n");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const outputs = [];

  if (args.shelf) {
    const shelf = await readJson(args.shelf);
    const shelfPath = path.join(args.outputDir, "weread-shelf.md");
    await writeFile(shelfPath, buildShelfMarkdown(shelf));
    outputs.push(shelfPath);
  }

  if (args.book) {
    const book = await readJson(args.book);
    const title = book.metadata?.title || book.page?.title || "book";
    const bookPath = path.join(args.outputDir, "books", `${slugify(title)}.md`);
    const reflectionData = await readJsonIfExists(reflectionFilePath(title, DEFAULT_REFLECTION_DIR), { entries: [] });
    await writeFile(bookPath, buildBookMarkdown(book, { reflections: reflectionData?.entries || [] }));
    outputs.push(bookPath);
  }

  console.log(JSON.stringify({ ok: true, outputs }, null, 2));
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exitCode = 1;
});
