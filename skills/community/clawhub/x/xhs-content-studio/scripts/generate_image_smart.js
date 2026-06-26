/**
 * 智能生图脚本 v2.0
 *
 * 核心改进：
 * - 豆包生图全自动化，无需用户引导操作
 * - 自动打开豆包 → 自动发送prompt → 等待生成 → 自动提取URL → 自动下载图片
 *
 * 使用方法:
 *   node generate_image_smart.js --prompt "描述" --aspect_ratio "3:4" --n 3
 */

const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const os = require('os');

// ============================================================
// playwright-core 加载（兼容 OpenClaw 全局安装，支持 Windows/macOS/Linux）
function getOpenClawPlaywright() {
  const home = os.homedir();
  const openclawGlobal = process.env.OPENCLAW_GLOBAL ||
    (process.platform === 'win32'
      ? 'D:\\openclaw-global'
      : path.join(home, '.openclaw-global'));

  const candidates = [
    // 1. OpenClaw 全局安装（主程序）
    path.join(openclawGlobal, 'node_modules', 'openclaw', 'node_modules', 'playwright-core'),
    // 2. OpenClaw 钉钉插件
    path.join(openclawGlobal, 'node_modules', 'openclaw-dingtalk', 'node_modules', 'playwright-core'),
    // 3. macOS/Linux 用户目录下的 openclaw（常见路径）
    path.join(home, '.openclaw-global', 'node_modules', 'openclaw', 'node_modules', 'playwright-core'),
    path.join(home, '.openclaw', 'node_modules', 'playwright-core'),
    // 4. 全局 npm（nvm 路径）
    path.join(home, '.nvm', 'versions', 'node', process.version.split('.')[0].replace('v',''), 'lib', 'node_modules', 'playwright-core'),
  ];

  for (const cand of candidates) {
    try { return require(cand); } catch (e) {}
  }
  return null;
}

let playwright;
try {
  playwright = require('playwright-core');
} catch (e) {
  playwright = getOpenClawPlaywright();
}

if (!playwright) {
  console.error('[ERROR] 找不到 playwright-core');
  console.error('  请确保 OpenClaw 已正确安装，或运行: npm install playwright-core');
  process.exit(1);
}
const { chromium } = playwright;

// ============================================================
// 路径配置
// ============================================================
function getSkillDir() {
  return path.dirname(path.dirname(path.resolve(__filename)));
}
function getConfigPath() {
  return path.join(path.dirname(path.resolve(__filename)), 'config.json');
}
function loadConfig() {
  const p = getConfigPath();
  if (fs.existsSync(p)) {
    try { return JSON.parse(fs.readFileSync(p, 'utf-8')); } catch (e) {}
  }
  return {};
}
function getImageOutputDir() {
  const cfg = loadConfig();
  const c = cfg.paths?.image_output_dir;
  if (c) {
    const expanded = c.startsWith('~') ? path.join(os.homedir(), c.slice(1)) : c;
    return path.resolve(expanded);
  }
  return path.join(getSkillDir(), 'generated_images');
}
function getTempDir() {
  const cfg = loadConfig();
  const c = cfg.paths?.upload_temp_dir;
  if (c) {
    const expanded = c.startsWith('~') ? path.join(os.homedir(), c.slice(1)) : c;
    return path.resolve(expanded);
  }
  return path.join(os.tmpdir(), 'openclaw', 'uploads');
}
function ensureDir(d) { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }); }

// ============================================================
// 日志
// ============================================================
const log = (level, msg) => {
  const time = new Date().toLocaleTimeString('zh-CN', { hour12: false });
  console.log('[' + time + '] [' + level + '] ' + msg);
};
const info = (msg) => log('INFO', msg);
const ok = (msg) => log('OK', msg);
const warn = (msg) => log('WARN', msg);
const error = (msg) => log('ERROR', msg);

// ============================================================
// 解析命令行参数
// ============================================================
function parseArgs() {
  const args = process.argv.slice(2);
  const result = { prompt: '', aspectRatio: '3:4', n: 3, images: [] };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--prompt' || a === '-p') result.prompt = args[++i] || '';
    else if (a === '--aspect_ratio' || a === '-r') result.aspectRatio = args[++i] || '3:4';
    else if (a === '--n') result.n = parseInt(args[++i]) || 3;
    else if (a === '--images' || a === '-i') {
      const s = args[++i] || '';
      result.images = s ? s.split(',').map(x => x.trim()) : [];
    } else if (a === '--help' || a === '-h') result.help = true;
  }
  return result;
}

// ============================================================
// 方案1: MiniMax API 生图（纯 Node.js 实现）
// ============================================================
async function generateWithMinimax(prompt, aspectRatio, n, outputDir) {
  info('━━━ 方案1: MiniMax API 生图 ━━━');

  const cfg = loadConfig();
  const apiKey = cfg.minimax?.api_key;
  const apiBase = cfg.minimax?.api_base || 'https://api.minimaxi.com';

  if (!apiKey || apiKey === '' || apiKey === '你的MiniMax API Key') {
    warn('MiniMax API Key 未配置，跳过');
    return { success: false, reason: 'no_api_key' };
  }

  const url = apiBase.replace(/\/$/, '') + '/v1/image_generation';

  const payload = {
    model: 'image-01',
    prompt: prompt,
    aspect_ratio: aspectRatio,
    n: n,
    response_format: 'base64',
  };

  info('正在调用 MiniMax API...');
  info('Prompt: ' + prompt);

  try {
    const bodyStr = JSON.stringify(payload);
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey,
        'Content-Length': Buffer.byteLength(bodyStr),
      },
      timeout: 120000,
    };

    const result = await new Promise((resolve, reject) => {
      const req = require('https').request(options, (res) => {
        let data = '';
        res.on('data', chunk => { data += chunk; });
        res.on('end', () => resolve({ status: res.statusCode, body: data }));
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
      req.write(bodyStr);
      req.end();
    });

    if (result.status !== 200) {
      warn('API 返回状态码: ' + result.status + ' - ' + result.body.substring(0, 200));
      return { success: false, reason: 'api_error_' + result.status, output: result.body };
    }

    let parsed;
    try {
      parsed = JSON.parse(result.body);
    } catch (e) {
      warn('API 返回非 JSON: ' + result.body.substring(0, 200));
      return { success: false, reason: 'json_parse_error' };
    }

    // API 返回格式: { data: { image_base64: ["base64...", "..."] } }
    const rawData = parsed.data?.image_base64 || [];
    if (!rawData.length) {
      warn('API 未返回图片数据: ' + result.body.substring(0, 200));
      return { success: false, reason: 'no_images', output: result.body };
    }

    ok('API 调用成功，准备处理 ' + rawData.length + ' 张图片（base64）');

    ensureDir(outputDir);
    const timestamp = Math.floor(Date.now() / 1000);
    const savedFiles = [];

    for (let i = 0; i < rawData.length; i++) {
      const b64 = rawData[i];
      const filename = 'img_' + timestamp + '_' + (i + 1) + '.jpeg';
      const filepath = path.join(outputDir, filename);

      info('解码并保存第 ' + (i + 1) + '/' + rawData.length + ' 张...');
      try {
        const imgBuffer = Buffer.from(b64, 'base64');
        fs.writeFileSync(filepath, imgBuffer);
        const sizeKB = Math.round(imgBuffer.length / 1024);
        if (imgBuffer.length > 1000) {
          savedFiles.push(filepath);
          ok('已保存: ' + filename + ' (' + sizeKB + 'KB)');
        }
      } catch (e) {
        warn('保存第 ' + (i + 1) + ' 张失败: ' + e.message);
      }
    }

    if (savedFiles.length === 0) {
      return { success: false, reason: 'all_downloads_failed' };
    }

    ok('MiniMax 生图成功！' + savedFiles.length + ' 张图片已保存');
    return { success: true, files: savedFiles, source: 'minimax' };

  } catch (e) {
    error('MiniMax API 调用失败: ' + e.message);
    return { success: false, reason: 'exception', error: e.message };
  }
}

// ============================================================
// 方案2: 豆包全自动化生图（无需用户引导）
// ============================================================
async function generateWithDoubao(prompt, n, aspectRatio, outputDir) {
  info('━━━ 方案2: 豆包全自动化生图 ━━━');

  const cfg = loadConfig();
  const cdpPort = cfg.upload?.cdp_port || 18800;
  const doubaoUrl = 'https://www.doubao.com';

  const ratioNote = aspectRatio === '3:4' ? '，3:4竖版比例' :
                    aspectRatio === '16:9' ? '，16:9横版比例' :
                    aspectRatio === '1:1' ? '，1:1正方形比例' : '';
  const doubaoPrompt = '帮我生成' + n + '张' + prompt + '的照片' + ratioNote + '，适合发小红书';

  let browser = null;

  try {
    info('连接 OpenClaw 浏览器 (CDP: ' + cdpPort + ')...');
    browser = await chromium.connectOverCDP('http://127.0.0.1:' + cdpPort);
    const context = browser.contexts()[0];
    const pages = await context.pages();

    let page = null;
    for (const p of pages) {
      if (p.url().includes('doubao.com')) {
        page = p;
        break;
      }
    }

    if (!page) {
      page = await context.newPage();
    }
    await page.bringToFront();

    info('打开豆包...');
    await page.goto(doubaoUrl, { timeout: 30000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);
    ok('豆包页面已打开');

    // 找输入框
    let inputArea = null;
    const inputSelectors = [
      'div[contenteditable="true"]',
      'textarea[placeholder*="输入"]',
      'textarea[placeholder*="问题"]',
      'textarea[placeholder*="搜索"]',
      'textarea',
      'div[contenteditable]',
      '.input-area textarea',
      '.chat-input textarea',
      '[class*="input"] textarea',
      '[class*="send"] textarea',
    ];

    for (const sel of inputSelectors) {
      try {
        const el = await page.$(sel);
        if (el && await el.isVisible()) {
          const tag = await el.evaluate(n => n.tagName.toLowerCase());
          const editable = await el.evaluate(n => n.isContentEditable);
          if (tag === 'textarea' || editable) {
            inputArea = el;
            ok('找到输入框: ' + sel);
            break;
          }
        }
      } catch (e) {}
    }

    if (!inputArea) {
      error('无法找到豆包的输入框，请确认豆包页面已加载');
      ensureDir(getTempDir());
      await page.screenshot({ path: path.join(getTempDir(), '_doubao_debug.png') });
      warn('截图已保存到 _doubao_debug.png');
      return { success: false, reason: 'no_input_found' };
    }

    // 输入并发送
    info('自动发送生图请求...');
    await inputArea.click();
    await page.waitForTimeout(500);
    await page.keyboard.press('Control+A');
    await page.waitForTimeout(200);
    await page.keyboard.type(doubaoPrompt, { delay: 50 });
    await page.waitForTimeout(300);
    await page.keyboard.press('Enter');
    ok('已发送: ' + doubaoPrompt);

    // 等待图片出现（轮询）
    let imgUrls = [];
    const maxWait = 90;
    const pollInterval = 3000;
    let waited = 0;

    await page.waitForTimeout(5000);

    // 获取发送前页面已有图片（用于过滤旧图，只下载新生成的）
    const existingImgs = new Set(
      await page.evaluate(() => {
        return Array.from(document.querySelectorAll('img'))
          .filter(img => img.naturalWidth > 200 && img.naturalHeight > 200)
          .filter(img => !img.src.includes('data:') && !img.src.includes('base64'))
          .filter(img => img.src.startsWith('http'))
          .map(img => img.src);
      })
    );
    info('发送前已有图片: ' + existingImgs.size + ' 张');

    while (waited < maxWait) {
      const currentImgs = await page.evaluate(() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs
          .filter(img => img.naturalWidth > 200 && img.naturalHeight > 200)
          .filter(img => !img.src.includes('data:') && !img.src.includes('base64'))
          .filter(img => img.src.startsWith('http'))
          .map(img => img.src);
      });

      // 过滤掉发送前已有的旧图，只保留新生成的
      const newUrls = [...new Set(currentImgs)].filter(url => !existingImgs.has(url));
      const totalNew = newUrls.length;

      if (totalNew > imgUrls.length) {
        info('检测到 ' + totalNew + ' 张新图片（+' + (totalNew - imgUrls.length) + '），等待更多生成...');
        imgUrls = newUrls;
      }

      if (imgUrls.length >= n) {
        ok('检测到 ' + imgUrls.length + ' 张新图片，生成完成');
        break;
      }

      await page.waitForTimeout(pollInterval);
      waited += pollInterval / 1000;
    }

    if (imgUrls.length === 0) {
      warn('未检测到图片，尝试其他提取方式...');
      const msgImgs = await page.evaluate(() => {
        const allElements = Array.from(document.querySelectorAll('*'));
        const urls = [];
        allElements.forEach(el => {
          const style = window.getComputedStyle(el);
          const bg = style.backgroundImage;
          if (bg && bg.startsWith('url(') && bg.match(/http/)) {
            const url = bg.match(/url\("?([^"]+)"?\)/)?.[1];
            if (url) urls.push(url);
          }
          if (el.tagName === 'IMG') {
            const src = el.src;
            if (src && src.startsWith('http') && !src.includes('data:')) urls.push(src);
          }
        });
        return [...new Set(urls)].filter(url => !existingImgs.has(url));
      });

      if (msgImgs.length > 0) {
        imgUrls = msgImgs;
        ok('从页面提取到 ' + imgUrls.length + ' 张新图片');
      }
    }

    if (imgUrls.length === 0) {
      error('未能提取到任何图片');
      return { success: false, reason: 'no_images_extracted' };
    }

    // 保存豆苞生成结果截图（供用户预览确认）
    const timestamp = Math.floor(Date.now() / 1000);
    const previewPath = path.join(getTempDir(), '_doubao_preview_' + timestamp + '.png');
    try {
      // 截取整个页面可见区域
      await page.screenshot({ path: previewPath, fullPage: false });
      ok('预览截图已保存: ' + previewPath);
    } catch (e) {
      warn('预览截图失败: ' + e.message);
    }

    const finalUrls = imgUrls.slice(0, n);
    ok('准备下载 ' + finalUrls.length + ' 张图片');

    // 下载图片
    ensureDir(outputDir);
    const savedFiles = [];

    for (let i = 0; i < finalUrls.length; i++) {
      const url = finalUrls[i];
      const ext = url.includes('.png') ? 'png' : 'jpeg';
      const filename = 'img_' + timestamp + '_' + (i + 1) + '.' + ext;
      const filepath = path.join(outputDir, filename);

      info('下载第 ' + (i + 1) + '/' + finalUrls.length + ' 张...');
      try {
        const http = url.startsWith('https') ? require('https') : require('http');
        const file = fs.createWriteStream(filepath);
        await new Promise((resolve, reject) => {
          http.get(url, (res) => {
            if (res.statusCode === 301 || res.statusCode === 302) {
              http.get(res.headers.location, (res2) => {
                res2.pipe(file);
                file.on('finish', () => { file.close(); resolve(); });
              }).on('error', reject);
            } else {
              res.pipe(file);
              file.on('finish', () => { file.close(); resolve(); });
            }
          }).on('error', reject);
        });
        const stats = fs.statSync(filepath);
        if (stats.size > 1000) {
          savedFiles.push(filepath);
          ok('已保存: ' + filename + ' (' + Math.round(stats.size / 1024) + 'KB)');
        } else {
          fs.unlinkSync(filepath);
        }
      } catch (e) {
        warn('下载失败: ' + e.message);
      }
    }

    if (savedFiles.length === 0) {
      error('所有图片下载失败');
      return { success: false, reason: 'all_downloads_failed' };
    }

    ok('━━━ 豆包生图完成 ━━━');
    console.log('[生成的文件]:');
    for (const f of savedFiles) console.log('  - ' + f);
    if (previewPath) console.log('[预览截图]: ' + previewPath);

    return {
      success: true,
      files: savedFiles,
      source: 'doubao',
      urls: finalUrls,
      previewPath: previewPath,
    };

  } catch (e) {
    error('豆包生图失败: ' + e.message);
    return { success: false, reason: 'exception', error: e.message };
  } finally {
    if (browser) {
      try { await browser.disconnect(); } catch (e) {}
    }
  }
}

// ============================================================
// 主入口
// ============================================================
async function main() {
  const args = parseArgs();

  if (args.help || !args.prompt) {
    console.log(`
智能生图工具 v2.0（全自动豆包版）
====================================
用法:
  node generate_image_smart.js --prompt "描述" --aspect_ratio "3:4" --n 3

参数:
  --prompt, -p        图片描述 (必填)
  --aspect_ratio, -r  图片比例 (默认 3:4，可选 3:4, 1:1, 16:9)
  --n                 生成数量 (默认 3)

策略:
  1. 优先 MiniMax API 生图（需配置 API Key）
  2. API 不可用或失败 → 自动切换豆包全自动化生图
     - 自动打开豆包
     - 自动发送生图请求
     - 自动等待生成
     - 自动提取并下载图片
     - 无需任何用户引导操作

示例:
  node generate_image_smart.js -p "可爱的橘猫" -n 4 -r 3:4
`);
    process.exit(0);
  }

  const outputDir = getImageOutputDir();
  ensureDir(outputDir);
  info('输出目录: ' + outputDir);

  // 方案1: MiniMax
  const minimaxResult = await generateWithMinimax(args.prompt, args.aspectRatio, args.n, outputDir);

  if (minimaxResult.success) {
    printSuccess(minimaxResult.files, 'MiniMax');
    process.exit(0);
  }

  // 降级到豆包
  warn('MiniMax 生图不可用（' + minimaxResult.reason + '），自动切换豆包全自动化生图...\n');
  const doubaoResult = await generateWithDoubao(args.prompt, args.n, args.aspectRatio, outputDir);

  if (doubaoResult.success) {
    printSuccess(doubaoResult.files, '豆包', doubaoResult.previewPath);
    process.exit(0);
  }

  error('所有生图方案均不可用');
  process.exit(1);
}

function printSuccess(files, source, previewPath) {
  ok('━━━ 生图完成（' + source + '）━━━');
  console.log('[生成的文件]:');
  for (const f of files) console.log('  - ' + f);
  if (previewPath) {
    console.log('');
    console.log('╔══════════════════════════════════════════════════╗');
    console.log('║  ⚠️  请查看预览截图确认图片是否符合要求        ║');
    console.log('║  截图路径: ' + previewPath.padEnd(34) + '║');
    console.log('║  如图片不符，请重新运行并换 prompt 描述        ║');
    console.log('╚══════════════════════════════════════════════════╝');
  }
  console.log('');
  console.log('[下一步] 使用以下命令发布：');
  const scriptPath = path.join(getSkillDir(), 'scripts', 'upload_auto.js');
  console.log('  node "' + scriptPath + '" --title "标题" --content-file "正文.txt" --images "' + path.basename(files[0]) + '"');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
