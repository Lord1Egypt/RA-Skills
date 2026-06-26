#!/usr/bin/env npx ts-node
// Dependencies: npm install eventsource @types/eventsource ts-node typescript
/**
 * ValueScan Stream Monitor (TypeScript)
 *
 * Usage:
 *   npx ts-node monitor.ts --market [--config=~/.vs-monitor/config.json]
 *   npx ts-node monitor.ts --signal [--tokens=BTC,ETH] [--config=~/.vs-monitor/config.json]
 */

import * as crypto from 'crypto';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import EventSource from 'eventsource';

const PID_DIR = path.join(os.homedir(), '.vs-monitor');

interface Config {
    apiKey: string;
    secretKey: string;
    outputDir: string;
    streamBaseUrl?: string;
    apiBaseUrl?: string;
}

// ── Auth ──────────────────────────────────────────────────────────────────────

function hmacHex(secretKey: string, message: string): string {
    return crypto.createHmac('sha256', secretKey).update(message).digest('hex');
}

function buildStreamUrl(base: string, endpoint: string, apiKey: string, secretKey: string, tokens?: string): string {
    const timestamp = Date.now().toString();
    const nonce = crypto.randomUUID();
    const sign = hmacHex(secretKey, timestamp + nonce);
    const params = new URLSearchParams({ apiKey, timestamp, nonce, sign });
    if (tokens) params.set('tokens', tokens);
    return `${base}${endpoint}?${params.toString()}`;
}

function buildApiHeaders(apiKey: string, secretKey: string, body: string): Record<string, string> {
    const timestamp = Date.now().toString();
    const sign = hmacHex(secretKey, timestamp + body);
    return {
        'X-API-KEY': apiKey,
        'X-TIMESTAMP': timestamp,
        'X-SIGN': sign,
        'Content-Type': 'application/json; charset=utf-8',
    };
}

// ── Token resolution ──────────────────────────────────────────────────────────

async function resolveTokenIds(symbols: string[], apiKey: string, secretKey: string, apiBaseUrl: string): Promise<string[]> {
    const tokenIds: string[] = [];
    for (const symbol of symbols) {
        const body = JSON.stringify({ search: symbol });
        const headers = buildApiHeaders(apiKey, secretKey, body);
        try {
            const resp = await fetch(`${apiBaseUrl}/api/open/v1/vs-token/list`, {
                method: 'POST', headers, body,
            });
            const data = await resp.json() as { data?: Array<{ id: number; symbol: string }> };
            const records = data.data ?? [];
            if (records.length === 0) {
                console.warn(`[warn] Symbol not found: ${symbol}`);
                continue;
            }
            const match = records.find(r => r.symbol.toUpperCase() === symbol.toUpperCase()) ?? records[0];
            if (match) tokenIds.push(match.id.toString());
            else console.warn(`[warn] Symbol not found: ${symbol}`);
        } catch (e) {
            console.warn(`[warn] Failed to resolve symbol ${symbol}:`, e);
        }
    }
    return tokenIds;
}

// ── File writing ──────────────────────────────────────────────────────────────

function writeMarket(content: string, outputDir: string): void {
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const timeStr = now.toTimeString().slice(0, 8);
    const dir = path.join(outputDir, '大盘分析');
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(path.join(dir, `大盘分析-${dateStr}.txt`), `[${timeStr}]\n${content}\n---\n`, 'utf-8');
}

function writeSignal(payload: string, outputDir: string): void {
    const msg = JSON.parse(payload) as { type: string; content: string };
    let inner: { symbol?: string } = {};
    try { inner = JSON.parse(msg.content); } catch { /* ignore */ }
    const symbol = inner.symbol ?? 'UNKNOWN';
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const timeStr = now.toTimeString().slice(0, 8);
    const dir = path.join(outputDir, '代币信号', dateStr);
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(path.join(dir, `${symbol}.txt`), `[${timeStr}] [${msg.type}]\n${msg.content}\n---\n`, 'utf-8');
}

// ── PID management ────────────────────────────────────────────────────────────

function writePid(mode: string): void {
    fs.mkdirSync(PID_DIR, { recursive: true });
    fs.writeFileSync(path.join(PID_DIR, `${mode}.pid`), process.pid.toString());
}

function cleanupPid(mode: string): void {
    const pidFile = path.join(PID_DIR, `${mode}.pid`);
    if (fs.existsSync(pidFile)) fs.unlinkSync(pidFile);
}

// ── Monitor ───────────────────────────────────────────────────────────────────

function runMarket(config: Config): void {
    const base = config.streamBaseUrl ?? 'https://stream.valuescan.ai';
    const url = buildStreamUrl(base, '/stream/market/subscribe', config.apiKey, config.secretKey);
    const es = new EventSource(url);

    es.addEventListener('market', (event: MessageEvent) => {
        writeMarket(event.data, config.outputDir);
    });

    es.onerror = () => { console.error('SSE connection error'); es.close(); process.exit(1); };
}

async function runSignal(config: Config, tokens?: string): Promise<void> {
    const base = config.streamBaseUrl ?? 'https://stream.valuescan.ai';
    let tokenParam: string | undefined;

    if (tokens) {
        const symbols = tokens.split(',').map(s => s.trim()).filter(Boolean);
        const apiBase = config.apiBaseUrl ?? 'https://api.valuescan.io';
        const ids = await resolveTokenIds(symbols, config.apiKey, config.secretKey, apiBase);
        if (ids.length === 0) {
            console.error('Error: none of the specified tokens could be resolved');
            process.exit(1);
        }
        tokenParam = ids.join(',');
    }

    const url = buildStreamUrl(base, '/stream/signal/subscribe', config.apiKey, config.secretKey, tokenParam);
    const es = new EventSource(url);

    es.addEventListener('signal', (event: MessageEvent) => {
        writeSignal(event.data, config.outputDir);
    });

    es.onerror = () => { console.error('SSE connection error'); es.close(); process.exit(1); };
}

// ── Entry point ───────────────────────────────────────────────────────────────

function loadConfig(configPath: string): Config {
    const resolved = configPath.startsWith('~') ? path.join(os.homedir(), configPath.slice(1)) : configPath;
    return JSON.parse(fs.readFileSync(resolved, 'utf-8'));
}

function getFlag(args: string[], flag: string): boolean {
    return args.includes(flag);
}

function getFlagValue(args: string[], flag: string): string | undefined {
    const entry = args.find(a => a.startsWith(`${flag}=`));
    return entry ? entry.slice(flag.length + 1) : undefined;
}

async function main(): Promise<void> {
    const args = process.argv.slice(2);
    const isMarket = getFlag(args, '--market');
    const isSignal = getFlag(args, '--signal');
    const tokens = getFlagValue(args, '--tokens');
    const configPath = getFlagValue(args, '--config') ?? path.join(PID_DIR, 'config.json');

    if (!isMarket && !isSignal) {
        console.error('Error: specify --market or --signal');
        process.exit(1);
    }
    if (isMarket && isSignal) {
        console.error('Error: use --market or --signal in separate processes');
        process.exit(1);
    }

    const config = loadConfig(configPath);
    const mode = isMarket ? 'market' : 'signal';
    writePid(mode);

    const cleanup = () => { cleanupPid(mode); process.exit(0); };
    process.on('SIGTERM', cleanup);
    process.on('SIGINT', cleanup);

    if (isMarket) {
        runMarket(config);
    } else {
        await runSignal(config, tokens);
    }
}

main().catch(err => { console.error(err); process.exit(1); });
