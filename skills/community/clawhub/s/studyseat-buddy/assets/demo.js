// StudySeat Buddy - Demo Application
(function(){
"use strict";

// === AUTH ===
var ACCOUNTS = {};
ACCOUNTS["student"] = {pw:"123456", role:"student"};
ACCOUNTS["admin"] = {pw:"admin123", role:"admin"};
var curUser = null;

function $(id){return document.getElementById(id)}

function doLogin(){
  var u = $("loginUser").value.trim();
  var p = $("loginPass").value;
  if(ACCOUNTS[u] && ACCOUNTS[u].pw === p){
    $("loginError").className = "login-error";
    curUser = {username:u, role:ACCOUNTS[u].role};
    $("loginPage").style.display = "none";
    $("appPage").style.display = "block";
    if(curUser.role === "admin"){
      $("roleTag").textContent = "管理员端";
      $("roleTag").className = "role-tag admin";
      $("studentPage").style.display = "none";
      $("adminPage").style.display = "block";
      renderAdmin();
    } else {
      $("roleTag").textContent = "学生端";
      $("roleTag").className = "role-tag student";
      $("studentPage").style.display = "block";
      $("adminPage").style.display = "none";
      runDemo(1);
    }
  } else {
    $("loginError").className = "login-error show";
  }
}

function doLogout(){
  curUser = null;
  $("loginUser").value = "";
  $("loginPass").value = "";
  $("loginError").className = "login-error";
  $("loginPage").style.display = "flex";
  $("appPage").style.display = "none";
  $("studentPage").style.display = "none";
  $("adminPage").style.display = "none";
}

function goStudent(){
  $("roleTag").textContent = "学生端";
  $("roleTag").className = "role-tag student";
  $("adminPage").style.display = "none";
  $("studentPage").style.display = "block";
  runDemo(1);
}

// === DATA ===
var classrooms=[
{id:"A101",campus:"北区",building:"A栋",floor:"1层",cap:60,plug:"全部有",ac:"有",quiet:3,open:"07:00-22:00",scene:"个人自习、小型上课",mode:["赶DDL","普通自习"],sit:"适合久坐",risk:"靠近入口人流较多，安静度一般",note:"靠近入口，人流较多",status:"正常"},
{id:"A103",campus:"北区",building:"A栋",floor:"1层",cap:50,plug:"全部有",ac:"有",quiet:3,open:"—",scene:"—",mode:[],sit:"—",risk:"—",note:"装修维修中",status:"维修"},
{id:"A201",campus:"北区",building:"A栋",floor:"2层",cap:80,plug:"全部有",ac:"有",quiet:4,open:"07:00-22:00",scene:"个人自习、中型上课",mode:["普通自习","赶DDL"],sit:"适合久坐",risk:"容量较大，单人自习氛围不如小教室",note:"",status:"正常"},
{id:"A202",campus:"北区",building:"A栋",floor:"2层",cap:45,plug:"部分有",ac:"有",quiet:4,open:"07:00-22:00",scene:"小组讨论、研讨课",mode:["小组讨论","备考"],sit:"适合久坐",risk:"部分区域插座不可用",note:"有白板，适合围坐",status:"正常"},
{id:"A301",campus:"北区",building:"A栋",floor:"3层",cap:100,plug:"全部有",ac:"有",quiet:3,open:"07:00-22:00",scene:"大型上课、讲座",mode:["普通自习"],sit:"一般",risk:"阶梯教室，不适合围坐，安静度低",note:"阶梯教室，不适合围坐",status:"正常"},
{id:"A302",campus:"北区",building:"A栋",floor:"3层",cap:50,plug:"全部有",ac:"有",quiet:5,open:"08:00-21:00",scene:"个人自习、备考",mode:["备考","普通自习"],sit:"适合久坐",risk:"需刷卡进入，忘带校园卡无法进入",note:"最安静，需刷卡进入",status:"正常"},
{id:"B101",campus:"北区",building:"B栋",floor:"1层",cap:40,plug:"部分有",ac:"无",quiet:3,open:"07:30-21:00",scene:"个人自习",mode:["普通自习"],sit:"一般",risk:"靠近食堂午饭时较吵，无空调夏天闷热",note:"靠近食堂，午饭时较吵",status:"正常"},
{id:"B103",campus:"北区",building:"B栋",floor:"1层",cap:45,plug:"全部有",ac:"有",quiet:3,open:"—",scene:"—",mode:[],sit:"—",risk:"—",note:"设备更新，2026-06-01恢复",status:"暂停开放"},
{id:"B201",campus:"北区",building:"B栋",floor:"2层",cap:70,plug:"全部有",ac:"有",quiet:4,open:"07:00-22:00",scene:"个人自习、上课",mode:["赶DDL","普通自习"],sit:"适合久坐",risk:"容量偏大，上课时段可能被占",note:"",status:"正常"},
{id:"B202",campus:"北区",building:"B栋",floor:"2层",cap:30,plug:"全部有",ac:"有",quiet:5,open:"08:00-21:30",scene:"小组讨论(≤6人)、研讨",mode:["小组讨论","备考"],sit:"适合久坐",risk:"座位较少(仅30座)，小组预约时可能满员",note:"小型研讨室，适合6人以内",status:"正常"},
{id:"B301",campus:"北区",building:"B栋",floor:"3层",cap:90,plug:"全部有",ac:"有",quiet:3,open:"07:00-22:00",scene:"大型上课、自习",mode:["普通自习"],sit:"一般",risk:"容量过大，单人自习氛围差",note:"",status:"正常"},
{id:"C101",campus:"南区",building:"C栋",floor:"1层",cap:55,plug:"全部有",ac:"有",quiet:4,open:"07:00-22:00",scene:"个人自习、上课",mode:["普通自习","备考"],sit:"适合久坐",risk:"近宿舍但非北区",note:"近宿舍区，步行5分钟",status:"正常"},
{id:"C201",campus:"南区",building:"C栋",floor:"2层",cap:65,plug:"全部有",ac:"有",quiet:4,open:"07:00-22:00",scene:"个人自习、上课",mode:["普通自习","赶DDL"],sit:"适合久坐",risk:"",note:"",status:"正常"},
{id:"C202",campus:"南区",building:"C栋",floor:"2层",cap:35,plug:"部分有",ac:"有",quiet:5,open:"08:00-21:00",scene:"备考、个人自习",mode:["备考","晚自习"],sit:"适合久坐",risk:"部分插座不可用，南区非北区",note:"安静优先，适合备考",status:"正常"},
{id:"C301",campus:"南区",building:"C栋",floor:"3层",cap:120,plug:"全部有",ac:"有",quiet:2,open:"07:00-22:00",scene:"大型讲座、报告",mode:[],sit:"一般",risk:"阶梯教室回声大，不适合自习",note:"大型阶梯教室，回声较大",status:"正常"},
{id:"D101",campus:"南区",building:"D栋",floor:"1层",cap:50,plug:"无",ac:"有",quiet:4,open:"07:30-21:30",scene:"个人自习",mode:["普通自习"],sit:"一般",risk:"无插座，长时间用电设备无法使用",note:"无插座，不建议长时间用电",status:"正常"},
{id:"D201",campus:"南区",building:"D栋",floor:"2层",cap:80,plug:"全部有",ac:"有",quiet:3,open:"07:00-22:00",scene:"上课、自习",mode:["赶DDL","普通自习"],sit:"适合久坐",risk:"安静度一般",note:"",status:"正常"},
{id:"D202",campus:"南区",building:"D栋",floor:"2层",cap:40,plug:"全部有",ac:"有",quiet:4,open:"08:00-21:30",scene:"小组讨论、研讨",mode:["小组讨论","备考"],sit:"适合久坐",risk:"可能有课程占用",note:"可移动桌椅，适合围坐",status:"正常"},
{id:"D301",campus:"南区",building:"D栋",floor:"3层",cap:60,plug:"部分有",ac:"无",quiet:5,open:"08:00-21:00",scene:"备考、个人自习",mode:["备考","晚自习"],sit:"一般",risk:"无空调，夏天闷热不适",note:"最安静楼层，无空调慎选夏天",status:"正常"},
{id:"Z101",campus:"综合楼",building:"综合楼",floor:"1层",cap:200,plug:"全部有",ac:"有",quiet:2,open:"07:00-22:00",scene:"大型报告、活动",mode:[],sit:"不适合久坐",risk:"大报告厅，不适合自习",note:"大报告厅，不适合自习",status:"正常"},
{id:"Z201",campus:"综合楼",building:"综合楼",floor:"2层",cap:60,plug:"全部有",ac:"有",quiet:4,open:"07:00-22:00",scene:"个人自习、上课",mode:["普通自习","赶DDL"],sit:"适合久坐",risk:"",note:"",status:"正常"},
{id:"Z301",campus:"综合楼",building:"综合楼",floor:"3层",cap:45,plug:"全部有",ac:"有",quiet:5,open:"08:00-21:00",scene:"自习专用、备考",mode:["备考","晚自习"],sit:"适合久坐",risk:"禁止喧哗，说话会被提醒",note:"自习专用楼层，禁止喧哗",status:"正常"},
{id:"Z302",campus:"综合楼",building:"综合楼",floor:"3层",cap:30,plug:"全部有",ac:"有",quiet:5,open:"08:00-21:00",scene:"小组讨论(≤6人)、自习",mode:["小组讨论","备考"],sit:"适合久坐",risk:"座位较少，小组时段可能满员",note:"自习专用，适合2-6人小组",status:"正常"}
];

var schedule=[
{id:"A101",day:"周一",s:"08:00",e:"09:45",ev:"高等数学",type:"硬"},
{id:"A101",day:"周一",s:"10:05",e:"11:50",ev:"线性代数",type:"硬"},
{id:"A201",day:"周一",s:"08:00",e:"09:45",ev:"大学英语",type:"硬"},
{id:"A201",day:"周一",s:"14:00",e:"15:45",ev:"数据结构",type:"硬"},
{id:"A301",day:"周一",s:"08:00",e:"11:50",ev:"思政课",type:"硬"},
{id:"B201",day:"周一",s:"10:05",e:"11:50",ev:"程序设计基础",type:"硬"},
{id:"B201",day:"周一",s:"14:00",e:"17:50",ev:"实验课",type:"硬"},
{id:"C101",day:"周一",s:"08:00",e:"09:45",ev:"物理",type:"硬"},
{id:"C201",day:"周一",s:"14:00",e:"15:45",ev:"经济学原理",type:"硬"},
{id:"D201",day:"周一",s:"08:00",e:"11:50",ev:"专业课",type:"硬"},
{id:"Z201",day:"周一",s:"19:00",e:"20:45",ev:"选修课",type:"硬"},
{id:"A101",day:"周二",s:"14:00",e:"15:45",ev:"概率论",type:"硬"},
{id:"A202",day:"周二",s:"08:00",e:"09:45",ev:"小组研讨课",type:"硬"},
{id:"A202",day:"周二",s:"14:00",e:"15:45",ev:"创业课",type:"硬"},
{id:"B101",day:"周二",s:"08:00",e:"11:50",ev:"化学实验",type:"硬"},
{id:"B201",day:"周二",s:"08:00",e:"09:45",ev:"操作系统",type:"硬"},
{id:"C101",day:"周二",s:"10:05",e:"11:50",ev:"高等数学",type:"硬"},
{id:"C201",day:"周二",s:"08:00",e:"09:45",ev:"英语写作",type:"硬"},
{id:"D201",day:"周二",s:"14:00",e:"15:45",ev:"管理学",type:"硬"},
{id:"D201",day:"周二",s:"16:05",e:"17:50",ev:"会计学",type:"硬"},
{id:"Z201",day:"周二",s:"08:00",e:"09:45",ev:"体育理论",type:"硬"},
{id:"A101",day:"周三",s:"08:00",e:"09:45",ev:"大学语文",type:"硬"},
{id:"A201",day:"周三",s:"10:05",e:"11:50",ev:"数学分析",type:"硬"},
{id:"A301",day:"周三",s:"14:00",e:"17:50",ev:"大型讲座",type:"硬"},
{id:"B201",day:"周三",s:"10:05",e:"11:50",ev:"数据库原理",type:"硬"},
{id:"B301",day:"周三",s:"08:00",e:"11:50",ev:"电路基础",type:"硬"},
{id:"C101",day:"周三",s:"14:00",e:"15:45",ev:"马克思主义",type:"硬"},
{id:"D202",day:"周三",s:"08:00",e:"09:45",ev:"团队项目课",type:"硬"},
{id:"D202",day:"周三",s:"14:00",e:"15:45",ev:"用户体验设计",type:"硬"},
{id:"Z201",day:"周三",s:"10:05",e:"11:50",ev:"心理健康课",type:"硬"},
{id:"Z301",day:"周三",s:"19:00",e:"20:45",ev:"晚自习(有监考)",type:"软"},
{id:"A101",day:"周四",s:"10:05",e:"11:50",ev:"统计学",type:"硬"},
{id:"A201",day:"周四",s:"08:00",e:"09:45",ev:"信号与系统",type:"硬"},
{id:"A202",day:"周四",s:"10:05",e:"11:50",ev:"研讨课",type:"硬"},
{id:"B201",day:"周四",s:"14:00",e:"15:45",ev:"编译原理",type:"硬"},
{id:"C201",day:"周四",s:"10:05",e:"11:50",ev:"财务管理",type:"硬"},
{id:"C202",day:"周四",s:"08:00",e:"09:45",ev:"备考辅导",type:"硬"},
{id:"D201",day:"周四",s:"08:00",e:"11:50",ev:"工程图学",type:"硬"},
{id:"Z201",day:"周四",s:"14:00",e:"15:45",ev:"选修讲座",type:"硬"},
{id:"A101",day:"周五",s:"08:00",e:"11:50",ev:"期末考试",type:"硬"},
{id:"A201",day:"周五",s:"14:00",e:"15:45",ev:"网络安全",type:"硬"},
{id:"B101",day:"周五",s:"10:05",e:"11:50",ev:"实验课",type:"硬"},
{id:"B201",day:"周五",s:"08:00",e:"09:45",ev:"软件工程",type:"硬"},
{id:"C101",day:"周五",s:"08:00",e:"09:45",ev:"高等数学",type:"硬"},
{id:"D202",day:"周五",s:"10:05",e:"11:50",ev:"产品设计",type:"硬"},
{id:"Z201",day:"周五",s:"08:00",e:"17:50",ev:"毕业答辩",type:"硬"},
{id:"A201",day:"周六",s:"09:00",e:"11:00",ev:"补课",type:"硬"},
{id:"B201",day:"周六",s:"14:00",e:"17:00",ev:"社团活动",type:"硬"},
{id:"C101",day:"周六",s:"09:00",e:"11:00",ev:"英语补课",type:"硬"},
{id:"Z301",day:"周日",s:"09:00",e:"17:00",ev:"考研自习",type:"软"},
{id:"A301",day:"周日",s:"14:00",e:"17:00",ev:"大型活动彩排",type:"硬"}
];

var feedback=[
{date:"2026-05-13",time:"14:00",id:"A302",crowd:"较少",noise:"安静",plug:"正常",text:"下午人很少，非常安静，插座都能用，需要刷卡"},
{date:"2026-05-12",time:"19:30",id:"A302",crowd:"适中",noise:"较安静",plug:"正常",text:"晚上人稍多但依然安静，学习氛围好"},
{date:"2026-05-13",time:"15:00",id:"B202",crowd:"较少",noise:"安静",plug:"正常",text:"研讨室很安静，只有2个人，插座充足"},
{date:"2026-05-11",time:"14:30",id:"A201",crowd:"较多",noise:"较吵",plug:"正常",text:"下午人比较多，有人在后排小声讨论，安静度不如3层"},
{date:"2026-05-12",time:"16:00",id:"A201",crowd:"适中",noise:"较安静",plug:"正常",text:"4点后人变少了，安静了一些，插座都正常"},
{date:"2026-05-10",time:"12:00",id:"B101",crowd:"拥挤",noise:"较吵",plug:"部分损坏",text:"午饭时间太吵了，而且靠窗那一排插座坏了2个"},
{date:"2026-05-13",time:"20:00",id:"Z301",crowd:"较少",noise:"安静",plug:"正常",text:"晚自习氛围很好，禁止喧哗执行到位"},
{date:"2026-05-12",time:"10:00",id:"D202",crowd:"适中",noise:"适中",plug:"正常",text:"有课占用到9:45，10点后才空出来，插座正常"},
{date:"2026-05-09",time:"14:00",id:"A301",crowd:"适中",noise:"较吵",plug:"正常",text:"虽然没课但100座太大，有人在后排走动，不如小教室安静"},
{date:"2026-05-13",time:"19:00",id:"B201",crowd:"较多",noise:"适中",plug:"正常",text:"晚上有人在自习也有人在讨论，氛围一般"},
{date:"2026-05-11",time:"08:30",id:"A302",crowd:"空旷",noise:"安静",plug:"正常",text:"早上8点几乎没人，完美安静，刷卡进入"},
{date:"2026-05-12",time:"14:00",id:"B101",crowd:"较多",noise:"较吵",plug:"部分损坏",text:"下午没空调又闷又吵，插座也有坏的，不推荐夏天来"}
];

// === ADMIN ===
function renderAdmin(){
  var total=classrooms.length,norm=0,rep=0;
  for(var i=0;i<classrooms.length;i++){if(classrooms[i].status==="正常")norm++;else rep++;}
  var dd="周三",hc=0,sc=0;
  for(var j=0;j<schedule.length;j++){if(schedule[j].day===dd){if(schedule[j].type==="硬")hc++;else sc++;}}
  var h='';
  h+='<div class="stat-card"><div class="stat-num">'+total+'</div><div class="stat-label">教室总数</div></div>';
  h+='<div class="stat-card"><div class="stat-num">'+norm+'</div><div class="stat-label">正常开放教室</div></div>';
  h+='<div class="stat-card orange"><div class="stat-num">'+rep+'</div><div class="stat-label">维修/暂停开放</div></div>';
  h+='<div class="stat-card red"><div class="stat-num">'+hc+'</div><div class="stat-label">'+dd+'硬占用数量</div></div>';
  h+='<div class="stat-card purple"><div class="stat-num">'+sc+'</div><div class="stat-label">'+dd+'软占用数量</div></div>';
  $("adminStats").innerHTML=h;
  var fh='<table class="fb-table purple"><tr><th>日期</th><th>教室</th><th>人流</th><th>噪音</th><th>插座</th><th>反馈内容</th></tr>';
  var fs=feedback.slice(0,6);
  for(var k=0;k<fs.length;k++){var f=fs[k];var nc=(f.noise==="安静"||f.noise==="较安静")?"good":(f.noise==="较吵"||f.noise==="吵闹")?"bad":"mid";
  fh+='<tr><td>'+f.date+'</td><td><strong>'+f.id+'</strong></td><td>'+f.crowd+'</td><td><span class="fb-noise '+nc+'">'+f.noise+'</span></td><td>'+f.plug+'</td><td style="max-width:220px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="'+f.text+'">'+f.text+'</td></tr>';}
  fh+='</table>';
  $("adminFeedback").innerHTML=fh;
}

// === HELPERS ===
function t2m(t){var p=t.split(":");return parseInt(p[0])*60+parseInt(p[1])}
function periodRange(p,s,e){if(p==="上午")return["08:00","11:50"];if(p==="下午")return["14:00","17:50"];if(p==="晚上")return["19:00","22:00"];return[s||"14:00",e||"16:00"];}
function stars(n){return "★".repeat(n)+"☆".repeat(5-n)}
function plugC(p){return p==="全部有"?"feat":p==="部分有"?"warn":"no"}
function acC(a){return a==="有"?"feat":"no"}

function fbScore(id){var sc=0;for(var i=0;i<feedback.length;i++){if(feedback[i].id!==id)continue;var n=feedback[i].noise,c=feedback[i].crowd,p=feedback[i].plug;if((n==="安静"||n==="较安静")&&(c==="较少"||c==="空旷")&&p==="正常")sc+=3;if(n==="较吵"||n==="吵闹"||c==="拥挤"||c==="较多")sc-=5;if(p==="部分损坏"||p==="不可用"||p==="不足")sc-=8;}return Math.max(-15,Math.min(10,sc));}

function isOv(s1,e1,s2,e2){var a=t2m(s1),b=t2m(e1),c=t2m(s2),d=t2m(e2);return a<d&&c<b;}
function isOpen(oH,qs,qe){if(oH==="—")return false;var ps=oH.split("-");return t2m(ps[0])<=t2m(qs)&&t2m(ps[1])>=t2m(qe);}

function calcSc(rm,qs,qe,mode,pe,pf,cp){
  var sc=0;var pw=(mode==="赶DDL模式")?40:30;
  if(pf.plug){if(rm.plug==="全部有")sc+=pw;else if(rm.plug==="部分有")sc+=Math.floor(pw/2);}
  var qW=(mode==="备考模式")?8:5;if(pf.quiet)sc+=rm.quiet*qW;else sc+=rm.quiet*2;
  var ratio=rm.cap/pe;if(ratio>=2&&ratio<=4)sc+=15;else if(ratio>4&&ratio<=8)sc+=5;else sc+=2;
  if(pf.ac&&rm.ac==="有")sc+=10;else if(rm.ac==="有")sc+=5;
  if(cp!=="全校"&&rm.campus===cp)sc+=20;else if(cp==="全校")sc+=5;
  if(pf.dorm&&rm.note.indexOf("宿舍")>=0)sc+=10;
  if(mode==="小组讨论模式"){if(rm.note.indexOf("围坐")>=0||rm.note.indexOf("白板")>=0)sc+=25;if(rm.cap>=pe&&rm.cap<=pe*4)sc+=20;if(rm.plug==="全部有")sc+=15;}
  if(mode==="备考模式"&&rm.quiet>=4&&rm.cap<=60)sc+=10;
  if(mode==="赶DDL模式"){var op=rm.open.split("-");if(op.length===2&&t2m(op[1])>=t2m("22:00"))sc+=10;}
  if(mode==="晚自习模式"){var op2=rm.open.split("-");if(op2.length===2&&t2m(op2[1])>=t2m("21:00"))sc+=15;}
  sc+=fbScore(rm.id);return Math.min(100,Math.max(0,sc));
}

function findCf(id,day,qs,qe){var h=[],s=[];for(var i=0;i<schedule.length;i++){if(schedule[i].id!==id||schedule[i].day!==day)continue;if(isOv(schedule[i].s,schedule[i].e,qs,qe)){if(schedule[i].type==="硬")h.push(schedule[i]);else s.push(schedule[i]);}}return{hard:h,soft:s};}

// === SEARCH ===
function doSearch(){
  var day=$("qDay").value,per=$("qPeriod").value;
  var rng=periodRange(per,$("qStart").value,$("qEnd").value);
  var qs=rng[0],qe=rng[1],cp=$("qCampus").value;
  var pe=parseInt($("qPeople").value)||1,mode=$("qMode").value;
  var pf={plug:$("pPlug").checked,quiet:$("pQuiet").checked,ac:$("pAC").checked,dorm:$("pDorm").checked};
  var res=[],av=[];
  for(var i=0;i<classrooms.length;i++){var r=classrooms[i];
    if(r.status==="维修"||r.status==="暂停开放"){av.push({id:r.id,reason:"当前状态为「"+r.status+"」，"+(r.note||"暂不可用")});continue;}
    if(cp!=="全校"&&r.campus!==cp)continue;
    if(!isOpen(r.open,qs,qe)){av.push({id:r.id,reason:"开放时段 "+r.open+" 不覆盖 "+qs+"-"+qe});continue;}
    if(r.cap<pe){av.push({id:r.id,reason:"容量 "+r.cap+" 座 < "+pe+" 人"});continue;}
    var cf=findCf(r.id,day,qs,qe);
    if(cf.hard.length>0){var evs=cf.hard.map(function(c){return c.ev+"("+c.s+"-"+c.e+")"}).join("、");av.push({id:r.id,reason:day+" "+evs+"，硬占用，已排除"});continue;}
    res.push({room:r,score:calcSc(r,qs,qe,mode,pe,pf,cp),softConflicts:cf.soft});
  }
  res.sort(function(a,b){return b.score-a.score});res=res.slice(0,5);av=av.slice(0,5);
  renderRes(res,av,day,qs,qe,mode);
}

function renderRes(res,av,day,qs,qe,mode){
  var h='<div class="card"><span class="mode-badge">🧠 学习模式：'+mode+'</span><div style="font-size:12px;color:var(--text-sec)">查询：'+day+" "+qs+"-"+qe+'</div></div>';
  if(res.length===0){h+='<div class="empty-state"><div class="empty-icon">😕</div><p>没有找到符合条件的教室，试试放宽条件</p></div>';$("results").innerHTML=h;return;}
  for(var i=0;i<res.length&&i<3;i++){var r=res[i],rm=r.room;var isB=i===0;var sC=r.score>=90?"#1D9E75":r.score>=70?"#3a9d8e":r.score>=50?"#f5a623":"#d9534f";
  h+='<div class="result-card rank-'+(i+1)+'"><span class="rank-tag '+(isB?"best":"alt")+'">'+(isB?"🏆 最优选择":"推荐 #"+(i+1))+'</span>';
  h+='<div class="room-name">'+rm.id+' · '+rm.building+' '+rm.floor+'</div>';
  h+='<div class="time-row">本次可用：<span class="avail">'+qs+' - '+qe+'</span>（开放时段：'+rm.open+'）</div>';
  h+='<div class="features"><span class="feat">容量 '+rm.cap+' 座</span><span class="'+plugC(rm.plug)+'">插座 '+rm.plug+'</span><span class="'+acC(rm.ac)+'">空调 '+rm.ac+'</span><span class="feat">安静 '+stars(rm.quiet)+'</span></div>';
  h+='<div class="score-bar"><div class="bar"><div class="fill" style="width:'+r.score+'%;background:'+sC+'"></div></div><span class="score">匹配度 '+r.score+'/100</span></div>';
  var reason="";if(mode==="备考模式")reason="备考优选：安静"+rm.quiet+"分+插座"+rm.plug+"+"+rm.cap+"座";
  else if(mode==="赶DDL模式")reason="赶DDL优选：插座"+rm.plug+"+开放至"+rm.open.split("-")[1];
  else if(mode==="小组讨论模式")reason="小组优选："+(rm.note.indexOf("围坐")>=0?"可围坐":"")+(" "+rm.cap+"座适合"+pe+"人");
  else if(mode==="晚自习模式")reason="晚自习优选：开放至"+rm.open.split("-")[1]+(rm.quiet>=4?"+安静":"");
  else reason="综合推荐：安静"+rm.quiet+"分+插座"+rm.plug+"+"+rm.cap+"座";
  if(rm.risk&&rm.risk.indexOf("刷卡")>=0)reason+="（需刷卡）";
  h+='<div class="reason">💡 '+reason+'</div>';
  if(r.softConflicts.length>0){for(var j=0;j<r.softConflicts.length;j++){var sc2=r.softConflicts[j];h+='<div class="soft-notice">📢 软占用提醒：'+sc2.s+"-"+sc2.e+" 有「"+sc2.ev+"」，可进入但须遵守规则</div>";}}
  h+='</div>';}
  if(av.length>0){h+='<div class="avoided"><h3>🚫 已避开的教室</h3>';for(var k=0;k<av.length;k++){h+='<div class="avoid-item">'+av[k].id+"："+av[k].reason+'</div>';}h+='</div>';}
  $("results").innerHTML=h;
}

function toggleCT(){var v=$("qPeriod").value;$("customTimeRow").style.display=v==="custom"?"block":"none";}

function runDemo(n){
  if(n===1){$("qDay").value="周三";$("qPeriod").value="custom";$("qStart").value="14:00";$("qEnd").value="16:00";$("qCampus").value="北区";$("qPeople").value="1";$("qMode").value="备考模式";$("pPlug").checked=true;$("pQuiet").checked=true;$("pAC").checked=false;$("pDorm").checked=false;toggleCT();}
  else if(n===2){$("qDay").value="周三";$("qPeriod").value="custom";$("qStart").value="14:00";$("qEnd").value="16:00";$("qCampus").value="北区";$("qPeople").value="6";$("qMode").value="小组讨论模式";$("pPlug").checked=true;$("pQuiet").checked=true;$("pAC").checked=false;$("pDorm").checked=false;toggleCT();}
  else{$("qDay").value="周三";$("qPeriod").value="晚上";$("qCampus").value="综合楼";$("qPeople").value="1";$("qMode").value="晚自习模式";$("pPlug").checked=true;$("pQuiet").checked=true;$("pAC").checked=false;$("pDorm").checked=false;toggleCT();}
  doSearch();
}

// === BIND EVENTS ===
$("loginBtn").addEventListener("click", doLogin);
$("logoutBtn").addEventListener("click", doLogout);
$("searchBtn").addEventListener("click", doSearch);
$("qPeriod").addEventListener("change", toggleCT);
$("demoBtn1").addEventListener("click", function(){runDemo(1)});
$("demoBtn2").addEventListener("click", function(){runDemo(2)});
$("demoBtn3").addEventListener("click", function(){runDemo(3)});
$("switchToStudentBtn").addEventListener("click", goStudent);

// Enter key login
$("loginUser").addEventListener("keydown", function(e){if(e.key==="Enter")doLogin();});
$("loginPass").addEventListener("keydown", function(e){if(e.key==="Enter")doLogin();});

})();
