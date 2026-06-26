#!/usr/bin/env python3
"""
HTML Prototype Generator
Generates interactive HTML prototypes from reference images or descriptions
DEFAULT output format for UI Prototype Generator skill
"""

import json
import re
from pathlib import Path
from datetime import datetime

class HTMLPrototypeGenerator:
    """Generate HTML prototypes from references"""
    
    def __init__(self):
        self.color_schemes = {
            'default': {
                'primary': '#1890ff',
                'success': '#52c41a',
                'warning': '#faad14',
                'error': '#ff4d4f',
                'text': '#333333',
                'text_secondary': '#666666',
                'text_light': '#999999',
                'border': '#e8e8e8',
                'background': '#f5f7fa'
            }
        }
    
    def generate_from_description(self, description, output_name=None):
        """Generate HTML from text description"""
        if output_name is None:
            output_name = f"prototype_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🎨 Generating HTML prototype: {output_name}")
        
        # Parse description to determine components
        components = self._parse_description(description)
        
        # Generate HTML
        html = self._build_html(output_name, components)
        
        # Save file
        output_file = f"{output_name}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ HTML prototype saved: {output_file}")
        return output_file
    
    def generate_from_analysis(self, analysis_data, output_name):
        """Generate HTML from image analysis"""
        print(f"🎨 Generating HTML from analysis: {output_name}")
        
        # Build components from analysis
        components = self._build_components_from_analysis(analysis_data)
        
        # Generate HTML
        html = self._build_html(output_name, components)
        
        # Save file
        output_file = f"{output_name}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ HTML prototype saved: {output_file}")
        return output_file
    
    def _parse_description(self, description):
        """Parse text description to extract components"""
        components = []
        
        # Detect common patterns
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['table', '列表', '表格']):
            components.append('table')
        
        if any(word in desc_lower for word in ['form', '表单', '输入']):
            components.append('form')
        
        if any(word in desc_lower for word in ['modal', '弹窗', '对话框']):
            components.append('modal')
        
        if any(word in desc_lower for word in ['sidebar', '侧边栏', '菜单']):
            components.append('sidebar')
        
        if any(word in desc_lower for word in ['header', '导航', '顶部']):
            components.append('header')
        
        if not components:
            components = ['header', 'content']
        
        return components
    
    def _build_components_from_analysis(self, analysis):
        """Build component list from image analysis"""
        # This would be populated from actual image analysis
        return ['header', 'sidebar', 'content']
    
    def _build_html(self, title, components):
        """Build complete HTML document"""
        
        html_parts = [
            self._html_head(title),
            '<body>',
            self._html_styles(),
        ]
        
        # Add components
        for component in components:
            if component == 'header':
                html_parts.append(self._component_header())
            elif component == 'sidebar':
                html_parts.append(self._component_sidebar())
            elif component == 'table':
                html_parts.append(self._component_table())
            elif component == 'form':
                html_parts.append(self._component_form())
            elif component == 'modal':
                html_parts.append(self._component_modal())
            elif component == 'content':
                html_parts.append(self._component_content())
        
        html_parts.extend([
            self._html_scripts(),
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_parts)
    
    def _html_head(self, title):
        """Generate HTML head section"""
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>'''
    
    def _html_styles(self):
        """Generate CSS styles"""
        return '''<style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 14px;
            color: #333;
            background-color: #f5f7fa;
        }
        
        /* Header */
        .header {
            height: 50px;
            background-color: #001529;
            display: flex;
            align-items: center;
            padding: 0 20px;
            color: white;
        }
        
        /* Sidebar */
        .sidebar {
            width: 200px;
            background-color: #fff;
            border-right: 1px solid #e8e8e8;
            padding: 20px 0;
            position: fixed;
            top: 50px;
            bottom: 0;
            left: 0;
        }
        
        /* Main Content */
        .main-content {
            margin-left: 200px;
            padding: 20px;
        }
        
        /* Buttons */
        .btn {
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            border: none;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background-color: #1890ff;
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #40a9ff;
        }
        
        /* Form Elements */
        .form-input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            font-size: 14px;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #1890ff;
        }
        
        /* Table */
        .table-container {
            background: white;
            border-radius: 4px;
            overflow: hidden;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e8e8e8;
        }
        
        th {
            background-color: #fafafa;
            font-weight: 600;
        }
        
        /* Modal */
        .modal {
            background: white;
            border-radius: 8px;
            width: 600px;
            max-width: 90%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .modal-header {
            padding: 20px 24px;
            border-bottom: 1px solid #e8e8e8;
        }
        
        .modal-body {
            padding: 24px;
        }
        
        .modal-footer {
            padding: 16px 24px;
            border-top: 1px solid #e8e8e8;
            display: flex;
            justify-content: flex-end;
            gap: 12px;
        }
    </style>'''
    
    def _component_header(self):
        """Generate header component"""
        return '''
    <header class="header">
        <span style="font-size: 18px; margin-right: 15px;">☰</span>
        <span style="font-size: 16px;">Application Name</span>
    </header>'''
    
    def _component_sidebar(self):
        """Generate sidebar component"""
        return '''
    <aside class="sidebar">
        <div style="padding: 12px 20px; cursor: pointer;">Menu Item 1</div>
        <div style="padding: 12px 20px; cursor: pointer;">Menu Item 2</div>
        <div style="padding: 12px 20px; cursor: pointer;">Menu Item 3</div>
    </aside>'''
    
    def _component_content(self):
        """Generate main content area"""
        return '''
    <main class="main-content">
        <h1 style="margin-bottom: 20px;">Page Title</h1>
        <p>Content goes here...</p>
    </main>'''
    
    def _component_table(self):
        """Generate table component"""
        return '''
    <main class="main-content">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Column 1</th>
                        <th>Column 2</th>
                        <th>Column 3</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Data 1</td>
                        <td>Data 2</td>
                        <td>Data 3</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>'''
    
    def _component_form(self):
        """Generate form component"""
        return '''
    <main class="main-content">
        <div class="modal">
            <div class="modal-header">
                <h2 style="font-size: 18px;">Form Title</h2>
            </div>
            <div class="modal-body">
                <div style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px;">Label:</label>
                    <input type="text" class="form-input" placeholder="Enter value">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn" style="background: #f5f5f5; border: 1px solid #d9d9d9;">Cancel</button>
                <button class="btn btn-primary">Submit</button>
            </div>
        </div>
    </main>'''
    
    def _component_modal(self):
        """Generate modal component"""
        return self._component_form()  # Reuse form as modal
    
    def _html_scripts(self):
        """Generate JavaScript"""
        return '''
    <script>
        // Basic interactivity
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Prototype loaded');
        });
    </script>'''

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate HTML prototypes')
    parser.add_argument('--description', '-d', help='Text description of the prototype')
    parser.add_argument('--output', '-o', help='Output file name')
    parser.add_argument('--template', '-t', choices=['admin', 'form', 'table', 'dashboard'],
                       help='Use predefined template')
    
    args = parser.parse_args()
    
    generator = HTMLPrototypeGenerator()
    
    if args.description:
        generator.generate_from_description(args.description, args.output)
    elif args.template:
        templates = {
            'admin': 'Admin dashboard with sidebar, header, and data table',
            'form': 'Modal form with input fields and buttons',
            'table': 'Data table with filters and pagination',
            'dashboard': 'Analytics dashboard with charts and metrics'
        }
        generator.generate_from_description(templates[args.template], args.output)
    else:
        # Generate default admin template
        generator.generate_from_description('Admin dashboard with sidebar and table', 'index')

if __name__ == '__main__':
    main()