"""SCL代码生成器：根据工艺描述和模板生成SCL代码"""

import os
import re
from jinja2 import Environment, FileSystemLoader, Template
from typing import Dict, Any, List

class SCLGenerator:
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate(self, block_type: str, name: str, description: str,
                 parameters: Dict[str, Any] = None) -> str:
        """
        生成SCL代码
        :param block_type: "OB", "FC", "FB", "DB"
        :param name: 块名称
        :param description: 工艺描述
        :param parameters: 用户提供的额外参数（如变量列表）
        """
        # 解析描述，提取变量和控制逻辑
        analysis = self._analyze_description(description)
        # 加载模板
        template = self.env.get_template(f"{block_type.lower()}_template.txt")
        # 渲染
        code = template.render(
            block_name=name,
            description=description,
            variables=analysis.get("variables", []),
            logic=analysis.get("logic", ""),
            parameters=parameters or {}
        )
        return code

    def _analyze_description(self, desc: str) -> dict:
        """
        简单关键词分析，提取变量和逻辑框架
        """
        result = {"variables": [], "logic": ""}

        # 提取输入/输出变量（简单模式）
        input_pattern = r"输入[：:]\s*(\w+)"
        output_pattern = r"输出[：:]\s*(\w+)"
        motor_pattern = r"电机\s*(\w+)"
        pump_pattern = r"泵\s*(\w+)"
        valve_pattern = r"阀\s*(\w+)"

        inputs = re.findall(input_pattern, desc)
        outputs = re.findall(output_pattern, desc)
        motors = re.findall(motor_pattern, desc)
        pumps = re.findall(pump_pattern, desc)
        valves = re.findall(valve_pattern, desc)

        for inp in inputs:
            result["variables"].append({"name": inp, "type": "Bool", "direction": "input"})
        for out in outputs:
            result["variables"].append({"name": out, "type": "Bool", "direction": "output"})
        for motor in motors:
            result["variables"].append({"name": f"Motor_{motor}_Run", "type": "Bool", "direction": "output"})
        for pump in pumps:
            result["variables"].append({"name": f"Pump_{pump}_Run", "type": "Bool", "direction": "output"})
        for valve in valves:
            result["variables"].append({"name": f"Valve_{valve}_Open", "type": "Bool", "direction": "output"})

        # 简单逻辑生成
        if "启动" in desc or "start" in desc.lower():
            result["logic"] = "IF #Start THEN #Run := TRUE; END_IF;"
        elif "停止" in desc or "stop" in desc.lower():
            result["logic"] = "IF #Stop THEN #Run := FALSE; END_IF;"
        elif "控制" in desc or "control" in desc.lower():
            result["logic"] = "IF #Auto THEN #Output := #Input; ELSE #Output := FALSE; END_IF;"
        else:
            result["logic"] = "// 用户逻辑占位符"
        return result