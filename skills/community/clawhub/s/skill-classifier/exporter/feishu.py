# -*- coding: utf-8 -*-
"""
飞书云文档导出
环境变量：FEISHU_APP_ID / FEISHU_APP_SECRET（必填）、FEISHU_FOLDER_TOKEN（可选，缺省写入云空间根目录）
流程：tenant_access_token → 上传 md（drive upload_all, parent_type=import）
     → 创建 docx 导入任务 → 轮询任务结果
凭据只从环境变量读取，严禁写入任何文件
"""
import logging
import os
import time

from utils.webclient import http_json, http_multipart

logger = logging.getLogger(__name__)
BASE = 'https://open.feishu.cn/open-apis'


def _credentials():
    app_id = os.environ.get('FEISHU_APP_ID')
    app_secret = os.environ.get('FEISHU_APP_SECRET')
    if not app_id or not app_secret:
        raise SystemExit("缺少环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET，无法推送飞书文档")
    return app_id, app_secret


def _tenant_token(app_id: str, app_secret: str) -> str:
    data = http_json('POST', f'{BASE}/auth/v3/tenant_access_token/internal',
                     body={'app_id': app_id, 'app_secret': app_secret})
    token = data.get('tenant_access_token')
    if not token:
        raise RuntimeError(f"获取 tenant_access_token 失败: {data.get('msg')}")
    return token


def _mount_key(headers) -> str:
    """导入挂载点：优先 FEISHU_FOLDER_TOKEN，缺省查云空间根目录"""
    folder = os.environ.get('FEISHU_FOLDER_TOKEN')
    if folder:
        return folder
    data = http_json('GET', f'{BASE}/drive/explorer/v2/root_folder/meta', headers=headers)
    token = (data.get('data') or {}).get('token')
    if not token:
        raise RuntimeError(f"获取根目录 token 失败: {data.get('msg')}")
    return token


def push_markdown(md_path: str, title: str) -> str:
    """
    上传 md 文件并导入为飞书云文档

    Returns:
        文档链接
    """
    app_id, app_secret = _credentials()
    headers = {'Authorization': f'Bearer {_tenant_token(app_id, app_secret)}'}

    with open(md_path, 'rb') as f:
        content = f.read()
    upload = http_multipart(
        f'{BASE}/drive/v1/medias/upload_all', headers,
        {'file_name': f'{title}.md', 'parent_type': 'import', 'size': str(len(content))},
        'file', f'{title}.md', content)
    file_token = (upload.get('data') or {}).get('file_token')
    if not file_token:
        raise RuntimeError(f"上传文件失败: {upload.get('msg')}")

    task = http_json('POST', f'{BASE}/docx/v1/import_tasks', headers=headers,
                     body={'file_token': file_token, 'type': 'md',
                           'point': {'mount_type': 1, 'mount_key': _mount_key(headers)}})
    ticket = (task.get('data') or {}).get('ticket')
    if not ticket:
        raise RuntimeError(f"创建导入任务失败: {task.get('msg')}")

    for _ in range(20):
        time.sleep(2)
        res = http_json('GET', f'{BASE}/docx/v1/import_tasks/{ticket}', headers=headers)
        result = (res.get('data') or {}).get('result') or {}
        if result.get('url'):
            return result['url']
        if result.get('token'):
            return f"https://feishu.cn/docx/{result['token']}"
        if result.get('job_status') == 1 or result.get('job_error'):
            raise RuntimeError(f"导入任务失败: {result}")
    raise TimeoutError("飞书导入任务轮询超时")
