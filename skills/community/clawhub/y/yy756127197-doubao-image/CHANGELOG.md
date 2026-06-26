# 更新日志 (Changelog)

本项目的所有重要更新都将记录在此文件中。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，并遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

## [2.0.0] - 2026-04-09

### ✨ 新增 (Added)

- **Python 实现版本**
  - 新增 `doubao-image-generate.py` 脚本
  - 使用面向对象设计，提供 `DoubaoImageGenerator` 类
  - 支持 `requests` 库和标准库 `urllib` 双模式
  - 完整的类型注解和文档字符串
  
- **增强的错误处理**
  - 详细的错误分类（ValidationError, APIError, DownloadError）
  - HTTP 状态码精确处理
  - 指数退避重试机制
  - 优雅的错误提示和恢复建议
  
- **完善的日志系统**
  - 分级日志输出（INFO, WARNING, ERROR, DEBUG）
  - 时间戳记录
  - 详细模式（verbose）开关
  - 彩色终端输出（Bash 版本）
  
- **配置选项扩展**
  - 支持更多环境变量配置
  - 自定义超时时间
  - 自定义重试次数
  - 自定义输出目录
  
- **文档完善**
  - 详细的 README.md 使用文档
  - 完整的 API 参考
  - 最佳实践指南
  - 故障排除手册
  - 开发者指南

### 🐛 修复 (Fixed)

- **JSON 转义问题**
  - 使用 Python 替代 shell 处理 JSON，避免转义错误
  - 正确处理中文字符和特殊字符
  
- **重试机制优化**
  - 修复重试延迟计算错误
  - 添加最大重试次数限制
  - 正确处理 429 频率限制
  
- **文件下载验证**
  - 添加文件大小检查（<1KB 视为失败）
  - 下载失败后自动清理临时文件
  - 改进文件名生成算法（使用哈希值）
  
- **环境变量读取**
  - 修复环境变量未设置时的错误提示
  - 添加环境变量检查脚本

### 🔧 改进 (Changed)

- **代码重构**
  - 模块化设计，提高代码复用性
  - 函数和类的职责单一化
  - 改进代码注释和文档
  
- **性能优化**
  - 优化 API 请求构建流程
  - 减少不必要的系统调用
  - 改进文件 I/O 效率
  
- **用户体验**
  - 改进命令行参数解析
  - 更友好的错误提示
  - 添加进度提示
  - 统一输出格式

### 📦 技术栈更新

- Python 3.8+ 支持
- Bash 4.0+ 优化
- 支持 requests 2.25+（可选依赖）
- 跨平台兼容（macOS/Linux）

---

## [1.0.0] - 2026-01-15

### ✨ 新增 (Added)

- **基础功能实现**
  - Bash 脚本实现 (`doubao-image-generate.sh`)
  - 支持基本的文生图功能
  - 简单的参数解析（prompt, size, watermark）
  
- **API 集成**
  - 集成火山引擎 ARK API
  - 支持豆包 SeeDream 模型
  - 基本的错误处理
  
- **文档**
  - 基础 SKILL.md 文档
  - 简单的使用说明

### 📝 说明

这是项目的初始版本，实现了基本的文生图功能。代码相对简单，错误处理不够完善，但为后续版本奠定了基础。

---

## 版本说明

### 语义化版本规范

本项目遵循语义化版本（Semantic Versioning）规范：

- **主版本号（Major）**：不兼容的 API 变更
- **次版本号（Minor）**：向后兼容的功能新增
- **修订号（Patch）**：向后兼容的问题修正

### 版本号格式

```
主版本号。次版本号。修订号
  ↑        ↑        ↑
  2   .    0    .   0
```

### 更新类型说明

- **Added（新增）**：新增功能
- **Changed（变更）**：现有功能的变更
- **Deprecated（弃用）**：即将移除的功能
- **Removed（移除）**：已移除的功能
- **Fixed（修复）**：Bug 修复
- **Security（安全）**：安全性修复

---

## 未来计划

### v2.1.0 (计划中)

- [ ] 支持批量生成
- [ ] 添加图片预览功能
- [ ] 支持 base64 格式输出
- [ ] 添加图片元数据保存
- [ ] 实现智能 prompt 优化

### v2.2.0 (计划中)

- [ ] 支持多种模型选择
- [ ] 添加图片编辑功能
- [ ] 实现图片风格迁移
- [ ] 支持图生图功能

### v3.0.0 (长期计划)

- [ ] 异步并发支持
- [ ] 分布式任务队列
- [ ] WebSocket 实时进度
- [ ] 完整的 GUI 界面

---

## 贡献者

感谢所有为本项目做出贡献的开发者！

- YangYang (作者)
- [你的名字] - 欢迎提交 PR 成为贡献者

---

**相关链接：**

- [GitHub 仓库](https://github.com/your-username/doubao-image-skill)
- [问题反馈](https://github.com/your-username/doubao-image-skill/issues)
- [PR 列表](https://github.com/your-username/doubao-image-skill/pulls)

**最后更新：** 2026-04-09
