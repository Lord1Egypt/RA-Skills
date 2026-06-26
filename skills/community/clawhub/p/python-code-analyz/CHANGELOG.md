# Changelog

所有版本更新记录。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-03-21

### 🎉 初始版本

**安全扫描 (P0):**
- ✅ **hardcoded_secrets** - 检测 API_KEY/SECRET/PASSWORD/TOKEN 硬编码
- ✅ **bare_except** - 检测裸 `except:` 语句
- ✅ **sql_injection** - 检测 SQL 注入风险（字符串拼接/format/f-string）
- ✅ **command_injection** - 检测命令注入（os.system/subprocess）
- ✅ **dangerous_functions** - 检测危险函数（eval/exec/pickle/yaml.load/marshal）

**可靠性检查 (P1):**
- ✅ **missing_timeout** - 检测 HTTP 请求缺少 timeout
- ✅ **resource_leaks** - 检测锁 acquire 没有 release
- ✅ **unclosed_files** - 检测文件打开后未关闭
- ✅ **debug_code** - 检测 pdb 调试代码

**代码质量 (P2):**
- ✅ **missing_type_hints** - 检测函数缺少类型提示
- ✅ **long_functions** - 检测函数超过 50 行
- ✅ **unused_variables** - 检测未使用的变量
- ✅ **inline_imports** - 检测函数内导入
- ✅ **debug_code** - 检测 print 调试语句
- ✅ **hardcoded_urls** - 检测硬编码 URL/IP

**功能特性:**
- 📊 分级报告 - P0/P1/P2/P3 四级问题分级
- 💾 数据缓存 - 55秒 TTL 减少 API 调用
- 🔒 原子写入 - 信号文件安全写入
- 🎯 信号优先级 - 高风险信号优先处理
- 📈 统计信息 - 函数/类/导入数量统计
- 💡 修复建议 - 每个问题都附带具体建议

### 支持的输出格式

- 文本格式（人类可读）
- JSON 格式（机器解析）

---

## 计划功能

### [1.1.0] - 开发中

- [ ] 支持配置文件 `.code_analyzer.yaml`
- [ ] 复杂度分析（圈复杂度、认知复杂度）
- [ ] 重复代码检测
- [ ] 集成 Black 代码格式化建议
- [ ] 支持异步代码分析

### [1.2.0] - 计划中

- [ ] 增量分析（只检查变更文件）
- [ ] CI/CD 集成
- [ ] GitHub Actions 支持
- [ ] VSCode 插件

### [2.0.0] - 远期

- [ ] 支持多语言（JavaScript、Go、Rust）
- [ ] AI 辅助修复建议
- [ ] 自定义规则 DSL
- [ ] 团队协作功能
