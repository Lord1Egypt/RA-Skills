#!/usr/bin/env python3
"""
天机·玄机子核心处理脚本（增强版）
集成豆包视觉模型分析功能
"""

import os
import sys
import json
import re
from pathlib import Path

# 尝试导入豆包视觉分析器
try:
    from doubao_vision_integration import DoubaoVisionAnalyzer
    DOUBAO_VISION_AVAILABLE = True
except ImportError:
    DOUBAO_VISION_AVAILABLE = False
    print("⚠️  豆包视觉分析器未找到，将使用传统分析方法")

class TianjiProcessor:
    """天机处理器（增强版）"""
    
    def __init__(self, config_path=None):
        """初始化"""
        # 使用当前文件所在目录的父目录作为workspace
        current_file = Path(__file__).resolve()
        self.workspace_dir = current_file.parent.parent.parent
        self.config = self.load_config(config_path)
        self.persona = self.config.get("persona", {})
        
        # 初始化豆包视觉分析器（如果可用）
        self.doubao_analyzer = None
        if DOUBAO_VISION_AVAILABLE:
            self.doubao_analyzer = DoubaoVisionAnalyzer(config_path)
            
            # 从配置中获取API密钥
            api_key = self.config.get("model_routing", {}).get("image_analysis", {}).get("api_key", "")
            if api_key:
                self.doubao_analyzer.set_api_key(api_key)
        
    def load_config(self, config_path):
        """加载配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "persona": {
                "name": "玄机子",
                "title": "风水大师智慧助手",
                "emoji": "🧭"
            },
            "model_routing": {
                "image_analysis": {
                    "model": "doubao-seed-2-0-pro-260215",
                    "provider": "volcengine",
                    "api_key": "",  # 需要用户配置
                    "base_url": "https://ark.cn-beijing.volces.com/api/v3"
                },
                "default_chat": {"model": "deepseek-chat"}
            }
        }
    
    def detect_request_type(self, user_input, context=None):
        """
        检测请求类型
        返回: request_type, details
        """
        input_text = user_input.lower().strip()
        
        # 图像分析关键词
        image_keywords = [
            '分析.*图片', '分析.*图像', '分析.*照片', '分析.*掌纹',
            '分析.*手相', '分析.*户型', '分析.*风水', '分析.*格局',
            '/tmp/', '.jpg', '.png', '.jpeg', '图片分析', '图像识别',
            '豆包.*分析', '视觉.*分析', '大模型.*分析'
        ]
        
        # 八字分析关键词
        bazi_keywords = [
            '八字', '生辰', '出生', '命理', '排盘', '年柱', '月柱',
            '日柱', '时柱', '大运', '十神', '五行', '命局'
        ]
        
        # 掌纹分析关键词
        palm_keywords = [
            '掌纹', '手相', '生命线', '智慧线', '感情线', '手掌'
        ]
        
        # 风水分析关键词
        fengshui_keywords = [
            '风水', '方位', '格局', '气场', '阴阳', '五行', '八卦',
            '青龙', '白虎', '朱雀', '玄武', '明堂', '靠山'
        ]
        
        # 豆包分析关键词
        doubao_keywords = [
            '豆包', '视觉模型', '大模型分析', 'api分析'
        ]
        
        # 检查是否包含文件路径
        file_path = self.extract_file_path(input_text)
        if file_path:
            # 检查是否明确要求豆包分析
            if any(keyword in input_text for keyword in doubao_keywords):
                return "doubao_analysis", {"file_path": file_path, "analysis_type": "auto"}
            
            # 检查掌纹分析
            for keyword in palm_keywords:
                if keyword in input_text:
                    return "doubao_analysis", {"file_path": file_path, "analysis_type": "palm"}
            
            # 检查风水分析
            for keyword in fengshui_keywords:
                if keyword in input_text:
                    return "doubao_analysis", {"file_path": file_path, "analysis_type": "fengshui"}
            
            # 默认图像分析
            return "image_analysis", {"file_path": file_path}
        
        # 检查图像分析关键词
        for keyword in image_keywords:
            if re.search(keyword, input_text):
                return "image_analysis", {"keyword": keyword}
        
        # 检查八字分析
        for keyword in bazi_keywords:
            if keyword in input_text:
                return "bazi_analysis", {"keyword": keyword}
        
        # 检查掌纹分析
        for keyword in palm_keywords:
            if keyword in input_text:
                return "palm_analysis", {"keyword": keyword}
        
        # 检查风水分析
        for keyword in fengshui_keywords:
            if keyword in input_text:
                return "fengshui_analysis", {"keyword": keyword}
        
        # 默认聊天
        return "chat", {}
    
    def extract_file_path(self, text):
        """从文本中提取文件路径（安全版本）"""
        # 安全路径模式：仅允许明确的、受信任的路径
        patterns = [
            # 模式1: /tmp/目录下的图片文件
            r'(/tmp/[^\s]*\.(?:jpg|png|jpeg|JPG|PNG|JPEG))',
            # 模式2: 当前用户home目录下的图片文件
            r'(/home/[^/\s]+/[^\s]*\.(?:jpg|png|jpeg|JPG|PNG|JPEG))',
            # 模式3: .openclaw目录下的文件
            r'(/home/[^/\s]+/\.openclaw/[^\s]*\.(?:jpg|png|jpeg))',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                file_path = matches[0]
                # 安全验证
                if self.is_safe_file_path(file_path):
                    return file_path
        
        return None
    
    def is_safe_file_path(self, file_path):
        """验证文件路径是否安全"""
        import os
        
        # 拒绝危险路径模式
        dangerous_patterns = [
            r'\.\./',  # 目录遍历
            r'\.\.\\',  # Windows目录遍历
            r'^/etc/',  # 系统配置文件
            r'^/var/',  # 系统目录
            r'^/usr/',  # 系统程序
            r'^/bin/',  # 系统二进制
            r'^/sbin/',  # 系统管理二进制
            r'^/proc/',  # 进程信息
            r'^/sys/',  # 系统信息
            r'^/dev/',  # 设备文件
            r'^/boot/',  # 启动文件
            r'^/lib/',  # 系统库
            r'^/opt/',  # 可选软件
            r'^/srv/',  # 服务数据
            r'^/media/',  # 可移动媒体
            r'^/mnt/',  # 挂载点
            r'^/root/',  # root用户目录
        ]
        
        # 转换为绝对路径并规范化
        abs_path = os.path.abspath(file_path)
        
        # 检查是否在允许的目录下
        allowed_prefixes = [
            '/tmp/',
            f'/home/{os.getenv("USER", "test")}/',
            f'/home/{os.getenv("USER", "test")}/.openclaw/',
        ]
        
        # 验证1: 不在危险目录中
        for pattern in dangerous_patterns:
            if re.search(pattern, abs_path):
                return False
        
        # 验证2: 在允许的目录下
        for prefix in allowed_prefixes:
            if abs_path.startswith(prefix):
                # 验证3: 文件存在且可读
                if os.path.exists(abs_path) and os.access(abs_path, os.R_OK):
                    # 验证4: 是普通文件（不是目录、符号链接等）
                    if os.path.isfile(abs_path):
                        return True
        
        return False
    
    def process_doubao_analysis(self, file_path, analysis_type="auto", user_prompt=None):
        """使用豆包视觉模型进行分析"""
        if not self.doubao_analyzer:
            return {
                "success": False,
                "error": "豆包视觉分析器未初始化",
                "suggestion": "请检查doubao_vision_integration.py是否可用"
            }
        
        # 检查API密钥
        if not self.doubao_analyzer.api_config.get("api_key"):
            return {
                "success": False,
                "error": "未配置豆包API密钥",
                "suggestion": "请在config.json中配置api_key，或使用set_api_key()方法"
            }
        
        print(f"🧭 使用豆包视觉模型分析: {file_path}")
        print(f"📋 分析类型: {analysis_type}")
        
        try:
            if analysis_type == "palm":
                result = self.doubao_analyzer.analyze_palm(file_path, detailed=True)
            elif analysis_type == "fengshui":
                result = self.doubao_analyzer.analyze_fengshui(file_path, "office")
            elif analysis_type == "home":
                result = self.doubao_analyzer.analyze_fengshui(file_path, "home")
            elif user_prompt:
                result = self.doubao_analyzer.analyze_general(file_path, user_prompt)
            else:
                # 自动检测：根据文件特征决定分析类型
                if "palm" in file_path.lower() or "hand" in file_path.lower():
                    result = self.doubao_analyzer.analyze_palm(file_path, detailed=True)
                elif "office" in file_path.lower() or "desk" in file_path.lower():
                    result = self.doubao_analyzer.analyze_fengshui(file_path, "office")
                else:
                    # 默认通用分析
                    result = self.doubao_analyzer.analyze_general(file_path, "请分析这张图片的内容和特征")
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"分析过程中出现错误: {type(e).__name__}: {e}"
            }
    
    def process_request(self, user_input):
        """处理用户请求"""
        request_type, details = self.detect_request_type(user_input)
        
        print(f"🔍 检测到请求类型: {request_type}")
        print(f"📋 详细信息: {details}")
        
        if request_type == "doubao_analysis" and "file_path" in details:
            file_path = details["file_path"]
            analysis_type = details.get("analysis_type", "auto")
            
            result = self.process_doubao_analysis(file_path, analysis_type)
            
            if result["success"]:
                response = f"🧭 玄机子·豆包视觉分析报告\n"
                response += "=" * 50 + "\n\n"
                response += f"✅ 分析成功！\n"
                response += f"⏱️  响应时间: {result.get('response_time', 0):.2f}秒\n\n"
                response += "📋 分析结果:\n"
                response += "-" * 50 + "\n"
                response += result["analysis"]
                response += "\n" + "-" * 50 + "\n"
                
                # 添加使用统计
                usage = result.get("usage", {})
                if usage:
                    response += f"\n📊 Token使用: 输入{usage.get('prompt_tokens')}, 输出{usage.get('completion_tokens')}, 总计{usage.get('total_tokens')}\n"
                
                return response
            else:
                error_msg = f"❌ 豆包视觉分析失败\n"
                error_msg += f"错误: {result.get('error', '未知错误')}\n"
                if "suggestion" in result:
                    error_msg += f"建议: {result['suggestion']}\n"
                
                # 提供传统分析作为备选
                error_msg += "\n💡 备选方案: 您可以描述图片特征，我将使用传统掌相学进行分析。"
                return error_msg
        
        elif request_type == "image_analysis":
            return "📸 检测到图像分析请求。请使用'豆包分析'关键词来调用豆包视觉模型，或描述图片特征进行传统分析。"
        
        elif request_type == "palm_analysis":
            return "🖐️ 检测到掌纹分析请求。请提供掌纹图片路径，或描述掌纹特征进行传统掌相学分析。"
        
        elif request_type == "fengshui_analysis":
            return "🏢 检测到风水分析请求。请提供环境图片路径，或描述环境特征进行传统风水分析。"
        
        elif request_type == "bazi_analysis":
            return "📅 检测到八字分析请求。请提供出生信息（年、月、日、时、性别）。"
        
        else:
            return f"🧭 玄机子为您服务！我是{self.persona.get('name', '玄机子')}，{self.persona.get('title', '风水大师智慧助手')}。\n\n我可以帮助您：\n1. 掌纹分析（使用豆包视觉模型）\n2. 风水分析（办公室、家居环境）\n3. 八字命理分析\n4. 传统掌相学咨询\n\n请告诉我您的需求。"


def main():
    """命令行主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python3 tianji_core_enhanced.py \"用户请求\"")
        print("")
        print("示例:")
        print("  掌纹分析: python3 tianji_core_enhanced.py \"豆包分析掌纹图片 /tmp/palm.jpg\"")
        print("  风水分析: python3 tianji_core_enhanced.py \"分析办公室风水 /tmp/office.jpg\"")
        print("  八字分析: python3 tianji_core_enhanced.py \"八字分析 1990年1月1日 子时 男\"")
        return
    
    user_input = " ".join(sys.argv[1:])
    
    # 初始化处理器
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    processor = TianjiProcessor(config_path)
    
    # 处理请求
    result = processor.process_request(user_input)
    
    print("\n" + "=" * 60)
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    main()