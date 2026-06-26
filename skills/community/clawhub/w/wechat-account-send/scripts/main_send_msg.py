import requests
import json
import time
import base64
import os
import uuid
from pathlib import Path
import sys
def get_openclaw_path():
    """获取OpenClaw安装路径，支持Windows、Linux、MacOS"""
    # 优先使用环境变量指定的路径
    state_dir = os.environ.get('OPENCLAW_STATE_DIR')
    if state_dir and os.path.exists(state_dir):
        return Path(state_dir)
    
    # 默认路径
    home = Path.home()
    if sys.platform == 'win32':
        # Windows: C:\Users\用户名\.openclaw
        return home / '.openclaw'
    else:
        # Linux/MacOS: ~/.openclaw
        return home / '.openclaw'
    

def find_account_json(account_id,use_path=False):
    """根据账号ID查找对应的JSON文件并返回内容"""
    try:
        if use_path:
            openclaw_path = use_path
        else:
            # 获取OpenClaw路径
            openclaw_path = get_openclaw_path()
        # 构建openclaw-weixin/accounts路径
        weixin_accounts_path = os.path.join( openclaw_path,'openclaw-weixin','accounts')
        # 检查路径是否存在
        if not os.path.exists(weixin_accounts_path):
            return {"error": f"路径不存在: {weixin_accounts_path}"}
        datas = {}
        for file_json in [account_id,account_id+".context-tokens",account_id+".sync"]:
            # 构建JSON文件路径
            json_file = os.path.join(weixin_accounts_path,f"{file_json}.json")
            # 读取并返回JSON内容
            with open(json_file, 'r', encoding='utf-8') as f:
                datas[file_json] = json.load(f)
        return {
            "account_id": account_id,
            "file_path": str(json_file),
            "data": datas
        }
        
    except Exception as e:
        return {"error": f"读取失败: {str(e)}"}

def send_weixin_message(BASE_URL,BOT_TOKEN,TARGET_USER_ID,CONTEXT_TOKEN,TXT_MSG):
    """
    通过微信后端API发送一条文本测试消息。
    """
    # 1. 构建请求URL (关键：端点路径为 /ilink/bot/sendmessage)
    api_endpoint = f"{BASE_URL.rstrip('/')}/ilink/bot/sendmessage"
    
    # 2. 生成请求唯一标识 (client_id) 和随机UIN
    timestamp_ms = int(time.time() * 1000)
    random_suffix = uuid.uuid4().hex[:8]
    client_id = f"openclaw-weixin:{timestamp_ms}-{random_suffix}"
    random_uint32 = os.urandom(4)
    x_wechat_uin = base64.b64encode(random_uint32).decode('utf-8')
    
    # 3. 构建请求体 (JSON)
    payload = {
        "msg": {
            "from_user_id": "",  # 机器人发送时固定为空字符串
            "to_user_id": TARGET_USER_ID,
            "client_id": client_id,
            "message_type": 2,   # 固定为2，代表Bot消息
            "message_state": 2,  # 固定为2，代表完成态
            "context_token": CONTEXT_TOKEN,  # 重要：如果为空，首次发送可能失败
            "item_list": [
                {
                    "type": 1,  # 1 代表文本消息
                    "text_item": {
                        "text": TXT_MSG
                    }
                }
            ]
        },
        "base_info": {
            "channel_version": "1.0.0"  # 应与您的信道插件版本一致
        }
    }
    # 4. 构建请求头
    raw = json.dumps(payload, ensure_ascii=False)  
    headers = {  
    "Content-Type": "application/json",  
    "AuthorizationType": "ilink_bot_token",  
    "Authorization": f"Bearer {BOT_TOKEN}",  
    "X-WECHAT-UIN": x_wechat_uin,  
    "Content-Length": str(len(raw.encode("utf-8"))),  
    }  
    print("=" * 50)
    print("【微信消息发送测试】")
    print(f"目标用户: {TARGET_USER_ID}")
    print(f"客户端ID: {client_id}")
    print(f"上下文Token: {CONTEXT_TOKEN if CONTEXT_TOKEN else '(为空，可能影响首次发送)'}")
    print("-" * 30)
    try:
        # 5. 发送POST请求
        response = requests.post(
            api_endpoint,
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            timeout=15  # 秒
        )
        # 6. 处理响应
        print(f"HTTP 状态码: {response.status_code}")
        if response.status_code == 200:
            resp_json = response.json()
            print(f"API 返回码 (ret): {resp_json.get('ret')}")
            print("✅ 消息发送成功！")
            print("服务器响应详情:")
            print(json.dumps(resp_json, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 请求失败，HTTP状态码非200。")
            print(f"响应内容: {response.text[:500]}")  # 打印前500字符以便调试
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ 解析服务器响应失败: {e}")
        print(f"原始响应文本: {response.text[:500]}")
    print("=" * 50)


def main():
    """主函数：从命令行参数获取账号ID并返回JSON"""
    if len(sys.argv) != 3:
        print("用法: python script.py <account_id> <msg>")
        print("示例: python script.py wechat_12345 你好")
        sys.exit(1)
    
    account_id = sys.argv[1]
    TXT_MSG = sys.argv[2]
    result = find_account_json(account_id)
    result = result["data"]
    # ==================== 配置区 (请根据您的实际情况修改) ====================
    # 1. 基础API地址 (从扫码登录后的账户配置中获取)
    BASE_URL = result[f"{account_id}"]["baseUrl"]  # 请替换为您的有效 baseUrl
    # 2. 机器人令牌 (Bot Token)
    BOT_TOKEN = result[f"{account_id}"]["token"]  # 请替换为您的有效 token
    # 3. 消息接收方用户ID
    TARGET_USER_ID = result[f"{account_id}"]["userId"]  # 请替换为目标用户的 userId 
    # 4. 会话上下文令牌 (Context Token)
    CONTEXT_TOKEN = result[f"{account_id}.context-tokens"][result[f"{account_id}"]["userId"]]

    # 正常的逻辑是机器人提供消息用户的ID，让后我通过查询插件数据获取token
    # 输出JSON格式的结果
    send_weixin_message(BASE_URL,BOT_TOKEN,TARGET_USER_ID,CONTEXT_TOKEN,TXT_MSG)

if __name__ == "__main__":
    # 执行发送测试
    main()
    # 调用方法
    # python main_send_msg.py XXXXXXXXXXXX-im-bot "你好"
