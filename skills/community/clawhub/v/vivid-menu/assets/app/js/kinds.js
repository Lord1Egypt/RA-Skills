/* ============================================================
 * kinds.js — 食材类别画法库
 * 每个画法都是 (rand, variant) => svg 片段，绘制在 0 0 100 100 内。
 * variant 用于在同类别内产生不同构图，避免整页插图雷同。
 * ============================================================ */

import {
  path, line, circle, ellipse, plate, bowl, block, leafShape, leafOval,
  steam, dots, chili, chopsticks, xy, dv, between,
} from './pen.js';

/* ---------- 肉类 ---------- */

// 猪肉：方块塔（红烧）/ 厚方绑绳（东坡）/ 切片覆梅菜（扣肉）
export function pork(rand) {
  const mode = Math.floor(rand() * 3);
  const out = [plate(33, 62)];

  if (mode === 0) {
    // 红烧肉：三块方肉垒成小塔，肥瘦分层
    for (const [x, y, w, h, r] of [[38, 55, 15, 11, -6], [62, 55, 15, 11, 5], [50, 45, 16, 11, 0]]) {
      out.push(block(x, y, w, h, r, rand));
      out.push(path(`M${xy(x - w * 0.42, y - 1.4)}q${xy(w * 0.42, -2.4)} ${xy(w * 0.84, 0.6)}`, { sw: 1.3, op: 0.55 }));
    }
    out.push(
      leafShape(31, 67, 12, -30, { sw: 1.8, vein: false, w: 0.36 }),
      leafShape(69, 67, 11, 210, { sw: 1.8, vein: false, w: 0.36 }),
      path(`M${xy(34, 62)}q${xy(16, 6)} ${xy(32, 0)}`, { sw: 1.3, op: 0.4 }),
    );
  } else if (mode === 1) {
    // 东坡肉：两块厚方，十字草绳捆绑
    for (const [x, y, s] of [[42, 54, 1], [60, 57, 0.86]]) {
      const w = 24 * s, h = 17 * s;
      out.push(path(`M${xy(x - w / 2, y - h / 2)}L${xy(x + w / 2, y - h / 2)}L${xy(x + w / 2, y + h / 2)}L${xy(x - w / 2, y + h / 2)}Z`, { sw: 2.4 }));
      // 肥皮
      out.push(path(`M${xy(x - w / 2, y - h / 2 + 2.6)}L${xy(x + w / 2, y - h / 2 + 2.6)}`, { sw: 1.4, op: 0.6 }));
      // 草绳
      out.push(
        path(`M${xy(x - w * 0.18, y - h / 2 - 1)}L${xy(x - w * 0.18, y + h / 2 + 1)}`, { sw: 1.4, op: 0.7, dash: '2 1.6' }),
        path(`M${xy(x - w / 2 - 1, y + 1)}L${xy(x + w / 2 + 1, y + 1)}`, { sw: 1.4, op: 0.7, dash: '2 1.6' }),
      );
    }
    out.push(path(`M${xy(34, 64)}q${xy(16, 5)} ${xy(32, 0)}`, { sw: 1.3, op: 0.4 }));
  } else {
    // 梅菜扣肉：肉片呈扇形层叠，顶上覆梅菜
    for (let i = 0; i < 5; i++) {
      const y = 50 + i * 4.2;
      out.push(path(`M${xy(36 + i * 0.7, y)}L${xy(64 - i * 0.7, y)}`, { sw: 2.2 - i * 0.1 }));
    }
    out.push(path(`M${xy(35, 48)}q${xy(15, -9)} ${xy(30, 0)}`, { sw: 2.4 }));
    // 梅菜碎
    for (let i = 0; i < 7; i++) {
      const x = 39 + i * 3.6;
      out.push(path(`M${xy(x, 47 - Math.sin(i) * 1.5)}q${xy(1.6, -2)} ${xy(3, 0.4)}`, { sw: 1.1, op: 0.6 }));
    }
  }
  return out.join('');
}

// 牛肉：块烧 / 牛排格纹 / 薄片扇形
export function beef(rand) {
  const mode = Math.floor(rand() * 3);
  const out = [plate(33, 62)];

  if (mode === 0) {
    out.push(
      path(`M${xy(34, 52)}L${xy(58, 46)}L${xy(70, 58)}L${xy(52, 68)}L${xy(32, 62)}Z`, { sw: 2.4 }),
      block(52, 46, 18, 11, -8, rand),
      path(`M${xy(40, 55)}q${xy(8, -4)} ${xy(16, -1)}`, { sw: 1.2, op: 0.5 }),
      path(`M${xy(38, 61)}q${xy(10, -3)} ${xy(20, 1)}`, { sw: 1.2, op: 0.5 }),
      dots(rand, 50, 56, 14, 6, 1.1),
    );
  } else if (mode === 1) {
    // 牛排：椭圆肉排 + 烤格纹 + 迷迭香
    out.push(ellipse(50, 55, 23, 14, { sw: 2.4 }), ellipse(50, 55, 18, 10.5, { sw: 1.2, op: 0.45 }));
    for (let i = -1; i <= 1; i++) {
      out.push(path(`M${xy(36 + i * 7, 46)}L${xy(50 + i * 7, 64)}`, { sw: 1.5, op: 0.45 }));
    }
    out.push(leafShape(66, 48, 13, -55, { sw: 1.5, w: 0.22 }));
    out.push(path(`M${xy(36, 44)}q${xy(8, -4)} ${xy(16, -1)}`, { sw: 1.2, op: 0.4 }));
  } else {
    // 牛肉片：三片薄肉扇形铺开
    for (let i = 0; i < 3; i++) {
      const y = 50 + i * 6;
      out.push(path(`M${xy(34, y)}q${xy(16, -7)} ${xy(32, 1)}q${xy(-14, 6)} ${xy(-32, -1)}Z`, { sw: 2 }));
    }
    out.push(dots(rand, 50, 58, 13, 4, 1.1));
  }
  return out.join('');
}

// 禽类：鸡块带辣椒 / 整只鸡腿带骨（两种都经得起放大）
export function chicken(rand) {
  const mode = Math.floor(rand() * 3);
  const out = [];

  if (mode === 0) {
    /* 鸡块：三块带棱的肉 + 双椒 + 花椒 + 葱段 */
    out.push(plate(33, 62));
    out.push(block(41, 54, 15, 13, -12, rand), block(60, 57, 14, 12, 9, rand), block(50, 45, 13, 11, 3, rand));
    out.push(dots(rand, 50, 57, 15, 6, 1.1));
    out.push(chili(28, 60, 13, 198, true), chili(72, 52, 11, 14, true));
    out.push(leafShape(36, 66, 12, -22, { sw: 1.6, vein: false, w: 0.34 }));
    out.push(path(`M${xy(34, 63)}q${xy(16, 6)} ${xy(32, -1)}`, { sw: 1.3, op: 0.42 }));
  } else if (mode === 1) {
    /* 整只鸡腿：梨形腿肉 + 一根骨头 + 骨节 */
    out.push(plate(35, 70));
    out.push(path(
      `M${xy(60, 50)}C${xy(67, 56)} ${xy(65, 68)} ${xy(53, 73)}C${xy(39, 78)} ${xy(29, 68)} ${xy(31, 57)}C${xy(33, 47)} ${xy(48, 43)} ${xy(60, 50)}Z`,
      { sw: 2.4 },
    ));
    // 骨头从肉的上端伸出，末端有两个骨节
    out.push(path(`M${xy(59, 51)}L${xy(71, 40)}`, { sw: 3.2 }));
    out.push(circle(73, 38, 3.4, { sw: 1.9 }), circle(69, 42, 2.6, { sw: 1.7 }));
    // 皮纹
    out.push(path(`M${xy(40, 58)}q${xy(8, -4)} ${xy(14, -1)}`, { sw: 1.2, op: 0.45 }));
    out.push(path(`M${xy(43, 64)}q${xy(7, -3)} ${xy(12, -1)}`, { sw: 1.1, op: 0.35 }));
    // 椒盐
    out.push(dots(rand, 46, 60, 11, 4, 1));
  } else {
    /* 白切鸡：并排码放的四片，带皮线，边片略矮 */
    out.push(plate(36, 71));
    for (let i = 0; i < 4; i++) {
      const x = 32 + i * 6.6;
      const top = 50 + (i === 0 || i === 3 ? 2.5 : 0);
      out.push(path(
        `M${xy(x, 69)}Q${xy(x + 0.6, top + 2)} ${xy(x + 3.7, top)}Q${xy(x + 6.8, top + 2)} ${xy(x + 7.4, 69)}Z`,
        { sw: 1.9 },
      ));
      // 皮线
      out.push(path(`M${xy(x + 0.5, 64)}Q${xy(x + 3.7, 62.2)} ${xy(x + 6.9, 64)}`, { sw: 1, op: 0.45 }));
    }
    // 姜葱蘸料小碟 + 葱花
    out.push(circle(50, 71, 4.4, { sw: 1.5, op: 0.65 }));
    out.push(dots(rand, 50, 71, 2.4, 3, 0.9));
    out.push(leafShape(70, 60, 10, -38, { sw: 1.4, vein: false, w: 0.34 }));
  }
  return out.join('');
}

/* ---------- 水产 ---------- */

// 整鱼：清蒸整条 / 汤碗鱼片 / 花刀松鼠鱼
export function fish(rand) {
  const mode = Math.floor(rand() * 3);

  if (mode === 1) {
    // 汤碗鱼片：梭形鱼片叠在汤面上，配酸菜与红油
    const out = [bowl(52, 30)];
    out.push(ellipse(50, 52, 25, 6.8, { sw: 1.6, op: 0.7 }));
    // 鱼片（梭形，三片重叠）
    const slice = (cx, cy, rot, s = 1) => {
      const w = 10.5 * s, h = 4.6 * s;
      return path(
        `M${xy(cx - w, cy)}Q${xy(cx, cy - h * 1.5)} ${xy(cx + w, cy)}Q${xy(cx, cy + h * 1.5)} ${xy(cx - w, cy)}Z`,
        { sw: 1.9, extra: JSON.stringify({ transform: `rotate(${rot} ${xy(cx, cy)})` }) },
      );
    };
    out.push(slice(42, 50, -12), slice(58, 53, 9), slice(50, 47, 2, 0.86), slice(66, 49, -18, 0.7));
    // 酸菜
    out.push(
      leafOval(36, 55, 9, -160, 0.5, { sw: 1.3, vein: false }),
      leafOval(64, 56, 8, -20, 0.5, { sw: 1.3, vein: false }),
    );
    // 红油浮层
    out.push(chili(33, 49, 8, 195, true), chili(63, 51, 7, 12, true));
    out.push(dots(rand, 50, 51, 16, 6, 1.1));
    out.push(steam(50, 42, 21, 3));
    return out.join('');
  }

  const out = [ellipse(50, 62, 38, 9, { sw: 2.2 })];
  const body = `M20 58C26 44 ${xy(48, 40)} 66 52Q${xy(70, 48)} 72 47Q${xy(74, 52)} 72.5 58Q${xy(74, 64)} 72 69Q70 68 66 64C48 76 26 72 20 58Z`;
  out.push(path(body, { sw: 2.4 }));
  out.push(
    circle(28, 57, 1.9, { fill: 'INK', sw: 0 }),
    circle(28, 57, 3.4, { sw: 1.2, op: 0.6 }),
    path(`M35 53q${xy(4, 5)} ${xy(0, 10)}`, { sw: 1.4, op: 0.7 }),
    path(`M72 47q${xy(10, 2)} ${xy(11, 11)}q${xy(-7, -1)} ${xy(-11, 11)}`, { sw: 2 }),
    path(`M42 45q${xy(9, -6)} ${xy(18, 1)}`, { sw: 1.8 }),
  );

  if (mode === 2) {
    // 松鼠鳜鱼：菱形花刀 + 浇汁
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 2; j++) {
        out.push(path(`M${xy(40 + i * 9, 49 + j * 6)}l${xy(4, 4)}l${xy(-4, 4)}l${xy(-4, -4)}Z`, { sw: 1.2, op: 0.55 }));
      }
    }
    out.push(path(`M${xy(34, 66)}q${xy(16, 5)} ${xy(32, -1)}`, { sw: 1.6, op: 0.5 }));
  } else {
    // 清蒸：鳞片 + 葱丝
    for (let i = 0; i < 3; i++) {
      out.push(path(`M${xy(40 + i * 8, 50)}q${xy(4, 6)} ${xy(0, 12)}`, { sw: 1.1, op: 0.4 }));
    }
    out.push(
      path(`M${xy(44, 44)}q${xy(6, -3)} ${xy(13, -1)}`, { sw: 1.5, op: 0.6 }),
      path(`M${xy(48, 41)}q${xy(7, -2)} ${xy(13, 1)}`, { sw: 1.5, op: 0.6 }),
    );
  }
  return out.join('');
}

// 虾：C 形身体 + 分节 + 尾扇 + 触须
export function shrimp(rand) {
  const out = [plate(31, 62)];
  out.push(path('M30 46C24 58 30 72 46 74C60 76 70 66 68 54', { sw: 2.4 }));
  out.push(path('M36 44C32 56 37 66 48 68C58 70 64 62 62 52', { sw: 2 }));
  // 分节
  for (let i = 0; i < 4; i++) {
    const t = i / 4;
    out.push(path(`M${xy(33 + t * 4, 50 + t * 18)}l${xy(7, 1.5)}`, { sw: 1.2, op: 0.55 }));
  }
  // 尾扇
  out.push(path('M68 54l8 -6l-1 8l7 -2l-6 8z', { sw: 1.8 }));
  // 头与眼
  out.push(circle(31, 44, 2, { fill: 'INK', sw: 0 }));
  // 触须
  out.push(path('M30 44q-10 -6 -14 -1', { sw: 1.2, op: 0.65 }), path('M30 47q-11 0 -13 6', { sw: 1.2, op: 0.5 }));
  return out.join('');
}

// 蟹：壳 + 双钳 + 六足
export function crab(rand) {
  const out = [plate(33, 64)];
  out.push(ellipse(50, 56, 19, 14, { sw: 2.4 }));
  out.push(path(`M36 50q${xy(14, -7)} ${xy(28, 0)}`, { sw: 1.3, op: 0.5 }));
  // 眼柄
  out.push(circle(44, 41, 1.6, { fill: 'INK', sw: 0 }), circle(56, 41, 1.6, { fill: 'INK', sw: 0 }));
  // 钳
  out.push(
    path('M31 52q-11 -8 -15 -2q-3 6 5 7q-6 2 -3 6q4 4 12 -3', { sw: 2.2 }),
    path('M69 52q11 -8 15 -2q3 6 -5 7q6 2 3 6q-4 4 -12 -3', { sw: 2.2 }),
  );
  // 腿
  for (let i = 0; i < 3; i++) {
    const y = 58 + i * 5;
    out.push(path(`M${xy(34, y)}q${xy(-10, 3)} ${xy(-12, 9)}`, { sw: 1.7 }));
    out.push(path(`M${xy(66, y)}q${xy(10, 3)} ${xy(12, 9)}`, { sw: 1.7 }));
  }
  return out.join('');
}

// 贝类：铰链在下的扇形壳 + 放射纹
export function shellfish(rand) {
  const out = [plate(33, 63)];
  const shell = (cx, cy, s) => {
    const hx = cx, hy = cy + 5 * s;
    const R = 13.5 * s;
    const a1 = -158, a2 = -22;
    const P = (ang, r) => [hx + Math.cos((ang * Math.PI) / 180) * r, hy + Math.sin((ang * Math.PI) / 180) * r];
    const p1 = P(a1, R), p2 = P(a2, R);
    let g = path(`M${xy(hx, hy)}L${xy(p1[0], p1[1])}A${R} ${R} 0 0 1 ${xy(p2[0], p2[1])}Z`, { sw: 2.2 });
    for (let i = 1; i < 7; i++) {
      const ang = a1 + ((a2 - a1) * i) / 7;
      const pp = P(ang, R * 0.94);
      g += path(`M${xy(hx, hy)}L${xy(pp[0], pp[1])}`, { sw: 1, op: 0.42 });
    }
    // 铰链小弧
    g += path(`M${xy(hx - 3.4 * s, hy)}q${xy(3.4 * s, 2.6 * s)} ${xy(6.8 * s, 0)}`, { sw: 1.6 });
    return g;
  };
  out.push(shell(40, 58, 1.05), shell(61, 60, 0.88));
  return out.join('');
}

/* ---------- 蔬食 ---------- */

// 青菜：整棵油菜（白帮 + 宽叶），或一丛炒叶菜
export function veg(rand) {
  const mode = Math.floor(rand() * 2);
  const out = [plate(33, 63)];

  if (mode === 0) {
    // 整棵油菜：底部菜帮，上面五片宽叶重叠成菜心
    const cabbage = (cx, cy, s, tilt) => {
      let g = path(
        `M${xy(cx - 3.4 * s, cy)}q${xy(0.2 * s, 6.2 * s)} ${xy(3.4 * s, 6.6 * s)}q${xy(3.2 * s, -0.4 * s)} ${xy(3.4 * s, -6.6 * s)}Z`,
        { sw: 1.9 },
      );
      const angles = [[-130, 1], [-88, 1.16], [-46, 1], [-108, 0.84]];
      for (const [ang, k] of angles) {
        g += leafOval(cx, cy - 2 * s, 16.5 * s * k, ang + tilt, 0.44, { sw: 1.8 });
      }
      return g;
    };
    out.push(cabbage(38, 56, 1.05, -9), cabbage(64, 60, 0.92, 11));
  } else {
    // 炒叶菜：叶片围绕中心放射，稍短
    for (let i = 0; i < 6; i++) {
      const ang = -155 + i * 25;
      out.push(leafOval(50 + (i % 3 - 1) * 3, 61, between(rand, 12, 16), ang, 0.36, { sw: 1.7 }));
    }
    out.push(dots(rand, 50, 58, 11, 3, 1.2));
  }
  return out.join('');
}

// 菌菇：伞盖 + 柄 + 斑点
export function mushroom(rand) {
  const out = [plate(32, 63)];
  const one = (cx, cy, s) => {
    let g = path(`M${xy(cx - 13 * s, cy + 2 * s)}Q${xy(cx - 12 * s, cy - 11 * s)} ${xy(cx, cy - 11 * s)}Q${xy(cx + 12 * s, cy - 11 * s)} ${xy(cx + 13 * s, cy + 2 * s)}Z`, { sw: 2.2 });
    g += path(`M${xy(cx - 4 * s, cy + 2 * s)}l${xy(-1.5 * s, 8 * s)}q${xy(5.5 * s, 2 * s)} ${xy(11 * s, 0)}l${xy(-1.5 * s, -8 * s)}`, { sw: 2 });
    g += path(`M${xy(cx - 8 * s, cy - 4 * s)}q${xy(4, -3)} ${xy(8, 0)}`, { sw: 1.1, op: 0.5 });
    return g;
  };
  out.push(one(42, 56, 0.9), one(58, 58, 1.05));
  return out.join('');
}

// 豆腐：立方体（顶面菱形 + 双侧面）
export function tofu(rand) {
  const out = [plate(33, 63)];
  const cube = (cx, cy, s) => {
    const w = 11 * s, h = 7 * s, d = 5 * s;
    return [
      path(`M${xy(cx, cy - h)}L${xy(cx + w, cy - h + d)}L${xy(cx, cy - h + 2 * d)}L${xy(cx - w, cy - h + d)}Z`, { sw: 2 }),
      path(`M${xy(cx - w, cy - h + d)}L${xy(cx - w, cy + h)}L${xy(cx, cy + h + d)}L${xy(cx, cy - h + 2 * d)}`, { sw: 2 }),
      path(`M${xy(cx + w, cy - h + d)}L${xy(cx + w, cy + h)}L${xy(cx, cy + h + d)}`, { sw: 2 }),
    ].join('');
  };
  out.push(cube(42, 56, 1), cube(60, 58, 0.85));
  return out.join('');
}

// 蛋：荷包蛋 / 番茄炒蛋
export function egg(rand, v) {
  const out = [plate(33, 62)];
  if (v % 2 === 0) {
    out.push(
      path('M32 58q-3 -13 9 -15q6 -8 14 -2q11 -3 12 7q6 6 0 11q-4 8 -13 5q-8 5 -14 -1q-8 -1 -8 -5Z', { sw: 2.2 }),
      circle(50, 55, 6.5, { sw: 2 }),
      circle(48, 53, 1.6, { sw: 1, op: 0.4 }),
    );
  } else {
    // 番茄炒蛋：红黄块交错
    const reds = [[37, 55, 6.5, 5, -12], [61, 61, 6, 4.6, 10], [48, 64, 5.5, 4.2, -4], [64, 50, 5.5, 4.2, 8]];
    const yellows = [[50, 52, 11, 8, 6], [64, 52, 9, 7, -8], [34, 63, 8, 6, 14]];
    for (const [x, y, w, h, r] of yellows) out.push(block(x, y, w, h, r, rand));
    for (const [x, y, w, h, r] of reds) out.push(path(`M${xy(x - w / 2, y - h / 2)}L${xy(x + w / 2, y - h / 2)}L${xy(x + w / 2, y + h / 2)}L${xy(x - w / 2, y + h / 2)}Z`, { fill: 'ACCENT', c: 'INK', sw: 1.5 }));
  }
  return out.join('');
}

// 凉菜：盘 + 两堆细丝（成束而非散落）
export function salad(rand) {
  const out = [plate(33, 62)];
  const heap = (cx, cy, s) => {
    let g = '';
    for (let i = 0; i < 6; i++) {
      const dy = (i - 2.5) * 2.3 * s;
      g += path(`M${xy(cx - 11 * s, cy + dy)}q${xy(11 * s, dy * 0.45 - 3.4 * s)} ${xy(22 * s, 0)}`, { sw: 1.6, op: 0.78 });
    }
    return g;
  };
  out.push(heap(43, 56, 0.92), heap(59, 60, 0.8));
  out.push(dots(rand, 50, 55, 12, 4, 1.3));
  return out.join('');
}

/* ---------- 主食 ---------- */

// 面：碗 + 面条 + 筷
export function noodle(rand, v) {
  const out = [bowl(54, 29)];
  for (let i = 0; i < 4; i++) {
    const x = 34 + i * 6.4;
    out.push(path(`M${xy(x, 46)}c${xy(4, -8)} ${xy(-4, -13)} ${xy(1, -21)}`, { sw: 1.8, op: 0.85 }));
  }
  // 浇头
  out.push(block(44, 40, 11, 7, -8, rand), block(59, 42, 10, 7, 10, rand), dots(rand, 50, 38, 10, 4, 1.1));
  if (v % 2 === 0) out.push(chopsticks(58, 20, 30, 62));
  out.push(steam(50, 30, 14, 2));
  return out.join('');
}

// 米饭：碗 + 饭堆
export function rice(rand) {
  const out = [bowl(56, 28)];
  out.push(path('M30 54q3 -16 20 -16q17 0 20 16', { sw: 2.2 }));
  for (let i = 0; i < 12; i++) {
    out.push(circle(between(rand, 33, 67), between(rand, 42, 53), between(rand, 0.7, 1.3), { sw: 1, op: 0.55 }));
  }
  out.push(steam(50, 36, 13, 3));
  return out.join('');
}

// 汤：碗 + 液面 + 浮料 + 蒸汽
export function soup(rand) {
  const out = [bowl(52, 30)];
  out.push(ellipse(50, 52, 24, 6.5, { sw: 1.6, op: 0.7 }));
  out.push(dots(rand, 44, 52, 9, 3, 2.2), dots(rand, 58, 53, 7, 2, 1.8));
  out.push(leafShape(53, 50, 8, -18, { sw: 1.4, vein: false }));
  out.push(steam(50, 42, 22, 3));
  return out.join('');
}

// 饺子：盘 + 三只月牙，顶部褶子
export function dumpling(rand) {
  const out = [plate(33, 63)];
  const jiao = (cx, cy, s) => {
    const w = 11 * s, h = 8 * s;
    let g = path(
      `M${xy(cx - w, cy + 1.5 * s)}Q${xy(cx, cy - h * 1.75)} ${xy(cx + w, cy + 1.5 * s)}Q${xy(cx, cy + h * 1.15)} ${xy(cx - w, cy + 1.5 * s)}Z`,
      { sw: 2.2 },
    );
    // 顶部褶：四道小弧，位置沿上弧抬升
    for (let i = 0; i < 4; i++) {
      const x0 = cx - w * 0.6 + i * (w * 1.2 / 4);
      const lift = (Math.abs(i - 1.5) ** 2) * 0.55 * s;
      g += path(`M${xy(x0, cy - h * 0.72 + lift)}q${dv(1.5 * s, -2.7 * s)} ${dv(3 * s, 0.1 * s)}`, { sw: 1.2, op: 0.7 });
    }
    // 下腹弧
    g += path(`M${xy(cx - w * 0.68, cy + 3.6 * s)}q${xy(w * 0.68, 2.5 * s)} ${xy(w * 1.36, 0)}`, { sw: 1.2, op: 0.4 });
    return g;
  };
  out.push(jiao(42, 58, 0.95), jiao(60, 61, 0.86), jiao(51, 49, 0.78));
  return out.join('');
}

// 饼：两层圆饼 + 厚度边 + 焦斑 + 芝麻
export function pancake(rand) {
  const out = [plate(33, 63)];
  // 下层饼（带厚度）
  out.push(
    ellipse(50, 56, 24, 10, { sw: 2.4 }),
    path(`M${xy(26, 56)}q${xy(24, 9)} ${xy(48, 0)}`, { sw: 1.3, op: 0.35 }),
  );
  // 上层饼
  out.push(ellipse(50, 50, 21.5, 9, { sw: 2 }));
  // 焦斑
  for (let i = 0; i < 5; i++) {
    const a = rand() * Math.PI * 2, r0 = Math.sqrt(rand()) * 13;
    out.push(ellipse(50 + Math.cos(a) * r0, 50 + Math.sin(a) * r0 * 0.42, between(rand, 1.6, 3), between(rand, 0.9, 1.5), { sw: 1.1, op: 0.45 }));
  }
  // 芝麻
  out.push(dots(rand, 50, 50, 15, 5, 1.1));
  return out.join('');
}

// 烧烤串：斜签 + 串肉
export function skewer(rand) {
  const out = [plate(30, 66)];
  out.push(path('M26 78L74 24', { sw: 2 }));
  const pos = [[36, 68], [45, 58], [54, 48], [63, 38]];
  for (const [x, y] of pos) out.push(block(x, y, 9, 8, -45, rand, { sw: 1.9, highlight: false }));
  out.push(dots(rand, 50, 52, 16, 5, 1.1));
  return out.join('');
}

// 火锅 / 干锅：锅体 + 烟囱 + 周围食材
export function hotpot(rand, v) {
  const out = [];
  out.push(ellipse(50, 66, 34, 8, { sw: 2.2 }));
  out.push(
    path('M18 56q1 16 32 16q31 0 32 -16', { sw: 2.4 }),
    ellipse(50, 56, 32, 10, { sw: 2.4 }),
    ellipse(50, 56, 22, 6.5, { sw: 1.4, op: 0.5 }),
  );
  // 烟囱
  out.push(
    path('M44 50L42 30h16l-2 20', { sw: 2 }),
    ellipse(50, 30, 8, 3, { sw: 1.8 }),
    steam(50, 26, 12, 2),
  );
  // 把手
  out.push(path('M16 54q-8 0 -8 6', { sw: 1.8 }), path('M84 54q8 0 8 6', { sw: 1.8 }));
  // 食材
  const items = v % 2 === 0 ? 4 : 3;
  for (let i = 0; i < items; i++) {
    const a = (i / items) * Math.PI * 2 + 0.6;
    out.push(block(50 + Math.cos(a) * 19, 54 + Math.sin(a) * 5.5, 7, 5, 0, rand, { sw: 1.6, highlight: false }));
  }
  out.push(chili(68, 50, 9, 20), chili(32, 52, 8, 200));
  return out.join('');
}

// 甜点：小碟 + 圆形糕 + 装饰
export function dessert(rand, v) {
  const out = [plate(29, 66)];
  if (v % 2 === 0) {
    out.push(circle(50, 54, 15, { sw: 2.3 }), circle(50, 54, 9, { sw: 1.3, op: 0.5 }));
    out.push(circle(50, 44, 4.2, { fill: 'ACCENT', c: 'INK', sw: 1.4 }));
    out.push(path('M50 40q4 -5 8 -4', { sw: 1.4 }));
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2;
      out.push(circle(50 + Math.cos(a) * 12, 54 + Math.sin(a) * 12, 1.5, { sw: 1, op: 0.5 }));
    }
  } else {
    // 切块蛋糕
    out.push(path('M34 60L50 66L66 58L50 52Z', { sw: 2.2 }), path('M34 60L34 48L50 42L50 52Z', { sw: 2.2 }), path('M66 58L66 46L50 40L50 52Z', { sw: 2.2 }));
    out.push(path('M34 48L50 42L66 46L50 40Z', { fill: 'ACCENT', c: 'INK', sw: 1.4 }));
    out.push(circle(50, 36, 3.6, { fill: 'ACCENT', c: 'INK', sw: 1.4 }));
  }
  return out.join('');
}

// 饮品：杯 / 壶
export function drink(rand, v) {
  const out = [];
  if (v % 2 === 0) {
    out.push(ellipse(50, 70, 20, 5, { sw: 2 }));
    out.push(path('M36 34L38 68q12 5 24 0L64 34', { sw: 2.3 }), ellipse(50, 34, 14, 4, { sw: 2 }));
    out.push(ellipse(50, 46, 12.5, 3.4, { sw: 1.3, op: 0.5 }));
    out.push(path('M58 24q4 -6 10 -4', { sw: 1.4, op: 0.6 }));
    for (let i = 0; i < 4; i++) out.push(circle(between(rand, 42, 58), between(rand, 52, 64), between(rand, 1, 1.8), { sw: 1, op: 0.5 }));
  } else {
    // 酒壶
    out.push(ellipse(50, 72, 18, 4.5, { sw: 2 }));
    out.push(path('M40 66q-8 -10 -2 -22q4 -8 12 -8q8 0 12 8q6 12 -2 22q-10 4 -20 0Z', { sw: 2.3 }));
    out.push(path('M46 36l1 -7h6l1 7', { sw: 2 }), ellipse(50, 29, 4, 1.6, { sw: 1.6 }));
    out.push(path('M44 48q6 -3 12 0', { sw: 1.3, op: 0.5 }));
    out.push(path('M66 46q9 -4 7 6q-2 8 -8 6', { sw: 2 }));
  }
  return out.join('');
}

// 通配：盘 + 一块主料 + 点缀
export function generic(rand) {
  const out = [plate(33, 62)];
  out.push(block(50, 56, 22, 15, -6, rand), block(40, 64, 12, 8, 10, rand), block(62, 64, 11, 7, -12, rand));
  out.push(leafShape(64, 50, 11, -40, { sw: 1.6, vein: false }), dots(rand, 50, 58, 15, 4, 1.2));
  return out.join('');
}

export const KINDS = {
  pork, beef, chicken, fish, shrimp, crab, shellfish,
  veg, mushroom, tofu, egg, salad,
  noodle, rice, soup, dumpling, pancake, skewer, hotpot,
  dessert, drink, generic,
};

export const KINDS_VARIANTS = { fish: 2, veg: 2, noodle: 2, egg: 2, hotpot: 2, dessert: 2, drink: 2 };
