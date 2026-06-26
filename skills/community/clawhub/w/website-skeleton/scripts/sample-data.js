#!/usr/bin/env node
/**
 * sample-data.js — 生成示例测试数据
 *
 * 用法:
 *   node scripts/sample-data.js              # 输出 SQL 到 stdout
 *   node scripts/sample-data.js > db/seed.sql # 重定向到文件
 *   node scripts/sample-data.js --json        # 输出 JSON 格式
 *   node scripts/sample-data.js --hash-passwords  # 生成 bcrypt 哈希密码
 *
 * SQL 使用 INSERT IGNORE 包装，可重复执行。
 * --hash-passwords 标志会自动使用 bcryptjs 生成密码哈希。
 */

import bcrypt from 'bcryptjs';

// ──────────────────────────────────────────────
// 常量
// ──────────────────────────────────────────────

const BCRYPT_ROUNDS = 10;

const USERS = [
  { id: 1, email: 'admin@example.com', password: 'admin123', name: '管理员', role: 'admin' },
  { id: 2, email: 'user@example.com', password: 'user123', name: '测试用户', role: 'user' },
];

// ──────────────────────────────────────────────
// 数据结构
// ──────────────────────────────────────────────

const categories = [
  { name: '电子产品', description: '手机、电脑、数码配件等电子产品', sort_order: 1 },
  { name: '服装',     description: '男装、女装、童装等服饰',        sort_order: 2 },
  { name: '食品',     description: '零食、饮料、生鲜等食品',        sort_order: 3 },
  { name: '书籍',     description: '文学、科技、教育等图书',        sort_order: 4 },
  { name: '家居',     description: '家具、家纺、日用品等家居产品',    sort_order: 5 },
];

const productsByCategory = {
  '电子产品': [
    { name: 'iPhone 15 Pro Max 256GB',          price: 8999.00, stock: 150, status: 'active', description: '苹果旗舰手机，A17 Pro 芯片，钛金属设计' },
    { name: 'MacBook Air M3 13.6"',             price: 9999.00, stock: 80,  status: 'active', description: '轻薄笔记本，M3 芯片，18 小时续航' },
    { name: 'Sony WH-1000XM5 降噪耳机',          price: 2499.00, stock: 200, status: 'active', description: '旗舰级降噪耳机，30 小时续航' },
    { name: 'Anker 65W GaN 充电器',             price: 299.00,  stock: 500, status: 'active', description: '氮化镓快充，支持笔记本/手机多设备' },
    { name: 'Samsung 1TB 移动固态硬盘 T7',      price: 899.00,  stock: 120, status: 'active', description: 'USB 3.2 Gen2，1050MB/s 读写' },
    { name: '罗技 MX Master 3S 鼠标',           price: 699.00,  stock: 180, status: 'active', description: '人体工学设计，8K DPI，无线充电' },
    { name: '戴尔 U2723QE 4K 显示器',            price: 4599.00, stock: 40,  status: 'active', description: '27 英寸 4K IPS Black，USB-C 90W 供电' },
    { name: 'Raspberry Pi 5 8GB',              price: 599.00,  stock: 300, status: 'active', description: '单板电脑，ARM Cortex-A76 四核' },
  ],
  '服装': [
    { name: '经典纯棉白 T 恤',                   price: 129.00,  stock: 1000, status: 'active', description: '100% 新疆棉，宽松版型' },
    { name: '轻量羽绒服',                        price: 599.00,  stock: 300,  status: 'active', description: '90% 白鹅绒，防风防泼水' },
    { name: '修身牛仔裤',                        price: 299.00,  stock: 500,  status: 'active', description: '弹力牛仔，百搭款' },
    { name: '运动跑步鞋',                        price: 459.00,  stock: 400,  status: 'active', description: '缓震回弹，透气网面' },
  ],
  '食品': [
    { name: '有机混合坚果 500g',                price: 89.00,   stock: 600, status: 'active', description: '腰果、杏仁、核桃混合装' },
    { name: '日式抹茶粉 100g',                  price: 68.00,   stock: 400, status: 'active', description: '宇治抹茶，烘焙冲饮皆可' },
    { name: '精品咖啡豆 哥伦比亚 250g',          price: 128.00,  stock: 250, status: 'active', description: '中浅烘焙，柑橘风味' },
    { name: '手工黑巧克力 72% 可可 80g',          price: 45.00,   stock: 800, status: 'active', description: '比利时工艺，低糖健康' },
  ],
  '书籍': [
    { name: '深入理解计算机系统 (CS:APP)',        price: 139.00,  stock: 200, status: 'active', description: '计算机科学经典教材，第3版' },
    { name: '设计模式：可复用面向对象软件的基础',   price: 79.00,   stock: 180, status: 'active', description: 'GoF 经典设计模式，程序员必读' },
    { name: '人类群星闪耀时',                     price: 49.00,   stock: 350, status: 'active', description: '斯蒂芬·茨威格历史特写集' },
    { name: '算法导论 (CLRS)',                   price: 128.00,  stock: 150, status: 'active', description: 'MIT 经典算法教材，第4版' },
  ],
  '家居': [
    { name: '人体工学办公椅',                    price: 1599.00, stock: 60,  status: 'active', description: '腰部支撑，可调节扶手，网面透气' },
    { name: '北欧风落地灯',                      price: 399.00,  stock: 120, status: 'active', description: '三色温调节，实木底座' },
    { name: '纯棉四件套 1.8m 床',               price: 499.00,  stock: 200, status: 'active', description: '60 支长绒棉，简约印花' },
    { name: '智能扫地机器人',                    price: 2499.00, stock: 90,  status: 'active', description: '激光导航，5000Pa 吸力，自动集尘' },
  ],
};

// ──────────────────────────────────────────────
// SQL 生成
// ──────────────────────────────────────────────

function generateSQL(passwordHashes) {
  const lines = [
    '-- ============================================================',
    '-- 示例种子数据 — 可重复执行 (使用 INSERT IGNORE)',
    '-- 生成时间: ' + new Date().toISOString(),
    '-- ============================================================',
    '',
    '-- ---------------------------',
    '-- 1. 商品分类',
    '-- ---------------------------',
  ];

  for (const cat of categories) {
    const desc = cat.description.replace(/'/g, "\\'");
    lines.push(
      `INSERT IGNORE INTO product_categories (id, name, description, sort_order) VALUES (${categories.indexOf(cat) + 1}, '${cat.name}', '${desc}', ${cat.sort_order});`
    );
  }

  lines.push('');
  lines.push('-- ---------------------------');
  lines.push('-- 2. 商品');
  lines.push('-- ---------------------------');

  let productId = 1;
  for (const [catName, products] of Object.entries(productsByCategory)) {
    const catIdx = categories.findIndex((c) => c.name === catName) + 1;
    for (const p of products) {
      const desc = p.description.replace(/'/g, "\\'");
      const name = p.name.replace(/'/g, "\\'");
      const imageUrl = `https://picsum.photos/seed/prod${productId}/400/400`;
      lines.push(
        `INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (${productId}, '${name}', ${p.price.toFixed(2)}, ${p.stock}, ${catIdx}, '${p.status}', '${desc}', '${imageUrl}');`
      );
      productId++;
    }
  }

  lines.push('');
  lines.push('-- ---------------------------');
  lines.push('-- 3. 示例用户');
  lines.push('-- ---------------------------');
  lines.push('');

  for (const u of USERS) {
    const ph = passwordHashes ? passwordHashes[u.id] : '$2a$10$placeholder_' + u.email.replace(/[^a-z]/g, '') + '_hash_change_me';
    lines.push(
      "INSERT IGNORE INTO users (id, email, password_hash, name, role) VALUES (" + u.id + ", '" + u.email + "', '" + ph + "', '" + u.name + "', '" + u.role + "');"
    );
  }

  lines.push('');
  lines.push('-- 密码说明：');
  for (const u of USERS) {
    lines.push('--   ' + u.name + ': email=' + u.email + ', password=' + u.password);
  }

  lines.push('');
  lines.push('-- ---------------------------');
  lines.push('-- 4. 测试订单');
  lines.push('-- ---------------------------');
  lines.push('');
  lines.push("INSERT IGNORE INTO orders (id, order_no, user_id, product_id, qty, amount, total, status) VALUES (1, 'ORD-TEST-20240101-0001', 2, 1, 1, 8999.00, 8999.00, 'completed');");

  lines.push('');
  lines.push('-- ---------------------------');
  lines.push('-- 5. 订单项');
  lines.push('-- ---------------------------');
  lines.push('');
  lines.push(`INSERT IGNORE INTO order_items (id, order_id, product_id, product_name, qty, price, subtotal) VALUES (1, 1, 1, 'iPhone 15 Pro Max 256GB', 1, 8999.00, 8999.00);`);

  return lines.join('\n') + '\n';
}

// ──────────────────────────────────────────────
// JSON 生成
// ──────────────────────────────────────────────

function generateJSON(passwordHashes) {
  const users = USERS.map((u) => ({
    id: u.id,
    email: u.email,
    password_hash: passwordHashes ? passwordHashes[u.id] : '<bcrypt-hash-here>',
    name: u.name,
    role: u.role,
  }));

  const productList = [];
  let pid = 1;
  for (const [catName, products] of Object.entries(productsByCategory)) {
    const catIdx = categories.findIndex((c) => c.name === catName) + 1;
    for (const p of products) {
      productList.push({
        id: pid,
        name: p.name,
        price: p.price,
        stock: p.stock,
        category_id: catIdx,
        status: p.status,
        description: p.description,
        image_url: `https://picsum.photos/seed/prod${pid}/400/400`,
      });
      pid++;
    }
  }

  const order = {
    id: 1,
    order_no: 'ORD-TEST-20240101-0001',
    user_id: 2,
    product_id: 1,
    qty: 1,
    amount: 8999.00,
    total: 8999.00,
    status: 'completed',
    items: [
      { id: 1, order_id: 1, product_id: 1, product_name: 'iPhone 15 Pro Max 256GB', qty: 1, price: 8999.00, subtotal: 8999.00 },
    ],
  };

  return JSON.stringify({ categories, products: productList, users, orders: [order] }, null, 2);
}

// ──────────────────────────────────────────────
// 入口
// ──────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const hashPasswords = args.includes('--hash-passwords');

  let passwordHashes = null;

  if (hashPasswords) {
    console.error('正在生成 bcrypt 密码哈希 (cost=' + BCRYPT_ROUNDS + ')...');
    passwordHashes = {};
    for (const u of USERS) {
      passwordHashes[u.id] = bcrypt.hashSync(u.password, BCRYPT_ROUNDS);
      console.error('  ' + u.email + ' -> ' + passwordHashes[u.id].substring(0, 30) + '...');
    }
    console.error('');
  }

  if (jsonMode) {
    console.log(generateJSON(passwordHashes));
  } else {
    console.log(generateSQL(passwordHashes));
  }
}

main();
