# Stock Decision Skill 更新日志

## [2.4.0] - 2026-04-01

### 关键修复
- **修复历史回测引擎重大bug**: 修复 backtest.py 多个关键问题
  - 修复 API 参数错误: `day` → `daily`, `qfq` → `hfq`
  - 修复数据结构解析: 使用正确路径 `data['data']['nodes']` 和 `data['data']['items']`
  - 修复技术指标字段映射: `tech.get('ma', {}).get('MA_5', 0)` 而非 `tech.get('MA5', 0)`
  - 修复除零错误: 预先计算风险收益比后再格式化
  - 添加价格验证: 防止买入价格为0或负数
  - 添加异常处理: 增强代码健壮性

- **修复宏观分析器误报问题**: 优化 macro_analyzer.py 搜索结果提取
  - 新增 `extract_search_summaries()` 函数: 仅提取搜索结果摘要,避免HTML噪声
  - 修复治理风险误报: 全页面搜索导致67个虚假严重风险
  - 提高风险阈值: 从 >=1 提升至 >=5,减少误报
  - 成功消除泡泡玛特等正常股票的误报

### 回测功能验证
- 成功运行泡泡玛特回测: 4笔交易,25%胜率,总收益+3.27%
- 回测数据完整性修复: 从2天数据恢复到120天完整数据
- 技术指标准确解析: MA/MACD/KDJ/RSI/DMI 指标正常读取

### 文档更新
- 更新 CHANGELOG.md 记录 v2.4.0 所有关键修复
- 确保版本号一致性

---

## [2.3.0] - 2026-04-01

### 关键修复
- **修复治理风险识别问题**: 优化搜索关键词，成功识别超微电脑管理层被捕等严重治理风险
- 改进宏观分析器(macro_analyzer.py)搜索策略，增加更多风险类型关键词

### 改进优化
- **行业周期搜索**: 针对美股使用英文关键词，包含trend/outlook/cycle/performance等多维度
- **公司治理搜索**: 大幅扩展风险关键词，覆盖:
  - 严重风险: fraud, arrest, criminal, indictment, FBI, delisting, accounting scandal
  - 中等风险: SEC investigation, lawsuit, regulatory, class action
  - 轻微风险: CEO change, management change, controversy
- **宏观经济搜索**: 针对美国市场使用英文关键词，包含economy outlook/Fed rate/inflation等

### 风险识别能力提升
- 成功识别67个严重风险关键词和75个中等风险关键词
- 准确识别FBI调查、管理层逮捕、财务欺诈、退市风险
- 风险系数从1.0提升至2.0 (严重风险)
- 调整系数从1.0降至0.5 (重大折价)

### 技术细节
- 每个搜索类别使用6组关键词，覆盖更多风险维度
- 增加搜索结果关键词计数和显示
- 优化风险判断逻辑，提高准确性
- 增加严重风险警告提示

### 文档更新
- 更新CHANGELOG.md记录v2.3.0改进
- 更新超微电脑分析报告,包含治理风险详情

---

## [2.2.0] - 2026-04-01

### 新增功能
- 宏观分析器(macro_analyzer.py)使用真实网页搜索替代模拟数据
- 实现方式: Python requests库 + Bing/Google搜索API, 命令行curl作为备用
- 增加搜索结果解析、错误处理、回退机制、超时控制

### 改进优化
- 优化搜索关键词,覆盖更多维度
- 增加搜索引擎反爬虫处理
- 改进搜索结果分析逻辑

### 技术细节
- 使用Bing搜索API的HTML版本
- 支持多种搜索引擎回退机制
- 搜索超时控制在10-20秒

### 文档更新
- 更新CHANGELOG.md
- 更新README.md使用说明

---

## [2.1.0] - 2026-04-01

### 新增功能
- 按照WorkBuddy技能标准规范重写SKILL.md
- 添加完整的YAML元数据(name/description/version/allowed-tools)
- 添加触发条件、核心功能、使用方法、输出格式等标准章节

### 改进优化
- 符合标准规范的SKILL.md格式
- 结构化的功能介绍
- 完整的使用示例和输出格式说明

### 文档更新
- 添加版本历史记录
- 更新README.md
- 添加CHANGELOG.md

---

## [2.0.0] - 2026-03-31

### 新增功能
- 宏观环境自动化分析器(macro_analyzer.py)
- 历史回测功能(backtest.py)
- 综合评分系统(技术面+基本面)
- 止盈止损价位计算

### 改进优化
- 优化SKILL.md,增加宏观自动化和回测功能的详细说明
- 优化README.md,更新功能说明,反映新增功能

### 文档更新
- 添加CHANGELOG.md
- 更新README.md
- 更新IMPLEMENTATION.md

---

## [1.0.0] - 2026-03-30

### 初始版本
- 技术指标分析(MA, MACD, KDJ, RSI, DMI)
- 买入条件判断(7个条件)
- 高位预警系统(6个预警)
- 技术评分计算(0-100分)
- 基础止盈止损建议

### 文档
- SKILL.md
- README.md
- IMPLEMENTATION.md
- scripts/analyze.py
