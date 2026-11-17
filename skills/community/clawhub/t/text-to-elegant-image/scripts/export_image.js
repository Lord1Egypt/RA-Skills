const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

/**
 * 参数解析
 * 用法: node export_image.js <html> <output.png> [width] [--author "作者信息" | --no-footer] [--fixed-height <px>] [--frame <px>] [--flat]
 *
 * --author "文字"       在图片底部注入自定义 footer（覆盖 HTML 中已有的 .footer 内容）
 * --no-footer           完全移除 footer 区域
 * --fixed-height <px>   固定版式高度（金句海报/封面卡 3:4，如 width=600 配 --fixed-height 800），跳过自适应测量和相框边距（这两种模式容器本身占满画布，自带内部留白）
 * --frame <px>          相框边距：画布在内容宽度基础上左右各加 <px>，并强制统一 body 上下 padding 为同值，实现四边相等的"相框感"。长图模式默认 32px；传 0 可关闭
 * --flat                关闭卡片背景：所有 19 种风格默认在 .container 上加一层卡片背景（background/border/圆角/阴影），传此参数移除，内容直接融入 body 背景（老版本的扁平效果）。
 *                        ⚠️ 玻璃拟态风（11_glass）的卡片背景是核心视觉效果本身，传 --flat 会让毛玻璃质感完全消失，不建议对该风格使用。
 * 不传任何 footer 参数：保留 HTML 原有内容（AI 生成时已按规范写入）
 */
const args = process.argv.slice(2);

const inputHtml  = args[0];
const outputImg  = args[1];
const designWidth = parseInt(args[2]) || 600;

let authorText  = null;   // null = 不注入，使用 HTML 原有内容
let noFooter    = false;
let fixedHeight = null;   // 固定版式高度（海报/封面卡 3:4），传入后跳过自适应测量
let frameArg    = null;   // 用户显式指定的相框边距（未指定则按模式给默认值）
let flatMode    = false;  // true = 关闭卡片背景，恢复扁平效果

for (let i = 3; i < args.length; i++) {
    if (args[i] === '--no-footer') {
        noFooter = true;
    } else if (args[i] === '--flat') {
        flatMode = true;
    } else if (args[i] === '--author' && args[i + 1]) {
        authorText = args[i + 1];
        i++;
    } else if (args[i] === '--fixed-height' && args[i + 1]) {
        fixedHeight = parseInt(args[i + 1]) || null;
        i++;
    } else if (args[i] === '--frame' && args[i + 1] !== undefined) {
        frameArg = parseInt(args[i + 1]);
        if (Number.isNaN(frameArg)) frameArg = null;
        i++;
    }
}

// 固定版式（海报/封面卡）容器本身占满画布、内部自带 padding，不叠加相框；长图模式默认相框 32px。
// 注意：固定版式下强制 frame=0，即使用户误传 --frame 也忽略（否则画布被左右撑宽但容器不注入相框，产生不对称空白）。
const frame = fixedHeight ? 0 : (frameArg !== null ? frameArg : 32);
const width = designWidth + frame * 2;   // 实际画布宽度 = 内容设计宽度 + 左右相框

if (!inputHtml || !outputImg) {
    console.error('Usage: node export_image.js <html> <output.png> [width] [--author "文字" | --no-footer] [--fixed-height <px>] [--frame <px>] [--flat]');
    process.exit(1);
}

function detectChromePath() {
    const candidates = [
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/snap/bin/chromium',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/mnt/c/Program Files/Google/Chrome/Application/chrome.exe',
    ];
    for (const p of candidates) {
        if (fs.existsSync(p)) return p;
    }
    try {
        const r = execSync('which google-chrome chromium chromium-browser 2>/dev/null | head -1', { encoding: 'utf8' }).trim();
        if (r) return r;
    } catch (_) {}
    return null;
}

// 仅渲染本地 HTML 文件：本 skill 的用途是「本地文本/Markdown → 图片」，
// 不作为通用网页抓取器。历史上曾支持传 http(s):// 直接渲染远程页面，
// 但该分支会把本工具扩成任意 URL 的无头浏览器（SSRF / 内网探测风险），
// 且正常使用流程从不传远程 URL，故已移除，只接受本地文件路径。
if (/^https?:\/\//i.test(inputHtml)) {
    console.error('[ERROR] 仅支持本地 HTML 文件路径，不接受远程 URL。请先用 write 工具把内容写到本地 .html 再传入。');
    process.exit(1);
}
const htmlUrl    = `file://${path.resolve(inputHtml)}`;
const outputPath = path.resolve(outputImg);

const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

(async () => {
    const chromePath = detectChromePath();
    if (!chromePath) {
        console.error('[ERROR] 未找到 Chrome/Chromium，请先运行 bash scripts/setup.sh');
        process.exit(1);
    }
    console.log(`[INFO] 浏览器: ${chromePath}`);

    try {
        const browser = await puppeteer.launch({
            executablePath: chromePath,
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
                   // 容器代理环境证书链不完整会拦掉字体 CDN 请求；本地静态截图场景忽略证书安全
                   '--ignore-certificate-errors'],
            defaultViewport: { width, height: 1000, deviceScaleFactor: 2 }
        });

        const page = await browser.newPage();
        await page.goto(htmlUrl, { waitUntil: 'networkidle0', timeout: 30000 });

        // ── 等待 webfont 加载完成（故宫/水墨/报纸等风格依赖 CDN 字体）────
        try {
            await Promise.race([
                page.evaluate(() => document.fonts.ready),
                new Promise(resolve => setTimeout(resolve, 8000))  // 最多等 8s，CDN 不可达时不阻塞
            ]);
            const fontCount = await page.evaluate(() => document.fonts.size);
            if (fontCount > 0) console.log(`[INFO] Webfont 就绪（${fontCount} 个字体声明）`);
        } catch (_) { /* 字体等待失败不阻塞截图 */ }

        // ── 相框边距注入：统一 body 上下 padding，配合画布加宽的左右留白，实现四边相等 ──
        // 原因：各风格 .container 用 max-width + margin:0 auto 居中，若画布宽度=容器宽度则左右边距为0；
        // 上下留白又完全取决于各风格自写的 body padding（参差不齐）。
        // 修法：画布宽度=内容宽度+frame*2（左右留白由 margin:auto 自动生成），并强制 body 上下 padding=frame（不叠加原有 padding，直接覆盖统一）。
        if (!fixedHeight && frame > 0) {
            await page.evaluate((f) => {
                document.body.style.setProperty('padding-top', f + 'px', 'important');
                document.body.style.setProperty('padding-bottom', f + 'px', 'important');
                document.body.style.setProperty('box-sizing', 'border-box', 'important');
            }, frame);
            console.log(`[INFO] 相框边距: ${frame}px（四边统一，画布宽度 ${width}px = 内容 ${designWidth}px + 边距 ${frame}px×2）`);
        }

        // ── 卡片背景开关：--flat 时移除 .container 的卡片视觉（默认打开，不传即保留风格 CSS 自带的卡片背景）──
        // 19 种风格的 .container 均自带 background/border/border-radius/box-shadow（卡片浮于 body 背景之上）。
        // --flat 用于恢复老版本的扁平通栏效果：内容直接融入 body 背景，无卡片边界。
        if (flatMode) {
            await page.evaluate(() => {
                const container = document.querySelector('.container');
                if (container) {
                    container.style.setProperty('background', 'transparent', 'important');
                    container.style.setProperty('border', 'none', 'important');
                    container.style.setProperty('border-radius', '0', 'important');
                    container.style.setProperty('box-shadow', 'none', 'important');
                }
            });
            console.log('[INFO] --flat 模式：已移除 .container 卡片背景');
        }

        // ── Footer 注入逻辑 ──────────────────────────────────
        if (noFooter) {
            // 移除所有 footer 元素
            await page.evaluate(() => {
                document.querySelectorAll('.footer, footer, [data-footer]').forEach(el => el.remove());
            });
            console.log('[INFO] Footer 已移除');
        } else if (authorText !== null) {
            // 替换 footer 文字；如果页面没有 .footer 则追加一个
            await page.evaluate((text) => {
                const existing = document.querySelector('.footer, footer, [data-footer]');
                if (existing) {
                    existing.textContent = text;
                } else {
                    const container = document.querySelector('.container') || document.body;
                    const div = document.createElement('div');
                    div.className = 'footer';
                    div.style.cssText = 'text-align:center;padding-top:16px;font-size:0.75em;opacity:0.5;';
                    div.textContent = text;
                    container.appendChild(div);
                }
            }, authorText);
            console.log(`[INFO] Footer 已设置为：${authorText}`);
        }
        // authorText === null：不做任何操作，保留 HTML 原有 footer

        // ── 精确测量内容高度，裁掉底部多余空白 ────────────────
        // 固定版式（海报/封面卡）：若传入 --fixed-height，直接用该高度，不做自适应测量
        let contentHeight;
        if (fixedHeight) {
            contentHeight = fixedHeight;
            console.log(`[INFO] 固定版式高度: ${contentHeight}px（视口宽度 ${width}px）`);
        } else {
            contentHeight = await page.evaluate((f) => {
                // 以 .container 的真实渲染底部为基准（不含装饰性绝对定位/blur 元素撑出的虚高）。
                // 底部留白 = frame，与顶部相框 padding-top（同为 frame）视觉对称。
                const container = document.querySelector('.container');
                if (!container) {
                    return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
                }
                const rect = container.getBoundingClientRect();
                const containerBottom = Math.ceil(rect.top + rect.height);
                // frame>0 时 body 上下 padding 已被相框逻辑统一覆盖为 frame，直接补 frame 即四边对称；
                // frame=0（用户显式关闭相框）时不额外留白。
                const bottomPad = f > 0 ? f : 0;
                return containerBottom + bottomPad;
            }, frame);
            console.log(`[INFO] 内容高度: ${contentHeight}px（视口宽度 ${width}px，已自适应裁剪）`);
        }

        // 设置视口高度为内容高度，避免 fullPage 截到多余空白
        await page.setViewport({ width, height: contentHeight, deviceScaleFactor: 2 });

        await page.screenshot({
            path: outputPath,
            clip: { x: 0, y: 0, width, height: contentHeight }
        });
        await browser.close();
        console.log(`[SUCCESS] 长图已导出至：${outputPath}`);
    } catch (error) {
        console.error('[ERROR] 截图导出失败:', error.message);
        console.error('[FALLBACK] 在浏览器中手动打开：', htmlUrl);
        process.exit(1);
    }
})();
