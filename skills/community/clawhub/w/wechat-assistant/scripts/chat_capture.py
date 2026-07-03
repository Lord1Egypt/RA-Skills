#!/usr/bin/env python3
"""
微信聊天记录抓取脚本
使用uiautomation库自动抓取微信聊天窗口中的聊天记录
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import uiautomation as auto
except ImportError:
    print(json.dumps({
        "status": "error",
        "error": "uiautomation库未安装，请运行: pip install uiautomation"
    }, ensure_ascii=False))
    sys.exit(1)


class WeChatCapture:
    def __init__(self):
        self.wechat_window = None
        self.chat_window = None
        
    def find_wechat_window(self):
        """查找微信主窗口"""
        try:
            self.wechat_window = auto.WindowControl(
                searchDepth=1,
                Name="微信"
            )
            if self.wechat_window.Exists(maxSearchSeconds=5):
                self.wechat_window.SetTopmost(True)
                return True
            return False
        except Exception as e:
            return False
    
    def find_chat_by_contact(self, contact_name):
        """根据联系人名称查找聊天窗口"""
        try:
            # 点击搜索按钮
            search_button = self.wechat_window.ButtonControl(
                Name="搜索"
            )
            if search_button.Exists():
                search_button.Click()
            
            # 输入联系人名称
                search_box = self.wechat_window.EditControl(Name="搜索")
            if search_box.Exists():
                search_box.SetValue(contact_name)
                auto.Sleep(0.5)
                
                # 点击搜索结果
                contact_item = self.wechat_window.ListItemControl(
                    Name=contact_name,
                    SubName=""
                )
                if contact_item.Exists(maxSearchSeconds=3):
                    contact_item.Click()
                    auto.Sleep(0.5)
                    return True
            return False
        except Exception as e:
            return False
    
    def capture_messages(self, count=100):
        """抓取聊天记录"""
        messages = []
        try:
            # 定位消息列表区域
            message_area = self.wechat_window.ListControl(
                Name="消息"
            )
            
            if not message_area.Exists():
                # 尝试滚动区域
                scroll_area = self.wechat_window.ScrollViewerControl()
                if scroll_area.Exists():
                    message_area = scroll_area
                else:
                    return messages
            
            # 获取所有消息项
            items = message_area.GetChildren()
            
            for i, item in enumerate(items[-count:] if len(items) > count else items):
                try:
                    msg_text = ""
                    msg_time = ""
                    is_from_me = False
                    
                    # 判断消息方向
                    if "右侧" in str(item.ControlType) or item.GetRuntimeId()[-1] > 500:
                        is_from_me = True
                    
                    # 提取文本内容
                    text_controls = item.GetChildren()
                    for ctrl in text_controls:
                        if ctrl.Name and len(ctrl.Name) > 0:
                            if ":" in ctrl.Name or "上午" in ctrl.Name or "下午" in ctrl.Name:
                                # 时间戳格式
                                msg_time = ctrl.Name.split(" ")[-1] if " " in ctrl.Name else ctrl.Name
                            elif len(ctrl.Name) > 3:
                                msg_text = ctrl.Name
                                break
                    
                    if msg_text:
                        messages.append({
                            "content": msg_text,
                            "time": msg_time,
                            "is_from_me": is_from_me,
                            "contact": "current"
                        })
                        
                except Exception:
                    continue
            
            return messages
            
        except Exception as e:
            return messages
    
    def run(self, contact, count, output):
        """执行抓取"""
        result = {
            "status": "success",
            "contact": contact,
            "count": 0,
            "messages": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 查找微信窗口
        if not self.find_wechat_window():
            result["status"] = "error"
            result["error"] = "无法找到微信窗口，请确保微信已打开"
            print(json.dumps(result, ensure_ascii=False))
            return
        
        # 查找联系人
        if not self.find_chat_by_contact(contact):
            result["status"] = "error"
            result["error"] = f"无法找到联系人: {contact}"
            print(json.dumps(result, ensure_ascii=False))
            return
        
        # 抓取消息
        messages = self.capture_messages(count)
        result["messages"] = messages
        result["count"] = len(messages)
        
        # 保存到文件
        if output:
            try:
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                result["file_saved"] = output
            except Exception as e:
                result["save_error"] = str(e)
        
        print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='微信聊天记录抓取工具')
    parser.add_argument('--contact', required=True, help='联系人名称')
    parser.add_argument('--count', type=int, default=100, help='抓取消息数量')
    parser.add_argument('--output', required=True, help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    capturer = WeChatCapture()
    capturer.run(args.contact, args.count, args.output)


if __name__ == "__main__":
    main()
