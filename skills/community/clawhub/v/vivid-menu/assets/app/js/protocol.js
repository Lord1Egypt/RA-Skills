/* ============================================================
 * protocol.js — 9 个网页工具
 *
 * 设计要点：这一层只定义「能力」，不关心谁来调用。
 * 外部 Agent（WebMCP）和内置生成器调的是同一批 handler，
 * 所以两条路径不会出现逻辑分叉。
 * ============================================================ */

import {
  blankMenu, blankDish, addDish, updateDish, removeDish, moveDish,
  themeOf, THEME_LIST, stats, PAPER, SZ, FS,
} from './model.js';
import { inspectMenu } from './inspect.js';
import { inferKind, sanitizeArt, artInner, applyTokens } from './art/index.js';
import { layoutMenu } from './layout.js';
import { parseTextMenu, dictLookup } from './parse.js';

/* ---------------- 工具说明（给 Agent 看的画法规范） ---------------- */

export const BRIEF = `# 生动菜单 · 绘制说明

你在为一个网页菜单应用工作。你的产出不是一张图片，而是**结构化菜品数据 + 每道菜的 SVG 线条插图**，由页面负责排版、质检和导出。

## 工作顺序
1. \`get_source\` 看有没有原图或文字；有原图就 \`zoom_source\` 局部放大，逐字辨认菜名和价格。
2. \`begin_menu\` 建一张纸，确定店名、纸张质感与点缀色。
3. 逐道 \`add_dish\`。**一次只加一道**，加完可以继续。
4. \`inspect_menu\` 检查，按返回的 issues 逐条 \`update_dish\` 修。
5. \`wait_for_user\` 等用户提新要求（换图、改文案、加菜）。

## 插图规范（art 字段）
- 视口固定 \`0 0 100 100\`，纯线条画，\`stroke-linecap="round"\`。
- 主描边 \`stroke-width\` 2~2.4，细节 1~1.3，不要用 fill 铺大面积。
- 颜色只允许三种 token：\`INK\`（墨）、\`ACCENT\`（点缀，仅用于辣椒/印章等小面积）、\`MUTE\`（淡）。
- 不要写 \`<svg>\` 外壳，只给内部图元。
- 一道菜 8~45 个图元为宜，太少了认不出，太多了缩到 88px 会糊。
- **留白**：四周至少留 8 单位，别顶到边。
- 如果没把握，可以不传 art，页面会自动用内置图形引擎按菜名生成。

## 内容规范
- 价格**照抄原图**。看不清就留空，绝不编造。
- 招牌菜必须给 \`signature_note\`，写明判断依据（销量、口碑、菜单上的标记）。
- 描述一句话，讲食材和口感，不要写"美味可口"这类空话。
- 菜名太长会被截断，超过 12 字要拆。

## 配色
${THEME_LIST.map((t) => `- \`${t.id}\` ${t.label}：纸 ${t.paper} / 墨 ${t.ink} / 点缀 ${t.accent}`).join('\n')}
`;

/* ---------------- 工具实现 ---------------- */

/**
 * @param {object} ctx 会话上下文
 * @param {() => object} ctx.getMenu 取当前菜单
 * @param {(m:object) => void} ctx.setMenu 写回菜单
 * @param {() => object} ctx.getSource 取原图/文字源
 * @param {(p:object) => void} ctx.pushEvent 记录一条用户事件
 */
export function createToolset(ctx) {
  const ok = (data = {}) => ({ ok: true, ...data });
  const fail = (error, hint = '') => ({ ok: false, error, hint });

  const findDish = (menu, { id, name }) => {
    if (id) return menu.dishes.find((d) => d.id === id) || null;
    if (name) return menu.dishes.find((d) => d.name === name) || null;
    return null;
  };

  return {
    /* 1. 画法说明 */
    read_brief: {
      description: '读取绘制规范：插图怎么画、文案怎么写、有哪些配色可选。开工前先调用一次。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => ok({ brief: BRIEF }),
    },

    /* 2. 原图状态 */
    get_source: {
      description: '获取当前原始菜单的状态：是否有照片、尺寸、以及当前放大区域。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => {
        const s = ctx.getSource();
        return ok({
          hasPhoto: !!s.dataUrl,
          width: s.width || 0,
          height: s.height || 0,
          zoom: s.zoom || null,
          textHint: s.text ? s.text.slice(0, 2000) : '',
          note: s.dataUrl
            ? '照片在左侧显示。需要辨认细节时用 zoom_source 按归一化坐标放大。'
            : '还没有照片。可以请用户上传图片，或直接粘贴文字菜单。',
        });
      },
    },

    /* 3. 局部放大 */
    zoom_source: {
      description: '按归一化坐标（0~1）放大原图某一块，用于辨认菜名和价格。返回放大后的图片与区域。',
      inputSchema: {
        type: 'object',
        properties: {
          x: { type: 'number', description: '左边界，0~1' },
          y: { type: 'number', description: '上边界，0~1' },
          w: { type: 'number', description: '宽度，0~1' },
          h: { type: 'number', description: '高度，0~1' },
        },
        required: ['x', 'y', 'w', 'h'],
      },
      handler: async ({ x, y, w, h }) => {
        const s = ctx.getSource();
        if (!s.dataUrl) return fail('还没有上传照片', '请用户上传原菜单图片，或改用文字输入。');
        const clamp01 = (v) => Math.max(0, Math.min(1, Number(v) || 0));
        const box = {
          x: clamp01(x), y: clamp01(y),
          w: Math.max(0.02, Math.min(1 - clamp01(x), clamp01(w))),
          h: Math.max(0.02, Math.min(1 - clamp01(y), clamp01(h))),
        };
        const crop = await ctx.cropSource(box);
        return ok({ box, image: crop.dataUrl, pixelWidth: crop.width, pixelHeight: crop.height });
      },
    },

    /* 4. 新建菜单 */
    begin_menu: {
      description: '创建一张新菜单纸，确定店名与配色。会清空已有菜品。',
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '店名' },
          name_original: { type: 'string', description: '原文店名/罗马音，可留空' },
          subtitle: { type: 'string', description: '一句话副标题' },
          footer: { type: 'string', description: '页脚说明（营业时间、备注）' },
          seal: { type: 'string', description: '印章文字，2~4 字' },
          theme: { type: 'string', enum: THEME_LIST.map((t) => t.id), description: '纸张配色' },
        },
        required: ['name'],
      },
      handler: async (args) => {
        const menu = blankMenu({
          name: args.name || '未命名小馆',
          name_original: args.name_original || '',
          subtitle: args.subtitle || '',
          footer: args.footer || '',
          seal: (args.seal || '').slice(0, 4),
          theme: THEME_LIST.some((t) => t.id === args.theme) ? args.theme : 'rice',
        });
        ctx.setMenu(menu);
        return ok({ menuId: menu.id, theme: menu.theme, note: '纸张已建好，接下来用 add_dish 逐道加菜。' });
      },
    },

    /* 5. 加菜 */
    add_dish: {
      description: '添加一道菜。art 可选，不传则按菜名自动生成线条插图。',
      inputSchema: {
        type: 'object',
        properties: {
          section: { type: 'string', description: '分节，如「凉菜」「热菜」；留空则沿用上一道' },
          name: { type: 'string', description: '菜名' },
          name_original: { type: 'string', description: '原文菜名，可留空' },
          price: { type: 'string', description: '价格，照抄原图，别编造' },
          blurb: { type: 'string', description: '一句话说明，讲食材和口感' },
          tags: { type: 'array', items: { type: 'string' }, description: '口味标签，2 个以内' },
          signature: { type: 'boolean', description: '是否招牌菜' },
          signature_note: { type: 'string', description: '招牌依据' },
          kind: { type: 'string', description: '食材类别，不传则自动推断' },
          art: { type: 'string', description: 'SVG 内部图元，0 0 100 100 坐标系' },
        },
        required: ['name'],
      },
      handler: async (args) => {
        if (!args.name) return fail('缺少菜名');
        const menu = ctx.getMenu();
        const dish = blankDish({
          section: args.section ?? '',
          name: String(args.name).slice(0, 40),
          name_original: args.name_original || '',
          price: args.price == null ? '' : String(args.price),
          blurb: args.blurb || '',
          tags: Array.isArray(args.tags) ? args.tags.slice(0, 3) : [],
          signature: !!args.signature,
          signature_note: args.signature_note || '',
          kind: args.kind || inferKind(args.name, args.tags || []),
          art: args.art ? sanitizeArt(args.art) : '',
        });
        ctx.setMenu(addDish(menu, dish));
        return ok({ dishId: dish.id, kind: dish.kind, count: ctx.getMenu().dishes.length });
      },
    },

    /* 6. 改菜 */
    update_dish: {
      description: '按 id 或菜名修改某道菜。只传要改的字段。',
      inputSchema: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          name: { type: 'string', description: '用于定位的菜名' },
          patch: {
            type: 'object',
            description: '要修改的字段：name/price/blurb/tags/section/signature/signature_note/kind/art',
          },
        },
        required: ['patch'],
      },
      handler: async ({ id, name, patch }) => {
        const menu = ctx.getMenu();
        const d = findDish(menu, { id, name });
        if (!d) return fail('找不到这道菜', '先用 get_source 或 inspect_menu 确认菜品列表。');
        const clean = { ...patch };
        if (clean.art) clean.art = sanitizeArt(clean.art);
        if (clean.name) clean.name = String(clean.name).slice(0, 40);
        if (Array.isArray(clean.tags)) clean.tags = clean.tags.slice(0, 3);
        ctx.setMenu(updateDish(menu, d.id, clean));
        return ok({ dishId: d.id, changed: Object.keys(clean) });
      },
    },

    /* 7. 删菜 */
    remove_dish: {
      description: '删除一道菜。',
      inputSchema: {
        type: 'object',
        properties: { id: { type: 'string' }, name: { type: 'string' } },
      },
      handler: async ({ id, name }) => {
        const menu = ctx.getMenu();
        const d = findDish(menu, { id, name });
        if (!d) return fail('找不到这道菜');
        ctx.setMenu(removeDish(menu, d.id));
        return ok({ removed: d.name, count: ctx.getMenu().dishes.length });
      },
    },

    /* 8. 质检 */
    inspect_menu: {
      description: '检查整张菜单：排版、插图、内容一致性。返回 error 和 warn 两级问题清单。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => {
        const report = inspectMenu(ctx.getMenu());
        return ok({
          passed: report.ok,
          errors: report.errors,
          warns: report.warns,
          metrics: report.metrics,
          issues: report.issues,
          hint: report.ok ? '没有 error 级问题。' : '按 issues 里的 dishId 逐条 update_dish 修复。',
        });
      },
    },

    /* 9. 等用户 */
    wait_for_user: {
      description: '暂停，等待用户的下一个动作（换图、文字要求、导出）。返回用户事件类型。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => {
        const ev = ctx.takeEvent();
        return ok({
          event: ev ? ev.type : 'idle',
          payload: ev ? ev.payload : null,
          hint: ev ? '按事件内容继续处理。' : '暂时没有新事件，可以让用户提要求。',
        });
      },
    },
  };
}

/* ---------------- 一次性批量导入（内置生成器专用） ---------------- */

/**
 * 从文字一次性填充菜单。内置生成器走这条路，等价于
 * 连续调用 begin_menu + N 次 add_dish，但不需要逐个 await。
 */
export function fillFromText(menu, text) {
  const parsed = parseTextMenu(text);
  let m = menu;
  const created = [];

  for (const p of parsed.dishes) {
    const hit = dictLookup(p.name);
    const d = blankDish({
      section: p.section || '',
      name: p.name,
      price: p.price || '',
      blurb: p.blurb || (hit ? hit.blurb : ''),
      tags: p.tags || (hit ? hit.tags : []),
      kind: p.kind || inferKind(p.name, p.tags || []),
    });
    m = addDish(m, d);
    created.push(d);
  }
  return { menu: m, parsed, created };
}
