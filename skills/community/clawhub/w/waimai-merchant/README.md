# Waimai Merchant - 外卖商家管理

外卖商家管理系统 CLI 工具，支持商家注册、商品管理、价格修改和配送承诺时间设置。

## 功能特性

- ✅ 商家注册与管理
- ✅ 商品上传与管理
- ✅ 价格修改
- ✅ 配送承诺时间设置
- ✅ 商家认证流程
- ✅ 商品上下架管理
- ✅ 库存管理
- ✅ 分类管理

## 快速开始

### 安装依赖

```bash
cd ~/.openclaw/workspace/skills/waimai-merchant
npm install
```

### 编译 TypeScript

```bash
npm run build
```

### 运行 CLI

```bash
# 查看帮助
node dist/index.js --help

# 查看数据存储位置
node dist/index.js data
```

## 使用示例

### 商家管理

```bash
# 注册新商家
node dist/index.js merchant register \
  -n "美味餐厅" \
  -p "13800138000" \
  -a "北京市朝阳区xxx街道" \
  -c "张经理"

# 列出所有商家
node dist/index.js merchant list

# 认证商家
node dist/index.js merchant approve 1

# 查看商家详情
node dist/index.js merchant show 1
```

### 商品管理

```bash
# 添加商品
node dist/index.js product add \
  -m 1 \
  -n "招牌红烧肉" \
  -p 38.00 \
  -o 48.00 \
  -d "肥而不腻，入口即化" \
  -c "热菜" \
  -t 30 \
  -s 100

# 列出商品
node dist/index.js product list

# 修改价格
node dist/index.js product price 1 35.00

# 修改配送时间
node dist/index.js product delivery 1 25

# 上架商品
node dist/index.js product activate 1
```

## 项目结构

```
waimai-merchant/
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript 配置
├── README.md             # 项目说明
├── SKILL.md              # OpenClaw Skill 文档
├── src/
│   ├── index.ts          # 主入口
│   ├── commands/         # CLI 命令实现
│   │   ├── index.ts
│   │   ├── merchant.ts   # 商家命令
│   │   └── product.ts    # 商品命令
│   └── db/               # 数据存储层
│       ├── index.ts
│       ├── database.ts   # 数据库连接
│       ├── merchant.ts   # 商家数据操作
│       └── product.ts    # 商品数据操作
└── dist/                 # 编译输出（npm run build 生成）
```

## 数据存储

数据存储在本地 SQLite 数据库：
- 位置: `~/.waimai-merchant/merchant.db`
- 包含表: `merchants`, `products`

## 技术栈

- **TypeScript** - 类型安全的 JavaScript
- **Node.js** - 运行时环境
- **SQLite** - 轻量级数据库
- **Commander.js** - CLI 框架
- **Chalk** - 终端样式

## 开发

```bash
# 开发模式（直接运行 TypeScript）
npm run dev

# 编译
npm run build

# 清理编译输出
npm run clean
```

## 许可证

MIT
