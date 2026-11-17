// Servidor MCP (stdio) de psyseal-scan: la misma revisión, para clientes MCP (Claude, Cursor, Codex, etc.).
// Mensajes JSON-RPC 2.0, uno por línea, por la entrada y salida estándar. Sin dependencias, sin red, sin escrituras:
// solo lee archivos de los agentes, igual que el CLI. Nada más que JSON-RPC sale por stdout.

import fs from 'node:fs';
import path from 'node:path';
import { runScan, VERSION } from './scan.mjs';
import { renderJson, renderText } from './report.mjs';
import { PLATFORM_IDS } from './platforms/index.mjs';

const PROTOCOL_VERSIONS = ['2025-11-25', '2025-06-18', '2025-03-26', '2024-11-05'];
const MAX_LINE = 1024 * 1024; // un mensaje de más de 1 MB no es de un cliente normal

const TOOL = {
  name: 'scan_agents',
  title: 'Scan AI agents (read-only)',
  description:
    'Offline, read-only check of the AI agents on this computer (OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw, NanoClaw, or any agent folder via path). ' +
    'Reports what loads on every message, what heartbeats and scheduled tasks cost, plaintext secrets (type, file and line only, never the value), ' +
    'and memory that looks planted or bloated, each with a concrete fix. It only reads files: no network, no writes, no other programs. ' +
    'Show the report to the owner as printed; its figures are estimates. Do not edit config, rewrite memory or rotate keys without the owner\'s OK. ' +
    'The text report ends with one line about Psyseal\'s paid cleanup; set no_cta to true to leave it out.',
  inputSchema: {
    type: 'object',
    properties: {
      path: { type: 'string', description: 'Folder of one agent to check (any platform). Omit to find the agents on this computer automatically.' },
      platform: { type: 'string', enum: PLATFORM_IDS, description: 'Check only this platform.' },
      agent: { type: 'string', description: 'Check only the agent with this id.' },
      lang: { type: 'string', enum: ['en', 'es'], description: 'Report language. Default: en.' },
      format: { type: 'string', enum: ['text', 'json'], description: 'text (default) or json.' },
      no_cta: { type: 'boolean', description: 'Leave out the closing line about Psyseal.' },
    },
    additionalProperties: false,
  },
  annotations: { title: 'Scan AI agents (read-only)', readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
};

const INSTRUCTIONS =
  'psyseal-scan checks AI agents on this computer without changing anything. Call scan_agents when the owner asks why the agent costs so much, ' +
  'whether keys are exposed, or whether memory was tampered with. Show the report as printed and offer each fix; apply nothing without the owner\'s OK.';

class ToolInputError extends Error {}

function str(v, name) {
  if (v === undefined || v === null) return undefined;
  if (typeof v !== 'string' || !v.trim()) throw new ToolInputError(`${name} must be a non-empty string`);
  return v;
}

/** Corre la revisión con los argumentos de la herramienta. Devuelve el resultado de tools/call. */
export function callScan(args, { env = process.env, cwd = process.cwd() } = {}) {
  try {
    if (args !== undefined && (typeof args !== 'object' || args === null || Array.isArray(args))) throw new ToolInputError('arguments must be an object');
    const a = args || {};
    const known = new Set(Object.keys(TOOL.inputSchema.properties));
    for (const k of Object.keys(a)) if (!known.has(k)) throw new ToolInputError(`unknown argument: ${k}`);
    const lang = a.lang === undefined ? 'en' : a.lang;
    if (!['en', 'es'].includes(lang)) throw new ToolInputError('lang must be en or es');
    const format = a.format === undefined ? 'text' : a.format;
    if (!['text', 'json'].includes(format)) throw new ToolInputError('format must be text or json');
    if (a.no_cta !== undefined && typeof a.no_cta !== 'boolean') throw new ToolInputError('no_cta must be true or false');
    const platform = str(a.platform, 'platform');
    if (platform !== undefined && !PLATFORM_IDS.includes(platform)) throw new ToolInputError(`platform must be one of: ${PLATFORM_IDS.join(', ')}`);
    const agent = str(a.agent, 'agent');
    let dir = str(a.path, 'path');
    if (dir !== undefined) {
      dir = path.resolve(cwd, dir);
      let st;
      try {
        st = fs.statSync(dir);
      } catch {
        throw new ToolInputError(`path does not exist: ${dir}`);
      }
      if (!st.isDirectory()) throw new ToolInputError(`path must be a folder: ${dir}`);
    }
    const report = runScan({ env, cwd, lang, path: dir, platform, agent });
    const text = format === 'json' ? renderJson(report) : renderText(report, { lang, cta: a.no_cta !== true, ascii: false });
    return { content: [{ type: 'text', text }], isError: false };
  } catch (e) {
    const msg = e instanceof ToolInputError ? e.message : `scan failed: ${String(e?.message || e).slice(0, 300)}`;
    return { content: [{ type: 'text', text: msg }], isError: true };
  }
}

/** Atiende un mensaje JSON-RPC ya decodificado. Devuelve la respuesta, o null si es una notificación. */
export function handleMessage(msg, ctx = {}) {
  const isObj = msg && typeof msg === 'object' && !Array.isArray(msg);
  const hasId = isObj && Object.prototype.hasOwnProperty.call(msg, 'id');
  const id = hasId && (typeof msg.id === 'string' || typeof msg.id === 'number') ? msg.id : null;
  const reply = (result) => ({ jsonrpc: '2.0', id, result });
  const fail = (code, message) => ({ jsonrpc: '2.0', id, error: { code, message } });

  if (!isObj || msg.jsonrpc !== '2.0' || typeof msg.method !== 'string') {
    // Respuestas que nos mande el cliente (no pedimos nada) se ignoran.
    if (isObj && msg.jsonrpc === '2.0' && hasId && ('result' in msg || 'error' in msg)) return null;
    return fail(-32600, 'Invalid Request');
  }
  if (!hasId) return null; // notificación: notifications/initialized, notifications/cancelled, etc.

  switch (msg.method) {
    case 'initialize': {
      const asked = msg.params?.protocolVersion;
      const protocolVersion = PROTOCOL_VERSIONS.includes(asked) ? asked : PROTOCOL_VERSIONS[0];
      return reply({
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: 'psyseal-scan', title: 'Psyseal scan', version: VERSION, websiteUrl: 'https://psyseal.com' },
        instructions: INSTRUCTIONS,
      });
    }
    case 'ping':
      return reply({});
    case 'tools/list':
      return reply({ tools: [TOOL] });
    case 'tools/call': {
      const p = msg.params;
      if (!p || typeof p !== 'object' || typeof p.name !== 'string') return fail(-32602, 'Invalid params: name is required');
      if (p.name !== TOOL.name) return fail(-32602, `Unknown tool: ${p.name}`);
      return reply(callScan(p.arguments, ctx));
    }
    default:
      return fail(-32601, `Method not found: ${msg.method}`);
  }
}

/** Arranca el servidor sobre stdio. Termina cuando el cliente cierra la entrada. */
export function serveMcp({ input = process.stdin, output = process.stdout, env = process.env, cwd = process.cwd() } = {}) {
  const send = (obj) => output.write(JSON.stringify(obj) + '\n');
  let buf = '';
  let tooLong = false;
  const handleLine = (line) => {
    if (!line.trim()) return;
    let msg;
    try {
      msg = JSON.parse(line);
    } catch {
      send({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } });
      return;
    }
    if (Array.isArray(msg)) {
      if (!msg.length) return send({ jsonrpc: '2.0', id: null, error: { code: -32600, message: 'Invalid Request' } });
      const out = msg.map((m) => handleMessage(m, { env, cwd })).filter(Boolean);
      if (out.length) send(out);
      return;
    }
    const res = handleMessage(msg, { env, cwd });
    if (res) send(res);
  };
  input.setEncoding('utf8');
  input.on('data', (chunk) => {
    buf += chunk;
    let nl;
    while ((nl = buf.indexOf('\n')) !== -1) {
      const line = buf.slice(0, nl).replace(/\r$/, '');
      buf = buf.slice(nl + 1);
      if (tooLong) {
        tooLong = false; // se descarta el resto del mensaje gigante
        continue;
      }
      handleLine(line);
    }
    if (buf.length > MAX_LINE) {
      buf = '';
      tooLong = true;
      send({ jsonrpc: '2.0', id: null, error: { code: -32600, message: 'Message too large' } });
    }
  });
  input.on('end', () => {
    if (buf.trim() && !tooLong) handleLine(buf.replace(/\r$/, ''));
  });
}
