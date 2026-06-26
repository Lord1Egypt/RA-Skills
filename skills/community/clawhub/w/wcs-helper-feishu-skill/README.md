# guanqi-feishu-config

私聊发送命令，控制 OpenClaw 飞书插件。纯文本响应，不需要按钮，不需要卡片。

## 安装

```bash
npx -y clawhub install guanqi0914/guanqi-feishu-config
```

## 命令列表

| 命令 | 作用 |
|------|------|
| `/万重山-飞书` | 查看当前所有设置 |
| `/万重山-飞书-打字效果` | 开/关打字效果（toggle） |
| `/万重山-飞书-群里-A` | 群里只回@我的 |
| `/万重山-飞书-群里-B` | 群里什么都回 |
| `/万重山-飞书-诊断` | 检查飞书插件状态 |
| `/万重山-飞书-重启` | 重启 OpenClaw 服务 |
| `/万重山-飞书-帮助` | 显示帮助 |

## 文件结构

```
guanqi-feishu-config/
├── feishu_handler.py   ← 命令路由（私聊消息 → skill.py）
├── skill.py            ← 核心逻辑（读写 openclaw config）
├── skill.json          ← 元数据
└── README.md
```

## 工作原理

```
飞书私聊消息
    ↓
feishu_handler.py（路由）
    ↓
skill.py（读写 openclaw config）
    ↓
纯文本响应 → 直接发回飞书
```

## 添加新命令

在 `skill.py` 的 `handle()` 函数中添加分支：

```python
if sub == "新命令":
    # 执行操作
    subprocess.run(["openclaw", "config", "set", "key", "value"])
    return "操作结果描述"
```
