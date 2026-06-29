#!/usr/bin/env node
/**
 * PubMed Search CLI
 *
 * Search PubMed (db=pubmed) for articles,
 * retrieve abstracts for ALL articles,
 * auto-fetch full text for OA articles.
 *
 * Usage:
 *   node pubmed-search.js search --query "myasthenia gravis" --max 20
 *   node pubmed-search.js abstract --pmid 30311866
 *   node pubmed-search.js fetch --pmid 30311866
 *   node pubmed-search.js test
 */

const pubmed = require('../lib/api.js');

// ANSI
const c = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  blue: '\x1b[34m',
  dim: '\x1b[2m',
  bold: '\x1b[1m',
  reset: '\x1b[0m',
};

function log(msg, color = 'reset') {
  console.log(`${c[color]}${msg}${c.reset}`);
}

function error(msg) {
  console.error(`${c.red}Error: ${msg}${c.reset}`);
  process.exit(1);
}

function printUsage() {
  console.log(`
${c.cyan}${c.bold}PubMed Search${c.reset} — Search 30M+ PubMed articles, abstracts for all, full text for OA

${c.yellow}Commands:${c.reset}
  search     Search PubMed by query
  abstract   Get structured abstract for a PMID
  fetch      Full fetch: abstract + auto full-text if OA
  test       Run test with sample query

${c.yellow}Options:${c.reset}
  --query <text>    PubMed query (full syntax supported)
  --pmid <id>       PubMed ID  
  --year <year>     Filter by publication year
  --max <n>         Max results (default: 50)
  --offset <n>      Pagination offset (default: 0)
  --full            Include full abstract text in search results

${c.yellow}Examples:${c.reset}
  node pubmed-search.js search --query "myasthenia gravis thymus" --max 20
  node pubmed-search.js search --query "IFN alpha AND thymic" --year 2023 --full
  node pubmed-search.js abstract --pmid 30311866
  node pubmed-search.js fetch --pmid 35480500
`);
}

// Parse command-line options
function parseArgs(args) {
  const getOpt = (name) => {
    const idx = args.indexOf(name);
    return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null;
  };
  const hasFlag = (name) => args.includes(name);
  return { getOpt, hasFlag };
}

async function cmdSearch(subArgs) {
  const { getOpt, hasFlag } = parseArgs(subArgs);

  const query = getOpt('--query');
  if (!query) error('--query required');

  const year = getOpt('--year');
  const max = parseInt(getOpt('--max') || '50');
  const offset = parseInt(getOpt('--offset') || '0');
  const showFull = hasFlag('--full');

  log(`\n${c.bold}Searching PubMed:${c.reset} ${c.cyan}${query}${c.reset}${year ? ` (${year})` : ''}`, 'cyan');
  log(`${c.dim}  Database: pubmed (30M+ articles)${c.reset}`);

  const result = await pubmed.searchPubMed(query, {
    year: year ? parseInt(year) : null,
    retmax: max,
    retstart: offset
  });

  log(`\n${c.bold}Results: ${result.count.toLocaleString()} total${c.reset}`, 'yellow');
  log(`  Showing ${result.pmids.length} (offset ${offset})\n`);

  if (result.pmids.length === 0) {
    log('No articles found.', 'dim');
    return;
  }

  // Get summaries
  const summaries = await pubmed.getSummaries(result.pmids);

  for (let i = 0; i < summaries.length; i++) {
    const s = summaries[i];
    const idx = offset + i + 1;
    const oaMark = s.pmcid ? ` ${c.green}[OA]${c.reset}` : '';

    console.log(`  ${c.bold}${idx}.${c.reset} ${c.yellow}[PMID:${s.pmid}]${c.reset}${oaMark} ${s.title?.substring(0, 80)}`);
    console.log(`     ${c.dim}${s.journal} | ${s.pubdate} | ${s.authors?.substring(0, 50)}${c.reset}`);

    if (s.doi) {
      console.log(`     ${c.dim}DOI: ${s.doi}${c.reset}`);
    }

    // Fetch abstract if --full flag
    if (showFull) {
      try {
        const abstractData = await pubmed.fetchAbstract(s.pmid);
        const preview = abstractData.abstract?.substring(0, 300) || '';
        if (preview) {
          console.log(`     ${c.dim}${preview}...${c.reset}`);
        }
      } catch (e) {
        // Skip abstract if fetch fails
      }
    }

    console.log('');
  }

  // Summary stats
  const oaCount = summaries.filter(s => s.pmcid).length;
  log(`${c.bold}Summary:${c.reset} ${oaCount}/${summaries.length} articles available as OA full text`, 'blue');
  log(`  OA articles can be retrieved with: node pubmed-search.js fetch --pmid <PMID>\n`, 'dim');
}

async function cmdAbstract(subArgs) {
  const { getOpt } = parseArgs(subArgs);
  const pmid = getOpt('--pmid');
  if (!pmid) error('--pmid required');

  log(`\n${c.bold}Fetching abstract:${c.reset} PMID:${pmid}`, 'cyan');

  try {
    const data = await pubmed.fetchAbstract(pmid);

    log(`\n${c.bold}${c.cyan}${data.title}${c.reset}`, 'bold');
    log(`${c.dim}${data.authors}${c.reset}`);
    log(`${c.dim}${data.journal} | ${data.pubdate}${c.reset}`);
    if (data.doi) log(`${c.dim}DOI: ${data.doi}${c.reset}`);
    log(`${c.dim}URL: ${data.url}${c.reset}`);

    if (data.keywords.length > 0) {
      log(`\n${c.yellow}Keywords:${c.reset} ${data.keywords.join(', ')}`);
    }

    if (data.pubtypes.length > 0) {
      log(`${c.dim}Type: ${data.pubtypes.join(', ')}${c.reset}`);
    }

    log(`\n${c.bold}Abstract ${data.abstractStructured ? '(structured)' : ''}:${c.reset}`);
    console.log(data.abstract);

    if (data.pmcid) {
      log(`\n${c.green}Full text available via PMC: ${data.pmcid}${c.reset}`);
      log(`${c.dim}  Use: node pubmed-search.js fetch --pmid ${pmid}${c.reset}`);
    } else {
      log(`\n${c.yellow}Full text NOT available (non-OA article)${c.reset}`);
      log(`${c.dim}  Try publisher link or institutional access for full text.${c.reset}`);
    }
  } catch (e) {
    error(`Failed to fetch abstract: ${e.message}`);
  }
}

async function cmdFetch(subArgs) {
  const { getOpt } = parseArgs(subArgs);
  const pmid = getOpt('--pmid');
  if (!pmid) error('--pmid required');

  log(`\n${c.bold}Fetching article:${c.reset} PMID:${pmid}`, 'cyan');

  try {
    const article = await pubmed.fetchArticle(pmid);

    // Header
    log(`\n${c.bold}${c.cyan}${article.title}${c.reset}`);
    log(`${c.dim}${article.authors}${c.reset}`);
    log(`${c.dim}${article.journal} | ${article.pubdate}${c.reset}`);
    if (article.doi) log(`${c.dim}DOI: ${article.doi}${c.reset}`);
    log(`${c.dim}URL: ${article.url}${c.reset}`);

    if (article.keywords.length > 0) {
      log(`\n${c.yellow}Keywords:${c.reset} ${article.keywords.join(', ')}`);
    }
    if (article.pubtypes.length > 0) {
      log(`${c.dim}Type: ${article.pubtypes.join(', ')}${c.reset}`);
    }
    if (article.language && article.language !== 'eng') {
      log(`${c.dim}Language: ${article.language}${c.reset}`);
    }

    // Abstract
    log(`\n${c.bold}Abstract ${article.abstractStructured ? '(structured)' : ''}:${c.reset}`);
    console.log(article.abstract);

    // Full text status
    if (article.fullText.available) {
      const charCount = (article.fullText.body?.length || 0).toLocaleString();
      log(`\n${c.green}${c.bold}✓ Full text available (${article.pmcid})${c.reset} — ${charCount} characters`);
    } else {
      log(`\n${c.yellow}✗ Full text not available${c.reset} — ${article.fullText.reason || 'not in PMC'}`);
      log(`${c.dim}  Only abstract is available. Try publisher site or institutional access.${c.reset}`);
    }
  } catch (e) {
    error(`Failed: ${e.message}`);
  }
}

async function cmdTest() {
  log(`\n${c.bold}${c.cyan}PubMed Search Test${c.reset}`, 'cyan');
  log(`${c.dim}  Database: PubMed (30M+ articles)${c.reset}\n`);

  // Test 1: Search
  log(`${c.bold}Test 1:${c.reset} Search "myasthenia gravis thymus"`);
  try {
    const result = await pubmed.searchPubMed('myasthenia gravis thymus', { retmax: 5 });
    log(`  ${c.green}OK${c.reset} — ${result.count.toLocaleString()} total, ${result.pmids.length} returned`);

    if (result.pmids.length > 0) {
      // Test 2: Summaries
      log(`\n${c.bold}Test 2:${c.reset} Get summaries for ${result.pmids.length} PMIDs`);
      const summaries = await pubmed.getSummaries(result.pmids);
      const oaCount = summaries.filter(s => s.pmcid).length;
      log(`  ${c.green}OK${c.reset} — ${summaries.length} summaries, ${oaCount}/${summaries.length} OA`);

      summaries.forEach((s, i) => {
        const oaTag = s.pmcid ? ' [OA]' : '';
        console.log(`    ${i + 1}. PMID:${s.pmid}${oaTag} - ${s.title?.substring(0, 50)}...`);
      });

      // Test 3: Abstract for first PMID
      const firstPmid = summaries[0].pmid;
      log(`\n${c.bold}Test 3:${c.reset} Fetch abstract for PMID:${firstPmid}`);
      const abstractData = await pubmed.fetchAbstract(firstPmid);
      log(`  ${c.green}OK${c.reset} — ${abstractData.title?.substring(0, 60)}`);
      const abPreview = abstractData.abstract?.substring(0, 150) || '';
      console.log(`    ${c.dim}${abPreview}...${c.reset}`);

      // Test 4: Check PMC availability for all
      log(`\n${c.bold}Test 4:${c.reset} Check PMC availability`);
      const pmcChecks = await pubmed.checkPMC(result.pmids);
      pmcChecks.forEach(check => {
        const status = check.hasPMC ? `${c.green}OA${c.reset}` : `${c.dim}abstract only${c.reset}`;
        console.log(`    PMID:${check.pmid} → ${status}${check.pmcid ? ` (${check.pmcid})` : ''}`);
      });

      // Test 5: Full fetch for an OA article
      const oaArticle = pmcChecks.find(c => c.hasPMC);
      if (oaArticle) {
        log(`\n${c.bold}Test 5:${c.reset} Full fetch for OA article PMID:${oaArticle.pmid}`);
        const article = await pubmed.fetchArticle(oaArticle.pmid);
        const bodyChars = (article.fullText.body?.length || 0).toLocaleString();
        log(`  ${c.green}OK${c.reset} — Full text: ${bodyChars} chars, Abstract: ${article.abstract.length} chars`);
      }

      // Test 6: Abstract for non-OA article (if exists)
      const nonOA = pmcChecks.find(c => !c.hasPMC);
      if (nonOA) {
        log(`\n${c.bold}Test 6:${c.reset} Abstract for non-OA article PMID:${nonOA.pmid}`);
        const nonOAData = await pubmed.fetchAbstract(nonOA.pmid);
        log(`  ${c.green}OK${c.reset} — "${nonOAData.title?.substring(0, 60)}"`);
        console.log(`    Abstract: ${nonOAData.abstract?.substring(0, 100)}...`);
      }
    }
  } catch (e) {
    log(`  ${c.red}FAIL${c.reset} — ${e.message}`, 'red');
  }

  log(`\n${c.green}${c.bold}All tests completed.${c.reset}\n`, 'green');
}

// -------------------------------------------------------------------
// Main
// -------------------------------------------------------------------

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printUsage();
    process.exit(0);
  }

  const command = args[0];
  const subArgs = args.slice(1);

  try {
    switch (command) {
      case 'search':
        await cmdSearch(subArgs);
        break;
      case 'abstract':
        await cmdAbstract(subArgs);
        break;
      case 'fetch':
        await cmdFetch(subArgs);
        break;
      case 'test':
        await cmdTest();
        break;
      default:
        error(`Unknown command: ${command}\nUse --help for usage.`);
    }
  } catch (e) {
    error(e.message);
  }
}

main();
