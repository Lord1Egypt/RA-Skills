#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import time
import requests
import paho.mqtt.client as mqtt
import threading
import pyaudio
import os
import sys
from colorama import init, Fore, Back, Style

# 初始化colorama
init()

# 检查opus.dll
def check_opus_dll():
    system32_path = os.path.join(os.environ['SystemRoot'], 'System32', 'opus.dll')
    if not os.path.exists(system32_path):
        print(f"{COLORS['ERROR']}错误：未找到opus.dll文件！{COLORS['RESET']}")
        print(f"{COLORS['SYSTEM_STATUS']}请将opus.dll文件复制到 C:\\Windows\\System32 目录下{COLORS['RESET']}")
        print(f"{COLORS['SYSTEM_STATUS']}下载地址：https://github.com/QiKeO/py-xiaozhi{COLORS['RESET']}")
        return False
    return True

# 在其他import之前先检查opus.dll
if sys.platform == 'win32' and not check_opus_dll():
    sys.exit(1)

import opuslib
import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom, path
import logging
from pynput import keyboard as pynput_keyboard
import uuid

# 颜色常量定义
COLORS = {
    'USER_INPUT': Fore.GREEN,
    'SYSTEM_STATUS': Fore.LIGHTBLACK_EX,
    'AI_RESPONSE': Fore.BLUE,
    'ERROR': Fore.RED,
    'RESET': Style.RESET_ALL
}

# 状态图标
ICONS = {
    'RECORDING': '🎤',
    'THINKING': '💭',
    'PLAYING': '▶️',
    'PAUSED': '⏸️',
    'RECOGNIZED': '✓',
    'AI': '🤖'
}

def get_or_create_device_id():
    """获取或创建设备唯一标识"""
    config_file = 'device_config.json'
    if path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config['device_id'], config['mac_addr']
    
    # 生成新的设备ID和MAC地址
    device_id = str(uuid.uuid4())
    mac_parts = [format(uuid.uuid4().int >> i & 0xFF, '02x') for i in (40, 32, 24, 16, 8, 0)]
    mac_addr = ':'.join(mac_parts)
    
    # 保存配置
    config = {'device_id': device_id, 'mac_addr': mac_addr}
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    return device_id, mac_addr

# 获取设备唯一标识
DEVICE_ID, MAC_ADDR = get_or_create_device_id()

OTA_VERSION_URL = 'https://api.tenclass.net/xiaozhi/ota/'
mqtt_info = {}
aes_opus_info = {
    "type": "hello",
    "version": 3,
    "transport": "udp",
    "udp": {
        "server": "120.24.160.13",
        "port": 8884,
        "encryption": "aes-128-ctr",
        "key": urandom(16).hex(),  # 生成随机密钥
        "nonce": urandom(16).hex()  # 生成随机nonce
    },
    "audio_params": {
        "format": "opus",
        "sample_rate": 24000,
        "channels": 1,
        "frame_duration": 60
    },
    "session_id": str(uuid.uuid4())  # 生成唯一会话ID
}

local_sequence = 0
listen_state = None
tts_state = None
key_state = None
audio = None
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn_state = False
recv_audio_thread = threading.Thread()
send_audio_thread = threading.Thread()
mqttc = None


def get_ota_version():
    global mqtt_info
    header = {
        'Device-Id': MAC_ADDR,
        'Content-Type': 'application/json'
    }
    post_data = {"flash_size": 16777216, "minimum_free_heap_size": 8318916, "mac_address": f"{MAC_ADDR}",
                 "chip_model_name": "esp32s3", "chip_info": {"model": 9, "cores": 2, "revision": 2, "features": 18},
                 "application": {"name": "xiaozhi", "version": "0.9.9", "compile_time": "Jan 22 2025T20:40:23Z",
                                 "idf_version": "v5.3.2-dirty",
                                 "elf_sha256": "22986216df095587c42f8aeb06b239781c68ad8df80321e260556da7fcf5f522"},
                 "partition_table": [{"label": "nvs", "type": 1, "subtype": 2, "address": 36864, "size": 16384},
                                     {"label": "otadata", "type": 1, "subtype": 0, "address": 53248, "size": 8192},
                                     {"label": "phy_init", "type": 1, "subtype": 1, "address": 61440, "size": 4096},
                                     {"label": "model", "type": 1, "subtype": 130, "address": 65536, "size": 983040},
                                     {"label": "storage", "type": 1, "subtype": 130, "address": 1048576,
                                      "size": 1048576},
                                     {"label": "factory", "type": 0, "subtype": 0, "address": 2097152, "size": 4194304},
                                     {"label": "ota_0", "type": 0, "subtype": 16, "address": 6291456, "size": 4194304},
                                     {"label": "ota_1", "type": 0, "subtype": 17, "address": 10485760,
                                      "size": 4194304}],
                 "ota": {"label": "factory"},
                 "board": {"type": "bread-compact-wifi", "ssid": "mzy", "rssi": -58, "channel": 6,
                           "ip": "192.168.124.38", "mac": "cc:ba:97:20:b4:bc"}}

    response = requests.post(OTA_VERSION_URL, headers=header, data=json.dumps(post_data))
    print('=========================')
    print(response.text)
    print('=========================')
    logging.info(f"get version: {response}")
    mqtt_info = response.json()['mqtt']
    print('===========mqtt_info0==============')
    print(mqtt_info)
    print('===========mqtt_info1==============')

def aes_ctr_encrypt(key, nonce, plaintext):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def aes_ctr_decrypt(key, nonce, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


def send_audio():
    global aes_opus_info, udp_socket, local_sequence, listen_state, audio
    key = aes_opus_info['udp']['key']
    nonce = aes_opus_info['udp']['nonce']
    server_ip = aes_opus_info['udp']['server']
    server_port = aes_opus_info['udp']['port']
    print('===========send_audio0==============')
    print(aes_opus_info)
    print('===========send_audio1==============')
    # 初始化Opus编码器
    encoder = opuslib.Encoder(16000, 1, opuslib.APPLICATION_AUDIO)
    # 打开麦克风流, 帧大小，应该与Opus帧大小匹配
    mic = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=960)
    try:
        while True:
            if listen_state == "stop":
                continue
                time.sleep(0.1)
            # 读取音频数据
            data = mic.read(960)
            # 编码音频数据
            encoded_data = encoder.encode(data, 960)
            # nonce插入data.size local_sequence_
            local_sequence += 1
            new_nonce = nonce[0:4] + format(len(encoded_data), '04x') + nonce[8:24] + format(local_sequence, '08x')
            # 加密数据，添加nonce
            encrypt_encoded_data = aes_ctr_encrypt(bytes.fromhex(key), bytes.fromhex(new_nonce), bytes(encoded_data))
            data = bytes.fromhex(new_nonce) + encrypt_encoded_data
            sent = udp_socket.sendto(data, (server_ip, server_port))
    except Exception as e:
        print(f"{COLORS['ERROR']}发送音频错误：{str(e)}{COLORS['RESET']}")
    finally:
        local_sequence = 0
        udp_socket = None
        # 关闭流和PyAudio
        mic.stop_stream()
        mic.close()


def recv_audio():
    global aes_opus_info, udp_socket, audio
    key = aes_opus_info['udp']['key']
    nonce = aes_opus_info['udp']['nonce']
    sample_rate = aes_opus_info['audio_params']['sample_rate']
    frame_duration = aes_opus_info['audio_params']['frame_duration']
    frame_num = int(frame_duration / (1000 / sample_rate))
    # 初始化Opus编码器
    decoder = opuslib.Decoder(sample_rate, 1)
    spk = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True, frames_per_buffer=frame_num)
    try:
        while True:
            data, server = udp_socket.recvfrom(4096)
            encrypt_encoded_data = data
            # 解密数据,分离nonce
            split_encrypt_encoded_data_nonce = encrypt_encoded_data[:16]
            split_encrypt_encoded_data = encrypt_encoded_data[16:]
            decrypt_data = aes_ctr_decrypt(bytes.fromhex(key),
                                           split_encrypt_encoded_data_nonce,
                                           split_encrypt_encoded_data)
            # 解码播放音频数据
            spk.write(decoder.decode(decrypt_data, frame_num))
    except Exception as e:
        print(f"{COLORS['ERROR']}接收音频错误：{str(e)}{COLORS['RESET']}")
    finally:
        udp_socket = None
        spk.stop_stream()
        spk.close()


def on_connect(client, userdata, flags, rs, pr):
    if rs != 0:  # 只在连接失败时显示错误
        print(f"{COLORS['ERROR']}❌ MQTT服务器连接失败，错误码：{rs}{COLORS['RESET']}")
        return
    
    # 订阅特定设备的主题
    subscribe_topic = f"{mqtt_info['subscribe_topic'].split('/')[0]}/p2p/GID_test@@@{MAC_ADDR.replace(':', '_')}"
    client.subscribe(subscribe_topic)


def on_message(client, userdata, message):
    global aes_opus_info, udp_socket, tts_state, recv_audio_thread, send_audio_thread
    msg = json.loads(message.payload)
    
    # 根据消息类型处理不同的显示效果
    if msg['type'] == 'stt':
        print(f"{COLORS['USER_INPUT']}{ICONS['RECOGNIZED']} 已识别：{msg['text']}{COLORS['RESET']}")
    
    elif msg['type'] == 'tts':
        tts_state = msg['state']  # 更新tts状态
        if msg['state'] == 'sentence_start':
            # 如果消息中包含验证码,添加控制台链接和重启提示
            if '验证码' in msg['text']:
                print(f"{COLORS['AI_RESPONSE']}{ICONS['AI']} 小优：{msg['text']}{COLORS['RESET']}")
                print(f"\n{COLORS['SYSTEM_STATUS']}📱 请访问控制台: https://xiaozhi.me/console/devices{COLORS['RESET']}")
                print(f"{COLORS['SYSTEM_STATUS']}✨ 完成设备添加后,请重启程序{COLORS['RESET']}\n")
            else:
                print(f"{COLORS['AI_RESPONSE']}{ICONS['AI']} 小优：{msg['text']}{COLORS['RESET']}")
        elif msg['state'] == 'start':
            print(f"{COLORS['SYSTEM_STATUS']}{ICONS['PLAYING']} 开始播放{COLORS['RESET']}")
        elif msg['state'] == 'stop':
            print(f"{COLORS['SYSTEM_STATUS']}{ICONS['PAUSED']} 播放结束{COLORS['RESET']}")
    
    elif msg['type'] == 'llm':
        if 'emotion' in msg:
            print(f"{COLORS['AI_RESPONSE']}{msg['text']} ({msg['emotion']}){COLORS['RESET']}")
    
    elif msg['type'] == 'hello':
        aes_opus_info = msg
        udp_socket.connect((msg['udp']['server'], msg['udp']['port']))
        
        if not recv_audio_thread.is_alive():
            recv_audio_thread = threading.Thread(target=recv_audio)
            recv_audio_thread.start()
        
        if not send_audio_thread.is_alive():
            send_audio_thread = threading.Thread(target=send_audio)
            send_audio_thread.start()
    
    elif msg['type'] == 'goodbye' and udp_socket and msg['session_id'] == aes_opus_info['session_id']:
        aes_opus_info['session_id'] = None


def push_mqtt_msg(message):
    global mqtt_info, mqttc
    mqttc.publish(mqtt_info['publish_topic'], json.dumps(message))


def on_space_key_press(event):
    global key_state, udp_socket, aes_opus_info, listen_state, conn_state
    if key_state == "press":
        return
    key_state = "press"
    print(f"{COLORS['SYSTEM_STATUS']}{ICONS['RECORDING']} 正在聆听...{COLORS['RESET']}")
    
    # 判断是否需要发送hello消息
    if conn_state is False or aes_opus_info['session_id'] is None:
        conn_state = True
        # 发送hello消息,建立udp连接
        hello_msg = {"type": "hello", "version": 3, "transport": "udp",
                     "audio_params": {"format": "opus", "sample_rate": 16000, "channels": 1, "frame_duration": 60}}
        push_mqtt_msg(hello_msg)
        print(f"{COLORS['SYSTEM_STATUS']}正在重新建立连接...{COLORS['RESET']}")
    
    if tts_state == "start" or tts_state == "sentence_start":
        # 在播放状态下发送abort消息
        push_mqtt_msg({"type": "abort"})
        print(f"{COLORS['SYSTEM_STATUS']}已中断当前播放{COLORS['RESET']}")
    
    if aes_opus_info['session_id'] is not None:
        # 发送start listen消息
        msg = {"session_id": aes_opus_info['session_id'], "type": "listen", "state": "start", "mode": "manual"}
        push_mqtt_msg(msg)


def on_space_key_release(event):
    global aes_opus_info, key_state
    key_state = "release"
    print(f"{COLORS['SYSTEM_STATUS']}{ICONS['THINKING']} 正在处理...{COLORS['RESET']}")
    
    # 发送stop listen消息
    if aes_opus_info['session_id'] is not None:
        msg = {"session_id": aes_opus_info['session_id'], "type": "listen", "state": "stop"}
        push_mqtt_msg(msg)


def on_press(key):
    if key == pynput_keyboard.Key.space:
        on_space_key_press(None)


def on_release(key):
    if key == pynput_keyboard.Key.space:
        on_space_key_release(None)
    # Stop listener
    if key == pynput_keyboard.Key.esc:
        print(f"\n{COLORS['SYSTEM_STATUS']}👋 感谢使用小优语音助手，再见！{COLORS['RESET']}")
        return False


def run():
    global mqtt_info, mqttc, audio
    
    # 显示欢迎信息
    print(f"\n{COLORS['AI_RESPONSE']}欢迎使用小优语音助手！{COLORS['RESET']}")
    print(f"{COLORS['SYSTEM_STATUS']}系统正在初始化...{COLORS['RESET']}")
    
    try:
        # 检查音频设备
        if audio.get_default_input_device_info() is None:
            print(f"{COLORS['ERROR']}错误：未检测到麦克风设备{COLORS['RESET']}")
            return
        if audio.get_default_output_device_info() is None:
            print(f"{COLORS['ERROR']}错误：未检测到扬声器设备{COLORS['RESET']}")
            return
            
        # 获取mqtt与版本信息
        print(f"{COLORS['SYSTEM_STATUS']}正在连接服务器...{COLORS['RESET']}")
        get_ota_version()
        
        # 监听键盘按键
        print(f"\n{COLORS['SYSTEM_STATUS']}✨ 系统已准备就绪！{COLORS['RESET']}")
        print(f"{COLORS['SYSTEM_STATUS']}📢 按住空格键开始对话，松开等待回复{COLORS['RESET']}")
        print(f"{COLORS['SYSTEM_STATUS']}❌ 按ESC键退出程序{COLORS['RESET']}\n")
        
        listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        
        # 创建MQTT客户端
        mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=mqtt_info['client_id'])
        mqttc.username_pw_set(username=mqtt_info['username'], password=mqtt_info['password'])
        mqttc.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=mqtt.ssl.CERT_REQUIRED,
                      tls_version=mqtt.ssl.PROTOCOL_TLS, ciphers=None)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        
        try:
            mqttc.connect(host=mqtt_info['endpoint'], port=8883)
            mqttc.loop_forever()
        except Exception as e:
            print(f"{COLORS['ERROR']}MQTT连接错误：{str(e)}{COLORS['RESET']}")
            
    except KeyboardInterrupt:
        print(f"\n{COLORS['SYSTEM_STATUS']}👋 感谢使用小优语音助手，再见！{COLORS['RESET']}")
    except Exception as e:
        print(f"{COLORS['ERROR']}系统错误：{str(e)}{COLORS['RESET']}")
    finally:
        if audio:
            audio.terminate()


if __name__ == "__main__":
    try:
        audio = pyaudio.PyAudio()
        run()
    except Exception as e:
        print(f"{COLORS['ERROR']}程序启动失败：{str(e)}{COLORS['RESET']}")
    finally:
        if audio:
            audio.terminate()