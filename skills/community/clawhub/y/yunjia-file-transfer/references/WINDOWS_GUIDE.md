# Windows 文件助手快速参考指南

## 🎯 核心原则
**Windows 优先，用户体验第一**

## 📋 常用场景

### 场景1：用户要查看文件
```
用户：把财报发给我
智能体：好的，我马上查找财报文件。
```

**智能体行动**：
1. 使用 PowerShell 搜索：
   ```powershell
   Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*财报*" -File
   Get-ChildItem -Path "$env:USERPROFILE\Documents" -Filter "*财报*" -File -Recurse
   ```

2. 生成发送指令：
   ```bash
   python3 assemble_send_instruction.py --file "C:\Users\用户\Downloads\2024Q1财报.xlsx" --text "已找到您要的2024年第一季度财报，请查收。"
   ```

### 场景2：用户需要合同文件
```
用户：发一下采购合同
智能体：好的，我查找一下采购合同。
```

**智能体行动**：
1. 搜索合同文件：
   ```powershell
   Get-ChildItem -Path "D:\合同管理" -Filter "*采购合同*" -File
   Get-ChildItem -Path "$env:USERPROFILE\Documents\合同" -Filter "*采购*" -File
   ```

### 场景3：用户要项目资料
```
用户：把项目计划发给我看看
智能体：我查找一下项目计划文件。
```

## 🔧 Windows 专用命令参考

### 快速查找命令
```powershell
# 查找最近3天修改的文件（用户可能刚下载）
Get-ChildItem -Path "$env:USERPROFILE\Downloads" -File | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-3)} | Sort-Object LastWriteTime -Descending

# 按文件类型查找
Get-ChildItem -Path "$env:USERPROFILE" -Include "*.xlsx", "*.xls", "*.docx", "*.pdf" -File -Recurse | Select-Object -First 20 FullName

# 查找大文件（可能包含重要资料）
Get-ChildItem -Path "$env:USERPROFILE" -File -Recurse | Where-Object {$_.Length -gt 10MB} | Sort-Object Length -Descending | Select-Object -First 10 FullName
```

### 常用目录映射
| 目录类型 | Windows 路径 | 说明 |
|---------|-------------|------|
| 下载目录 | `C:\Users\%USERNAME%\Downloads` | 用户最常放文件的地方 |
| 文档目录 | `C:\Users\%USERNAME%\Documents` | 正式文档存放处 |
| 桌面 | `C:\Users\%USERNAME%\Desktop` | 当前工作文件 |
| D盘工作 | `D:\工作文件\` | 很多用户习惯用D盘 |

## 💬 与用户沟通的话术

### 找到文件时
```
✅ "已找到您要的[文件名]，这就发给您。"
✅ "[文件名]已发送，请您审阅。"
✅ "文件已发送，请查收。"
```

### 找不到文件时
```
❓ "没有找到您说的文件。您能告诉我更具体的文件名吗？"
❓ "我搜索了常见位置，没找到该文件。您最近保存在哪个目录了？"
❓ "要不您告诉我文件的大概修改日期，我帮您缩小范围查找？"
```

### 找到多个文件时
```
📁 "找到了3个相关文件：1) 2024Q1财报.xlsx 2) 2023年报.pdf 3) 财务分析.docx。您要哪个？"
```

## 🚨 重要提醒

1. **绝对不要使用相对路径** - 用户电脑上会失败
2. **路径中的中文要正确处理** - Windows 支持中文路径
3. **反斜杠要转义或使用正斜杠** - `C:\\Users\\` 或 `C:/Users/`
4. **优先使用 PowerShell** - 比 CMD 更强大
5. **考虑用户的使用习惯** - 很多用户文件在桌面或下载目录

## 📞 紧急情况处理

如果技能无法正常工作：
1. 首先检查路径格式是否正确
2. 确认文件确实存在
3. 尝试使用正斜杠代替反斜杠
4. 如果还是不行，可以手动发送文件并说明情况

---
**最后记住**：用户满意是第一要务，技术细节要隐藏好，体验要流畅自然。