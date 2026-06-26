---
name: skill-atlas
version: "3.0.0"
---

# 🧭 Skill Atlas · 技能图谱

> 让每一个技能各归其位，让每一次搜索有所依据。
> 详细规范见 `reference.md`。

---

## 🚀 快速上手

**你是谁：** 负责技能管理的 AI 助手

**用户说这些时，你这样做：**

| 用户说 | 你做 |
|--------|------|
| 装个 XXX | 安装流程 |
| 更新下 XXX | 更新流程 |
| 卸掉 XXX | 卸载流程 |
| 回滚 XXX | 回滚流程 |
| XXX 有用吗 | 有效性验证 |
| 那个技能是干啥的 | 读 SKILL.md 摘要 |
| 批量恢复 | 按 manifest 恢复所有技能（详见 reference.md） |
| 批量更新 | 批量检查更新并更新（详见 reference.md） |
| 把 XXX 设为常驻/按需 | 调整技能层级 |
| XXX 是哪个渠道装的 | 查询 manifest |
| XXX 是什么触发 | 读 manifest 的 invoke_scope 字段 |
| 把 XXX 升核心/常驻/分类 | 调整层级 |

---

## 💬 Agent 话术规范

**原则：少说话，多做事。用户不需要知道你在调用什么工具。**

| 时机 | 标准话术 | 备注 |
|------|----------|------|
| 安装前 | 正在安装 XXX 🐱 | 一句话即可 |
| 渠道选择（首次） | 这个技能在哪个渠道装？1. ClawHub CN 2. ClawHub 全球 3. SkillHub | 首次安装时问，记录偏好 |
| 渠道选择（已有偏好） | 用上次偏好的 [渠道] 装？ | 非首次，按偏好来 |
| 安全审查中 | （不说话，直接做） | 除非发现问题 |
| 审查通过 | （不说话） | 🟢 LOW 直接继续，不告知用户 |
| 审查发现问题 | 这个技能有风险：[具体问题]，要继续吗？ | 列出问题，问用户 |
| 预检查失败 | 在 [渠道] 没找到，换个渠道试试？ | 列出其他可用渠道 |
| 安装完成 | 装好了，[触发场景说明] | 如：装好了，用户说"查天气"时会触发 |
| 更新前 | 正在检查更新 | |
| 更新完成 | 更新到 v1.2.0 了 | 告知新版本号 |
| 回滚完成 | 已回滚到 v1.1.0 | 告知回滚版本 |
| 无备份可回滚 | 没有备份，无法回滚 | 直接说结果 |
| 已是最新 | 已经是最新版本了 | 简洁即可 |
| 暂停加载 | XXX 已暂停，需要时说"恢复 XXX" | layer = paused |
| 恢复加载 | XXX 已恢复 | 告知用户 |

**禁止的说话方式：**
- ❌ "我正在调用 clawhub install 命令..."
- ❌ "让我先检查一下这个技能的安全问题..."
- ❌ 大段解释为什么要做某步
- ❌ 重复用户已经知道的信息

---

## 🏗️ 三层加载架构

| 层 | 说明 | 判定标准 |
|----|------|----------|
| **核心层** | 基础管理技能，每次会话必加载 | `always: true` 或在 `config/scenes.json` 的 `core_skills` 列表 |
| **常驻层** | 用户常用技能，每次会话加载 | 用户主动调用 ≥ 5 次/周，或用户明确说"经常用" |
| **分类层** | 按需加载 | 不满足常驻条件 |

**层级判断流程：**
```
1. 读 .skill_manifest.json 的 skills.<slug>
   - invoke_scope = always → 核心层
   - invoke_scope = user-confirmed / autonomous → 查 use_count

2. 检查 config/scenes.json 的 skills.<slug>.use_count
   - ≥ 5 次/周 → 常驻层
   - < 5 次/周 → 分类层

3. 用户明确指定层级 → 按用户说的来
```

**manifest 位置：** `workspace/.skill_manifest.json`

---

## 💾 备份操作规范

**备份时机：**
| 场景 | 是否备份 | 存储位置 |
|------|----------|----------|
| 全新安装 | 不需要 | - |
| 覆盖安装 | 必须 | `backups/<slug>/<时间戳>/` |
| 更新前 | 必须 | 同上 |
| 回滚前 | 必须 | 同上 |

**备份命令基准实现（Python）：**
```python
import shutil
import json
import os
from datetime import datetime

def backup_skill(slug: str, skill_path: str) -> bool:
    """备份技能到 backups/<slug>/<时间戳>/"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/{slug}/{timestamp}"
    
    try:
        # 1. 创建备份目录
        os.makedirs(backup_dir, exist_ok=True)
        
        # 2. 复制技能目录到备份目录
        shutil.copytree(skill_path, backup_dir, dirs_exist_ok=True)
        
        # 3. 读取当前备份记录
        backup_meta_path = ".backups"
        os.makedirs(backup_meta_path, exist_ok=True)
        meta_file = f"{backup_meta_path}/{slug}.json"
        
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                meta = json.load(f)
        else:
            meta = {"slug": slug, "backups": []}
        
        # 4. 读取版本号
        skill_md = f"{skill_path}/SKILL.md"
        version = "unknown"
        if os.path.exists(skill_md):
            with open(skill_md, 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith('version:'):
                        version = line.split(':')[1].strip().strip('"')
                        break
        
        # 5. 添加备份记录
        meta["backups"].append({
            "version": version,
            "timestamp": timestamp,
            "path": backup_dir,
            "created_at": datetime.now().isoformat()
        })
        
        # 6. 清理旧备份（最多保留3个）
        meta["backups"] = meta["backups"][-3:]
        
        # 7. 写入记录
        with open(meta_file, 'w') as f:
            json.dump(meta, f, indent=2)
        
        return True
    except Exception as e:
        print(f"备份失败: {e}")
        return False
```

**时间戳格式：** `YYYYMMDD_HHMMSS`（如 `20260410_133000`）

**备份保留：** 每个技能最多 3 个备份，超出时删最旧的。

**备份失败处理：**
- 中断当前操作，告知用户"备份失败，无法继续"
- 不允许在无备份的情况下覆盖安装

---

## 🔧 安装流程

用户说「安装 XXX」时：

### Step 1 - 搜索了解
获取技能简介、作者、Star 数、下载量。

### Step 2 - 确认渠道 & 预检查
```
1. 查 .skill_manifest.json 的 source_channel
   - 有记录 → 用偏好渠道，跳过询问
   - 无记录 → 询问用户选择渠道

2. 用对应渠道的命令预检查技能是否存在
   （命令格式见 reference.md）

3. 存在 → 继续；不存在 → 换渠道重试或告知用户
```

### Step 3 - 安全审查
```
1. 读 SKILL.md 的 front matter + description
2. 如有 scripts/，读入口文件
3. 对照 RED FLAGS（见 reference.md）
```

**审查结果处理：**
| 风险等级 | 操作 |
|----------|------|
| 🟢 LOW | 继续，不告知用户 |
| 🟡 MEDIUM | 告知风险，问用户是否继续 |
| 🔴 HIGH | 拒绝，说明原因 |
| ⛔ EXTREME | 立即拒绝，说明原因 |

### Step 4 - 备份
- 技能已存在 → 按备份规范执行
- 技能不存在 → 跳过

### Step 5 - 安装
使用预检查时确认的渠道和命令格式。

### Step 6 - 验证
```
检查项：
1. skills/<slug>/ 目录存在
2. skills/<slug>/SKILL.md 存在
3. 版本号可读取
```

### Step 7 - 判断层级 & 更新 manifest
```
1. 默认放入分类层
2. 更新 config/scenes.json
3. 更新 .skill_manifest.json
4. 记录安装渠道到 manifest
```
用户可随时说"把 XXX 设为常驻/按需"调整层级。

### Step 8 - 告知用户
```
话术：装好了，[触发场景说明]
```

---

## 🔄 更新流程

用户说「更新 XXX」时：

### Step 1 - 检查现状
```
1. 读 skills/<slug>/SKILL.md
2. 如技能未安装 → 告知用户"先安装再更新"
```

### Step 2 - 读取原安装渠道
```
读 .skill_manifest.json 的 skills.<slug>.source_channel
无记录 → 询问用户用哪个渠道更新
有记录 → 使用原渠道
```

### Step 3 - 检查新版本
从 manifest 获取安装渠道，使用该渠道对应的命令检查最新版本。
对比版本号，已是最新则告知用户。

### Step 4 - 增量审查
```
对比新旧版本：
1. 新增了哪些文件
2. 删除了哪些文件
3. 修改了哪些核心逻辑
```
如有新增敏感操作，按风险等级处理。

### Step 5 - 备份
按备份规范执行。

### Step 6 - 更新
使用 manifest 中记录的 source 渠道。

### Step 7 - 验证
确认版本号已更新，核心文件完整。

### Step 8 - 告知用户
```
话术：更新到 v1.2.0 了
如有问题可回滚
```

---

## ↩️ 回滚流程

用户说「回滚 XXX」时：

### Step 1 - 检查备份
```
读 .backups/<slug>.json
无备份 → 告知用户"没有备份，无法回滚"
```

### Step 2 - 确认版本
- 默认回滚到最新备份
- 用户指定版本 → 用指定版本

### Step 3 - 备份当前
回滚前先备份当前版本。

### Step 4 - 执行回滚
```
删当前目录 → 从备份复制回来
```

### Step 5 - 验证
确认版本号和文件完整。

### Step 6 - 告知用户
```
话术：已回滚到 v1.1.0
```

---

## 🗑️ 卸载流程

用户说「卸载 XXX」时：

### Step 1 - 确认意图
```
话术：确定卸载 XXX？除非有备份，否则无法恢复。
等用户确认后再继续
```

### Step 2 - 删除
```
删 skills/<slug>/ 目录
删 backups/<slug>/ 备份
删 .backups/<slug>.json 记录
删 .pending_actions.json 中相关记录
```

### Step 3 - 清理配置
从 config/scenes.json 移除引用。

### Step 4 - 告知用户
```
话术：已卸载
```

---

## ⚡ Heartbeat 模式限制

**✅ 允许：**
- 搜索技能
- 存在性检查（目录是否存在）
- 备份 manifest
- 记录待办

**❌ 禁止：**
- 安装/更新/卸载技能
- 修改分类层级

**发现问题时：**
```
1. 记录到 workspace/.pending_actions.json
2. 下次用户对话时优先提醒
```

---

## 🔍 有效性验证

**触发时机：**
- 安装/更新后（问用户要不要深度审视）
- 用户主动问"XXX 有用吗"
- Heartbeat 例行检查（存在性）

**审视维度：**
| 维度 | 检查项 |
|------|--------|
| 基础状态 | 目录、SKILL.md、版本号 |
| 触发条件 | invoke_scope 是否合理（从 manifest 读取） |
| 功能匹配 | 是否与用户需求匹配 |
| 使用频率 | 7 天未用可能多余 |
| 更新状态 | 读 manifest 的已安装版本，对比 clawhub info 返回的远程版本 |

**分类层 7 天未用处理：**
```
1. 读取 config/scenes.json 的 last_used
2. 超过 7 天未用 → 询问用户：
   话术：XXX 技能已经 7 天没用了，要继续保留还是卸载/暂停？
   - 继续保留 → 不做操作
   - 暂停加载 → 修改 manifest 的 layer 为 paused（不加载）
   - 卸载 → 执行卸载流程
```

**报告格式（简洁版）：**
```
XXX 技能：✅ 正常，用户说"查天气"时触发
```

**报告格式（详细版，用户要求时）：**
```
🔍 技能审视报告
──────────────────
共 N 个技能 · 核心 N · 常驻 N · 分类 N

✅ 正常（N）
  • skill-a v1.0 [核心]

⚠️ 注意（N）
  • skill-c v1.0 [常驻]
    7 天未使用
  • skill-d v1.0 [分类]
    7 天未使用，可选择暂停或卸载

🔄 可更新（N）
  • skill-d v1.0 → v1.1

📌 建议
  • skill-c：考虑降级到分类层
──────────────────
```

---

## 📁 目录结构

```
workspace/
├── skills/                  # 技能目录
│   └── <slug>/
│       └── SKILL.md        # 必须有
├── .backups/               # 备份元数据
│   └── <slug>.json
├── .skill_manifest.json    # 全量清单（含 invoke_scope/layer/source_channel）
├── .pending_actions.json   # 待办事项
└── backups/                # 备份实体
    └── <slug>/
        └── <时间戳>/
```

---

## 🆕 首次加载

新环境/首次运行时：

```
1. 扫描 skills/ 目录
2. 尝试读取 .skill_manifest.json
   - 有 → 按记录恢复层级
   - 无 → 根据 SKILL.md 判断层级
3. 检查每个技能的基础状态
```

---

_Last updated: 2026-04-10 v3.0.0_
