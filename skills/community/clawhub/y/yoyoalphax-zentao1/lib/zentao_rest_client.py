#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道 REST API 客户端 - 完整版
基于禅道官方 REST API 文档：/zentao/dev-api-restapi.html
"""

import httpx
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path


class ZenTaoRESTClient:
    """禅道 REST API 客户端（完整版）"""
    
    def __init__(self, endpoint: str, username: str, password: str):
        self.endpoint = endpoint.rstrip('/')
        self.username = username
        self.password = password
        self.base_url = f"{self.endpoint}/api.php/v1"
        self.token: Optional[str] = None
    
    # ==================== 认证 ====================
    
    def get_token(self) -> Optional[str]:
        """POST /tokens - 获取 Token"""
        url = f"{self.base_url}/tokens"
        data = {'account': self.username, 'password': self.password}
        
        try:
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
    
    def _request(self, method: str, path: str, data: Optional[Dict] = None, 
                 params: Optional[Dict] = None) -> Tuple[bool, Any]:
        """通用请求方法"""
        if not self.token:
            self.get_token()
        
        if not self.token:
            return False, "认证失败"
        
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {'Token': self.token}
        
        try:
            if method.upper() == 'GET':
                response = httpx.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = httpx.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = httpx.put(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = httpx.delete(url, headers=headers, timeout=30)
            else:
                return False, f"不支持的方法：{method}"
            
            if response.status_code in [200, 201]:
                return True, response.json()
            elif response.status_code == 204:
                return True, {'message': '操作成功'}
            else:
                return False, f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            return False, str(e)
    
    # ==================== 用户 User ====================
    
    def get_users(self, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /users - 获取用户列表"""
        return self._request('GET', '/users', params={'page': page, 'limit': limit})
    
    def get_user(self, user_id: int) -> Tuple[bool, Any]:
        """GET /users/{id} - 获取用户信息"""
        return self._request('GET', f'/users/{user_id}')
    
    def get_user_myself(self) -> Tuple[bool, Any]:
        """GET /user - 获取我的个人信息"""
        return self._request('GET', '/user')
    
    def create_user(self, data: Dict) -> Tuple[bool, Any]:
        """POST /users - 创建用户"""
        return self._request('POST', '/users', data=data)
    
    def update_user(self, user_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /users/{id} - 修改用户信息"""
        return self._request('PUT', f'/users/{user_id}', data=data)
    
    def delete_user(self, user_id: int) -> Tuple[bool, Any]:
        """DELETE /users/{id} - 删除用户"""
        return self._request('DELETE', f'/users/{user_id}')
    
    # ==================== 项目集 Program ====================
    
    def get_programs(self, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /programs - 获取项目集列表"""
        return self._request('GET', '/programs', params={'page': page, 'limit': limit})
    
    def get_program(self, program_id: int) -> Tuple[bool, Any]:
        """GET /programs/{id} - 获取项目集信息"""
        return self._request('GET', f'/programs/{program_id}')
    
    def create_program(self, data: Dict) -> Tuple[bool, Any]:
        """POST /programs - 创建项目集"""
        return self._request('POST', '/programs', data=data)
    
    def update_program(self, program_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /programs/{id} - 修改项目集"""
        return self._request('PUT', f'/programs/{program_id}', data=data)
    
    def delete_program(self, program_id: int) -> Tuple[bool, Any]:
        """DELETE /programs/{id} - 删除项目集"""
        return self._request('DELETE', f'/programs/{program_id}')
    
    # ==================== 产品 Product ====================
    
    def get_products(self, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /products - 获取产品列表"""
        return self._request('GET', '/products', params={'page': page, 'limit': limit})
    
    def get_product(self, product_id: int) -> Tuple[bool, Any]:
        """GET /products/{id} - 获取产品信息"""
        return self._request('GET', f'/products/{product_id}')
    
    def create_product(self, data: Dict) -> Tuple[bool, Any]:
        """POST /products - 创建产品"""
        return self._request('POST', '/products', data=data)
    
    def update_product(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /products/{id} - 修改产品"""
        return self._request('PUT', f'/products/{product_id}', data=data)
    
    def delete_product(self, product_id: int) -> Tuple[bool, Any]:
        """DELETE /products/{id} - 删除产品"""
        return self._request('DELETE', f'/products/{product_id}')
    
    def get_product_teams(self, product_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/teams - 获取产品团队"""
        return self._request('GET', f'/products/{product_id}/teams')
    
    # ==================== 产品计划 ProductPlan ====================
    
    def get_product_plans(self, product_id: int, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /products/{id}/plans - 获取产品计划列表"""
        return self._request('GET', f'/products/{product_id}/plans', params={'page': page, 'limit': limit})
    
    def get_product_plan(self, product_id: int, plan_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/plans/{planID} - 获取产品计划"""
        return self._request('GET', f'/products/{product_id}/plans/{plan_id}')
    
    def create_product_plan(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/plans - 创建产品计划"""
        return self._request('POST', f'/products/{product_id}/plans', data=data)
    
    def update_product_plan(self, product_id: int, plan_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /products/{id}/plans/{planID} - 修改产品计划"""
        return self._request('PUT', f'/products/{product_id}/plans/{plan_id}', data=data)
    
    def delete_product_plan(self, product_id: int, plan_id: int) -> Tuple[bool, Any]:
        """DELETE /products/{id}/plans/{planID} - 删除产品计划"""
        return self._request('DELETE', f'/products/{product_id}/plans/{plan_id}')
    
    # ==================== 发布 Release ====================
    
    def get_releases(self, product_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/releases - 获取发布列表"""
        return self._request('GET', f'/products/{product_id}/releases')
    
    def create_release(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/releases - 创建发布"""
        return self._request('POST', f'/products/{product_id}/releases', data=data)
    
    # ==================== 需求 Story ====================
    
    def get_stories(self, product_id: int, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /products/{id}/stories - 获取需求列表"""
        return self._request('GET', f'/products/{product_id}/stories', params={'page': page, 'limit': limit})
    
    def get_story(self, product_id: int, story_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/stories/{storyID} - 获取需求"""
        return self._request('GET', f'/products/{product_id}/stories/{story_id}')
    
    def create_story(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/stories - 创建需求"""
        return self._request('POST', f'/products/{product_id}/stories', data=data)
    
    def update_story(self, product_id: int, story_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /products/{id}/stories/{storyID} - 修改需求"""
        return self._request('PUT', f'/products/{product_id}/stories/{story_id}', data=data)
    
    def delete_story(self, product_id: int, story_id: int) -> Tuple[bool, Any]:
        """DELETE /products/{id}/stories/{storyID} - 删除需求"""
        return self._request('DELETE', f'/products/{product_id}/stories/{story_id}')
    
    def activate_story(self, product_id: int, story_id: int) -> Tuple[bool, Any]:
        """PUT /products/{id}/stories/{storyID}/activate - 激活需求"""
        return self._request('PUT', f'/products/{product_id}/stories/{story_id}/activate')
    
    def close_story(self, product_id: int, story_id: int) -> Tuple[bool, Any]:
        """PUT /products/{id}/stories/{storyID}/close - 关闭需求"""
        return self._request('PUT', f'/products/{product_id}/stories/{story_id}/close')
    
    # ==================== 项目 Project ====================
    
    def get_projects(self, status: str = 'doing', page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /projects - 获取项目列表"""
        return self._request('GET', '/projects', params={'status': status, 'page': page, 'limit': limit})
    
    def get_project(self, project_id: int) -> Tuple[bool, Any]:
        """GET /projects/{id} - 获取项目信息"""
        return self._request('GET', f'/projects/{project_id}')
    
    def get_project_stories(self, project_id: int) -> Tuple[bool, Any]:
        """GET /projects/{id}/stories - 获取项目需求列表"""
        return self._request('GET', f'/projects/{project_id}/stories')
    
    def get_project_executions(self, project_id: int, status: str = 'all') -> Tuple[bool, Any]:
        """GET /projects/{id}/executions - 获取项目执行列表"""
        return self._request('GET', f'/projects/{project_id}/executions', params={'status': status})
    
    def get_project_builds(self, project_id: int) -> Tuple[bool, Any]:
        """GET /projects/{id}/builds - 获取项目版本列表"""
        return self._request('GET', f'/projects/{project_id}/builds')
    
    def create_project(self, data: Dict) -> Tuple[bool, Any]:
        """POST /projects - 创建项目"""
        return self._request('POST', '/projects', data=data)
    
    def update_project(self, project_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /projects/{id} - 修改项目"""
        return self._request('PUT', f'/projects/{project_id}', data=data)
    
    def delete_project(self, project_id: int) -> Tuple[bool, Any]:
        """DELETE /projects/{id} - 删除项目"""
        return self._request('DELETE', f'/projects/{project_id}')
    
    # ==================== 版本 Build ====================
    
    def get_build(self, build_id: int) -> Tuple[bool, Any]:
        """GET /builds/{id} - 获取版本"""
        return self._request('GET', f'/builds/{build_id}')
    
    def create_build(self, project_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /projects/{id}/builds - 创建版本"""
        return self._request('POST', f'/projects/{project_id}/builds', data=data)
    
    def update_build(self, build_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /builds/{id} - 修改版本"""
        return self._request('PUT', f'/builds/{build_id}', data=data)
    
    def delete_build(self, build_id: int) -> Tuple[bool, Any]:
        """DELETE /builds/{id} - 删除版本"""
        return self._request('DELETE', f'/builds/{build_id}')
    
    # ==================== 执行 Execution ====================
    
    def get_executions(self, status: str = 'doing', page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /executions - 获取执行列表"""
        return self._request('GET', '/executions', params={'status': status, 'page': page, 'limit': limit})
    
    def get_execution(self, execution_id: int) -> Tuple[bool, Any]:
        """GET /executions/{id} - 获取执行信息"""
        return self._request('GET', f'/executions/{execution_id}')
    
    def get_execution_tasks(self, execution_id: int, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /executions/{id}/tasks - 获取执行任务列表"""
        return self._request('GET', f'/executions/{execution_id}/tasks', params={'page': page, 'limit': limit})
    
    def get_execution_bugs(self, execution_id: int) -> Tuple[bool, Any]:
        """GET /executions/{id}/bugs - 获取执行 Bug 列表"""
        return self._request('GET', f'/executions/{execution_id}/bugs')
    
    def get_execution_builds(self, execution_id: int) -> Tuple[bool, Any]:
        """GET /executions/{id}/builds - 获取执行版本列表"""
        return self._request('GET', f'/executions/{execution_id}/builds')
    
    def create_execution(self, data: Dict) -> Tuple[bool, Any]:
        """POST /executions - 创建执行"""
        return self._request('POST', '/executions', data=data)
    
    def update_execution(self, execution_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /executions/{id} - 修改执行"""
        return self._request('PUT', f'/executions/{execution_id}', data=data)
    
    def delete_execution(self, execution_id: int) -> Tuple[bool, Any]:
        """DELETE /executions/{id} - 删除执行"""
        return self._request('DELETE', f'/executions/{execution_id}')
    
    # ==================== 任务 Task ====================
    
    def get_tasks(self, status: str = 'all', page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /tasks - 获取任务列表"""
        return self._request('GET', '/tasks', params={'status': status, 'page': page, 'limit': limit})
    
    def get_task(self, task_id: int) -> Tuple[bool, Any]:
        """GET /tasks/{id} - 获取任务"""
        return self._request('GET', f'/tasks/{task_id}')
    
    def create_task(self, execution_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /executions/{id}/tasks - 创建任务"""
        return self._request('POST', f'/executions/{execution_id}/tasks', data=data)
    
    def update_task(self, task_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /tasks/{id} - 修改任务"""
        return self._request('PUT', f'/tasks/{task_id}', data=data)
    
    def delete_task(self, task_id: int) -> Tuple[bool, Any]:
        """DELETE /tasks/{id} - 删除任务"""
        return self._request('DELETE', f'/tasks/{task_id}')
    
    # ==================== 缺陷 Bug ====================
    
    def get_bugs(self, product_id: int, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /products/{id}/bugs - 获取 Bug 列表"""
        return self._request('GET', f'/products/{product_id}/bugs', params={'page': page, 'limit': limit})
    
    def get_bug(self, bug_id: int) -> Tuple[bool, Any]:
        """GET /bugs/{id} - 获取 Bug"""
        return self._request('GET', f'/bugs/{bug_id}')
    
    def create_bug(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/bugs - 创建 Bug"""
        return self._request('POST', f'/products/{product_id}/bugs', data=data)
    
    def update_bug(self, bug_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /bugs/{id} - 修改 Bug"""
        return self._request('PUT', f'/bugs/{bug_id}', data=data)
    
    def delete_bug(self, bug_id: int) -> Tuple[bool, Any]:
        """DELETE /bugs/{id} - 删除 Bug"""
        return self._request('DELETE', f'/bugs/{bug_id}')
    
    # ==================== 用例 TestCase ====================
    
    def get_test_cases(self, product_id: int, page: int = 1, limit: int = 20) -> Tuple[bool, Any]:
        """GET /products/{id}/testcases - 获取用例列表"""
        return self._request('GET', f'/products/{product_id}/testcases', params={'page': page, 'limit': limit})
    
    def get_test_case(self, case_id: int) -> Tuple[bool, Any]:
        """GET /testcases/{id} - 获取用例"""
        return self._request('GET', f'/testcases/{case_id}')
    
    def create_test_case(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/testcases - 创建用例"""
        return self._request('POST', f'/products/{product_id}/testcases', data=data)
    
    def update_test_case(self, case_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /testcases/{id} - 修改用例"""
        return self._request('PUT', f'/testcases/{case_id}', data=data)
    
    def delete_test_case(self, case_id: int) -> Tuple[bool, Any]:
        """DELETE /testcases/{id} - 删除用例"""
        return self._request('DELETE', f'/testcases/{case_id}')
    
    # ==================== 测试单 TestTask ====================
    
    def get_test_tasks(self, product_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/testtasks - 获取测试单列表"""
        return self._request('GET', f'/products/{product_id}/testtasks')
    
    def get_test_task(self, task_id: int) -> Tuple[bool, Any]:
        """GET /testtasks/{id} - 获取测试单"""
        return self._request('GET', f'/testtasks/{task_id}')
    
    def create_test_task(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/testtasks - 创建测试单"""
        return self._request('POST', f'/products/{product_id}/testtasks', data=data)
    
    def run_test_case(self, testtask_id: int, case_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /testtasks/{id}/testcases/{caseID}/run - 执行用例"""
        return self._request('POST', f'/testtasks/{testtask_id}/testcases/{case_id}/run', data=data)
    
    # ==================== 反馈 Feedback ====================
    
    def get_feedbacks(self, product_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/feedbacks - 获取反馈列表"""
        return self._request('GET', f'/products/{product_id}/feedbacks')
    
    def get_feedback(self, feedback_id: int) -> Tuple[bool, Any]:
        """GET /feedbacks/{id} - 获取反馈"""
        return self._request('GET', f'/feedbacks/{feedback_id}')
    
    def create_feedback(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/feedbacks - 创建反馈"""
        return self._request('POST', f'/products/{product_id}/feedbacks', data=data)
    
    def update_feedback(self, feedback_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /feedbacks/{id} - 修改反馈"""
        return self._request('PUT', f'/feedbacks/{feedback_id}', data=data)
    
    def delete_feedback(self, feedback_id: int) -> Tuple[bool, Any]:
        """DELETE /feedbacks/{id} - 删除反馈"""
        return self._request('DELETE', f'/feedbacks/{feedback_id}')
    
    # ==================== 工单 Ticket ====================
    
    def get_tickets(self, product_id: int) -> Tuple[bool, Any]:
        """GET /products/{id}/tickets - 获取工单列表"""
        return self._request('GET', f'/products/{product_id}/tickets')
    
    def get_ticket(self, ticket_id: int) -> Tuple[bool, Any]:
        """GET /tickets/{id} - 获取工单"""
        return self._request('GET', f'/tickets/{ticket_id}')
    
    def create_ticket(self, product_id: int, data: Dict) -> Tuple[bool, Any]:
        """POST /products/{id}/tickets - 创建工单"""
        return self._request('POST', f'/products/{product_id}/tickets', data=data)
    
    def update_ticket(self, ticket_id: int, data: Dict) -> Tuple[bool, Any]:
        """PUT /tickets/{id} - 修改工单"""
        return self._request('PUT', f'/tickets/{ticket_id}', data=data)
    
    def delete_ticket(self, ticket_id: int) -> Tuple[bool, Any]:
        """DELETE /tickets/{id} - 删除工单"""
        return self._request('DELETE', f'/tickets/{ticket_id}')


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
    # 测试 REST API
    creds = read_credentials()
    if creds:
        client = ZenTaoRESTClient(creds['endpoint'], creds['username'], creds['password'])
        
        print("=== REST API 测试 ===")
        
        # 测试获取 Token
        token = client.get_token()
        print(f"Token: {token[:20] if token else None}...")
        
        # 测试获取用户列表
        success, users = client.get_users()
        print(f"用户列表：{success}, {len(users.get('users', [])) if isinstance(users, dict) else users}")
        
        # 测试获取产品列表
        success, products = client.get_products()
        print(f"产品列表：{success}, {len(products.get('products', [])) if isinstance(products, dict) else products}")
        
        # 测试获取项目列表
        success, projects = client.get_projects()
        print(f"项目列表：{success}, {len(projects.get('projects', [])) if isinstance(projects, dict) else projects}")
    else:
        print("未找到禅道凭证，请在 TOOLS.md 中配置")
