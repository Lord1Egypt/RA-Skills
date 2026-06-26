import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
import pandas as pd
import os

# 添加 SimHei 字体
font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simhei.ttf")
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['SimHei', 'PingFang SC', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_temp_precip(
    temp_data,
    prec_data=None,
    components=('temp',),
    enable_adaptive=True,
    min_data_range=0.5,
    figsize=None,
    point_size=None,
    point_halo_factor=None,
    point_halo_alpha=0.25,
    label_fontsize=None,
    label_offset=None,
    temp_color='#e53e3e',
    prec_color='#3182ce',
    bar_width=0.6,
    temp_window=5,
    temp_polyorder=2,
    smooth_points=400,
    label_temp_format=None,      # 若为 None，则使用原始值（保留2位小数）
    label_prec_format=None,      # 若为 None，则使用原始值（保留1位小数，但避开取整）
    title='',
    save_path=None,
    bar_downward_shift=0.0,
    bar_alpha=0.5,
    bar_edgecolor='white',
    bar_edgewidth=1.2,
    curve_linewidth=2.8,
    curve_alpha=0.9,
    fill_alpha=0,
    point_edgecolor='white',
    point_edgewidth=1.5,
    label_color='#2d3748',
    bg_color='#f7f9fc',
    show_legend=False,
    legend_loc='upper left',
    transparent=False,
):
    # 标准化 components
    if isinstance(components, str):
        components = (components,)
    draw_temp = 'temp' in components
    dual_mode = prec_data is not None
    draw_precip = dual_mode and ('precip' in components)

    labels = list(temp_data.keys())
    n_points = len(labels)
    x_idx = np.arange(n_points)
    y_temp_raw = np.array([temp_data[k] for k in labels])
    if dual_mode:
        y_prec = np.array([prec_data.get(k, 0) for k in labels])
    else:
        y_prec = None
        draw_precip = False

    # 自适应尺寸等（保持原样）
    if enable_adaptive:
        if figsize is None:
            width = max(8, min(16, n_points * 0.6))
            figsize = (width, 5.5)
        if point_size is None:
            point_size = max(40, min(80, int(80 * (12 / max(n_points, 1)))))
        if point_halo_factor is None:
            point_halo_factor = 1.8 + (40 / max(n_points, 1)) * 0.5
        if label_fontsize is None:
            label_fontsize = max(6, min(10, int(10 * (15 / max(n_points, 1)))))
        if label_offset is None:
            label_offset = 0.04 + (5 / max(n_points, 1)) * 0.02
    else:
        figsize = figsize or (12, 5.5)
        point_size = point_size or 80
        point_halo_factor = point_halo_factor or 2.2
        label_fontsize = label_fontsize or 9
        label_offset = label_offset or 0.06

    # 气温平滑（保持不变）
    if draw_temp:
        win = temp_window
        if win % 2 == 0:
            win += 1
        win = min(win, len(y_temp_raw) if len(y_temp_raw) % 2 == 1 else len(y_temp_raw) - 1)
        if win < 3:
            win = 3
        if win <= len(y_temp_raw):
            y_temp_smooth = savgol_filter(y_temp_raw, win, temp_polyorder, mode='nearest')
        else:
            y_temp_smooth = y_temp_raw
        if len(x_idx) >= 4:
            interp = interp1d(x_idx, y_temp_smooth, kind='cubic', fill_value='extrapolate')
        else:
            interp = interp1d(x_idx, y_temp_smooth, kind='linear', fill_value='extrapolate')
        x_dense = np.linspace(x_idx.min(), x_idx.max(), smooth_points)
        y_dense = interp(x_dense)

    # 创建画布
    if transparent:
        fig, ax1 = plt.subplots(figsize=figsize, facecolor='none')
        ax1.set_facecolor('none')
    else:
        fig, ax1 = plt.subplots(figsize=figsize, facecolor=bg_color)
        ax1.set_facecolor(bg_color)

    if draw_precip and draw_temp:
        ax2 = ax1.twinx()
    else:
        ax2 = None

    # ========= 降水柱状图（真实高度） =========
    if draw_precip and y_prec is not None:
        ax = ax2 if ax2 is not None else ax1
        bottom = bar_downward_shift
        ax.bar(x_idx, y_prec, width=bar_width,
               color=prec_color, alpha=bar_alpha,
               edgecolor=bar_edgecolor, linewidth=bar_edgewidth,
               label='降水量', bottom=bottom, zorder=0 if ax2 is None else -10)
        max_prec = y_prec.max() if y_prec.max() > 0 else 1
        y_bottom = min(bottom, 0) - max_prec * 0.1
        y_top = max(bottom + max_prec, 0) + max_prec * 0.1
        ax.set_ylim(y_bottom, y_top)

        label_y = bottom - max_prec * 0.05
        for xi, yi in zip(x_idx, y_prec):
            # 显示真实数值，避免四舍五入
            if label_prec_format is None:
                # 默认：保留合适的位数，但不丢失精度
                if yi == int(yi):
                    text = str(int(yi))
                else:
                    # 保留2位小数，去除末尾无意义的0
                    text = f"{yi:.2f}".rstrip('0').rstrip('.')
            else:
                text = label_prec_format.format(yi)
            ax.text(xi, label_y, text,
                    ha='center', va='top', fontsize=label_fontsize,
                    fontweight='medium', color=label_color, zorder=10)

    # ========= 气温/单变量曲线 =========
    if draw_temp:
        if ax2 is None:
            ax1.fill_between(x_dense, y_dense, alpha=fill_alpha, color=temp_color, zorder=2)
            ax1.plot(x_dense, y_dense, color=temp_color, linewidth=curve_linewidth,
                     alpha=curve_alpha, solid_capstyle='round', label='曲线', zorder=3)
            ax1.scatter(x_idx, y_temp_smooth, s=point_size * point_halo_factor,
                        facecolor=temp_color, edgecolor='none', alpha=point_halo_alpha, zorder=4)
            ax1.scatter(x_idx, y_temp_smooth, s=point_size, facecolor=temp_color,
                        edgecolor=point_edgecolor, linewidth=point_edgewidth, zorder=5)

            y_min, y_max = y_temp_smooth.min(), y_temp_smooth.max()
            y_range = y_max - y_min
            if y_range < min_data_range:
                data_avg = (y_min + y_max) / 2
                y_min = data_avg - min_data_range / 2
                y_max = data_avg + min_data_range / 2
                y_range = min_data_range
            offset_temp = y_range * label_offset if y_range > 0 else 0.5
            for xi, yi_raw, yi_smooth in zip(x_idx, y_temp_raw, y_temp_smooth):
                # 气温标签同样避免四舍五入
                if label_temp_format is None:
                    if yi_raw == int(yi_raw):
                        text = str(int(yi_raw))
                    else:
                        text = f"{yi_raw:.2f}".rstrip('0').rstrip('.')
                else:
                    text = label_temp_format.format(yi_raw)
                ax1.text(xi, yi_smooth + offset_temp, text,
                         ha='center', va='bottom', fontsize=label_fontsize,
                         fontweight='medium', color=label_color, zorder=6)
            y_pad = y_range * 0.08 if y_range > 0 else 0.5
            ax1.set_ylim(y_min - y_pad, y_max + y_pad)
        else:
            ax1.set_zorder(ax2.get_zorder() + 1)
            ax1.patch.set_visible(False)
            ax1.fill_between(x_dense, y_dense, alpha=fill_alpha, color=temp_color, zorder=2)
            ax1.plot(x_dense, y_dense, color=temp_color, linewidth=curve_linewidth,
                     alpha=curve_alpha, solid_capstyle='round', label='气温曲线', zorder=3)
            ax1.scatter(x_idx, y_temp_smooth, s=point_size * point_halo_factor,
                        facecolor=temp_color, edgecolor='none', alpha=point_halo_alpha, zorder=4)
            ax1.scatter(x_idx, y_temp_smooth, s=point_size, facecolor=temp_color,
                        edgecolor=point_edgecolor, linewidth=point_edgewidth, zorder=5)

            y_min, y_max = y_temp_smooth.min(), y_temp_smooth.max()
            y_range = y_max - y_min
            if y_range < min_data_range:
                data_avg = (y_min + y_max) / 2
                y_min = data_avg - min_data_range / 2
                y_max = data_avg + min_data_range / 2
                y_range = min_data_range
            offset_temp = y_range * label_offset if y_range > 0 else 0.5
            for xi, yi_raw, yi_smooth in zip(x_idx, y_temp_raw, y_temp_smooth):
                if label_temp_format is None:
                    if yi_raw == int(yi_raw):
                        text = str(int(yi_raw))
                    else:
                        text = f"{yi_raw:.2f}".rstrip('0').rstrip('.')
                else:
                    text = label_temp_format.format(yi_raw)
                ax1.text(xi, yi_smooth + offset_temp, text,
                         ha='center', va='bottom', fontsize=label_fontsize,
                         fontweight='medium', color=label_color, zorder=6)
            y_pad = y_range * 0.08 if y_range > 0 else 0.5
            ax1.set_ylim(y_min - y_pad, y_max + y_pad)

    # 隐藏轴线刻度（不变）
    axes_to_hide = [ax1]
    if ax2 is not None:
        axes_to_hide.append(ax2)
    for ax in axes_to_hide:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xlabel('')
        ax.set_ylabel('')
    margin = 0.6 if n_points < 10 else 0.4
    ax1.set_xlim(-margin, n_points - 1 + margin)
    if ax2 is not None:
        ax2.set_xlim(-margin, n_points - 1 + margin)

    # 图例
    if show_legend:
        from matplotlib.lines import Line2D
        legend_elements = []
        if draw_temp:
            label_name = '气温曲线' if dual_mode else (title if title else '曲线')
            legend_elements.append(Line2D([0], [0], color=temp_color, lw=curve_linewidth, alpha=curve_alpha, label=label_name))
        if draw_precip:
            legend_elements.append(Line2D([0], [0], color=prec_color, lw=bar_edgewidth*2, alpha=bar_alpha, label='降水量'))
        if legend_elements:
            ax1.legend(handles=legend_elements, loc=legend_loc,
                       frameon=True, fancybox=True, edgecolor='none',
                       facecolor='white', framealpha=0.7, fontsize=label_fontsize)

    ax1.set_title(title, fontsize=16, fontweight='bold', color='#1a202c', pad=20)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                    facecolor='none' if transparent else bg_color,
                    transparent=transparent)
        print(f"✅ 图表已保存至: {save_path}")
    plt.close(fig)


if __name__ == "__main__":
    temp_dict = {'A': 10.2, 'B': 11.5, 'C': 10.8}
    prec_dict = {'A': 0.0, 'B': 0.8, 'C': 0.6}
    plot_temp_precip(
        temp_dict, prec_dict,
        components=('temp', 'precip'),
        bar_downward_shift=-0.5,
        enable_adaptive=True,
        min_data_range=0.5,
        save_path='no_rounding.png',
        transparent=True
    )