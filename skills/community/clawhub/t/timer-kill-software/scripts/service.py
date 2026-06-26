import sys
import json
import hashlib
import subprocess
import time
from datetime import datetime, timedelta
import urllib.request
import urllib.error

from file_utils import load_order

GET_RESULT_URL = "http://119.29.236.244:8080/api/service/execute"

# 硬编码的skill-name，与 create_order.py 保持一致
SKILL_NAME = "timer-kill-software"


def compute_indicator(skill_name: str) -> str:
    """根据 skill-name 计算 MD5 作为 indicator。"""
    return hashlib.md5(skill_name.encode("utf-8")).hexdigest()


# 软件类别对应的进程名
SOFTWARE_PROCESSES = {
    "游戏软件": [
        "steam", "steamservice", "steamwebhelper",
        "EpicGamesLauncher", "EpicWebHelper",
        "WeGame", "WeGameBootstrap",
        "League of Legends", "LeagueClient",
        "dota2", "csgo",
        "Minecraft", "javaw",
    ],
    "办公软件": [
        "WINWORD", "EXCEL", "POWERPNT", "OUTLOOK", "ONENOTE",
        "wps", "et", "wpp",
        "Acrobat", "AcroRd32", "FoxitReader",
        "notepad++", "Notepad++",
        "Teams", "Slack",
    ],
    "聊天软件": [
        "QQ", "WeChat", "DingTalk",
        "TIM", "QQMail",
        "Telegram", "Discord",
    ],
    "娱乐软件": [
        "Spotify", "QQMusic", "CloudMusic",
        "vlc", "PotPlayer",
        "TencentVideo", "iQiyi",
    ],
    "全部": []  # 全部类别需要合并所有软件
}


def get_all_processes():
    """获取所有需要关闭的软件进程列表"""
    all_processes = []
    for category in SOFTWARE_PROCESSES:
        if category != "全部":
            all_processes.extend(SOFTWARE_PROCESSES[category])
    # 去重
    return list(set(all_processes))


def parse_time_to_seconds(time_str: str) -> int:
    """
    解析时间字符串为延迟秒数
    """
    time_str = time_str.strip()
    
    # 尝试解析为纯数字（秒数）
    try:
        return int(time_str)
    except ValueError:
        pass
    
    # 尝试解析为时间格式 HH:MM
    try:
        target_time = datetime.strptime(time_str, "%H:%M")
        now = datetime.now()
        
        # 如果目标时间已过，计算到第二天
        target_datetime = now.replace(
            hour=target_time.hour,
            minute=target_time.minute,
            second=0,
            microsecond=0
        )
        
        if target_datetime <= now:
            target_datetime += timedelta(days=1)
        
        delay = (target_datetime - now).total_seconds()
        return int(delay)
    except ValueError:
        return 0  # 无效格式，返回 0（立即执行）


def kill_software(process_names: list, delay_seconds: int = 0) -> dict:
    """
    关闭指定的软件进程
    """
    # 如果有延迟，等待指定时间
    if delay_seconds > 0:
        time.sleep(delay_seconds)
    
    killed = []
    failed = []
    
    for process_name in process_names:
        try:
            # 使用 PowerShell 关闭进程
            result = subprocess.run(
                ["powershell", "-Command", f"Stop-Process -Name '{process_name}' -Force -ErrorAction SilentlyContinue"],
                capture_output=True,
                text=True,
                timeout=5
            )
            killed.append(process_name)
        except Exception as e:
            failed.append(process_name)
    
    return {
        "killed": killed,
        "failed": failed,
        "total_killed": len(killed),
        "total_failed": len(failed),
        "delay_seconds": delay_seconds
    }


def counseling(question: str, order_no: str, credential: str, delay: str = "0") -> str:
    print(f"timer kill software category is: {question}")
    if credential is None:
        return "Please enter your counseling credential"

    payload = json.dumps({
        "question": question,
        "orderNo": order_no,
        "credential": credential,
        "delay": delay
    }).encode("utf-8")

    req = urllib.request.Request(
        GET_RESULT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8")).get("resultData")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Counseling request failed: {e}") from e

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"Counseling failed: {body.get('responseMessage', 'unknown error')}"
        )

    pay_status = body.get("payStatus")
    print(f"PAY_STATUS: {pay_status}")

    answer = body.get("answer")
    if not answer and "ERROR" == pay_status:
        # 避免 key 不存在时报错
        raise RuntimeError(f'获取信息失败：原因：{body.get("errorInfo", "未知错误")}')
    return answer


import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get timer kill software service")
    parser.add_argument("order_no", help="Order number")
    parser.add_argument("--delay", default="0", help="Delay in seconds or time (HH:MM)")
    args = parser.parse_args()

    indicator = compute_indicator(SKILL_NAME)

    try:
        order_data = load_order(indicator, args.order_no)
        question = order_data.get("question")
        if not question:
            raise RuntimeError("订单文件中缺少 question 字段")
        credential = order_data.get("payCredential")
        if not credential:
            raise RuntimeError("订单文件中缺少 payCredential 字段")
        
        # 解析延迟时间
        delay_seconds = parse_time_to_seconds(args.delay)
        delay_str = str(delay_seconds)
        
        # 调用服务端验证
        result = counseling(question, args.order_no, credential, delay_str)
        
        # 获取要关闭的软件列表
        if question == "全部":
            process_list = get_all_processes()
        else:
            process_list = SOFTWARE_PROCESSES.get(question, [])
        
        # 执行关闭操作
        if delay_seconds > 0:
            target_time = datetime.now() + timedelta(seconds=delay_seconds)
            target_str = target_time.strftime("%H:%M")
            print(f"已设置定时关闭，将在 {delay_seconds} 秒后（{target_str}）执行...")
        
        kill_result = kill_software(process_list, delay_seconds)
        
        # 输出结果
        if kill_result["total_failed"] == 0:
            print(f"已关闭 {kill_result['total_killed']} 个软件进程")
            if kill_result["killed"]:
                print(f"已关闭: {', '.join(kill_result['killed'])}")
        else:
            print(f"关闭完成: 成功 {kill_result['total_killed']} 个，失败 {kill_result['total_failed']} 个")
            if kill_result["killed"]:
                print(f"已关闭: {', '.join(kill_result['killed'])}")
            if kill_result["failed"]:
                print(f"失败: {', '.join(kill_result['failed'])}")
                
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
