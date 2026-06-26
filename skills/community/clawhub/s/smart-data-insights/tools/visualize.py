#!/usr/bin/env python3
"""
Data visualization utilities.
"""

import pandas as pd
import numpy as np
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
except ImportError:
    print("Error: matplotlib not installed. Run: pip3 install matplotlib")
    raise


def generate_charts(df, output_dir, base_name, style='professional'):
    """
    Generate various charts for data analysis.
    
    Args:
        df: Input DataFrame
        output_dir: Directory to save charts
        base_name: Base filename for charts
        style: Chart style ('professional', 'simple', 'colorful')
    
    Returns:
        List of generated chart file paths
    """
    output_dir = Path(output_dir)
    chart_paths = []
    
    # Set style
    if style == 'professional':
        plt.style.use('seaborn-v0_8-whitegrid')
    elif style == 'simple':
        plt.style.use('ggplot')
    else:
        plt.style.use('default')
    
    # 1. Missing values heatmap
    if df.isnull().sum().sum() > 0:
        path = _plot_missing_values(df, output_dir, base_name)
        if path:
            chart_paths.append(path)
    
    # 2. Numeric distributions
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        path = _plot_distributions(df, numeric_cols, output_dir, base_name)
        if path:
            chart_paths.append(path)
    
    # 3. Correlation heatmap
    if len(numeric_cols) >= 2:
        path = _plot_correlation(df, numeric_cols, output_dir, base_name)
        if path:
            chart_paths.append(path)
    
    # 4. Categorical bar charts
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols[:3]:  # Top 3 categorical columns
        if df[col].nunique() <= 20:  # Only if reasonable number of categories
            path = _plot_categorical(df, col, output_dir, base_name)
            if path:
                chart_paths.append(path)
    
    # 5. Time series (if date column exists)
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        path = _plot_time_series(df, date_cols[0], numeric_cols[0], output_dir, base_name)
        if path:
            chart_paths.append(path)
    
    return chart_paths


def _plot_missing_values(df, output_dir, base_name):
    """Plot missing values overview."""
    try:
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=True)
        
        if len(missing) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, max(4, len(missing) * 0.4)))
        bars = ax.barh(missing.index, missing.values, color='coral')
        ax.set_xlabel('Missing Values Count')
        ax.set_title('Missing Values by Column')
        
        # Add value labels
        for bar, val in zip(bars, missing.values):
            ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                   f'{val} ({val/len(df)*100:.1f}%)', 
                   va='center', fontsize=9)
        
        plt.tight_layout()
        path = output_dir / f"{base_name}_missing_values.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return str(path)
    except Exception as e:
        print(f"Warning: Could not generate missing values chart: {e}")
        return None


def _plot_distributions(df, numeric_cols, output_dir, base_name):
    """Plot distributions of numeric columns."""
    try:
        n_cols = min(4, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 3*n_rows))
        if n_rows * n_cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        for i, col in enumerate(numeric_cols):
            if i >= len(axes):
                break
            ax = axes[i]
            data = df[col].dropna()
            if len(data) > 0:
                ax.hist(data, bins=30, color='steelblue', alpha=0.7, edgecolor='white')
                ax.set_title(col, fontsize=10)
                ax.set_ylabel('Frequency')
        
        # Hide empty subplots
        for i in range(len(numeric_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Numeric Distributions', fontsize=12, y=1.02)
        plt.tight_layout()
        path = output_dir / f"{base_name}_distributions.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return str(path)
    except Exception as e:
        print(f"Warning: Could not generate distributions chart: {e}")
        return None


def _plot_correlation(df, numeric_cols, output_dir, base_name):
    """Plot correlation heatmap."""
    try:
        corr = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(max(8, len(numeric_cols)*0.8), max(6, len(numeric_cols)*0.6)))
        im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
        
        # Add colorbar
        plt.colorbar(im, ax=ax, shrink=0.8)
        
        # Set ticks
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=8)
        ax.set_yticklabels(numeric_cols, fontsize=8)
        
        # Add correlation values
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                val = corr.iloc[i, j]
                color = 'white' if abs(val) > 0.5 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center', 
                       color=color, fontsize=7)
        
        ax.set_title('Correlation Heatmap', fontsize=12)
        plt.tight_layout()
        path = output_dir / f"{base_name}_correlation.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return str(path)
    except Exception as e:
        print(f"Warning: Could not generate correlation chart: {e}")
        return None


def _plot_categorical(df, column, output_dir, base_name):
    """Plot categorical column distribution."""
    try:
        value_counts = df[column].value_counts().head(15)
        
        fig, ax = plt.subplots(figsize=(10, max(4, len(value_counts) * 0.4)))
        bars = ax.barh(value_counts.index, value_counts.values, color='steelblue')
        ax.set_xlabel('Count')
        ax.set_title(f'Distribution: {column}')
        
        # Add value labels
        for bar, val in zip(bars, value_counts.values):
            ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                   f'{val}', va='center', fontsize=9)
        
        plt.tight_layout()
        path = output_dir / f"{base_name}_cat_{column}.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return str(path)
    except Exception as e:
        print(f"Warning: Could not generate categorical chart for {column}: {e}")
        return None


def _plot_time_series(df, date_col, value_col, output_dir, base_name):
    """Plot time series."""
    try:
        df_sorted = df.sort_values(date_col)
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df_sorted[date_col], df_sorted[value_col], color='steelblue', linewidth=1.5)
        ax.fill_between(df_sorted[date_col], df_sorted[value_col], alpha=0.2)
        
        ax.set_xlabel(date_col)
        ax.set_ylabel(value_col)
        ax.set_title(f'Time Series: {value_col} over {date_col}')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = output_dir / f"{base_name}_timeseries.png"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return str(path)
    except Exception as e:
        print(f"Warning: Could not generate time series chart: {e}")
        return None
