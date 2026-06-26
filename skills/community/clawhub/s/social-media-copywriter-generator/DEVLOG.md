# 自媒体文案生成器 - 开发日志

## 2026-03-03 Sprint 1 开发记录

### 12:30 - 项目启动
- 创建项目结构
- 确定 Sprint 1 范围（核心功能 MVP）

### 12:35 - 核心生成器完成
- `src/generator.py` - 4 平台 Prompt 模板
- 支持平台：小红书、抖音、公众号、知乎
- 支持语气：自然、专业、幽默、温暖
- 支持长度：short、medium、long

### 12:40 - 标签推荐器完成
- `src/tag_recommender.py` - 标签推荐逻辑
- 3 类标签：热门、精准、长尾
- 平台差异化输出格式

### 12:45 - 命令行接口完成
- `generate.py` - 主入口
- 支持参数：topic, platform, tone, length, keywords, audience, output
- 特殊模式：--titles-only, --no-tags

### 12:50 - 文档完成
- `SKILL.md` - 技能说明
- `README.md` - 使用文档

### 12:55 - 测试通过
```bash
# 标题生成测试 ✅
python generate.py "AI 写作技巧" -p xiaohongshu --titles-only

# 完整生成测试 ✅
python generate.py "AI 工具提升工作效率" -p xiaohongshu -k AI 效率 工具 -o examples/sample.md
```

### 13:00 - 当前状态
**进度**: Sprint 1 70% 完成

**已完成**:
- ✅ 项目结构
- ✅ 核心生成器（4 平台模板）
- ✅ 标签推荐器
- ✅ 命令行接口
- ✅ 文档
- ✅ Mock 测试通过

**待完成**:
- [ ] 接入真实 LLM API（需要 cellcog 或 dashscope）
- [ ] 单元测试（pytest）
- [ ] Few-shot 示例库
- [ ] 输出格式优化（去除 mock 占位内容）

---

### 14:30 - LLM API 集成完成
**进度**: Sprint 1 90% 完成

**新增完成**:
- ✅ 百炼 dashscope API 集成
- ✅ 4 平台 mock 模板优化（备用方案）
- ✅ 错误处理（API 失败自动降级到 mock）

**API 配置**:
- 端点：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- 模型：`qwen3.5-plus`
- API Key: 使用现有百炼 Key

**降级策略**:
1. 优先调用真实 LLM API
2. API 失败时自动切换到 mock 模板
3. 输出警告信息但不中断

**待完成** (5%):
- [ ] Few-shot 示例库（Sprint 2）
- [ ] Sprint 1 发布测试

### 14:45 - 单元测试通过 ✅
**进度**: Sprint 1 95% 完成

**测试结果**:
```
Ran 10 tests in 0.001s
OK
```

**测试覆盖**:
- ✅ 标题生成测试（3 个用例）
- ✅ 标签推荐测试（4 个用例）
- ✅ 文案生成器测试（3 个用例）

**Sprint 1 发布清单**:
- [x] 核心功能完成
- [x] 文档完善
- [x] 单元测试通过
- [ ] 发布到 ClawHub（待老板确认）

### 下一步计划

#### 1. 接入 LLM API（优先级 P0）
方案 A: 使用 cellcog client（需要安装 cellcog）
方案 B: 直接调用 dashscope API（已有百炼 API Key）

推荐方案 B，减少依赖。

#### 2. 优化 Prompt 模板（优先级 P0）
当前问题是 mock 内容太简单，需要：
- 增加 few-shot 示例
- 细化各平台格式要求
- 添加字数控制逻辑

#### 3. 单元测试（优先级 P1）
- 测试生成器基本功能
- 测试标签推荐准确性
- 测试命令行参数解析

#### 4. 示例库（优先级 P2）
收集各平台爆款文案作为 few-shot 示例。

---

## 技术决策

### 为什么用 Python 而不是 Node.js?
- 团队更熟悉 Python
- 无需额外依赖（标准库即可）
- 易于集成 LLM API

### 为什么先做 mock 版本？
- 快速验证架构
- 并行开发（LLM 接入可后续进行）
- 便于测试（不消耗 token）

### Prompt 模板设计
每个平台独立模板，包含：
- system: 平台特点 + 格式要求 + 禁用项
- user: 主题 + 语气 + 长度 + 关键词

---

## 性能目标

| 指标 | 目标 | 当前 |
|:---|:---|:---|
| 单次生成时间 | <5s | ~1s (mock) |
| 标题满意度 | >80% | 待测试 |
| 标签采纳率 | >60% | 待测试 |
| 文案可用率 | >70% | 待测试 |

---

*最后更新：2026-03-03 13:00*
