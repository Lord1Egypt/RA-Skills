# python-matplotlib-chinese-font

**Python matplotlib 中文字体配置解决方案**

---

## 📌 问题描述

**matplotlib 默认不支持中文，中文会显示为方块/方框**

控制台警告：
```
UserWarning: Glyph XXXXX missing from current font
```

**根本原因**：matplotlib 的默认字体不包含中文字符。

---

## 🎯 使用场景

**当以下情况时使用此 Skill**：
1. ✅ matplotlib 绑图中中文显示为方框/乱码
2. ✅ 需要配置中文字体
3. ✅ 负号显示为方框
4. ✅ 图例、标题、坐标轴标签中文显示异常
5. ✅ 跨平台字体兼容问题
6. ✅ 字体路径配置问题
7. ✅ 字体缓存问题

---

## 🚀 快速开始

### 第 0 步：下载字体文件

```bash
# 创建字体目录
mkdir -p fonts

# 下载 BabelStoneHan 字体（约 50MB）
curl -L -o fonts/BabelStoneHan.ttf "https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf"

# 或者使用 wget
wget -O fonts/BabelStoneHan.ttf "https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf"
```

**其他字体选择**（小于 10MB）：
- **WenQuanYi Micro Hei** (文泉驿微米黑) - 约 4MB
- **SimHei** (黑体) - 系统自带
- **Microsoft YaHei** (微软雅黑) - Windows 系统自带

### 方法 1：复制模板（推荐）

```bash
# 复制配置模板到你的项目
cp ~/.openclaw/skills/python-matplotlib-chinese-font/templates/setup_font.py ./
```

### 方法 2：直接使用字体文件

```python
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 字体文件路径（请修改为你的实际路径）
font_file = './fonts/BabelStoneHan.ttf'

# 关键：显式添加字体
fm.fontManager.addfont(font_file)

# 创建 FontProperties
font_prop = fm.FontProperties(fname=font_file)

# 设置全局字体
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# 使用
fig, ax = plt.subplots()
ax.set_title('中文标题', fontproperties=font_prop)
ax.set_xlabel('横轴', fontproperties=font_prop)
ax.legend(['图例'], prop=font_prop)
```

---

## 📋 完整配置代码（3 步）

### **第 1 步：下载并准备字体文件**

```bash
# 创建字体目录
mkdir -p fonts

# 下载 BabelStoneHan 字体
curl -L -o fonts/BabelStoneHan.ttf "https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf"
```

**项目结构**：
```
your_project/
├── fonts/
│   └── BabelStoneHan.ttf  ← 中文字体文件（需自行下载）
├── scripts/
│   └── your_script.py
└── ...
```

**字体推荐**：
- `BabelStoneHan.ttf`（开源，支持中文）← **需自行下载**，约 50MB
- `SimHei.ttf`（黑体）- 系统自带
- `Microsoft YaHei.ttf`（微软雅黑）- Windows 系统自带
- `WenQuanYi Micro Hei`（文泉驿微米黑）- 约 4MB

---

### **第 2 步：配置字体**

```python
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 字体文件相对于脚本的路径
_FONT_FILE_RELATIVE = os.path.join('..', '..', 'fonts', 'BabelStoneHan.ttf')

def _get_font_path():
    """获取字体文件的绝对路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_file = os.path.join(script_dir, _FONT_FILE_RELATIVE)
    return os.path.normpath(font_file)

def setup_chinese_font():
    """配置中文字体（兼容所有 matplotlib 版本）"""
    font_file = _get_font_path()
    
    if os.path.exists(font_file):
        # 创建 FontProperties
        font_prop = fm.FontProperties(fname=font_file)
        font_name = font_prop.get_name()
        
        # 注册字体（兼容新旧版本 matplotlib）
        try:
            # 方法1：matplotlib 3.2+ 使用 addfont
            if hasattr(fm.fontManager, 'addfont'):
                fm.fontManager.addfont(font_file)
            else:
                # 方法2：旧版本 matplotlib，手动添加到字体列表
                try:
                    fm.fontManager.ttflist.append(fm.FontEntry(
                        fname=font_file,
                        name=font_name,
                        style=font_prop.get_style(),
                        variant=font_prop.get_variant(),
                        weight=font_prop.get_weight(),
                        stretch=font_prop.get_stretch(),
                        size=font_prop.get_size()
                    ))
                except Exception:
                    pass
        except Exception:
            pass
        
        # 设置全局字体
        plt.rcParams['font.family'] = font_name
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        return font_prop
    
    return fm.FontProperties()
```

**⚠️ 版本兼容性说明**：

| matplotlib 版本 | 方法 | 说明 |
|----------------|------|------|
| **≥ 3.2** | `fontManager.addfont()` | 推荐方法 |
| **< 3.2** | `fontManager.ttflist.append()` | 兼容方法 |
        
        # 创建 FontProperties
        font_prop = fm.FontProperties(fname=font_file)
        
        # 设置全局字体
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        print(f"✅ 已加载中文字体: {font_file}")
        return font_prop
    else:
        print(f"⚠️ 未找到字体文件: {font_file}")
        return fm.FontProperties()

# 使用
chinese_font = setup_chinese_font()
```

---

### **第 3 步：在绑图时使用字体**

#### **方法 A：全局设置（推荐）**

```python
# 配置字体
chinese_font = setup_chinese_font()

# 绑图时自动使用全局字体
fig, ax = plt.subplots()
ax.set_title('中文标题')  # 自动使用全局字体
ax.set_xlabel('横轴标签')
ax.legend(['图例1', '图例2'])
```

#### **方法 B：局部指定（精确控制）**

```python
# 配置字体
chinese_font = setup_chinese_font()

# 绑图时显式指定 fontproperties
fig, ax = plt.subplots()
ax.set_title('中文标题', fontproperties=chinese_font)
ax.set_xlabel('横轴标签', fontproperties=chinese_font)
ax.legend(['图例1', '图例2'], prop=chinese_font)
```

---

## 🎯 核心要点（5 个关键点）

### **1. 字体文件路径**

```python
# ❌ 错误：使用运行目录
font_file = os.path.join(os.getcwd(), 'fonts', 'BabelStoneHan.ttf')

# ✅ 正确：使用脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
font_file = os.path.join(script_dir, '..', '..', 'fonts', 'BabelStoneHan.ttf')
font_file = os.path.normpath(font_file)  # 规范化路径
```

### **2. 显式添加字体（最关键！）**

```python
# ❌ 错误：直接创建 FontProperties
font_prop = fm.FontProperties(fname=font_file)

# ✅ 正确：先 addfont，再创建 FontProperties
fm.fontManager.addfont(font_file)  # 关键！
font_prop = fm.FontProperties(fname=font_file)
```

### **3. 设置全局字体**

```python
# 设置全局字体
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
```

### **4. 使用绝对路径**

```python
# ✅ 使用 os.path.normpath() 规范化路径
font_file = os.path.normpath(font_file)

# ✅ 检查文件是否存在
if os.path.exists(font_file):
    fm.fontManager.addfont(font_file)
```

### **5. 字体文件在项目内**

```
✅ 优点：
- 不依赖系统字体
- 可移植性好
- 跨平台兼容

❌ 避免：
- 使用系统字体路径（/usr/share/fonts/...）
- 假设字体已安装
```

---

## 🚨 常见问题

### **问题 1：中文显示为方框**

**原因**：没有调用 `addfont()` 显式添加字体

**解决**：
```python
# ✅ 必须先调用 addfont
fm.fontManager.addfont(font_file)
font_prop = fm.FontProperties(fname=font_file)
```

---

### **问题 2：负号显示为方框**

**原因**：字体不支持负号

**解决**：
```python
plt.rcParams['axes.unicode_minus'] = False
```

---

### **问题 3：字体路径错误**

**原因**：使用 `os.getcwd()` 而不是脚本所在目录

**解决**：
```python
# ✅ 使用脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
```

---

### **问题 4：图片已生成但中文仍是方框**

**原因**：代码修改有误或发送了旧图片

**解决**：
1. 删除旧图片：`rm -f output.png`
2. 重新运行脚本
3. 检查图片修改时间：`stat output.png | grep Modify`

---

### **问题 6：`'FontManager' object has no attribute 'addfont'`**

**原因**：`fontManager.addfont()` 是 matplotlib 3.2+ 才有的方法

**解决**：使用版本兼容性检查
```python
# 兼容所有 matplotlib 版本
if hasattr(fm.fontManager, 'addfont'):
    # matplotlib 3.2+
    fm.fontManager.addfont(font_file)
else:
    # matplotlib < 3.2
    try:
        fm.fontManager.ttflist.append(fm.FontEntry(...))
    except Exception:
        pass
```

**检查 matplotlib 版本**：
```python
import matplotlib
print(matplotlib.__version__)
```

---

### **问题 7：字体缓存问题**

**原因**：matplotlib 缓存了旧字体配置

**解决**：
```python
# 清除字体缓存
try:
    fm._load_fontmanager(try_read_cache=False)
except:
    pass
```

---

## 📊 对比总结

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **字体文件在项目内** | 可移植、跨平台 | 需要管理字体文件 | ⭐⭐⭐⭐⭐ |
| **使用系统字体** | 无需管理文件 | 依赖系统、不可移植 | ⭐⭐ |
| **临时下载字体** | 自动化 | 网络依赖、速度慢 | ⭐⭐⭐ |

---

## 📁 Skill 包含内容

```
python-matplotlib-chinese-font/
├── SKILL.md                    # Skill 说明文档（本文件）
├── references/
│   ├── plot_utils.py          # 完整工具模块
│   └── test_chinese_font.py   # 测试代码
└── templates/
    └── setup_font.py          # 配置模板（可直接复制）

⚠️ 字体文件需自行下载，详见"第 0 步：下载字体文件"
```

---

## 📚 参考代码

### **完整工具模块**：`references/plot_utils.py`
- ✅ 完整的字体配置函数
- ✅ 可直接导入使用
- ✅ 包含常用绘图参数

### **测试代码**：`references/test_chinese_font.py`
- ✅ 4 种测试场景
- ✅ 验证中文显示是否正常
- ✅ 包含负数测试

### **配置模板**：`templates/setup_font.py`
- ✅ 可直接复制到项目
- ✅ 只需修改字体路径

---

## 💡 最佳实践

```python
# ✅ 推荐配置
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 1. 字体路径（相对于脚本）
_FONT_FILE_RELATIVE = os.path.join('..', '..', 'fonts', 'BabelStoneHan.ttf')

# 2. 获取绝对路径
def _get_font_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_file = os.path.join(script_dir, _FONT_FILE_RELATIVE)
    return os.path.normpath(font_file)

# 3. 配置字体
def setup_chinese_font():
    font_file = _get_font_path()
    
    if os.path.exists(font_file):
        fm.fontManager.addfont(font_file)  # 关键！
        font_prop = fm.FontProperties(fname=font_file)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        return font_prop
    
    return fm.FontProperties()

# 4. 使用
chinese_font = setup_chinese_font()
```

---

## 🔗 相关链接

- **BabelStone Fonts**: https://www.babelstone.co.uk/Fonts/Han.html
- **Matplotlib Font Management**: https://matplotlib.org/stable/api/font_manager_api.html
- **Matplotlib Chinese Font Guide**: https://matplotlib.org/stable/tutorials/text/text_intro.html

---

## 📝 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| **v1.0.0** | 2026-03-21 | 初始版本 - BabelStoneHan 字体配置方案 |
| **v1.1.0** | 2026-03-21 | 添加 matplotlib 版本兼容性支持 |
| **v1.2.0** | 2026-04-02 | 字体文件改为用户自行下载（满足 clawhub 文件大小限制） |

---

**Skill 创建时间**：2026-03-21  
**维护者**：太子  
**当前版本**：v1.2.0
