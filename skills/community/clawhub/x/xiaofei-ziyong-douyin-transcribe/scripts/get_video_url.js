#!/usr/bin/env node
/**
 * get_video_url.js
 * 通过 puppeteer-core 拦截 hellotik 视频直链
 */

const { launch } = require('/tmp/puppeteer_test/node_modules/puppeteer-core');

const douyinUrl = process.argv[2] || process.env.DOUYIN_URL;

async function main() {
    let videoUrl = null;
    let coverUrl = null;
    let browser;

    try {
        console.error('Launching Chrome (puppeteer-core)...');
        
        browser = await launch({
            headless: true,
            executablePath: '/usr/bin/google-chrome',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            ],
            protocolTimeout: 30000
        });

        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });
        
        // 启用请求拦截
        await page.setRequestInterception(true);
        
        let reqCount = 0;
        page.on('request', req => {
            reqCount++;
            const url = req.url();
            // 记录所有非图片/CSS/JS请求
            if (!url.includes('.css') && !url.includes('.js') && !url.includes('.png') && !url.includes('.jpg') && !url.includes('.woff')) {
                if (url.includes('365yg') || url.includes('mp4') || url.includes('video')) {
                    console.error('REQ[' + reqCount + ']: ' + url.substring(0, 200));
                }
            }
            // 捕获视频CDN请求
            // 注意：视频URL可能在query string里含.mp4，路径里含 /video/tos/
            if (!videoUrl) {
                const isVideo = (url.includes('.mp4')) || 
                    (url.includes('/video/') && (url.includes('365yg') || url.includes('v.smtcdns') || url.includes('amemv')));
                
                if (isVideo) {
                    // 完整记录前3个视频相关请求
                    if (videoUrl === null) {
                        videoUrl = url;  // 保存第一个
                        console.error('CANDIDATE_VIDEO: ' + url);
                    }
                }
            }
            req.continue();
        });

        // 控制台消息拦截
        page.on('console', msg => {
            const text = msg.text();
            if (!videoUrl && text.includes('.mp4') && text.includes('365yg')) {
                const match = text.match(/https?:\/\/[^\s"']+\.mp4[^\s"'<>]*/);
                if (match) {
                    videoUrl = match[0];
                    console.error('FOUND_VIDEO_CONSOLE: ' + match[0].substring(0, 120));
                }
            }
        });

        page.on('pageerror', err => {
            console.error('PageError: ' + err.message.substring(0, 200));
        });

        console.error('Navigating to hellotik...');
        await page.goto('https://www.hellotik.app/zh', { 
            timeout: 15000, 
            waitUntil: 'domcontentloaded' 
        });
        
        await new Promise(r => setTimeout(r, 2000));

        // 找到输入框并填入URL
        console.error('Filling URL input...');
        try {
            // 尝试多个选择器
            const selectors = [
                'input[placeholder*="粘贴"]',
                'input[placeholder*="链接"]', 
                'input[type="text"]'
            ];
            
            let filled = false;
            for (const sel of selectors) {
                try {
                    const el = await page.$(sel);
                    if (el) {
                        await el.click();
                        await page.keyboard.type(douyinUrl, { delay: 50 });
                        filled = true;
                        console.error('Filled with selector: ' + sel);
                        break;
                    }
                } catch(e) {}
            }
            
            if (!filled) {
                // 尝试直接在active element输入
                await page.keyboard.type(douyinUrl, { delay: 50 });
            }
            
            await new Promise(r => setTimeout(r, 1000));
        } catch(e) {
            console.error('Fill error: ' + e.message);
        }

        // 点击解析按钮
        console.error('Clicking parse button...');
        try {
            const allBtns = await page.$$('button');
            for (const btn of allBtns) {
                const txt = await btn.evaluate(el => el.textContent);
                if (txt && txt.trim().includes('解析')) {
                    await btn.click();
                    console.error('Clicked button: ' + txt.trim());
                    break;
                }
            }
        } catch(e) {
            console.error('Button error: ' + e.message);
        }

        // 等待视频URL出现
        console.error('Waiting for video URL...');
        let waited = 0;
        while (!videoUrl && waited < 20000) {
            await new Promise(r => setTimeout(r, 1000));
            waited += 1000;
            console.error('  ...' + waited + 'ms');
        }

        // 如果还没找到，尝试点击某个下载按钮
        if (!videoUrl) {
            console.error('Trying download buttons...');
            try {
                const dlBtns = await page.$$('button');
                for (const btn of dlBtns) {
                    const txt = await btn.evaluate(el => el.textContent);
                    if (txt && (txt.includes('540p') || txt.includes('720p') || txt.includes('1080p') || txt.includes('超高清'))) {
                        await btn.click();
                        console.error('Clicked: ' + txt.trim());
                        await new Promise(r => setTimeout(r, 3000));
                        break;
                    }
                }
            } catch(e) {
                console.error('DL btn error: ' + e.message);
            }
        }

        // DOM提取备选
        if (!videoUrl) {
            console.error('DOM extraction attempt...');
            try {
                const domUrl = await page.evaluate(() => {
                    // 搜索script标签
                    const scripts = Array.from(document.querySelectorAll('script'));
                    for (const s of scripts) {
                        const txt = s.textContent || '';
                        const m = txt.match(/https?:\/\/[^\s"'<>]+\.mp4[^\s"'<>]*/);
                        if (m) return m[0];
                    }
                    // data属性
                    const dataEls = Array.from(document.querySelectorAll('*'));
                    for (const el of dataEls) {
                        for (const attr of ['data-url', 'data-src', 'data-video']) {
                            const v = el.getAttribute(attr);
                            if (v && v.includes('.mp4') && v.includes('365yg')) return v;
                        }
                    }
                    return null;
                });
                if (domUrl) {
                    videoUrl = domUrl;
                    console.error('DOM found: ' + domUrl.substring(0, 100));
                }
            } catch(e) {
                console.error('DOM error: ' + e.message);
            }
        }

        // 提取封面
        if (!coverUrl) {
            try {
                coverUrl = await page.evaluate(() => {
                    const imgs = Array.from(document.querySelectorAll('img'));
                    for (const img of imgs) {
                        let src = img.src || img.getAttribute('data-src') || '';
                        if ((src.includes('douyinpic') || src.includes('p9-sign')) && !src.includes('avatar')) {
                            return src.replace(/q\d{2}/, 'q90');
                        }
                    }
                    return null;
                });
                if (coverUrl) console.error('Cover: ' + coverUrl.substring(0, 80));
            } catch(e) {}
        }

        await browser.close();

    } catch(err) {
        console.error('Fatal: ' + err.message);
        if (browser) await browser.close().catch(() => {});
    }

    // 输出结果
    const result = { videoUrl, coverUrl };
    console.log('RESULT_JSON:' + JSON.stringify(result));
    
    if (!videoUrl) {
        process.exit(1);
    }
}

main().catch(err => {
    console.error('Fatal error: ' + err.message);
    process.exit(1);
});
