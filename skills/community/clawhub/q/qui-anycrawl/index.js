// AnyCrawl Skill - powered by SkillBoss API Hub
// Scrape, Crawl, and Search web content via https://api.heybossai.com/v1/pilot

const API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.heybossai.com/v1";

async function pilot(body) {
  if (!API_KEY) {
    throw new Error(
      "SKILLBOSS_API_KEY not found!\n\n" +
      "Please set your API key:\n" +
      "export SKILLBOSS_API_KEY=\"your-key\"\n\n" +
      "Get your API key at: https://heybossai.com"
    );
  }

  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  const data = await r.json();

  if (!r.ok) {
    throw new Error(`SkillBoss API Error: ${data.error || data.message || r.statusText}`);
  }

  return data;
}

/**
 * Scrape a single URL and convert to LLM-ready structured data
 *
 * @param {Object} params
 * @param {string} params.url - URL to scrape (required)
 * @param {string} params.engine - Scraping engine: 'cheerio' (default), 'playwright', 'puppeteer'
 * @param {Array} params.formats - Output formats: ['markdown'], ['html'], ['text'], ['json'], ['screenshot'], etc.
 * @param {number} params.timeout - Timeout in milliseconds (default: 30000)
 * @param {number} params.wait_for - Delay before extraction in ms (browser engines only)
 * @param {string|Object|Array} params.wait_for_selector - Wait for CSS selectors
 * @param {Array} params.include_tags - Include only these HTML tags
 * @param {Array} params.exclude_tags - Exclude these HTML tags
 * @param {string} params.proxy - Proxy URL (http://proxy:port)
 * @param {Object} params.json_options - JSON extraction options with schema and prompt
 * @param {string} params.extract_source - Source for JSON extraction: 'markdown' (default) or 'html'
 *
 * @returns {Promise<Object>} Scraped content in requested formats
 */
export async function anycrawl_scrape({
  url,
  engine = "cheerio",
  formats = ["markdown"],
  timeout,
  wait_for,
  wait_for_selector,
  include_tags,
  exclude_tags,
  proxy,
  json_options,
  extract_source
}) {
  if (!url) {
    throw new Error("URL is required");
  }

  const inputs = { url, engine, formats };

  if (timeout !== undefined) inputs.timeout = timeout;
  if (wait_for !== undefined) inputs.wait_for = wait_for;
  if (wait_for_selector !== undefined) inputs.wait_for_selector = wait_for_selector;
  if (include_tags !== undefined) inputs.include_tags = include_tags;
  if (exclude_tags !== undefined) inputs.exclude_tags = exclude_tags;
  if (proxy !== undefined) inputs.proxy = proxy;
  if (json_options !== undefined) inputs.json_options = json_options;
  if (extract_source !== undefined) inputs.extract_source = extract_source;

  const result = await pilot({ type: "scraping", inputs, prefer: "balanced" });
  return result.result;
}

/**
 * Search Google and return structured results
 *
 * @param {Object} params
 * @param {string} params.query - Search query string (required)
 * @param {string} params.engine - Search engine: 'google' (default)
 * @param {number} params.limit - Max results per page (default: 10)
 * @param {number} params.offset - Number of results to skip (default: 0)
 * @param {number} params.pages - Number of pages to retrieve (default: 1, max: 20)
 * @param {string} params.lang - Language locale (e.g., 'en', 'zh', 'vi', default: 'en')
 * @param {number} params.safe_search - Safe search: 0 (off), 1 (medium), 2 (high)
 * @param {Object} params.scrape_options - Optional: scrape each result URL with these options
 *
 * @returns {Promise<Object>} Search results and suggestions
 */
export async function anycrawl_search({
  query,
  engine = "google",
  limit,
  offset,
  pages,
  lang,
  safe_search,
  scrape_options
}) {
  if (!query) {
    throw new Error("Query is required");
  }

  const inputs = { query };

  if (engine !== undefined) inputs.engine = engine;
  if (limit !== undefined) inputs.limit = limit;
  if (offset !== undefined) inputs.offset = offset;
  if (pages !== undefined) inputs.pages = pages;
  if (lang !== undefined) inputs.lang = lang;
  if (safe_search !== undefined) inputs.safe_search = safe_search;
  if (scrape_options !== undefined) inputs.scrape_options = scrape_options;

  const result = await pilot({ type: "search", inputs, prefer: "balanced" });
  return result.result;
}

/**
 * Start a crawl job for an entire website
 *
 * @param {Object} params
 * @param {string} params.url - Seed URL to start crawling (required)
 * @param {string} params.engine - Scraping engine: 'cheerio' (default), 'playwright', 'puppeteer'
 * @param {string} params.strategy - Crawl scope: 'all', 'same-domain' (default), 'same-hostname', 'same-origin'
 * @param {number} params.max_depth - Max depth from seed URL (default: 10)
 * @param {number} params.limit - Max pages to crawl (default: 100)
 * @param {Array} params.include_paths - Path patterns to include (glob-like)
 * @param {Array} params.exclude_paths - Path patterns to exclude (glob-like)
 * @param {Array} params.scrape_paths - Only scrape URLs matching these patterns
 * @param {Object} params.scrape_options - Per-page scrape options
 *
 * @returns {Promise<Object>} Job ID and status
 */
export async function anycrawl_crawl_start({
  url,
  engine = "cheerio",
  strategy = "same-domain",
  max_depth,
  limit,
  include_paths,
  exclude_paths,
  scrape_paths,
  scrape_options
}) {
  if (!url) {
    throw new Error("URL is required");
  }

  const inputs = { url, engine, strategy, crawl: true };

  if (max_depth !== undefined) inputs.max_depth = max_depth;
  if (limit !== undefined) inputs.limit = limit;
  if (include_paths !== undefined) inputs.include_paths = include_paths;
  if (exclude_paths !== undefined) inputs.exclude_paths = exclude_paths;
  if (scrape_paths !== undefined) inputs.scrape_paths = scrape_paths;
  if (scrape_options !== undefined) inputs.scrape_options = scrape_options;

  const result = await pilot({ type: "scraping", inputs, prefer: "balanced" });
  return result.result;
}

/**
 * Get crawl job status
 *
 * @param {Object} params
 * @param {string} params.job_id - Crawl job ID (required)
 *
 * @returns {Promise<Object>} Job status, progress, and stats
 */
export async function anycrawl_crawl_status({ job_id }) {
  if (!job_id) {
    throw new Error("Job ID is required");
  }

  const result = await pilot({ type: "scraping", inputs: { job_id, action: "status" }, prefer: "balanced" });
  return result.result;
}

/**
 * Get crawl results (paginated)
 *
 * @param {Object} params
 * @param {string} params.job_id - Crawl job ID (required)
 * @param {number} params.skip - Number of results to skip (default: 0)
 *
 * @returns {Promise<Object>} Crawled pages with content
 */
export async function anycrawl_crawl_results({ job_id, skip = 0 }) {
  if (!job_id) {
    throw new Error("Job ID is required");
  }

  const result = await pilot({ type: "scraping", inputs: { job_id, action: "results", skip }, prefer: "balanced" });
  return result.result;
}

/**
 * Cancel a crawl job
 *
 * @param {Object} params
 * @param {string} params.job_id - Crawl job ID (required)
 *
 * @returns {Promise<Object>} Cancellation confirmation
 */
export async function anycrawl_crawl_cancel({ job_id }) {
  if (!job_id) {
    throw new Error("Job ID is required");
  }

  const result = await pilot({ type: "scraping", inputs: { job_id, action: "cancel" }, prefer: "balanced" });
  return result.result;
}

/**
 * Quick search and scrape - Search Google then scrape top results
 *
 * @param {Object} params
 * @param {string} params.query - Search query (required)
 * @param {number} params.max_results - Max results to scrape (default: 3)
 * @param {string} params.scrape_engine - Engine for scraping: 'cheerio' (default) or 'playwright'
 * @param {Array} params.formats - Output formats for scraped content
 * @param {string} params.lang - Search language
 *
 * @returns {Promise<Object>} Search results with scraped content
 */
export async function anycrawl_search_and_scrape({
  query,
  max_results = 3,
  scrape_engine = "cheerio",
  formats = ["markdown"],
  lang
}) {
  if (!query) {
    throw new Error("Query is required");
  }

  // First, search
  const searchInputs = { query, limit: max_results };
  if (lang) searchInputs.lang = lang;

  const searchResult = await pilot({ type: "search", inputs: searchInputs, prefer: "balanced" });
  const searchData = searchResult.result;

  if (!searchData) {
    return searchResult.data;
  }

  // Filter only web results (not suggestions)
  const webResults = Array.isArray(searchData)
    ? searchData.filter(r => r.url && r.category === "web")
    : [];

  // Scrape top results
  const scrapedResults = [];
  for (const result of webResults.slice(0, max_results)) {
    try {
      const scrapeResult = await pilot({
        type: "scraping",
        inputs: { url: result.url, engine: scrape_engine, formats },
        prefer: "balanced"
      });

      scrapedResults.push({
        ...result,
        scraped: scrapeResult.result,
        scrape_error: null
      });
    } catch (error) {
      scrapedResults.push({
        ...result,
        scraped: null,
        scrape_error: error.message
      });
    }
  }

  return {
    success: true,
    query,
    search_results: searchData,
    scraped_results: scrapedResults
  };
}

// Export all functions for OpenClaw
export default {
  anycrawl_scrape,
  anycrawl_search,
  anycrawl_crawl_start,
  anycrawl_crawl_status,
  anycrawl_crawl_results,
  anycrawl_crawl_cancel,
  anycrawl_search_and_scrape
};
