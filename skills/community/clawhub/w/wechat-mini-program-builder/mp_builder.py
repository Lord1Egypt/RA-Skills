#!/usr/bin/env python3
"""
微信小程序快速搭建工具
用途：AI 辅助生成小程序代码
"""

import os
import json
import argparse
from pathlib import Path
from openclaw import OpenClaw

class MiniProgramBuilder:
    """小程序构建器"""
    
    TEMPLATES = {
        "shop": {
            "pages": ["index", "category", "product", "cart", "profile"],
            "features": ["商品展示", "购物车", "订单管理", "用户中心"]
        },
        "restaurant": {
            "pages": ["index", "menu", "order", "profile"],
            "features": ["菜单展示", "在线点餐", "订单跟踪", "会员积分"]
        },
        "booking": {
            "pages": ["index", "service", "booking", "profile"],
            "features": ["服务列表", "在线预约", "订单管理", "提醒通知"]
        },
        "showcase": {
            "pages": ["index", "about", "products", "contact"],
            "features": ["企业介绍", "产品展示", "联系方式", "地图导航"]
        }
    }
    
    def __init__(self):
        self.api_key = os.getenv("OPENCLAW_API_KEY")
        if not self.api_key:
            raise ValueError("请设置环境变量 OPENCLAW_API_KEY")
    
    def create_project(self, template, project_name):
        """创建项目"""
        if template not in self.TEMPLATES:
            print(f"❌ 模板不存在: {template}")
            print(f"可用模板: {', '.join(self.TEMPLATES.keys())}")
            return
        
        # 创建目录结构
        project_dir = Path(project_name)
        project_dir.mkdir(exist_ok=True)
        
        (project_dir / "pages").mkdir(exist_ok=True)
        (project_dir / "utils").mkdir(exist_ok=True)
        (project_dir / "components").mkdir(exist_ok=True)
        (project_dir / "cloudfunctions").mkdir(exist_ok=True)
        
        # 创建 app.json
        template_data = self.TEMPLATES[template]
        app_json = {
            "pages": [f"pages/{p}/main" for p in template_data["pages"]],
            "window": {
                "navigationBarTitleText": project_name,
                "navigationBarBackgroundColor": "#ffffff"
            }
        }
        
        with open(project_dir / "app.json", "w") as f:
            json.dump(app_json, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 项目创建成功: {project_dir}")
        print(f"📦 模板: {template}")
        print(f"📄 页面: {', '.join(template_data['pages'])}")
        print(f"🎯 功能: {', '.join(template_data['features'])}")
    
    def generate_page(self, page_name, prompt):
        """AI 生成页面代码"""
        full_prompt = f"""根据以下需求，生成微信小程序页面代码（WXML + WXSS + JS）：

页面名称：{page_name}
需求：{prompt}

请输出完整的代码，包括：
1. WXML（页面结构）
2. WXSS（样式）
3. JS（逻辑）

使用 Markdown 代码块格式输出。"""

        client = OpenClaw(api_key=self.api_key)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        code = response.choices[0].message.content
        
        # 保存到文件
        page_dir = Path("pages") / page_name
        page_dir.mkdir(exist_ok=True)
        
        with open(page_dir / "generated.md", "w") as f:
            f.write(code)
        
        print(f"✅ 页面代码生成成功: {page_dir / 'generated.md'}")
        print(f"\n{code}")
    
    def generate_cloud_function(self, func_name):
        """生成云函数模板"""
        templates = {
            "login": """// 用户登录
const cloud = require('wx-server-sdk')
cloud.init()

exports.main = async (event) => {
  const { userInfo } = await cloud.getOpenData({ list: [event.openid] })
  return { openid: event.openid, userInfo }
}""",
            "order": """// 创建订单
const cloud = require('wx-server-sdk')
cloud.init()
const db = cloud.database()

exports.main = async (event) => {
  const { productId, quantity } = event
  const order = {
    productId,
    quantity,
    status: 'pending',
    createdAt: new Date()
  }
  const result = await db.collection('orders').add({ data: order })
  return { orderId: result._id }
}""",
            "payment": """// 支付
const cloud = require('wx-server-sdk')
cloud.init()

exports.main = async (event) => {
  const { orderId, amount } = event
  // 调用微信支付 API
  // 返回支付参数
  return { paymentParams: {} }
}"""
        }
        
        if func_name not in templates:
            print(f"❌ 云函数模板不存在: {func_name}")
            print(f"可用模板: {', '.join(templates.keys())}")
            return
        
        func_dir = Path("cloudfunctions") / func_name
        func_dir.mkdir(exist_ok=True)
        
        with open(func_dir / "index.js", "w") as f:
            f.write(templates[func_name])
        
        with open(func_dir / "package.json", "w") as f:
            json.dump({"name": func_name, "version": "1.0.0", "dependencies": {"wx-server-sdk": "latest"}}, f, indent=2)
        
        print(f"✅ 云函数创建成功: {func_dir}")

def main():
    parser = argparse.ArgumentParser(description="微信小程序快速搭建")
    parser.add_argument("command", choices=["create", "generate-page", "generate-func"])
    parser.add_argument("--template", help="模板名称")
    parser.add_argument("--name", help="项目/页面/函数名称")
    parser.add_argument("--prompt", help="页面需求描述")
    args = parser.parse_args()
    
    builder = MiniProgramBuilder()
    
    if args.command == "create":
        if not args.template or not args.name:
            print("❌ 请提供 --template 和 --name")
            return
        builder.create_project(args.template, args.name)
    
    elif args.command == "generate-page":
        if not args.name or not args.prompt:
            print("❌ 请提供 --name 和 --prompt")
            return
        builder.generate_page(args.name, args.prompt)
    
    elif args.command == "generate-func":
        if not args.name:
            print("❌ 请提供 --name")
            return
        builder.generate_cloud_function(args.name)

if __name__ == "__main__":
    main()