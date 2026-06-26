#!/usr/bin/env python3
"""
代码功能测试主程序
根据用户需求搜索代码、生成测试用例、执行测试并尝试修复问题
"""

import os
import sys
import json
import subprocess
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


PROJECT_ROOT = Path(__file__).parent.parent.parent
SKILL_DIR = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
SCRIPTS_DIR = SKILL_DIR / "scripts"
LOG_DIR = SCRIPTS_DIR / "log"
RELEASE_DIR = SCRIPTS_DIR / "release"


def ensure_dirs():
    """确保必要的目录存在"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)


def search_code(keywords: list, project_root: Path) -> list:
    """搜索与关键词相关的代码"""
    results = []
    
    py_files = list(project_root.glob("**/*.py"))
    py_files = [f for f in py_files if ".opencode" not in str(f) and "skill" not in f.name.lower()]
    
    priority_score = {
        "def ": 3,
        "class ": 3,
        "async def ": 3,
        "import ": 1,
        "from ": 1,
    }
    
    for py_file in py_files:
        try:
            content = py_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                priority = 0
                
                for kw in keywords:
                    if kw.lower() in line.lower():
                        for kw_prefix, p in priority_score.items():
                            if kw_prefix in line_stripped:
                                priority = p
                                break
                        results.append({
                            "file": str(py_file),
                            "line": i,
                            "content": line_stripped,
                            "keyword": kw,
                            "priority": priority
                        })
                        break
        except Exception as e:
            continue
    
    results.sort(key=lambda x: x.get("priority", 0), reverse=True)
    return results


def extract_function_class(code: str, target_name: str) -> dict:
    """提取目标类或函数的完整代码"""
    lines = code.split("\n")
    result = {
        "name": target_name,
        "type": "function",
        "code": [],
        "start_line": 0,
        "end_line": 0,
        "file": ""
    }
    
    class_stack = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        if line_stripped.startswith("class "):
            class_match = re.match(r'class (\w+)', line_stripped)
            if class_match:
                class_stack.append({
                    "name": class_match.group(1),
                    "indent": len(line) - len(line.lstrip())
                })
        
        if f"def {target_name}(" in line:
            in_target = True
            result["type"] = "method" if class_stack else "function"
            result["start_line"] = i + 1
            result["class_name"] = class_stack[-1]["name"] if class_stack else None
            indent = len(line) - len(line.lstrip())
            result["code"].append(line)
            
            for j in range(i + 1, len(lines)):
                next_line = lines[j]
                if next_line.strip():
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= indent:
                        result["end_line"] = j
                        break
                    result["code"].append(next_line)
            else:
                result["end_line"] = len(lines)
            break
        elif f"class {target_name}" in line:
            result["type"] = "class"
            result["start_line"] = i + 1
            indent = len(line) - len(line.lstrip())
            result["code"].append(line)
            
            for j in range(i + 1, len(lines)):
                next_line = lines[j]
                if next_line.strip():
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= indent:
                        result["end_line"] = j
                        break
                    result["code"].append(next_line)
            else:
                result["end_line"] = len(lines)
            break
    
    return result


def generate_test_case(target_info: dict, requirement: str) -> dict:
    """生成测试用例"""
    test_case = {
        "requirement": requirement,
        "target": target_info,
        "ground_truth_source": "auto" if is_mathematical_function(requirement) else "external",
        "test_code": "",
        "expected_behavior": ""
    }
    
    if is_mathematical_function(requirement):
        test_case["test_code"] = generate_math_test(target_info, requirement)
        test_case["expected_behavior"] = "数学验证通过"
    else:
        test_case["test_code"] = generate_external_test(target_info, requirement)
        test_case["expected_behavior"] = "需要外部数据验证"
    
    return test_case


def is_mathematical_function(requirement: str) -> bool:
    """判断是否为数学分析类功能"""
    math_keywords = ["聚类", "cluster", "插值", "interpolat", "回归", "regress", 
                     "统计", "statistic", "计算", "calculat", "优化", "optimiz",
                     "矩阵", "matrix", "排序", "sort", "搜索", "search"]
    return any(kw in requirement.lower() for kw in math_keywords)


def generate_math_test(target_info: dict, requirement: str) -> str:
    """生成数学验证测试"""
    target_name = target_info.get("name", "unknown")
    target_type = target_info.get("type", "function")
    code_lines = target_info.get("code", [])
    class_name = target_info.get("class_name")
    file_path = target_info.get("file", "")
    
    module_name = file_path.split("/")[-1].replace(".py", "")
    
    if target_type == "method" or class_name:
        import_path = f"from {module_name} import {class_name}"
        test_invocation = f"{class_name}().{target_name}("
    else:
        import_path = f"from {module_name} import {target_name}"
        test_invocation = f"{target_name}("
    
    if "cluster" in requirement.lower() or "聚类" in requirement:
        test_code = f'''import unittest
import numpy as np
import pandas as pd
import sys
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "references", "test_data_cluster.csv")

def generate_test_data():
    """生成带已知聚类标签的测试数据并保存"""
    np.random.seed(42)
    n_per_cluster = 20
    
    centers = np.array([
        [1.0, 100, 10],   # 聚类1中心
        [3.0, 300, 30],   # 聚类2中心
        [5.0, 400, 40],   # 聚类3中心
    ])
    
    data_list = []
    labels = []
    
    for i, center in enumerate(centers):
        for _ in range(n_per_cluster):
            point = center + np.random.normal(0, 0.3, size=3)
            data_list.append(point)
            labels.append(i)
    
    data = pd.DataFrame(data_list, columns=['TiO2', 'Zr', 'Nb'])
    data['true_label'] = labels
    
    data.to_csv(DATA_PATH, index=False)
    print(f"测试数据已保存: {{DATA_PATH}}")
    return data

def load_test_data():
    """加载测试数据"""
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return generate_test_data()

from {module_name} import {class_name}

class Test{target_name.capitalize()}(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """生成并保存测试数据"""
        cls.data = generate_test_data()
        cls.centers = np.array([
            [1.0, 100, 10],
            [3.0, 300, 30],
            [5.0, 400, 40],
        ])
    
    def test_clustering_correctness(self):
        """验证聚类结果的正确性"""
        stats = {class_name}(self.data[['TiO2', 'Zr', 'Nb']])
        
        result = stats.cluster_analysis(
            elements=['TiO2', 'Zr', 'Nb'],
            n_clusters=3,
            method='kmeans'
        )
        
        self.assertIn('cluster_centers', result)
        cluster_centers = np.array(result['cluster_centers'])
        
        for true_center in self.centers:
            distances = np.linalg.norm(cluster_centers - true_center, axis=1)
            min_dist = np.min(distances)
            self.assertLess(min_dist, 1.0, 
                f"聚类中心距离过大: {{true_center}}, 最近中心距离: {{min_dist}}")
    
    def test_cluster_stability(self):
        """验证聚类稳定性（多次运行结果一致）"""
        stats1 = {class_name}(self.data[['TiO2', 'Zr', 'Nb']])
        result1 = stats1.cluster_analysis(
            elements=['TiO2', 'Zr', 'Nb'],
            n_clusters=3,
            method='kmeans'
        )
        
        stats2 = {class_name}(self.data[['TiO2', 'Zr', 'Nb']])
        result2 = stats2.cluster_analysis(
            elements=['TiO2', 'Zr', 'Nb'],
            n_clusters=3,
            method='kmeans'
        )
        
        centers1 = np.array(result1['cluster_centers'])
        centers2 = np.array(result2['cluster_centers'])
        
        distances = np.linalg.norm(centers1 - centers2, axis=1)
        self.assertLess(np.max(distances), 0.1, "聚类结果不稳定")
    
    def test_element_subset(self):
        """测试元素子集聚类"""
        stats = {class_name}(self.data[['TiO2', 'Zr']])
        
        result = stats.cluster_analysis(
            elements=['TiO2', 'Zr'],
            n_clusters=3,
            method='kmeans'
        )
        
        self.assertEqual(result['n_clusters'], 3)

if __name__ == "__main__":
    unittest.main()
'''
    else:
        test_code = f'''import unittest
import numpy as np
import pandas as pd
import sys
import os

{import_path}

class Test{target_name.capitalize()}(unittest.TestCase):
    def test_basic_functionality(self):
        """基础功能测试"""
        # 创建测试数据
        test_data = pd.DataFrame({{
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        }})
        
        # 执行测试
        # {test_invocation}
        
        # 验证结果
        # self.assertIsNotNone(result)
        pass

    def test_edge_cases(self):
        """边界情况测试"""
        # 空输入
        empty_data = pd.DataFrame()
        
        # 验证边界情况处理
        pass

if __name__ == "__main__":
    unittest.main()
'''
    return test_code


def generate_external_test(target_info: dict, requirement: str) -> str:
    """生成外部数据测试"""
    target_name = target_info.get("name", "unknown")
    test_code = f'''import unittest
import sys
import os

class Test{target_name.capitalize()}(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """下载或加载外部测试数据"""
        # 数据文件路径
        cls.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "references", "test_data.csv")
        
        # 如果数据不存在，提示用户下载
        # 或者使用以下方式下载:
        # import urllib.request
        # urllib.request.urlretrieve("url", cls.data_path)
        
        if not os.path.exists(cls.data_path):
            print("请提供测试数据文件: {{cls.data_path}}")
            raise FileNotFoundError("测试数据文件不存在")
    
    def test_with_real_data(self):
        """使用真实数据测试"""
        import pandas as pd
        # df = pd.read_csv(self.data_path)
        # result = your_function(df)
        pass

if __name__ == "__main__":
    unittest.main()
'''
    return test_code


def install_requirements():
    """自动安装依赖"""
    req_file = SCRIPTS_DIR / "requirements.txt"
    if req_file.exists():
        try:
            subprocess.run(["pip", "install", "-r", str(req_file)], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    return False


def run_test(test_file: Path) -> dict:
    """运行测试并返回结果"""
    result = {
        "timestamp": datetime.now().isoformat(),
        "test_file": str(test_file),
        "passed": False,
        "output": "",
        "error": None,
        "version": 0,
        "needs_fix": False,
        "fix_action": None
    }
    
    try:
        proc = subprocess.run(
            ["python", "-m", "pytest", str(test_file), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60
        )
        result["output"] = proc.stdout + proc.stderr
        result["passed"] = proc.returncode == 0
        
        if not result["passed"]:
            combined_output = result["output"]
            
            if "No module named" in combined_output:
                module_name = re.search(r"No module named '(\w+)'", combined_output)
                if module_name:
                    result["error"] = f"缺少模块: {module_name.group(1)}"
                    result["needs_fix"] = True
                    result["fix_action"] = f"install_module"
            elif "ImportError" in combined_output or "ModuleNotFoundError" in combined_output:
                result["error"] = "导入错误"
                result["needs_fix"] = True
                result["fix_action"] = "install_module"
            elif "SyntaxError" in combined_output:
                result["error"] = "语法错误"
                result["needs_fix"] = True
                result["fix_action"] = "fix_syntax"
            elif "Error" in combined_output or "Exception" in combined_output:
                result["error"] = "运行时错误"
                result["needs_fix"] = True
                result["fix_action"] = "analyze_error"
            else:
                result["error"] = "测试失败"
                
    except subprocess.TimeoutExpired:
        result["error"] = "测试超时"
        result["needs_fix"] = True
        result["fix_action"] = "timeout"
    except Exception as e:
        result["error"] = str(e)
        result["needs_fix"] = True
        result["fix_action"] = "exception"
    
    return result


def save_log(result: dict, version: int):
    """保存测试日志"""
    log_file = LOG_DIR / f"test_log_v{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return log_file


def get_next_version() -> int:
    """获取下一个版本号"""
    if not RELEASE_DIR.exists():
        return 1
    
    versions = []
    for d in RELEASE_DIR.iterdir():
        if d.is_dir() and d.name.startswith("v"):
            try:
                versions.append(int(d.name[1:]))
            except ValueError:
                continue
    
    return max(versions) + 1 if versions else 1


def analyze_and_fix(error_msg: str, code_info: dict) -> str:
    """分析错误并尝试修复代码"""
    fix_suggestions = []
    
    if "NoneType" in error_msg and "None" in error_msg:
        fix_suggestions.append("检查空值处理，添加None类型检查")
    if "IndexError" in error_msg:
        fix_suggestions.append("检查数组索引边界")
    if "KeyError" in error_msg:
        fix_suggestions.append("检查字典键是否存在")
    if "ValueError" in error_msg:
        fix_suggestions.append("检查输入值的有效性")
    if "AttributeError" in error_msg:
        fix_suggestions.append("检查对象属性和方法")
    if "ImportError" in error_msg:
        fix_suggestions.append("检查模块导入路径")
    
    return "\n".join(fix_suggestions) if fix_suggestions else "需要手动分析错误原因"


def update_project_code(original_file: Path, code_info: dict, version: int):
    """将修复后的代码更新到项目"""
    backup_file = original_file.with_suffix(original_file.suffix + ".bak")
    
    try:
        import shutil
        shutil.copy(original_file, backup_file)
        
        content = original_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        target_name = code_info.get("name", "")
        start = code_info.get("start_line", 1) - 1
        end = code_info.get("end_line", len(lines))
        
        fixed_lines = code_info.get("code", [])
        
        new_lines = lines[:start] + fixed_lines + lines[end:]
        
        original_file.write_text("\n".join(new_lines), encoding="utf-8")
        
        return True, "代码已更新"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="代码功能测试工具")
    parser.add_argument("--requirement", "-r", required=True, help="测试需求描述")
    parser.add_argument("--keywords", "-k", help="搜索关键词，用逗号分隔")
    parser.add_argument("--fix", action="store_true", help="是否自动尝试修复")
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    keywords = args.keywords.split(",") if args.keywords else args.requirement.split()
    
    print(f"[*] 搜索关键词: {keywords}")
    results = search_code(keywords, PROJECT_ROOT)
    
    if not results:
        print("[!] 未找到相关代码")
        return
    
    print(f"[*] 找到 {len(results)} 处相关代码")
    for r in results[:5]:
        print(f"    {r['file']}:{r['line']} - {r['content'][:60]}")
    
    target = results[0]
    target_file = Path(target["file"])
    code_content = target_file.read_text(encoding="utf-8")
    
    target_keyword = target.get("keyword", keywords[0])
    match = re.search(r'(def|class)\s+(\w+)', target["content"])
    if match:
        target_keyword = match.group(2)
    
    target_info = extract_function_class(code_content, target_keyword)
    target_info["file"] = str(target_file)
    
    print(f"[*] 目标: {target_info['name']} ({target_info['type']})")
    
    test_case = generate_test_case(target_info, args.requirement)
    
    test_file = REFERENCES_DIR / f"test_{target_info['name']}.py"
    test_file.write_text(test_case["test_code"], encoding="utf-8")
    print(f"[*] 测试用例已保存: {test_file}")
    
    result = run_test(test_file)
    
    if not result["passed"] and result.get("needs_fix"):
        fix_action = result.get("fix_action")
        
        if fix_action == "install_module":
            print("[*] 检测到缺少模块，尝试安装依赖...")
            if install_requirements():
                print("[+] 依赖安装成功，重新运行测试...")
                result = run_test(test_file)
            else:
                print("[!] 依赖安装失败，请手动安装")
    
    version = get_next_version()
    log_file = save_log(result, version)
    print(f"[*] 测试结果: {'通过' if result['passed'] else '失败'}")
    print(f"[*] 日志已保存: {log_file}")
    
    if not result["passed"]:
        print(f"[!] 错误信息: {result.get('error', '未知错误')}")
        
        if args.fix or result.get("needs_fix"):
            fix_suggestions = analyze_and_fix(result.get("error", "") + result.get("output", ""), target_info)
            print(f"[*] 修复建议:\n{fix_suggestions}")
            
            release_dir = RELEASE_DIR / f"v{version}"
            release_dir.mkdir(exist_ok=True)
            
            release_test = release_dir / f"test_{target_info['name']}.py"
            release_test.write_text(test_case["test_code"], encoding="utf-8")
            
            print(f"[*] 已保存到: {release_dir}")
    
    print(f"\n[+] 测试完成")


if __name__ == "__main__":
    main()
