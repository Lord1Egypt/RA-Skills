# PT Agent

用自然语言搜索私有 PT 资源、查看账户与下载器状态，并把选中的资源直接交给下载器。

你只需要告诉 Agent 想做什么：

```text
帮我搜索星际穿越，优先免费
只看 4K 的电视剧资源
看看我的 PT 数据
查看下载器里暂停的任务
下载第 1 个
```

PT Agent 会调用你已经配置的 PT 站点和下载器完成操作，不需要你记命令或手动复制下载链接。

> 仅用于你有权访问的站点、账户与下载器。请遵守站点规则、当地法律和内容版权要求。

## 能做什么

- **搜索资源**：按电影、剧集、站点、Free 状态、分辨率与做种数筛选或排序
- **管理下载**：把搜索结果交给默认下载器，查看下载中、暂停或已完成的任务
- **查看账户**：汇总上传量、下载量、分享率、魔力值与站点连接状态
- **连接常见服务**：支持 NexusPHP、Torznab、Prowlarr、Jackett、RSS、Unit3D API、Gazelle JSON 与 qBittorrent
- **保护凭据**：只保存凭据引用，不在配置、日志或对话结果中暴露敏感信息

## 安装

### Codex

```bash
git clone https://github.com/xzulab/pt-agent.git ~/.codex/skills/pt-agent
```

重启 Codex，让它加载新 skill。

### OpenClaw

```bash
git clone https://github.com/xzulab/pt-agent.git ~/.openclaw/skills/pt-agent
```

重启 OpenClaw 或重新加载 skills。

### 运行要求

- Python 3.10 或更高版本
- 支持 `SKILL.md` 的 Agent 宿主
- 你有权使用的 PT 站点账户
- 可选：qBittorrent 或其他受支持的下载器

本地运行脚本只使用 Python 标准库，不需要额外安装 Python 包。

## 首次配置

安装完成后，直接对 Agent 说：

```text
配置 PT 站点
```

Agent 会引导你完成：

1. 选择站点或接入方式
2. 填写站点地址
3. 关联浏览器登录状态或安全凭据引用
4. 验证连接并保存配置
5. 可选配置默认下载器

也可以随时说：

```text
检查 PT 配置
我有哪些 PT 配置
查看下载器状态
```

## 使用示例

### 搜索与筛选

```text
搜索盗梦空间
搜索最后生还者，只看 4K
搜索周星驰的电影，优先免费
在 HDFans 搜索沙丘，按做种数排序
```

“优先免费”会把 Free 资源排在前面，同时保留其他匹配结果；“只看免费”只返回 Free 资源。

### 下载资源

搜索结果会以编号展示。继续回复即可下载：

```text
下载第 1 个
```

PT Agent 会使用已配置的默认下载器；如果尚未配置，会引导你补充必要信息。

### 账户与下载器

```text
看看我的 PT 数据
查看 HDFans 的账户状态
查看下载中的任务
有哪些暂停任务
```

## 凭据安全

不要在聊天、配置文件、Issue 或日志中粘贴 Cookie、passkey、密码、API Token 或私有下载链接。

PT Agent 使用安全引用来定位凭据：

```text
env://PT_SITE_COOKIE
secret://trackers/main
profile://trackers/main
proxy://trackers/main
```

- `env://` 可由本地运行时直接解析
- `secret://`、`profile://` 和 `proxy://` 需要宿主提供对应能力
- 如果敏感凭据曾在公开或共享环境中暴露，请立即轮换

## 支持范围

PT Agent 提供通用接入能力，但具体站点能否使用取决于站点类型、认证方式和页面/API 兼容性。遇到不支持的站点时，Agent 会说明缺少的接入信息，不会猜测接口或尝试未知凭据。

当前重点支持：

- NexusPHP 及站点预设
- Prowlarr、Jackett 与 Torznab
- RSS、Unit3D API 与 Gazelle JSON
- qBittorrent 状态、任务查询与下载交接

### 站点规则与参考来源

站点预设、通用 Schema 和部分解析规则参考了开源项目 [PT-depiler](https://github.com/pt-plugins/PT-depiler)。PT-depiler 是成熟的 PT 浏览器扩展，提供多站点聚合搜索、用户信息管理和下载器集成等能力。

PT Agent 主要借鉴其公开的规则组织方式：

- 用站点定义记录名称、别名、类型与能力，而不是运行时猜测接口
- 让站点复用 NexusPHP、Unit3D、Gazelle 等通用 Schema，并只覆盖差异字段
- 按站点声明解析标题、大小、做种数、优惠状态、发布时间与下载入口
- 将站点配置、认证信息、搜索结果和下载器配置分开处理

PT Agent 是独立的 Agent skill，不是 PT-depiler 的浏览器扩展版本，也不代表 PT-depiler 官方。预设中出现某个站点，只表示可以识别其规则元数据；能否实际搜索、读取账户信息或下载，仍取决于当前宿主是否实现对应适配器，以及用户是否提供兼容的认证方式。

感谢 PT-depiler 与 PT-Plugin-Plus 社区长期维护的公开站点适配经验。本项目只保留运行所需的最小规则元数据，不包含其用户数据、Cookie、passkey、私有下载链接或其他敏感内容。PT-depiler 同样采用 MIT License，详细许可与贡献者信息请以其仓库为准。

## 常见问题

### 为什么搜索不到资源？

先尝试简化关键词、指定站点或取消筛选条件。PT Agent 不会在后台擅自更换关键词、站点或过滤条件。

### 为什么不能直接粘贴 Cookie 或 Token？

私有站点凭据通常等同于账户访问权限。使用环境变量、Secret Provider 或隔离浏览器 Profile，可以避免凭据进入聊天记录和仓库。

### 一定要配置下载器吗？

不需要。资源搜索和账户查询可以独立使用；只有直接下载与任务管理需要下载器。

## 开发

修改 skill 后运行：

```bash
python3 scripts/validate_skill.py
python3 scripts/benchmark_common.py
```

贡献站点适配器时，请只使用脱敏 fixture，不要提交真实站点凭据、私有下载链接、torrent hash 或可识别个人活动的数据。

## License

[MIT](LICENSE) © 2026 xzulab
