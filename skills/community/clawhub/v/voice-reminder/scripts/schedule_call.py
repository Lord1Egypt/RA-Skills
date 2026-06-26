#!/usr/bin/env python3
"""
定时外呼任务调度器
支持：X分钟后、X小时后、明天下午、今天晚上等时间表达式
使用 AI 模型智能提取电话播报内容
"""
import json
import sys
import re
import os
import subprocess
from datetime import datetime, timedelta

# 通讯录
CONTACTS = {
    "季天雄": "15345602935",
    "天雄": "15345602935",
    "何天龙": "15655170806",
    "天龙": "15655170806",
}

# 任务存储文件
TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "scheduled_tasks.json")


def find_phone(contact: str) -> str:
    if contact in CONTACTS:
        return CONTACTS[contact]
    if contact.isdigit():
        return contact
    raise ValueError(f"未找到联系人：{contact}")


def extract_time_info(text: str) -> tuple[int, str, str]:
    """
    提取时间信息，返回 (延迟秒数, 时间描述, 去除时间后的文本)
    """
    now = datetime.now()
    delay = 0
    time_desc = "立即"
    remaining_text = text
    
    # 中文数字映射
    cn_num_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '半': 0.5
    }
    
    # X分钟后（支持阿拉伯数字和中文数字）
    match = re.search(r'(\d+|一|二|三|四|五|六|七|八|九|十)\s*分钟后', text)
    if match:
        num_str = match.group(1)
        minutes = int(num_str) if num_str.isdigit() else cn_num_map.get(num_str, 1)
        delay = minutes * 60
        target_time = now + timedelta(minutes=minutes)
        time_desc = target_time.strftime("%H:%M")
        # 去除时间表达式
        remaining_text = re.sub(r'\d+\s*分钟后', '', remaining_text)
        remaining_text = re.sub(r'[一二三四五六七八九十]\s*分钟后', '', remaining_text)
    
    # X小时后（支持阿拉伯数字和中文数字）
    elif re.search(r'(\d+|一|二|三|四|五|六|七|八|九|十|半)\s*小时后', text):
        match = re.search(r'(\d+|一|二|三|四|五|六|七|八|九|十|半)\s*小时后', text)
        num_str = match.group(1)
        if num_str.isdigit():
            hours = int(num_str)
        else:
            hours = cn_num_map.get(num_str, 1)
        delay = int(hours * 3600)
        target_time = now + timedelta(hours=hours)
        time_desc = target_time.strftime("%H:%M")
        remaining_text = re.sub(r'\d+\s*小时后', '', remaining_text)
        remaining_text = re.sub(r'[一二三四五六七八九十半]\s*小时后', '', remaining_text)
    
    # 明天下午
    elif '明天下午' in text:
        target = now + timedelta(days=1)
        target = target.replace(hour=14, minute=0, second=0)
        delay = int((target - now).total_seconds())
        time_desc = "明天下午14:00"
        remaining_text = remaining_text.replace('明天下午', '')
    
    # 明天上午
    elif '明天上午' in text or '明天早上' in text:
        target = now + timedelta(days=1)
        target = target.replace(hour=9, minute=0, second=0)
        delay = int((target - now).total_seconds())
        time_desc = "明天上午09:00"
        remaining_text = remaining_text.replace('明天上午', '').replace('明天早上', '')
    
    # 今天晚上
    elif '今天晚上' in text or '今晚' in text:
        target = now.replace(hour=20, minute=0, second=0)
        if target < now:
            target += timedelta(days=1)
        delay = int((target - now).total_seconds())
        time_desc = "今晚20:00"
        remaining_text = remaining_text.replace('今天晚上', '').replace('今晚', '')
    
    return delay, time_desc, remaining_text.strip()


def extract_phone_content_with_ai(full_content: str) -> str:
    """
    使用简单的规则模拟 AI 判断，提取适合电话播报的内容
    去除时间描述，保留核心动作
    """
    # 去除常见的时间前缀模式
    content = full_content
    
    # 去除时间相关词汇（这些已经在 extract_time_info 中去掉了，但可能还有残留）
    time_words = ['分钟后', '小时后', '明天下午', '明天上午', '明天早上', '今天晚上', '今晚']
    for word in time_words:
        content = content.replace(word, '')
    
    # 去除数字（可能是时间数字）
    content = re.sub(r'\d+', '', content)
    
    # 去除中文数字
    cn_nums = '一二三四五六七八九十半'
    for num in cn_nums:
        content = content.replace(num, '')
    
    # 去除常见的连接词，但保留有意义的词
    # 使用更智能的判断：如果开头是动词，保留；如果是连接词，去除
    content = content.strip()
    
    # 定义需要去除的连接词
    connectors = ['去', '该', '要', '得', '需要', '应该']
    
    # 检查开头是否是连接词
    for conn in connectors:
        if content.startswith(conn):
            # 去除这个连接词
            content = content[len(conn):].strip()
            break
    
    # 如果内容为空，返回默认提示
    if not content:
        return "有事项提醒"
    
    return content


def parse_command(text: str) -> tuple[str, int, str, str, str]:
    """
    解析指令，返回 (联系人, 延迟秒数, 时间描述, 完整通知内容, 电话通知内容)
    """
    # 提取联系人
    contact = None
    for name in sorted(CONTACTS.keys(), key=len, reverse=True):
        if name in text:
            contact = name
            break
    
    if not contact:
        match = re.search(r'1[3-9]\d{9}', text)
        if match:
            contact = match.group(0)
        else:
            raise ValueError(f"未在指令中找到联系人")
    
    # 提取时间信息
    delay, time_desc, remaining_text = extract_time_info(text)
    
    # 提取完整通知内容（保留时间描述，只去掉开头词和联系人）
    # 从原始文本中去掉开头词和联系人，保留时间描述
    full_content = text
    full_content = re.sub(r'^(通知|让)\s*', '', full_content)
    full_content = full_content.replace(contact, '', 1)
    full_content = full_content.strip()
    
    if not full_content:
        full_content = "有事项提醒"
    
    # 使用 AI 模拟逻辑提取电话播报内容（去除时间描述，也去掉开头词和联系人）
    phone_content_text = remaining_text
    phone_content_text = re.sub(r'^(通知|让)\s*', '', phone_content_text)
    phone_content_text = phone_content_text.replace(contact, '', 1)
    phone_content_text = phone_content_text.strip()
    phone_content = extract_phone_content_with_ai(phone_content_text)
    
    return contact, delay, time_desc, full_content, phone_content


def get_python_executable():
    """获取可用的 Python 解释器"""
    import shutil
    if shutil.which("python3"):
        return "python3"
    if shutil.which("python"):
        return "python"
    raise RuntimeError("找不到 Python 解释器 (python3 或 python)")


def schedule_task(contact: str, phone_content: str, delay_seconds: int, time_desc: str):
    """创建定时任务，phone_content 是电话要播报的内容（不含时间）"""
    script_dir = os.path.dirname(__file__)
    main_script = os.path.join(script_dir, "main.py")
    python_exe = get_python_executable()
    
    if delay_seconds > 0:
        cmd = f"(sleep {delay_seconds} && {python_exe} {main_script} '{contact}' '{phone_content}' 0) &"
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    else:
        subprocess.run([python_exe, main_script, contact, phone_content, "0"])
        return True


def save_task(contact: str, phone: str, full_content: str, phone_content: str, delay_seconds: int, time_desc: str):
    """保存任务到文件"""
    tasks = []
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        except:
            tasks = []
    
    task = {
        "contact": contact,
        "phone": phone,
        "content": full_content,
        "phone_content": phone_content,
        "delay_seconds": delay_seconds,
        "time_desc": time_desc,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        python_exe = get_python_executable()
        print(f"用法: {python_exe} schedule_call.py '<指令>'")
        print(f"示例: {python_exe} schedule_call.py '通知天龙三分钟后去吃饭'")
        return 1
    
    command = sys.argv[1]
    
    try:
        contact, delay, time_desc, full_content, phone_content = parse_command(command)
        phone = find_phone(contact)
        
        schedule_task(contact, phone_content, delay, time_desc)
        save_task(contact, phone, full_content, phone_content, delay, time_desc)
        
        response = {
            "version": "3.0",
            "messageId": f"dispatch_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "messages": [
                {
                    "recipient": {
                        "type": "shrimp",
                        "phone": phone
                    },
                    "content": {
                        "type": "text",
                        "text": full_content
                    }
                }
            ]
        }
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return 0
        
    except ValueError as e:
        print(f"❌ 错误: {e}")
        return 1
    except Exception as e:
        print(f"❌ 系统错误: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
