/**
 * website-to-ads — OpenClaw Skill
 *
 * Scrape any business website → analyze the brand → generate 4-5
 * Meta-ready ad variants that match the brand's voice.
 */

import "dotenv/config";
import * as fs from "node:fs";
import * as path from "node:path";
import * as readline from "node:readline";
import * as crypto from "node:crypto";
import { scrapeWebsite } from "./scrape.js";
import { analyzeBrand } from "./analyze.js";
import { generateAds } from "./generate.js";
import { formatResult } from "./format.js";
import { isCivicAuthEnabled, verifyCivicToken } from "./auth.js";
import type {
  ScrapeResult,
  GeneratedAd,
  WebsiteToAdsResult,
  AdTone,
  BrandProfile,
  CachedBrand,
  NumberedAd,
  CivicAuthResult,
} from "./types.js";
import { AD_TONES } from "./types.js";

const CACHE_DIR = path.join(process.cwd(), ".cache");
const TOTAL_ADS = 5;

function getEnv(key: string): string {
  const val = process.env[key];
  if (!val) throw new Error(`Missing required env var: ${key}`);
  return val;
}

function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function cacheKey(url: string): string {
  const normalized = url.replace(/\/+$/, "").toLowerCase();
  return crypto.createHash("md5").update(normalized).digest("hex");
}

function loadCache(url: string): CachedBrand | null {
  const file = path.join(CACHE_DIR, `${cacheKey(url)}.json`);
  if (!fs.existsSync(file)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(file, "utf-8")) as CachedBrand;
    const age = Date.now() - new Date(data.cached_at).getTime();
    if (age > 24 * 60 * 60 * 1000) return null;
    return data;
  } catch {
    return null;
  }
}

function saveCache(url: string, brand: BrandProfile, content: string): void {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  const file = path.join(CACHE_DIR, `${cacheKey(url)}.json`);
  const data: CachedBrand = { url, brand, scraped_content: content, cached_at: new Date().toISOString() };
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

function distributeCounts(total: number, buckets: number): number[] {
  const base = Math.floor(total / buckets);
  const remainder = total % buckets;
  return Array.from({ length: buckets }, (_, i) => base + (i < remainder ? 1 : 0));
}

export async function scrape(args: {
  url: string;
  max_pages?: number;
}): Promise<ScrapeResult> {
  const apifyToken = getEnv("APIFY_TOKEN");
  return scrapeWebsite(args.url, apifyToken, args.max_pages ?? 3);
}

export async function generate(args: {
  website_content: string;
  url?: string;
  platform?: string;
  budget_hint?: string;
  tone?: AdTone;
}): Promise<{ brand: Record<string, unknown>; ads: GeneratedAd[] }> {
  const openaiKey = getEnv("OPENAI_API_KEY");
  const model = process.env.OPENAI_MODEL || "gpt-4o";

  const brand = await analyzeBrand(args.website_content, args.url || "unknown", openaiKey, model);
  const ads = await generateAds(brand, openaiKey, model, args.platform || "instagram", args.budget_hint, args.tone || "professional");

  return { brand: brand as unknown as Record<string, unknown>, ads };
}

export async function websiteToAds(args: {
  url: string;
  platform?: string;
  budget_hint?: string;
  max_pages?: number;
  tones?: AdTone[];
  civic_token?: string;
}): Promise<WebsiteToAdsResult> {
  const apifyToken = getEnv("APIFY_TOKEN");
  const openaiKey = getEnv("OPENAI_API_KEY");
  const model = process.env.OPENAI_MODEL || "gpt-4o";
  const tones = args.tones?.length ? args.tones : ["professional" as AdTone];

  let brand: BrandProfile;
  const cached = loadCache(args.url);

  if (cached) {
    console.log(`\n  ⚡ Using cached brand data for ${args.url}`);
    console.log(`     (cached ${new Date(cached.cached_at).toLocaleString()})\n`);
    brand = cached.brand;
  } else {
    console.log(`\n  🔍 Scraping ${args.url} (max ${args.max_pages ?? 3} pages)...`);
    const scraped = await scrapeWebsite(args.url, apifyToken, args.max_pages ?? 3);
    console.log(`  ✓ Scraped ${scraped.pages_crawled} pages.`);

    console.log(`  🧠 Analyzing brand...`);
    brand = await analyzeBrand(scraped.content, args.url, openaiKey, model);
    console.log(`  ✓ Brand: ${brand.brand_name} | Voice: ${brand.voice}`);

    saveCache(args.url, brand, scraped.content);
    console.log(`  💾 Cached for next run.\n`);
  }

  const counts = distributeCounts(TOTAL_ADS, tones.length);
  const allAds: NumberedAd[] = [];
  let globalNum = 1;

  for (let i = 0; i < tones.length; i++) {
    const tone = tones[i];
    const count = counts[i];
    const toneInfo = AD_TONES.find((t) => t.key === tone)!;

    console.log(`  ${toneInfo.emoji} Generating ${count} ${toneInfo.label.toLowerCase()} ad${count > 1 ? "s" : ""}...`);
    const ads = await generateAds(brand, openaiKey, model, args.platform || "instagram", args.budget_hint, tone, count);

    for (const ad of ads) {
      allAds.push({ ...ad, number: globalNum++, tone });
    }
    console.log(`  ✓ Done.`);
  }

  return { url: args.url, brand, ads: allAds, budget: args.budget_hint || "not specified" };
}

function exportForMeta(
  ads: NumberedAd[],
  verification?: CivicAuthResult
): Record<string, unknown> {
  return {
    generated_at: new Date().toISOString(),
    verified_by: verification && verification.verified
      ? {
          method: verification.method || "civic",
          user_id: verification.userId || null,
          display_name: verification.displayName || null,
        }
      : null,
    ads: ads.map((ad) => ({
      name: ad.hook,
      status: "PAUSED",
      creative: {
        title: ad.hook,
        body: ad.body,
        call_to_action_type: ad.cta.toUpperCase().replace(/\s+/g, "_"),
        link_data: { message: ad.body, call_to_action: { type: "LEARN_MORE" } },
      },
      targeting: ad.targeting,
      adset_schedule: ad.adset_schedule,
    })),
  };
}

// CLI entry point
if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  const args = process.argv.slice(2);
  const jsonFlag = args.includes("--json");
  const clearCache = args.includes("--no-cache");
  const url = args.find((a) => !a.startsWith("--"));

  if (!url) {
    console.error("Usage: npx tsx src/index.ts <url> [--json] [--no-cache]");
    process.exit(1);
  }

  (async () => {
    if (clearCache) {
      const file = path.join(CACHE_DIR, `${cacheKey(url)}.json`);
      if (fs.existsSync(file)) fs.unlinkSync(file);
      console.log("  🗑️  Cache cleared.");
    }

    console.log(`
╔═════════════════════════════════════════════════════════════════╗
║  WEBSITE → ADS                                                 
║  ${url}
╚═════════════════════════════════════════════════════════════════╝
`);

    const cached = loadCache(url);
    if (cached) {
      console.log(`  ⚡ Found cached brand data for: ${cached.brand.brand_name}`);
      console.log(`     (will skip scraping — use --no-cache to force refresh)\n`);
    }

    const budgetInput = await prompt("  💰 Budget (e.g. $200/week, $1000/month): ");
    const budget = budgetInput || undefined;

    console.log("\n  🎨 Choose ad tone(s) — comma-separate for mix (5 ads total):\n");
    for (let i = 0; i < AD_TONES.length; i++) {
      console.log(`     ${i + 1}. ${AD_TONES[i].emoji}  ${AD_TONES[i].label}`);
    }
    console.log();

    const toneInput = await prompt("  Your pick (e.g. 1,3 or 2): ");
    const toneIndices = toneInput
      .split(/[,\s]+/)
      .map((s) => parseInt(s, 10) - 1)
      .filter((i) => i >= 0 && i < AD_TONES.length);

    const tones: AdTone[] = toneIndices.length
      ? [...new Set(toneIndices.map((i) => AD_TONES[i].key))]
      : ["professional"];

    const toneLabels = tones.map((t) => {
      const info = AD_TONES.find((x) => x.key === t)!;
      return `${info.emoji}  ${info.label}`;
    });

    console.log(`\n  ✓ Budget: ${budget || "not specified"}`);
    console.log(`  ✓ Tones:  ${toneLabels.join(" + ")}`);
    console.log(`  ✓ Total:  5 ads\n`);

    const result = await websiteToAds({ url, budget_hint: budget, tones });

    if (jsonFlag) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(formatResult(result));
    }

    // Selection prompt
    const selection = await prompt("\n  🚀 Which ads to push to Meta? (e.g. 1,3,5 or 'all' or 'none'): ");

    if (selection.toLowerCase() === "none" || !selection) {
      console.log("\n  👋 No ads selected. Done!\n");
      return;
    }

    let selected: NumberedAd[];
    if (selection.toLowerCase() === "all") {
      selected = result.ads;
    } else {
      const nums = selection.split(/[,\s]+/).map((s) => parseInt(s, 10)).filter((n) => n >= 1 && n <= result.ads.length);
      selected = result.ads.filter((ad) => nums.includes(ad.number));
    }

    if (selected.length === 0) {
      console.log("\n  ⚠️  No valid ads selected. Done!\n");
      return;
    }

    let verification: CivicAuthResult | undefined;
    if (isCivicAuthEnabled()) {
      console.log("\n  🔐 Civic auth is enabled for Meta export.");
      const civicTokenFromEnv = process.env.CIVIC_ACCESS_TOKEN?.trim();
      const civicToken = civicTokenFromEnv
        ? civicTokenFromEnv
        : await prompt("  Enter your Civic token to continue: ");
      if (civicTokenFromEnv) {
        console.log("  ℹ️  Using CIVIC_ACCESS_TOKEN from environment.");
      }
      verification = await verifyCivicToken(civicToken);

      if (!verification.verified) {
        console.log(`\n  ❌ Civic verification failed: ${verification.reason || "Unknown error"}`);
        console.log("  Export blocked. Only authenticated users can push campaigns to Meta.\n");
        return;
      }

      console.log(
        `  ✅ Civic verified${verification.displayName ? ` as ${verification.displayName}` : ""}.`
      );
    }

    const metaPayload = exportForMeta(selected, verification);
    const outDir = path.join(process.cwd(), "output");
    fs.mkdirSync(outDir, { recursive: true });
    const outFile = path.join(outDir, `meta-ads-${Date.now()}.json`);
    fs.writeFileSync(outFile, JSON.stringify(metaPayload, null, 2));

    console.log(`\n  ✅ ${selected.length} ad${selected.length > 1 ? "s" : ""} exported for Meta:`);
    for (const ad of selected) {
      console.log(`     #${ad.number} "${ad.hook}"`);
    }
    console.log(`\n  📁 Saved to: ${outFile}`);
    console.log(`  💡 Import this JSON into Meta Ads Manager or use the Marketing API.\n`);
  })().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
