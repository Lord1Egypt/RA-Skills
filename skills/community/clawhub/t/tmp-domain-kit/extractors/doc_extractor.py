"""
文档提取器 - 从 Markdown / 纯文本（PDF fallback）提取知识实体
解析标题层级、关键参数（型号、数值、规格）
"""

import re
import os
from typing import Dict, Any, List
from pathlib import Path

from extractors.base import BaseExtractor


class DocExtractor(BaseExtractor):
    """从 Markdown / 文本文件提取知识"""

    # 常见设备型号正则：大写字母+数字 组合，如 AM600, H5U, AM522
    MODEL_PATTERN = re.compile(r'\b([A-Z]{1,4}\d{2,4}[A-Z]?)\b')

    # 数值+单位 正则
    PARAM_PATTERN = re.compile(
        r'(\d+(?:\.\d+)?)\s*(KB|MB|GB|ms|s|kg|m/s|Hz|V|A|℃|°C|mm|μm|点|通道)',
        re.IGNORECASE
    )

    # Markdown 标题正则
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        """从文档提取实体"""
        if not self._file_exists(file_path):
            return []

        text = self._read_text(file_path)
        results = []
        source_type = "document"
        if file_path.lower().endswith('.pdf'):
            source_type = "document_pdf"
        elif file_path.lower().endswith(('.md', '.markdown')):
            source_type = "document_markdown"

        provenance = self._make_provenance(file_path, confidence=0.85, source_type=source_type)

        # 1. 提取标题 → BestPractice 或 Constraint 候选
        headings = self._extract_headings(text)
        for heading in headings:
            tags = self._extract_tags_from_text(heading['text'])
            # 如果标题包含"约束"/"限制"/"不得" → Constraint
            if any(kw in heading['text'] for kw in ['约束', '限制', '不得', '禁止', '必须', '上限']):
                entity = {
                    "rule": heading['text'],
                    "scope": "",
                    "severity": "warning",
                    "rationale": f"从文档标题提取 (level={heading['level']})"
                }
                results.append({
                    "entity_type": "Constraint",
                    "entity": entity,
                    "provenance": dict(provenance),
                    "tags": tags
                })
            elif len(heading['text']) > 5:
                # 一般标题 → BestPractice 候选
                entity = {
                    "title": heading['text'],
                    "content": "",
                    "tags": tags,
                    "examples": []
                }
                results.append({
                    "entity_type": "BestPractice",
                    "entity": entity,
                    "provenance": dict(provenance),
                    "tags": tags
                })

        # 2. 提取设备型号 → Device 实体
        models_found = set(self.MODEL_PATTERN.findall(text))
        for model in models_found:
            tags = [model]
            # 查找型号周围的上下文
            context = self._find_context(text, model, window=200)
            tags.extend(self._extract_tags_from_text(context))
            entity = {
                "name": model,
                "model": model,
                "manufacturer": "",
                "specs": {},
                "capabilities": []
            }
            results.append({
                "entity_type": "Device",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": list(set(tags))
            })

        # 3. 提取参数 → 附加到 specs
        params = self.PARAM_PATTERN.findall(text)
        if params:
            specs = {}
            for value, unit in params[:10]:  # 限制数量
                key = f"{unit.strip()}"
                specs[key] = float(value)
            if specs and models_found:
                # 把参数关联到第一个型号
                model = list(models_found)[0]
                entity = {
                    "name": f"{model}_参数",
                    "model": model,
                    "manufacturer": "",
                    "specs": specs,
                    "capabilities": []
                }
                results.append({
                    "entity_type": "Device",
                    "entity": entity,
                    "provenance": dict(provenance),
                    "tags": [model, "参数提取"]
                })

        return results

    def _extract_headings(self, text: str) -> List[Dict[str, Any]]:
        """提取 Markdown 标题"""
        headings = []
        for match in self.HEADING_PATTERN.finditer(text):
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append({"level": level, "text": title})
        return headings

    def _extract_tags_from_text(self, text: str) -> List[str]:
        """从文本提取标签关键词"""
        tags = []
        # 设备型号
        tags.extend(self.MODEL_PATTERN.findall(text))
        # 场景关键词
        scenario_keywords = [
            '输送带', '堆垛机', '分拣', 'AGV', '视觉', '检测', '调度',
            '焊接', '包装', '码垛', '注塑', '冲压', 'PLC', 'HMI',
            'Modbus', 'OPC', 'EtherCAT', 'Profinet'
        ]
        for kw in scenario_keywords:
            if kw in text:
                tags.append(kw)
        return list(set(tags))

    def _find_context(self, text: str, keyword: str, window: int = 200) -> str:
        """查找关键词周围的上下文"""
        idx = text.find(keyword)
        if idx == -1:
            return ""
        start = max(0, idx - window // 2)
        end = min(len(text), idx + window // 2)
        return text[start:end]


if __name__ == "__main__":
    import tempfile

    # 创建测试 Markdown 文件
    test_md = """# AM600 PLC 使用指南

## 硬件参数
AM600 配备 ARM Cortex-A9 处理器，程序区限制 500KB。
支持 ST、LD、FBD 编程语言。I/O 容量 256 点。

## 约束规则
AM600 程序编译后大小不得超过 500KB。
禁止在高速计数器中使用浮点运算。

## 输送带控制
输送带速度闭环控制，积分时间建议 0.5s。
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_md)
        tmpfile = f.name

    try:
        extractor = DocExtractor()
        results = extractor.extract(tmpfile)
        print(f"提取到 {len(results)} 个实体:")
        for r in results:
            print(f"  [{r['entity_type']}] {r['entity'].get('model', r['entity'].get('title', r['entity'].get('rule', '?')))}")
            print(f"    tags: {r['tags']}")
    finally:
        os.unlink(tmpfile)
