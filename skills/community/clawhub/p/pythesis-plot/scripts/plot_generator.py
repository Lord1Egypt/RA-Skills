#!/usr/bin/env python3
"""
图表生成模块
根据配置生成科研图表
"""

import os
import sys
import json
import matplotlib
matplotlib.use('Agg')  # 非交互式后端

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class PlotGenerator:
    """图表生成器"""
    
    # 配色方案
    PALETTES = {
        'academic': ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5'],
        'nature': ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F'],
        'science': ['#074893', '#C41E3A', '#FFC800', '#4C4C4C', '#7F7F7F'],
        'vibrant': ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00'],
    }
    
    def __init__(self, config, output_dir, timestamp):
        self.config = config
        self.output_dir = output_dir
        self.timestamp = timestamp
        self.data_file = config.get('data_file')
        self.df = None
        self._setup_style()
        if self.data_file:
            self._load_data()
    
    def _setup_style(self):
        """设置科研样式"""
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # 科研论文常用设置
        plt.rcParams['figure.dpi'] = 150
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 11
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['legend.fontsize'] = 9
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        
        # 中文字体设置（尝试常见字体）
        chinese_fonts = ['SimHei', 'Heiti TC', 'WenQuanYi Micro Hei', 'Arial Unicode MS']
        for font in chinese_fonts:
            try:
                plt.rcParams['font.sans-serif'] = [font, 'Arial', 'DejaVu Sans']
                plt.rcParams['axes.unicode_minus'] = False
                break
            except:
                continue
    
    def _load_data(self):
        """加载数据"""
        ext = os.path.splitext(self.data_file)[1].lower()
        
        if ext == '.csv':
            self.df = pd.read_csv(self.data_file)
        elif ext in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.data_file)
        else:
            self.df = pd.read_csv(self.data_file, sep=r'\s+')
    
    def _save_figure(self, fig, plot_type, desc=""):
        """
        保存图表为PDF和PNG两种格式
        
        命名规范: {timestamp}_fig{n}_{type}_{desc}.{ext}
        """
        # 查找当前已有图表数量
        existing = [f for f in os.listdir(self.output_dir) 
                   if f.startswith(self.timestamp) and f.endswith('.pdf')]
        fig_num = len(existing) + 1
        
        desc_suffix = f"_{desc}" if desc else ""
        base_name = f"{self.timestamp}_fig{fig_num}_{plot_type}{desc_suffix}"
        
        # 保存PDF（矢量图，适合LaTeX）
        pdf_path = os.path.join(self.output_dir, f"{base_name}.pdf")
        fig.savefig(pdf_path, bbox_inches='tight', format='pdf')
        
        # 保存PNG（预览图，适合查看）
        png_path = os.path.join(self.output_dir, f"{base_name}.png")
        fig.savefig(png_path, bbox_inches='tight', format='png')
        
        plt.close(fig)
        
        return [pdf_path, png_path]
    
    def _generate_line_plot(self, plot_config):
        """生成折线图"""
        x_col = plot_config['x_col']
        y_col = plot_config['y_col']
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # 检查是否是时间序列
        if pd.api.types.is_datetime64_any_dtype(self.df[x_col]):
            ax.plot(self.df[x_col], self.df[y_col], 
                   linewidth=2, color=self.PALETTES['academic'][0])
        else:
            # 按X排序
            df_sorted = self.df.sort_values(by=x_col)
            ax.plot(df_sorted[x_col], df_sorted[y_col], 
                   linewidth=2, color=self.PALETTES['academic'][0])
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col}趋势图')
        ax.grid(True, alpha=0.3)
        
        return self._save_figure(fig, 'line', y_col)
    
    def _generate_bar_plot(self, plot_config):
        """生成柱状图"""
        x_col = plot_config['x_col']
        y_col = plot_config['y_col']
        
        # 聚合数据
        agg_data = self.df.groupby(x_col)[y_col].mean().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        bars = ax.bar(range(len(agg_data)), agg_data.values,
                     color=self.PALETTES['academic'][:len(agg_data)])
        ax.set_xticks(range(len(agg_data)))
        ax.set_xticklabels(agg_data.index, rotation=45, ha='right')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col}按{x_col}分组对比')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=8)
        
        return self._save_figure(fig, 'bar', f"{y_col}_by_{x_col}")
    
    def _generate_box_plot(self, plot_config):
        """生成箱线图"""
        y_col = plot_config['y_col']
        x_col = plot_config.get('x_col')
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        if x_col:
            self.df.boxplot(column=y_col, by=x_col, ax=ax)
            ax.set_title(f'{y_col}分布（按{x_col}分组）')
        else:
            self.df.boxplot(column=y_col, ax=ax)
            ax.set_title(f'{y_col}分布')
        
        ax.set_ylabel(y_col)
        plt.suptitle('')  # 移除默认标题
        
        return self._save_figure(fig, 'box', y_col)
    
    def _generate_scatter_plot(self, plot_config):
        """生成散点图"""
        x_col = plot_config['x_col']
        y_col = plot_config['y_col']
        add_reg = plot_config.get('add_regression', False)
        
        fig, ax = plt.subplots(figsize=(7, 6))
        
        # 散点
        ax.scatter(self.df[x_col], self.df[y_col], 
                  alpha=0.6, s=50, color=self.PALETTES['academic'][0])
        
        # 回归线
        if add_reg:
            z = np.polyfit(self.df[x_col].dropna(), 
                          self.df[y_col].dropna(), 1)
            p = np.poly1d(z)
            x_line = np.linspace(self.df[x_col].min(), self.df[x_col].max(), 100)
            ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2,
                   label=f'拟合: y={z[0]:.2f}x+{z[1]:.2f}')
            ax.legend()
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col} vs {x_col}')
        ax.grid(True, alpha=0.3)
        
        return self._save_figure(fig, 'scatter', f"{y_col}_vs_{x_col}")
    
    def _generate_heatmap(self, plot_config):
        """生成热力图"""
        cols = plot_config['cols']
        corr = self.df[cols].corr()
        
        fig, ax = plt.subplots(figsize=(max(6, len(cols)), max(5, len(cols)*0.8)))
        
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r',
                   center=0, square=True, ax=ax,
                   cbar_kws={'shrink': 0.8})
        ax.set_title('变量相关性热力图')
        
        return self._save_figure(fig, 'heatmap', 'correlation')
    
    def _generate_dashboard(self, plot_config):
        """生成综合仪表盘"""
        plots = plot_config['plots']
        n_plots = len(plots)
        n_cols = 2
        n_rows = (n_plots + 1) // 2
        
        fig = plt.figure(figsize=(14, 5 * n_rows))
        
        for idx, plot in enumerate(plots):
            ax = fig.add_subplot(n_rows, n_cols, idx + 1)
            
            if plot['type'] == 'line':
                ax.plot(self.df[plot['x']], self.df[plot['y']],
                       linewidth=2, color=self.PALETTES['academic'][0])
            elif plot['type'] == 'bar':
                agg = self.df.groupby(plot['x'])[plot['y']].mean()
                ax.bar(range(len(agg)), agg.values,
                      color=self.PALETTES['academic'][:len(agg)])
                ax.set_xticks(range(len(agg)))
                ax.set_xticklabels(agg.index, rotation=45, ha='right')
            elif plot['type'] == 'scatter':
                ax.scatter(self.df[plot['x']], self.df[plot['y']],
                          alpha=0.6, color=self.PALETTES['academic'][0])
            
            ax.set_xlabel(plot['x'])
            ax.set_ylabel(plot['y'])
            ax.set_title(f"({chr(97+idx)}) {plot['title']}")
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self._save_figure(fig, 'dashboard', 'multi')
    
    def generate(self):
        """
        根据配置生成所有图表
        
        返回: 生成的文件路径列表
        """
        generated_files = []
        plots = self.config.get('plots', [])
        
        for plot_config in plots:
            plot_type = plot_config['type']
            
            try:
                if plot_type == 'line':
                    files = self._generate_line_plot(plot_config)
                elif plot_type == 'bar':
                    files = self._generate_bar_plot(plot_config)
                elif plot_type == 'box':
                    files = self._generate_box_plot(plot_config)
                elif plot_type == 'scatter':
                    files = self._generate_scatter_plot(plot_config)
                elif plot_type == 'heatmap':
                    files = self._generate_heatmap(plot_config)
                elif plot_type == 'dashboard':
                    files = self._generate_dashboard(plot_config)
                else:
                    print(f"⚠️  未知图表类型: {plot_type}")
                    continue
                
                generated_files.extend(files)
                
            except Exception as e:
                print(f"❌ 生成图表失败 ({plot_type}): {e}")
        
        return generated_files


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='图表生成工具')
    parser.add_argument('--config', '-c', required=True, help='配置文件')
    parser.add_argument('--output-dir', '-o', default='.', help='输出目录')
    
    args = parser.parse_args()
    
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    timestamp = config.get('timestamp', pd.Timestamp.now().strftime('%Y%m%d-%H%M%S'))
    
    generator = PlotGenerator(config, args.output_dir, timestamp)
    files = generator.generate()
    
    print(f"✅ 已生成 {len(files)} 个文件")
    for f in files:
        print(f"   📊 {f}")


if __name__ == '__main__':
    main()
