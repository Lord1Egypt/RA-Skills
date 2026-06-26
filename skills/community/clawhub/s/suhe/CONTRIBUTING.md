# 贡献指南

感谢您对 Suhe 中国女友的项目的关注！我们欢迎各种形式的贡献，包括但不限于修复错误、改进文档、添加新功能或提出建议。

## 项目概述

Suhe 中国女友是一个为 OpenClaw 智能代理添加自拍能力的技能插件，通过集成阿里云通义万相实现 AI 图像生成，使虚拟角色具备视觉表达能力。

## 开发环境设置

1. 确保您的系统满足以下要求：
   - Node.js >= 18.0.0
   - npm 或 pnpm
   - OpenClaw 运行时环境

2. 克隆项目仓库：
   ```bash
   git clone https://github.com/lilozhao/Suhe.git
   git clone https://gitee.com/lilozhao/Suhe.git
   cd Suhe
   ```

3. 安装依赖：
   ```bash
   npm install
   ```

## 代码规范

- 使用 TypeScript 编写代码
- 遵循 ESLint 和 Prettier 的格式化规则
- 为新功能编写单元测试
- 更新相关文档

## 提交 Pull Request

1. Fork 仓库
2. 创建新分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

## 安全注意事项

**重要**: 请勿在代码中提交任何敏感信息，如 API 密钥、密码或其他认证凭据。所有敏感配置应通过环境变量提供。

## 问题报告

如果发现 bug 或有改进建议，请提交 Issue。请确保在报告中包含：

- 详细描述问题
- 复现步骤
- 您的环境信息
- 预期行为

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](./LICENSE) 文件。