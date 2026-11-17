# 示例：auto 从 quick 升级到 deep

## 输入

用户要求快速检查 `skills/万能助手/`。目录有 `SKILL.md`，但目录名与 slug 不同；frontmatter 版本低于 `_meta.json`；正文要求 `API_TOKEN`，却未声明环境变量；示例出现真实格式的 token。

## quick 发现

- frontmatter 可解析，但身份和版本信号冲突
- 页面摘要是“帮助所有开发者提高效率”，缺少具体场景
- 示例疑似包含敏感值

这些问题同时涉及 P0、安全与证据冲突，quick 不足以可靠结论。

## 自动升级

- 请求模式：auto
- 初选：quick
- 实际模式：deep
- 升级原因：版本冲突与疑似凭据

## deep 结论

- 结论：先别发
- P0：删除并轮换示例凭据；统一目录、稳定 slug 和版本来源
- P1：声明实际环境变量；把目标用户与结果写具体
- 未验证：dry-run、registry moderation、隔离安装

## 最小修复路径

先处理凭据，再统一身份与版本，补环境声明，最后执行显式 slug/name 的 dry-run。不要通过重试掩盖确定性配置错误。
