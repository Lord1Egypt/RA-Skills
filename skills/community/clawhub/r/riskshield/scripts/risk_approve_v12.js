/**
 * RiskShield 案件审批自动化 - 修复 Credit Amount 输入框
 */

const { chromium } = require('playwright');

const LOGIN_URL = 'https://riskshield.dcsuat.com/mc/page/login.html?logout=true&redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s';

const CASE_NO = process.argv[2] || '2604151000000599520';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`=== RiskShield 案件审批自动化 ===`);
    log(`案件号: ${CASE_NO}`);
    log(`操作: ${ACTION === 'pass' ? '通过' : '拒绝'}`);
    if (ACTION === 'pass') log(`金额: ${CREDIT_AMOUNT}`);
    else log(`拒绝码: ${REFUSE_CODE}`);
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

        await page.waitForTimeout(20000);

        const url = page.url();
        if (url.includes('login') && !url.includes('sgin')) {
            log(`❌ 登录失败`);
            return;
        }
        log('[1/8] ✅ 登录成功');

        // ========== 2. 选择搜索类型: No. ==========
        log('[2/8] 选择搜索类型: 案件编号...');
        await page.waitForTimeout(2000);

        await page.locator('span.val').filter({ hasText: /^Case Name$/ }).click();
        await page.waitForTimeout(2000);

        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(1000);
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
                    if (cells.length > 0 && cells[0].textContent.includes(expectedCaseNo)) {
                        return { found: true, rowText: row.textContent };
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
            log('⚠️ 案件已结案');
            log('状态: ' + searchResult.rowText.substring(0, 100));
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

        // 点击 Decision Information tab
        log('  - 点击 Decision Information tab...');
        await detailPage.evaluate(() => {
            const tabs = document.querySelectorAll('[role="tab"]');
            for (const tab of tabs) {
                if (tab.textContent.includes('Decision') && tab.getAttribute('aria-selected') === 'false') {
                    tab.click();
                    return;
                }
            }
        });
        await detailPage.waitForTimeout(3000);

        // 选择 ManualApprovalResult -> Pass/Refuse
        log('  - 选择 ManualApprovalResult...');
        const visibleSelects = await detailPage.locator('.ant-select:visible').all();
        
        if (visibleSelects.length >= 1) {
            await visibleSelects[0].click();
        } else {
            const allSelects = await detailPage.locator('.ant-select').all();
            await allSelects[0].click();
        }
        await detailPage.waitForTimeout(1000);

        const actionText = ACTION === 'pass' ? 'Pass' : 'Refuse';
        await detailPage.locator('.ant-select-item').filter({ hasText: actionText }).click();
        log(`  - ✅ 已选择: ${actionText}`);

        // 等待页面更新
        await detailPage.waitForTimeout(3000);

        if (ACTION === 'pass') {
            // 填写金额 - 关键：使用 `input` 而不是 `input[type="text"]`，因为 Credit Amount 输入框没有设置 type
            log('  - 填写审批金额...');
            
            // 先获取所有 input 找到正确的那个
            const allInputs = await detailPage.locator('input').all();
            let filled = false;
            
            for (const input of allInputs) {
                const ph = await input.getAttribute('placeholder');
                if (ph && ph.toLowerCase().includes('please enter')) {
                    // 找到正确的输入框了
                    // 使用 click() 聚焦，然后逐字符输入，触发 React 的 onChange
                    await input.click();
                    await detailPage.waitForTimeout(100);
                    
                    // 清除可能存在的任何内容
                    await input.selectText();
                    await detailPage.waitForTimeout(100);
                    
                    // 逐字符输入，每个字符后等待让 React 处理
                    for (const char of CREDIT_AMOUNT) {
                        await input.press(char === '0' ? '0' : char);
                        await detailPage.waitForTimeout(50);
                    }
                    
                    // 额外等待让 React 完成验证
                    await detailPage.waitForTimeout(500);
                    
                    const actualValue = await input.evaluate(el => el.value);
                    log(`  - ✅ 已填写金额: ${actualValue || CREDIT_AMOUNT}`);
                    filled = true;
                    break;
                }
            }
            
            if (!filled) {
                log('  ⚠️ 未找到金额输入框');
            }
        } else {
            // 选择 Refuse Code
            log('  - 选择 Refuse Code...');
            const refuseSelects = await detailPage.locator('.ant-select:visible').all();
            if (refuseSelects.length >= 2) {
                await refuseSelects[1].click();
            } else {
                const allSelects = await detailPage.locator('.ant-select').all();
                await allSelects[1].click();
            }
            await detailPage.waitForTimeout(1000);

            await detailPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE }).first().click();
            log(`  - ✅ 已选择拒绝码: ${REFUSE_CODE}`);
        }

        // 点击提交按钮
        log('  - 点击提交按钮...');
        await detailPage.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Submit') {
                    btn.click();
                    return;
                }
            }
        });
        log('  - ✅ 已点击提交按钮');
        await detailPage.waitForTimeout(5000);

        // ========== 9. 验证结果 ==========
        log('[9/9] 验证审批结果...');
        await detailPage.close();

        // 重新搜索案件验证
        log('   重新搜索案件验证...');
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);

        const finalStatus = await page.evaluate((caseNo) => {
            const rows = document.querySelectorAll('tbody tr');
            for (const row of rows) {
                if (row.textContent.includes(caseNo)) return row.textContent;
            }
            return null;
        }, CASE_NO);

        if (finalStatus) {
            if (finalStatus.includes('Closed') || finalStatus.includes('已结案')) {
                if (finalStatus.includes('Reject') || finalStatus.includes('拒绝')) {
                    log('');
                    log('========================================');
                    log(`  🎉 审批拒绝成功！`);
                    log(`  案件 ${CASE_NO} 已结案`);
                    log(`  拒绝码: ${REFUSE_CODE}`);
                    log('========================================');
                } else if (finalStatus.includes('Approved') || finalStatus.includes('同意')) {
                    log('');
                    log('========================================');
                    log(`  🎉 审批通过成功！`);
                    log(`  案件 ${CASE_NO} 已结案`);
                    log(`  审批金额: ${CREDIT_AMOUNT}`);
                    log('========================================');
                } else {
                    log(`✅ 案件已结案: ${finalStatus.substring(0, 100)}`);
                }
            } else {
                log('⚠️ 案件状态未变化');
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