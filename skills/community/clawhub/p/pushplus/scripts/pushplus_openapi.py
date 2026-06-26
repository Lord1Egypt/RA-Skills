#!/usr/bin/env python3
"""
PushPlus OpenAPI 客户端
提供 AccessKey 管理、消息接口、用户接口、消息Token接口、群组接口等功能

使用说明:
1. 首先调用 get_access_key() 获取 AccessKey（有效期2小时）
2. 使用 AccessKey 调用其他接口，需要在请求头中设置 access-key

环境变量:
- PUSHPLUS_USER_TOKEN: 用户 Token（用于获取 AccessKey）
- PUSHPLUS_SECRET_KEY: 用户 SecretKey（用于获取 AccessKey）
"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


# OpenAPI 基础地址
OPENAPI_BASE_URL = "https://www.pushplus.plus/api"

# 环境变量名
ENV_USER_TOKEN = "PUSHPLUS_USER_TOKEN"
ENV_SECRET_KEY = "PUSHPLUS_SECRET_KEY"
MAX_PAGE_SIZE = 50
MAX_TOPIC_QRCODE_SECOND = 2592000


def get_access_key(user_token: Optional[str] = None, secret_key: Optional[str] = None) -> Dict[str, Any]:
    """
    获取 AccessKey（有效期2小时）
    
    Args:
        user_token: 用户 Token（如不提供，从环境变量 PUSHPLUS_USER_TOKEN 获取）
        secret_key: 用户 SecretKey（如不提供，从环境变量 PUSHPLUS_SECRET_KEY 获取）
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": {
                "accessKey": "d7b******62f",
                "expiresIn": 7200
            }
        }
    """
    # 从环境变量获取（如果未提供）
    token = user_token or os.environ.get(ENV_USER_TOKEN)
    secret = secret_key or os.environ.get(ENV_SECRET_KEY)
    
    if not token or not secret:
        raise ValueError("请提供 user_token 和 secret_key，或设置环境变量 PUSHPLUS_USER_TOKEN 和 PUSHPLUS_SECRET_KEY")
    
    url = f"{OPENAPI_BASE_URL}/common/openApi/getAccessKey"
    payload = {
        "token": token,
        "secretKey": secret
    }
    
    return _make_request(url, payload)


def _validate_non_empty_text(field_name: str, value: Optional[str]) -> str:
    """校验必填文本参数"""
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} 不能为空")
    return str(value).strip()


def _validate_positive_int(field_name: str, value: int, minimum: int = 1) -> int:
    """校验正整数参数"""
    if not isinstance(value, int):
        raise ValueError(f"{field_name} 必须为整数")
    if value < minimum:
        raise ValueError(f"{field_name} 必须大于等于 {minimum}")
    return value


def _validate_page_params(current: int, page_size: int) -> None:
    """校验分页参数"""
    _validate_positive_int("current", current)
    _validate_positive_int("page_size", page_size)
    if page_size > MAX_PAGE_SIZE:
        raise ValueError(f"page_size 不能大于 {MAX_PAGE_SIZE}")


# ==================== 消息接口 ====================

def list_messages(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取消息列表
    
    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20
        
    Returns:
        消息列表数据
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)

    url = f"{OPENAPI_BASE_URL}/open/message/list"
    payload = {
        "current": current,
        "pageSize": page_size
    }
    
    return _make_request(url, payload, validated_access_key)


def get_message_result(access_key: str, short_code: str) -> Dict[str, Any]:
    """
    查询消息发送结果
    
    Args:
        access_key: AccessKey
        short_code: 消息短链码
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": {
                "status": 2,
                "errorMessage": "",
                "updateTime": "2021-12-08 12:19:02"
            }
        }
        status: 0-未投递，1-发送中，2-已发送，3-发送失败
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_short_code = _validate_non_empty_text("short_code", short_code)
    return _make_request(
        f"{OPENAPI_BASE_URL}/open/message/sendMessageResult?shortCode={validated_short_code}",
        method="GET",
        access_key=validated_access_key
    )


def delete_message(access_key: str, short_code: str) -> Dict[str, Any]:
    """
    删除消息
    
    注：删除后所有接收人均无法查看，且无法撤销。
    
    Args:
        access_key: AccessKey
        short_code: 消息短链码
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "删除成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_short_code = _validate_non_empty_text("short_code", short_code)
    url = f"{OPENAPI_BASE_URL}/open/message/deleteMessage?shortCode={validated_short_code}"
    
    return _make_request(url, method="DELETE", access_key=validated_access_key)


def get_message_detail(access_key: str, short_code: str) -> str:
    """
    获取消息详情

    注：返回 HTML 格式的消息内容，非 JSON。

    Args:
        access_key: AccessKey
        short_code: 消息短链码

    Returns:
        消息内容的 HTML 文本
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_short_code = _validate_non_empty_text("short_code", short_code)
    url = f"https://www.pushplus.plus/shortMessage/{validated_short_code}"

    headers = {
        "Content-Type": "text/html;charset=UTF-8",
        "User-Agent": "PushPlus-OpenAPI-Python/1.0"
    }
    headers["access-key"] = validated_access_key
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP 错误: {e.code}")
    except urllib.error.URLError as e:
        raise Exception(f"URL 错误: {e.reason}")
    except Exception as e:
        raise Exception(f"请求失败: {str(e)}")


# ==================== 用户接口 ====================

def get_user_token(access_key: str) -> Dict[str, Any]:
    """
    获取用户 Token
    
    Args:
        access_key: AccessKey
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "604******f0b"
        }
    """
    url = f"{OPENAPI_BASE_URL}/open/user/token"
    
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_user_info(access_key: str) -> Dict[str, Any]:
    """
    获取个人资料详情
    
    Args:
        access_key: AccessKey
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": {
                "openId": "o0a******A3Y",
                "nickName": "昵称",
                "headImgUrl": "头像URL",
                "userSex": 1,
                "token": "604******f0b",
                "phoneNumber": "13******4",
                "email": "admin@xxx.com",
                "emailStatus": 1,
                "birthday": "1990-01-01",
                "points": 2
            }
        }
    """
    url = f"{OPENAPI_BASE_URL}/open/user/myInfo"
    
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_limit_time(access_key: str) -> Dict[str, Any]:
    """
    获取解封剩余时间
    
    Args:
        access_key: AccessKey
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": {
                "sendLimit": 1,
                "userLimitTime": ""
            }
        }
        sendLimit: 1-无限制，2-短期限制，3-永久限制
    """
    url = f"{OPENAPI_BASE_URL}/open/user/userLimitTime"
    
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_send_count(access_key: str) -> Dict[str, Any]:
    """
    查询当日消息接口请求次数
    
    Args:
        access_key: AccessKey
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": {
                "wechatSendCount": 283,
                "cpSendCount": 0,
                "webhookSendCount": 19,
                "mailSendCount": 0
            }
        }
    """
    url = f"{OPENAPI_BASE_URL}/open/user/sendCount"
    
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    return _make_request(url, method="GET", access_key=validated_access_key)


# ==================== 消息Token接口 ====================

def list_tokens(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取消息 Token 列表
    
    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20
        
    Returns:
        消息 Token 列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)

    url = f"{OPENAPI_BASE_URL}/open/token/list"
    payload = {
        "current": current,
        "pageSize": page_size,
        "params": {}
    }

    return _make_request(url, payload, validated_access_key)


def add_token(access_key: str, name: str, expire_time: Optional[str] = None) -> Dict[str, Any]:
    """
    新增消息 Token
    
    Args:
        access_key: AccessKey
        name: 令牌名称
        expire_time: 过期时间，格式 "2035-05-09 22:34:00"，默认 "2999-12-31"
        
    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": "837******46e2"  # 新建的消息 Token
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_name = _validate_non_empty_text("name", name)
    url = f"{OPENAPI_BASE_URL}/open/token/add"
    payload = {
        "name": validated_name
    }
    if expire_time:
        payload["expireTime"] = expire_time
    
    return _make_request(url, payload, validated_access_key)


def edit_token(access_key: str, token_id: int, name: str, expire_time: Optional[str] = None) -> Dict[str, Any]:
    """
    修改消息 Token
    
    Args:
        access_key: AccessKey
        token_id: 消息 Token 编号
        name: 令牌名称
        expire_time: 过期时间，格式 "2035-05-09 22:34:00"
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "修改成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_token_id = _validate_positive_int("token_id", token_id)
    validated_name = _validate_non_empty_text("name", name)
    url = f"{OPENAPI_BASE_URL}/open/token/edit"
    payload = {
        "id": validated_token_id,
        "name": validated_name
    }
    if expire_time:
        payload["expireTime"] = expire_time
    
    return _make_request(url, payload, validated_access_key)


def delete_token(access_key: str, token_id: int) -> Dict[str, Any]:
    """
    删除消息 Token
    
    Args:
        access_key: AccessKey
        token_id: 消息 Token 编号
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "删除成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_token_id = _validate_positive_int("token_id", token_id)
    url = f"{OPENAPI_BASE_URL}/open/token/deleteToken?id={validated_token_id}"
    
    return _make_request(url, method="DELETE", access_key=validated_access_key)


def select_token_list(access_key: str, token_type: int = 0) -> Dict[str, Any]:
    """
    消息 Token 下拉选择列表

    Args:
        access_key: AccessKey
        token_type: 0-返回所有消息token，1-返回未配置默认推送渠道的消息token，默认0

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": [{"id": 1, "name": "token1"}, ...]
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    if token_type not in (0, 1):
        raise ValueError("token_type 仅支持 0 或 1")
    url = f"{OPENAPI_BASE_URL}/open/token/selectTokenList?type={token_type}"
    return _make_request(url, method="GET", access_key=validated_access_key)


# ==================== 群组接口 ====================

def list_topics(access_key: str, topic_type: int = 0, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取群组列表
    
    Args:
        access_key: AccessKey
        topic_type: 群组类型，0-我创建的，1-我加入的，默认0
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20
        
    Returns:
        群组列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    if topic_type not in (0, 1):
        raise ValueError("topic_type 仅支持 0（我创建的）或 1（我加入的）")

    url = f"{OPENAPI_BASE_URL}/open/topic/list"
    payload = {
        "current": current,
        "pageSize": page_size,
        "params": {
            "topicType": topic_type
        }
    }
    
    return _make_request(url, payload, validated_access_key)


def get_topic_detail(access_key: str, topic_id: int) -> Dict[str, Any]:
    """
    获取群组详情（我创建的群组）
    
    Args:
        access_key: AccessKey
        topic_id: 群组编号
        
    Returns:
        群组详情
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_id = _validate_positive_int("topic_id", topic_id)
    url = f"{OPENAPI_BASE_URL}/open/topic/detail?topicId={validated_topic_id}"
    
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_join_topic_detail(access_key: str, topic_id: int) -> Dict[str, Any]:
    """
    获取我加入的群详情

    Args:
        access_key: AccessKey
        topic_id: 群组编号

    Returns:
        群组详情（加入的群组）
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_id = _validate_positive_int("topic_id", topic_id)
    url = f"{OPENAPI_BASE_URL}/open/topic/joinTopicDetail?topicId={validated_topic_id}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def edit_topic(
    access_key: str,
    topic: int,
    topic_code: str,
    topic_name: str,
    contact: Optional[str] = None,
    introduction: Optional[str] = None,
    receipt_message: Optional[str] = None,
    icon: Optional[str] = None,
    price: Optional[float] = None,
    topic_describe: Optional[str] = None
) -> Dict[str, Any]:
    """
    修改群组

    Args:
        access_key: AccessKey
        topic: 群组编号
        topic_code: 群组编码
        topic_name: 群组名称
        contact: 联系方式（可选）
        introduction: 群组简介（可选）
        receipt_message: 加入后回复内容（可选）
        icon: 群组图标（可选）
        price: 积分群组订阅积分，按月（可选）
        topic_describe: 一句话介绍（可选）

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": "修改成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic = _validate_positive_int("topic", topic)
    validated_topic_code = _validate_non_empty_text("topic_code", topic_code)
    validated_topic_name = _validate_non_empty_text("topic_name", topic_name)
    url = f"{OPENAPI_BASE_URL}/open/topic/editTopic"
    payload = {
        "topic": validated_topic,
        "topicCode": validated_topic_code,
        "topicName": validated_topic_name
    }
    if contact:
        payload["contact"] = contact
    if introduction:
        payload["introduction"] = introduction
    if receipt_message:
        payload["receiptMessage"] = receipt_message
    if icon:
        payload["icon"] = icon
    if price is not None:
        payload["price"] = price
    if topic_describe:
        payload["topicDescribe"] = topic_describe
    return _make_request(url, payload, validated_access_key)


def add_topic(
    access_key: str,
    topic_code: str,
    topic_name: str,
    contact: str,
    introduction: str,
    receipt_message: Optional[str] = None,
    app_id: Optional[str] = None,
    icon: Optional[str] = None,
    topic_type: Optional[int] = None,
    price: Optional[float] = None,
    topic_describe: Optional[str] = None
) -> Dict[str, Any]:
    """
    新增群组

    Args:
        access_key: AccessKey
        topic_code: 群组编码
        topic_name: 群组名称
        contact: 联系方式
        introduction: 群组简介
        receipt_message: 加入后回复内容（可选）
        app_id: 微信公众号 Id（可选，默认使用 pushplus 公众号）
        icon: 群组图标（可选）
        topic_type: 群组类型，0-普通群组，1-积分群组，2-公开群组（可选，默认0）
        price: 积分群组订阅积分，按月（可选，默认0.00）
        topic_describe: 一句话介绍（可选）

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": 2  # 新建群组的群组编号
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_code = _validate_non_empty_text("topic_code", topic_code)
    validated_topic_name = _validate_non_empty_text("topic_name", topic_name)
    validated_contact = _validate_non_empty_text("contact", contact)
    validated_introduction = _validate_non_empty_text("introduction", introduction)
    if topic_type is not None and topic_type not in (0, 1, 2):
        raise ValueError("topic_type 仅支持 0（普通群组）、1（积分群组）或 2（公开群组）")
    url = f"{OPENAPI_BASE_URL}/open/topic/add"
    payload = {
        "topicCode": validated_topic_code,
        "topicName": validated_topic_name,
        "contact": validated_contact,
        "introduction": validated_introduction
    }
    if receipt_message:
        payload["receiptMessage"] = receipt_message
    if app_id:
        payload["appId"] = app_id
    if icon:
        payload["icon"] = icon
    if topic_type is not None:
        payload["topicType"] = topic_type
    if price is not None:
        payload["price"] = price
    if topic_describe:
        payload["topicDescribe"] = topic_describe

    return _make_request(url, payload, validated_access_key)


def get_topic_qrcode(
    access_key: str,
    topic_id: int,
    second: int = 604800,
    scan_count: int = -1
) -> Dict[str, Any]:
    """
    获取群组二维码
    
    Args:
        access_key: AccessKey
        topic_id: 群组编号
        second: 二维码有效期（单位秒），默认7天（604800秒），最长30天
        scan_count: 可扫码次数，范围1-999次，-1代表无限次
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": {
                "qrCodeImgUrl": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=...",
                "forever": 0  # 0-临时二维码，1-永久二维码
            }
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_id = _validate_positive_int("topic_id", topic_id)
    validated_second = _validate_positive_int("second", second)
    if validated_second > MAX_TOPIC_QRCODE_SECOND:
        raise ValueError(f"second 不能大于 {MAX_TOPIC_QRCODE_SECOND}")
    if not isinstance(scan_count, int):
        raise ValueError("scan_count 必须为整数")
    if scan_count != -1 and not 1 <= scan_count <= 999:
        raise ValueError("scan_count 仅支持 -1 或 1-999")
    url = f"{OPENAPI_BASE_URL}/open/topic/qrCode?topicId={validated_topic_id}&second={validated_second}&scanCount={scan_count}"
    
    return _make_request(url, method="GET", access_key=validated_access_key)


def exit_topic(access_key: str, topic_id: int) -> Dict[str, Any]:
    """
    退出群组
    
    Args:
        access_key: AccessKey
        topic_id: 群组编号
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "退订成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_id = _validate_positive_int("topic_id", topic_id)
    url = f"{OPENAPI_BASE_URL}/open/topic/exitTopic?topicId={validated_topic_id}"
    
    return _make_request(url, method="GET", access_key=validated_access_key)


def delete_topic(access_key: str, topic_id: int) -> Dict[str, Any]:
    """
    删除群组
    
    Args:
        access_key: AccessKey
        topic_id: 群组编号
        
    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "群组删除成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_id = _validate_positive_int("topic_id", topic_id)
    url = f"{OPENAPI_BASE_URL}/open/topic/delete?topicId={validated_topic_id}"
    
    return _make_request(url, method="GET", access_key=validated_access_key)


def set_topic_is_open(access_key: str, topic: int, is_open: int) -> Dict[str, Any]:
    """
    上下架积分群组

    Args:
        access_key: AccessKey
        topic: 群组编号
        is_open: 是否上架，1-上架，0-下架

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "操作成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic = _validate_positive_int("topic", topic)
    if is_open not in (0, 1):
        raise ValueError("is_open 仅支持 0（下架）或 1（上架）")
    url = f"{OPENAPI_BASE_URL}/open/topic/isOpen"
    payload = {"topic": validated_topic, "isOpen": is_open}
    return _make_request(url, payload, validated_access_key)


# ==================== 群组用户接口 ====================


def list_topic_subscribers(access_key: str, topic_id: int, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取群组内用户

    Args:
        access_key: AccessKey
        topic_id: 群组编号
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        群组用户列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_topic_id = _validate_positive_int("topic_id", topic_id)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/topicUser/subscriberList"
    payload = {
        "current": current,
        "pageSize": page_size,
        "params": {"topicId": validated_topic_id}
    }
    return _make_request(url, payload, validated_access_key)


def delete_topic_user(access_key: str, topic_relation_id: int) -> Dict[str, Any]:
    """
    删除群组内用户

    Args:
        access_key: AccessKey
        topic_relation_id: 用户编号

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "删除成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("topic_relation_id", topic_relation_id)
    url = f"{OPENAPI_BASE_URL}/open/topicUser/deleteTopicUser?topicRelationId={validated_id}"
    return _make_request(url, method="POST", access_key=validated_access_key)


def edit_topic_user_remark(access_key: str, user_id: int, remark: str) -> Dict[str, Any]:
    """
    修改订阅人备注

    Args:
        access_key: AccessKey
        user_id: 用户编号
        remark: 备注信息，20个字以内

    Returns:
        {
            "code": 200,
            "msg": "执行成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("user_id", user_id)
    validated_remark = _validate_non_empty_text("remark", remark)
    url = f"{OPENAPI_BASE_URL}/open/topicUser/editRemark"
    payload = {"id": validated_id, "remark": validated_remark}
    return _make_request(url, payload, validated_access_key)


# ==================== 渠道配置接口 ====================


def list_webhooks(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取 webhook 列表

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        webhook 列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/webhook/list"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def get_webhook_detail(access_key: str, webhook_id: int) -> Dict[str, Any]:
    """
    获取 webhook 详情

    Args:
        access_key: AccessKey
        webhook_id: webhook 编号

    Returns:
        webhook 详情
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("webhook_id", webhook_id)
    url = f"{OPENAPI_BASE_URL}/open/webhook/detail?webhookId={validated_id}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def add_webhook(
    access_key: str,
    webhook_code: str,
    webhook_name: str,
    webhook_type: int,
    webhook_url: str,
    http_method: Optional[str] = None,
    headers: Optional[str] = None,
    body: Optional[str] = None
) -> Dict[str, Any]:
    """
    新增 webhook

    Args:
        access_key: AccessKey
        webhook_code: webhook 编码
        webhook_name: webhook 名称
        webhook_type: webhook 类型（1-企业微信机器人, 2-钉钉机器人, 3-飞书机器人,
                      4-Server酱, 50-bark, 6-企业微信应用, 7-腾讯轻联, 8-IFTTT,
                      9-集简云, 10-Gotify, 11-WxPusher, 12-自定义）
        webhook_url: 调用的 URL 地址
        http_method: 请求方法（仅自定义类型中需要）
        headers: 请求头（仅自定义类型中需要）
        body: body 内容（仅自定义类型中需要）

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": 2  # 新建 webhook 编号
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_code = _validate_non_empty_text("webhook_code", webhook_code)
    validated_name = _validate_non_empty_text("webhook_name", webhook_name)
    validated_url = _validate_non_empty_text("webhook_url", webhook_url)
    url = f"{OPENAPI_BASE_URL}/open/webhook/add"
    payload = {
        "webhookCode": validated_code,
        "webhookName": validated_name,
        "webhookType": webhook_type,
        "webhookUrl": validated_url
    }
    if http_method:
        payload["httpMethod"] = http_method
    if headers:
        payload["headers"] = headers
    if body:
        payload["body"] = body
    return _make_request(url, payload, validated_access_key)


def edit_webhook(
    access_key: str,
    webhook_id: int,
    webhook_code: str,
    webhook_name: str,
    webhook_type: int,
    webhook_url: str,
    http_method: Optional[str] = None,
    headers: Optional[str] = None,
    body: Optional[str] = None
) -> Dict[str, Any]:
    """
    修改 webhook 配置

    Args:
        access_key: AccessKey
        webhook_id: webhook 编号
        webhook_code: webhook 编码
        webhook_name: webhook 名称
        webhook_type: webhook 类型
        webhook_url: 调用的 URL 地址
        http_method: 请求方法（仅自定义类型中需要）
        headers: 请求头（仅自定义类型中需要）
        body: body 内容（仅自定义类型中需要）

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "修改成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("webhook_id", webhook_id)
    validated_code = _validate_non_empty_text("webhook_code", webhook_code)
    validated_name = _validate_non_empty_text("webhook_name", webhook_name)
    validated_url = _validate_non_empty_text("webhook_url", webhook_url)
    url = f"{OPENAPI_BASE_URL}/open/webhook/edit"
    payload = {
        "id": validated_id,
        "webhookCode": validated_code,
        "webhookName": validated_name,
        "webhookType": webhook_type,
        "webhookUrl": validated_url
    }
    if http_method:
        payload["httpMethod"] = http_method
    if headers:
        payload["headers"] = headers
    if body:
        payload["body"] = body
    return _make_request(url, payload, validated_access_key)


def list_mp_channels(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取微信公众号渠道列表

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        微信公众号列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/mp/list"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def list_cp_channels(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取企业微信应用渠道列表

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        企业微信应用列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/cp/list"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def list_mail_channels(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取邮箱渠道列表

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        邮箱渠道列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/mail/list"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def get_mail_channel_detail(access_key: str, mail_id: int) -> Dict[str, Any]:
    """
    获取邮箱渠道详情

    Args:
        access_key: AccessKey
        mail_id: 邮箱编号

    Returns:
        邮箱渠道详情
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("mail_id", mail_id)
    url = f"{OPENAPI_BASE_URL}/open/mail/detail?mailId={validated_id}"
    return _make_request(url, method="GET", access_key=validated_access_key)


# ==================== 微信ClawBot接口 ====================


def get_clawbot_qrcode(access_key: str) -> Dict[str, Any]:
    """
    获取微信 ClawBot 二维码

    Args:
        access_key: AccessKey

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": {
                "url": "二维码地址",
                "qrcode": "二维码编号"
            }
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    url = f"{OPENAPI_BASE_URL}/open/clawBot/getBotQrcode"
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_clawbot_qrcode_status(access_key: str, qrcode: str) -> Dict[str, Any]:
    """
    查询 ClawBot 扫码结果

    Args:
        access_key: AccessKey
        qrcode: 二维码编号

    Returns:
        {
            "code": 200,
            "msg": "请求成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_qrcode = _validate_non_empty_text("qrcode", qrcode)
    url = f"{OPENAPI_BASE_URL}/open/clawBot/getQrcodeStatus?qrcode={validated_qrcode}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_clawbot_bind_info(access_key: str) -> Dict[str, Any]:
    """
    获取 ClawBot 绑定详情

    Args:
        access_key: AccessKey

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": {
                "createTime": "绑定时间",
                "haveContextToken": 1
            }
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    url = f"{OPENAPI_BASE_URL}/open/clawBot/botInfo"
    return _make_request(url, method="GET", access_key=validated_access_key)


def unbind_clawbot(access_key: str) -> Dict[str, Any]:
    """
    解绑 ClawBot

    Args:
        access_key: AccessKey

    Returns:
        {
            "code": 200,
            "msg": "执行成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    url = f"{OPENAPI_BASE_URL}/open/clawBot/unbind"
    return _make_request(url, method="GET", access_key=validated_access_key)


def get_clawbot_messages(access_key: str) -> Dict[str, Any]:
    """
    获取 ClawBot 发送消息

    Args:
        access_key: AccessKey

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": [{"type": 1, "text": "文字消息"}, ...]
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    url = f"{OPENAPI_BASE_URL}/open/clawBot/getMsg"
    return _make_request(url, method="GET", access_key=validated_access_key)


# ==================== 功能设置接口 ====================


def list_default_settings(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取默认配置列表

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        默认配置列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/setting/listUserDefault"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def get_default_setting_detail(access_key: str, setting_id: int) -> Dict[str, Any]:
    """
    获取默认配置详情

    Args:
        access_key: AccessKey
        setting_id: 默认配置编号

    Returns:
        默认配置详情
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("setting_id", setting_id)
    url = f"{OPENAPI_BASE_URL}/open/setting/detailUserDefault?id={validated_id}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def add_default_setting(
    access_key: str,
    channel: str,
    option: str,
    pre: str,
    token_id: str
) -> Dict[str, Any]:
    """
    新增默认配置

    Args:
        access_key: AccessKey
        channel: 渠道编码（wechat/cp/webhook/mail/sms/voice/extension）
        option: 渠道参数
        pre: 预处理编码
        token_id: 消息令牌 id，用户令牌为 "0"

    Returns:
        {
            "code": 200,
            "msg": "请求成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_channel = _validate_non_empty_text("channel", channel)
    validated_option = _validate_non_empty_text("option", option)
    validated_pre = _validate_non_empty_text("pre", pre)
    validated_token_id = _validate_non_empty_text("token_id", token_id)
    url = f"{OPENAPI_BASE_URL}/open/setting/addUserDefault"
    payload = {
        "channel": validated_channel,
        "option": validated_option,
        "pre": validated_pre,
        "tokenId": validated_token_id
    }
    return _make_request(url, payload, validated_access_key)


def edit_default_setting(
    access_key: str,
    setting_id: str,
    channel: str,
    token_id: str,
    option: Optional[str] = None,
    pre: Optional[str] = None
) -> Dict[str, Any]:
    """
    修改默认配置

    Args:
        access_key: AccessKey
        setting_id: 默认配置编号
        channel: 渠道编码
        token_id: 消息令牌 id，用户令牌为 "0"
        option: 渠道参数（可选）
        pre: 预处理编码（可选）

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": "修改成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_channel = _validate_non_empty_text("channel", channel)
    validated_token_id = _validate_non_empty_text("token_id", token_id)
    url = f"{OPENAPI_BASE_URL}/open/setting/editUserDefault"
    payload = {
        "id": setting_id,
        "channel": validated_channel,
        "tokenId": validated_token_id
    }
    if option is not None:
        payload["option"] = option
    if pre is not None:
        payload["pre"] = pre
    return _make_request(url, payload, validated_access_key)


def delete_default_setting(access_key: str, setting_id: int) -> Dict[str, Any]:
    """
    删除默认配置

    Args:
        access_key: AccessKey
        setting_id: 默认配置编号

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "默认配置删除成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("setting_id", setting_id)
    url = f"{OPENAPI_BASE_URL}/open/setting/deleteUserDefault?id={validated_id}"
    return _make_request(url, method="DELETE", access_key=validated_access_key)


def set_receive_limit(access_key: str, receive_limit: int) -> Dict[str, Any]:
    """
    修改接收消息限制

    Args:
        access_key: AccessKey
        receive_limit: 0-接收全部，1-不接收消息

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": null
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    if receive_limit not in (0, 1):
        raise ValueError("receive_limit 仅支持 0（接收全部）或 1（不接收消息）")
    url = f"{OPENAPI_BASE_URL}/open/setting/changeRecevieLimit?recevieLimit={receive_limit}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def set_send_enabled(access_key: str, is_send: int) -> Dict[str, Any]:
    """
    开启/关闭发送消息功能

    Args:
        access_key: AccessKey
        is_send: 0-禁用，1-启用

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": null
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    if is_send not in (0, 1):
        raise ValueError("is_send 仅支持 0（禁用）或 1（启用）")
    url = f"{OPENAPI_BASE_URL}/open/setting/changeIsSend?isSend={is_send}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def set_open_message_type(access_key: str, open_message_type: int) -> Dict[str, Any]:
    """
    修改打开消息方式

    Args:
        access_key: AccessKey
        open_message_type: 0-H5，1-小程序

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": null
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    if open_message_type not in (0, 1):
        raise ValueError("open_message_type 仅支持 0（H5）或 1（小程序）")
    url = f"{OPENAPI_BASE_URL}/open/setting/changeOpenMessageType?openMessageType={open_message_type}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def set_extension_forward(access_key: str, forward: int) -> Dict[str, Any]:
    """
    修改插件渠道转发

    Args:
        access_key: AccessKey
        forward: 微信渠道消息是否同步浏览器扩展和桌面应用程序，0-否，1-是

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": null
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    if forward not in (0, 1):
        raise ValueError("forward 仅支持 0（否）或 1（是）")
    url = f"{OPENAPI_BASE_URL}/open/setting/extension?forward={forward}"
    return _make_request(url, method="GET", access_key=validated_access_key)


# ==================== 好友功能接口 ====================


def get_personal_qrcode(
    access_key: str,
    app_id: Optional[str] = None,
    content: Optional[str] = None,
    second: int = 604800,
    scan_count: int = -1
) -> Dict[str, Any]:
    """
    获取个人二维码

    Args:
        access_key: AccessKey
        app_id: 微信公众号 Id（可选）
        content: 自定义参数，扫描后回调（可选）
        second: 二维码有效期（单位秒），默认7天，最长30天
        scan_count: 可扫码次数，范围1-999次，-1代表无限次

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": {
                "qrCodeImgUrl": "二维码图片地址"
            }
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_second = _validate_positive_int("second", second)
    if validated_second > MAX_TOPIC_QRCODE_SECOND:
        raise ValueError(f"second 不能大于 {MAX_TOPIC_QRCODE_SECOND}")
    if not isinstance(scan_count, int):
        raise ValueError("scan_count 必须为整数")
    if scan_count != -1 and not 1 <= scan_count <= 999:
        raise ValueError("scan_count 仅支持 -1 或 1-999")
    params = f"second={validated_second}&scanCount={scan_count}"
    if app_id:
        params += f"&appId={app_id}"
    if content:
        params += f"&content={content}"
    url = f"{OPENAPI_BASE_URL}/open/friend/getQrCode?{params}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def list_friends(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取好友列表

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        好友列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/friend/list"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def delete_friend(access_key: str, friend_id: int) -> Dict[str, Any]:
    """
    删除好友

    Args:
        access_key: AccessKey
        friend_id: 好友 id

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": null
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("friend_id", friend_id)
    url = f"{OPENAPI_BASE_URL}/open/friend/deleteFriend?friendId={validated_id}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def edit_friend_remark(access_key: str, friend_id: int, remark: str) -> Dict[str, Any]:
    """
    修改好友备注

    Args:
        access_key: AccessKey
        friend_id: 好友编号
        remark: 好友备注

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": null
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("friend_id", friend_id)
    validated_remark = _validate_non_empty_text("remark", remark)
    url = f"{OPENAPI_BASE_URL}/open/friend/editRemark"
    payload = {"id": validated_id, "remark": validated_remark}
    return _make_request(url, payload, validated_access_key)


# ==================== 预处理信息接口 ====================


def list_pre_info(access_key: str, current: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """
    获取预处理信息列表

    注：预处理信息功能需开通会员才能使用。

    Args:
        access_key: AccessKey
        current: 当前页码，默认1
        page_size: 每页大小，最大50，默认20

    Returns:
        预处理信息列表
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    _validate_page_params(current, page_size)
    url = f"{OPENAPI_BASE_URL}/open/pre/list"
    payload = {"current": current, "pageSize": page_size}
    return _make_request(url, payload, validated_access_key)


def get_pre_info_detail(access_key: str, pre_id: int) -> Dict[str, Any]:
    """
    获取预处理信息详情

    Args:
        access_key: AccessKey
        pre_id: 预处理信息编号

    Returns:
        预处理信息详情
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("pre_id", pre_id)
    url = f"{OPENAPI_BASE_URL}/open/pre/detail?preId={validated_id}"
    return _make_request(url, method="GET", access_key=validated_access_key)


def add_pre_info(
    access_key: str,
    content: str,
    pre_name: str,
    pre_code: str,
    content_type: int
) -> Dict[str, Any]:
    """
    新增预处理信息

    注：需开通会员才能使用。

    Args:
        access_key: AccessKey
        content: 预处理代码
        pre_name: 预处理名称
        pre_code: 预处理编码
        content_type: 编程语言类型，1-JavaScript

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": 1  # 新建预处理信息编号
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_content = _validate_non_empty_text("content", content)
    validated_name = _validate_non_empty_text("pre_name", pre_name)
    validated_code = _validate_non_empty_text("pre_code", pre_code)
    url = f"{OPENAPI_BASE_URL}/open/pre/add"
    payload = {
        "content": validated_content,
        "preName": validated_name,
        "preCode": validated_code,
        "contentType": content_type
    }
    return _make_request(url, payload, validated_access_key)


def edit_pre_info(
    access_key: str,
    pre_id: int,
    content: str,
    pre_name: str,
    pre_code: str,
    content_type: int
) -> Dict[str, Any]:
    """
    修改预处理信息

    注：需开通会员才能使用。

    Args:
        access_key: AccessKey
        pre_id: 预处理信息编号
        content: 预处理代码
        pre_name: 预处理名称
        pre_code: 预处理编码
        content_type: 编程语言类型，1-JavaScript

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "修改成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("pre_id", pre_id)
    validated_content = _validate_non_empty_text("content", content)
    validated_name = _validate_non_empty_text("pre_name", pre_name)
    validated_code = _validate_non_empty_text("pre_code", pre_code)
    url = f"{OPENAPI_BASE_URL}/open/pre/edit"
    payload = {
        "id": validated_id,
        "content": validated_content,
        "preName": validated_name,
        "preCode": validated_code,
        "contentType": content_type
    }
    return _make_request(url, payload, validated_access_key)


def delete_pre_info(access_key: str, pre_id: int) -> Dict[str, Any]:
    """
    删除预处理信息

    注：需开通会员才能使用。

    Args:
        access_key: AccessKey
        pre_id: 预处理信息编号

    Returns:
        {
            "code": 200,
            "msg": "执行成功",
            "data": "删除成功"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_id = _validate_positive_int("pre_id", pre_id)
    url = f"{OPENAPI_BASE_URL}/open/pre/delete?preId={validated_id}"
    return _make_request(url, method="DELETE", access_key=validated_access_key)


def test_pre_code(
    access_key: str,
    content: str,
    content_type: int,
    message: str
) -> Dict[str, Any]:
    """
    测试预处理代码

    注：需开通会员才能使用。

    Args:
        access_key: AccessKey
        content: 预处理代码
        content_type: 编程语言类型，1-JavaScript
        message: 测试消息内容

    Returns:
        {
            "code": 200,
            "msg": "请求成功",
            "data": "预处理后的消息内容"
        }
    """
    validated_access_key = _validate_non_empty_text("access_key", access_key)
    validated_content = _validate_non_empty_text("content", content)
    validated_message = _validate_non_empty_text("message", message)
    url = f"{OPENAPI_BASE_URL}/open/pre/test"
    payload = {
        "content": validated_content,
        "contentType": content_type,
        "message": validated_message
    }
    return _make_request(url, payload, validated_access_key)


# ==================== 内部工具函数 ====================

def _make_request(
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    access_key: Optional[str] = None,
    method: str = "POST"
) -> Dict[str, Any]:
    """
    发送 HTTP 请求（内部函数）
    
    Args:
        url: 请求 URL
        payload: 请求体数据（POST/PUT 请求）
        access_key: AccessKey（用于在请求头中设置）
        method: 请求方法，默认 POST
        
    Returns:
        API 返回的 JSON 数据
    """
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PushPlus-OpenAPI-Python/1.0"
    }
    
    # 设置 AccessKey
    if access_key:
        headers["access-key"] = access_key
    
    # 准备请求数据
    data = None
    if payload and method in ["POST", "PUT"]:
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    
    # 创建请求
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP 错误: {e.code}"
        try:
            error_body = json.loads(e.read().decode('utf-8'))
            error_msg += f" - {error_body.get('msg', '')}"
        except:
            pass
        raise Exception(error_msg)
    except urllib.error.URLError as e:
        raise Exception(f"URL 错误: {e.reason}")
    except Exception as e:
        raise Exception(f"请求失败: {str(e)}")


# ==================== 便捷函数 ====================

def get_access_key_from_env() -> Dict[str, Any]:
    """
    从环境变量获取 AccessKey
    
    需要设置环境变量:
    - PUSHPLUS_USER_TOKEN
    - PUSHPLUS_SECRET_KEY
    
    Returns:
        AccessKey 响应数据
    """
    return get_access_key()


if __name__ == "__main__":
    print("PushPlus OpenAPI 客户端")
    print("请使用以下函数：")
    print("  [认证] get_access_key(user_token, secret_key)")
    print("  [消息] list_messages(access_key) / get_message_result(access_key, short_code) / delete_message(access_key, short_code) / get_message_detail(access_key, short_code)")
    print("  [用户] get_user_token(access_key) / get_user_info(access_key) / get_limit_time(access_key) / get_send_count(access_key)")
    print("  [Token] list_tokens(access_key) / add_token(access_key, name) / edit_token(access_key, id, name) / delete_token(access_key, id) / select_token_list(access_key)")
    print("  [群组] list_topics(access_key) / get_topic_detail(access_key, topic_id) / get_join_topic_detail(access_key, topic_id) / add_topic(access_key, ...) / edit_topic(access_key, ...) / get_topic_qrcode(access_key, topic_id) / exit_topic(access_key, topic_id) / delete_topic(access_key, topic_id) / set_topic_is_open(access_key, topic, is_open)")
    print("  [群组用户] list_topic_subscribers(access_key, topic_id) / delete_topic_user(access_key, id) / edit_topic_user_remark(access_key, user_id, remark)")
    print("  [渠道配置] list_webhooks(access_key) / get_webhook_detail(access_key, id) / add_webhook(access_key, ...) / edit_webhook(access_key, ...)")
    print("  [渠道配置] list_mp_channels(access_key) / list_cp_channels(access_key) / list_mail_channels(access_key) / get_mail_channel_detail(access_key, id)")
    print("  [ClawBot] get_clawbot_qrcode(access_key) / get_clawbot_qrcode_status(access_key, qrcode) / get_clawbot_bind_info(access_key) / unbind_clawbot(access_key) / get_clawbot_messages(access_key)")
    print("  [功能设置] list_default_settings(access_key) / get_default_setting_detail(access_key, id) / add_default_setting(access_key, ...) / edit_default_setting(access_key, ...) / delete_default_setting(access_key, id)")
    print("  [功能设置] set_receive_limit(access_key, limit) / set_send_enabled(access_key, is_send) / set_open_message_type(access_key, type) / set_extension_forward(access_key, forward)")
    print("  [好友] get_personal_qrcode(access_key) / list_friends(access_key) / delete_friend(access_key, friend_id) / edit_friend_remark(access_key, friend_id, remark)")
    print("  [预处理] list_pre_info(access_key) / get_pre_info_detail(access_key, id) / add_pre_info(access_key, ...) / edit_pre_info(access_key, ...) / delete_pre_info(access_key, id) / test_pre_code(access_key, ...)")
