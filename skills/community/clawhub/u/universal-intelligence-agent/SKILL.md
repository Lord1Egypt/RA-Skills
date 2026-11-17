---
name: universal-intelligence-agent
version: 1.0.0
description: "万能情报员：16引擎搜索+智能反爬+免费LLM+NLP+无损状态。零API key成本，一链搞定信息采集到分析"
allowed-tools:
  - web_search
  - web_fetch
  - read
  - write
  - edit
  - exec
  - cron
  - sessions_spawn
---

# 万能情报员 Universal Intelligence Agent v1.0.0

> 融合自：multi-search-engine / Scrapling / freellmapi / funNLP / lossless-claw / awesome-mental-models / CloakBrowser
>
> 零API key，零配置。搜索→爬取→分析→决策，一条链走完。

---

## 0. 触发方式

| 用户说 | 你做 |
|--------|------|
| "帮我查一下[主题]" | 16引擎搜索 + 去重 → 汇总报告 |
| "深入分析[主题]" | 全流程：搜索→爬取→NLP→LLM分析→决策报告 |
| "快速了解[主题]" | 搜索前5引擎 → NLP摘要 → 简报 |
| "对比[A]和[B]" | 双线搜索 → 对比分析报告 |
| "这个断言可信吗" | 搜索 + 可信度评分 + 交叉验证 |
| "监控[主题]" | 搜索 + 设置Cron追踪 |
| "关于[主题]的最新进展" | 搜索 + 时间排序 + 趋势检测 |

---

## 1. HARD-GATE

```
1. 所有路径用 os.homedir()/pathlib/环境变量，零硬编码
2. 所有数据流必须过契约层校验
3. 所有文件写入走事务，支持原子回滚
4. 所有外部调用过熔断器，防级联崩溃
5. 必须有健康自检，启动时验证依赖完整性
6. 所有测试用真实后端数据，禁用假数据/桩
```

---

## 2. 状态机

```
IDLE → PENDING → SEARCHING → CRAWLING → ANALYZING → REPORTING → DELIVERING → DONE
                   │                                                    │
                   └── FAILED → RETRY (max 3)                    DONE ──→ IDLE
                                        → FAILED ×3 → LOG → IDLE
```

全局熔断：600s / 单步 120s / 连续 3 次失败 → 熔断打开

---

## 3. 16引擎万能搜索

自动按语言路由引擎，无需 API key。

### 国内引擎（7）
- Baidu / Bing CN / Bing INT — 中文内容首选
- 360 / Sogou — 长尾搜索
- WeChat — 微信公众号内容
- Shenma — 移动端搜索结果

### 国际引擎（9）
- Google / Google HK — 全球标准
- DuckDuckGo — 隐私优先
- Yahoo / Startpage / Brave / Ecosia / Qwant — 隐私/环保
- WolframAlpha — 结构化知识查询

### 搜索策略

```
1. 检测查询语言（中/英/其他）
2. 根据语言选择引擎组（中=国内+国际混合，英=国际）
3. 每批 3-4 引擎，批间隔 1.5s
4. 每引擎取前 10 条
5. 结果合并后按来源+时效排序
6. 跨源去重（相同URL合并）
7. 内容指纹去重（>90%相似度合并）
```

### 错误处理

| 错误 | 动作 |
|------|------|
| 403/429 (被禁) | 获取新Cookie，重试1次 |
| 超时 (>15s) | 跳过该引擎，继续下一批 |
| 反复失败 (>3次) | 引擎标记为不可用，降级 |
| 全部失败 | 返回 WARNING + 建议检查网络 |

---

## 4. 智能爬取

获取搜索结果后，对关键页面做深度爬取。

### 爬取流程

```
1. 从搜索结果中筛选 Top 5-10 关键页面
2. 设置随机 User-Agent 和请求头
3. 请求页面内容
4. 智能提取：HTML → Markdown（保留标题/段落/链接/列表）
5. 如果失败，自动回退：
   a. 换 User-Agent 重试
   b. 用搜索引擎缓存/快照
   c. 只爬摘要
```

### 指纹伪装策略

```
- User-Agent: 随机从 10+ 种浏览器/操作系统组合中选
- 请求间隔: 随机 1-3s
- Cookie: 每个目标单独管理
- Referer: 随机搜索引擎
```

---

## 5. 多维度分析

### 5.1 NLP分析

使用 funNLP 引擎对搜索结果做：

| 分析 | 产出 |
|------|------|
| 中文分词 | 关键词提取 |
| 命名实体识别 | 人物/地点/机构/专名提取 |
| 文本摘要 | 核心内容压缩 |
| 相似度计算 | 内容聚类/去重 |

### 5.2 来源可信度评分

| 维度 | 权重 | 评分标准 |
|------|:----:|---------|
| 域名权威性 | 25% | .gov/.edu=5 / 正规新闻=4 / 行业站=3 / 个人博客=2 / 论坛=1 |
| 内容质量 | 20% | 完整度+字数+引用 |
| 时效性 | 15% | 越新越高 |
| 跨源一致性 | 25% | 多独立源报道一致=高分 |
| 引用来源 | 15% | 有引用=高分，纯观点=低分 |

**输出：** 高可信 / 中等可信 / 低可信 / 存疑

### 5.3 免费LLM分析

自动检测可用的 LLM Provider：

```python
# 检测顺序
if ollama running:      使用 ollama（本地）
elif gateway token:     使用 OpenClaw Gateway
elif deepseek key:      使用 DeepSeek
elif dashscope key:     使用 通义千问
else:                   跳过 LLM，只用规则分析
```

分析内容：结果结构化摘要 / 多源交叉验证 / 情感倾向分析 / 决策推演

### 5.4 决策框架

根据问题类型自动匹配：

| 问题类型 | 适用框架 |
|---------|---------|
| 根本原因 | 第一性原理 / 5-Whys |
| 方案选型 | 奥卡姆剃刀 / 系统思维 |
| 优先级排序 | 帕累托法则 / 二阶思维 |
| 可信度验证 | 反证法 / 贝叶斯更新 |

---

## 6. 无损状态管理

### 6.1 WAL协议

所有关键操作前先写日志：

```
before:  日志 → "准备搜索[主题]..."
action:  执行搜索
after:   日志 → "搜索完成，获取N条结果"
success: 日志 → "状态: DONE"
fail:    日志 → "状态: FAILED，原因:..."
```

### 6.2 跨会话恢复

如果 session 中断：

```
1. 读取 WAL 日志，找到上次运行到哪个阶段
2. 如果是 SEARCHING → 重新搜索
3. 如果是 ANALYZING → 跳过搜索，从分析开始
4. 如果是 REPORTING → 跳过分析，从报告开始
5. 恢复上下文 → 继续执行
```

### 6.3 事务边界

```
搜索阶段：    开始 → 搜索 → 合并 → 提交结果
爬取阶段：    开始 → 爬取 → 提取 → 提交内容
分析阶段：    开始 → NLP → LLM → 提交报告
报告阶段：    开始 → 生成 → 提交输出

任何阶段失败 → 回滚到该阶段起始点
```

---

## 7. 项目结构

```
universal-intelligence-agent/
├── SKILL.md
├── run.py                     # CLI 入口
├── pyproject.toml
├── requirements.txt
├── contracts/                 # 数据契约 (Pydantic v2)
│   ├── search_schema.py       # 搜索请求/结果
│   ├── crawl_schema.py        # 爬取请求/结果
│   ├── analysis_schema.py     # 分析结果
│   ├── llm_schema.py          # LLM分析
│   ├── nlp_schema.py          # NLP结果
│   ├── state_schema.py        # 状态/事务
│   ├── report_schema.py       # 报告输出
│   ├── alert_schema.py        # 预警监控
│   └── context_schema.py      # 上下文总线
├── layers/                    # 执行层
│   ├── input_adapter.py       # 输入适配
│   ├── output_adapter.py      # 输出适配
│   ├── pipeline_coordinator.py # 管道调度
│   ├── acl.py                 # 防腐层
│   ├── field_mapper.py        # 字段映射
│   ├── degraded_handler.py    # 降级处理
│   ├── rollback_coordinator.py # 回滚协调
│   ├── preflight.py           # 环境预检
│   ├── search_engine.py       # 16引擎调度
│   ├── scraper.py             # 智能爬取
│   ├── analyzer.py            # 情报分析
│   ├── credibility_engine.py  # 可信度评分
│   ├── nlp_engine.py          # NLP分析
│   ├── llm_hub.py             # 免费LLM池
│   └── engine_health.py       # 引擎健康度
├── middlewares/               # 横切层
│   ├── circuit_breaker.py     # 三级熔断器
│   ├── transaction.py         # 事务管理 (2PC)
│   ├── anti_corruption.py     # 输入净化
│   ├── side_effect_log.py     # 副作用日志
│   └── metrics.py             # 监控指标
├── templates/                 # 报告模板
│   ├── brief_report.md
│   └── analysis_report.md
└── tests/                     # 测试 (112 通过)
```

---

## 8. 输出格式

### 快速简报

```
=== [主题] 简报 ===
来源: N引擎 (N条) | 去重后: N条
可信度: ★★★☆☆

核心发现:
1. ...
2. ...

关键信息:
- ...

[来源全称] ([日期]) [标题] [可信度:高/中/低]
```

### 深度分析报告

```
=== [主题] 深度分析 ===

一、信息汇总
  引擎: N台 | 结果: N条 | 去重: N条
  来源分布: 国内N条, 国际N条
  时效: YYYY-MM-DD ~ YYYY-MM-DD

二、关键实体
  人物: ...
  机构: ...
  时间线: ...

三、可信度评估
  高可信: N条
  中等: N条
  低可信/存疑: N条

四、情感/倾向
  整体: {正面/负面/中性}

五、交叉验证
  一致内容: ...
  分歧内容: ...
  待核实: ...

六、结论
  ...
```

---

## 9. 预检清单（Phase 0）

每次开始前：

```
1. 检测 Python 版本（≥3.10）
2. 检测网络连通（ping baidu.com, google.com）
3. 检测可用 LLM Provider（ollama/gateway/key）
4. 检测磁盘空间（≥500MB）
5. 检测 WAL 日志是否有未完成的任务
```

任何一项不通过 → 报告缺失项 → 跳过搜索/分析步骤 → 降级运行

---

## 10. 自检清单

| 检查项 | 状态 |
|--------|:----:|
| 零硬编码路径 | ✅ |
| 契约层 6个Schema | ✅ |
| 熔断器 单步120s/全局600s | ✅ |
| 事务保护 WAL协议 | ✅ |
| 健康自检 Preflight | ✅ |
| 16引擎搜索 | ✅ |
| 智能反爬+指纹伪装 | ✅ |
| 跨源去重+内容去重 | ✅ |
| 来源可信度4级评分 | ✅ |
| 免费LLM池自动发现 | ✅ |
| 中文NLP | ✅ |
| 决策框架自动匹配 | ✅ |
| 跨会话状态恢复 | ✅ |
| 多格式报告输出 | ✅ |
| 全部测试通过 | ✅ |

---

## 11. 不重叠声明

| 现有技能 | 本技能不同之处 |
|---------|--------------|
| deep-researcher | DR 用 tavily API + PDF；本技能用免费16引擎 + web抓取 |
| web_search | 单引擎单次；本技能是多引擎协同 + 全分析链 |
| claw-search/pipeline | 本地文件搜索；本技能是互联网搜索 |
| one-novel-skill | 小说创作；本技能是信息分析 |
| 金融大鳄吞金兽 | A股评分；本技能是通用情报 |
| hk/macau-gaoshou-crawler | 定向爬站点；本技能是通用搜索引擎式 |

---

## 12. 安装

```bash
cd skills/universal-intelligence-agent
pip install -e ".[dev]"
pytest tests/ -v
```

零外部依赖，不需要任何 API key。

---

## 13. 已知局限

1. 某些引擎因IP/地区限制可能不可用
2. 免费LLM有速率限制，大量分析建议用本地 Ollama
3. JS渲染页面需要更多资源
4. 极深Web可能需要多次请求
