# project-triple-sync - 项目三线同步技能

_版本：V3.0 | 创建时间：2026-03-08 | 状态：已上线（项目 worklog 分级管理 + 自动汇总）_

---

## 📋 技能描述

当用户说"项目三线同步"时，自动同步更新项目的三个载体 + Worklog（分级管理 + 自动汇总）：

1. **MD 文件**：`tasks/projects/项目名.md`（项目卡片，主数据源）
2. **TXT 文件**：`atomic-actions/项目名.txt`（简要说明）
3. **飞书文档**：立项报告（展示层，从 MD 同步增量信息）
4. **Worklog 分级管理**：
   - **项目专属日报**：`worklog/daily/项目专属/日期 - 项目名 worklog.md`
   - **项目专属周报**：`worklog/weekly/项目专属/周数 - 项目名 worklog.txt`
   - **Master 日报**：`worklog/daily/日期 -1 worklog.md`（汇总所有项目）
   - **Master 周报**：`worklog/weekly/周数-worklog.txt`（汇总所有项目）

**原则**：MD 为主，飞书为展示层，Worklog 分级管理（项目独立 + Master 汇总）

**核心机制**：
- 项目增量信息自动更新到飞书立项报告
- 项目 worklog 独立存储（便于单独查看）
- 自动汇总到 Master worklog（含项目索引链接）

---

## 🎯 触发词

- "项目三线同步"
- "三线同步"
- "同步项目知识"
- "更新立项报告"
- "更新项目 worklog"
- "[项目名] + 三线同步"

---

## 🔄 工作流程（V3.0）

### **Step 1: 读取 MD 文件**
```powershell
# 读取项目卡片
$mdContent = Get-Content "tasks/projects/项目名.md" -Encoding UTF8

# 提取项目知识库章节（增量信息）
$knowledgeSection = Extract-KnowledgeSection $mdContent

# 提取今日新增内容（根据时间戳）
$todayContent = Extract-TodayContent $mdContent "2026-03-08"
```

### **Step 2: 读取 TXT 文件**
```powershell
# 读取简要说明
$txtContent = Get-Content "atomic-actions/项目名.txt" -Encoding UTF8
```

### **Step 3: 对比变更**
```powershell
# 对比飞书文档当前内容
$feishuContent = Get-FeishuDoc $docId

# 识别增量内容
$delta = Compare-Content $feishuContent $knowledgeSection
```

### **Step 4: 更新飞书文档（增量信息同步）**
```powershell
# 发送更新前通知
Send-Message "🔄 开始更新 [项目名] 立项报告..."

# 对比飞书文档当前内容
$feishuContent = Get-FeishuDoc $docId

# 识别增量内容（MD 文件中的项目知识库章节）
$knowledgeSection = Extract-KnowledgeSection $mdContent

# 提取今日新增内容（带时间戳的条目）
$todayContent = Extract-TodayContent $knowledgeSection "2026-03-08"

# 对比飞书文档，找出未同步的增量信息
$delta = Compare-Content $feishuContent $todayContent

if ($delta) {
    # 更新飞书文档（追加模式，不覆盖原有内容）
    # 将增量信息追加到"项目知识库"章节
    Update-FeishuDoc $docId $delta -AppendMode
    
    # 更新版本号和时间戳
    $version = Get-NextVersion
    Update-Metadata $version
    
    # 发送更新后通知
    Send-Message "✅ [项目名] 立项报告已更新（V$version）"
    Send-Message "📝 新增内容：$delta"
} else {
    # 无增量内容
    Send-Message "ℹ️ [项目名] 立项报告无新增内容"
}
```

### **Step 5: 创建项目专属文件夹**
```powershell
# 创建项目 worklog 文件夹（日报）
$projectDailyDir = "worklog/daily/项目专属"
New-Item -ItemType Directory -Path $projectDailyDir -Force

# 创建项目 worklog 文件夹（周报）
$projectWeeklyDir = "worklog/weekly/项目专属"
New-Item -ItemType Directory -Path $projectWeeklyDir -Force
```

### **Step 6: 创建/更新项目专属日报**
```powershell
# 生成文件名
$date = Get-Date -Format "yyyy-MM-dd (ddd)"
$projectDailyPath = "$projectDailyDir/$date - 项目名 worklog.md"

# 提取今日项目进展（从 MD 文件）
$projectUpdate = Extract-ProjectUpdate $mdContent "2026-03-08"

# 写入项目专属日报
$content = @"
# 项目名 - Worklog

**日期：** $date  
**项目：** [[../../tasks/projects/项目名.md]]  
**同步次数：** 今日第 1 次

---

## 📋 今日进展

$projectUpdate

---

## 📊 产出统计
- 新建文件：X 个
- 更新文件：Y 个
- 代码行数：~Z 行

---

_创建时间：$(Get-Date -Format "yyyy-MM-dd HH:mm")_
"@

$content | Out-File -FilePath $projectDailyPath -Encoding UTF8
```

### **Step 7: 汇总到 Master 日报**
```powershell
# Master 日报路径
$masterDailyPath = "worklog/daily/$date -1 worklog.md"

if (Test-Path $masterDailyPath) {
    # 读取 Master 日报
    $masterContent = Get-Content $masterDailyPath -Encoding UTF8
    
    # 检查是否已有该项目索引
    if ($masterContent -notlike "*项目名*") {
        # 提取项目摘要（标题 + 关键进展 + 产出统计）
        $projectSummary = Get-ProjectSummary $projectDailyPath
        
        # 生成项目索引条目
        $indexEntry = @"

### 项目名
- **项目 worklog：** [[worklog/daily/项目专属/$date - 项目名 worklog.md]]
- **核心进展：** $projectSummary
- **产出：** X 个文件

"@
        
        # 找到"## 📁 项目 worklog 索引"章节，追加条目
        $masterContent = $masterContent -replace "(## 📁 项目 worklog 索引)", "`$1$indexEntry"
        
        # 保存 Master 日报
        $masterContent | Out-File -FilePath $masterDailyPath -Encoding UTF8
    }
} else {
    # 创建 Master 日报
    $newContent = @"
# $date 工作日志

**日期：** $date  
**项目数：** 1  
**总同步次数：** 1 次

---

## 📁 项目 worklog 索引

### 项目名
- **项目 worklog：** [[worklog/daily/项目专属/$date - 项目名 worklog.md]]
- **核心进展：** 进展摘要
- **产出：** X 个文件

---

## 📊 全局统计
- 完成任务：X 项
- 技能升级：Y 个
- 项目立项：Z 个

---

_最后更新：$(Get-Date -Format "yyyy-MM-dd HH:mm")_
"@
    $newContent | Out-File -FilePath $masterDailyPath -Encoding UTF8
}
```

### **Step 8: 创建/更新项目专属周报**
```powershell
# 获取当前周数（周四→周三为一周）
$weekNum = Get-WeekNumber  # 返回 2026w11 格式
$projectWeeklyPath = "$projectWeeklyDir/$weekNum-项目名 worklog.txt"

# 提取本周项目进展
$weeklyUpdate = Extract-WeeklyUpdate $mdContent $weekNum

# 写入项目专属周报（追加模式）
if (Test-Path $projectWeeklyPath) {
    # 追加内容
    Add-Content -Path $projectWeeklyPath -Value "`n## $(Get-Date -Format "yyyy-MM-dd (ddd)")`n$weeklyUpdate" -Encoding UTF8
} else {
    # 创建新周报
    $weeklyContent = @"
# 项目名 - 周报

**周期：** $weekNum
**项目状态：** 进行中

---

## $(Get-Date -Format "yyyy-MM-dd (ddd)")

$weeklyUpdate

---

_创建时间：$(Get-Date -Format "yyyy-MM-dd HH:mm")_
"@
    $weeklyContent | Out-File -FilePath $projectWeeklyPath -Encoding UTF8
}
```

### **Step 9: 汇总到 Master 周报**
```powershell
# Master 周报路径
$masterWeeklyPath = "worklog/weekly/$weekNum-worklog.txt"

# 获取周数范围
$weekStart = Get-WeekStart $weekNum  # 返回周四日期
$weekEnd = Get-WeekEnd $weekNum      # 返回下周三日期

if (Test-Path $masterWeeklyPath) {
    # 读取 Master 周报
    $masterContent = Get-Content $masterWeeklyPath -Encoding UTF8
    
    # 检查是否已有该项目
    if ($masterContent -notlike "*项目名*") {
        # 提取项目周报摘要
        $projectSummary = Get-ProjectWeeklySummary $projectWeeklyPath
        
        # 生成项目索引条目
        $indexEntry = @"

### 项目名（$weekStart ~ $weekEnd）
- **项目周报：** [[worklog/weekly/项目专属/$weekNum-项目名 worklog.txt]]
- **核心进展：** $projectSummary

"@
        
        # 找到"## 项目汇总"章节，追加条目
        $masterContent = $masterContent -replace "(## 项目汇总)", "`$1$indexEntry"
        
        # 保存 Master 周报
        $masterContent | Out-File -FilePath $masterWeeklyPath -Encoding UTF8
    }
} else {
    # 创建 Master 周报
    $masterWeeklyContent = @"
# $weekNum 工作周报

**周期：** $weekStart (周四) ~ $weekEnd (下周三)
**总项目数：** 1

---

## 项目汇总

### 项目名（$weekStart ~ $weekEnd）
- **项目周报：** [[worklog/weekly/项目专属/$weekNum-项目名 worklog.txt]]
- **核心进展：** 进展摘要

---

_创建时间：$(Get-Date -Format "yyyy-MM-dd HH:mm")_
"@
    $masterWeeklyContent | Out-File -FilePath $masterWeeklyPath -Encoding UTF8
}
```

### **Step 10: 发送飞书通知**
```powershell
# 发送同步完成通知
Send-Message @"
✅ **项目三线同步完成！**（项目名）

**同步内容：**
- ✅ MD 文件：已读取
- ✅ 飞书文档：已更新（V$version）
- ✅ 项目日报：已创建（worklog/daily/项目专属/）
- ✅ Master 日报：已汇总（含项目索引）
- ✅ 项目周报：已创建（worklog/weekly/项目专属/）
- ✅ Master 周报：已汇总（含项目索引）

**文件链接：**
- 项目 worklog：[[worklog/daily/项目专属/日期 - 项目名 worklog.md]]
- Master worklog：[[worklog/daily/日期 -1 worklog.md]]
"@
```

---

## 📁 文件结构（V3.0）

```
workspace/
├── tasks/projects/                    # MD 项目卡片
│   ├── 万物卡片化/
│   │   └── PROJECT.md
│   ├── 数据治理 - 小米汽车.md
│   └── ...
├── atomic-actions/                    # TXT 简要说明
│   ├── 万物卡片化.txt
│   └── ...
├── worklog/
│   ├── daily/                         # 每日总 worklog（Master）
│   │   ├── 项目专属/                  # 项目专属日报目录
│   │   │   ├── 2026-03-08 (周日) - 万物卡片化 worklog.md
│   │   │   ├── 2026-03-08 (周日) - 玩家系统 worklog.md
│   │   │   └── ...
│   │   └── 2026-03-08 (周日) -1 worklog.md  # Master（汇总所有项目）
│   └── weekly/                        # 每周总 worklog（Master）
│       ├── 项目专属/                  # 项目专属周报目录
│       │   ├── 2026w11-万物卡片化 worklog.txt
│       │   ├── 2026w11-玩家系统 worklog.txt
│       │   └── ...
│       └── 2026w11-worklog.txt        # Master（汇总所有项目）
└── feishu-docs/
    └── project-links.md               # 飞书文档映射表
```

---

## 🗺️ 飞书文档映射表

| 项目名称 | 飞书文档 ID | 飞书链接 |
|----------|------------|---------|
| 数据治理 - 小米汽车 | I49YdfIQ8omBxBxtW3Mc3PAWnBc | https://feishu.cn/docx/I49YdfIQ8omBxBxtW3Mc3PAWnBc |
| 豆包会话自动化 | NTWmdppaWoxzpwxIjpQcZPiFn9f | https://feishu.cn/docx/NTWmdppaWoxzpwxIjpQcZPiFn9f |
| 地理知识库 | NyVtdMB1NomyooxHnoTcHKw5nRh | https://feishu.cn/docx/NyVtdMB1NomyooxHnoTcHKw5nRh |
| 周报系统 | CEoRdPxG2oiwlzxg9i9c9M1sngf | https://feishu.cn/docx/CEoRdPxG2oiwlzxg9i9c9M1sngf |
| 感知与行动中心 | TNIVdysYHoJ0tex1wTMc5yE8nAc | https://feishu.cn/docx/TNIVdysYHoJ0tex1wTMc5yE8nAc |
| 万物卡片化 | AaC9dkA8QoAmAKx3hQqcLqFznRf | https://feishu.cn/docx/AaC9dkA8QoAmAKx3hQqcLqFznRf |

---

## ⚙️ 配置项

### **更新策略**
- **模式**：追加模式（不覆盖原有内容）
- **频率**：用户手动触发
- **通知**：更新前 + 更新后各一条消息
- **Worklog**：项目专属 + Master 双层汇总

### **版本管理**
- **格式**：V{主版本}.{次版本}
- **升级规则**：每次三线同步升级次版本
- **记录位置**：飞书文档底部版本记录表

### **冲突处理**
- **原则**：MD 为主，飞书为展示层
- **策略**：飞书内容始终从 MD 同步
- **Worklog**：项目独立存储，Master 汇总索引

### **Worklog 命名规则**
| 类型 | 命名格式 | 示例 |
|------|----------|------|
| **项目日报** | `YYYY-MM-DD (周 X) - 项目名 worklog.md` | 2026-03-08 (周日) - 万物卡片化 worklog.md |
| **Master 日报** | `YYYY-MM-DD (周 X) -N worklog.md` | 2026-03-08 (周日) -1 worklog.md |
| **项目周报** | `YYYYwXX-项目名 worklog.txt` | 2026w11-万物卡片化 worklog.txt |
| **Master 周报** | `YYYYwXX-worklog.txt` | 2026w11-worklog.txt |

### **周数计算规则**
- **周期**：周四 → 下周三（小米自然周）
- **周数格式**：2026w11（年 +w+ 周数）
- **跨年处理**：1 月 1 日可能属于上一年的最后一周

---

## 🧪 测试用例

### **测试 1：单项目同步（V3.0 新机制）**
```
触发：项目三线同步 [万物卡片化]
预期：
  - 读取 tasks/projects/万物卡片化/PROJECT.md
  - 更新飞书文档 AaC9dkA8QoAmAKx3hQqcLqFznRf（V1.3 → V1.4）
  - 创建项目专属日报：worklog/daily/项目专属/2026-03-08 (周日) - 万物卡片化 worklog.md
  - 汇总到 Master 日报：worklog/daily/2026-03-08 (周日) -1 worklog.md（含项目索引链接）
  - 创建项目专属周报：worklog/weekly/项目专属/2026w11-万物卡片化 worklog.txt
  - 汇总到 Master 周报：worklog/weekly/2026w11-worklog.txt（含项目索引链接）
  - 发送更新通知（含文件链接）
```

### **测试 2：全项目同步**
```
触发：所有项目三线同步
预期：
  - 遍历 6 个项目
  - 逐个更新飞书文档
  - 为每个项目创建项目专属日报 + 周报
  - 汇总到 Master 日报 + Master 周报（每个项目都有索引）
  - 每个项目发送更新通知
```

### **测试 3：同周第二次同步**
```
触发：项目三线同步 [万物卡片化]（同周内第二次）
预期：
  - 检测到项目周报已存在（2026w11-万物卡片化 worklog.txt）
  - 追加今日内容到周报（不覆盖）
  - Master 周报中已有项目索引，跳过
  - 项目日报：创建新文件（日期不同）
  - Master 日报：追加项目索引（如日期相同则更新）
```

---

## 📊 监控指标

- **同步成功率**：目标 100%
- **平均同步时间**：<120 秒/项目（含项目 worklog + Master 汇总）
- **Worklog 创建率**：目标 100%（项目专属 + Master）
- **用户满意度**：待收集

---

## 🚀 使用说明

### **单项目同步**
```
项目三线同步 [数据治理]
```

### **全项目同步**
```
所有项目三线同步
```

### **查看同步状态**
```
项目同步状态
```

### **查看项目专属 worklog**
```
查看 [项目名] worklog
```

### **查看 Master worklog**
```
查看今日 worklog
查看本周 worklog
```

---

## 📝 版本记录

| 版本号 | 修改时间 | 修改内容 | 修改人 |
|--------|----------|----------|--------|
| V3.0 | 2026-03-08 22:45 | 项目 worklog 分级管理（项目专属 + Master 汇总） | 阿福 |
| V2.2 | 2026-03-08 18:55 | 新增周报同步机制（项目周报 + 每周总周报） | 阿福 |
| V2.1 | 2026-03-08 18:22 | 明确增量信息同步机制 | 阿福 |
| V2.0 | 2026-03-08 18:05 | 新增 Worklog 同步机制（日报） | 阿福 |
| V1.1 | 2026-03-08 16:10 | 三线同步，更新项目知识库 | 阿福 |
| V1.0 | 2026-03-08 16:00 | 初始版本 | 阿福 |

---

_本技能由阿福开发，遵循三线同步原则（MD+TXT+ 飞书 +Worklog 分级管理）_
