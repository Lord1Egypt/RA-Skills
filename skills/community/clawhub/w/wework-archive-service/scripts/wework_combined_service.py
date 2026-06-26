#!/usr/bin/env python3
"""
企业微信整合服务 - 包含普通回调和会话内容存档
运行在8400端口
整合线程安全存储功能和查询接口
"""

from flask import Flask, request, jsonify
import hashlib
import base64
import json
import logging
import time
import struct
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import sys
import requests
from datetime import datetime

# 导入线程安全存储系统
sys.path.append('.')
from simple_storage import SimpleStorage

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wework_combined.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ==================== 配置部分 ====================

# 普通回调配置（自建应用）
CALLBACK_TOKEN = "QFIFdVxh"
CALLBACK_ENCODING_AES_KEY = "EsHGr7F9296zJaAhAKtO5Mfa5qnITs2D0S7fSBS0Fj3"
CORP_ID = "ww1533baf21ccf36ff"
AGENT_ID = 1000016
CORP_SECRET = "zddW0DZ3YIYykXyqk5SKmMm4GN1fduqVhFsR8UXSENA"

# 会话内容存档配置
ARCHIVE_TOKEN = "mXSkgsfxr3k0OKQrJprkPl"
ARCHIVE_ENCODING_AES_KEY = "EuauICQFeCAUI6srNiVR0jDBc8X6oE2QclpHbnrjhyS"

# 全局变量缓存access_token
access_token_cache = None
access_token_expire_time = 0

def get_access_token():
    """获取企业微信access_token，带缓存"""
    global access_token_cache, access_token_expire_time
    current_time = int(time.time())
    
    # 如果缓存有效直接返回
    if access_token_cache and current_time < access_token_expire_time:
        return access_token_cache
    
    try:
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={CORP_SECRET}"
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            access_token_cache = result.get('access_token')
            access_token_expire_time = current_time + result.get('expires_in', 7200) - 60 # 提前1分钟过期
            logger.info(f"✅ 获取access_token成功，有效期至: {datetime.fromtimestamp(access_token_expire_time)}")
            return access_token_cache
        else:
            logger.error(f"❌ 获取access_token失败: {result.get('errmsg')}")
            return None
    except Exception as e:
        logger.error(f"❌ 获取access_token异常: {e}")
        return None

def send_text_message(user_id, content):
    """给指定用户发送文本消息"""
    access_token = get_access_token()
    if not access_token:
        return False
    
    try:
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        data = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": AGENT_ID,
            "text": {
                "content": content
            },
            "safe": 0
        }
        
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            logger.info(f"✅ 给用户{user_id}发送消息成功: {content}")
            return True
        else:
            logger.error(f"❌ 给用户{user_id}发送消息失败: {result.get('errmsg')}")
            return False
    except Exception as e:
        logger.error(f"❌ 发送消息异常: {e}")
        return False

# 回调URL - 统一使用 ai.hexync.com
CALLBACK_URL = "https://ai.hexync.com/wework/callback"
ARCHIVE_CALLBACK_URL = "https://ai.hexync.com/wework/archive"

# ==================== 初始化存储系统 ====================

# 初始化线程安全存储系统
storage_system = SimpleStorage(db_path="wework_combined.db")
logger.info("线程安全存储系统初始化完成")

# ==================== 通用工具函数 ====================

def verify_signature(token, timestamp, nonce, msg_signature, encrypt_msg=None):
    """验证签名"""
    if encrypt_msg:
        tmp_list = [token, timestamp, nonce, encrypt_msg]
    else:
        tmp_list = [token, timestamp, nonce]
    
    tmp_list.sort()
    tmp_str = ''.join(tmp_list)
    calculated = hashlib.sha1(tmp_str.encode()).hexdigest()
    
    return calculated == msg_signature

def decrypt_data(encrypt_data, encoding_aes_key, corp_id):
    """解密数据"""
    try:
        # 补等号
        aes_key = base64.b64decode(encoding_aes_key + "=")
        
        encrypt_bytes = base64.b64decode(encrypt_data)
        
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        decrypted = cipher.decrypt(encrypt_bytes)
        
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        
        random_str = decrypted[:16]
        data_len = struct.unpack("!I", decrypted[16:20])[0]
        raw_data = decrypted[20:20+data_len]
        recv_corp_id = decrypted[20+data_len:].decode("utf-8")
        
        if recv_corp_id != corp_id:
            logger.error(f"CorpID验证失败: 期望 {corp_id}, 实际 {recv_corp_id}")
            return None
        
        raw_text = raw_data.decode("utf-8")
        return raw_text
        
    except Exception as e:
        logger.error(f"解密失败: {e}")
        return None

# ==================== 普通回调处理 ====================

@app.route('/wework/callback', methods=['GET', 'POST'])
def wework_callback():
    """企业微信普通回调接口"""
    # 企业微信openapi使用signature，存档使用msg_signature
    signature = request.args.get('signature', '') or request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')
    
    logger.info(f"📞 收到普通回调请求: method={request.method}")
    
    if request.method == 'GET':
        logger.info("处理GET请求（URL验证）")
        # GET验证需要将echostr作为encrypt_msg参数
        if verify_signature(CALLBACK_TOKEN, timestamp, nonce, signature, echostr):
            logger.info("✅ 普通回调GET签名验证成功")
            return echostr
        else:
            logger.error("❌ 普通回调GET签名验证失败")
            return '验证失败', 403
    
    elif request.method == 'POST':
        logger.info("处理POST请求（消息接收）")
        
        request_data = request.get_data(as_text=True)
        logger.info(f"📥 收到普通回调请求体，长度: {len(request_data)}")
        
        try:
            xml_root = ET.fromstring(request_data)
            encrypt_msg = xml_root.find('Encrypt').text
            logger.info(f"提取加密消息，长度: {len(encrypt_msg)}")
        except Exception as e:
            logger.error(f"❌ 解析XML失败: {e}")
            return 'XML解析失败', 400
        
        if not verify_signature(CALLBACK_TOKEN, timestamp, nonce, signature, encrypt_msg):
            logger.error("❌ 普通回调POST签名验证失败")
            return '验证失败', 403
        
        logger.info("✅ 普通回调POST签名验证成功")
        
        raw_data = decrypt_data(encrypt_msg, CALLBACK_ENCODING_AES_KEY, CORP_ID)
        if not raw_data:
            logger.error("❌ 普通回调消息解密失败")
            return 'success'
        
        logger.info(f"✅ 普通回调消息解密成功，原始数据: {raw_data}")
        
        # 解析普通消息，自动回复
        try:
            msg_root = ET.fromstring(raw_data)
            from_user = msg_root.find('FromUserName').text
            msg_type = msg_root.find('MsgType').text
            
            if msg_type == 'text':
                content = msg_root.find('Content').text
                logger.info(f"📩 收到用户{from_user}的文本消息: {content}")
                # 自动回复内容
                reply_content = "你好！我已经收到你的消息啦😉 普通回调功能目前运行正常，后续会根据你的需求处理消息~"
                send_success = send_text_message(from_user, reply_content)
                if send_success:
                    logger.info(f"✅ 已自动回复用户{from_user}")
                else:
                    logger.error(f"❌ 回复用户{from_user}失败")
        except Exception as e:
            logger.error(f"❌ 处理普通消息异常: {e}")
        
        return 'success'
    
    return 'Method Not Allowed', 405

# ==================== 会话内容存档处理 ====================

def parse_archive_message(raw_data):
    """解析会话内容存档消息 - 返回与存储系统兼容的格式"""
    try:
        data = json.loads(raw_data)
        msg_type = data.get('msgtype', '')
        msg_id = data.get('msgid', '')
        action = data.get('action', '')
        from_user = data.get('from', {}).get('userid', '')
        to_list = data.get('tolist', [])
        room_id = data.get('roomid', '')
        msg_time = data.get('msgtime', 0)
        
        logger.info(f"存档消息ID: {msg_id}, 类型: {msg_type}, 动作: {action}")
        logger.info(f"发送者: {from_user}, 接收者: {to_list}, 群聊: {room_id}")
        
        # 构建基础消息数据（与simple_storage.py兼容）
        message_data = {
            'msg_id': msg_id,
            'type': msg_type,
            'from': from_user,
            'to': to_list,
            'room': room_id,
            'time': msg_time,
            'action': action
        }
        
        # 根据消息类型解析内容
        if msg_type == 'text':
            content = data.get('text', {}).get('content', '')
            logger.info(f"文本消息: {content}")
            message_data['content'] = content
        
        elif msg_type == 'image':
            image_info = data.get('image', {})
            md5sum = image_info.get('md5sum', '')
            filesize = image_info.get('filesize', 0)
            sdkfileid = image_info.get('sdkfileid', '')
            logger.info(f"图片消息: md5={md5sum}, 大小={filesize}")
            message_data['image'] = {
                'md5': md5sum,
                'size': filesize,
                'file_id': sdkfileid
            }
        
        elif msg_type == 'voice':
            voice_info = data.get('voice', {})
            md5sum = voice_info.get('md5sum', '')
            voice_size = voice_info.get('voicesize', 0)
            play_length = voice_info.get('play_length', 0)
            sdkfileid = voice_info.get('sdkfileid', '')
            logger.info(f"语音消息: md5={md5sum}, 时长={play_length}秒")
            message_data['voice'] = {
                'md5': md5sum,
                'size': voice_size,
                'duration': play_length,
                'file_id': sdkfileid
            }
        
        elif msg_type == 'video':
            video_info = data.get('video', {})
            md5sum = video_info.get('md5sum', '')
            filesize = video_info.get('filesize', 0)
            play_length = video_info.get('play_length', 0)
            sdkfileid = video_info.get('sdkfileid', '')
            logger.info(f"视频消息: md5={md5sum}, 时长={play_length}秒")
            message_data['video'] = {
                'md5': md5sum,
                'size': filesize,
                'duration': play_length,
                'file_id': sdkfileid
            }
        
        elif msg_type == 'file':
            file_info = data.get('file', {})
            filename = file_info.get('filename', '')
            md5sum = file_info.get('md5sum', '')
            filesize = file_info.get('filesize', 0)
            sdkfileid = file_info.get('sdkfileid', '')
            logger.info(f"文件消息: {filename}, 大小={filesize}")
            message_data['file'] = {
                'filename': filename,
                'md5': md5sum,
                'size': filesize,
                'file_id': sdkfileid
            }
        
        elif msg_type == 'revoke':
            revoked_msg_id = data.get('revoke', {}).get('pre_msgid', '')
            logger.info(f"撤回消息: 原消息ID={revoked_msg_id}")
            message_data['revoke'] = {
                'original_msg_id': revoked_msg_id
            }
        
        else:
            logger.warning(f"未知消息类型: {msg_type}")
            message_data['raw_data'] = data
        
        return message_data
            
    except Exception as e:
        logger.error(f"解析存档消息失败: {e}")
        return None

def save_archive_to_database(message_data):
    """保存存档消息到数据库（示例）"""
    try:
        archive_dir = "wework_archive"
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        
        # 按日期保存
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{archive_dir}/archive_{date_str}.json"
        
        # 读取现有数据
        existing_data = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except:
                    existing_data = []
        
        # 添加新消息
        existing_data.append({
            'timestamp': datetime.now().isoformat(),
            'data': message_data
        })
        
        # 保存
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"存档消息已保存到: {filename}")
        return True
        
    except Exception as e:
        logger.error(f"保存存档失败: {e}")
        return False

@app.route('/wework/archive', methods=['GET', 'POST'])
def archive_callback():
    """会话内容存档回调接口"""
    # 临时修复：如果没有参数，返回简单响应
    if not request.args:
        return 'OK - WeWork Archive Service', 200

    # 企业微信openapi使用signature，存档使用msg_signature
    signature = request.args.get('signature', '') or request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')
    
    # 确保echostr正确解码（处理URL编码）
    import urllib.parse
    if echostr:
        # Flask应该已经自动解码了，但为了安全再次解码
        echostr = urllib.parse.unquote(echostr)
    
    logger.info(f"📚 收到会话内容存档请求: method={request.method}")
    
    if request.method == 'GET':
        logger.info("处理GET请求（URL验证）")
        # GET验证需要将echostr作为encrypt_msg参数
        if verify_signature(ARCHIVE_TOKEN, timestamp, nonce, signature, echostr):
            logger.info("✅ 存档GET签名验证成功")
            
            # 解密echostr并返回明文
            logger.info(f"尝试解密echostr，长度: {len(echostr)}")
            decrypted_echostr = decrypt_data(echostr, ARCHIVE_ENCODING_AES_KEY, CORP_ID)
            if decrypted_echostr:
                logger.info(f"✅ echostr解密成功: {decrypted_echostr}")
                return decrypted_echostr
            else:
                logger.error("❌ echostr解密失败")
                # 企业微信可能期望返回错误
                return '解密失败', 500
        else:
            logger.error("❌ 存档GET签名验证失败")
            return '验证失败', 403
    
    elif request.method == 'POST':
        logger.info("处理POST请求（存档消息接收）")
        
        request_data = request.get_data(as_text=True)
        logger.info(f"📥 收到存档请求体，长度: {len(request_data)}")
        
        try:
            xml_root = ET.fromstring(request_data)
            encrypt_msg = xml_root.find('Encrypt').text
            logger.info(f"提取加密存档消息，长度: {len(encrypt_msg)}")
        except Exception as e:
            logger.error(f"❌ 解析存档XML失败: {e}")
            return 'XML解析失败', 400
        
        if not verify_signature(ARCHIVE_TOKEN, timestamp, nonce, signature, encrypt_msg):
            logger.error("❌ 存档POST签名验证失败")
            return '验证失败', 403
        
        logger.info("✅ 存档POST签名验证成功")
        
        raw_data = decrypt_data(encrypt_msg, ARCHIVE_ENCODING_AES_KEY, CORP_ID)
        if not raw_data:
            logger.error("❌ 存档消息解密失败")
            return 'success'
        
        logger.info(f"✅ 存档消息解密成功，原始数据长度: {len(raw_data)}")
        
        # 解析存档消息
        message_data = parse_archive_message(raw_data)
        if message_data:
            logger.info(f"📝 存档消息解析成功: {message_data.get('type')}")
            
            # 保存到存储系统
            try:
                success = storage_system.save_message(message_data)
                if success:
                    logger.info("💾 消息已成功保存到存储系统")
                else:
                    logger.error("❌ 消息保存到存储系统失败")
            except Exception as e:
                logger.error(f"保存消息到存储系统失败: {e}")
            
            # 同时保存到文件备份（可选）
            save_archive_to_database(message_data)
            
        else:
            logger.warning("⚠️ 存档消息解析失败，但已接收")
        
        return 'success'
    
    return 'Method Not Allowed', 405

# ==================== 数据查询接口 ====================

@app.route('/api/messages', methods=['GET'])
def api_get_messages():
    """查询消息接口"""
    try:
        # 获取查询参数
        start_time = request.args.get('start_time', type=int)
        end_time = request.args.get('end_time', type=int)
        from_user = request.args.get('from_user')
        room_id = request.args.get('room_id')
        msg_type = request.args.get('msg_type')
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # 查询消息
        messages = storage_system.query_messages(
            start_time=start_time,
            end_time=end_time,
            from_user=from_user,
            room_id=room_id,
            msg_type=msg_type,
            limit=limit,
            offset=offset
        )
        
        return jsonify({
            'success': True,
            'count': len(messages),
            'messages': messages
        })
        
    except Exception as e:
        logger.error(f"查询消息接口失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """获取统计信息"""
    try:
        stats = storage_system.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"获取统计信息接口失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== 健康检查和统计 ====================

@app.route('/health', methods=['GET'])
def health_check():
    """整合服务健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'wework_combined',
        'timestamp': int(time.time()),
        'endpoints': {
            'callback': '/wework/callback',
            'archive': '/wework/archive',
            'api_messages': '/api/messages',
            'api_stats': '/api/stats',
            'archive_health': '/archive/health',
            'archive_stats': '/archive/stats'
        }
    })

@app.route('/archive/health', methods=['GET'])
def archive_health():
    """存档服务健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'wework_archive',
        'timestamp': int(time.time())
    })

@app.route('/archive/stats', methods=['GET'])
def archive_stats():
    """存档统计信息"""
    archive_dir = "wework_archive"
    
    if not os.path.exists(archive_dir):
        return jsonify({
            'total_files': 0,
            'total_messages': 0,
            'message_types': {}
        })
    
    total_messages = 0
    message_types = {}
    
    for filename in os.listdir(archive_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(archive_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_messages += len(data)
                    
                    for msg in data:
                        msg_type = msg.get('data', {}).get('type', 'unknown')
                        message_types[msg_type] = message_types.get(msg_type, 0) + 1
            except:
                pass
    
    return jsonify({
        'total_files': len([f for f in os.listdir(archive_dir) if f.endswith('.json')]),
        'total_messages': total_messages,
        'message_types': message_types
    })

@app.route('/debug/signature', methods=['POST'])
def debug_signature():
    """调试签名验证"""
    data = request.json
    token = data.get('token', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    msg_signature = data.get('msg_signature', '')
    encrypt_msg = data.get('encrypt_msg', '')
    
    result = verify_signature(token, timestamp, nonce, msg_signature, encrypt_msg)
    
    return jsonify({
        'verified': result,
        'token': token,
        'timestamp': timestamp,
        'nonce': nonce,
        'msg_signature': msg_signature,
        'encrypt_msg_provided': bool(encrypt_msg)
    })

# ==================== 主函数 ====================

if __name__ == '__main__':
    logger.info("🚀 启动企业微信整合服务")
    logger.info(f"监听端口: 8400")
    logger.info(f"CorpID: {CORP_ID}")
    logger.info(f"AgentID: {AGENT_ID}")
    logger.info("=" * 60)
    logger.info("普通回调配置:")
    logger.info(f"  回调URL: {CALLBACK_URL}")
    logger.info(f"  Token: {CALLBACK_TOKEN}")
    logger.info("=" * 60)
    logger.info("会话内容存档配置:")
    logger.info(f"  回调URL: {ARCHIVE_CALLBACK_URL}")
    logger.info(f"  Token: {ARCHIVE_TOKEN}")
    logger.info("=" * 60)
    logger.info("存储系统配置:")
    logger.info(f"  数据库: wework_combined.db")
    logger.info(f"  线程安全: 是")
    logger.info("=" * 60)
    logger.info("可用接口:")
    logger.info("  GET  /wework/callback    - 普通回调验证")
    logger.info("  POST /wework/callback    - 普通消息接收")
    logger.info("  GET  /wework/archive     - 存档回调验证")
    logger.info("  POST /wework/archive     - 存档消息接收")
    logger.info("  GET  /api/messages       - 查询消息")
    logger.info("  GET  /api/stats          - 获取统计")
    logger.info("  GET  /health             - 整合服务健康检查")
    logger.info("  GET  /archive/health     - 存档服务健康检查")
    logger.info("  GET  /archive/stats      - 存档统计信息")
    logger.info("  POST /debug/signature    - 调试签名验证")
    logger.info("=" * 60)
    logger.info("等待企业微信请求...")
    
    app.run(host='0.0.0.0', port=8400, debug=False)