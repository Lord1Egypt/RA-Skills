# 贡献指南
首先感谢你有兴趣为 video-merger 做贡献！

## 行为准则
参与本项目请遵守 [Code of Conduct](CODE_OF_CONDUCT.md)。

## 如何贡献
### 报告 Bug
1. 先搜索已有的Issue，确认没有重复报告
2. 创建新Issue，清晰描述Bug现象、复现步骤、你的环境信息
3. 如果可以的话，提供可以复现问题的测试素材

### 提交功能请求
1. 先搜索已有的Issue，确认没有重复的功能请求
2. 创建新Issue，清晰描述你想要的功能、使用场景、期望行为

### 提交代码
1. Fork 本仓库
2. 从 `main` 分支创建你的功能分支：`git checkout -b feature/your-feature-name`
3. 编写代码，确保符合以下规范：
   - Python代码使用 [Black](https://github.com/psf/black) 格式化
   - 遵循 PEP 8 规范
   - 为新功能添加对应的单元测试
   - 更新相关文档
4. 运行测试，确保所有测试通过：`pytest tests/`
5. 提交你的更改：`git commit -m 'feat: add some feature'`，提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 规范
6. 推送到你的分支：`git push origin feature/your-feature-name`
7. 创建 Pull Request

## 提交信息规范
提交信息格式：`<type>(<scope>): <subject>`

### Type 类型
- feat: 新功能
- fix: 修复Bug
- docs: 文档更新
- style: 代码格式调整（不影响代码运行）
- refactor: 代码重构（既不新增功能也不修复Bug）
- perf: 性能优化
- test: 测试相关更改
- chore: 构建/工具链/依赖等非代码更改

### 示例
```
feat: 添加批量处理多个目录的功能
fix: 修复Windows路径处理错误
docs: 更新安装说明
```

## 版本发布
版本号遵循语义化版本规范：
- 主版本号：不兼容的API更改
- 次版本号：新增功能，向后兼容
- 修订号：Bug修复，向后兼容

## 许可证
你提交的代码将默认使用 MIT 许可证授权。
