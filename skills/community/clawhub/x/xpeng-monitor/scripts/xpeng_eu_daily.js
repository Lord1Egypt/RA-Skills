/**
 * 获取 XPENG 欧洲市场最近 12 个月的日更明细数据
 * 数据来源：https://eu-evs.com/brands/XPENG/ALL_DAILY/Models-Daily/Year/${year}
 *
 * 用法：
 *   node xpeng_eu_daily.js [year]                  # 输出 JSON（daily + monthly_full + monthly_partial）
 *   node xpeng_eu_daily.js [year] --report         # 输出 markdown 报告（①②③ 表格，④ 综合分析留给 LLM）
 *   node xpeng_eu_daily.js [year] --email <email> --password <password>
 *
 *   year 可选，默认当前年份。
 *   --report 输出 3 个 markdown 表格（月度环比 / 全月总销量 / 车型明细），
 *   供 LLM 直接展示并附加 ④ 综合分析。
 *   如果数据页返回 302（未登录 / bot 拦截 / 会话失效，重定向目标可能为
 *   /bots、/login、/onlyNamed 等），脚本向 stdout 输出 LOGIN_REQUIRED
 *   （退出码 2），agent 见此应询问账密。
 *   提供了 --email 和 --password 时，脚本会自动登录后重试；
 *   登录成功后会话保存到 .eu-session.json，后续请求自动复用。
 *
 *   所有信号（正常输出、LOGIN_REQUIRED、ERROR|...）统一走 stdout，agent
 *   只需检查 stdout 内容即可判断后续动作，无需依赖 stderr 或退出码。
 *
 *   GET 请求内置瞬时网络错误重试（socket hang up / ECONNRESET / 超时等，
 *   指数退避重试 3 次），大多数网络抖动对调用方透明，不会输出 ERROR。
 *
 * 输出格式（单行 JSON，紧凑无缩进）：
 *   {
 *     "meta": {
 *       "latest_date": "YYYY-MM-DD", "latest_day": D, "partial_range": "1-D",
 *       "models": ["车型1", ...],                   // 基准车型列表（可能含逗号如 "P7,P7I"）
 *       "months": ["YYYY-MM", ...]                  // 12 个月，正序（最旧在前）
 *     },
 *     "daily": [
 *       {"date":"YYYY-MM-DD","month":"YYYY-MM","sales":{"车型1":N,...},"total":N}, ...
 *     ],
 *     "monthly_full": [                             // 全月汇总（所有有数据日期累加）
 *       {"month":"YYYY-MM","days":N,"sales":{...},"total":N}, ...
 *     ],
 *     "monthly_partial": [                          // 同范围汇总（仅 day ≤ latest_day，跨月公平对比用）
 *       {"month":"YYYY-MM","days":N,"range":"1-D","sales":{...},"total":N}, ...
 *     ]
 *   }
 *   车型名作为 JSON 对象键，彻底避免列错位；月度预汇总免去 LLM 手动累加。
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
const BASE_URL = 'https://eu-evs.com';
const SESSION_FILE = path.join(__dirname, '.eu-session.json');

// ---- cookie jar ----
const cookieJar = {};

function loadSession() {
  try {
    Object.assign(cookieJar, JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8')));
    return true;
  } catch {
    return false;
  }
}

function saveSession() {
  try {
    fs.writeFileSync(SESSION_FILE, JSON.stringify(cookieJar));
  } catch {
    /* 忽略写入错误 */
  }
}

function captureCookies(setCookie) {
  if (!setCookie) return;
  const list = Array.isArray(setCookie) ? setCookie : [setCookie];
  for (const entry of list) {
    const kv = entry.split(';')[0];
    const idx = kv.indexOf('=');
    if (idx > 0) cookieJar[kv.substring(0, idx).trim()] = kv.substring(idx + 1).trim();
  }
}

function cookieString() {
  return Object.entries(cookieJar)
    .map(([k, v]) => k + '=' + v)
    .join('; ');
}

// ---- HTTP ----
function httpRequest(method, urlPath, body) {
  return new Promise((resolve, reject) => {
    const headers = { 'User-Agent': UA };
    const ck = cookieString();
    if (ck) headers.Cookie = ck;
    if (body !== undefined) {
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
      headers['Content-Length'] = Buffer.byteLength(body);
      headers.Referer = BASE_URL + '/login';
      headers.Origin = BASE_URL;
    }
    const req = https.request(BASE_URL + urlPath, { method, headers }, (res) => {
      captureCookies(res.headers['set-cookie']);
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => resolve({ status: res.statusCode, body: data, headers: res.headers }));
    });
    req.on('error', reject);
    if (body !== undefined) req.write(body);
    req.end();
  });
}

// 判断是否为可重试的瞬时网络错误（socket hang up / 连接重置 / 超时 / DNS 等）
function isTransientError(err) {
  const msg = String((err && err.message) || err);
  return /socket hang up|ECONNRESET|ETIMEDOUT|ENOTFOUND|EAI_AGAIN|ECONNREFUSED|EPIPE|getaddrinfo|timeout|network is unreachable/i.test(msg);
}

// 带指数退避的重试封装（仅对 GET，避免 POST 重复提交）
// 瞬时网络抖动在脚本内部消化，避免 agent 误判脚本不可用而改用其他方式
async function httpGetRetry(urlPath, retries = 3) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await httpRequest('GET', urlPath);
    } catch (e) {
      lastErr = e;
      if (attempt < retries && isTransientError(e)) {
        const delay = 800 * Math.pow(2, attempt) + Math.floor(Math.random() * 400); // ~0.8s/1.6s/3.2s + 抖动
        await new Promise((r) => setTimeout(r, delay));
        continue;
      }
      throw e; // 非瞬时错误或重试耗尽，抛出
    }
  }
  throw lastErr;
}

const httpGet = (p) => httpGetRetry(p);
const httpPost = (p, b) => httpRequest('POST', p, b);

// ---- HTML 解析 ----
function parseHtml(html) {
  const tableStart = html.indexOf('id="latestDateTable"');
  if (tableStart < 0) return null;
  const tableEnd = html.indexOf('</table>', tableStart);
  if (tableEnd < 0) return null;
  const tableHtml = html.substring(tableStart, tableEnd);

  const trRegex = /<tr>([\s\S]*?)<\/tr>/g;
  const trs = [];
  let m;
  while ((m = trRegex.exec(tableHtml)) !== null) trs.push(m[1]);
  if (trs.length === 0) return null;

  const models = [];
  const aRegex = /<a[^>]*>([^<]+)<\/td>/g;
  while ((m = aRegex.exec(trs[0])) !== null) models.push(m[1].trim());

  const rows = [];
  const tdRegex = /<td[^>]*>([^<]*)<\/td>/g;
  for (let i = 1; i < trs.length; i++) {
    const cells = [];
    while ((m = tdRegex.exec(trs[i])) !== null) cells.push(m[1].trim());
    if (cells.length >= 2 && /^\d{4}-\d{2}-\d{2}$/.test(cells[0])) {
      const date = cells[0];
      const values = cells.slice(1).map((v) => parseInt(v, 10) || 0);
      const total = values.reduce((a, b) => a + b, 0);
      rows.push({ date, values, total });
    }
  }
  return { models, rows };
}

// ---- 业务逻辑 ----
function subtractMonths(year, month, n) {
  const total = year * 12 + (month - 1) - n;
  return { year: Math.floor(total / 12), month: (total % 12) + 1 };
}

const pad2 = (n) => String(n).padStart(2, '0');
const ymKey = (y, m) => y + '-' + pad2(m);

function isBlocked(res) {
  // eu-evs.com 对未登录 / 被判定为 bot 的请求会 302 重定向到各种页面
  // （已观察到 /bots、/login、/onlyNamed 等，后续可能继续变化）。
  // 成功的数据请求固定返回 200 + HTML 表格，因此对数据页的任何 302
  // 都视为需要登录，不再枚举重定向目标。
  return res.status === 302;
}

/** 获取指定年份数据，返回 { blocked, data }；blocked=true 表示需要登录 */
async function fetchYear(year) {
  const res = await httpGet(`/brands/XPENG/ALL_DAILY/Models-Daily/Year/${year}`);
  if (isBlocked(res)) return { blocked: true };
  if (res.status !== 200) throw new Error('HTTP_' + res.status + '_year_' + year);
  const data = parseHtml(res.body);
  if (!data) throw new Error('PARSE_FAILED_year_' + year);
  return { blocked: false, data };
}

/** 登录获取认证态 */
async function login(email, password) {
  // 1. GET /login 获取 CSRF token
  const page = await httpGet('/login');
  if (page.status !== 200) throw new Error('LOGIN_PAGE_HTTP_' + page.status);

  // 从 HTML 提取 _token（hidden input 或 meta tag）
  let token = null;
  const inputMatch = page.body.match(/name="_token"\s+(?:value|content)="([^"]+)"/i);
  if (inputMatch) {
    token = inputMatch[1];
  } else {
    const metaMatch = page.body.match(/<meta\s+name="csrf-token"\s+content="([^"]+)"/i);
    if (metaMatch) token = metaMatch[1];
  }
  if (!token) throw new Error('CSRF_TOKEN_NOT_FOUND');

  // 2. POST /login
  const body =
    '_token=' + encodeURIComponent(token) +
    '&email=' + encodeURIComponent(email) +
    '&password=' + encodeURIComponent(password);

  const res = await httpPost('/login', body);

  // Laravel 登录成功 → 302 重定向到非 /login 页面；失败 → 重定向回 /login
  if (res.status === 302) {
    const loc = res.headers.location || '';
    if (loc.includes('/login')) throw new Error('LOGIN_FAILED');
    saveSession();
    return true;
  }
  // 200 通常表示验证错误，重新显示登录表单
  if (res.status === 200) throw new Error('LOGIN_FAILED_CHECK_CREDENTIALS');
  throw new Error('LOGIN_HTTP_' + res.status);
}

// ---- 参数解析 ----
function parseArgs() {
  const args = process.argv.slice(2);
  let year = String(new Date().getFullYear());
  let email = null;
  let password = null;
  let report = false;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--email' && i + 1 < args.length) {
      email = args[++i];
    } else if (args[i] === '--password' && i + 1 < args.length) {
      password = args[++i];
    } else if (args[i] === '--report') {
      report = true;
    } else if (!args[i].startsWith('--')) {
      year = args[i];
    }
  }
  return { year: parseInt(year, 10), email, password, report };
}

// ---- 报告格式化 ----

/** 将预汇总数据格式化为 markdown 报告（①②③ 表格，④ 综合分析留给 LLM 生成） */
function formatReport(data) {
  const { meta, monthly_full, monthly_partial } = data;
  const ld = meta.latest_day;
  const models = meta.models;
  const last3p = monthly_partial.slice(-3);
  const last3f = monthly_full.slice(-3);
  const prevBase = monthly_partial.length >= 4
    ? monthly_partial[monthly_partial.length - 4].total
    : null;

  const fmtDiff = (d) => (d >= 0 ? '+' : '') + d;
  const fmtPct = (num, denom) => {
    if (denom === 0) return 'N/A';
    const pct = (num / denom) * 100;
    return (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%';
  };

  const blocks = [];

  // ① 月度环比对比
  const rows1 = [
    '| 月份 | 销量（1–' + ld + ' 日累计） | 环比变化量 | 环比百分比 |',
    '|------|-------------------|-----------|-----------|',
  ];
  let prev = prevBase;
  for (const m of last3p) {
    const diff = prev !== null ? fmtDiff(m.total - prev) : '—';
    const pct = prev !== null ? fmtPct(m.total - prev, prev) : '—';
    rows1.push('| ' + m.month + ' | ' + m.total + ' | ' + diff + ' | ' + pct + ' |');
    prev = m.total;
  }
  blocks.push('## ① 最近 3 个月月度环比对比（1-' + ld + ' 日累计）\n\n' + rows1.join('\n'));

  // ② 全月总销量
  const rows2 = [
    '| 月份 | 全月总销量 | 有数据天数 |',
    '|------|-----------|-----------|',
  ];
  last3f.forEach((m, i) => {
    const note = i === last3f.length - 1 ? '（截至 ' + ld + ' 日，月未结束）' : '';
    rows2.push('| ' + m.month + ' | ' + m.total + note + ' | ' + m.days + ' |');
  });
  blocks.push('## ② 最近 3 个月全月总销量\n\n' + rows2.join('\n'));

  // ③ 各车型销量明细
  const header3 = '| 车型 | ' + last3p.map((m) => m.month).join(' | ') + ' |';
  const sep3 = '|------|' + last3p.map(() => '------|').join('');
  const rows3 = [header3, sep3];
  for (const model of models) {
    const vals = last3p.map((m) => m.sales[model] || 0).join(' | ');
    rows3.push('| ' + model + ' | ' + vals + ' |');
  }
  rows3.push('| **合计** | **' + last3p.map((m) => m.total).join('** | **') + '** |');
  blocks.push('## ③ 最近 3 个月各车型销量明细（1-' + ld + ' 日累计）\n\n' + rows3.join('\n'));

  return blocks.join('\n\n');
}

// ---- 主流程 ----
async function main() {
  const { year: inputYear, email, password, report } = parseArgs();

  // 1. 加载已保存的会话
  loadSession();

  // 跟踪本轮是否已登录过，避免重复登录
  let loggedIn = false;

  // 统一封装：获取年份数据，被拦截时按需登录重试；
  // 仍被拦截（无凭据，或登录后仍被拦）则向 stdout 输出 LOGIN_REQUIRED 让 agent 介入
  async function fetchYearOrExit(year) {
    let r = await fetchYear(year);
    if (r.blocked && email && password && !loggedIn) {
      await login(email, password);
      loggedIn = true;
      r = await fetchYear(year);
    }
    if (r.blocked) {
      console.log('LOGIN_REQUIRED');
      process.exit(2);
    }
    return r.data;
  }

  // 2. 尝试获取基准年份数据
  const baseData = await fetchYearOrExit(inputYear);
  if (!baseData.rows.length) {
    console.log('ERROR|no_data_for_year_' + inputYear);
    process.exit(1);
  }

  // 3. 找最新日期
  const latestRow = baseData.rows[baseData.rows.length - 1];
  const [ly, lm, ld] = latestRow.date.split('-').map(Number);

  // 4. 计算 12 个月
  const targets = [];
  for (let n = 11; n >= 0; n--) targets.push(subtractMonths(ly, lm, n));
  const targetKeys = targets.map((t) => ymKey(t.year, t.month));

  // 5. 获取所需年份（跨年取数同样走 fetchYearOrExit，统一处理拦截）
  const yearsNeeded = [...new Set(targets.map((t) => t.year))];
  const yearData = { [inputYear]: baseData };
  for (const y of yearsNeeded) {
    if (yearData[y]) continue;
    yearData[y] = await fetchYearOrExit(y);
  }

  // 6. 车型对齐
  const canonicalModels = baseData.models;

  // 7. 收集数据
  const outRows = [];
  for (const t of targets) {
    const key = ymKey(t.year, t.month);
    const yd = yearData[t.year];
    if (!yd) continue;
    const idxMap = canonicalModels.map((m) => yd.models.indexOf(m));
    for (const r of yd.rows) {
      if (!r.date.startsWith(key)) continue;
      const aligned = idxMap.map((idx) => (idx >= 0 ? r.values[idx] || 0 : 0));
      const total = aligned.reduce((a, b) => a + b, 0);
      outRows.push({ date: r.date, values: aligned, total });
    }
  }

  // 8. 预计算月度汇总（FULL = 全月，PARTIAL = 1 ~ latest_day 同范围对比）
  const monthly = {};
  for (const t of targets) {
    const key = ymKey(t.year, t.month);
    const sales = {};
    for (const m of canonicalModels) sales[m] = 0;
    monthly[key] = {
      full: { days: 0, sales: { ...sales } },
      partial: { days: 0, sales: { ...sales } },
    };
  }
  for (const r of outRows) {
    const key = r.date.substring(0, 7);
    const entry = monthly[key];
    if (!entry) continue;
    const day = parseInt(r.date.substring(8, 10), 10);
    entry.full.days++;
    for (let i = 0; i < canonicalModels.length; i++) {
      entry.full.sales[canonicalModels[i]] += r.values[i];
    }
    if (day <= ld) {
      entry.partial.days++;
      for (let i = 0; i < canonicalModels.length; i++) {
        entry.partial.sales[canonicalModels[i]] += r.values[i];
      }
    }
  }

  // 9. 构建 JSON 输出
  const daily = outRows.map((r) => {
    const sales = {};
    for (let i = 0; i < canonicalModels.length; i++) {
      sales[canonicalModels[i]] = r.values[i];
    }
    return {
      date: r.date,
      month: r.date.substring(0, 7),
      sales,
      total: r.total,
    };
  });

  const monthlyFull = targets.map((t) => {
    const key = ymKey(t.year, t.month);
    const e = monthly[key].full;
    const total = canonicalModels.reduce((s, m) => s + e.sales[m], 0);
    return { month: key, days: e.days, sales: e.sales, total };
  });

  const monthlyPartial = targets.map((t) => {
    const key = ymKey(t.year, t.month);
    const e = monthly[key].partial;
    const total = canonicalModels.reduce((s, m) => s + e.sales[m], 0);
    return { month: key, range: '1-' + ld, days: e.days, sales: e.sales, total };
  });

  const data = {
    meta: {
      latest_date: latestRow.date,
      latest_day: ld,
      partial_range: '1-' + ld,
      models: canonicalModels,
      months: targetKeys,
    },
    daily,
    monthly_full: monthlyFull,
    monthly_partial: monthlyPartial,
  };

  if (report) {
    console.log(formatReport(data));
  } else {
    console.log(JSON.stringify(data));
  }
}

main().catch((e) => {
  // 错误统一走 stdout，便于 agent 捕获并原样上报给用户
  console.log('ERROR|' + e.message);
  process.exit(1);
});
