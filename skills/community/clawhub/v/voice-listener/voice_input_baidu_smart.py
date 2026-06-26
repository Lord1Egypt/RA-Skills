#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音输入助手 - 百度语音识别 + 智能唤醒
唤醒词: "小龙虾" - 进入激活模式
停止词: "停止" - 回到待机模式

工作流程:
1. 待机模式：持续监听，只识别包含"小龙虾"的语音
2. 检测到"小龙虾" → 进入激活模式
3. 激活模式：持续监听，所有语音都会输入
4. 检测到"停止" → 回到待机模式
"""

import sys
import io
import json
import time
import base64
import os
import tempfile

# 强制不缓冲输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

# 打印并立即刷新
def print_flush(msg):
    print(msg)
    sys.stdout.flush()

print_flush("=" * 60)
print_flush("语音输入助手 - 百度语音识别 + 智能唤醒")
print_flush("=" * 60)

try:
    import sounddevice as sd
    import numpy as np
    import queue
    import keyboard
    import pyperclip
    from datetime import datetime
    import requests

    print_flush("\n🎤 正在初始化系统...")

    # 配置
    SAMPLE_RATE = 16000  # 百度要求16kHz
    CHANNELS = 1
    CHUNK_SIZE = 1024
    SILENCE_THRESHOLD = 0.02
    SILENCE_DURATION = 1.5
    MIN_SPEECH_DURATION = 0.5

    # 唤醒词和停止词
    WAKE_WORD = "小龙虾"
    STOP_WORD = "停止"

    WORKSPACE = 'C:\\Users\\11666\\.openclaw\\workspace'

    # 百度配置
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(skill_dir, 'baidu_config.json')

    # 读取百度配置
    print_flush("📖 读取百度配置...")
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        APP_ID = config['APP_ID']
        API_KEY = config['API_KEY']
        SECRET_KEY = config['SECRET_KEY']

        print_flush("✅ 百度配置加载完成\n")

    except FileNotFoundError:
        print_flush(f"\n❌ 找不到配置文件: {CONFIG_FILE}")
        print_flush("请确保 baidu_config.json 在当前目录下")
        input("\n按 Enter 退出...")
        sys.exit(1)

    except json.JSONDecodeError:
        print_flush(f"\n❌ 配置文件格式错误: {CONFIG_FILE}")
        print_flush("请检查JSON格式是否正确")
        input("\n按 Enter 退出...")
        sys.exit(1)

    except KeyError as e:
        print_flush(f"\n❌ 配置文件缺少必要字段: {e}")
        print_flush("请确保包含: APP_ID, API_KEY, SECRET_KEY")
        input("\n按 Enter 退出...")
        sys.exit(1)

    # 创建音频队列
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        """音频回调函数"""
        if status:
            print_flush(f"音频状态: {status}")
        audio_queue.put(indata.copy())

    # 创建音频流
    print_flush("创建音频流...")
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=audio_callback,
        blocksize=CHUNK_SIZE
    )

    print_flush("启动音频流...")
    stream.start()

    print_flush("✅ 音频系统已启动\n")

    # 获取百度Access Token
    def get_baidu_token():
        """获取百度Access Token"""
        try:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": API_KEY,
                "client_secret": SECRET_KEY
            }

            response = requests.post(url, params=params, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if 'access_token' in result:
                    return result['access_token']
                else:
                    print_flush(f"❌ 获取Token失败: {result.get('error_description', '未知错误')}")
                    return None
            else:
                print_flush(f"❌ HTTP错误: {response.status_code}")
                return None

        except Exception as e:
            print_flush(f"❌ 获取Token错误: {e}")
            return None

    # 获取Token
    print_flush("🔐 获取百度Access Token...")
    ACCESS_TOKEN = get_baidu_token()

    if not ACCESS_TOKEN:
        print_flush("\n❌ 无法获取百度Access Token，请检查API密钥是否正确")
        input("\n按 Enter 退出...")
        sys.exit(1)

    print_flush(f"✅ Token获取成功\n")

    # 百度语音识别
    def recognize_speech_baidu(audio_data):
        """百度语音识别"""
        try:
            # 转换音频为int16
            audio_int16 = (audio_data * 32767).astype(np.int16)

            # 保存为临时WAV文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name

            try:
                import wave
                with wave.open(temp_filename, 'wb') as wav_file:
                    wav_file.setnchannels(CHANNELS)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(SAMPLE_RATE)
                    wav_file.writeframes(audio_int16.tobytes())

                # 读取音频文件
                with open(temp_filename, 'rb') as f:
                    audio_content = f.read()

                # Base64编码音频
                audio_base64 = base64.b64encode(audio_content).decode('utf-8')

                # 构建请求
                url = f"https://vop.baidu.com/server_api"
                params = {
                    "dev_pid": 1537,  # 普通话（支持简单的英文识别）
                    "format": "wav",
                    "rate": SAMPLE_RATE,
                    "token": ACCESS_TOKEN,
                    "cuid": APP_ID,
                    "channel": 1,
                    "speech": audio_base64,
                    "len": len(audio_content)
                }

                # 发送POST请求
                headers = {
                    "Content-Type": "application/json"
                }

                response = requests.post(url, json=params, headers=headers, timeout=10)

                if response.status_code == 200:
                    result = response.json()

                    if result.get('err_no') == 0:
                        # 提取识别文本
                        if 'result' in result and len(result['result']) > 0:
                            text = result['result'][0]
                            return text
                        else:
                            return None
                    else:
                        print_flush(f"❌ API错误: {result.get('err_msg', '未知错误')}")
                        return None
                else:
                    print_flush(f"❌ HTTP错误: {response.status_code}")
                    return None

            finally:
                # 删除临时文件
                try:
                    os.unlink(temp_filename)
                except:
                    pass

        except Exception as e:
            print_flush(f"❌ 识别错误: {e}")
            return None

    def auto_input(text):
        """自动输入文字到输入框"""
        try:
            # 复制到剪贴板
            pyperclip.copy(text)
            time.sleep(0.1)

            # 模拟 Ctrl+V 粘贴
            keyboard.press('ctrl')
            keyboard.press('v')
            time.sleep(0.05)
            keyboard.release('v')
            keyboard.release('ctrl')

            print_flush(f"✅ 已输入: {text}\n")

        except Exception as e:
            print_flush(f"❌ 自动输入失败: {e}")
            print_flush(f"💡 文字已复制到剪贴板，请手动按 Ctrl+V 粘贴\n")

    print_flush("=" * 60)
    print_flush("语音输入助手 - 智能唤醒模式")
    print_flush("=" * 60)
    print_flush(f"\n💡 使用方法：")
    print_flush(f"")
    print_flush(f"📌 待机模式（当前）:")
    print_flush(f"   只识别包含'{WAKE_WORD}'的语音")
    print_flush(f"   说: '{WAKE_WORD}' → 进入激活模式")
    print_flush(f"")
    print_flush(f"📌 激活模式:")
    print_flush(f"   所有语音都会自动输入")
    print_flush(f"   说: '{STOP_WORD}' → 回到待机模式")
    print_flush(f"")
    print_flush(f"📌 示例:")
    print_flush(f"   1. 说: '{WAKE_WORD}'")
    print_flush(f"   2. 说: '你好' → 自动输入")
    print_flush(f"   3. 说: '帮我打开淘宝' → 自动输入")
    print_flush(f"   4. 说: '{STOP_WORD}' → 停止输入")
    print_flush(f"")
    print_flush(f"🚪 按 Ctrl+C 停止监听\n")

    audio_buffer = []
    silence_count = 0
    max_silence_count = int(SAMPLE_RATE * SILENCE_DURATION / CHUNK_SIZE)
    speech_detected = False
    is_activated = False  # 是否激活

    try:
        while True:
            try:
                data = audio_queue.get(timeout=0.1)
                volume = np.abs(data).mean()

                if volume > SILENCE_THRESHOLD:
                    if not speech_detected:
                        speech_detected = True
                        audio_buffer.append(data)
                        silence_count = 0

                    else:
                        audio_buffer.append(data)
                        silence_count = 0

                elif speech_detected:
                    audio_buffer.append(data)
                    silence_count += 1

                    if silence_count >= max_silence_count:
                        if audio_buffer:
                            total_audio = np.concatenate(audio_buffer)
                            duration = len(total_audio) / SAMPLE_RATE

                            if duration > MIN_SPEECH_DURATION:
                                print_flush(f"🎤 录音完成: {duration:.2f}秒")
                                print_flush(f"🔄 正在识别...")

                                # 识别语音
                                text = recognize_speech_baidu(total_audio)

                                if text:
                                    print_flush(f"✅ 识别结果: {text}")

                                    if not is_activated:
                                        # 待机模式：检查唤醒词
                                        if WAKE_WORD in text:
                                            is_activated = True
                                            print_flush(f"✨ 进入激活模式！")
                                            print_flush(f"💡 现在所有语音都会自动输入")
                                            print_flush(f"💡 说'{STOP_WORD}'可以停止\n")

                                            # 如果唤醒词后面还有内容，也输入
                                            command_text = text.replace(WAKE_WORD, '').strip()
                                            if command_text:
                                                print_flush(f"⌨️  输入: {command_text}")
                                                auto_input(command_text)

                                        else:
                                            # 没有唤醒词，忽略
                                            print_flush(f"❌ 未检测到唤醒词: '{WAKE_WORD}'")
                                            print_flush(f"💡 忽略，继续待机...\n")

                                    else:
                                        # 激活模式：检查停止词
                                        if STOP_WORD in text:
                                            is_activated = False
                                            print_flush(f"🛑 停止激活模式！")
                                            print_flush(f"💡 回到待机模式")
                                            print_flush(f"💡 说'{WAKE_WORD}'可以再次激活\n")

                                        else:
                                            # 普通指令，直接输入
                                            print_flush(f"⌨️  正在输入...")
                                            auto_input(text)

                                print_flush(f"\n👂 继续监听...\n")

                        audio_buffer = []
                        speech_detected = False
                        silence_count = 0

            except queue.Empty:
                continue

    except KeyboardInterrupt:
        print_flush(f"\n\n[{datetime.now().strftime('%H:%M:%S')}] 停止监听")

    finally:
        stream.stop()
        stream.close()
        print_flush("麦克风已关闭")

except ImportError as e:
    print_flush(f"\n❌ 缺少必要的库: {e}")
    print_flush("请安装: pip install sounddevice numpy keyboard pyperclip requests")
except Exception as e:
    print_flush(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print_flush("\n程序已退出")
input("按 Enter 退出...")