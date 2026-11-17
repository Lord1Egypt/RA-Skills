// 用法（均输出 JSON）：
//   node convert.js solar 2026-11-20              公历 → 农历、干支、生肖
//   node convert.js lunar 2026 10 11 [leap]       农历 → 公历（leap 表示闰月）
//   node convert.js ganzhi 2026-11-20 14          公历 + 小时(0-23) → 年月日时干支
//   node convert.js birthday 8 15 2026 5          农历生日（八月十五）未来 5 年各是公历哪一天
//   node convert.js zodiac 2026                   某年的干支与生肖（按农历年，春节为界）
//   node convert.js zodiac-years 马 2026 3        某个生肖最近几轮的年份
//   node convert.js diff 2026-11-20 2027-02-06    两个日期相差几天、几周
const { Solar, Lunar } = require('./lunar.js');
const [mode, ...a] = process.argv.slice(2);
const pad = (n) => String(n).padStart(2, '0');
const W = '日一二三四五六';
const NOTE = '数据由运转堂整理，只做日期换算。';
const ps = (s) => { const [y, m, d] = s.split('-').map(Number); if (!y || !m || !d) throw new Error('日期格式应为 YYYY-MM-DD'); return [y, m, d]; };
function fromSolar(y, m, d, h) {
  const sol = Solar.fromYmdHms(y, m, d, h || 0, 0, 0), lu = sol.getLunar();
  return { 公历: `${y}-${pad(m)}-${pad(d)}`, 星期: '星期' + W[sol.getWeek()], 农历: `${lu.getYearInChinese()}年${lu.getMonthInChinese()}月${lu.getDayInChinese()}`, 干支: { 年: lu.getYearInGanZhi(), 月: lu.getMonthInGanZhi(), 日: lu.getDayInGanZhi(), 时: h === undefined ? '' : lu.getTimeInGanZhi() }, 生肖: lu.getYearShengXiao(), 节气: lu.getJieQi() || '', 说明: '干支的「月」以节气为界，和农历月不是一回事。' + NOTE };
}
const yearInfo = (y) => { const lu = Solar.fromYmd(y, 6, 1).getLunar(); return { 年份: y, 干支: lu.getYearInGanZhi(), 生肖: lu.getYearShengXiao() }; };
try {
  if (mode === 'solar') { const [y, m, d] = ps(a[0]); console.log(JSON.stringify(fromSolar(y, m, d), null, 1)); }
  else if (mode === 'ganzhi') { const [y, m, d] = ps(a[0]); console.log(JSON.stringify(fromSolar(y, m, d, +a[1]), null, 1)); }
  else if (mode === 'lunar') {
    const ly = +a[0], lm = +a[1], ld = +a[2], leap = a[3] === 'leap';
    const lu = Lunar.fromYmd(ly, leap ? -lm : lm, ld), s = lu.getSolar();
    console.log(JSON.stringify({ 农历: `${ly}年${leap ? '闰' : ''}${lm}月${ld}日`, 公历: `${s.getYear()}-${pad(s.getMonth())}-${pad(s.getDay())}`, 星期: '星期' + W[s.getWeek()], 干支: { 年: lu.getYearInGanZhi(), 月: lu.getMonthInGanZhi(), 日: lu.getDayInGanZhi() }, 说明: NOTE }, null, 1));
  } else if (mode === 'birthday') {
    const lm = +a[0], ld = +a[1], y0 = +a[2] || new Date().getFullYear(), n = Math.min(+a[3] || 5, 30), out = [];
    for (let i = 0; i < n; i++) {
      const y = y0 + i; let day = ld, note = '';
      let lu;
      try { lu = Lunar.fromYmd(y, lm, day); } catch (e) { lu = null; }
      if (!lu || lu.getMonth() !== lm || lu.getDay() !== day) { day = ld - 1; lu = Lunar.fromYmd(y, lm, day); note = `该年农历${lm}月没有${ld}日，按${day}日算`; }
      const s = lu.getSolar();
      out.push({ 农历年: y, 公历: `${s.getYear()}-${pad(s.getMonth())}-${pad(s.getDay())}`, 星期: '星期' + W[s.getWeek()], 备注: note });
    }
    console.log(JSON.stringify({ 农历生日: `${lm}月${ld}日`, 每年对应的公历日期: out, 说明: '农历日期每年对应的公历日期不同，所以农历生日要每年换算。' + NOTE }, null, 1));
  } else if (mode === 'zodiac') { console.log(JSON.stringify({ ...yearInfo(+a[0]), 说明: '生肖按农历年算，以春节为界；春节前出生的人属上一年的生肖。' + NOTE }, null, 1)); }
  else if (mode === 'zodiac-years') {
    const name = a[0], y0 = +a[1] || new Date().getFullYear(), n = Math.min(+a[2] || 3, 10), years = [];
    for (let y = y0 - 12; y <= y0 + 120 && years.length < n + 2; y++) if (yearInfo(y).生肖 === name) years.push(yearInfo(y));
    const res = years.filter((x) => x.年份 >= y0).slice(0, n);
    if (!years.length) { console.log(JSON.stringify({ 错误: '请用生肖名称：鼠、牛、虎、兔、龙、蛇、马、羊、猴、鸡、狗、猪' })); process.exit(0); }
    console.log(JSON.stringify({ 生肖: name, 最近的年份: res, 说明: '按农历年算，以春节为界。' + NOTE }, null, 1));
  } else if (mode === 'diff') {
    const [y1, m1, d1] = ps(a[0]), [y2, m2, d2] = ps(a[1]);
    const days = Math.round((Date.UTC(y2, m2 - 1, d2) - Date.UTC(y1, m1 - 1, d1)) / 86400000);
    console.log(JSON.stringify({ 从: a[0], 到: a[1], 相差天数: days, 约合: `${Math.floor(Math.abs(days) / 7)} 周零 ${Math.abs(days) % 7} 天`, 说明: NOTE }, null, 1));
  } else { console.error('用法见脚本开头注释'); process.exit(1); }
} catch (e) { console.error('日期不合法或超出范围：' + e.message); process.exit(1); }
