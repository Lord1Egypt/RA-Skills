# UCloud 文档来源

## 来源顺序

当当前上下文不足以安全执行请求时，按以下顺序使用信息来源：

1. 本地 CLI help 输出，如 `ucloud --help`、`ucloud <product> --help` 或 `ucloud <product> <subcommand> --help`
2. UCloud CLI 文档和 CLI 仓库
3. UCloud 产品文档
4. UCloud API 文档，仅在产品子命令不存在、能力不足或语义不明确时用于 `ucloud api` 兜底调用

## 官方入口

- CLI 快速入门文档：`https://docs.ucloud.cn/cli/intro`
- CLI 仓库：`https://github.com/ucloud/ucloud-cli`
- API 文档：`https://github.com/UCloudDoc-Team/api`
- 产品文档：`https://docs.ucloud.cn/`

## 各来源的验证内容

### CLI 文档和仓库

使用 CLI 文档或仓库验证：

- 安装方法和支持的操作平台
- Profile 在 `~/.ucloud` 下的存储和初始化方式
- 产品子命令是否覆盖当前任务，以及对应 flag、profile 和输出行为
- `ucloud api` 的兜底调用模式和 `--local-file` 行为
- Profile 设置、激活 profile 行为和 profile 选择工作流

### API 文档

仅在需要回退到 `ucloud api` 时，使用 API 文档验证：

- 确切的 Action 名称
- 必填请求参数
- 在构建 `ucloud api` payload 之前，对应 API markdown 文件中记录的接口定义
- 是否需要 `Region`、`Zone` 或 `ProjectId`
- 响应字段名
- Action 特定的约束或枚举值

每次 `ucloud api` 执行前，先确认没有合适的产品子命令可以完成该操作；然后在 `github.com/UCloudDoc-Team/api` 下找到对应的 API markdown 文件，并基于该接口定义构建 payload，而不是仅依赖本地 CLI help。

### 产品文档

使用产品文档验证：

- 产品概念和资源关系
- Region 或可用区行为
- API schema 中不显式体现的操作约束
- 用户使用的产品术语

### 本地 CLI help 输出

使用本地 help 输出验证：

- 是否存在产品专用命令
- 已安装 CLI 暴露了哪些高层子命令和 flag
- 对于当前任务，产品命令是否可以作为首要执行路径

## 操作规则

不要仅凭产品术语去猜测缺失的 CLI flag 或 API 字段。如果当前上下文不足，先查阅产品子命令 help 和官方文档；只有进入 `ucloud api` 兜底路径时才查阅 API 文档，然后仅向用户询问仍然未知的值。
