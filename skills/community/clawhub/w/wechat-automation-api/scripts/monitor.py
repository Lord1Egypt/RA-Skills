"""
微信掉线独立监控进程
由 app.py 拉起，负责定期检查微信窗口状态并通过 WPush 发送通知
"""
import os
import sys
import json
import time
import logging
import requests
import uiautomation as auto
from wechat_controller import WeChatController

# 获取项目根目录绝对路径
def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
def setup_logging(config):
    log_level = config.get('log_level', 'INFO')
    log_file_name = config.get('log_file', 'wechat_automation.log')
    log_file = os.path.join(get_project_root(), log_file_name)
    
    # 避免日志冲突，这里我们可以复用同一个日志文件，也可以分开。复用时要注意多进程写入问题
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - [Monitor] %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# 加载配置
def load_config():
    config_file = os.path.join(get_project_root(), 'config.json')
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"配置文件 {config_file} 不存在")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# 发送 WPush 通知
def send_wpush_notification(config, logger):
    wpush_config = config.get('wpush', {})
    apikey = wpush_config.get('apikey')
    
    if not apikey or apikey == '你的apikey':
        logger.warning("未配置有效的 WPush apikey，跳过通知发送。")
        return False
        
    url = "https://api.wpush.cn/api/v1/send"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "apikey": apikey,
        "title": wpush_config.get('title', '微信监控通知'),
        "content": wpush_config.get('content', '微信可能已掉线。')
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"WPush 通知发送成功: {response.text}")
        return True
    except Exception as e:
        logger.error(f"WPush 通知发送失败: {str(e)}")
        return False

def main():
    try:
        config = load_config()
    except Exception as e:
        print(f"Monitor 加载配置失败: {e}")
        return

    logger = setup_logging(config)
    
    monitor_interval = config.get('monitor_interval', 0)
    if monitor_interval <= 0:
        logger.info("monitor_interval 为 0，监控进程退出。")
        return
        
    monitor_max_retries = config.get('monitor_max_retries', 3)
    
    logger.info(f"监控进程已启动 (检查间隔: {monitor_interval}s, 最大通知次数: {monitor_max_retries})")
    
    # 初始化
    wechat_controller = WeChatController()
    fail_count = 0  # 连续获取失败的次数
    
    while True:
        try:
            logger.debug("开始检查微信窗口状态...")
            # 尝试获取微信窗口
            wx_window = wechat_controller._get_wechat_window()
            
            if wx_window:
                logger.debug("微信窗口状态: 正常在线")
                # 获取成功，重置失败次数
                if fail_count > 0:
                    logger.info("微信窗口已恢复，重置失败计数。")
                fail_count = 0
            else:
                # 获取失败
                fail_count += 1
                logger.warning(f"无法获取微信窗口，当前失败次数: {fail_count}/{monitor_max_retries}")
                
                if fail_count <= monitor_max_retries:
                    # 发送通知
                    logger.info(f"正在发送第 {fail_count} 次掉线通知...")
                    send_wpush_notification(config, logger)
                else:
                    # 超过最大次数
                    logger.info(f"连续失败次数({fail_count}) 已超过最大通知次数({monitor_max_retries})，静默等待恢复...")
                    
        except Exception as e:
            logger.error(f"监控循环发生异常: {str(e)}", exc_info=True)
            
        # 休眠到下一次检查
        time.sleep(monitor_interval)

if __name__ == '__main__':
    # 确保在正确初始化 COM 后运行
    with auto.UIAutomationInitializerInThread():
        main()
