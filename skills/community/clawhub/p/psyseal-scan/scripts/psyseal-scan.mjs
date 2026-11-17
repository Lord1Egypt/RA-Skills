#!/usr/bin/env node
// CLI de psyseal-scan. Solo lectura: sin red, sin escrituras, sin ejecutar nada externo.
import fs from 'node:fs';
import { runScan, VERSION } from '../src/scan.mjs';
import { renderJson, renderText } from '../src/report.mjs';
import { PLATFORM_IDS } from '../src/platforms/index.mjs';

const HELP = {
  es: `psyseal-scan v${VERSION} — revisión local y de solo lectura de tus agentes de IA

Busca por sí mismo los agentes de OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw y NanoClaw que haya en esta computadora.

Uso: node scripts/psyseal-scan.mjs [opciones]
     node scripts/psyseal-scan.mjs mcp     (servidor MCP por stdio, para Claude, Cursor, Codex y otros clientes MCP)

  --path <carpeta>         Revisa esa carpeta (cualquier agente; si no reconoce la plataforma, revisa credenciales y memoria)
  --platform <id>          Solo esa plataforma: openclaw, hermes, nanobot, picoclaw, zeroclaw, nanoclaw
  --agent <id>             Revisa solo ese agente
  --workspace <ruta>       OpenClaw: carpeta del workspace (por defecto la que indica tu config)
  --config <ruta>          OpenClaw: openclaw.json (por defecto ~/.openclaw/openclaw.json o OPENCLAW_CONFIG_PATH)
  --usage <archivo|->      OpenClaw: salida de openclaw gateway usage-cost --days 30 --json  (gasto real; "-" lee de la entrada estándar)
  --session-tokens <n>     OpenClaw: tamaño de tu sesión principal en tokens (mira /context); afina el estimado del latido
  --billing <api|subscription|auto>   OpenClaw: cómo pagas a tu proveedor (por defecto: auto)
  --price <in,out,lectura,escritura>  Precio propio en USD por millón de tokens (modelos no listados)
  --lang <es|en>           Idioma del reporte (por defecto según tu sistema)
  --json                   Reporte en JSON
  --no-cta                 Sin mensaje final
  --ascii                  Texto sin acentos ni símbolos (terminales viejas de Windows)
  --exit-zero              Termina con código 0 aunque haya hallazgos altos (útil si lo corre un agente)
  -h, --help               Esta ayuda

Códigos de salida: 0 sin hallazgos altos · 1 hay hallazgos altos · 2 error de uso.
`,
  en: `psyseal-scan v${VERSION} — local, read-only review of your AI agents

Finds the OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw and NanoClaw agents on this computer by itself.

Usage: node scripts/psyseal-scan.mjs [options]
       node scripts/psyseal-scan.mjs mcp     (MCP server over stdio, for Claude, Cursor, Codex and other MCP clients)

  --path <folder>          Review that folder (any agent; if the platform is unknown, it checks credentials and memory)
  --platform <id>          Only that platform: openclaw, hermes, nanobot, picoclaw, zeroclaw, nanoclaw
  --agent <id>             Review only that agent
  --workspace <path>       OpenClaw: workspace folder (default: the one your config points to)
  --config <path>          OpenClaw: openclaw.json (default ~/.openclaw/openclaw.json or OPENCLAW_CONFIG_PATH)
  --usage <file|->         OpenClaw: output of openclaw gateway usage-cost --days 30 --json  (real spend; "-" reads stdin)
  --session-tokens <n>     OpenClaw: size of your main session in tokens (see /context); sharpens the heartbeat estimate
  --billing <api|subscription|auto>   OpenClaw: how you pay your provider (default: auto)
  --price <in,out,read,write>         Your own price in USD per million tokens (unlisted models)
  --lang <es|en>           Report language (default: from your system)
  --json                   JSON report
  --no-cta                 No closing message
  --ascii                  Plain ASCII output, no accents or symbols (old Windows terminals)
  --exit-zero              Exit 0 even with high findings (useful when an agent runs it)
  -h, --help               This help

Exit codes: 0 no high findings · 1 high findings present · 2 usage error.
`,
};

function guessLang(env) {
  const v = String(env.PSYSEAL_LANG || env.LC_ALL || env.LC_MESSAGES || env.LANG || '').toLowerCase();
  return v.startsWith('es') ? 'es' : v.startsWith('en') ? 'en' : 'es';
}

function parseArgs(argv, env) {
  const o = { lang: guessLang(env), json: false, cta: true, exitZero: false, ascii: env.PSYSEAL_ASCII === '1' };
  const needsValue = new Set(['--workspace', '--config', '--agent', '--usage', '--session-tokens', '--billing', '--price', '--lang', '--path', '--platform']);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    let key = a;
    let val;
    const eq = a.indexOf('=');
    if (a.startsWith('--') && eq > 0) {
      key = a.slice(0, eq);
      val = a.slice(eq + 1);
    }
    if (key === '-h' || key === '--help') o.help = true;
    else if (key === '--json') o.json = true;
    else if (key === '--no-cta') o.cta = false;
    else if (key === '--exit-zero') o.exitZero = true;
    else if (key === '--ascii') o.ascii = true;
    else if (needsValue.has(key)) {
      if (val === undefined) val = argv[++i];
      if (val === undefined || val.startsWith('--')) throw new Error(`Falta el valor de ${key}`);
      o[key.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = val;
    } else throw new Error(`Opción desconocida: ${a}`);
  }
  return o;
}

function parsePrice(s) {
  const parts = String(s).split(',').map((x) => Number(x.trim()));
  if (parts.length !== 4 || parts.some((n) => !Number.isFinite(n) || n < 0)) {
    throw new Error('--price espera 4 números: entrada,salida,lectura,escritura (USD por millón de tokens)');
  }
  const [inp, out, read, write] = parts;
  return { in: inp, out, read, w5: write, w1h: inp * 2 };
}

function main() {
  const env = process.env;
  let args;
  try {
    args = parseArgs(process.argv.slice(2), env);
  } catch (e) {
    process.stderr.write(`${e.message}\n\n${HELP[guessLang(env)]}`);
    return 2;
  }
  if (!['es', 'en'].includes(args.lang)) {
    process.stderr.write('--lang debe ser es o en\n');
    return 2;
  }
  if (args.help) {
    process.stdout.write(HELP[args.lang]);
    return 0;
  }

  const opts = { env, config: args.config, workspace: args.workspace, agent: args.agent, lang: args.lang, path: args.path, platform: args.platform };
  try {
    if (args.platform !== undefined && !PLATFORM_IDS.includes(args.platform)) throw new Error(`--platform debe ser uno de: ${PLATFORM_IDS.join(', ')}`);
    if (args.path !== undefined) {
      let st;
      try {
        st = fs.statSync(args.path);
      } catch {
        throw new Error(`--path: no existe la carpeta ${args.path}`);
      }
      if (!st.isDirectory()) throw new Error('--path debe ser una carpeta');
    }
    if (args.billing !== undefined) {
      if (!['api', 'subscription', 'auto'].includes(args.billing)) throw new Error('--billing debe ser api, subscription o auto');
      opts.billing = args.billing;
    }
    if (args.sessionTokens !== undefined) {
      const n = Number(args.sessionTokens);
      if (!Number.isFinite(n) || n <= 0) throw new Error('--session-tokens debe ser un número positivo');
      opts.sessionTokens = n;
    }
    if (args.price !== undefined) opts.price = parsePrice(args.price);
    if (args.usage !== undefined) {
      if (args.usage === '-') {
        const buf = fs.readFileSync(0);
        if (buf.length > 20 * 1024 * 1024) throw new Error('--usage: la entrada supera 20 MB');
        opts.usageText = buf.toString('utf8');
      } else {
        const st = fs.statSync(args.usage);
        if (!st.isFile() || st.size > 20 * 1024 * 1024) throw new Error('--usage debe ser un archivo de menos de 20 MB');
        opts.usageText = fs.readFileSync(args.usage, 'utf8');
      }
    }
  } catch (e) {
    process.stderr.write(`${e.message}\n`);
    return 2;
  }

  const report = runScan(opts);
  process.stdout.write(args.json ? `${renderJson(report)}\n` : renderText(report, { lang: args.lang, cta: args.cta, ascii: args.ascii }));
  return report.summary.counts.high > 0 && !args.exitZero ? 1 : 0;
}

const argv0 = process.argv[2];
if (argv0 === 'mcp' && process.argv.length === 3) {
  const { serveMcp } = await import('../src/mcp.mjs');
  serveMcp();
} else if (argv0 === 'mcp') {
  process.stderr.write('Usage: psyseal-scan mcp   (no options; the MCP client passes them per call)\n');
  process.exitCode = 2;
} else {
  process.exitCode = main();
}
