# 窗口定位与微信主界面操作

## 启动/重新激活微信主界面

**重要，后续操作依赖微信主窗口**

```powershell
Start-Process "C:\Program Files (x86)\Tencent\Weixin\Weixin.exe" --scene=taskbarpins
```

- 如果微信还没启动，执行命令可以启动微信登录界面。
- 如果微信已在后台运行，执行命令可以激活主窗口（需要`--scene=taskbarpins`参数）。
- 当微信窗口快照返回空白时，执行命令可以重新激活主窗口，使快照返回正常内容。

### 已有微信窗口时

#### 恢复最小化窗口
```powershell
python scripts\winguictl.py window --window-id <wx_window_id> restore
```

#### 将窗口置于前台
```powershell
python scripts\winguictl.py window --window-id <wx_window_id> focus
```

## 查找微信窗口

### 列出所有可见窗口，识别微信窗口 ID

```powershell
python scripts\winguictl.py window list
```

### 微信窗口特征

微信主窗口的 UIA 特征：
- `class_name`: `mmui::MainWindow`
- `class_name` (登录界面): `mmui::LoginWindow`
- 通用 Qt 窗口类名：`Qt\d+QWindowIcon`
