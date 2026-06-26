#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道 API 客户端 - 整合 REST API 和老 API
"""

import json
import hashlib
import requests
import httpx
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


class ZenTaoClient:
    """禅道 API 统一客户端"""
    
    def __init__(self, endpoint: str, username: str, password: str):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password
        
        # REST API 配置
        self.rest_api_base = f"{self.endpoint}/api.php/v1"
        self.token = None
        
        # 老 API 配置
        self.old_api_base = self.endpoint
        self.session = None
        self.sid = None
        
    # ==================== 认证相关 ====================
    
    def get_token(self) -> Optional[str]:
        """REST API: 获取 Token"""
        try:
            url = f"{self.rest_api_base}/tokens"
            data = {'account': self.username, 'password': self.password}
            response = httpx.post(url, json=data, timeout=30)
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.token = result.get('token')
                return self.token
            else:
                print(f"Token 获取失败：{response.status_code}")
                return None
        except Exception as e:
            print(f"Token 获取异常：{e}")
            return None
    
    def get_session(self) -> Optional[str]:
        """老 API: 获取 Session"""
        try:
            # 获取 SID
            sid_url = f"{self.old_api_base}/api-getSessionID.json"
            response = requests.get(sid_url, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.sid = json.loads(result['data'])['sessionID']
                    
                    # 登录
                    login_url = f"{self.old_api_base}/user-login.json?zentaosid={self.sid}"
                    self.session = requests.session()
                    login_data = {
                        'account': self.username,
                        'password': self.password,
                        'keepLogin[]': 'on',
                        'referer': f"{self.old_api_base}/my/"
                    }
                    login_response = self.session.post(login_url, data=login_data, timeout=30)
                    if login_response.status_code == 200:
                        login_result = login_response.json()
                        if login_result.get('status') == 'success':
                            return self.sid
            return None
        except Exception as e:
            print(f"Session 获取异常：{e}")
            return None
    
    def rest_request(self, method: str, path: str, data: Optional[Dict] = None) -> Tuple[bool, Any]:
        """REST API 请求"""
        if not self.token:
            self.get_token()
        
        if not self.token:
            return False, "认证失败"
        
        url = f"{self.rest_api_base}/{path.lstrip('/')}"
        headers = {'Token': self.token}
        
        try:
            if method.upper() == 'GET':
                response = httpx.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = httpx.post(url, headers=headers, json=data, timeout=30)
            else:
                return False, f"不支持的方法：{method}"
            
            if response.status_code in [200, 201]:
                return True, response.json()
            else:
                return False, f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)
    
    def old_request(self, method: str, path: str, data: Optional[Dict] = None) -> Tuple[bool, Any]:
        """老 API 请求"""
        if not self.sid:
            self.get_session()
        
        if not self.sid:
            return False, "认证失败"
        
        url = f"{self.old_api_base}/{path.lstrip('/')}"
        if '?' in url:
            url += f"&zentaosid={self.sid}"
        else:
            url += f"?zentaosid={self.sid}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, data=data, timeout=30)
            else:
                return False, f"不支持的方法：{method}"
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success' or result.get('result') == 'success':
                    return True, result
                else:
                    return False, result
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    # ==================== REST API 方法 ====================
    
    def get_products(self) -> Tuple[bool, List[Dict]]:
        """获取产品列表"""
        success, result = self.rest_request('GET', '/products')
        if success and isinstance(result, dict) and 'products' in result:
            return True, result['products']
        return success, result
    
    def get_projects(self, status: str = 'doing') -> Tuple[bool, List[Dict]]:
        """获取项目列表"""
        success, result = self.rest_request('GET', f'/projects?status={status}')
        if success and isinstance(result, dict) and 'projects' in result:
            return True, result['projects']
        return success, result
    
    def get_executions(self, project_id: int) -> Tuple[bool, List[Dict]]:
        """获取执行列表"""
        success, result = self.rest_request('GET', f'/projects/{project_id}/executions?status=all')
        if success and isinstance(result, dict) and 'executions' in result:
            return True, result['executions']
        return success, result
    
    def get_user(self, user_id: int) -> Tuple[bool, Dict]:
        """获取用户信息"""
        return self.rest_request('GET', f'/users/{user_id}')
    
    def get_user_myself(self) -> Tuple[bool, Dict]:
        """获取当前用户信息"""
        return self.rest_request('GET', '/user')
    
    def get_stories(self, project_id: int) -> Tuple[bool, List[Dict]]:
        """获取项目需求列表"""
        success, result = self.rest_request('GET', f'/projects/{project_id}/stories')
        if success and isinstance(result, dict) and 'stories' in result:
            return True, result['stories']
        return success, result
    
    def get_tasks(self, execution_id: int) -> Tuple[bool, List[Dict]]:
        """获取执行任务列表"""
        success, result = self.rest_request('GET', f'/executions/{execution_id}/tasks')
        if success and isinstance(result, dict) and 'tasks' in result:
            return True, result['tasks']
        return success, result
    
    def get_bugs(self, product_id: int) -> Tuple[bool, List[Dict]]:
        """获取产品缺陷列表"""
        success, result = self.rest_request('GET', f'/products/{product_id}/bugs')
        if success and isinstance(result, dict) and 'bugs' in result:
            return True, result['bugs']
        return success, result
    
    def get_builds(self, execution_id: int) -> Tuple[bool, List[Dict]]:
        """获取版本列表"""
        success, result = self.rest_request('GET', f'/executions/{execution_id}/builds')
        if success and isinstance(result, dict) and 'builds' in result:
            return True, result['builds']
        return success, result
    
    # ==================== 老 API 方法 ====================
    
    def get_product_list_old(self) -> Dict[str, str]:
        """获取产品列表（老 API）- 返回 {产品名：ID}"""
        success, result = self.old_request('GET', '/product-index-no.json')
        if success and 'data' in result:
            data = json.loads(result['data'])
            products = data.get('products', {})
            return {v: k for k, v in products.items()}
        return {}
    
    def get_project_list_old(self) -> Dict[str, str]:
        """获取项目列表（老 API）- 返回 {项目名：ID}"""
        success, result = self.old_request('GET', '/project-browse-0-doing-0-order_asc-2000-2000-1.json')
        if success and 'data' in result:
            data = json.loads(result['data'])
            projects = data.get('projectStats', {})
            return {v['name']: v['id'] for k, v in projects.items()}
        return {}
    
    def get_bug_list_old(self, product_id: str) -> List[Dict]:
        """获取缺陷列表（老 API）"""
        success, result = self.old_request('GET', f'/bug-browse-{product_id}-0-all.json')
        if success and 'data' in result:
            return json.loads(result['data'])
        return []
    
    def get_productplan_list_old(self, product_id: str) -> Dict[str, str]:
        """获取发布计划列表（老 API）- 返回 {计划名：ID}"""
        success, result = self.old_request('GET', f'/productplan-browse-{product_id}-0-all.json')
        if success and 'data' in result:
            data = json.loads(result['data'])
            plans = data.get('productPlansNum', {})
            return {v['title']: v['id'] for k, v in plans.items()}
        return {}
    
    def get_projectstory_list_old(self, execution_id: str, product_id: str) -> Dict[str, str]:
        """获取项目需求列表（老 API）- 返回 {需求名：ID}"""
        success, result = self.old_request('GET', f'/projectstory-story-{execution_id}-{product_id}-0-all-0-story-name_desc-0-2000-1.json')
        if success and 'data' in result:
            data = json.loads(result['data'])
            stories = data.get('stories', {})
            return {v['title']: v['id'] for k, v in stories.items()}
        return {}
    
    def get_executiontask_list_old(self, execution_id: str) -> Dict[str, str]:
        """获取执行任务列表（老 API）- 返回 {任务名：ID}"""
        success, result = self.old_request('GET', f'/execution-task-{execution_id}-all-0--0-2000-1.json')
        if success and 'data' in result:
            data = json.loads(result['data'])
            tasks = data.get('tasks', {})
            return {v['name']: v['id'] for k, v in tasks.items()}
        return {}
    
    def get_project_executionid_old(self, project_id: str, product_id: str) -> str:
        """获取项目执行 ID（老 API）"""
        success, result = self.old_request('GET', f'/project-execution-0-{project_id}-0-{product_id}.json')
        if success and 'data' in result:
            try:
                data = json.loads(result['data'])
                locate = data.get('locate', '')
                if locate:
                    # 从 URL 中提取 execution ID
                    start = locate.find('task-') + 5
                    end = locate.find('.json', start)
                    if start > 4 and end > start:
                        return locate[start:end]
            except:
                pass
        return project_id
    
    # ==================== 写操作方法（需要确认）====================
    
    def create_story(self, product_id: str, execution_id: str, title: str, plan_id: str = '0', reviewer: str = '') -> Tuple[bool, Dict]:
        """新建需求（老 API）"""
        # 先检查是否已存在
        existing = self.get_projectstory_list_old(execution_id, product_id)
        title_escaped = title.replace('&', '&amp;')
        if title_escaped in existing:
            return True, {'message': '已存在', 'id': existing[title_escaped]}
        
        post_data = {
            'product': product_id,
            'module': 0,
            'modules[0]': 0,
            'plans[0]': 0,
            'title': title,
            'plan': plan_id,
            'reviewer[]': reviewer or 'xuzn'
        }
        return self.old_request('POST', f'/story-create-{product_id}-0-0-0-{execution_id}-0-0-0-story.json', post_data)
    
    def create_task(self, execution_id: str, story_id: str, name: str, assign_to: str) -> Tuple[bool, Dict]:
        """新建任务（老 API）"""
        # 先检查是否已存在
        existing = self.get_executiontask_list_old(execution_id)
        name_escaped = name.replace('&', '&amp;')
        if name_escaped in existing:
            return True, {'message': '已存在', 'id': existing[name_escaped]}
        
        post_data = {
            'execution': execution_id,
            'type': 'devel',
            'assignedTo[]': assign_to,
            'name': name,
            'story': story_id,
            'testStory[0]': story_id
        }
        return self.old_request('POST', f'/task-create-{execution_id}-{story_id}.json', post_data)
    
    def create_productplan(self, product_id: str, title: str) -> Tuple[bool, Dict]:
        """新建发布计划（老 API）"""
        # 先检查是否已存在
        existing = self.get_productplan_list_old(product_id)
        if title in existing:
            return True, {'message': '已存在', 'id': existing[title]}
        
        post_data = {
            'title': title,
            'branch': 0,
            'product': product_id
        }
        return self.old_request('POST', f'/productplan-create-{product_id}-0-0.json', post_data)
    
    def review_story(self, story_id: str) -> Tuple[bool, Dict]:
        """评审需求（老 API）"""
        post_data = {'result': 'pass'}
        return self.old_request('POST', f'/story-review-{story_id}-project-story.json', post_data)
    
    def run_testcase(self, run_id: str, case_id: str, version: str, steps: Dict[str, str] = None) -> Tuple[bool, Any]:
        """执行测试用例（老 API）"""
        post_data = {
            'steps[27282]': 'pass',
            'reals[27282]': '',
            'steps[27283]': 'pass',
            'reals[27283]': '',
            'case': case_id,
            'version': version
        }
        if steps:
            post_data.update(steps)
        return self.old_request('POST', f'/testtask-runCase-{run_id}-{case_id}-{version}.json', post_data)


def read_credentials() -> Optional[Dict[str, str]]:
    """从 TOOLS.md 读取禅道凭证"""
    tools_path = Path.home() / '.openclaw' / 'workspace' / 'TOOLS.md'
    
    if not tools_path.exists():
        return None
    
    content = tools_path.read_text(encoding='utf-8')
    
    # 查找禅道配置部分
    zentao_section_start = -1
    zentao_section_end = -1
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '## 禅道 API' in line or '## 禅道' in line:
            zentao_section_start = i
        elif zentao_section_start >= 0 and line.strip().startswith('## ') and zentao_section_start not in [i]:
            zentao_section_end = i
            break
    
    if zentao_section_start < 0:
        return None
    
    # 提取禅道配置部分
    if zentao_section_end < 0:
        zentao_section = '\n'.join(lines[zentao_section_start:])
    else:
        zentao_section = '\n'.join(lines[zentao_section_start:zentao_section_end])
    
    endpoint = None
    username = None
    password = None
    
    for line in zentao_section.split('\n'):
        line = line.strip()
        if 'API 地址' in line and '：' in line:
            endpoint = line.split('：')[-1].strip().strip('*').strip()
        elif '用户名' in line and '：' in line:
            username = line.split('：')[-1].strip().strip('*').strip()
        elif '密码' in line and '：' in line:
            password = line.split('：')[-1].strip().strip('*').strip()
    
    if endpoint and username and password:
        return {
            'endpoint': endpoint,
            'username': username,
            'password': password
        }
    
    return None


if __name__ == '__main__':
    # 测试
    creds = read_credentials()
    if creds:
        client = ZenTaoClient(creds['endpoint'], creds['username'], creds['password'])
        
        print("=== REST API 测试 ===")
        success, products = client.get_products()
        print(f"产品列表：{success}, {len(products) if isinstance(products, list) else products}")
        
        success, projects = client.get_projects()
        print(f"项目列表：{success}, {len(projects) if isinstance(projects, list) else projects}")
        
        print("\n=== 老 API 测试 ===")
        product_list = client.get_product_list_old()
        print(f"产品列表（老）：{product_list}")
        
        project_list = client.get_project_list_old()
        print(f"项目列表（老）：{project_list}")
    else:
        print("未找到禅道凭证，请在 TOOLS.md 中配置")
