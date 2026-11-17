"""接入向导的页面模板（HTML）。放在 .py 里，是因为部分技能市场不接受 .tmpl/.html 之类的资源后缀。
__TOKEN__ / __POLICY__ / <!--BRAND:xxx--> 由 setup.py 在运行时替换。
这里只有页面结构和本页脚本，不含任何品牌内容（品牌在 assets/brand.json，可选）。"""

PAGE = r"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>连接腾讯云 · 首次设置</title>
<link rel="icon" href="data:image/png;base64,__LOGO__">
<style>
:root{
  --bg:#FDF8F3;--paper:#F7F1E6;--subtle:#F2EDE3;--card:#FFFFFF;
  --border:#E5DFD4;--border-light:#EFE9DE;
  --text:#111827;--text-mid:#4B5563;--muted:#8A8577;
  --orange:#F25C2A;--sienna:#B84C20;--sienna-pale:#FDF0EA;
  --green:#1E3D2F;--green-mid:#2E5D45;--green-pale:#EAF3EE;
  --gold:linear-gradient(100deg,#E4B454,#FCB46C);
  --r-btn:4px;--r-card:8px;
  --shadow:0 2px 12px rgba(33,24,16,.06),0 1px 3px rgba(33,24,16,.04);
  --serif:"Noto Serif SC","Songti SC","STSong","SimSun",serif;
  --sans:"Noto Sans SC","PingFang SC","Microsoft YaHei",-apple-system,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);line-height:1.75;font-size:15px}
a{color:var(--sienna)}
code{background:var(--subtle);padding:1px 6px;border-radius:3px;font-size:14px}

/* 顶栏 */
.top{background:var(--green);color:#fff}
.top .in{max-width:1080px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:12px}
.top img{width:32px;height:32px;border-radius:6px}
.top .brand{font-family:var(--serif);font-weight:700;font-size:17px;letter-spacing:.5px}
.top .brand small{font-family:var(--sans);font-weight:400;opacity:.7;font-size:13px;margin-left:6px}
.top .badge{margin-left:auto;font-size:12px;padding:3px 10px;border-radius:999px;background:var(--gold);color:#3b2a0a;font-weight:600;white-space:nowrap}

/* 布局 */
.wrap{max-width:820px;margin:0 auto;padding:28px 20px 40px;display:grid;grid-template-columns:minmax(0,1fr);gap:28px}
@media(max-width:900px){.wrap{grid-template-columns:1fr}.side{order:2}}

/* Hero */
.hero h1{font-family:var(--serif);font-size:30px;line-height:1.35;margin:0 0 8px}
.hero h1 em{font-style:normal;color:var(--orange)}
.hero p{color:var(--text-mid);margin:0 0 20px}
.meta{display:flex;gap:16px;flex-wrap:wrap;color:var(--muted);font-size:13px;margin-bottom:22px}

/* 卡片 */
.card{background:var(--card);border:1px solid var(--border-light);border-radius:var(--r-card);box-shadow:var(--shadow);padding:20px 22px;margin-bottom:18px}
.trust{background:var(--green-pale);border-color:#D5E6DC}
.trust h3{font-family:var(--serif);margin:0 0 8px;font-size:17px;color:var(--green)}
.trust ul{margin:0;padding-left:0;list-style:none}
.trust li{margin:6px 0;padding-left:26px;position:relative}
.trust li::before{position:absolute;left:0}
.trust .y::before{content:"✓";color:var(--green-mid);font-weight:700}
.trust .n::before{content:"✕";color:var(--sienna);font-weight:700}
.trust .k::before{content:"🔑"} .trust .r::before{content:"🧯"} .trust .a::before{content:"📋"} .trust .w::before{content:"⚠️"}
.trust .n{color:var(--sienna)}

.step{display:grid;grid-template-columns:44px 1fr;gap:14px}
.num{width:40px;height:40px;border-radius:50%;background:var(--orange);color:#fff;font-family:var(--serif);font-weight:700;font-size:18px;display:flex;align-items:center;justify-content:center}
.step h2{font-family:var(--serif);font-size:19px;margin:6px 0 10px}
.step ol{padding-left:20px;margin:10px 0}
.step li{margin:4px 0}
.hl{font-weight:600}
.no{color:var(--sienna);font-weight:600}
.tip{color:var(--muted);font-size:13.5px}

/* 按钮 */
.btn,button{display:inline-flex;align-items:center;gap:6px;background:var(--green);color:#fff;border:0;border-radius:var(--r-btn);padding:9px 18px;margin:4px 8px 4px 0;text-decoration:none;font-size:14.5px;font-family:var(--sans);cursor:pointer;transition:background .15s}
.btn:hover,button:hover{background:var(--green-mid)}
button.sec{background:var(--paper);color:var(--green);border:1px solid var(--border)}
button.sec:hover{background:var(--subtle)}
button.primary{background:var(--orange);font-weight:600;padding:11px 26px;font-size:15.5px}
button.primary:hover{background:var(--sienna)}
button:disabled{opacity:.6;cursor:wait}

details summary{cursor:pointer}
textarea{width:100%;height:120px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;border:1px solid var(--border);border-radius:var(--r-btn);background:var(--paper);padding:8px;margin-top:8px}
label{font-weight:600;font-size:14px;display:block;margin-top:6px}
input{width:100%;padding:10px 12px;font-size:15px;border:1px solid var(--border);border-radius:var(--r-btn);background:#fff;margin:4px 0 12px;font-family:ui-monospace,Menlo,Consolas,monospace}
input:focus{outline:2px solid var(--orange);outline-offset:-1px;border-color:transparent}
.secure{display:flex;gap:8px;align-items:center;background:var(--paper);border-radius:var(--r-btn);padding:8px 12px;font-size:13px;color:var(--text-mid);margin-bottom:12px}

#msg{padding:12px 14px;border-radius:var(--r-btn);display:none;white-space:pre-wrap;margin-top:12px}
#msg.ok{background:var(--green-pale);color:var(--green)} #msg.err{background:var(--sienna-pale);color:var(--sienna)}

/* 完成卡片 */
#done{display:none;background:var(--green);color:#fff;border:0}
#done h2{font-family:var(--serif);font-size:22px;margin:0 0 6px}
#done p{color:rgba(255,255,255,.82);margin:0 0 14px}
#done .row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0 18px}
@media(max-width:640px){#done .row{grid-template-columns:1fr}}
#done .it{background:rgba(255,255,255,.08);border-radius:var(--r-card);padding:12px}
#done .it b{display:block;font-family:var(--serif);font-size:15px}
#done .it span{font-size:13px;color:rgba(255,255,255,.72)}
#done .btn{background:var(--orange);font-weight:600}
#done .btn:hover{background:var(--sienna)}
#done .btn.ghost{background:transparent;border:1px solid rgba(255,255,255,.35)}

/* 侧栏 */
.side .card{position:relative}
.side .sticky{position:sticky;top:20px}
.side h3{font-family:var(--serif);font-size:17px;margin:0 0 4px}
.side .kicker{font-size:12px;color:var(--orange);font-weight:700;letter-spacing:1px}
.side p{color:var(--text-mid);font-size:14px;margin:6px 0 12px}
.side ul{list-style:none;padding:0;margin:0 0 14px}
.side li{font-size:14px;padding:7px 0;border-top:1px dashed var(--border)}
.side li b{color:var(--text)}
.side li span{color:var(--muted);font-size:12.5px;display:block}
.side .btn{width:100%;justify-content:center;background:var(--orange);font-weight:600}
.side .btn:hover{background:var(--sienna)}
.side .mk{font-size:13px;color:var(--text-mid)}
.side .mk a{display:inline-block;margin:2px 8px 2px 0}
.adtag{position:absolute;top:10px;right:12px;font-size:11px;color:var(--muted);border:1px solid var(--border);border-radius:3px;padding:0 5px}

footer{border-top:1px solid var(--border);color:var(--muted);font-size:13px}
footer .in{max-width:1080px;margin:0 auto;padding:18px 20px;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}
footer img{width:20px;height:20px;border-radius:4px;vertical-align:-4px;margin-right:6px}
footer a{color:var(--text-mid);text-decoration:none} footer a:hover{color:var(--orange)}
</style></head><body>

<!--BRAND:header-->

<div class="wrap">
<main>
  <section class="hero">
    <h1>把你的 AI 助手接入<em>腾讯云</em></h1>
    <p>四步完成，约 5 分钟，只需要做一次。之后部署网站、配域名、开证书、加速国内访问，都交给 AI 助手。</p>
    <div class="meta"><span>🖥️ 页面运行在你自己的电脑上（127.0.0.1）</span><span>🔒 只有你能看到</span><span>⏱ 约 5 分钟</span></div>
  </section>

  <div class="card trust">
    <h3>先说清楚：AI 助手会拿到什么权限</h3>
    <ul>
      <li class="y">能做：配置域名解析、网站加速和免费证书、管理你已有的服务器（开端口、部署网站、执行命令）</li>
      <li class="n">做不了（腾讯云会直接拒绝）：花钱（买服务器、续费、买域名）、删除或重装服务器、删除或转让域名、查看余额、查看你的实名资料</li>
      <li class="k">你填的密钥只保存在这台电脑上，不会发给 AI 对话，也不会发给技能出品方</li>
      <li class="r">随时可以收回：腾讯云控制台 → 访问管理 → 用户列表 → agent-ops → 禁用，立即生效</li>
      <li class="a">它的每次操作都会记在腾讯云「<a href="https://console.cloud.tencent.com/cloudaudit" target="_blank" rel="noopener">操作审计</a>」里</li>
      <li class="w">需要说明：为了部署网站，它能在你的服务器上以管理员（root）身份执行命令。请只把要交给它管理的服务器放在这个账号里。</li>
    </ul>
  </div>

  <div class="card step"><div class="num">1</div><div>
    <h2>有腾讯云账号吗？</h2>
    <p>已经有、并且完成了实名认证 → 直接跳到第 2 步。还没有：</p>
    <a class="btn" href="https://cloud.tencent.com/register" target="_blank" rel="noopener">① 注册腾讯云</a>
    <a class="btn" href="https://console.cloud.tencent.com/developer/auth" target="_blank" rel="noopener">② 实名认证</a>
    <p class="tip">注册：可以用微信扫码，也可以用邮箱或 QQ，需要一个中国大陆手机号（+86）。<br>
    实名认证：个人选「微信扫码」或「人脸识别」，几分钟就能完成；需要开公司发票就选企业认证。不实名就买不了任何云服务。</p>
  </div></div>

  <div class="card step"><div class="num">2</div><div>
    <h2>创建权限策略（规定 AI 助手能做什么）</h2>
    <a class="btn" href="https://console.cloud.tencent.com/cam/policy" target="_blank" rel="noopener">打开「策略」页面</a>
    <button class="sec" onclick="copyPolicy()">📋 复制策略内容</button> <span id="copied" class="tip"></span>
    <ol>
      <li>在打开的页面上，点 <span class="hl">「新建自定义策略」</span> → <span class="hl">「按策略语法创建」</span> → 选 <span class="hl">「空白模板」</span> → 下一步</li>
      <li>策略名称填：<code>agent-ops-web</code></li>
      <li>把「策略内容」框里原有的文字<b>全部删掉</b>，粘贴刚才复制的内容 → 点「完成」</li>
    </ol>
    <details><summary class="tip">查看策略内容（不需要看懂）</summary><textarea id="policy" readonly>__POLICY__</textarea></details>
  </div></div>

  <div class="card step"><div class="num">3</div><div>
    <h2>创建 AI 助手专用的子账号</h2>
    <a class="btn" href="https://console.cloud.tencent.com/cam" target="_blank" rel="noopener">打开「用户列表」页面</a>
    <ol>
      <li>点 <span class="hl">「新建用户」</span> → 选 <span class="hl">「自定义创建」</span> → 选 <span class="hl">「可访问资源并接收消息」</span> → 下一步</li>
      <li>用户名填：<code>agent-ops</code></li>
      <li>访问方式：<b>只勾「编程访问」</b>，<span class="no">不要勾「腾讯云控制台访问」</span> → 下一步</li>
      <li>设置权限：在搜索框输入 <code>agent-ops-web</code>，勾选它。<span class="no">不要勾 AdministratorAccess 或其他任何策略</span> → 下一步 → 完成</li>
      <li>最后一页会显示 <b>SecretId</b> 和 <b>SecretKey</b>（只显示这一次），把它们分别复制到下面：</li>
    </ol>
  </div></div>

  <div class="card step"><div class="num">4</div><div>
    <h2>把密钥交给 AI 助手</h2>
    <div class="secure">🔒 密钥只会发到你这台电脑上的设置程序，验证通过后保存在本机，页面随后自动关闭。</div>
    <label for="sid">SecretId（以 AKID 开头）</label><input id="sid" autocomplete="off" spellcheck="false">
    <label for="skey">SecretKey</label><input id="skey" type="password" autocomplete="off" spellcheck="false">
    <button class="primary" onclick="save()" id="savebtn">保存并验证</button>
    <div id="msg"></div>
  </div></div>

  <div class="card" id="done">
    <h2>🎉 接入完成</h2>
    <p>现在可以关掉这个页面，回到 AI 助手那里，告诉它你想上线什么网站。</p>
    <!--BRAND:done-->
  </div>
</main>

</div>

<!--BRAND:footer-->

<script>
const T="__TOKEN__";
function copyPolicy(){const t=document.getElementById('policy');
 (navigator.clipboard?navigator.clipboard.writeText(t.value):Promise.reject()).catch(()=>{t.parentElement.open=true;t.select();document.execCommand('copy')})
 .finally(()=>{document.getElementById('copied').textContent='已复制，去腾讯云页面粘贴'})}
async function save(){const m=document.getElementById('msg'),b=document.getElementById('savebtn');
 b.disabled=true;b.textContent='验证中…';m.style.display='none';
 try{const r=await fetch('/save?t='+T,{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({sid:document.getElementById('sid').value,skey:document.getElementById('skey').value})});
  const d=await r.json();m.className=d.ok?'ok':'err';m.textContent=d.text;m.style.display='block';
  if(d.ok){document.getElementById('skey').value='';b.textContent='已完成';
   const done=document.getElementById('done');if(done){done.style.display='block';done.scrollIntoView({behavior:'smooth',block:'center'})}return}
 }catch(e){m.className='err';m.textContent='页面和本机程序断开了，请回到 AI 助手那里，让它重新打开这个页面。';m.style.display='block'}
 b.disabled=false;b.textContent='保存并验证'}
</script></body></html>
"""
