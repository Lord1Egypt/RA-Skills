"""
zlqa-gmt-api Skill 核心执行器
支持动态配置项目路径，适配不同用户环境
"""

import subprocess
import sys
import os
import re
import glob
import json
from datetime import datetime

# Skill 自身目录
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, 'skill_config.json')

# 用例分类映射
CASE_GROUP_MAP = {
    '正向': ['TC001', 'TC002', 'TC003'],
    '优先级': ['TC004', 'TC005'],
    '参数校验': ['TC006', 'TC007', 'TC008'],
    '异常': ['TC009', 'TC010', 'TC011', 'TC012'],
    '字段验证': ['TC013', 'TC014'],
    '状态验证': ['TC015', 'TC016', 'TC017', 'TC018'],
    '性能': ['TC019', 'TC020', 'TC021', 'TC022'],
    '全部': None,
}


# ─────────────────────────────────────────────
# 配置管理
# ─────────────────────────────────────────────

def load_config() -> dict:
    """加载 Skill 配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"project_root": "", "gmt_api_dir": "", "interfaces": {}}


def save_config(config: dict):
    """保存 Skill 配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def init_project(project_root: str) -> str:
    """
    初始化项目：扫描 api/gmt 目录，自动发现所有接口
    返回初始化结果描述
    """
    project_root = project_root.strip().strip('"').strip("'")

    if not os.path.exists(project_root):
        return f"[ERROR] 路径不存在: {project_root}"

    # 查找 api/gmt 目录
    gmt_api_dir = os.path.join(project_root, 'api', 'gmt')
    if not os.path.exists(gmt_api_dir):
        return f"[ERROR] 未找到 api/gmt 目录，请确认项目结构是否正确: {gmt_api_dir}"

    # 扫描接口目录（包含 run_tests.py 的子目录）
    interfaces = {}
    for item in os.listdir(gmt_api_dir):
        item_path = os.path.join(gmt_api_dir, item)
        if os.path.isdir(item_path):
            run_script = os.path.join(item_path, 'run_tests.py')
            if os.path.exists(run_script):
                interfaces[item] = item_path

    if not interfaces:
        return f"[ERROR] 未发现任何接口测试目录（需包含 run_tests.py）"

    # 保存配置
    config = {
        "project_root": project_root,
        "gmt_api_dir": gmt_api_dir,
        "interfaces": interfaces
    }
    save_config(config)

    lines = [f"[OK] 初始化成功！"]
    lines.append(f"[项目] {project_root}")
    lines.append(f"[发现接口] {len(interfaces)} 个:")
    for name, path in interfaces.items():
        lines.append(f"  - {name}: {path}")
    lines.append(f"\n现在可以使用: 执行 {list(interfaces.keys())[0]} 全部用例")
    return '\n'.join(lines)


def get_interface_map() -> dict:
    """获取接口映射，优先从配置文件读取"""
    config = load_config()
    if config.get('interfaces'):
        return config['interfaces']
    return {}


# ─────────────────────────────────────────────
# 意图解析
# ─────────────────────────────────────────────

def parse_intent(user_input: str):
    """
    解析用户意图
    返回: (action, interface_name, case_ids)
    action: 'init' | 'run' | 'report' | 'list'
    """
    user_input_lower = user_input.lower()

    # 初始化指令
    if any(kw in user_input for kw in ['初始化', 'init', '绑定项目', '配置项目']):
        # 提取路径
        path_match = re.search(r'[A-Za-z]:[\\\/][^\s]+|\/[^\s]+', user_input)
        path = path_match.group(0) if path_match else ''
        return 'init', path, None

    # 查看接口列表
    if any(kw in user_input for kw in ['接口列表', '支持哪些接口', '有哪些接口']):
        return 'list', None, None

    # 查看报告
    if any(kw in user_input for kw in ['查看报告', '打开报告', '测试报告']):
        interface_map = get_interface_map()
        for name in interface_map:
            if name.lower() in user_input_lower:
                return 'report', name, None
        return 'report', list(interface_map.keys())[0] if interface_map else None, None

    # 执行测试
    interface_map = get_interface_map()
    interface_name = None
    for name in interface_map:
        if name.lower() in user_input_lower:
            interface_name = name
            break

    if not interface_name:
        return 'unknown', None, None

    # 识别用例ID列表
    tc_ids = re.findall(r'TC\d+', user_input.upper())

    # 识别分组关键词
    if not tc_ids:
        for group_key, group_cases in CASE_GROUP_MAP.items():
            if group_key in user_input:
                tc_ids = group_cases
                break

    # 默认全部
    if not tc_ids and tc_ids != []:
        tc_ids = None

    return 'run', interface_name, tc_ids


# ─────────────────────────────────────────────
# 测试执行
# ─────────────────────────────────────────────

def set_execute_cases(script_path: str, case_ids):
    """修改 run_tests.py 中的 EXECUTE_CASES 配置"""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_value = 'None' if case_ids is None else str(case_ids)
    content = re.sub(
        r'EXECUTE_CASES\s*=\s*.*',
        f'EXECUTE_CASES = {new_value}',
        content
    )

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)


def run_tests(interface_name: str, case_ids) -> dict:
    """执行测试并返回结果"""
    interface_map = get_interface_map()
    interface_dir = interface_map.get(interface_name)

    if not interface_dir:
        return {'error': f'未找到接口: {interface_name}，请先执行初始化'}

    script_path = os.path.join(interface_dir, 'run_tests.py')
    if not os.path.exists(script_path):
        return {'error': f'测试脚本不存在: {script_path}'}

    # 设置要执行的用例
    set_execute_cases(script_path, case_ids)

    # 执行测试
    result = subprocess.run(
        ['python', 'run_tests.py'],
        cwd=interface_dir,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=120
    )

    # 找到最新的报告文件
    report_files = glob.glob(os.path.join(interface_dir, '*_report_*.html'))
    latest_report = max(report_files, key=os.path.getmtime) if report_files else None

    return {
        'stdout': result.stdout,
        'stderr': result.stderr,
        'returncode': result.returncode,
        'report_path': latest_report,
        'interface': interface_name,
        'case_ids': case_ids,
        'interface_dir': interface_dir,
    }


def open_latest_report(interface_name: str) -> str:
    """打开最新报告"""
    interface_map = get_interface_map()
    interface_dir = interface_map.get(interface_name)
    if not interface_dir:
        return f"[ERROR] 未找到接口: {interface_name}"

    report_files = glob.glob(os.path.join(interface_dir, '*_report_*.html'))
    if not report_files:
        return f"[ERROR] 未找到报告文件，请先执行测试"

    latest = max(report_files, key=os.path.getmtime)
    os.startfile(latest)
    return f"[OK] 已打开报告: {os.path.basename(latest)}"


# ─────────────────────────────────────────────
# 结果解析与展示
# ─────────────────────────────────────────────

def parse_results(stdout: str) -> dict:
    """从输出中解析测试结果"""
    results = {
        'passed': 0, 'failed': 0, 'error': 0, 'total': 0,
        'fail_cases': [], 'pass_cases': [],
    }

    lines = stdout.split('\n')
    for i, line in enumerate(lines):
        if '[PASS]' in line and re.search(r'\d+', line) and ':' in line:
            m = re.search(r'(\d+)', line)
            if m:
                results['passed'] = int(m.group(1))
        elif '[FAIL]' in line and re.search(r'\d+', line) and ':' in line:
            m = re.search(r'(\d+)', line)
            if m:
                results['failed'] = int(m.group(1))
        elif '[ERROR]' in line and re.search(r'\d+', line) and ':' in line:
            m = re.search(r'(\d+)', line)
            if m:
                results['error'] = int(m.group(1))
        elif '[TOTAL]' in line and re.search(r'\d+', line) and ':' in line:
            m = re.search(r'(\d+)', line)
            if m:
                results['total'] = int(m.group(1))

        m = re.match(r'\[(\d+)/(\d+)\]', line)
        if m and i + 1 < len(lines):
            case_match = re.search(r'TC\d+[^\n]*', line)
            case_name = case_match.group(0).strip() if case_match else line.strip()
            next_line = lines[i + 1]
            if '[PASS]' in next_line:
                results['pass_cases'].append(case_name)
            elif '[FAIL]' in next_line or '[ERROR]' in next_line:
                results['fail_cases'].append(case_name)

    return results


def format_summary(run_result: dict, parsed: dict) -> str:
    """格式化输出摘要"""
    interface = run_result.get('interface', '')
    case_ids = run_result.get('case_ids')
    report_path = run_result.get('report_path', '')

    sep = '=' * 50
    lines = [f"\n{sep}"]
    lines.append(f"[接口] {interface}")
    lines.append(f"[用例] {', '.join(case_ids) if case_ids else '全部'}")
    lines.append(sep)

    passed = parsed['passed']
    failed = parsed['failed']
    error  = parsed['error']
    total  = parsed['total']

    lines.append(f"\n[统计]")
    lines.append(f"  通过: {passed}  失败: {failed}  错误: {error}  总计: {total}")

    # FAIL 用例重点展示
    if parsed['fail_cases']:
        lines.append(f"\n{sep}")
        lines.append(f"[!!! FAIL 用例 - 需关注 !!!]")
        lines.append(sep)
        for case in parsed['fail_cases']:
            lines.append(f"  [FAIL] {case}")
    else:
        lines.append(f"\n[OK] 全部通过！")

    if report_path:
        lines.append(f"\n[报告] {os.path.basename(report_path)}")

    lines.append(f"{sep}\n")
    return '\n'.join(lines)


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

def main(user_input: str):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    action, interface_name, case_ids = parse_intent(user_input)

    # 初始化
    if action == 'init':
        if not interface_name:
            print("[ERROR] 请提供项目路径，例如: 初始化 C:\\Users\\xxx\\ZLQA")
            return
        print(init_project(interface_name))
        return

    # 查看接口列表
    if action == 'list':
        interface_map = get_interface_map()
        if not interface_map:
            print("[ERROR] 尚未初始化，请先执行: 初始化 <项目路径>")
            return
        print(f"\n[支持的接口] 共 {len(interface_map)} 个:")
        for name, path in interface_map.items():
            print(f"  - {name}: {path}")
        return

    # 打开报告
    if action == 'report':
        if not interface_name:
            print("[ERROR] 请指定接口名称")
            return
        print(open_latest_report(interface_name))
        return

    # 未识别
    if action == 'unknown':
        interface_map = get_interface_map()
        if not interface_map:
            print("[提示] 尚未初始化，请先执行: 初始化 <项目路径>")
        else:
            print(f"[提示] 未识别接口，支持: {', '.join(interface_map.keys())}")
        return

    # 执行测试
    print(f"[识别] 接口: {interface_name}, 用例: {case_ids or '全部'}")
    run_result = run_tests(interface_name, case_ids)

    if 'error' in run_result:
        print(f"[ERROR] {run_result['error']}")
        return

    parsed = parse_results(run_result['stdout'])
    print(format_summary(run_result, parsed))

    # 自动打开报告
    if run_result.get('report_path'):
        os.startfile(run_result['report_path'])
        print(f"[报告] 已自动打开浏览器")


if __name__ == '__main__':
    user_input = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else input("请输入测试指令: ")
    main(user_input)
