# Memory Manager Skill

## 概述
简化记忆管理系统，支持主代理与子代理间的记忆交换、归档和管理。

## 功能特性
- ✅ **简化目录结构**：清晰的记忆组织方式
- ✅ **代理记忆交换**：主代理与子代理间的可控记忆共享
- ✅ **文件归档管理**：按需归档，避免混乱
- ✅ **操作记录系统**：所有操作自动记录
- ✅ **极简脚本工具**：避免复杂语法问题

## 适用场景
1. **多代理协作**：主代理与写作助手等子代理间的记忆共享
2. **项目记忆管理**：写作项目、分析项目等的记忆组织
3. **长期记忆维护**：重要记忆的归档和版本管理
4. **系统状态监控**：记忆系统健康状态检查

## 快速开始

### 1. 安装技能
```bash
# 通过ClawHub安装（如果发布）
clawhub install memory-manager

# 或手动复制到skills目录
```

### 2. 初始化系统
```powershell
# 检查系统状态
.\scripts\memory_check.ps1

# 检查代理状态
.\scripts\agent_check.ps1 list
```

### 3. 基本使用
```powershell
# 查看共享文件
.\scripts\memory_check.ps1 -Action list-files

# 归档文件
.\scripts\archive_tool.ps1 -File "character_profiles.md" -Reason "季度备份"
```

## 目录结构
```
memory/
├── main/          # 主代理记忆
├── shared_pool/   # 共享记忆池
├── agent_access/  # 子代理访问点
├── logs/          # 操作记录
├── archive/       # 归档文件
└── temp/          # 临时文件
```

## 配置说明

### 默认配置 (config/default.json)
```json
{
  "base_dir": "D:\\openclaw\\.openclaw\\workspace\\memory",
  "agents": {
    "writing-assistant": {
      "path": "D:\\writing-bot\\workspace\\memory",
      "name": "Writing Assistant"
    }
  },
  "archive_retention_days": 30,
  "log_retention_days": 90
}
```

## 工具脚本

### memory_check.ps1
- **功能**：检查记忆系统状态
- **参数**：`status`, `list-files`, `list-dirs`
- **示例**：`.\memory_check.ps1 status`

### agent_check.ps1
- **功能**：检查代理状态
- **参数**：`list`, `check <agent-name>`
- **示例**：`.\agent_check.ps1 list`

### simple_logger.ps1
- **功能**：简单操作记录
- **参数**：自动调用，无需手动使用
- **用途**：内部工具，供其他脚本调用

### archive_tool.ps1
- **功能**：文件归档
- **参数**：`-File <path>`, `-Reason <description>`
- **示例**：`.\archive_tool.ps1 -File "project.md" -Reason "项目完成"`

## 使用示例

### 示例1：日常检查
```powershell
# 检查系统状态
.\scripts\memory_check.ps1

# 检查代理状态
.\scripts\agent_check.ps1 list

# 列出共享文件
.\scripts\memory_check.ps1 -Action list-files
```

### 示例2：文件归档
```powershell
# 归档单个文件
.\scripts\archive_tool.ps1 -File "project_progress.md" -Reason "月度归档"

# 批量归档（通过循环）
Get-ChildItem "memory\main\shared\*.md" | ForEach-Object {
    .\scripts\archive_tool.ps1 -File $_.FullName -Reason "批量清理"
}
```

### 示例3：代理记忆访问
```powershell
# 检查写作助手记忆空间
.\scripts\agent_check.ps1 check writing-assistant

# 如果需要访问，可以通过配置文件路径直接访问
```

## 最佳实践

### 1. 定期检查
- 每周检查一次系统状态
- 每月检查一次归档文件
- 每季度清理一次临时文件

### 2. 文件命名规范
- 活跃文件：`filename.md`
- 归档文件：`filename_archived_YYYYMMDD.md`
- 待删除：`filename_delete_YYYYMMDD.md`

### 3. 操作记录
- 所有重要操作都应有记录
- 记录文件保存在`logs/`目录
- 定期备份记录文件

### 4. 安全注意事项
- 敏感文件不要放入共享目录
- 归档前检查文件内容
- 定期清理临时文件

## 故障排除

### 常见问题

#### Q1: 脚本执行报错
**问题**：PowerShell脚本执行报语法错误
**解决**：
1. 使用极简脚本版本
2. 检查文件编码（使用UTF-8无BOM）
3. 避免复杂语法结构

#### Q2: 代理路径不存在
**问题**：代理检查显示路径不存在
**解决**：
1. 检查代理配置文件
2. 确认代理工作空间是否存在
3. 更新配置文件中的路径

#### Q3: 归档文件名不正确
**问题**：归档后文件名没有按预期重命名
**解决**：
1. 手动重命名文件
2. 使用简化版归档工具
3. 检查文件扩展名处理

#### Q4: 记录文件为空
**问题**：操作记录文件创建但内容为空
**解决**：
1. 使用`simple_logger.ps1`
2. 检查JSON生成逻辑
3. 验证文件写入权限

## 扩展开发

### 添加新代理
1. 编辑`config/default.json`
2. 添加代理配置
3. 测试代理访问

### 自定义归档规则
1. 修改`archive_tool.ps1`
2. 添加自定义命名规则
3. 测试归档功能

### 集成到工作流
1. 在AGENTS.md中添加记忆检查步骤
2. 设置定期检查任务
3. 集成到项目工作流中

## 版本历史

### v1.0.0 (2026-04-17)
- 初始版本发布
- 基础记忆管理功能
- 代理记忆交换支持
- 简化脚本工具集

## 支持与反馈

### 问题报告
如遇问题，请提供：
1. 错误信息截图
2. 操作步骤
3. 系统环境信息

### 功能建议
如需新功能，请描述：
1. 使用场景
2. 预期行为
3. 优先级评估

### 联系方式
- 通过OpenClaw会话反馈
- 查看文档获取更多信息

---
*技能ID: memory-manager*
*版本: 1.0.0*
*创建日期: 2026-04-17*
*最后更新: 2026-04-17*