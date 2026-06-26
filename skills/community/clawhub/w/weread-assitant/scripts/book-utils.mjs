import path from "node:path";

export const DEFAULT_SHELF_PATH = "output/weread/shelf.json";
export const DEFAULT_BOOK_DIR = "output/weread/books";
export const DEFAULT_REFLECTION_DIR = "output/weread/reflections";
export const DEFAULT_OBSIDIAN_DIR = "output/obsidian";

export function slugify(input) {
  return (input || "book")
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/gi, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "book";
}

export function normalizeTitle(input) {
  return String(input || "")
    .toLowerCase()
    .replace(/[\s"'“”‘’`~!@#$%^&*()_+=|\\[\]{}:;,.<>/?，。！？；：（）【】《》、·-]+/g, "");
}

function scoreBookMatch(query, candidate) {
  const queryKey = normalizeTitle(query);
  const titleKey = normalizeTitle(candidate.title || "");

  if (!queryKey || !titleKey) return 0;
  if (queryKey === titleKey) return 100;
  if (titleKey.includes(queryKey)) return 80;
  if (queryKey.includes(titleKey)) return 70;

  let shared = 0;
  for (const char of new Set(queryKey.split(""))) {
    if (titleKey.includes(char)) shared += 1;
  }

  return shared >= Math.min(4, queryKey.length) ? shared : 0;
}

export function resolveBookByTitle(books, query) {
  const candidates = (books || [])
    .map((book) => ({
      book,
      score: scoreBookMatch(query, book),
    }))
    .filter((item) => item.score > 0)
    .sort((left, right) => right.score - left.score);

  return {
    match: candidates[0]?.book || null,
    candidates: candidates.slice(0, 5).map((item) => ({
      title: item.book.title || "",
      href: item.book.href || "",
      bookId: item.book.bookId || "",
      score: item.score,
    })),
  };
}

export function reflectionFilePath(title, reflectionDir = DEFAULT_REFLECTION_DIR) {
  return path.join(reflectionDir, `${slugify(title)}.json`);
}

export function bookJsonPath(title, bookDir = DEFAULT_BOOK_DIR) {
  return path.join(bookDir, `${slugify(title)}.json`);
}

export function bookMarkdownPath(title, obsidianDir = DEFAULT_OBSIDIAN_DIR) {
  return path.join(obsidianDir, "books", `${slugify(title)}.md`);
}
