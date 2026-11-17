#!/usr/bin/env node
/*
 * make-preview.js — 把生成的皮肤 CSS 渲染成「WorkBuddy 界面预览」HTML
 * 用法:
 *   node make-preview.js --skin skins/dahua-classic.css --hero assets/dahua_scene.png --avatar-user assets/zhi_zun_bao.png --avatar-ai assets/zi_xia.png --name "大话西游经典" --out preview.html
 * 输出一个自包含 HTML（内联皮肤 CSS + 仿 WorkBuddy 布局 + 背景/头像 base64），双击即可看效果。
 */
const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const a = { skin: '', hero: '', avatarUser: '', avatarAi: '', name: '', out: '' };
  for (let i = 2; i < argv.length; i++) {
    const x = argv[i];
    if (x === '--skin') a.skin = argv[++i] || '';
    else if (x === '--hero') a.hero = argv[++i] || '';
    else if (x === '--avatar-user') a.avatarUser = argv[++i] || '';
    else if (x === '--avatar-ai') a.avatarAi = argv[++i] || '';
    else if (x === '--name') a.name = argv[++i] || '';
    else if (x === '--out') a.out = argv[++i] || '';
  }
  return a;
}

function toDataUri(filePath) {
  if (!filePath || !fs.existsSync(filePath)) return '';
  const ext = path.extname(filePath).toLowerCase().replace('.', '') || 'png';
  const b64 = fs.readFileSync(filePath).toString('base64');
  return `data:image/${ext === 'jpg' ? 'jpeg' : ext};base64,${b64}`;
}

function mockUi(name, avatarUserUri, avatarAiUri) {
  const userAvatar = avatarUserUri ? `<img class="wb-ava" src="${avatarUserUri}" alt="至尊宝">` : '';
  const aiAvatar = avatarAiUri ? `<img class="wb-ava" src="${avatarAiUri}" alt="紫霞">` : '';
  const us = (t) => `<div class="wb-msg user">${userAvatar}<div class="wb-bubble"><span class="wb-role">你</span><p>${t}</p></div></div>`;
  const ai = (t) => `<div class="wb-msg ai">${aiAvatar}<div class="wb-bubble"><span class="wb-role">WorkBuddy</span><p>${t}</p></div></div>`;
  return `<!-- 仿 WorkBuddy（VS Code 内核）布局，仅用于预览皮肤效果 -->
<div class="wb-win">
  <div class="wb-titlebar">
    <span class="wb-dots"><i></i><i></i><i></i></span>
    <span class="wb-title">WorkBuddy — ${name || '预览'}</span>
    <span class="wb-winctl">— ▢ ✕</span>
  </div>
  <div class="wb-body">
    <div class="wb-actbar">
      <div class="wb-act on">💬</div>
      <div class="wb-act">📁</div>
      <div class="wb-act">🔍</div>
      <div class="wb-act">🧩</div>
      <div class="wb-act wb-act-bot">⚙️</div>
    </div>
    <div class="wb-side">
      <div class="wb-side-h">对话</div>
      <div class="wb-conv active">大话西游经典界面</div>
      <div class="wb-conv">CDP 注入器改造</div>
      <div class="wb-conv">周报草稿</div>
      <div class="wb-conv">读书笔记 · 西游记</div>
      <div class="wb-conv-h">收藏</div>
      <div class="wb-conv">提示词模板</div>
    </div>
    <div class="wb-main">
      <div class="wb-tabs">
        <span class="wb-tab on">大话西游经典界面</span>
        <span class="wb-tab">main.js</span>
      </div>
      <div class="wb-chat">
        ${us('帮我生成《大话西游》经典界面皮肤')}
        ${ai('已生成「大话西游经典界面」——大漠落日、七彩祥云、至尊宝与紫霞仙子，画面作为背景，面板为毛玻璃。')}
        ${us('这就是我想要的，意境全有了！')}
        ${ai('应用会重启 WorkBuddy（单实例锁），请先保存当前对话，再运行 <code>apply-skin.ps1</code>。')}
      </div>
      <div class="wb-input">
        <input class="wb-text" placeholder="输入消息，Enter 发送…" />
        <button class="wb-send">发送</button>
      </div>
    </div>
  </div>
  <div class="wb-status">
    <span>● 已连接</span><span>皮肤: ${name || '预览'}</span><span>UTF-8</span><span>☁ 已同步</span>
  </div>
</div>`;
}

function layoutCss() {
  return `
* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; overflow: hidden; }
body { font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif; }
.wb-win{height:100vh;width:100vw;display:flex;flex-direction:column;overflow:hidden;
  box-shadow:0 20px 60px rgba(0,0,0,.45);border:1px solid var(--vscode-contrastBorder);}
.wb-titlebar{height:34px;display:flex;align-items:center;gap:12px;padding:0 12px;
  background:var(--vscode-titleBar-activeBackground);color:var(--vscode-titleBar-activeForeground);font-size:13px;}
.wb-dots{display:flex;gap:6px}.wb-dots i{width:11px;height:11px;border-radius:50%;background:#ff5f57}
.wb-dots i:nth-child(2){background:#febc2e}.wb-dots i:nth-child(3){background:#28c840}
.wb-title{flex:1;text-align:center;opacity:.9}
.wb-winctl{opacity:.55;letter-spacing:2px}
.wb-body{flex:1;display:flex;min-height:0}
.wb-actbar{width:52px;background:var(--vscode-activityBar-background);display:flex;flex-direction:column;
  align-items:center;padding:10px 0;gap:8px}
.wb-act{width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:18px;
  border-radius:8px;color:var(--vscode-activityBar-inactiveForeground);cursor:pointer}
.wb-act.on{color:var(--vscode-activityBar-foreground);background:rgba(255,255,255,.06);
  box-shadow:inset 2px 0 0 var(--vscode-activityBar-foreground)}
.wb-act-bot{margin-top:auto}
.wb-side{width:220px;background:var(--vscode-sideBar-background);color:var(--vscode-sideBar-foreground);
  padding:10px 8px;overflow:auto;font-size:13px}
.wb-side-h{color:var(--vscode-sideBarTitle-foreground);font-weight:600;padding:6px 8px;font-size:12px;
  letter-spacing:1px}
.wb-conv{padding:7px 10px;border-radius:7px;margin:2px 0;cursor:pointer;opacity:.85}
.wb-conv:hover{background:var(--vscode-list-hoverBackground)}
.wb-conv.active{background:var(--vscode-list-activeSelectionBackground);color:var(--vscode-list-activeSelectionForeground);opacity:1}
.wb-conv-h{color:var(--vscode-descriptionForeground);font-size:11px;padding:12px 8px 4px;letter-spacing:1px}
.wb-main{flex:1;display:flex;flex-direction:column;min-width:0;background:var(--vscode-editor-background);position:relative}
.wb-tabs{display:flex;background:var(--vscode-editorGroupHeader-tabsBackground);
  border-bottom:1px solid var(--vscode-editorGroupHeader-tabsBorder);position:relative;z-index:1}
.wb-tab{padding:9px 16px;font-size:12px;color:var(--vscode-tab-inactiveForeground);cursor:pointer}
.wb-tab.on{background:var(--vscode-tab-activeBackground);color:var(--vscode-tab-activeForeground);
  border-right:1px solid var(--vscode-tab-border)}
.wb-chat{flex:1;overflow:auto;padding:18px;display:flex;flex-direction:column;gap:14px;position:relative;z-index:1}
.wb-msg{display:flex;gap:9px;align-items:flex-start;max-width:82%;font-size:13px;line-height:1.6;
  color:var(--vscode-editor-foreground);}
.wb-bubble{flex:1;min-width:0;padding:10px 14px;border-radius:12px;
  background:var(--vscode-editorWidget-background);color:var(--vscode-editorWidget-foreground);
  border:1px solid var(--vscode-editorWidget-border);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);}
.wb-ava{width:34px;height:34px;border-radius:50%;object-fit:cover;flex-shrink:0;
  border:2px solid var(--vscode-editorWidget-border);box-shadow:0 4px 12px rgba(0,0,0,.35);margin-top:2px}
.wb-msg.user{align-self:flex-end;flex-direction:row-reverse;}
.wb-msg.user .wb-bubble{background:var(--vscode-button-background);color:var(--vscode-button-foreground);border:none;}
.wb-role{display:block;font-size:11px;opacity:.7;margin-bottom:3px}
.wb-msg code{background:rgba(255,255,255,.12);padding:1px 5px;border-radius:4px;font-size:12px}
.wb-input{display:flex;gap:8px;padding:12px;border-top:1px solid var(--vscode-panel-border);
  background:var(--vscode-panel-background);position:relative;z-index:1}
.wb-text{flex:1;padding:9px 12px;border-radius:8px;font-size:13px;
  background:var(--vscode-input-background);color:var(--vscode-input-foreground);
  border:1px solid var(--vscode-input-border);outline:none;backdrop-filter:blur(6px);}
.wb-text::placeholder{color:var(--vscode-input-placeholderForeground)}
.wb-send{padding:0 18px;border:none;border-radius:8px;cursor:pointer;font-size:13px;
  background:var(--vscode-button-background);color:var(--vscode-button-foreground);transition:transform .15s,box-shadow .15s,filter .15s;}
.wb-send:hover{background:var(--vscode-button-hoverBackground);transform:translateY(-1px);box-shadow:0 6px 18px rgba(232,184,109,.35);filter:brightness(1.08);}
.wb-status{height:24px;display:flex;align-items:center;gap:18px;padding:0 14px;font-size:11px;
  background:var(--vscode-statusBar-background);color:var(--vscode-statusBar-foreground)}
`;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.skin) { console.error('缺少 --skin <css 路径>'); process.exit(2); }
  const css = fs.readFileSync(args.skin, 'utf8');
  const name = args.name || path.basename(args.skin, '.css');
  const out = args.out || path.resolve(path.dirname(args.skin), 'preview.html');

  const heroUri = args.hero ? toDataUri(args.hero) : '';
  const avatarUserUri = args.avatarUser ? toDataUri(args.avatarUser) : '';
  const avatarAiUri = args.avatarAi ? toDataUri(args.avatarAi) : '';

  let heroOverride = '';
  if (heroUri) {
    // 让预览自包含：用 base64 场景图覆盖皮肤 CSS 中的 file:// 路径
    heroOverride = `
body::before {
  background-image: linear-gradient(180deg, rgba(60, 25, 60, 0.25) 0%, rgba(12, 5, 20, 0.55) 100%),
    url("${heroUri}") !important;
}`;
  }

  const html = `<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WorkBuddy 皮肤预览 · ${name}</title>
<style>${css}</style>
<style>${heroOverride}</style>
<style>${layoutCss()}</style>
</head><body>
${mockUi(name, avatarUserUri, avatarAiUri)}
</body></html>`;
  fs.writeFileSync(out, html, 'utf8');
  console.log('✔ 预览已生成 → ' + out + (heroUri ? '（含背景+头像）' : ''));
}
main();
