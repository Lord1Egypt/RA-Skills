/**
 * 详细检查案件状态
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

(async () => {
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    try {
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(20000);

        // 选择 No. 搜索类型
        await page.locator('span.val').filter({ hasText: /^Case Name$/ }).click();
        await page.waitForTimeout(2000);
        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(1000);

        // 搜索案件
        await page.locator('input[type="text"]').nth(2).fill('2604151000000599520');
        await page.waitForTimeout(500);
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);

        // 检查表格内容
        const tableContent = await page.evaluate(() => {
            const rows = document.querySelectorAll('tbody tr');
            if (rows.length === 0) return '表格为空';
            
            let result = `共 ${rows.length} 行\n`;
            for (const row of rows) {
                const cells = row.querySelectorAll('td');
                const rowText = Array.from(cells).map(c => c.textContent.trim()).join(' | ');
                result += rowText + '\n';
            }
            return result;
        });

        console.log('搜索结果:');
        console.log(tableContent);

    } catch (error) {
        console.error('错误:', error.message);
    } finally {
        await browser.close();
    }
})();