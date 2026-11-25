import { blankMenu, blankDish, PAPER } from '../js/model.js';
import { renderMenu } from '../js/render.js';
import { inspectMenu } from '../js/inspect.js';
import { parseTextMenu } from '../js/parse.js';
import { runLocal, autoFix, autoPickSignature } from '../js/driver.js';
import { createToolset } from '../js/protocol.js';

let pass = 0, fail = 0;
const ok = (cond, label, extra = '') => {
  if (cond) { pass++; console.log('  ✓', label); }
  else { fail++; console.log('  ✗', label, extra); }
};

/* ---- 1. 长菜单触发 too-long ---- */
console.log('\n[1] 长菜单质检');
{
  const m = blankMenu({ name: '大菜单' });
  const cats = ['热菜','凉菜','主食','汤羹','饮品'];
  for (let i = 0; i < 40; i++) {
    m.dishes.push(blankDish({ section: cats[i % 5], name: `菜${i}号`, price: `${20 + i}`, blurb: '一句话说明这道菜的食材与口感特点。', kind: 'pork' }));
  }
  const L = renderMenu(m).layout;
  const r = inspectMenu(m);
  ok(L.height > PAPER.maxHeight, `40 道菜高度 ${Math.round(L.height)} 超过上限`, L.height);
  ok(r.issues.some(i => i.code === 'too-long'), '报出 too-long');
}

/* ---- 2. 导出 SVG 不含热区 ---- */
console.log('\n[2] 导出');
{
  const m = blankMenu({ name: '测试店' });
  m.dishes.push(blankDish({ name: '红烧肉', price: '68', blurb: '五花肉慢炖。', kind: 'pork' }));
  const withHit = renderMenu(m).svg;
  const clean = renderMenu(m, { hitAreas: false }).svg;
  ok(withHit.includes('vm-hit'), '预览含点击热区');
  ok(!clean.includes('vm-hit'), '导出不含热区');
  ok(clean.startsWith('<svg') && clean.includes('xmlns'), 'SVG 有根节点与命名空间');
  ok(!/<script/i.test(clean), 'SVG 无脚本');
  // 标签闭合粗检
  const open = (clean.match(/<[a-zA-Z][^>]*?(?<!\/)>/g) || []).length;
  const close = (clean.match(/<\/[a-zA-Z]+>/g) || []).length;
  ok(Math.abs(open - close) <= 2, `标签基本闭合 open=${open} close=${close}`);
}

/* ---- 3. 解析 + 端到端 ---- */
console.log('\n[3] 端到端生成');
{
  const text = `测试小馆\n【热菜】\n红烧肉 68\n宫保鸡丁 48 微辣\n麻婆豆腐 32\n【主食】\n蛋炒饭 26\n【汤】\n番茄蛋汤 18`;
  const p = parseTextMenu(text);
  ok(p.dishes.length === 5, `解析出 5 道（实际 ${p.dishes.length}）`);
  ok(p.shopName === '测试小馆', '认出店名');

  let menu = blankMenu({ name: '' });
  const ctx = {
    getMenu: () => menu,
    setMenu: (m) => { menu = m; },
    getSource: () => ({ text, dataUrl: '', width: 0, height: 0 }),
    pushEvent: () => {},
    takeEvent: () => null,
    cropSource: async () => ({ dataUrl: '', width: 0, height: 0 }),
  };
  const ts = createToolset(ctx);
  const res = await runLocal(ctx, ts, { pace: 0 });
  ok(res.ok, '生成成功');
  ok(menu.dishes.length === 5, `菜单 5 道（实际 ${menu.dishes.length}）`);
  ok(menu.dishes.some(d => d.signature), '自动标出招牌');
  ok(menu.name === '测试小馆', '店名写进菜单');
  const r = inspectMenu(menu);
  ok(r.errors === 0, `无 error（实际 ${r.errors}）`, JSON.stringify(r.issues.filter(i=>i.level==='error')));
}

/* ---- 4. 自动修复 ---- */
console.log('\n[4] 自动修复');
{
  const m = blankMenu({ name: '修' });
  m.dishes.push(blankDish({ name: '红烧肉', price: '68', blurb: '', kind: 'pork' }));
  m.dishes.push(blankDish({ name: '宫保鸡丁', price: '48', blurb: '鸡丁滑嫩。', kind: 'chicken', signature: true, signature_note: '' }));
  m.dishes.push(blankDish({ name: '蛋炒饭', price: '26', blurb: '粒粒分明。', kind: 'rice' }));
  const before = inspectMenu(m);
  const fixed = autoFix(m);
  const after = inspectMenu(fixed.menu);
  ok(before.warns > after.warns, `warn 数下降 ${before.warns} → ${after.warns}`);
  ok(fixed.log.length > 0, `修复 ${fixed.log.length} 项：${fixed.log.join('；')}`);
  ok(after.errors === 0, '修复后无 error');
}

/* ---- 5. 工具数量 ---- */
console.log('\n[5] 协议');
{
  const ts = createToolset({
    getMenu: () => blankMenu(), setMenu: () => {}, getSource: () => ({ text: '', dataUrl: '' }),
    pushEvent: () => {}, takeEvent: () => null, cropSource: async () => ({}),
  });
  ok(Object.keys(ts).length === 9, `9 个工具（实际 ${Object.keys(ts).length}）`);
  ok(Object.values(ts).every(t => t.description && t.inputSchema && typeof t.handler === 'function'), '每个工具都有描述/参数定义/处理器');
}

console.log(`\n结果：${pass} 通过，${fail} 失败`);
if (fail) process.exitCode = 1;
