import requests
import json

class TeambitionSkill:
    def __init__(self, config):
        # 从配置读取密钥，适配多应用
        self.app_id = config["TEAMBITION_APP_ID"]
        self.app_secret = config["TEAMBITION_APP_SECRET"]
        self.access_token = config.get("TEAMBITION_ACCESS_TOKEN", "")
        self.org_id = config.get("TEAMBITION_ORG_ID", "")  # 团队/组织ID
        self.default_project_id = config.get("TEAMBITION_DEFAULT_PROJECT_ID", "")  # 默认项目ID

    def get_access_token(self):
        """获取 TeamBition 访问令牌（如果未配置则自动获取）"""
        if self.access_token:
            return self.access_token
        
        # 从 Client Credentials 获取 Token（TeamBition 官方方式）
        url = "https://open.teambition.com/oauth2/access_token"
        payload = {
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "grant_type": "client_credentials",
            "scope": "task:read task:write"  # 按需调整权限
        }
        resp = requests.post(url, data=payload)
        result = resp.json()
        return result.get("access_token")

    def create_task(self, params):
        """
        创建 TeamBition 任务
        :param params: 包含 project_id, title, content, assignee 等
        :return: 创建结果
        """
        token = self.get_access_token()
        if not token:
            return {"code": -1, "msg": "获取 Token 失败"}
        
        # 优先用传入的项目ID，无则用默认
        project_id = params.get("project_id", self.default_project_id)
        if not project_id:
            return {"code": -2, "msg": "缺少 project_id（未配置默认值）"}
        
        # 必传参数校验
        title = params.get("title")
        if not title:
            return {"code": -3, "msg": "缺少任务标题 title"}
        
        # 构建任务参数
        task_data = {
            "projectId": project_id,
            "title": title,
            "content": params.get("content", ""),
            "assigneeId": params.get("assignee", "")  # 负责人ID
        }

        # 调用 TeamBition 创建任务 API
        url = "https://open.teambition.com/api/v3/tasks"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp = requests.post(url, headers=headers, json=task_data)
        return resp.json()

    def get_task(self, params):
        """查询单个任务详情（按 task_id）"""
        token = self.get_access_token()
        task_id = params.get("task_id")
        if not task_id:
            return {"code": -4, "msg": "缺少 task_id"}
        
        url = f"https://open.teambition.com/api/v3/tasks/{task_id}"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()

# OpenClaw 固定入口函数
def run(config, params):
    skill = TeambitionSkill(config)
    # 根据 action 选择执行的操作（创建/查询任务）
    action = params.get("action", "create_task")
    
    if action == "create_task":
        return skill.create_task(params)
    elif action == "get_task":
        return skill.get_task(params)
    else:
        return {"code": -5, "msg": f"不支持的操作：{action}"}