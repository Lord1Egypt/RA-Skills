"""
代码提取器 - 从 .st (Structured Text) 代码文件提取知识实体
解析 PROGRAM / FUNCTION / FUNCTION_BLOCK 结构，提取变量声明和参数列表
"""

import re
from typing import Dict, Any, List
from extractors.base import BaseExtractor


class CodeExtractor(BaseExtractor):
    """从 ST 代码文件提取知识"""

    # ST 代码结构正则
    PROGRAM_PATTERN = re.compile(
        r'PROGRAM\s+(\w+)(.*?)END_PROGRAM',
        re.DOTALL | re.IGNORECASE
    )
    FUNCTION_PATTERN = re.compile(
        r'FUNCTION\s+(\w+)(.*?)END_FUNCTION',
        re.DOTALL | re.IGNORECASE
    )
    FB_PATTERN = re.compile(
        r'FUNCTION_BLOCK\s+(\w+)(.*?)END_FUNCTION_BLOCK',
        re.DOTALL | re.IGNORECASE
    )

    # 变量声明正则
    VAR_PATTERN = re.compile(
        r'VAR\s*(.*?)END_VAR',
        re.DOTALL | re.IGNORECASE
    )
    VAR_INPUT_PATTERN = re.compile(
        r'VAR_INPUT\s*(.*?)END_VAR',
        re.DOTALL | re.IGNORECASE
    )
    VAR_OUTPUT_PATTERN = re.compile(
        r'VAR_OUTPUT\s*(.*?)END_VAR',
        re.DOTALL | re.IGNORECASE
    )

    # 单个变量声明
    VAR_DECL = re.compile(
        r'(\w+)\s*:\s*(\w+(?:\s*\[.*?\])?)\s*(?::=\s*(.+?))?\s*;',
        re.IGNORECASE
    )

    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        """从 ST 代码文件提取实体"""
        if not self._file_exists(file_path):
            return []

        text = self._read_text(file_path)
        results = []
        provenance = self._make_provenance(file_path, confidence=1.0, source_type="code")

        # 提取 PROGRAM 块
        for match in self.PROGRAM_PATTERN.finditer(text):
            name = match.group(1)
            body = match.group(2)
            entity = self._build_code_template(name, "ST", body, file_path)
            tags = self._extract_tags(name, body)
            results.append({
                "entity_type": "CodeTemplate",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })

        # 提取 FUNCTION 块
        for match in self.FUNCTION_PATTERN.finditer(text):
            name = match.group(1)
            body = match.group(2)
            entity = self._build_code_template(name, "ST", body, file_path)
            tags = self._extract_tags(name, body)
            results.append({
                "entity_type": "CodeTemplate",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })

        # 提取 FUNCTION_BLOCK 块
        for match in self.FB_PATTERN.finditer(text):
            name = match.group(1)
            body = match.group(2)
            entity = self._build_code_template(name, "ST", body, file_path)
            tags = self._extract_tags(name, body)
            results.append({
                "entity_type": "CodeTemplate",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })

        # 如果没有匹配到结构块，把整个文件当作一个模板
        if not results and text.strip():
            name = file_path.rsplit('/', 1)[-1].rsplit('\\', 1)[-1].replace('.st', '')
            entity = self._build_code_template(name, "ST", text, file_path)
            tags = self._extract_tags(name, text)
            results.append({
                "entity_type": "CodeTemplate",
                "entity": entity,
                "provenance": dict(provenance),
                "tags": tags
            })

        return results

    def _build_code_template(self, name: str, language: str, body: str,
                              file_path: str) -> Dict[str, Any]:
        """构建 CodeTemplate 实体"""
        # 提取变量
        parameters = []
        for var_section in self.VAR_INPUT_PATTERN.finditer(body):
            for var_match in self.VAR_DECL.finditer(var_section.group(1)):
                var_name = var_match.group(1)
                var_type = var_match.group(2).strip()
                parameters.append(f"{var_name} ({var_type}) [INPUT]")

        for var_section in self.VAR_OUTPUT_PATTERN.finditer(body):
            for var_match in self.VAR_DECL.finditer(var_section.group(1)):
                var_name = var_match.group(1)
                var_type = var_match.group(2).strip()
                parameters.append(f"{var_name} ({var_type}) [OUTPUT]")

        # 内部变量
        for var_section in self.VAR_PATTERN.finditer(body):
            # 排除 VAR_INPUT / VAR_OUTPUT（已被上面处理）
            section_text = var_section.group(0)
            if section_text.upper().startswith('VAR_INPUT') or \
               section_text.upper().startswith('VAR_OUTPUT'):
                continue
            for var_match in self.VAR_DECL.finditer(var_section.group(1)):
                var_name = var_match.group(1)
                var_type = var_match.group(2).strip()
                parameters.append(f"{var_name} ({var_type})")

        return {
            "name": name,
            "language": language,
            "content": body.strip()[:2000],  # 限制长度
            "parameters": parameters,
            "description": f"从 {file_path} 提取的 {name}"
        }

    def _extract_tags(self, name: str, body: str) -> List[str]:
        """从代码提取标签"""
        tags = ["ST"]
        # 从名称提取场景关键词
        scenario_keywords = [
            'conveyor', 'stacker', 'sort', 'agv', 'vision', 'weld',
            'pack', 'palletiz', 'inject', 'stamp', 'control',
            '输送带', '堆垛', '分拣', '焊接', '包装', '控制'
        ]
        name_lower = name.lower()
        body_lower = body.lower()
        for kw in scenario_keywords:
            if kw in name_lower or kw in body_lower:
                # 映射为中文标签
                tag_map = {
                    'conveyor': '输送带', 'stacker': '堆垛机', 'sort': '分拣',
                    'agv': 'AGV', 'vision': '视觉', 'weld': '焊接',
                    'pack': '包装', 'control': '控制'
                }
                tags.append(tag_map.get(kw, kw))

        # 提取型号
        model_pattern = re.compile(r'\b([A-Z]{1,4}\d{2,4}[A-Z]?)\b')
        tags.extend(model_pattern.findall(body))

        return list(set(tags))


if __name__ == "__main__":
    import tempfile
    import os

    test_st = """PROGRAM ConveyorControl
VAR_INPUT
  StartBtn : BOOL;
  StopBtn : BOOL;
  SpeedRef : REAL;
END_VAR
VAR_OUTPUT
  MotorRun : BOOL;
  ActualSpeed : REAL;
END_VAR
VAR
  Timer : INT;
  Status : STRING;
END_VAR

IF StartBtn AND NOT StopBtn THEN
  MotorRun := TRUE;
  ActualSpeed := SpeedRef;
ELSIF StopBtn THEN
  MotorRun := FALSE;
  ActualSpeed := 0.0;
END_IF
END_PROGRAM

FUNCTION_BLOCK PID_Controller
VAR_INPUT
  Setpoint : REAL;
  Feedback : REAL;
  Kp : REAL := 1.0;
  Ki : REAL := 0.5;
END_VAR
VAR_OUTPUT
  Output : REAL;
END_VAR
VAR
  Error : REAL;
  Integral : REAL;
END_VAR

Error := Setpoint - Feedback;
Integral := Integral + Error;
Output := Kp * Error + Ki * Integral;
END_FUNCTION_BLOCK
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.st', delete=False, encoding='utf-8') as f:
        f.write(test_st)
        tmpfile = f.name

    try:
        extractor = CodeExtractor()
        results = extractor.extract(tmpfile)
        print(f"提取到 {len(results)} 个代码模板:")
        for r in results:
            e = r['entity']
            print(f"  [{r['entity_type']}] {e['name']}")
            print(f"    参数: {e['parameters']}")
            print(f"    标签: {r['tags']}")
    finally:
        os.unlink(tmpfile)
