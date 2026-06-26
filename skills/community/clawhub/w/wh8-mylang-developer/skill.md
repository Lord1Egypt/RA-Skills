# WT8Skill

文华财经WT8麦语言量化交易助手

## 功能定位

专注量化交易模型编写、回测、运行

## 核心能力

- 量化模型编写
- 历史回测分析
- 参数优化定参
- 策略运行管理
- 头寸风险管理
- 跨周期跨合约

## 文件结构

```
WT8Skill/
├── skill.md              # 本文件
├── skill.yaml            # 元数据
├── README.md             # 使用指南
├── HOW_TO_USE.md         # 使用方法
├── SYSTEM_PROMPT.md      # AI提示词
├── SYNTAX.md             # 语法规范
├── CLASSIFICATION.md      # 需求分类
├── FUNCTIONS/
│   ├── INDEX.md          # 函数索引
│   ├── signals.md        # 信号指令
│   ├── indicators.md     # 技术指标
│   ├── position.md       # 持仓资金
│   ├── backtest.md       # 回测函数
│   ├── optimization.md   # 优化函数
│   ├── cross.md          # 跨周期合约
│   └── execution.md      # 运行优化
├── EXAMPLES/
│   ├── basic_model.md    # 基础模型
│   ├── stop_loss.md      # 止损止盈
│   ├── position_management.md  # 头寸管理
│   ├── batch_entry.md    # 分批进出
│   └── cross_cycle.md    # 跨周期
├── EDGE_CASES/
│   └── common_mistakes.md # 常见错误
└── TEMPLATES/
    └── model_template.md # 模型模板
```

## 快速开始

### 编写量化模型

```
请帮我编写一个WT8模型：
1. 双均线金叉买，死叉卖
2. 止损15跳
3. 日线周期
```

### 核心信号

```mql
// 开平仓
BK/SK    // 买开/卖开
BP/SP    // 买平/卖平

// 止损
CLOSE<=BKPRICE-15*MINPRICE,SP

// 必须
AUTOFILTER;
```

## 官方文档

- 麦语言教程：https://wt8.wenhua.com.cn/#/download/download/2
- 语法说明：https://www.wenhua.com.cn/guide/views41a3.htm
