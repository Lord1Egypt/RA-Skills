---
id: module-23
name: 系统文件完整性检查与修复（SFC / DISM）
description: 扫描并修复受损的 Windows 系统文件，诊断组件存储损坏，解决因系统文件破坏导致的服务异常。
keywords: ['系统文件好像坏了', '服务启动报错找不到文件', 'DISM 修复', 'SFC 扫描']
permission: admin
mode: confirm
subset: basic
---

## 🆕 模块 23：系统文件完整性检查与修复（SFC / DISM）


<details>
<summary>📋 展开查看：🆕 模块 23：系统文件完整性检查与修复（SFC / DISM）</summary>

**用途**：扫描并修复受损的 Windows 系统文件，诊断组件存储损坏，解决因系统文件破坏导致的服务异常。

**常你说**：`"系统文件好像坏了"` / `"服务启动报错找不到文件"` / `"DISM 修复"` / `"SFC 扫描"`

> ⚠️ **本模块需要管理员权限，仅扫描和修复系统文件，不修改用户数据。**


```powershell
# 扫描所有系统文件完整性（不修复）
sfc /scanfile=C:\Windows\System32\kernel32.dll

# 扫描并尝试修复（需管理员）
# sfc /scannow
```



```powershell
# 扫描组件存储是否损坏（不修复）
DISM /Online /Cleanup-Image /ScanHealth

# 检查组件存储健康状态
DISM /Online /Cleanup-Image /CheckHealth

# 查看可修复的组件列表
DISM /Online /Cleanup-Image /AnalyzeComponentStore

# 清理组件存储中的旧版本组件
# DISM /Online /Cleanup-Image /StartComponentCleanup

# 修复组件存储（需联网）
# DISM /Online /Cleanup-Image /RestoreHealth
```



```powershell
# 标准修复流程：先 DISM 修复组件存储，再 SFC 修复系统文件
# DISM /Online /Cleanup-Image /RestoreHealth
# sfc /scannow
# 完成后重启系统
```


**风险等级**：🟢 扫描只读 / 🟡 修复需确认

| 报错 | 含义 | 解决 |
|-----|------|-----|
| `Windows Resource Protection did not find any integrity violations` | 系统文件正常 | 无需修复 |
| `There is a system repair pending which requires reboot` | 有挂起的修复 | 重启后再扫描 |
| `The source files could not be downloaded` | 需联网 | 使用安装介质作为源 |

**常见坑 & 解决**：

| 场景 | 说明 |
|-----|------|
| SFC 报告无法修复某些文件 | 通常是组件存储损坏，先执行 DISM |
| DISM 报错 0x800f081f | 找不到源文件，需指定安装介质 |
| 修复后问题依旧 | 可能是文件权限问题，检查 ACL |


</details>

[↑ 返回顶部](#module-1)

---

<a name="module-24"></a>

