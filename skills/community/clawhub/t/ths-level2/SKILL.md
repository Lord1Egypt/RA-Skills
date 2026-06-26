---
name: ths-level2
description: |
  同花顺Level2数据获取与深度分析工具。支持读取同花顺远航版本地数据、
  分析股票行情、获取实时Level2数据、生成技术分析报告。
  用于：(1) 获取持仓股票实时数据 (2) Level2资金流向分析 (3) 个股深度分析 (4) 生成投资策略报告
---

# 同花顺Level2数据接入Skill

通过分析同花顺远航版客户端实现Level2数据获取与深度分析。

## 📦 安装方法

### 方法一：直接复制（推荐）
```bash
# 复制整个目录到你的skills目录
cp -r ths_level2 ~/.openclaw/skills/
```

### 方法二：Git克隆
```bash
# 克隆到skills目录
git clone https://github.com/your-repo/ths-level2.git ~/.openclaw/skills/ths_level2
```

### 方法三：手动创建
1. 在 `~/.openclaw/skills/` 目录下创建 `ths_level2` 文件夹
2. 将以下必需文件放入该文件夹：
   - `SKILL.md` (本文件)
   - `_meta.json`
   - `.clawhub/manifest.json`
   - 核心Python脚本文件

## 🔧 必需文件结构

```
ths_level2/
├── SKILL.md                    # 技能描述文件 ✅
├── _meta.json                  # 元数据文件 ✅  
├── .clawhub/                   # 技能标识目录 ✅
│   └── manifest.json           # 清单文件
├── config.json                 # 配置文件 ✅
├── ths_client.py               # TCP客户端 ✅
├── ths_local_analysis.py       # 本地分析工具 ✅
├── complete_technical_analysis.py # 完整技术指标 ✅
├── chip_analysis.py            # 筹码分析 ✅
└── level2_integration.py       # Level2集成分析 ✅
```

## ⚙️ 配置说明

### 1. 基础配置 (`config.json`)
```json
{
  "tushare_token": "your-tushare-token-here",
  "ths_path": "D:\\同花顺远航版",
  "default_stocks": [
    {"code": "600276.SH", "name": "恒瑞医药"},
    {"code": "600760.SH", "name": "中航沈飞"},
    {"code": "600999.SH", "name": "招商证券"},
    {"code": "601888.SH", "name": "中国中免"},
    {"code": "002202.SZ", "name": "金风科技"},
    {"code": "300188.SZ", "name": "国投智能"}
  ]
}
```

### 2. Tushare Token配置（可选但推荐）
- 获取Token: https://tushare.pro/register
- 设置环境变量:
  ```bash
  # Windows
  setx TUSHARE_TOKEN your_token_here
  
  # Linux/Mac
  export TUSHARE_TOKEN=your_token_here
  ```

## 🚀 使用方法

### 快速开始（无需配置）
```bash
# 基础持仓分析
python ths_local_analysis.py

# 完整技术指标分析  
python complete_technical_analysis.py

# 筹码分析
python chip_analysis.py

# Level2深度分析
python level2_integration.py
```

### 高级功能（需要Tushare Token）
```bash
# 获取真实行情数据
python ths_full_analysis.py

# 连接同花顺服务器
python ths_client.py
```

### API调用方式
```python
from ths_local_analysis import TechnicalAnalyzer

# 分析单只股票
analyzer = TechnicalAnalyzer("600276", {
    "name": "恒瑞医药",
    "cost": 53.12,
    "shares": 1000,
    "current": 51.63,
    "change": -2.80
})
result = analyzer.analyze_position("600276", stock_info)
print(result)
```

## 📊 功能特性

### 1. 技术指标分析
- **MACD/KDJ/RSI** - 经典技术指标
- **神奇五线谱** - MA5/MA10/MA20/MA60/MA120多均线评分
- **神奇九转** - 连续9日同向变化反转信号
- **牛熊线** - 长期趋势判断
- **多空线** - 短期多空状态

### 2. 资金分析
- **资金抄底** - 价格超跌+量能配合信号
- **主力净额** - 主力资金流入/流出强度
- **成交量分析** - 量比、放量/缩量判断

### 3. 筹码分析
- **筹码分布** - 价格区间筹码密集区识别
- **股东人数变化** - 识别筹码集中/分散趋势
- **获利盘比例** - 估算市场获利盘占比
- **压力支撑位** - 基于筹码密集区计算

### 4. Level2数据
- **五档行情** - 实时买卖盘口数据
- **成交明细** - Level2逐笔成交分析
- **大单统计** - 主力资金流向判断
- **市场深度** - 买卖盘对比分析

### 5. 智能建议系统
- **综合评分** - 0-100分量化评分
- **操作建议** - 积极关注/适度关注/观望/回避
- **关键信号** - 自动提取重要技术信号

## 📁 文件说明

| 文件 | 功能 | 依赖 |
|------|------|------|
| `ths_local_analysis.py` | 基础持仓分析 | 无需Token ✅ |
| `complete_technical_analysis.py` | 完整技术指标 | 无需Token ✅ |
| `chip_analysis.py` | 筹码分析 | 无需Token ✅ |
| `level2_integration.py` | Level2深度分析 | 无需Token ✅ |
| `ths_full_analysis.py` | 完整分析 | 需要Tushare Token |
| `ths_client.py` | 数据客户端 | 需要同花顺运行 |

## 🌐 数据来源

- **本地数据库**: `D:\同花顺远航版\bin\stockname\stocknameV2.db`
- **Tushare API**: https://tushare.pro (需要Token)
- **同花顺服务器**: hevo-h.10jqka.com.cn:9601
- **协议文件**: `DataPushJob.xml`

## 📝 输出结果

所有分析脚本都会生成JSON结果文件：
- `ths_analysis.json` - 基础分析结果
- `complete_analysis_results.json` - 完整技术指标结果  
- `chip_analysis_results.json` - 筹码分析结果
- `level2_analysis_results.json` - Level2分析结果

## ⚠️ 注意事项

1. **合规使用**: 本工具仅供学习研究使用，请遵守相关法律法规和用户协议
2. **数据权限**: 同花顺Level2数据为付费服务，请确保您已开通相关权限
3. **网络要求**: 部分功能需要网络连接，确保防火墙允许访问
4. **管理员权限**: 内存读取功能需要以管理员权限运行

## 🆘 故障排除

### 常见问题
**Q: 运行报错"UnicodeEncodeError"**
A: 确保系统编码为UTF-8，或在命令前添加 `chcp 65001`

**Q: 无法连接同花顺服务器**  
A: 检查网络连接，或使用本地分析模式

**Q: 缺少依赖库**
A: 安装所需库: `pip install akshare pandas numpy`

### 调试命令
```bash
# 测试本地数据读取
python ths_client.py

# 测试基础分析
python ths_local_analysis.py

# 查看配置
cat config.json
```

## 📈 版本信息

- **版本**: 1.0.0
- **作者**: TE
- **最后更新**: 2026-03-27
- **兼容性**: OpenClaw v1.0+

## 🔗 相关资源

- **同花顺官网**: https://www.10jqka.com.cn/
- **Tushare文档**: https://tushare.pro/document/1
- **OpenClaw文档**: https://docs.openclaw.ai

---
> 💡 **提示**: 对于日常使用，推荐先运行 `ths_local_analysis.py` 进行快速分析，再根据需要使用其他深度分析工具。