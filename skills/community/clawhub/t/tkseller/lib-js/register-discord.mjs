/**
 * 注册 /tkseller 斜杠命令到 Discord（guild scope，立刻生效，无 1 小时缓存）。
 *
 * 用法：
 *   node register-discord.mjs
 */
import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const OPENCLAW_CONFIG = join(homedir(), '.openclaw', 'openclaw.json');

const COMMAND_DEF = {
  name: 'tkseller',
  description: 'TKSeller 自动带货 (SaaS)',
  description_localizations: { 'zh-CN': 'TKSeller 自动带货' },
  type: 1,
  options: [
    {
      name: 'url',
      description: '指定视频 URL（抖音/TikTok 等），留空则推荐热门',
      type: 3,
      required: false,
    },
  ],
};

function loadCfg() {
  return JSON.parse(readFileSync(OPENCLAW_CONFIG, 'utf-8'));
}

function getProxy(cfg) {
  let p = (cfg.channels?.discord || {}).proxy;
  if (!p) {
    const env = cfg.env?.vars || {};
    p = env.HTTPS_PROXY || env.HTTP_PROXY;
  }
  return p || null;
}

// Node 18+ global fetch doesn't support proxies natively.
// For proxy support, use the ProxyAgent from undici (built-in in Node 18+).
async function fetchWithProxy(url, options, proxy) {
  if (!proxy) return fetch(url, options);
  try {
    // undici is bundled with Node 18+
    const { ProxyAgent } = await import('undici');
    const dispatcher = new ProxyAgent(proxy);
    return fetch(url, { ...options, dispatcher });
  } catch {
    // fallback: ignore proxy
    return fetch(url, options);
  }
}

async function main() {
  const cfg = loadCfg();
  const discord = cfg.channels?.discord || {};
  const token = discord.token;
  if (!token) {
    console.log(JSON.stringify({ ok: false, error: 'discord token missing' }));
    process.exit(1);
  }

  const proxy = getProxy(cfg);
  const headers = {
    'Authorization': `Bot ${token}`,
    'Content-Type': 'application/json',
  };

  // 1) 拿 application id
  const meResp = await fetchWithProxy(
    'https://discord.com/api/v10/applications/@me',
    { headers, signal: AbortSignal.timeout(15000) },
    proxy,
  );
  const me = await meResp.json();
  const appId = me.id;
  if (!appId) {
    console.log(JSON.stringify({ ok: false, error: `cannot get app id: ${JSON.stringify(me)}` }));
    process.exit(2);
  }

  // 2) 列出 bot 加入的所有 guild
  const guildsResp = await fetchWithProxy(
    'https://discord.com/api/v10/users/@me/guilds',
    { headers, signal: AbortSignal.timeout(15000) },
    proxy,
  );
  const guilds = await guildsResp.json();
  if (!Array.isArray(guilds)) {
    console.log(JSON.stringify({ ok: false, error: `list guilds failed: ${JSON.stringify(guilds)}` }));
    process.exit(3);
  }

  const results = [];

  // 注册 guild command（立即生效，无缓存，不 @ bot 和 @ bot 都能用）
  for (const g of guilds) {
    const gid = g.id;
    const gname = g.name;
    if (!gid) continue;
    const url = `https://discord.com/api/v10/applications/${appId}/guilds/${gid}/commands`;
    try {
      const r = await fetchWithProxy(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(COMMAND_DEF),
        signal: AbortSignal.timeout(20000),
      }, proxy);
      const ok = r.status === 200 || r.status === 201;
      const body = await r.json();
      results.push({
        guild: gname,
        guild_id: gid,
        status: r.status,
        ok,
        cmd_id: ok ? body.id : null,
        error: ok ? null : JSON.stringify(body).slice(0, 200),
      });
    } catch (e) {
      results.push({ guild: gname, guild_id: gid, ok: false, error: e.message });
    }
  }

  const summary = {
    ok: results.length ? results.every(r => r.ok) : true,
    app_id: appId,
    guild_count: results.length,
    results,
  };
  console.log(JSON.stringify(summary, null, 2));
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
