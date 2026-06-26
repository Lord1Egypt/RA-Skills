# Windows UI 控制教程

## 📚 什么是 pywinauto？

### 定义

**pywinauto** 是一个 Python 库，用于自动化控制 Windows 应用程序。

### 它能做什么？

- ✅ 扫描窗口所有控件（按钮、输入框、菜单、列表等）
- ✅ 点击任意按钮
- ✅ 输入文字到输入框
- ✅ 选择菜单项
- ✅ 拖放文件
- ✅ 等待窗口/控件出现
- ✅ 验证控件状态

### 适用场景

- 微信/QQ 自动发消息
- 网易云音乐自动播放
- 百度网盘自动下载
- 软件自动化测试
- 重复性操作自动化

---

## 🛠️ 安装 pywinauto

### 方法 1: 在线安装（推荐）

```bash
pip install pywinauto
```

### 方法 2: 手动下载安装

**下载地址：**
- **官方 PyPI**: https://pypi.org/project/pywinauto/#files
- **GitHub**: https://github.com/pywinauto/pywinauto/releases

**下载文件：**
- `pywinauto-0.6.9-py2.py3-none-any.whl`
- `six-1.17.0-py2.py3-none-any.whl` (依赖)
- `comtypes-1.4.16-py3-none-any.whl` (依赖)
- `pywin32-311-cp312-cp312-win_amd64.whl` (依赖)

**离线安装：**
```bash
cd 下载的文件夹
pip install --no-index --find-links=. pywinauto
```

### 验证安装

```python
from pywinauto import Desktop
print("安装成功！")
```

### 系统要求

- **操作系统**: Windows 10/11
- **Python**: 3.8 或更高版本
- **权限**: 某些应用需要管理员权限

---

## 🚀 快速开始

### 第一步：导入库

```python
from pywinauto import Desktop
import time
```

### 第二步：创建 Desktop 对象

```python
# 使用 UIA 后端（推荐，支持现代应用）
desktop = Desktop(backend='uia')

# 或者使用 win32 后端（老应用）
# desktop = Desktop(backend='win32')
```

### 第三步：扫描窗口

```python
# 列出所有窗口
for w in desktop.windows():
    title = w.window_text()
    if title:
        print(f'窗口：{title}')
```

### 第四步：找到目标窗口

```python
# 方法 1: 遍历查找
for w in desktop.windows():
    if '微信' in w.window_text():
        target_window = w
        break

# 方法 2: 直接连接
# app = Desktop(backend='uia').connect(title='微信')
```

### 第五步：扫描控件

```python
# 扫描窗口所有控件
for ctrl in target_window.descendants():
    info = ctrl.element_info
    if info.name:  # 只显示有名字的控件
        print(f'[{info.control_type}] {info.name}')
```

### 第六步：操作控件

```python
# 点击按钮
button.click_input()

# 输入文字
edit_box.set_focus()
edit_box.type_keys('你好世界')

# 选择菜单
menu_item.select()
```

---

## 💡 完整示例

### 示例 1: 列出所有窗口

```python
from pywinauto import Desktop

desktop = Desktop(backend='uia')

print('=== 当前所有窗口 ===\n')
for w in desktop.windows():
    title = w.window_text()
    if title:
        rect = w.element_info.rectangle
        print(f'{title}')
        print(f'  位置：{rect.left}x{rect.top} - {rect.right}x{rect.bottom}')
        print(f'  尺寸：{rect.right - rect.left}x{rect.bottom - rect.top}')
```

### 示例 2: 扫描微信窗口

```python
from pywinauto import Desktop

desktop = Desktop(backend='uia')

print('=== 扫描微信窗口 ===\n')

for w in desktop.windows():
    if '微信' in w.window_text():
        print(f'窗口：{w.window_text()}\n')
        
        # 扫描所有控件
        for ctrl in w.descendants():
            info = ctrl.element_info
            if info.name:  # 只显示有名字的控件
                print(f'[{info.control_type}] {info.name}')
        
        break
```

### 示例 3: 点击按钮

```python
from pywinauto import Desktop

desktop = Desktop(backend='uia')

for w in desktop.windows():
    if '微信' in w.window_text():
        # 查找发送按钮
        for ctrl in w.descendants():
            info = ctrl.element_info
            if info.control_type == 'Button' and '发送' in info.name:
                print(f'找到发送按钮：{info.name}')
                ctrl.click_input()
                print('已点击！')
                break
        break
```

### 示例 4: 输入文字

```python
from pywinauto import Desktop
import time

desktop = Desktop(backend='uia')

for w in desktop.windows():
    if '微信' in w.window_text():
        # 查找输入框
        for ctrl in w.descendants():
            info = ctrl.element_info
            if info.control_type == 'Edit':
                print(f'找到输入框：{info.name}')
                
                # 聚焦并输入
                ctrl.set_focus()
                time.sleep(0.3)
                ctrl.type_keys('你好世界', with_spaces=True)
                print('输入完成！')
                break
        break
```

---

## ⚠️ 注意事项

### 1. 编码问题（重要！）

**问题**: 输出中文乱码

**解决**: 脚本开头添加

```python
import sys
import io
# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

### 2. 权限问题

**问题**: 某些软件需要管理员权限

**解决**: 用管理员身份运行 Python

```bash
# Windows 右键 → 以管理员身份运行
```

### 3. 等待 UI 加载

**问题**: 操作太快，UI 还没加载

**解决**: 添加等待时间

```python
import time

# 操作后等待
ctrl.click_input()
time.sleep(1)  # 等待 1 秒

# 或者等待特定窗口出现
from pywinauto import Application
app = Application(backend='uia').wait('ready', timeout=10)
```

### 4. 控件找不到

**可能原因**:
- 窗口标题不对
- 后端选错了（uia vs win32）
- 控件还没加载
- 权限不足

**解决方法**:
```python
# 1. 打印所有窗口，确认标题
for w in desktop.windows():
    print(w.window_text())

# 2. 尝试不同后端
desktop = Desktop(backend='win32')  # 试试 win32

# 3. 等待加载
time.sleep(2)

# 4. 以管理员身份运行
```

### 5. 位置计算

**获取控件相对位置**:

```python
win_rect = window.element_info.rectangle
ctrl_rect = ctrl.element_info.rectangle

# 计算相对位置（百分比）
rel_top = (ctrl_rect.top - win_rect.top) / (win_rect.bottom - win_rect.top) * 100
rel_left = (ctrl_rect.left - win_rect.left) / (win_rect.right - win_rect.left) * 100

print(f'位置：top={rel_top:.1f}%, left={rel_left:.1f}%')
```

---

## 🎯 最佳实践

### 1. 每步验证

```python
# ❌ 错误：不验证直接继续
ctrl.click_input()
# 假设点击成功了...

# ✅ 正确：验证后再继续
ctrl.click_input()
time.sleep(0.5)
# 检查窗口状态，确认点击成功
```

### 2. 智能等待

```python
# ❌ 错误：固定等待太久
time.sleep(5)

# ✅ 正确：等待特定条件
from pywinauto import Application
app.wait('ready', timeout=10)  # 最多等 10 秒
```

### 3. 异常处理

```python
try:
    ctrl.click_input()
    print('点击成功')
except Exception as e:
    print(f'点击失败：{e}')
    # 尝试其他方法
```

### 4. 记录操作历史

```python
history = []

def safe_click(ctrl, name):
    try:
        ctrl.click_input()
        history.append({'action': 'click', 'target': name, 'success': True})
        return True
    except:
        history.append({'action': 'click', 'target': name, 'success': False})
        return False
```

---

## 📚 常用 API 参考

### Desktop 类

```python
from pywinauto import Desktop

desktop = Desktop(backend='uia')

# 列出所有窗口
desktop.windows()

# 连接已有窗口
desktop.connect(title='微信')

# 启动应用
desktop.start('notepad.exe')
```

### Window 类

```python
# 获取窗口信息
window.window_text()
window.element_info.rectangle  # 位置
window.element_info.control_type  # 类型

# 关闭窗口
window.close()

# 最小化/最大化
window.minimize()
window.maximize()

# 扫描控件
window.children()  # 直接子控件
window.descendants()  # 所有后代控件
```

### Control 类

```python
# 获取控件信息
ctrl.element_info.name  # 名称
ctrl.element_info.control_type  # 类型
ctrl.element_info.class_name  # 类名
ctrl.element_info.rectangle  # 位置

# 操作控件
ctrl.click_input()  # 点击
ctrl.double_click_input()  # 双击
ctrl.right_click_input()  # 右键
ctrl.set_focus()  # 聚焦
ctrl.type_keys('文字')  # 输入
ctrl.select()  # 选择（菜单项）
```

---

## 🔍 调试技巧

### 1. 打印所有控件

```python
for i, ctrl in enumerate(window.descendants()):
    info = ctrl.element_info
    print(f'{i}. [{info.control_type}] {info.name}')
```

### 2. 使用 Spy 工具

Windows 自带 **Inspect.exe** 或 **Accessibility Insights**

```bash
# 位置
C:\Program Files (x86)\Windows Kits\10\bin\Inspect.exe
```

### 3. 截图标注

```python
# 使用 see() 方法（需要额外配置）
# 或者手动截图对比
```

---

## 📖 学习资源

- **官方文档**: https://pywinauto.readthedocs.io/
- **GitHub**: https://github.com/pywinauto/pywinauto
- **示例代码**: https://github.com/pywinauto/pywinauto/tree/master/pywinauto/tests
- **UI Automation 文档**: https://docs.microsoft.com/windows/win32/winauto/uiautooverview

---

## ❓ 常见问题

### Q: pywinauto 支持 Mac/Linux 吗？
**A**: 不支持，只支持 Windows。

### Q: 能控制网页吗？
**A**: 部分支持，但推荐用 Selenium 控制网页。

### Q: 能控制游戏吗？
**A**: 大部分游戏不行（自定义渲染），但可以用图像识别。

### Q: 为什么点击没反应？
**A**: 可能是权限问题，尝试用管理员身份运行。

### Q: 为什么输出乱码？
**A**: 编码问题，添加 UTF-8 设置（见注意事项）。

---

**版本**: 1.0.0  
**更新时间**: 2026-03-30  
**适用**: Python 3.8+, Windows 10/11
