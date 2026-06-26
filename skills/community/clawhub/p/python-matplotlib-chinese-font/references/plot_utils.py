#!/usr/bin/env python3
# =============================================================================
# plot_utils.py - matplotlib 绑图工具模块
# =============================================================================
#
# 功能说明：
#   提供 matplotlib 绑图的公共配置，包括中文字体支持等。
#
# 使用方法：
#   from plot_utils import setup_matplotlib
#   setup_matplotlib()
#
# =============================================================================

import os
import matplotlib.pyplot as plt
from matplotlib import font_manager


# =============================================================================
# 中文字体配置
# =============================================================================
# 问题描述：
#   matplotlib 默认不支持中文，中文会显示为方块，控制台警告：
#   "UserWarning: Glyph XXXXX missing from current font"
#
# 解决方案：
#   使用 font_manager.fontManager.addfont() 显式添加字体到缓存
#
# 核心要点：
#   - addfont() 是关键：必须显式把字体添加到 matplotlib 的 fontManager 缓存
#   - 使用绝对路径：避免路径问题
#   - 字体文件放在项目内：不依赖系统字体，可移植性好
# =============================================================================

# 字体文件相对于本模块的路径
# plot_utils.py 位于 your_project/scripts/
# 字体文件位于 your_project/fonts/BabelStoneHan.ttf
# 相对路径: ../fonts/BabelStoneHan.ttf
_FONT_FILE_RELATIVE = os.path.join('..', 'fonts', 'BabelStoneHan.ttf')

# 是否已初始化
_initialized = False


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
    global _initialized
    
    if _initialized:
        return font_manager.FontProperties()
    
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
            font_prop = font_manager.FontProperties(fname=font_file)
            font_name = font_prop.get_name()
            
            # 注册字体（兼容新旧版本 matplotlib）
            try:
                # 方法1：matplotlib 3.2+ 使用 addfont
                if hasattr(font_manager.fontManager, 'addfont'):
                    font_manager.fontManager.addfont(font_file)
                    if verbose:
                        print(f"  ✅ 已加载 (addfont): {font_name}")
                else:
                    # 方法2：旧版本 matplotlib，手动添加到字体列表
                    try:
                        font_manager.fontManager.ttflist.append(font_manager.FontEntry(
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
                    except Exception:
                        if verbose:
                            print(f"  ✅ 已加载 (FontProperties): {font_name}")
            except Exception as e:
                if verbose:
                    print(f"  ⚠️ 字体注册失败: {e}")
            
            # 设置全局字体
            plt.rcParams['font.family'] = font_name
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            
            _initialized = True
            
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
    
    return font_manager.FontProperties()
        bool: 是否成功配置
    """
    font_file = _get_font_path()

    if os.path.exists(font_file):
        font_manager.fontManager.addfont(font_file)
        font_prop = font_manager.FontProperties(fname=font_file)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        if verbose:
            print(f"[字体] 已加载中文字体: {font_file}")
        return True
    else:
        print(f"[警告] 未找到中文字体文件: {font_file}")
        return False


def setup_matplotlib(chinese_font=True, style=None, verbose=False):
    """
    初始化 matplotlib 配置

    Args:
        chinese_font: 是否配置中文字体
        style: matplotlib 样式（如 'seaborn', 'ggplot' 等）
        verbose: 是否打印详细信息

    Returns:
        bool: 是否成功配置
    """
    global _initialized

    if _initialized:
        return True

    success = True

    # 设置样式
    if style:
        try:
            plt.style.use(style)
            if verbose:
                print(f"[样式] 已应用样式: {style}")
        except Exception as e:
            print(f"[警告] 无法应用样式 {style}: {e}")
            success = False

    # 配置中文字体
    if chinese_font:
        if not setup_chinese_font(verbose=verbose):
            success = False

    _initialized = True
    return success


# =============================================================================
# 常用绑图参数
# =============================================================================
# 标准字体大小
FONT_SIZE = {
    'title': 14,
    'subtitle': 12,
    'label': 10,
    'tick': 9,
    'legend': 9,
    'annotation': 8,
}

# 标准线宽
LINE_WIDTH = {
    'main': 1.5,
    'secondary': 1.0,
    'thin': 0.5,
    'thick': 2.0,
}

# 标准颜色
COLORS = {
    'target': '#2E86AB',      # 蓝色 - 目标值
    'actual': '#E94F37',      # 红色 - 实际值
    'error': '#2ECC71',       # 绿色 - 误差
    'torque': '#9B59B6',      # 紫色 - 力矩
    'reference': '#95A5A6',   # 灰色 - 参考线
}


# =============================================================================
# 交互功能：点击图例切换曲线显示/隐藏
# =============================================================================
def enable_legend_toggle(ax, legend=None):
    """
    启用点击图例切换曲线显示/隐藏功能

    用法：
        fig, ax = plt.subplots()
        line1, = ax.plot(x, y1, label='曲线1')
        line2, = ax.plot(x, y2, label='曲线2')
        legend = ax.legend()
        enable_legend_toggle(ax, legend)
        plt.show()

    Args:
        ax: matplotlib Axes 对象
        legend: Legend 对象（如果为 None，则使用 ax.get_legend()）
    """
    if legend is None:
        legend = ax.get_legend()

    if legend is None:
        return

    # 建立图例项与曲线的映射
    legend_lines = legend.get_lines()
    legend_texts = legend.get_texts()
    ax_lines = ax.get_lines()

    # 创建映射字典：图例线条 -> 曲线，图例文字 -> 曲线
    line_map = {}
    text_map = {}

    for i, (leg_line, ax_line) in enumerate(zip(legend_lines, ax_lines)):
        # 设置图例线条可点击
        leg_line.set_picker(True)
        leg_line.set_pickradius(5)
        line_map[leg_line] = (ax_line, leg_line, legend_texts[i] if i < len(legend_texts) else None)

        # 设置图例文字可点击
        if i < len(legend_texts):
            legend_texts[i].set_picker(True)
            text_map[legend_texts[i]] = (ax_line, leg_line, legend_texts[i])

    def on_pick(event):
        artist = event.artist

        # 查找对应的曲线和图例元素
        if artist in line_map:
            ax_line, leg_line, leg_text = line_map[artist]
        elif artist in text_map:
            ax_line, leg_line, leg_text = text_map[artist]
        else:
            return

        # 切换可见性
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)

        # 更新图例样式：隐藏的曲线图例变淡
        alpha = 1.0 if visible else 0.2
        leg_line.set_alpha(alpha)
        if leg_text:
            leg_text.set_alpha(alpha)

        # 重绘
        ax.figure.canvas.draw()

    ax.figure.canvas.mpl_connect('pick_event', on_pick)


def enable_legend_toggle_for_figure(fig):
    """
    为整个 figure 的所有子图启用图例切换功能

    Args:
        fig: matplotlib Figure 对象
    """
    for ax in fig.get_axes():
        legend = ax.get_legend()
        if legend is not None:
            enable_legend_toggle(ax, legend)
