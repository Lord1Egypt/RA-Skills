#!/usr/bin/env python3
"""
企业微信会议API客户端
提供统一的接口用于创建、查询、取消企业微信会议
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path


class WeComMeeting:
    """企业微信会议管理类"""

    def __init__(self, corpid=None, secret=None, agentid=None):
        """
        初始化企业微信会议客户端

        Args:
            corpid: 企业微信CorpID
            secret: 企业微信应用Secret
            agentid: 企业微信应用AgentID
        """
        self.corpid = corpid
        self.secret = secret
        self.agentid = agentid
        self.access_token = None
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin"

        # 如果没有提供凭证，尝试从配置文件加载
        if not all([corpid, secret, agentid]):
            config = self.load_config()
            if config:
                self.corpid = self.corpid or config.get("corpid")
                self.secret = self.secret or config.get("secret")
                self.agentid = self.agentid or config.get("agentid")

    @staticmethod
    def load_config():
        """从配置文件加载凭证"""
        config_path = Path.home() / ".wecom" / "config.json"

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_access_token(self, force_refresh=False):
        """
        获取 access_token

        Args:
            force_refresh: 是否强制刷新token

        Returns:
            access_token字符串
        """
        if self.access_token and not force_refresh:
            return self.access_token

        url = f"{self.base_url}/gettoken"
        params = {
            "corpid": self.corpid,
            "corpsecret": self.secret
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()

            if result["errcode"] == 0:
                self.access_token = result["access_token"]
                return self.access_token
            else:
                raise Exception(f"获取 access_token 失败: {result}")
        except Exception as e:
            raise Exception(f"请求失败: {e}")

    def create_meeting(self, admin_userid, title, meeting_start, meeting_duration,
                       description="", invitees=None, reminders=None):
        """
        创建预约会议

        Args:
            admin_userid: 发起人UserID
            title: 会议主题（最多40字节或20个utf8字符）
            meeting_start: 会议开始时间（Unix时间戳，秒）
            meeting_duration: 会议时长（秒），最小300，最大86399
            description: 会议描述（可选）
            invitees: 参会人列表，格式：{"userid": ["user1", "user2"]}
            reminders: 提醒设置，格式：{"is_repeat": 0, "remind_before": [120]}

        Returns:
            API响应结果，包含meetingid等字段

        Raises:
            Exception: 创建失败时抛出异常
        """
        access_token = self.get_access_token()

        url = f"{self.base_url}/meeting/create?access_token={access_token}"

        # 构建请求数据
        data = {
            "admin_userid": admin_userid,
            "title": title,
            "meeting_start": meeting_start,
            "meeting_duration": meeting_duration,
        }

        # 可选参数
        if description:
            data["description"] = description

        if invitees:
            data["invitees"] = invitees

        if reminders:
            data["reminders"] = reminders
        else:
            # 默认提醒设置
            data["reminders"] = {
                "is_repeat": 0,
                "remind_before": [120]  # 默认提前2分钟
            }

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result["errcode"] == 0:
                return result
            else:
                raise Exception(f"创建会议失败: {result}")
        except Exception as e:
            raise Exception(f"请求失败: {e}")

    def get_meeting(self, meetingid):
        """
        获取会议详情

        Args:
            meetingid: 会议ID

        Returns:
            API响应结果，包含会议详细信息

        Raises:
            Exception: 查询失败时抛出异常
        """
        access_token = self.get_access_token()

        url = f"{self.base_url}/meeting/get?access_token={access_token}"

        data = {
            "meetingid": meetingid
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result["errcode"] == 0:
                return result
            else:
                raise Exception(f"获取会议失败: {result}")
        except Exception as e:
            raise Exception(f"请求失败: {e}")

    def cancel_meeting(self, meetingid, admin_userid):
        """
        取消会议

        Args:
            meetingid: 会议ID
            admin_userid: 发起人UserID

        Returns:
            API响应结果

        Raises:
            Exception: 取消失败时抛出异常
        """
        access_token = self.get_access_token()

        url = f"{self.base_url}/meeting/cancel?access_token={access_token}"

        data = {
            "meetingid": meetingid,
            "admin_userid": admin_userid
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result["errcode"] == 0:
                return result
            else:
                raise Exception(f"取消会议失败: {result}")
        except Exception as e:
            raise Exception(f"请求失败: {e}")

    def get_user_meetings(self, userid):
        """
        获取成员的会议ID列表

        Args:
            userid: 成员UserID

        Returns:
            API响应结果，包含会议ID列表

        Raises:
            Exception: 查询失败时抛出异常
        """
        access_token = self.get_access_token()

        url = f"{self.base_url}/meeting/get_user_meetings?access_token={access_token}"

        data = {
            "userid": userid
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result["errcode"] == 0:
                return result
            else:
                raise Exception(f"获取会议列表失败: {result}")
        except Exception as e:
            raise Exception(f"请求失败: {e}")

    @staticmethod
    def parse_time(time_str, date_str=None):
        """
        解析时间字符串为Unix时间戳

        Args:
            time_str: 时间字符串，格式：HH:MM
            date_str: 日期字符串，格式：YYYY-MM-DD，默认为今天

        Returns:
            Unix时间戳（秒）
        """
        try:
            if date_str:
                dt_str = f"{date_str} {time_str}:00"
            else:
                today = datetime.now().strftime("%Y-%m-%d")
                dt_str = f"{today} {time_str}:00"

            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp())
        except ValueError:
            raise ValueError(f"时间格式错误，请使用 HH:MM 格式，日期使用 YYYY-MM-DD 格式")

    @staticmethod
    def format_timestamp(timestamp):
        """
        格式化Unix时间戳为可读字符串

        Args:
            timestamp: Unix时间戳（秒）

        Returns:
            格式化后的时间字符串，如：2026-03-06 17:40:00
        """
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    # 测试代码
    try:
        meeting = WeComMeeting()
        print("✅ 企业微信会议客户端初始化成功")

        # 测试配置
        print(f"CorpID: {meeting.corpid}")
        print(f"AgentID: {meeting.agentid}")

        # 测试获取token
        token = meeting.get_access_token()
        print(f"✅ 成功获取 access_token: {token[:20]}...")

    except Exception as e:
        print(f"❌ 初始化失败: {e}")