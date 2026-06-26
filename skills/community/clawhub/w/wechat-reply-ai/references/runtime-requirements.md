# 运行前提

## 环境要求

- Windows 桌面环境
- 已安装并登录 PC 微信
- Python 环境可用
- 能安装并调用下列依赖：
  - `uiautomation`
  - `pywinauto`
  - `pywin32`
  - `Pillow`
  - `rapidocr-onnxruntime`

## 微信窗口要求

- 优先复用已经打开的微信主窗口。
- 不要把系统托盘里的 `WxTrayIconMessageWindow` 当成可操作主窗口。
- 如果看到 `win32` 后端拿到白屏窗口，优先回退到现有脚本里的 `uiautomation` + `pywinauto` 混合方案，不要单独依赖白屏句柄。

## 常见启动方式

如果微信没开，可以在命令里传：

```powershell
--exe "D:\app\Weixin\Weixin.exe"
```

脚本只会在找不到可用窗口时才尝试拉起微信。

## 中文发送要求

- 发送中文时，优先使用 `--message-file`。
- 回复文本文件必须是 `UTF-8`。
- 不要把长中文回复直接塞进容易丢编码的终端内联命令里，否则可能变成 `???`。

## 中断要求

- 调试或长轮询过程中，一旦检测到 `Esc`，应立即停止。
- 需要保留脚本里现有的 `raise_if_escape_pressed()` / `sleep_with_abort()` 路径，不要绕过。
