#!/usr/bin/env python3
"""
OpenClaw与思源笔记集成示例
展示如何在OpenClaw会话中使用思源笔记技能
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note import SiYuanNote

class OpenClawSiYuanIntegration:
    """OpenClaw与思源笔记集成类"""
    
    def __init__(self):
        """初始化"""
        self.siyuan = SiYuanNote()
        self.connected = False
        
    def ensure_connected(self):
        """确保已连接到思源笔记"""
        if not self.connected:
            self.connected = self.siyuan.test_connection()
        return self.connected
    
    def handle_query_request(self, query_type, params=None):
        """处理查询请求"""
        if not self.ensure_connected():
            return "❌ 无法连接到思源笔记，请检查配置"
        
        try:
            if query_type == "notebooks":
                # 查询笔记本
                notebooks = self.siyuan.get_notebooks()
                if not notebooks:
                    return "📚 思源笔记中没有找到笔记本"
                
                response = f"📚 找到 {len(notebooks)} 个笔记本:\n"
                for i, nb in enumerate(notebooks[:5], 1):  # 只显示前5个
                    response += f"{i}. **{nb['name']}** (ID: `{nb['id']}`)\n"
                
                if len(notebooks) > 5:
                    response += f"\n... 还有 {len(notebooks) - 5} 个笔记本"
                
                return response
                
            elif query_type == "documents":
                # 查询文档
                notebook_name = params.get('notebook', '其他')
                notebook_id = self.siyuan.get_notebook_id(notebook_name)
                
                if not notebook_id:
                    return f"❌ 未找到笔记本: {notebook_name}"
                
                documents = self.siyuan.get_documents(notebook_id)
                if not documents:
                    return f"📄 笔记本 '{notebook_name}' 中没有文档"
                
                response = f"📄 笔记本 '{notebook_name}' 中有 {len(documents)} 个文档:\n"
                for i, doc in enumerate(documents[:5], 1):  # 只显示前5个
                    doc_name = doc.get('name', '').replace('.sy', '')
                    response += f"{i}. **{doc_name}** (ID: `{doc.get('id')}`)\n"
                
                if len(documents) > 5:
                    response += f"\n... 还有 {len(documents) - 5} 个文档"
                
                return response
                
            elif query_type == "search":
                # 搜索内容
                query = params.get('query', '')
                if not query:
                    return "❌ 请提供搜索关键词"
                
                notebook_name = params.get('notebook')
                results = self.siyuan.search_content(query, notebook_name)
                
                if not results:
                    return f"🔍 未找到包含 '{query}' 的内容"
                
                response = f"🔍 找到 {len(results)} 个包含 '{query}' 的内容:\n"
                for i, block in enumerate(results[:3], 1):  # 只显示前3个
                    content = block.get('content', '')
                    # 截断长内容
                    if len(content) > 100:
                        content = content[:100] + "..."
                    
                    response += f"\n**结果 {i}:**\n{content}\n"
                
                if len(results) > 3:
                    response += f"\n... 还有 {len(results) - 3} 个结果"
                
                return response
                
            else:
                return f"❌ 未知查询类型: {query_type}"
                
        except Exception as e:
            return f"❌ 查询时出错: {str(e)}"
    
    def handle_sync_request(self, conversation_data=None, summary=None):
        """处理同步请求"""
        if not self.ensure_connected():
            return False, "无法连接到思源笔记"
        
        try:
            # 如果没有提供对话数据，创建示例数据
            if not conversation_data:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conversation_data = {
                    'summary': summary or f'OpenClaw对话 - {current_time}',
                    'messages': [
                        {
                            'role': 'user',
                            'content': f'同步测试，时间: {current_time}'
                        },
                        {
                            'role': 'assistant',
                            'content': f'正在同步到思源笔记...\n\n**同步信息:**\n- 时间: {current_time}\n- 笔记本: {self.siyuan.sync_config.notebook_name}\n- 文档: {self.siyuan.sync_config.document_name}'
                        }
                    ],
                    'conclusion': f'同步完成于 {current_time}'
                }
            
            # 同步对话
            success = self.siyuan.sync_conversation(conversation_data)
            
            if success:
                message = f"✅ 对话已同步到思源笔记\n位置: **{self.siyuan.sync_config.notebook_name}** → **{self.siyuan.sync_config.document_name}**"
                return True, message
            else:
                return False, "❌ 同步失败"
                
        except Exception as e:
            return False, f"❌ 同步时出错: {str(e)}"
    
    def handle_command(self, command, args=None):
        """处理命令"""
        if not args:
            args = {}
        
        command = command.lower()
        
        if command in ["查询思源笔记", "查看思源笔记", "思源笔记查询"]:
            # 默认查询笔记本
            return self.handle_query_request("notebooks")
            
        elif command in ["查询笔记本", "查看笔记本", "笔记本列表"]:
            return self.handle_query_request("notebooks")
            
        elif command in ["查询文档", "查看文档", "文档列表"]:
            notebook = args.get('notebook', '其他')
            return self.handle_query_request("documents", {'notebook': notebook})
            
        elif command in ["搜索思源笔记", "思源笔记搜索", "查找笔记"]:
            query = args.get('query', '')
            if not query:
                return "❌ 请提供搜索关键词，例如: 搜索思源笔记 关键词=OpenChat"
            
            notebook = args.get('notebook')
            params = {'query': query}
            if notebook:
                params['notebook'] = notebook
            
            return self.handle_query_request("search", params)
            
        elif command in ["同步到思源笔记", "写入思源笔记", "保存到思源笔记"]:
            # 尝试从args获取对话数据
            conversation_data = args.get('conversation')
            summary = args.get('summary')
            
            success, message = self.handle_sync_request(conversation_data, summary)
            return message
            
        elif command in ["测试思源笔记", "思源笔记测试"]:
            # 测试连接和基本功能
            if not self.ensure_connected():
                return "❌ 思源笔记连接测试失败"
            
            # 获取笔记本数量
            notebooks = self.siyuan.get_notebooks()
            notebook_count = len(notebooks) if notebooks else 0
            
            # 获取默认笔记本的文档数量
            notebook_id = self.siyuan.get_notebook_id(self.siyuan.sync_config.notebook_name)
            document_count = 0
            if notebook_id:
                documents = self.siyuan.get_documents(notebook_id)
                document_count = len(documents) if documents else 0
            
            return f"""✅ 思源笔记测试通过！

**连接状态:** 正常
**API地址:** {self.siyuan.siyuan_config.api_url}
**笔记本数量:** {notebook_count}
**默认笔记本:** {self.siyuan.sync_config.notebook_name}
**文档数量:** {document_count}
**操作次数:** {self.siyuan.operation_count}
**最后操作:** {self.siyuan.last_operation_time or '无'}
"""
            
        elif command in ["帮助", "help", "使用说明"]:
            return self.get_help_message()
            
        else:
            return f"❌ 未知命令: {command}\n\n{self.get_help_message()}"
    
    def get_help_message(self):
        """获取帮助信息"""
        return """📚 **思源笔记技能使用帮助**

**可用命令:**

1. **查询思源笔记** - 查看所有笔记本
2. **查询文档** - 查看指定笔记本中的文档（可加参数 notebook=名称）
3. **搜索思源笔记** - 搜索内容（需加参数 query=关键词）
4. **同步到思源笔记** - 将当前对话同步到思源笔记
5. **测试思源笔记** - 测试连接和基本功能
6. **帮助** - 显示此帮助信息

**示例:**
- `查询思源笔记`
- `查询文档 notebook=其他`
- `搜索思源笔记 query=OpenChat`
- `同步到思源笔记`

**配置信息:**
- API地址: {api_url}
- 默认笔记本: {notebook}
- 默认文档: {document}
""".format(
    api_url=self.siyuan.siyuan_config.api_url,
    notebook=self.siyuan.sync_config.notebook_name,
    document=self.siyuan.sync_config.document_name
)

def parse_command(input_text):
    """解析命令输入"""
    input_text = input_text.strip()
    
    # 简单解析：命令 [参数=值] ...
    parts = input_text.split()
    if not parts:
        return None, {}
    
    command = parts[0]
    args = {}
    
    # 解析参数
    for part in parts[1:]:
        if '=' in part:
            key, value = part.split('=', 1)
            args[key] = value
        else:
            # 如果没有=，可能是查询关键词
            if '搜索' in command or '查找' in command:
                args['query'] = part
    
    return command, args

def interactive_demo():
    """交互式演示"""
    print("=" * 60)
    print("OpenClaw 思源笔记集成演示")
    print("=" * 60)
    
    integration = OpenClawSiYuanIntegration()
    
    print("\n📚 思源笔记技能已加载")
    print(f"API地址: {integration.siyuan.siyuan_config.api_url}")
    print(f"默认笔记本: {integration.siyuan.sync_config.notebook_name}")
    print(f"默认文档: {integration.siyuan.sync_config.document_name}")
    
    print("\n" + integration.get_help_message())
    
    while True:
        try:
            print("\n" + "-" * 40)
            user_input = input("请输入命令 (输入 '退出' 或 'quit' 结束): ").strip()
            
            if user_input.lower() in ['退出', 'quit', 'exit']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            # 解析命令
            command, args = parse_command(user_input)
            
            if not command:
                print("❌ 无效命令")
                continue
            
            # 执行命令
            result = integration.handle_command(command, args)
            print(f"\n{result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断")
            break
        except Exception as e:
            print(f"\n❌ 出错: {e}")

def quick_test():
    """快速测试"""
    print("🧪 快速测试思源笔记集成...")
    
    integration = OpenClawSiYuanIntegration()
    
    # 测试1: 连接测试
    print("\n1. 测试连接...")
    if integration.ensure_connected():
        print("   ✅ 连接成功")
    else:
        print("   ❌ 连接失败")
        return
    
    # 测试2: 查询笔记本
    print("\n2. 查询笔记本...")
    result = integration.handle_command("查询思源笔记")
    print(f"   结果: {result[:100]}..." if len(result) > 100 else f"   结果: {result}")
    
    # 测试3: 同步测试
    print("\n3. 测试同步...")
    success, message = integration.handle_sync_request()
    print(f"   结果: {message}")
    
    print("\n🎉 快速测试完成！")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            quick_test()
        elif sys.argv[1] == "--demo":
            interactive_demo()
        else:
            # 执行单个命令
            integration = OpenClawSiYuanIntegration()
            command, args = parse_command(" ".join(sys.argv[1:]))
            result = integration.handle_command(command, args)
            print(result)
    else:
        # 默认运行交互式演示
        interactive_demo()

if __name__ == "__main__":
    main()