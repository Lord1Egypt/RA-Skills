# 参考说明

## 配置设计

`config.yaml` 是这个 Skill 的运维配置总表。

建议在其中维护：

- 连接目标
- 服务说明
- 日志文件路径
- 相关配置文件
- 排查提示
- 默认下载策略

不要放入：

- 明文密码
- 私钥
- 一次性事故说明这类应写入单独报告的信息

## 字段说明

### `analysis`

- `local_temp_dir`：下载日志片段的本地目录
- `default_time_window`：用户未提供时间范围时的默认时间窗口
- `default_tail_lines`：默认抓取的最近日志行数
- `max_download_mb_per_file`：单文件下载大小的软限制
- `prefer_remote_filter`：是否优先在远端先过滤再下载
- `preserve_downloads`：分析完成后是否保留本地文件

### `connections`

每个连接项代表一个 SSH 目标或访问入口。

推荐字段：

- `host`
- `port`
- `username`
- `auth.method`
- `auth.password_env` or key reference
- `notes`

如果需要跳板机，可扩展如下字段：

- `jump_host`
- `jump_port`
- `jump_username`

### `services`

每个服务都应尽量写到无需额外口口相传信息也能理解。

推荐字段：

- `description`
- `aliases`
- `keywords`
- `connection`
- `workdir`
- `startup_command`
- `investigation_hints`
- `log_files`
- `related_files`
- `related_services`

### `log_files`

每个日志项不仅要写路径，还要写明用途。

推荐字段：

- `name`
- `path`
- `format`
- `priority`
- `purpose`

## 推荐远程排查流程

1. 将问题匹配到 `config.yaml` 中的服务
2. 确认连接目标
3. 检查文件是否存在、文件大小是否合理
4. 先在远端查看最近 tail 或关键词匹配结果
5. 下载最小必要日志片段
6. 在本地进行分析
7. 证据不足时再扩大范围

## 推荐下载策略

按以下顺序逐步扩大范围：

1. 先取最高优先级日志的最近若干行
2. 再抽取问题关键词附近片段
3. 再拉取指定时间窗口日志
4. 如果问题更早开始，补充滚动日志
5. 只有必要时才下载完整文件

## 服务说明示例

`提供用户登录、令牌刷新和会话校验能力。常见问题包括 Redis 会话失败、下游认证超时和启动配置错误。`

## 排查提示示例

- `登录失败时，联动检查 gateway 与 auth-service 日志。`
- `如果部署后启动失败，检查 application-prod.yml 和 systemd 环境变量。`
- `如果响应时间突然升高，将应用超时日志与数据库连接耗尽进行关联分析。`

## Output Template

Use a concise structure:

```markdown
## 问题摘要
[一句话描述]

## 关键证据
- [日志证据 1]
- [日志证据 2]

## 初步判断
[最可能原因]

## 置信度
[高/中/低]

## 建议下一步
- [建议 1]
- [建议 2]
```

## 备注

- 服务名、别名和对外描述尽量保持术语一致
- 回复中优先使用统一的服务标准名称
- 当日志路径或部署拓扑发生变化时，要及时更新 `config.yaml`
