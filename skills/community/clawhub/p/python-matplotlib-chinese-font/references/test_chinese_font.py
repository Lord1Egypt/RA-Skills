#!/usr/bin/env python3
"""
test_chinese_font.py - 测试 matplotlib 中文显示

实验目的：
  验证中文字体配置是否正确
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

# ============================================================================
# 字体配置（参考 Matplotlib 中文显示完整指南）
# ============================================================================

# 字体文件相对于脚本的路径
# test_chinese_font.py 位于 spot_micro_body_control_sim/03_gait_control/tests/
# 字体文件位于 spot_micro_body_control_sim/fonts/BabelStoneHan.ttf
_FONT_FILE_RELATIVE = os.path.join('..', '..', 'fonts', 'BabelStoneHan.ttf')

def _get_font_path():
    """获取字体文件的绝对路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_file = os.path.join(script_dir, _FONT_FILE_RELATIVE)
    return os.path.normpath(font_file)

def setup_chinese_font():
    """配置中文字体"""
    font_file = _get_font_path()
    
    print("\n" + "=" * 70)
    print("【字体配置测试】")
    print("=" * 70)
    print(f"  字体路径: {font_file}")
    print(f"  存在: {os.path.exists(font_file)}")
    
    if os.path.exists(font_file):
        try:
            # 关键：显式添加字体到 matplotlib 的 fontManager 缓存
            fm.fontManager.addfont(font_file)
            
            # 创建 FontProperties
            font_prop = fm.FontProperties(fname=font_file)
            
            # 设置全局字体
            plt.rcParams['font.family'] = font_prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            
            print(f"  ✅ 已加载: {font_prop.get_name()}")
            print("=" * 70 + "\n")
            return font_prop
        except Exception as e:
            print(f"  ❌ 加载失败: {e}")
            print("=" * 70 + "\n")
    else:
        print(f"  ⚠️ 未找到字体文件")
        print("=" * 70 + "\n")
    
    return fm.FontProperties()


def main():
    """主测试函数"""
    
    # 1. 配置字体
    chinese_font = setup_chinese_font()
    
    # 2. 创建测试数据
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # 3. 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # ============================================================================
    # 子图 1：基础测试
    # ============================================================================
    ax = axes[0, 0]
    ax.plot(x, y1, label='正弦曲线', linewidth=2)
    ax.plot(x, y2, label='余弦曲线', linewidth=2)
    ax.set_title('基础测试：中文标题', fontsize=14, fontweight='bold')
    ax.set_xlabel('横轴：角度（弧度）', fontsize=11)
    ax.set_ylabel('纵轴：幅值', fontsize=11)
    ax.legend(prop=chinese_font, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    # ============================================================================
    # 子图 2：多元素测试
    # ============================================================================
    ax = axes[0, 1]
    categories = ['类别一', '类别二', '类别三', '类别四', '类别五']
    values = [23, 45, 56, 78, 32]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    bars = ax.bar(categories, values, color=colors, alpha=0.8)
    ax.set_title('多元素测试：柱状图', fontsize=14, fontweight='bold')
    ax.set_xlabel('分类标签', fontsize=11)
    ax.set_ylabel('数值大小', fontsize=11)
    ax.set_xticklabels(categories, fontproperties=chinese_font)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}',
                ha='center', va='bottom', fontsize=10, fontproperties=chinese_font)
    
    # ============================================================================
    # 子图 3：负数测试
    # ============================================================================
    ax = axes[1, 0]
    y_negative = y1 - 0.5
    ax.plot(x, y_negative, label='偏移正弦（含负数）', linewidth=2, color='#E94F37')
    ax.fill_between(x, y_negative, alpha=0.3, color='#E94F37')
    ax.set_title('负数测试：验证负号显示', fontsize=14, fontweight='bold')
    ax.set_xlabel('横轴标签', fontsize=11)
    ax.set_ylabel('纵轴（含负值）', fontsize=11)
    ax.legend(prop=chinese_font, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    # ============================================================================
    # 子图 4：综合测试
    # ============================================================================
    ax = axes[1, 1]
    
    # 多条曲线
    ax.plot(x, y1, label='数据系列一', linewidth=2, marker='o', markevery=10)
    ax.plot(x, y2, label='数据系列二', linewidth=2, marker='s', markevery=10)
    ax.plot(x, y1*0.5, label='数据系列三', linewidth=2, marker='^', markevery=10)
    
    ax.set_title('综合测试：多系列图例', fontsize=14, fontweight='bold')
    ax.set_xlabel('时间（秒）', fontsize=11)
    ax.set_ylabel('测量值（单位）', fontsize=11)
    ax.legend(prop=chinese_font, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 添加注释
    ax.text(0.5, 0.95, '这是中文注释文本', 
            transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', fontproperties=chinese_font,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # ============================================================================
    # 总标题
    # ============================================================================
    fig.suptitle('Matplotlib 中文显示完整测试', fontsize=16, fontweight='bold', y=0.995)
    
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    
    # ============================================================================
    # 保存图片
    # ============================================================================
    output_path = os.path.join(os.getcwd(), 'test_chinese_font.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    
    print("=" * 70)
    print("【测试结果】")
    print("=" * 70)
    print(f"  ✅ 图片已保存: {output_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()
