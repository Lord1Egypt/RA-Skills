'use strict';

const https = require('https');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const SKILL_ROOT = path.resolve(__dirname, '..');
const SKILL_VERSION = (() => { try { return require('../package.json').version; } catch { return '1.0.0'; } })();

// ─── Credentials ──────────────────────────────────────────────────────────────

function getApiKey() {
    const key = process.env.OPENWEBNINJA_API_KEY || process.env.RAPIDAPI_KEY;
    if (!key) {
        console.error('Error: OPENWEBNINJA_API_KEY (or RAPIDAPI_KEY) env var is required.');
        process.exit(1);
    }
    return key;
}

// ─── Meta ─────────────────────────────────────────────────────────────────────

function loadMeta(apiId) {
    const metaPath = path.join(SKILL_ROOT, 'apis', apiId, 'meta.json');
    try {
        return JSON.parse(fs.readFileSync(metaPath, 'utf8'));
    } catch (e) {
        return {};
    }
}

// ─── HTTP ─────────────────────────────────────────────────────────────────────

function isOpenWebNinjaKey(apiKey) {
    return apiKey && apiKey.startsWith('ak_');
}

function resolveOwnSlug(host) {
    // Find the OWN slug by reading the YAML spec's servers[0].url for the matching API.
    // The YAML server URL is the source of truth (e.g. https://api.openwebninja.com/realtime-events-data).
    // meta.json api_id can differ from the actual OWN slug, so we parse the YAML.
    const apisDir = path.join(SKILL_ROOT, 'apis');
    try {
        for (const dir of fs.readdirSync(apisDir)) {
            const metaPath = path.join(apisDir, dir, 'meta.json');
            if (fs.existsSync(metaPath)) {
                const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
                if (meta.rapidapi_host === host) {
                    // Try to extract slug from YAML server URL
                    const yamlFiles = fs.readdirSync(path.join(apisDir, dir)).filter(f => f.endsWith('.yaml'));
                    if (yamlFiles.length > 0) {
                        const yaml = fs.readFileSync(path.join(apisDir, dir, yamlFiles[0]), 'utf8');
                        const match = yaml.match(/url:\s*https:\/\/api\.openwebninja\.com\/([^\s\n]+)/);
                        if (match) return match[1];
                    }
                    // Fallback to the authoritative OWN slug (portal_api_id in hyphen
                    // form), then api_id / folder name.
                    if (meta.portal_api_id) return meta.portal_api_id.replace(/_/g, '-');
                    return meta.api_id || dir;
                }
            }
        }
    } catch (e) { /* fallback */ }
    // Fallback: strip .p.rapidapi.com
    return host.replace('.p.rapidapi.com', '');
}

// Resolve the OWN URL slug from an api folder id. The slug is the API's portal_api_id in
// hyphen form (e.g. real_time_walmart_data -> real-time-walmart-data). These slugs are
// irregular and do NOT always match the folder name, so derive from meta.json's
// portal_api_id (authoritative). If no meta match (apiId may already be the hyphen slug),
// use it verbatim.
function ownSlugForApiId(apiId) {
    const meta = loadMeta(apiId);
    if (meta && meta.portal_api_id) return meta.portal_api_id.replace(/_/g, '-');
    return apiId;
}

function apiCall(host, endpoint, params, apiKey, method = 'GET', body = null, apiId = null) {
    const useOWN = isOpenWebNinjaKey(apiKey);
    const actualHost = useOWN ? 'api.openwebninja.com' : host;
    const slug = useOWN ? (apiId ? ownSlugForApiId(apiId) : resolveOwnSlug(host)) : null;
    const actualEndpoint = useOWN ? `/${slug}${endpoint}` : endpoint;

    const url = new URL(`https://${actualHost}${actualEndpoint}`);

    if (method === 'GET') {
        for (const [k, v] of Object.entries(params || {})) {
            if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
        }
    }

    return new Promise((resolve, reject) => {
        const bodyStr = body ? JSON.stringify(body) : null;
        const headers = useOWN
            ? { 'x-api-key': apiKey }
            : { 'x-rapidapi-host': host, 'x-rapidapi-key': apiKey };
        headers['X-OWN-Client'] = `openwebninja-universal-scraper/${SKILL_VERSION}`;
        if (bodyStr) {
            headers['Content-Type'] = 'application/json';
            headers['Content-Length'] = Buffer.byteLength(bodyStr);
        }
        const options = {
            hostname: url.hostname,
            port: 443,
            path: url.pathname + url.search,
            method,
            headers,
        };

        const req = https.request(options, res => {
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                const raw = Buffer.concat(chunks).toString('utf8');
                if (res.statusCode < 200 || res.statusCode >= 300) {
                    return reject(new Error(`HTTP ${res.statusCode}: ${raw.slice(0, 300)}`));
                }
                try {
                    resolve(JSON.parse(raw));
                } catch (e) {
                    reject(new Error(`JSON parse error: ${raw.slice(0, 200)}`));
                }
            });
        });
        req.on('error', reject);
        if (bodyStr) req.write(bodyStr);
        req.end();
    });
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getNestedValue(obj, dotPath) {
    if (!dotPath) return obj;
    return dotPath.split('.').reduce((cur, key) => (cur && cur[key] !== undefined ? cur[key] : undefined), obj);
}

function collectRecords(data, resultsPath, callNum) {
    const records = getNestedValue(data, resultsPath);
    if (Array.isArray(records)) return records;
    if (callNum === 1) return [data];
    return [];
}

// ─── Output ───────────────────────────────────────────────────────────────────

function flattenRecord(obj, prefix) {
    const result = {};
    for (const [k, v] of Object.entries(obj)) {
        const key = prefix ? `${prefix}_${k}` : k;
        if (v !== null && typeof v === 'object' && !Array.isArray(v)) {
            Object.assign(result, flattenRecord(v, key));
        } else {
            result[key] = Array.isArray(v) ? JSON.stringify(v) : v;
        }
    }
    return result;
}

function toCSV(records) {
    if (!records.length) return '';
    const flat = records.map(r => (typeof r === 'object' && r !== null ? flattenRecord(r, '') : { value: r }));
    const keys = [...new Set(flat.flatMap(r => Object.keys(r)))];
    const escape = v => {
        if (v === null || v === undefined) return '';
        const s = String(v);
        return s.includes(',') || s.includes('"') || s.includes('\n')
            ? `"${s.replace(/"/g, '""')}"` : s;
    };
    return [keys.join(','), ...flat.map(r => keys.map(k => escape(r[k])).join(','))].join('\n');
}

function writeOutput(records, outputPath, format, manifest) {
    if (!outputPath) {
        displayQuickAnswer(records);
        return;
    }
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    const content = format === 'csv' ? toCSV(records) : JSON.stringify(records, null, 2);
    fs.writeFileSync(outputPath, content);
    if (manifest) {
        fs.writeFileSync(outputPath + '.meta.json', JSON.stringify({ ...manifest, recordCount: records.length, completedAt: new Date().toISOString() }, null, 2));
    }
    console.error(`\nDone. ${records.length} records → ${outputPath}`);
}

// ─── Pagination ───────────────────────────────────────────────────────────────

async function fetchAll({ host, endpoint, params, apiKey, count, pagination, pageSize, pageParam, offsetParam, cursorParam, cursorPath, resultsPath, dryRun, delay, maxCalls, apiId }) {
    const allResults = [];
    let totalCallsMade = 0;

    function call(p) {
        totalCallsMade++;
        if (totalCallsMade > maxCalls) throw new Error(`Cost cap exceeded: ${totalCallsMade} calls, limit is ${maxCalls}. Use --max-calls to raise.`);
        return apiCall(host, endpoint, p, apiKey, 'GET', null, apiId);
    }

    if (pagination === 'none') {
        console.error('  Call 1 (single response, no pagination)');
        const data = await call(params);
        allResults.push(...collectRecords(data, resultsPath, 1));

    } else if (pagination === 'page_number') {
        const totalPages = dryRun ? 1 : Math.ceil(count / pageSize);
        console.error(`Fetching up to ${count} results across up to ${totalPages} page(s)...`);
        for (let page = 1; page <= totalPages; page++) {
            if (page > 1) await sleep(delay);
            console.error(`  Page ${page}/${totalPages} (call ${totalCallsMade + 1})`);
            const data = await call({ ...params, [pageParam]: page });
            const records = collectRecords(data, resultsPath, page);
            if (!records.length) { console.error('  No results, stopping early.'); break; }
            allResults.push(...records);
            if (allResults.length >= count) break;
            const totalPagesInResponse = getNestedValue(data, 'num_pages');
            if (totalPagesInResponse && page >= Number(totalPagesInResponse)) break;
        }

    } else if (pagination === 'offset') {
        let offset = 0, callNum = 0;
        console.error(`Fetching up to ${count} results (offset-based, param: ${offsetParam})...`);
        while (allResults.length < count) {
            if (callNum > 0) await sleep(delay);
            callNum++;
            console.error(`  Offset ${offset} (call ${totalCallsMade + 1})`);
            const data = await call({ ...params, [offsetParam]: offset });
            const records = collectRecords(data, resultsPath, callNum);
            if (!records.length) { console.error('  No results, stopping.'); break; }
            allResults.push(...records);
            offset += records.length;
            if (dryRun) break;
        }

    } else if (pagination === 'cursor') {
        let cursor = null, callNum = 0;
        console.error(`Fetching up to ${count} results (cursor-based, param: ${cursorParam})...`);
        while (allResults.length < count) {
            if (callNum > 0) await sleep(delay);
            callNum++;
            console.error(`  Cursor call ${callNum} (call ${totalCallsMade + 1})`);
            const p = { ...params };
            if (cursor !== null) p[cursorParam] = cursor;
            const data = await call(p);
            const records = collectRecords(data, resultsPath, callNum);
            if (!records.length) { console.error('  No results, stopping.'); break; }
            allResults.push(...records);
            cursor = getNestedValue(data, cursorPath) || null;
            if (!cursor) { console.error('  No next cursor, stopping.'); break; }
            if (dryRun) break;
        }

    } else {
        throw new Error(`Unknown pagination style "${pagination}". Use: page_number | offset | cursor | none`);
    }

    return { results: allResults.slice(0, count), totalCallsMade };
}

// ─── Untrusted Content ────────────────────────────────────────────────────────

// Strips patterns that frequently appear in prompt-injection attempts.
// API responses contain third-party text; sanitize string fields before they
// reach the agent's reasoning context or the user's view.
function sanitizeUntrusted(text) {
    if (typeof text !== 'string') return text;
    return text
        // Role-tag and tool-tag styled markup
        .replace(/<\/?(system|assistant|user|tool|antml:[a-z_]+|claude|anthropic)\b[^>]*>/gi, '')
        // "ignore/disregard/forget/override (the/all/your/...) previous/prior/earlier/above ..." patterns
        .replace(/(?:^|\n|\.\s)\s*(?:please\s+)?(ignore|disregard|forget|override)\s+(?:all\s+|the\s+|your\s+|previous|prior|earlier|above)[^\n.]{0,120}/gi, '')
        // Handlebars-style template injection
        .replace(/\{\{[^}]{0,200}\}\}/g, '');
}

// ─── Quick Answer ─────────────────────────────────────────────────────────────

function displayQuickAnswer(records, { limit = 5, fields } = {}) {
    if (!records.length) { console.log('\nNo results found.'); return; }
    const top = records.slice(0, limit);
    const pick = fields || Object.keys(top[0]).filter(k => {
        const v = top[0][k];
        return v !== null && v !== undefined && !(Array.isArray(v) && !v.length);
    }).slice(0, 10);

    console.log(`\n${'='.repeat(60)}`);
    console.log(`TOP ${top.length} RESULTS (of ${records.length} total)`);
    console.log('='.repeat(60));

    for (let i = 0; i < top.length; i++) {
        console.log(`\n--- Result ${i + 1} ---`);
        for (const key of pick) {
            let val = top[i][key];
            if (val === null || val === undefined) continue;
            if (typeof val === 'string') {
                val = sanitizeUntrusted(val);
                if (val.length > 120) val = val.slice(0, 120) + '...';
            }
            else if (typeof val === 'object') {
                const s = JSON.stringify(val);
                val = s.length > 120 ? s.slice(0, 120) + '...' : s;
            }
            console.log(`  ${key}: ${val}`);
        }
    }
    console.log(`\n${'='.repeat(60)}`);
    if (records.length > limit) console.log(`Showing ${limit} of ${records.length} results. Use --output to save all.`);
}


// ─── Exports ──────────────────────────────────────────────────────────────────

module.exports = { getApiKey, loadMeta, apiCall, sleep, getNestedValue, collectRecords, flattenRecord, toCSV, writeOutput, sanitizeUntrusted, displayQuickAnswer, fetchAll };
