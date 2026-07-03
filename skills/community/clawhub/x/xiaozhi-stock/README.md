# 🦊 小智A股分析引擎

> 问一句股票，给你三个分析师的判断。多源数据 + 三维框架 + 双评分 + 对抗验证，武装到牙齿。

![License](https://img.shields.io/badge/license-MIT--0-green)
![Version](https://img.shields.io/badge/version-1.2.0-blue)
![Agent Skills](https://img.shields.io/badge/agent-skills-orange)
![OpenClaw](https://img.shields.io/badge/openclaw-compatible-purple)

---

## 你什么时候需要它？

- **查股票**：输入代码，立刻获得实时行情 + BigA评分 + 择时分
- **想买/卖**：问它能买吗，它会自己跟你吵一架（看涨vs看跌）再给结论
- **选股**：主动推池外候选，双信号对齐（长线OK + 短线入场OK + 风控通过）
- **盯大盘/板块**：大盘情绪 + 热点板块十强
- **管持仓**：动态股票池，超分入池低分出池

## 它会交付什么？

| 场景 | 交付物 | 预览 |
|------|--------|------|
| 行情查询 | 📊 格式化股票卡片 | 代码·名称·价格·涨跌·量能·PE·来源 |
| 个股分析 | 📋 三维分析报告 | 基本面→技术面→量化行为→对抗验证→建议 |
| 大盘情绪 | 📈 五指数+情绪+风险等级 | 上证/深成/创业/科创/北证 |
| 选股推荐 | 🐂 池外筛选卡片 | 评分·方向·入场区间·止损·目标·核心理由 |

## 快速开始

无需安装任何额外插件或API Key：

```bash
# 查询单只股票
python3 skills/xiaozhi-stock/scripts/fetch_stock.py --code 600519

# 查询大盘指数
python3 skills/xiaozhi-stock/scripts/fetch_stock.py --index

# 热点板块TOP10
python3 skills/xiaozhi-stock/scripts/fetch_stock.py --hot-sectors

# JSON输出供程序调用
python3 skills/xiaozhi-stock/scripts/fetch_stock.py --code 600519 --json
```

**在Agent中使用：**
```
用户："分析一下600519"
Agent → 触发xiaozhi-stock → 调用fetch_stock.py获取行情 → 三维分析 → 双评分 → 对抗验证 → 输出建议
```

## 触发方式

| 你说 | 它做 |
|------|------|
| "茅台多少钱" | 实时行情卡片 |
| "分析中芯国际" | 完整三维分析报告 |
| "今天大盘怎么样" | 五指数+情绪+风险 |
| "有什么好股推荐" | 池外筛选+双信号对齐 |
| "能买宁德时代吗" | 生成+对抗验证+结论 |

## 它和同类有什么不同？

| 维度 | 小智引擎 | 同类技能 |
|------|---------|---------|
| 数据源 | 新浪+东财+腾讯+同花顺 自动切备 | 固定单源或双源 |
| 评分体系 | BigA总分(0-100)+择时分(-10~+10) 正交使用 | 单评分或纯技术面 |
| 验证机制 | 对抗验证（看涨→挑刺→综判） | 无内部验证 |
| ST分析 | 专项五维度ST分析框架 | 少数支持 |
| 脚本层 | multi-stock/大盘/板块/JSON 全场景覆盖 | 多为纯LLM推理 |

## 实现架构

```
用户输入 → 意图识别
  → 数据层（新浪→东财→腾讯 自动切备）
  → 分析层（基本面+技术面+量化行为金融）
  → 评分层（BigA综合分 0-100 + 择时分 -10~+10）
  → 验证层（生成→反向→综判）
  → 风控层（双信号对齐 + 三重过滤）
  → 输出层（场景模板格式化）
```

## 安全边界

- ✅ 不依赖任何API Key（全部使用公开免费API）
- ✅ 不影响任何外部系统状态（只读）
- ✅ 不删除/修改用户文件或配置
- ✅ 建议前附风险提示
- ✅ 数据源故障自动切换（不中断服务）

## 文件结构

```
xiaozhi-stock/
├── SKILL.md                  ← 技能主文件（含完整流程定义）
├── README.md                 ← 展示页（你正在读的）
├── references/
│   ├── analysis-methods.md   ← 技术/基本面分析细则
│   ├── data-sources.md       ← 三源API参数参考
│   └── technical-timing.md   ← 择时分评分规则
└── scripts/
    └── fetch_stock.py        ← 多源行情抓取脚本
```

## License

MIT-0 — 免费使用、修改、再分发，无需署名。
