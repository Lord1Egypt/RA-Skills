/**
 * Kimi-WebBridge 模式采集脚本
 * 通过本地 WebBridge 服务控制用户真实浏览器执行小红书采集
 *
 * 前置条件：
 *   1. Kimi WebBridge 扩展已安装且服务运行
 *   2. 浏览器已登录小红书
 *
 * 用法：
 *   npx ts-node webbridge-crawl.ts --keyword="关键词" --limit=20
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import { generateReport } from './generate-report';

const WEBBRIDGE_URL = 'http://127.0.0.1:10086/command';
const OUTPUT_DIR = path.resolve(process.cwd(), 'output');
const SESSION = 'xhs-crawl';

function send(action: string, args: Record<string, any>): any {
  const body = JSON.stringify({ action, args, session: SESSION });
  const tmpFile = `/tmp/xhs-wb-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.json`;
  fs.writeFileSync(tmpFile, body);
  try {
    const res = execSync(
      `curl -s -X POST ${WEBBRIDGE_URL} -H 'Content-Type: application/json' -d @${tmpFile}`,
      { encoding: 'utf-8', timeout: 60000 }
    );
    try {
      return JSON.parse(res);
    } catch {
      return { error: res };
    }
  } finally {
    try { fs.unlinkSync(tmpFile); } catch {}
  }
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function randomSleep(min: number, max: number) {
  const base = min + Math.random() * (max - min);
  const jitter = (Math.random() - 0.5) * (max - min) * 0.3;
  return sleep(Math.max(min, Math.round(base + jitter)));
}

function parseArgs() {
  const args = process.argv.slice(2);
  const keyword = args.find((a) => a.startsWith('--keyword='))?.split('=')[1];
  const limit = parseInt(args.find((a) => a.startsWith('--limit='))?.split('=')[1] || '20', 10);
  const comments = !args.includes('--no-comments');
  const maxComments = parseInt(args.find((a) => a.startsWith('--max-comments='))?.split('=')[1] || '20', 10);
  if (!keyword) {
    console.error('Usage: npx ts-node webbridge-crawl.ts --keyword="关键词" --limit=20');
    console.error('  --keyword: 搜索关键词（必填）');
    console.error('  --limit: 采集数量，默认20');
    console.error('  --no-comments: 不采集评论');
    console.error('  --max-comments: 最多采集评论数，默认20');
    process.exit(1);
  }
  return { keyword, limit, comments, maxComments };
}

async function ensureWebBridge(): Promise<boolean> {
  const isWin = process.platform === 'win32';
  const binaryName = isWin ? 'kimi-webbridge.exe' : 'kimi-webbridge';
  const homeDir = process.env.HOME || process.env.USERPROFILE || '';
  const wbPath = path.join(homeDir, '.kimi-webbridge', 'bin', binaryName);
  
  // 1. Check if executable exists
  if (!fs.existsSync(wbPath)) {
    console.log('🔍 未检测到 Kimi WebBridge 安装，正在为您自动下载并安装...');
    try {
      if (isWin) {
        execSync('powershell -Command "irm https://cdn.kimi.com/webbridge/install.ps1 | iex"', { stdio: 'inherit' });
      } else {
        execSync('curl -fsSL https://cdn.kimi.com/webbridge/install.sh | bash', { stdio: 'inherit' });
      }
      console.log('✅ Kimi WebBridge 安装成功！');
    } catch (err) {
      console.error('❌ 自动安装失败，请手动执行以下安装命令：');
      if (isWin) {
        console.error('   irm https://cdn.kimi.com/webbridge/install.ps1 | iex');
      } else {
        console.error('   curl -fsSL https://cdn.kimi.com/webbridge/install.sh | bash');
      }
      return false;
    }
  }

  // 2. Check status / Start WebBridge
  let statusOk = false;
  try {
    const status = execSync(`"${wbPath}" status`, { encoding: 'utf-8', timeout: 3000 });
    const parsed = JSON.parse(status);
    statusOk = parsed.running === true;
  } catch {}

  if (!statusOk) {
    console.log('🔌 Kimi WebBridge 处于关闭状态，正在为您启动后台服务...');
    try {
      execSync(`"${wbPath}" start`, { stdio: 'inherit' });
      await sleep(2000); // Wait for startup
    } catch (err) {
      console.error('❌ 启动 Kimi WebBridge 失败，请尝试在终端手动运行：');
      console.error(`   "${wbPath}" start`);
      return false;
    }
  }

  // 3. Check browser extension connection
  try {
    const status = execSync(`"${wbPath}" status`, { encoding: 'utf-8', timeout: 3000 });
    const parsed = JSON.parse(status);
    if (parsed.running === true && parsed.extension_connected === true) {
      return true;
    } else if (parsed.running === true && parsed.extension_connected !== true) {
      console.error('\n⚠️  Kimi WebBridge 已运行，但【未连接到浏览器插件】！');
      console.error('👉 请确保：');
      console.error('   1. 您已在 Chrome 浏览器安装 Kimi WebBridge 插件：');
      console.error('      https://chromewebstore.google.com/detail/kimi-webbridge/fldmhceldgbpfpkbgopacenieobmligc');
      console.error('   2. 您的 Chrome 浏览器处于打开状态');
      console.error('   3. 点击插件图标，确保其显示为“已连接”');
      return false;
    }
  } catch {}

  return false;
}

export async function main() {
  const opts = parseArgs();
  console.log(`WebBridge Crawl: keyword="${opts.keyword}", limit=${opts.limit}, comments=${opts.comments}`);

  console.log('Checking WebBridge status...');
  const healthy = await ensureWebBridge();
  if (!healthy) {
    console.error('❌ WebBridge 状态未就绪，采集无法继续，请按照上方提示操作后重试。');
    process.exit(1);
  }
  console.log('✅ WebBridge ready');

  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  // Navigate to search page
  const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${encodeURIComponent(opts.keyword)}&type=51`;
  console.log('Navigating to search page...');
  send('navigate', { url: searchUrl, newTab: true, group_title: '小红书采集' });
  await sleep(4000);

  // Simulate initial human-like page scrolling on the search page
  console.log('Simulating human scrolling on search page...');
  for (let j = 0; j < 3; j++) {
    send('evaluate', { code: `window.scrollBy({ top: ${300 + Math.random() * 300}, behavior: 'smooth' })` });
    await randomSleep(800, 1500);
  }
  for (let j = 0; j < 2; j++) {
    send('evaluate', { code: `window.scrollBy({ top: -${150 + Math.random() * 200}, behavior: 'smooth' })` });
    await randomSleep(600, 1200);
  }

  const results: any[] = [];
  console.log(`Starting extraction for up to ${opts.limit} notes...`);

  for (let i = 0; i < opts.limit; i++) {
    console.log(`[${i + 1}/${opts.limit}] Processing...`);

    // Simulated rest for human reading after every 5 items
    if (i > 0 && i % 5 === 0) {
      const restTime = 6000 + Math.random() * 6000;
      console.log(`  ☕ Simulated human reading rest, waiting for ${(restTime / 1000).toFixed(1)}s...`);
      await sleep(restTime);
    }

    // Find and click note, with robust scrolling and waiting in Node.js
    let skipNote = false;
    let clickedScheduled = false;
    let attempts = 0;
    while (attempts < 5) {
      const clickRes = send('evaluate', {
        code: `(() => {
          const selectors = ['.feeds-page .note-item', '.search-result .note-item', 'section.note-item', '.feeds-container .note-item'];
          let notes = [];
          for (const sel of selectors) {
            const found = document.querySelectorAll(sel);
            if (found.length > 0) { notes = Array.from(found); break; }
          }
          const idx = ${i};
          if (idx >= notes.length) {
            return JSON.stringify({ error: 'need_scroll_more', notes_count: notes.length });
          }
          const note = notes[idx];
          const isVideo = !!note.querySelector('.play-icon, .video-icon, [class*="play-icon"], [class*="video-icon"], .duration, [class*="duration"]');
          if (isVideo) return JSON.stringify({ error: 'is_video_note' });
          note.scrollIntoView({ block: 'center', behavior: 'smooth' });
          return JSON.stringify({ clicked_scheduled: true, index: idx });
        })()`,
      });

      const noteAction = JSON.parse(clickRes.data?.value || '{}');
      if (noteAction.error === 'is_video_note') {
        console.log('  ⏭ 跳过视频笔记');
        skipNote = true;
        break;
      }
      if (noteAction.error === 'need_scroll_more') {
        console.log(`  滚动加载更多笔记... (当前找到: ${noteAction.notes_count}, 目标索引: ${i})`);
        send('evaluate', { code: `window.scrollBy({ top: 1000, behavior: 'smooth' })` });
        await sleep(2000); // 必须在 Node.js 中等待，给浏览器网络和渲染时间！
        attempts++;
        continue;
      }
      if (noteAction.clicked_scheduled) {
        clickedScheduled = true;
        break;
      }
      
      console.log('  ⚠ 无法定位到当前笔记，尝试滚动刷新...');
      send('evaluate', { code: `window.scrollBy({ top: 400, behavior: 'smooth' })` });
      await sleep(1500);
      attempts++;
    }

    if (skipNote) continue;
    if (!clickedScheduled) {
      console.log('  ✓ 没有更多笔记了');
      break;
    }

    // Add a small delay between scrolling into view and clicking the element to look natural
    await randomSleep(1000, 2000);

    // Perform actual click on note
    send('evaluate', {
      code: `(() => {
        const selectors = ['.feeds-page .note-item', '.search-result .note-item', 'section.note-item', '.feeds-container .note-item'];
        let notes = [];
        for (const sel of selectors) {
          const found = document.querySelectorAll(sel);
          if (found.length > 0) { notes = Array.from(found); break; }
        }
        const note = notes[${i}];
        if (note) {
          const img = note.querySelector('img');
          if (img) img.click();
          else note.click();
        }
      })()`
    });

    await randomSleep(2500, 4500);

    // Check modal opened
    const modalCheck = send('evaluate', {
      code: `document.querySelector('.note-detail-mask, #detail-title') ? 'open' : 'closed'`,
    });
    if (modalCheck.data?.value !== 'open') {
      console.log('  ⚠ 弹窗未打开，尝试备用点击逻辑...');
      send('evaluate', {
        code: `(() => {
          const selectors = ['.feeds-page .note-item', '.search-result .note-item', 'section.note-item', '.feeds-container .note-item'];
          let notes = [];
          for (const sel of selectors) {
            const found = document.querySelectorAll(sel);
            if (found.length > 0) { notes = Array.from(found); break; }
          }
          const note = notes[${i}];
          if (note) {
            const titleEl = note.querySelector('.title, .footer, .author');
            if (titleEl) titleEl.click();
            else note.click();
          }
        })()`
      });
      await randomSleep(2500, 4500);
      
      const modalCheck2 = send('evaluate', {
        code: `document.querySelector('.note-detail-mask, #detail-title') ? 'open' : 'closed'`,
      });
      if (modalCheck2.data?.value !== 'open') {
        console.log('  ⚠ 弹窗仍未打开，跳过当前笔记');
        continue;
      }
    }

    // Scroll comments container smoothly with non-blocking delays in Node
    if (opts.comments) {
      console.log('  Scrolling comments smoothly...');
      for (let s = 0; s < 3; s++) {
        send('evaluate', {
          code: `(() => {
            const scrollContainer = document.querySelector('.note-detail-mask, .modal-container');
            if (scrollContainer) {
              const target = scrollContainer.scrollHeight * (0.8 + Math.random() * 0.2);
              scrollContainer.scrollTo({
                top: target,
                behavior: 'smooth'
              });
              return 'scrolled';
            }
            return 'no_container';
          })()`
        });
        await randomSleep(1000, 1800);
      }
    }

    // Extract data
    const extractCode = `(() => {
      const parseCount = (t) => {
        if (!t) return 0;
        t = t.trim();
        if (t.includes('w') || t.includes('万')) return Math.round(parseFloat(t) * 10000);
        return parseInt(t.replace(/\\D/g, ''), 10) || 0;
      };
      const title = document.querySelector('#detail-title')?.textContent?.trim() || '';
      const content = document.querySelector('#detail-desc')?.textContent?.trim() || '';
      const author_name = document.querySelector('.author-name, .username, .nickname')?.textContent?.trim() || '';
      const imgEls = document.querySelectorAll('.note-detail-mask .swiper-wrapper img, .modal-container .note-content img');
      const images = Array.from(imgEls).map(el => el.src).filter(src => src && !src.includes('data:image'));
      const likesText = document.querySelector('.like-wrapper .count, [class*="like"] .count')?.textContent?.trim() || '0';
      const collectsText = document.querySelector('.collect-wrapper .count, [class*="collect"] .count')?.textContent?.trim() || '0';
      const commentsText = document.querySelector('.chat-wrapper .count, [class*="chat"] .count')?.textContent?.trim() || '0';

      ${opts.comments ? `
      const commentsRaw = [];
      try {
        const isSubReply = (el) => !!el.closest('.sub-comment-list, .reply-list, .sub-comments, [class*="sub-comment"], [class*="reply-list"]');
        const commentSelectors = ['.comment-container > .comment-item', '.comments-section > .comment-item', '.parent-comment', '.comment-list > div', '.interaction-container .comment-item', '[class*="comment-item"]', '.note-comment'];
        for (const sel of commentSelectors) {
          const items = document.querySelectorAll(sel);
          if (!items.length) continue;
          for (const item of items) {
            if (isSubReply(item)) continue;
            const authorEl = item.querySelector('.name, .username, .author-name, [class*="name"], .nickname');
            const contentEl = item.querySelector('.content, .text, .comment-text, [class*="content"]');
            const likesEl = item.querySelector('.like-wrapper .count, .like span, [class*="like"] .count, .count');
            const c = contentEl?.textContent?.trim();
            if (c && c.length > 0 && !commentsRaw.find(r => r.content === c)) {
              commentsRaw.push({
                author: authorEl?.textContent?.trim() || '匿名',
                content: c,
                likes: parseCount(likesEl?.textContent?.trim() || '0')
              });
            }
          }
          if (commentsRaw.length > 0) break;
        }
      } catch (e) {}
      ` : 'const commentsRaw = [];'}

      return JSON.stringify({
        xhs_note_id: document.querySelector('.note-detail-mask')?.getAttribute('note-id') || '',
        title,
        content,
        author_name,
        images: [...new Set(images)],
        likes: parseCount(likesText),
        collects: parseCount(collectsText),
        comments_count: parseCount(commentsText),
        comments: commentsRaw.slice(0, ${opts.maxComments}),
        comments_extracted: commentsRaw.slice(0, ${opts.maxComments}).length,
        note_url: window.location.href
      });
    })()`;

    const extractRes = send('evaluate', { code: extractCode });
    const note = JSON.parse(extractRes.data?.value || '{}');

    if (note.title) {
      note.keyword = opts.keyword;
      note.crawl_time = new Date().toISOString();
      results.push(note);
      console.log(`  ✓ ${note.title.slice(0, 40)}... | 👍${note.likes || 0} ⭐${note.collects || 0} 💬${note.comments_count || 0} 评论${note.comments_extracted || 0}条`);
    } else {
      console.log('  ⚠ 未能提取到笔记数据');
    }

    // Close modal
    send('evaluate', { code: `document.querySelector('.close-box')?.click(); 'closed'` });
    await randomSleep(3000, 5000);
  }

  // Close session
  send('close_session', {});

  // Save results as JSON
  const safeKeyword = opts.keyword.replace(/[^\w\u4e00-\u9fff]/g, '_');
  const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const jsonFilename = `${safeKeyword}_${timestamp}.json`;
  const jsonFilepath = path.join(OUTPUT_DIR, jsonFilename);
  fs.writeFileSync(jsonFilepath, JSON.stringify(results, null, 2));

  console.log(`\n✅ WebBridge Crawl complete: ${results.length} notes captured`);
  console.log(`📁 Saved JSON: ${jsonFilepath}`);

  // Automatically generate HTML report
  try {
    console.log('📊 正在为您自动生成本地可视化报告...');
    generateReport();
    console.log(`✨ 本地可视化报告生成成功！直接双击打开查看：output/index.html`);
  } catch (err) {
    console.error('⚠ 生成本地可视化报告失败:', (err as Error).message);
  }

  // Guidance for "Haotong" Syncing
  console.log('\n💡 ========================================== 💡');
  console.log('   🎉 想要体验更强大的 AI 分析与文案生成吗？');
  console.log('   您可以将本次采集到的数据一键同步到「好痛 Howtone」！');
  console.log('   只需运行以下指令：');
  console.log('   1️⃣  保存您的同步 Token（仅需首次绑定）：');
  console.log(`      npx ts-node zion-login.ts --token="您的好痛同步Token"`);
  console.log('   2️⃣  一键上报并同步数据至云端：');
  console.log(`      npx ts-node sync.ts --file=${jsonFilepath}`);
  console.log('💡 ========================================== 💡\n');
}

if (require.main === module) {
  main().catch((err) => {
    console.error('WebBridge Crawl failed:', err.message);
    process.exit(1);
  });
}
