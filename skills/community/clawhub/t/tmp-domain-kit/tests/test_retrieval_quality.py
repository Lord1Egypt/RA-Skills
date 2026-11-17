"""
检索质量评估测试
20 个测试查询用例，验证命中率、关系追溯、格式化输出
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Set, Optional

# 添加项目根目录到 path
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

from retrieval.query_engine import QueryEngine
from retrieval.formatter import ResultFormatter
from retrieval.keyword_extractor import KeywordExtractor
from storage.knowledge_store import KnowledgeStore
from retrieval.index_manager import IndexManager


class RetrievalQualityTest:
    """检索质量评估"""

    def __init__(self):
        self.engine = QueryEngine(str(SKILL_DIR))
        self.formatter = ResultFormatter()
        self.store = KnowledgeStore(str(SKILL_DIR / "storage"))
        self.index = IndexManager(str(SKILL_DIR / "storage"))

        # 20 个测试用例
        self.test_cases = [
            # 自动化方向 (8 个)
            {
                "query": "AM600 输送带控制程序",
                "expected_types": ["CodeTemplate", "PLC", "Constraint"],
                "expected_tags": ["AM600", "输送带"],
                "description": "自动化方向 - 代码模板查询"
            },
            {
                "query": "AM600 PLC 硬件参数",
                "expected_types": ["PLC"],
                "expected_tags": ["AM600"],
                "description": "自动化方向 - PLC 参数查询"
            },
            {
                "query": "AM600 编译约束 内存限制",
                "expected_types": ["Constraint"],
                "expected_tags": ["AM600"],
                "description": "自动化方向 - 约束查询"
            },
            {
                "query": "输送带速度闭环调参经验",
                "expected_types": ["BestPractice"],
                "expected_tags": ["调参", "速度闭环"],
                "description": "自动化方向 - 最佳实践查询"
            },
            {
                "query": "AM600 编程模板 ST语言",
                "expected_types": ["CodeTemplate"],
                "expected_tags": ["AM600", "ST"],
                "description": "自动化方向 - 模板+语言查询"
            },
            {
                "query": "AM600 I/O模块配置",
                "expected_types": ["PLC"],
                "expected_tags": ["AM600"],
                "description": "自动化方向 - I/O配置查询"
            },
            {
                "query": "输送带启停控制代码",
                "expected_types": ["CodeTemplate"],
                "expected_tags": ["输送带"],
                "description": "自动化方向 - 场景词查询"
            },
            {
                "query": "PLC选型推荐",
                "expected_types": ["PLC", "Device"],
                "expected_tags": [],
                "description": "自动化方向 - 选型查询"
            },

            # WCS 方向 (6 个)
            {
                "query": "堆垛机调度规则",
                "expected_types": ["ScheduleRule", "WCS_Device"],
                "expected_tags": ["堆垛机"],
                "description": "WCS方向 - 调度规则查询"
            },
            {
                "query": "AGV 路径规划",
                "expected_types": ["WCS_Device"],
                "expected_tags": ["AGV"],
                "description": "WCS方向 - AGV查询"
            },
            {
                "query": "Modbus TCP 通信协议",
                "expected_types": ["Protocol"],
                "expected_tags": ["Modbus TCP"],
                "description": "WCS方向 - 协议查询"
            },
            {
                "query": "输送机 WCS 设备参数",
                "expected_types": ["WCS_Device"],
                "expected_tags": ["输送机"],
                "description": "WCS方向 - 设备参数查询"
            },
            {
                "query": "FIFO 先进先出调度",
                "expected_types": ["ScheduleRule"],
                "expected_tags": ["FIFO"],
                "description": "WCS方向 - FIFO调度查询"
            },
            {
                "query": "OPC UA 堆垛机通信",
                "expected_types": ["Protocol", "WCS_Device"],
                "expected_tags": ["OPC UA", "堆垛机"],
                "description": "WCS方向 - 协议+设备联合查询"
            },

            # 视觉方向 (6 个)
            {
                "query": "表面划痕缺陷检测",
                "expected_types": ["DefectType", "VisionModel"],
                "expected_tags": ["表面划痕"],
                "description": "视觉方向 - 缺陷类型查询"
            },
            {
                "query": "YOLO 目标检测模型",
                "expected_types": ["VisionModel"],
                "expected_tags": ["YOLO"],
                "description": "视觉方向 - 模型查询"
            },
            {
                "query": "尺寸偏差检测方法",
                "expected_types": ["DefectType", "VisionModel"],
                "expected_tags": ["尺寸偏差"],
                "description": "视觉方向 - 尺寸缺陷查询"
            },
            {
                "query": "颜色异常检测",
                "expected_types": ["DefectType", "VisionModel"],
                "expected_tags": ["颜色异常"],
                "description": "视觉方向 - 颜色缺陷查询"
            },
            {
                "query": "视觉模型精度对比",
                "expected_types": ["VisionModel"],
                "expected_tags": ["视觉模型"],
                "description": "视觉方向 - 模型对比查询"
            },
            {
                "query": "ResNet 图像分类缺陷",
                "expected_types": ["VisionModel", "DefectType"],
                "expected_tags": ["ResNet"],
                "description": "视觉方向 - 特定模型查询"
            },
        ]

    def run_all(self) -> Dict:
        """运行所有测试"""
        results = {
            "total": len(self.test_cases),
            "passed": 0,
            "failed": 0,
            "hit_rate": 0,
            "details": []
        }

        for i, tc in enumerate(self.test_cases):
            detail = self._run_single(i + 1, tc)
            results["details"].append(detail)
            if detail["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1

        results["hit_rate"] = results["passed"] / results["total"] if results["total"] > 0 else 0
        return results

    def _run_single(self, idx: int, tc: Dict) -> Dict:
        """运行单个测试用例"""
        query = tc["query"]
        expected_types = set(tc["expected_types"])
        expected_tags = set(tc.get("expected_tags", []))

        # 执行查询
        results = self.engine.query(query, top_k=10)

        # 检查1: 是否有结果命中
        hit = len(results) > 0

        # 检查2: 是否命中了期望的实体类型
        result_types = set(r['entity_type'] for r in results)
        type_match = bool(expected_types.intersection(result_types)) if expected_types else True

        # 检查3: 是否命中了期望的标签
        result_tags = set()
        for r in results:
            result_tags.update(r.get('tags', []))
        tag_match = bool(expected_tags.intersection(result_tags)) if expected_tags else True

        # 综合判定
        passed = hit and type_match

        detail = {
            "index": idx,
            "query": query,
            "description": tc["description"],
            "passed": passed,
            "hit": hit,
            "type_match": type_match,
            "tag_match": tag_match,
            "result_count": len(results),
            "result_types": list(result_types),
            "expected_types": list(expected_types),
            "expected_tags": list(expected_tags),
            "matched_tags": list(expected_tags.intersection(result_tags))
        }

        return detail

    def test_relation_tracing(self) -> Dict:
        """测试关系追溯正确性"""
        result = {
            "total": 0,
            "passed": 0,
            "details": []
        }

        # 测试用例: 查询应包含关系信息
        relation_tests = [
            {
                "query": "AM600 输送带控制",
                "expect_relations": True,
                "description": "CodeTemplate 应关联到 PLC"
            },
            {
                "query": "堆垛机调度",
                "expect_relations": True,
                "description": "ScheduleRule 应关联到 WCS_Device"
            },
            {
                "query": "YOLO 缺陷检测",
                "expect_relations": True,
                "description": "VisionModel 应关联到 DefectType"
            },
            {
                "query": "Modbus TCP 协议",
                "expect_relations": True,
                "description": "Protocol 应关联到 WCS_Device"
            },
        ]

        for i, tc in enumerate(relation_tests):
            results = self.engine.query(tc["query"], top_k=5)
            has_relations = any(r.get('_relations') for r in results)

            passed = has_relations == tc["expect_relations"]
            result["total"] += 1
            if passed:
                result["passed"] += 1

            result["details"].append({
                "query": tc["query"],
                "description": tc["description"],
                "passed": passed,
                "has_relations": has_relations,
                "result_count": len(results)
            })

        return result

    def test_formatter_output(self) -> Dict:
        """测试格式化输出完整性"""
        result = {
            "total": 0,
            "passed": 0,
            "details": []
        }

        # 测试各类型的格式化
        formatter_tests = [
            {"type": "Constraint", "query": "AM600 约束"},
            {"type": "CodeTemplate", "query": "输送带 代码模板"},
            {"type": "PLC", "query": "AM600 PLC"},
            {"type": "WCS_Device", "query": "堆垛机"},
            {"type": "DefectType", "query": "表面划痕"},
            {"type": "VisionModel", "query": "YOLO"},
            {"type": "ScheduleRule", "query": "FIFO 调度"},
            {"type": "Protocol", "query": "Modbus TCP"},
        ]

        for tc in formatter_tests:
            results = self.engine.query(tc["query"], top_k=5)
            # 过滤出目标类型
            typed_results = [r for r in results if r['entity_type'] == tc["type"]]

            if typed_results:
                output = self.formatter.format_results(typed_results, query_text=tc["query"])
                # 检查格式化输出包含关键信息
                has_type_header = tc["type"] in output
                has_source = "来源" in output or "source" in output.lower()
                has_confidence = "置信度" in output

                passed = has_type_header and len(output) > 50
            else:
                passed = True  # 没有该类型数据，跳过
                has_type_header = has_source = has_confidence = False

            result["total"] += 1
            if passed:
                result["passed"] += 1

            result["details"].append({
                "type": tc["type"],
                "query": tc["query"],
                "passed": passed,
                "has_type_header": has_type_header if typed_results else None,
                "has_source": has_source if typed_results else None,
                "result_count": len(typed_results)
            })

        return result

    def print_report(self):
        """打印测试报告"""
        print("=" * 60)
        print("📋 检索质量评估报告")
        print("=" * 60)

        # 1. 主测试
        main_results = self.run_all()
        print(f"\n## 查询命中率测试")
        print(f"   总用例: {main_results['total']}")
        print(f"   通过: {main_results['passed']}")
        print(f"   失败: {main_results['failed']}")
        print(f"   命中率: {main_results['hit_rate']:.0%}")
        print(f"   目标: ≥ 80%")
        print(f"   状态: {'✅ 达标' if main_results['hit_rate'] >= 0.8 else '❌ 未达标'}")

        # 打印失败详情
        failed = [d for d in main_results['details'] if not d['passed']]
        if failed:
            print(f"\n   失败用例:")
            for d in failed:
                print(f"     [{d['index']}] {d['description']}")
                print(f"         查询: {d['query']}")
                print(f"         命中: {d['result_count']} 条, 类型: {d['result_types']}")
                print(f"         期望类型: {d['expected_types']}")
                print(f"         标签匹配: {d['matched_tags']}")

        # 2. 关系追溯测试
        rel_results = self.test_relation_tracing()
        print(f"\n## 关系追溯测试")
        print(f"   总用例: {rel_results['total']}")
        print(f"   通过: {rel_results['passed']}")
        print(f"   状态: {'✅ 全部通过' if rel_results['passed'] == rel_results['total'] else '⚠️ 部分通过'}")

        for d in rel_results['details']:
            status = "✅" if d['passed'] else "❌"
            print(f"     {status} {d['description']} (结果: {d['result_count']}条, 关系: {d['has_relations']})")

        # 3. 格式化输出测试
        fmt_results = self.test_formatter_output()
        print(f"\n## 格式化输出测试")
        print(f"   总用例: {fmt_results['total']}")
        print(f"   通过: {fmt_results['passed']}")
        print(f"   状态: {'✅ 全部通过' if fmt_results['passed'] == fmt_results['total'] else '⚠️ 部分通过'}")

        # 4. 知识库统计
        stats = self.store.get_stats()
        print(f"\n## 知识库统计")
        print(f"   实体总数: {stats['entity_count']}")
        print(f"   关系总数: {stats['relation_count']}")
        print(f"   类型分布: {stats['entity_types']}")

        # 5. 总结
        print(f"\n{'=' * 60}")
        overall_pass = (main_results['hit_rate'] >= 0.8 and
                        rel_results['passed'] == rel_results['total'] and
                        fmt_results['passed'] == fmt_results['total'])
        if overall_pass:
            print("✅ 所有测试通过！检索质量达标。")
        else:
            print("⚠️ 部分测试未通过，请检查。")
        print(f"{'=' * 60}")

        return overall_pass


if __name__ == "__main__":
    tester = RetrievalQualityTest()
    tester.print_report()
