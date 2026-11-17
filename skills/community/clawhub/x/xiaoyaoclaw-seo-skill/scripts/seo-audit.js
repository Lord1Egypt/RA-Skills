#!/usr/bin/env node
/**
 * seo-audit.js — 轻量技术 SEO 快检脚本入口（零依赖，Node 18+）
 *
 * 用法：
 *   node seo-audit.js <domain> [more-domains...]
 *   例：node seo-audit.js dtsola.com landoo.me project.xiaoyaosai.com
 *
 * 检查项：
 *   1. 裸域 DNS A 记录（无 A → 🔴）
 *   2. http:// 是否 301 → https（200 并存 → 🔴 重复内容）
 *   3. www/裸域 跳转归一（都 200 → 🟠）
 *   4. robots.txt / sitemap.xml / llms.txt 真实性（⚠️ HTML fallback 检测）
 *   5. 首页 title / meta description / canonical / H1 数量 / JSON-LD / viewport / lang
 *
 * 输出：按 🔴🟠🟡 分级的控制台报告。schema 检测是静态的，JS 注入的 JSON-LD
 *   检测不到 —— 需浏览器渲染复核（见 references/schema.md）。
 *
 * 语言 / Language：用法说明与输出默认中文，可改为英文或其他语言
 *   （output language is your choice, not a constraint）。
 *
 * 代码结构与安全边界（便于逐文件审阅）：
 *   - 本文件：参数校验 + 逐域名检查流程 + 分级摘要（不直接碰 socket）
 *   - scripts/lib/limits.js：全部硬上限（域名数 / 字节 / 跳数 / 超时 / 端口）
 *   - scripts/lib/net-guard.js：公网地址校验（预检 + **建连时逐地址校验**，防 DNS 重绑定）、终端注入净化
 *   - scripts/lib/http-fetch.js：只读 GET —— 80/443 限定、重定向逐跳复核、
 *     响应体字节上限（按解压后计）、「不下载不需要的正文」
 *   - scripts/lib/html-meta.js：首页 HTML 的静态标签提取（纯函数，无网络）
 *
 * 只读：不写文件、不改远端内容、不登录、不提交表单、不发 POST、不探端口、
 *   不访问非 http(s) 协议、不把抓到的内容外发到任何第三方。
 *
 * 退出码：0 = 正常完成（无论发现多少问题）；非 0 = 脚本自身错误。
 */
'use strict';

const net = require('node:net');
const dns = require('node:dns').promises;
const { MAX_DOMAINS, MAX_BYTES_HTML } = require('./lib/limits');
const { safe, isBlockedIp } = require('./lib/net-guard');
const { timeout, probe, getText } = require('./lib/http-fetch');
const { looksLikeHtml, extractMeta } = require('./lib/html-meta');

async function checkDomain(domain) {
  console.log(`\n========== ${domain} ==========`);
  const issues = { red: [], orange: [], yellow: [] };

  // 0. 确定实际可访问的 host（裸域无 DNS 时 fallback 到 www）
  const isWwwInput = domain.startsWith('www.');
  const bareDomain = isWwwInput ? domain.slice(4) : domain;

  // 1. 裸域 DNS A 记录
  let bareHasA = false;
  try {
    const recs = await dns.resolve4(bareDomain);
    bareHasA = true;
    console.log(`[dns] ${bareDomain} A 记录: ${safe(recs.join(', '), 200)}`);
    issues.yellow.push('裸域有 A 记录，但请确认裸域是否 301 到 www（版本归一）');
  } catch {
    console.log(`[dns] ${bareDomain} ❌ 无 A 记录（只有 www 可访问?）`);
    issues.red.push('裸域无 DNS A 记录：用户输入不带 www 域名打不开，外链若用裸域全失效 → DNS 控制台加 A 记录并 301 归一');
  }

  // 2. http → https（对规范主机探测；若输入是裸域且无 DNS，用 www 探测并注明）
  const httpHost = (!bareHasA && !isWwwInput) ? `www.${bareDomain}` : domain;
  if (httpHost !== domain) console.log(`[note] 裸域无 DNS，后续检查 fallback 到 ${httpHost}`);
  const httpProbe = await probe(`http://${httpHost}/`);
  if (httpProbe.error) {
    console.log(`[http] http://${httpHost} ERROR ${safe(httpProbe.error, 120)}`);
  } else if (httpProbe.status === 301 || httpProbe.status === 308) {
    console.log(`[http] http://${httpHost} -> ${httpProbe.status} → ${safe(httpProbe.location, 200)}`);
    issues.yellow.push('http 已 301，确认目标是 https 规范版本');
  } else if (httpProbe.status === 200) {
    console.log(`[http] http://${httpHost} -> 200 ⚠️ http/https 并存无跳转`);
    issues.red.push('http:// 返回 200 未 301 到 https：重复内容权重分散 + 明文传输 → 服务器/CDN 配 http→https 301');
  } else {
    console.log(`[http] http://${httpHost} -> ${httpProbe.status}${httpProbe.location ? ' → ' + safe(httpProbe.location, 200) : ''}`);
  }

  // 3. www/裸域 版本归一探测（仅对裸域或 www 域名有意义；多级子域跳过）
  const isSubdomain = domain.split('.').length > 2 && !isWwwInput;
  if (isSubdomain) {
    console.log(`[www] ${domain} 是多级子域，跳过 www/裸域归一探测（子域站点无此问题）`);
  } else {
    const other = isWwwInput ? bareDomain : `www.${bareDomain}`;
    const wwwProbe = await probe(`https://${other}/`);
    if (wwwProbe.error) {
      console.log(`[www] https://${other} ERROR ${safe(wwwProbe.error, 120)}`);
    } else if (wwwProbe.status === 301 || wwwProbe.status === 308) {
      console.log(`[www] https://${other} -> ${wwwProbe.status} → ${safe(wwwProbe.location, 200)}`);
    } else if (wwwProbe.status === 200) {
      // 输入版本本身可访问（200）且另一版本也 200 → 真双版本问题；
      // 输入版本不可访问时，另一版本 200 属正常 fallback
      const inputProbe = await probe(`https://${domain}/`);
      const inputOk = !inputProbe.error && (inputProbe.status === 200);
      if (inputOk) {
        console.log(`[www] https://${other} -> 200 ⚠️ ${isWwwInput ? '裸域' : 'www'}版本也可访问`);
        issues.orange.push(`https://${other} 返回 200 未跳转：${isWwwInput ? '裸域' : 'www'}与 ${domain} 双版本并存 → 统一 301 到 canonical 版本`);
      } else {
        console.log(`[www] https://${other} -> 200（${domain} 不可访问，${other} 为可访问版本）`);
      }
    } else {
      console.log(`[www] https://${other} -> ${wwwProbe.status}`);
    }
  }

  // 4. 关键文件真实性（robots / sitemap / llms.txt）
  for (const f of ['/robots.txt', '/sitemap.xml', '/llms.txt']) {
    const r = await getText(`https://${httpHost}${f}`);
    if (!r.ok) {
      console.log(`[file] ${f} -> ${r.status || safe(r.error, 120)}${r.status === 404 ? '（不存在）' : ''}`);
      if (f === '/robots.txt' && r.status === 404) issues.orange.push('robots.txt 404：无法控制抓取与 AI bot 策略 → 补真实 robots.txt');
      if (f === '/sitemap.xml' && r.status === 404) issues.red.push('sitemap.xml 404：收录全靠爬虫自己发现，新页收录慢 → 生成真实 sitemap 并提交站长平台');
    } else {
      const isHtml = looksLikeHtml(r.text);
      const isPlain = r.ct.includes('text/plain') || r.ct.includes('application/xml') || r.ct.includes('text/xml');
      if (isHtml || (!isPlain && f !== '/robots.txt' && f !== '/sitemap.xml')) {
        console.log(`[file] ${f} -> 200 ct=${safe(r.ct, 60)} ⚠️ HTML fallback（非真实文件）`);
        if (f === '/robots.txt') issues.orange.push('robots.txt 返回 HTML fallback（文件不存在）：无法控制抓取 → 站点根放真实文本文件');
        if (f === '/sitemap.xml') issues.red.push('sitemap.xml 返回 HTML fallback（文件不存在）→ 生成真实 XML sitemap');
        if (f === '/llms.txt') issues.yellow.push('llms.txt 返回 HTML fallback：AI 可读入口缺失 → 补真实 llms.txt（AI 引用红利）');
      } else {
        console.log(`[file] ${f} -> 200 ct=${safe(r.ct, 60)} ✅ 真实文件（${r.text.length} 字符）`);
        if (f === '/robots.txt') {
          const hasSitemap = /sitemap:/i.test(r.text);
          // 全站屏蔽判定：Disallow: / 独占一行（路径仅 "/" 后跟空白/注释/行尾）
          const blockedAll = /^\s*disallow:\s*\/\s*(#.*)?$/gim.test(r.text);
          console.log(`       sitemap 引用: ${hasSitemap ? '✅' : '⚠️ 无'} | 全站屏蔽: ${blockedAll ? '⚠️ 是' : '否'}`);
          if (!hasSitemap) issues.yellow.push('robots.txt 未引用 Sitemap → 加一行 Sitemap: <绝对URL>');
          if (blockedAll) issues.red.push('robots.txt 疑似全站 Disallow: / → 检查是否误屏蔽');
        }
        if (f === '/sitemap.xml') {
          const urlCount = (r.text.match(/<url>/g) || []).length;
          const isIndex = /<sitemapindex/i.test(r.text);
          console.log(`       ${isIndex ? 'sitemap index' : 'URL 数: ' + urlCount}`);
        }
      }
    }
    await timeout(250);
  }

  // 5. 首页关键标签（HTML 用较大的 1 MB 上限；远端字符串打印前一律 safe()）
  const home = await getText(`https://${httpHost}/`, { maxBytes: MAX_BYTES_HTML });
  console.log(`[home] https://${httpHost}/ -> ${home.ok ? home.status + ' (' + home.text.length + ' 字符)' : safe(home.error || home.status, 120)}`);
  if (home.ok && !looksLikeHtml(home.text)) {
    console.log('       ⚠️ 首页返回非 HTML（可能是 API/重定向页）');
  } else if (home.ok) {
    const m = extractMeta(home.text);
    console.log(`       title: ${m.title ? safe(m.title) : '❌ 无'}`);
    console.log(`       meta description: ${m.metaDesc ? safe(m.metaDesc, 120) : '❌ 无'}`);
    console.log(`       canonical: ${m.canonical ? safe(m.canonical, 200) : '❌ 无'}`);
    const h1s = m.h1Samples.map((s) => safe(s, 60));
    console.log(`       H1: ${m.h1Count} 个${h1s.length ? ' → ' + JSON.stringify(h1s) : ''} | H2: ${m.h2Count} 个`);
    console.log(`       JSON-LD: ${m.jsonldCount} 个${m.jsonldTypes.length ? ' → ' + m.jsonldTypes.map((t) => safe(t, 40)).join(',') : ''}（⚠️ 静态检测，JS 注入需浏览器复核）`);
    console.log(`       viewport: ${m.viewport ? '✅' : '❌ 无'} | lang: ${m.lang ? safe(m.lang, 20) : '❌ 无'} | robots meta: ${m.robotsMeta ? safe(m.robotsMeta, 60) : '无'}`);
    if (!m.title) issues.red.push('首页无 title');
    else if (m.title.length > 70) issues.yellow.push(`首页 title 过长（${m.title.length} 字符，建议 50-60）`);
    if (!m.metaDesc) issues.orange.push('首页缺 meta description → 补 150-160 字符描述');
    if (!m.canonical) issues.orange.push('首页缺 canonical → 补自引用 canonical（配合 http/https 归一）');
    if (m.h1Count === 0) issues.orange.push('首页无 H1 → 结构信号缺失');
    else if (m.h1Count > 1) issues.orange.push(`首页 ${m.h1Count} 个 H1 → 收敛为 1 个，其余降 H2/H3`);
    if (!m.viewport) issues.orange.push('无 viewport meta → 移动端渲染异常');
    if (!m.lang) issues.yellow.push('html 缺 lang 属性');
    if (m.jsonldCount === 0) issues.yellow.push('静态检测 JSON-LD = 0（JS 注入需浏览器复核；若真无 → 补 Organization/WebSite schema）');
  }

  // 输出分级摘要
  const fmt = (arr, icon) => arr.map((x) => `  ${icon} ${x}`).join('\n');
  console.log('\n--- 分级问题摘要 ---');
  if (!issues.red.length && !issues.orange.length && !issues.yellow.length) {
    console.log('  ✅ 未发现明显问题（静态检查范围内）');
  } else {
    if (issues.red.length) console.log('🔴 高危:\n' + fmt(issues.red, '•'));
    if (issues.orange.length) console.log('🟠 中危:\n' + fmt(issues.orange, '•'));
    if (issues.yellow.length) console.log('🟡 优化:\n' + fmt(issues.yellow, '•'));
  }
}

(async () => {
  const rawDomains = process.argv.slice(2);
  if (!rawDomains.length) {
    console.log('用法: node seo-audit.js <domain> [more-domains...]');
    console.log('例:   node seo-audit.js dtsola.com www.landoo.me project.xiaoyaosai.com');
    process.exit(1);
  }
  if (rawDomains.length > MAX_DOMAINS) {
    console.log(`ERROR: 单次最多 ${MAX_DOMAINS} 个域名（收到 ${rawDomains.length} 个）—— 分批运行，避免批量探测拖垮本机。`);
    process.exit(2);
  }
  // 输入规范化 + 白名单校验：只接受裸主机名，剔除协议/路径/端口/凭据等
  const domains = [];
  for (const raw of rawDomains) {
    const cleaned = safe(raw, 253).replace(/^https?:\/\//i, '').replace(/\/.*$/, '').replace(/^[^@]*@/, '');
    if (!/^[a-zA-Z0-9]([a-zA-Z0-9.\-]*[a-zA-Z0-9])?$/.test(cleaned)) {
      console.log(`ERROR: 非法域名，已跳过：${safe(raw, 80)}（只接受形如 example.com 的主机名）`);
      process.exit(2);
    }
    // 内网/保留字面量直接拒绝（域名会在每次请求前再解析校验一次）
    if (net.isIP(cleaned) && isBlockedIp(cleaned)) {
      console.log(`ERROR: ${cleaned} 属于内网/保留地址，本脚本只审计公网站点。`);
      process.exit(2);
    }
    domains.push(cleaned);
  }
  for (const d of domains) {
    await checkDomain(d);
    await timeout(300);
  }
  console.log('\nDONE');
})();
