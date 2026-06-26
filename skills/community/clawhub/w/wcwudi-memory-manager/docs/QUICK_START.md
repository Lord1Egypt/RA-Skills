# 快速开始指南

## 5分钟上手Memory Manager

### 第一步：环境检查
```powershell
# 进入脚本目录
cd D:\openclaw\.openclaw\workspace\memory-manager\scripts

# 检查系统状态
.\memory_check.ps1
```

预期输出：
```
=== Memory System Check ===
Time: 2026-04-17 14:15:00
Base: D:\openclaw\.openclaw\workspace\memory
Action: status

--- Directory Status ---
Base: OK
Main Memory: OK
Shared Files: OK
Archive: OK
Logs: OK
...
```

### 第二步：代理检查
```powershell
# 列出所有代理
.\agent_check.ps1 list

# 检查特定代理
.\agent_check.ps1 check writing-assistant
```

### 第三步：测试归档功能
```powershell
# 先创建一个测试文件
$testContent = "# Test File`nCreated for testing"
$testContent | Out-File "..\..\memory\main\shared\test_quickstart.md" -Encoding UTF8

# 测试归档（测试模式）
.\archive_tool.ps1 -File "test_quickstart.md" -Reason "快速开始测试" -Test

# 实际归档
.\archive_tool.ps1 -File "test_quickstart.md" -Reason "快速开始测试"
```

### 第四步：验证结果
```powershell
# 检查共享文件
.\memory_check.ps1 -Action list-files

# 检查归档文件
.\memory_check.ps1 -Action list-archive

# 检查操作记录
Get-ChildItem "..\..\memory\logs\operations\" | Select-Object -Last 3
```

## 常用命令速查

### 系统状态
```powershell
# 完整状态检查
.\memory_check.ps1

# 只检查文件
.\memory_check.ps1 -Action list-files

# 只检查目录结构
.\memory_check.ps1 -Action list-dirs
```

### 代理管理
```powershell
# 列出所有代理
.\agent_check.ps1 list

# 检查代理详情
.\agent_check.ps1 check writing-assistant
```

### 文件操作
```powershell
# 归档文件
.\archive_tool.ps1 -File "filename.md" -Reason "描述原因"

# 测试归档（不实际执行）
.\archive_tool.ps1 -File "filename.md" -Reason "测试" -Test
```

### 日志查看
```powershell
# 查看最新操作记录
Get-ChildItem "..\..\memory\logs\operations\" | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# 查看交换记录
Get-ChildItem "..\..\memory\logs\exchanges\" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

## 日常维护流程

### 每日检查（可选）
```powershell
cd D:\openclaw\.openclaw\workspace\memory-manager\scripts
.\memory_check.ps1 -Action status
```

### 每周维护
```powershell
# 1. 系统状态检查
.\memory_check.ps1

# 2. 代理状态检查
.\agent_check.ps1 list

# 3. 归档30天未修改的文件
$cutoffDate = (Get-Date).AddDays(-30)
Get-ChildItem "..\..\memory\main\shared\*.md" | Where-Object {
    $_.LastWriteTime -lt $cutoffDate
} | ForEach-Object {
    .\archive_tool.ps1 -File $_.Name -Reason "自动清理-30天未修改"
}
```

### 每月清理
```powershell
# 清理临时文件（超过7天）
$tempDir = "..\..\memory\temp"
if (Test-Path $tempDir) {
    Get-ChildItem $tempDir -Recurse -File | Where-Object {
        $_.LastWriteTime -lt (Get-Date).AddDays(-7)
    } | Remove-Item -Force
}
```

## 故障排除快速指南

### 问题1：脚本执行报错
```powershell
# 检查PowerShell执行策略
Get-ExecutionPolicy

# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### 问题2：文件找不到
```powershell
# 检查文件是否存在
Test-Path "..\..\memory\main\shared\filename.md"

# 列出所有文件
Get-ChildItem "..\..\memory\main\shared\"
```

### 问题3：归档失败
```powershell
# 手动检查
$file = "filename.md"
$source = "..\..\memory\main\shared\$file"
$archive = "..\..\memory\archive\"

# 检查源文件
Test-Path $source

# 检查归档目录
Test-Path $archive

# 手动归档
Move-Item -Path $source -Destination $archive -Force
```

### 问题4：代理访问失败
```powershell
# 检查代理路径
$agentPath = "D:\writing-bot\workspace\memory"
Test-Path $agentPath

# 手动访问
Get-ChildItem $agentPath
```

## 下一步学习

1. **查看完整文档**：阅读`README.md`了解所有功能
2. **学习架构**：查看`docs/ARCHITECTURE.md`了解系统设计
3. **参考示例**：查看`examples/`目录中的使用示例
4. **自定义配置**：修改`config/default.json`适应你的需求

## 获取帮助

- 查看`docs/TROUBLESHOOTING.md`获取详细故障排除指南
- 查看脚本帮助：`.\memory_check.ps1 -?`（如果支持）
- 查看示例代码：`examples/`目录

---
*快速开始指南 v1.0*
*最后更新: 2026-04-17*