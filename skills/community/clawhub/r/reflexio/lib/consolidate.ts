import * as fs from "node:fs";
import * as path from "node:path";

import { writeProfileFile, writePlaybookFile, deleteFile, type Ttl } from "./io.ts";
import { memorySearch, reindexMemory, type CommandRunner, type InferFn } from "./openclaw-cli.ts";
import { ttlSweepProfiles } from "../hook/handler.ts";

export interface ConsolidationResult {
  profilesClustered: number;
  playbooksClustered: number;
  filesWritten: number;
  filesDeleted: number;
}

interface FileEntry {
  id: string;
  path: string;
  content: string;
  ttl?: string;
  created?: string;
}

interface ConsolidationFact {
  slug: string;
  body: string;
  source_ids: string[];
}

interface LlmConsolidationResult {
  action: "keep_all" | "consolidate";
  facts?: ConsolidationFact[];
  ids_to_delete?: string[];
  rationale?: string;
}

const CONSOLIDATION_PROMPT = `You consolidate a cluster of similar items (profiles or playbooks).

**One fact per file.** Each output entry must contain exactly ONE atomic fact (1-2 sentences). Do NOT combine unrelated facts.

Decisions:
- "keep_all" — items are already distinct, no redundancy.
- "consolidate" — deduplicate, resolve contradictions (most recent wins), split into individual facts.

Answer with ONLY a JSON object:
{"action": "keep_all"} or {"action": "consolidate", "facts": [{"slug": "kebab-case", "body": "single fact"}], "ids_to_delete": ["id1", "id2"], "rationale": "why"}

Cluster:
{cluster}`;

/**
 * Load all .md files from a .reflexio subdirectory, extracting frontmatter fields.
 */
function loadFiles(dir: string): FileEntry[] {
  if (!fs.existsSync(dir)) return [];
  const entries: FileEntry[] = [];
  for (const name of fs.readdirSync(dir)) {
    if (!name.endsWith(".md")) continue;
    const full = path.join(dir, name);
    let raw: string;
    try {
      raw = fs.readFileSync(full, "utf8");
    } catch {
      continue;
    }
    const idMatch = /^id:\s*(\S+)/m.exec(raw);
    const ttlMatch = /^ttl:\s*(\S+)/m.exec(raw);
    const createdMatch = /^created:\s*(\S+)/m.exec(raw);
    const body = raw.split("---").slice(2).join("---").trim();
    if (!idMatch || !body) continue;
    entries.push({
      id: idMatch[1],
      path: full,
      content: body,
      ttl: ttlMatch?.[1],
      created: createdMatch?.[1],
    });
  }
  return entries;
}

/**
 * Cluster files by similarity using memory search.
 * Returns groups of 2+ related files. Each file appears in at most one cluster.
 */
async function clusterFiles(
  files: FileEntry[],
  type: "profile" | "playbook",
  workspaceDir: string,
  runner: CommandRunner
): Promise<FileEntry[][]> {
  const visited = new Set<string>();
  const clusters: FileEntry[][] = [];

  for (const file of files) {
    if (visited.has(file.id)) continue;
    visited.add(file.id);

    const results = await memorySearch(file.content, 10, runner);
    console.info(`[reflexio] clustering: file=${file.id} searchResults=${results.length} paths=[${results.map((r) => r.path).join(", ")}]`);
    const typeDir = type === "profile" ? "/profiles/" : "/playbooks/";
    const neighbors = results
      .filter((r) => r.path.includes(typeDir))
      .map((r) => {
        // Match by path — memory search returns relative paths, loaded files have absolute
        const absPath = r.path.startsWith("/") ? r.path : path.join(workspaceDir, r.path);
        const match = files.find((f) => f.path === absPath);
        if (!match) console.info(`[reflexio] clustering: no file match for path=${r.path} absPath=${absPath}`);
        return match;
      })
      .filter((f): f is FileEntry => f !== undefined && f.id !== file.id && !visited.has(f.id));
    console.info(`[reflexio] clustering: file=${file.id} neighbors=${neighbors.length} neighborIds=[${neighbors.map((n) => n.id).join(", ")}]`);

    if (neighbors.length === 0) continue;

    const cluster = [file, ...neighbors.slice(0, 9)];
    for (const member of cluster) visited.add(member.id);
    clusters.push(cluster);
  }

  return clusters;
}

/**
 * Format cluster items for the LLM prompt.
 */
function formatCluster(cluster: FileEntry[]): string {
  return cluster
    .map((f) => `- id: ${f.id}\n  created: ${f.created ?? "unknown"}\n  content: ${f.content}`)
    .join("\n\n");
}

/**
 * Pick the most conservative TTL from a cluster of profiles.
 */
function pickSmallestTtl(cluster: FileEntry[]): Ttl {
  const order: Ttl[] = ["one_day", "one_week", "one_month", "one_quarter", "one_year", "infinity"];
  let smallest = order.length - 1;
  for (const file of cluster) {
    const idx = order.indexOf(file.ttl as Ttl);
    if (idx >= 0 && idx < smallest) smallest = idx;
  }
  return order[smallest];
}

/**
 * Run a full consolidation sweep: TTL sweep → cluster → LLM judge → write/delete.
 * Uses inferFn (SDK simple completion) for LLM — bypasses lanes entirely.
 */
export async function runConsolidation(opts: {
  workspaceDir: string;
  runner: CommandRunner;
  inferFn: InferFn;
}): Promise<ConsolidationResult> {
  const result: ConsolidationResult = { profilesClustered: 0, playbooksClustered: 0, filesWritten: 0, filesDeleted: 0 };
  console.info(`[reflexio] consolidation: starting, workspace=${opts.workspaceDir}`);

  // 1. TTL sweep
  await ttlSweepProfiles(opts.workspaceDir);
  console.info(`[reflexio] consolidation: TTL sweep done`);

  // 2. Process profiles, then playbooks
  for (const type of ["profile", "playbook"] as const) {
    const dir = path.join(opts.workspaceDir, ".reflexio", type === "profile" ? "profiles" : "playbooks");
    const files = loadFiles(dir);
    console.info(`[reflexio] consolidation: loaded ${files.length} ${type} files`);
    if (files.length < 2) continue;

    const clusters = await clusterFiles(files, type, opts.workspaceDir, opts.runner);
    console.info(`[reflexio] consolidation: found ${clusters.length} ${type} cluster(s) with >1 member`);

    for (const cluster of clusters) {
      console.info(`[reflexio] consolidation: processing ${type} cluster of ${cluster.length} items: ${cluster.map((f) => f.id).join(", ")}`);

      const prompt = CONSOLIDATION_PROMPT.replace("{cluster}", formatCluster(cluster));
      const llmResult = await opts.inferFn(prompt);

      if (!llmResult) {
        console.error(`[reflexio] consolidation: inferFn returned empty for cluster, skipping`);
        continue;
      }

      let decision: LlmConsolidationResult;
      try {
        decision = JSON.parse(llmResult);
      } catch (err) {
        console.error(`[reflexio] consolidation: JSON parse failed: ${err}, skipping cluster`);
        continue;
      }

      console.info(`[reflexio] consolidation: decision="${decision.action}" rationale="${(decision.rationale ?? "").slice(0, 100)}"`);

      if (decision.action === "keep_all") continue;

      if (decision.action === "consolidate" && decision.facts && decision.ids_to_delete) {
        // Build id→file lookup for deletion
        const idToFile = new Map(cluster.map((f) => [f.id, f]));

        // Write new fact files
        for (const fact of decision.facts) {
          if (type === "profile") {
            const sourceFiles = (fact.source_ids ?? []).map((id) => idToFile.get(id)).filter((f): f is FileEntry => f !== undefined);
            const ttl = sourceFiles.length > 0 ? pickSmallestTtl(sourceFiles) : pickSmallestTtl(cluster);
            const supersedes = fact.source_ids?.filter((id) => idToFile.has(id));
            writeProfileFile({ slug: fact.slug, ttl, body: fact.body, supersedes, workspace: opts.workspaceDir });
            result.filesWritten++;
          } else {
            const supersedes = fact.source_ids?.filter((id) => idToFile.has(id));
            writePlaybookFile({ slug: fact.slug, body: fact.body, supersedes, workspace: opts.workspaceDir });
            result.filesWritten++;
          }
        }

        // Delete old files
        for (const id of decision.ids_to_delete) {
          const file = idToFile.get(id);
          if (file) {
            deleteFile(file.path);
            result.filesDeleted++;
          }
        }

        if (type === "profile") result.profilesClustered += cluster.length;
        else result.playbooksClustered += cluster.length;
      }
    }
  }

  // 3. Reindex memory
  await reindexMemory(opts.runner);
  console.info(`[reflexio] consolidation: complete. wrote=${result.filesWritten} deleted=${result.filesDeleted}`);

  return result;
}
