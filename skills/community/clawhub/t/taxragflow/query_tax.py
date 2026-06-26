import requests
import json
import os
import sys

def query_ragflow(query_text, conversation_id=None):
    """
    向 RAGFlow 的 OpenAI 兼容接口发送问题并获取回答。
    
    Args:
        query_text (str): 用户提出的问题。
        conversation_id (str): 对话ID，用于多轮对话。首次对话可为 None。
    
    Returns:
        str: RAGFlow 返回的答案。
    """
    # 从环境变量中读取配置，保持安全性
    RAGFLOW_API_URL = os.getenv("RAGFLOW_API_URL")
    RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
    # 此ID是你在 RAGFlow 中创建的对话助手的 ID
    RAGFLOW_CHAT_ID = os.getenv("RAGFLOW_CHAT_ID")
    
    # 检查必需的环境变量是否已配置
    if not all([RAGFLOW_API_URL, RAGFLOW_API_KEY, RAGFLOW_CHAT_ID]):
        return "错误：请配置环境变量 RAGFLOW_API_URL、RAGFLOW_API_KEY 和 RAGFLOW_CHAT_ID。\n请参考 README.md 中的安装说明。" 

    # 注意：如果你调用的不是标准 OpenAI 兼容端点，请根据你的实际 API 修改 URL 路径
    url = f"{RAGFLOW_API_URL}/api/v1/chats_openai/{RAGFLOW_CHAT_ID}/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RAGFLOW_API_KEY}"
    }

    # 使用非流式请求（最简单、最可靠）
    payload = {
        "model": "deepseek-chat",   # 必须与你后台的模型名称一致
        "messages": [{"role": "user", "content": query_text}],
        "stream": False
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        # print("状态码:", response.status_code)
        # print("原始内容:", response.text)
        answer = response.json()
        # 标准 openai 格式
        if 'choices' in answer:
            return answer['choices'][0]['message']['content']
        else:
            return json.dumps(answer, ensure_ascii=False)

        # answer = response.json()
        # print(json.dumps(answer, indent=2, ensure_ascii=False))
        # return answer['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        return f"API 请求发生错误: {e}"

if __name__ == "__main__":
    # 检查是否安装了 python-dotenv（可选）
    try:
        from dotenv import load_dotenv
        load_dotenv()  # 加载 .env 文件中的配置
    except ImportError:
        pass  # 如果没有安装 python-dotenv，则只使用系统环境变量
    
    # 从命令行参数获取用户问题
    user_query = " ".join(sys.argv[1:])
    if not user_query:
         print("请提供一个查询问题。")
         print("用法: python query_tax.py \"你的问题\"")
    else:
        result = query_ragflow(user_query)
        print(result)