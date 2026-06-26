---
name: weflow-group-summarizer
description: Use when user asks to monitor WeChat groups, set up WeFlow API access, or when a heartbeat triggers for WeChat group summarization
---

# WeFlow 群聊总结器

设置和运行 WeChat 群聊定期总结。所有脚本和配置都在此技能目录下（`<skill_dir>` 即本 SKILL.md 所在目录）。

**前置条件：**
- [WeFlow 桌面端](https://github.com/hicccc77/WeFlow)已在运行，且 API 服务已启用（设置页面 → API 服务 → 启动服务）
- Python 3 已安装
- 安装依赖：`pip install pyyaml openpyxl`

**目录结构：**
```
scripts/          Python 脚本
weflow-proxy/     Go 反向代理（跨机器访问 WeFlow API 时需要）
reference/        API 文档
weflow-groups.yaml  配置模板（勿直接修改，复制到工作目录使用）
```

## Step a: 检查 WeFlow 连接

```bash
python3 <skill_dir>/scripts/check_weflow.py
```

**如果成功**（输出 host 地址）→ 进入 Step b。

**如果失败**，先排查：
1. WeFlow 是否在运行？
2. API 服务是否已启用？（WeFlow 设置 → API 服务 → 启动服务，默认端口 5031）
3. 如果 WeFlow 在同一台机器：检查端口 `lsof -i :5031`
4. 如果 WeFlow 在其他机器（如 Windows VM）→ 需要部署代理，见下方

### 部署代理（WeFlow 在远程机器时）

1. 确认本机已安装 Go（`go version`）。如未安装：`brew install go`（macOS）
2. 编译 Windows 代理：
   ```bash
   cd <skill_dir>/weflow-proxy && ./build-windows.sh
   ```
3. 告知用户 `weflow-proxy.exe` 的完整路径，请用户复制到 Windows 机器并在命令行（cmd/PowerShell）中运行。**注意**：Windows 防火墙可能拦截，需要允许通过
4. 代理启动后会输出局域网地址，如：
   ```
   weflow-proxy listening
   您可通过此地址访问 Weflow API: http://192.168.1.100:5032
   ```
   如果显示多个 IP，选择与本机同一子网的地址。请用户提供该地址
5. 验证：
   ```bash
   python3 <skill_dir>/scripts/check_weflow.py --host http://<windows-ip>:5032
   ```
6. 如果验证仍然失败：确认代理还在运行、Windows 防火墙已放行 5032 端口、VM 网络为桥接模式（非 NAT）

## Step b: 获取群聊列表

```bash
python3 <skill_dir>/scripts/fetch_groups.py <HOST>
```

输出格式：
```
1. 群名A [12345678@chatroom]
2. 群名B [87654321@chatroom]
```

展示列表给用户，让用户选择要监控的群聊。用户可选多个，对每个群重复 Step c。

## Step c: 配置群聊

首先准备配置文件（仅首次）：
```bash
cp <skill_dir>/weflow-groups.yaml <用户指定路径>/weflow-groups.yaml
```
让用户选择存放位置，后续统一使用此路径（记为 `CONFIG`）。

对每个选中的群聊，依次收集：

### 1. 总结提示词

询问用户希望如何总结群消息。示例：
- `"简洁总结今天的讨论要点"`
- `"你是情报分析专家，挖掘群聊中的高价值信息"`
- `"关注技术讨论，忽略闲聊"`

### 2. 关注特定群友（可选）

如果用户需要单独追踪某些群友的发言：

1. 请用户从 WeFlow 导出群成员：WeFlow 界面 → 群聊分析 → 群成员查看 → 导出成员（生成 .xlsx 文件）。如果用户还没有文件，等用户提供后再继续
2. 运行转换脚本（仅生成 JSON，不修改配置）：
   ```bash
   python3 <skill_dir>/scripts/convert_members.py <xlsx文件>
   ```
   输出文件为 `<xlsx文件名>_members.json`，格式：`{"wxid_xxx": "昵称（群昵称）"}`
3. 询问用户要关注谁，用 `grep` 在 JSON 中搜索：
   ```bash
   grep "张三" <生成的_members.json>
   ```
4. 将匹配的 wxid 展示给用户确认

### 3. 写入配置

```bash
python3 <skill_dir>/scripts/add_group.py CONFIG \
  --host <HOST> \
  --talker <chatroom_id> \
  --name "群聊名称" \
  --summary-prompt "总结提示词" \
  --members /path/to/members.json \
  --subscribe-members wxid_1 wxid_2
```

- `--host` 仅首次需要
- `--members` 使用绝对路径（即 convert_members.py 输出中 `Written to` 后的路径）
- `--subscribe-members` 可选，建议与 `--members` 一起使用以显示昵称
- 修改已有群聊：加 `--update` 标志

## Step d: 配置心跳

心跳即定期运行以下命令来检查新消息并生成总结。`CONFIG` 即 Step c 中复制的配置文件路径。

**心跳执行命令：**
```bash
python3 <skill_dir>/scripts/fetch_messages.py CONFIG
```

如果脚本报错（连接失败、配置缺失等），将错误信息报告给用户，不要回复 `HEARTBEAT_OK`。

**处理脚本输出：**
- 如果所有群的输出都包含 `无新消息` → 回复 `HEARTBEAT_OK`
- 如果有新消息 → 脚本会输出每个群的消息，格式如下：

```
群名：工作群
用户要求：简洁总结今天的讨论要点
近期群信息：
[2026-03-10 09:15] 张三: 会议改到下午3点
[2026-03-10 09:20] 李四: 好的，已通知客户
[2026-03-10 10:00] 王五: [图片] /path/to/image.jpg

另外总结关注群友的发言：
张三说：
1. 会议改到下午3点
```

对每个有新消息的群：
1. 将「用户要求」作为总结指令
2. 根据指令总结「近期群信息」中的内容
3. 如有「关注群友的发言」部分，单独总结
4. 如有图片路径，读取图片并在总结中描述内容
5. 跳过无新消息的群，不需要提及
