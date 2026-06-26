# spending-log

个人消费记录 OpenClaw Skill。支持自然语言记账、自动分类、月度统计、预算提醒和精美 HTML 报表生成。

## 功能

- **自然语言记账** — "午饭35"、"昨天打车25"、"买书128"
- **自动分类** — 餐饮、交通、购物、娱乐、医疗、房租、日用、社交、其他
- **月度统计** — 按分类、日期、金额等多维度查询
- **预算提醒** — 每次记账自动检查，超支主动提醒
- **HTML 报表** — 交互式 SVG 饼图/柱状图，交叉筛选，环比对比，PC/手机自适应
- **CSV 导出** — 一键导出当月明细

## 安装

### 方式一：ClawHub（推荐）

```bash
openclaw skills install spending-log
```

### 方式二：手动安装

1. 克隆仓库到 OpenClaw skills 目录：

```bash
cd ~/.openclaw/skills
git clone https://github.com/baoxinwen/spending-log.git
```

2. 确保 Python 3 可用（脚本无需额外依赖）

3. 重启 OpenClaw 或执行 `openclaw skills reload`

## 使用

对 OpenClaw 说以下任意指令即可触发：

| 说法 | 动作 |
|------|------|
| 午饭35 | 记一笔餐饮支出 |
| 昨天打车花了25 | 记一笔昨天的交通支出 |
| 这个月花了多少 | 查看当月统计 |
| 4月餐饮花了多少 | 按分类查询 |
| 预算还剩多少 | 查看预算余额 |
| 生成报表 / 月度报表 | 生成 HTML 报表 |
| 删除刚才那条 | 删除最近一条记录 |
| 把午饭改成40 | 修改记录 |

## 项目结构

```
spending-log/
├── SKILL.md              # Skill 定义（OpenClaw 入口）
├── scripts/
│   ├── module.py         # 共享配置和数据层
│   ├── crud.py           # 增删改查操作
│   ├── query.py          # 统计查询
│   └── report.py         # HTML/CSV 报表生成
└── data/                 # 用户数据（运行时生成）
    ├── expenses.json     # 消费记录
    └── config.json       # 配置（月预算）
```

## 配置

月预算默认 2000 元，可通过修改 `data/config.json` 调整：

```json
{ "monthly_budget": 3000 }
```

## 报表预览

生成的 HTML 报表包含：

- **月度总览** — 总支出、预算环形进度、日均支出、最高单笔/最高消费日
- **支出分布** — SVG 交互饼图，hover/点击查看详情
- **分类详情** — 各分类金额、占比、进度条
- **每日趋势** — SVG 柱状图 + 日均参考线
- **消费明细** — 支持分类+日期交叉筛选，联动饼图/分类卡片/趋势图
- **环比对比** — 与上月各分类涨跌对比
- **月份导航** — 顶部箭头快速切换月份

## License

MIT
