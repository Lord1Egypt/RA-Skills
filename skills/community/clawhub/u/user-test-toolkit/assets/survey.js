/**
 * survey.js — 用户 情境嵌入式用户测试引擎 v1
 *
 * ⚠️ 加载顺序（重要）：
 *   1. tracker-config.js
 *   2. tracker.js
 *   3. survey-config.js（必须在本文件之前引入）
 *   4. 本文件
 *
 * 依赖：tracker.js（UserTestTracker.record）
 * 触发：URL 含 mode=test 参数时激活
 */
(function(global){
'use strict';
var params=new URLSearchParams(location.search);
var testMode=params.get('smode')||params.get('mode'),testRound=params.get('test')||'default',uid=params.get('uid')||'';
if(testMode!=='test'||!uid)return;

// ===== URL 配置开关（由测试中心生成） =====
var cfgType=params.get('stype')||''; // internal / user
var cfgTasks=params.get('stasks')!=='0'; // 任务面板开关（默认开）
var cfgSurveys=params.get('ssurveys')!=='0'; // 情境问卷开关（默认开）
var cfgExit=params.get('sexit')!=='0'; // 总结问卷开关（默认开）
var cfgWelcome=params.get('swelcome')!=='0'; // 欢迎页开关（默认开）
var cfgCPs=params.get('scp')?params.get('scp').split(','):[]; // 启用的情境问卷节点

// ===== 配置 =====
var TASKS_INTERNAL=[
{id:'T1',label:'把一个视频翻译成英文',hint:'用你觉得合适的方式完成',detect:'mps_complete'},
{id:'T2',label:'对翻译结果做一些修改',hint:'比如改条字幕、调个区域',detect:'finetune_edit'},
{id:'T3',label:'把最终结果导出',hint:'下载你满意的版本',detect:'export'}
];
var TASKS_USER=[
{id:'T1',label:'把这个视频翻译成中文',hint:'',detect:'mps_complete'},
{id:'T2',label:'下载翻译好的视频',hint:'',detect:'export'}
];
var CP_INTERNAL=[
{id:'upload_ease',trigger:'upload_done',delay:1500,type:'rating',question:'刚才找到上传入口顺利吗？',scale:5,labels:['很困难','有点绕','还行','比较顺','一下就找到了'],allowComment:true,commentPH:'在哪卡住过？（可选）'},
{id:'wait_sam',trigger:'processing_wait_30s',delay:500,type:'sam',question:'等 AI 处理的这段时间感觉怎样？',dims:[{id:'arousal',label:'紧张程度',l:'很放松',r:'很焦虑'},{id:'valence',label:'心情',l:'不太好',r:'挺好的'}]},
{id:'result_sam',trigger:'view_result',delay:3000,type:'sam',question:'看到 AI 处理的结果，感觉如何？',dims:[{id:'valence',label:'满意程度',l:'不满意',r:'很满意'},{id:'dominance',label:'掌控感',l:'不知道怎么调',r:'我知道怎么改'}]},
{id:'finetune_ease',trigger:'finetune_edit',delay:1500,type:'rating',question:'刚才修改结果的操作顺利吗？',scale:5,labels:['完全不会','有点绕','还行','比较顺','很容易'],allowComment:true,commentPH:'哪个操作让你卡住了？（可选）'}
];
var CP_USER=[
{id:'upload_ease',trigger:'upload_done',delay:2000,type:'rating',question:'上传视频顺利吗？',scale:5,labels:['很困难','有点绕','还行','比较顺','一下就找到了'],allowComment:false},
{id:'result_quality',trigger:'view_result',delay:3000,type:'rating',question:'翻译的效果你满意吗？',scale:5,labels:['很不满意','不太行','一般','还不错','很满意'],allowComment:true,commentPH:'哪里满意/不满意？'}
];
var isInternal=cfgType==='user'?false:(cfgType==='internal'?true:!(testRound.includes('user')||testRound.includes('external')));
var tasks=isInternal?TASKS_INTERNAL:TASKS_USER;
var checkpoints=isInternal?CP_INTERNAL:CP_USER;
var guidedMode=isInternal;
var pn=(global.SURVEY_CONFIG||{}).productName||'本产品';

// SUS 标准10题
var SUS_Q=[
'我认为我会经常使用 ' + pn + '','我觉得 ' + pn + ' 不必要地复杂','我认为 ' + pn + ' 很容易使用',
'我认为我需要技术人员的支持才能使用 ' + pn + '','我觉得 ' + pn + ' 的各项功能整合得很好',
'我觉得 ' + pn + ' 有太多不一致的地方','我认为大多数人都能很快学会使用 ' + pn + '',
'我觉得 ' + pn + ' 用起来很麻烦','我使用 ' + pn + ' 时感到很有信心','我需要学很多东西才能使用 ' + pn + ''
];
// 情绪价值量表
var EV_Q=[
'使用过程让我感到愉悦','等待 AI 处理时我不觉得无聊','看到成片效果让我惊喜',
'' + pn + ' 让我觉得视频翻译不再困难','整个过程让我有掌控感','我愿意向朋友展示 ' + pn + ' 的成果',
'' + pn + ' 的界面让我感到专业和可信','处理过程中的角色让体验更有趣','整体体验超出了我的预期'
];

// 根据 URL 配置过滤情境问卷
if(!cfgSurveys){checkpoints=[]}
else if(cfgCPs.length>0){checkpoints=checkpoints.filter(function(cp){return cfgCPs.indexOf(cp.id)!==-1})}

// ===== 状态 =====
var STORAGE_KEY='sv_state_'+uid;
var taskIdx=0,taskStates=tasks.map(function(){return'pending'}),answered={},exitShown=false,startTs=Date.now(),procStart=0,procTimerDone=false;

// 从 sessionStorage 恢复状态（跨页面）
try{
var saved=JSON.parse(sessionStorage.getItem(STORAGE_KEY)||'null');
if(saved){
if(saved.taskStates&&saved.taskStates.length===tasks.length)taskStates=saved.taskStates;
if(saved.answered)answered=saved.answered;
if(saved.startTs)startTs=saved.startTs;
if(saved.exitShown)exitShown=saved.exitShown;
// 计算 taskIdx
taskIdx=0;for(var ri=0;ri<taskStates.length;ri++){if(taskStates[ri]==='done')taskIdx=ri+1;}
if(taskIdx>=tasks.length)taskIdx=tasks.length-1;
}
}catch(e){}

function saveState(){
try{sessionStorage.setItem(STORAGE_KEY,JSON.stringify({taskStates:taskStates,answered:answered,startTs:startTs,exitShown:exitShown}))}catch(e){}
}

// ===== 注入CSS =====
var css=document.createElement('style');
css.textContent='\
.sv-overlay{position:fixed;inset:0;z-index:10000;background:rgba(255,255,255,.85);backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;animation:svF .4s}\
.sv-card{width:90%;max-width:480px;background:#fff;border:1px solid #e2e8f0;border-radius:20px;padding:36px 32px 28px;text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.1);animation:svU .5s}\
.sv-card h2{font-size:1.3rem;font-weight:800;color:#1e293b;margin:0 0 6px}\
.sv-card .sv-sub{font-size:.82rem;color:#64748b;line-height:1.6;margin-bottom:20px}\
.sv-card .sv-note{font-size:.72rem;color:#64748b;background:#f8fafc;border:1px solid #f1f5f9;border-radius:10px;padding:10px 14px;margin-bottom:20px;line-height:1.6}\
.sv-btn{padding:12px 36px;border-radius:12px;border:none;background:linear-gradient(135deg,#818cf8,#6366f1);color:#fff;font-size:.9rem;font-weight:700;cursor:pointer;font-family:inherit;box-shadow:0 4px 20px rgba(99,102,241,.25);transition:all .2s}\
.sv-btn:hover{filter:brightness(1.05);transform:translateY(-1px)}\
.sv-tp{position:fixed;top:16px;right:16px;z-index:9990;width:280px;background:#fff;border:1px solid #e2e8f0;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,.08);overflow:hidden;animation:svR .4s;transition:all .3s ease}\
.sv-tp.min{width:auto;max-width:280px;border-radius:28px;cursor:pointer;background:linear-gradient(135deg,#4f46e5,#6366f1);border:none;box-shadow:0 4px 24px rgba(99,102,241,.3),0 0 0 0 rgba(99,102,241,.2);position:fixed;bottom:24px;right:24px;top:auto;animation:svBounce .5s ease,svGlow 2s ease-in-out infinite}\
.sv-tp.min .sv-tp-b{display:none}\
.sv-tp.min .sv-tp-h{border-bottom:none;padding:11px 18px 11px 14px;border-radius:28px;background:none}\
.sv-tp.min:hover{transform:translateY(-3px);box-shadow:0 6px 32px rgba(99,102,241,.4)}\
.sv-tp.min .sv-tp-x{display:none}\
.sv-tp.min .sv-tp-p{color:rgba(255,255,255,.8)}\
.sv-tp.min .sv-fab-txt{color:#fff}\
.sv-tp.min .sv-fab-num{color:#fff}\
.sv-tp.min .sv-fab-ring{border-color:rgba(255,255,255,.3)}\
.sv-tp.min .sv-fab-ring svg circle{stroke:#fff}\
@keyframes svBounce{0%{transform:scale(.8);opacity:0}60%{transform:scale(1.05)}100%{transform:scale(1);opacity:1}}\
@keyframes svGlow{0%,100%{box-shadow:0 4px 24px rgba(99,102,241,.3),0 0 0 0 rgba(99,102,241,.1)}50%{box-shadow:0 4px 24px rgba(99,102,241,.3),0 0 0 8px rgba(99,102,241,.06)}}\
.sv-fab{display:none;align-items:center;gap:8px;font-size:.72rem;color:#a5b4fc;white-space:nowrap}\
.sv-tp.min .sv-fab{display:flex}\
.sv-tp.min .sv-tp-t>span:first-child{display:none}\
.sv-fab-ring{width:28px;height:28px;border-radius:50%;border:2.5px solid #e2e8f0;display:flex;align-items:center;justify-content:center;position:relative;flex-shrink:0}\
.sv-fab-ring svg{position:absolute;inset:-3px;transform:rotate(-90deg)}\
.sv-fab-ring svg circle{fill:none;stroke:#6366f1;stroke-width:2.5;stroke-linecap:round;transition:stroke-dashoffset .5s ease}\
.sv-fab-num{font-size:.65rem;font-weight:800;color:#6366f1}\
.sv-fab-txt{overflow:hidden;text-overflow:ellipsis;font-weight:500;color:#475569}\
.sv-tp-h{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid #f1f5f9;background:#fafbfc}\
.sv-tp-t{font-size:.78rem;font-weight:700;color:#1e293b;display:flex;align-items:center;gap:8px}\
.sv-tp-p{font-size:.65rem;color:#6366f1;font-weight:600}\
.sv-tp-x{width:26px;height:26px;border-radius:7px;border:none;background:#f1f5f9;color:#94a3b8;font-size:.75rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s}\
.sv-tp-x:hover{background:#e2e8f0;color:#475569}\
.sv-tp-b{padding:12px 16px 14px}\
.sv-timer{font-size:.65rem;color:#94a3b8;text-align:center;padding-top:10px;border-top:1px solid #f1f5f9;margin-top:10px}\
.sv-mo{position:fixed;bottom:24px;right:24px;z-index:10001;width:340px;background:#fff;border:1px solid #e2e8f0;border-radius:18px;padding:22px 24px 18px;box-shadow:0 12px 48px rgba(0,0,0,.1);animation:svU .35s}\
.sv-mo-q{font-size:.88rem;font-weight:700;color:#1e293b;margin-bottom:16px;line-height:1.4}\
.sv-mo-sk{position:absolute;top:12px;right:14px;font-size:.65rem;color:#94a3b8;cursor:pointer;border:none;background:none;font-family:inherit}\
.sv-mo-sk:hover{color:#475569}\
.sv-rr{display:flex;gap:6px;justify-content:center;margin-bottom:10px}\
.sv-rs{width:44px;height:44px;border-radius:12px;border:1px solid #e2e8f0;background:#fafbfc;color:#94a3b8;font-size:.82rem;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;font-family:inherit}\
.sv-rs:hover,.sv-rs.on{background:rgba(245,158,11,.1);border-color:#f59e0b;color:#d97706}\
.sv-rl{display:flex;justify-content:space-between;font-size:.6rem;color:#94a3b8;margin-bottom:12px;padding:0 2px}\
.sv-ci{width:100%;padding:9px 12px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0;color:#1e293b;font-size:.76rem;font-family:inherit;resize:none;outline:none}\
.sv-ci:focus{border-color:#818cf8}\
.sv-mo-sub{margin-top:12px;width:100%;padding:10px;border-radius:10px;border:none;background:linear-gradient(135deg,#818cf8,#6366f1);color:#fff;font-size:.8rem;font-weight:600;cursor:pointer;font-family:inherit;opacity:.4;pointer-events:none;transition:all .2s}\
.sv-mo-sub.rdy{opacity:1;pointer-events:auto}.sv-mo-sub.rdy:hover{filter:brightness(1.05)}\
.sv-sam-d{margin-bottom:16px}\
.sv-sam-l{font-size:.72rem;font-weight:600;color:#64748b;margin-bottom:8px;text-align:center}\
.sv-sam-w{display:flex;align-items:center;gap:10px}\
.sv-sam-e{font-size:.6rem;color:#94a3b8;min-width:44px;text-align:center}\
.sv-sam-s{flex:1;-webkit-appearance:none;appearance:none;height:6px;border-radius:3px;background:#e2e8f0;outline:none}\
.sv-sam-s::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:#6366f1;cursor:pointer;box-shadow:0 2px 8px rgba(99,102,241,.3)}\
.sv-sam-v{font-size:.7rem;color:#6366f1;font-weight:700;min-width:20px;text-align:center}\
.sv-exit{position:fixed;inset:0;z-index:10002;background:rgba(255,255,255,.9);backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;animation:svF .4s}\
.sv-exit-c{width:92%;max-width:600px;max-height:85vh;background:#fff;border:1px solid #e2e8f0;border-radius:20px;overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,.1);animation:svU .5s}\
.sv-exit-h{padding:24px 28px 16px;border-bottom:1px solid #f1f5f9;position:sticky;top:0;background:#fff;z-index:1}\
.sv-exit-h h2{font-size:1.1rem;font-weight:800;color:#1e293b;margin:0 0 4px}\
.sv-exit-h p{font-size:.75rem;color:#94a3b8}\
.sv-exit-b{padding:20px 28px 28px}\
.sv-sec{margin-bottom:28px}\
.sv-sec-t{font-size:.82rem;font-weight:700;color:#1e293b;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;gap:8px}\
.sv-sec-tag{font-size:.58rem;color:#6366f1;background:rgba(99,102,241,.08);padding:2px 7px;border-radius:5px;font-weight:600}\
.sv-sq{margin-bottom:14px}\
.sv-sq-t{font-size:.76rem;color:#475569;margin-bottom:8px;line-height:1.5}\
.sv-sq-s{display:flex;gap:4px;align-items:center}\
.sv-sq-e{font-size:.6rem;color:#94a3b8;min-width:50px}.sv-sq-e:last-child{text-align:right}\
.sv-sq-o{flex:1;height:36px;border-radius:8px;border:1px solid #e2e8f0;background:#fafbfc;color:#64748b;font-size:.72rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:inherit}\
.sv-sq-o:hover{background:rgba(99,102,241,.06);border-color:rgba(99,102,241,.2)}\
.sv-sq-o.sel{background:rgba(99,102,241,.1);border-color:#818cf8;color:#4f46e5}\
.sv-nps-r{display:flex;gap:3px;margin-bottom:6px}\
.sv-nps-b{flex:1;height:38px;border-radius:8px;border:1px solid #e2e8f0;background:#fafbfc;color:#64748b;font-size:.78rem;font-weight:700;cursor:pointer;transition:all .2s;font-family:inherit}\
.sv-nps-b:hover{background:#f1f5f9}\
.sv-nps-b.sel{color:#fff}\
.sv-nps-b.sel.nl{background:#ef4444;border-color:#ef4444}\
.sv-nps-b.sel.nm{background:#f59e0b;border-color:#f59e0b}\
.sv-nps-b.sel.nh{background:#10b981;border-color:#10b981}\
.sv-nps-l{display:flex;justify-content:space-between;font-size:.58rem;color:#94a3b8}\
.sv-oi{width:100%;padding:10px 14px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0;color:#1e293b;font-size:.76rem;font-family:inherit;resize:vertical;min-height:60px;outline:none;margin-bottom:14px}\
.sv-oi:focus{border-color:#818cf8}\
.sv-wr{display:flex;gap:8px;margin-bottom:14px}\
.sv-wr input{flex:1;padding:9px 12px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0;color:#1e293b;font-size:.76rem;font-family:inherit;outline:none;text-align:center}\
.sv-wr input:focus{border-color:#818cf8}\
.sv-ev{margin-bottom:10px}\
.sv-ev-t{font-size:.72rem;color:#475569;margin-bottom:6px;line-height:1.4}\
.sv-ev-s{display:flex;gap:3px}\
.sv-ev-o{flex:1;height:32px;border-radius:7px;border:1px solid #e2e8f0;background:#fafbfc;color:#94a3b8;font-size:.65rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:inherit}\
.sv-ev-o:hover{background:rgba(245,158,11,.06)}\
.sv-ev-o.sel{background:rgba(245,158,11,.1);border-color:#f59e0b;color:#d97706}\
.sv-thx{text-align:center;padding:48px 32px}\
.sv-thx-ic{font-size:3rem;margin-bottom:16px}\
.sv-thx-t{font-size:1.3rem;font-weight:800;color:#1e293b;margin-bottom:8px}\
.sv-thx-s{font-size:.82rem;color:#64748b;line-height:1.6;margin-bottom:24px}\
.sv-thx-m{display:inline-flex;gap:24px;padding:14px 24px;background:#f8fafc;border-radius:14px;border:1px solid #e2e8f0}\
.sv-thx-v{text-align:center}.sv-thx-v .vn{font-size:1.5rem;font-weight:800}.sv-thx-v .vl{font-size:.65rem;color:#94a3b8;margin-top:2px}\
@keyframes svF{from{opacity:0}to{opacity:1}}\
@keyframes svU{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}\
@keyframes svR{from{opacity:0;transform:translateX(30px)}to{opacity:1;transform:translateX(0)}}\
@keyframes svP{0%,100%{box-shadow:0 0 0 0 rgba(129,140,248,0)}50%{box-shadow:0 0 0 4px rgba(129,140,248,.15)}}\
@media(max-width:640px){.sv-tp{width:240px;right:8px;top:8px}.sv-mo{width:300px;right:12px;bottom:12px}.sv-exit-c{width:96%}}\
';
document.head.appendChild(css);

function rec(type,d){if(global.UserTestTracker)global.UserTestTracker.record(type,d)}

// ===== 欢迎浮层 =====
var TEST_VIDEO_URL='assets/test-video.mov';
function showWelcome(){
var ov=document.createElement('div');ov.className='sv-overlay';ov.id='svWelcome';
var w=config().welcome;
var c='<div class="sv-card"><h2>'+w.title+'</h2><p class="sv-sub">'+w.subtitle+'</p>';
c+='<div style="margin:0 auto 16px;max-width:340px;padding:12px 16px;border-radius:12px;background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.15);text-align:left">';
c+='<div style="font-size:.72rem;font-weight:600;color:#f59e0b;margin-bottom:6px">📹 测试素材</div>';
c+='<div style="font-size:.76rem;color:#475569;margin-bottom:8px">请先下载测试视频，稍后上传使用：</div>';
c+='<a href="'+TEST_VIDEO_URL+'" download="test-video.mov" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:9px;background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.25);color:#f59e0b;font-size:.78rem;font-weight:600;text-decoration:none">⬇ 下载测试视频 <span style="font-weight:400;color:#a3873a;font-size:.65rem">(2.4MB)</span></a>';
c+='</div>';
c+='<div style="text-align:left;margin:0 auto 16px;max-width:340px;padding:12px 16px;border-radius:12px;background:rgba(129,140,248,.06);border:1px solid rgba(129,140,248,.12)">';
c+='<div style="font-size:.68rem;color:#818cf8;font-weight:600;margin-bottom:6px">🎯 你的任务</div>';
c+='<div style="font-size:.85rem;color:#1e293b;font-weight:600">'+tasks[0].label+'</div>';
if(guidedMode&&tasks.length>1)c+='<div style="font-size:.62rem;color:#475569;margin-top:6px">完成后会给你下一个任务，共 '+tasks.length+' 个</div>';
c+='</div>';
c+='<div class="sv-note">'+w.note+'</div>';
c+='<div style="font-size:.68rem;color:#64748b;margin-bottom:16px">⏱ 预计用时约 '+w.estimatedTime+'</div>';
c+='<button class="sv-btn" id="svStart">开始体验</button></div>';
ov.innerHTML=c;document.body.appendChild(ov);
document.getElementById('svStart').onclick=function(){ov.style.animation='svF .3s reverse forwards';setTimeout(function(){ov.remove();if(cfgTasks)showTaskPanel();rec('survey_welcome_done',{config:configKey()})},300)};
rec('survey_welcome_show',{config:configKey()});
}
function config(){return{welcome:isInternal?{title:'感谢参与可用性测试',subtitle:'' + pn + ' 是一个 AI 视频翻译工具，可以自动将视频翻译成其他语言。我们希望通过你的真实操作体验，发现产品的易用性问题。',note:'请像第一次使用一个新产品一样自然操作。没有对错之分，你遇到的任何困惑都是我们需要改进的地方。过程中会在关键节点弹出简短问卷，请如实作答。',estimatedTime:'5-8 分钟'}:{title:'感谢参与体验测试',subtitle:'请使用 ' + pn + ' 将一段视频翻译成中文，并下载翻译后的结果。',note:'请像平时使用新产品一样自然操作。过程中会弹出几个简短问题，请如实作答。',estimatedTime:'5-8 分钟'}}}
function configKey(){return isInternal?'internal_v1':'user_v1'}

// ===== 任务面板 =====
var tpEl=null;
function showTaskPanel(){
tpEl=document.createElement('div');tpEl.className='sv-tp';tpEl.id='svTaskPanel';
renderTaskPanel();document.body.appendChild(tpEl);
// 8秒后自动收起为气泡
setTimeout(function(){if(tpEl&&!tpEl.classList.contains('min'))tpEl.classList.add('min')},8000);
}
function renderTaskPanel(){
if(!tpEl)return;
var done=taskStates.filter(function(s){return s==='done'}).length;
var pct=Math.round(done/tasks.length*100);
var circumference=Math.PI*2*12.75;
var dashoffset=circumference-(pct/100)*circumference;
// 当前任务
var curTask=null,curIdx=-1;
for(var ci=0;ci<tasks.length;ci++){if(taskStates[ci]==='pending'){curTask=tasks[ci];curIdx=ci;break;}}
var allDone=!curTask;
var curLabel=allDone?'全部完成!':curTask.label;

var h='<div class="sv-tp-h"><div class="sv-tp-t"><span>📋</span> <span class="sv-tp-p">'+done+'/'+tasks.length+'</span>';
// 气泡模式内容
h+='<div class="sv-fab"><div class="sv-fab-ring"><svg width="28" height="28" viewBox="0 0 28 28"><circle cx="14" cy="14" r="12.75" stroke-dasharray="'+circumference.toFixed(1)+'" stroke-dashoffset="'+dashoffset.toFixed(1)+'"/></svg><span class="sv-fab-num">'+(allDone?'✓':done)+'</span></div><span class="sv-fab-txt">'+curLabel+'</span></div>';
h+='</div><button class="sv-tp-x" id="svTpToggle">−</button></div>';

// 展开面板：只显示当前任务（不显示全部）
h+='<div class="sv-tp-b">';
if(allDone){
h+='<div style="text-align:center;padding:8px 0"><div style="font-size:1.2rem;margin-bottom:4px">🎉</div><div style="font-size:.82rem;font-weight:700;color:#10b981">全部完成！</div><div style="font-size:.68rem;color:#64748b;margin-top:4px">感谢你的参与</div></div>';
}else{
// 已完成的，只显示打勾的数量
if(done>0){
h+='<div style="font-size:.65rem;color:#64748b;margin-bottom:8px">✅ 已完成 '+done+' 步</div>';
}
// 当前任务 — 大号显示
h+='<div style="padding:10px 12px;border-radius:10px;background:rgba(129,140,248,.06);border:1px solid rgba(129,140,248,.15);margin-bottom:8px">';
h+='<div style="font-size:.62rem;color:#818cf8;font-weight:600;margin-bottom:4px">当前任务 · 第 '+(curIdx+1)+' 步</div>';
h+='<div style="font-size:.82rem;color:#1e293b;font-weight:600;line-height:1.4">'+curTask.label+'</div>';
if(curTask.hint)h+='<div style="font-size:.68rem;color:#64748b;margin-top:4px">💡 '+curTask.hint+'</div>';
h+='</div>';
// 后续预告
if(curIdx+1<tasks.length){
h+='<div style="font-size:.62rem;color:#334155">接下来还有 '+(tasks.length-curIdx-1)+' 步</div>';
}
}
var elapsed=Math.round((Date.now()-startTs)/1000);var m=Math.floor(elapsed/60),s=elapsed%60;
h+='<div class="sv-timer">⏱ '+m+':'+String(s).padStart(2,'0')+'</div>';
h+='</div>';

tpEl.innerHTML=h;
// 保留最小化状态
var wasMin=tpEl.classList.contains('min');
if(wasMin)tpEl.classList.add('min');
document.getElementById('svTpToggle').onclick=function(e){e.stopPropagation();tpEl.classList.toggle('min')};
tpEl.onclick=function(){if(tpEl.classList.contains('min'))tpEl.classList.remove('min')};
}
// 每秒更新计时器
setInterval(function(){if(tpEl&&!tpEl.classList.contains('min')){var t=tpEl.querySelector('.sv-timer');if(t){var e=Math.round((Date.now()-startTs)/1000);t.textContent='⏱ 已用时 '+Math.floor(e/60)+':'+String(e%60).padStart(2,'0')}}},1000);

// ===== 任务完成检测 =====
function completeTask(detect){
for(var i=0;i<tasks.length;i++){
if(tasks[i].detect===detect&&taskStates[i]==='pending'){
taskStates[i]='done';
rec('task_complete',{taskId:tasks[i].id,label:tasks[i].label,elapsed:Math.round((Date.now()-startTs)/1000)});
if(guidedMode&&i===taskIdx)taskIdx=Math.min(taskIdx+1,tasks.length);
saveState();
renderTaskPanel();
// 任务完成时短暂展开面板，让用户看到下一个任务
if(tpEl&&tpEl.classList.contains('min')){
tpEl.classList.remove('min');
setTimeout(function(){if(tpEl)tpEl.classList.add('min')},4000);
}
// 全部完成？
if(taskStates.every(function(s){return s==='done'})&&!exitShown&&cfgExit){
setTimeout(function(){showExitSurvey()},2000);
}
break;
}}
}

// ===== 微问卷触发 =====
function triggerCheckpoint(eventName){
checkpoints.forEach(function(cp){
if(cp.trigger===eventName&&!answered[cp.id]){
answered[cp.id]=true;
setTimeout(function(){showMicroSurvey(cp)},cp.delay||1000);
}
});
}

// ===== 微问卷UI =====
function showMicroSurvey(cp){
var existing=document.getElementById('svMicro');if(existing)existing.remove();
var wrap=document.createElement('div');wrap.className='sv-mo';wrap.id='svMicro';
var h='<button class="sv-mo-sk" id="svMoSkip">跳过</button><div class="sv-mo-q">'+cp.question+'</div>';
if(cp.type==='rating'){
h+='<div class="sv-rr">';for(var i=1;i<=cp.scale;i++)h+='<button class="sv-rs" data-v="'+i+'">'+i+'</button>';h+='</div>';
if(cp.labels&&cp.labels.length>=2)h+='<div class="sv-rl"><span>'+cp.labels[0]+'</span><span>'+cp.labels[cp.labels.length-1]+'</span></div>';
if(cp.allowComment)h+='<textarea class="sv-ci" id="svMoComment" placeholder="'+(cp.commentPH||'补充说明（可选）')+'" rows="2"></textarea>';
h+='<button class="sv-mo-sub" id="svMoSubmit">确认</button>';
}else if(cp.type==='sam'){
cp.dims.forEach(function(d,di){
h+='<div class="sv-sam-d"><div class="sv-sam-l">'+d.label+'</div><div class="sv-sam-w"><span class="sv-sam-e">'+d.l+'</span><input type="range" class="sv-sam-s" min="1" max="9" value="5" data-dim="'+d.id+'" id="svSam'+di+'"><span class="sv-sam-v" id="svSamV'+di+'">5</span><span class="sv-sam-e">'+d.r+'</span></div></div>';
});
h+='<button class="sv-mo-sub rdy" id="svMoSubmit">确认</button>';
}
wrap.innerHTML=h;document.body.appendChild(wrap);
rec('survey_show',{checkpoint:cp.id,type:cp.type});

// 绑定事件
var val=null;
if(cp.type==='rating'){
wrap.querySelectorAll('.sv-rs').forEach(function(btn){btn.onclick=function(){
val=parseInt(this.dataset.v);
wrap.querySelectorAll('.sv-rs').forEach(function(b){b.classList.toggle('on',parseInt(b.dataset.v)<=val)});
document.getElementById('svMoSubmit').classList.add('rdy');
}});
}
if(cp.type==='sam'){
wrap.querySelectorAll('.sv-sam-s').forEach(function(sl,i){sl.oninput=function(){
document.getElementById('svSamV'+i).textContent=this.value;
}});
}
document.getElementById('svMoSubmit').onclick=function(){
var data={checkpoint:cp.id,type:cp.type,elapsed:Math.round((Date.now()-startTs)/1000)};
if(cp.type==='rating'){data.rating=val;var cm=document.getElementById('svMoComment');if(cm)data.comment=cm.value.trim();}
if(cp.type==='sam'){data.sam={};wrap.querySelectorAll('.sv-sam-s').forEach(function(sl){data.sam[sl.dataset.dim]=parseInt(sl.value)})}
rec('survey_answer',data);
saveState();
closeMicro();
};
document.getElementById('svMoSkip').onclick=function(){rec('survey_skip',{checkpoint:cp.id});saveState();closeMicro()};
function closeMicro(){wrap.style.animation='svU .3s reverse forwards';setTimeout(function(){wrap.remove()},300)}
}

// ===== 总结问卷 =====
function showExitSurvey(){
if(exitShown)return;exitShown=true;
var ov=document.createElement('div');ov.className='sv-exit';ov.id='svExit';
var h='<div class="sv-exit-c"><div class="sv-exit-h"><h2>📋 总结问卷</h2><p>感谢完成所有任务！请花 2 分钟填写以下问卷</p></div><div class="sv-exit-b">';

// SUS
h+='<div class="sv-sec"><div class="sv-sec-t">系统可用性量表 <span class="sv-sec-tag">SUS</span></div>';
SUS_Q.forEach(function(q,i){
h+='<div class="sv-sq"><div class="sv-sq-t">'+(i+1)+'. '+q+'</div><div class="sv-sq-s"><span class="sv-sq-e">非常不同意</span>';
for(var v=1;v<=5;v++)h+='<button class="sv-sq-o" data-sus="'+i+'" data-v="'+v+'">'+v+'</button>';
h+='<span class="sv-sq-e">非常同意</span></div></div>';
});h+='</div>';

// 情绪价值
h+='<div class="sv-sec"><div class="sv-sec-t">情绪价值量表 <span class="sv-sec-tag">EV</span></div>';
EV_Q.forEach(function(q,i){
h+='<div class="sv-ev"><div class="sv-ev-t">'+(i+1)+'. '+q+'</div><div class="sv-ev-s">';
['非常不同意','不同意','中立','同意','非常同意'].forEach(function(l,v){
h+='<button class="sv-ev-o" data-ev="'+i+'" data-v="'+(v+1)+'">'+l+'</button>';
});h+='</div></div>';
});h+='</div>';

// NPS
h+='<div class="sv-sec"><div class="sv-sec-t">推荐意愿 <span class="sv-sec-tag">NPS</span></div>';
h+='<div class="sv-sq-t">你有多大可能向同事/朋友推荐 ' + pn + '？</div>';
h+='<div class="sv-nps-r">';for(var n=0;n<=10;n++)h+='<button class="sv-nps-b" data-nps="'+n+'">'+n+'</button>';
h+='</div><div class="sv-nps-l"><span>完全不会</span><span>非常愿意</span></div>';
h+='<div class="sv-sq-t" style="margin-top:14px">你愿意推荐的主要原因是？</div>';
h+='<textarea class="sv-oi" id="svNpsWhy" placeholder="（可选）"></textarea>';
h+='</div>';

// 三词描述
h+='<div class="sv-sec"><div class="sv-sec-t">三个词描述 ' + pn + '</div>';
h+='<div class="sv-wr"><input id="svW1" placeholder="第一个词"><input id="svW2" placeholder="第二个词"><input id="svW3" placeholder="第三个词"></div></div>';

// 开放题
h+='<div class="sv-sec"><div class="sv-sec-t">开放反馈</div>';
h+='<div class="sv-sq-t">使用过程中最困惑/卡住的地方是什么？</div><textarea class="sv-oi" id="svOpen1" placeholder="请描述…"></textarea>';
h+='<div class="sv-sq-t">你觉得 ' + pn + ' 最有价值的功能是什么？</div><textarea class="sv-oi" id="svOpen2" placeholder="请描述…"></textarea>';
h+='</div>';

h+='<button class="sv-btn" style="width:100%;padding:14px;font-size:.92rem" id="svExitSubmit">提交问卷</button>';
h+='</div></div>';
ov.innerHTML=h;document.body.appendChild(ov);
rec('survey_exit_show',{});

// 绑定SUS
ov.querySelectorAll('.sv-sq-o').forEach(function(b){b.onclick=function(){
var idx=this.dataset.sus;ov.querySelectorAll('[data-sus="'+idx+'"]').forEach(function(x){x.classList.remove('sel')});this.classList.add('sel');
}});
// 绑定EV
ov.querySelectorAll('.sv-ev-o').forEach(function(b){b.onclick=function(){
var idx=this.dataset.ev;ov.querySelectorAll('[data-ev="'+idx+'"]').forEach(function(x){x.classList.remove('sel')});this.classList.add('sel');
}});
// 绑定NPS
ov.querySelectorAll('.sv-nps-b').forEach(function(b){b.onclick=function(){
ov.querySelectorAll('.sv-nps-b').forEach(function(x){x.classList.remove('sel','nl','nm','nh')});
this.classList.add('sel');var v=parseInt(this.dataset.nps);this.classList.add(v<=6?'nl':v<=8?'nm':'nh');
}});
// 提交
document.getElementById('svExitSubmit').onclick=function(){submitExitSurvey(ov)};
}

function submitExitSurvey(ov){
var sus=[],ev=[];
for(var i=0;i<10;i++){var s=ov.querySelector('.sv-sq-o[data-sus="'+i+'"].sel');sus.push(s?parseInt(s.dataset.v):0)}
for(var i=0;i<EV_Q.length;i++){var e=ov.querySelector('.sv-ev-o[data-ev="'+i+'"].sel');ev.push(e?parseInt(e.dataset.v):0)}
var npsBtn=ov.querySelector('.sv-nps-b.sel');var nps=npsBtn?parseInt(npsBtn.dataset.nps):-1;
// SUS 计算
var susScore=0;
sus.forEach(function(v,i){if(i%2===0)susScore+=(v-1);else susScore+=(5-v)});
susScore=susScore*2.5;
var data={
sus:sus,susScore:susScore,
ev:ev,evAvg:ev.length?(ev.reduce(function(a,b){return a+b},0)/ev.length).toFixed(1):0,
nps:nps,npsWhy:(document.getElementById('svNpsWhy')||{}).value||'',
words:[(document.getElementById('svW1')||{}).value||'',(document.getElementById('svW2')||{}).value||'',(document.getElementById('svW3')||{}).value||''].filter(Boolean),
open1:(document.getElementById('svOpen1')||{}).value||'',
open2:(document.getElementById('svOpen2')||{}).value||'',
totalTime:Math.round((Date.now()-startTs)/1000),
config:configKey()
};
rec('survey_exit_submit',data);
if(global.UserTestTracker)global.UserTestTracker.flush();
// 显示感谢
ov.querySelector('.sv-exit-c').innerHTML='<div class="sv-thx"><div class="sv-thx-ic">🎉</div><div class="sv-thx-t">感谢你的参与！</div><div class="sv-thx-s">你的反馈对我们改进产品非常重要。<br>问卷数据已保存，你现在可以关闭页面了。</div><div class="sv-thx-m"><div class="sv-thx-v"><div class="vn" style="color:#818cf8">'+susScore.toFixed(0)+'</div><div class="vl">SUS 分数</div></div><div class="sv-thx-v"><div class="vn" style="color:'+(nps>=9?'#10b981':nps>=7?'#f59e0b':'#ef4444')+'">'+nps+'</div><div class="vl">NPS 评分</div></div><div class="sv-thx-v"><div class="vn" style="color:#f59e0b">'+Math.round((Date.now()-startTs)/1000/60)+'<span style="font-size:.7rem">min</span></div><div class="vl">测试用时</div></div></div></div>';
}

// ===== 事件桥接 — 监听 tracker 事件 =====
function hookTracker(){
if(!global.UserTestTracker)return;
var origRecord=global.UserTestTracker.record;
global.UserTestTracker.record=function(type,detail){
var result=origRecord.call(global.UserTestTracker,type,detail);
// 任务检测
if(type==='milestone'&&detail&&detail.name){
var mn=detail.name;
completeTask(mn);
if(mn.indexOf('mps_complete')===0){completeTask('mps_complete');triggerCheckpoint('view_result')}
if(mn==='view_result')triggerCheckpoint('view_result');
if(mn==='finetune_edit'){completeTask('finetune_edit');triggerCheckpoint('finetune_edit')}
}
if(type==='upload_done'){completeTask('upload_done');triggerCheckpoint('upload_done')}
if(type==='mps_status'&&detail&&(detail.status==='complete'||detail.status==='COMPLETED')){completeTask('mps_complete');triggerCheckpoint('view_result')}
if(type==='click'&&detail){
if(detail.action==='export'){completeTask('export');triggerCheckpoint('export')}
if(detail.action==='finetune_done'){completeTask('finetune_edit');triggerCheckpoint('finetune_edit')}
if(detail.action==='finetune')triggerCheckpoint('finetune_edit');
}
if(type==='phase_start'&&detail){
if(detail.phase==='processing'||detail.phase==='mps_submit'){procStart=Date.now();if(!procTimerDone){procTimerDone=true;setTimeout(function(){triggerCheckpoint('processing_wait_30s')},30000)}}
}
if(type==='enter'&&detail&&detail.url){
if(detail.url.indexOf('translate')!==-1)completeTask('page_translate');
}
return result;
};
var origMilestone=global.UserTestTracker.milestone;
global.UserTestTracker.milestone=function(name,extra){
origMilestone.call(global.UserTestTracker,name,extra);
completeTask(name);
if(name.indexOf('mps_complete')===0){completeTask('mps_complete');triggerCheckpoint('view_result')}
if(name==='view_result')triggerCheckpoint('view_result');
if(name==='finetune_edit'){completeTask('finetune_edit');triggerCheckpoint('finetune_edit')}
};
}

// ===== 公开API =====
global.UserTestSurvey={
completeTask:completeTask,
triggerCheckpoint:triggerCheckpoint,
showExitSurvey:function(){showExitSurvey()},
getTaskStates:function(){return taskStates.slice()},
getAnswered:function(){return Object.assign({},answered)}
};

// ===== 初始化 =====
function init(){
hookTracker();
// 如果已经在 translate 页面，标记 T1
if(location.pathname.indexOf('translate')!==-1){
completeTask('page_translate');
// 自动启动模式下，启动处理等待计时器
if(params.get('autostart')==='1'&&!procTimerDone){
procTimerDone=true;
setTimeout(function(){triggerCheckpoint('processing_wait_30s')},30000);
}
}
// 有恢复的进度？直接显示气泡（跳过欢迎页）
var hasDone=taskStates.some(function(s){return s==='done'});
if(hasDone){
if(cfgTasks){showTaskPanel();setTimeout(function(){if(tpEl)tpEl.classList.add('min')},500)}
// 跨页面补弹：已完成的任务对应的问卷如果还没答，延迟补弹
setTimeout(function(){
for(var ti=0;ti<tasks.length;ti++){
if(taskStates[ti]==='done'){
var detect=tasks[ti].detect;
// 找到对应的 checkpoint trigger
checkpoints.forEach(function(cp){
if(cp.trigger===detect&&!answered[cp.id]){
answered[cp.id]=true;
setTimeout(function(){showMicroSurvey(cp)},cp.delay||1000);
}
});
}
}
},1500);
}else if(cfgWelcome){
showWelcome();
}else{
// 没有欢迎页，直接显示任务面板
if(cfgTasks)showTaskPanel();
}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();

})(window);
