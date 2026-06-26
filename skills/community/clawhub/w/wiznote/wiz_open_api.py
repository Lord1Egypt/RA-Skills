"""为知笔记 Open API 封装 - HTTP/WS 调用（v2 全协作笔记模式）"""
import json
import re
import time
import ssl
import uuid
from urllib.parse import urlparse, quote
import requests
from websocket import create_connection

from config import Config
from wiz_logging import get_logger

logger = get_logger()


class WizOpenApi:
    """为知笔记 Open API 封装类 - 默认协作笔记模式"""

    ATTACHMENT_CONNECT_TIMEOUT_S = 10
    ATTACHMENT_READ_TIMEOUT_S = 60
    ATTACHMENT_CHUNK_SIZE = 64 * 1024

    def __init__(self, config: Config):
        self.config = config
        self.token = ''
        self.kb_server = ''
        self.kb_guid = ''
        self.user_guid = ''
        self.domain = ''

        self._auth()

    def _headers(self):
        """通用请求头"""
        return {'X-Wiz-Token': self.token, 'Content-Type': 'application/json'}

    def _get(self, path, params=None):
        """GET 请求封装"""
        url = f'{self.kb_server}{path}'
        resp = requests.get(url, params=params or {}, headers=self._headers())
        return self._parse_response(resp)

    def _post(self, path, data=None, params=None):
        """POST 请求封装"""
        url = f'{self.kb_server}{path}'
        resp = requests.post(url, params=params or {}, json=data or {}, headers=self._headers())
        return self._parse_response(resp)

    def _put(self, path, data=None, params=None):
        """PUT 请求封装"""
        url = f'{self.kb_server}{path}'
        resp = requests.put(url, params=params or {}, json=data or {}, headers=self._headers())
        return self._parse_response(resp)

    def _delete(self, path, params=None):
        """DELETE 请求封装"""
        url = f'{self.kb_server}{path}'
        resp = requests.delete(url, params=params or {}, headers=self._headers())
        return self._parse_response(resp)

    @staticmethod
    def _parse_response(resp):
        if resp.status_code != 200:
            raise Exception(f'HTTP错误 {resp.status_code}: {resp.text[:200]}')
        data = resp.json()
        if data.get('returnCode') != 200:
            raise Exception(f'API错误: {data}')
        return data.get('result', data)

    # ================================================================
    # 认证
    # ================================================================

    def _auth(self):
        """认证登录"""
        data = self._login()
        self.token = data['result']['token']
        self.kb_server = data['result']['kbServer']
        self.kb_guid = data['result']['kbGuid']
        self.user_guid = data['result']['userGuid']
        parsed = urlparse(self.kb_server)
        self.domain = parsed.netloc
        logger.info(f"登录成功: kb_guid={self.kb_guid}, user_guid={self.user_guid}")
        if self.config.group_name:
            self._switch_group()

    def _login(self):
        login_url = f'{self.config.as_url}/as/user/login'
        response = requests.post(
            login_url,
            data={'userId': self.config.user_id, 'password': self.config.password}
        )
        if response.status_code != 200:
            raise Exception(f'登录失败: HTTP {response.status_code}')
        data = response.json()
        if data.get('returnCode') != 200:
            raise Exception(f'登录失败: {data}')
        return data

    def _switch_group(self):
        if not self.config.group_name:
            return
        data = self._get('/as/user/groups', headers={'X-Wiz-Token': self.token})
        # 上面用的是 self._get 但 as_url 可能不同，走原始逻辑
        group_list_url = f'{self.config.as_url}/as/user/groups'
        resp = requests.get(group_list_url, headers={'X-Wiz-Token': self.token})
        data = resp.json()
        if data.get('returnCode') != 200:
            raise Exception(f'获取群组列表失败: {data}')
        for group in data.get('result', []):
            if group.get('name') == self.config.group_name:
                self.kb_guid = group['kbGuid']
                self.domain = urlparse(group.get('kbServer', self.kb_server)).netloc
                logger.info(f"已切换到群组: {self.config.group_name}, kb_guid={self.kb_guid}")
                return
        raise Exception(f'群组不存在: {self.config.group_name}')

    # ================================================================
    # 笔记 CRUD（默认协作笔记）
    # ================================================================

    def create_note(self, title, content='', category="/My Notes/", tags="",
                    content_type='markdown'):
        """
        创建笔记（默认协作笔记）
        :param title: 标题
        :param content: 内容（Markdown或纯文本）
        :param category: 分类路径
        :param tags: 标签（逗号分隔）
        :param content_type: 'markdown' | 'blocks' | 'html'
            - markdown: 自动转换为 blocks
            - blocks: content 已是 blocks 列表
            - html: 创建传统 HTML 笔记
        :return: {docGuid, editorToken, title, category}
        """
        if content_type == 'html':
            return self._create_html_note(title, content, category, tags)

        if content_type == 'blocks':
            blocks = content
        else:
            blocks = self.markdown_to_blocks(content)

        return self.create_collaboration_note(title, blocks, category, tags)

    def update_note(self, doc_guid, content='', title=None, content_type='markdown'):
        """
        更新笔记（默认协作笔记）
        :param doc_guid: 笔记GUID
        :param content: 新内容
        :param title: 可选新标题
        :param content_type: 同 create_note
        """
        if content_type == 'blocks':
            blocks = content
        elif content_type == 'html':
            return self.save_note(doc_guid, title or '', content)
        else:
            blocks = self.markdown_to_blocks(content)

        return self.update_collaboration_note(doc_guid, blocks, title)

    def delete_note(self, doc_guid):
        """
        删除笔记（移到回收站）
        :param doc_guid: 笔记GUID
        """
        result = self._delete(f'/ks/note/delete/{self.kb_guid}/{doc_guid}')
        logger.info(f"笔记已删除: {doc_guid}")
        return result

    def move_note(self, doc_guid, category):
        """
        移动笔记到指定分类
        :param doc_guid: 笔记GUID
        :param category: 目标分类路径，如 "/My Notes/项目/"
        """
        data = {
            'docGuid': doc_guid,
            'kbGuid': self.kb_guid,
            'category': category,
        }
        result = self._put(
            f'/ks/note/save/{self.kb_guid}/{doc_guid}',
            data=data,
            params={'infoOnly': '1'}
        )
        logger.info(f"笔记已移动: {doc_guid} -> {category}")
        return result

    def copy_note(self, doc_guid, title=None, category=None):
        """
        复制笔记
        :param doc_guid: 源笔记GUID
        :param title: 新标题（默认 "标题 - 副本"）
        :param category: 目标分类（默认同源）
        :return: 新笔记信息
        """
        # 获取源笔记详情
        detail = self.get_note_detail(doc_guid)
        info = detail.get('info', {})
        src_title = title or (info.get('title', '') + ' - 副本')
        src_category = category or info.get('category', '/My Notes/')
        src_tags = info.get('tags', '')

        note_type = info.get('type', 'document')
        if note_type == 'collaboration':
            # 读取协作笔记内容
            content = self.get_note_content(doc_guid)
            blocks = self.markdown_to_blocks(content)
            return self.create_collaboration_note(src_title, blocks, src_category, src_tags)
        else:
            html = detail.get('html', '')
            return self._create_html_note(src_title, html, src_category, src_tags)

    # ================================================================
    # 协作笔记操作
    # ================================================================

    def create_collaboration_note(self, title, blocks, category="/My Notes/", tags=""):
        """创建协作笔记并写入初始内容"""
        url = f'{self.kb_server}/ks/note/create/{self.kb_guid}'
        params = {'clientType': 'web', 'clientVersion': '4.0', 'lang': 'zh-cn'}
        data = {
            'kbGuid': self.kb_guid,
            'html': '',
            'category': category,
            'owner': self.config.user_id,
            'tags': tags,
            'title': title,
            'type': 'collaboration',
        }
        resp = requests.post(url, params=params, json=data, headers={
            'X-Wiz-Token': self.token, 'content-type': 'application/json'
        })
        result = resp.json()
        if result.get('returnCode') != 200:
            raise Exception(f'创建协作笔记失败: {result}')

        doc_guid = result['result']['docGuid']
        editor_token = result['editor']['editorToken']
        logger.info(f"协作笔记已创建: doc_guid={doc_guid}, title={title}")

        if blocks:
            self._ws_write_collaboration(doc_guid, editor_token, 0, blocks)

        return {
            'docGuid': doc_guid,
            'editorToken': editor_token,
            'title': title,
            'category': category,
        }

    def update_collaboration_note(self, doc_guid, blocks, title=None):
        """更新协作笔记内容（del + create 覆盖写）"""
        if title:
            self._put(
                f'/ks/note/save/{self.kb_guid}/{doc_guid}',
                data={
                    'category': '', 'docGuid': doc_guid,
                    'kbGuid': self.kb_guid, 'title': title,
                    'html': '', 'resources': []
                },
                params={'infoOnly': '1', 'clientType': 'web', 'clientVersion': '4.0', 'lang': 'zh-cn'}
            )

        token_info = self.get_collaboration_token(doc_guid)
        editor_token = token_info['editorToken'] if isinstance(token_info, dict) else token_info
        raw_content = self.get_collaboration_content(editor_token, doc_guid)
        content_data = json.loads(raw_content)
        current_v = content_data.get('data', {}).get('v', 0)
        doc_type = content_data.get('data', {}).get('type')

        if doc_type is None or current_v == 0:
            self._ws_write_collaboration(doc_guid, editor_token, 0, blocks)
        else:
            self._ws_write_collaboration(doc_guid, editor_token, current_v, blocks, delete_first=True)

        logger.info(f"协作笔记已更新: doc_guid={doc_guid}")
        return {'docGuid': doc_guid, 'status': 'updated'}

    # ================================================================
    # 笔记读取
    # ================================================================

    def get_note_list(self, version=0, count=50):
        return self._get(
            f'/ks/note/list/version/{self.kb_guid}',
            params={'version': version, 'count': count}
        )

    def get_notes_by_category(self, category, count=50, start=0):
        """
        按分类获取笔记列表
        :param category: 分类路径
        :param count: 返回数量
        :param start: 起始位置
        """
        return self._get(
            f'/ks/note/list/{self.kb_guid}',
            params={'category': category, 'count': count, 'start': start}
        )

    def search_notes(self, keyword, with_abstract=True, with_favor=False):
        return self._get(
            f'/ks/note/search/{self.kb_guid}',
            params={
                'ss': keyword,
                'withAbstract': 'true' if with_abstract else 'false',
                'withFavor': 'true' if with_favor else 'false',
                'clientType': 'web', 'clientVersion': '4.0', 'lang': 'zh-cn'
            }
        )

    def get_note_detail(self, doc_guid):
        return self._get(
            f'/ks/note/download/{self.kb_guid}/{doc_guid}',
            params={'downloadInfo': '0', 'downloadData': '1'}
        )

    def get_note_content(self, doc_guid):
        """获取笔记正文（自动检测协作笔记）"""
        detail = self.get_note_detail(doc_guid)
        info = detail.get('info', {})
        note_type = info.get('type', 'document')

        if note_type == 'collaboration':
            try:
                token_info = self.get_collaboration_token(doc_guid)
                editor_token = token_info['editorToken'] if isinstance(token_info, dict) else token_info
                raw_content = self.get_collaboration_content(editor_token, doc_guid)
                content_data = json.loads(raw_content)
                inner_data = content_data.get('data', {})
                if inner_data.get('type') is None and inner_data.get('v', 0) == 0:
                    return ''
                return self.parse_collaboration_content(raw_content)
            except Exception as e:
                logger.error(f"协作笔记获取失败，回退: {e}")
                return detail.get('html', '')

        return detail.get('html', '')

    # ================================================================
    # 分类/文件夹管理
    # ================================================================

    def list_categories(self):
        """获取所有分类（文件夹）列表"""
        return self._get(f'/ks/category/all/{self.kb_guid}')

    def create_category(self, parent, name):
        """
        创建分类
        :param parent: 父分类路径，如 "/My Notes/"
        :param name: 新分类名
        :return: 创建结果
        """
        category = parent.rstrip('/') + '/' + name + '/'
        return self._post(
            f'/ks/category/create/{self.kb_guid}',
            data={'category': category}
        )

    def delete_category(self, category):
        """
        删除分类（文件夹）
        :param category: 分类路径
        """
        return self._delete(
            f'/ks/category/delete/{self.kb_guid}',
            params={'category': category}
        )

    def rename_category(self, old_category, new_name):
        """
        重命名分类
        :param old_category: 原分类路径
        :param new_name: 新名称
        """
        # 解析父路径
        parts = old_category.rstrip('/').rsplit('/', 1)
        parent = parts[0] + '/' if len(parts) > 1 else '/'
        new_category = parent + new_name + '/'
        return self._post(
            f'/ks/category/rename/{self.kb_guid}',
            data={'oldCategory': old_category, 'newCategory': new_category}
        )

    # ================================================================
    # 标签管理
    # ================================================================

    def list_tags(self):
        """获取所有标签"""
        return self._get(f'/ks/tag/all/{self.kb_guid}')

    def add_tags(self, doc_guid, tags):
        """
        为笔记添加标签
        :param doc_guid: 笔记GUID
        :param tags: 标签列表或逗号分隔字符串
        """
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        return self._post(
            f'/ks/tag/add/{self.kb_guid}/{doc_guid}',
            data={'tags': tags}
        )

    def remove_tags(self, doc_guid, tags):
        """移除笔记标签"""
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        return self._post(
            f'/ks/tag/remove/{self.kb_guid}/{doc_guid}',
            data={'tags': tags}
        )

    def rename_tag(self, old_name, new_name):
        """重命名标签（全局）"""
        return self._post(
            f'/ks/tag/rename/{self.kb_guid}',
            data={'oldTag': old_name, 'newTag': new_name}
        )

    # ================================================================
    # 评论
    # ================================================================

    def get_comments(self, doc_guid):
        """获取笔记评论列表"""
        return self._get(
            f'/ks/comment/list/{self.kb_guid}/{doc_guid}',
            params={'clientType': 'web', 'clientVersion': '4.0'}
        )

    def add_comment(self, doc_guid, text):
        """
        添加评论
        :param doc_guid: 笔记GUID
        :param text: 评论内容
        """
        return self._post(
            f'/ks/comment/create/{self.kb_guid}/{doc_guid}',
            data={
                'text': text,
                'docGuid': doc_guid,
                'kbGuid': self.kb_guid,
            },
            params={'clientType': 'web', 'clientVersion': '4.0'}
        )

    def delete_comment(self, doc_guid, comment_guid):
        """删除评论"""
        return self._delete(
            f'/ks/comment/delete/{self.kb_guid}/{doc_guid}/{comment_guid}'
        )

    # ================================================================
    # 历史版本
    # ================================================================

    def get_note_history(self, doc_guid):
        """获取笔记历史版本列表"""
        return self._get(
            f'/ks/note/history/{self.kb_guid}/{doc_guid}',
            params={'clientType': 'web', 'clientVersion': '4.0'}
        )

    def get_note_version(self, doc_guid, version_id):
        """
        获取指定历史版本内容
        :param doc_guid: 笔记GUID
        :param version_id: 版本ID
        """
        return self._get(
            f'/ks/note/version/{self.kb_guid}/{doc_guid}/{version_id}',
            params={'clientType': 'web', 'clientVersion': '4.0'}
        )

    # ================================================================
    # 分享
    # ================================================================

    def share_note(self, doc_guid, access='read', expire_days=30):
        """
        分享笔记，返回分享链接
        :param doc_guid: 笔记GUID
        :param access: 'read' 或 'edit'
        :param expire_days: 过期天数，0 表示永久
        :return: 分享信息（含URL）
        """
        return self._post(
            f'/ks/share/create/{self.kb_guid}/{doc_guid}',
            data={
                'docGuid': doc_guid,
                'kbGuid': self.kb_guid,
                'access': access,
                'expire': expire_days * 86400 if expire_days > 0 else 0,
            }
        )

    def list_shares(self):
        """列出所有分享"""
        return self._get(f'/ks/share/list/{self.kb_guid}')

    def cancel_share(self, share_id):
        """取消分享"""
        return self._delete(f'/ks/share/delete/{self.kb_guid}/{share_id}')

    # ================================================================
    # 附件操作
    # ================================================================

    def get_note_attachments(self, doc_guid):
        return self._get(
            f'/ks/note/attachments/{self.kb_guid}/{doc_guid}',
            params={'extra': '1', 'clientType': 'web', 'clientVersion': '4.0'}
        )

    def download_attachment(self, doc_guid, att_guid):
        url = f'{self.kb_server}/ks/attachment/download/{self.kb_guid}/{doc_guid}/{att_guid}'
        timeout = (self.ATTACHMENT_CONNECT_TIMEOUT_S, self.ATTACHMENT_READ_TIMEOUT_S)
        resp = requests.get(url, params={'clientType': 'web', 'clientVersion': '4.0'},
                            headers={'X-Wiz-Token': self.token}, stream=True, timeout=timeout)
        if resp.status_code != 200:
            raise Exception(f'下载附件失败: HTTP {resp.status_code}')
        return resp.content

    def upload_attachment(self, doc_guid, file_path, name=None):
        """
        上传附件到笔记
        :param doc_guid: 笔记GUID
        :param file_path: 本地文件路径
        :param name: 附件名称（默认取文件名）
        :return: 附件信息
        """
        import os
        name = name or os.path.basename(file_path)
        url = f'{self.kb_server}/ks/attachment/upload/{self.kb_guid}/{doc_guid}'
        with open(file_path, 'rb') as f:
            resp = requests.post(
                url,
                files={'file': (name, f)},
                headers={'X-Wiz-Token': self.token},
                params={'clientType': 'web', 'clientVersion': '4.0'}
            )
        data = resp.json()
        if data.get('returnCode') != 200:
            raise Exception(f'上传附件失败: {data}')
        return data.get('result', data)

    def download_collaboration_resource(self, editor_token, doc_guid, src):
        url = f'{self.kb_server}/editor/{self.kb_guid}/{doc_guid}/resources/{src}'
        timeout = (self.ATTACHMENT_CONNECT_TIMEOUT_S, self.ATTACHMENT_READ_TIMEOUT_S)
        headers = {
            'cookie': f'x-live-editor-token={editor_token}',
            'user-agent': 'Mozilla/5.0'
        }
        resp = requests.get(url, headers=headers, stream=True, timeout=timeout)
        if resp.status_code != 200:
            raise Exception(f'下载协作资源失败: HTTP {resp.status_code}')
        return resp.content

    def get_collaboration_image(self, doc_guid, image_name):
        token_info = self.get_collaboration_token(doc_guid)
        token = token_info['editorToken'] if isinstance(token_info, dict) else token_info
        return self.download_collaboration_resource(token, doc_guid, image_name)

    # ================================================================
    # 传统 HTML 笔记（内部使用）
    # ================================================================

    def _create_html_note(self, title, html, category="/My Notes/", tags=""):
        """创建传统 HTML 笔记（内部方法）"""
        data = {
            'kbGuid': self.kb_guid, 'html': html,
            'category': category, 'owner': self.config.user_id,
            'tags': tags, 'title': title,
        }
        return self._post(
            f'/ks/note/create/{self.kb_guid}',
            data=data,
            params={'clientType': 'web', 'clientVersion': '4.0', 'lang': 'zh-cn'}
        )

    def save_note(self, doc_guid, title, html, category="/My Notes/"):
        """保存/更新传统 HTML 笔记"""
        data = {
            'category': category, 'docGuid': doc_guid,
            'kbGuid': self.kb_guid, 'title': title,
            'html': html, 'resources': []
        }
        return self._put(
            f'/ks/note/save/{self.kb_guid}/{doc_guid}',
            data=data,
            params={'clientType': 'web', 'clientVersion': '4.0', 'lang': 'zh-cn'}
        )

    # ================================================================
    # 协作笔记 WebSocket 协议
    # ================================================================

    def get_collaboration_token(self, doc_guid):
        """获取协作笔记 editorToken"""
        return self._post(f'/ks/note/{self.kb_guid}/{doc_guid}/tokens')

    def get_collaboration_content(self, editor_token, doc_guid):
        """通过 WebSocket 获取协作笔记内容"""
        scheme = 'wss' if self.config.base_url.startswith('https') else 'ws'
        ws_url = f"{scheme}://{self.domain}/editor/{self.kb_guid}/{doc_guid}"
        sslopt = None
        if scheme == 'wss':
            import certifi
            sslopt = {'cert_reqs': ssl.CERT_REQUIRED, 'ca_certs': certifi.where()}

        hs = {
            "a": "hs", "id": None,
            "auth": {
                "appId": self.kb_guid, "docId": doc_guid,
                "userId": self.user_guid, "permission": "w", "token": editor_token
            }
        }

        ws = create_connection(ws_url, sslopt=sslopt, timeout=10)
        ws.send(json.dumps(hs))
        init_resp = ws.recv()  # server returns {"a":"init",...}

        ws.send(json.dumps({"a": "f", "c": self.kb_guid, "d": doc_guid, "v": None}))
        ws.recv()  # ack
        content = ws.recv()  # actual content

        ws.send(json.dumps({"a": "s", "c": self.kb_guid, "d": doc_guid, "v": None}))
        ws.recv()
        ws.close()
        return content

    def _ws_write_collaboration(self, doc_guid, editor_token, version, blocks,
                                delete_first=False):
        """通过 WebSocket 写入协作笔记"""
        scheme = 'wss' if self.config.base_url.startswith('https') else 'ws'
        ws_url = f"{scheme}://{self.domain}/editor/{self.kb_guid}/{doc_guid}"
        sslopt = None
        if scheme == 'wss':
            import certifi
            sslopt = {'cert_reqs': ssl.CERT_REQUIRED, 'ca_certs': certifi.where()}

        hs = {
            'a': 'hs', 'id': None,
            'auth': {
                'appId': self.kb_guid, 'docId': doc_guid,
                'userId': self.user_guid, 'permission': 'w', 'token': editor_token
            }
        }

        ws = create_connection(ws_url, sslopt=sslopt, timeout=10)
        ws.send(json.dumps(hs))
        init_resp = ws.recv()  # server returns {"a":"init",...}

        # 同步
        ws.send(json.dumps({'a': 'f', 'c': self.kb_guid, 'd': doc_guid, 'v': None}))
        ws.recv()
        sync_content = ws.recv()
        try:
            server_v = json.loads(sync_content).get('data', {}).get('v', 0)
            if server_v > version:
                version = server_v
        except Exception:
            pass

        src = str(uuid.uuid4())[:20]
        seq = 1
        v = version

        if delete_first:
            ws.send(json.dumps({
                'a': 'op', 'c': self.kb_guid, 'd': doc_guid,
                'v': v, 'src': src, 'seq': seq, 'del': True,
            }))
            ws.recv()
            seq += 1
            v += 1

        doc_data = {
            'blocks': blocks,
            'comments': [], 'meta': {},
            'authors': [], 'commentators': [],
        }

        ws.send(json.dumps({
            'a': 'op', 'c': self.kb_guid, 'd': doc_guid,
            'v': v, 'src': src, 'seq': seq,
            'create': {
                'type': 'http://sharejs.org/types/JSONv1',
                'data': doc_data,
            }
        }))
        ws.recv()

        ws.send(json.dumps({'a': 's', 'c': self.kb_guid, 'd': doc_guid, 'v': None}))
        try:
            ws.recv()
        except Exception:
            pass
        ws.close()

    # ================================================================
    # Markdown → Blocks 转换器
    # ================================================================

    def markdown_to_blocks(self, markdown_text):
        """
        将 Markdown 文本转换为协作笔记 blocks 列表
        支持：标题(#/##/###)、段落、粗体、斜体、行内代码、链接、
              有序/无序列表、复选框、引用、代码块、表格、分隔线、图片
        """
        if not markdown_text or not markdown_text.strip():
            return []

        blocks = []
        lines = markdown_text.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # 空行跳过
            if not line.strip():
                i += 1
                continue

            # 代码块
            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip()
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # 跳过结束的 ```
                code_id = str(uuid.uuid4())[:8]
                child_id = f'_code_{code_id}_0'
                blocks.append({
                    'id': code_id,
                    'type': 'code',
                    'language': lang,
                    'children': [child_id],
                })
                blocks.append({
                    '__id': child_id,
                    '__type': 'code_cell',
                    'text': [{'insert': '\n'.join(code_lines)}],
                })
                continue

            # 标题
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = self._parse_inline_markdown(heading_match.group(2))
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'text',
                    'text': text,
                    'heading': min(level, 6),
                })
                i += 1
                continue

            # 分隔线
            if re.match(r'^(-{3,}|\*{3,}|_{3,})$', line.strip()):
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'embed',
                    'embedType': 'hr',
                    'embedData': {},
                })
                i += 1
                continue

            # 引用
            if line.strip().startswith('>'):
                text = self._parse_inline_markdown(line.strip().lstrip('> ').lstrip())
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'text',
                    'text': text,
                    'quoted': True,
                })
                i += 1
                continue

            # 复选框
            check_match = re.match(r'^(\s*)- \[([ xX])\] (.+)$', line)
            if check_match:
                text = self._parse_inline_markdown(check_match.group(3))
                level = len(check_match.group(1)) // 2 + 1
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'list',
                    'text': text,
                    'level': level,
                    'checkbox': 'checked' if check_match.group(2) != ' ' else 'unchecked',
                })
                i += 1
                continue

            # 无序列表
            ul_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
            if ul_match:
                text = self._parse_inline_markdown(ul_match.group(2))
                level = len(ul_match.group(1)) // 2 + 1
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'list',
                    'text': text,
                    'level': level,
                })
                i += 1
                continue

            # 有序列表
            ol_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
            if ol_match:
                text = self._parse_inline_markdown(ol_match.group(3))
                level = len(ol_match.group(1)) // 2 + 1
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'list',
                    'text': text,
                    'level': level,
                    'ordered': True,
                    'start': int(ol_match.group(2)),
                })
                i += 1
                continue

            # 表格
            if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i + 1]):
                headers = [c.strip() for c in line.strip('|').split('|')]
                i += 2  # 跳过分隔行
                rows = []
                while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                    row = [c.strip() for c in lines[i].strip('|').split('|')]
                    rows.append(row)
                    i += 1
                block, extra = self.table_block(headers, rows)
                blocks.append(block)
                # 添加额外数据
                for key, val in extra.items():
                    blocks.append({'__id': key, **val})
                continue

            # 图片
            img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip())
            if img_match:
                blocks.append({
                    'id': str(uuid.uuid4())[:8],
                    'type': 'embed',
                    'embedType': 'image',
                    'embedData': {'src': img_match.group(2), 'alt': img_match.group(1)},
                })
                i += 1
                continue

            # 普通段落
            text = self._parse_inline_markdown(line)
            blocks.append({
                'id': str(uuid.uuid4())[:8],
                'type': 'text',
                'text': text,
            })
            i += 1

        return blocks

    def _parse_inline_markdown(self, text):
        """解析行内 Markdown 为 text 数组（insert + attributes）"""
        if not text.strip():
            return [{'insert': text}]

        result = []
        # 简化处理：按优先级匹配粗体、斜体、代码、链接
        pattern = re.compile(
            r'(\*\*\*(.+?)\*\*\*)'   # 粗斜体
            r'|(\*\*(.+?)\*\*)'       # 粗体
            r'|(\*(.+?)\*)'           # 斜体
            r'|(`([^`]+)`)'           # 行内代码
            r'|(\[([^\]]+)\]\(([^)]+)\))'  # 链接
            r'|([^*\[`]+)'           # 普通文本
        )

        pos = 0
        while pos < len(text):
            match = pattern.match(text, pos)
            if not match:
                result.append({'insert': text[pos]})
                pos += 1
                continue

            if match.group(2):  # 粗斜体
                result.append({'insert': match.group(2), 'attributes': {'style-bold': True, 'style-italic': True}})
            elif match.group(4):  # 粗体
                result.append({'insert': match.group(4), 'attributes': {'style-bold': True}})
            elif match.group(6):  # 斜体
                result.append({'insert': match.group(6), 'attributes': {'style-italic': True}})
            elif match.group(8):  # 代码
                result.append({'insert': match.group(8), 'attributes': {'style-code': True}})
            elif match.group(10):  # 链接
                result.append({'insert': match.group(10), 'attributes': {'link': match.group(11)}})
            elif match.group(12):  # 普通文本
                result.append({'insert': match.group(12)})

            pos = match.end()

        return result if result else [{'insert': text}]

    # ================================================================
    # 协作笔记内容解析
    # ================================================================

    def parse_collaboration_content(self, raw_content):
        """解析协作笔记 JSON 为可读 Markdown 文本"""
        try:
            content_data = json.loads(raw_content) if isinstance(raw_content, str) else raw_content
        except json.JSONDecodeError:
            return str(raw_content)

        if not isinstance(content_data, dict) or 'data' not in content_data:
            return str(content_data)

        data_section = content_data['data']
        if not isinstance(data_section, dict) or 'data' not in data_section:
            return json.dumps(content_data, ensure_ascii=False, indent=2)

        inner_data = data_section['data']
        if 'blocks' not in inner_data:
            return json.dumps(content_data, ensure_ascii=False, indent=2)

        blocks = inner_data['blocks']
        lines = []
        for block in blocks:
            text = self._parse_block(inner_data, block)
            if text:
                lines.append(text)

        return '\n'.join(lines)

    def _parse_block(self, full_data, block):
        block_type = block.get('type', '')

        if block_type == 'text':
            text = self._parse_text_array(block.get('text', []))
            heading = block.get('heading')
            if heading:
                return f"{'#' * heading} {text}"
            elif block.get('quoted'):
                return f"> {text}"
            return text

        elif block_type == 'list':
            text = self._parse_text_array(block.get('text', []))
            level = block.get('level', 1)
            indent = '  ' * (level - 1)
            checkbox = block.get('checkbox')
            prefix = ''
            if checkbox == 'checked':
                prefix = '[x] '
            elif checkbox == 'unchecked':
                prefix = '[ ] '
            if block.get('ordered'):
                return f"{indent}{block.get('start', 1)}. {prefix}{text}"
            return f"{indent}- {prefix}{text}"

        elif block_type == 'code':
            language = block.get('language', '')
            children = block.get('children', [])
            code_lines = []
            for child_id in children:
                if child_id in full_data:
                    child_data = full_data[child_id]
                if child_data and isinstance(child_data, dict) and 'text' in child_data:
                        if child_data['text']:
                            code_lines.append(child_data['text'][0].get('insert', ''))
                        else:
                            code_lines.append('')
            return f"```{language}\n{'\n'.join(code_lines)}\n```"

        elif block_type == 'table':
            cols = block.get('cols', 0)
            children = block.get('children', [])
            cells = []
            for child_id in children:
                if child_id in full_data:
                    child_data = full_data[child_id]
                if child_data and isinstance(child_data, dict) and 'text' in child_data:
                        if child_data['text']:
                            cells.append(child_data['text'][0].get('insert', ''))
                        else:
                            cells.append('')
                else:
                    cells.append('')
            if not cells or cols == 0:
                return ''
            header = '| ' + ' | '.join(cells[:cols]) + ' |'
            sep = '| ' + ' | '.join(['---'] * cols) + ' |'
            rows = []
            body = cells[cols:]
            for i in range(0, len(body), cols):
                row = body[i:i + cols]
                while len(row) < cols:
                    row.append('')
                rows.append('| ' + ' | '.join(row) + ' |')
            return header + '\n' + sep + '\n' + '\n'.join(rows)

        elif block_type == 'embed':
            embed_type = block.get('embedType', '')
            embed_data = block.get('embedData', {})
            if embed_type == 'image':
                return f"![图片]({embed_data.get('src', '')})"
            elif embed_type == 'hr':
                return '---'
            return f"<!-- embed: {embed_type} -->"

        return ''

    def _parse_text_array(self, text_array):
        if not text_array:
            return ''
        parts = []
        for text_obj in text_array:
            insert = text_obj.get('insert', '')
            attrs = text_obj.get('attributes', {})
            if not attrs:
                parts.append(insert)
            elif attrs.get('style-bold'):
                parts.append(f"**{insert}**")
            elif attrs.get('style-italic'):
                parts.append(f"*{insert}*")
            elif attrs.get('style-code'):
                parts.append(f"`{insert}`")
            elif attrs.get('link'):
                parts.append(f"[{insert}]({attrs.get('link')})")
            else:
                parts.append(insert)
        return ''.join(parts)

    # ================================================================
    # 笔记模板
    # ================================================================

    @staticmethod
    def get_template(template_name, **kwargs):
        """
        获取预定义模板的 Markdown 内容
        :param template_name: 模板名称
            - weekly_report: 周报
            - meeting_minutes: 会议纪要
            - todo: 待办清单
            - reading_notes: 读书笔记
            - project_plan: 项目计划
            - blank: 空白
        :param kwargs: 模板变量
        :return: Markdown 文本
        """
        templates = {
            'weekly_report': """# {title}

## 本周完成

- 
- 
- 

## 进行中

- 
- 

## 下周计划

- 
- 
- 

## 风险与问题

> 

## 备注

""",
            'meeting_minutes': """# {title}

**日期**: {date}
**参会人**: {attendees}
**记录人**: {recorder}

## 会议议题

1. 

## 讨论内容

### 议题一


### 议题二


## 决议

- [ ] 
- [ ] 

## 后续行动

| 任务 | 负责人 | 截止日期 | 状态 |
|------|--------|----------|------|
|  |  |  | 待开始 |

""",
            'todo': """# {title}

## 🔴 紧急重要

- [ ] 

## 🟡 重要不紧急

- [ ] 
- [ ] 

## 🔵 紧急不重要

- [ ] 

## ⚪ 其他

- [ ] 

""",
            'reading_notes': """# {title}

**书名**: {book_name}
**作者**: {author}
**阅读日期**: {date}

## 核心观点

> 

## 章节摘要

### 第一章


### 第二章


## 精彩摘录

- 
- 
- 

## 个人思考


## 行动清单

- [ ] 
- [ ] 

""",
            'project_plan': """# {title}

## 项目背景


## 目标

1. 
2. 
3. 

## 时间线

| 阶段 | 时间 | 交付物 | 负责人 |
|------|------|--------|--------|
| 需求分析 |  |  |  |
| 设计 |  |  |  |
| 开发 |  |  |  |
| 测试 |  |  |  |
| 上线 |  |  |  |

## 资源需求

- 
- 

## 风险评估

| 风险 | 概率 | 影响 | 应对策略 |
|------|------|------|----------|
|  |  |  |  |

""",
            'blank': """# {title}

""",
        }

        template = templates.get(template_name, templates['blank'])
        return template.format(
            title=kwargs.get('title', '未命名'),
            date=kwargs.get('date', time.strftime('%Y-%m-%d')),
            attendees=kwargs.get('attendees', ''),
            recorder=kwargs.get('recorder', ''),
            book_name=kwargs.get('book_name', ''),
            author=kwargs.get('author', ''),
            **{k: v for k, v in kwargs.items()
               if k not in ('title', 'date', 'attendees', 'recorder', 'book_name', 'author')}
        )

    def create_from_template(self, template_name, title, category="/My Notes/", tags="",
                             **kwargs):
        """
        从模板创建协作笔记
        :param template_name: 模板名称
        :param title: 笔记标题
        :param category: 分类
        :param tags: 标签
        :param kwargs: 模板变量
        """
        kwargs['title'] = title
        md_content = self.get_template(template_name, **kwargs)
        blocks = self.markdown_to_blocks(md_content)
        return self.create_collaboration_note(title, blocks, category, tags)

    # ================================================================
    # Block 快捷构造方法
    # ================================================================

    @staticmethod
    def text_block(text, heading=None, quoted=False, block_id=None):
        block = {
            'id': block_id or str(uuid.uuid4())[:8],
            'type': 'text',
            'text': [{'insert': text}],
        }
        if heading:
            block['heading'] = heading
        if quoted:
            block['quoted'] = True
        return block

    @staticmethod
    def list_block(text, ordered=False, level=1, checkbox=None, block_id=None):
        block = {
            'id': block_id or str(uuid.uuid4())[:8],
            'type': 'list',
            'text': [{'insert': text}],
            'level': level,
        }
        if ordered:
            block['ordered'] = True
            block['start'] = 1
        if checkbox:
            block['checkbox'] = checkbox
        return block

    @staticmethod
    def table_block(headers, rows, block_id=None):
        cols = len(headers)
        children = []
        extra_data = {}
        cell_idx = 0

        for h in headers:
            cell_id = f'_t{block_id or ""}_{cell_idx}'
            children.append(cell_id)
            extra_data[cell_id] = {'text': [{'insert': str(h)}]}
            cell_idx += 1

        for row in rows:
            for cell in row:
                cell_id = f'_t{block_id or ""}_{cell_idx}'
                children.append(cell_id)
                extra_data[cell_id] = {'text': [{'insert': str(cell)}]}
                cell_idx += 1

        block = {
            'id': block_id or str(uuid.uuid4())[:8],
            'type': 'table',
            'cols': cols,
            'children': children,
        }
        return block, extra_data

    @staticmethod
    def code_block(code, language='', block_id=None):
        """快捷方法：创建代码块"""
        code_id = block_id or str(uuid.uuid4())[:8]
        child_id = f'_code_{code_id}_0'
        block = {
            'id': code_id,
            'type': 'code',
            'language': language,
            'children': [child_id],
        }
        extra = {
            child_id: {'__id': child_id, '__type': 'code_cell', 'text': [{'insert': code}]}
        }
        return block, extra

    @staticmethod
    def divider_block():
        """快捷方法：创建分隔线"""
        return {
            'id': str(uuid.uuid4())[:8],
            'type': 'embed',
            'embedType': 'hr',
            'embedData': {},
        }

    @staticmethod
    def image_block(src, alt='图片'):
        """快捷方法：创建图片块"""
        return {
            'id': str(uuid.uuid4())[:8],
            'type': 'embed',
            'embedType': 'image',
            'embedData': {'src': src, 'alt': alt},
        }
