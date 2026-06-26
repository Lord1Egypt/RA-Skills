#!/usr/bin/env python3
"""
日志分析脚本 - 解析服务器日志文件，提取关键问题和性能指标
支持格式: [时间] 模块路径 日志级别 行号: 消息
新增功能: Python Traceback异常追踪
"""

import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import io

# 修复Windows控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class ExceptionTracker:
    """Python异常追踪器"""

    def __init__(self):
        self.exceptions: List[Dict] = []
        self.current_exception: Optional[Dict] = None
        self.in_traceback = False
        self.traceback_lines: List[str] = []

    def process_line(self, line: str, line_num: int, entry: Optional[Dict]) -> Optional[Dict]:
        """处理每行日志，检测异常"""
        # 检测异常开始标记
        if 'Traceback (most recent call last):' in line:
            self.in_traceback = True
            self.traceback_lines = []
            if entry:
                self.current_exception = {
                    'start_line': line_num,
                    'timestamp': entry.get('timestamp_str', ''),
                    'module': entry.get('module', ''),
                    'level': entry.get('level', 'ERROR'),
                    'error_msg': entry.get('message', ''),
                    'traceback': '',
                    'exception_type': '',
                    'exception_msg': '',
                    'source_files': [],
                }
            return None

        # 如果在Traceback中
        if self.in_traceback:
            self.traceback_lines.append(line)

            # 检测异常类型 (通常是最后一行的错误类型)
            # 例如: RuntimeError: (PreconditionNotMet) Tensor holds no memory.
            runtime_match = re.match(r'(\w+Error|\w+Exception):\s*(.+)', line)
            if runtime_match:
                exc_type = runtime_match.group(1)
                exc_msg = runtime_match.group(2)
                if self.current_exception:
                    self.current_exception['exception_type'] = exc_type
                    self.current_exception['exception_msg'] = exc_msg

            # 提取源文件信息
            # 例如: File "/path/to/file.py", line 123, in function_name
            file_match = re.match(r'\s+File "(.+)", line (\d+), in (.+)', line)
            if file_match:
                file_path = file_match.group(1)
                file_line = file_match.group(2)
                func_name = file_match.group(3)
                if self.current_exception:
                    self.current_exception['source_files'].append({
                        'file': file_path,
                        'line': int(file_line),
                        'function': func_name
                    })

            # 检测异常结束（空行或新的日志行）
            if not line.strip() or (entry and line.startswith('[')):
                self._finalize_exception()
                return None

        return None

    def _finalize_exception(self):
        """完成异常记录"""
        if self.current_exception and self.traceback_lines:
            # 限制traceback长度
            self.current_exception['traceback'] = '\n'.join(self.traceback_lines[:50])

            # 计算关键源文件（通常是项目自己的代码，非phi/phi_core等底层库）
            project_files = []
            for sf in self.current_exception.get('source_files', []):
                file_path = sf['file']
                # 过滤掉 Paddle 底层库，只保留项目代码
                if '/home/javanep/' in file_path or '/home/' in file_path:
                    if 'paddle' not in file_path.lower() and 'phi' not in file_path.lower():
                        project_files.append(sf)

            if project_files:
                self.current_exception['key_source'] = project_files[0]  # 最内层项目代码

            self.exceptions.append(self.current_exception)

        self.in_traceback = False
        self.current_exception = None
        self.traceback_lines = []

    def finalize(self):
        """处理结束时确保所有异常都被记录"""
        self._finalize_exception()


class LogAnalyzer:
    """日志分析器"""

    # 日志行正则表达式
    LOG_PATTERN = re.compile(
        r'\[(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})\] '  # 时间戳
        r'(\S+) '  # 模块路径
        r'(INFO|WARNING|ERROR|CRITICAL) '  # 日志级别
        r'(\d+): '  # 行号
        r'(.+)'  # 消息
    )

    # 关键问题模式定义
    ISSUE_PATTERNS = {
        # 数据库问题
        'db_update_failed': (re.compile(r'\[DB\]\s*更新失败'), '数据库更新失败', 'high'),
        'db_insert_failed': (re.compile(r'\[DB\]\s*插入失败'), '数据库插入失败', 'high'),

        # 邮件问题
        'email_failed': (re.compile(r'\[Email\]\s*无法获取.*发送邮件通知失败'), '邮件通知失败', 'medium'),

        # OCR/识别问题
        'no_valid_answer': (re.compile(r'图像无有效答题'), '图像无有效答题区域', 'medium'),
        'invalid_student_no': (re.compile(r'识别出无效学号'), '学号识别失败', 'low'),
        'paper_type_error': (re.compile(r'纸张类型识别错误|所有图像均为 classify=0/未知'), '纸张类型识别失败', 'medium'),

        # 批改问题
        'no_corrector': (re.compile(r'topic type \d+ has no corrector'), '题目缺少批改器', 'high'),

        # 性能问题
        'slow_processing': (re.compile(r'耗时.*\d+\.\d+s'), '处理耗时', 'low'),

        # 模型问题
        'batch_proxy': (re.compile(r'开始批量处理图片|被分为\d+组'), '批量模型推理', 'low'),
    }

    # 模块分类
    MODULE_CATEGORIES = {
        'flow': '工作流',
        'workers': 'Worker处理器',
        'task': '任务调度',
        'math_tools': '数学工具',
        'models': '模型推理',
        'correction': '批改',
    }

    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.entries: List[Dict] = []
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.info_stats: Counter = Counter()
        self.issues: Dict[str, List[Dict]] = defaultdict(list)
        self.performance_stats: Dict = {
            'total_batches': 0,
            'total_items': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
            'tps_list': [],
        }
        self.module_stats: Counter = Counter()
        self.exception_tracker = ExceptionTracker()

    def parse_line(self, line: str, line_num: int) -> Optional[Dict]:
        """解析单行日志"""
        match = self.LOG_PATTERN.match(line)
        if not match:
            return None

        timestamp_str, module, level, line_no, message = match.groups()

        # 解析时间
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y/%m/%d %H:%M:%S')
        except ValueError:
            timestamp = None

        entry = {
            'line_num': line_no,
            'timestamp': timestamp,
            'timestamp_str': timestamp_str,
            'module': module,
            'level': level,
            'line_no': int(line_no),
            'message': message,
        }

        # 检测问题
        self._detect_issues(entry)

        # 提取性能数据
        self._extract_performance(entry)

        # 统计模块
        self._update_module_stats(module)

        # 检测异常 (Python Traceback)
        self.exception_tracker.process_line(line, line_num, entry)

        return entry

    def _detect_issues(self, entry: Dict):
        """检测日志中的问题"""
        message = entry['message']

        for issue_type, (pattern, desc, severity) in self.ISSUE_PATTERNS.items():
            if pattern.search(message):
                entry['issue_type'] = issue_type
                entry['issue_desc'] = desc
                entry['severity'] = severity
                self.issues[issue_type].append(entry)

                if entry['level'] == 'ERROR':
                    self.errors.append(entry)
                elif entry['level'] == 'WARNING':
                    self.warnings.append(entry)
                break

    def _extract_performance(self, entry: Dict):
        """提取性能统计数据"""
        message = entry['message']

        # 批改完成统计
        match = re.search(r'批改完成:\s*(\d+)\s*条数据', message)
        if match:
            self.performance_stats['total_items'] += int(match.group(1))

        # 耗时统计
        match = re.search(r'耗时[:：]?\s*(\d+\.\d+)s', message)
        if match:
            self.performance_stats['total_time'] += float(match.group(1))

        # TPS统计
        match = re.search(r'tps=(\d+\.\d+)', message)
        if match:
            self.performance_stats['tps_list'].append(float(match.group(1)))

        # 批次统计
        if '批改完成' in message:
            self.performance_stats['total_batches'] += 1

        # 统计特定耗时
        if 'batch_process cost:' in message:
            match = re.search(r'batch_process cost:\s*(\d+\.\d+)s', message)
            if match:
                entry['batch_time'] = float(match.group(1))

    def _update_module_stats(self, module: str):
        """更新模块统计"""
        self.module_stats[module] += 1

    def analyze(self) -> Dict:
        """执行完整分析"""
        if not self.log_file.exists():
            return {'error': f'文件不存在: {self.log_file}'}

        last_entry = None
        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    # 空行也可能是异常结束标记
                    self.exception_tracker.process_line(line, line_num, last_entry)
                    continue

                entry = self.parse_line(line, line_num)
                if entry:
                    self.entries.append(entry)
                    last_entry = entry
                else:
                    # 非标准日志行（如 Traceback），仍然进行异常检测
                    self.exception_tracker.process_line(line, line_num, last_entry)

        # 确保处理完所有异常
        self.exception_tracker.finalize()

        return self.generate_report()

    def generate_report(self) -> Dict:
        """生成分析报告"""
        report = {
            'log_file': str(self.log_file),
            'total_lines': len(self.entries),
            'timestamp_range': self._get_time_range(),
            'summary': self._generate_summary(),
            'issues': self._summarize_issues(),
            'performance': self._generate_performance_report(),
            'modules': self._generate_module_report(),
            'critical_issues': self._get_critical_issues(),
            'exceptions': self._generate_exception_report(),  # 新增：异常报告
        }

        return report

    def _get_time_range(self) -> Dict:
        """获取时间范围"""
        timestamps = [e['timestamp'] for e in self.entries if e['timestamp']]
        if not timestamps:
            return {}

        return {
            'start': min(timestamps).strftime('%Y-%m-%d %H:%M:%S') if min(timestamps) else None,
            'end': max(timestamps).strftime('%Y-%m-%d %H:%M:%S') if max(timestamps) else None,
            'duration_seconds': (max(timestamps) - min(timestamps)).total_seconds() if min(timestamps) and max(timestamps) else 0,
        }

    def _generate_summary(self) -> Dict:
        """生成总体摘要"""
        level_counts = Counter(e['level'] for e in self.entries)

        return {
            'total_entries': len(self.entries),
            'info_count': level_counts.get('INFO', 0),
            'warning_count': level_counts.get('WARNING', 0),
            'error_count': level_counts.get('ERROR', 0),
            'critical_count': level_counts.get('CRITICAL', 0),
            'total_issues': len(self.errors) + len(self.warnings),
            'total_exceptions': len(self.exception_tracker.exceptions),
        }

    def _summarize_issues(self) -> Dict:
        """汇总问题"""
        summary = {}
        for issue_type, entries in self.issues.items():
            if entries:
                desc = entries[0].get('issue_desc', issue_type)
                severity = entries[0].get('severity', 'low')
                summary[issue_type] = {
                    'description': desc,
                    'severity': severity,
                    'count': len(entries),
                    'examples': [
                        {
                            'line': e['line_num'],
                            'time': e.get('timestamp_str', ''),
                            'module': e['module'],
                            'message': e['message'][:200]
                        }
                        for e in entries[:3]
                    ]
                }
        return summary

    def _generate_performance_report(self) -> Dict:
        """生成性能报告"""
        stats = self.performance_stats.copy()

        # 计算平均TPS
        if stats['tps_list']:
            stats['avg_tps'] = sum(stats['tps_list']) / len(stats['tps_list'])
            stats['max_tps'] = max(stats['tps_list'])
            stats['min_tps'] = min(stats['tps_list'])
        else:
            stats['avg_tps'] = 0
            stats['max_tps'] = 0
            stats['min_tps'] = 0

        # 计算平均耗时
        if stats['total_batches'] > 0:
            stats['avg_time_per_batch'] = stats['total_time'] / stats['total_batches']
        else:
            stats['avg_time_per_batch'] = 0

        del stats['tps_list']  # 移除原始列表

        return stats

    def _generate_module_report(self) -> Dict:
        """生成模块报告"""
        return {
            'total_modules': len(self.module_stats),
            'top_modules': dict(self.module_stats.most_common(10)),
        }

    def _generate_exception_report(self) -> Dict:
        """生成异常报告"""
        exceptions = self.exception_tracker.exceptions

        if not exceptions:
            return {'count': 0, 'exceptions': [], 'by_type': {}, 'by_module': {}}

        # 按异常类型分组统计
        exception_types: Dict[str, int] = Counter()
        exception_by_module: Dict[str, int] = Counter()
        exception_details = []

        for exc in exceptions:
            exc_type = exc.get('exception_type', 'Unknown')
            exception_types[exc_type] += 1

            module = exc.get('module', 'unknown')
            exception_by_module[module] += 1

            # 提取关键代码位置
            key_file = 'N/A'
            key_line = 0
            key_func = 'N/A'

            key_source = exc.get('key_source')
            if key_source:
                # 简化文件路径显示
                file_path = key_source['file']
                # 只保留最后两个路径组件
                parts = file_path.split('/')
                key_file = '/'.join(parts[-2:]) if len(parts) >= 2 else file_path
                key_line = key_source.get('line', 0)
                key_func = key_source.get('function', 'N/A')

            exception_details.append({
                'timestamp': exc.get('timestamp', ''),
                'start_line': exc.get('start_line', 0),
                'exception_type': exc_type,
                'exception_msg': exc.get('exception_msg', '')[:150],
                'module': module,
                'key_file': key_file,
                'key_line': key_line,
                'key_function': key_func,
                'source_files': exc.get('source_files', [])[:3],
            })

        return {
            'count': len(exceptions),
            'by_type': dict(exception_types),
            'by_module': dict(exception_by_module),
            'details': exception_details,
        }

    def _get_critical_issues(self) -> List[Dict]:
        """获取关键问题列表"""
        critical = []

        # 首先添加异常（最高优先级）
        for exc in self.exception_tracker.exceptions[:10]:
            key_source = exc.get('key_source', {})
            exception_details = {
                'severity': 'critical',
                'type': 'exception',
                'description': f"{exc.get('exception_type', 'Unknown')}: {exc.get('exception_msg', '')[:80]}",
                'line': exc.get('start_line', 0),
                'time': exc.get('timestamp', ''),
                'module': exc.get('module', ''),
                'message': exc.get('error_msg', '')[:200] if exc.get('error_msg') else exc.get('exception_msg', '')[:200],
                'key_file': key_source.get('file', ''),
                'key_line': key_source.get('line', 0),
                'key_function': key_source.get('function', ''),
            }
            critical.append(exception_details)

        # 按严重程度排序其他问题
        for severity in ['high', 'medium', 'low']:
            for entries in self.issues.values():
                for entry in entries:
                    if entry.get('severity') == severity and severity in ['high', 'medium']:
                        critical.append({
                            'severity': severity,
                            'type': entry.get('issue_type', 'unknown'),
                            'description': entry.get('issue_desc', ''),
                            'line': entry['line_num'],
                            'time': entry.get('timestamp_str', ''),
                            'module': entry['module'],
                            'message': entry['message'][:200],
                        })

        return critical[:20]

    def print_report(self, report: Dict):
        """打印格式化报告"""
        print("\n" + "=" * 80)
        print("📊 服务器日志分析报告")
        print("=" * 80)

        # 基本信息
        print(f"\n📁 日志文件: {report['log_file']}")
        print(f"📝 总日志行数: {report['total_lines']}")

        if report.get('timestamp_range'):
            tr = report['timestamp_range']
            print(f"⏰ 时间范围: {tr.get('start', 'N/A')} ~ {tr.get('end', 'N/A')}")
            print(f"⏱️  总时长: {tr.get('duration_seconds', 0):.0f} 秒")

        # 总体摘要
        summary = report['summary']
        print("\n" + "-" * 40)
        print("📈 总体统计")
        print("-" * 40)
        print(f"  INFO:       {summary['info_count']:,} 条")
        print(f"  WARNING:    {summary['warning_count']:,} 条")
        print(f"  ERROR:      {summary['error_count']:,} 条")
        print(f"  ⛔ EXCEPTION: {summary.get('total_exceptions', 0):,} 个")
        print(f"  问题总计:   {summary['total_issues']:,} 个")

        # 异常报告（最高优先级）
        exc_report = report.get('exceptions', {})
        if exc_report.get('count', 0) > 0:
            print("\n" + "=" * 40)
            print("🚨 PYTHON 程序异常 (最高优先级)")
            print("=" * 40)
            print(f"  总计: {exc_report['count']} 个异常")

            # 按类型统计
            print("\n  📊 异常类型分布:")
            for exc_type, count in exc_report.get('by_type', {}).items():
                print(f"    - {exc_type}: {count} 次")

            # 按模块统计
            print("\n  📊 异常模块分布:")
            for module, count in exc_report.get('by_module', {}).items():
                print(f"    - {module}: {count} 次")

            # 详细列表
            print("\n  📋 异常详情:")
            for i, exc in enumerate(exc_report.get('details', [])[:10], 1):
                print(f"\n  {i}. 【{exc['exception_type']}】")
                print(f"     时间: {exc['timestamp']} | 行号: {exc['start_line']}")
                print(f"     模块: {exc['module']}")
                if exc['key_file'] != 'N/A':
                    print(f"     位置: {exc['key_file']}:{exc['key_line']} ({exc['key_function']})")
                print(f"     错误: {exc['exception_msg'][:100]}...")

        # 性能统计
        perf = report['performance']
        print("\n" + "-" * 40)
        print("⚡ 性能指标")
        print("-" * 40)
        print(f"  总处理批次: {perf['total_batches']:,}")
        print(f"  总处理数据: {perf['total_items']:,} 条")
        print(f"  平均TPS:    {perf['avg_tps']:.2f}")
        print(f"  最大TPS:    {perf['max_tps']:.2f}")
        print(f"  平均耗时:   {perf['avg_time_per_batch']:.2f}s/批次")

        # 问题汇总（排除异常）
        issues = report['issues']
        if issues:
            print("\n" + "-" * 40)
            print("🔍 问题汇总 (按严重程度)")
            print("-" * 40)

            for severity in ['high', 'medium', 'low']:
                severity_issues = {k: v for k, v in issues.items() if v.get('severity') == severity}
                if severity_issues:
                    icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(severity, '⚪')
                    print(f"\n  {icon} {severity.upper()} 级问题:")
                    for issue_type, info in severity_issues.items():
                        print(f"    - {info['description']}: {info['count']} 次")

            # 关键问题详情（排除异常，因为已经在上面展示了）
            critical = [c for c in report.get('critical_issues', []) if c.get('type') != 'exception']
            if critical:
                print("\n" + "-" * 40)
                print("📌 关键问题详情 (Top 10)")
                print("-" * 40)
                for i, issue in enumerate(critical[:10], 1):
                    print(f"\n  {i}. [{issue['severity'].upper()}] {issue['description']}")
                    print(f"     行号: {issue['line']} | 模块: {issue['module']}")
                    print(f"     消息: {issue['message'][:100]}...")

        # 模块统计
        modules = report['modules']
        if modules.get('top_modules'):
            print("\n" + "-" * 40)
            print("📦 模块调用统计 (Top 5)")
            print("-" * 40)
            for module, count in list(modules['top_modules'].items())[:5]:
                print(f"  {module}: {count:,} 次")

        print("\n" + "=" * 80)
        print("✅ 分析完成")
        print("=" * 80 + "\n")


def main():
    if len(sys.argv) < 2:
        print("用法: python log_analyzer.py <日志文件路径> [--json]")
        sys.exit(1)

    log_file = sys.argv[1]
    output_json = '--json' in sys.argv

    analyzer = LogAnalyzer(log_file)
    report = analyzer.analyze()

    if output_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    else:
        analyzer.print_report(report)


if __name__ == '__main__':
    main()
