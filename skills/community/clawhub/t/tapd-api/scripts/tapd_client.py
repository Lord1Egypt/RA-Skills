#!/usr/bin/env python3
"""
TAPD OAuth 完整客户端

实现所有 API 模块和方法。
支持 OAuth 认证和 Basic 认证两种方式。
"""

import json
import os
import time
import urllib.parse
import urllib.request
from base64 import b64encode
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class TapdHttp:
    """HTTP 请求基类"""
    
    API_BASE_URL = "https://api.tapd.cn"
    TOKEN_ENDPOINT = "/tokens/request_token"
    TOKEN_CACHE_FILE = Path.home() / ".tapd_token_cache.json"
    
    def __init__(self, auth_type: str = "oauth", **kwargs):
        """
        初始化 HTTP 客户端
        
        Args:
            auth_type: 认证类型 ("oauth" 或 "basic")
            **kwargs: 认证参数
                - OAuth: client_id, client_secret
                - Basic: api_user, api_password
        """
        self.auth_type = auth_type
        self.auth_params = kwargs
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0
        
        if auth_type == "oauth":
            self._load_cached_token()
    
    def _load_cached_token(self):
        """加载缓存的 OAuth token"""
        if not self.TOKEN_CACHE_FILE.exists():
            return
        
        try:
            with open(self.TOKEN_CACHE_FILE) as f:
                cache = json.load(f)
            
            if cache.get("expires_at", 0) > time.time() + 300:
                self._access_token = cache.get("access_token")
                self._token_expires_at = cache.get("expires_at")
        except Exception:
            pass
    
    def _save_token_cache(self):
        """保存 OAuth token 到缓存"""
        cache = {
            "access_token": self._access_token,
            "expires_at": self._token_expires_at,
            "updated_at": time.time()
        }
        
        with open(self.TOKEN_CACHE_FILE, "w") as f:
            json.dump(cache, f)
    
    def _get_access_token(self) -> str:
        """获取 OAuth access_token（自动刷新）"""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        
        client_id = self.auth_params.get("client_id")
        client_secret = self.auth_params.get("client_secret")
        
        url = f"{self.API_BASE_URL}{self.TOKEN_ENDPOINT}"
        auth_str = f"{client_id}:{client_secret}"
        auth_b64 = b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("status") != 1:
            raise Exception(f"获取 access_token 失败: {result.get('info')}")
        
        token_data = result["data"]
        self._access_token = token_data["access_token"]
        self._token_expires_at = time.time() + token_data["expires_in"]
        self._save_token_cache()
        
        return self._access_token
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """获取认证头"""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        if self.auth_type == "oauth":
            token = self._get_access_token()
            headers["Authorization"] = f"Bearer {token}"
        else:  # basic
            api_user = self.auth_params.get("api_user")
            api_password = self.auth_params.get("api_password")
            auth_str = f"{api_user}:{api_password}"
            auth_b64 = b64encode(auth_str.encode()).decode()
            headers["Authorization"] = f"Basic {auth_b64}"
        
        return headers
    
    def request(self, method: str, endpoint: str, 
                params: Optional[Dict] = None, 
                data: Optional[Dict] = None) -> Union[Dict, List]:
        """
        发送 HTTP 请求
        
        Args:
            method: HTTP 方法 (GET, POST)
            endpoint: API 端点
            params: URL 参数
            data: POST 数据
        
        Returns:
            API 响应数据
        """
        url = f"{self.API_BASE_URL}/{endpoint.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        
        headers = self._get_auth_headers()
        req_data = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("status") != 1:
            raise Exception(f"API 请求失败: {result.get('info')}")
        
        return result.get("data", [])
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Union[Dict, List]:
        """GET 请求"""
        return self.request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Union[Dict, List]:
        """POST 请求"""
        return self.request("POST", endpoint, data=data)


class TapdModule:
    """TAPD 模块基类"""
    
    def __init__(self, http: TapdHttp):
        self.http = http
    
    def _validate(self, data: Dict, required_fields: List[str]):
        """验证必需字段"""
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"缺少必需字段: {', '.join(missing)}")


class Story(TapdModule):
    """需求模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取需求列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("stories", params=kwargs)
        return [item["Story"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """需求计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("stories/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建需求"""
        self._validate(kwargs, ["workspace_id", "name"])
        result = self.http.post("stories", data=kwargs)
        return result.get("Story", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新需求"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("stories", data=kwargs)
        return result.get("Story", {}) if isinstance(result, dict) else {}
    
    def custom_fields_settings(self, **kwargs) -> List[Dict]:
        """获取需求自定义字段配置"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("stories/custom_fields_settings", params=kwargs)
    
    def get_link_stories(self, **kwargs) -> List[Dict]:
        """获取需求关联关系"""
        self._validate(kwargs, ["workspace_id", "story_id"])
        return self.http.get("stories/get_link_stories", params=kwargs)
    
    def changes(self, **kwargs) -> List[Dict]:
        """获取需求变更历史"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("story_changes", params=kwargs)
        return [item["StoryChange"] for item in result] if isinstance(result, list) else []
    
    def changes_count(self, **kwargs) -> int:
        """获取需求变更次数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("story_changes/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def categories(self, **kwargs) -> List[Dict]:
        """获取需求分类"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("story_categories", params=kwargs)
    
    def categories_count(self, **kwargs) -> int:
        """获取需求分类数量"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("story_categories/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def get_story_tcase(self, **kwargs) -> List[Dict]:
        """获取需求与测试用例关联关系"""
        self._validate(kwargs, ["workspace_id", "story_id"])
        return self.http.get("stories/get_story_tcase", params=kwargs)
    
    def update_select_field_options(self, **kwargs) -> Dict:
        """更新需求下拉字段候选值"""
        self._validate(kwargs, ["workspace_id", "id", "options"])
        return self.http.post("custom_field_configs/update_story_select_field_options", data=kwargs)
    
    def get_fields_info(self, **kwargs) -> List[Dict]:
        """获取需求所有字段及候选值"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("stories/get_fields_info", params=kwargs)


class Task(TapdModule):
    """任务模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取任务列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("tasks", params=kwargs)
        return [item["Task"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """任务计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("tasks/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建任务"""
        self._validate(kwargs, ["workspace_id", "name"])
        result = self.http.post("tasks", data=kwargs)
        return result.get("Task", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新任务"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("tasks", data=kwargs)
        return result.get("Task", {}) if isinstance(result, dict) else {}
    
    def custom_fields_settings(self, **kwargs) -> List[Dict]:
        """获取任务自定义字段配置"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("tasks/custom_fields_settings", params=kwargs)
    
    def changes(self, **kwargs) -> List[Dict]:
        """获取任务变更历史"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("task_changes", params=kwargs)
        return [item["TaskChange"] for item in result] if isinstance(result, list) else []
    
    def changes_count(self, **kwargs) -> int:
        """获取任务变更次数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("task_changes/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0


class Bug(TapdModule):
    """缺陷模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取缺陷列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("bugs", params=kwargs)
        return [item["Bug"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """缺陷计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("bugs/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def group_count(self, **kwargs) -> List[Dict]:
        """缺陷统计"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("bugs/group_count", params=kwargs)
    
    def create(self, **kwargs) -> Dict:
        """创建缺陷"""
        self._validate(kwargs, ["workspace_id", "title"])
        result = self.http.post("bugs", data=kwargs)
        return result.get("Bug", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新缺陷"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("bugs", data=kwargs)
        return result.get("Bug", {}) if isinstance(result, dict) else {}
    
    def custom_fields_settings(self, **kwargs) -> List[Dict]:
        """获取缺陷自定义字段配置"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("bugs/custom_fields_settings", params=kwargs)
    
    def changes(self, **kwargs) -> List[Dict]:
        """获取缺陷变更历史"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("bug_changes", params=kwargs)
        return [item["BugChange"] for item in result] if isinstance(result, list) else []
    
    def changes_count(self, **kwargs) -> int:
        """获取缺陷变更次数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("bug_changes/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def get_link_bugs(self, **kwargs) -> List[Dict]:
        """获取缺陷关联关系"""
        self._validate(kwargs, ["workspace_id", "bug_id"])
        return self.http.get("bugs/get_link_bugs", params=kwargs)


class Iteration(TapdModule):
    """迭代模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取迭代列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("iterations", params=kwargs)
        return [item["Iteration"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """迭代计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("iterations/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建迭代"""
        self._validate(kwargs, ["workspace_id", "name"])
        result = self.http.post("iterations", data=kwargs)
        return result.get("Iteration", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新迭代"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("iterations", data=kwargs)
        return result.get("Iteration", {}) if isinstance(result, dict) else {}
    
    def custom_fields_settings(self, **kwargs) -> List[Dict]:
        """获取迭代自定义字段配置"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("iterations/custom_fields_settings", params=kwargs)


class Comment(TapdModule):
    """评论模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取评论列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("comments", params=kwargs)
        return [item["Comment"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """评论计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("comments/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建评论"""
        self._validate(kwargs, ["workspace_id", "entry_id", "entry_type", "description"])
        result = self.http.post("comments", data=kwargs)
        return result.get("Comment", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新评论"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("comments", data=kwargs)
        return result.get("Comment", {}) if isinstance(result, dict) else {}


class Wiki(TapdModule):
    """Wiki 模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取 Wiki 列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("wikis", params=kwargs)
        return [item["Wiki"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """Wiki 计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("wikis/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建 Wiki"""
        self._validate(kwargs, ["workspace_id", "title"])
        result = self.http.post("wikis", data=kwargs)
        return result.get("Wiki", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新 Wiki"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("wikis", data=kwargs)
        return result.get("Wiki", {}) if isinstance(result, dict) else {}


class Test(TapdModule):
    """测试用例模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取测试用例列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("tcases", params=kwargs)
        return [item["TCase"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """测试用例计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("tcases/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建测试用例"""
        self._validate(kwargs, ["workspace_id", "name"])
        result = self.http.post("tcases", data=kwargs)
        return result.get("TCase", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新测试用例"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("tcases", data=kwargs)
        return result.get("TCase", {}) if isinstance(result, dict) else {}
    
    def plans(self, **kwargs) -> List[Dict]:
        """获取测试计划"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("tplans", params=kwargs)
    
    def plans_count(self, **kwargs) -> int:
        """测试计划计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("tplans/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def categories(self, **kwargs) -> List[Dict]:
        """获取测试用例目录"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("tcase_categories", params=kwargs)
    
    def categories_count(self, **kwargs) -> int:
        """测试用例目录计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("tcase_categories/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def result(self, **kwargs) -> List[Dict]:
        """获取测试用例执行结果"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("tcase_results", params=kwargs)
    
    def get_story_by_tcase_id(self, **kwargs) -> List[Dict]:
        """获取测试用例关联的需求"""
        self._validate(kwargs, ["workspace_id", "tcase_id"])
        return self.http.get("tcases/get_story_by_tcase_id", params=kwargs)


class Timesheet(TapdModule):
    """工时模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取工时列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("timesheets", params=kwargs)
        return [item["Timesheet"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """工时计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("timesheets/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建工时"""
        self._validate(kwargs, ["workspace_id", "timespent", "entity_type", "entity_id"])
        result = self.http.post("timesheets", data=kwargs)
        return result.get("Timesheet", {}) if isinstance(result, dict) else {}
    
    def update(self, **kwargs) -> Dict:
        """更新工时"""
        self._validate(kwargs, ["workspace_id", "id"])
        result = self.http.post("timesheets", data=kwargs)
        return result.get("Timesheet", {}) if isinstance(result, dict) else {}


class Workspace(TapdModule):
    """工作空间模块"""
    
    def projects(self, **kwargs) -> List[Dict]:
        """获取项目列表"""
        result = self.http.get("workspaces/projects", params=kwargs)
        return [item["Workspace"] for item in result] if isinstance(result, list) else []
    
    def users(self, **kwargs) -> List[Dict]:
        """获取项目成员"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("workspaces/users", params=kwargs)
        return [item["WorkspaceMember"] for item in result] if isinstance(result, list) else []
    
    def add_member_by_nick(self, **kwargs) -> Dict:
        """添加成员到项目"""
        self._validate(kwargs, ["workspace_id", "nick"])
        return self.http.post("workspaces/add_member_by_nick", data=kwargs)


class Workflow(TapdModule):
    """工作流模块"""
    
    def status_map(self, **kwargs) -> Dict:
        """获取工作流状态映射"""
        self._validate(kwargs, ["workspace_id", "system"])
        return self.http.get("workflows/status_map", params=kwargs)


class Boardcard(TapdModule):
    """看板工作项模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取看板工作项列表"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("boardcards", params=kwargs)
    
    def create(self, **kwargs) -> Dict:
        """创建看板工作项"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.post("boardcards", data=kwargs)
    
    def update(self, **kwargs) -> Dict:
        """更新看板工作项"""
        self._validate(kwargs, ["workspace_id", "id"])
        return self.http.post("boardcards", data=kwargs)


class Module(TapdModule):
    """模块管理"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取模块列表"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("modules", params=kwargs)
    
    def count(self, **kwargs) -> int:
        """模块计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("modules/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建模块"""
        self._validate(kwargs, ["workspace_id", "name"])
        return self.http.post("modules", data=kwargs)
    
    def update(self, **kwargs) -> Dict:
        """更新模块"""
        self._validate(kwargs, ["workspace_id", "id"])
        return self.http.post("modules", data=kwargs)


class Relation(TapdModule):
    """关联关系模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取关联关系列表"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("relations", params=kwargs)


class Release(TapdModule):
    """发布计划模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取发布计划列表"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("releases", params=kwargs)
        return [item["Release"] for item in result] if isinstance(result, list) else []
    
    def count(self, **kwargs) -> int:
        """发布计划计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("releases/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0


class Version(TapdModule):
    """版本模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取版本列表"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("versions", params=kwargs)
    
    def count(self, **kwargs) -> int:
        """版本计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("versions/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def create(self, **kwargs) -> Dict:
        """创建版本"""
        self._validate(kwargs, ["workspace_id", "name"])
        return self.http.post("versions", data=kwargs)
    
    def update(self, **kwargs) -> Dict:
        """更新版本"""
        self._validate(kwargs, ["workspace_id", "id"])
        return self.http.post("versions", data=kwargs)


class Role(TapdModule):
    """角色模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取角色列表"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("roles", params=kwargs)


class Launchform(TapdModule):
    """发布评审模块"""
    
    def list(self, **kwargs) -> List[Dict]:
        """获取发布评审列表"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("launchforms", params=kwargs)
    
    def count(self, **kwargs) -> int:
        """发布评审计数"""
        self._validate(kwargs, ["workspace_id"])
        result = self.http.get("launchforms/count", params=kwargs)
        return result.get("count", 0) if isinstance(result, dict) else 0
    
    def custom_fields_settings(self, **kwargs) -> List[Dict]:
        """获取发布评审自定义字段配置"""
        self._validate(kwargs, ["workspace_id"])
        return self.http.get("launchforms/custom_fields_settings", params=kwargs)


class TapdClient:
    """
    TAPD 完整客户端
    
    支持 OAuth 和 Basic 两种认证方式，实现所有 TAPD API 模块。
    """
    
    def __init__(self, auth_type: str = "oauth", config_file: Optional[str] = None, **kwargs):
        """
        初始化客户端
        
        Args:
            auth_type: 认证类型 ("oauth" 或 "basic")
            config_file: tapd.json 路径（仅 OAuth）
            **kwargs: 认证参数
                - OAuth 手动: client_id, client_secret, workspace_id
                - Basic: api_user, api_password, workspace_id
        """
        self.auth_type = auth_type
        self.workspace_id = kwargs.get("workspace_id")
        
        # OAuth 从配置文件读取
        if auth_type == "oauth" and not kwargs.get("client_id"):
            self._load_oauth_config(config_file)
            auth_params = {
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        else:
            auth_params = kwargs
        
        # 初始化 HTTP 客户端
        self.http = TapdHttp(auth_type=auth_type, **auth_params)
        
        # 初始化所有模块
        self.story = Story(self.http)
        self.task = Task(self.http)
        self.bug = Bug(self.http)
        self.iteration = Iteration(self.http)
        self.comment = Comment(self.http)
        self.wiki = Wiki(self.http)
        self.test = Test(self.http)
        self.timesheet = Timesheet(self.http)
        self.workspace = Workspace(self.http)
        self.workflow = Workflow(self.http)
        self.boardcard = Boardcard(self.http)
        self.module = Module(self.http)
        self.relation = Relation(self.http)
        self.release = Release(self.http)
        self.version = Version(self.http)
        self.role = Role(self.http)
        self.launchform = Launchform(self.http)
    
    def _load_oauth_config(self, config_file: Optional[str] = None):
        """从 tapd.json 加载 OAuth 配置"""
        if config_file is None:
            config_file = Path.home() / ".openclaw/workspace" / "tapd.json"
        
        if not self.client_id or not self.client_secret:
            raise ValueError("缺少 clientId 或 clientSecret")
        
        # 找到默认工作空间
        if not self.workspace_id:
            for ws in self.workspaces:
                if ws.get("default"):
                    self.workspace_id = ws["id"]
                    break
            
            if not self.workspace_id and self.workspaces:
                self.workspace_id = self.workspaces[0]["id"]


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TAPD 完整客户端")
    parser.add_argument("module", help="模块名称 (story, task, bug, etc.)")
    parser.add_argument("action", help="操作 (list, count, create, update)")
    parser.add_argument("--workspace", help="工作空间 ID")
    parser.add_argument("--auth", choices=["oauth", "basic"], default="oauth", help="认证类型")
    parser.add_argument("--limit", type=int, default=10, help="返回数量")
    parser.add_argument("--id", help="记录 ID")
    parser.add_argument("--name", help="名称/标题")
    parser.add_argument("--status", help="状态")
    
    args = parser.parse_args()
    
    # 初始化客户端
    client = TapdClient(auth_type=args.auth, workspace_id=args.workspace)
    
    # 获取模块
    if not hasattr(client, args.module):
        print(f"错误: 模块 '{args.module}' 不存在")
        return
    
    module = getattr(client, args.module)
    
    # 获取操作
    if not hasattr(module, args.action):
        print(f"错误: 操作 '{args.action}' 不存在")
        return
    
    action = getattr(module, args.action)
    
    # 构建参数
    params = {"workspace_id": args.workspace or client.workspace_id}
    if args.limit:
        params["limit"] = args.limit
    if args.id:
        params["id"] = args.id
    if args.name:
        params["name"] = args.name
    if args.status:
        params["status"] = args.status
    
    # 执行操作
    try:
        result = action(**params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
