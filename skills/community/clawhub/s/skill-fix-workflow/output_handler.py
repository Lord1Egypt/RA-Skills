# -*- coding: utf-8 -*-
"""
输出处理器 - V3.0

处理四种输出方式：屏幕 / 文件 / API / 网页
"""

import os
import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger("OpenClaw.OutputHandler")


class OutputHandler:
    """输出处理器"""
    
    OUTPUT_TYPES = ["screen", "file", "api", "web"]
    
    def __init__(self, output_type: str = "screen", output_path: str = None,
                 api_url: str = None):
        self.output_type = output_type
        self.output_path = output_path
        self.api_url = api_url
    
    def output(self, data: Any) -> Dict[str, Any]:
        """
        执行输出
        
        Args:
            data: 要输出的数据
            
        Returns:
            输出结果
        """
        if self.output_type == "screen":
            return self._output_screen(data)
        elif self.output_type == "file":
            return self._output_file(data)
        elif self.output_type == "api":
            return self._output_api(data)
        elif self.output_type == "web":
            return self._output_web(data)
        else:
            return self._output_screen(data)
    
    def _output_screen(self, data: Any) -> Dict[str, Any]:
        """输出到屏幕"""
        logger.info("[输出] 屏幕输出")
        
        if isinstance(data, (dict, list)):
            output_text = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            output_text = str(data)
        
        print("\n" + "="*60)
        print(output_text)
        print("="*60 + "\n")
        
        return {"status": "success", "type": "screen", "data": output_text}
    
    def _output_file(self, data: Any) -> Dict[str, Any]:
        """输出到文件"""
        if not self.output_path:
            self.output_path = f"./output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        logger.info(f"[输出] 文件输出：{self.output_path}")
        
        # 确保目录存在
        output_dir = os.path.dirname(self.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 根据扩展名选择格式
        if self.output_path.endswith(".json"):
            content = json.dumps(data, ensure_ascii=False, indent=2)
        elif self.output_path.endswith(".csv"):
            content = self._to_csv(data)
        else:
            content = str(data)
        
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return {"status": "success", "type": "file", "path": self.output_path}
    
    def _output_api(self, data: Any) -> Dict[str, Any]:
        """输出到 API"""
        if not self.api_url:
            return {"status": "error", "message": "API URL 未配置"}
        
        logger.info(f"[输出] API 输出：{self.api_url}")
        
        # TODO: 实际实现 API POST
        # import requests
        # response = requests.post(self.api_url, json=data)
        
        return {
            "status": "simulated",
            "type": "api",
            "url": self.api_url,
            "message": "API 输出（模拟）"
        }
    
    def _output_web(self, data: Any) -> Dict[str, Any]:
        """输出到网页"""
        logger.info("[输出] 网页发布")
        
        # TODO: 实际实现网页发布
        # 可以生成 HTML 文件或发布到 Web 平台
        
        html_path = f"./output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html_content = self._to_html(data)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return {
            "status": "success",
            "type": "web",
            "path": html_path,
            "message": f"已生成 HTML: {html_path}"
        }
    
    def _to_csv(self, data: Any) -> str:
        """转换为 CSV 格式"""
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                headers = list(data[0].keys())
                lines = [",".join(headers)]
                for row in data:
                    lines.append(",".join(str(row.get(h, "")) for h in headers))
                return "\n".join(lines)
        return str(data)
    
    def _to_html(self, data: Any) -> str:
        """转换为 HTML 格式"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OpenClaw 输出 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        pre {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>OpenClaw 固化程序输出</h1>
    <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <pre>{json.dumps(data, ensure_ascii=False, indent=2)}</pre>
</body>
</html>"""
        return html


def create_output_handler(output_type: str = "screen", 
                          output_path: str = None,
                          api_url: str = None) -> OutputHandler:
    """便捷函数：创建输出处理器"""
    return OutputHandler(output_type, output_path, api_url)


def get_output_function_code(output_type: str, output_path: str = None, 
                              api_url: str = None) -> str:
    """
    生成输出函数代码（用于拼接）
    
    Returns:
        Python 代码字符串
    """
    if output_type == "file" and output_path:
        return f'output_file(result, path="{output_path}")'
    elif output_type == "api" and api_url:
        return f'output_api(result, url="{api_url}")'
    elif output_type == "web":
        return 'output_web(result)'
    else:
        return 'output_screen(result)'


# 测试
if __name__ == "__main__":
    test_data = {"status": "success", "count": 10, "items": ["item1", "item2"]}
    
    # 测试屏幕输出
    handler = OutputHandler("screen")
    result = handler.output(test_data)
    print(f"屏幕输出：{result}")
    
    # 测试文件输出
    handler = OutputHandler("file", "./test_output.json")
    result = handler.output(test_data)
    print(f"文件输出：{result}")
