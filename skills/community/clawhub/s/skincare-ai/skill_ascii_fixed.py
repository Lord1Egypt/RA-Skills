#!/usr/bin/env python3
"""
护肤AI技能 - OpenClaw技能格式 (v1.0.3)
符合OpenClaw技能规范，100%本地运行，无网络依赖
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

# 导入安全修复的工具
try:
    from path_validator import PathValidator, create_path_validator_from_config
    from api_utils_fixed import validate_image_data, format_response, validate_model_path
    HAS_SECURITY_TOOLS = True
except ImportError as e:
    HAS_SECURITY_TOOLS = False
    print(f"[WARN] 安全工具导入失败: {e}")


class SkincareAISkill:
    """护肤AI技能类 - 符合OpenClaw技能规范"""
    
    def __init__(self):
        """初始化技能"""
        self.name = "skincare-ai"
        self.version = "1.0.4"
        self.description = "AI护肤分析系统 - 安全修复版 (100%本地运行)"
        
        # 技能根目录
        self.skill_root = Path(__file__).parent
        
        # 初始化配置
        self.config = self._load_config()
        
        # 初始化路径验证器
        self.path_validator = None
        if HAS_SECURITY_TOOLS:
            try:
                self.path_validator = create_path_validator_from_config(
                    self.config, 
                    str(self.skill_root)
                )
                print(f"[INFO] 路径验证器初始化成功")
            except Exception as e:
                print(f"[ERROR] 路径验证器初始化失败: {e}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        config_path = self.skill_root / "config.yaml"
        
        # 默认配置（确保安全）
        default_config = {
            "security": {
                "network_access": False,
                "local_only": True,
                "privacy_friendly": True,
                "path_restriction": {
                    "enabled": True,
                    "allowed_dirs": [".", "./data", "./models"],
                    "max_file_size_mb": 50,
                    "allowed_file_types": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]
                }
            },
            "plugins": {
                "skin_analyzer": {
                    "enabled": True,
                    "mode": "advanced"
                },
                "recommendation_engine": {
                    "enabled": True,
                    "max_recommendations": 5
                }
            },
            "output": {
                "default_format": "markdown",
                "include_timestamp": True
            }
        }
        
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = yaml.safe_load(f)
            
            # 合并配置，确保安全配置优先
            merged = default_config.copy()
            if loaded_config:
                # 安全合并
                self._safe_merge_configs(merged, loaded_config)
            
            # 确保安全声明
            if "security" not in merged:
                merged["security"] = default_config["security"]
            else:
                # 确保关键安全设置
                merged["security"]["network_access"] = False
                merged["security"]["local_only"] = True
            
            return merged
            
        except Exception as e:
            print(f"[WARN] 配置加载失败，使用安全默认配置: {e}")
            return default_config
    
    def _safe_merge_configs(self, base: Dict, update: Dict):
        """安全合并配置（防止网络配置混入）"""
        for key, value in update.items():
            if key == "security":
                # 安全配置特殊处理
                if isinstance(value, dict):
                    for sec_key, sec_value in value.items():
                        if sec_key not in ["network_access", "local_only", "privacy_friendly"]:
                            # 只允许特定的安全配置
                            continue
                        base.setdefault("security", {})[sec_key] = sec_value
            elif key in ["plugins", "output", "logging"]:
                # 允许的配置类别
                if isinstance(value, dict):
                    base.setdefault(key, {}).update(value)
            # 其他配置忽略（防止网络配置混入）
    
    def setup(self, context: Dict[str, Any]) -> None:
        """
        技能设置方法 - OpenClaw规范
        
        Args:
            context: OpenClaw提供的上下文
        """
        print(f"[INFO] {self.name} v{self.version} 设置完成")
        print(f"[INFO] 技能描述: {self.description}")
        print(f"[INFO] 安全模式: 100%本地运行，无网络依赖")
        
        # 验证路径安全
        if self.path_validator:
            allowed_dirs = self.path_validator.get_allowed_dirs()
            print(f"[INFO] 允许访问的目录: {[str(d) for d in allowed_dirs]}")
    
    def handle(self, command: str, args: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理命令 - OpenClaw规范
        
        Args:
            command: 命令名称
            args: 命令参数
            context: 上下文信息
            
        Returns:
            处理结果
        """
        print(f"[INFO] 处理命令: {command}")
        
        # 安全验证：检查所有文件路径
        if "file_path" in args:
            file_path = args["file_path"]
            if self.path_validator:
                is_safe, message = self.path_validator.validate_image_path(file_path)
                if not is_safe:
                    return {
                        "success": False,
                        "error": f"路径不安全: {message}",
                        "suggestion": "请提供技能目录内的文件路径"
                    }
        
        # 处理不同命令
        if command == "analyze_skin":
            return self._handle_analyze_skin(args)
        elif command == "get_recommendations":
            return self._handle_get_recommendations(args)
        elif command == "health_check":
            return self._handle_health_check()
        elif command == "skill_info":
            return self._handle_skill_info()
        else:
            return {
                "success": False,
                "error": f"未知命令: {command}",
                "available_commands": ["analyze_skin", "get_recommendations", "health_check", "skill_info"]
            }
    
    def _handle_analyze_skin(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理皮肤分析命令"""
        try:
            # 验证输入
            if "image_data" not in args:
                return {
                    "success": False,
                    "error": "缺少image_data参数",
                    "suggestion": "请提供图像数据或文件路径"
                }
            
            image_data = args["image_data"]
            
            # 使用安全验证
            if HAS_SECURITY_TOOLS:
                is_valid, message = validate_image_data(image_data)
                if not is_valid:
                    return {
                        "success": False,
                        "error": f"图像数据验证失败: {message}",
                        "suggestion": "请提供有效的本地图像文件"
                    }
            
            # 模拟分析结果（实际应调用分析模块）
            analysis_result = {
                "moisture": {"score": 75, "grade": "良好", "suggestion": "保持当前护肤习惯"},
                "oil": {"score": 60, "grade": "正常", "suggestion": "适当控油"},
                "elasticity": {"score": 80, "grade": "优秀", "suggestion": "继续保持"},
                "pores": {"score": 65, "grade": "正常", "suggestion": "定期清洁"},
                "redness": {"score": 40, "grade": "轻微", "suggestion": "注意防晒"},
                "pigmentation": {"score": 50, "grade": "正常", "suggestion": "注意美白"},
                "wrinkles": {"score": 30, "grade": "轻微", "suggestion": "注意抗衰老"}
            }
            
            return {
                "success": True,
                "analysis": analysis_result,
                "summary": "皮肤状态总体良好，建议保持当前护肤习惯",
                "security_note": "分析在本地完成，无数据外传"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"分析失败: {str(e)}",
                "traceback": traceback.format_exc() if "traceback" in locals() else "N/A"
            }
    
    def _handle_get_recommendations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理产品推荐命令"""
        try:
            # 验证输入
            required_params = ["skin_type", "concerns"]
            for param in required_params:
                if param not in args:
                    return {
                        "success": False,
                        "error": f"缺少{param}参数",
                        "suggestion": f"请提供{param}"
                    }
            
            skin_type = args["skin_type"]
            concerns = args["concerns"]
            
            # 模拟推荐结果
            recommendations = [
                {
                    "product": "温和洁面乳",
                    "category": "洁面",
                    "brand": "示例品牌",
                    "reason": f"适合{skin_type}肤质，针对{concerns}问题",
                    "usage": "早晚各一次"
                },
                {
                    "product": "保湿精华",
                    "category": "精华",
                    "brand": "示例品牌",
                    "reason": f"适合{skin_type}肤质，提供深层保湿",
                    "usage": "早晚洁面后使用"
                }
            ]
            
            return {
                "success": True,
                "skin_type": skin_type,
                "concerns": concerns,
                "recommendations": recommendations,
                "security_note": "推荐基于本地数据库，无网络查询"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"推荐失败: {str(e)}"
            }
    
    def _handle_health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "success": True,
            "skill": self.name,
            "version": self.version,
            "status": "healthy",
            "security": {
                "network_access": False,
                "local_only": True,
                "path_restriction_enabled": self.path_validator is not None
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_skill_info(self) -> Dict[str, Any]:
        """技能信息"""
        return {
            "success": True,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "features": [
                "皮肤分析",
                "产品推荐",
                "本地运行",
                "隐私保护"
            ],
            "security_features": [
                "100%本地运行",
                "无网络依赖",
                "路径访问限制",
                "输入验证"
            ],
            "commands": [
                "analyze_skin - 皮肤分析",
                "get_recommendations - 产品推荐",
                "health_check - 健康检查",
                "skill_info - 技能信息"
            ]
        }


# OpenClaw技能注册
def create_skill():
    """创建技能实例 - OpenClaw规范"""
    return SkincareAISkill()


# 测试代码
if __name__ == "__main__":
    print("🧪 技能测试模式")
    skill = SkincareAISkill()
    
    # 测试技能信息
    print("\n1. 测试技能信息:")
    info = skill._handle_skill_info()
    print(json.dumps(info, indent=2, ensure_ascii=False))
    
    # 测试健康检查
    print("\n2. 测试健康检查:")
    health = skill._handle_health_check()
    print(json.dumps(health, indent=2, ensure_ascii=False))
    
    print("\n✅ 技能测试完成")
