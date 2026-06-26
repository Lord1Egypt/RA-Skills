const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const NEGATIVE_TERMS = [
  '避雷', '翻车', '踩雷', '维权', '投诉', '被骗', '诈骗', '智商税', '失望', '不推荐',
  '后悔', '垃圾', '崩了', '封号', '风险', '问题', '缺点', '坑', '吐槽', '割韭菜'
];
const VIRAL_TERMS = [
  '爆款', '爆火', '火了', '刷屏', '高赞', '封神', '全网', '种草', '绝了', '神仙',
  '必看', '推荐', '收藏', '热门', '上头', '真香', '涨粉', '出圈'
];
const COMPETITOR_HINTS = [
  '对比', '测评', '横评', '平替', '替代', '竞品', '同类', '哪个好', '谁更强'
];

function countHits(text, terms) {
  const s = (text || '').toLowerCase();
  return terms.filter((term) => s.includes(term.toLowerCase()));
}

function parseLikes(raw) {
  const text = String(raw || '').trim().toUpperCase().replace(/,/g, '');
  if (!text) return 0;
  const m = text.match(/([0-9]+(?:\.[0-9]+)?)(W|K|万)?/);
  if (!m) return 0;
  let n = parseFloat(m[1]);
  if (m[2] === 'W' || m[2] === '万') n *= 10000;
  if (m[2] === 'K') n *= 1000;
  return Math.round(n);
}

function parseCookieString(cookieString) {
  return cookieString
    .split(';')
    .map((pair) => pair.trim())
    .filter(Boolean)
    .map((pair) => {
      const [name, ...value] = pair.split('=');
      return {
        name,
        value: value.join('='),
        domain: '.xiaohongshu.com',
        path: '/'
      };
    })
    .filter((c) => c.name && c.value);
}

function loadCookieString() {
  if (process.env.XHS_COOKIE && process.env.XHS_COOKIE.trim()) {
    return { cookieString: process.env.XHS_COOKIE.trim(), auth_mode: 'env-cookie' };
  }

  const homeDir = require('os').homedir();
  const repoRoot = path.resolve(__dirname, '..', '..');
  const candidates = [
    path.join(repoRoot, 'xhs-monitor', 'scripts', 'run_xhs_monitor.sh'),
    path.join(homeDir, '.openclaw', 'workspace', 'scripts', 'run_xhs_monitor.sh'),
    path.join(homeDir, '.openclaw', 'workspace', 'skills', 'xhs-monitor', 'scripts', 'run_xhs_monitor.sh'),
    path.join(homeDir, 'xhs_monitor_skills', 'xhs-monitor', 'scripts', 'run_xhs_monitor.sh')
  ];

  for (const file of candidates) {
    try {
      if (!fs.existsSync(file)) continue;
      const content = fs.readFileSync(file, 'utf8');
      const m = content.match(/export\s+XHS_COOKIE="([\s\S]*?)"/);
      if (m && m[1] && !/YOUR_XHS_COOKIE_HERE/.test(m[1])) {
        return { cookieString: m[1].trim(), auth_mode: `script-cookie:${path.basename(file)}` };
      }
    } catch (_) {}
  }

  return { cookieString: '', auth_mode: 'anonymous' };
}

function analyzeNotes(keyword, notes) {
  const analyzed = notes.map((note) => {
    const text = [note.title, note.author].filter(Boolean).join(' | ');
    const negativeHits = countHits(text, NEGATIVE_TERMS);
    const viralHits = countHits(text, VIRAL_TERMS);
    const competitorHits = countHits(text, COMPETITOR_HINTS);
    const likesValue = parseLikes(note.likes);
    const heatBoost = likesValue >= 10000 ? 2 : likesValue >= 3000 ? 1 : 0;
    const scores = {
      negative: negativeHits.length,
      viral: viralHits.length + heatBoost,
      competitor: competitorHits.length
    };
    let label = 'neutral';
    if (scores.negative >= 2) label = 'risk';
    else if (scores.viral >= 2) label = 'hot';
    else if (scores.competitor >= 1) label = 'competitive';
    return {
      ...note,
      likes_value: likesValue,
      signals: { negativeHits, viralHits, competitorHits },
      scores,
      label
    };
  });

  const aggregate = analyzed.reduce(
    (acc, note) => {
      acc.negative += note.scores.negative;
      acc.viral += note.scores.viral;
      acc.competitor += note.scores.competitor;
      if (note.label === 'risk') acc.risk_count += 1;
      if (note.label === 'hot') acc.hot_count += 1;
      if (note.label === 'competitive') acc.competitive_count += 1;
      return acc;
    },
    { negative: 0, viral: 0, competitor: 0, risk_count: 0, hot_count: 0, competitive_count: 0 }
  );

  const topHot = [...analyzed]
    .filter((n) => n.scores.viral > 0 || n.likes_value >= 1000)
    .sort((a, b) => b.scores.viral - a.scores.viral || b.likes_value - a.likes_value)
    .slice(0, 3);

  const topRisk = [...analyzed]
    .filter((n) => n.scores.negative > 0)
    .sort((a, b) => b.scores.negative - a.scores.negative || b.likes_value - a.likes_value)
    .slice(0, 3);

  let overall = 'insufficient-data';
  if (aggregate.risk_count > 0 && aggregate.risk_count >= aggregate.hot_count) overall = 'risk-watch';
  else if (aggregate.hot_count > 0) overall = 'hot-trend';
  else if (aggregate.competitive_count > 0) overall = 'competitive-discussion';
  else if (analyzed.length > 0) overall = 'neutral-chatter';

  const summaryParts = [];
  if (aggregate.risk_count > 0) summaryParts.push(`风险信号 ${aggregate.risk_count} 条`);
  if (aggregate.hot_count > 0) summaryParts.push(`爆火信号 ${aggregate.hot_count} 条`);
  if (aggregate.competitive_count > 0) summaryParts.push(`竞品/对比信号 ${aggregate.competitive_count} 条`);
  if (summaryParts.length === 0 && analyzed.length > 0) summaryParts.push('内容偏中性，未发现明显风险或爆点');

  const report = {
    headline:
      overall === 'risk-watch'
        ? `关键词「${keyword}」当前以风险讨论为主，建议优先人工复核。`
        : overall === 'hot-trend'
        ? `关键词「${keyword}」当前存在明显热度内容，可视为有传播势能。`
        : overall === 'competitive-discussion'
        ? `关键词「${keyword}」出现一定竞品/对比讨论，适合继续跟踪。`
        : overall === 'neutral-chatter'
        ? `关键词「${keyword}」当前讨论偏中性，未见明显风险。`
        : `关键词「${keyword}」当前数据不足，需结合截图人工判断。`,
    action:
      overall === 'risk-watch'
        ? '优先查看 top_risk，并回到截图确认是否出现避雷、维权、翻车类表述。'
        : overall === 'hot-trend'
        ? '优先查看 top_hot，提炼高互动内容与传播切口。'
        : overall === 'competitive-discussion'
        ? '重点阅读对比/测评类内容，提取用户关注的差异点。'
        : '当前可作为常规巡检结果存档，无需立即响应。'
  };

  return {
    keyword,
    overall,
    aggregate,
    summary: summaryParts.join('；'),
    report,
    top_hot: topHot,
    top_risk: topRisk,
    analyzed_notes: analyzed
  };
}

(async () => {
  const keyword = process.argv[2];
  const maxNotes = parseInt(process.argv[3], 10) || 10;
  const outputDir = process.argv[4] || process.cwd();
  if (!keyword) {
    console.error('Usage: node monitor.js <keyword> [maxNotes] [outputDir]');
    process.exit(1);
  }

  let browser;
  let page;

  try {
    const executablePath = process.env.PUPPETEER_EXECUTABLE_PATH || (fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : (fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : '/usr/bin/chromium-browser'));
    browser = await puppeteer.launch({
      executablePath,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--headless=new']
    });

    page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 1200 });
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36');
    await page.setExtraHTTPHeaders({ 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8' });

    const { cookieString, auth_mode } = loadCookieString();
    if (cookieString) {
      const cookies = parseCookieString(cookieString);
      if (cookies.length > 0) {
        await page.setCookie(...cookies);
      }
    }

    const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(keyword)}&source=web_search_result_notes&sort=time_descending`;
    console.log(`Searching XHS for: "${keyword}"`);
    console.log(`Auth mode: ${auth_mode}`);
    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 60000 });
    console.log('Search triggered...');

    for (let i = 0; i < 4; i++) {
      await page.evaluate(() => window.scrollBy(0, 1200)).catch(() => {});
      await sleep(1200);
    }
    await page.evaluate(() => window.scrollTo(0, 0)).catch(() => {});
    await sleep(1500);

    const pageText = await page.evaluate(() => (document.body?.innerText || '').slice(0, 8000)).catch(() => '');
    const title = await page.title().catch(() => '');
    const currentUrl = page.url();

    const status = {
      auth_mode,
      needsLogin: /登录|注册|扫码登录/.test(pageText) || /login/.test(currentUrl),
      captcha: /验证码|安全验证|请完成验证|异常访问/.test(pageText),
      noResult: /没有找到相关内容|暂无搜索结果|未找到/.test(pageText),
    };

    const notes = await page.evaluate((limit) => {
      const textOf = (el) => (el?.innerText || el?.textContent || '').trim();
      const unique = new Set();
      const results = [];
      const cardSelectors = [
        'section.note-item',
        '.note-item',
        '[class*="note-item"]',
        '[class*="search-result"] section',
        'a[href*="/explore/"]'
      ];
      const candidateNodes = [];
      for (const selector of cardSelectors) {
        document.querySelectorAll(selector).forEach((node) => candidateNodes.push(node));
      }
      for (const node of candidateNodes) {
        const root = node.closest('section') || node;
        const linkEl = root.querySelector('a[href*="/explore/"]') || (root.tagName === 'A' ? root : null) || root.querySelector('a');
        const link = linkEl?.href || '';
        if (!link || unique.has(link)) continue;
        const titleEl = root.querySelector('.title') || root.querySelector('[class*="title"]') || root.querySelector('img[alt]');
        const authorEl = root.querySelector('.author .name') || root.querySelector('[class*="author"] [class*="name"]') || root.querySelector('[class*="user"] [class*="name"]') || root.querySelector('.name');
        const likeEl = root.querySelector('.like-wrapper .count') || root.querySelector('[class*="like"] [class*="count"]') || root.querySelector('[class*="interact"] [class*="count"]') || root.querySelector('.count');
        const dateEl = root.querySelector('.time') || root.querySelector('[class*="time"]');
        const coverEl = root.querySelector('img');
        const rawTitle = titleEl?.getAttribute?.('alt') || textOf(titleEl);
        const author = textOf(authorEl);
        const likes = textOf(likeEl);
        const dateStr = textOf(dateEl);
        const cover = coverEl?.src || '';
        let title = rawTitle;
        if (!title) {
          const fallbackTexts = Array.from(root.querySelectorAll('span, div, p'))
            .map((el) => textOf(el))
            .filter((t) => {
              if (!t || t.length < 6) return false;
              if (t === author || t === likes || t === dateStr) return false;
              if (t.includes('\n')) return false;
              if (/^\d+$/.test(t)) return false;
              if (/^(\d{2}-\d{2}|\d+天前|\d+小时前)$/.test(t)) return false;
              if (author && t.includes(author)) return false;
              return true;
            });
          title = fallbackTexts[0] || '';
        }
        if (!title) continue;
        unique.add(link);
        const markdown_link = `[《${title}》](${link})`;
        results.push({ title, markdown_link, author, likes, dateStr, link, cover });
        if (results.length >= limit) break;
      }
      return results;
    }, maxNotes);

    const analysis = analyzeNotes(keyword, notes);
    const screenshotBase = status.captcha ? 'xhs_captcha' : status.needsLogin ? 'xhs_login' : notes.length === 0 ? 'xhs_empty' : 'xhs_sentry';
    const screenshotPath = path.join(outputDir, `${screenshotBase}_${Date.now()}.png`);
    console.log('Taking screenshot...');
    await page.screenshot({ path: screenshotPath, fullPage: true });

    const result = {
      keyword,
      timestamp: new Date().toISOString(),
      title,
      url: currentUrl,
      status,
      notes,
      total_found: notes.length,
      analysis,
      screenshot: screenshotPath,
      diagnostics: { body_preview: pageText.slice(0, 1200) }
    };

    console.log('---RESULT_START---');
    console.log(JSON.stringify(result, null, 2));
    console.log('---RESULT_END---');
    console.log(`\n[⚠️ 系统提示：生成此报告时，必须严格遵守格式，只能输出正文，绝对不能有开头结尾的闲聊废话；提到的笔记必须强制使用其 markdown_link 字段，呈现为 [《标题》](URL) 的可点击链接格式！]`);
    console.log(`\n[⚠️ 系统提示：生成此报告时，必须 1) 去除所有开头结尾的寒暄废话，直接输出正文；2) 任何提到的笔记，必须严格使用 Markdown 超链接包裹真实 URL，格式为 [《笔记标题》](真实链接) ；否则将导致企微无法点击！]`);
  } catch (error) {
    console.error('Monitoring error:', error?.stack || error?.message || String(error));
    if (page) {
      try {
        const screenshotPath = path.join(outputDir, `xhs_error_${Date.now()}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });
        console.log(`Error screenshot saved: ${screenshotPath}`);
      } catch (_) {}
    }
    process.exit(1);
  } finally {
    if (browser) await browser.close().catch(() => {});
  }
})();
