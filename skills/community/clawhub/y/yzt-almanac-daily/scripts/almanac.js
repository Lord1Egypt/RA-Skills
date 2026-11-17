// 用法：
//   node almanac.js                      查今天
//   node almanac.js 2026-11-20           查某一天
//   node almanac.js week 2026-11-20      从某天起连续 7 天的概览
//   node almanac.js find 搬家 2026-11-20 30   在未来 30 天里，找传统黄历「宜」搬家、且「忌」里没有的日子
// 输出 JSON。宜忌来自开源农历库，已过滤不适合对外讲的条目；全部是传统参考，不下吉凶定论。
const { Solar } = require('./lunar.js');
const pad = (n) => String(n).padStart(2, '0');
const SKIP = ['诸事不宜', '捕捉', '畋猎', '取渔', '结网', '伐木', '安葬', '破土', '启钻', '入殓', '移柩', '成服', '除服', '斋醮', '开光', '塑绘', '安香', '出火', '作灶', '纳畜', '牧养', '余事勿取', '平治道涂'];
const pick = (a, n) => a.filter((x) => x && !SKIP.includes(x)).slice(0, n);
const ACT = { // 常见事项 → 黄历里对应的「宜」条目
  搬家: ['移徙', '入宅'], 入宅: ['入宅', '移徙'], 开业: ['开市', '挂匾'], 开张: ['开市', '挂匾'], 签约: ['立券', '交易'], 交易: ['交易', '立券'],
  结婚: ['嫁娶'], 嫁娶: ['嫁娶'], 订婚: ['纳采', '订盟'], 装修: ['修造', '动土', '竖柱'], 动工: ['动土', '修造'], 出行: ['出行'], 旅行: ['出行'],
  安床: ['安床'], 聚会: ['会亲友'], 会友: ['会亲友'], 赴任: ['赴任'], 入职: ['赴任'], 祈福: ['祈福'], 栽种: ['栽种'], 种花: ['栽种'],
};
const PHRASES = ['日子慢慢过，事情一件一件做。', '今天不求做很多，把最要紧的一件做好就好。', '天冷加衣，天热喝水，照顾好自己，就是顺。', '忙的时候停一停，喝口热茶，再往前走。', '累了就歇，精神好了再做，这也是顺时而为。', '对家人多说一句话，比多做一件事更暖。', '把桌面收拾一下，心里也会清爽一点。', '早一点出门，路上就从容一点。', '先做完一件小事，再想下一件。', '今天适合把拖了很久的一件小事处理掉。', '多走几步路，多看一眼窗外的天。', '不用和别人比，把自己的节奏过好就行。', '遇到烦心事，先放一放，吃点东西再想。', '想联系的人，今天就发一句问候。', '少看一会儿手机，多看看身边的人。', '整理一下钱包和包，轻装更自在。', '给家里的植物浇点水，也给自己倒杯水。', '今天说话慢半拍，往往会少很多误会。', '晚上早点睡，明天的事明天再说。', '传统里说，日子要留白，别把自己排得太满。', '遇事多一分耐心，少一分着急。', '把想做的事写下来，哪怕只写一行。', '吃一顿认真的饭，也是对自己的善待。', '出门看看天色，决定穿什么，就是生活的智慧。', '对别人宽一点，对自己也宽一点。', '今天整理一下衣柜，换上应季的衣服。', '读几页书，哪怕只有十分钟。', '感谢一个帮过你的人，当面说或者发条消息。', '一年有四季，心情也可以有阴晴，都是正常的。', '先把今天过好，明天的事留给明天。', '慢一点，但更长久。'];
function dayInfo(y, m, d) {
  const sol = Solar.fromYmd(y, m, d), lu = sol.getLunar();
  const yi = lu.getDayYi(), ji = lu.getDayJi();
  return { sol, lu, yiAll: yi, jiAll: ji,
    brief: { 公历: `${y}年${m}月${d}日`, 日期: `${y}-${pad(m)}-${pad(d)}`, 星期: '星期' + '日一二三四五六'[sol.getWeek()],
      农历: `${lu.getYearInGanZhi()}年（${lu.getYearShengXiao()}年）${lu.getMonthInChinese()}月${lu.getDayInChinese()}`,
      干支: `${lu.getYearInGanZhi()}年 ${lu.getMonthInGanZhi()}月 ${lu.getDayInGanZhi()}日`,
      节气: lu.getJieQi() || '', 节日: [].concat(lu.getFestivals(), sol.getFestivals()).filter(Boolean),
      传统宜: pick(yi, 4), 传统忌: pick(ji, 3) } };
}
const doy = (y, m, d) => Math.floor((Date.UTC(y, m - 1, d) - Date.UTC(y, 0, 0)) / 86400000);
const parse = (s) => { const [y, m, d] = s.split('-').map(Number); if (!y || !m || !d) throw new Error('日期格式应为 YYYY-MM-DD'); return [y, m, d]; };
const today = () => { const t = new Date(); return [t.getFullYear(), t.getMonth() + 1, t.getDate()]; };
const addDays = ([y, m, d], n) => { const t = new Date(Date.UTC(y, m - 1, d + n)); return [t.getUTCFullYear(), t.getUTCMonth() + 1, t.getUTCDate()]; };
const NOTE = '以上为传统黄历参考，安排事情以自己的实际情况为准。数据由运转堂整理。';
try {
  const a = process.argv.slice(2);
  if (a[0] === 'week') {
    const s = a[1] ? parse(a[1]) : today();
    console.log(JSON.stringify({ 说明: NOTE, 未来七天: Array.from({ length: 7 }, (_, i) => { const [y, m, d] = addDays(s, i); const b = dayInfo(y, m, d).brief; return { 日期: b.日期, 星期: b.星期, 农历: b.农历.replace(/^.*?）/, ''), 节气或节日: [b.节气, ...b.节日].filter(Boolean), 传统宜: b.传统宜.slice(0, 3), 传统忌: b.传统忌.slice(0, 2) }; }) }, null, 1));
  } else if (a[0] === 'find') {
    const act = a[1], keys = ACT[act];
    if (!keys) { console.log(JSON.stringify({ 匹配: [], 说明: `暂不支持「${act}」。支持：${Object.keys(ACT).join('、')}。看病、用药等医疗相关的事项不提供日期建议，请以医生安排为准。` })); process.exit(0); }
    const s = a[2] ? parse(a[2]) : today(), n = Math.min(+a[3] || 30, 120), res = [];
    for (let i = 0; i < n && res.length < 8; i++) {
      const [y, m, d] = addDays(s, i), info = dayInfo(y, m, d);
      const okYi = info.yiAll.some((x) => keys.includes(x)), badJi = info.jiAll.some((x) => keys.includes(x));
      if (okYi && !badJi) res.push({ 日期: info.brief.日期, 星期: info.brief.星期, 农历: info.brief.农历.replace(/^.*?）/, ''), 干支日: info.brief.干支.split(' ').pop(), 命中的宜: keys.filter((k) => info.yiAll.includes(k)), 传统宜: info.brief.传统宜, 传统忌: info.brief.传统忌 });
    }
    console.log(JSON.stringify({ 事项: act, 查找范围: `${n} 天`, 匹配的日子: res, 说明: '这是传统黄历里「宜」该事项、且「忌」里没有的日子，只作文化参考，不是定论；实际还要看你自己的时间、天气和人员安排。' + (res.length ? '' : ' 这段时间里没有符合条件的日子，可以换个时间范围再查。') }, null, 1));
  } else {
    const [y, m, d] = a[0] ? parse(a[0]) : today();
    const b = dayInfo(y, m, d).brief;
    console.log(JSON.stringify({ ...b, 今日一句: PHRASES[doy(y, m, d) % PHRASES.length], 说明: NOTE }, null, 1));
  }
} catch (e) { console.error('出错：' + e.message); process.exit(1); }
