import httpx
import json
import base64
import random
import time
import hashlib
from pathlib import Path
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote
import os
import requests
import uuid
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
            return {"error": f"路径不存在: {weixin_accounts_path} 你可以设置一个测试地址use_path" }
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


# 计算AES-128-ECB加密后的文件大小
def calculate_encrypted_size(raw_size: int) -> int:
    """
    计算AES-128-ECB加密后的文件大小
    
    根据文档公式：filesize = ceil((rawsize + 1) / 16) * 16
    因为PKCS7填充会至少填充1个字节
    """
    return ((raw_size + 1 + 15) // 16) * 16
    

# 准备上传参数
def prepare_image_upload( image_path: str) -> Dict[str, Any]:
    """
    准备图片上传：计算所有必要参数
    返回包含所有上传所需参数的字典
    """
    if not Path(image_path).exists():
        return {
            "success": False,
            "error": f"图片文件不存在: {image_path}"
        }
    
    try:
        # 读取文件
        with open(image_path, 'rb') as f:
            file_data = f.read()
        
        # 计算文件参数
        rawsize = len(file_data)
        rawfilemd5 = hashlib.md5(file_data).hexdigest()
        
        # 生成随机参数
        filekey = ''.join(random.choices('0123456789abcdef', k=32))  # 16字节hex
        aeskey_hex = ''.join(random.choices('0123456789abcdef', k=32))  # 16字节hex
        
        # 计算加密后大小
        filesize = calculate_encrypted_size(rawsize)
        
        return {
            "success": True,
            "filekey": filekey,
            "aeskey_hex": aeskey_hex,
            "rawsize": rawsize,
            "rawfilemd5": rawfilemd5,
            "filesize": filesize,
            "file_data": file_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"准备图片失败: {str(e)}"
        }

# 加密文件
def aes_encrypt_file(file_path: str, aes_key_hex: str) -> bytes:
        """
        使用AES-128-ECB模式加密文件，使用PKCS7 padding
        
        根据文档第二步：本地加密文件
        """
        if len(aes_key_hex) != 32:
            raise ValueError("AES密钥必须是32个十六进制字符（16字节）")
        
        # 将十六进制字符串转换为字节
        aes_key = bytes.fromhex(aes_key_hex)
        
        # 读取文件
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # 创建AES-128-ECB加密器
        cipher = AES.new(aes_key, AES.MODE_ECB)
        
        # 对数据进行PKCS7填充并加密
        padded_data = pad(file_data, AES.block_size, style='pkcs7')
        encrypted_data = cipher.encrypt(padded_data)
        
        return encrypted_data

# 编码AES密钥
def encode_aes_key(aes_key_hex: str) -> str:
    """
    将AES密钥编码为"base64(hex string)"格式
    
    根据文档8.4节：先把hex文本当作字节，再base64
    例如：hex "00112233445566778899aabbccddeeff" → "MDAxMTIyMzM0NDU1NjY3Nzg4OTlhYWJiY2NkZGVlZmY="
    """
    # 将十六进制字符串转换为字节
    hex_bytes = aes_key_hex.encode('utf-8')
    # 进行base64编码
    return base64.b64encode(hex_bytes).decode('utf-8')


# 申请上传参数
def get_upload_params(  use_token: str,
                        filekey: str,
                        media_type: int,
                        to_user_id: str,
                        rawsize: int,
                        rawfilemd5: str,
                        filesize: int,
                        aeskey_hex: str,
                        no_need_thumb: bool = True) -> Dict[str, Any]:
    """
    第一步：申请上传参数 (getuploadurl)
    
    根据文档8.2节第一步
    """
    random_uint32 = os.urandom(4)
    x_wechat_uin = base64.b64encode(random_uint32).decode('utf-8')
    # 构造请求体
    body = {
        "filekey": filekey,
        "media_type": media_type,  # 1=图片
        "to_user_id": to_user_id,
        "rawsize": rawsize,
        "rawfilemd5": rawfilemd5,
        "filesize": filesize,
        "no_need_thumb": no_need_thumb,
        "aeskey": aeskey_hex,
        "base_info": {
            "channel_version": "1.0.0"
        }
    }
    # 发送请求
    raw = json.dumps(body, ensure_ascii=False)  
    headers = {  
    "Content-Type": "application/json",  
    "AuthorizationType": "ilink_bot_token",  
    "Authorization": f"Bearer {use_token}",  
    "X-WECHAT-UIN": x_wechat_uin,  
    "Content-Length": str(len(raw.encode("utf-8"))),  
    }  
    
    # 发送POST请求
    resp = requests.post(
        "https://ilinkai.weixin.qq.com/ilink/bot/getuploadurl",
        headers=headers,
        data=  raw.encode('utf-8'),
        timeout=15  # 秒
    )
    if resp.status_code != 200:
        return {
            "success": False,
            "error": f"申请上传参数失败，HTTP状态码: {resp.status_code}",
            "response": resp.text
        }
    
    result = resp.json()
    upload_param = result.get("upload_param", "")
    
    if not upload_param:
        return {
            "success": False,
            "error": "响应中未包含upload_param",
            "response": result
        }
    
    return {
        "success": True,
        "upload_param": upload_param,  # 就是encrypted_query_param
        "thumb_upload_param": result.get("thumb_upload_param", ""),
        "response": result
    }

# 上传到CDN
def upload_to_cdn(  upload_param: str,
                    filekey: str,
                    encrypted_data: bytes) -> Dict[str, Any]:
    """
    第三步：上传到CDN
    
    根据文档8.2节第三步
    """
    # 构建CDN上传URL
    encoded_param = quote(upload_param, safe='')
    cdn_url = f"https://novac2c.cdn.weixin.qq.com/c2c/upload?encrypted_query_param={encoded_param}&filekey={filekey}"
    # 构造请求头
    headers = {
        "Content-Type": "application/octet-stream"
    }
    
    try:
        # 发送请求
        resp = httpx.post(
            cdn_url,
            headers=headers,
            content=encrypted_data,
            timeout=30,
        )
        
        if resp.status_code == 200:
            encrypt_query_param = resp.headers.get('x-encrypted-param', '')
            
            if not encrypt_query_param:
                return {
                    "success": False,
                    "error": "未在响应头中找到x-encrypted-param",
                    "headers": dict(resp.headers)
                }
            return {
                "success": True,
                "encrypt_query_param": encrypt_query_param,
                "response_headers": dict(resp.headers)
            }
        else:
            return {
                "success": False,
                "error": f"上传失败，HTTP状态码: {resp.status_code}",
                "response": resp.text
            }
    except httpx.RequestError as e:
        return {
            "success": False,
            "error": f"上传请求失败: {str(e)}"
        }

def send_weixin_file(BOT_TOKEN,TARGET_USER_ID,CONTEXT_TOKEN,IMAGE_PATH):
    """
    根据文件类型发送微信文件
    
    参数说明：
    BOT_TOKEN: 机器人令牌
    TARGET_USER_ID: 目标用户ID
    CONTEXT_TOKEN: 上下文令牌
    FILE_PATH: 文件路径（支持图片、视频、文件等多种类型）
    
    媒体类型说明：
    1: 图片消息类型
    2: 视频消息类型
    3: 文件消息类型
    4: 音频消息类型
    """
    
    # 根据文件后缀判断媒体类型
    file_ext = IMAGE_PATH.lower().split('.')[-1] if '.' in IMAGE_PATH else ''
    
    # 图片类型
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff', 'svg']
    # 视频类型
    video_extensions = ['mp4', 'mov', 'avi', 'wmv', 'flv', 'mkv', 'webm', 'mpeg', 'mpg']
    # 音频类型
    audio_extensions = ['mp3', 'wav', 'aac', 'flac', 'm4a', 'ogg', 'wma']
    # 文档类型
    document_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt']
    # 压缩文件类型
    archive_extensions = ['zip', 'rar', '7z', 'tar', 'gz']
    
    # 判断文件类型
    if file_ext in image_extensions:
        media_type = 1
    elif file_ext in video_extensions:
        media_type = 2
    elif file_ext in audio_extensions:
        media_type = 4
    elif file_ext in document_extensions or file_ext in archive_extensions:
        media_type = 3
    else:
        # 默认处理为文件类型
        media_type = 3
        print(f"警告：未知文件类型 .{file_ext}，将作为普通文件发送")

    # 1.准备上传参数
    print("1. 准备上传参数...")
    prepare_result = prepare_image_upload(IMAGE_PATH)
    if not prepare_result["success"]:
        print(f"准备失败: {prepare_result.get('error')}")
    else:
        print(f"准备成功，filekey: {prepare_result['filekey'][:16]}..., aeskey: {prepare_result['aeskey_hex'][:16]}...")

        filekey = prepare_result["filekey"]
        aeskey_hex = prepare_result["aeskey_hex"]
        rawsize = prepare_result["rawsize"]
        rawfilemd5 = prepare_result["rawfilemd5"]
        filesize = prepare_result["filesize"]

         # 2.申请上传参数
        print("2. 申请上传参数...")
        upload_params = get_upload_params(
            use_token=BOT_TOKEN,
            filekey=filekey,
            media_type=media_type,
            to_user_id=TARGET_USER_ID,
            rawsize=rawsize,
            rawfilemd5=rawfilemd5,
            filesize=filesize,
            aeskey_hex=aeskey_hex,
            no_need_thumb=True
        )
        print(f"获取到upload_param: {upload_params['upload_param'][:20]}...")
            
        # 3. 加密文件...
        print("3. 加密文件...")
        encrypted_data = aes_encrypt_file(IMAGE_PATH,aeskey_hex)
        print(f"  加密完成，原始大小: {rawsize}, 加密后大小: {len(encrypted_data)}")
        # 4. 上传到CDN...
        print("4. 上传到CDN...")
        upload_result = upload_to_cdn(upload_params["upload_param"],filekey, encrypted_data)
        encrypt_query_param = upload_result["encrypt_query_param"]
        print(f"  上传成功，encrypt_query_param: {encrypt_query_param[:20]}...")
        # 编码AES密钥
        encoded_aes_key = encode_aes_key(aeskey_hex)    
        upload_result = {
            "success": True,
            "encrypt_query_param": encrypt_query_param,
            "aes_key_hex": aeskey_hex,
            "encoded_aes_key": encoded_aes_key,
            "file_size": rawsize,
            "filesize": filesize,
            "filekey": filekey
        }

        # 5. 发送图片...
        print("5. 发送文件...")
        timestamp_ms = int(time.time() * 1000)
        random_suffix = uuid.uuid4().hex[:8]
        client_id = f"openclaw-weixin:{timestamp_ms}-{random_suffix}"
        random_uint32 = os.urandom(4)
        x_wechat_uin = base64.b64encode(random_uint32).decode('utf-8')
        # 构造图片消息体（第四步）
        if media_type == 1:
            payload = {
                "msg": {
                    "from_user_id": "",
                    "to_user_id": TARGET_USER_ID,
                    "client_id": client_id,
                    "message_type": 2,
                    "message_state": 2,
                    "context_token": CONTEXT_TOKEN,
                    "item_list": [
                        {
                            "type": 2,  # 图片消息类型
                            "image_item": {
                                "media": {
                                    "encrypt_query_param": upload_result["encrypt_query_param"],
                                    "aes_key": upload_result["encoded_aes_key"],
                                    "encrypt_type": 1
                                },
                                "mid_size": upload_result["file_size"]  # 明文文件大小
                            }
                        }
                    ]
                },
                "base_info": {
                    "channel_version": "1.0.0"
                }
            }
        # 构造文件消息体（第四步）
        elif media_type == 3:
            payload = {
                "msg": {
                    "from_user_id": "",
                    "to_user_id": TARGET_USER_ID,
                    "client_id": client_id,
                    "message_type": 2,
                    "message_state": 2,
                    "context_token": CONTEXT_TOKEN,
                    "item_list": [
                        {
                            "type": 4,
                            "file_item": {
                                "media": {
                                    "encrypt_query_param": upload_result["encrypt_query_param"],
                                    "aes_key": upload_result["encoded_aes_key"],
                                    "encrypt_type": 1
                                },
                                "file_name": Path(IMAGE_PATH).name,
                                # "len": filesize, 写了发不出去，应该是前面有问题
                                # "md5": rawfilemd5 同
                            }
                        }
                    ]
                },
                "base_info": {
                    "channel_version": "1.0.0"
                }
            }
        
        # 构造视频消息体（第四步）
        elif media_type == 2:
            payload = {
                "msg": {
                    "from_user_id": "",
                    "to_user_id": TARGET_USER_ID,
                    "client_id": client_id,
                    "message_type": 2,
                    "message_state": 2,
                    "context_token": CONTEXT_TOKEN,
                    "item_list": [
                        {
                            "type": 5,
                            "video_item": {
                                "media": {
                                    "encrypt_query_param": upload_result["encrypt_query_param"],
                                    "aes_key": upload_result["encoded_aes_key"],
                                    "encrypt_type": 1
                                },
                                "video_size": upload_result["file_size"]  # 明文文件大小
                            }
                        }
                    ]
                },
                "base_info": {
                    "channel_version": "1.0.0"
                }
            }
        
        # 发送请求
        # 4. 构建请求头
        raw = json.dumps(payload, ensure_ascii=False)  
        headers = {  
        "Content-Type": "application/json",  
        "AuthorizationType": "ilink_bot_token",  
        "Authorization": f"Bearer {BOT_TOKEN}",  
        "X-WECHAT-UIN": x_wechat_uin,  
        "Content-Length": str(len(raw.encode("utf-8"))),  
        }  
            # 发送POST请求
        response = requests.post(
            "https://ilinkai.weixin.qq.com/ilink/bot/sendmessage",
            headers=headers,
            data=  raw.encode('utf-8'),
            timeout=15  # 秒
        )
        print(f"HTTP 状态码: {response.status_code}")
        if response.status_code == 200:
            resp_json = response.json()
            print(f"API 返回码 (ret): {resp_json.get('ret')}")
            print("✅ 文件发送成功！")
            print("服务器响应详情:")
            print(json.dumps(resp_json, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 请求失败，HTTP状态码非200。")
            print(f"响应内容: {response.text[:500]}")  # 打印前500字符以便调试

def main():
    """主函数：从命令行参数获取账号ID并返回JSON"""
    if len(sys.argv) != 3:
        print("用法: python script.py <account_id> <msg>")
        print("示例: python script.py wechat_12345 你好")
        sys.exit(1)
    
    account_id = sys.argv[1]
    IMAGE_PATH = sys.argv[2]
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
    send_weixin_file(BOT_TOKEN,TARGET_USER_ID,CONTEXT_TOKEN,IMAGE_PATH)

if __name__ == "__main__":
    main()
    # 调用方法
    # python main_send_file.py XXXXXXXXXXXX-im-bot "测试文件.txt"
    # python main_send_file.py XXXXXXXXXXXX-im-bot "测试视频.txt"
    # python main_send_file.py XXXXXXXXXXXX-im-bot "测试图片.txt"

