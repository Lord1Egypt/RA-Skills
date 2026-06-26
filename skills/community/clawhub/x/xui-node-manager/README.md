# xui-node-manager

OpenClaw AI 技能 — 让 AI 自动安装 3x-ui 面板并创建 VLESS+Reality+TCP 节点。

## 这是什么

这是一个给 **AI 助手** 用的技能包（Skill），不是给人类手动执行的脚本集合。安装后，AI 会直接帮你完成以下工作：

> 你只需告诉 AI「把这个 SOCKS5 出口配到 server-1」，剩下的 AI 全自动搞定。

AI 能做的事：
- SSH 登服务器，全自动安装 3x-ui 面板
- 创建 VLESS+Reality+TCP 入站，自动生成密钥
- 绑定 SOCKS5 出站 + 路由规则，自动重启 Xray
- 生成二维码和 `vless://` 链接直接发给你

## 安装

```bash
# 放到 OpenClaw 的 skills 目录
unzip xui-node-manager.skill -d ~/.openclaw/skills/
```

## 使用方式

对话即可，无需手动操作。AI 会自动选择合适的脚本执行。

| 你想做什么 | 跟 AI 说 | AI 执行 |
|-----------|---------|--------|
| 装面板 | 「用这个 IP:端口:用户名:密码 装个 3x-ui」 | `xui_install.sh` |
| 注册面板 | 「把这个面板加到 server-2」 | 修改 `servers.yaml` |
| 创建节点 | 「出口 214.0.13.15 配到 server-1」 | `xui_batch.py` |

## 依赖

需在运行 OpenClaw 的机器上安装：

```bash
pip install -r scripts/requirements.txt
brew install sshpass expect   # 仅安装面板需要
```

## 配置

`scripts/servers.yaml`（安装面板后 AI 会自动写入，也可手动编辑）：

```yaml
proxy: socks5://127.0.0.1:10808   # 访问面板的代理

defaults:
  dest: 1.1.1.1:443                # Reality 回落目标
  server_names: [www.microsoft.com] # Reality SNI
  port: random
  port_range: [10000, 60000]

servers:
  - name: server-1
    url: http://<ip>:<port>/<path>
    username: <用户名>
    password: <密码>
```

## 脚本说明（供参考，一般无需手动执行）

### `xui_install.sh` — 面板安装

```bash
bash scripts/xui_install.sh <ip> <ssh端口> <用户名> <密码>
```

自动 SSH 连接 → 执行 3x-ui 安装 → 全自动应答 → 提取面板信息。

### `xui_batch.py` — 节点创建

```bash
python3 scripts/xui_batch.py --server <服务器名> --socks5 <ip:port:user:pass>
```

创建 VLESS+Reality+TCP 入站 + SOCKS5 出站绑定 + 路由规则 + Xray 重启。

### 自动配置项

| 配置 | 规则 | 示例 |
|------|------|------|
| 备注 | 日期 + IP 末两段 | `2026-05-21-23.109` |
| 端口 | 随机 10000–60000 | `25827` |
| 客户端标识 | IP末两段-日期 | `23.109-2026-05-21` |
| Reality dest | `1.1.1.1:443` | — |
| Reality SNI | `www.microsoft.com` | — |

## 安全

- `servers.yaml` 含面板凭据，**已加入 .gitignore**
- AI 不会删除已有入站，需用户明确确认

## 文件结构

```
xui-node-manager/
├── README.md
├── SKILL.md                 # AI 行为指令
├── .gitignore
└── scripts/
    ├── xui_install.sh
    ├── xui_batch.py
    ├── requirements.txt
    ├── servers.yaml.example
    └── servers.yaml         # 不提交
```
