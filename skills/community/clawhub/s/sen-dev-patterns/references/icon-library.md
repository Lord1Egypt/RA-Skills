# 图标库

本文档沉淀常用图标配置，便于快速复用。

---

## 1. 按钮图标（Unicode符号）

### 基础操作按钮

| 图标 | Unicode | 用途 | 样式示例 |
|------|---------|------|----------|
| 📁 | - | 选择文件 | `color: #0b3d91;` |
| ➕ | - | 添加 | `color: #48bb78;` |
| ➖ | - | 删除 | `color: #fc8181;` |
| 💾 | - | 保存 | `color: #667eea;` |
| ⚙️ | - | 设置 | `color: #718096;` |
| ▶️ | - | 开始/播放 | `color: #48bb78;` |
| ⏹️ | - | 停止 | `color: #fc8181;` |
| 🔄 | - | 刷新 | `color: #667eea;` |
| 📊 | - | 数据统计 | `color: #0b3d91;` |
| 📤 | - | 导出 | `color: #48bb78;` |
| 📥 | - | 导入 | `color: #667eea;` |
| 🔍 | - | 搜索 | `color: #718096;` |
| ℹ️ | - | 信息 | `color: #63b3ed;` |
| ⚠️ | - | 警告 | `color: #f6ad55;` |
| ❌ | - | 错误 | `color: #fc8181;` |
| ✅ | - | 成功 | `color: #48bb78;` |

### 状态指示符

```python
# 状态图标
STATUS_ICONS = {
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
    'pending': '⏳',
    'running': '🔄',
    'idle': '⭕'
}

# 日志级别图标
LOG_ICONS = {
    'DEBUG': '🔵',
    'INFO': 'ℹ️',
    'WARNING': '⚠️',
    'ERROR': '❌',
    'SUCCESS': '✅'
}
```

---

## 2. Tkinter按钮图标

### 使用ttk主题按钮

```python
from tkinter import ttk
import tkinter as tk

# 按钮样式配置
BUTTON_STYLES = {
    'primary': {
        'style': 'primary.TButton',
        'bg': '#667eea',
        'fg': 'white',
        'hover': '#5a71d6'
    },
    'success': {
        'style': 'success.TButton',
        'bg': '#48bb78',
        'fg': 'white',
        'hover': '#3da066'
    },
    'danger': {
        'style': 'danger.TButton',
        'bg': '#fc8181',
        'fg': 'white',
        'hover': '#e66b6b'
    },
    'warning': {
        'style': 'warning.TButton',
        'bg': '#f6ad55',
        'fg': 'black',
        'hover': '#e69a3d'
    },
    'info': {
        'style': 'info.TButton',
        'bg': '#63b3ed',
        'fg': 'white',
        'hover': '#4aa3db'
    }
}

def setup_button_styles(style):
    """配置按钮样式"""
    for name, config in BUTTON_STYLES.items():
        style.configure(
            config['style'],
            font=('Microsoft YaHei', 10, 'bold'),
            foreground=config['fg'],
            background=config['bg'],
            padding=(15, 8),
            relief='flat',
            borderwidth=0
        )
        style.map(
            config['style'],
            background=[('active', config['hover']), ('pressed', config['hover'])],
            foreground=[('active', config['fg']), ('pressed', config['fg'])]
        )
```

---

## 3. PyQt/PySide按钮图标

### 使用QIcon.fromTheme

```python
from PySide6.QtWidgets import QPushButton, QStyleFactory
from PySide6.QtGui import QIcon, QPalette, QColor
from PySide6.QtCore import Qt

def create_icon_button(text, icon_name=None, style='primary'):
    """创建带图标的按钮"""
    btn = QPushButton(text)
    
    if icon_name:
        # 使用系统主题图标
        btn.setIcon(QStyle.StandardPixmap.SP_DirHomeIcon)
    
    # 根据样式设置样式表
    styles = {
        'primary': """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border-radius: 14px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background: #7c8ff0; }
            QPushButton:pressed { padding-top: 12px; }
        """,
        'success': """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
                color: white;
                border-radius: 14px;
                padding: 10px 20px;
                font-weight: bold;
            }
        """,
        'danger': """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fc8181, stop:1 #f56565);
                color: white;
                border-radius: 14px;
                padding: 10px 20px;
                font-weight: bold;
            }
        """
    }
    btn.setStyleSheet(styles.get(style, styles['primary']))
    return btn
```

---

## 4. 常用图标路径配置

### 项目级图标配置

```python
# 项目图标配置模板
ICON_CONFIG = {
    'app_icon': {
        'path': 'assets/app_icon.ico',
        'description': '应用程序图标'
    },
    'toolbar': {
        'open': 'assets/icons/open.png',
        'save': 'assets/icons/save.png',
        'settings': 'assets/icons/settings.png',
        'help': 'assets/icons/help.png'
    },
    'status': {
        'success': 'assets/icons/success.png',
        'warning': 'assets/icons/warning.png',
        'error': 'assets/icons/error.png'
    }
}

# 图标加载工具函数
import os

def load_icon(icon_path, base_dir=None):
    """加载图标文件"""
    if base_dir:
        icon_path = os.path.join(base_dir, icon_path)
    
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return QIcon()  # 返回空图标

def get_icon_path(name, icon_config=ICON_CONFIG):
    """获取图标路径"""
    for category in icon_config.values():
        if name in category:
            return category[name]
    return None
```

---

## 5. SVG图标（内联）

### 小图标SVG模板

```python
# SVG图标模板（可直接嵌入HTML或转换为QPixmap）
SVG_ICONS = {
    'loading': '''
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2">
            <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
            <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round">
                <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
            </path>
        </svg>
    ''',
    'check': '''
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#48bb78" stroke-width="3" stroke-linecap="round">
            <polyline points="20 6 9 17 4 12"/>
        </svg>
    ''',
    'warning': '''
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f6ad55" stroke-width="2">
            <path d="M12 9v4m0 4h.01M12 2L2 22h20L12 2z"/>
        </svg>
    ''',
    'error': '''
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fc8181" stroke-width="2" stroke-linecap="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
        </svg>
    '''
}
```

---

## 6. Emoji按钮（简单方案）

### Tkinter Emoji按钮

```python
class EmojiButton(tk.Button):
    """Emoji按钮"""
    
    EMOJI_MAP = {
        'open': '📂',
        'save': '💾',
        'add': '➕',
        'delete': '🗑️',
        'run': '▶️',
        'stop': '⏹️',
        'settings': '⚙️',
        'help': '❓',
        'export': '📤',
        'import': '📥',
        'refresh': '🔄',
        'search': '🔍'
    }
    
    def __init__(self, master, emoji_key, text='', command=None, **kwargs):
        emoji = self.EMOJI_MAP.get(emoji_key, '📄')
        display_text = f"{emoji} {text}" if text else emoji
        super().__init__(
            master, text=display_text, command=command,
            font=('Microsoft YaHei', 10),
            **kwargs
        )

# 使用示例
btn_open = EmojiButton(root, 'open', '打开文件', command=open_file)
btn_save = EmojiButton(root, 'save', '保存', command=save_file)
btn_add = EmojiButton(root, 'add', '添加', command=add_item)
```

---

## 7. 状态栏图标

```python
class StatusBar:
    """状态栏组件"""
    
    STATUS_COLORS = {
        'ready': '#48bb78',      # 绿色
        'processing': '#f6ad55', # 橙色
        'error': '#fc8181',      # 红色
        'idle': '#a0aec0'        # 灰色
    }
    
    STATUS_TEXTS = {
        'ready': '就绪',
        'processing': '处理中...',
        'error': '错误',
        'idle': '空闲'
    }
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='#f0f4f8', height=30)
        self.frame.pack(side='bottom', fill='x')
        
        self.label = tk.Label(
            self.frame, text='就绪',
            font=('Microsoft YaHei', 9),
            bg='#f0f4f8', fg='#718096'
        )
        self.label.pack(side='left', padx=10)
        
        self.indicator = tk.Label(
            self.frame, text='●',
            font=('Arial', 12),
            bg='#f0f4f8', fg='#48bb78'
        )
        self.indicator.pack(side='left', padx=(5, 0))
    
    def set_status(self, status):
        """设置状态"""
        color = self.STATUS_COLORS.get(status, '#a0aec0')
        text = self.STATUS_TEXTS.get(status, status)
        self.indicator.config(fg=color)
        self.label.config(text=text, fg='#4a5568' if status == 'ready' else color)
```

---

## 8. 工具栏按钮组

```python
class ToolBar:
    """工具栏组件"""
    
    def __init__(self, parent, buttons_config):
        """
        buttons_config: [
            {'key': 'open', 'text': '打开', 'icon': '📂', 'command': func},
            {'key': 'save', 'text': '保存', 'icon': '💾', 'command': func},
            ...
        ]
        """
        self.frame = tk.Frame(parent, bg='#f8f9fa', height=50)
        self.frame.pack(side='top', fill='x')
        self.frame.pack_propagate(False)
        
        self.buttons = {}
        for config in buttons_config:
            btn = EmojiButton(
                self.frame,
                emoji_key=config.get('icon'),
                text=config.get('text', ''),
                command=config.get('command'),
                bg='#f8f9fa',
                relief='flat',
                padx=12, pady=5
            )
            btn.pack(side='left', padx=5, pady=5)
            self.buttons[config['key']] = btn
    
    def enable(self, key):
        """启用按钮"""
        if key in self.buttons:
            self.buttons[key].config(state='normal')
    
    def disable(self, key):
        """禁用按钮"""
        if key in self.buttons:
            self.buttons[key].config(state='disabled')
```

---

## 9. 快速参考表

### 常用Emoji速查

```
文件操作: 📂 📁 📄 📝 💾 📤 📥 🗂️
操作按钮: ➕ ➖ ✏️ 🗑️ 🔄 ↻ 🔍
状态指示: ✅ ❌ ⚠️ ℹ️ ⏳ ⭕ 🔵
图表数据: 📊 📈 📉 📋 📌 📍
时间相关: ⏰ ⏱️ ⏺️ 📅 🗓️
通讯相关: 📧 📞 📱 💬 🔔
系统相关: ⚙️ 🔧 🖥️ 💻 ⌨️ 🖱️
```
