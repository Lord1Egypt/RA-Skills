# 喜乐姐真蚕丝喜被 AI Skill

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![MCP](https://img.shields.io/badge/protocol-MCP-purple) ![Transport](https://img.shields.io/badge/transport-Streamable%20HTTP-orange)

这是一个 AI Skill——安装后，你的 AI 助手就能帮你查询喜乐姐蚕丝被的产品信息：有什么规格、多少钱、怎么选、蚕丝是不是真的、怎么洗怎么保养。还能直接帮你下单，货到付款。

一床好蚕丝被，现在有了自己的AI助手。

## 关于喜乐姐

喜乐姐真蚕丝喜被，专注桑蚕长丝被。手工拉丝、工厂直发、假一赔十。

| 项目 | 内容 |
|------|------|
| 品牌名称 | 喜乐姐真蚕丝喜被 |
| 主营产品 | 桑蚕长丝被（夏凉被/春秋被/冬被/子母被/喜被） |
| 付款方式 | 货到付款，不用提前转账 |
| 售后承诺 | 7天无理由退换，3年质保，假一赔十 |

## 这个 Skill 能做什么

| 能力 | 你可以问 |
|------|----------|
| 品牌介绍 | "喜乐姐是什么牌子？" |
| 产品规格价格 | "蚕丝被多少钱？""有什么规格？" |
| 选购推荐 | "1.8米的床买多大？""送人买哪款？" |
| 蚕丝真伪鉴别 | "蚕丝是真的吗？""怎么辨别真假？" |
| 洗涤保养 | "蚕丝被能洗吗？""怎么保养？" |
| 售后政策 | "包邮吗？""能退吗？" |
| **下单** | "我要买一床""下单" |
| 查订单 | "我的订单到哪了？" |
| 最新活动 | "有什么优惠？" |

## 安装

### 最简单的方式：告诉你的 AI 助手

直接拷贝下面这句话发给你的 AI 助手：

> 帮我安装喜乐姐蚕丝被 Skill，仓库地址：https://gitee.com/lao-zou2026/xilejie-silk-quilt-skill

Agent 会自动克隆仓库并安装到对应的 Skill 目录。

### 手动克隆到 Skill 目录

将本仓库克隆到你项目下的 Skill 目录，不同 IDE 对应的路径：

| IDE | Skill 目录 |
|-----|-------------|
| Qoder | `.qoder/skills/xilejie-silk-quilt-skill/` |
| Cursor | `.cursor/skills/xilejie-silk-quilt-skill/` |
| Trae | `.trae/skills/xilejie-silk-quilt-skill/` |
| Windsurf | `.windsurf/skills/xilejie-silk-quilt-skill/` |
| Claude Code | `.claude/skills/xilejie-silk-quilt-skill/` |
| 通用 | `.agents/skills/xilejie-silk-quilt-skill/` |

```bash
# 示例：安装到 Windsurf
git clone https://gitee.com/lao-zou2026/xilejie-silk-quilt-skill.git \
  .windsurf/skills/xilejie-silk-quilt-skill
```

只要目录下有 `SKILL.md`，Agent 下次启动就会自动加载这个 Skill。

## 目录结构

```
xilejie-silk-quilt-skill/
├── SKILL.md                 # 核心文件：元数据 + Agent 指令
├── skill.json               # 机器可读配置（MCP 端点、工具定义）
├── backend/                 # 后端服务代码
│   ├── main.py              # FastAPI 服务主文件
│   ├── data.py              # 产品数据与业务逻辑
│   ├── requirements.txt     # Python 依赖
│   └── start.bat            # 一键启动脚本（Windows）
├── README.md
└── LICENSE
```

## 技术协议

| 项目 | 说明 |
|------|------|
| 协议 | MCP (Model Context Protocol) |
| 传输 | Streamable HTTP |
| MCP 端点 | https://xilejie-silk.com |
| 后端框架 | Python FastAPI |
| 数据库 | SQLite |
| 部署 | 腾讯云轻量服务器（已上线） |

## 版本

当前版本：0.1.0

## License

[MIT](LICENSE)
