---
name: wechat-moments
description: 微信朋友圈操作技能。用于打开朋友圈、浏览动态、滚动查看内容等。使用场景：(1) 打开朋友圈，(2) 滚动浏览朋友圈内容，(3) 查看好友动态，(4) 给朋友圈点赞评论
---

# 微信朋友圈操作

## ⚠️ 重要：打开微信的正确方式

**禁止使用 Start-Process 启动微信！必须通过点击任务栏图标打开！**

正确流程：
1. 点击显示隐藏图标 (1142, 744)
2. 点击微信图标 (1111, 701)
3. 点击屏幕中间 (400, 300) 激活微信窗口

❌ 错误方式：Start-Process "D:\Weixin\Weixin.exe"（这只启动进程，不会打开界面）

## 关键坐标

| 功能 | 坐标 (X, Y) | 说明 |
|------|-------------|------|
| 显示隐藏图标 | 1142, 744 | 任务栏显示隐藏图标按钮 |
| 微信图标 | 1111, 701 | 微信启动图标 |
| 激活微信 | 400, 300 | 点击屏幕中间激活微信窗口 |
| 朋友圈按钮 | 272, 322 | 朋友圈标签位置 |
| 语音电话 | 1055, 108 | 聊天窗口右上角电话按钮 |

## 使用流程

### 打开朋友圈

**重要：若微信未显示在任务栏，需先点击显示隐藏图标！**

1. 点击显示隐藏图标 (1142, 744) 展开隐藏图标
2. 点击微信图标 (1111, 701) 打开微信
3. 点击屏幕中间位置 (400, 300) 激活微信窗口
4. 点击朋友圈按钮 (272, 322)

```powershell
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WMoments {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(int flags, int dx, int dy, int d, int e);
}
"@

# 1. 点击显示隐藏图标 (1142, 744)
[WMoments]::SetCursorPos(1142, 744)
Start-Sleep -Milliseconds 100
[WMoments]::mouse_event(2, 0, 0, 0, 0)
[WMoments]::mouse_event(4, 0, 0, 0, 0)
Start-Sleep -Milliseconds 300

# 2. 点击微信图标 (1111, 701)
[WMoments]::SetCursorPos(1111, 701)
Start-Sleep -Milliseconds 100
[WMoments]::mouse_event(2, 0, 0, 0, 0)
[WMoments]::mouse_event(4, 0, 0, 0, 0)
Start-Sleep -Milliseconds 500

# 3. 激活微信（点击屏幕中间）
[WMoments]::SetCursorPos(400, 300)
Start-Sleep -Milliseconds 100
[WMoments]::mouse_event(2, 0, 0, 0, 0)
[WMoments]::mouse_event(4, 0, 0, 0, 0)
Start-Sleep -Milliseconds 200

# 4. 点击朋友圈按钮
[WMoments]::SetCursorPos(272, 322)
Start-Sleep -Milliseconds 100
[WMoments]::mouse_event(2, 0, 0, 0, 0)
[WMoments]::mouse_event(4, 0, 0, 0, 0)

### 关闭朋友圈

点击右上角关闭按钮 (932, 108)

```powershell
# 点击右上角关闭朋友圈
[WMoments]::SetCursorPos(932, 108)
Start-Sleep -Milliseconds 100
[WMoments]::mouse_event(2, 0, 0, 0, 0)
[WMoments]::mouse_event(4, 0, 0, 0, 0)
```

### 浏览朋友圈（滚动）

**正确的浏览方式：先向下滚动浏览，再慢慢往上滚回顶部**

- 滚动位置：600, 400（屏幕中间偏上）
- 向下滚动：100次，每次50单位，间隔200ms
- 向上滚动：300次（3倍），间隔150ms，速度要慢

```powershell
# 1. 先向下滚动100次浏览内容
for ($i = 0; $i -lt 100; $i++) {
    [WMoments]::SetCursorPos(600, 400)
    [WMoments]::mouse_event(0x0800, 0, 0, -50, 0)
    Start-Sleep -Milliseconds 200
}

# 2. 再慢慢往上滚动300次回到顶部（是向下滚动的3倍）
for ($i = 0; $i -lt 300; $i++) {
    [WMoments]::SetCursorPos(600, 400)
    [WMoments]::mouse_event(0x0800, 0, 0, 50, 0)
    Start-Sleep -Milliseconds 150
}
```

### 聊天窗口操作

#### 搜索联系人

```powershell
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("^f")
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait("联系人名字")
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
```

#### 发送消息

```powershell
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("你好，我是贾维斯")
Start-Sleep -Milliseconds 100
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
```

#### 拨打电话

```powershell
# 点击语音电话按钮 (1055, 108)
[WMoments]::SetCursorPos(1055, 108)
Start-Sleep -Milliseconds 50
[WMoments]::mouse_event(2, 0, 0, 0, 0)
[WMoments]::mouse_event(4, 0, 0, 0, 0)

# 选择语音通话
Start-Sleep -Milliseconds 200
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("{DOWN}")
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
```

## 注意事项

1. **微信未显示时**：若任务栏无微信图标，先点击显示隐藏图标 (1142, 744) 展开隐藏图标，再点击微信图标 (1111, 701)
2. **必须先激活微信**：每次操作前先点击屏幕中间 (400, 300) 激活微信窗口
3. **坐标适配**：坐标基于当前窗口大小，不同分辨率可能需要微调
4. **等待时间**：每次操作后适当等待 (100-300ms)，确保界面响应
5. **滚动标志**：mouse_event 0x0800 表示垂直滚动

## 常见问题

- **点击无效**：尝试增加等待时间或重新激活微信窗口
- **滚动不动**：检查鼠标位置是否在有效区域
- **发送失败**：确保焦点在微信输入框
