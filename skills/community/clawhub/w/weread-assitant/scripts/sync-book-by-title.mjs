import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  DEFAULT_BOOK_DIR,
  DEFAULT_OBSIDIAN_DIR,
  DEFAULT_SHELF_PATH,
  bookJsonPath,
  bookMarkdownPath,
  resolveBookByTitle,
} from "./book-utils.mjs";

const execFileAsync = promisify(execFile);

function parseArgs(argv) {
  const args = {
    title: "",
    shelf: DEFAULT_SHELF_PATH,
    bookDir: DEFAULT_BOOK_DIR,
    obsidianDir: DEFAULT_OBSIDIAN_DIR,
    vault: "",
    publishShelf: false,
    keepOpen: false,
    scrolls: 6,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--title") args.title = argv[index + 1];
    if (token === "--shelf") args.shelf = argv[index + 1];
    if (token === "--book-dir") args.bookDir = argv[index + 1];
    if (token === "--output-dir") args.obsidianDir = argv[index + 1];
    if (token === "--vault") args.vault = argv[index + 1];
    if (token === "--scrolls") args.scrolls = Number.parseInt(argv[index + 1], 10);
    if (token === "--publish-shelf") args.publishShelf = true;
    if (token === "--keep-open") args.keepOpen = true;
  }

  if (!args.title) {
    throw new Error("Missing required argument: --title");
  }

  return args;
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

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  await runNodeScript(path.join("scripts", "fetch-shelf.mjs"), [
    "--output",
    args.shelf,
    ...(args.keepOpen ? ["--keep-open"] : []),
  ]);

  const shelf = await readJson(args.shelf);
  const { match, candidates } = resolveBookByTitle(shelf.books || [], args.title);

  if (!match?.href) {
    throw new Error(
      `Could not resolve book title "${args.title}". Top candidates: ${JSON.stringify(candidates, null, 2)}`
    );
  }

  const bookOutput = bookJsonPath(match.title || args.title, args.bookDir);
  await runNodeScript(path.join("scripts", "fetch-book.mjs"), [
    "--book-url",
    match.href,
    "--output",
    bookOutput,
    "--scrolls",
    String(args.scrolls || 6),
    ...(args.keepOpen ? ["--keep-open"] : []),
  ]);

  await runNodeScript(path.join("scripts", "export-obsidian.mjs"), [
    "--shelf",
    args.shelf,
    "--book",
    bookOutput,
    "--output-dir",
    args.obsidianDir,
  ]);

  const bookData = await readJson(bookOutput);
  const resolvedTitle = bookData.metadata?.title || match.title || args.title;
  const noteFile = path.resolve(bookMarkdownPath(resolvedTitle, args.obsidianDir));

  if (!(await fileExists(noteFile))) {
    throw new Error(`Expected exported note file was not created: ${noteFile}`);
  }

  await runNodeScript(path.join("scripts", "publish-obsidian.mjs"), [
    "--file",
    noteFile,
    ...(args.vault ? ["--vault", args.vault] : []),
  ]);

  if (args.publishShelf) {
    const shelfNote = path.resolve(path.join(args.obsidianDir, "weread-shelf.md"));
    if (await fileExists(shelfNote)) {
      await runNodeScript(path.join("scripts", "publish-obsidian.mjs"), [
        "--file",
        shelfNote,
        ...(args.vault ? ["--vault", args.vault] : []),
      ]);
    }
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        query: args.title,
        matchedBook: {
          title: resolvedTitle,
          href: match.href,
          bookId: match.bookId || "",
        },
        outputs: {
          shelf: path.resolve(args.shelf),
          bookJson: path.resolve(bookOutput),
          noteFile,
        },
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
