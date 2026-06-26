# Sum2Slides Lite 平台兼容性说明
# 版本: 1.0.1 (安全修复版)

## 🎯 概述

本文档详细说明 Sum2Slides Lite 在不同操作系统和软件环境下的兼容性情况。

## 📊 平台支持矩阵

### **操作系统支持**
| 操作系统 | 版本要求 | 支持程度 | 备注 |
|----------|----------|----------|------|
| **macOS** | 10.15+ | ✅ 完整支持 | 支持所有功能，包括AppleScript自动化 |
| **Windows** | 10+ | ✅ 基础支持 | 支持核心功能，无AppleScript |
| **Linux** | Ubuntu 18.04+ | ✅ 基础支持 | 支持核心功能，无AppleScript |

### **PPT软件支持**
| 软件 | 版本要求 | macOS | Windows | Linux | 备注 |
|------|----------|-------|---------|-------|------|
| **Microsoft PowerPoint** | 2016+ | ✅ 完整 | ✅ 完整 | ❌ 不支持 | 需要安装 |
| **WPS Office** | 10.0+ | ✅ 完整 | ✅ 完整 | ✅ 完整 | 推荐跨平台使用 |

### **功能支持矩阵**
| 功能 | macOS | Windows | Linux | 说明 |
|------|-------|---------|-------|------|
| **对话分析** | ✅ 完整 | ✅ 完整 | ✅ 完整 | 核心功能，全平台 |
| **PPT生成** | ✅ 完整 | ✅ 完整 | ✅ 完整 | 使用python-pptx |
| **飞书上传** | ✅ 可选 | ✅ 可选 | ✅ 可选 | 需要网络权限 |
| **AppleScript自动化** | ✅ 可选 | ❌ 不支持 | ❌ 不支持 | macOS特有 |
| **本地文件保存** | ✅ 完整 | ✅ 完整 | ✅ 完整 | 核心功能 |

## 🍎 macOS 平台详情

### **支持的功能**
1. ✅ **完整PPT生成** - 使用python-pptx库
2. ✅ **AppleScript自动化** - 控制PowerPoint/WPS
3. ✅ **飞书上传** - 网络功能
4. ✅ **本地保存** - 文件系统操作

### **系统要求**
- **操作系统**: macOS 10.15 (Catalina) 或更高
- **Python**: 3.7 或更高
- **内存**: 4GB RAM 或更多
- **磁盘空间**: 100MB 可用空间

### **权限要求**
```markdown
必需权限:
1. 文件系统权限 - 保存PPT文件

可选权限:
1. AppleScript自动化权限 - 控制PPT软件
   - 系统偏好设置 → 安全性与隐私 → 隐私 → 自动化
   - 需要用户手动授权

2. 网络权限 - 飞书上传
   - 系统提示时授权
   - 可以随时撤销
```

### **已知限制**
1. **AppleScript权限**: 需要用户手动在系统设置中授权
2. **沙盒限制**: 某些目录可能无法访问
3. **系统版本**: 旧版本macOS可能不支持某些功能

## 🪟 Windows 平台详情

### **支持的功能**
1. ✅ **完整PPT生成** - 使用python-pptx库
2. ✅ **飞书上传** - 网络功能
3. ✅ **本地保存** - 文件系统操作
4. ⚠️ **无AppleScript** - 使用标准生成模式

### **系统要求**
- **操作系统**: Windows 10 或更高
- **Python**: 3.7 或更高
- **内存**: 4GB RAM 或更多
- **磁盘空间**: 100MB 可用空间

### **权限要求**
```markdown
必需权限:
1. 文件系统权限 - 保存PPT文件

可选权限:
1. 网络权限 - 飞书上传
   - Windows防火墙可能提示
   - 可以配置例外规则
```

### **已知限制**
1. **无AppleScript**: Windows不支持AppleScript
2. **路径分隔符**: 使用反斜杠 `\` 作为路径分隔符
3. **权限模型**: 不同的权限管理方式

## 🐧 Linux 平台详情

### **支持的功能**
1. ✅ **完整PPT生成** - 使用python-pptx库
2. ✅ **飞书上传** - 网络功能
3. ✅ **本地保存** - 文件系统操作
4. ⚠️ **无AppleScript** - 使用标准生成模式

### **系统要求**
- **操作系统**: Ubuntu 18.04+ / CentOS 7+ / 其他主流发行版
- **Python**: 3.7 或更高
- **内存**: 4GB RAM 或更多
- **磁盘空间**: 100MB 可用空间

### **权限要求**
```markdown
必需权限:
1. 文件系统权限 - 保存PPT文件 (用户目录)

可选权限:
1. 网络权限 - 飞书上传
   - 可能需要配置防火墙
```

### **已知限制**
1. **无AppleScript**: Linux不支持AppleScript
2. **PPT软件**: 需要安装WPS Office或使用Web版本
3. **字体支持**: 可能需要安装中文字体

## 🔧 跨平台兼容性设计

### **1. 核心功能兼容**
```python
# 所有平台都支持的核心功能
def generate_ppt(content, template="business"):
    """跨平台PPT生成函数"""
    from pptx import Presentation  # 跨平台库
    
    prs = Presentation()
    # 标准PPT生成逻辑
    return prs
```

### **2. 平台特有功能**
```python
import platform

def get_platform_specific_features():
    """获取平台特有功能"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return {
            "applescript": True,
            "automation": True
        }
    elif system == "Windows":
        return {
            "com_automation": False,  # 未来支持
            "applescript": False
        }
    else:  # Linux
        return {
            "libreoffice": False,  # 未来支持
            "applescript": False
        }
```

### **3. 优雅降级机制**
```python
def save_ppt_with_fallback(prs, file_path):
    """带降级机制的保存函数"""
    try:
        # 尝试使用AppleScript保存 (macOS)
        if platform.system() == "Darwin" and has_applescript_permission():
            return save_with_applescript(prs, file_path)
    except PermissionError:
        print("⚠️ AppleScript权限不足，使用标准保存")
    
    # 降级到标准保存
    return save_standard(prs, file_path)
```

## 🚀 最佳实践建议

### **macOS 用户**
```markdown
推荐配置:
1. 软件: PowerPoint 或 WPS Office
2. 权限: 根据需要授权AppleScript
3. 输出目录: ~/Desktop/Sum2Slides
4. 网络: 按需启用飞书上传
```

### **Windows 用户**
```markdown
推荐配置:
1. 软件: PowerPoint 或 WPS Office
2. 输出目录: C:\Users\<用户名>\Desktop\Sum2Slides
3. 网络: 按需启用飞书上传
4. 注意: 使用标准生成模式
```

### **Linux 用户**
```markdown
推荐配置:
1. 软件: WPS Office (推荐) 或 LibreOffice
2. 输出目录: ~/Desktop/Sum2Slides
3. 网络: 按需启用飞书上传
4. 字体: 安装必要的中文字体
```

## ⚠️ 常见问题与解决方案

### **问题1: AppleScript权限不足 (macOS)**
**症状**: "无法控制应用程序" 错误
**解决**:
1. 打开系统偏好设置 → 安全性与隐私 → 隐私 → 自动化
2. 添加 PowerPoint 或 WPS Office 到允许列表
3. 或者使用标准生成模式 (无需权限)

### **问题2: 网络连接失败**
**症状**: 飞书上传失败
**解决**:
1. 检查网络连接
2. 检查防火墙设置
3. 验证API凭证
4. 或仅使用本地保存功能

### **问题3: 文件保存失败**
**症状**: 无法保存PPT文件
**解决**:
1. 检查输出目录权限
2. 尝试其他目录
3. 检查磁盘空间
4. 检查文件是否被占用

### **问题4: 平台特有功能不可用**
**症状**: 某些功能在其他平台不可用
**解决**:
1. 查看本兼容性文档
2. 使用跨平台兼容的功能
3. 考虑使用其他平台

## 🔄 未来平台支持计划

### **短期计划 (3个月内)**
1. **Windows COM自动化** - 增强Windows支持
2. **Linux LibreOffice集成** - 增强Linux支持
3. **Web版本支持** - 浏览器扩展

### **中期计划 (6个月内)**
1. **移动端支持** - iOS/Android应用
2. **云服务集成** - 更多云存储支持
3. **协作功能** - 团队协作支持

### **长期计划 (1年内)**
1. **跨平台统一体验**
2. **AI增强功能**
3. **企业级功能**

## 📞 平台支持联系

### **macOS 问题**
- **渠道**: GitHub Issues (标签: macos)
- **优先级**: 高
- **响应时间**: 24小时内

### **Windows 问题**
- **渠道**: GitHub Issues (标签: windows)
- **优先级**: 高
- **响应时间**: 24小时内

### **Linux 问题**
- **渠道**: GitHub Issues (标签: linux)
- **优先级**: 中
- **响应时间**: 48小时内

## 🎯 总结

Sum2Slides Lite 设计时考虑了跨平台兼容性：

1. ✅ **核心功能全平台支持** - 对话分析、PPT生成、文件保存
2. ✅ **平台特有功能明确标注** - AppleScript仅限macOS
3. ✅ **优雅降级机制** - 无平台特有功能时自动降级
4. ✅ **详细文档说明** - 明确的兼容性说明

**我们致力于为所有平台的用户提供优秀的体验！** 🌍