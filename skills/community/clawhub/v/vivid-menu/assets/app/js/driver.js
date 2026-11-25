/* ============================================================
 * driver.js — 双驱动
 *  A. 内置生成器：不依赖任何外部服务，规则解析 + 参数化插图
 *  B. WebMCP 桥：把同一套工具暴露给外部 Agent
 * 两者的差别只在「谁来决策」，执行路径完全一致。
 * ============================================================ */

import { updateDish, stats, blankMenu } from './model.js';
import { parseTextMenu, dictLookup } from './parse.js';
import { inferKind, artInner } from './art/index.js';
import { inspectMenu } from './inspect.js';
import { THEMES } from './model.js';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const toNum = (v) => {
  const n = parseFloat(String(v).replace(/[^\d.]/g, ''));
  return Number.isNaN(n) ? -1 : n;
};

/* ---------------- 挑招牌 ---------------- */

const NOT_SIGNATURE_KIND = /^(drink|dessert|soup)$/;
const SIGN_WORDS = /招牌|特色|镇店|必点|推荐|招牌菜|拿手/;

export function autoPickSignature(menu) {
  if (!menu.dishes.length) return menu;
  if (menu.dishes.some((d) => d.signature)) return menu;

  const pool = menu.dishes.filter((d) => !NOT_SIGNATURE_KIND.test(d.kind || ''));
  if (!pool.length) return menu;

  let pick = pool.find((d) => SIGN_WORDS.test(d.name));
  let note = '菜名带「招牌/特色」字样，据此标为主推';
  if (!pick) {
    pick = pool.slice().sort((a, b) => toNum(b.price) - toNum(a.price))[0];
    note = '按价位在该品类中最高，暂定为主推；可改为实际销量最高的一道';
  }
  return updateDish(menu, pick.id, { signature: true, signature_note: note });
}

/* ---------------- 自动修复闭环 ---------------- */

/**
 * 按质检结果修可以机器修的问题。
 * 明确不修：价格缺失（不编造）、菜名重复（要人判断）、菜名过长（要人删字）。
 */
export function autoFix(menu, rounds = 3) {
  let m = menu;
  const log = [];

  for (let r = 0; r < rounds; r++) {
    const report = inspectMenu(m);
    if (!report.issues.length) break;
    let changed = false;

    for (const issue of report.issues) {
      const d = issue.dishId ? m.dishes.find((x) => x.id === issue.dishId) : null;

      switch (issue.code) {
        case 'no-blurb': {
          const hit = dictLookup(d?.name);
          if (d && hit?.blurb) {
            m = updateDish(m, d.id, { blurb: hit.blurb });
            log.push(`补全「${d.name}」的描述`);
            changed = true;
          }
          break;
        }
        case 'sig-no-evidence': {
          if (d) {
            m = updateDish(m, d.id, { signature_note: '人工标记为主推菜，未记录具体依据' });
            log.push(`为「${d.name}」补上招牌依据说明`);
            changed = true;
          }
          break;
        }
        case 'art-thin':
        case 'art-tiny': {
          if (d) {
            // 丢掉不够用的外部图，交回引擎重画
            m = updateDish(m, d.id, { art: '', kind: d.kind || inferKind(d.name, d.tags) });
            log.push(`重新绘制「${d.name}」的插图`);
            changed = true;
          }
          break;
        }
        case 'mixed-section': {
          const fix = m.dishes.map((x) => ({ ...x, section: x.section || '热菜' }));
          m = { ...m, dishes: fix };
          log.push('把未分类的菜品统一归到「热菜」');
          changed = true;
          break;
        }
        case 'multi-signature': {
          const sigs = m.dishes.filter((x) => x.signature);
          for (const s of sigs.slice(1)) {
            m = updateDish(m, s.id, { signature: false, signature_note: '' });
          }
          log.push(`只保留第一道招牌，取消另外 ${sigs.length - 1} 道的标记`);
          changed = true;
          break;
        }
        case 'price-format': {
          const fixed = m.dishes.map((x) =>
            String(x.price || '').trim() && !/^[¥￥$]/.test(String(x.price).trim())
              ? { ...x, price: `¥${String(x.price).trim()}` }
              : x,
          );
          m = { ...m, dishes: fixed };
          log.push('统一价格写法，全部加上货币符号');
          changed = true;
          break;
        }
        default:
          break;
      }
    }
    if (!changed) break;
  }
  return { menu: m, log };
}

/* ---------------- 内置生成器 ---------------- */

/**
 * 从文字菜单跑完整流程。走的是 toolset 的同一批 handler。
 * @param {object} ctx 会话上下文
 * @param {object} toolset protocol.createToolset() 的产物
 * @param {{onStep?:(s:object)=>void, pace?:number}} opts
 */
export async function runLocal(ctx, toolset, opts = {}) {
  const { onStep = () => {}, pace = 55 } = opts;
  const src = ctx.getSource();
  const text = String(src.text || '');
  const cur = ctx.getMenu();

  const parsed = parseTextMenu(text);
  if (!parsed.dishes.length) {
    return {
      ok: false,
      error: '没能从文字里解析出菜品',
      hint: '每行一道菜，格式如「红烧肉 68」，或用【热菜】这样的分节标题。',
    };
  }

  const total = parsed.dishes.length + 2;
  let done = 0;
  const step = (label, phase = 'work') => {
    done += 1;
    onStep({ label, phase, done, total });
  };

  // 1) 铺纸
  const shopName = parsed.shopName || cur.name || '未命名小馆';
  await toolset.begin_menu.handler({
    name: shopName,
    name_original: cur.name_original || '',
    subtitle: cur.subtitle || '',
    footer: cur.footer || '',
    seal: cur.seal || (shopName.length >= 2 ? shopName.slice(0, 2) : ''),
    theme: cur.theme || 'rice',
  });
  step('铺好菜单纸', 'paper');

  // 2) 逐道落笔
  for (const p of parsed.dishes) {
    await toolset.add_dish.handler({
      section: p.section || '',
      name: p.name,
      price: p.price || '',
      blurb: p.blurb || '',
      tags: p.tags || [],
      kind: p.kind || inferKind(p.name, p.tags || []),
    });
    step(`写下「${p.name}」`, 'dish');
    if (pace) await sleep(pace);
  }

  // 3) 挑招牌 → 自动修复 → 复检
  let menu = ctx.getMenu();
  menu = autoPickSignature(menu);
  ctx.setMenu(menu);
  step('挑出主推菜', 'sign');

  const fixed = autoFix(ctx.getMenu());
  ctx.setMenu(fixed.menu);
  const report = inspectMenu(fixed.menu);
  step('质检完成', 'inspect');

  return {
    ok: true,
    shopName,
    parsed: { dishes: parsed.dishes.length, sections: parsed.sections },
    fixed: fixed.log,
    report,
  };
}

/** 对已有菜单做一次「重画全部插图」——换掉外部 art，回到引擎 */
export function redrawAll(menu) {
  return {
    ...menu,
    dishes: menu.dishes.map((d) => ({
      ...d,
      art: '',
      kind: d.kind || inferKind(d.name, d.tags),
    })),
  };
}

/* ---------------- WebMCP 桥 ---------------- */

/**
 * 把工具注册到页面的 WebMCP。不支持的浏览器返回 unsupported，
 * 此时应用仍可用内置生成器工作。
 */
export function mountWebMCP(toolset, meta = {}) {
  const mc = globalThis.document?.modelContext;
  if (!mc || typeof mc.provideContext !== 'function') {
    return { supported: false, reason: '当前浏览器未提供 WebMCP（document.modelContext）' };
  }
  try {
    const tools = Object.entries(toolset).map(([name, def]) => ({
      name,
      description: def.description,
      inputSchema: def.inputSchema,
      execute: async (args) => {
        const r = await def.handler(args || {});
        return { content: [{ type: 'text', text: JSON.stringify(r) }] };
      },
    }));
    mc.provideContext({
      name: meta.name || 'vivid-menu',
      description: meta.description || '把网页变成 Agent 的画布：逐道菜绘制菜单',
      tools,
    });
    return { supported: true, count: tools.length };
  } catch (e) {
    return { supported: false, reason: `注册失败：${e.message}` };
  }
}

/** 当前主题是否是已知预设 */
export const isValidTheme = (id) => !!THEMES[id];
