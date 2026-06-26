# 编程任务分类

详细的编程任务分类体系，用于智能模型路由。

---

## 一级分类

### 1. 代码生成 (Code Generation)

**定义：** 根据需求描述创建新的代码

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 算法实现 | 实现特定算法 | "写一个快速排序" | qwen-coder-plus |
| 业务逻辑 | 实现业务功能 | "创建用户注册接口" | qwen-coder-plus |
| 组件开发 | 开发 UI 组件 | "生成一个表格组件" | qwen-coder-plus |
| 工具函数 | 编写工具类函数 | "写一个日期格式化函数" | qwen-turbo |
| API 开发 | 开发 RESTful API | "创建用户 CRUD 接口" | qwen-coder-plus |
| 脚本编写 | 编写自动化脚本 | "写一个批量处理图片的脚本" | qwen-plus |

**触发关键词：**
```
写一个、实现、创建、生成、开发、编写、make、create、
implement、generate、build、develop、code、function、class
```

---

### 2. 代码审查 (Code Review)

**定义：** 评估现有代码的质量和潜在问题

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 质量评估 | 整体代码质量 | "这段代码质量如何" | claude-sonnet |
| 安全检查 | 安全漏洞扫描 | "有什么安全隐患" | claude-sonnet |
| 规范检查 | 编码规范遵循 | "符合 PEP8 吗" | qwen-max |
| 性能审查 | 性能问题分析 | "有性能瓶颈吗" | qwen-max |
| 最佳实践 | 最佳实践建议 | "有什么改进建议" | claude-sonnet |
| 技术债务 | 技术债务识别 | "有哪些技术债务" | qwen-max |

**触发关键词：**
```
审查、检查、review、audit、quality、问题、隐患、改进、
代码质量、code review、best practice、smell
```

---

### 3. Bug 调试 (Bug Debugging)

**定义：** 定位和修复代码中的错误

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 错误定位 | 找出错误位置 | "为什么报错" | glm-4 |
| 原因分析 | 分析错误原因 | "这个 bug 怎么产生的" | glm-4 |
| 修复建议 | 提供修复方案 | "怎么修复这个问题" | qwen-plus |
| 日志分析 | 分析日志定位问题 | "从日志看问题在哪" | glm-4 |
| 并发问题 | 调试并发相关 bug | "死锁怎么解决" | glm-4 |
| 内存问题 | 内存泄漏调试 | "内存泄漏在哪" | qwen-plus |

**触发关键词：**
```
bug、错误、修复、调试、debug、fix、为什么报错、
exception、error、locate、issue、problem
```

---

### 4. 性能优化 (Performance Optimization)

**定义：** 提升代码的执行效率和资源利用率

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 算法优化 | 优化算法复杂度 | "如何优化这个排序" | qwen-coder-plus |
| 内存优化 | 减少内存占用 | "降低内存使用" | qwen-coder-plus |
| 并发优化 | 提升并发性能 | "提高并发处理能力" | qwen-max |
| 数据库优化 | SQL 和索引优化 | "优化这个查询" | qwen-plus |
| 缓存策略 | 设计缓存方案 | "添加缓存提升性能" | qwen-max |
| 资源优化 | CPU/IO 优化 | "减少 CPU 占用" | qwen-coder-plus |

**触发关键词：**
```
优化、性能、optimize、performance、加速、效率、
bottleneck、slow、fast、memory、cpu
```

---

### 5. 重构 (Refactoring)

**定义：** 改进代码结构而不改变外部行为

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 代码清理 | 清理冗余代码 | "清理这段代码" | claude-sonnet |
| 结构优化 | 改进代码结构 | "重构这个模块" | claude-sonnet |
| 设计模式 | 应用设计模式 | "用工厂模式重构" | qwen-max |
| 模块化 | 拆分大模块 | "拆分成小模块" | claude-sonnet |
| 命名优化 | 改进命名 | "改进变量命名" | qwen-turbo |
| 接口设计 | 优化接口设计 | "重新设计这个 API" | qwen-max |

**触发关键词：**
```
重构、refactor、restructuring、改进结构、清理代码、
clean code、architecture、design pattern、模块化
```

---

### 6. 单元测试 (Unit Testing)

**定义：** 生成和执行单元测试

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 测试生成 | 生成测试代码 | "写单元测试" | deepseek-coder |
| 用例设计 | 设计测试用例 | "设计测试场景" | deepseek-coder |
| 边界测试 | 边界条件测试 | "测试边界情况" | deepseek-coder |
| Mock 测试 | Mock 外部依赖 | "mock 这个 API" | deepseek-coder |
| 覆盖率 | 提升测试覆盖率 | "提高覆盖率" | qwen-plus |
| 测试调试 | 调试测试失败 | "测试为什么失败" | qwen-plus |

**触发关键词：**
```
测试、test、unit test、单元测试、测试用例、coverage、
pytest、jest、mock、assertion
```

---

### 7. 技术问答 (Technical Q&A)

**定义：** 回答技术相关问题

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 概念解释 | 解释技术概念 | "什么是闭包" | qwen-plus |
| 原理分析 | 分析技术原理 | "React 虚拟 DOM 原理" | glm-4 |
| 方案对比 | 对比技术方案 | "Vue vs React" | qwen-max |
| 最佳实践 | 询问最佳实践 | "Python 最佳实践" | qwen-plus |
| 工具使用 | 工具使用方法 | "git rebase 怎么用" | qwen-turbo |
| 版本差异 | 版本间差异 | "Python2 和 3 的区别" | qwen-plus |

**触发关键词：**
```
怎么、如何、how to、what is、为什么、explain、
concept、principle、技术、question
```

---

### 8. 文档生成 (Documentation)

**定义：** 生成代码相关的文档

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 注释编写 | 添加代码注释 | "给这个函数加注释" | qwen-turbo |
| API 文档 | 生成 API 文档 | "写 API 文档" | qwen-turbo |
| README | 编写 README | "写个 README" | qwen-turbo |
| 技术文档 | 技术说明文档 | "写技术设计文档" | qwen-plus |
| 变更日志 | 编写 changelog | "写更新日志" | qwen-turbo |
| 使用指南 | 用户使用指南 | "写使用手册" | qwen-plus |

**触发关键词：**
```
文档、document、comment、注释、readme、api doc、
说明、describe、write doc
```

---

### 9. 架构设计 (Architecture Design)

**定义：** 设计系统架构和技术方案

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 系统设计 | 整体系统设计 | "设计一个电商系统" | qwen-max |
| 微服务 | 微服务架构设计 | "微服务怎么拆分" | qwen-max |
| 数据库设计 | 数据库 schema 设计 | "设计数据库表结构" | qwen-max |
| 接口设计 | API 接口设计 | "设计 RESTful API" | claude-sonnet |
| 扩展性 | 可扩展性设计 | "如何支持百万并发" | qwen-max |
| 技术选型 | 技术栈选择 | "用什么技术栈" | qwen-max |

**触发关键词：**
```
架构、architecture、design、系统、system、pattern、
微服务、microservice、scalability、design pattern
```

---

### 10. 代码解释 (Code Explanation)

**定义：** 解释代码的含义和逻辑

**子分类：**

| 子类型 | 描述 | 示例 | 推荐模型 |
|--------|------|------|---------|
| 功能解释 | 解释代码功能 | "这段代码做什么" | qwen-plus |
| 逻辑分析 | 分析执行逻辑 | "这个函数怎么执行" | qwen-plus |
| 复杂代码 | 解释复杂代码 | "解释这个算法" | glm-4 |
| 正则解释 | 解释正则表达式 | "这个正则什么意思" | qwen-turbo |
| 错误信息 | 解释错误信息 | "这个报错什么意思" | qwen-plus |
| 依赖分析 | 分析依赖关系 | "这个模块依赖什么" | qwen-plus |

**触发关键词：**
```
解释、explain、理解、understand、什么意思、what does、
这段代码、this code、analyze
```

---

## 复合任务识别

实际场景中，用户请求可能包含多个任务类型：

### 示例 1：生成 + 测试
```
"写一个排序函数，并加上单元测试"
→ 任务类型：CODE_GENERATION + UNIT_TEST
→ 协作模式：qwen-coder-plus → deepseek-coder
```

### 示例 2：审查 + 重构
```
"审查这段代码并重构"
→ 任务类型：CODE_REVIEW + REFACTORING
→ 协作模式：claude-sonnet → qwen-coder-plus
```

### 示例 3：调试 + 优化
```
"修复这个 bug 并优化性能"
→ 任务类型：BUG_DEBUG + PERFORMANCE_OPT
→ 协作模式：glm-4 → qwen-coder-plus
```

---

## 任务复杂度评估

| 复杂度 | 特征 | 推荐模式 | 预算范围 |
|--------|------|---------|---------|
| 简单 | 单一功能，代码量少 | 单模型 (turbo/plus) | ¥0.01-0.05 |
| 中等 | 多模块，需要设计 | 单模型 (coder/max) | ¥0.05-0.20 |
| 复杂 | 系统级，多约束 | 多模型协作 | ¥0.20-1.00 |
| 极复杂 | 架构级，高风险 | 多模型 + 人工审核 | ¥1.00+ |

---

## 任务描述优化建议

### ❌ 模糊描述
```
"帮我写个代码"
"这个有问题，修一下"
"优化一下"
```

### ✅ 清晰描述
```
"用 Python 写一个线程安全的 LRU 缓存，支持 get/put 操作，时间复杂度 O(1)"
"这个函数在并发时会返回空值，帮我定位原因并修复"
"优化这个排序算法，当前处理 10 万条数据需要 5 秒，目标是 1 秒内"
```

### 清晰描述要素：
1. **技术栈**：Python/JS/Java 等
2. **功能需求**：具体要实现什么
3. **约束条件**：性能/安全/兼容性要求
4. **输入输出**：期望的输入和输出格式
5. **上下文**：相关代码或背景信息

---

*最后更新：2026-03-18*
