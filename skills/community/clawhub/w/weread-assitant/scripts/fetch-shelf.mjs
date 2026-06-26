import fs from "node:fs/promises";
import path from "node:path";
import { evalTarget, infoTarget, scrollTarget, sleep, withNewTarget } from "./cdp-client.mjs";

const DEFAULT_URL = "https://weread.qq.com/web/shelf";
const DEFAULT_OUTPUT = "output/weread/shelf.json";

function parseArgs(argv) {
  const args = { url: DEFAULT_URL, output: DEFAULT_OUTPUT, keepOpen: false, debugDom: false };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--url") args.url = argv[index + 1];
    if (token === "--output") args.output = argv[index + 1];
    if (token === "--keep-open") args.keepOpen = true;
    if (token === "--debug-dom") args.debugDom = true;
  }
  return args;
}

async function writeJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

const SHELF_EXTRACTOR = String.raw`
(() => {
  const normalize = (value) => (value || "").replace(/\s+/g, " ").trim();
  const asArray = (value) => Array.from(value || []);

  const guessBookId = (href) => {
    if (!href) return null;
    const match =
      href.match(/(?:bookDetail|reader|book)\/([A-Za-z0-9_-]+)/) ||
      href.match(/[?&]bookId=([A-Za-z0-9_-]+)/);
    return match ? match[1] : null;
  };

  const anchors = asArray(document.querySelectorAll("a[href]"));
  const candidates = anchors
    .map((anchor) => {
      const href = anchor.href || anchor.getAttribute("href") || "";
      const text = normalize(anchor.innerText || anchor.textContent);
      const dataset = { ...anchor.dataset };
      const parentText = normalize(anchor.parentElement?.innerText || "");
      const nearbyImage = anchor.querySelector("img")?.src || anchor.closest("a")?.querySelector("img")?.src || null;
      return {
        href,
        text,
        title: normalize(anchor.getAttribute("title") || ""),
        ariaLabel: normalize(anchor.getAttribute("aria-label") || ""),
        dataset,
        bookId: guessBookId(href) || dataset.bookId || dataset.bookid || null,
        cover: nearbyImage,
        parentText,
      };
    })
    .filter((item) => item.href.includes("weread.qq.com"));

  const bookCandidates = candidates.filter((item) => {
    const combined = [item.href, item.text, item.title, item.parentText].join(" ").toLowerCase();
    return /book|reader|shelf|阅读|书架/.test(combined) || Boolean(item.bookId);
  });

  const dedupeKey = (item) => item.href || [item.bookId || "", item.text || item.title || ""].join(":");
  const seen = new Set();
  const books = [];

  for (const item of bookCandidates) {
    const key = dedupeKey(item);
    if (seen.has(key)) continue;
    seen.add(key);

    books.push({
      bookId: item.bookId,
      href: item.href,
      title: item.text || item.title || item.ariaLabel || null,
      cover: item.cover,
      dataset: item.dataset,
      nearbyText: item.parentText || null,
    });
  }

  return {
    title: document.title,
    url: location.href,
    bodyTextSnippet: normalize(document.body?.innerText || "").slice(0, 2000),
    books,
    rawCandidates: bookCandidates.slice(0, 200),
  };
})()
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));

  const data = await withNewTarget(
    args.url,
    async (targetId) => {
      await sleep(2500);
      await scrollTarget(targetId, { direction: "bottom" }).catch(() => {});
      await sleep(1500);
      await scrollTarget(targetId, { y: 0 }).catch(() => {});
      await sleep(800);

      const [pageInfo, extracted] = await Promise.all([
        infoTarget(targetId).catch(() => null),
        evalTarget(targetId, SHELF_EXTRACTOR),
      ]);

      return {
        capturedAt: new Date().toISOString(),
        page: {
          info: pageInfo,
          title: extracted.title,
          url: extracted.url,
          bodyTextSnippet: extracted.bodyTextSnippet,
        },
        books: extracted.books || [],
        ...(args.debugDom ? { rawCandidates: extracted.rawCandidates || [] } : {}),
      };
    },
    { keepOpen: args.keepOpen }
  );

  await writeJson(args.output, data);

  console.log(
    JSON.stringify(
      {
        ok: true,
        output: args.output,
        books: data.books.length,
        title: data.page?.title || null,
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
