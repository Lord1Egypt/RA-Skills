"""
格式化输出器 - 将查询结果格式化为 Markdown
按实体类型分组，包含来源标注和置信度
"""

import json
from typing import Dict, Any, List


class ResultFormatter:
    """Markdown 格式化输出"""

    # 实体类型中文名映射
    TYPE_NAMES = {
        "Device": "设备",
        "PLC": "PLC控制器",
        "IO_Module": "I/O模块",
        "CodeTemplate": "代码模板",
        "Constraint": "约束规则",
        "BestPractice": "最佳实践",
        "Protocol": "通信协议",
        "WCS_Device": "WCS设备",
        "ScheduleRule": "调度规则",
        "DefectType": "缺陷类型",
        "VisionModel": "视觉模型"
    }

    def format_results(self, results: List[Dict[str, Any]],
                        query_text: str = "",
                        show_relations: bool = True) -> str:
        """
        格式化查询结果为 Markdown。

        Args:
            results: 查询结果列表
            query_text: 原始查询文本
            show_relations: 是否显示关系追溯

        Returns:
            Markdown 格式字符串
        """
        lines = []
        lines.append("## 📚 领域知识参考\n")

        if query_text:
            lines.append(f"> 查询: {query_text}\n")

        if not results:
            lines.append("未找到匹配的知识条目。\n")
            return '\n'.join(lines)

        # 按类型分组
        by_type = {}
        for r in results:
            etype = r['entity_type']
            if etype not in by_type:
                by_type[etype] = []
            by_type[etype].append(r)

        # 按优先级输出各类型
        type_order = [
            'Constraint', 'CodeTemplate', 'PLC', 'Device',
            'IO_Module', 'WCS_Device', 'ScheduleRule',
            'DefectType', 'VisionModel', 'Protocol', 'BestPractice'
        ]

        for etype in type_order:
            if etype in by_type:
                lines.append(self._format_type_group(etype, by_type[etype]))

        # 其他未列出类型
        for etype, items in by_type.items():
            if etype not in type_order:
                lines.append(self._format_type_group(etype, items))

        # 关系追溯
        if show_relations:
            lines.append(self._format_relations(results))

        lines.append("\n---\n⚠️ 以上知识来自部门知识库，请在回答中标注来源")

        return '\n'.join(lines)

    def _format_type_group(self, entity_type: str, items: List[Dict[str, Any]]) -> str:
        """格式化一组同类型实体"""
        lines = []
        type_name = self.TYPE_NAMES.get(entity_type, entity_type)
        lines.append(f"### {type_name} ({entity_type})\n")

        for item in items:
            entity = item.get('entity', {})
            provenance = item.get('provenance', {})
            confidence = provenance.get('confidence', 0)
            source = provenance.get('source_path', '未知来源')

            conf_bar = self._confidence_bar(confidence)

            if entity_type == 'Constraint':
                rule = entity.get('rule', '')
                severity = entity.get('severity', '')
                scope = entity.get('scope', '')
                lines.append(f"- **{rule}**")
                lines.append(f"  - 严重性: {severity} | 范围: {scope or '通用'}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'CodeTemplate':
                name = entity.get('name', '')
                language = entity.get('language', '')
                content = entity.get('content', '')
                params = entity.get('parameters', [])
                lines.append(f"- **{name}** ({language})")
                if params:
                    lines.append(f"  - 参数: {', '.join(params[:5])}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")
                # 代码块（限制长度）
                code = content[:500]
                if len(content) > 500:
                    code += "\n... (截断)"
                lines.append(f"```{language.lower()}")
                lines.append(code)
                lines.append("```")

            elif entity_type == 'PLC':
                model = entity.get('model', '')
                cpu = entity.get('cpu_type', '')
                mem = entity.get('memory_limit', '')
                io = entity.get('io_capacity', '')
                langs = entity.get('supported_languages', [])
                lines.append(f"- **{model}**")
                lines.append(f"  - CPU: {cpu} | 内存: {mem}MB | I/O: {io}点")
                lines.append(f"  - 编程语言: {', '.join(langs)}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'Device':
                name = entity.get('name', '')
                model = entity.get('model', '')
                mfr = entity.get('manufacturer', '')
                specs = entity.get('specs', {})
                lines.append(f"- **{name}** (型号: {model})")
                if mfr:
                    lines.append(f"  - 厂商: {mfr}")
                if specs:
                    spec_str = ', '.join(f"{k}={v}" for k, v in list(specs.items())[:5])
                    lines.append(f"  - 参数: {spec_str}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'IO_Module':
                model = entity.get('model', '')
                io_type = entity.get('type', '')
                channels = entity.get('channel_count', '')
                signal = entity.get('signal_type', '')
                lines.append(f"- **{model}** ({io_type})")
                lines.append(f"  - 通道数: {channels} | 信号: {signal}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'WCS_Device':
                dtype = entity.get('device_type', '')
                model = entity.get('model', '')
                capacity = entity.get('capacity', '')
                speed = entity.get('speed', '')
                comm = entity.get('communication', [])
                lines.append(f"- **{model}** ({dtype})")
                if capacity:
                    lines.append(f"  - 容量: {capacity}kg | 速度: {speed}m/s")
                if comm:
                    lines.append(f"  - 通信: {', '.join(comm)}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'ScheduleRule':
                name = entity.get('name', '')
                algo = entity.get('algorithm', '')
                priority = entity.get('priority', '')
                constraints = entity.get('constraints', [])
                lines.append(f"- **{name}**")
                lines.append(f"  - 算法: {algo or '未指定'} | 优先级: {priority}")
                if constraints:
                    lines.append(f"  - 约束: {', '.join(constraints[:3])}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'DefectType':
                name = entity.get('name', '')
                category = entity.get('category', '')
                severity = entity.get('severity_level', '')
                chars = entity.get('characteristics', [])
                lines.append(f"- **{name}** ({category})")
                lines.append(f"  - 严重等级: {severity}")
                if chars:
                    lines.append(f"  - 特征: {', '.join(chars[:3])}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'VisionModel':
                name = entity.get('name', '')
                algo = entity.get('algorithm', '')
                defects = entity.get('applicable_defects', [])
                precision = entity.get('precision', '')
                recall = entity.get('recall', '')
                lines.append(f"- **{name}** ({algo})")
                if defects:
                    lines.append(f"  - 适用缺陷: {', '.join(defects[:3])}")
                if precision or recall:
                    lines.append(f"  - 精度: {precision} | 召回率: {recall}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'Protocol':
                name = entity.get('name', '')
                version = entity.get('version', '')
                lines.append(f"- **{name}** (v{version})" if version else f"- **{name}**")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            elif entity_type == 'BestPractice':
                title = entity.get('title', '')
                content = entity.get('content', '')
                examples = entity.get('examples', [])
                lines.append(f"- **{title}**")
                if content:
                    lines.append(f"  - {content[:200]}")
                if examples:
                    lines.append(f"  - 示例: {', '.join(examples[:3])}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            else:
                # 通用格式
                entity_str = json.dumps(entity, ensure_ascii=False)[:200]
                lines.append(f"- {entity_str}")
                lines.append(f"  - 来源: {source} | 置信度: {conf_bar}")

            lines.append("")

        return '\n'.join(lines)

    def _format_relations(self, results: List[Dict[str, Any]]) -> str:
        """格式化关系追溯"""
        lines = ["### 🔗 关联实体\n"]
        has_relations = False

        for r in results[:5]:  # 只对前5个追溯
            relations = r.get('_relations', [])
            if not relations:
                continue

            etype = r['entity_type']
            entity = r.get('entity', {})
            name = entity.get('name', entity.get('model', entity.get('title', '?')))

            for rel_info in relations:
                hop = rel_info.get('hop', 1)
                rel = rel_info.get('relation', {})
                neighbor = rel_info.get('neighbor_entity')

                if not neighbor:
                    continue

                has_relations = True
                direction = "→" if rel.get('direction') == 'forward' else "←"
                rel_type = rel.get('type', '?')
                n_entity = neighbor.get('entity', {})
                n_name = n_entity.get('name', n_entity.get('model', n_entity.get('title', '?')))
                n_type = neighbor.get('entity_type', '?')

                hop_mark = " (2-hop)" if hop == 2 else ""
                lines.append(f"- {name} [{etype}] {direction} {rel_type} {direction} {n_name} [{n_type}]{hop_mark}")

        if not has_relations:
            lines.append("- 无关联实体")

        lines.append("")
        return '\n'.join(lines)

    def _confidence_bar(self, confidence: float) -> str:
        """置信度可视化"""
        if confidence >= 0.95:
            return f"{confidence:.0%} 🟢"
        elif confidence >= 0.8:
            return f"{confidence:.0%} 🟡"
        else:
            return f"{confidence:.0%} 🔴"

    def format_stats(self, store_stats: Dict, index_stats: Dict) -> str:
        """格式化统计信息"""
        lines = [
            "## 📊 知识库统计\n",
            f"- 实体总数: {store_stats.get('entity_count', 0)}",
            f"- 关系总数: {store_stats.get('relation_count', 0)}",
            "",
            "### 实体类型分布\n",
            "| 类型 | 数量 |",
            "|------|------|"
        ]

        for etype, count in sorted(store_stats.get('entity_types', {}).items()):
            type_name = self.TYPE_NAMES.get(etype, etype)
            lines.append(f"| {type_name} ({etype}) | {count} |")

        lines.extend([
            "",
            "### 索引统计\n",
            f"- 唯一标签数: {index_stats.get('unique_tags', 0)}",
            f"- 正向关系数: {index_stats.get('forward_relations', 0)}",
            f"- 反向关系数: {index_stats.get('backward_relations', 0)}"
        ])

        return '\n'.join(lines)


if __name__ == "__main__":
    # 测试格式化
    formatter = ResultFormatter()

    test_results = [
        {
            "entity_type": "Constraint",
            "entity": {"rule": "AM600 程序不得超过500KB", "severity": "critical", "scope": "AM600项目"},
            "provenance": {"source_path": "docs/rules.xlsx", "confidence": 0.9}
        },
        {
            "entity_type": "CodeTemplate",
            "entity": {"name": "ConveyorControl", "language": "ST",
                       "content": "PROGRAM ConveyorControl\nVAR\n  StartBtn: BOOL;\nEND_VAR",
                       "parameters": ["StartBtn (BOOL)"]},
            "provenance": {"source_path": "templates/conveyor.st", "confidence": 1.0},
            "_relations": [
                {
                    "hop": 1,
                    "relation": {"type": "depends_on", "direction": "forward"},
                    "neighbor_entity": {
                        "entity_type": "PLC",
                        "entity": {"model": "AM600"}
                    }
                }
            ]
        }
    ]

    output = formatter.format_results(test_results, query_text="AM600 输送带")
    print(output)
