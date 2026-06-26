/**
 * 3.2.0 secure-onboarding CLI wizard.
 *
 * Runs as `openclaw totalreclaw onboard` via OpenClaw's `api.registerCli`
 * plugin hook. Lives on a pure TTY surface — stdout/stderr/stdin — and
 * NEVER routes any of its I/O through the LLM provider, the gateway
 * transcript, or any session-persisted channel. This is the load-bearing
 * property of the 3.2.0 threat model: the recovery phrase is generated,
 * displayed, entered, and persisted ENTIRELY on the user's local machine.
 *
 * Dispatch (registered from `index.ts`):
 *   openclaw totalreclaw onboard    — interactive generate / import / skip
 *   openclaw totalreclaw status     — show current onboarding state
 *
 * Scope (per user ratification 2026-04-19):
 *   - LOCAL USERS ONLY in 3.2.0. Import on a remote OpenClaw gateway is
 *     not supported; QR-pairing is deferred to 3.3.0.
 *   - Two paths: generate a new 12-word BIP-39 mnemonic, or import an
 *     existing one. Skip exits without side-effects.
 *
 * Non-goals:
 *   - This file does NOT touch the gateway's `register()` flow. It neither
 *     calls `initialize()` nor drives key derivation. Users re-enter their
 *     chat session after running the wizard; `initialize()` reads the new
 *     credentials.json on the next `ensureInitialized()` call. Forcing a
 *     re-init here would require importing the full plugin key-derivation
 *     stack, which this module intentionally avoids.
 *
 * Architectural constraints:
 *   - No network. No `process.env` reads. No outbound markers in comments
 *     — see skill/scripts/check-scanner.mjs. The module imports nothing
 *     that contains a network surface.
 *   - Minimal deps. Uses `@scure/bip39` (already a transitive dep via
 *     `@totalreclaw/core`) for mnemonic generation + validation. Uses
 *     `node:readline/promises` for interactive prompts. No `inquirer`,
 *     no `readline-sync`.
 *
 * See docs/plans/2026-04-20-plugin-320-secure-onboarding.md (internal repo,
 * commit dc6bddd) for the full design rationale.
 */
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import { generateMnemonic, validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english.js';
import { defaultPairPendingPath, deletePairPendingFile, writeCredentialsJson, loadCredentialsJson, writeOnboardingState, loadOnboardingState, } from './fs-helpers.js';
// ---------------------------------------------------------------------------
// User-facing strings (centralised so tests can assert on them + localisation
// has one place to grow into later).
// ---------------------------------------------------------------------------
/**
 * 3.3.1-rc.18 (issue #95) — deprecation warning for the interactive
 * phrase-print branch. Emitted to STDERR (never stdout) so it is visible
 * to humans but does not pollute any pipe consuming the wizard's output.
 *
 * The phrase-print branch will be REMOVED in the next RC after rc.18.
 * Users running on a TTY can still complete the flow in rc.18; agents
 * MUST use `--pair-only` or the `totalreclaw_pair` tool today.
 */
export const PHRASE_PRINT_DEPRECATION_WARNING = '\nDEPRECATION (issue #95): the interactive `openclaw totalreclaw onboard` flow\n' +
    '  prints your recovery phrase to this terminal. This is being removed in the\n' +
    '  next release candidate. For agent / scripted invocation, use:\n' +
    '    openclaw totalreclaw onboard --pair-only\n' +
    '  which emits ONLY {pair_url, pin} JSON and routes the phrase through the\n' +
    '  browser flow (never on stdout).\n\n';
export const COPY = {
    welcome: '\nTotalReclaw — Secure onboarding\n\n' +
        'TotalReclaw is an end-to-end encrypted memory vault for AI agents.\n' +
        'Your memories are encrypted with a key only you control, stored on-chain\n' +
        'so they persist across sessions and clients.\n',
    menu: 'How would you like to set up TotalReclaw?\n\n' +
        '  [1] Generate a new recovery phrase (first-time users)\n' +
        '  [2] Import an existing TotalReclaw recovery phrase (returning users)\n' +
        '  [3] Skip for now — memory features stay disabled\n',
    menuPrompt: 'Enter 1, 2, or 3: ',
    alreadyActive: '\nTotalReclaw is already set up and active on this machine.\n' +
        'Run `openclaw totalreclaw status` for details, or delete\n' +
        '~/.totalreclaw/credentials.json to start over.\n',
    generateWarning: '\nABOUT YOUR RECOVERY PHRASE\n\n' +
        '  - It is the ONLY key to your encrypted memories. TotalReclaw servers\n' +
        '    cannot recover it. If you lose it, your memories are gone forever.\n' +
        '  - You can import it into other TotalReclaw clients (Hermes, MCP) to\n' +
        '    recall the same memories everywhere.\n' +
        '  - You can restore your account on a new machine at any time using\n' +
        '    this phrase.\n' +
        '  - It is NOT a blockchain wallet. Do NOT fund it with crypto, and do\n' +
        '    NOT reuse an existing wallet\'s phrase here.\n',
    importWarning: '\nBEFORE YOU PASTE AN EXISTING PHRASE\n\n' +
        '  Your TotalReclaw recovery phrase must be DEDICATED to TotalReclaw.\n\n' +
        '  - NEVER import a phrase that controls a crypto wallet with funds.\n' +
        '  - NEVER import a phrase used with another service (Metamask, Ledger,\n' +
        '    Trust, seed backups, etc.).\n' +
        '  - If your only copy of a TotalReclaw phrase is on a shared wallet,\n' +
        '    STOP NOW, move your funds off the wallet, and pick a new dedicated\n' +
        '    phrase.\n',
    importRemoteLimitation: '\nNote: in 3.2.0, import only works when you run OpenClaw locally on the\n' +
        'machine that will hold the credentials. Importing an existing vault on a\n' +
        'remote OpenClaw gateway is not yet supported — that arrives in 3.3.0 via\n' +
        'QR-pairing.\n',
    importPrompt: 'Paste your 12-word recovery phrase (input hidden): ',
    clipboardHint: '\nTip: prefer typing the phrase into a password manager over copy-paste.\n' +
        'OS clipboards can be captured by other apps.\n',
    ackPromptTemplate: 'Type word #%N% from your phrase: ',
    postSuccessGenerate: '\nDone. Your recovery phrase is saved at ~/.totalreclaw/credentials.json\n' +
        '(mode 0600). Memory tools are now active.\n\n' +
        '  Next: run `openclaw chat` to start. I will automatically remember\n' +
        '        important things and recall relevant context across sessions.\n\n' +
        '  To view your phrase again later on this machine, open credentials.json\n' +
        '  directly. Keep it safe — on a new machine, run this wizard again and\n' +
        '  choose "import" with this phrase.\n',
    postSuccessImport: '\nDone. Your phrase is saved at ~/.totalreclaw/credentials.json (mode 0600).\n' +
        'Memory tools are now active.\n\n' +
        '  Next: run `openclaw chat` to start. Existing memories tied to this\n' +
        '        phrase will be available via totalreclaw_recall.\n',
    skipped: '\nSkipped. Run `openclaw totalreclaw onboard` anytime to resume.\n' +
        'Memory tools remain disabled until you do.\n',
    ackFailed: '\nWord mismatch. Please write the phrase down carefully and run this\n' +
        'wizard again. No credentials have been written.\n',
    importInvalid: '\nInvalid recovery phrase (12 words required, checksum must match).\n' +
        'No credentials have been written. Run the wizard again with the\n' +
        'correct phrase.\n',
    existingPhraseHint: '\nA recovery phrase already exists at ~/.totalreclaw/credentials.json.\n' +
        'Delete that file first to replace it, or re-import with the same phrase.\n',
    statusHeader: 'TotalReclaw status\n',
    statusFresh: '  onboarding: not complete\n' +
        '  next step:  run `openclaw totalreclaw onboard` on this machine\n' +
        '  note:       your recovery phrase will be shown on the terminal, never in chat.\n',
    statusActive: '  onboarding: complete\n' +
        '  credentials: ~/.totalreclaw/credentials.json (mode 0600)\n' +
        '  state:       ~/.totalreclaw/state.json\n',
};
// ---------------------------------------------------------------------------
// IO factory — default builds a readline-backed prompter over process.stdin/out.
// ---------------------------------------------------------------------------
/**
 * Build a WizardIo backed by `process.stdin` / `process.stdout`. Hidden
 * input (for the import path) is implemented via direct raw-mode manipulation
 * of the TTY, which is the standard node technique when no prompter library
 * is available. Falls back to non-hidden input if the process is not
 * attached to a TTY (e.g. CI / piped stdin) — the caller's responsibility
 * to decide whether that is OK.
 */
export function buildDefaultIo() {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const stdout = process.stdout;
    const stderr = process.stderr;
    async function ask(question) {
        return (await rl.question(question)).trim();
    }
    async function askHidden(question) {
        const stdin = process.stdin;
        const isTTY = stdin.isTTY === true;
        if (!isTTY || typeof stdin.setRawMode !== 'function') {
            // No TTY — fall back to visible input with a note. Safer than refusing.
            stdout.write('(input will be visible because stdin is not a TTY)\n');
            return ask(question);
        }
        stdout.write(question);
        return new Promise((resolve) => {
            const chars = [];
            const onData = (chunk) => {
                const str = chunk.toString('utf-8');
                for (const ch of str) {
                    const code = ch.charCodeAt(0);
                    if (code === 13 || code === 10) {
                        // Enter / newline → finalise
                        stdout.write('\n');
                        stdin.setRawMode(false);
                        stdin.pause();
                        stdin.off('data', onData);
                        resolve(chars.join('').trim());
                        return;
                    }
                    if (code === 3) {
                        // Ctrl-C → propagate SIGINT so the CLI exits cleanly
                        stdin.setRawMode(false);
                        stdin.pause();
                        stdin.off('data', onData);
                        process.kill(process.pid, 'SIGINT');
                        return;
                    }
                    if (code === 127 || code === 8) {
                        // Backspace / delete
                        if (chars.length > 0)
                            chars.pop();
                        continue;
                    }
                    chars.push(ch);
                }
            };
            stdin.setRawMode(true);
            stdin.resume();
            stdin.on('data', onData);
        });
    }
    return {
        stdout,
        stderr,
        ask,
        askHidden,
        close: () => rl.close(),
    };
}
// ---------------------------------------------------------------------------
// Internals
// ---------------------------------------------------------------------------
function printMnemonicGrid(mnemonic, out) {
    const words = mnemonic.trim().split(/\s+/);
    const cols = 4;
    const pad = 14;
    const lines = [];
    for (let row = 0; row * cols < words.length; row++) {
        const parts = [];
        for (let col = 0; col < cols; col++) {
            const idx = row * cols + col;
            if (idx >= words.length)
                break;
            const label = `${String(idx + 1).padStart(2, ' ')}. ${words[idx]}`;
            parts.push(label.padEnd(pad, ' '));
        }
        lines.push('  ' + parts.join(''));
    }
    out.write(lines.join('\n') + '\n');
}
/**
 * Pick three distinct random word indices (0..11) for the retype-ack challenge.
 * Overridable for tests.
 */
function defaultRandomProbeIndices() {
    const pool = [...Array(12).keys()];
    const out = [];
    for (let i = 0; i < 3; i++) {
        const pick = Math.floor(Math.random() * pool.length);
        out.push(pool[pick]);
        pool.splice(pick, 1);
    }
    return out.sort((a, b) => a - b);
}
async function runAckChallenge(mnemonic, indices, io) {
    const words = mnemonic.trim().split(/\s+/);
    for (const idx of indices) {
        const ans = await io.ask(COPY.ackPromptTemplate.replace('%N%', String(idx + 1)));
        if (ans.trim().toLowerCase() !== words[idx]) {
            return false;
        }
    }
    return true;
}
function normaliseMnemonic(input) {
    // Collapse whitespace, strip zero-width, lowercase. BIP-39 wordlist is
    // entirely lowercase ASCII; any uppercase the user paste-in gets normalised.
    return input
        .normalize('NFKC')
        .replace(/[\u200B-\u200F\uFEFF]/g, '')
        .toLowerCase()
        .trim()
        .split(/\s+/)
        .join(' ');
}
function writeCredsAndState(credentialsPath, statePath, mnemonic, createdBy) {
    const creds = { mnemonic };
    if (!writeCredentialsJson(credentialsPath, creds)) {
        throw new Error(`Could not write credentials.json at ${credentialsPath}. Check that the parent directory is writable.`);
    }
    const state = {
        onboardingState: 'active',
        createdBy,
        credentialsCreatedAt: new Date().toISOString(),
        version: '3.2.0',
    };
    if (!writeOnboardingState(statePath, state)) {
        throw new Error(`Could not write state.json at ${statePath}. Check that the parent directory is writable.`);
    }
    // 3.3.13 — sentinel cleanup. The CLI wizard finalizes setup independently
    // of the relay flow, but the user may have triggered auto-pair-on-load
    // earlier in the same dir; the .pair-pending.json sentinel must not
    // outlive credentials.json or the agent will keep surfacing a stale URL.
    deletePairPendingFile(defaultPairPendingPath(credentialsPath));
    return state;
}
// ---------------------------------------------------------------------------
// Public entry points
// ---------------------------------------------------------------------------
/**
 * Interactive onboarding wizard. Single shot — caller builds a WizardDeps and
 * awaits. All user-visible output goes to `io.stdout` / `io.stderr`; all
 * input comes from `io.ask` / `io.askHidden`. No console.log calls.
 *
 * Returns a `WizardResult`. Tests can assert on both the result and the
 * stdout buffer.
 */
export async function runOnboardingWizard(deps) {
    const { credentialsPath, statePath, io } = deps;
    const genMnemonic = deps.generateMnemonic ?? (() => generateMnemonic(wordlist, 128));
    const validate = deps.validateMnemonic ?? ((p) => validateMnemonic(p, wordlist));
    const probe = deps.randomProbeIndices ?? defaultRandomProbeIndices;
    // If onboarding is already complete on disk, short-circuit instead of
    // letting the user overwrite an existing phrase by accident.
    const existingCreds = loadCredentialsJson(credentialsPath);
    if (existingCreds?.mnemonic && typeof existingCreds.mnemonic === 'string' && existingCreds.mnemonic.trim()) {
        io.stdout.write(COPY.alreadyActive);
        const persisted = loadOnboardingState(statePath);
        return {
            choice: 'skip',
            state: persisted ?? {
                onboardingState: 'active',
                version: '3.2.0',
            },
        };
    }
    io.stdout.write(COPY.welcome);
    io.stdout.write(COPY.menu);
    const choiceRaw = await io.ask(COPY.menuPrompt);
    let choice;
    if (choiceRaw === '1' || choiceRaw.toLowerCase() === 'generate') {
        choice = 'generate';
    }
    else if (choiceRaw === '2' || choiceRaw.toLowerCase() === 'import') {
        choice = 'import';
    }
    else if (choiceRaw === '3' || choiceRaw.toLowerCase() === 'skip') {
        choice = 'skip';
    }
    else {
        io.stderr.write(`\nUnrecognised choice "${choiceRaw}". Aborting.\n`);
        return { choice: 'skip', error: `invalid-choice:${choiceRaw}` };
    }
    if (choice === 'skip') {
        io.stdout.write(COPY.skipped);
        return { choice: 'skip' };
    }
    if (choice === 'generate') {
        // 3.3.1-rc.18 (issue #95) — deprecation banner on stderr ONLY.
        // The phrase-print branch is scheduled for removal in the RC after
        // rc.18; we keep it functional in rc.18 for back-compat with users
        // running the wizard on a real TTY today.
        io.stderr.write(PHRASE_PRINT_DEPRECATION_WARNING);
        io.stdout.write(COPY.generateWarning);
        io.stdout.write(COPY.importRemoteLimitation);
        const mnemonic = genMnemonic();
        if (typeof mnemonic !== 'string' || mnemonic.trim().split(/\s+/).length !== 12) {
            io.stderr.write('\nInternal error: recovery phrase generator returned an invalid phrase.\n');
            return { choice, error: 'generator-invalid' };
        }
        io.stdout.write('\nYour recovery phrase (WRITE THIS DOWN):\n\n');
        printMnemonicGrid(mnemonic, io.stdout);
        // 3.3.0-rc.2: storage guidance canonical copy — emitted verbatim so
        // the CLI, the browser page, and any future surface share identical
        // wording. See first-run.ts COPY.STORAGE_GUIDANCE.
        io.stdout.write('\n' +
            'Your recovery phrase is 12 words. Store it somewhere safe — a password manager works well. Use it only for TotalReclaw. Don\'t reuse it anywhere else. Don\'t put funds on it.\n');
        io.stdout.write(COPY.clipboardHint);
        io.stdout.write('\n');
        const indices = probe();
        const ok = await runAckChallenge(mnemonic, indices, io);
        if (!ok) {
            io.stderr.write(COPY.ackFailed);
            return { choice, error: 'ack-failed' };
        }
        try {
            const state = writeCredsAndState(credentialsPath, statePath, mnemonic, 'generate');
            io.stdout.write(COPY.postSuccessGenerate);
            return { choice, state };
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            io.stderr.write(`\n${msg}\n`);
            return { choice, error: `write-failed:${msg}` };
        }
    }
    // choice === 'import'
    io.stdout.write(COPY.importWarning);
    io.stdout.write(COPY.importRemoteLimitation);
    const raw = await io.askHidden(COPY.importPrompt);
    const normalised = normaliseMnemonic(raw);
    const words = normalised.split(/\s+/).filter(Boolean);
    if (words.length !== 12 || !validate(normalised)) {
        io.stderr.write(COPY.importInvalid);
        return { choice, error: 'invalid-phrase' };
    }
    try {
        const state = writeCredsAndState(credentialsPath, statePath, normalised, 'import');
        io.stdout.write(COPY.postSuccessImport);
        return { choice, state };
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        io.stderr.write(`\n${msg}\n`);
        return { choice, error: `write-failed:${msg}` };
    }
}
/**
 * Print the current onboarding status to the given stdout. Safe — never
 * displays the mnemonic; only the state + file paths. Called by both the
 * `openclaw totalreclaw status` CLI subcommand and (if desired) the
 * `totalreclaw_status` tool.
 */
export function printStatus(credentialsPath, statePath, out) {
    out.write(COPY.statusHeader);
    const credExists = fs.existsSync(credentialsPath);
    const stateFileExists = fs.existsSync(statePath);
    if (credExists) {
        const creds = loadCredentialsJson(credentialsPath);
        // Accept both canonical `mnemonic` and legacy `recovery_phrase` — same
        // back-compat pattern used by fs-helpers.ts::extractBootstrapMnemonic.
        const hasMnemonic = (typeof creds?.mnemonic === 'string' && creds.mnemonic.trim().length > 0) ||
            (typeof creds?.recovery_phrase === 'string' && creds.recovery_phrase.trim().length > 0);
        if (hasMnemonic) {
            out.write(COPY.statusActive);
            if (stateFileExists) {
                const st = loadOnboardingState(statePath);
                if (st?.credentialsCreatedAt)
                    out.write(`  created:     ${st.credentialsCreatedAt}\n`);
                if (st?.createdBy)
                    out.write(`  method:      ${st.createdBy}\n`);
            }
            return;
        }
    }
    out.write(COPY.statusFresh);
}
/**
 * Run the onboarding flow without any TTY prompts. Never throws on
 * invalid input — always returns a NonInteractiveOnboardResult so the
 * CLI can render a clear JSON error.
 *
 * Security:
 *   - Never writes the phrase to stdout unless `emitPhrase === true`.
 *   - Writes credentials.json with mode 0600 via `writeCredentialsJson`.
 *   - Does NOT prompt the user. Does NOT call readline.
 */
export async function runNonInteractiveOnboard(inputs) {
    const action = inputs.mode;
    const generateFn = inputs.generateMnemonic ?? (() => generateMnemonic(wordlist, 128));
    const validateFn = inputs.validateMnemonic ?? ((p) => validateMnemonic(p, wordlist));
    // Refuse to overwrite an existing active onboarding — matches the
    // interactive wizard's shortcut. Agents can still delete the file
    // themselves if they truly want to re-onboard.
    const existing = loadCredentialsJson(inputs.credentialsPath);
    if (existing?.mnemonic &&
        typeof existing.mnemonic === 'string' &&
        existing.mnemonic.trim().length > 0) {
        return {
            ok: false,
            action,
            error: 'already-active',
            error_detail: `A recovery phrase already exists at ${inputs.credentialsPath}. Delete it first to re-onboard.`,
        };
    }
    let mnemonic;
    if (action === 'generate') {
        mnemonic = generateFn();
        if (typeof mnemonic !== 'string' || mnemonic.trim().split(/\s+/).length !== 12) {
            return {
                ok: false,
                action,
                error: 'generator-invalid',
                error_detail: 'generateMnemonic produced an invalid phrase',
            };
        }
    }
    else {
        const raw = inputs.phrase ?? '';
        if (!raw.trim()) {
            return {
                ok: false,
                action,
                error: 'missing-phrase',
                error_detail: 'mode=restore requires --phrase <12-or-24-words> or --phrase - (read from stdin).',
            };
        }
        const normalised = normaliseMnemonic(raw);
        const words = normalised.split(/\s+/).filter(Boolean);
        if ((words.length !== 12 && words.length !== 24) || !validateFn(normalised)) {
            return {
                ok: false,
                action,
                error: 'invalid-phrase',
                error_detail: 'phrase must be 12 or 24 BIP-39 words with a valid checksum.',
            };
        }
        mnemonic = normalised;
    }
    let state;
    try {
        state = writeCredsAndState(inputs.credentialsPath, inputs.statePath, mnemonic, action === 'generate' ? 'generate' : 'import');
    }
    catch (err) {
        return {
            ok: false,
            action,
            error: 'write-failed',
            error_detail: err instanceof Error ? err.message : String(err),
        };
    }
    // Derive scope address if possible — best-effort, never block success.
    let scopeAddress;
    if (inputs.deriveScopeAddress) {
        try {
            scopeAddress = await inputs.deriveScopeAddress(mnemonic);
        }
        catch {
            scopeAddress = undefined;
        }
    }
    const result = {
        ok: true,
        action,
        credentials_path: inputs.credentialsPath,
    };
    if (scopeAddress)
        result.scope_address = scopeAddress;
    if (inputs.emitPhrase)
        result.mnemonic = mnemonic;
    void state; // Touch for clarity — state is persisted via writeCredsAndState.
    return result;
}
// ---------------------------------------------------------------------------
// CLI registration
// ---------------------------------------------------------------------------
/**
 * Helper the `index.ts` registerCli hook calls to wire both subcommands
 * onto the OpenClaw program. Kept here so the wiring + the wizard live in
 * the same module — index.ts just forwards.
 *
 * `program` is the OpenClaw-provided commander Command. We attach a
 * top-level `totalreclaw` command with `onboard` + `status` subcommands.
 *
 * 3.3.1 — `onboard` now accepts:
 *   --non-interactive      Fail fast if any input would be prompted for.
 *   --json                 Emit the result as structured JSON.
 *   --mode <generate|restore>
 *                          Skip the menu prompt.
 *   --phrase <12-or-24>    Required for --mode restore. `-` reads stdin.
 *   --emit-phrase          Include the plaintext phrase in the JSON payload
 *                          (NOT recommended — the phrase lives in
 *                          credentials.json; prefer reading it there).
 *
 * 3.3.1-rc.18 — `onboard` accepts:
 *   --pair-only            Phrase-safe agent-shell flag (issue #95).
 *                          Delegates to the pair flow and emits a single
 *                          line of JSON `{v, pair_url, pin, expires_at_ms}`
 *                          to stdout. Phrase NEVER touches stdout, stderr,
 *                          or the logger in this mode. Use this for any
 *                          agent-driven setup; it is the recommended path
 *                          when a container-based agent does not have the
 *                          `totalreclaw_pair` tool injected.
 *
 *                          Requires `pairSessionsPath` + `renderPairingUrl`
 *                          to be supplied to `registerOnboardingCli`. If
 *                          absent, `--pair-only` exits non-zero with a
 *                          clear message instead of falling through to the
 *                          phrase-print branch.
 */
export function registerOnboardingCli(program, opts) {
    const tr = program
        .command('totalreclaw')
        .description('TotalReclaw encrypted memory — secure onboarding + status');
    tr.command('onboard')
        .description('Interactive onboarding: generate or import a recovery phrase (runs locally, no LLM). For agent-driven setup prefer --pair-only.')
        .option('--non-interactive', 'Exit non-zero if any input would be prompted for (agent-driven use)')
        .option('--json', 'Emit the result as a structured JSON payload. Only valid with --non-interactive.')
        .option('--mode <mode>', 'generate | restore — skip the menu prompt')
        .option('--phrase <phrase>', 'Recovery phrase for --mode restore. `-` reads from stdin.')
        .option('--emit-phrase', 'Include the plaintext phrase in the JSON payload (not recommended). Default: false.')
        .option('--pair-only', 'Phrase-safe agent-invocation mode (issue #95). Emits ONLY {v,pair_url,pin,expires_at_ms} JSON to stdout via the pair flow. Phrase never touches stdout/stderr/logger. RECOMMENDED for any agent or scripted invocation.')
        .action(async (...actionArgs) => {
        // commander: (options, cmd)
        const cliOpts = (actionArgs[0] ?? {});
        // ---------------------------------------------------------------
        // 3.3.1-rc.18 — `--pair-only` (issue #95)
        //
        // Phrase-safe agent-shell flag. Delegates to the pair flow and
        // emits a single line of JSON `{v, pair_url, pin, expires_at_ms}`
        // to stdout. By construction:
        //   - The pair flow is x25519-only — pair-crypto.ts does NOT
        //     import @scure/bip39 and never touches a recovery phrase.
        //   - No interactive prompts, no readline, no @scure/bip39 import
        //     in this code path. Phrase never enters stdout/stderr/logger.
        //   - Stays silent on status transitions (the runPairCli
        //     `pair-only` output mode suppresses banners, spinners, and
        //     all human-readable copy).
        //
        // This MUST be the path agents take when they need to set up
        // TotalReclaw via a shell. The interactive phrase-print branch
        // below is deprecated for that use case and emits a warning when
        // the user falls through to it.
        // ---------------------------------------------------------------
        if (cliOpts.pairOnly) {
            if (!opts.pairSessionsPath || !opts.renderPairingUrl) {
                process.stderr.write('--pair-only is unavailable: this OpenClaw build did not wire the pair flow into the onboard CLI. ' +
                    'Use `openclaw totalreclaw pair generate --url-pin-only` instead.\n');
                process.exit(1);
            }
            // Resolve mode. --mode restore is incompatible with --pair-only
            // since pair flow's "import" mode runs in the browser, not in
            // the CLI. Default to 'generate' silently.
            const pairMode = cliOpts.mode === 'restore' || cliOpts.mode === 'import' ? 'import' : 'generate';
            // Lazy import — keeps pair-cli + qrcode-terminal off the
            // onboarding hot path when --pair-only is not used.
            const { runPairCli, defaultRenderQr, buildDefaultPairCliIo } = await import('./pair-cli.js');
            const io = buildDefaultPairCliIo();
            try {
                const outcome = await runPairCli(pairMode, {
                    sessionsPath: opts.pairSessionsPath,
                    renderPairingUrl: opts.renderPairingUrl,
                    renderQr: defaultRenderQr,
                    io,
                    outputMode: 'pair-only',
                });
                if (outcome.status !== 'completed') {
                    process.exit(outcome.status === 'canceled' ? 130 : 1);
                }
                process.exit(0);
            }
            catch (err) {
                // CRITICAL: this catch MUST NOT include the phrase, the
                // mnemonic, or any user secret in the message. The pair flow
                // does not produce phrase material, so this is structurally
                // safe — but defense-in-depth: emit a fixed error string.
                opts.logger.error(`pair-only delegation crashed: ${err instanceof Error ? err.message : String(err)}`);
                process.stderr.write('--pair-only failed (see logs).\n');
                process.exit(2);
            }
        }
        if (cliOpts.nonInteractive) {
            // Non-interactive path — no readline, no prompts.
            const mode = cliOpts.mode === 'generate'
                ? 'generate'
                : cliOpts.mode === 'restore' || cliOpts.mode === 'import'
                    ? 'restore'
                    : null;
            if (!mode) {
                const msg = '--non-interactive requires --mode <generate|restore>. ' +
                    'Example: openclaw totalreclaw onboard --non-interactive --json --mode generate';
                if (cliOpts.json) {
                    process.stdout.write(JSON.stringify({ ok: false, error: 'missing-mode', error_detail: msg }) + '\n');
                }
                else {
                    process.stderr.write(msg + '\n');
                }
                process.exit(1);
            }
            // Resolve phrase input. `-` means read all of stdin.
            let phrase = cliOpts.phrase;
            if (phrase === '-') {
                phrase = await readAllStdin();
            }
            const result = await runNonInteractiveOnboard({
                credentialsPath: opts.credentialsPath,
                statePath: opts.statePath,
                mode,
                phrase,
                emitPhrase: cliOpts.emitPhrase === true,
                deriveScopeAddress: opts.deriveScopeAddress,
            });
            if (cliOpts.json) {
                // 3.3.1-rc.18 (issue #95) — emit deprecation on stderr when
                // the JSON payload is about to include the plaintext phrase.
                // stderr is intentional: stdout must remain a single
                // machine-parseable JSON line.
                if (cliOpts.emitPhrase && result.ok && result.mnemonic) {
                    process.stderr.write(PHRASE_PRINT_DEPRECATION_WARNING);
                }
                process.stdout.write(JSON.stringify(result) + '\n');
            }
            else {
                if (result.ok) {
                    if (result.mnemonic) {
                        process.stderr.write(PHRASE_PRINT_DEPRECATION_WARNING);
                        process.stderr.write('WARNING: --emit-phrase was set. The plaintext recovery phrase was returned.\n' +
                            'For agent-driven flows, prefer reading ~/.totalreclaw/credentials.json directly ' +
                            'in the user\'s terminal instead of echoing the phrase.\n');
                    }
                    process.stdout.write(`onboarding: ok  action=${result.action}  ` +
                        (result.scope_address ? `scope_address=${result.scope_address}  ` : '') +
                        `credentials=${result.credentials_path}\n`);
                }
                else {
                    process.stderr.write(`onboarding: ${result.error}: ${result.error_detail ?? ''}\n`);
                }
            }
            process.exit(result.ok ? 0 : 1);
        }
        if (cliOpts.json) {
            process.stderr.write('--json requires --non-interactive. Use: openclaw totalreclaw onboard --non-interactive --json --mode generate\n');
            process.exit(1);
        }
        // Interactive path — original 3.2.0 behaviour preserved in full.
        const io = buildDefaultIo();
        try {
            const result = await runOnboardingWizard({
                credentialsPath: opts.credentialsPath,
                statePath: opts.statePath,
                io,
            });
            if (result.error) {
                opts.logger.warn(`onboarding wizard exited with error: ${result.error}`);
                io.close();
                process.exit(1);
            }
            if (result.choice === 'generate' || result.choice === 'import') {
                opts.logger.info(`onboarding: state=active createdBy=${result.state?.createdBy}`);
            }
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            opts.logger.error(`onboarding wizard crashed: ${msg}`);
            io.close();
            process.exit(2);
        }
        io.close();
    });
    tr.command('status')
        .description('Show TotalReclaw onboarding state — never displays the recovery phrase')
        .action(() => {
        printStatus(opts.credentialsPath, opts.statePath, process.stdout);
    });
}
// ---------------------------------------------------------------------------
// stdin helper — reads until EOF. Used when --phrase=- is given.
// ---------------------------------------------------------------------------
async function readAllStdin() {
    const chunks = [];
    process.stdin.setEncoding('utf-8');
    return new Promise((resolve) => {
        const onData = (chunk) => chunks.push(chunk);
        const onEnd = () => {
            process.stdin.off('data', onData);
            process.stdin.off('end', onEnd);
            resolve(chunks.join(''));
        };
        process.stdin.on('data', onData);
        process.stdin.on('end', onEnd);
        // If stdin is a TTY with no data (e.g. user forgot to pipe), resolve
        // after a short grace so we don't hang forever. Tests override by
        // piping a string.
        if (process.stdin.isTTY) {
            setTimeout(() => {
                process.stdin.off('data', onData);
                process.stdin.off('end', onEnd);
                resolve(chunks.join(''));
            }, 50);
        }
    });
}
// Ensure this module is reachable for import resolution in ESM tests.
export const __modulePath = (() => {
    try {
        return path.resolve(path.dirname(new URL(import.meta.url).pathname));
    }
    catch {
        return __dirname;
    }
})();
