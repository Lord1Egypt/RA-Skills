# -*- coding: utf-8 -*-
"""
Score Analysis - Radar Chart Generator
Generates grouped radar charts by student type
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# Configure Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Default color scheme (customizable)
DEFAULT_COLORS = {
    'primary': '#006B6B',
    'secondary': '#2E8686',
    'accent': '#C0392B',
    'chart_colors': ['#006B6B', '#C0392B', '#2E8686', '#D4A017', '#8E44AD']
}


def create_student_radar_chart(students, chart_type, output_path, colors=None):
    """
    Generate radar chart for a group of students
    
    Args:
        students: list of dict, each containing:
            - name: student name
            - scores: dict {'Chinese': x, 'Math': x, 'English': x, 'Physics': x, 'Chemistry': x, 'Biology': x}
        chart_type: str, chart title (e.g., "Critical Students")
        output_path: str, output file path
        colors: list, custom color palette
    """
    if not students:
        return
    
    if colors is None:
        colors = DEFAULT_COLORS['chart_colors']
    
    subjects = ['Chinese', 'Math', 'English', 'Physics', 'Chemistry', 'Biology']
    max_scores = {'Chinese': 150, 'Math': 150, 'English': 150, 'Physics': 100, 'Chemistry': 100, 'Biology': 100}
    N = len(subjects)
    
    # Calculate angles
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Create chart
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    
    # Plot each student
    for i, student in enumerate(students):
        name = student['name']
        scores = student['scores']
        
        # Normalize to percentage
        values = [scores.get(s, 0) / max_scores[s] * 100 for s in subjects]
        values += values[:1]
        
        color = colors[i % len(colors)]
        ax.plot(angles, values, 'o-', linewidth=2.5, label=name, color=color, markersize=6)
        ax.fill(angles, values, alpha=0.15, color=color)
    
    # Configure chart
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(subjects, fontsize=13)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9, color='gray')
    
    ax.set_title(f'{chart_type}', fontsize=16, fontweight='bold', pad=30, color='#333333')
    
    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=11, 
                       framealpha=0.9, edgecolor='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Generated: {output_path}')


def create_all_radar_charts(analysis_data, output_dir, colors=None):
    """
    Generate all radar charts based on analysis data
    
    Args:
        analysis_data: dict containing:
            - critical_special: special control line critical students
            - critical_undergrad: undergraduate line critical students
            - poor_balance: subject-imbalanced students
        output_dir: str, output directory
        colors: list, custom color palette
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Special control line critical students
    if analysis_data.get('critical_special'):
        students = analysis_data['critical_special'][:5]
        create_student_radar_chart(
            students, 
            'Special Control Line Critical Students',
            os.path.join(output_dir, 'radar_critical_special.png'),
            colors
        )
    
    # Undergraduate line critical students
    if analysis_data.get('critical_undergrad'):
        students = analysis_data['critical_undergrad'][:5]
        create_student_radar_chart(
            students,
            'Undergraduate Line Critical Students', 
            os.path.join(output_dir, 'radar_critical_undergrad.png'),
            colors
        )
    
    # Subject-imbalanced students
    if analysis_data.get('poor_balance'):
        students = analysis_data['poor_balance'][:5]
        create_student_radar_chart(
            students,
            'Subject-Imbalanced Students',
            os.path.join(output_dir, 'radar_poor_balance.png'),
            colors
        )


# Example usage
if __name__ == '__main__':
    example_data = {
        'critical_special': [
            {'name': 'Student A', 'scores': {'Chinese': 109, 'Math': 74, 'English': 117.5, 'Physics': 51, 'Chemistry': 77, 'Biology': 57}},
            {'name': 'Student B', 'scores': {'Chinese': 105, 'Math': 81, 'English': 80, 'Physics': 76, 'Chemistry': 81, 'Biology': 63}},
            {'name': 'Student C', 'scores': {'Chinese': 101, 'Math': 99, 'English': 116, 'Physics': 36, 'Chemistry': 76, 'Biology': 55}},
        ],
        'critical_undergrad': [
            {'name': 'Student D', 'scores': {'Chinese': 104, 'Math': 37, 'English': 89.5, 'Physics': 37, 'Chemistry': 71, 'Biology': 74}},
            {'name': 'Student E', 'scores': {'Chinese': 94, 'Math': 69, 'English': 87, 'Physics': 24, 'Chemistry': 73, 'Biology': 39}},
        ],
        'poor_balance': [
            {'name': 'Student F', 'scores': {'Chinese': 112, 'Math': 45, 'English': 108.5, 'Physics': 65, 'Chemistry': 88, 'Biology': 73}},
            {'name': 'Student G', 'scores': {'Chinese': 116, 'Math': 135, 'English': 109, 'Physics': 77, 'Chemistry': 82, 'Biology': 56}},
        ]
    }
    
    output_dir = './charts'
    create_all_radar_charts(example_data, output_dir)
