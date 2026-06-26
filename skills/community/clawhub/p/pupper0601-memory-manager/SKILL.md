---
name: memory-manager
description: OpenClaw专用三层AI记忆管理系统。管理临时记忆(L1)/长期记忆(L2)/永久记忆(L3)，支持向量语义搜索、自动压缩、OpenClaw用户身份识别和跨设备同步。
version: 3.5.0
license: MIT
allowed-tools: Read,Write,Bash,Glob,Grep
environment:
  - OPENAI_API_KEY: 可选，OpenAI API密钥（用于向量嵌入）
  - SILICONFLOW_API_KEY: 可选，硅基流动API密钥（国内推荐）
  - ZHIPU_API_KEY: 可选，智谱AI API密钥
  - EMBED_BACKEND: 必需，指定后端（openai/siliconflow/zhipu）
  - GITHUB_TOKEN: 可选，用于GitHub同步
  - MM_UID: 可选，指定用户ID
  - MM_BASE_DIR: 可选，记忆仓库路径
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": {"bins": ["python", "git"]},
        "environment_variables": ["EMBED_BACKEND"],
        "optional_environment_variables": ["OPENAI_API_KEY", "SILICONFLOW_API_KEY", "ZHIPU_API_KEY", "GITHUB_TOKEN", "MM_UID", "MM_BASE_DIR"],
        "security_note": "该技能会读取users/目录下所有用户的profile.md文件以实现多用户识别，修改shell RC文件以持久化配置，使用curl|bash方式安装需谨慎",
        "data_scope": "会访问多用户私有文件、执行git操作、修改环境变量和配置文件",
        "install":
          [
            {
              "id": "openclaw-workspace",
              "kind": "script",
              "script": "install.sh",
              "args": ["-p", "$HOME/.openclaw/memory"],
              "label": "安装到 OpenClaw workspace (会修改shell配置文件)"
            }
          ],
        "integration": "OpenClaw 记忆后端",
        "auto_enable": true
      }
  }
read_when:
  - OpenClaw 会话开始时
  - 用户询问历史记忆时
  - 需要上下文理解时
  - 记录重要信息时
  - 总结近期工作时
---

# Memory Manager — 三层记忆 + 向量搜索 + 关联记忆（v3.5）

> [!IMPORTANT]
> **AI 必须遵守**：`MEMORY_STYLE_GUIDE.md` 中定义的记忆文件规范。  
> 任何写入记忆系统的操作，都必须遵循该规范。

> [!TIP]
> **OpenClaw 用户**：请参考 `README.md` 中的「OpenClaw 集成安装」章节。

## OpenClaw 专用安装

```bash
# 方法1: 通过 OpenClaw skill 管理器安装
# （推荐）OpenClaw 会自动处理依赖和配置

# 方法2: 手动安装到 OpenClaw workspace
cd ~/.openclaw/workspace/skills/
git clone https://github.com/Pupper0601/memory-manager.git
cd memory-manager

# 安装依赖
pip install -r requirements.txt

# 配置 OpenClaw 记忆系统
mm onboard --openclaw

# 方法3: 一键安装脚本
curl -fsSL https://raw.githubusercontent.com/Pupper0601/memory-manager/main/install.sh | bash -s -- -p "$HOME/.openclaw/memory"
```

## 多用户架构

```
memory-repo/
├── shared/              # 公共记忆
│   ├── daily/           # 公共临时（当天）
│   ├── weekly/          # 公共周报（本周）
│   └── permanent/      # 公共永久
└── users/{uid}/        # 私人记忆
    ├── daily/           # L1 临时
    ├── weekly/          # L2 长期
    ├── archive/         # 归档
    └── permanent/       # L3 永久
```

## 记忆归属

| 内容 | 归属 | 路径 |
|------|------|------|
| 个人当天任务/进展 | 私人L1 | `users/{uid}/daily/YYYY-MM-DD.md` |
| 个人本周计划/总结 | 私人L2 | `users/{uid}/weekly/YYYY-WNN.md` |
| 个人经验/偏好/决策 | 私人L3 | `users/{uid}/permanent/*.md` |
| 团队当天进展 | 公共临时 | `shared/daily/YYYY-MM-DD.md` |
| 团队本周摘要 | 公共周报 | `shared/weekly/YYYY-WNN.md` |
| 项目/技术/决策 | 公共L3 | `shared/permanent/*.md` |
| 行为习惯 | 私人 | `users/{uid}/HABITS.md` |

## 会话启动流程

> ⚠️ **跨设备场景**：用户可能从不同设备（WorkBuddy / 企微 / 飞书 / Web）发起会话，AI **必须**通过以下步骤自动解析 uid，不能假设用户 ID。

```
1. 自动解析 uid（按优先级）：
   ① 检查 users/ 目录下的子目录列表（git pull 后可见）
      - 若只有 1 个用户目录 → 直接使用该 uid
      - 若有多个 → 读取每个 users/{uid}/profile.md 的 uid 字段
      - 根据对话上下文（用户名/签名/问候）匹配最可能的 uid
   ② 读取 .current_user 文件（本地设备快速路径）
   ③ 环境变量 MEMORY_USER_ID
   ④ 都没有 → 询问用户："请问你是哪位？（输入你的用户ID）"

2. git pull → 同步最新记忆（确保拿到最新 profile.md 等文件）

3. ⚠️ 版本检查（必做）：
   - 读取记忆仓库根目录的 SKILL_VERSION.md
   - 提取 required_skill_version 字段
   - 与本 SKILL.md 顶部的 version 字段对比
   - 若本地版本 < required_skill_version：
     ⛔ 立即提示用户：
     "⚠️ memory-manager skill 需要更新！
      当前版本: {local_version}，要求版本: {required_version}
      请运行：git -C ~/.workbuddy/skills/memory-manager pull
      或查看 Release：https://github.com/Pupper0601/memory-manager/releases"
   - 版本满足则静默继续

4. 读取 users/{uid}/profile.md → 确认身份
5. 读取当天 L1 文件（如存在）
6. 读取 users/{uid}/HABITS.md
7. 读取 shared/permanent/（如上下文相关）
8. 如有搜索需求 → 使用 memory_search.py
```

### uid 自动解析脚本

```python
import os

def resolve_uid(repo_dir: str) -> str:
    """跨设备自动解析当前用户 uid"""
    
    # 方式 1：读取本地 .current_user（本设备快速路径）
    current_user_file = os.path.join(repo_dir, ".current_user")
    if os.path.exists(current_user_file):
        with open(current_user_file) as f:
            uid = f.read().strip()
        if uid:
            return uid
    
    # 方式 2：扫描 users/ 目录下的 profile.md（跨设备路径）
    users_dir = os.path.join(repo_dir, "users")
    if os.path.exists(users_dir):
        candidates = []
        for name in os.listdir(users_dir):
            profile = os.path.join(users_dir, name, "profile.md")
            if os.path.exists(profile):
                candidates.append(name)
        if len(candidates) == 1:
            return candidates[0]   # 单用户直接返回
        # 多用户 → 返回列表让 AI 选择
        return f"[多用户: {', '.join(candidates)}]"
    
    # 方式 3：环境变量
    return os.environ.get("MEMORY_USER_ID", "")
```



## 写入规则

> ⚠️ **严格遵守 MEMORY_STYLE_GUIDE.md 规范！**

- **命名规范**：`{类型前缀}_{简短描述}_{日期}.md`，如 `idea_autosave_v2_20260404.md`
- **必须字段**：`type`, `created`, `updated`, `tags`, `scope`, `importance`
- **Frontmatter**：每个记忆文件开头必须有完整的 YAML frontmatter
- **内容模板**：使用规范中定义的模板（idea/dec/learn/daily）
- **文件大小**：单个文件不超过 10KB
- **禁止内容**：禁止记录密码、密钥、Token、他人隐私信息
- 公共记忆：写入 `shared/permanent/` + git pull + push
- 私人记忆：写入 `users/{uid}/` + git add + commit + push
- 压缩触发：L1 >150行 / L2 >200行 / L3 >300行 → `python scripts/memory_compress.py --uid {uid} --upgrade`

### 写入前自检

```bash
# 写入前运行检查
mm lint --path {新文件路径}
```

## 升级标记

| 标记 | 动作 |
|------|------|
| `[IMPORTANT]` | 升级到 L2 |
| `[PERMANENT]` / `[升级L3]` | 升级到 L3 |
| `[HABIT]` | 提取到 HABITS.md |

## 向量搜索

```bash
# 首次：生成向量库
mm embed --rebuild

# 语义搜索（直接输入搜索内容）
mm search "我上周做了什么"

# 搜索公共记忆
mm search "团队进展" --shared

# 关键词 fallback（无 API 依赖）
mm search "memory" --keyword-only

# 调整语义权重（默认 0.6）
# 0.8 = 纯语义相似度，0.3 = 重要性优先
python scripts/memory_search.py --uid pupper --query "重要决策" --semantic-weight 0.3

# 查看向量库统计
mm stats

# 重建 LanceDB HNSW 索引（加速搜索 100x）
python scripts/memory_search.py --uid pupper --rebuild-index

# 显示缓存统计
python scripts/memory_search.py --uid pupper --cache-stats
```

> **性能优化**：安装 LanceDB 可获得 100x 搜索加速：`pip install lancedb`

## 快捷命令

- `"记住这个"` → `mm log "内容"`
- `"同步记忆"` → git pull + push
- `"查找记忆 [词]"` → `mm search "[词]"`
- `"记忆报告"` → `mm insight`
- `"AI 总结"` → `mm insight --weekly`
- `"生成向量"` → `mm embed`

## AI 洞察

```bash
# 综合洞察
mm insight

# 每日洞察
mm insight --daily

# 每周洞察
mm insight --weekly
```

> 💡 **推荐**：使用 memory-agent skill，无需命令，开口即搜。

## 核心原则

1. **身份优先**：操作前确认 uid，公私绝不混写
2. **同步为先**：写入前 pull，写入后立即 push
3. **冲突保守**：公共冲突不覆盖，标记待人工处理
4. **向量优先**：搜索优先向量语义，关键词作 fallback

---

完整文档见 `reference.md`
