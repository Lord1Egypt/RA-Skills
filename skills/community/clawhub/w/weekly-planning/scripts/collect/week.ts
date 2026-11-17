/**
 * Collect last week's evidence into the cadence layer.
 *
 * The deterministic half of weekly planning: it dumps git commits, pull
 * requests, active initiatives, declared infra, and cadence files dated
 * inside the previous ISO week into
 * cadence/log/raw/planning/<YYYY-Www>.md. It makes no judgements — no
 * recommendations, no ranking, no "what to do". That is the planner
 * agent's job, and keeping the two apart is the point: a fetch loop an
 * LLM re-derives every Monday is a fetch loop that silently changes
 * shape.
 *
 * Run from the repo root:
 *
 *   npx tsx scripts/weekly-planning/collect/week.ts
 *   npx tsx scripts/weekly-planning/collect/week.ts --dry-run
 *
 * The week is the previous complete ISO week in PLANNING_TIMEZONE
 * (default America/Los_Angeles). The cron fires Monday morning, so the
 * window is last Monday through last Sunday.
 *
 * This file sits at scripts/<skill>/collect/, so the repo root is three
 * up. Resolved from the file rather than from cwd: the agent may run it
 * from anywhere in the working tree.
 */
import { execFileSync } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { basename, join, relative, resolve, sep } from "node:path";

const ROOT = resolve(import.meta.dirname, "..", "..", "..");
const RAW_DIR = join(ROOT, "cadence", "log", "raw", "planning");
const LOG_DIR = join(ROOT, "cadence", "log");
const INITIATIVES_DIR = join(ROOT, "initiatives");
const INFRA_DIR = join(ROOT, "infra");

const TIMEZONE =
  process.env["PLANNING_TIMEZONE"] === undefined ||
  process.env["PLANNING_TIMEZONE"] === ""
    ? "America/Los_Angeles"
    : process.env["PLANNING_TIMEZONE"];

const dryRun = process.argv.includes("--dry-run");

const dateInZone = (value: Date, timeZone: string): string =>
  new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(value);

const fromYmd = (ymd: string): Date => {
  const [year, month, day] = ymd.split("-").map(Number);
  return new Date(Date.UTC(year, month - 1, day));
};

const toYmd = (value: Date): string => value.toISOString().slice(0, 10);

const addDays = (value: Date, days: number): Date => {
  const next = new Date(value);
  next.setUTCDate(next.getUTCDate() + days);
  return next;
};

const isoWeek = (value: Date): { year: number; week: number } => {
  const tmp = new Date(
    Date.UTC(value.getUTCFullYear(), value.getUTCMonth(), value.getUTCDate()),
  );
  const day = tmp.getUTCDay() || 7;
  tmp.setUTCDate(tmp.getUTCDate() + 4 - day);
  const yearStart = new Date(Date.UTC(tmp.getUTCFullYear(), 0, 1));
  const week = Math.ceil(
    ((Number(tmp) - Number(yearStart)) / 86400000 + 1) / 7,
  );
  return { year: tmp.getUTCFullYear(), week };
};

const padWeek = (week: number): string => week.toString().padStart(2, "0");

const today = dateInZone(new Date(), TIMEZONE);
const todayUtc = fromYmd(today);
const isoDay = todayUtc.getUTCDay() || 7;
const thisMonday = addDays(todayUtc, 1 - isoDay);
const weekStart = addDays(thisMonday, -7);
const weekEnd = addDays(thisMonday, -1);
const { year, week } = isoWeek(weekStart);
const weekId = `${year}-W${padWeek(week)}`;
const startYmd = toYmd(weekStart);
const endYmd = toYmd(weekEnd);

const inWeek = (ymd: string): boolean => ymd >= startYmd && ymd <= endYmd;

// git and GitHub search both read these dates in UTC (or the sandbox's zone),
// and the edges of a Pacific week are a different day in UTC. Query a day
// either side, then keep only what falls inside the week in TIMEZONE.
const queryStart = toYmd(addDays(weekStart, -1));
const queryEnd = toYmd(addDays(weekEnd, 1));

type Result = { ok: true; stdout: string } | { ok: false; error: string };

const run = (command: string, args: string[]): Result => {
  try {
    const stdout = execFileSync(command, args, {
      cwd: ROOT,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });
    return { ok: true, stdout: stdout.trimEnd() };
  } catch (error) {
    const err = error as { stderr?: string; message?: string };
    const detail =
      typeof err.stderr === "string" && err.stderr.trim() !== ""
        ? err.stderr.trim()
        : (err.message ?? String(error));
    return { ok: false, error: detail };
  }
};

const walk = (dir: string): string[] => {
  if (!existsSync(dir)) return [];
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.name === "node_modules") continue;
    if (entry.isDirectory()) out.push(...walk(path));
    else out.push(path);
  }
  return out;
};

const frontmatterStatus = (text: string): string | undefined => {
  if (!text.startsWith("---")) return undefined;
  const end = text.indexOf("\n---", 3);
  if (end === -1) return undefined;
  const match = /^status:\s*["']?([^\s"']+)/m.exec(text.slice(0, end));
  return match === null ? undefined : match[1];
};

const commits = run("git", [
  "log",
  "--format=%cI %h %s",
  `--since=${queryStart}`,
  `--until=${queryEnd}T23:59:59`,
]);

const commitLines =
  commits.ok === false
    ? [`_git log failed: ${commits.error}_`]
    : commits.stdout
        .split("\n")
        .filter((line) => line !== "")
        .flatMap((line) => {
          const space = line.indexOf(" ");
          if (space === -1) return [];
          const iso = line.slice(0, space);
          const rest = line.slice(space + 1);
          if (!/^\d{4}-\d{2}-\d{2}T/.test(iso)) return [];
          const day = dateInZone(new Date(iso), TIMEZONE);
          if (!inWeek(day)) return [];
          return [`- ${rest} (${iso})`];
        });

const merged = run("gh", [
  "pr",
  "list",
  "--state",
  "merged",
  "--search",
  `merged:${queryStart}..${queryEnd}`,
  "--limit",
  "100",
  "--json",
  "number,title,url,author,mergedAt",
]);

const opened = run("gh", [
  "pr",
  "list",
  "--state",
  "all",
  "--search",
  `created:${queryStart}..${queryEnd}`,
  "--limit",
  "100",
  "--json",
  "number,title,url,author,createdAt,state",
]);

type Pull = {
  number: number;
  title: string;
  url: string;
  author?: { login?: string };
  mergedAt?: string;
  createdAt?: string;
  state?: string;
};

const formatPulls = (
  result: Result,
  stamp: "mergedAt" | "createdAt",
): string[] => {
  if (result.ok === false) {
    return [`_gh unavailable: ${result.error}_`];
  }
  let rows: Pull[] = [];
  try {
    rows = JSON.parse(result.stdout === "" ? "[]" : result.stdout) as Pull[];
  } catch {
    return [`_gh returned unreadable JSON_`];
  }
  const week = rows.filter((row) => {
    const when = row[stamp];
    return when !== undefined && inWeek(dateInZone(new Date(when), TIMEZONE));
  });
  if (week.length === 0) return ["_none_"];
  return week.map((row) => {
    const who = row.author?.login ?? "unknown";
    const state = row.state === undefined ? "" : `, ${row.state}`;
    return `- #${row.number} ${row.title} (${who}${state}, ${row[stamp]}) — ${row.url}`;
  });
};

// README.md and `_`-prefixed files (`_template.md`) describe the folder; they
// are not initiatives.
const initiativeFiles = walk(INITIATIVES_DIR).filter((path) => {
  const name = basename(path);
  return (
    name.endsWith(".md") &&
    name.toLowerCase() !== "readme.md" &&
    !name.startsWith("_")
  );
});

// The slug names a branch and a plan file, so a nested initiative
// (initiatives/q4/foo.md) flattens to `q4-foo` rather than carrying a slash.
const initiativeSlug = (path: string): string => {
  return relative(INITIATIVES_DIR, path)
    .replace(/\.md$/, "")
    .split(sep)
    .join("-");
};

const initiativeLines =
  initiativeFiles.length === 0
    ? ["_no initiatives/ folder, or it is empty_"]
    : initiativeFiles.map((path) => {
        const rel = relative(ROOT, path);
        const slug = initiativeSlug(path);
        let status = "unset";
        try {
          status = frontmatterStatus(readFileSync(path, "utf8")) ?? "unset";
        } catch {
          status = "unreadable";
        }
        return `- \`${slug}\` status: ${status} — \`${rel}\``;
      });

const infraFiles = walk(INFRA_DIR).filter(
  (path) => path.endsWith(".ts") && !path.endsWith(".d.ts"),
);

const infraLines =
  infraFiles.length === 0
    ? ["_no infra/ TypeScript, or infra/ is missing_"]
    : infraFiles.map((path) => {
        const rel = relative(ROOT, path);
        let kind = "file";
        try {
          const text = readFileSync(path, "utf8");
          if (/\bdefineAgent\s*\(/.test(text)) kind = "agent";
          else if (/\bdefinePlay\s*\(/.test(text)) kind = "play";
          else if (/\bdefineModel\s*\(/.test(text)) kind = "model";
          else if (/\bdefineConnector\s*\(/.test(text)) kind = "connector";
          else if (/\bdefineFolder\s*\(/.test(text)) kind = "folder";
          else if (/\bdefineTool\s*\(/.test(text)) kind = "tool";
        } catch {
          kind = "unreadable";
        }
        return `- ${kind}: \`${rel}\``;
      });

const cadenceFiles = walk(LOG_DIR)
  .filter((path) => {
    if (path.includes(`${join("raw", "planning")}`)) return false;
    const match = path.match(/(\d{4}-\d{2}-\d{2})/);
    return match !== null && inWeek(match[1]);
  })
  .map((path) => `- \`${relative(ROOT, path)}\``);

const lines = [
  `---`,
  `title: Weekly planning capture ${weekId}`,
  `description: Deterministic evidence dump for the ${TIMEZONE} ISO week ${weekId} (${startYmd} to ${endYmd}).`,
  `week: ${weekId}`,
  `start: ${startYmd}`,
  `end: ${endYmd}`,
  `timezone: ${TIMEZONE}`,
  `---`,
  ``,
  `## Window`,
  ``,
  `${startYmd} to ${endYmd} (${TIMEZONE}). Previous complete ISO week.`,
  ``,
  `## Initiatives`,
  ``,
  ...initiativeLines,
  ``,
  `## Declared infra`,
  ``,
  ...infraLines,
  ``,
  `## Commits`,
  ``,
  ...(commitLines.length === 0 ? ["_none_"] : commitLines),
  ``,
  `## Pull requests merged`,
  ``,
  ...formatPulls(merged, "mergedAt"),
  ``,
  `## Pull requests opened`,
  ``,
  ...formatPulls(opened, "createdAt"),
  ``,
  `## Cadence files dated this week`,
  ``,
  ...(cadenceFiles.length === 0 ? ["_none_"] : cadenceFiles),
  ``,
];

const markdown = lines.join("\n");

if (dryRun) {
  console.log(markdown);
  process.exit(0);
}

mkdirSync(RAW_DIR, { recursive: true });
const out = join(RAW_DIR, `${weekId}.md`);
writeFileSync(out, markdown);
console.log(`wrote ${relative(ROOT, out)}`);
