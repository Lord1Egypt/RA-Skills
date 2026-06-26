---
name: smarter-task-planner
displayName: 更好的任务规划 (Smarter Task Planner)
description: |
  【Smarter Task Planner】自动创建时间戳任务文件夹，支持步骤规划、检查点保存、中断恢复与进度追踪，确保任务可追溯、可恢复。适用于分析、调研、信息提取、文档生成等需要结构化步骤的任务场景。
metadata:
  openclaw:
    triggers:
      # 核心步骤规划
      - 任务步骤规划
      - 规划任务步骤
      - 步骤规划
      - 结构化执行
      - 自动任务结构
      
      # 任务管理
      - 安排任务
      - 计划任务
      - 创建任务
      - 开始任务
      - 执行任务
      - 任务规划
      - 管理项目
      - 项目执行
      - 任务管理
      
      # 工作组织
      - 组织工作
      - 工作流程
      - 整理工作空间
      - 任务文件夹
      
      # 进度恢复
      - 恢复任务
      - 恢复上次任务
      - 保存进度
      - 任务进度保存
      - 任务中断恢复
      - 检查点
      - 工作追踪
      - 上次做到哪了
      
      # 分析调研
      - 分析任务
      - 进行分析
      - 调研任务
      - 进行调研
      
      # 信息提取
      - 提取信息
      - 提取数据
      
      # 文档生成
      - 生成文档
      - 生成报告
      - 撰写报告
      - 分析并生成报告
      - 调研并提取信息
---

# 更好的任务规划 (Smarter Task Planner)

**更高效的结构化任务执行与步骤规划**。自动创建 `YYYY-MM-DD_描述/01_步骤/` 文件夹结构，支持步骤规划、检查点保存、中断恢复与进度追踪。适用于分析、调研、信息提取、文档生成等多种任务场景，确保任务可规划、可追踪、可恢复。

## 核心规则

### 1. 路径基准
- **工作空间根目录** = `.openclaw\workspace\`
- **正确示例**: `output/2026-03-19_任务/`
- **验证位置**: `pwd` 应显示工作空间根目录

### 2. 检查点记忆保存
创建任务目录后立即保存检查点：
```powershell
# Python可用时（推荐）
py scripts/safe-writer.py "开始任务: [描述]" --task-id "YYYY-MM-DD_描述" --step "01_开始"

# Python不可用时（备用方案）
# 如果需要PowerShell版本，将 safe-writer-ps1.txt 重命名为 safe-writer.ps1
# powershell scripts/safe-writer.ps1 "开始任务: [描述]" --task-id "YYYY-MM-DD_描述" --step "01_开始"
```

### 3. 规划-执行流程
1. **完整规划**：明确所有步骤（01_步骤名、02_步骤名...）
2. **创建结构**：`output/YYYY-MM-DD_描述/01_步骤/`
3. **保存检查点**：立即执行检查点写入命令
4. **顺序执行**：按步骤目录顺序工作，每阶段保存进展

## AI工作流程

### 开始新任务
1. **规划步骤**：分析任务，确定3-5个主要阶段
2. **验证位置**：确保在工作空间根目录
3. **创建目录**：`output/YYYY-MM-DD_描述/` 及所有步骤子目录
4. **保存记忆**：运行检查点写入命令记录任务开始
5. **执行工作**：按步骤顺序进行，每个步骤强制输出内容文档，禁止写入空文件，定期保存进展

### 恢复任务
- 说"**恢复上次任务**"或运行 `task-memory-manager.py recovery`
- 系统显示未完成任务列表供选择

## 核心脚本
- `safe-writer.py` - Python版记忆写入（原子操作+双写保证，推荐使用）
- `task-memory-manager.py` - 任务扫描与恢复管理
- `task-recovery-check.py` - 自动检查未完成任务（Python版本）

## 备用脚本（如需PowerShell版本）
- `safe-writer-ps1.txt` - PowerShell备用版本（重命名为 .ps1 使用）
- `task-recovery-check-ps1.txt` - PowerShell包装器（重命名为 .ps1 使用）
- `workspace-commands-ps1.txt` - PowerShell快捷命令（重命名为 .ps1 使用）

## 环境检测
系统优先使用Python版本：
- **Python可用** → 使用 `safe-writer.py`（功能完整，推荐）
- **Python不可用** → 可将 `safe-writer-ps1.txt` 重命名为 `safe-writer.ps1` 使用（基础功能）

## 快速检查
```powershell
# 验证当前位置
pwd

# 如有嵌套错误
cd ..
```

## Heartbeat 自动检查
技能包含自动任务恢复检查功能：

1. **配置方法**：查看 `templates/HEARTBEAT-guide.md` 文件
2. **执行频率**：每2-4小时自动检查未完成任务
3. **行为**：
   - 发现未完成任务 → 提醒用户恢复
   - 无未完成任务 → 静默通过
4. **手动检查**：`py scripts/task-recovery-check.py notify`

## 关键命令速查
- `safe-writer.py <内容> --task-id <ID> --step <步骤>` - 保存记忆
- `task-memory-manager.py recovery` - 恢复界面
- `task-memory-manager.py scan` - 扫描任务
- `task-recovery-check.py notify` - 心跳检查（Python版本）