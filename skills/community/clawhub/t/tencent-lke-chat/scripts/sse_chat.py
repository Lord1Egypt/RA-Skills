#!/usr/bin/env python3
"""
腾讯云智能体 HTTP SSE 对话客户端示例

使用方法:
    python sse_chat.py --app-key YOUR_APP_KEY --content "你好"

完整参数:
    --app-key: 应用 AppKey (必填)
    --content: 消息内容 (必填)
    --session-id: 会话ID (可选,默认自动生成)
    --visitor-id: 访客ID (可选,默认自动生成)
    --model: 模型名称 (可选)
    --system-role: 系统角色指令 (可选)
    --streaming-throttle: 流式回包频率 (可选,默认5)
    --search-network: 联网搜索 enable/disable (可选)
    --stream: 流式传输 enable/disable (可选)
    --workflow-status: 工作流 enable/disable (可选)
    --incremental: 增量输出 (可选,默认True)
    --custom-vars: 自定义变量 JSON (可选)
    --visitor-labels: 访客标签 JSON (可选)
    --file-infos: 文件信息 JSON (可选)
"""

import json
import uuid
import argparse
import requests


def generate_id():
    """生成符合要求的ID (2-64字符，只包含字母数字_- )"""
    return str(uuid.uuid4())


def parse_json_arg(arg_str, arg_name):
    """解析JSON格式的参数"""
    if not arg_str:
        return None
    try:
        return json.loads(arg_str)
    except json.JSONDecodeError as e:
        print(f"❌ 参数 {arg_name} JSON格式错误: {e}")
        return None


def parse_sse_line(line):
    """解析SSE行数据"""
    if line.startswith('data:'):
        try:
            return json.loads(line[5:].strip())
        except json.JSONDecodeError:
            return None
    return None


def chat_with_bot(app_key, content, session_id=None, visitor_id=None, 
                 model=None, system_role=None, streaming_throttle=5,
                 search_network=None, stream=None, workflow_status=None,
                 incremental=True, custom_vars=None, visitor_labels=None,
                 file_infos=None, raw=False):
    """
    与智能体进行对话
    
    Args:
        app_key: 应用AppKey
        content: 消息内容
        session_id: 会话ID
        visitor_id: 访客ID
        model: 模型名称
        system_role: 系统角色指令
        streaming_throttle: 流式回包频率
        search_network: 联网搜索设置
        stream: 流式传输设置
        workflow_status: 工作流设置
        incremental: 是否增量输出
        custom_vars: 自定义变量
        visitor_labels: 访客标签
        file_infos: 文件信息
    """
    url = "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse"
    
    session_id = session_id or generate_id()
    visitor_id = visitor_id or generate_id()
    
    # 构建完整请求体
    payload = {
        "session_id": session_id,
        "bot_app_key": app_key,
        "visitor_biz_id": visitor_id,
        "content": content,
        "request_id": generate_id(),
        "incremental": incremental,
        "streaming_throttle": streaming_throttle
    }
    
    # 可选参数
    if model:
        payload["model_name"] = model
    if system_role:
        payload["system_role"] = system_role
    if search_network:
        payload["search_network"] = search_network
    if stream:
        payload["stream"] = stream
    if workflow_status:
        payload["workflow_status"] = workflow_status
    if custom_vars:
        payload["custom_variables"] = custom_vars
    if visitor_labels:
        payload["visitor_labels"] = visitor_labels
    if file_infos:
        payload["file_infos"] = file_infos
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"📡 发送请求...")
    print(f"   Session ID: {session_id}")
    print(f"   Visitor ID: {visitor_id}")
    
    # 打印参数信息
    if model:
        print(f"   模型: {model}")
    if system_role:
        print(f"   系统角色: {system_role[:50]}..." if len(system_role) > 50 else f"   系统角色: {system_role}")
    if custom_vars:
        print(f"   自定义变量: {json.dumps(custom_vars, ensure_ascii=False)}")
    if file_infos:
        print(f"   文件数量: {len(file_infos)}")
    
    print("-" * 50)
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            json=payload, 
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        full_content = ""
        token_info = None
        references = None
        thoughts = []
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                # 原始模式：直接打印原始 SSE 行
                if raw:
                    print(line, flush=True)
                    continue
                
                data = parse_sse_line(line)
                
                if not data:
                    continue
                
                event_type = data.get('type')
                payload_data = data.get('payload', {})
                
                # 处理回复事件
                if event_type == 'reply':
                    content_piece = payload_data.get('content', '')
                    is_final = payload_data.get('is_final', False)
                    is_evil = payload_data.get('is_evil', False)
                    reply_method = payload_data.get('reply_method', 0)
                    
                    if is_evil:
                        print("\n⚠️  消息命中敏感内容")
                        return
                    
                    # 增量输出
                    if content_piece:
                        print(content_piece, end='', flush=True)
                        full_content += content_piece
                    
                    if is_final:
                        print("\n")
                        # 显示回复方式
                        reply_methods = {
                            1: "大模型回复", 2: "未知问题回复", 3: "拒答问题回复",
                            4: "敏感回复", 5: "已采纳问答对优先回复", 6: "欢迎语回复",
                            7: "并发数超限回复", 8: "全局干预知识", 9: "任务流回复",
                            10: "任务流答案", 11: "搜索引擎回复", 12: "知识润色后回复",
                            13: "图片理解回复", 14: "实时文档回复", 15: "澄清确认回复",
                            16: "工作流回复", 17: "工作流运行结束", 18: "智能体回复",
                            19: "多意图回复"
                        }
                        method_name = reply_methods.get(reply_method, f"未知方式({reply_method})")
                        print(f"📝 回复方式: {method_name}")
                
                # 处理Token统计
                elif event_type == 'token_stat':
                    token_info = payload_data
                
                # 处理参考来源
                elif event_type == 'reference':
                    references = payload_data.get('references', [])
                
                # 处理思考过程 (DeepSeek-R1)
                elif event_type == 'thought':
                    procedures = payload_data.get('procedures', [])
                    for proc in procedures:
                        if proc.get('name') == 'thought':
                            debugging = proc.get('debugging', {})
                            thought_content = debugging.get('content', '')
                            if thought_content:
                                thoughts.append(thought_content)
                                print(f"\n💭 思考过程: {thought_content[:200]}...")
                
                # 处理错误
                elif event_type == 'error':
                    error = data.get('error', {})
                    print(f"\n❌ 错误 [{error.get('code')}]: {error.get('message')}")
                    return
        
        # 打印统计信息
        print("-" * 50)
        if token_info:
            print(f"📊 Token统计: 总计 {token_info.get('token_count', 0)} tokens")
            print(f"⏱️  耗时: {token_info.get('elapsed', 0)}ms")
            
            # 打印各阶段详情
            procedures = token_info.get('procedures', [])
            for proc in procedures:
                print(f"   - {proc.get('title')}: {proc.get('count', 0)} tokens")
        
        # 打印参考来源
        if references:
            print(f"\n📚 参考来源 ({len(references)}个):")
            for i, ref in enumerate(references, 1):
                ref_type = ref.get('type')
                if ref_type == 1:
                    type_str = "问答"
                elif ref_type == 2:
                    type_str = "文档片段"
                elif ref_type == 4:
                    type_str = "联网检索"
                else:
                    type_str = "未知"
                print(f"   [{i}] {ref.get('name', '未知')} ({type_str})")
                if ref.get('url'):
                    print(f"       URL: {ref.get('url')}")
        
        # 打印思考过程总结
        if thoughts:
            print(f"\n💭 思考过程总结 ({len(thoughts)}段)")
            for i, thought in enumerate(thoughts, 1):
                print(f"   [{i}] {thought[:100]}...")
        
        print(f"\n✅ 对话完成")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求失败: {e}")


def main():
    parser = argparse.ArgumentParser(description='腾讯云智能体 HTTP SSE 对话客户端')
    
    # 必填参数
    parser.add_argument('--app-key', required=True, help='应用 AppKey')
    parser.add_argument('--content', required=True, help='消息内容')
    
    # 基础参数
    parser.add_argument('--session-id', help='会话ID (可选)')
    parser.add_argument('--visitor-id', help='访客ID (可选)')
    parser.add_argument('--model', choices=[
        'hunyuan', 'hunyuan-13B', 'hunyuan-turbo', 'hunyuan-standard-256K', 'hunyuan-role',
        'lke-deepseek-r1', 'lke-deepseek-v3', 'lke-deepseek-r1-0528', 'lke-deepseek-v3-0324'
    ], help='模型名称 (可选)')
    
    # 高级参数
    parser.add_argument('--system-role', help='系统角色指令 (可选)')
    parser.add_argument('--streaming-throttle', type=int, default=5, help='流式回包频率 (默认: 5)')
    parser.add_argument('--search-network', choices=['enable', 'disable'], help='联网搜索 enable/disable (可选)')
    parser.add_argument('--stream', choices=['enable', 'disable'], help='流式传输 enable/disable (可选)')
    parser.add_argument('--workflow-status', choices=['enable', 'disable'], help='工作流 enable/disable (可选)')
    parser.add_argument('--incremental', type=bool, default=True, help='增量输出 (默认: True)')
    
    # JSON参数
    parser.add_argument('--custom-vars', help='自定义变量 JSON (可选, 如: \'{"UserID":"123"}\')')
    parser.add_argument('--visitor-labels', help='访客标签 JSON (可选)')
    parser.add_argument('--file-infos', help='文件信息 JSON (可选)')
    
    # 输出模式
    parser.add_argument('--raw', action='store_true', help='原始输出模式，显示完整 SSE 流数据')
    
    args = parser.parse_args()
    
    # 解析JSON参数
    custom_vars = parse_json_arg(args.custom_vars, 'custom-vars')
    visitor_labels = parse_json_arg(args.visitor_labels, 'visitor-labels')
    file_infos = parse_json_arg(args.file_infos, 'file-infos')
    
    if any(arg is None for arg in [custom_vars, visitor_labels, file_infos]):
        return
    
    chat_with_bot(
        app_key=args.app_key,
        content=args.content,
        session_id=args.session_id,
        visitor_id=args.visitor_id,
        model=args.model,
        system_role=args.system_role,
        streaming_throttle=args.streaming_throttle,
        search_network=args.search_network,
        stream=args.stream,
        workflow_status=args.workflow_status,
        incremental=args.incremental,
        custom_vars=custom_vars,
        visitor_labels=visitor_labels,
        file_infos=file_infos,
        raw=args.raw
    )


if __name__ == '__main__':
    main()
