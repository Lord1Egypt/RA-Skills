# OpenCode Skill Package: 时寒冰式多维投资分析模型（增强版）

## 目录结构

```text
.opencode/
├─ skills/
│  └─ shihanbing-investment-analysis/
│     └─ SKILL.md
└─ commands/
   ├─ invest-analyze.md
   ├─ invest-compare.md
   └─ invest-thesis.md
opencode.json.example
README.md
```

## 安装方式

### 方式一：项目内安装
把整个 `.opencode` 目录复制到你的项目根目录。

### 方式二：全局安装
把技能目录复制到：

```text
~/.config/opencode/skills/shihanbing-investment-analysis/
```

如果你也想使用命令，把命令文件复制到：

```text
~/.config/opencode/commands/
```

## 推荐权限
把 `opencode.json.example` 中的 `permission` 合并到你自己的 `opencode.json`。

## 触发方式

### 自动触发（由 OpenCode 根据描述判断）
直接对话输入：
- 用时寒冰式多维投资分析模型分析铀矿
- 分析英伟达现在是观察还是中仓
- 比较黄金股和铜矿股谁更值得配置

### 命令触发
- `/invest-analyze 铀矿主题是否值得中期配置`
- `/invest-analyze 分析英伟达的宏观逻辑、护城河和时机`
- `/invest-compare 黄金 vs 铀矿，谁更适合当前配置`
- `/invest-thesis AI 带动数据中心电力需求，核电和铀矿是否受益`

## 适用范围
- 股票
- 商品与资源主题
- ETF/指数
- 国家与地区配置

## 这个增强版相比基础版新增了什么
- 资产类别分流：股票 / 商品 / ETF / 国家配置
- 四维评分器
- 风险反证模块
- 对比分析模式
- 投研备忘录模式
- 命令模板

## 使用建议
1. 先让模型判断大势，不要一上来就问会不会涨。
2. 对高波动主题，优先使用“观察 / 轻仓 / 中仓”的梯度表达。
3. 如果你接了 WebSearch/WebFetch，再让它引用最新资料，效果更好。
