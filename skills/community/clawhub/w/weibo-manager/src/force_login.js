const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
require('dotenv').config();

const COOKIE_FILE = path.join(__dirname, '../cookies.json');
const LOGIN_URL = 'https://weibo.com/login.php';
const TARGET_CHAT_ID = process.argv[2]; 

(async () => {
    // Force delete existing cookies for a clean slate
    if (fs.existsSync(COOKIE_FILE)) {
        fs.unlinkSync(COOKIE_FILE);
    }

    console.log('[Weibo] Launching browser...');
    const browser = await puppeteer.launch({
        headless: "new",
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--window-size=1280,800']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    try {
        console.log('[Weibo] Navigating to login page...');
        await page.goto(LOGIN_URL, { waitUntil: 'networkidle2' });

        // Wait for QR code container
        const qrSelector = '.qrcode-img img'; 
        try {
            await page.waitForSelector(qrSelector, { timeout: 15000 });
        } catch (e) {
            console.log('[Weibo] QR Code selector not found, taking full page screenshot.');
        }
        
        // Screenshot
        const screenshotPath = path.join(__dirname, '../qrcode.png');
        try {
            const element = await page.$(qrSelector);
            if (element) {
                // Add some padding or context if needed, but element screenshot is usually fine
                await element.screenshot({ path: screenshotPath });
            } else {
                await page.screenshot({ path: screenshotPath });
            }
        } catch (e) {
            await page.screenshot({ path: screenshotPath });
        }
        
        console.log(`[Weibo] QR Code saved to ${screenshotPath}`);

        // Upload to Feishu
        const uploadCmd = `node skills/feishu-sender/upload_image.js "${screenshotPath}"`;
        const rawOutput = execSync(uploadCmd).toString();
        const imageKey = rawOutput.split('\n')
            .map(line => line.trim())
            .filter(line => line.startsWith('img_'))
            .pop();

        if (!imageKey) {
            console.error(`[Weibo] Upload output: ${rawOutput}`);
            throw new Error(`Failed to upload QR code.`);
        }

        // Send QR Code to user
        const msg = JSON.stringify({
            zh_cn: {
                title: "请扫码登录微博 📱",
                content: [
                    [{ tag: "text", text: "这是刚刚生成的登录二维码，请使用微博APP扫码（有效期约1分钟）：" }],
                    [{ tag: "img", image_key: imageKey }],
                    [{ tag: "text", text: "扫码确认登录后，请稍等片刻，我会自动检测并保存状态。" }]
                ]
            }
        });
        execSync(`node skills/feishu-sender/send_post.js "${TARGET_CHAT_ID}" '${msg}'`);

        // Poll for login success
        console.log('[Weibo] Waiting for login...');
        const maxRetries = 60; // 2 minutes
        let loggedIn = false;

        for (let i = 0; i < maxRetries; i++) {
            // Check URL change or specific cookie presence
            const cookies = await page.cookies();
            const subCookie = cookies.find(c => c.name === 'SUB'); 
            
            if (subCookie) {
                console.log('[Weibo] Login detected! Saving cookies...');
                fs.writeFileSync(COOKIE_FILE, JSON.stringify(cookies, null, 2));
                loggedIn = true;
                break;
            }
            await new Promise(r => setTimeout(r, 2000));
        }

        if (loggedIn) {
            const successMsg = JSON.stringify({
                zh_cn: {
                    title: "登录成功！🎉",
                    content: [[{ tag: "text", text: "Cookie 已保存。现在可以使用微博技能了！" }]]
                }
            });
            execSync(`node skills/feishu-sender/send_post.js "${TARGET_CHAT_ID}" '${successMsg}'`);
        } else {
            const failMsg = JSON.stringify({
                zh_cn: {
                    title: "登录超时 ❌",
                    content: [[{ tag: "text", text: "等待扫码超时，请重新触发指令。" }]]
                }
            });
            execSync(`node skills/feishu-sender/send_post.js "${TARGET_CHAT_ID}" '${failMsg}'`);
        }

    } catch (error) {
        console.error('[Weibo] Error:', error);
        const errorMsg = JSON.stringify({
             zh_cn: {
                 title: "登录流程出错 ⚠️",
                 content: [[{ tag: "text", text: `错误信息: ${error.message}` }]]
             }
         });
         execSync(`node skills/feishu-sender/send_post.js "${TARGET_CHAT_ID}" '${errorMsg}'`);
    } finally {
        await browser.close();
    }
})();
