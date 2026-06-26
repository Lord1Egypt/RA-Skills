"""测试：APP手机号登录注册工时评估"""
import sys
sys.path.insert(0, "C:/Users/Administrator/AppData/Roaming/LobsterAI/SKILLs/work-estimation/scripts")
from generate_estimation import generate_estimation_excel

modules = [
    {
        "name": "用户系统",
        "desc": "APP手机号登录注册模块",
        "items": [
            {
                "name": "登录注册界面",
                "desc": "手机号输入、验证码发送、倒计时、协议勾选",
                "analysis": 0.5,
                "design": 1.0,
                "frontend": 2.0,
                "backend": 1.5,
                "algorithm": 0,
                "test": 0.5,
                "complexity": "低",
                "risk": "低",
                "parallel": True,
                "prerequisite": "",
                "coordination": "需与短信服务商协调"
            },
            {
                "name": "验证码服务",
                "desc": "短信验证码生成、发送、校验（60秒有效期）",
                "analysis": 0.5,
                "design": 0.5,
                "frontend": 0,
                "backend": 2.0,
                "algorithm": 0,
                "test": 0.5,
                "complexity": "中",
                "risk": "低",
                "parallel": True,
                "prerequisite": "",
                "coordination": "需与短信服务商协调接口"
            },
            {
                "name": "用户信息存储",
                "desc": "用户表设计、注册流程、登录Token生成",
                "analysis": 0.5,
                "design": 1.0,
                "frontend": 0,
                "backend": 2.5,
                "algorithm": 0,
                "test": 0.5,
                "complexity": "中",
                "risk": "低",
                "parallel": False,
                "prerequisite": "验证码服务完成后",
                "coordination": ""
            },
            {
                "name": "第三方登录（可选）",
                "desc": "微信/Apple登录集成",
                "analysis": 0.5,
                "design": 0.5,
                "frontend": 1.5,
                "backend": 1.5,
                "algorithm": 0,
                "test": 0.5,
                "complexity": "高",
                "risk": "中",
                "parallel": True,
                "prerequisite": "",
                "coordination": "需微信/Apple开发者账号"
            }
        ]
    }
]

output = generate_estimation_excel("APP手机号登录注册", modules)
print(f"已生成: {output}")
