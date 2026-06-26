---
name: remote-install
description: Remote software installation via automated installer detection and GUI automation. Use when: user needs to install software packages (.exe/.msi) on Windows machines, automate Office/Adobe/Chrome installations, or handle unattended software deployment. NOT for: Linux/macOS installations, package manager installs (apt/yum/brew), or containerized deployments.
---

# Remote Install Skill - 远程软件安装

通过自动化检测和 GUI 控制实现 Windows 远程软件安装。

## 何时使用

✅ **使用场景：**
- "帮我安装桌面上的软件"
- "远程安装 Office"
- "自动安装下载目录的安装包"
- "静默安装 MSI 包"
- "检测并安装用户电脑上的软件"

❌ **不使用：**
- Linux/macOS 安装
- 包管理器安装 (apt/yum/brew)
- 容器化部署

## 工作流程

1. **检测安装包** - 扫描桌面/下载目录查找 .exe/.msi/.zip/.rar
2. **识别软件类型** - Office/Adobe/Chrome/7-Zip 等
3. **选择安装方式**：
   - `.msi` → msiexec 静默安装
   - `.exe` → pywinauto GUI 自动化
   - `.zip/.rar` → 解压后安装
4. **执行安装** - 处理弹窗、点击"下一步"按钮
5. **返回结果** - 成功/失败报告

## 调用示例

**"安装桌面上的所有软件"**
→ 自动检测桌面所有安装包并依次安装

**"只安装 Office"**
→ 过滤并安装 Office 相关安装包（自动判断 32/64 位）

**"检查下载目录有什么安装包"**
→ 列出安装包但不安装

**"安装 C:\Users\桌面\setup.exe"**
→ 安装指定路径的安装包

## 输出格式

```json
{
  "success": true,
  "message": "远程安装流程完成",
  "summary": {
    "total_packages": 2,
    "successful_installs": 1,
    "failed_installs": 1,
    "results": [
      {
        "package": "C:\\Users\\...\\Office.exe",
        "success": true,
        "message": "EXE 包安装成功"
      }
    ]
  }
}
```

## 配置

编辑 `config.json` 自定义：

```json
{
  "installation": {
    "timeout_seconds": 300,
    "retry_attempts": 3,
    "log_level": "INFO"
  },
  "ui_elements": {
    "next_button_texts": ["下一步", "Next", "继续", "Install"],
    "finish_button_texts": ["完成", "Finish", "Close"]
  }
}
```

## 依赖

- Python 3.8+
- pyautogui, pywinauto, Pillow
- Windows 系统

## 安装

```bash
pip install pyautogui pywinauto Pillow
```

## 使用说明

脚本会自动：
1. 检测系统架构（32/64 位）
2. 检测已安装 Office 版本（如有）
3. 根据内存大小推荐架构
4. 自动点击安装窗口的"下一步"按钮
5. 记录完整日志到 `installer.log`

## 安全说明

- 仅在用户授权下运行
- 所有操作记录日志
- 可配置超时和重试
- 不收集或外传用户数据
