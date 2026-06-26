# 一键搬家材料打包清单

> 搬家包完整内容记录，确保一键搬家不遗漏任何关键材料
> 
> **v2.0 更新**：backup/ 目录列入维护，新增 backup_existing() 自动备份逻辑。

---

## 一、搬家包结构

```
搬家包/
├── README.md                    ← 动态生成（v2.0自动推断内容）
├── migrate.py                   ← v2.0 一键执行脚本
│
├── 身份层/                      ← Main Agent（自动检测workspace）
│   ├── SOUL.md                  ← 人格定义（必须）
│   ├── MEMORY.md                ← 长期记忆（必须）
│   ├── TOOLS.md                 ← 工具配置（必须）
│   ├── AGENTS.md                ← 团队成员表（必须）
│   ├── IDENTITY.md              ← 身份标识（必须）
│   ├── USER.md                  ← 用户信息（必须）
│   └── memory/                  ← 历史记录
│
├── 团队成员层/                  ← 团队成员（自动检测，有则包含）
│   ├── 成员A/
│   │   └── SOUL.md
│   ├── 成员B/
│   │   └── SOUL.md
│   └── ...（其他成员）
│
├── skills/                      ← Skills（自动检测，有则包含）
│   ├── team-resurrection/       ← 本skill
│   ├── agent-creator/
│   ├── novel-writer-structure/
│   └── 短流创规则/
│
├── openclaw-agents.json         ← Agent配置片段
└── cron_tasks.json              ← Cron任务清单
```

---

## 二、脚本说明（v2.0）

### 核心脚本

| 脚本 | 功能 | 必需性 |
|------|------|--------|
| `pack.py` | 打包所有资料 | ✅ 必需 |
| `migrate.py` | 一键搬家执行 | ✅ 必需 |
| `setup_config.py` | ~~仅更新配置~~ | ❌ 已废弃 |
| `init.sh` | ~~创建main agent~~ | ❌ 已废弃 |

> ⚠️ v2.0 将 setup_config.py 和 init.sh 的功能全部并入 migrate.py，无需单独执行。

### pack.py（打包脚本）

**功能：** 自动检测 active workspace，收集所有资料，生成搬家包

**执行方式：**
```bash
cd skills/team-resurrection
python3 pack.py
```

**收集内容（v2.0 自动检测）：**
- Main Agent 信息（SOUL.md/MEMORY.md 等，自动推断 workspace）
- 团队成员信息（自动检测，有则打包）
- Skills（自动检测，有则打包）
- Cron 任务配置（自动获取）
- Agent 配置片段

**输出：** `~/一键搬家包/{Agent名称}搬家包_YYYYMMDD_HHMMSS.zip`

### migrate.py（一键执行脚本）

**功能：** 完整的一键搬家流程

**执行方式：**
```bash
unzip Agent搬家包.zip
python3 Agent搬家包/migrate.py
```

**执行步骤：**
1. 检测环境（是否有main agent）
2. **让用户选择如何处理main agent**（不强制）
3. 复制身份文件
4. 复制团队成员
5. 复制skills
6. 更新openclaw.json
7. 创建cron任务
8. 重启Gateway

**用户选择逻辑：**
```
如果有main agent：
  1. 指向现有agent（把当前 agent 指向新 workspace）
  2. 新建main agent实例（保留当前的main，创建新的 main agent）
  3. 覆盖现有main agent（⚠️ 当前的main会被替换）

如果没有main agent：
  1. 指向现有agent
  2. 新建main agent实例
```

### setup_config.py（配置更新脚本）

**功能：** 仅更新配置，不复制文件

**执行方式：**
```bash
python3 setup_config.py
python3 setup_config.py --skip-cron      # 跳过cron创建
python3 setup_config.py --skip-restart   # 跳过Gateway重启
```

**用途：** 如果文件已手动复制，只需更新配置时使用

### init.sh（Step 0脚本）

**功能：** 创建main agent实例

**执行方式：**
```bash
chmod +x init.sh
./init.sh
```

**用途：** 如果新环境没有main agent，且用户选择"新建main agent实例"时使用

---

## 三、身份层文件说明

| 文件 | 作用 | 是否必须 |
|------|------|----------|
| SOUL.md | 人格定义、说话风格、行为规矩 | ✅ 必须 |
| MEMORY.md | 长期记忆、重要事件、决策记录 | ✅ 必须 |
| TOOLS.md | 工具配置、Agent ID、飞书ID | ✅ 必须 |
| AGENTS.md | 团队成员表、职责分工 | ✅ 必须 |
| IDENTITY.md | 身份标识（名字、头像） | ✅ 必须 |
| USER.md | 用户信息（姓名、偏好） | ✅ 必须 |
| memory/ | 历史记录目录 | ⭕ 可选 |

---

## 四、团队成员层说明

**目录命名规范：** `中文名/`（不带旧版ID后缀）

| 成员 | 目录名 | Agent ID | 职责 |
|------|--------|----------|------|
| 成员A | 成员A/ | member-a | 团队成员 |
| 成员B | 成员B/ | member-b | 团队成员 |
| 成员C | 成员C/ | member-c | 团队成员 |
| 成员D | 成员D/ | member-d | 团队成员 |
| 成员I | 成员I/ | member-i | 团队成员 |
| 成员E | 成员E/ | member-e | 团队成员 |
| 成员F | 成员F/ | member-f | 团队成员 |
| 成员G | 成员G/ | member-g | 团队成员 |
| 成员H | 成员H/ | member-h | 团队成员 |

**每个成员目录包含：**
- SOUL.md（人格定义）
- MEMORY.md（长期记忆）
- TOOLS.md（可选）

---

## 五、配置文件说明

### openclaw-agents.json

**位置：** 搬家包根目录

**作用：** Agent配置片段，用于`config.patch`更新

**关键配置：**
```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 10,
      "subagents": {
        "allowAgents": ["*"]
      }
    },
    "list": [
      {"id": "main", "name": "QClaw"},
      {"id": "member-a", "name": "成员A", "workspace": "...", "agentDir": "..."}
    ]
  },
  "hooks": {
    "allowedAgentIds": ["member-a", "member-b", ...]
  }
}
```

### cron_tasks.json

**位置：** 搬家包根目录

**作用：** Cron任务模板

**任务清单：**
| 任务名 | 频率 | 用途 |
|--------|------|------|
| team-daily-{name} | 每天01:00 | 激活成员 |
| main 每日自迭代 | 每天22:30 | 自我优化 |
| 短流创进度催促 | 每30分钟 | 检查未定稿作品 |

---

## 六、一键搬家完整流程

### 用户视角

```
用户（旧环境）：我要搬家
Agent：好的，开始打包...
       [执行 pack.py]
       打包完成：~/一键搬家包/xxx.zip

用户（新环境）：[把包丢给agent] 这是一键搬家包，帮我搬家
Agent：好的，开始执行...
       [解压 + 执行 migrate.py]
       
       请选择如何处理 Main Agent：
         1. 指向现有agent
         2. 新建main agent实例
         3. 覆盖现有main agent
       
       用户选择：2
       
       复制身份文件 ✓
       复制团队成员 ✓
       复制skills ✓
       更新配置 ✓
       创建cron ✓
       重启Gateway ✓
       ✅ 搬家完成！
```

### 手动执行

```bash
# Step 1: 打包（旧环境）
python3 skills/team-resurrection/pack.py

# Step 2: 复制搬家包到新环境

# Step 3: 执行搬家（新环境）
unzip Agent搬家包.zip
python3 Agent搬家包/migrate.py
```

---

## 七、通用化设计

### 核心原则

**自动适配，无需手动配置：**
- pack.py 会自动检测是否有团队成员
- migrate.py 会自动检测搬家包里是否有团队成员
- README.md 会根据实际情况动态生成

### 自动检测逻辑

#### pack.py（打包脚本）

```python
# Step 2: 收集团队成员信息（可选）
agents = get_agent_info()

# 检测是否有团队成员
has_team = False
if agents:
    for agent in agents:
        if agent.get('id') != 'main':
            has_team = True
            break

if not has_team:
    info("未检测到团队成员，跳过此步骤")
else:
    # 收集团队成员信息...
```

**结果：**
- 有团队成员 → 生成"团队成员层"目录
- 没有团队成员 → 不生成"团队成员层"目录

#### migrate.py（执行脚本）

```python
def copy_team_members(package_dir):
    info("检查是否有团队成员...")
    
    team_dir = package_dir / "团队成员层"
    if not team_dir.exists():
        info("未检测到团队成员，跳过此步骤")
        return True
    
    # 复制团队成员...
```

**结果：**
- 有"团队成员层"目录 → 复制团队成员
- 没有"团队成员层"目录 → 跳过，输出友好提示

### 适用场景

| 场景 | pack.py行为 | migrate.py行为 |
|------|-------------|----------------|
| 有团队的agent | 打包团队成员 | 复制团队成员 |
| 没有团队的agent | 跳过，不打包 | 跳过，不复制 |

---

## 八、验证清单

搬家完成后，逐一检查：

### 基础检查

- [ ] `openclaw gateway status` 显示 running
- [ ] `cat ~/.qclaw/workspace-xxx/SOUL.md | head -20` 显示正确人格
- [ ] `ls ~/.qclaw/workspace-xxx/*/SOUL.md` 显示团队成员文件

### 配置检查

- [ ] openclaw.json 包含所有 agent 配置
- [ ] `agents.defaults.subagents.allowAgents: ["*"]` 已设置
- [ ] 每个 agent 的 workspace 目录存在
- [ ] 每个 workspace 包含 SOUL.md

### 功能检查

- [ ] Gateway 已重启并等待5-10秒
- [ ] 测试 spawn 至少 2 个 agent，确认人格正确
- [ ] Cron 任务已创建（如需要）
- [ ] Skills 已安装（如需要）

---

## 附录：版本变更记录（v2.0）

### v2.0（2026-04-22）

**P0 修复：**
- ✅ pack.py 不再硬编码 workspace-xxx，改为 `detect_active_workspace()` 自动检测
- ✅ migrate.py 新增 `backup_existing()`，搬家前自动备份到 `~/.qclaw/backup/搬家备份_时间戳/`
- ✅ migrate.py 新增 `deep_merge()`，config merge 而非 replace，保护新环境其他配置
- ✅ `prompt_main_agent_handling()` 三个选项逻辑补全（v1.0 选项1/2 只打印警告不执行）

**P1 修复：**
- ✅ 删除了 init.sh/setup_config.py 的"可选执行"误导文档
- ✅ migrate.py 新增 `find_package_dir()`，支持解压后直接 `cd` 进目录运行
- ✅ cron 创建区分"已存在/创建/失败"三类状态

**相关文件：**
- `pack.py` → v2.0，12751 bytes
- `migrate.py` → v2.0，19240 bytes
- `SKILL.md` → v2.0，9768 bytes

