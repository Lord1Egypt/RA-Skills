/**
 * 小红书草稿自动化发布脚本 v4.4
 *
 * 跨平台支持: Windows / macOS / Linux
 * - 所有路径改为动态计算，不再写死 Windows 路径
 * - 保存草稿后主动询问是否发布
 * - 未登录时自动点出二维码登录
 * - 富文本正文使用剪贴板粘贴写入
 *
 * 使用方法:
 *   node upload_auto.js --title "标题" --content "正文" --images "img1.jpg,img2.jpg"
 *   node upload_auto.js -t "标题" -f 正文.txt -i "img1.jpg,img2.jpg"
 */

const path = require('path');
const fs = require('fs');
const os = require('os');

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
    // 4. 全局 npm
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
// 跨平台动态配置
// ============================================================
function getSkillDir() {
  const scriptPath = path.dirname(path.resolve(__filename));
  return path.dirname(scriptPath);
}

function getDefaultTempDir() {
  return path.join(os.tmpdir(), 'openclaw', 'uploads');
}

function getDefaultImageOutputDir() {
  return path.join(getSkillDir(), 'generated_images');
}

function getConfigPath() {
  return path.join(path.dirname(path.resolve(__filename)), 'config.json');
}

function loadConfig() {
  const configPath = getConfigPath();
  if (fs.existsSync(configPath)) {
    try { return JSON.parse(fs.readFileSync(configPath, 'utf-8')); } catch (e) {}
  }
  return {};
}

const CONFIG = {
  uploadTempDir: (() => {
    const cfg = loadConfig();
    const c = cfg.paths?.upload_temp_dir;
    if (c) {
      const expanded = c.startsWith('~') ? path.join(os.homedir(), c.slice(1)) : c;
      return path.resolve(expanded);
    }
    return getDefaultTempDir();
  })(),
  imageOutputDir: (() => {
    const cfg = loadConfig();
    const c = cfg.paths?.image_output_dir;
    if (c) {
      const expanded = c.startsWith('~') ? path.join(os.homedir(), c.slice(1)) : c;
      return path.resolve(expanded);
    }
    return getDefaultImageOutputDir();
  })(),
  creatorUrl: 'https://creator.xiaohongshu.com/publish/publish?from=menu&target=image',
  cdpPort: (() => {
    const cfg = loadConfig();
    return cfg.upload?.cdp_port || 18800;
  })(),
};

// 日志工具
const log = (level, msg) => {
  const time = new Date().toLocaleTimeString('zh-CN', { hour12: false });
  console.log('[' + time + '] [' + level + '] ' + msg);
};
const info = (msg) => log('INFO', msg);
const ok = (msg) => log('OK', msg);
const error = (msg) => log('ERROR', msg);
const warn = (msg) => log('WARN', msg);

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// 复制图片到临时目录（跨平台）
function copyImagesToTemp(imagePaths) {
  ensureDir(CONFIG.uploadTempDir);
  const copiedPaths = [];

  for (const imgPath of imagePaths) {
    let fullPath = imgPath.trim();
    if (!path.isAbsolute(fullPath)) {
      fullPath = path.join(CONFIG.imageOutputDir, imgPath);
    }
    if (fs.existsSync(fullPath)) {
      const fileName = path.basename(fullPath);
      const destPath = path.join(CONFIG.uploadTempDir, fileName);
      fs.copyFileSync(fullPath, destPath);
      copiedPaths.push(destPath);
      ok('已准备: ' + fileName);
    } else {
      warn('文件不存在: ' + fullPath);
    }
  }

  return copiedPaths;
}

// ============================================================
// 登录状态检测
// ============================================================
async function checkLoginStatus(page) {
  const bodyText = await page.evaluate(() => document.body.innerText);
  const hasAvatar = await page.$('.avatar, [class*="avatar"], img[class*="user"]');

  return {
    isLoggedIn: (bodyText.includes('小红薯') || bodyText.includes('创作中心')) && !!hasAvatar,
    hasText: bodyText.includes('小红薯') || bodyText.includes('创作中心'),
    hasAvatar: !!hasAvatar,
  };
}

// ============================================================
// 二维码登录处理（提示后直接退出，不等待扫码）
// ============================================================
async function handleQRLogin(page) {
  info('━━━ 检测到未登录 ━━━');

  // 尝试点击登录入口唤出二维码（截图留存）
  const clicked = await page.evaluate(() => {
    const selectors = [
      'button:has-text("登录")',
      'button:has-text("扫码")',
      'a:has-text("登录")',
      '[class*="login"]',
      '[class*="qr"]',
      'img[class*="code"]',
      '.login-btn',
      '.scan-btn',
    ];
    for (const sel of selectors) {
      try {
        const el = document.querySelector(sel);
        if (el && el.offsetParent !== null) {
          el.click();
          return sel;
        }
      } catch (e) {}
    }
    return null;
  });

  await page.waitForTimeout(2000);

  // 截图留存
  try {
    ensureDir(CONFIG.uploadTempDir);
    await page.screenshot({ path: path.join(CONFIG.uploadTempDir, '_qrcode.png') });
  } catch (e) {}

  // 直接提示用户，不等待
  console.log('');
  console.log('╔══════════════════════════════════════════════════╗');
  console.log('║              ⚠️  请先登录小红书                ║');
  console.log('╠══════════════════════════════════════════════════╣');
  console.log('║  📱 当前未检测到登录状态，请先完成登录        ║');
  console.log('║                                                  ║');
  console.log('║  操作步骤：                                     ║');
  console.log('║  1. 在浏览器中点击「登录/扫码」按钮           ║');
  console.log('║  2. 用小红书 App 扫描二维码登录               ║');
  console.log('║  3. 登录成功后，重新运行本脚本                 ║');
  console.log('║                                                  ║');
  console.log('║  💡 提示：登录一次后浏览器会记住登录状态     ║');
  console.log('║     后续使用无需重复登录！                    ║');
  console.log('╚══════════════════════════════════════════════════╝');
  console.log('');

  return false;
}

// ============================================================
// 主工作流
// ============================================================
async function uploadAndPublish(options) {
  const { title, content, images } = options;

  info('='.repeat(50));
  info('  小红书草稿发布工具 v4.4');
  info('  临时目录: ' + CONFIG.uploadTempDir);
  info('  图片目录: ' + CONFIG.imageOutputDir);
  info('='.repeat(50));

  info('准备上传图片...');
  const tempImagePaths = copyImagesToTemp(images);

  if (tempImagePaths.length === 0) {
    error('没有可用的图片，请检查图片路径是否正确');
    return { success: false, error: 'No images' };
  }

  ok(tempImagePaths.length + ' 张图片已准备\n');

  let browser = null;

  try {
    info('连接浏览器 (CDP: ' + CONFIG.cdpPort + ')...');
    const cdpUrl = 'http://127.0.0.1:' + CONFIG.cdpPort;
    browser = await chromium.connectOverCDP(cdpUrl);

    const context = browser.contexts()[0];
    const pages = await context.pages();

    let page = null;
    for (const p of pages) {
      if (p.url().includes('creator.xiaohongshu.com')) {
        page = p;
        break;
      }
    }

    if (!page) {
      page = await context.newPage();
      await page.goto(CONFIG.creatorUrl, { timeout: 30000 });
    }

    ok('已连接到浏览器\n');

    info('打开创作平台...');
    await page.goto(CONFIG.creatorUrl, { timeout: 60000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);

    const loginStatus = await checkLoginStatus(page);

    if (!loginStatus.isLoggedIn) {
      const loginSuccess = await handleQRLogin(page);
      if (!loginSuccess) {
        return { success: false, error: 'Login timeout' };
      }
    } else {
      ok('已确认登录状态');
    }

    // 点击"上传图文"
    info('点击上传图文按钮...');
    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('*'));
      const found = items.filter(el =>
        el.textContent.trim() === '上传图文' &&
        el.children.length === 0 &&
        el.tagName !== 'IMG'
      );
      if (found.length >= 2) {
        found[1].click();
        return 'clicked 2nd';
      } else if (found.length === 1) {
        found[0].click();
        return 'clicked 1st';
      }
      return 'not found';
    });
    await page.waitForTimeout(2000);
    ok('已点击上传图文\n');

    // 点击"上传图片"按钮
    info('触发图片上传...');
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find(b => b.textContent.includes('上传图片'));
      if (btn) btn.click();
    });
    await page.waitForTimeout(1500);
    ok('已触发上传\n');

    // 上传图片
    info('上传 ' + tempImagePaths.length + ' 张图片...');
    const fileInput = await page.$('input[type="file"]');

    if (fileInput) {
      await fileInput.setInputFiles(tempImagePaths);
      ok('文件已选择');
      ok('等待图片处理（10秒）...\n');
      await page.waitForTimeout(10000);
    } else {
      error('未找到文件输入框，请确认上传弹窗是否正常打开');
      return { success: false, error: 'No file input' };
    }

    // 填写标题
    info('填写标题...');
    const titleInput = await page.$('input[placeholder*="填写标题"]');

    if (titleInput) {
      await titleInput.fill(title);
      ok('标题: "' + title.substring(0, 15) + (title.length > 15 ? '...' : '') + '"\n');
    } else {
      warn('未找到标题输入框');
    }

    // 填写正文（富文本编辑器，使用剪贴板粘贴）
    info('填写正文...');
    const editorEl = await page.$('.tiptap.ProseMirror');

    if (editorEl) {
      // 清空编辑器
      await page.evaluate(() => {
        const editor = document.querySelector('.tiptap.ProseMirror');
        if (editor) {
          editor.innerHTML = '';
          editor.dispatchEvent(new Event('input', { bubbles: true }));
        }
      });

      // 将内容通过剪贴板粘贴
      await page.evaluate((text) => {
        const textarea = document.createElement('textarea');
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }, content);

      await editorEl.click();
      await page.waitForTimeout(300);
      await page.keyboard.press('Control+v');
      await page.waitForTimeout(500);

      // 验证内容
      const writtenContent = await page.evaluate(() => {
        const editor = document.querySelector('.tiptap.ProseMirror');
        return editor ? editor.innerText : '';
      });

      ok('正文: ' + writtenContent.length + ' 字（原始 ' + content.length + ' 字）');

      // 如果粘贴后内容为空，降级为 DOM 直接写入
      if (writtenContent.length === 0 || writtenContent.length < content.length * 0.5) {
        warn('剪贴板粘贴失败，改用 DOM 直接写入...');
        await page.evaluate((text) => {
          const editor = document.querySelector('.tiptap.ProseMirror');
          if (editor) {
            const paragraphs = text.split(/\n\n+/);
            const html = paragraphs.map(p => {
              const lines = p.split(/\n/);
              return '<p>' + lines.join('<br>') + '</p>';
            }).join('');
            editor.innerHTML = html;
            editor.dispatchEvent(new Event('input', { bubbles: true }));
            editor.dispatchEvent(new Event('change', { bubbles: true }));
          }
        }, content);
        const verify2 = await page.evaluate(() => {
          const editor = document.querySelector('.tiptap.ProseMirror');
          return editor ? editor.innerText : '';
        });
        ok('正文（DOM写入）: ' + verify2.length + ' 字');
      }
    } else {
      warn('未找到正文编辑器');
    }

    // 保存草稿
    info('保存草稿...');
    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('*'));
      const saveBtn = items.find(el => el.textContent.trim() === '暂存离开');
      if (saveBtn) saveBtn.click();
    });
    await page.waitForTimeout(2000);
    ok('草稿已保存!\n');

    // 发布确认
    info('='.repeat(50));
    info('  ✅ 草稿保存成功！');
    info('='.repeat(50));
    ok('标题: ' + title);
    ok('正文: ' + content.length + ' 字');
    ok('图片: ' + tempImagePaths.length + ' 张');
    info('='.repeat(50));
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('  🎯 草稿已存入小红书草稿箱');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log('📌 是否需要我现在帮你发布？');
    console.log('   回复"发布"或"是"即发布到小红书');
    console.log('   回复"否"或"不用"则保留草稿，稍后手动发布');
    console.log('');
    console.log('[AWAIT_CONFIRM] 等待用户确认发布...');

    return {
      success: true,
      draft: true,
      awaitingPublish: true,
      imagesUploaded: tempImagePaths.length,
      titleLength: title.length,
      contentLength: content.length,
      tempImagePaths: tempImagePaths,
    };

  } catch (err) {
    error('执行失败: ' + err.message);
    return { success: false, error: err.message };
  } finally {
    if (browser) {
      try { await browser.disconnect(); } catch (e) {}
    }
  }
}

// 显示帮助
function showHelp() {
  console.log(`
小红书草稿发布工具 v4.4 (跨平台版)
====================================

用法:
  node upload_auto.js --title "标题" --content "正文" --images "img1.jpg,img2.jpg"
  node upload_auto.js -t "标题" -f 正文.txt -i "img1.jpg,img2.jpg"

参数:
  -t, --title           笔记标题（必填）
  -c, --content          笔记正文（短文本）
  -f, --content-file     从文件读取正文（长文本推荐，解决编码问题）
  -i, --images           图片文件，多个用逗号分隔（必填）
  -h, --help            显示帮助

功能:
  - 跨平台: Windows / macOS / Linux
  - 未登录时自动点出二维码登录
  - 草稿保存后询问是否发布
  - 富文本编辑器使用剪贴板粘贴，支持长文本和特殊字符（#等）

前置条件:
  - OpenClaw 浏览器必须正在运行
`);
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const result = { title: '', content: '', images: [] };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--title' || arg === '-t') {
      result.title = args[++i] || '';
    } else if (arg === '--content' || arg === '-c') {
      result.content = args[++i] || '';
    } else if (arg === '--content-file' || arg === '-f') {
      const filePath = args[++i] || '';
      try {
        result.content = fs.readFileSync(filePath, 'utf8').trim();
        ok('从文件读取正文: ' + filePath + ' (' + result.content.length + ' 字)');
      } catch (e) {
        error('读取正文文件失败: ' + e.message);
        process.exit(1);
      }
    } else if (arg === '--images' || arg === '-i') {
      const imgStr = args[++i] || '';
      result.images = imgStr ? imgStr.split(',').map(s => s.trim()) : [];
    } else if (arg === '--help' || arg === '-h') {
      result.help = true;
    }
  }

  return result;
}

// 主入口
async function main() {
  const args = parseArgs();

  if (args.help) {
    showHelp();
    process.exit(0);
  }

  if (!args.title || !args.content || args.images.length === 0) {
    console.error('[ERROR] 缺少必要参数!');
    console.error('  --title         标题');
    console.error('  --content 或 --content-file  正文（长文本建议用 -f 读取文件）');
    console.error('  --images        图片');
    console.error('\n使用 --help 查看帮助');
    process.exit(1);
  }

  const result = await uploadAndPublish({
    title: args.title,
    content: args.content,
    images: args.images,
  });

  if (result.awaitingPublish) {
    process.exit(42);
  }

  process.exit(result.success ? 0 : 1);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
