import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import {
  CdpConnection,
  findChromeExecutable,
  findExistingChromeDebugPort,
  getDefaultProfileDir,
  getFreePort,
  killChromeByProfile,
  sleep,
  waitForChromeDebugPort,
} from './weibo-utils.js';

const WEIBO_HOTSEARCH_URL = 'https://weibo.com/newlogin?tabtype=search';

export interface HotSearchItem {
  rank: number;
  title: string;
  link?: string;
  heat?: string;
  tag?: string;
  isTop?: boolean;
}

export interface FetchHotSearchOptions {
  /** 输出文件路径，默认：当前目录下 `./<YYYY-MM-DD>-weibo-hot-search.md` */
  outputPath?: string;
  /** Chrome 配置文件目录，默认：`getDefaultProfileDir()` */
  profileDir?: string;
  /** Chrome/Edge 可执行文件路径，默认：自动检测 */
  chromePath?: string;
  /** 等待热搜列表出现的超时时间（毫秒），默认：60000 */
  timeoutMs?: number;
}

// 页面快照脚本 — 在每次滚动后注入页面上下文执行。
// 返回当前 DOM 中所有可见热搜条目，不做任何过滤，
// 由 TS 层跨虚拟滚动窗口累积去重。
//
// DOM 结构（每个条目由两个兄弟节点组成）：
//   <div class="woo-box-item-flex">
//     <div class="_titout_...">                       ← 条目主体
//       <div class="_rankimg_...">
//         <img class="_ranktop_...">                  ← 置顶图标
//         <span class="_ranknum_...">3</span>          ← 排名数字
//       </div>
//       <a class="_tit_..."><span>标题</span></a>
//       <span class="wbpro-icon-...">新</span>         ← 可选标签
//       <div class="_doticon_..."></div>               ← 广告标识
//     </div>
//     <div class="_num_..."><span>热度值</span></div>  ← 热度（兄弟节点，非子节点）
//   </div>
const SNAPSHOT_SCRIPT = `(() => {
  const containers = Array.from(document.querySelectorAll('[class*="_titout_"]'));
  return containers.map(el => {
    const titleA = el.querySelector('a[class*="_tit_"]');
    const titleEl = titleA?.querySelector('span') || titleA;
    const title = titleEl?.textContent?.trim().replace(/^#|#$/g, '').trim() || '';
    const link = titleA?.href || '';

    const numSibling = el.nextElementSibling;
    const heat = numSibling?.className?.includes('_num_')
      ? (numSibling.querySelector('span')?.textContent?.trim() || '')
      : '';

    let tag = '';
    for (const span of el.querySelectorAll('span[class*="wbpro-icon"], span[class*="_label_"], span[class*="_tag_"]')) {
      const t = span.textContent?.trim();
      if (t && t.length <= 4) { tag = t; break; }
    }

    const isAd  = !!el.querySelector('[class*="_doticon_"]');
    const isTop = !!el.querySelector('[class*="_ranktop_"]');
    const rankEl = el.querySelector('[class*="_ranknum_"]');
    const rankNum = rankEl ? (parseInt(rankEl.textContent?.trim() || '0', 10) || 0) : 0;

    return { title, link, heat, tag, isAd, isTop, rankNum };
  }).filter(item => item.title.length > 0);
})()`;

interface SnapshotItem {
  title: string;
  link: string;
  heat: string;
  tag: string;
  isAd: boolean;
  isTop: boolean;
  rankNum: number;
}

export async function fetchHotSearch(options: FetchHotSearchOptions = {}): Promise<HotSearchItem[]> {
  const {
    profileDir = getDefaultProfileDir(),
    timeoutMs = 60_000,
  } = options;

  await mkdir(profileDir, { recursive: true });

  const chromePath = options.chromePath ?? findChromeExecutable();
  if (!chromePath) throw new Error('未找到 Chrome/Edge，请设置环境变量 WEIBO_BROWSER_CHROME_PATH。');

  // ── 启动或复用 Chrome/Edge ─────────────────────────────────────────────
  const launchChrome = async (): Promise<number> => {
    const port = await getFreePort();
    console.log(`[weibo-hot-search] 启动浏览器（配置目录：${profileDir}）`);
    const chromeArgs = [
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profileDir}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-blink-features=AutomationControlled',
      '--start-maximized',
      WEIBO_HOTSEARCH_URL,
    ];
    if (process.platform === 'darwin') {
      const appPath = chromePath.replace(/\/Contents\/MacOS\/[^/]+$/, '');
      spawn('open', ['-na', appPath, '--args', ...chromeArgs], { stdio: 'ignore' });
    } else {
      spawn(chromePath, chromeArgs, { stdio: 'ignore' });
    }
    return port;
  };

  let port: number;
  const existingPort = findExistingChromeDebugPort(profileDir);

  if (existingPort) {
    console.log(`[weibo-hot-search] 检测到已有浏览器实例（端口 ${existingPort}），验证健康状态...`);
    try {
      const wsUrl = await waitForChromeDebugPort(existingPort, 5_000);
      const testCdp = await CdpConnection.connect(wsUrl, 5_000, { defaultTimeoutMs: 5_000 });
      await testCdp.send('Target.getTargets');
      testCdp.close();
      console.log('[weibo-hot-search] 复用已有浏览器实例。');
      port = existingPort;
    } catch {
      console.log('[weibo-hot-search] 已有实例无响应，重新启动...');
      killChromeByProfile(profileDir);
      await sleep(2000);
      port = await launchChrome();
    }
  } else {
    port = await launchChrome();
  }

  let cdp: CdpConnection | null = null;

  try {
    // ── 建立 CDP 连接 ────────────────────────────────────────────────────
    console.log('[weibo-hot-search] 等待调试端口就绪...');
    const wsUrl = await waitForChromeDebugPort(port, 30_000);
    cdp = await CdpConnection.connect(wsUrl, 30_000, { defaultTimeoutMs: 15_000 });

    // ── 定位或创建热搜标签页 ─────────────────────────────────────────────
    const targets = await cdp.send<{
      targetInfos: Array<{ targetId: string; url: string; type: string }>;
    }>('Target.getTargets');

    let pageTarget = targets.targetInfos.find(
      (t) => t.type === 'page' && t.url.includes('weibo.com'),
    );

    if (!pageTarget) {
      const { targetId } = await cdp.send<{ targetId: string }>(
        'Target.createTarget', { url: WEIBO_HOTSEARCH_URL },
      );
      pageTarget = { targetId, url: WEIBO_HOTSEARCH_URL, type: 'page' };
    }

    const { sessionId } = await cdp.send<{ sessionId: string }>(
      'Target.attachToTarget', { targetId: pageTarget.targetId, flatten: true },
    );
    await cdp.send('Target.activateTarget', { targetId: pageTarget.targetId });
    await cdp.send('Page.enable', {}, { sessionId });
    await cdp.send('Runtime.enable', {}, { sessionId });

    // ── 确保在热搜页面 ──────────────────────────────────────────────────
    const urlResult = await cdp.send<{ result: { value: string } }>(
      'Runtime.evaluate',
      { expression: 'window.location.href', returnByValue: true },
      { sessionId },
    );

    if (!urlResult.result.value.includes('weibo.com/newlogin')) {
      console.log('[weibo-hot-search] 导航到热搜页面...');
      await cdp.send('Page.navigate', { url: WEIBO_HOTSEARCH_URL }, { sessionId });
      await sleep(4000);
    } else {
      console.log('[weibo-hot-search] 已在热搜页，刷新数据...');
      await cdp.send('Page.reload', {}, { sessionId });
      await sleep(4000);
    }

    // ── 等待热搜列表加载 ────────────────────────────────────────────────
    console.log('[weibo-hot-search] 等待热搜列表加载...');
    const waitStart = Date.now();
    let listReady = false;

    while (Date.now() - waitStart < timeoutMs) {
      const check = await cdp.send<{ result: { value: boolean } }>(
        'Runtime.evaluate',
        {
          expression: `(
            document.querySelectorAll('[class*="_titout_"]').length > 5 ||
            document.querySelectorAll('a[href*="s.weibo.com/weibo"]').length > 5
          )`,
          returnByValue: true,
        },
        { sessionId },
      );
      if (check.result.value) { listReady = true; break; }
      await sleep(1000);
    }

    if (!listReady) {
      console.warn('[weibo-hot-search] 未检测到热搜列表，请在浏览器中登录微博。');
      console.warn('[weibo-hot-search] 等待 30 秒，请手动完成登录...');
      await sleep(30_000);
    }

    // ── 滚动采集（虚拟滚动：每次 DOM 中约保留 30 条）────────────────────
    // 页面使用虚拟滚动，必须在每一步滚动后采集快照，
    // 才能覆盖全部约 50 条热搜（每次只有约 30 条在 DOM 中）。
    console.log('[weibo-hot-search] 开始滚动采集...');

    const collected = new Map<string, SnapshotItem>();

    const snapshot = async () => {
      const r = await cdp!.send<{ result: { value: SnapshotItem[] } }>(
        'Runtime.evaluate',
        { expression: SNAPSHOT_SCRIPT, returnByValue: true },
        { sessionId },
      );
      for (const item of r.result.value ?? []) {
        if (!collected.has(item.title)) collected.set(item.title, item);
      }
    };

    // 先采集顶部初始内容
    await snapshot();

    // 缓慢向下滚动：每步 200px，间隔 600ms，等待虚拟 DOM 渲染
    for (let i = 0; i < 30; i++) {
      await cdp.send('Runtime.evaluate', { expression: `window.scrollBy(0, 200)` }, { sessionId });
      await sleep(600);
      await snapshot();
    }

    // 停在底部稍等，确保末尾条目完全渲染
    await sleep(1000);
    await snapshot();

    // 回到顶部，补采下滑时可能被回收的顶部条目
    await cdp.send('Runtime.evaluate', { expression: `window.scrollTo(0, 0)` }, { sessionId });
    await sleep(1000);
    await snapshot();

    console.log(`[weibo-hot-search] 采集完成，共发现 ${collected.size} 条（含广告）。`);

    // ── 过滤广告，按原始排名排序 ─────────────────────────────────────────
    const organic = Array.from(collected.values()).filter(item => !item.isAd);

    organic.sort((a, b) => {
      // 置顶排最前
      if (a.isTop && !b.isTop) return -1;
      if (!a.isTop && b.isTop) return 1;
      // 按原始排名升序；无排名数字的排最后
      if (a.rankNum === 0 && b.rankNum === 0) return 0;
      if (a.rankNum === 0) return 1;
      if (b.rankNum === 0) return -1;
      return a.rankNum - b.rankNum;
    });

    const items: HotSearchItem[] = organic.map((item, i) => ({
      rank: i + 1,
      title: item.title,
      link: item.link || undefined,
      heat: item.heat,
      tag: item.tag,
      isTop: item.isTop,
    }));

    if (items.length === 0) {
      throw new Error('未采集到任何热搜数据，请检查页面结构是否已变化。');
    }

    console.log(`[weibo-hot-search] 过滤广告后共 ${items.length} 条热搜。`);
    return items;

  } finally {
    cdp?.close();
  }
}

export async function saveHotSearchToMarkdown(
  items: HotSearchItem[],
  outputPath: string,
): Promise<void> {
  const today = new Date().toISOString().slice(0, 10);
  const lines: string[] = [
    `# 微博热搜 ${today}`,
    '',
    `> 采集时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}  `,
    `> 共 ${items.length} 条`,
    '',
    '| 排名 | 热搜词 | 热度 | 标签 |',
    '|------|--------|------|------|',
  ];

  for (const item of items) {
    const heat = item.heat ? item.heat.replace(/\s+/g, '') : '-';
    const tag = item.isTop ? '置顶' : (item.tag ? item.tag.replace(/\s+/g, '') : '-');
    const titleCell = item.link ? `[${item.title}](${item.link})` : item.title;
    lines.push(`| ${item.rank} | ${titleCell} | ${heat} | ${tag} |`);
  }

  lines.push('');

  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, lines.join('\n'), 'utf-8');
}

// ── CLI 入口 ───────────────────────────────────────────────────────────────

function printUsage(): never {
  console.log(`抓取微博热搜并保存为 Markdown 文件

用法：
  npx -y bun weibo-hot-search.ts [选项]

选项：
  --output <路径>   输出文件路径（默认：当前目录下 ./<日期>-weibo-hot-search.md）
  --profile <目录>  Chrome/Edge 配置文件目录
  --help            显示此帮助

示例：
  npx -y bun weibo-hot-search.ts
  npx -y bun weibo-hot-search.ts --output ./data/hotsearch.md
`);
  process.exit(0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  let outputPath: string | undefined;
  let profileDir: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg === '--output' && args[i + 1]) {
      outputPath = path.resolve(args[++i]!);
    } else if (arg === '--profile' && args[i + 1]) {
      profileDir = args[++i];
    }
  }

  const today = new Date().toISOString().slice(0, 10);
  const resolvedOutput = outputPath ?? path.join(process.cwd(), `${today}-weibo-hot-search.md`);

  const items = await fetchHotSearch({ profileDir });
  await saveHotSearchToMarkdown(items, resolvedOutput);

  console.log(`[weibo-hot-search] 已保存到：${resolvedOutput}`);
}

await main().catch((err) => {
  console.error(`错误：${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
