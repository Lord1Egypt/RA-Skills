/**
 * PubMed Search API Client
 *
 * Searches full PubMed (db=pubmed, 30M+ articles),
 * retrieves abstracts via efetch for ALL articles,
 * auto-fetches full text via OAI-PMH for OA articles in PMC.
 *
 * No API key required — uses public NCBI E-utilities.
 */

const https = require('https');
const zlib = require('zlib');
const { URL } = require('url');

const EUTILS_BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils';
const OAI_BASE = 'https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/';
const IDCONV_BASE = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/';

// Rate limiting: NCBI ~3 req/s without API key
const NCBI_DELAY_MS = 400;
let lastRequestTime = 0;

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function rateLimitedGet(url) {
  const now = Date.now();
  const elapsed = now - lastRequestTime;
  if (elapsed < NCBI_DELAY_MS) {
    await sleep(NCBI_DELAY_MS - elapsed);
  }
  lastRequestTime = Date.now();
  return httpGet(url);
}

/**
 * HTTP GET with redirect following and gzip/deflate handling
 */
function httpGet(url, redirects = 0) {
  return new Promise((resolve, reject) => {
    if (redirects > 5) {
      reject(new Error('Too many redirects'));
      return;
    }

    const parsedUrl = new URL(url);
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'PubMed-Search/1.0 (research tool; contact via NCBI E-utilities guidelines)'
      }
    };

    https.get(options, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const location = res.headers.location;
        const redirectUrl = location.startsWith('http') ? location : new URL(location, parsedUrl.origin).href;
        return httpGet(redirectUrl, redirects + 1).then(resolve).catch(reject);
      }

      let stream = res;
      const encoding = res.headers['content-encoding'];
      if (encoding === 'gzip') {
        stream = res.pipe(zlib.createGunzip());
      } else if (encoding === 'deflate') {
        stream = res.pipe(zlib.createInflate());
      }

      let data = '';
      stream.on('data', chunk => data += chunk);
      stream.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data.substring(0, 200)}`));
        }
      });
      stream.on('error', reject);
    }).on('error', reject);
  });
}

// -------------------------------------------------------------------
// 1. SEARCH — PubMed (db=pubmed), covers ALL indexed articles
// -------------------------------------------------------------------

/**
 * Search PubMed for articles
 * @param {string} query  - PubMed query (full syntax supported)
 * @param {object} options - { year, retmax, retstart }
 * @returns {{ count: number, pmids: string[], query: string }}
 */
async function searchPubMed(query, options = {}) {
  const { year, retmax = 50, retstart = 0 } = options;

  let fullQuery = query;
  if (year) {
    fullQuery += ` AND ${year}[pdat]`;
  }

  const params = new URLSearchParams({
    db: 'pubmed',
    term: fullQuery,
    retmax,
    retstart,
    retmode: 'json',
    sort: 'pub_date',
    usehistory: 'n'
  });

  const url = `${EUTILS_BASE}/esearch.fcgi?${params}`;
  const data = await rateLimitedGet(url);
  const json = JSON.parse(data);

  const count = parseInt(json.esearchresult?.count || 0);
  const pmids = json.esearchresult?.idlist || [];

  return { count, pmids, query: fullQuery };
}

// -------------------------------------------------------------------
// 2. SUMMARIES — esummary (db=pubmed), metadata for any PMID
// -------------------------------------------------------------------

/**
 * Get article summaries from PubMed
 * @param {string[]} pmids - Array of PMIDs (strings)
 * @returns {object[]} Array of summary objects
 */
async function getSummaries(pmids) {
  if (pmids.length === 0) return [];

  const batchSize = 200;
  const results = [];

  for (let i = 0; i < pmids.length; i += batchSize) {
    const batch = pmids.slice(i, i + batchSize);

    const params = new URLSearchParams({
      db: 'pubmed',
      id: batch.join(','),
      retmode: 'json'
    });

    const url = `${EUTILS_BASE}/esummary.fcgi?${params}`;
    const data = await rateLimitedGet(url);
    const json = JSON.parse(data);

    const summaries = Object.entries(json.result || {})
      .filter(([key]) => key !== 'uids')
      .map(([uid, article]) => {
        const getAuthorList = () => {
          if (!article.authors) return 'N/A';
          return article.authors.map(a => a.name).filter(Boolean).join(', ') || 'N/A';
        };

        const getDOI = () => {
          const doiObj = article.articleids?.find(id => id.idtype === 'doi');
          return doiObj?.value || null;
        };

        const getPMCID = () => {
          const pmcObj = article.articleids?.find(id => id.idtype === 'pmc');
          return pmcObj ? `PMC${pmcObj.value}` : null;
        };

        return {
          pmid: uid,
          title: article.title || 'N/A',
          authors: getAuthorList(),
          journal: article.fulljournalname || article.source || 'N/A',
          pubdate: article.pubdate || article.sortpubdate || 'N/A',
          doi: getDOI(),
          pmcid: getPMCID(),
          elocationid: article.elocationid || null,
          pubtype: Array.isArray(article.pubtype) ? article.pubtype : [article.pubtype].filter(Boolean),
          url: `https://pubmed.ncbi.nlm.nih.gov/${uid}/`
        };
      });

    results.push(...summaries);
    await sleep(NCBI_DELAY_MS * 0.5); // extra breathing room between batches
  }

  return results;
}

// -------------------------------------------------------------------
// 3. PMID → PMCID CONVERSION
// -------------------------------------------------------------------

/**
 * Check if a PMID has a corresponding PMCID (i.e., available as OA full text)
 * @param {string|string[]} pmids - Single PMID or array
 * @returns {{ hasPMC: boolean, pmcid: string|null } | object[]}
 */
async function checkPMC(pmids) {
  const idList = Array.isArray(pmids) ? pmids : [pmids];
  const batchSize = 200;
  const allResults = [];

  for (let i = 0; i < idList.length; i += batchSize) {
    const batch = idList.slice(i, i + batchSize);

    const url = `${IDCONV_BASE}?ids=${batch.join(',')}&format=json`;
    const data = await httpGet(url); // idconv has looser rate limit, no need for rateLimitedGet

    try {
      const json = JSON.parse(data);
      const records = json.records || [];

      const results = batch.map(pmid => {
        const record = records.find(r => r.pmid === pmid || String(r.pmid) === String(pmid));
        return {
          pmid,
          hasPMC: !!(record && record.pmcid),
          pmcid: record?.pmcid ? (record.pmcid.startsWith('PMC') ? record.pmcid : `PMC${record.pmcid}`) : null,
          doi: record?.doi || null,
          versions: record?.versions || []
        };
      });

      allResults.push(...results);
    } catch (e) {
      // If conversion fails, return empty for this batch
      batch.forEach(pmid => {
        allResults.push({ pmid, hasPMC: false, pmcid: null, error: e.message });
      });
    }
  }

  return Array.isArray(pmids) ? allResults : allResults[0];
}

// -------------------------------------------------------------------
// 4. ABSTRACT — efetch (db=pubmed), works for ALL PMIDs
// -------------------------------------------------------------------

/**
 * Fetch structured abstract from PubMed via efetch
 * Works for ALL articles (not just OA). Returns parsed abstract + metadata.
 * @param {string} pmid - PubMed ID
 * @returns {object} { pmid, title, abstract, authors, journal, pubdate, doi, keywords, pmcid }
 */
async function fetchAbstract(pmid) {
  const params = new URLSearchParams({
    db: 'pubmed',
    id: pmid,
    rettype: 'abstract',
    retmode: 'xml'
  });

  const url = `${EUTILS_BASE}/efetch.fcgi?${params}`;
  const xml = await rateLimitedGet(url);

  return parsePubMedXML(xml, pmid);
}

/**
 * Parse PubMed efetch XML output
 */
function parsePubMedXML(xml, pmid) {
  // Article title
  const titleMatch = xml.match(/<ArticleTitle>(.*?)<\/ArticleTitle>/s);
  const title = stripXML(titleMatch?.[1]);

  // Abstract - structured: includes Background/Methods/Results/Conclusions labels
  const abstractMatch = xml.match(/<Abstract>(.*?)<\/Abstract>/s);
  let abstract = '';
  let abstractStructured = false;

  if (abstractMatch) {
    // Check if structured (has AbstractText with Label attributes)
    const sections = [...abstractMatch[1].matchAll(/<AbstractText[^>]*Label="([^"]*)"[^>]*>(.*?)<\/AbstractText>/gs)];
    if (sections.length > 0) {
      abstractStructured = true;
      abstract = sections.map(m => `**${m[1]}**: ${stripXML(m[2])}`).join('\n\n');
    } else {
      // Unstructured abstract
      const simpleMatch = [...abstractMatch[1].matchAll(/<AbstractText[^>]*>(.*?)<\/AbstractText>/gs)];
      if (simpleMatch.length > 0) {
        abstract = simpleMatch.map(m => stripXML(m[1])).join(' ');
      } else {
        abstract = stripXML(abstractMatch[1]);
      }
    }
  }

  // Authors
  const authorMatches = [...xml.matchAll(/<Author[^>]*>.*?<LastName>(.*?)<\/LastName>.*?<ForeName>(.*?)<\/ForeName>.*?<\/Author>/gs)];
  const authors = authorMatches.map(m => `${m[2]?.trim() || ''} ${m[1]?.trim() || ''}`.trim()).filter(Boolean);

  // Journal
  const journalMatch = xml.match(/<Title>(.*?)<\/Title>/);
  const journal = stripXML(journalMatch?.[1]);

  // PubDate
  const yearMatch = xml.match(/<PubDate>.*?<Year>(.*?)<\/Year>.*?<\/PubDate>/s);
  const monthMatch = xml.match(/<Month>(.*?)<\/Month>/);
  const dayMatch = xml.match(/<Day>(.*?)<\/Day>/);
  const year = yearMatch?.[1] || '';
  const month = monthMatch?.[1] || '';
  const day = dayMatch?.[1] || '';
  const pubdate = [year, month, day].filter(Boolean).join(' ');

  // DOI
  const doiMatch = xml.match(/<ArticleId IdType="doi">(.*?)<\/ArticleId>/);
  const doi = doiMatch?.[1] || null;

  // PMCID
  const pmcidMatch = xml.match(/<ArticleId IdType="pmc">(.*?)<\/ArticleId>/);
  const pmcid = pmcidMatch?.[1] ? (pmcidMatch[1].startsWith('PMC') ? pmcidMatch[1] : `PMC${pmcidMatch[1]}`) : null;

  // Keywords
  const keywordMatches = [...xml.matchAll(/<Keyword[^>]*>(.*?)<\/Keyword>/gs)];
  const keywords = keywordMatches.map(m => stripXML(m[1])).filter(Boolean);

  // Publication type
  const pubTypeMatches = [...xml.matchAll(/<PublicationType[^>]*>(.*?)<\/PublicationType>/gs)];
  const pubtypes = pubTypeMatches.map(m => stripXML(m[1])).filter(Boolean);

  // Language
  const langMatch = xml.match(/<Language>(.*?)<\/Language>/);
  const language = langMatch?.[1] || '';

  return {
    pmid,
    title: title || 'N/A',
    abstract: abstract || 'No abstract available',
    abstractStructured,
    authors: authors.length > 0 ? authors.join(', ') : 'N/A',
    journal: journal || 'N/A',
    pubdate: pubdate || 'N/A',
    doi,
    pmcid,
    keywords,
    pubtypes,
    language,
    url: `https://pubmed.ncbi.nlm.nih.gov/${pmid}/`
  };
}

// -------------------------------------------------------------------
// 5. FULL TEXT — OAI-PMH, for OA articles only
// -------------------------------------------------------------------

/**
 * Fetch full text from PMC OAI-PMH
 * @param {string} pmcid - PMC ID (e.g., "PMC12345678")
 * @returns {{ pmcid: string, available: boolean, xml?: string, reason?: string }}
 */
async function fetchFullText(pmcid) {
  const numericId = pmcid.replace(/^PMC/i, '');
  const identifier = `oai:pubmedcentral.nih.gov:${numericId}`;

  const params = new URLSearchParams({
    verb: 'GetRecord',
    identifier,
    metadataPrefix: 'pmc'
  });

  const url = `${OAI_BASE}?${params}`;
  const xml = await httpGet(url);

  if (xml.includes('<error code="cannotDisseminateFormat"')) {
    return { pmcid, available: false, reason: 'restricted (not open access)' };
  }
  if (xml.includes('<error')) {
    const match = xml.match(/<error[^>]*>(.*?)<\/error>/s);
    return { pmcid, available: false, reason: match?.[1] || 'unknown error' };
  }

  return { pmcid, available: true, xml };
}

/**
 * Parse JATS XML (PMC full text) to extract content
 */
function parseJATS(xml) {
  const strip = (s) => s?.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() || '';

  const titleMatch = xml.match(/<article-title[^>]*>(.*?)<\/article-title>/s);
  const abstractMatch = xml.match(/<abstract[^>]*>(.*?)<\/abstract>/s);
  const bodyMatch = xml.match(/<body[^>]*>(.*?)<\/body>/s);
  const keywordMatches = xml.matchAll(/<kwd[^>]*>(.*?)<\/kwd>/gs);
  const articleTypeMatch = xml.match(/<article[^>]*article-type="([^"]+)"/);

  return {
    title: strip(titleMatch?.[1]),
    abstract: strip(abstractMatch?.[1]),
    body: strip(bodyMatch?.[1]),
    keywords: [...keywordMatches].map(m => strip(m[1])).filter(Boolean),
    articleType: articleTypeMatch?.[1] || 'research'
  };
}

// -------------------------------------------------------------------
// 6. COMBINED FETCH — abstract + auto full-text fallback
// -------------------------------------------------------------------

/**
 * Fetch article from PubMed: always get abstract, try full text if OA
 * @param {string} pmid - PubMed ID
 * @returns {object} { pmid, abstract, fullText: { available, xml?, body? }, pmcid }
 */
async function fetchArticle(pmid) {
  // Step 1: Get structured abstract (works for ALL articles)
  const abstractData = await fetchAbstract(pmid);

  // Step 2: Check if PMC full text is available
  let fullText = { available: false, reason: 'not in PMC' };

  if (abstractData.pmcid) {
    // Already have PMCID from abstract XML
    fullText = await fetchFullText(abstractData.pmcid);
  } else {
    // Try ID converter
    const conv = await checkPMC(pmid);
    if (conv.hasPMC) {
      fullText = await fetchFullText(conv.pmcid);
      abstractData.pmcid = conv.pmcid;
    }
  }

  let body = null;
  if (fullText.available) {
    const parsed = parseJATS(fullText.xml);
    body = parsed.body;
    // Prefer JATS-parsed abstract over PubMed XML abstract
    if (parsed.abstract && parsed.abstract.length > abstractData.abstract.length) {
      abstractData.abstract = parsed.abstract;
    }
  }

  return {
    pmid,
    title: abstractData.title,
    abstract: abstractData.abstract,
    abstractStructured: abstractData.abstractStructured,
    authors: abstractData.authors,
    journal: abstractData.journal,
    pubdate: abstractData.pubdate,
    doi: abstractData.doi,
    pmcid: abstractData.pmcid,
    keywords: abstractData.keywords,
    pubtypes: abstractData.pubtypes,
    language: abstractData.language,
    url: abstractData.url,
    fullText: {
      available: fullText.available,
      body: body || null,
      reason: fullText.reason || null
    }
  };
}

// -------------------------------------------------------------------
// 7. BATCH OPERATIONS
// -------------------------------------------------------------------

/**
 * Batch search multiple journals
 * @param {object[]} journals - [{ name: string, query: string }]
 * @param {object} options - { year }
 * @returns {object[]} Array of article summary objects
 */
async function harvestJournals(journals, options = {}) {
  const { year } = options;
  const allArticles = [];

  for (const journal of journals) {
    const { pmids } = await searchPubMed(journal.query, { year, retmax: 500 });

    if (pmids.length > 0) {
      const summaries = await getSummaries(pmids);
      summaries.forEach(s => {
        allArticles.push({ ...s, journalKey: journal.name });
      });
    }

    await sleep(NCBI_DELAY_MS * 2); // extra gap between journals
  }

  return allArticles;
}

/**
 * Batch fetch abstracts for multiple PMIDs
 * @param {string[]} pmids
 * @returns {object[]}
 */
async function batchFetchAbstracts(pmids) {
  const results = [];
  for (const pmid of pmids) {
    try {
      const data = await fetchAbstract(pmid);
      results.push(data);
    } catch (e) {
      results.push({ pmid, error: e.message });
    }
  }
  return results;
}

// -------------------------------------------------------------------
// Helpers
// -------------------------------------------------------------------

function stripXML(str) {
  if (!str) return '';
  return str
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// -------------------------------------------------------------------
// Exports
// -------------------------------------------------------------------

module.exports = {
  // Core
  searchPubMed,
  getSummaries,
  fetchAbstract,
  fetchArticle,
  fetchFullText,
  checkPMC,

  // Parsing
  parsePubMedXML,
  parseJATS,

  // Batch
  harvestJournals,
  batchFetchAbstracts,

  // Low-level
  httpGet,
  rateLimitedGet
};
