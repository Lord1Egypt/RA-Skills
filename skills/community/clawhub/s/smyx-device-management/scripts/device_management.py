#!/usr/bin/env python3
"""
设备管理脚本
功能：设备增删改查、直播流地址获取、状态监控
"""
import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, parent_dir)

import argparse
import json
import yaml
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from skills.smyx_common.scripts import CommonUtil
# 添加脚本目录到路径
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, SCRIPT_DIR)

# 添加根目录到路径
# root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# if root_dir not in sys.path:
#     sys.path.insert(0, root_dir)

from .api_service import ApiService
from .config import *
from .skill import Skill

from skills.smyx_common.scripts.util import RequestUtil
from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

# 配置文件路径
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.yaml")

# 默认配置
DEFAULT_CONFIG = {
    "devices": [],
    "stream_server": "https://stream.example.com",
    "stream_expire_hours": 24
}


def load_config() -> Dict:
    """加载配置文件"""
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, allow_unicode=True)
        return DEFAULT_CONFIG

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or DEFAULT_CONFIG


def save_config(config: Dict) -> None:
    """保存配置文件"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


def generate_device_id() -> str:
    """生成设备ID"""
    return str(uuid.uuid4())[:8]


def generate_stream_url(device: Dict, protocol: str = "m3u8", config: Dict = None) -> str:
    """生成直播流地址"""
    config = config or load_config()
    stream_server = config.get("stream_server", "https://stream.example.com")

    # 模拟流地址生成，实际使用时替换为真实的流媒体API调用
    expire_time = datetime.now() + timedelta(hours=config.get("stream_expire_hours", 24))
    expire_ts = int(expire_time.timestamp())

    if protocol == "m3u8":
        return f"{stream_server}/live/{device['id']}.m3u8?expire={expire_ts}&sign=xxxxxx"
    elif protocol == "flv":
        return f"{stream_server}/live/{device['id']}.flv?expire={expire_ts}&sign=xxxxxx"
    elif protocol == "rtmp":
        return f"rtmp://{stream_server.replace('https://', '').replace('http://', '')}/live/{device['id']}?expire={expire_ts}&sign=xxxxxx"
    else:
        return f"{stream_server}/live/{device['id']}?protocol={protocol}&expire={expire_ts}&sign=xxxxxx"


def list_devices() -> List[Dict]:
    """列出所有设备"""
    config = load_config()
    return config.get("devices", [])


def add_device(name: str, type: str, ip: str, username: Optional[str] = None,
               password: Optional[str] = None, **kwargs) -> Dict:
    """添加设备"""
    config = load_config()
    # 确保devices字段存在
    if "devices" not in config:
        config["devices"] = []

    device = {
        "id": generate_device_id(),
        "name": name,
        "type": type,
        "ip": ip,
        "username": username,
        "password": password,
        "status": "online",  # 初始状态设为在线，实际使用时可添加状态检测
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        **kwargs
    }

    config["devices"].append(device)
    save_config(config)
    return device


def get_device(device_id: str) -> Optional[Dict]:
    """获取设备详情"""
    config = load_config()
    for device in config.get("devices", []):
        if device["id"] == device_id:
            return device
    return None


def update_device(device_id: str, **kwargs) -> Optional[Dict]:
    """更新设备信息"""
    config = load_config()
    for i, device in enumerate(config.get("devices", [])):
        if device["id"] == device_id:
            config["devices"][i].update(kwargs)
            config["devices"][i]["updated_at"] = datetime.now().isoformat()
            save_config(config)
            return config["devices"][i]
    return None


def delete_device(device_id: str) -> bool:
    """删除设备"""
    config = load_config()
    original_length = len(config.get("devices", []))
    config["devices"] = [d for d in config.get("devices", []) if d["id"] != device_id]

    if len(config["devices"]) < original_length:
        save_config(config)
        return True
    return False


def get_stream_url(device_id: str, protocol: str = "m3u8") -> Optional[Dict]:
    """获取设备直播流地址"""
    device = get_device(device_id)
    if not device:
        return None

    config = load_config()
    stream_url = generate_stream_url(device, protocol, config)
    expire_time = datetime.now() + timedelta(hours=config.get("stream_expire_hours", 24))

    return {
        "device_id": device_id,
        "device_name": device["name"],
        "protocol": protocol,
        "stream_url": stream_url,
        "expire_at": expire_time.isoformat(),
        "expire_timestamp": int(expire_time.timestamp())
    }


def format_devices_table(devices: List[Dict]) -> str:
    if not devices:
        return "暂无任何设备"
    return f"""
设备列表的json结构化数据如下(id=记录唯一标识,cameraSn=摄像头序列号,cameraName=摄像头名称,cameraType=摄像头牌子,createTimeString=注册时间,online=设备是否在线,hlsUrl=m3u8流地址,flvUrl=flv流地址):
{devices}
"""


def format_stream_result(stream_info: Dict) -> str:
    """格式化直播流结果"""
    return f"""
📹 **{stream_info['device_name']} 实时画面**
- 流格式：{stream_info['protocol'].upper()}
- 播放地址：[▶️ 点击播放]({stream_info['stream_url']})
- 有效期：{stream_info['expire_at']}
- 提示：复制地址到支持{stream_info['protocol'].upper()}的播放器即可播放，或点击链接直接在浏览器中观看
"""


async def main():
    parser = argparse.ArgumentParser(description="设备管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 列出设备
    list_parser = subparsers.add_parser("list", help="列出所有设备")
    list_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")

    # 添加设备
    add_parser = subparsers.add_parser("add", help="添加设备")
    add_parser.add_argument("--sn", required=True, help="设备序列号")
    add_parser.add_argument("--name", required=True, help="设备名称")
    add_parser.add_argument("--type", help="设备牌子 (大华/海康/宇视/探鸽等)")
    add_parser.add_argument("--scode", help="设备安全码")
    add_parser.add_argument("--scene-code", help="设备场景码")
    add_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    add_parser.add_argument("--ip", help="设备IP地址")
    add_parser.add_argument("--username", help="设备登录用户名")
    add_parser.add_argument("--password", help="设备登录密码")
    add_parser.add_argument("--location", help="设备位置")

    # 获取设备详情
    get_parser = subparsers.add_parser("get", help="获取设备详情")
    get_parser.add_argument("--id", required=True, help="设备ID")
    get_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")

    # 更新设备
    update_parser = subparsers.add_parser("update", help="更新设备信息")
    # update_parser.add_argument("--id", required=True, help="设备ID")
    update_parser.add_argument("--sn", required=True, help="设备序列号")
    update_parser.add_argument("--name", required=True, help="新的设备名称")
    update_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    # update_parser.add_argument("--ip", help="新的IP地址")
    # update_parser.add_argument("--username", help="新的用户名")
    # update_parser.add_argument("--password", help="新的密码")
    # update_parser.add_argument("--status", choices=["online", "offline"], help="设备状态")

    # 删除设备
    delete_parser = subparsers.add_parser("delete", help="删除设备")
    # delete_parser.add_argument("--id", required=True, help="设备ID")
    delete_parser.add_argument("--sn", required=True, help="设备序列号")
    delete_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")

    # 获取直播流
    stream_parser = subparsers.add_parser("stream", help="获取设备直播流地址")
    # stream_parser.add_argument("--id", help="设备ID")
    stream_parser.add_argument("--sn", required=True, help="设备序列号")
    stream_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    # stream_parser.add_argument("--protocol", choices=["m3u8", "flv", "rtmp"], default="m3u8",
    #                            help="流协议 (默认: m3u8)")

    # 设备控制：云台转动、音频开关
    control_parser = subparsers.add_parser("control", help="设备远程控制（云台转动/音频开关）")
    control_parser.add_argument("--sn", required=True, help="设备序列号")
    control_parser.add_argument("--direction", choices=["up", "down", "left", "right", "reset"],
                                help="控制选项：up/down/left/right/reset 控制云台转动方向")
    control_parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    control_parser.add_argument("--speed", type=int, default=5, choices=range(1, 11),
                                help="云台转动速度 1-10 (默认: 5)，仅对云台转动有效")
    control_parser.add_argument("--sound", type=str, choices=["on", "off"],
                                help="开启/关闭声音，仅对sound控制有效")

    args = parser.parse_args()

    skill = Skill()

    api_service = ApiService.get_instance()

    try:
        if "open_id" in args:
            ConstantEnumBase.CURRENT__OPEN_ID = args.open_id

        if args.command == "list":
            devices = await skill.list()
            print(format_devices_table(devices))

        elif args.command == "add":
            def getQrCode():
                return f"https://service.dahuatech.com?cn=m&sn={camera_sn}&dt=DH-IPC-H4AC&sc={camera_scode}"

            camera_sn = args.sn
            camera_scode = args.scode
            camera_name = args.name
            scene_code = ConstantEnum.SceneCodeEnum.PUBLIC_AREA_AI_ANALYSIS.value if args.scene_code and "展厅" in args.scene_code else args.scene_code
            camera_type = "TAN_GE" if args.type == "探鸽" else "DA_HUA"
            qr_code = getQrCode()
            device = {
                "cameraSn": camera_sn,
                "cameraName": camera_name,
                "cameraType": camera_type,
                "daHua": {"qrCode":
                              qr_code
                          },
                "appCategory": "XIAN_ZHAO_GAN_ZHI",
            }
            if scene_code:
                device["sceneCodes"] = [scene_code]
            device = skill.add(device) or device
            print(f"✅ 设备添加成功：\n{format_devices_table([device])}")

        elif args.command == "get":
            device = get_device(args.id)
            if device:
                print(f"📋 设备详情：\n{json.dumps(device, indent=2, ensure_ascii=False)}")
            else:
                print("❌ 设备不存在")

        elif args.command == "update":
            camera_sn = args.sn
            camera_name = args.name
            device = {
                "cameraSn": camera_sn,
                "newCameraName": camera_name,
            }
            device = skill.edit(device) or device
            print(f"✅ 设备更新成功：\n{format_devices_table([device])}")

        elif args.command == "delete":
            camera_sn = args.sn
            print("will delete camerasn:", camera_sn)
            skill.delete(camera_sn)
            print("✅ 设备删除成功")

        elif args.command == "stream":
            stream_info = get_stream_url(args.id, args.protocol)
            if stream_info:
                print(format_stream_result(stream_info))
            else:
                print("❌ 设备不存在")

        elif args.command == "control":
            camera_sn = args.sn
            direction_type = args.direction
            sound_type = args.sound

            if direction_type in ["up", "down", "left", "right", "reset"]:
                # 云台控制
                speed = args.speed if "speed" in args else 5
                print(f"🔧 正在控制设备 {camera_sn} 云台向 {direction_type} 转动，速度 {speed}...")
                api_service.control_ptz(camera_sn, direction_type, speed)
                print(f"✅ 云台{direction_type}转动控制成功")

            elif sound_type:
                enable = sound_type == "on"
                status_text = "开启" if enable else "关闭"
                print(f"🔧 正在控制设备 {camera_sn} {status_text}声音侦听...")
                api_service.control_audio(camera_sn, enable)
                print(f"✅ 声音{status_text}成功")

    except Exception as e:
        CommonUtil.trace_exception_stack(e)
        print("❌ 设备操作失败")


if __name__ == "__main__":
    asyncio.run(main())
