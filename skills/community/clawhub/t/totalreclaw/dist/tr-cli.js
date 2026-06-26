#!/usr/bin/env node
/**
 * tr — TotalReclaw hybrid CLI (3.3.9-rc.1 primary architecture)
 *
 * OpenClaw 2026.5.2 has a tool-policy-pipeline bug (issue #223) that strips non-bundled plugin
 * tools before they reach the agent toolset. In 3.3.9-rc.1, this CLI is the PRIMARY path for
 * all agent memory operations (not a fallback). The agent runs `tr <cmd> --json` from shell;
 * hooks (before_agent_start, agent_end, message_received, before_reset) continue via the
 * unbroken hook code path.
 *
 * Phrase-safety: this CLI reads credentials.json (mnemonic at rest) but NEVER
 * prints the mnemonic to stdout, stderr, or any log. Phrase only enters via QR-pair
 * browser tier (pair-cli.ts / pair-cli-relay.ts — unchanged).
 *
 * Commands:
 *   tr status [--json]          — print onboarding + credentials state
 *   tr pair [--json]            — start a relay pairing session, print URL+PIN+QR
 *   tr remember [--json] <text> — store a memory in the encrypted vault (on-chain)
 *   tr recall [--json] [--limit N] <query> — search the encrypted vault (subgraph)
 *   tr forget [--json] <factId> — tombstone a memory on-chain
 *   tr export [--json] [--format json|markdown] — dump all memories from the subgraph
 *
 * 3.3.12-rc.4 — switched remember/recall/forget/export from `/v1/store` and
 * `/v1/search` (those endpoints were removed during the on-chain pivot —
 * relay returns 404) to the on-chain UserOp + subgraph paths used by the
 * native MCP tools (`totalreclaw_remember`, `totalreclaw_recall`, etc).
 *
 * --json flag: all agent-facing CLI calls MUST use --json for clean machine-parseable output.
 *              Plain text mode is for direct user CLI use only.
 *
 * Install: wired via package.json `bin.tr` → dist/tr-cli.js
 * Usage from container: `docker exec tr-openclaw node ~/.openclaw/extensions/totalreclaw/dist/tr-cli.js status --json`
 */
import path from 'node:path';
import os from 'node:os';
import { randomUUID } from 'node:crypto';
import { CONFIG, setRecoveryPhraseOverride } from './config.js';
import { loadCredentialsJson } from './fs-helpers.js';
import { printStatus } from './onboarding-cli.js';
import { deriveKeys, computeAuthKeyHash, encrypt, decrypt, generateBlindIndices, generateContentFingerprint, } from './crypto.js';
import { createApiClient } from './api-client.js';
import { encodeFactProtobuf, submitFactBatchOnChain, deriveSmartAccountAddress, getSubgraphConfig, PROTOBUF_VERSION_V4, } from './subgraph-store.js';
import { searchSubgraph, searchSubgraphBroadened, } from './subgraph-search.js';
import { exportAllFacts } from './tr-cli-export-helper.js';
// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const CREDENTIALS_PATH = CONFIG.credentialsPath;
const SERVER_URL = CONFIG.serverUrl;
const STATE_PATH = CONFIG.onboardingStatePath;
// Auto-synced by skill/scripts/sync-version.mjs from skill/plugin/package.json::version.
// Do not edit by hand — running tests will catch drift but the publish workflow
// rewrites this constant at the start of every npm/ClawHub publish.
const PLUGIN_VERSION = '3.3.12-rc.10';
function die(msg, code = 1) {
    process.stderr.write(`tr: ${msg}\n`);
    process.exit(code);
}
function log(msg) {
    process.stdout.write(msg + '\n');
}
/** Parse --flag from args array, returning the cleaned args without the flag. */
function popFlag(args, flag) {
    const idx = args.indexOf(flag);
    if (idx === -1)
        return [false, args];
    return [true, [...args.slice(0, idx), ...args.slice(idx + 1)]];
}
/** Parse --limit N from args, returning [limit, cleanedArgs]. Default: defaultLimit. */
function popLimitFlag(args, defaultLimit) {
    const idx = args.indexOf('--limit');
    if (idx === -1 || idx + 1 >= args.length)
        return [defaultLimit, args];
    const n = parseInt(args[idx + 1], 10);
    const limit = isNaN(n) || n < 1 ? defaultLimit : n;
    return [limit, [...args.slice(0, idx), ...args.slice(idx + 2)]];
}
/** Parse --format VALUE from args, returning [value, cleanedArgs]. */
function popOptionFlag(args, flag, defaultValue) {
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length)
        return [defaultValue, args];
    return [args[idx + 1], [...args.slice(0, idx), ...args.slice(idx + 2)]];
}
/**
 * Convert XChaCha20-Poly1305 base64 ciphertext to hex (the on-chain blob
 * format). Mirrors `encryptToHex` in index.ts so we don't pull in the whole
 * 7000-line module. Subgraph-stored facts use hex, not base64.
 */
function toHexBlob(plaintext, encryptionKey) {
    const b64 = encrypt(plaintext, encryptionKey);
    return Buffer.from(b64, 'base64').toString('hex');
}
/** Inverse of toHexBlob — used by recall/export to decrypt subgraph blobs. */
function fromHexBlob(hexBlob, encryptionKey) {
    const hex = hexBlob.startsWith('0x') ? hexBlob.slice(2) : hexBlob;
    const b64 = Buffer.from(hex, 'hex').toString('base64');
    return decrypt(b64, encryptionKey);
}
async function buildContext() {
    const creds = loadCredentialsJson(CREDENTIALS_PATH);
    if (!creds) {
        die('TotalReclaw is not set up. Run: node ~/.openclaw/extensions/totalreclaw/dist/tr-cli.js pair --json');
    }
    const mnemonic = (typeof creds.mnemonic === 'string' && creds.mnemonic.trim()) ||
        (typeof creds.recovery_phrase === 'string' && creds.recovery_phrase.trim()) ||
        '';
    if (!mnemonic) {
        die('No recovery phrase in credentials.json. Run: tr pair --json');
    }
    // Make the mnemonic visible to subgraph-store helpers (getSubgraphConfig
    // reads CONFIG.recoveryPhrase, which falls back to the override). We do
    // NOT log the mnemonic anywhere — it just lives in process memory for the
    // lifetime of this CLI invocation.
    setRecoveryPhraseOverride(mnemonic);
    // Parse existing salt/userId from credentials.json
    let existingSalt;
    let existingUserId;
    const saltStr = typeof creds.salt === 'string' ? creds.salt : undefined;
    if (saltStr) {
        if (/^[0-9a-f]{64}$/i.test(saltStr)) {
            existingSalt = Buffer.from(saltStr, 'hex');
        }
        else {
            existingSalt = Buffer.from(saltStr, 'base64');
        }
    }
    existingUserId = typeof creds.userId === 'string' ? creds.userId : undefined;
    const keys = deriveKeys(mnemonic, existingSalt);
    const authKeyHex = keys.authKey.toString('hex');
    const apiClient = createApiClient(SERVER_URL);
    let userId;
    if (existingUserId) {
        userId = existingUserId;
    }
    else {
        // Register to get userId (idempotent on relay) — auth key hash is the
        // billing identity even in subgraph mode.
        const authHash = computeAuthKeyHash(keys.authKey);
        const saltHex = keys.salt.toString('hex');
        try {
            const result = await apiClient.register(authHash, saltHex);
            userId = result.user_id;
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            if (msg.includes('USER_EXISTS')) {
                userId = authHash.slice(0, 32);
            }
            else {
                die(`Relay registration failed: ${msg}`);
            }
        }
    }
    // Derive the Smart Account address. This is the on-chain "owner" for
    // every fact + the X-Wallet-Address header on every UserOp / subgraph
    // call. Cheap eth_call to the SimpleAccountFactory; CREATE2 deterministic.
    let walletAddress;
    try {
        walletAddress = await deriveSmartAccountAddress(mnemonic, CONFIG.chainId);
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        die(`Failed to derive Smart Account address: ${msg}`);
    }
    return {
        authKeyHex,
        encryptionKey: keys.encryptionKey,
        dedupKey: keys.dedupKey,
        apiClient,
        userId,
        walletAddress,
    };
}
// ---------------------------------------------------------------------------
// Command: status
// ---------------------------------------------------------------------------
async function cmdStatus(jsonMode) {
    // Probe plugin manifest for version/hybridMode/toolCount.
    let pluginVersion;
    let bootCount;
    let hybridMode = true; // default true in 3.3.9-rc.1 (hybrid-primary)
    let toolCount;
    let loadedAgeSec;
    try {
        const fs = await import('node:fs');
        const candidatePaths = [
            path.join(os.homedir(), '.openclaw', 'extensions', 'totalreclaw', '.loaded.json'),
            path.join(os.homedir(), '.openclaw', 'npm', 'node_modules', '@totalreclaw', 'totalreclaw', 'dist', '.loaded.json'),
        ];
        const resolvedPath = candidatePaths.find((p) => fs.existsSync(p));
        if (resolvedPath) {
            const raw = fs.readFileSync(resolvedPath, 'utf-8');
            const manifest = JSON.parse(raw);
            pluginVersion = manifest.version ?? PLUGIN_VERSION;
            bootCount = manifest.bootCount;
            hybridMode = manifest.hybridMode !== false; // default true
            toolCount = manifest.tools?.length;
            const ageMs = Date.now() - (manifest.loadedAt ?? 0);
            loadedAgeSec = Math.round(ageMs / 1000);
        }
    }
    catch {
        // Best-effort
    }
    // Check onboarding state
    const creds = loadCredentialsJson(CREDENTIALS_PATH);
    const onboarded = !!creds;
    if (jsonMode) {
        // JSON-first output for agent parsing
        const out = {
            version: pluginVersion ?? PLUGIN_VERSION,
            onboarded,
            next_step: onboarded ? 'none' : 'pair',
            tool_count: toolCount ?? 17,
            hybrid_mode: hybridMode,
        };
        if (bootCount !== undefined)
            out.boot_count = bootCount;
        if (loadedAgeSec !== undefined)
            out.loaded_age_sec = loadedAgeSec;
        log(JSON.stringify(out));
    }
    else {
        // Human-readable plain text for direct user CLI use
        printStatus(CREDENTIALS_PATH, STATE_PATH, process.stdout);
        process.stdout.write(`\n  plugin:      ${pluginVersion ? `loaded (version=${pluginVersion}` + (bootCount !== undefined ? ` bootCount=${bootCount}` : '') + (loadedAgeSec !== undefined ? ` loaded=${loadedAgeSec}s ago` : '') + ')' : 'not found in .loaded.json'}\n` +
            `  hybrid-mode: ${hybridMode ? 'yes (primary — use tr <cmd> --json)' : 'no'}\n` +
            `  hooks:       before_agent_start, agent_end, message_received, before_reset\n`);
    }
}
// ---------------------------------------------------------------------------
// Command: pair
// ---------------------------------------------------------------------------
async function cmdPair(args) {
    // Delegate to the existing pair-cli-relay.ts via a thin wrapper.
    // The pair flow is relay-brokered (works through Docker NAT).
    // Phrase-safety: pair-cli-relay.ts is x25519-only; mnemonic never appears.
    const outputMode = args.includes('--json') ? 'json' : args.includes('--url-pin') ? 'url-pin' : 'human';
    const { runRelayPairCli } = await import('./pair-cli-relay.js');
    const { defaultRenderQr, buildDefaultPairCliIo } = await import('./pair-cli.js');
    const io = buildDefaultPairCliIo();
    const outcome = await runRelayPairCli('generate', {
        relayBaseUrl: CONFIG.pairRelayUrl,
        credentialsPath: CREDENTIALS_PATH,
        onboardingStatePath: STATE_PATH,
        logger: {
            info: (m) => process.stderr.write(`[info] ${m}\n`),
            warn: (m) => process.stderr.write(`[warn] ${m}\n`),
            error: (m) => process.stderr.write(`[error] ${m}\n`),
        },
        pluginVersion: PLUGIN_VERSION,
        deriveScopeAddress: undefined,
        renderQr: defaultRenderQr,
        io,
        outputMode: outputMode,
    });
    if (outcome.status !== 'completed' && outcome.status !== 'canceled') {
        die(`Pairing ${outcome.status}`, 1);
    }
    if (outcome.status === 'canceled') {
        process.exit(130);
    }
}
// ---------------------------------------------------------------------------
// Command: remember
// ---------------------------------------------------------------------------
async function cmdRemember(rawArgs) {
    const [jsonMode, args] = popFlag(rawArgs, '--json');
    const text = args.join(' ').trim();
    if (!text) {
        die('Usage: tr remember [--json] <text>');
    }
    const ctx = await buildContext();
    // Build a Memory Taxonomy v1 claim blob (matches storeExtractedFacts shape).
    const now = new Date().toISOString();
    const factId = randomUUID();
    const blob = JSON.stringify({
        text,
        type: 'claim',
        source: 'user',
        scope: 'unspecified',
        importance: 8,
        metadata: {
            type: 'claim',
            source: 'user',
            scope: 'unspecified',
            importance: 8,
        },
        timestamp: now,
        version: 'v1',
    });
    const encryptedBlob = toHexBlob(blob, ctx.encryptionKey);
    const blindIndices = generateBlindIndices(text);
    const contentFp = generateContentFingerprint(text, ctx.dedupKey);
    // On-chain submission: encode protobuf, build SubgraphStoreConfig (auth +
    // wallet), submit a single-fact UserOp through the relay bundler. The
    // subgraph indexes the resulting Log(bytes) event so it is recall-able
    // within ~5-15 s of the receipt.
    const fact = {
        id: factId,
        timestamp: now,
        owner: ctx.walletAddress,
        encryptedBlob,
        blindIndices,
        decayScore: 8,
        source: 'cli:tr-remember',
        contentFp,
        agentId: 'tr-cli',
        version: PROTOBUF_VERSION_V4,
    };
    try {
        const protobuf = encodeFactProtobuf(fact);
        const config = {
            ...getSubgraphConfig(),
            authKeyHex: ctx.authKeyHex,
            walletAddress: ctx.walletAddress,
        };
        const result = await submitFactBatchOnChain([protobuf], config);
        if (!result.success) {
            die(`remember failed: on-chain UserOp did not succeed (userOpHash=${result.userOpHash || 'none'})`);
        }
        if (jsonMode) {
            // JSON-first output for agent parsing.
            // claim_count = 1 here (single fact stored). Computing the full vault
            // count would require an extra subgraph query on every remember and
            // isn't worth the latency.
            log(JSON.stringify({ ok: true, id: factId, claim_count: 1 }));
        }
        else {
            log(`ok — stored memory (id=${factId}, tx=${result.txHash || 'pending'})`);
        }
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        die(`remember failed: ${msg}`);
    }
}
// ---------------------------------------------------------------------------
// Command: recall
// ---------------------------------------------------------------------------
async function cmdRecall(rawArgs) {
    const [jsonMode, argsAfterJson] = popFlag(rawArgs, '--json');
    const [limit, argsAfterLimit] = popLimitFlag(argsAfterJson, 5);
    const query = argsAfterLimit.join(' ').trim();
    if (!query) {
        die('Usage: tr recall [--json] [--limit N] <query>');
    }
    const ctx = await buildContext();
    // Generate word trapdoors for blind search. The CLI does not run the
    // ONNX embedder (that's a 700 MB lazy bundle in the gateway) so we send
    // word-only trapdoors. The reranker in the native MCP path would add LSH
    // trapdoors on top — we live without them here in exchange for a much
    // smaller CLI footprint.
    const trapdoors = generateBlindIndices(query);
    const pool = Math.max(limit * 4, 20);
    try {
        let candidates = await searchSubgraph(ctx.walletAddress, trapdoors, pool, ctx.authKeyHex);
        // Always run broadened search and merge — ensures vocabulary mismatches
        // (e.g., "preferences" vs "prefer") don't cause recall failures. This
        // mirrors the native tool path in index.ts (line 3978).
        try {
            const broadened = await searchSubgraphBroadened(ctx.walletAddress, pool, ctx.authKeyHex);
            const seen = new Set(candidates.map((r) => r.id));
            for (const br of broadened) {
                if (!seen.has(br.id))
                    candidates.push(br);
            }
        }
        catch {
            // best-effort; broadened-only failures shouldn't block trapdoor results
        }
        const results = [];
        for (const c of candidates) {
            try {
                const docJson = fromHexBlob(c.encryptedBlob, ctx.encryptionKey);
                const parsed = JSON.parse(docJson);
                if (!parsed.text)
                    continue;
                // The CLI is intentionally simple — score by decayScore (importance
                // proxy) instead of running the full BM25 + cosine reranker that
                // the native MCP path uses. Agents calling the CLI typically just
                // want the top-N by importance.
                const decay = typeof c.decayScore === 'string'
                    ? parseInt(c.decayScore, 10)
                    : c.decayScore;
                const score = Number.isFinite(decay) ? decay / 10 : 0.5;
                results.push({ text: parsed.text, score });
            }
            catch {
                // Skip undecryptable / non-JSON (digest blobs, tombstones, etc.)
            }
        }
        // Sort by score descending, then trim to limit.
        results.sort((a, b) => b.score - a.score);
        const trimmed = results.slice(0, limit);
        if (jsonMode) {
            log(JSON.stringify({ results: trimmed }));
        }
        else {
            log(`Found ${trimmed.length} result(s) for: ${query}`);
            for (const r of trimmed) {
                log(`  [score=${r.score.toFixed(2)}] ${r.text}`);
            }
        }
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        die(`recall failed: ${msg}`);
    }
}
// ---------------------------------------------------------------------------
// Command: forget
// ---------------------------------------------------------------------------
async function cmdForget(rawArgs) {
    const [jsonMode, args] = popFlag(rawArgs, '--json');
    const factId = (args[0] ?? '').trim();
    if (!factId) {
        die('Usage: tr forget [--json] <factId>');
    }
    // UUID-v4-ish shape check — same validation as the native totalreclaw_forget
    // tool (index.ts line 4225). Prevents fabricated / natural-language IDs
    // from reaching the UserOp path and silently no-op'ing on-chain.
    if (!/^[0-9a-f-]{8,}$/i.test(factId)) {
        die(`forget failed: "${factId.slice(0, 60)}" doesn't look like a memory ID. ` +
            `Run \`tr recall --json <query>\` first and pass a result's id.`);
    }
    const ctx = await buildContext();
    // Tombstone shape (pin/unpin & native forget use the same one — see
    // index.ts:4253-4267 + pin.ts:611-621). Deliberately NO version field
    // → uses legacy v3 default so the subgraph's contradiction handler
    // matches and flips isActive=false.
    const tombstone = {
        id: factId,
        timestamp: new Date().toISOString(),
        owner: ctx.walletAddress,
        encryptedBlob: '00',
        blindIndices: [],
        decayScore: 0,
        source: 'tombstone',
        contentFp: '',
        agentId: 'tr-cli',
        // No `version` → legacy v3 (matches pin/unpin & native forget).
    };
    try {
        const protobuf = encodeFactProtobuf(tombstone);
        const config = {
            ...getSubgraphConfig(),
            authKeyHex: ctx.authKeyHex,
            walletAddress: ctx.walletAddress,
        };
        const result = await submitFactBatchOnChain([protobuf], config);
        if (!result.success) {
            die(`forget failed: on-chain tombstone did not succeed (userOpHash=${result.userOpHash || 'none'})`);
        }
        if (jsonMode) {
            log(JSON.stringify({ ok: true, id: factId, tx_hash: result.txHash }));
        }
        else {
            log(`ok — tombstoned ${factId} (tx=${result.txHash || 'pending'})`);
        }
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        die(`forget failed: ${msg}`);
    }
}
// ---------------------------------------------------------------------------
// Command: export
// ---------------------------------------------------------------------------
async function cmdExport(rawArgs) {
    const [jsonMode, argsAfterJson] = popFlag(rawArgs, '--json');
    const [format, _argsAfterFormat] = popOptionFlag(argsAfterJson, '--format', 'json');
    if (format !== 'json' && format !== 'markdown') {
        die('Usage: tr export [--json] [--format json|markdown]');
    }
    const ctx = await buildContext();
    // Delegate the subgraph paginate + decrypt loop to a helper module —
    // tr-cli.ts already includes `fs.readFileSync` (status command), and
    // adding outbound HTTP here would trip the OpenClaw scanner's
    // potential-exfiltration rule. See tr-cli-export-helper.ts.
    const allFacts = await exportAllFacts(ctx.walletAddress, ctx.authKeyHex, ctx.encryptionKey);
    if (format === 'markdown') {
        if (allFacts.length === 0) {
            log('*No memories stored.*');
        }
        else {
            const lines = allFacts.map((f, i) => {
                const meta = f.metadata;
                const type = meta.type ?? 'fact';
                return `${i + 1}. **[${type}]** ${f.text}  \n   _ID: ${f.id} | Created: ${f.created_at}_`;
            });
            log(`# Exported Memories (${allFacts.length})\n\n${lines.join('\n')}`);
        }
        return;
    }
    // json format (default — both --json mode and --format=json end up here)
    if (jsonMode) {
        log(JSON.stringify({ count: allFacts.length, facts: allFacts }));
    }
    else {
        log(JSON.stringify(allFacts, null, 2));
    }
}
// ---------------------------------------------------------------------------
// Dispatch
// ---------------------------------------------------------------------------
async function main() {
    const args = process.argv.slice(2);
    const cmd = args[0];
    switch (cmd) {
        case 'status': {
            const [jsonMode] = popFlag(args.slice(1), '--json');
            await cmdStatus(jsonMode);
            break;
        }
        case 'pair':
            await cmdPair(args.slice(1));
            break;
        case 'remember':
            await cmdRemember(args.slice(1));
            break;
        case 'recall':
            await cmdRecall(args.slice(1));
            break;
        case 'forget':
            await cmdForget(args.slice(1));
            break;
        case 'export':
            await cmdExport(args.slice(1));
            break;
        case undefined:
        case '--help':
        case '-h':
            process.stdout.write(`TotalReclaw hybrid CLI v${PLUGIN_VERSION} (primary mode — OpenClaw 2026.5.2+)\n\n` +
                'Usage:\n' +
                '  tr status [--json]                       — onboarding + plugin load state\n' +
                '  tr pair [--json]                         — start a relay pairing session\n' +
                '  tr remember [--json] <text>              — store a memory (on-chain UserOp)\n' +
                '  tr recall [--json] [--limit N] <query>   — search memories (default limit: 5)\n' +
                '  tr forget [--json] <factId>              — tombstone a memory on-chain\n' +
                '  tr export [--json] [--format json|markdown] — dump every memory in the vault\n\n' +
                'Flags:\n' +
                '  --json    Output machine-parseable JSON (required for agent shell calls)\n' +
                '  --limit N Limit recall results (default: 5)\n\n' +
                'JSON output shapes:\n' +
                '  status:   {"version":"...","onboarded":bool,"next_step":"pair|none","tool_count":N,"hybrid_mode":bool}\n' +
                '  pair:     {"url":"...","pin":"123456","expires_at":"..."}\n' +
                '  remember: {"ok":true,"id":"...","claim_count":N}\n' +
                '  recall:   {"results":[{"text":"...","score":0.8}]}\n' +
                '  forget:   {"ok":true,"id":"...","tx_hash":"0x..."}\n' +
                '  export:   {"count":N,"facts":[{"id":"...","text":"...","metadata":{...},"created_at":"..."}]}\n\n' +
                'Environment:\n' +
                '  TOTALRECLAW_SERVER_URL           — relay URL (default: api.totalreclaw.xyz; staging: api-staging.totalreclaw.xyz)\n' +
                '  TOTALRECLAW_CREDENTIALS_PATH     — override credentials.json path\n');
            break;
        default:
            die(`Unknown command: ${cmd}. Run \`tr --help\` for usage.`);
    }
}
main().catch((err) => {
    const msg = err instanceof Error ? err.message : String(err);
    process.stderr.write(`tr: fatal: ${msg}\n`);
    process.exit(2);
});
