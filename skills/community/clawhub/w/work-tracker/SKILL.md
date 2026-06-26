---
name: worktracker
displayName: WorkTracker
description: 简单快速的工作日志系统，专为AI助手团队设计。解决助手忘记报告工作进展的问题，确保所有工作都有记录、可追踪、可报告。
author: iSenlink
version: 1.0.0
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["python3"]}}}
user-invocable: true
tags: ["productivity", "team-collaboration", "work-log", "ai-assistant"]
---

# WorkTracker - 简单快速的工作日志系统

## 🎯 技能概述

WorkTracker是一个专为AI助手团队设计的简单工作日志系统，解决助手忘记报告工作进展的问题，确保所有工作都有记录、可追踪、可报告。

### 核心价值
- **解决实际问题**：助手经常忘记报告工作进展
- **提高透明度**：随时查看助手工作状态
- **建立工作纪律**：强制的工作记录习惯
- **便于管理**：集中查看团队工作进展

## 🚀 快速开始

### 安装后自动可用
技能安装后，以下命令立即生效：

```bash
# 开始工作
worktracker start "助手名" "工作描述" "截止时间"

# 更新进展
worktracker update "助手名" 进度百分比 "更新内容"

# 完成工作
worktracker complete "助手名" "完成结果" "后续事项"

# 查看状态
worktracker status

# 查看详细日志
worktracker log
```

### 环境变量配置
```bash
# 工作日志文件路径（可选）
export WORK_LOG_PATH="/path/to/work_log.md"

# 工作状态文件路径（可选）
export WORK_STATUS_PATH="/path/to/work_status.json"
```

## 📋 核心功能

### 1. 工作流程管理
```
开始工作 → 记录开始 → 定期更新 → 完成工作 → 记录完成 → 报告结果
```

### 2. 强制工作要求
1. **必须记录**：所有超过10分钟的工作必须记录
2. **必须更新**：每30分钟至少更新一次进展
3. **必须报告**：完成工作后必须报告结果
4. **必须确认**：重要工作完成后必须向管理员确认

### 3. 状态跟踪
- 实时查看各助手工作状态
- 工作进度百分比显示
- 最后更新时间跟踪
- 工作历史记录

## 🔧 技术架构

### 数据存储
- **工作状态**：JSON格式，实时更新
- **工作日志**：Markdown格式，便于阅读
- **备份机制**：自动备份历史记录

### 文件结构
```
.worktracker/
├── work_status.json      # 当前工作状态
├── work_log.md          # 工作日志记录
└── backups/             # 历史备份
    ├── work_status_20260314.json
    └── work_log_20260314.md
```

### 支持的助手
默认支持以下助手，可扩展：
- 小新（总协调助手）
- 小雅（市场助手）
- 小锐（销售助手）
- 小暖（服务助手）

## 📝 使用示例

### 示例1：开始新工作
```bash
# 小新开始修复宝塔面板问题
worktracker start "小新" "修复宝塔面板SSL证书问题" "今天14:00前完成"

# 输出：✅ 小新已开始工作：修复宝塔面板SSL证书问题（截止：今天14:00前完成）
```

### 示例2：更新工作进展
```bash
# 小新更新工作进展到50%
worktracker update "小新" 50 "已找到证书配置问题，正在重新生成证书"

# 输出：✅ 小新工作进展更新：50% - 已找到证书配置问题，正在重新生成证书
```

### 示例3：完成工作
```bash
# 小新完成工作
worktracker complete "小新" "成功修复SSL证书，宝塔面板可正常访问" "需要测试其他功能是否正常"

# 输出：✅ 小新工作完成：成功修复SSL证书，宝塔面板可正常访问（后续：需要测试其他功能是否正常）
```

### 示例4：查看团队状态
```bash
# 查看所有助手工作状态
worktracker status

# 输出：
# 📋 工作状态报告（2026-03-14 01:45）
# ┌──────┬────────────────────────────┬────────┬────────────┬─────────────┐
# │ 助手 │ 当前工作                  │ 进度   │ 开始时间   │ 最后更新    │
# ├──────┼────────────────────────────┼────────┼────────────┼─────────────┤
# │ 小新 │ 修复宝塔面板SSL证书问题   │ 100%   │ 01:40      │ 01:45       │
# │ 小雅 │ 市场分析报告撰写          │ 30%    │ 01:30      │ 01:35       │
# │ 小锐 │ 销售数据整理              │ 0%     │ -          │ -           │
# │ 小暖 │ 客户问题处理              │ 0%     │ -          │ -           │
# └──────┴────────────────────────────┴────────┴────────────┴─────────────┘
```

## ⚙️ 高级功能

### 1. 自定义助手配置
```bash
# 添加新助手
worktracker config add-assistant "新助手名" "角色描述"

# 移除助手
worktracker config remove-assistant "助手名"

# 查看配置
worktracker config show
```

### 2. 数据导出
```bash
# 导出工作日志为CSV
worktracker export csv --output work_log.csv

# 导出工作状态为JSON
worktracker export json --output work_status.json

# 导出今日工作报告
worktracker export daily --date 2026-03-14
```

### 3. 数据清理
```bash
# 清理30天前的日志
worktracker clean --days 30

# 备份当前数据
worktracker backup

# 恢复备份
worktracker restore --date 2026-03-13
```

## 🔒 安全与权限

### 数据安全
- 所有数据本地存储
- 支持加密备份
- 访问日志记录

### 权限控制
- 只读权限：查看工作状态
- 写入权限：更新工作进展
- 管理权限：配置系统

### 审计日志
所有操作都会记录审计日志：
- 操作时间
- 操作人员
- 操作内容
- IP地址（如果可用）

## 📊 性能指标

### 系统要求
- **Python版本**：3.8+
- **内存需求**：<10MB
- **存储需求**：<100MB（包含历史记录）
- **网络需求**：无（纯本地运行）

### 性能表现
- **启动时间**：<100ms
- **查询响应**：<50ms
- **数据更新**：<100ms
- **日志写入**：<50ms

## 🛠️ 故障排除

### 常见问题

#### 问题1：命令找不到
```bash
# 确保技能已正确安装
openclaw skills list | grep worktracker

# 如果未找到，重新安装
skillhub install worktracker
```

#### 问题2：权限错误
```bash
# 检查文件权限
ls -la ~/.openclaw/workspace/.worktracker/

# 修复权限
chmod 755 ~/.openclaw/workspace/.worktracker/
chmod 644 ~/.openclaw/workspace/.worktracker/*.json
chmod 644 ~/.openclaw/workspace/.worktracker/*.md
```

#### 问题3：数据损坏
```bash
# 从备份恢复
worktracker restore --latest

# 或手动修复
worktracker repair
```

### 错误代码
| 代码 | 含义 | 解决方案 |
|------|------|----------|
| ERR-001 | 助手不存在 | 使用`worktracker config add-assistant`添加助手 |
| ERR-002 | 工作已存在 | 先完成或取消当前工作 |
| ERR-003 | 进度无效 | 进度必须在0-100之间 |
| ERR-004 | 文件权限错误 | 检查文件权限和所有权 |
| ERR-005 | 数据格式错误 | 使用`worktracker repair`修复 |

## 🔄 更新与维护

### 版本历史
- **v1.0.0** (2026-03-14)：初始版本发布
  - 基本工作跟踪功能
  - 四助手团队支持
  - 工作日志记录
  - 状态查看功能

### 更新计划
- **v1.1.0**：添加Web界面
- **v1.2.0**：添加API接口
- **v1.3.0**：添加数据分析功能

### 维护承诺
- **安全更新**：发现漏洞24小时内修复
- **功能更新**：每月发布小版本更新
- **兼容性**：保持向后兼容至少2个主要版本

## 📞 支持与反馈

### 技术支持
- **文档**：本SKILL.md文件
- **示例**：examples/目录中的示例
- **问题反馈**：GitHub Issues

### 社区支持
- **讨论区**：OpenClaw社区论坛
- **用户群**：飞书工作群
- **邮件支持**：support@isenlink.com

### 贡献指南
欢迎贡献代码：
1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 通过代码审查

## 📄 许可证

### 开源许可证
WorkTracker采用**MIT许可证**发布。

### 商业使用
- ✅ 允许个人和商业使用
- ✅ 允许修改和分发
- ✅ 允许私有部署
- ❌ 不允许重新包装后声称原创

### 版权声明
© 2026 iSenlink. 保留所有权利。

---

## 🎯 使用场景

### 场景1：AI助手团队管理
```bash
# 管理员查看团队状态
worktracker status

# 管理员导出工作报告
worktracker export daily --date $(date +%Y-%m-%d)
```

### 场景2：个人工作管理
```bash
# 个人工作记录
worktracker start "我" "完成项目文档" "今天下班前"
worktracker update "我" 50 "已完成大纲和第一章"
worktracker complete "我" "文档已完成并提交" "等待评审反馈"
```

### 场景3：跨团队协作
```bash
# 多团队协作
worktracker config add-assistant "开发团队" "后端开发"
worktracker config add-assistant "设计团队" "UI/UX设计"
worktracker config add-assistant "测试团队" "质量保证"

# 跟踪各团队进展
worktracker status
```

---

**最后更新**：2026-03-14  
**版本**：v1.0.0  
**作者**：iSenlink  
**状态**：✅ 生产就绪