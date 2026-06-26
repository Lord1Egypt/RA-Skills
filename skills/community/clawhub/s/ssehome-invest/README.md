# 📊 投资研究报告技能

## 快速开始

### 1. 安装依赖

```bash
cd skills/ssehome-invest
pip install -r requirements.txt
```

### 2. 配置 Tavily API（可选，用于新闻搜索）

在 `~/.openclaw/.env` 中添加：

```bash
TAVILY_API_KEY=tvly-你的API_Key
```

### 3. 运行分析

```bash
# 默认分析 002328 新朋股份
python3 analyze_stock.py

# 或在 Python 中调用
python3 -c "from analyze_stock import analyze_stock; analyze_stock('002328', '新朋股份')"
```

### 4. 查看报告

生成的报告保存在工作区的 `data/` 目录：

- `{股票代码}_investment_report.md` - Markdown 格式报告

## 功能特性

✅ **多时间框架分析**
- 3 年趋势分析（与大盘对比）
- 3 个月月度表现（月线三连阳检测）
- 6 个月横盘检测（突破判断）
- 1 周技术指标（MACD/RSI/DMI/BOLL）

✅ **均线系统**
- 5/14/21/89/250 日均线
- 多空头排列评分

✅ **新闻热点搜索（Tavily）**
- 公司动态
- 产品与业务
- 行业动态
- 情感分析与股价影响评估

✅ **专业报告生成**
- Markdown 格式（可编辑）

## 分析模块对照

| 要求 | 状态 |
|------|------|
| 获取近 3 年 K 线数据（baostock） | ✅ |
| 近三年走势与大盘相关性 | ✅ |
| 近三月涨跌幅和成交量（月线三连阳） | ✅ |
| 近六月横盘和突破分析 | ✅ |
| 近一周 MACD/RSI/DMI/BOLL | ✅ |
| 均线系统 (5/14/21/89/250) | ✅ |
| Tavily 新闻搜索与情感分析 | ✅ |
| 生成 Markdown 报告 | ✅ |

## 数据源说明

### baostock（唯一数据源）

- 优点：稳定、免费、无需 API Key
- 安装：`pip install baostock`
- 数据：A股日K线、指数数据

### 新闻搜索（Tavily，可选）

- 优点：AI 优化的搜索结果，支持深度搜索
- 安装：`pip install tavily-python`
- 配置：在 `~/.openclaw/.env` 中设置 `TAVILY_API_KEY`
- 未配置时跳过新闻搜索，不影响其他功能

## 示例输出

```
开始分析股票：新朋股份 (002328)
============================================================
📡 正在获取 2023-04-02 至 2026-04-02 的 K 线数据...
🔸 使用 baostock 数据源...
✅ 成功通过 baostock 获取 730 条数据

🔍 执行各项分析...
  - 三年趋势分析...
    三年收益率：29.28%
  - 三个月表现分析...
    月线三连阳：是
  - 六个月横盘分析...
    横盘判断：否
  - 一周技术分析...
    MACD: 多头, RSI: 55.46 (中性)
  - 均线系统分析...
    均线评分：4/5，趋势：部分多头

📰 正在搜索 新朋股份 相关新闻...
  🔍 搜索公司动态... 找到 5 条
  🔍 搜索产品业务... 找到 3 条
  🔍 搜索行业动态... 找到 3 条

📝 生成 Markdown 报告...
✅ Markdown 报告已保存：data/002328_investment_report.md

📊 分析完成！
```

## 自定义分析

编辑 `analyze_stock.py` 文件最后一行：

```python
if __name__ == "__main__":
    analyze_stock("股票代码", "股票名称")
```

## 故障排除

### 无法获取数据
- 检查 baostock 网络连接
- baostock 有时网络不稳定，稍后重试即可

### Tavily 搜索失败
- 确认 `~/.openclaw/.env` 中配置了正确的 `TAVILY_API_KEY`
- 未配置 API Key 时会跳过新闻搜索，不影响技术分析

---

**版本**: 1.0.3  
**许可**: MIT License  
**最后更新**: 2026-04-02
