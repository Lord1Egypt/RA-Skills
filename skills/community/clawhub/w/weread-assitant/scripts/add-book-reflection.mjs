import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  DEFAULT_BOOK_DIR,
  DEFAULT_OBSIDIAN_DIR,
  DEFAULT_REFLECTION_DIR,
  bookJsonPath,
  bookMarkdownPath,
  reflectionFilePath,
  resolveBookByTitle,
  slugify,
} from "./book-utils.mjs";

const execFileAsync = promisify(execFile);

function parseArgs(argv) {
  const args = {
    title: "",
    reflection: "",
    mode: "polished",
    book: "",
    reflectionDir: DEFAULT_REFLECTION_DIR,
    obsidianDir: DEFAULT_OBSIDIAN_DIR,
    bookDir: DEFAULT_BOOK_DIR,
    vault: "",
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--title") args.title = argv[index + 1];
    if (token === "--reflection") args.reflection = argv[index + 1];
    if (token === "--mode") args.mode = argv[index + 1];
    if (token === "--book") args.book = argv[index + 1];
    if (token === "--reflection-dir") args.reflectionDir = argv[index + 1];
    if (token === "--output-dir") args.obsidianDir = argv[index + 1];
    if (token === "--book-dir") args.bookDir = argv[index + 1];
    if (token === "--vault") args.vault = argv[index + 1];
  }

  if (!args.reflection) {
    throw new Error("Missing required argument: --reflection");
  }

  return args;
}

function normalizeParagraphs(input) {
  return String(input || "")
    .split(/\n{2,}/)
    .map((part) => part.replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .join("\n\n");
}

async function runNodeScript(scriptPath, argv) {
  const { stdout } = await execFileAsync(process.execPath, [scriptPath, ...argv], {
    cwd: process.cwd(),
    maxBuffer: 1024 * 1024 * 16,
  });

  return stdout ? JSON.parse(stdout) : null;
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function readJsonIfExists(filePath, fallback) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    if (error?.code === "ENOENT") return fallback;
    throw error;
  }
}

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function resolveBookPathFromTitle(title, bookDir) {
  const entries = await fs.readdir(bookDir, { withFileTypes: true }).catch(() => []);
  const books = [];

  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".json")) continue;
    const fullPath = path.join(bookDir, entry.name);
    const book = await readJsonIfExists(fullPath, null);
    if (!book) continue;
    books.push({
      title: book.metadata?.title || book.page?.title || entry.name.replace(/\.json$/i, ""),
      href: fullPath,
      bookId: "",
    });
  }

  const { match, candidates } = resolveBookByTitle(books, title);
  if (!match?.href) {
    throw new Error(
      `Could not find a synced book matching "${title}". Sync the book first or pass --book. Candidates: ${JSON.stringify(candidates, null, 2)}`
    );
  }

  return match.href;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let bookPath = args.book || "";

  if (!bookPath && args.title) {
    try {
      bookPath = await resolveBookPathFromTitle(args.title, args.bookDir);
    } catch (error) {
      const fallbackPath = bookJsonPath(args.title, args.bookDir);
      if (await fileExists(fallbackPath)) {
        bookPath = fallbackPath;
      } else {
        throw error;
      }
    }
  }

  if (!bookPath) {
    throw new Error("Provide --title or --book so the reflection can be attached to a book note");
  }

  const book = await readJson(bookPath);
  const resolvedTitle = book.metadata?.title || book.page?.title || args.title || slugify(bookPath);
  const reflectionPath = reflectionFilePath(resolvedTitle, args.reflectionDir);
  const current = await readJsonIfExists(reflectionPath, {
    title: resolvedTitle,
    slug: slugify(resolvedTitle),
    entries: [],
  });

  current.title = resolvedTitle;
  current.slug = slugify(resolvedTitle);
  current.entries = current.entries || [];
  current.entries.push({
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    mode: args.mode || "polished",
    content: normalizeParagraphs(args.reflection),
  });

  await writeJson(reflectionPath, current);

  await runNodeScript(path.join("scripts", "export-obsidian.mjs"), [
    "--book",
    path.resolve(bookPath),
    "--output-dir",
    args.obsidianDir,
  ]);

  const noteFile = path.resolve(bookMarkdownPath(resolvedTitle, args.obsidianDir));
  await runNodeScript(path.join("scripts", "publish-obsidian.mjs"), [
    "--file",
    noteFile,
    ...(args.vault ? ["--vault", args.vault] : []),
  ]);

  console.log(
    JSON.stringify(
      {
        ok: true,
        title: resolvedTitle,
        reflectionPath: path.resolve(reflectionPath),
        noteFile,
        entries: current.entries.length,
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
