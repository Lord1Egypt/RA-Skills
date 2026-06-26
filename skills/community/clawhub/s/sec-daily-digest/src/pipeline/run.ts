import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { createProvider } from "../ai/providers/factory";
import type { AIProvider } from "../ai/providers/types";
import { applyArchivePenalty, dedupeByUrl, filterByHours } from "../articles/normalize";
import { enrichArticles } from "../articles/enrich";
import { readRecentArchive, writeArchiveEntry, cleanOldArchive } from "../archive/store";
import { loadConfig } from "../config/load";
import { loadSourcesConfig, getTwitterSources } from "../config/sources";
import { sendEmailViaGog } from "../delivery/email";
import { loadHealthStore, saveHealthStore, recordSourceResult, getUnhealthySources } from "../health/store";
import { mergeVulnerabilityItems } from "../merge/vuln";
import { parseOpmlFeeds } from "../opml/parse";
import { syncOpml } from "../opml/sync";
import { renderDigest } from "../report/markdown";
import { fetchAllFeeds, type FeedSource } from "../rss/fetch";
import type { Article } from "../rss/parse";
import { fetchTwitterKols } from "../twitter/fetch";
import type { TwitterSourceResult } from "../twitter/backends/types";
import { generateTrendHighlights } from "./stages/highlights";
import { scoreAndClassifyArticles } from "./stages/scoring";
import { summarizeSelectedArticles } from "./stages/summary";
import type { FinalArticle, ScoredArticle } from "./types";

export interface RunPipelineOptions {
  provider?: "openai" | "gemini" | "claude" | "ollama";
  opmlProfile?: "tiny" | "full";
  hours?: number;
  topN?: number;
  outputPath?: string;
  dryRun?: boolean;
  env?: NodeJS.ProcessEnv;
  now?: Date;
  fetcher?: typeof fetch;
  seedArticles?: Article[];
  twitterEnabled?: boolean;
  seedTwitterResults?: TwitterSourceResult[];
  enrich?: boolean;
  emailTo?: string;
}

export interface RunPipelineResult {
  outputPath: string;
  counters: {
    feeds: number;
    articles: number;
    recent: number;
    selected: number;
    vulnerabilities: number;
    twitter_kols: number;
  };
  usedCache: boolean;
  provider: string;
}

function toDateString(date: Date): string {
  return date.toISOString().slice(0, 10);
}

function splitByFocus<T extends { security: number; ai: number; score: number }>(items: T[]): { ai: T[]; security: T[] } {
  const ai: T[] = [];
  const security: T[] = [];

  for (const item of items) {
    if (item.security >= item.ai) {
      security.push(item);
    } else {
      ai.push(item);
    }
  }

  ai.sort((a, b) => b.score - a.score);
  security.sort((a, b) => b.score - a.score);
  return { ai, security };
}

function normalizeWeights(weights: { security: number; ai: number }): { security: number; ai: number } {
  const security = Math.max(0, weights.security);
  const ai = Math.max(0, weights.ai);
  const total = security + ai;
  if (total <= 0) {
    return { security: 0.5, ai: 0.5 };
  }
  return {
    security: security / total,
    ai: ai / total,
  };
}

function pickBalanced<T extends { security: number; ai: number; score: number }>(
  items: T[],
  topN: number,
  weights: { security: number; ai: number },
): { ai: T[]; security: T[]; selected: T[] } {
  const { ai, security } = splitByFocus(items);
  const normalized = normalizeWeights(weights);

  const secQuota = Math.max(0, Math.min(topN, Math.floor(topN * normalized.security)));
  const aiQuota = Math.max(0, Math.min(topN, Math.floor(topN * normalized.ai)));

  const pickedAi = ai.slice(0, aiQuota);
  const pickedSec = security.slice(0, secQuota);
  const selected: T[] = [...pickedAi, ...pickedSec];

  if (selected.length < topN) {
    const extras = items
      .filter((item) => !selected.includes(item))
      .sort((a, b) => b.score - a.score)
      .slice(0, topN - selected.length);
    selected.push(...extras);
  }

  const rebucket = splitByFocus(selected);
  return {
    ai: rebucket.ai,
    security: rebucket.security,
    selected,
  };
}

async function loadArticles(options: Required<Pick<RunPipelineOptions, "env">> & {
  profile: "tiny" | "full";
  fetcher: typeof fetch;
  seedArticles?: Article[];
}): Promise<{ articles: Article[]; feedsCount: number; usedCache: boolean; feedResults: Array<{ id: string; name: string; ok: boolean }> }> {
  if (options.seedArticles && options.seedArticles.length > 0) {
    return {
      articles: options.seedArticles,
      feedsCount: 0,
      usedCache: false,
      feedResults: [],
    };
  }

  const syncResult = await syncOpml({
    profile: options.profile,
    env: options.env,
    fetcher: options.fetcher,
  });
  const opmlXml = await readFile(syncResult.opmlPath, "utf8");
  const feeds: FeedSource[] = parseOpmlFeeds(opmlXml);
  const { articles, results: feedResults } = await fetchAllFeeds(feeds, { fetcher: options.fetcher });

  return {
    articles,
    feedsCount: feeds.length,
    usedCache: syncResult.usedCache,
    feedResults,
  };
}

export async function runPipeline(options: RunPipelineOptions = {}): Promise<RunPipelineResult> {
  const env = options.env ?? process.env;
  const now = options.now ?? new Date();
  const twitterEnabled = options.twitterEnabled !== false;

  const config = await loadConfig(
    {
      provider: options.provider,
      opml_profile: options.opmlProfile,
      time_range_hours: options.hours,
      top_n: options.topN,
    },
    env,
  );

  // Load sources config for Twitter KOLs
  const sourcesConfig = await loadSourcesConfig(env);
  const twitterSources = getTwitterSources(sourcesConfig);

  // Step 1: parallel RSS fetch + Twitter fetch
  const [articlesResult, twitterResult] = await Promise.all([
    loadArticles({
      env,
      profile: config.opml_profile === "full" ? "full" : "tiny",
      fetcher: options.fetcher ?? fetch,
      seedArticles: options.seedArticles,
    }),
    twitterEnabled && !options.seedTwitterResults
      ? fetchTwitterKols(twitterSources, {
          hours: config.time_range_hours,
          env,
          fetcher: options.fetcher,
        })
      : Promise.resolve({
          articles: options.seedTwitterResults?.flatMap((r) => r.tweets) ?? [],
          results: options.seedTwitterResults ?? [],
        }),
  ]);

  // Merge all articles
  const allArticles: Article[] = [...articlesResult.articles, ...twitterResult.articles];

  // Step 2: time filter
  const deduped = dedupeByUrl(allArticles).map((item) => ({
    ...item,
    link: item.link,
  }));
  const recent = filterByHours(deduped, config.time_range_hours, now);

  // Archive dedup: read previous N days
  const seenUrls = await readRecentArchive(env, 7);

  // Enrich articles if requested
  const enriched = options.enrich
    ? await enrichArticles(recent, { fetcher: options.fetcher ?? fetch })
    : recent;

  let provider: AIProvider | null = null;
  if (!options.dryRun) {
    try {
      provider = createProvider(config.provider, env, options.fetcher ?? fetch);
    } catch (error) {
      console.warn(`[pipeline] provider init failed, using rule fallback: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  // Step 3: AI scoring + classification
  const scored = await scoreAndClassifyArticles({
    articles: enriched,
    provider,
    weights: config.weights,
  });

  // Apply archive penalty (seen articles get -5 score)
  const penalized = applyArchivePenalty(scored, seenUrls);

  penalized.sort((a, b) => b.score - a.score);
  const balancedScored = pickBalanced<ScoredArticle>(penalized, config.top_n, config.weights);

  // Step 4: AI summary + translation
  const summarizedSelected = await summarizeSelectedArticles({
    articles: balancedScored.selected,
    provider,
    lang: "zh",
  });

  const balancedFinal = splitByFocus<FinalArticle>(summarizedSelected);

  // Step 5: trend highlights
  const highlights = await generateTrendHighlights({
    articles: summarizedSelected,
    provider,
    lang: "zh",
  });

  const vulnerabilities = mergeVulnerabilityItems(
    balancedFinal.security
      .filter((item) => item.security >= 6 || /CVE-\d{4}-\d{4,7}/i.test(`${item.title} ${item.description}`))
      .map((item) => ({
        title: item.title,
        summary: item.summaryZh || item.description,
        link: item.link,
        source: item.sourceName,
      })),
  );

  // Health tracking
  const healthStore = await loadHealthStore(env);
  for (const feedResult of articlesResult.feedResults) {
    recordSourceResult(healthStore, feedResult.id, feedResult.name, feedResult.ok);
  }
  for (const twitterRes of twitterResult.results) {
    recordSourceResult(healthStore, twitterRes.sourceId, twitterRes.handle, twitterRes.status === "ok");
  }
  await saveHealthStore(healthStore, env);
  const unhealthyNames = getUnhealthySources(healthStore);

  // KOL entries for render (all fetched tweets, unfiltered by top_n)
  const kolEntries = twitterResult.articles.map((a) => ({
    displayName: a.displayName,
    handle: a.handle,
    text: a.text ?? a.title,
    link: a.link,
    tweetId: a.tweetId,
    metrics: a.metrics,
  }));

  const dateStr = toDateString(now);
  const report = renderDigest({
    date: dateStr,
    highlights,
    ai: balancedFinal.ai.map((item) => ({
      titleZh: item.titleZh,
      title: item.title,
      link: item.link,
      summaryZh: item.summaryZh,
      reasonZh: item.reasonZh,
      category: item.category,
      keywords: item.keywords,
      score: item.score,
      sourceName: item.sourceName,
    })),
    security: balancedFinal.security.map((item) => ({
      titleZh: item.titleZh,
      title: item.title,
      link: item.link,
      summaryZh: item.summaryZh,
      reasonZh: item.reasonZh,
      category: item.category,
      keywords: item.keywords,
      score: item.score,
      sourceName: item.sourceName,
    })),
    vulnerabilities,
    kols: kolEntries,
    healthWarnings: unhealthyNames,
  });

  const outputPath = options.outputPath ?? `./output/sec-digest-${dateStr.replace(/-/g, "")}.md`;
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, report, "utf8");

  // Write archive + clean old
  await writeArchiveEntry(
    summarizedSelected.map((a) => ({ title: a.title, link: a.link, date: dateStr })),
    dateStr,
    env,
  );
  await cleanOldArchive(env, 90);

  // Email delivery
  const emailTo = options.emailTo;
  if (emailTo) {
    const body = await readFile(outputPath, "utf8");
    const emailResult = await sendEmailViaGog({
      to: emailTo,
      subject: `sec-daily-digest ${dateStr}`,
      body,
    });
    if (emailResult.ok) {
      console.log(`[sec-digest] email=sent to ${emailTo}`);
    } else {
      console.log(`[sec-digest] email=failed: ${emailResult.error}`);
    }
  }

  return {
    outputPath,
    counters: {
      feeds: articlesResult.feedsCount,
      articles: allArticles.length,
      recent: recent.length,
      selected: summarizedSelected.length,
      vulnerabilities: vulnerabilities.length,
      twitter_kols: twitterResult.articles.length,
    },
    usedCache: articlesResult.usedCache,
    provider: config.provider,
  };
}
