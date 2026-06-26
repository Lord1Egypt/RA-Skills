#!/usr/bin/env python3
"""
setup_font.py - matplotlib 中文字体配置模板

使用方法：
0. 先下载字体文件（首次使用）：
   mkdir -p fonts
   curl -L -o fonts/BabelStoneHan.ttf "https://www.babelstone.co.uk/Fonts/Download/BabelStoneHan.ttf"

1. 复制此文件到你的项目
2. 修改 _FONT_FILE_RELATIVE 路径
3. 在你的代码中导入并调用 setup_chinese_font()

示例：
    from setup_font import setup_chinese_font
    chinese_font = setup_chinese_font()
    
    # 使用全局字体（推荐）
    ax.set_title('中文标题')
    
    # 或显式指定（精确控制）
    ax.set_title('中文标题', fontproperties=chinese_font)
"""

import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm


# ============================================================================
# 字体文件路径配置
# ============================================================================
# 修改这个路径，使其指向你的字体文件
# 示例：
#   - 如果 setup_font.py 和 fonts/ 在同一目录：
#     _FONT_FILE_RELATIVE = 'fonts/BabelStoneHan.ttf'
#   - 如果 setup_font.py 在 scripts/ 目录，字体在项目根目录的 fonts/：
#     _FONT_FILE_RELATIVE = os.path.join('..', 'fonts', 'BabelStoneHan.ttf')

_FONT_FILE_RELATIVE = os.path.join('..', 'fonts', 'BabelStoneHan.ttf')


# ============================================================================
# 字体配置函数
# ============================================================================

def _get_font_path():
    """获取字体文件的绝对路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_file = os.path.join(script_dir, _FONT_FILE_RELATIVE)
    return os.path.normpath(font_file)


def setup_chinese_font(verbose=False):
    """
    配置中文字体（兼容所有 matplotlib 版本）
    
    Args:
        verbose: 是否打印详细信息
    
    Returns:
        FontProperties: 字体属性对象
    
    兼容性：
        - matplotlib 3.2+: 使用 fontManager.addfont()
        - matplotlib < 3.2: 使用 fontManager.ttflist.append()
    """
    font_file = _get_font_path()
    
    if verbose:
        print("\n" + "=" * 70)
        print("【字体配置】")
        print("=" * 70)
        print(f"  字体路径: {font_file}")
        print(f"  存在: {os.path.exists(font_file)}")
    
    if os.path.exists(font_file):
        try:
            # 创建 FontProperties
            font_prop = fm.FontProperties(fname=font_file)
            font_name = font_prop.get_name()
            
            # 注册字体（兼容新旧版本 matplotlib）
            try:
                # 方法1：matplotlib 3.2+ 使用 addfont
                if hasattr(fm.fontManager, 'addfont'):
                    fm.fontManager.addfont(font_file)
                    if verbose:
                        print(f"  ✅ 已加载 (addfont): {font_name}")
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
                        if verbose:
                            print(f"  ✅ 已加载 (ttflist): {font_name}")
                    except Exception as e:
                        if verbose:
                            print(f"  ✅ 已加载 (FontProperties): {font_name}")
            except Exception as e:
                if verbose:
                    print(f"  ⚠️ 字体注册失败: {e}")
            
            # 设置全局字体
            plt.rcParams['font.family'] = font_name
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            
            if verbose:
                print("=" * 70 + "\n")
            
            return font_prop
        except Exception as e:
            if verbose:
                print(f"  ❌ 加载失败: {e}")
                print("=" * 70 + "\n")
    else:
        if verbose:
            print(f"  ⚠️ 未找到字体文件")
            print("=" * 70 + "\n")
    
    return fm.FontProperties()


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == '__main__':
    import numpy as np
    
    # 1. 配置字体
    chinese_font = setup_chinese_font(verbose=True)
    
    # 2. 创建测试数据
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # 3. 绘图
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(x, y1, label='正弦曲线', linewidth=2)
    ax.plot(x, y2, label='余弦曲线', linewidth=2)
    
    ax.set_title('matplotlib 中文显示测试', fontsize=14, fontweight='bold')
    ax.set_xlabel('横轴：角度（弧度）', fontsize=11)
    ax.set_ylabel('纵轴：幅值', fontsize=11)
    ax.legend(prop=chinese_font, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 4. 保存
    output_path = 'test_chinese_font.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ 图片已保存: {output_path}")
