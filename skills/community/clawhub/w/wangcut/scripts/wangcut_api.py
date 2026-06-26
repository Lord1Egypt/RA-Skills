#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
秦丝智能视频剪辑APP API客户端
支持创建视频剪辑任务、查看任务状态、下载视频等功能
"""

import hashlib
import json
import random
import time
import uuid
import configparser
import os
import urllib.parse
import requests
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta


# 语音类型友好名称映射
VOICE_TYPE_MAP = {
    'f_liuyuxi_20251009': '刘雨希',
    'f_xinjie_20251011_1': '欣姐(真诚大姐)',
    'f_zhaotang_20251103_3': '赵棠',
    'f_yunqi_20251018': '云起',
    'f_yena_20251009': '耶娜',
}


def get_voice_name(voice_type: str) -> str:
    """获取语音类型的友好名称"""
    return VOICE_TYPE_MAP.get(voice_type, voice_type)


def _find_config_path(config_path: str = None) -> str:
    """
    查找配置文件路径，按优先级搜索：
    1. 指定的路径
    2. 当前工作目录
    3. skill脚本所在目录
    4. 项目根目录
    """
    if config_path and os.path.exists(config_path):
        return config_path

    # 可能的配置文件位置
    script_dir = Path(__file__).parent
    possible_paths = [
        Path.cwd() / "config.ini",
        script_dir.parent.parent.parent.parent / "config.ini",  # 项目根目录
        script_dir / "config.ini",
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    # 返回默认路径（用于创建新配置）
    return str(Path.cwd() / "config.ini")


# 配置状态常量
class ConfigStatus:
    OK = 'ok'                           # 配置正常
    NOT_FOUND = 'not_found'             # 配置文件不存在
    MISSING_CREDENTIALS = 'missing'     # 账号密码未配置
    INVALID_CREDENTIALS = 'invalid'     # 账号密码无效


def check_config(config_path: str = None) -> tuple:
    """
    检查配置状态

    Args:
        config_path: 配置文件路径（可选）

    Returns:
        (状态码, 状态描述, 配置文件路径)
    """
    actual_path = _find_config_path(config_path)

    # 检查文件是否存在
    if not os.path.exists(actual_path):
        return (ConfigStatus.NOT_FOUND,
                "配置文件不存在，请提供秦丝旺剪账号密码进行配置",
                actual_path)

    # 读取配置
    config = configparser.ConfigParser()
    config.read(actual_path, encoding='utf-8')

    # 检查账号密码
    username = config.get('wangcut', 'username', fallback='')
    password = config.get('wangcut', 'password', fallback='')

    if not username or not password:
        return (ConfigStatus.MISSING_CREDENTIALS,
                "账号密码未配置，请提供秦丝旺剪账号密码",
                actual_path)

    return (ConfigStatus.OK,
            "配置正常",
            actual_path)


def setup_config(username: str, password: str, config_path: str = None,
                 folder_id: str = '', base_url: str = None) -> str:
    """
    配置账号密码，自动创建或更新 config.ini

    Args:
        username: 手机号
        password: 密码（明文，会自动MD5加密存储）
        config_path: 配置文件路径（可选）
        folder_id: 素材文件夹ID（可选）
        base_url: API地址（可选）

    Returns:
        配置文件路径
    """
    actual_path = _find_config_path(config_path)

    config = configparser.ConfigParser()

    # 如果文件存在，先读取现有配置
    if os.path.exists(actual_path):
        config.read(actual_path, encoding='utf-8')

    # 更新账号配置
    if not config.has_section('wangcut'):
        config.add_section('wangcut')

    config.set('wangcut', 'username', username)
    config.set('wangcut', 'password', password)
    config.set('wangcut', 'base_url', base_url or config.get('wangcut', 'base_url', fallback='https://cloud.qinsilk.com/aicut/api/v1'))
    config.set('wangcut', 'folder_id', folder_id or config.get('wangcut', 'folder_id', fallback=''))
    config.set('wangcut', 'download_dir', config.get('wangcut', 'download_dir', fallback='./downloads'))

    # 如果没有 task_defaults 节，添加默认值
    if not config.has_section('task_defaults'):
        config.add_section('task_defaults')
        config.set('task_defaults', 'voice_type', 'f_liuyuxi_20251009')
        config.set('task_defaults', 'voice_speed', '1.3')
        config.set('task_defaults', 'voice_pitch', '1.0')
        config.set('task_defaults', 'resolution_width', '1080')
        config.set('task_defaults', 'resolution_height', '1920')
        config.set('task_defaults', 'subtitle_enabled', 'true')
        config.set('task_defaults', 'subtitle_font_size', '90')
        config.set('task_defaults', 'subtitle_font_color', 'yellow')
        config.set('task_defaults', 'subtitle_font', '江城律动宋')
        config.set('task_defaults', 'subtitle_position', '0.7')
        config.set('task_defaults', 'music_enabled', 'true')
        config.set('task_defaults', 'music_name', '夏季有你')
        config.set('task_defaults', 'music_volume', '0.4')

    # 写入配置文件
    with open(actual_path, 'w', encoding='utf-8') as f:
        config.write(f)

    return actual_path


def is_configured() -> bool:
    """检查是否已配置账号密码"""
    status, _, _ = check_config()
    return status == ConfigStatus.OK


def get_config_status_message() -> str:
    """获取配置状态消息（用于提示用户）"""
    status, message, path = check_config()
    if status == ConfigStatus.OK:
        return "✅ 旺剪账号已配置"
    else:
        return f"⚠️ {message}\n请提供账号密码，格式：账号 158xxx 密码 xxx"


class WangcutAPI:
    """秦丝智能视频剪辑API客户端"""

    def __init__(self, config_path: str = None, verify_config: bool = True):
        """
        初始化API客户端

        Args:
            config_path: 配置文件路径（可选，自动查找）
            verify_config: 是否检查配置状态（默认True）
        """
        self.config_path = _find_config_path(config_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding='utf-8')

        self.base_url = self.config.get('wangcut', 'base_url', fallback='https://cloud.qinsilk.com/aicut/api/v1')
        self.username = self.config.get('wangcut', 'username', fallback='')
        self.password = self.config.get('wangcut', 'password', fallback='')
        self.folder_id = self.config.get('wangcut', 'folder_id', fallback='')

        # 检查配置状态
        self._config_status = None
        if verify_config:
            self._config_status = check_config(self.config_path)
            if self._config_status[0] != ConfigStatus.OK:
                # 配置异常，打印提示
                print(f"⚠️ 旺剪配置异常: {self._config_status[1]}")
                print("请提供账号密码进行配置，格式：账号 158xxx 密码 xxx")

        self.access_token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.cid: Optional[int] = None

        # 请求头模板
        self.headers_template = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'content-type': 'application/json;charset=UTF-8',
            'x-app-version': '1.7.1_5',
            'x-client-type': 'app',
        }

        self._session = requests.Session()

    def _generate_device_id(self) -> str:
        """生成设备ID"""
        return str(random.randint(10**18, 10**19 - 1))

    def _generate_request_id(self) -> str:
        """生成请求ID"""
        timestamp = int(time.time() * 1000)
        random_str = uuid.uuid4().hex[:10]
        return f"{timestamp}-{random_str}"

    def _get_device_info(self) -> str:
        """获取设备信息JSON字符串"""
        device_info = {
            "platform": "ios",
            "system": "iOS 18.5",
            "version": "",
            "model": "iPhone",
            "pixelRatio": 3,
            "screenWidth": 390,
            "screenHeight": 844,
            "windowWidth": 390,
            "windowHeight": 844,
            "statusBarHeight": 0,
            "safeArea": {"left": 0, "right": 390, "top": 0, "bottom": 844, "width": 390, "height": 844},
            "safeAreaInsets": {"top": 0, "right": 0, "bottom": 0, "left": 0},
            "deviceId": self._generate_device_id(),
            "deviceType": "phone",
            "deviceModel": "iPhone"
        }
        return json.dumps(device_info)

    def _get_headers(self, with_auth: bool = True) -> Dict[str, str]:
        """
        获取请求头

        Args:
            with_auth: 是否包含认证信息

        Returns:
            请求头字典
        """
        headers = self.headers_template.copy()
        headers['x-device-info'] = self._get_device_info()
        headers['x-request-id'] = self._generate_request_id()

        if with_auth and self.access_token:
            headers['authorization'] = f'Bearer {self.access_token}'
            headers['x-cid'] = str(self.cid)
            headers['x-uid'] = str(self.user_id)
        else:
            headers['x-cid'] = '0'
            headers['x-uid'] = '0'

        return headers

    def _md5_password(self, password: str) -> str:
        """
        将密码进行MD5加密并转大写

        Args:
            password: 原始密码

        Returns:
            MD5加密后的大写字符串
        """
        return hashlib.md5(password.encode('utf-8')).hexdigest().upper()

    def login(self) -> Dict[str, Any]:
        """
        登录API

        Returns:
            登录响应数据

        Raises:
            Exception: 登录失败时抛出异常，包含配置提示
        """
        # 检查账号密码是否已配置
        if not self.username or not self.password:
            raise Exception(
                "❌ 旺剪账号密码未配置！\n"
                "请提供账号密码进行配置，格式：账号 158xxx 密码 xxx\n"
                "或说：配置旺剪账号"
            )

        url = f"{self.base_url}/auth/login"
        headers = self._get_headers(with_auth=False)
        data = {
            "username": self.username,
            "password": self._md5_password(self.password)
        }

        try:
            response = self._session.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            if result.get('status_code') == 1:
                data = result.get('data', {})
                self.access_token = data.get('access_token')
                self.user_id = data.get('user_id')
                self.cid = data.get('cid')
                print(f"登录成功! 用户: {data.get('nickname', self.username)}")
            else:
                error_msg = result.get('message', '未知错误')
                # 登录失败，提示用户重新配置
                raise Exception(
                    f"❌ 登录失败: {error_msg}\n"
                    "请检查账号密码是否正确，或重新配置：\n"
                    "格式：账号 158xxx 密码 xxx"
                )

            return result

        except requests.exceptions.RequestException as e:
            raise Exception(f"❌ 网络请求失败: {e}")

    def ensure_login(self):
        """确保已登录"""
        if not self.access_token:
            self.login()

    def get_materials(self, page: int = 1, size: int = 18, material_type: str = 'video',
                      folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取素材列表

        Args:
            page: 页码
            size: 每页数量
            material_type: 素材类型 (video/image)
            folder_id: 文件夹ID

        Returns:
            素材列表响应数据
        """
        self.ensure_login()

        url = f"{self.base_url}/materials"
        params = {
            'page': page,
            'size': size,
            'material_type': material_type
        }
        if folder_id:
            params['folder_id'] = folder_id
        elif self.folder_id:
            params['folder_id'] = self.folder_id

        headers = self._get_headers()
        response = self._session.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()

        if result.get('status_code') != 1:
            raise Exception(f"获取素材列表失败: {result.get('message', '未知错误')}")

        return result

    def get_recent_materials(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        获取最近N个视频素材

        Args:
            count: 需要获取的素材数量

        Returns:
            素材列表
        """
        all_materials = []
        page = 1
        page_size = 50  # 每页最多50个

        while len(all_materials) < count:
            result = self.get_materials(page=page, size=page_size)
            items = result.get('data', {}).get('items', [])
            if not items:
                break
            all_materials.extend(items)
            pagination = result.get('data', {}).get('pagination', {})
            if not pagination.get('has_next', False):
                break
            page += 1

        return all_materials[:count]

    def create_task(self, script_content: str, material_ids: Optional[List[int]] = None,
                    **kwargs) -> Dict[str, Any]:
        """
        创建视频剪辑任务

        Args:
            script_content: 视频文案/脚本内容
            material_ids: 素材ID列表，如果不提供则自动随机选择
            **kwargs: 其他任务参数

        Returns:
            任务创建响应数据
        """
        self.ensure_login()

        # 如果没有提供素材ID，则随机选择
        if material_ids is None:
            materials = self.get_recent_materials(100)
            if len(materials) < 7:
                raise Exception(f"素材数量不足，当前只有 {len(materials)} 个素材")
            selected = random.sample(materials, 7)
            material_ids = [m['id'] for m in selected]
            print(f"随机选择了 {len(material_ids)} 个素材: {material_ids}")

        # 从配置文件读取默认值
        defaults = {
            'voice_type': self.config.get('task_defaults', 'voice_type', fallback='f_liuyuxi_20251009'),
            'voice_speed': self.config.getfloat('task_defaults', 'voice_speed', fallback=1.3),
            'voice_pitch': self.config.getfloat('task_defaults', 'voice_pitch', fallback=1.0),
            'resolution_width': self.config.getint('task_defaults', 'resolution_width', fallback=1080),
            'resolution_height': self.config.getint('task_defaults', 'resolution_height', fallback=1920),
            'subtitle_enabled': self.config.getboolean('task_defaults', 'subtitle_enabled', fallback=True),
            'subtitle_font_size': self.config.getint('task_defaults', 'subtitle_font_size', fallback=90),
            'subtitle_font_color': self.config.get('task_defaults', 'subtitle_font_color', fallback='yellow'),
            'subtitle_font': self.config.get('task_defaults', 'subtitle_font', fallback='江城律动宋'),
            'subtitle_position': self.config.getfloat('task_defaults', 'subtitle_position', fallback=0.7),
            'music_enabled': self.config.getboolean('task_defaults', 'music_enabled', fallback=True),
            'music_name': self.config.get('task_defaults', 'music_name', fallback='夏季有你'),
            'music_volume': self.config.getfloat('task_defaults', 'music_volume', fallback=0.4),
            'cover_required': self.config.getint('task_defaults', 'cover_required', fallback=1),
            'compute_account_type': self.config.getint('task_defaults', 'compute_account_type', fallback=2),
        }

        # 构建请求数据
        data = {
            "material_ids": material_ids,
            "script_content": script_content,
            "script_list": [script_content],
            "cover_required": defaults['cover_required'],
            "content_description": kwargs.get('content_description', ''),
            "top_subtitle": kwargs.get('top_subtitle', ''),
            "top_subtitle_enabled": kwargs.get('top_subtitle_enabled', False),
            "voice_type": kwargs.get('voice_type', defaults['voice_type']),
            "voice_speed": kwargs.get('voice_speed', defaults['voice_speed']),
            "voice_pitch": kwargs.get('voice_pitch', defaults['voice_pitch']),
            "resolution_width": kwargs.get('resolution_width', defaults['resolution_width']),
            "resolution_height": kwargs.get('resolution_height', defaults['resolution_height']),
            "subtitle_enabled": kwargs.get('subtitle_enabled', defaults['subtitle_enabled']),
            "subtitle_font_size": kwargs.get('subtitle_font_size', defaults['subtitle_font_size']),
            "subtitle_font_color": kwargs.get('subtitle_font_color', defaults['subtitle_font_color']),
            "subtitle_font": kwargs.get('subtitle_font', defaults['subtitle_font']),
            "subtitle_position": kwargs.get('subtitle_position', defaults['subtitle_position']),
            "music_enabled": kwargs.get('music_enabled', defaults['music_enabled']),
            "music_name": kwargs.get('music_name', defaults['music_name']),
            "music_volume": kwargs.get('music_volume', defaults['music_volume']),
            "compute_account_type": kwargs.get('compute_account_type', defaults['compute_account_type']),
            "remark": kwargs.get('remark', '')
        }

        url = f"{self.base_url}/video-editing/tasks"
        headers = self._get_headers()
        response = self._session.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if result.get('status_code') != 1:
            raise Exception(f"创建任务失败: {result.get('message', '未知错误')}")

        task_id = result.get('data', {}).get('id') or result.get('data', {}).get('task_id')
        print(f"任务创建成功! 任务ID: {task_id}")

        return result

    def get_task_progress(self, task_id: int) -> Dict[str, Any]:
        """
        获取任务进度

        Args:
            task_id: 任务ID

        Returns:
            任务进度响应数据
        """
        self.ensure_login()

        url = f"{self.base_url}/video-editing/tasks/{task_id}/progress"
        headers = self._get_headers()
        response = self._session.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result.get('status_code') != 1:
            raise Exception(f"获取任务进度失败: {result.get('message', '未知错误')}")

        return result

    def get_task_detail(self, task_id: int) -> Dict[str, Any]:
        """
        获取任务详情

        Args:
            task_id: 任务ID

        Returns:
            任务详情响应数据
        """
        self.ensure_login()

        url = f"{self.base_url}/video-editing/tasks"
        params = {'ids': task_id}
        headers = self._get_headers()
        response = self._session.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()

        if result.get('status_code') != 1:
            raise Exception(f"获取任务详情失败: {result.get('message', '未知错误')}")

        items = result.get('data', {}).get('items', [])
        if items:
            return items[0]
        return None

    def extract_task_info(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        从任务详情中提取关键信息

        Args:
            task: 任务详情字典

        Returns:
            包含扩展信息的任务字典
        """
        config = task.get('config', {})
        voice_config = config.get('voice_config', {})
        resolution_config = config.get('resolution_config', {})
        cover_config = config.get('cover_issue_config', {})

        # 视频下载地址（原始地址）
        video_url = task.get('output_path_auth') or task.get('output_path')

        # 视频播放地址（用于浏览器预览）
        play_url = None
        if video_url:
            play_url = f"https://www.qinsilk.com/player/vod.html?pSrc={urllib.parse.quote(video_url, safe='')}"

        return {
            'id': task.get('id'),
            'status': task.get('status'),
            'create_time': task.get('create_time'),
            'completed_at': task.get('completed_at'),
            # 文案（正确字段名）
            'script_content': task.get('user_script', ''),
            'user_script': task.get('user_script', ''),
            'content_description': task.get('content_description', ''),
            # 视频信息
            'duration': task.get('duration'),
            'video_url': video_url,           # 下载地址（原始）
            'play_url': play_url,             # 播放地址（预览用）
            'cover_image_path': task.get('cover_image_path_auth') or task.get('cover_image_path'),
            # 分辨率
            'resolution_width': resolution_config.get('width'),
            'resolution_height': resolution_config.get('height'),
            'resolution': f"{resolution_config.get('width', '')}x{resolution_config.get('height', '')}" if resolution_config else None,
            # 封面标题
            'cover_title': cover_config.get('title', ''),
            # 语音信息
            'voice_type': voice_config.get('voice_type', ''),
            'voice_name': get_voice_name(voice_config.get('voice_type', '')),
            'voice_speed': voice_config.get('speed'),
        }

    def get_task_list(self, page: int = 1, size: int = 10,
                      start_date: Optional[str] = None,
                      end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取任务列表

        Args:
            page: 页码
            size: 每页数量
            start_date: 开始日期 (格式: YYYY-MM-DD HH:MM:SS)
            end_date: 结束日期 (格式: YYYY-MM-DD HH:MM:SS)

        Returns:
            任务列表响应数据
        """
        self.ensure_login()

        url = f"{self.base_url}/video-editing/tasks"
        params = {
            'page': page,
            'size': size
        }

        if start_date:
            params['create_time_start'] = start_date
        if end_date:
            params['create_time_end'] = end_date

        # 如果没有指定日期范围，默认查询最近30天
        if not start_date and not end_date:
            end = datetime.now()
            start = end - timedelta(days=30)
            params['create_time_start'] = start.strftime('%Y-%m-%d 00:00:00')
            params['create_time_end'] = end.strftime('%Y-%m-%d 23:59:59')

        headers = self._get_headers()
        response = self._session.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()

        if result.get('status_code') != 1:
            raise Exception(f"获取任务列表失败: {result.get('message', '未知错误')}")

        return result

    def wait_for_task_completion(self, task_id: int, timeout: int = 600,
                                  poll_interval: int = 10) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务ID
            timeout: 超时时间(秒)
            poll_interval: 轮询间隔(秒)

        Returns:
            完成后的任务详情
        """
        self.ensure_login()

        start_time = time.time()
        status_map = {
            0: '待处理',
            1: '处理中',
            2: '处理中',
            3: '处理中',
            4: '已完成',
            5: '失败',
        }

        print(f"开始等待任务 {task_id} 完成...")

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"等待任务超时 ({timeout}秒)")

            progress = self.get_task_progress(task_id)
            data = progress.get('data', {})
            status = int(data.get('status', 0))
            progress_percent = data.get('progress', 0)

            status_text = status_map.get(status, f'未知状态({status})')
            print(f"任务状态: {status_text}, 进度: {progress_percent}%, 已等待: {int(elapsed)}秒")

            if status == 4:  # 已完成
                print(f"任务 {task_id} 已完成!")
                return self.get_task_detail(task_id)
            elif status == 5:  # 失败
                error_msg = data.get('error_message', '未知错误')
                raise Exception(f"任务失败: {error_msg}")

            time.sleep(poll_interval)

    def download_video(self, task_id: int, save_dir: Optional[str] = None,
                       filename: Optional[str] = None) -> str:
        """
        下载任务生成的视频

        Args:
            task_id: 任务ID
            save_dir: 保存目录
            filename: 文件名(不含扩展名)

        Returns:
            下载后的文件路径
        """
        self.ensure_login()

        # 获取任务详情
        task = self.get_task_detail(task_id)
        if not task:
            raise Exception(f"找不到任务 {task_id}")

        # 检查任务状态
        if int(task.get('status', 0)) != 4:
            status_map = {0: '待处理', 1: '处理中', 2: '处理中', 3: '处理中', 4: '已完成', 5: '失败'}
            status_text = status_map.get(task.get('status'), '未知')
            raise Exception(f"任务尚未完成，当前状态: {status_text}")

        # 获取下载地址
        output_path = task.get('output_path_auth') or task.get('output_path')
        if not output_path:
            raise Exception("未找到视频下载地址")

        # 确定保存路径
        if save_dir is None:
            save_dir = self.config.get('wangcut', 'download_dir', fallback='./downloads')

        Path(save_dir).mkdir(parents=True, exist_ok=True)

        if filename is None:
            filename = f"video_{task_id}_{int(time.time())}"

        filepath = os.path.join(save_dir, f"{filename}.mp4")

        # 下载视频
        print(f"开始下载视频: {output_path}")
        response = self._session.get(output_path, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\r下载进度: {percent:.1f}%", end='', flush=True)

        print(f"\n视频已保存到: {filepath}")
        return filepath


# 便捷函数
def create_video_task(script: str, config_path: str = None,
                      material_ids: Optional[List[int]] = None, **kwargs) -> int:
    """
    创建视频剪辑任务的便捷函数

    Args:
        script: 视频文案
        config_path: 配置文件路径(可选，自动查找)
        material_ids: 素材ID列表(可选，不提供则自动随机选择7个)
        **kwargs: 其他任务参数

    Returns:
        任务ID
    """
    api = WangcutAPI(config_path)
    result = api.create_task(script_content=script, material_ids=material_ids, **kwargs)
    task_id = result.get('data', {}).get('id') or result.get('data', {}).get('task_id')
    return task_id


def wait_and_download(task_id: int, config_path: str = None,
                      save_dir: Optional[str] = None, timeout: int = 600) -> str:
    """
    等待任务完成并下载视频的便捷函数

    Args:
        task_id: 任务ID
        config_path: 配置文件路径(可选，自动查找)
        save_dir: 保存目录
        timeout: 超时时间

    Returns:
        下载后的文件路径
    """
    api = WangcutAPI(config_path)
    api.wait_for_task_completion(task_id, timeout=timeout)
    return api.download_video(task_id, save_dir=save_dir)


def list_recent_tasks(config_path: str = None, count: int = 10, with_details: bool = True) -> List[Dict]:
    """
    查看最近任务的便捷函数

    Args:
        config_path: 配置文件路径(可选，自动查找)
        count: 返回的任务数量
        with_details: 是否获取详细信息（包括文案、时长、分辨率等）

    Returns:
        任务列表（包含扩展信息）
    """
    api = WangcutAPI(config_path)
    result = api.get_task_list(page=1, size=count)
    tasks = result.get('data', {}).get('items', [])

    if with_details:
        # 为每个任务获取详细信息
        enriched_tasks = []
        for task in tasks:
            detail = api.get_task_detail(task.get('id'))
            if detail:
                enriched_tasks.append(api.extract_task_info(detail))
            else:
                enriched_tasks.append(task)
        return enriched_tasks

    return tasks


if __name__ == "__main__":
    # 示例用法
    import argparse

    parser = argparse.ArgumentParser(description='秦丝智能视频剪辑API客户端')
    parser.add_argument('--config', default='config.ini', help='配置文件路径')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 创建任务命令
    create_parser = subparsers.add_parser('create', help='创建视频剪辑任务')
    create_parser.add_argument('script', help='视频文案内容')
    create_parser.add_argument('--materials', nargs='+', type=int, help='素材ID列表')

    # 查看任务列表命令
    list_parser = subparsers.add_parser('list', help='查看任务列表')
    list_parser.add_argument('--count', type=int, default=10, help='显示数量')

    # 查看任务详情命令
    detail_parser = subparsers.add_parser('detail', help='查看任务详情')
    detail_parser.add_argument('task_id', type=int, help='任务ID')

    # 等待任务命令
    wait_parser = subparsers.add_parser('wait', help='等待任务完成')
    wait_parser.add_argument('task_id', type=int, help='任务ID')
    wait_parser.add_argument('--timeout', type=int, default=600, help='超时时间(秒)')

    # 下载视频命令
    download_parser = subparsers.add_parser('download', help='下载视频')
    download_parser.add_argument('task_id', type=int, help='任务ID')
    download_parser.add_argument('--dir', help='保存目录')

    args = parser.parse_args()

    if args.command == 'create':
        task_id = create_video_task(args.script, args.config, args.materials)
        print(f"任务ID: {task_id}")
    elif args.command == 'list':
        tasks = list_recent_tasks(args.config, args.count)
        for task in tasks:
            status_map = {0: '待处理', 1: '处理中', 2: '处理中', 3: '处理中', 4: '已完成', 5: '失败'}
            status = status_map.get(task.get('status'), '未知')
            print(f"ID: {task['id']}, 状态: {status}, 创建时间: {task.get('create_time')}")
    elif args.command == 'detail':
        api = WangcutAPI(args.config)
        task = api.get_task_detail(args.task_id)
        print(json.dumps(task, ensure_ascii=False, indent=2))
    elif args.command == 'wait':
        api = WangcutAPI(args.config)
        api.wait_for_task_completion(args.task_id, args.timeout)
    elif args.command == 'download':
        api = WangcutAPI(args.config)
        filepath = api.download_video(args.task_id, args.dir)
        print(f"下载完成: {filepath}")
    else:
        parser.print_help()
