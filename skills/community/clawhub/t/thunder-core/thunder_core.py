"""
Thunder 客户端核心模块
通过 COM 接口调用 ThunderAgent 下载引擎

使用前提: 已安装Thunder客户端 (Xunlei)
COM组件: ThunderAgent.ThunderAgent
安装路径: C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe
"""

import win32com.client
import pythoncom
import os
from typing import Optional, List, Dict


class ThunderCore:
    """Thunder 下载核心类"""
    
    def __init__(self):
        self._agent = None
        self._initialized = False
        self._install_path = r"C:\Program Files (x86)\Thunder Network\Thunder\Program"
    
    def _check_installed(self) -> bool:
        """检查 Thunder 是否已安装"""
        exe_path = os.path.join(self._install_path, "Thunder.exe")
        return os.path.exists(exe_path)
    
    def initialize(self) -> bool:
        """初始化 Thunder COM 组件"""
        if not self._check_installed():
            print("错误: Thunder 客户端未安装")
            print("请先安装 Thunder (https://www.xunlei.com/)")
            return False
        
        try:
            pythoncom.CoInitialize()
            self._agent = win32com.client.Dispatch("ThunderAgent.ThunderAgent")
            self._initialized = True
            return True
        except Exception as e:
            print(f"COM组件初始化失败: {e}")
            print("可能原因: Thunder 未正确注册 COM 组件")
            print("请尝试: 重新安装 Thunder 或以管理员身份运行")
            return False
    
    def add_task(self, url: str, save_path: str, 
                 refer_url: str = "", 
                 user_agent: str = "", 
                 cookie: str = "",
                 priority: int = -1,
                 custom_id: int = -1,
                 job_type: int = -1) -> bool:
        """
        添加下载任务
        
        Args:
            url: 下载链接
            save_path: 保存路径
            refer_url: Referer URL
            user_agent: User-Agent
            cookie: Cookie
            priority: 优先级
            custom_id: 自定义ID
            job_type: 任务类型
        """
        if not self._initialized:
            if not self.initialize():
                return False
        
        try:
            self._agent.AddTask(url, save_path, refer_url, user_agent, cookie, 
                               priority, custom_id, job_type)
            return True
        except Exception as e:
            print(f"添加任务失败: {e}")
            return False
    
    def commit_tasks(self) -> bool:
        """提交所有任务开始下载"""
        if not self._agent:
            return False
        
        try:
            self._agent.CommitTasks()
            return True
        except Exception as e:
            print(f"提交任务失败: {e}")
            return False
    
    def add_and_commit(self, url: str, save_path: str,
                       refer_url: str = "",
                       user_agent: str = "",
                       cookie: str = "") -> bool:
        """添加任务并立即提交"""
        if self.add_task(url, save_path, refer_url, user_agent, cookie):
            return self.commit_tasks()
        return False
    
    def cancel_all(self) -> bool:
        """取消所有任务"""
        if not self._agent:
            return False
        try:
            self._agent.CancelAllTasks()
            return True
        except Exception as e:
            print(f"取消任务失败: {e}")
            return False
    
    def get_tasks(self) -> list:
        """获取任务列表"""
        if not self._agent:
            return []
        try:
            return self._agent.GetTaskList()
        except:
            return []
    
    def close(self):
        """关闭并释放资源"""
        if self._agent:
            self._agent = None
        pythoncom.CoUninitialize()
        self._initialized = False


def download(url: str, save_path: str,
             refer_url: str = "",
             user_agent: str = "",
             cookie: str = "") -> bool:
    """
    快捷下载函数
    
    Args:
        url: 下载链接
        save_path: 保存路径
        refer_url: Referer URL
        user_agent: User-Agent
        cookie: Cookie
    
    Returns:
        bool: 是否成功
    """
    thunder = ThunderCore()
    return thunder.add_and_commit(url, save_path, refer_url, user_agent, cookie)


if __name__ == "__main__":
    # 测试
    result = download(
        url="https://ollama.com/download/OllamaSetup.exe",
        save_path="F:\\Ollama\\OllamaSetup.exe"
    )
    print(f"下载任务已添加: {result}")