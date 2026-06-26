# SKILL.md - 「自己」通用版微信画像分析

> 给任何使用 OpenClaw 的用户使用的版本
> 内置 three-layer-memory 三层记忆系统，无需额外安装

---

## 这是什么

一个**零依赖、开箱即用**的微信画像分析 Skill，包含：

1. **wechat-decrypt** — 微信数据库解密工具
2. **三层记忆系统** — 热/暖/冷三层记忆，自动管理 Token 消耗
3. **微信画像分析引擎** — 生成 9 个维度的结构化人格画像
4. **Micro Sync** — 自动同步到热层，让 AI 助手持续进化

---

## 工作流程

```
微信数据库 → 解密 → 分析引擎 → 画像文件 → 冷层存储
                                              ↓
                                    三层记忆系统
                                              ↓
                                    热层(MEMORY.md) → AI 直接调用
```

---

## 目录结构

```
自己/
├── SKILL.md                      ← 本文件
├── README.md                     ← 使用说明（给最终用户的）
├── analyzer/                     ← 微信分析引擎
│   ├── setup.py                  ← 下载 wechat-decrypt
│   ├── main.py                   ← 主分析脚本
│   ├── sync.py                   ← Micro Sync
│   ├── config.py                 ← 过滤规则
│   └── models.py                 ← 数据模型
├── three-layer-memory/           ← ⭐ 三层记忆系统本体（内置，无需额外安装）
│   ├── SKILL.md                  ← 详细文档
│   ├── scripts/
│   │   ├── micro-sync.sh
│   │   ├── daily-wrapup.sh
│   │   └── weekly-compound.sh
│   ├── references/
│   │   └── agents-rules.md
│   └── _meta/
│       └── origin.json
└── storage/                     ← 用户数据目录（可选）
    └── cold/另一个我/           ← 画像文件存放位置
```

---

## 安装（一次性）

### Step 1: 下载 wechat-decrypt

```powershell
# 在 PowerShell（管理员模式）运行：
python "C:\Users\12084\Desktop\阿巴阿巴工作区\自己\analyzer\setup.py"
```

### Step 2: 解密微信数据库

1. 打开微信电脑版并登录
2. 在微信里打开几张图片（触发密钥提取）
3. 保持微信运行，运行：

```powershell
python C:\wechat-decrypt\main.py decrypt
```

成功标志：
```
21 成功, 0 失败, 共 21 个
解密数据量: 0.7GB
```

---

## 使用

### 方式一：通过 OpenClaw 触发（推荐）

直接跟 AI 说：
- "分析我的微信"
- "更新我的画像"
- "另一个我"
- "解密微信"

### 方式二：手动运行

```powershell
# 分析
cd "C:\Users\12084\Desktop\阿巴阿巴工作区\自己"
python analyzer/main.py

# 同步到热层
python analyzer/sync.py
```

---

## 内置的三层记忆系统

### 架构

```
热层（每次加载）
├── MEMORY.md           ← AI 直接读取
├── SOUL/USER/AGENTS.md
└── LanceDB 向量注入

暖层（自动维护）
├── autoCapture         ← 实时抓取 session
├── Micro Sync          ← 每天 5 次
└── Daily Wrapup        ← 每天凌晨

冷层（按需查询）
├── storage/cold/       ← 画像文件
├── archive/           ← 历史归档
└── second-brain/      ← 深度报告
```

### Token 节省效果

- **无三层记忆**：每次对话重载全部上下文，消耗大
- **有三层记忆**：热层 ≤8KB，暖层按需，冷层向量检索，**节省 99% Token**

---

## 过滤规则

分析引擎会自动过滤以下内容：

- 营销/福利群（奶茶、咖啡、外卖、红包、优惠券等）
- 公众号推送（gh_、brandsessionholder 等）
- 商业账号（论文辅导、考证推销等）
- 机器人消息

---

## 数据存储位置

| 类型 | 路径 |
|---|---|
| 解密工具 | `C:\wechat-decrypt\` |
| 解密数据 | `C:\wechat-decrypt\decrypted\` |
| 画像文件 | `C:\Users\12084\Desktop\阿巴阿巴工作区\自己\storage\cold\另一个我\` |
| 热层记忆 | `~/.openclaw/workspace/MEMORY.md` |

---

## 隐私说明

- ✅ 所有数据存储在本地，不上传任何服务器
- ✅ 仅分析用户本人的微信数据
- ✅ 垃圾群/公众号自动过滤
- ✅ wechat-decrypt 从进程内存读取密钥，不涉及账号密码

---

## 前置要求

- Windows 10/11
- 微信电脑版 4.x（2025年8月后）
- Python 3.8+
- Git
- 管理员权限（读取进程内存）

---

## 更新日志

- 2026-04-02: 首次创建，通用版打包 three-layer-memory 本体
