'use strict';

/**
 * Self-subscribe the current OpenWeb Ninja API key to an API's free (BASIC) tier,
 * so a scrape can proceed without a manual trip to the portal.
 *
 * Mirrors the openwebninja-mcp `subscribe` tool: it POSTs { api_id, plan_key } to the
 * dev-portal `/self-subscribe-free` endpoint using the OpenWeb Ninja key. Free tier
 * only -- the backend never touches Stripe and refuses to downgrade an active paid sub.
 *
 * Usage:
 *   node --env-file=.env subscribe.js <api_id> [--plan basic]
 *   e.g. node --env-file=.env subscribe.js realtime-walmart-data
 *
 * Only works with an OpenWeb Ninja portal key (OPENWEBNINJA_API_KEY=ak_...). RapidAPI
 * subscriptions are managed on RapidAPI and cannot be self-subscribed from here.
 */

const https = require('https');
const { loadMeta } = require('./lib/utils');

// Same default the MCP uses; override with OPENWEBNINJA_PORTAL_API_URL if it ever moves.
const DEFAULT_PORTAL_API = 'https://rpuo5v9cbe.execute-api.us-east-1.amazonaws.com/v1';

function portalRoot() {
    return (process.env.OPENWEBNINJA_PORTAL_API_URL || DEFAULT_PORTAL_API).replace(/\/$/, '');
}

// Resolve the api_id the dev-portal expects for self-subscribe. For most APIs this is the
// portal_api_id; the /self-subscribe-free handler normalizes real_time_ <-> realtime_, so
// either prefix matches. But a few APIs are keyed differently in the portal that the toggle
// can't reach -- e.g. Redfin's free plan is under "redfin_api", not realtime_redfin_data --
// so those carry an explicit `subscribe_api_id` override. portal_api_id stays the
// api.openwebninja.com URL slug (used for data calls); this is only the subscribe key.
// Order: subscribe_api_id (override) -> portal_api_id -> folder id.
function resolveSubscribeApiId(apiId, meta) {
    if (meta && meta.subscribe_api_id) return meta.subscribe_api_id;
    if (meta && meta.portal_api_id) return meta.portal_api_id;
    console.error(`Warning: no subscribe_api_id/portal_api_id in meta.json for "${apiId}"; falling back to "${apiId.replace(/-/g, '_')}".`);
    return apiId.replace(/-/g, '_');
}

function subscribeFree(portalApiId, apiKey, planKey) {
    const payload = JSON.stringify({ api_id: portalApiId, plan_key: planKey });
    const url = new URL(`${portalRoot()}/self-subscribe-free`);
    return new Promise((resolve, reject) => {
        const req = https.request({
            hostname: url.hostname,
            port: 443,
            path: url.pathname + url.search,
            method: 'POST',
            headers: {
                'x-api-key': apiKey,
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload),
                'Accept': 'application/json',
                'User-Agent': 'openwebninja-universal-scraper',
            },
        }, res => {
            const chunks = [];
            res.on('data', c => chunks.push(c));
            res.on('end', () => {
                const raw = Buffer.concat(chunks).toString('utf8');
                let parsed;
                try { parsed = raw ? JSON.parse(raw) : undefined; } catch { parsed = raw; }
                if (res.statusCode < 200 || res.statusCode >= 300) {
                    const detail = (parsed && (parsed.message || (parsed.error && parsed.error.message) || parsed.error))
                        || (typeof parsed === 'string' ? parsed.slice(0, 300) : '')
                        || res.statusMessage;
                    return reject(new Error(`Subscribe failed (HTTP ${res.statusCode}): ${detail}`));
                }
                resolve(parsed);
            });
        });
        req.on('error', reject);
        req.write(payload);
        req.end();
    });
}

async function main() {
    const args = process.argv.slice(2);
    let apiId = null;
    let planKey = 'basic';
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--plan') planKey = args[++i];
        else if (!args[i].startsWith('--') && !apiId) apiId = args[i];
    }

    if (!apiId) {
        console.error('Usage: node --env-file=.env subscribe.js <api_id> [--plan basic]');
        console.error('Example: node --env-file=.env subscribe.js realtime-walmart-data');
        process.exit(1);
    }

    const apiKey = process.env.OPENWEBNINJA_API_KEY || process.env.RAPIDAPI_KEY;
    if (!apiKey) {
        console.error('Error: OPENWEBNINJA_API_KEY is required for self-subscribe.');
        console.error('Add it to .env (format: OPENWEBNINJA_API_KEY=ak_your_key_here).');
        process.exit(1);
    }
    // Self-subscribe is a portal (OpenWeb Ninja key) capability only. RapidAPI keys
    // do not start with "ak_" and their plans live on RapidAPI, not the dev portal.
    if (!apiKey.startsWith('ak_')) {
        console.error('Self-subscribe needs an OpenWeb Ninja portal key (OPENWEBNINJA_API_KEY=ak_...).');
        console.error('The key in .env looks like a RapidAPI key. RapidAPI plans are managed on RapidAPI:');
        const meta = loadMeta(apiId);
        if (meta && meta.rapidapi_url) console.error(`  open "${meta.rapidapi_url}" and subscribe to the free plan there.`);
        else console.error('  open the API\'s rapidapi_url and subscribe to the free plan there.');
        process.exit(1);
    }

    const meta = loadMeta(apiId);
    const subscribeApiId = resolveSubscribeApiId(apiId, meta);

    console.error(`Self-subscribing "${apiId}" (portal id: ${subscribeApiId}) to the free (${planKey.toUpperCase()}) tier...`);
    try {
        const result = await subscribeFree(subscribeApiId, apiKey, planKey);
        console.log(`Subscribed "${apiId}" to the free (${planKey.toUpperCase()}) tier. Wait a few seconds for it to take effect, then retry the request.`);
        const note = result && typeof result === 'object' ? (result.message || result.status) : null;
        if (note) console.log(`Portal: ${note}`);
    } catch (e) {
        console.error(e.message);
        console.error('Free tier only: this never charges and will not change an existing paid subscription.');
        console.error('If you are already subscribed, an HTTP 429 means rate-limiting -- wait briefly and retry the request instead.');
        process.exit(1);
    }
}

main();
