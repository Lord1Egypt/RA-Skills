# Report template

The page `/todo-report` writes to `docs/status.html`. Copy the HTML below exactly, replacing only the four placeholders (see SKILL.md). It is generated output for the user's project: the plugin does not run it, and the page loads nothing from the network. `tools/template.html` in the todo-skills repository holds the same text (a test keeps them identical).

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'">
<title>Project status</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1c2230;--mute:#5d6676;--line:#dde1e8;--acc:#2f6fed;--ok:#1f9d55;--act:#2f6fed;--blk:#d64545;--open:#8a93a3}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#12151c;--card:#1b2029;--ink:#e6e9ef;--mute:#98a1b1;--line:#2b3240;--acc:#6b9bff;--ok:#43c47a;--act:#6b9bff;--blk:#ff7b7b;--open:#7d8798}}
:root[data-theme=dark]{--bg:#12151c;--card:#1b2029;--ink:#e6e9ef;--mute:#98a1b1;--line:#2b3240;--acc:#6b9bff;--ok:#43c47a;--act:#6b9bff;--blk:#ff7b7b;--open:#7d8798}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
header{padding:20px 16px 8px;max-width:1100px;margin:0 auto}h1{margin:0;font-size:22px}.sub{color:var(--mute);font-size:13px}
main{max-width:1100px;margin:0 auto;padding:8px 16px 40px;display:grid;gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);margin:0 0 10px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.kpi b{display:block;font-size:24px}.kpi span{color:var(--mute);font-size:12px}
.prog{margin:12px 0 0;font:13px/1.5 ui-monospace,monospace;color:var(--mute);word-break:break-word}.prog .bar{margin-top:6px}
.bar{height:8px;background:var(--line);border-radius:4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--ok)}
.lanes{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.lane{border:1px solid var(--line);border-radius:8px;padding:10px;cursor:pointer}.lane.on{outline:2px solid var(--acc)}
.lane h3{margin:0 0 4px;font-size:15px}.lane small{color:var(--mute)}
.tools{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}
input,select,button{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:6px;padding:5px 8px}button{cursor:pointer}
ul.tree{list-style:none;margin:0;padding-left:18px}ul.tree.top{padding-left:0}
.node>.row{display:flex;gap:8px;align-items:baseline;padding:4px 6px;border-radius:6px;cursor:pointer}.node>.row:hover{background:var(--bg)}
.mk{font-family:ui-monospace,monospace;font-weight:700;min-width:2.2em}.mk.x{color:var(--ok)}.mk.s{color:var(--act)}.mk.b{color:var(--blk)}.mk.o{color:var(--open)}
.id{font-family:ui-monospace,monospace;font-size:13px}.tag{font-size:11px;border:1px solid var(--line);border-radius:10px;padding:0 7px;color:var(--mute)}
.det{margin:2px 0 6px 40px;padding:8px 10px;border-left:3px solid var(--line);color:var(--mute);font-size:13px;display:none;word-break:break-word}.det.show{display:block}
.det div{margin:2px 0}.det b{color:var(--ink)}code{font-family:ui-monospace,monospace;background:var(--bg);padding:1px 5px;border-radius:4px}
.hist h3{margin:12px 0 4px;font-size:15px}.hist li{margin:3px 0}
dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:0}dt{color:var(--mute)}dd{margin:0;word-break:break-word}
pre{white-space:pre-wrap;margin:0;font:13px/1.5 ui-monospace,monospace}.empty{color:var(--mute)}
</style>
</head>
<body>
<header><h1 id="title">Project status</h1><div class="sub" id="sub"></div></header>
<main>
<section class="card"><div class="kpis" id="kpis"></div><div class="prog"><span id="progress"></span><div class="bar" id="progbar"><i></i></div></div></section>
<section class="card"><h2>Lanes <span class="tag" id="lanehint">click to filter</span></h2><div class="lanes" id="lanes"></div></section>
<section class="card"><h2>Task tree</h2>
<div class="tools"><input id="q" placeholder="Search id, title, command" size="26"><select id="st"><option value="">All statuses</option><option value="open">Open</option><option value="active">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option></select><button id="exp">Expand all</button><button id="theme">Theme</button></div>
<ul class="tree top" id="tree"></ul></section>
<section class="card hist"><h2>History (CHANGELOG.md)</h2><div id="hist"></div></section>
<section class="card"><h2>Project</h2><dl id="meta"></dl></section>
<section class="card" id="plancard"><h2>Plan</h2><pre id="plan"></pre></section>
</main>
<script type="text/plain" id="d-meta">__META__</script>
<script type="text/plain" id="d-todo">__TODO__</script>
<script type="text/plain" id="d-changelog">__CHANGELOG__</script>
<script type="text/plain" id="d-plan">__PLAN__</script>
<script>
const $=id=>document.getElementById(id),raw=id=>$(id).textContent.replace(/^\n/,'').replace(/&lt;/g,'<').replace(/&amp;/g,'&').replace(/\r/g,'');
const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
const meta={},metaList=[];
raw('d-meta').split('\n').forEach(l=>{const m=l.match(/^([\w ]+): (.*)$/);if(m){meta[m[1].trim()]=m[2];metaList.push([m[1].trim(),m[2]])}});
// ---- parse TODO.md
const nodes=[],stack=[];
const hdr=/^(\s*)- \[(.)\] \*\*([A-Z]+-\d+(?:\.\d+)*)\*\* · (.*)$/;
raw('d-todo').split('\n').forEach(l=>{
  let m=l.match(hdr);
  if(m){const lvl=m[1].length/2,p=m[4].split(' · ');let pri='',size;
    if(lvl===0){pri=p.shift()}size=p.shift();
    const n={id:m[3],mk:m[2],lvl,pri,size,title:p.join(' · '),f:{},kids:[],par:null};
    stack.length=lvl;n.par=lvl?stack[lvl-1]:null;if(n.par)n.par.kids.push(n);stack[lvl]=n;nodes.push(n);return}
  m=l.match(/^\s+- (Done when|Links|State|Blocked): (.*)$/);
  if(m&&stack.length)stack[stack.length-1].f[m[1]]=m[2];
});
const roots=nodes.filter(n=>!n.par);
roots.forEach(r=>{const lm=(r.f.Links||'').match(/Lane: ([a-z0-9-]+)/);r.lane=lm?lm[1]:'main'});
const laneOf=n=>{while(n.par)n=n.par;return n.lane};
const status=n=>n.mk==='x'?'done':n.mk==='/'?'active':n.mk==='!'?'blocked':'open';
const desc=n=>n.kids.reduce((a,k)=>a.concat(k,desc(k)),[]);
const prog=n=>{const d=desc(n);if(!d.length)return n.mk==='x'?1:0;return d.filter(x=>x.mk==='x').length/d.length};
// ---- history
const hist=[];let cur=null,grp='';
raw('d-changelog').split('\n').forEach(l=>{
  let m=l.match(/^## \[(.+?)\](?: - (.+))?/);if(m){cur={ver:m[1],date:m[2]||'',items:[]};hist.push(cur);return}
  m=l.match(/^### (.+)/);if(m){grp=m[1];return}
  if(cur&&/^- /.test(l))cur.items.push({g:grp,t:l.slice(2)});
});
// ---- progress: the same line as `todo-lint.sh --progress` (FEAT-042); change both together
function progressLine(todo,changelog){
  const ns=[],idre=/[A-Z]+-\d+(?:\.\d+)*/g;
  todo.replace(/\r/g,'').split('\n').forEach(l=>{const m=l.match(/^( *)- \[(.)\] \*\*[A-Z]+-\d+(?:\.\d+)*\*\*/);if(m)ns.push({lv:m[1].length/2,mk:m[2]})});
  let leaves=0,done=0,blocked=0,active=0,roots=0,on=false,dr=0,dl=0;
  ns.forEach((n,i)=>{if(!n.lv)roots++;if(n.mk==='/')active++;
    if(i===ns.length-1||ns[i+1].lv<=n.lv){leaves++;if(n.mk==='x')done++;if(n.mk==='!')blocked++}});
  (changelog||'').replace(/\r/g,'').split('\n').forEach(l=>{
    if(/^## \[Unreleased\]/.test(l)){on=true;return}if(/^## /.test(l)){on=false;return}
    if(!on||!/^- \*\*[A-Z]+-\d+(?:\.\d+)*\*\*/.test(l))return;dr++;
    const p=l.indexOf('Includes:'),ids=p<0?[]:(l.slice(p+9).match(idre)||[]);
    dl+=ids.length?ids.filter(a=>!ids.some(b=>b.startsWith(a+'.'))).length:1});
  const total=leaves+dl,d=done+dl;let nd=0,nb=0;
  if(total>0){nd=Math.floor(10*d/total);nb=Math.floor(10*blocked/total+0.5);if(blocked>0&&nb<1)nb=1;if(nb>10-nd)nb=10-nd}
  return 'Progress: ['+'#'.repeat(nd)+'!'.repeat(nb)+'-'.repeat(10-nd-nb)+'] '+d+'/'+total+' leaves · '+active+' active · '+blocked+' blocked · '+roots+' roots open · '+dr+' drained in [Unreleased]';
}
// ---- end progress
// ---- render
$('title').textContent=(meta.project||'Project')+' · status';
$('sub').textContent='Generated '+(meta.generated||'')+(meta.base?' · base '+meta.base:'')+(meta.branch?' · on '+meta.branch:'');
const all=nodes,cnt=s=>all.filter(n=>status(n)===s).length;
const leaves=all.filter(n=>!n.kids.length),doneL=leaves.filter(n=>n.mk==='x').length;
[['Roots',roots.length],['Nodes',all.length],['In progress',cnt('active')],['Blocked',cnt('blocked')],['Done in tree',cnt('done')],['Drained',hist.reduce((a,h)=>a+h.items.length,0)]]
 .forEach(([k,v])=>{const d=el('div','kpi');d.append(el('b','',v),el('span','',k));$('kpis').append(d)});
$('progress').textContent=progressLine(raw('d-todo'),raw('d-changelog'));
{const m=$('progress').textContent.match(/ (\d+)\/(\d+) leaves/);$('progbar').firstChild.style.width=(m&&+m[2]?100*m[1]/m[2]:0)+'%'}
let laneSel='';
const lanes=Object.create(null);roots.forEach(r=>(lanes[r.lane]=lanes[r.lane]||[]).push(r));
function drawLanes(){$('lanes').textContent='';
  if(!roots.length){$('lanes').append(el('div','empty','No tasks in the tree.'));return}
  Object.keys(lanes).sort().forEach(name=>{const rs=lanes[name],ds=rs.flatMap(r=>[r,...desc(r)]),dn=ds.filter(n=>n.mk==='x').length;
    const d=el('div','lane'+(laneSel===name?' on':''));d.onclick=()=>{laneSel=laneSel===name?'':name;drawLanes();drawTree()};
    d.append(el('h3','',name),el('small','',rs.length+' root'+(rs.length>1?'s':'')+' · '+ds.length+' nodes · '+ds.filter(n=>n.mk==='/').length+' active · '+ds.filter(n=>n.mk==='!').length+' blocked'));
    const b=el('div','bar');const i=el('i');i.style.width=(ds.length?100*dn/ds.length:0)+'%';b.append(i);d.append(b);$('lanes').append(d)})}
const MK={x:['[x]','x'],'/':['[/]','s'],'!':['[!]','b'],' ':['[ ]','o']};
let expandAll=false;
function nodeEl(n,q,st){
  const li=el('li','node'),row=el('div','row');
  const m=MK[n.mk]||MK[' '];row.append(el('span','mk '+m[1],m[0]),el('span','id',n.id),el('span','tag',n.size+(n.pri?' · '+n.pri:'')),el('span','',n.title));
  if(n.kids.length){const d=desc(n);row.append(el('span','tag',d.filter(x=>x.mk==='x').length+'/'+d.length+' done'))}
  const det=el('div','det'+(expandAll?' show':''));
  [['Done when','Done when'],['Links','Links'],['State','State'],['Blocked','Blocked']].forEach(([k,l])=>{if(n.f[k]){const d=el('div');d.append(el('b','',l+': '));
    const parts=n.f[k].split(/(`[^`]+`)/);parts.forEach(p=>d.append(p[0]==='`'?el('code','',p.slice(1,-1)):document.createTextNode(p)));det.append(d)}});
  if(!Object.keys(n.f).length)det.append(el('div','','No further details.'));
  row.onclick=()=>det.classList.toggle('show');li.append(row,det);
  if(n.kids.length){const ul=el('ul','tree');n.kids.forEach(k=>{const e=nodeEl(k,q,st);if(e)ul.append(e)});li.append(ul)}
  const self=(!q||(n.id+' '+n.title+' '+Object.values(n.f).join(' ')).toLowerCase().includes(q))&&(!st||status(n)===st);
  if(!self&&!li.querySelector('.node'))return null;return li}
function drawTree(){const t=$('tree');t.textContent='';const q=$('q').value.toLowerCase(),st=$('st').value;
  const rs=roots.filter(r=>!laneSel||r.lane===laneSel);let any=false;
  rs.forEach(r=>{const e=nodeEl(r,q,st);if(e){t.append(e);any=true;
    const b=el('div','bar');const i=el('i');i.style.width=(100*prog(r))+'%';b.append(i);e.insertBefore(b,e.children[1])}});
  if(!any)t.append(el('li','empty',roots.length?'Nothing matches the filter.':'The task tree is empty.'))}
$('q').oninput=drawTree;$('st').onchange=drawTree;
$('exp').onclick=()=>{expandAll=!expandAll;$('exp').textContent=expandAll?'Collapse all':'Expand all';drawTree()};
$('theme').onclick=()=>{const r=document.documentElement,d=r.dataset.theme==='dark'||(!r.dataset.theme&&matchMedia('(prefers-color-scheme:dark)').matches);r.dataset.theme=d?'light':'dark'};
// history
const H=$('hist');if(!hist.length)H.append(el('div','empty','Nothing released or drained yet.'));
hist.forEach(h=>{if(!h.items.length&&h.ver==='Unreleased')return;H.append(el('h3','',h.ver==='Unreleased'?'Unreleased':'v'+h.ver+(h.date?' · '+h.date:'')));
  const ul=el('ul');h.items.forEach(i=>{const li=el('li');li.append(el('span','tag',i.g||'-'),document.createTextNode(' '+i.t));ul.append(li)});H.append(ul)});
// meta + plan
if(!metaList.length)$('meta').append(el('dd','empty','No project details recorded.'));
metaList.forEach(([k,v])=>{if(k==='project'||k==='generated')return;$('meta').append(el('dt','',k),el('dd','',v))});
const plan=raw('d-plan').trim();if(plan&&plan!=='__'+'PLAN__')$('plan').textContent=plan;else $('plancard').style.display='none';
drawLanes();drawTree();
</script>
</body>
</html>
````
