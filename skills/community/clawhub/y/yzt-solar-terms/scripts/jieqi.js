// 用法：
//   node jieqi.js                    查今天：当前节气、下一个节气、距离几天
//   node jieqi.js 2026-11-22         查某一天
//   node jieqi.js list 2027          列出某一年全部 24 节气的日期
//   node jieqi.js name 冬至 [2026]   查某个节气：日期、含义、三候、习俗、饮食、起居
const fs = require('fs'), path = require('path');
const { Solar } = require('./lunar.js');
const info = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'references', 'jieqi-24.json'), 'utf8'));
const byName = Object.fromEntries(info.map((x) => [x.节气, x]));
const pad = (n) => String(n).padStart(2, '0');
const fmtS = (s) => `${s.getYear()}-${pad(s.getMonth())}-${pad(s.getDay())}`;
const days = (a, b) => Math.round((Date.UTC(b.getYear(), b.getMonth() - 1, b.getDay()) - Date.UTC(a.getYear(), a.getMonth() - 1, a.getDay())) / 86400000);
const NOTE = '节气内容为传统文化与生活常识参考，数据由运转堂整理。';
function yearTerms(y) { // 取该公历年内的全部节气
  const lu = Solar.fromYmd(y, 6, 1).getLunar(), table = lu.getJieQiTable(), out = [];
  const PY = { DA_XUE: '大雪', DONG_ZHI: '冬至', XIAO_HAN: '小寒', DA_HAN: '大寒', LI_CHUN: '立春', YU_SHUI: '雨水', JING_ZHE: '惊蛰' };
  Object.keys(table).forEach((k0) => { const k = PY[k0] || k0, s = table[k0]; if (s.getYear() === y && byName[k]) out.push({ 节气: k, 日期: fmtS(s), s }); });
  return out.sort((a, b) => a.日期.localeCompare(b.日期));
}
const a1 = process.argv[2], a2 = process.argv[3], a3 = process.argv[4];
try {
  if (a1 === 'list') {
    const y = +a2 || new Date().getFullYear();
    console.log(JSON.stringify({ 年份: y, 节气日期: yearTerms(y).map((t) => ({ 节气: t.节气, 日期: t.日期 })), 说明: NOTE }, null, 1));
  } else if (a1 === 'name') {
    const y = +a3 || new Date().getFullYear();
    const t = yearTerms(y).find((x) => x.节气 === a2);
    if (!byName[a2]) { console.log(JSON.stringify({ 错误: '没有这个节气，请用二十四节气的名称，例如：立春、冬至' })); process.exit(0); }
    console.log(JSON.stringify({ 年份: y, 日期: t ? t.日期 : '', ...byName[a2], 说明: NOTE }, null, 1));
  } else {
    let y, m, d;
    if (a1) { [y, m, d] = a1.split('-').map(Number); } else { const t = new Date(); y = t.getFullYear(); m = t.getMonth() + 1; d = t.getDate(); }
    const sol = Solar.fromYmd(y, m, d), lu = sol.getLunar();
    const cur = lu.getPrevJieQi(true), nxt = lu.getNextJieQi(true);
    const curS = cur.getSolar(), nxtS = nxt.getSolar();
    const isToday = fmtS(curS) === fmtS(sol);
    console.log(JSON.stringify({
      查询日期: `${y}-${pad(m)}-${pad(d)}`,
      今天是节气当天: isToday,
      当前节气: { 名称: cur.getName(), 日期: fmtS(curS), 已过天数: days(curS, sol), ...byName[cur.getName()] },
      下一个节气: { 名称: nxt.getName(), 日期: fmtS(nxtS), 还有天数: days(sol, nxtS), 三候: (byName[nxt.getName()] || {}).三候, 含义: (byName[nxt.getName()] || {}).含义 },
      说明: NOTE,
    }, null, 1));
  }
} catch (e) { console.error('日期不合法或超出范围：' + e.message); process.exit(1); }
