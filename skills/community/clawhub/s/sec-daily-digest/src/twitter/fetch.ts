import type { TwitterSourceConfig } from "../config/sources";
import type { TweetArticle } from "./types";
import type { TwitterBackend, TwitterSourceResult } from "./backends/types";
import { selectBackend } from "./backends/factory";

export interface FetchTwitterKolsOptions {
  hours: number;
  env: NodeJS.ProcessEnv;
  backend?: TwitterBackend;
  fetcher?: typeof fetch;
}

export async function fetchTwitterKols(
  sources: TwitterSourceConfig[],
  options: FetchTwitterKolsOptions,
): Promise<{ articles: TweetArticle[]; results: TwitterSourceResult[] }> {
  if (sources.length === 0) {
    return { articles: [], results: [] };
  }

  const backend = options.backend ?? selectBackend(options.env, options.fetcher ?? fetch);
  if (!backend) {
    return { articles: [], results: [] };
  }

  const cutoff = new Date(Date.now() - options.hours * 3_600_000);
  const results = await backend.fetch(sources, cutoff);
  const articles = results.flatMap((r) => r.tweets);

  return { articles, results };
}
