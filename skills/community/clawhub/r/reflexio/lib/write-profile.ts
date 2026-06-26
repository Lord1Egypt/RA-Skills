import { writeProfileFile, deleteFile, validateSlug, validateTtl, type Ttl } from "./io.ts";
import { preprocessQuery, judgeDedup, extractId } from "./dedup.ts";
import { rawSearch } from "./search.ts";
import type { CommandRunner, InferFn } from "./openclaw-cli.ts";

export interface WriteProfileConfig {
  shallow_threshold: number;
  top_k: number;
}

export interface WriteProfileOpts {
  slug: string;
  ttl: Ttl | string;
  body: string;
  workspace?: string;
  config: WriteProfileConfig;
  runner: CommandRunner;
  inferFn: InferFn;
}

/**
 * Full profile write orchestration:
 * validate → preprocess → search → judge → write → delete (if merging)
 */
export async function writeProfile(opts: WriteProfileOpts): Promise<string> {
  console.info(`[reflexio] writeProfile: slug=${opts.slug} ttl=${opts.ttl} bodyLen=${opts.body.length} workspace=${opts.workspace ?? "(default)"}`);

  validateSlug(opts.slug);
  validateTtl(opts.ttl);

  const query = await preprocessQuery(opts.body, opts.inferFn);
  console.info(`[reflexio] writeProfile: preprocessed query="${query.slice(0, 120)}"`);

  const neighbors = await rawSearch(query, opts.config.top_k, "profile", opts.runner);
  console.info(`[reflexio] writeProfile: found ${neighbors.length} neighbor(s)${neighbors[0] ? `, top score=${neighbors[0].score.toFixed(3)} path=${neighbors[0].path}` : ""}`);

  const top = neighbors[0];
  let bodyToWrite = opts.body;
  let supersedes: string[] | undefined;
  let deleteTarget: string | undefined;

  if (top) {
    const bodyFromSnippet = top.snippet.split("---").slice(2).join("---").trim();
    const result = await judgeDedup(opts.body, bodyFromSnippet, opts.inferFn);
    console.info(`[reflexio] writeProfile: dedup decision="${result.decision}"`);

    if (result.decision === "merge_and_resolve") {
      bodyToWrite = result.resolved;
      const oldId = extractId(top.snippet);
      if (oldId) {
        supersedes = [oldId];
        deleteTarget = top.path;
        console.info(`[reflexio] writeProfile: merge_and_resolve id=${oldId} path=${top.path} resolvedLen=${result.resolved.length}`);
      } else {
        console.error(`[reflexio] writeProfile: merge_and_resolve but could not extract id from snippet`);
      }
    }
  }

  const newPath = writeProfileFile({
    slug: opts.slug,
    ttl: opts.ttl as Ttl,
    body: bodyToWrite,
    supersedes,
    workspace: opts.workspace,
  });
  console.info(`[reflexio] writeProfile: wrote ${newPath}${supersedes ? ` (supersedes: ${supersedes.join(", ")})` : ""}`);

  if (deleteTarget) {
    const ws = opts.workspace || process.env.WORKSPACE || process.cwd();
    const absDelete = deleteTarget.startsWith("/")
      ? deleteTarget
      : `${ws}/${deleteTarget}`;
    deleteFile(absDelete);
    console.info(`[reflexio] writeProfile: deleted old file ${absDelete}`);
  }

  return newPath;
}
