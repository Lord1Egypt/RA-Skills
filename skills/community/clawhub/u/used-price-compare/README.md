# Used Price Compare — 二手低价助手

跨平台二手商品比价与深度评估工具，通过 bb-browser site adapter 实现对多个二手交易平台的 CLI 化访问。

## 架构

```
used-price-compare/
├── SKILL.md                          # 根 Skill（路由 compare / evaluate）
├── skills/
│   ├── compare/SKILL.md              # 比价子技能
│   └── evaluate/SKILL.md             # 评估子技能
├── adapters/                         # bb-browser site adapters
│   ├── ok/                           # OK.com 搜索 + 详情
│   ├── gumtree/                      # Gumtree 搜索 + 详情
│   ├── ebay/                         # eBay 搜索 + 详情（per-country）
│   └── amazon/                       # Amazon 搜索 + 详情（per-country）
├── scripts/
│   ├── cli.py                        # CLI 入口
│   ├── smoke_test.py                 # 发布前冒烟测试
│   └── used_price_compare/
│       ├── compare.py                # 多平台比价引擎
│       ├── fetcher.py                # 详情页抓取
│       ├── evaluator.py              # 商品评估与视觉模型
│       └── platforms.py              # 平台定义、city→country 路由
├── CHANGELOG.md
└── LICENSE
```

## 多国域名架构

bb-browser 的 `domain` 字段是静态的——adapter 只能在匹配域名的 tab 上下文中执行 fetch。
对于 eBay、Amazon 这类不同国家使用不同域名的平台，采用 **per-country adapter** 方案：

- 每个国家一个 adapter 文件（`search-us.js`、`search-uk.js` 等）
- 共享同一份解析逻辑（`_template.js`），通过 `build.js` 构建生成
- `platforms.py` 中的 `resolve_platforms()` 根据 `city→country` 映射自动路由

```
用户: --keyword "iPhone" --city london
  → city "london" → country "uk"
  → 选择 ebay-uk (domain: www.ebay.co.uk)
  → bb-browser site ebay/search-uk "iPhone"

用户: --keyword "iPhone" --city los-angeles
  → city "los-angeles" → country "us"
  → 选择 ebay-us (domain: www.ebay.com)
  → bb-browser site ebay/search-us "iPhone"

用户: --platforms ebay-uk （显式指定）
  → 直接使用 ebay-uk，不走 city 推断
```

### 新增国家

```bash
# 1. 在 adapters/ebay/build.js 的 SITES 数组中添加条目
# 2. 运行构建
node adapters/ebay/build.js

# 3. 在 scripts/used_price_compare/platforms.py 中添加 Platform 实例 + CITY_COUNTRY_MAP 条目
# 4. 重新安装
python scripts/cli.py install
```

## 快速开始

### 前置条件

```bash
# 1. 安装 bb-browser
npm install -g bb-browser

# 2. 启动 bb-browser daemon（浏览器需以调试模式启动）
# macOS:
open -a "Google Chrome" --args --remote-debugging-port=9222
```

### 安装 Adapters

```bash
cd used-price-compare
python scripts/cli.py install
```

### 使用

```bash
# 比价搜索（默认 city: los-angeles → eBay US）
python scripts/cli.py compare --keyword "iPhone 15 Pro"

# 指定城市（自动路由到对应国家的 eBay）
python scripts/cli.py compare --keyword "PS5" --city london        # → eBay UK
python scripts/cli.py compare --keyword "PS5" --city sydney        # → eBay AU
python scripts/cli.py compare --keyword "PS5" --city toronto       # → eBay CA

# 显式指定平台
python scripts/cli.py compare --keyword "MacBook Air" --platforms ebay-uk
python scripts/cli.py compare --keyword "MacBook Air" --platforms ebay  # auto-route

# 指定平台组合
python scripts/cli.py compare --keyword "MacBook Air" --platforms ok,gumtree,ebay

# 查看支持的平台
python scripts/cli.py platforms

# 商品评估（可选视觉模型，见 skills/evaluate/SKILL.md）
python scripts/cli.py summarize --urls "https://us.ok.com/en/item/123,https://www.ebay.com/itm/456"
```

### 重新构建 eBay Adapters

修改 `_template.js` 后运行：

```bash
node adapters/ebay/build.js
python scripts/cli.py install
```

## 发布前检查

```bash
python scripts/smoke_test.py
```

## 技术选型

使用 bb-browser（CDP 直连方案）而非 Chrome Extension Bridge，原因：

1. **多平台覆盖** — 一个 daemon 操控所有网站，通过 adapter 扩展
2. **零扩展安装** — `npm install -g bb-browser` 一条命令
3. **通用框架** — 每站一个 JS adapter 文件，边际成本极低
4. **MCP 原生支持** — 未来可直接接入 Cursor / Claude Code
