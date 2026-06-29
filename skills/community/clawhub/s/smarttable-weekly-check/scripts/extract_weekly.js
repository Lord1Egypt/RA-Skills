/**
 * 一键周报数据提取脚本（Puppeteer 版）
 * 用法: node scripts/extract_weekly.js <links_file>
 *   links_file: 每行一个智能表格链接
 *
 * 全自动：启动浏览器 → 登录检测 → 等待扫码 → 提取数据 → 保存JSON → 关闭
 * 用户只需提供链接文件，其余无需操作
 * 首次运行会自动下载 Chromium（约 150MB）
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const puppeteer = require('puppeteer');

const DATA_DIR = path.join(__dirname, '..', 'smartsheet_data');

// ====== 登录等待配置 ======
const LOGIN_POLL_INTERVAL = 3000;  // 轮询间隔 3秒
const LOGIN_POLL_TIMEOUT = 300000; // 最多等 5分钟

// ====== 工具函数 ======

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

/**
 * 判断 API 返回是否为未登录错误
 */
function isLoginError(j) {
  if (!j) return false;
  // 顶层 errcode
  if (j.errcode === 30004) return true;
  // clientVars 层 retcode
  if (j.clientVars && j.clientVars.retcode && j.clientVars.retcode !== 0) {
    const msg = String(j.clientVars.errmsg || '').toLowerCase();
    if (msg.includes('userinfo') || msg.includes('check user') || msg.includes('login')) return true;
  }
  return false;
}

/**
 * 在页面内 fetch 提取智能表格数据
 */
async function extractFromPage(page, padId, scode) {
  return await page.evaluate(async (padId, scode) => {
    try {
      const resp = await fetch(`https://doc.weixin.qq.com/dop-api/opendoc?scode=${scode}&tab=MhFWYk&id=${padId}&outformat=1&normal=1&startrow=0&endrow=60&wb=1&nowb=0&noEscape=1&enableSmartsheetSplit=1`);
      const text = await resp.text();
      const j = JSON.parse(text);

      // 未登录
      if (j.errcode === 30004) {
        return { error: true, retcode: 30004, errmsg: j.errmsg || 'check userInfo failed' };
      }
      if (j.clientVars && j.clientVars.retcode && j.clientVars.retcode !== 0) {
        return { error: true, retcode: j.clientVars.retcode, errmsg: j.clientVars.errmsg };
      }

      const ss = j.clientVars.collab_client_vars.initialAttributedText.text[0].smartsheet;
      const data = JSON.parse(ss);
      const meta = data[0][0], cells = data[0][1];
      const users = meta.c['3']['5'];
      const userName = {};
      for (const [k, v] of Object.entries(users)) userName[k] = v['2'];
      const fields = meta.c['3']['3'];
      let nameFid, workFid, planFid;
      for (const [fid, finfo] of Object.entries(fields)) {
        const n = finfo['30'];
        if (n === '姓名') nameFid = fid;
        if (n === '本周工作内容') workFid = fid;
        if (n === '下周工作计划') planFid = fid;
      }
      const rows = cells.c['2']['1'];
      const people = [];
      for (const [rid, row] of Object.entries(rows)) {
        const rc = row['1'];
        const nameCell = rc[nameFid];
        let name = '';
        if (nameCell && nameCell['7'] && nameCell['7'][0] && nameCell['7'][0]['1']) {
          const uid = nameCell['7'][0]['1'];
          name = userName[uid] || '';
        }
        if (!name) continue;
        const work = (rc[workFid] && rc[workFid]['1']) ? rc[workFid]['1'].map(s => s['2'] || '').join('').trim() : '';
        const plan = (rc[planFid] && rc[planFid]['1']) ? rc[planFid]['1'].map(s => s['2'] || '').join('').trim() : '';
        people.push({ name, work, plan });
      }
      return { title: j.clientVars.title, count: people.length, people };
    } catch (e) {
      return { error: true, message: e.message };
    }
  }, padId, scode);
}

/**
 * 轮询等待登录完成
 * 反复用第一个链接的 API 探测，直到返回正常数据
 */
async function waitForLogin(page, padId, scode) {
  console.log('⏳ 等待扫码登录...');
  const startTime = Date.now();
  let dots = 0;

  while (Date.now() - startTime < LOGIN_POLL_TIMEOUT) {
    await sleep(LOGIN_POLL_INTERVAL);
    try {
      const result = await extractFromPage(page, padId, scode);
      if (!result.error) {
        console.log('\n✅ 登录成功！');
        return true;
      }
    } catch { /* 忽略，继续轮询 */ }
    dots++;
    process.stdout.write('.');
    if (dots % 10 === 0) process.stdout.write(` (${Math.round((Date.now() - startTime) / 1000)}s)`);
  }

  console.log('\n❌ 等待登录超时（5分钟），请重新运行脚本。');
  return false;
}

// ====== 解析链接 ======

const linksFile = process.argv[2];
if (!linksFile || !fs.existsSync(linksFile)) {
  console.error('用法: node scripts/extract_weekly.js <links_file>');
  console.error('  links_file: 每行一个智能表格链接');
  process.exit(1);
}

const links = fs.readFileSync(linksFile, 'utf8')
  .split('\n')
  .map(l => l.trim())
  .filter(l => l.startsWith('http'));

if (links.length === 0) {
  console.error('链接文件为空或格式不正确');
  process.exit(1);
}

console.log(`发现 ${links.length} 个链接`);

// ====== 确保输出目录 ======
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// ====== 主流程 ======

(async () => {
  let browser;
  try {
    // 启动浏览器（使用用户数据目录保留登录态）
    const userDataDir = path.join(os.homedir(), '.smarttable-check-browser');
    console.log('\n启动浏览器...');
    browser = await puppeteer.launch({
      headless: false,
      defaultViewport: null,
      userDataDir,
      args: ['--no-sandbox', '--disable-blink-features=AutomationControlled']
    });

    const results = [];

    // ====== Step 1: 打开第一个链接，探测登录 ======
    console.log('\n[1/3] 检测登录状态...');
    const page1 = await browser.newPage();
    await page1.goto(links[0], { waitUntil: 'domcontentloaded', timeout: 30000 });
    await sleep(5000);

    const firstPadId = links[0].match(/(s3_[A-Za-z0-9]+)/)?.[1];
    const firstScode = links[0].match(/scode=([A-Za-z0-9]+)/)?.[1];

    if (firstPadId && firstScode) {
      const probeData = await extractFromPage(page1, firstPadId, firstScode);

      if (probeData.error && (probeData.retcode === 30004 || isLoginError(probeData))) {
        console.log('\n⚠️  未登录企业微信！');
        console.log('📋 请在弹出的浏览器窗口中扫码登录，脚本将自动检测登录状态...');
        const loggedIn = await waitForLogin(page1, firstPadId, firstScode);
        if (!loggedIn) {
          await browser.close();
          process.exit(1);
        }
      }
      // 无论是否需要登录，都提取第一个链接的数据
      // 登录后或网络超时后需要刷新再提取（最多重试3次）
      let w1Data = probeData;
      if (w1Data.error) {
        for (let retry = 0; retry < 3; retry++) {
          await page1.reload({ waitUntil: 'domcontentloaded', timeout: 30000 });
          await sleep(3000 + retry * 2000); // 逐步加长等待
          w1Data = await extractFromPage(page1, firstPadId, firstScode);
          if (!w1Data.error) break;
          console.log(`  W1: 重试 ${retry + 1}/3...`);
        }
      }
      if (w1Data.error) {
        console.error(`  W1: API错误 - ${w1Data.errmsg || w1Data.message}`);
      } else {
        if (!probeData.error) console.log('✅ 已登录');
        results.push({ idx: 1, data: w1Data });
        console.log(`  W1: ${w1Data.title} (${w1Data.count}人)`);
      }
    }

    // ====== Step 2: 逐个打开并提取剩余链接 ======
    console.log('\n[2/3] 提取数据...');
    for (let i = 1; i < links.length; i++) {
      const url = links[i];
      const padId = url.match(/(s3_[A-Za-z0-9]+)/)?.[1];
      const scode = url.match(/scode=([A-Za-z0-9]+)/)?.[1];
      if (!padId || !scode) {
        console.error(`  W${i + 1}: 链接格式不正确`);
        continue;
      }

      const page = await browser.newPage();
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await sleep(3000);

      let data = await extractFromPage(page, padId, scode);
      // 网络超时重试
      if (data.error && data.retcode !== 30004) {
        for (let retry = 0; retry < 2; retry++) {
          console.log(`  W${i + 1}: 重试 ${retry + 1}/2...`);
          await sleep(3000);
          data = await extractFromPage(page, padId, scode);
          if (!data.error) break;
        }
      }
      if (data.error) {
        console.error(`  W${i + 1}: API错误 - ${data.errmsg || data.message} (retcode=${data.retcode})`);
      } else {
        results.push({ idx: i + 1, data });
        console.log(`  W${i + 1}: ${data.title} (${data.count}人)`);
      }

      await page.close();
      await sleep(500); // 避免请求过快
    }

    // 关闭第一个页面
    await page1.close();

    // ====== Step 3: 保存到文件 ======
    console.log('\n[3/3] 保存数据...');
    for (const r of results) {
      const outFile = path.join(DATA_DIR, `w${r.idx}.json`);
      fs.writeFileSync(outFile, JSON.stringify(r.data, null, 2), 'utf8');
      const verify = JSON.parse(fs.readFileSync(outFile, 'utf8'));
      console.log(`  w${r.idx}.json: ${verify.people?.length || 0}人, ${verify.title}`);
    }

    console.log(`\n✅ 完成！提取了 ${results.length}/${links.length} 周数据。`);
    console.log(`运行分析: node scripts/analyze.js`);
    console.log(`项目汇总: node scripts/project_summary.js`);

  } catch (e) {
    console.error(`\n❌ 运行出错: ${e.message}`);
    process.exit(1);
  } finally {
    if (browser) {
      try { await browser.close(); } catch {}
    }
  }
})();
