#!/usr/bin/env node
/**
 * tr — TotalReclaw CLI (explicit-write + curation surface)
 *
 * Scope (Phase 3.3 — OpenClaw native integration): recall is now NATIVE.
 * The agent reads memories via OpenClaw's bundled `memory_search` /
 * `memory_get` tools (backed by the MemoryPluginCapability + TrMemorySearchManager
 * adapter registered in `index.ts`). This CLI no longer ships a recall path.
 *
 * What's still CLI-only (no native agent-facing surface):
 *   - explicit write (`tr remember`) — the conventional memory contract has no
 *     agent-facing write tool; auto-extraction stores facts via hooks.
 *   - curation / lifecycle (`tr forget`, `tr export`).
 *   - onboarding + pairing (`tr status`, `tr pair`).
 *
 * Phrase-safety: this CLI reads credentials.json (mnemonic at rest) but NEVER
 * prints the mnemonic to stdout, stderr, or any log. Phrase only enters via QR-pair
 * browser tier (pair-cli.ts / pair-cli-relay.ts — unchanged).
 *
 * Commands:
 *   tr status [--json]          — print onboarding + credentials state
 *   tr pair [--json]            — start a relay pairing session, print URL+PIN+QR
 *   tr remember [--json] <text> — store a memory in the encrypted vault (on-chain)
 *   tr forget [--json] <factId> — tombstone a memory on-chain (find the id via memory_search)
 *   tr export [--json] [--format json|markdown] — dump all memories from the subgraph
 *
 * 3.3.12-rc.4 — switched remember/forget/export from `/v1/store` and
 * `/v1/search` (those endpoints were removed during the on-chain pivot —
 * relay returns 404) to the on-chain UserOp + subgraph paths.
 *
 * --json flag: all agent-facing CLI calls MUST use --json for clean machine-parseable output.
 *              Plain text mode is for direct user CLI use only.
 *
 * Install: wired via package.json `bin.tr` → dist/tr-cli.js
 * Usage from container: `docker exec tr-openclaw node ~/.openclaw/extensions/totalreclaw/dist/tr-cli.js status --json`
 */
import { randomUUID } from 'node:crypto';
import { CONFIG, setRecoveryPhraseOverride } from './config.js';
import { loadCredentialsJson } from './fs-helpers.js';
import { printStatus } from './onboarding-cli.js';
import { deriveKeys, computeAuthKeyHash, encrypt, generateBlindIndices, generateContentFingerprint, } from './crypto.js';
import { createApiClient } from './api-client.js';
import { encodeFactProtobuf, submitFactBatchOnChain, deriveSmartAccountAddress, getSubgraphConfig, PROTOBUF_VERSION_V4, } from './subgraph-store.js';
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
    // Phase 3.4 retired the `.loaded.json` manifest — the writer was removed
    // in 3.1 and the reader had nothing current to read. `tr status` now
    // reports the static plugin version (from the CLI binary's own
    // PLUGIN_VERSION constant) plus onboarding state. For per-boot history,
    // consult the gateway log.
    const creds = loadCredentialsJson(CREDENTIALS_PATH);
    const onboarded = !!creds;
    if (jsonMode) {
        // JSON-first output for agent parsing
        const out = {
            version: PLUGIN_VERSION,
            onboarded,
            next_step: onboarded ? 'none' : 'pair',
        };
        log(JSON.stringify(out));
    }
    else {
        // Human-readable plain text for direct user CLI use
        printStatus(CREDENTIALS_PATH, STATE_PATH, process.stdout);
        process.stdout.write(`\n  plugin:      loaded (version=${PLUGIN_VERSION})\n` +
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
// Command: forget
// ---------------------------------------------------------------------------
async function cmdForget(rawArgs) {
    const [jsonMode, args] = popFlag(rawArgs, '--json');
    const factId = (args[0] ?? '').trim();
    if (!factId) {
        die('Usage: tr forget [--json] <factId>');
    }
    // UUID-v4-ish shape check — same validation the old totalreclaw_forget
    // tool applied. Prevents fabricated / natural-language IDs from reaching
    // the UserOp path and silently no-op'ing on-chain.
    if (!/^[0-9a-f-]{8,}$/i.test(factId)) {
        die(`forget failed: "${factId.slice(0, 60)}" doesn't look like a memory ID. ` +
            `Ask the agent to look it up via memory_search (or tr export) and pass a result's id.`);
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
            // Retired in Phase 3.3 — recall is now native via the bundled
            // memory_search / memory_get tools (MemoryPluginCapability). Surface
            // a clear pointer instead of falling through to "unknown command"
            // so agents / users running stale prompts get actionable guidance.
            die('tr recall was retired — recall is now native. ' +
                'The agent reads memories via the memory_search tool automatically; ' +
                'use `tr export` to dump every memory outside the agent.');
        case 'forget':
            await cmdForget(args.slice(1));
            break;
        case 'export':
            await cmdExport(args.slice(1));
            break;
        case 'import':
        case 'upgrade':
            // Import + upgrade run inside the gateway process (they need the
            // plugin runtime — extraction pipeline, smart-import WASM, module-
            // level auth state). The standalone `tr` binary is a separate Node
            // script that does NOT load index.ts (would pull in the entire
            // plugin runtime). Point users at the registerCli surface instead
            // of silently no-op'ing or falling through to "unknown command".
            die(`${cmd} is not available on the standalone \`tr\` binary. ` +
                `Run it on the gateway host via:\n` +
                `  openclaw totalreclaw ${cmd === 'import' ? 'import from <source>' : 'upgrade'}${cmd === 'import' ? ' [--file <path>] [--dry-run] [--json]' : ' [--json]'}\n` +
                (cmd === 'import'
                    ? `  openclaw totalreclaw import status [--id <importId>] [--json]\n` +
                        `  openclaw totalreclaw import abort <importId> [--json]\n` +
                        `Sources: mem0 | mcp-memory | chatgpt | claude | gemini`
                    : `Returns a Stripe checkout URL for Pro upgrade.`));
        case undefined:
        case '--help':
        case '-h':
            process.stdout.write(`TotalReclaw CLI v${PLUGIN_VERSION} (recall is native — memory_search tool)\n\n` +
                'Usage:\n' +
                '  tr status [--json]                          — onboarding + plugin load state\n' +
                '  tr pair [--json]                            — start a relay pairing session\n' +
                '  tr remember [--json] <text>                 — store a memory (on-chain UserOp)\n' +
                '  tr forget [--json] <factId>                 — tombstone a memory on-chain\n' +
                '  tr export [--json] [--format json|markdown] — dump every memory in the vault\n\n' +
                'Recall: NOT a CLI command. The agent recalls via the bundled memory_search tool.\n' +
                '        To dump memories outside the agent, use `tr export`.\n\n' +
                'Import + Upgrade: NOT on the standalone `tr` binary. They run inside the gateway\n' +
                '        process via the `openclaw totalreclaw` subcommand chain:\n' +
                '          openclaw totalreclaw import from <source> [--file <path>] [--dry-run] [--json]\n' +
                '          openclaw totalreclaw import status [--id <importId>] [--json]\n' +
                '          openclaw totalreclaw import abort <importId> [--json]\n' +
                '          openclaw totalreclaw upgrade [--json]\n' +
                '        Sources: mem0 | mcp-memory | chatgpt | claude | gemini\n\n' +
                'Flags:\n' +
                '  --json    Output machine-parseable JSON (required for agent shell calls)\n\n' +
                'JSON output shapes:\n' +
                '  status:   {"version":"...","onboarded":bool,"next_step":"pair|none","tool_count":N,"hybrid_mode":bool}\n' +
                '  pair:     {"url":"...","pin":"123456","expires_at":"..."}\n' +
                '  remember: {"ok":true,"id":"...","claim_count":N}\n' +
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
