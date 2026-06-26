import fs from "node:fs/promises";
import path from "node:path";
import { evalTarget, infoTarget, scrollTarget, sleep, withNewTarget } from "./cdp-client.mjs";
import { slugify } from "./book-utils.mjs";

const DEFAULT_OUTPUT_DIR = "output/weread/books";

function parseArgs(argv) {
  const args = {
    bookUrl: "",
    output: "",
    outputDir: DEFAULT_OUTPUT_DIR,
    keepOpen: false,
    scrolls: 6,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--book-url") args.bookUrl = argv[index + 1];
    if (token === "--output") args.output = argv[index + 1];
    if (token === "--output-dir") args.outputDir = argv[index + 1];
    if (token === "--scrolls") args.scrolls = Number.parseInt(argv[index + 1], 10);
    if (token === "--keep-open") args.keepOpen = true;
  }

  if (!args.bookUrl) {
    throw new Error("Missing required argument: --book-url");
  }

  return args;
}

async function writeJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

const PAGE_EXTRACTOR = String.raw`
(() => {
  const normalize = (value) => (value || "").replace(/\s+/g, " ").trim();
  const asArray = (value) => Array.from(value || []);

  const pickTextList = (selectors, limit = 100) => {
    const values = [];
    for (const selector of selectors) {
      for (const node of asArray(document.querySelectorAll(selector))) {
        const text = normalize(node.innerText || node.textContent);
        if (!text) continue;
        if (values.includes(text)) continue;
        values.push(text);
        if (values.length >= limit) return values;
      }
    }
    return values;
  };

  const noteSelectors = [
    '[class*="note"]',
    '[class*="review"]',
    '[class*="highlight"]',
    '[class*="bookmark"]',
    '[data-type*="note"]',
  ];

  const contentSelectors = [
    '[class*="chapter"]',
    '[class*="reader"]',
    'article',
    'main',
    '.content',
    '.app_content',
  ];

  const extractParagraphs = () => {
    const blocks = [];
    const seen = new Set();

    for (const selector of contentSelectors) {
      for (const node of asArray(document.querySelectorAll(selector))) {
        const text = normalize(node.innerText || node.textContent);
        if (!text || text.length < 20) continue;
        if (seen.has(text)) continue;
        seen.add(text);
        blocks.push(text);
      }
      if (blocks.length) break;
    }

    if (!blocks.length) {
      const bodyText = normalize(document.body?.innerText || "");
      if (bodyText) blocks.push(bodyText);
    }

    return blocks.slice(0, 200);
  };

  const tocLinks = asArray(document.querySelectorAll('a[href]'))
    .map((anchor) => ({
      title: normalize(anchor.innerText || anchor.textContent),
      href: anchor.href || anchor.getAttribute("href") || "",
    }))
    .filter((item) => item.title && /章|节|chapter|目录|contents/i.test([item.title, item.href].join(" ")))
    .slice(0, 200);

  const headings = pickTextList(["h1", "h2", "h3"], 20);
  const metaDescription = document.querySelector('meta[name="description"]')?.content || "";
  const cover = document.querySelector("img")?.src || null;
  const title =
    normalize(document.querySelector("h1")?.innerText) ||
    normalize(document.querySelector('[class*="title"]')?.innerText) ||
    document.title;
  const author = pickTextList(['[class*="author"]', '[data-author]', '.author'], 10)[0] || null;

  return {
    url: location.href,
    title: document.title,
    headings,
    metadata: {
      title,
      author,
      intro: normalize(metaDescription),
      cover,
    },
    toc: tocLinks,
    notes: pickTextList(noteSelectors, 100),
    contentBlocks: extractParagraphs(),
  };
})()
`;

async function collectContent(targetId, scrolls) {
  const blocks = [];
  const seen = new Set();

  for (let index = 0; index < scrolls; index += 1) {
    const snapshot = await evalTarget(targetId, PAGE_EXTRACTOR);
    for (const paragraph of snapshot.contentBlocks || []) {
      if (!seen.has(paragraph)) {
        seen.add(paragraph);
        blocks.push(paragraph);
      }
    }

    await scrollTarget(targetId, { y: 2200 }).catch(() => {});
    await sleep(1200);
  }

  return blocks;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const data = await withNewTarget(
    args.bookUrl,
    async (targetId) => {
      await sleep(2500);

      const initial = await evalTarget(targetId, PAGE_EXTRACTOR);
      const contentBlocks = await collectContent(targetId, Number.isFinite(args.scrolls) ? args.scrolls : 6);
      const pageInfo = await infoTarget(targetId).catch(() => null);

      return {
        capturedAt: new Date().toISOString(),
        sourceUrl: args.bookUrl,
        page: {
          info: pageInfo,
          title: initial.title,
          url: initial.url,
          headings: initial.headings || [],
        },
        metadata: initial.metadata || {},
        toc: initial.toc || [],
        notes: initial.notes || [],
        content: {
          blocks: contentBlocks,
          text: contentBlocks.join("\n\n"),
        },
      };
    },
    { keepOpen: args.keepOpen }
  );

  const inferredName = slugify(data.metadata?.title || data.page?.title || "book");
  const outputFile = args.output || path.join(args.outputDir, `${inferredName}.json`);

  await writeJson(outputFile, data);

  console.log(
    JSON.stringify(
      {
        ok: true,
        output: outputFile,
        title: data.metadata?.title || null,
        tocItems: data.toc.length,
        noteItems: data.notes.length,
        contentBlocks: data.content.blocks.length,
      },
      null,
      2
    )
  );
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exitCode = 1;
});
