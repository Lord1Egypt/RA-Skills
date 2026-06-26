// Simple session-store for workflow-runner (file-backed)
const fs = require('fs');
const path = require('path');
const STORE = path.join(process.cwd(), 'skills', 'workflow-runner', 'session-store.json');

function load(){
  try{ return JSON.parse(fs.readFileSync(STORE,'utf8')); }catch(e){ return {}; }
}
function save(s){ fs.writeFileSync(STORE, JSON.stringify(s, null, 2)); }

module.exports = {
  getAll: () => load(),
  get: (k) => load()[k],
  set: (k, v) => { const s = load(); s[k]=v; save(s); },
  del: (k) => { const s = load(); delete s[k]; save(s); }
};
