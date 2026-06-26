# Skill Atlas - 详细规范参考

> 这是 SKILL.md 的详细参考文档。核心流程在 SKILL.md 里，这里是补充细节。

---

## 📡 渠道配置

| 渠道 ID | 名称 | URL | 速度 |
|---------|------|-----|------|
| `clawhub-cn` | ClawHub CN | https://mirror-cn.clawhub.com | 最快，国内 |
| `clawhub-global` | ClawHub 全球 | https://clawhub.ai | 国际站 |
| `skillhub` | SkillHub | https://skillhub.tencent.com | 腾讯 |

**渠道选择流程（首次安装）：**

```
1. 用户请求安装技能
2. 查 .skill_manifest.json 是否有 source_channel 记录
   - 有 → 用该渠道，跳过询问
   - 无 → 询问用户选择渠道

3. 预检查技能是否存在（命令格式见下方）
4. 预检查通过 → 记录到 manifest
   预检查失败 → 换渠道重试
```

**渠道选择流程（已有偏好）：**

```
1. 直接用 manifest 中记录的 source_channel
2. 无需询问，除非用户主动说"换个渠道"
```

**为什么先选渠道再安装：**
- 不同渠道的技能版本可能不同
- 有些技能只在特定渠道存在
- 避免安装到一半失败
- 后续更新需要知道原渠道

**配置方式：**
```json
// config/scenes.json
{
  "channels": {
    "preferred": "clawhub-cn"
  }
}
```
preferred 只作为默认提示，不代表强制使用。

**渠道切换策略：**
```
预检查失败时自动换渠道：
clawhub-cn 失败 → clawhub-global → skillhub

换渠道后重新预检查，直到找到技能或全部失败。
```

**📡 各渠道实际命令格式：**

| 渠道 | 搜索 | 预检查 | 安装 | 更新 |
|------|------|--------|------|------|
| **clawhub-cn** | `clawhub search <slug> --channel clawhub-cn` | `clawhub info <slug> --channel clawhub-cn` | `clawhub install <slug> --channel clawhub-cn` | `clawhub update <slug> --channel clawhub-cn` |
| **clawhub-global** | `clawhub search <slug> --channel clawhub-global` | `clawhub info <slug> --channel clawhub-global` | `clawhub install <slug> --channel clawhub-global` | `clawhub update <slug> --channel clawhub-global` |
| **skillhub** | `clawhub search <slug> --channel skillhub` | `clawhub info <slug> --channel skillhub` | `clawhub install <slug> --channel skillhub` | `clawhub update <slug> --channel skillhub` |

**clawhub info 返回格式：**
```json
{
  "slug": "weather-skill",
  "name": "Weather Skill",
  "version": "1.2.0",
  "author": "xxx",
  "description": "...",
  "stars": 520,
  "downloads": 1234,
  "exists": true
}
```

**不存在时返回：**
```json
{
  "error": "skill not found",
  "slug": "weather-skill",
  "exists": false
}
```

**版本比较示例：**
```
已安装版本（来自 manifest）: 1.2.0
远程版本（来自 clawhub info）: 1.3.0

比较结果: 1.3.0 > 1.2.0 → 有更新可用
```

---

## 🚨 安全审查 - RED FLAGS 清单

**发现任一条 → 拒绝安装：**

### 网络相关
- curl/wget 到未知 URL（非知名 API）
- 向非目标服务的外部服务器发送数据
- 硬编码的外部 IP 地址

### 凭证相关
- 请求用户的凭证 / API Key（非用户主动提供）
- 读取 ~/.ssh、~/.aws、~/.config、~/.env
- 访问环境变量中的敏感信息（如 AWS_SECRET_ACCESS_KEY）

### 文件相关
- 读取 MEMORY.md、USER.md、SOUL.md、IDENTITY.md
- 修改 workspace 外的系统文件
- 未经过滤的文件写入（路径穿越风险）
- 删除非技能自身的文件

### 代码相关
- base64 decode / eval() / exec() 外部输入
- 代码压缩/加密/混淆
- 动态导入未声明的模块
- 请求 sudo / 提升权限

### 依赖相关
- 安装 package.json / requirements.txt 之外的包
- 从非官方源安装依赖

---

## 风险等级判定

| 等级 | 条件 | 操作 | 示例 |
|------|------|------|------|
| 🟢 LOW | 无上述风险，仅数据处理/格式化/简单查询 | 直接安装 | 天气、笔记、格式转换 |
| 🟡 MEDIUM | 有文件操作/浏览器/API 调用，但用途明确 | 告知风险，问用户 | 浏览器自动化、文件整理 |
| 🔴 HIGH | 涉及系统修改/凭证访问/外部通信 | 拒绝 | 读取 ~/.ssh、向未知服务器发数据 |
| ⛔ EXTREME | 加密通信/远程代码执行/混淆代码 | 立即拒绝 | base64 混淆、eval 外部输入 |

---

## 审查执行方法

### 读取顺序
```
1. SKILL.md → front matter + description + invoke_scope
2. scripts/ → 入口文件（index.py / main.py / app.py）
3. 如发现可疑模式 → 深入读其他文件
```

### 审查命令示例
```bash
# 检查是否有外部请求
grep -r "curl\|wget\|http://" skills/<slug>/

# 检查是否有 eval/exec
grep -r "eval\|exec" skills/<slug>/

# 检查是否访问敏感目录
grep -r "~/.ssh\|~/.aws\|~/.config" skills/<slug>/
```

### 审查结果记录
```
【技能】<slug>
【来源】<平台>
【安全审查】
  - RED FLAGS: <无 / 具体问题>
  - 风险等级: <等级>
  - 建议: <操作>
```

---

## 💾 备份详细规范

### 单技能备份

**存储位置：** `backups/<slug>/<时间戳>/`

**时间戳格式：** `YYYYMMDD_HHMMSS`

**元数据文件：** `.backups/<slug>.json`

```json
{
  "slug": "weather-skill",
  "backups": [
    {
      "version": "1.2.0",
      "timestamp": "20260410_133000",
      "path": "backups/weather-skill/20260410_133000",
      "created_at": "2026-04-10T13:30:00+08:00"
    },
    {
      "version": "1.1.0",
      "timestamp": "20260408_100000",
      "path": "backups/weather-skill/20260408_100000",
      "created_at": "2026-04-08T10:00:00+08:00"
    }
  ]
}
```

**清理规则：**
- 每个技能最多保留 3 个备份
- 超出时按时间戳排序，删除最旧的
- 删除时同时删除：
  - 备份目录 `backups/<slug>/<旧时间戳>/`
  - 元数据中的对应记录

**备份失败处理：**
```bash
# 备份失败时
1. 不继续安装/更新
2. 告知用户：备份失败，无法继续
3. 建议检查磁盘空间或权限
```

---

### 全量清单备份（manifest）

**存储位置：** `.skill_manifest.json`

```json
{
  "manifest_version": "2.0",
  "updated_at": "2026-04-10T14:47:00+08:00",
  "skills": [
    {
      "slug": "skill-atlas",
      "source": "local",
      "source_channel": null,
      "version": "3.3.0",
      "invoke_scope": "always",
      "layer": "core"
    },
    {
      "slug": "weather-skill",
      "source": "clawhub-global",
      "source_channel": "clawhub-global",
      "version": "1.2.0",
      "invoke_scope": "user-confirmed",
      "layer": "resident"
    },
    {
      "slug": "smart-web-fetch",
      "source": "clawhub-cn",
      "source_channel": "clawhub-cn",
      "version": "1.0.0",
      "invoke_scope": "autonomous",
      "layer": "category"
    }
  ]
}
```

**manifest v2.0 字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `slug` | 是 | 技能唯一标识 |
| `source` | 是 | 安装来源：clawhub / github / local / unknown |
| `source_channel` | 是 | 具体渠道：clawhub-cn / clawhub-global / skillhub / null |
| `version` | 是 | 当前安装版本 |
| `invoke_scope` | 是 | always=核心层，user-confirmed=按需确认，autonomous=自主触发 |
| `layer` | 是 | 当前层级：core / resident / category / paused |

**source_channel 重要性：**
- 更新技能时需要知道原渠道
- 不同渠道的技能版本可能不同
- 避免用错渠道导致更新失败

**layer=paused 的含义：**
- 技能存在但不会被加载
- 用于"暂停使用但不想卸载"的场景
- 用户可随时说"恢复 XXX"重新加载

**如果 source_channel 为空或缺失：**
- 更新时询问用户用哪个渠道
- 或者提示"这个技能的安装渠道未记录，请手动指定"

**维护时机：**
- 安装技能后 → 添加记录（含 invoke_scope、layer）
- 更新技能后 → 更新版本
- 层级调整后 → 更新 layer
- 暂停/恢复后 → 更新 layer（paused/normal）
- 卸载技能后 → 移除记录
- Heartbeat → 每次检查，若当天已更新则跳过

**使用场景：**

| 场景 | 操作 |
|------|------|
| 定期备份 | Heartbeat 时更新 manifest |
| 批量恢复 | 读取 manifest，逐个重装 |
| 迁移环境 | 复制 manifest + skills/ 目录 |
| 检查更新 | 读 manifest 的 source_channel，用对应渠道命令检查 |

**批量恢复流程：**
```
1. 读取 .skill_manifest.json
2. 遍历 skills 数组
3. 使用对应渠道的命令格式安装每个技能
4. 记录成功/失败结果
5. 汇总报告：成功 N 个，失败 N 个
```

**批量更新详细流程：**
```
1. 读取 .skill_manifest.json 获取所有技能
2. 遍历 skills 数组，对每个技能检查是否有更新
3. 列出有更新的技能（core 层默认跳过），问用户确认
4. 用户确认后，逐个执行更新（每个都要备份）
5. 汇总报告：成功 N 个，失败 N 个
```

**core 层更新策略：**
```
- core 层技能默认跳过更新，避免系统管理技能被意外破坏
- 如用户明确要求更新 core 层技能 → 需单独确认
- skill-atlas 自身更新需特别谨慎，建议先备份
```

---

## 📊 版本追踪

### 读取顺序
```
1. .skill_manifest.json 的 skills.<slug>.version（首选）
2. SKILL.md 的 version: 字段（YAML front matter）
3. _meta.json 的 version 字段
4. 都没有 → unknown
```

### version 字段格式
```yaml
---
name: xxx
version: "1.2.3"
---
```

### 版本比较策略（SemVer）

**使用 SemVer 规范：`<major>.<minor>.<patch>`**

比较规则：
```
1. 比较 major，大的更新
2. major 相同比较 minor，大的更新
3. minor 相同比较 patch，大的更新
```

特殊情况处理：
| 输入 | 处理 |
|------|------|
| `v1.0.0` vs `1.0.0` | 去掉 v 前缀后比较 |
| `1.0.0-beta` vs `1.0.0` | 正式版 > 预发布版 |
| `2026.04.10` vs `1.0.0` | 转为 semver 格式或字符串比较 |
| `abc` vs `1.0.0` | 字符串比较 |

**实现函数（Python）：**
```python
from packaging import version

def compare_versions(installed: str, remote: str) -> str:
    """比较版本，返回 'update_available' | 'same' | 'older'"""
    installed = installed.lstrip('v')
    remote = remote.lstrip('v')
    
    try:
        if version.parse(remote) > version.parse(installed):
            return 'update_available'
        elif version.parse(remote) < version.parse(installed):
            return 'older'
        else:
            return 'same'
    except:
        # 回退到字符串比较
        if installed != remote:
            return 'update_available'
        return 'same'
```

**版本比较示例：**
```
已安装版本（来自 manifest）: 1.2.0
远程版本（来自 clawhub info）: 1.3.0

比较结果: 1.3.0 > 1.2.0 → 有更新可用
```

---

## 🔄 技能升降级规则

### 使用次数记录

**统计时机：** 每次对话结束时，Agent 更新 scenes.json 中的 use_count。

**调用定义：** 只有技能实际被加载执行才算调用一次。用户只是提及技能不算。

**周期定义：** 日历周（周一 00:00 到周日 23:59）。

存储位置：`config/scenes.json`

```json
{
  "skills": {
    "weather-skill": {
      "layer": "resident",
      "use_count": 12,
      "last_used": "2026-04-10",
      "installed_at": "2026-04-01"
    }
  }
}
```

### 升降级触发

| 触发条件 | 自动操作 | 告知用户 |
|----------|----------|----------|
| 分类层使用 ≥ 5 次/周 | 标记「可升级」 | 下次对话时询问 |
| 分类层使用 ≥ 10 次/周 | 自动升为常驻 | ✅ 告知 |
| 常驻层 7 天未用 | 标记「可降级」 | 下次对话时询问 |
| 用户主动调整 | 按用户意愿 | ✅ 确认 |

### 升降级操作
```bash
# 升级到常驻层
修改 .skill_manifest.json：skills.<slug>.layer = "resident"

# 降级到分类层
修改 .skill_manifest.json：skills.<slug>.layer = "category"

# 暂停加载
修改 .skill_manifest.json：skills.<slug>.layer = "paused"

# 恢复加载
修改 .skill_manifest.json：skills.<slug>.layer = "category" 或 "resident"
```

**注意：** manifest 是唯一数据源，所有层级操作都改 manifest，不再依赖 config/scenes.json 的 layer 字段。

---

## 🔍 技能审视详细规范

### 审视类型

| 类型 | 触发时机 | 检查内容 | 耗时 |
|------|----------|----------|------|
| 存在性检查 | Heartbeat | 目录是否存在 | 秒级 |
| 深度审视 | 用户要求/安装后 | 全维度检查 | 分钟级 |

### 审视维度详解

**1. 基础状态**
```
- skills/<slug>/ 目录存在？
- SKILL.md 存在？
- 版本号可读？
- 核心脚本存在？
```

**2. 触发条件**
```
- manifest 里 invoke_scope 是否合理？
  - always → 应在核心层
  - user-confirmed → 应有使用场景说明
  - autonomous → 应有触发条件说明
```

**3. 功能匹配**
```
- 技能解决什么问题？
- 用户是否有这个需求？
- 从对话历史推断需求匹配度
```

**4. 使用频率**
```
- 读取 use_count 和 last_used
- 7 天未用 → 可能不需要
- 30 天未用 → 建议降级或卸载
```

**5. 更新状态**
```
- clawhub info <slug>
- 对比版本号
- 有新版本 → 标记可更新
```

### 审视报告模板

**简洁版（默认）：**
```
XXX 技能：✅ 正常，[触发场景]
XXX 技能：⚠️ 7天未使用
XXX 技能：🔄 有新版本 v1.1
```

**详细版（用户要求）：**
```
🔍 技能审视报告
═══════════════════════════════════════
共 N 个技能 · 核心 N 个 · 常驻 N 个 · 分类 N 个
───────────────────────────────────────
✅ 正常（N 个）
  • skill-a · v1.0 · 核心
    触发：用户说"管理技能"

⚠️ 注意（N 个）
  • skill-c · v1.0 · 常驻
    14 天未使用，考虑降级

🔴 问题（N 个）
  • skill-d · v1.0 · 分类
    缺少 API Key

🔄 可更新（N 个）
  • skill-e · v1.0 → v1.1
───────────────────────────────────────
📌 建议
  • skill-c：询问用户是否降级
  • skill-d：设置 API Key 或卸载
═══════════════════════════════════════
```

---

## 📋 待办事项管理

### 存储位置
`workspace/.pending_actions.json`

### 格式
```json
{
  "pending": [
    {
      "id": "001",
      "action": "update",
      "slug": "skill-e",
      "reason": "有新版本 v1.1",
      "created_at": "2026-04-10T08:00:00+08:00",
      "source": "heartbeat"
    }
  ]
}
```

### 操作流程
```
1. Heartbeat 发现问题 → 添加到 pending
2. 用户下次对话时 → 优先提醒待办
3. 用户确认后 → 执行操作，从 pending 移除
```

---

## 🆕 首次加载详细流程

### 触发条件
- 新安装 skill-atlas
- 新环境/清空后的 workspace
- .skill_manifest.json 不存在

### 执行步骤
```
1. 扫描 skills/ 目录
   ls skills/

2. 对每个发现的技能：
   - 读取 SKILL.md 获取版本和 invoke_scope
   - 根据 invoke_scope 初步判断层级
   - 检查基础状态

3. 生成 .skill_manifest.json（含 invoke_scope、layer、source_channel）

4. 告知用户：
   发现 N 个已安装技能，已生成清单
```

### 层级推断逻辑
```
invoke_scope: always → 核心层
用户主动安装记录存在 → 常驻层
其他 → 分类层
```

**注意：** 首次加载后 manifest 即为唯一数据源，不再依赖 scenes.json 的 layer 字段。

---

## 🛠️ 常见问题处理

### 安装后找不到技能
```
可能原因：
1. 渠道问题，文件未完整下载
2. 安装目录不正确

解决方法：
1. 换渠道重装
2. 检查 skills/ 目录权限
```

### 更新后行为异常
```
解决方法：
1. 回滚到上一版本
2. 报告问题到 ClawHub issue
3. 等修复后再更新
```

### 不知道技能在哪一层
```
查询方法：
读取 .skill_manifest.json 的 skills.<slug>.layer
```

### 备份占用太多空间
```
解决方法：
1. 检查 backups/ 目录大小
2. 手动删除旧备份
3. 调整备份保留数量（默认 3 个）
```

---

## 📌 批量操作规范

### 批量恢复
```
1. 显示进度：正在恢复 1/10...
2. 单个失败 → 记录错误，继续下一个
3. 完成后汇总：
   ✅ 成功：N 个
   ❌ 失败：N 个
   失败列表：[slug1, slug2, ...]
```

### 批量更新
```
1. 先检查哪些有更新（core 层默认跳过）
2. 列出有更新的技能，问用户确认
3. 用户确认后逐个更新（每个都要备份）
4. 完成后汇总报告
```

**注意：** core 层技能默认跳过更新。详见上方「core 层更新策略」。

---

_Last updated: 2026-04-10 v3.0.0_
