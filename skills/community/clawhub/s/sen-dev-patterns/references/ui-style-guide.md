# UI样式规范

## 配色方案

### 颜色变量表

```python
COLORS = {
    # 主色调渐变
    "primary_start": "#667eea",
    "primary_mid": "#5a67d8",
    "primary_end": "#4c51bf",
    
    # 成功色
    "success": "#48bb78",
    "success_light": "#68d391",
    
    # 警告/进度色
    "warning": "#f6ad55",
    "warning_dark": "#ed8936",
    "status_working": "#ff9500",
    
    # 错误色
    "error": "#fc8181",
    "error_dark": "#e74c3c",
    
    # 信息色
    "info": "#63b3ed",
    "info_dark": "#3498db",
    
    # 辅助色
    "purple": "#9f7aea",
    "purple_dark": "#805ad5",
    "cyan": "#00d4aa",  # 数据分割功能
    
    # 背景色
    "bg_light": "#f0f5f9",
    "bg_gradient": "#f0f4ff",
    "bg_white": "#ffffff",
    
    # 日志区域（深色主题）
    "log_bg": "#1a202c",
    "log_text": "#e2e8f0",
    "log_gray": "#a0aec0",
    "log_border": "#667eea",
    
    # 状态栏
    "status_bg": "#ffffffb3",
    "status_text": "#5a6a8a",
    
    # 边框
    "border_light": "#647ea0",
}
```

## PySide6/Qt 样式

### 主窗口样式

```python
self.setStyleSheet("""
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #f0f4ff, stop:0.5 #e8f0ff, stop:1 #f5f0ff);
    }
""")
```

### 状态栏样式

```python
status.setStyleSheet("""
    QStatusBar {
        background: #ffffffb3;
        color: #5a6a8a;
        border-top: 1px solid #647ea0;
    }
""")
```

### 主容器样式（毛玻璃效果）

```python
container = QFrame()
container.setStyleSheet("""
    QFrame {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid #667eea;
    }
""")
shadow = QGraphicsDropShadowEffect(
    blurRadius=30, xOffset=0, yOffset=8, color=QColor(100, 120, 180, 40)
)
container.setGraphicsEffect(shadow)
```

### 日志文本框样式

```python
self.log_box.setStyleSheet("""
    QTextEdit {
        background: #1a202c;
        border-radius: 14px;
        border: 1px solid #667eea;
        color: #e2e8f0;
        font-family: Consolas, 'Courier New', monospace;
        font-size: 13px;
        padding: 8px;
    }
    QScrollBar:vertical {
        background: #2d3748;
        border-radius: 6px;
        width: 10px;
        margin: 4px;
    }
    QScrollBar::handle:vertical {
        background: #667eea;
        border-radius: 5px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background: #7c8ff5;
    }
""")
```

### 水晶质感按钮颜色配置

```python
btn_colors = {
    self.btn_load: {
        "start": "#667eea", "mid": "#5a67d8", "end": "#4c51bf",
        "hover_start": "#7c8ff5", "hover_mid": "#6972e0", "hover_end": "#5a5ac8",
        "pressed_start": "#5a67d8", "pressed_mid": "#4c51bf", "pressed_end": "#43439a"
    },
    self.btn_export: {
        "start": "#48bb78", "mid": "#38a169", "end": "#2f855a",
        "hover_start": "#5fcd8e", "hover_mid": "#48bb78", "hover_end": "#38a169",
        "pressed_start": "#38a169", "pressed_mid": "#2f855a", "pressed_end": "#276749"
    },
    self.btn_img: {
        "start": "#ed8936", "mid": "#dd6b20", "end": "#c05621",
        "hover_start": "#f6a03d", "hover_mid": "#ed8936", "hover_end": "#dd6b20",
        "pressed_start": "#dd6b20", "pressed_mid": "#c05621", "pressed_end": "#9c4221"
    },
    self.btn_log: {
        "start": "#9f7aea", "mid": "#805ad5", "end": "#6b46c1",
        "hover_start": "#b794f4", "hover_mid": "#9f7aea", "hover_end": "#805ad5",
        "pressed_start": "#805ad5", "pressed_mid": "#6b46c1", "pressed_end": "#553c9a"
    },
}
```

### 设置按钮样式

```python
self.btn_settings.setStyleSheet("""
    QPushButton {
        color: #4a5568;
        font-weight: 600;
        font-size: 13px;
        border-radius: 18px;
        border: 1px solid #667eea;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #ffffff,
            stop:0.3 #ffffff,
            stop:1 #f0f5ff);
    }
    QPushButton:hover {
        border: 1px solid #667eea;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #ffffff,
            stop:0.3 #f8faff,
            stop:1 #e6ebff);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #e6ebff,
            stop:1 #c8d2ff);
    }
""")
```

## Tkinter 样式

### 主窗口背景

```python
self.root.configure(bg="#f0f5f9")
```

### Frame样式

```python
style.configure("TFrame", background="#f0f5f9")
style.configure("TLabelframe", background="#f0f5f9", foreground="#2c3e50")
style.configure("TLabelframe.Label", background="#f0f5f9", foreground="#2c3e50", font=font_main)
```

### 日志文本框

```python
self.log_text = scrolledtext.ScrolledText(
    log_frame,
    width=80,
    height=15,
    font=("Consolas", 10),
    bg="#ffffff",
    fg="#333333",
    insertbackground="#2980b9",
    relief=tk.SOLID,
    borderwidth=1,
    state=tk.NORMAL
)

# 日志标签样式
self.log_text.tag_config('info', foreground='#2980b9')
self.log_text.tag_config('warning', foreground='#e67e22')
self.log_text.tag_config('error', foreground='#e74c3c')
self.log_text.tag_config('success', foreground='#27ae60')
```

## 页面布局规范

### 标准布局结构

```
┌─────────────────────────────────────────────────────────┐
│ 标题                                    [⚙ 设置]        │
│ 副标题                                                    │
├─────────────────────────────────────────────────────────┤
│ [🚀 一键执行按钮 - 跨越整行]                               │
├─────────────────────────────────────────────────────────┤
│ [1.选择文件] [2.拆分] [3.汇总] [4.映射] [5.导出]         │
├─────────────────────────────────────────────────────────┤
│ 日志区域 (ScrolledText, 可滚动)                          │
│                                                          │
├─────────────────────────────────────────────────────────┤
│ 状态栏                              v1.0 | Windows & Mac │
└─────────────────────────────────────────────────────────┘
```

### 按钮grid布局

```python
btn_configs = [
    ("1. 选择原始数据文件", self.btn_select_file),
    ("2. 按日期拆分中间表", self.btn_split_by_date),
    ("3. 生成月度汇总表", self.btn_generate_monthly),
    ("4. 加载模板执行映射", self.btn_map_template),
    ("5. 导出最终结果", self.btn_export_result),
]

for i, (text, cmd) in enumerate(btn_configs):
    btn = CrystalButton(
        btn_container,
        text=text,
        command=lambda c=cmd: self.run_async(c),
        width=200,
        height=50
    )
    btn.grid(row=0, column=i, padx=4, pady=8, sticky="ew")
    self.buttons.append(btn)

# 配置列权重，使按钮均匀分布
for i in range(num_buttons):
    btn_container.columnconfigure(i, weight=1)
```

### 日志颜色映射

```python
def _on_worker_progress(self, text: str) -> None:
    """处理进度更新"""
    if "完成" in text or "成功" in text:
        color = "#68d391"  # 绿色
    elif "开始" in text or "统计" in text or "处理" in text:
        color = "#63b3ed"  # 蓝色
    elif "错误" in text or "失败" in text:
        color = "#fc8181"  # 红色
    elif "跳过" in text:
        color = "#a0aec0"  # 灰色
    else:
        color = "#e2e8f0"  # 浅灰色
    self._append_plain(text, color=color)
```

## 窗口居中显示

```python
def center_window(dialog, width, height):
    """将窗口居中显示"""
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() - width) // 2
    y = (dialog.winfo_screenheight() - height) // 2
    dialog.geometry(f"{width}x{height}+{x}+{y}")
```

## 图标使用

### 按钮图标

| 图标 | 用途 | 颜色 |
|------|------|------|
| 💁 | 前台现场解决 | 蓝色 |
| ⚔️ | 一线生产战队 | 绿色 |
| 🔔 | 投申诉高效处置 | 橙色 |
| 📋 | 生成日志 | 紫色 |
| ✂️ | 数据分割 | 青色 |
| 📤 | 导出 | 粉色 |
| ⚙ | 设置 | 边框色 |
| ◆ | 系统图标 | 渐变紫蓝 |

## 状态指示器

### 状态灯

```python
# 空闲状态
self.status_light.setStyleSheet("QLabel { color: #48bb78; font-size: 18px; }")

# 工作中状态
self.status_light.setStyleSheet("QLabel { color: #ff9500; font-size: 18px; }")

# 异常状态
self.status_light.setStyleSheet("QLabel { color: #fc8181; font-size: 18px; }")
```
