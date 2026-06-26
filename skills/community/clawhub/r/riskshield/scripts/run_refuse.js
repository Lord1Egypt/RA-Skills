/**
 * RiskShield 案件审批自动化 - 执行脚本
 * 案件号: 2604161000000599527
 * 操作: refuse
 * 拒绝码: CA_TRUE_HIT
 */

const { chromium } = require('playwright');

const CASE_NO = '2604161000000599527';
const ACTION = 'refuse';
const REFUSE_CODE = 'CA_TRUE_HIT';
const CREDIT_AMOUNT = '100';

const REDIRECT_URL = encodeURIComponent('https://riskshield.dcsuat.com/anytask-web/task/case/page/main.html');
const LOGIN_URL = `https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=${REDIRECT_URL}`;

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`=== RiskShield 案件审批自动化 ===`);
    log(`案件号: ${CASE_NO}`);
    log(`操作: 拒绝 (REFUSE)`);
    log(`拒绝码: ${REFUSE_CODE}`);
    log('========================================');

    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    const page = await context.newPage();

    try {
        // ========== 1. 登录 ==========
        log('[1/8] 正在登录...');
        await page.goto(LOGIN_URL, { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(5000);

        await page.locator('input[placeholder*="user name"]').fill('taskAccount');
        await page.locator('input[placeholder*="password"]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();

        // 等待跳转
        await page.waitForResponse(resp => resp.url().includes('auth/login'), { timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(10000);
        log('[1/8] ✅ 登录成功');

        // ========== 2. 选择搜索类型: No. ==========
        log('[2/8] 选择搜索类型: 案件编号 (No.)...');

        await page.locator('span.val').filter({ hasText: 'Case Name' }).first().click();
        await page.waitForTimeout(2000);

        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(500);
        log('[2/8] ✅ 已选择"案件编号"');

        // ========== 3. 输入案件号 ==========
        log(`[3/8] 输入案件号: ${CASE_NO}...`);

        await page.locator('input[type="text"]').nth(2).fill(CASE_NO);
        await page.waitForTimeout(500);
        log('[3/8] ✅ 案件号已输入');

        // ========== 4. 点击搜索 ==========
        log('[4/8] 点击搜索...');

        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);
        log('[4/8] ✅ 搜索完成');

        // ========== 5. 验证案件 ==========
        log('[5/8] 验证案件...');
        const searchResult = await page.evaluate((expectedCaseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(expectedCaseNo)) {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        const firstCell = cells[0].textContent;
                        if (firstCell.includes(expectedCaseNo)) {
                            return { found: true, rowText: row.textContent };
                        }
                    }
                }
            }
            return { found: false };
        }, CASE_NO);

        if (!searchResult.found) {
            log(`❌ 案件 ${CASE_NO} 未找到`);
            return;
        }

        if (searchResult.rowText.includes('Closed') || searchResult.rowText.includes('已结案')) {
            log('⚠️ 案件已结案，无法重复审批');
            log('当前状态:', searchResult.rowText);
            return;
        }
        log('[5/8] ✅ 案件验证通过');

        // ========== 6. 获取审批页面URL ==========
        log('[6/8] 获取审批页面链接...');
        const approvalUrl = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) {
                    const links = row.querySelectorAll('a');
                    for (const link of links) {
                        if (link.textContent.trim() === 'Approval') {
                            return link.href;
                        }
                    }
                }
            }
            return null;
        }, CASE_NO);

        if (!approvalUrl) {
            log('❌ 找不到审批入口');
            return;
        }
        log('[6/8] ✅ 获取到审批链接');

        // ========== 7. 打开审批详情页 ==========
        log('[7/8] 打开审批详情页...');
        const detailPage = await context.newPage();
        await detailPage.goto(approvalUrl, { waitUntil: 'domcontentloaded' });
        await detailPage.waitForTimeout(5000);
        log('[7/8] ✅ 审批详情页已打开');

        // ========== 8. 填写审批表单 ==========
        log('[8/8] 填写审批表单...');

        // 点击 "Decision Information" 选项卡
        log('  - 点击 Decision Information 选项卡...');
        await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"], .ant-tabs-tab, div');
            for (const tab of tabs) {
                if (tab.textContent.includes('Decision')) {
                    tab.click();
                    return;
                }
            }
        });
        await detailPage.waitForTimeout(2000);

        // 查找并点击 ManualApprovalResult 下拉框
        log('  - 选择 ManualApprovalResult -> Refuse...');
        const manualApprovalSelect = detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first();
        await manualApprovalSelect.click();
        await detailPage.waitForTimeout(1000);

        await detailPage.locator('.ant-select-item').filter({ hasText: 'Refuse' }).click();
        log('  - ✅ 已选择 Refuse');

        // 选择 Refuse Code
        log('  - 选择 Refuse Code...');
        const refuseCodeSelect = detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).nth(1);
        await refuseCodeSelect.click();
        await detailPage.waitForTimeout(1000);

        await detailPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE }).first().click();
        log(`  - ✅ 已选择拒绝码: ${REFUSE_CODE}`);

        // 点击 Submit
        log('  - 点击提交按钮...');
        await detailPage.locator('button').filter({ hasText: '提交' }).click();
        log('  - ✅ 已提交');
        await detailPage.waitForTimeout(5000);

        // ========== 9. 验证结果 ==========
        log('[9/9] 验证审批结果...');
        await detailPage.close();

        // 重新搜索案件
        await page.locator('span.val').filter({ hasText: 'Case Name' }).first().click();
        await page.waitForTimeout(1500);
        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(500);

        await page.locator('input[type="text"]').nth(2).fill(CASE_NO);
        await page.waitForTimeout(500);

        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);

        const finalStatus = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) {
                    return row.textContent;
                }
            }
            return null;
        }, CASE_NO);

        if (finalStatus) {
            if (finalStatus.includes('Closed') || finalStatus.includes('已结案')) {
                if (finalStatus.includes('Reject') || finalStatus.includes('拒绝')) {
                    log('');
                    log('========================================');
                    log('  🎉 审批拒绝成功！');
                    log(`  案件 ${CASE_NO} 已结案，审批结果: Reject`);
                    log(`  拒绝码: ${REFUSE_CODE}`);
                    log('========================================');
                } else {
                    log(`✅ 案件已结案，状态: ${finalStatus}`);
                }
            } else {
                log('⚠️ 案件状态未变化，请手动确认');
                log('状态:', finalStatus.substring(0, 200));
            }
        }

        log('\n========================================');
        log('  自动化任务完成');
        log('========================================');

    } catch (error) {
        log(`❌ 错误: ${error.message}`);
        console.error(error);
    } finally {
        await browser.close();
    }
})();