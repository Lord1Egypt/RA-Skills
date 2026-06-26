#!/usr/bin/env node
/** SETUP – Interactive installer for SecondMind. Created by Emphaiser. */
const path=require('path'),fs=require('fs'),os=require('os'),{execSync}=require('child_process');
const BASE=path.resolve(__dirname),DATA=path.join(BASE,'data'),DBPATH=path.join(DATA,'secondmind.db');
const CFGPATH=path.join(BASE,'config.json'),SCHEMAPATH=path.join(BASE,'templates','schema.sql');

async function main() {
  const isReset = process.argv.includes('--reset');
  console.log('🧠 SecondMind Setup\n');
  if (isReset) {
    console.log('⚠️  RESET – Recreating database.\n');
    try{fs.unlinkSync(DBPATH)}catch{} try{fs.unlinkSync(DBPATH+'-wal')}catch{} try{fs.unlinkSync(DBPATH+'-shm')}catch{}
  }

  console.log('1️⃣  Dependencies...');
  checkBin('node','Required'); checkBin('sqlite3','Optional, for manual inspection');
  console.log();

  console.log('2️⃣  npm install...');
  if (!fs.existsSync(path.join(BASE,'node_modules','better-sqlite3'))) {
    try { execSync('npm install --production',{cwd:BASE,stdio:'inherit'}); }
    catch { console.error('❌ npm install failed'); process.exit(1); }
  } else console.log('   Already installed.');
  console.log();

  console.log('3️⃣  Database...');
  fs.mkdirSync(DATA,{recursive:true});
  const Database=require('better-sqlite3');
  const db=new Database(DBPATH); db.pragma('journal_mode=WAL'); db.pragma('foreign_keys=ON');
  db.exec(fs.readFileSync(SCHEMAPATH,'utf8')); db.close();
  console.log(`   ✅ ${DBPATH}\n`);

  console.log('4️⃣  Configuration...');
  if (fs.existsSync(CFGPATH) && !isReset) {
    console.log('   Config exists, keeping it.');
  } else {
    const ex=JSON.parse(fs.readFileSync(path.join(BASE,'config.example.json'),'utf8'));
    const clean=JSON.parse(JSON.stringify(ex));
    for (const k of Object.keys(clean)) if(k.startsWith('_')) delete clean[k];
    for (const s of Object.values(clean)) if(typeof s==='object'&&s) for(const k of Object.keys(s)) if(k.startsWith('_')) delete s[k];
    fs.writeFileSync(CFGPATH, JSON.stringify(clean,null,2));
    console.log(`   ✅ Created: ${CFGPATH}`);
    console.log('   ⚠️  Add your OpenRouter API key!');
    console.log('   All models (LLM + Embeddings) run via OpenRouter Cloud.');
  }
  console.log();

  console.log('5️⃣  Cron jobs...');
  const scripts=path.join(BASE,'scripts');
  if (os.platform()==='win32') setupWin(scripts); else setupLinux(scripts);
  console.log();

  const home=os.homedir(), sessDir=path.join(home,'.openclaw','agents','main','sessions');
  console.log('6️⃣  OpenClaw sessions...');
  if (fs.existsSync(sessDir)) {
    const n=fs.readdirSync(sessDir).filter(f=>f.endsWith('.jsonl')).length;
    console.log(`   ✅ ${n} transcript(s) found`);
  } else console.log(`   ⚠️  Not found: ${sessDir} – check openclaw.agentId in config.json`);
  console.log();

  console.log('═══════════════════════════════════════');
  console.log('🎉 Ready!\n');
  console.log('Next:');
  console.log(`  1. nano ${CFGPATH}  → Add OpenRouter key + Telegram`);
  console.log('  2. node scripts/ingest.js  → Test ingest');
  console.log('  3. node scripts/status.js  → Health check');
  console.log(`  4. Optional: node ${path.join(scripts,'session-watcher.js')}`);
  console.log('═══════════════════════════════════════');
}

function setupLinux(scripts) {
  const base=path.resolve(scripts,'..');
  const nodePath=process.execPath; // Use actual Node binary, NVM-safe
  const crons=[
    `*/30 * * * * cd ${base} && ${nodePath} scripts/ingest.js >> /tmp/secondmind-ingest.log 2>&1`,
    `15 */6 * * * cd ${base} && ${nodePath} scripts/consolidate.js >> /tmp/secondmind-consolidate.log 2>&1`,
    `0 3 * * * cd ${base} && ${nodePath} scripts/archive.js >> /tmp/secondmind-archive.log 2>&1`,
    `45 */6 * * * cd ${base} && ${nodePath} scripts/initiative.js >> /tmp/secondmind-initiative.log 2>&1`,
  ];
  try {
    let ex=''; try{ex=execSync('crontab -l 2>/dev/null',{encoding:'utf8'})}catch{}
    const filtered=ex.split('\n').filter(l=>!l.includes('secondmind-')&&!l.includes('secondmind')).filter(l=>l.trim()).join('\n');
    const nc=filtered+'\n\n# ── SecondMind ──\n'+crons.join('\n')+'\n';
    fs.writeFileSync('/tmp/secondmind-crontab',nc); execSync('crontab /tmp/secondmind-crontab'); fs.unlinkSync('/tmp/secondmind-crontab');
    console.log(`   ✅ ${crons.length} cron jobs installed`);
  } catch(e) { console.error('   ❌',e.message); }
}

function setupWin(scripts) {
  const node=process.execPath;
  [{name:'Eigen-Ingest',s:'ingest.js',m:30},{name:'Eigen-Consolidate',s:'consolidate.js',m:360},{name:'Eigen-Archive',s:'archive.js',d:'03:00'},{name:'Eigen-Initiative',s:'initiative.js',m:360}].forEach(t=>{
    const cmd=`"${node}" "${path.join(scripts,t.s)}"`;
    try{execSync(`schtasks /Delete /TN "${t.name}" /F 2>nul`,{stdio:'ignore'})}catch{}
    try{
      if(t.d) execSync(`schtasks /Create /TN "${t.name}" /TR ${cmd} /SC DAILY /ST ${t.d} /F`);
      else execSync(`schtasks /Create /TN "${t.name}" /TR ${cmd} /SC MINUTE /MO ${t.m} /F`);
      console.log(`   ✅ ${t.name}`);
    }catch(e){console.error(`   ❌ ${t.name}: ${e.message}`);}
  });
}

function checkBin(name,note) {
  try{execSync(os.platform()==='win32'?`where ${name} 2>nul`:`which ${name} 2>/dev/null`,{stdio:'ignore'}); console.log(`   ✅ ${name}`); return true;}
  catch{console.log(`   ⚠️  ${name} – ${note}`); return false;}
}
main().catch(e=>{console.error(e);process.exit(1);});
