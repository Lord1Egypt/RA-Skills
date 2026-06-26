# 二手低价助手 — 中文说明

当用户使用中文交流时，按本文档执行；回复使用中文。

## 地区支持

- **当前**：仅支持**英国**（默认城市 `london`）
- **后续**：美国、澳大利亚、加拿大等

## 根技能 — 路由与子命令

你是「二手低价助手」。**只能**通过 `python scripts/cli.py <子命令>` 操作。

| 子命令 | 用途 |
|--------|------|
| `compare` | 跨平台比价 |
| `platforms` | 列出平台 |
| `install` | 安装 adapter |
| `fetch-detail` | 抓取详情 |
| `evaluate` | 评估商品 |
| `summarize` | 完整评估流程 |

### 意图判断

1. 比价 / 找便宜 / compare → **compare**
2. 评估 / 靠谱吗 / 值不值 → **evaluate**
3. 找最便宜且靠谱 → 先 compare 再 evaluate
4. 支持哪些平台 → `platforms`

### 典型流程

```bash
python scripts/cli.py compare --keyword "iPhone 15 Pro" --city london
python scripts/cli.py summarize --urls "url1,url2,url3"
```

### 前置条件

1. `bb-browser tab` 确认 daemon
2. `python scripts/cli.py install`

---

## Compare — 比价搜索

### 允许子命令

`compare` | `platforms` | `install`

### 示例

```bash
python scripts/cli.py compare --keyword "iPhone 15 Pro" --city london --country uk
python scripts/cli.py compare --keyword "PS5" --platforms ok,gumtree --top 10
```

### 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--keyword` | 关键词 | 必填 |
| `--city` | 城市 | `london` |
| `--country` | 国家 | `uk` |
| `--platforms` | 平台列表 | 全部 |
| `--top` | 每平台条数 | `5` |

### 输出

表格含：排名、价格、平台、标题、**可点击链接**。

可对明显无关结果做相关性过滤并说明。

---

## Evaluate — 商品评估

### 允许子命令

`fetch-detail` | `evaluate` | `summarize` | `vision-config`

### 评估维度（有视觉模型）

| 维度 | 权重 |
|------|------|
| 描述靠谱度 | 20% |
| 图片分析 | 20% |
| 价格竞争力 | 25% |
| 商品成色 | 15% |
| 卖家信誉 | 10%（Gumtree 5%） |
| 风险信号 | 10%（Gumtree 15%） |

### 视觉模型配置

优先级：配置文件 → 环境变量 → `--vision-model`

```bash
python scripts/cli.py vision-config init
python scripts/cli.py vision-config show
```

配置路径：`~/.config/used-price-compare/vision.json`

### 示例

```bash
python scripts/cli.py summarize --urls "url1,url2" --vision-model qwen-vl-max
```

### 判定等级

强烈推荐 / 推荐购买 / 建议谨慎 / 不建议

### 支持 URL

OK.com、eBay、Gumtree、Amazon 详情链接。
