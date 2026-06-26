#!/usr/bin/env node
/**
 * todolist Skill – 简单的命令行待办管理
 */
const { Command } = require('commander');
const fs = require('fs');
const path = require('path');
const os = require('os');

const BASE_DIR = path.join(os.homedir(), '.tasktodolist');

const program = new Command();
program.name('tasktodolist').description('简易待办管理').version('1.0.0');
program.option('-t, --task <name>', '指定任务名称 (默认为 default)', 'default');

function getTaskName() { return program.opts().task || 'default'; }
function getDataFile() { return path.join(BASE_DIR, `${getTaskName()}_tasktodolist.json`); }

function ensureDataFile(){
  const dataFile = getDataFile();
  const dir = path.dirname(dataFile);
  if(!fs.existsSync(dir)) fs.mkdirSync(dir,{recursive:true});
  if(!fs.existsSync(dataFile)) fs.writeFileSync(dataFile,'[]','utf8');
}
function loadTodos(){
  ensureDataFile();
  try{ return JSON.parse(fs.readFileSync(getDataFile(),'utf8')); }
  catch(e){ return []; }
}
function saveTodos(t){ fs.writeFileSync(getDataFile(), JSON.stringify(t,null,2),'utf8'); }
function print(t){
  const taskName = getTaskName();
  if(t.length===0){ console.log(`🗒️ [${taskName}] 当前没有待办事项。`); return; }
  console.log(`🗒️ [${taskName}] 待办列表:`);
  t.forEach((it,i)=>{ const s=it.done?'✅':'🔲'; console.log(`${i+1}. ${s} ${it.text}`); });
}

program.command('add <text...>').description('添加待办项目').action(txt=>{ const todos=loadTodos(); const item={id:Date.now(), text:txt.join(' '), done:false}; todos.push(item); saveTodos(todos); console.log(`✅ 已添加到 [${getTaskName()}]: "${item.text}"`);});
program.command('list').description('列出当前任务的待办项目').action(()=>{ print(loadTodos());});
program.command('done <num>').description('标记完成').action(num=>{ const i=Number(num)-1; const todos=loadTodos(); if(i<0||i>=todos.length){ console.error('❌ 序号超出范围'); process.exit(1);} todos[i].done=true; saveTodos(todos); console.log(`✅ [${getTaskName()}] 第 ${num} 条已标记为完成`);});
program.command('rm <num>').description('删除待办项目').action(num=>{ const i=Number(num)-1; const todos=loadTodos(); if(i<0||i>=todos.length){ console.error('❌ 序号超出范围'); process.exit(1);} const r=todos.splice(i,1)[0]; saveTodos(todos); console.log(`🗑️ [${getTaskName()}] 已删除: "${r.text}"`);});
program.command('clear').description('清除当前任务中已完成的项目').action(()=>{ const todos=loadTodos(); const before=todos.length; const kept=todos.filter(it=>!it.done); saveTodos(kept); console.log(`🧹 [${getTaskName()}] 已清理 ${before-kept.length} 条已完成的待办`);});

const tasks = program.command('tasks').description('管理任务列表');
tasks.command('list').description('列出所有任务列表').action(() => {
  if (!fs.existsSync(BASE_DIR)) { console.log('🗒️ 尚未创建任何任务。'); return; }
  const files = fs.readdirSync(BASE_DIR);
  const taskNames = files
    .filter(f => f.endsWith('_tasktodolist.json'))
    .map(f => f.replace('_tasktodolist.json', ''));
  
  if (taskNames.length === 0) { console.log('🗒️ 尚未创建任何任务。'); return; }
  console.log('📂 现有任务列表:');
  taskNames.forEach((n, i) => console.log(`${i + 1}. ${n}${n === getTaskName() ? ' (当前)' : ''}`));
});

tasks.command('rm <name>').description('删除指定任务列表').action(name => {
  const dataFile = path.join(BASE_DIR, `${name}_tasktodolist.json`);
  if (fs.existsSync(dataFile)) {
    fs.unlinkSync(dataFile);
    console.log(`🗑️ 已删除任务列表: [${name}]`);
  } else {
    console.error(`❌ 找不到任务列表: [${name}]`);
  }
});

program.parse(process.argv);
