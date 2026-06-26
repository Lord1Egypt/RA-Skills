#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信批量发送脚本 - 每次只发送给一个人
使用方法：python send_batch.py "[王沛，高哲，贾福果]" "消息内容"
联系人格式必须为 [A,B,C] 格式
"""

import sys
import os
import re
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import send_message_to_contact, send_message_skip_steps, get_queue_file, load_queue, save_queue, clear_queue


def load_test_config():
    """加载测试配置"""
    config_file = os.path.join(os.path.dirname(__file__), "test_config.json")
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"test_mode": False, "test_contact": None}


def parse_contacts(contacts_str):
    """解析联系人列表，必须为 [A,B,C] 格式"""
    # 检查是否为 [A,B,C] 格式
    match = re.match(r'^\[(.+)\]$', contacts_str.strip())
    if not match:
        return None
    
    # 提取括号内的内容
    inner = match.group(1)
    
    # 按逗号或顿号分割（支持中文逗号、英文逗号、顿号）
    contacts = [c.strip() for c in inner.replace("，", ",").replace("、", ",").split(",") if c.strip()]
    
    return contacts if contacts else None


def main():
    if len(sys.argv) < 2:
        print("用法：python send_batch.py \"[联系人 1，联系人 2,...]\" \"消息内容\"")
        print("注意：联系人格式必须为 [A,B,C] 格式，例如：[王沛，高哲，贾福果]")
        sys.exit(1)
    
    queue_file = get_queue_file()
    
    # 加载测试配置
    test_config = load_test_config()
    test_mode = test_config.get("test_mode", False)
    test_contact = test_config.get("test_contact", "张璞")
    
    # 检查是否是继续发送
    if sys.argv[1] == "--next":
        queue_data = load_queue()
        if queue_data.get("current_index", 0) >= len(queue_data.get("contacts", [])):
            print("[DONE] 所有消息已发送完成")
            return
        
        contacts = queue_data["contacts"]
        message = queue_data["message"]
    else:
        if len(sys.argv) < 3:
            print("错误：需要指定联系人列表和消息内容")
            print("用法：python send_batch.py \"[王沛，高哲]\" \"消息内容\"")
            sys.exit(1)
        
        # 解析参数
        contacts_str = sys.argv[1]
        message = sys.argv[2]
        
        # 验证并解析联系人格式
        contacts = parse_contacts(contacts_str)
        
        if contacts is None:
            print("错误：请输入正确的发送人格式")
            print("正确格式：[王沛，高哲，贾福果]")
            print("示例：python send_batch.py \"[王沛，高哲]\" \"消息内容\"")
            sys.exit(1)
        
        if len(contacts) < 1:
            print("错误：需要指定联系人列表")
            sys.exit(1)
        
        # 测试模式：统一替换为测试联系人（保持数量）
        if test_mode:
            print(f"\n[测试模式] 所有消息将发送给：{test_contact}")
            original_contacts = contacts
            contacts = [test_contact for _ in contacts]  # 保持相同数量
            print(f"[测试模式] 原始联系人：{original_contacts} → 实际发送：{contacts} (共{len(contacts)}条)")
            print(f"[测试模式] 第 1 条执行 Step 1-7，后续执行 Step 2-7\n")
        
        # 初始化队列
        queue_data = {
            "contacts": contacts,
            "message": message,
            "current_index": 0,
            "test_mode": test_mode
        }
        save_queue(queue_data)
        print(f"[INIT] 初始化队列：{len(contacts)} 个联系人")
    
    # 检查是否完成
    if queue_data["current_index"] >= len(queue_data["contacts"]):
        clear_queue()
        print("[DONE] 所有消息已发送完成")
        return
    
    # 获取当前要发送的联系人
    current_contact = queue_data["contacts"][queue_data["current_index"]]
    total = len(queue_data["contacts"])
    current_num = queue_data["current_index"] + 1
    is_first = (current_num == 1)
    is_last = (current_num == total)
    
    print(f"\n{'='*50}")
    print(f"正在发送给 [{current_num}/{total}]: {current_contact}")
    print(f"{'='*50}\n")
    
    # 根据位置决定执行逻辑
    total_contacts = len(queue_data["contacts"])
    
    if total_contacts == 1:
        # 只有一个人：执行完整流程 (Step 1-7)
        print("[模式] 单人发送 - 执行完整流程 (Step 1-7)")
        success, err = send_message_to_contact(current_contact, message)
    elif is_first:
        # 多个人中的第一个：执行完整流程 (Step 1-7)
        print("[模式] 多人发送 - 第一个人 - 执行完整流程 (Step 1-7)")
        success, err = send_message_to_contact(current_contact, message)
    elif is_last:
        # 多个人中的最后一个：执行 Step 2-7（跳过打开微信）
        print("[模式] 多人发送 - 最后一个人 - 执行 Step 2-7")
        success, err = send_message_skip_steps(current_contact, message, skip_open_wechat=True)
    else:
        # 多个人中的中间：执行 Step 2-7（跳过打开微信）
        print("[模式] 多人发送 - 中间 - 执行 Step 2-7")
        success, err = send_message_skip_steps(current_contact, message, skip_open_wechat=True)
    
    if success:
        # 更新索引
        queue_data["current_index"] += 1
        save_queue(queue_data)
        
        remaining = len(queue_data["contacts"]) - queue_data["current_index"]
        if remaining > 0:
            next_contact = queue_data["contacts"][queue_data["current_index"]]
            print(f"\n[OK] 已发送给 {current_contact}")
            print(f"[REMAINING] 剩余：{remaining} 人 (下一个：{next_contact})")
            print(f"[NEXT] 运行 'python send_batch.py --next' 继续发送")
        else:
            clear_queue()
            print(f"\n[OK] 已发送给 {current_contact}")
            print(f"[DONE] 所有消息已发送完成")
    else:
        print(f"\n[ERROR] 发送给 {current_contact} 失败：{err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
