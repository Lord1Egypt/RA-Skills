#!/usr/bin/env python3
"""
源码分析器 - 提取代码结构、依赖关系和调用链路
"""

import os
import json
import subprocess
from typing import Dict, List, Any

class SourceAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.analysis_result = {
            'code_structure': {},
            'dependencies': {},
            'call_chains': {},
            'logical_mapping': {}
        }
    
    def analyze_code_structure(self):
        """分析代码目录结构和文件依赖"""
        # 使用 tree 命令获取目录结构
        try:
            result = subprocess.run(['tree', '-J', self.project_path], 
                                  capture_output=True, text=True, check=True)
            tree_data = json.loads(result.stdout)
            self.analysis_result['code_structure'] = tree_data
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to manual directory traversal
            self._manual_structure_analysis()
    
    def _manual_structure_analysis(self):
        """手动目录结构分析（tree不可用时）"""
        structure = []
        for root, dirs, files in os.walk(self.project_path):
            rel_root = os.path.relpath(root, self.project_path)
            if rel_root == '.':
                rel_root = ''
            
            dir_info = {
                'type': 'directory',
                'name': os.path.basename(root) if rel_root else os.path.basename(self.project_path),
                'path': rel_root,
                'children': []
            }
            
            # Add files
            for file in files:
                if not file.startswith('.'):
                    dir_info['children'].append({
                        'type': 'file',
                        'name': file,
                        'path': os.path.join(rel_root, file) if rel_root else file
                    })
            
            # Add subdirectories (will be filled in later)
            structure.append(dir_info)
        
        self.analysis_result['code_structure'] = structure
    
    def analyze_dependencies(self):
        """分析文件间依赖关系"""
        # 使用 ripgrep 分析 import/require 语句
        dependencies = {}
        
        # Python imports
        try:
            py_result = subprocess.run([
                'rg', '--type', 'python', '--json', 
                r'(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_.]*)'
            ], cwd=self.project_path, capture_output=True, text=True)
            
            if py_result.returncode == 0:
                for line in py_result.stdout.strip().split('\n'):
                    if line:
                        try:
                            match = json.loads(line)
                            if 'data' in match and 'submatches' in match['data']:
                                file_path = match['data']['path']['text']
                                for submatch in match['data']['submatches']:
                                    module_name = submatch['match']['text']
                                    if file_path not in dependencies:
                                        dependencies[file_path] = []
                                    dependencies[file_path].append(module_name)
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            pass
        
        self.analysis_result['dependencies'] = dependencies
    
    def generate_logical_mapping(self, business_domains: List[str] = None):
        """生成逻辑层映射（基于业务域）"""
        if business_domains is None:
            business_domains = ['core', 'api', 'service', 'model', 'utils']
        
        logical_mapping = {}
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_path)
                    
                    # 简单的业务域映射逻辑
                    logical_domain = 'unknown'
                    for domain in business_domains:
                        if domain in rel_path.lower():
                            logical_domain = domain
                            break
                    
                    logical_mapping[rel_path] = {
                        'physical_path': rel_path,
                        'logical_domain': logical_domain,
                        'business_function': self._extract_business_function(file_path)
                    }
        
        self.analysis_result['logical_mapping'] = logical_mapping
    
    def _extract_business_function(self, file_path: str) -> str:
        """从文件中提取业务功能描述"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单提取：查找函数名或类名中的业务关键词
                # 这里可以扩展为更复杂的NLP分析
                return "业务功能待分析"
        except:
            return "无法分析"
    
    def save_analysis(self, output_path: str):
        """保存分析结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_result, f, indent=2, ensure_ascii=False)
    
    def run_full_analysis(self, output_path: str = None):
        """执行完整分析"""
        print("🔍 分析代码结构...")
        self.analyze_code_structure()
        
        print("🔗 分析依赖关系...")
        self.analyze_dependencies()
        
        print("🧠 生成逻辑映射...")
        self.generate_logical_mapping()
        
        if output_path:
            self.save_analysis(output_path)
            print(f"✅ 分析结果已保存到: {output_path}")
        
        return self.analysis_result

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python source-analyzer.py <project_path> [output_path]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyzer = SourceAnalyzer(project_path)
    result = analyzer.run_full_analysis(output_path)