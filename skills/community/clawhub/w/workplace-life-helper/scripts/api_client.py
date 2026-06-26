#!/usr/bin/env python3
"""
职场+生活全能助手 - API调用客户端
处理支付宝AI收(A2M)支付流程和API调用
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

# 配置
API_BASE_URL = "https://w4h8ghmxcv.coze.site"
SERVICE_PRICE = 0.10  # 元/次


def call_api(endpoint: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    调用职场助手API
    
    Args:
        endpoint: API端点路径 (如 "bahe/jianli", "zufang/contract")
        body: 请求体字典
    
    Returns:
        API响应字典
    
    Raises:
        PaymentRequired: 需要支付时抛出
        APIError: API调用失败时抛出
    """
    url = f"{API_BASE_URL}/api/v1/skill/{endpoint}"
    
    # 构建请求
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except urllib.error.HTTPError as e:
        if e.code == 402:
            # 支付需要 - 支付宝AI收
            error_body = json.loads(e.read().decode('utf-8'))
            raise PaymentRequired(
                f"该服务需要支付 {SERVICE_PRICE} 元",
                payment_info=error_body
            )
        else:
            raise APIError(f"API调用失败: HTTP {e.code}", details=e.read().decode('utf-8'))
            
    except urllib.error.URLError as e:
        raise APIError(f"网络连接失败: {str(e)}")
    except Exception as e:
        raise APIError(f"未知错误: {str(e)}")


class PaymentRequired(Exception):
    """需要支付异常"""
    def __init__(self, message: str, payment_info: Optional[Dict] = None):
        super().__init__(message)
        self.payment_info = payment_info or {}


class APIError(Exception):
    """API错误异常"""
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message)
        self.details = details


def format_result(result: Dict[str, Any], endpoint: str = "") -> str:
    """
    格式化API结果为易读的文本
    
    实际API统一返回格式:
    {
        "success": true,
        "message": "操作成功",
        "data": {"content": "..."} 或 {"report": "..."} 等,
        "credits_used": 10,
        "disclaimer": "..."
    }
    
    Args:
        result: API返回的原始字典
        endpoint: 端点路径，用于判断格式化方式
    
    Returns:
        格式化后的文本
    """
    # 检查是否有错误
    if not result.get("success", True):
        return f"❌ 操作失败: {result.get('error', result.get('message', '未知错误'))}"
    
    # 提取数据
    data = result.get("data", {})
    disclaimer = result.get("disclaimer", "")
    
    # 根据端点类型格式化
    endpoint_group = endpoint.split("/")[0] if "/" in endpoint else ""
    
    if endpoint_group == "zufang":
        return format_zufang_result(data, endpoint, disclaimer)
    elif endpoint_group == "xianyu":
        return format_xianyu_result(data, endpoint, disclaimer)
    elif endpoint_group == "bahe":
        return format_bahe_result(data, endpoint, disclaimer)
    elif endpoint_group == "comply":
        return format_comply_result(data, endpoint, disclaimer)
    else:
        # 通用格式化
        output = json.dumps(data, ensure_ascii=False, indent=2)
        if disclaimer:
            output += f"\n\n⚠️ {disclaimer}"
        return output


def format_zufang_result(data: Dict, endpoint: str, disclaimer: str) -> str:
    """格式化租房避坑结果"""
    if "/contract" in endpoint:
        output = "🔍 **租房合同审查结果**\n\n"
    elif "/deposit" in endpoint:
        output = "💰 **押金计算结果**\n\n"
    elif "/document" in endpoint:
        output = "📝 **法律文书生成**\n\n"
    elif "/complaint" in endpoint:
        output = "🛡️ **维权建议**\n\n"
    else:
        output = "🏠 **租房避坑助手**\n\n"
    
    # data中的内容可能是 content/report/guide/document 等
    content = (data.get("content") or data.get("report") or 
               data.get("guide") or data.get("document") or 
               json.dumps(data, ensure_ascii=False, indent=2))
    output += str(content)
    
    if disclaimer:
        output += f"\n\n⚠️ {disclaimer}"
    return output


def format_xianyu_result(data: Dict, endpoint: str, disclaimer: str) -> str:
    """格式化闲鱼助手结果"""
    if "/describe" in endpoint:
        output = "✍️ **商品文案**\n\n"
    elif "/price" in endpoint:
        output = "💰 **定价建议**\n\n"
    elif "/negotiate" in endpoint:
        output = "🤝 **谈判话术**\n\n"
    elif "/antiscam" in endpoint:
        output = "🛡️ **防骗识别**\n\n"
    else:
        output = "🛒 **闲鱼助手**\n\n"
    
    content = (data.get("content") or data.get("price_guide") or 
               data.get("tactics") or data.get("risk_analysis") or 
               json.dumps(data, ensure_ascii=False, indent=2))
    output += str(content)
    
    if disclaimer:
        output += f"\n\n⚠️ {disclaimer}"
    return output


def format_bahe_result(data: Dict, endpoint: str, disclaimer: str) -> str:
    """格式化职场赋能结果"""
    if "/qingxing" in endpoint:
        output = "💡 **清醒搭子**\n\n"
    elif "/jianli" in endpoint:
        output = "📝 **简历优化结果**\n\n"
    elif "/shemei" in endpoint:
        output = "📱 **社媒文案**\n\n"
    elif "/dianshang" in endpoint:
        output = "🛍️ **电商文案**\n\n"
    elif "/zhoubao" in endpoint:
        output = "📊 **周报/月报**\n\n"
    elif "/aitools" in endpoint:
        output = "🔧 **AI工具推荐**\n\n"
    else:
        output = "💼 **职场助手**\n\n"
    
    content = (data.get("content") or json.dumps(data, ensure_ascii=False, indent=2))
    output += str(content)
    
    if disclaimer:
        output += f"\n\n⚠️ {disclaimer}"
    return output


def format_comply_result(data: Dict, endpoint: str, disclaimer: str) -> str:
    """格式化内容合规检测结果"""
    if "/wechat" in endpoint:
        output = "✅ **公众号文章合规检测**\n\n"
    elif "/douyin" in endpoint:
        output = "✅ **抖音短视频合规检测**\n\n"
    elif "/xiaohongshu" in endpoint:
        output = "✅ **小红书笔记合规检测**\n\n"
    elif "/ecommerce" in endpoint:
        output = "✅ **电商详情页合规检测**\n\n"
    elif "/ad" in endpoint:
        output = "✅ **广告文案合规检测**\n\n"
    elif "/general" in endpoint:
        output = "✅ **通用文本合规检测**\n\n"
    else:
        output = "✅ **内容合规检测**\n\n"
    
    report = data.get("report", "")
    if report:
        # 尝试解析JSON格式的报告
        try:
            if isinstance(report, str):
                report_data = json.loads(report)
                output += format_comply_report(report_data)
            else:
                output += format_comply_report(report)
        except:
            output += str(report)
    else:
        output += json.dumps(data, ensure_ascii=False, indent=2)
    
    if disclaimer:
        output += f"\n\n⚠️ {disclaimer}"
    return output


def format_comply_report(report: Dict) -> str:
    """格式化合规检测报告"""
    risk_level = report.get("risk_level", "未知")
    total_issues = report.get("total_issues", 0)
    issues = report.get("issues", [])
    passed = report.get("pass", True)
    summary = report.get("summary", "")
    
    # 风险等级emoji
    risk_emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(risk_level, "⚪")
    
    output = f"{risk_emoji} 风险等级：{risk_level}\n"
    output += f"📊 问题数量：{total_issues} 个\n"
    output += f"✅ 通过状态：{'通过' if passed else '未通过'}\n\n"
    
    if issues:
        output += "📋 **问题详情：**\n"
        for i, issue in enumerate(issues, 1):
            issue_type = issue.get("type", "其他")
            content = issue.get("content", "")
            suggestion = issue.get("suggestion", "")
            output += f"\n{i}. 【{issue_type}】\n"
            output += f"   问题：{content}\n"
            if suggestion:
                output += f"   建议：{suggestion}\n"
    
    if summary:
        output += f"\n📝 **总体评估：**\n{summary}\n"
    
    return output


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python api_client.py <endpoint> <json_body>")
        print("示例: python api_client.py 'bahe/jianli' '{\"resume_text\": \"...\"}'")
        sys.exit(1)
    
    endpoint = sys.argv[1]
    try:
        body = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        sys.exit(1)
    
    try:
        result = call_api(endpoint, body)
        formatted = format_result(result, endpoint)
        print(formatted)
    except PaymentRequired as e:
        print(f"💳 {e}")
        print(f"\n支付信息: {json.dumps(e.payment_info, ensure_ascii=False, indent=2)}")
        sys.exit(1)
    except APIError as e:
        print(f"❌ API错误: {e}")
        if e.details:
            print(f"详情: {e.details}")
        sys.exit(1)


if __name__ == "__main__":
    main()
