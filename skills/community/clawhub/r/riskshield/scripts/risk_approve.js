/**
 * RiskShield 案件审批自动化 - 最终稳定版
 * 
 * 使用方法:
 *   node risk_approve.js <案件号> <操作> [拒绝码] [审批金额]
 * 
 * 示例:
 *   node risk_approve.js 2604151000000598528 pass
 *   node risk_approve.js 2604151000000598528 refuse CA_TRUE_HIT
 *   node risk_approve.js 2604151000000598528 pass 100 50000
 */

const { chromium } = require('playwright');

const CASE_NO = process.argv[2] || '2604151000000598528';
const ACTION = (process.argv[3] || 'pass').toLowerCase();
const REFUSE_CODE = process.argv[4] || 'CA_TRUE_HIT';
const CREDIT_AMOUNT = process.argv[5] || '100';

async function log(msg) {
    console.log(`[${new Date().toISOString()}] ${msg}`);
}

(async () => {
    log(`=== RiskShield 案件审批自动化 ===`);
    log(`案件号: ${CASE_NO}`);
    log(`操作: ${ACTION === 'pass' ? '通过 (PASS)' : '拒绝 (REFUSE)'}`);
    if (ACTION === 'pass') {
        log(`审批金额: ${CREDIT_AMOUNT}`);
    } else {
        log(`拒绝码: ${REFUSE_CODE}`);
    }
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
        await page.goto('https://riskshield.dcsuat.com/mc/page/login.html?redirect=aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(6000);
        
        await page.locator('input[placeholder*="user" i]').fill('taskAccount');
        await page.locator('input[placeholder*="password" i]').fill('ZIdongshenpi1.');
        await page.locator('button:has-text("login")').click();
        await page.waitForTimeout(10000);
        log('[1/8] ✅ 登录成功');

        // ========== 2. 选择搜索类型: No. ==========
        log('[2/8] 选择搜索类型: 案件编号 (No.)...');
        
        // 点击 Case Name 下拉框
        await page.locator('span.val:has-text("Case Name")').first().click();
        await page.waitForTimeout(1500);
        
        // 选择 No. (第二个选项)
        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(500);
        log('[2/8] ✅ 已选择"案件编号"');

        // ========== 3. 输入案件号 ==========
        log(`[3/8] 输入案件号: ${CASE_NO}...`);
        
        // 使用第三个输入框 (index 2) 输入案件号
        const inputBox = page.locator('input[type="text"]').nth(2);
        await inputBox.click();
        await page.keyboard.type(CASE_NO, { delay: 30 });
        await page.waitForTimeout(500);
        log('[3/8] ✅ 案件号已输入');

        // ========== 4. 点击搜索 ==========
        log('[4/8] 点击搜索...');
        
        // 使用 JS 点击搜索按钮避免被遮罩
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const searchBtn = buttons.find(b => b.textContent.trim() === 'Search');
            if (searchBtn) searchBtn.click();
        });
        await page.waitForTimeout(5000);

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
            log('❌ 案件已结案，无法重复审批');
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
        
        // 首先填写 Basic Information 中的 WI_cFrG4FQa 字段（如果存在）
        const wiFieldExists = await detailPage.evaluate(() => {
            return !!document.getElementById('WI_cFrG4FQa');
        });
        
        if (wiFieldExists) {
            log('  - 找到 WI_cFrG4FQa 字段，正在填写...');
            await detailPage.locator('#WI_cFrG4FQa .ant-select').click();
            await detailPage.waitForTimeout(1500);
            await detailPage.locator('.ant-select-item').filter({ hasText: REFUSE_CODE || 'CA_TRUE_HIT' }).click();
            await detailPage.waitForTimeout(1000);
            log(`  - WI_cFrG4FQa 已填写: ${REFUSE_CODE || 'CA_TRUE_HIT'}`);
        }
        
        // 点击 "Decision Information" 选项卡
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
        log('  - 已切换到 Decision Information 选项卡');
        
        // 选择 ManualApprovalResult: Pass 或 Refuse
        await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first().click();
        await detailPage.waitForTimeout(1000);
        
        if (ACTION === 'pass') {
            // 点击第一个 Please choose 下拉框
            await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first().click();
            await detailPage.waitForTimeout(1000);
            log('  - 已打开 ManualApprovalResult 下拉框');
            
            // 等待并选择 Pass 选项
            await detailPage.locator('.ant-select-item').filter({ hasText: /^Pass$/ }).click();
            await detailPage.waitForTimeout(2000);
            log('  - 已选择: Pass');
            
            // 使用 JavaScript 找到 Credit Amount 输入框并填写
            const filled = await detailPage.evaluate((amount) => {
                // 找到 Credit Amount 字段
                const allElements = document.querySelectorAll('*');
                for (const el of allElements) {
                    if (el.childNodes.length === 1 && el.textContent.toLowerCase().includes('credit amount')) {
                        const formItem = el.closest('.ant-form-item');
                        if (formItem) {
                            const inputNumber = formItem.querySelector('.ant-input-number input');
                            if (inputNumber) {
                                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                                nativeInputValueSetter.call(inputNumber, amount);
                                inputNumber.dispatchEvent(new Event('input', { bubbles: true }));
                                inputNumber.dispatchEvent(new Event('change', { bubbles: true }));
                                return true;
                            }
                            // 也尝试直接找 input
                            const input = formItem.querySelector('input');
                            if (input) {
                                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                                nativeInputValueSetter.call(input, amount);
                                input.dispatchEvent(new Event('input', { bubbles: true }));
                                input.dispatchEvent(new Event('change', { bubbles: true }));
                                return true;
                            }
                        }
                    }
                }
                return false;
            }, CREDIT_AMOUNT);
            
            if (filled) {
                log(`  - 已填写审批金额: ${CREDIT_AMOUNT}`);
            } else {
                // 备用方案：使用 ant-input-number
                const inputNum = detailPage.locator('.ant-input-number input').first();
                await inputNum.fill(CREDIT_AMOUNT);
                log(`  - 已填写审批金额(备用方案): ${CREDIT_AMOUNT}`);
            }
            log(`  - 已填写审批金额: ${CREDIT_AMOUNT}`);
        } else {
            // Refuse 操作：WI_cFrG4FQa 已经在前面填写了，这里只需要选择 Refuse
            await detailPage.locator('.ant-select').filter({ hasText: 'Please choose' }).first().click();
            await detailPage.waitForTimeout(1000);
            
            // 选择 Refuse
            await detailPage.locator('.ant-select-item').filter({ hasText: /^Refuse$/ }).click();
            await detailPage.waitForTimeout(2000);
            log('  - 已选择: Refuse');
        }
        
        // 点击 Submit
        await detailPage.locator('button').filter({ hasText: 'Submit' }).click();
        log('  - 已点击提交按钮');
        await detailPage.waitForTimeout(3000);
        log('[8/8] ✅ 表单已提交');

        // ========== 9. 验证结果 ==========
        log('[9/9] 验证审批结果...');
        await detailPage.close();
        await page.bringToFront();
        await page.waitForTimeout(2000);
        
        // 重新搜索案件 - 同样流程
        log('重新搜索案件验证结果...');
        
        // 选择搜索类型
        await page.locator('span.val:has-text("Case Name")').first().click();
        await page.waitForTimeout(1500);
        await page.locator('a.dropdown-item').nth(1).click();
        await page.waitForTimeout(500);
        
        // 输入案件号
        const inputCase = page.locator('input[type="text"]').nth(2);
        await inputCase.click();
        await page.keyboard.type(CASE_NO, { delay: 30 });
        await page.waitForTimeout(500);
        
        // 点击搜索
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
                if (finalStatus.includes('Approved') || finalStatus.includes('同意')) {
                    log('');
                    log('========================================');
                    log('  🎉 审批通过成功！');
                    log(`  案件 ${CASE_NO} 已结案，审批结果: Approved`);
                    log('========================================');
                } else if (finalStatus.includes('Reject') || finalStatus.includes('拒绝')) {
                    log('');
                    log('========================================');
                    log('  🎉 审批拒绝成功！');
                    log(`  案件 ${CASE_NO} 已结案，审批结果: Reject`);
                    log('========================================');
                } else {
                    log(`✅ 案件已结案，状态: ${finalStatus.includes('Closed') ? 'Closed' : '已结案'}`);
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
    } finally {
        await browser.close();
    }
})();
