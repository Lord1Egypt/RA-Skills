/**
 * 有头浏览器常驻控制器 —— 视频下载的核心驱动
 *
 * 用途：打开目标视频页，长驻不关，拦截所有媒体请求并记录 URL；
 *       同时暴露「文件命令通道」供外部脚本远程控制播放器(seek/play/填密码等)。
 *
 * 用法：
 *   node browser_ctl.mjs <工作目录> <视频页URL> [最小时长秒]
 *   例： node browser_ctl.mjs /tmp/dl "https://v.youku.com/v_show/id_XXX.html" 600
 *
 * 文件通道（都在<工作目录>下）：
 *   cmd.txt        写入一行命令即执行（执行后自动删除）
 *   status.txt     每 0.7s 刷新：{"t":当前秒,"dur":总时长,"paused":bool,"w":视频宽度}
 *   netlog2.jsonl  追加模式，每条 {status,url,ts}
 *   shots/latest.png  每 4s 自动截图
 *   dom.txt        `dom` 命令导出：主文档+所有 iframe 的可见文本与输入框（诊断弹窗）
 *   stop.flag      存在即优雅退出
 *
 * 支持命令：
 *   seek <秒>              跳转并播放（会触发新的媒体请求）
 *   play / pause           播放 / 暂停
 *   rate <倍数>            设置倍速
 *   dom                    导出页面文本与输入框，用于诊断弹窗/验证码
 *   logininfo              检测登录态（优酷以 cookie `unb` 用户ID 为准，写 logininfo.txt + 日志）
 *                          未登录无法切 1080P，必须提醒用户手动登录并切画质后再采集
 *   pwauto <密码>          【优酷·首选】一条龙过密码：真实点击聚焦→keyboard.type 逐字符输入
 *                          →真实鼠标点「确定」。已验证可全自动（Enter 键对该弹窗无效）。
 *   pwfill <密码>          【优酷·已弃用】原生 setter 填值（Vue v-model 不同步，提交空密码）
 *   pwsubmit               【优酷】JS 派发事件点确定（可能被拦截，备用）
 *   pwinfo                 【优酷】导出密码弹窗 HTML 与输入框当前值（诊断用）
 *   ktype <文本>           真实键盘逐字符输入（需先 click 聚焦目标）
 *   press <键名>           按键，如 Enter / Tab / Escape
 *   realclick <选择器>     真实鼠标坐标点击（绕过前端事件拦截；不带参则点文本为「确定」的按钮）
 *   type <选择器> <文本>   向输入框填内容（自动跨 iframe）
 *   click <选择器>         点击元素（自动跨 iframe）
 *
 * ⚠️ 命令通道竞态：cmd.txt 是单文件，连发两条命令会互相覆盖（后写冲掉先写，先写永不执行）。
 *    每条命令之间等日志出现 [CMD] xxx（被消费）再发下一条，不要 sleep 短就连续覆盖。
 *
 * 关键设计（踩过的坑）：
 *  1. 必须用 CDP Network.setCacheDisabled 禁用缓存，否则重复 seek 到同一位置
 *     会命中浏览器缓存、不发网络请求，导致监听不到 URL。
 *  2. 主页面在监听器注册之后才 goto，否则首屏请求全部漏掉。
 *  3. 用 launchPersistentContext + 固定 profile，登录态可跨会话复用。
 *  4. 不要用 page.waitForTimeout（某些版本不存在），统一用 setTimeout Promise。
 *  5. 用 file 通道而非 stdin 通信，脚本崩溃重启后不丢上下文。
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { chromium } from 'playwright-core';

const ROOT = process.argv[2];
const TARGET = process.argv[3];
const MINDUR = parseFloat(process.argv[4] || '600'); // 主视频判定时长阈值
if (!ROOT || !TARGET) {
  console.error('用法: node browser_ctl.mjs <工作目录> <视频页URL> [最小时长秒]');
  process.exit(1);
}
fs.mkdirSync(path.join(ROOT, 'shots'), { recursive: true });

// ── 浏览器与 profile：全局唯一，杜绝"两边横跳、反复登录" ──
// 规则：
//  1. 浏览器固定用本机 Chrome（channel:'chrome'）；只有 Chrome 启动失败才回退内置 Chromium。
//  2. profile 默认用【全局共享目录】（与工作目录无关），所有视频下载任务共用同一个登录态：
//       ~/.workbuddy/browser-profiles/video-downloader
//     用户在任意一次任务里登录后，以后所有任务（优酷/腾讯/爱奇艺/B站…）都免登录。
//  3. 可用环境变量 CHROME_PROFILE 覆盖（例如想驱动用户真实 Chrome 时指向其 Default profile，
//     但注意真实 Chrome 正在运行时会因 profile 被占用而启动失败）。
//  4. 不要每个工作目录建独立 profile——那会导致每个任务都要重新登录。
const SHARED_PROFILE = process.env.CHROME_PROFILE
  || path.join(os.homedir(), '.workbuddy', 'browser-profiles', 'video-downloader');
fs.mkdirSync(SHARED_PROFILE, { recursive: true });
const PROFILE = SHARED_PROFILE;

const LOGFILE = path.join(ROOT, 'netlog2.jsonl');
const CMD = path.join(ROOT, 'cmd.txt');
const STATUS = path.join(ROOT, 'status.txt');
const STOP = path.join(ROOT, 'stop.flag');

// 追加模式：重启后保留已抓到的 URL，不清空
for (const f of [CMD, STATUS]) { try { fs.unlinkSync(f); } catch (e) {} }
try { fs.unlinkSync(STOP); } catch (e) {}

const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a);

function isMedia(url) {
  return /\.(m3u8|ts|mp4|m4s|f4v|flv|mkv|webm)(\?|$)/i.test(url)
    || /\/youkula\//.test(url)
    || /cibntv|alicdn|bilivideo|qq\.com\/.*video|douyinvod|ixigua/i.test(url);
}

const launchOpts = {
  headless: false,
  slowMo: 80,
  viewport: null,
  // 稳定性参数：macOS 沙箱/无独显环境下 GPU 合成易崩溃，关掉后 renderer 更稳
  args: [
    '--disable-blink-features=AutomationControlled',
    '--no-first-run', '--no-default-browser-check', '--disable-infobars',
    '--autoplay-policy=no-user-gesture-required',
    '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage',
    '--disable-features=Translate,BackForwardCache', '--no-zygote',
  ],
};

// 优先本机 Chrome；启动失败（未安装等）才回退内置 Chromium。统一浏览器，避免两套环境横跳。
let ctx;
let usedBrowser = 'chrome';
try {
  ctx = await chromium.launchPersistentContext(PROFILE, { ...launchOpts, channel: 'chrome' });
  log('使用浏览器: 本机 Google Chrome');
} catch (e) {
  log('本机 Chrome 启动失败，回退内置 Chromium:', e.message.slice(0, 80));
  usedBrowser = 'chromium';
  ctx = await chromium.launchPersistentContext(PROFILE, launchOpts);
  log('使用浏览器: 内置 Chromium');
}
log('共享 profile:', PROFILE);
await ctx.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});

const seen = new Set();
function attach(p) {
  p.on('response', (res) => {
    try {
      const url = res.url();
      if (!isMedia(url)) return;
      if (seen.has(url)) return;
      seen.add(url);
      fs.appendFileSync(LOGFILE, JSON.stringify({ status: res.status(), url, ts: Date.now() }) + '\n');
      log('[HIT]', url.slice(0, 130));
    } catch (e) {}
  });
}
ctx.on('page', attach);
ctx.pages().forEach(attach);

const page = ctx.pages()[0] || await ctx.newPage();
page.on('crash', () => log('[page crash] 渲染进程崩溃'));
page.on('close', () => log('[page close] 页面被关闭'));
try {
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  log('CDP 缓存已禁用');
} catch (e) { log('[cdp warn]', e.message.slice(0, 80)); }
await page.goto(TARGET, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch((e) => log('[goto]', e.message));

// 跨 iframe 查找主视频元素（时长 > MINDUR 判定为正片，排除广告/预览）
async function findVideo() {
  for (const fr of page.frames()) {
    try {
      const ok = await fr.evaluate((d) => {
        return [...document.querySelectorAll('video')].some((v) => v.duration > d);
      }, MINDUR);
      if (ok) return fr;
    } catch (e) {}
  }
  return null;
}

async function vact(fn) {
  const fr = await findVideo();
  if (!fr) return null;
  try { return await fr.evaluate(fn); } catch (e) { return 'ERR:' + e.message.slice(0, 80); }
}

// ---------- 优酷密码弹窗专用 ----------
const PW_INPUT = '#kui_layer_password-layer_passwordInput, .kui-passwordlayer-password-input';

// 密码弹窗检测：弹窗一出现就可以接受 pwauto 等命令，不用死等主视频。
// 优酷用专用选择器；其他平台兜底检测「可见的密码输入框」。
async function findPasswordDialog() {
  try {
    return await page.evaluate((sel) => {
      if (document.querySelector(sel)) return true;
      return [...document.querySelectorAll('input[type=password]')]
        .some((i) => i.offsetParent !== null);
    }, PW_INPUT);
  } catch (e) { return false; }
}

log(`等待主视频元素(duration>${MINDUR}s)或密码弹窗...`);
let ready = false;
let pwDialog = false;
for (let i = 0; i < 150 && !ready && !pwDialog; i++) {
  await new Promise((r) => setTimeout(r, 1000)).catch(() => {});
  try {
    ready = !!(await findVideo());
    if (!ready) pwDialog = await findPasswordDialog();
  } catch (e) {}
}
if (ready) {
  log('主视频就绪（无密码拦截），开始接受命令，可直接采集 URL');
} else if (pwDialog) {
  log('检测到观看密码弹窗，命令通道已就绪：发 `pwauto <密码>` 自动过，失败则请用户手动输入');
} else {
  log('超时：既无主视频也无密码弹窗（可能需登录/滑动验证）。命令通道仍开启，用户处理后 status 会自动刷新');
}

// 启动后自动检测登录态（未登录无法切 1080P，必须提醒用户）
async function checkLogin() {
  try {
    let names = [];
    try { names = (await ctx.cookies()).map(c => c.name); } catch (e) {}
    const loggedIn = names.includes('unb') || names.includes('tracknick');
    log(loggedIn
      ? '【登录态】已登录 ✓ 可切换/采集最高画质'
      : '【登录态】未登录 ✗ 请提醒用户手动登录并把清晰度切到最高（1080P），否则只能拿到低画质');
  } catch (e) {}
}
await checkLogin();

function fillPwJs(pwd) {
  // 用 JSON.stringify 转义，避免密码里含引号/反斜杠时把 JS 语法撑破
  const safe = JSON.stringify(String(pwd ?? ''));
  return `(() => {
    const inp = document.querySelector(${JSON.stringify(PW_INPUT)});
    if (!inp) return 'no-input';
    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    setter.call(inp, ${safe});
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    inp.dispatchEvent(new Event('change', { bubbles: true }));
    return 'filled:' + inp.value;
  })()`;
}

const submitPwJs = `(() => {
  const inp = document.querySelector('${PW_INPUT}');
  let cands = [...document.querySelectorAll('.kui-passwordlayer-password-option, [class*=password-option]')];
  if (!cands.length) {
    cands = [...document.querySelectorAll('button, [role=button], a')].filter(el => el.textContent.trim() === '确定');
  }
  if (!cands.length) return 'no-btn';
  const target = cands[0].querySelector('button, span') || cands[0];
  ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(t => {
    target.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window }));
    cands[0].dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window }));
  });
  return 'clicked:' + (target.className || target.tagName) + ' val=' + (inp ? inp.value : '?');
})()`;

let lastShot = 0;
const t = setInterval(async () => {
  let st = null;
  try {
    st = await vact(`(() => {
      const v = [...document.querySelectorAll('video')].find(v => v.duration > ${MINDUR});
      if (!v) return 'novideo';
      return JSON.stringify({t: v.currentTime.toFixed(1), dur: Math.round(v.duration), paused: v.paused, w: v.videoWidth, rate: v.playbackRate});
    })()`);
  } catch (e) { st = 'ERR:' + e.message.slice(0, 60); }
  if (st) fs.writeFileSync(STATUS, String(st));

  if (Date.now() - lastShot > 4000) {
    lastShot = Date.now();
    page.screenshot({ path: path.join(ROOT, 'shots', 'latest.png') }).catch(() => {});
  }

  try {
    if (fs.existsSync(CMD)) {
      const lines = fs.readFileSync(CMD, 'utf8').split('\n').map((s) => s.trim()).filter(Boolean);
      fs.unlinkSync(CMD);
      for (const line of lines) {
        log('[CMD]', line);
        const [op, arg] = line.split(/\s+/);

        if (op === 'seek') {
          const sec = parseFloat(arg);
          if (!isFinite(sec) || sec < 0) { log('[seek] 非法秒数:', arg); continue; }
          await vact(`(() => {
            const v=[...document.querySelectorAll('video')].find(v=>v.duration>${MINDUR});
            if(!v) return 'no';
            v.muted=true; v.currentTime=${sec};
            const pr=v.play(); if(pr) pr.catch(()=>{});
            return 'ok '+v.currentTime;
          })()`);
        } else if (op === 'rate') {
          await vact(`(() => { const v=[...document.querySelectorAll('video')].find(v=>v.duration>${MINDUR}); if(!v)return 'no'; v.playbackRate=${parseFloat(arg)}; return v.playbackRate; })()`);
        } else if (op === 'pause') {
          await vact(`(() => { const v=[...document.querySelectorAll('video')].find(v=>v.duration>${MINDUR}); if(!v)return 'no'; v.pause(); return 'paused'; })()`);
        } else if (op === 'play') {
          await vact(`(() => { const v=[...document.querySelectorAll('video')].find(v=>v.duration>${MINDUR}); if(!v)return 'no'; v.muted=true; const p=v.play(); if(p)p.catch(()=>{}); return 'playing'; })()`);
        } else if (op === 'dom') {
          let dump = '== MAIN ' + page.url() + '\n';
          try {
            dump += (await page.evaluate(() => document.body.innerText.slice(0, 1500))) + '\n';
            dump += '== INPUTS: ' + String(await page.evaluate(() =>
              [...document.querySelectorAll('input')].map(i => `${i.type}|${i.placeholder}|${i.id}|${i.className}`).join(' ; '))).slice(0, 800) + '\n';
          } catch (e) { dump += 'ERR ' + e.message.slice(0, 60) + '\n'; }
          for (const fr of page.frames()) {
            if (fr === page.mainFrame()) continue;
            try {
              const txt = await fr.evaluate(() => document.body ? document.body.innerText.slice(0, 800) : '');
              const inp = await fr.evaluate(() => [...document.querySelectorAll('input')].map(i => `${i.type}|${i.placeholder}|${i.id}`).join(' ; ')).catch(() => '');
              dump += `== FRAME ${fr.url().slice(0, 90)}\n${txt}\nINPUTS: ${String(inp).slice(0, 400)}\n`;
            } catch (e) {}
          }
          fs.writeFileSync(path.join(ROOT, 'dom.txt'), dump);
          log('[DOM] dumped');
        } else if (op === 'logininfo') {
          // 检测登录状态：未登录无法切 1080P，必须提醒用户手动登录。
          // 优酷登录态核心 cookie 是 unb（用户数字ID），未登录时不存在；httpOnly 也能被 ctx.cookies 读到。
          try {
            let cookies = [];
            try { cookies = await ctx.cookies(); } catch (e) {}
            const names = cookies.map(c => c.name);
            // 优酷/淘宝系登录态标识：unb(用户ID)、tracknick(昵称)、cookie2、_l_g_
            const loginCookies = cookies
              .filter(c => /^(unb|tracknick|cookie2|_l_g_)$/.test(c.name))
              .map(c => `${c.name}=${String(c.value).slice(0, 16)}`);
            const hasUnb = names.includes('unb');
            const pageLoginBtn = await page.evaluate(() => {
              const btn = [...document.querySelectorAll('a,button,span,div')]
                .find(e => e.textContent.trim() === '登录' && e.offsetParent && e.children.length === 0);
              return !!btn;
            }).catch(() => null);
            // 以 unb 为准（最可靠）；页面登录入口作辅助参考
            const loggedIn = hasUnb;
            fs.writeFileSync(path.join(ROOT, 'logininfo.txt'),
              JSON.stringify({ loggedIn, hasUnb, pageHasLoginBtn: pageLoginBtn,
                loginCookies, allCookieNames: names }, null, 2));
            log('[logininfo]', loggedIn ? '已登录（可切1080P）✓' : '未登录（需提醒用户登录+切1080P）✗',
                '| 登录cookie:', loginCookies.join(', ') || '(无 unb/tracknick)');
          } catch (e) { log('[logininfo err]', e.message.slice(0, 100)); }
        } else if (op === 'cookies') {
          // 导出全部 cookie（含 httpOnly 的 SESSDATA 等），供需要登录态的站点（B站/优酷/腾讯）拉高画质 manifest 用
          try {
            const cookies = await ctx.cookies();
            fs.writeFileSync(path.join(ROOT, 'cookies.json'), JSON.stringify(cookies, null, 2));
            const names = cookies.map(c => c.name);
            log('[cookies] dumped', cookies.length, 'cookies;',
              'SESSDATA=' + (names.includes('SESSDATA') ? '有✓' : '无✗'),
              '| bili_jct=' + (names.includes('bili_jct') ? '有✓' : '无✗'));
          } catch (e) { log('[cookies err]', e.message.slice(0, 100)); }
        } else if (op === 'pwfill') {
          try { log('[pwfill]', await page.evaluate(fillPwJs(arg || ''))); }
          catch (e) { log('[pwfill err]', e.message.slice(0, 60)); }
        } else if (op === 'pwsubmit') {
          try { log('[pwsubmit]', await page.evaluate(submitPwJs)); }
          catch (e) { log('[pwsubmit err]', e.message.slice(0, 60)); }
        } else if (op === 'pwinfo') {
          const js = `(() => {
            let el = document.querySelector('${PW_INPUT}');
            if (!el) return 'no-input';
            let node = el;
            for (let i=0;i<6 && node.parentElement;i++) node = node.parentElement;
            return JSON.stringify({inputVal: el.value, containerClass: node.className, html: node.outerHTML.slice(0,1500)});
          })()`;
          try {
            fs.writeFileSync(path.join(ROOT, 'pwinfo.txt'), String(await page.evaluate(js)));
            log('[pwinfo] saved');
          } catch (e) { log('[pwinfo err]', e.message.slice(0, 60)); }
        } else if (op === 'realclick') {
          try {
            const js = `(() => {
              const btn = ${arg ? `document.querySelector(${JSON.stringify(arg)}) ||` : ''}
                [...document.querySelectorAll('*')].filter(e => e.textContent.trim()==='确定' && e.children.length===0 && e.offsetParent)[0];
              if (!btn) return 'no-btn';
              const r = btn.getBoundingClientRect();
              return JSON.stringify({x: r.x + r.width/2, y: r.y + r.height/2});
            })()`;
            const info = JSON.parse(await page.evaluate(js));
            log('[realclick] target', info);
            await page.mouse.move(info.x, info.y);
            await page.mouse.down();
            await new Promise((r) => setTimeout(r, 120));
            await page.mouse.up();
            log('[realclick] done');
          } catch (e) { log('[realclick err]', e.message.slice(0, 80)); }
        } else if (op === 'pwauto') {
          // 【优酷密码·已验证一条龙】真实点击聚焦 → 逐字符键盘输入 → 真实鼠标点确定
          // 关键坑（2026-09 实测）：
          //  1) 原生 setter(pwfill) 只改 DOM value，优酷 Vue 组件的 v-model 响应式数据
          //     不同步 → 点确定时提交空密码 → "密码错误"。必须用 keyboard.type 逐字符
          //     派发完整 keydown/keypress/input/keyup，Vue 才认。
          //  2) Enter 键对该弹窗无效（未绑定回车提交），必须真实鼠标点"确定"按钮。
          //  3) 真实鼠标坐标点击(page.mouse)最可靠，JS dispatchEvent 可能被前端拦截。
          const pwd = line.slice(7).trim();
          try {
            const handle = await page.$(PW_INPUT);
            if (!handle) { log('[pwauto] no-input（密码框不在 DOM）'); continue; }
            await handle.click({ clickCount: 3 }).catch(() => {});   // 聚焦+全选
            await page.keyboard.press('Backspace').catch(() => {});  // 清空残留
            await page.keyboard.type(pwd, { delay: 90 });
            const val = await page.evaluate((s) => {
              const el = document.querySelector(s); return el ? el.value : 'NOEL';
            }, PW_INPUT);
            log('[pwauto] typed, inputVal=', JSON.stringify(val));
            await page.screenshot({ path: path.join(ROOT, 'shots', 'pw_typed.png') }).catch(() => {});
            // 真实鼠标点击"确定"按钮（坐标取自 getBoundingClientRect，与 mouse 同坐标系）
            const coordJs = `(() => {
              const btn = [...document.querySelectorAll('*')]
                .find(e => e.textContent.trim() === '确定' && e.children.length === 0 && e.offsetParent);
              if (!btn) return null;
              const r = btn.getBoundingClientRect();
              return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
            })()`;
            const coord = await page.evaluate(coordJs);
            if (coord) {
              await page.mouse.move(coord.x, coord.y);
              await page.mouse.down();
              await new Promise((r) => setTimeout(r, 120));
              await page.mouse.up();
              log('[pwauto] clicked 确定 at', JSON.stringify(coord));
            } else {
              log('[pwauto] 未找到确定按钮，仅完成输入（可手动点确定）');
            }
          } catch (e) { log('[pwauto err]', e.message.slice(0, 100)); }
        } else if (op === 'ktype') {
          // 真实键盘逐字符输入（需先 click/focus 目标元素）
          const txt = line.slice(6).trim();
          try { await page.keyboard.type(txt, { delay: 90 }); log('[ktype]', JSON.stringify(txt)); }
          catch (e) { log('[ktype err]', e.message.slice(0, 80)); }
        } else if (op === 'press') {
          // 按键，如 Enter / Tab / Escape
          const key = line.slice(6).trim() || 'Enter';
          try { await page.keyboard.press(key); log('[press]', key); }
          catch (e) { log('[press err]', e.message.slice(0, 80)); }
        } else if (op === 'type') {
          const rest = line.slice(4).trim();
          const sp = rest.indexOf(' ');
          const sel = rest.slice(0, sp).trim();
          const txt = rest.slice(sp + 1).trim();
          try {
            await page.fill(sel, txt, { timeout: 5000 });
            log('[type ok]', sel);
          } catch (e) {
            for (const fr of page.frames()) {
              try { await fr.fill(sel, txt, { timeout: 3000 }); log('[type ok iframe]', fr.url().slice(0, 60)); break; } catch (e2) {}
            }
          }
        } else if (op === 'click') {
          try {
            await page.click(arg, { timeout: 5000 });
            log('[click ok]', arg);
          } catch (e) {
            for (const fr of page.frames()) {
              try { await fr.click(arg, { timeout: 3000 }); log('[click ok iframe]', fr.url().slice(0, 60)); break; } catch (e2) {}
            }
          }
        }
        await new Promise((r) => setTimeout(r, 600)).catch(() => {});
      }
    }
  } catch (e) { log('[cmd err]', e.message.slice(0, 100)); }

  if (fs.existsSync(STOP)) {
    clearInterval(t);
    log('收到停止信号，3 秒后关闭');
    setTimeout(async () => { try { await ctx.close(); } catch (e) {} process.exit(0); }, 3000);
  }
}, 700);

process.on('unhandledRejection', (e) => { log('[unhandled]', String(e).slice(0, 100)); });
ctx.on('close', () => { log('浏览器被关闭，退出'); process.exit(0); });
process.on('SIGINT', () => {});
process.on('SIGTERM', () => {});
