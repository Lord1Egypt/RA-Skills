# 服务器安装（仅首次需要）

本 Skill 的运行依赖一个**独立的第三方本地组件** [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)。本 Skill 自身**不包含、不分发、不打包**该组件的任何二进制或源代码，也**不会自动下载**它。是否安装、安装哪个版本、授予哪种账号权限，**完全由用户本人在安装本 Skill 之前独立决定**。

## 安装前检查清单（Preflight Checklist）

在继续之前，请逐项勾选以下条件。**如有任何一项无法满足，请停止安装本 Skill**：

- [ ] 我已独立审核并信任第三方组件 `xpzouying/xiaohongshu-mcp`。
- [ ] 我会使用一个**独立注册的专用账号**，不会使用我的主账号或企业账号。
- [ ] 我会将该组件仅运行在受我本人物理控制的个人电脑上。
- [ ] 我会使用该组件的默认 loopback 配置，不会修改其网络绑定。
- [ ] 我理解并接受：该组件运行期间可代表上述专用账号发布公开内容，误操作不可撤回。
- [ ] 任务完成后，我会停止该组件进程，并在官方 App 中手动吊销对应的登录设备。

> ℹ️ 本 Skill 随附的 Python 客户端 `scripts/xhs_client.py` 在客户端一侧已内置多道自动拒绝机制：
> 非 loopback 端点、非交互环境下的发布、未声明专用账号的发布，都会被**直接拒绝执行**，
> 详见 `xhs_client.py` 顶部注释。

## 第 0 步：安装 Python 依赖

```bash
pip install requests
```

## 第 1 步：获取第三方 MCP 组件（推荐从源码编译）

为避免供应链风险，**推荐**直接从官方仓库克隆并锁定到一个你已审核的具体版本 tag，然后用 Go 工具链自行编译：

```bash
git clone https://github.com/xpzouying/xiaohongshu-mcp.git
cd xiaohongshu-mcp
git checkout <YOUR_REVIEWED_TAG>     # 必须是一个你已人工审核过的具体 tag，禁止使用 main/latest
go build -o xiaohongshu-mcp ./cmd/mcp
go build -o xiaohongshu-login ./cmd/login
```

如必须使用预编译产物，请从 [官方 Releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) 下载指定 tag 的文件，并核对其 SHA256 与你从源码独立计算的哈希一致后再使用。

完成后，将你确认使用的版本号写入环境变量，供本 Skill 的客户端进行一致性提示：

```bash
export XHS_UPSTREAM_PINNED_VERSION="<YOUR_REVIEWED_TAG>"
```

## 第 2 步：登录

完成登录后，客户端会声明你正在使用的是**专用账号**；本 Skill 的 `publish` 命令要求用户显式设置该声明后才会放行：

```bash
export XHS_DEDICATED_ACCOUNT=yes     # 只有在你用的是独立的专用账号时才设置
./xiaohongshu-login-<your-platform>  # 扫码登录
```

## 第 3 步：启动 MCP 组件（保持默认 loopback 绑定）

按照第三方组件文档的**默认**方式启动即可（其默认就绑定在本机回环接口）。本 Skill 的客户端会验证端点必须是 loopback，否则**直接拒绝发起任何请求**。

```bash
./xiaohongshu-mcp-<your-platform>
```

## 第 4 步：验证

```bash
python scripts/xhs_client.py status
```

## 使用结束后

```bash
pkill -f xiaohongshu-mcp
unset XHS_DEDICATED_ACCOUNT XHS_UPSTREAM_PINNED_VERSION
```

并在小红书官方 App 的「登录设备管理」中主动下线对应设备。
