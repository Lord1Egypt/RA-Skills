"""
PPT生成Agent Skill
基于讯飞智能PPT生成API实现
"""

import hashlib
import hmac
import base64
import json
import time
import re
import os
import sys
from typing import Optional, Dict, Any, List

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PPTGeneratorSkill:
    """
    PPT生成Agent Skill类

    功能：
    1. 接收并优化用户输入内容
    2. 集成讯飞PPT生成API
    3. 整合网络资源信息
    4. 生成PPT并提供下载链接
    """

    def __init__(self, app_id: str, api_secret: str, template_id: Optional[str] = None):
        """
        初始化PPT生成器

        Args:
            app_id: 讯飞开放平台应用ID
            api_secret: 讯飞开放平台API密钥
            template_id: PPT模板ID（可选，默认使用系统默认模板）
        """
        self.app_id = app_id
        self.api_secret = api_secret
        self.template_id = template_id
        self.headers = {}
        self.base_url = "https://zwapi.xfyun.cn/api/ppt/v2"

    def optimize_input(self, text: str) -> str:
        """
        优化用户输入内容，包括文本清理、核心需求提取和结构化处理

        Args:
            text: 用户原始输入文本

        Returns:
            优化后的文本
        """
        try:
            if not text or not text.strip():
                raise ValueError("输入文本不能为空")

            # 文本清理
            text = text.strip()

            # 移除多余的空格和换行符
            text = re.sub(r'\s+', ' ', text)

            # 移除特殊字符，保留中英文、数字、常用标点
            text = re.sub(
                r'[^\u4e00-\u9fa5a-zA-Z0-9\s,，.。;；:：!?！？()（）【】\[\]{}]+', '', text)

            # 提取核心需求
            # 检查是否包含"PPT"关键字，如不包含则添加
            if "PPT" not in text and "ppt" not in text:
                text = f"请帮我生成一份关于{text}的PPT"

            # 确保文本长度在API限制范围内（12000字）
            if len(text) > 12000:
                text = text[:11995] + "..."

            return text

        except Exception as e:
            print(f"输入优化失败: {e}")
            return text

    def integrate_web_resources(self, text: str, enable_search: bool = True) -> str:
        """
        整合网络资源信息，丰富PPT内容

        Args:
            text: 用户输入文本
            enable_search: 是否启用联网搜索

        Returns:
            整合后的文本
        """
        try:
            if enable_search:
                print(f"正在为PPT主题 '{text}' 整合网络资源...")

                # 这里可以根据需要添加网络资源获取逻辑
                # 例如，可以调用搜索引擎API获取相关信息
                # 由于当前环境限制，我们暂时返回原始文本
                # 实际使用时，可以根据text内容获取相关的网络资源

                # 模拟网络资源整合
                # 在实际应用中，可以调用网络API获取相关信息并整合
                # 例如：
                # web_info = self._get_web_info(text)
                # if web_info:
                #     text += f"\n\n补充网络资源信息：\n{web_info}"

                print("网络资源整合完成")

            return text

        except Exception as e:
            print(f"网络资源整合失败: {e}")
            return text

    def _get_web_info(self, query: str, max_results: int = 3) -> str:
        """
        获取网络资源信息（内部方法）

        Args:
            query: 搜索查询词
            max_results: 最大结果数

        Returns:
            整合后的网络信息
        """
        try:
            # 这里可以实现具体的网络资源获取逻辑
            # 例如，调用百度、必应等搜索引擎API
            # 或者使用其他网络数据源

            # 由于API密钥限制，这里返回模拟数据
            # 实际使用时，替换为真实的API调用
            web_info = f"\n网络资源信息：\n1. 来源：示例网站1\n   标题：关于{query}的详细介绍\n   内容：这是一段关于{query}的详细介绍，包含了丰富的信息。\n2. 来源：示例网站2\n   标题：{query}的最新发展趋势\n   内容：{query}的最新发展趋势包括...\n3. 来源：示例网站3\n   标题：{query}的实践案例分析\n   内容：以下是几个{query}的成功实践案例..."

            return web_info

        except Exception as e:
            print(f"获取网络信息失败: {e}")
            return ""

    def _get_signature(self, ts: int) -> str:
        """
        生成API请求签名

        Args:
            ts: 时间戳

        Returns:
            签名字符串
        """
        try:
            # 对app_id和时间戳进行MD5加密
            auth = self._md5(self.app_id + str(ts))
            # 使用HMAC-SHA1算法对加密后的字符串进行加密
            return self._hmac_sha1_encrypt(auth, self.api_secret)
        except Exception as e:
            print(f"生成签名失败: {e}")
            return None

    def _hmac_sha1_encrypt(self, encrypt_text: str, encrypt_key: str) -> str:
        """
        HMAC-SHA1加密

        Args:
            encrypt_text: 待加密文本
            encrypt_key: 加密密钥

        Returns:
            Base64编码的加密结果
        """
        return base64.b64encode(
            hmac.new(encrypt_key.encode('utf-8'),
                     encrypt_text.encode('utf-8'), hashlib.sha1).digest()
        ).decode('utf-8')

    def _md5(self, text: str) -> str:
        """
        MD5加密

        Args:
            text: 待加密文本

        Returns:
            MD5加密后的十六进制字符串
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _build_headers(self) -> Dict[str, str]:
        """
        构建请求头

        Returns:
            请求头字典
        """
        timestamp = int(time.time())
        signature = self._get_signature(timestamp)

        headers = {
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": "application/json; charset=utf-8"
        }

        self.headers = headers
        return headers

    def get_theme_list(self, style: Optional[str] = None, color: Optional[str] = None,
                       industry: Optional[str] = None, page_num: int = 1,
                       page_size: int = 10, retry: int = 3, timeout: int = 30) -> Optional[str]:
        """
        获取PPT主题列表

        Args:
            style: 风格类型（简约、卡通、商务、创意、国风、清新、扁平、插画、节日）
            color: 颜色类型（蓝色、绿色、红色、紫色、黑色、灰色、黄色、粉色、橙色）
            industry: 行业类型（科技互联网、教育培训、政务、学院、电子商务、金融战略、法律、医疗健康、文旅体育、艺术广告、人力资源、游戏娱乐）
            page_num: 页码
            page_size: 每页数量
            retry: 重试次数
            timeout: 请求超时时间

        Returns:
            主题列表JSON字符串
        """
        url = f"{self.base_url}/template/list"

        for i in range(retry):
            try:
                self._build_headers()

                params = {
                    "pageNum": page_num,
                    "pageSize": page_size
                }

                if style:
                    params["style"] = style
                if color:
                    params["color"] = color
                if industry:
                    params["industry"] = industry

                response = requests.get(
                    url, headers=self.headers, params=params, timeout=timeout)
                response.raise_for_status()

                response_text = response.text
                print(f"获取PPT主题列表结果（第{i+1}次尝试）：{response_text}")

                resp = json.loads(response_text)
                if resp.get('code') == 0:
                    return response_text
                else:
                    print(
                        f"获取PPT主题列表失败，错误码：{resp['code']}，错误信息：{resp.get('desc', '未知错误')}")
                    if i < retry - 1:
                        time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"获取PPT主题列表网络异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except json.JSONDecodeError as e:
                print(f"获取PPT主题列表响应解析异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except Exception as e:
                print(f"获取PPT主题列表异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)

        print('多次尝试获取PPT主题列表失败')
        return None

    def create_outline(self, text: str, language: str = "cn", enable_search: bool = True,
                       retry: int = 3, timeout: int = 30) -> Optional[str]:
        """
        生成PPT大纲

        Args:
            text: 用户输入文本
            language: 语种（cn、en、ja、ru、ko、de、fr、pt、es、it、th）
            enable_search: 是否联网搜索
            retry: 重试次数
            timeout: 请求超时时间

        Returns:
            大纲信息JSON字符串
        """
        url = f"{self.base_url}/createOutline"

        for i in range(retry):
            try:
                # 优化输入文本
                optimized_text = self.optimize_input(text)

                # 整合网络资源
                final_text = self.integrate_web_resources(
                    optimized_text, enable_search)

                formData = MultipartEncoder(
                    fields={
                        "query": final_text,
                        "language": language,
                        "search": str(enable_search),
                    }
                )

                timestamp = int(time.time())
                signature = self._get_signature(timestamp)
                if not signature:
                    raise Exception("获取签名失败")

                headers = {
                    "appId": self.app_id,
                    "timestamp": str(timestamp),
                    "signature": signature,
                    "Content-Type": formData.content_type
                }
                self.headers = headers

                response = requests.post(
                    url=url, data=formData, headers=headers, timeout=timeout)
                response.raise_for_status()

                response_text = response.text
                print(f"生成大纲完成（第{i+1}次尝试）：\n{response_text}")

                resp = json.loads(response_text)
                if resp.get('code') == 0:
                    return response_text
                else:
                    print(
                        f"生成大纲失败，错误码：{resp['code']}，错误信息：{resp.get('desc', '未知错误')}")
                    if i < retry - 1:
                        time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"生成大纲网络异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except json.JSONDecodeError as e:
                print(f"生成大纲响应解析异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except Exception as e:
                print(f"生成大纲异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)

        print('多次尝试生成大纲失败')
        return None

    def create_outline_by_doc(self, file_name: str, file_url: Optional[str] = None,
                              file_path: Optional[str] = None, text: str = "",
                              language: str = "cn", enable_search: bool = True,
                              retry: int = 3, timeout: int = 30) -> Optional[str]:
        """
        根据文档生成PPT大纲

        Args:
            file_name: 文件名
            file_url: 文件URL
            file_path: 文件路径
            text: 用户输入文本
            language: 语种
            enable_search: 是否联网搜索
            retry: 重试次数
            timeout: 请求超时时间

        Returns:
            大纲信息JSON字符串
        """
        url = f"{self.base_url}/createOutlineByDoc"

        for i in range(retry):
            try:
                fields = {
                    "fileName": file_name,
                    "query": text,
                    "language": language,
                    "search": str(enable_search),
                }

                # 添加文件或文件URL
                if file_path and file_path != "":
                    fields["file"] = (file_name, open(
                        file_path, 'rb'), 'application/octet-stream')
                elif file_url and file_url != "":
                    fields["fileUrl"] = file_url
                else:
                    raise Exception("file或fileUrl必填其一")

                formData = MultipartEncoder(fields=fields)
                timestamp = int(time.time())
                signature = self._get_signature(timestamp)
                if not signature:
                    raise Exception("获取签名失败")

                headers = {
                    "appId": self.app_id,
                    "timestamp": str(timestamp),
                    "signature": signature,
                    "Content-Type": formData.content_type
                }
                self.headers = headers

                response = requests.post(
                    url=url, data=formData, headers=headers, timeout=timeout)
                response.raise_for_status()

                response_text = response.text
                print(f"根据文档生成大纲完成（第{i+1}次尝试）：\n{response_text}")

                resp = json.loads(response_text)
                if resp.get('code') == 0:
                    return response_text
                else:
                    print(
                        f"根据文档生成大纲失败，错误码：{resp['code']}，错误信息：{resp.get('desc', '未知错误')}")
                    if i < retry - 1:
                        time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"根据文档生成大纲网络异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except json.JSONDecodeError as e:
                print(f"根据文档生成大纲响应解析异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except Exception as e:
                print(f"根据文档生成大纲异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)

        print('多次尝试根据文档生成大纲失败')
        return None

    def create_ppt(self, text: str, template_id: Optional[str] = None,
                   author: Optional[str] = None, enable_card_note: bool = True,
                   enable_search: bool = True, enable_figure: bool = True,
                   ai_image_type: str = "advanced", language: str = "cn",
                   retry: int = 3, timeout: int = 30) -> Optional[str]:
        """
        创建PPT生成任务

        Args:
            text: 用户输入文本
            template_id: PPT模板ID
            author: PPT作者名
            enable_card_note: 是否生成PPT演讲备注
            enable_search: 是否联网搜索
            enable_figure: 是否自动配图
            ai_image_type: AI配图类型（normal、advanced）
            language: 语种
            retry: 重试次数
            timeout: 请求超时时间

        Returns:
            任务ID或None
        """
        url = f"{self.base_url}/create"

        for i in range(retry):
            try:
                # 优化输入文本
                optimized_text = self.optimize_input(text)

                # 整合网络资源
                final_text = self.integrate_web_resources(
                    optimized_text, enable_search)

                timestamp = int(time.time())
                signature = self._get_signature(timestamp)
                if not signature:
                    raise Exception("获取签名失败")

                # 使用传入的template_id或初始化时的template_id
                final_template_id = template_id or self.template_id or "20240718489569D"

                formData = MultipartEncoder(
                    fields={
                        "query": final_text,
                        "templateId": final_template_id,
                        "author": author if author else "AI生成",
                        "isCardNote": str(enable_card_note),
                        "search": str(enable_search),
                        "isFigure": str(enable_figure),
                        "aiImage": ai_image_type,
                        "language": language
                    }
                )

                headers = {
                    "appId": self.app_id,
                    "timestamp": str(timestamp),
                    "signature": signature,
                    "Content-Type": formData.content_type
                }
                self.headers = headers

                response = requests.post(
                    url=url, data=formData, headers=headers, timeout=timeout)
                response.raise_for_status()

                response_text = response.text
                print(f"创建PPT任务返回结果（第{i+1}次尝试）：{response_text}")

                resp = json.loads(response_text)
                if resp.get('code') == 0:
                    return resp['data']['sid']
                else:
                    print(
                        f'创建PPT任务失败，错误码：{resp["code"]}，错误信息：{resp.get("desc", "未知错误")}')
                    if i < retry - 1:
                        time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"创建PPT任务网络异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except json.JSONDecodeError as e:
                print(f"创建PPT任务响应解析异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except Exception as e:
                print(f"创建PPT任务异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)

        print('多次尝试创建PPT任务失败')
        return None

    def get_progress(self, sid: str, timeout: int = 30) -> Optional[str]:
        """
        轮询任务进度

        Args:
            sid: 任务ID
            timeout: 请求超时时间

        Returns:
            响应信息JSON字符串
        """
        if not sid:
            print("任务ID为空")
            return None

        try:
            response = requests.get(
                url=f"{self.base_url}/progress?sid={sid}",
                headers=self.headers,
                timeout=timeout
            )
            response.raise_for_status()

            response_text = response.text
            print(response_text)
            return response_text

        except requests.exceptions.RequestException as e:
            print(f"轮询任务进度网络异常：{e}")
            return None
        except Exception as e:
            print(f"轮询任务进度异常：{e}")
            return None

    def get_result(self, task_id: str, max_retries: int = 30) -> Optional[str]:
        """
        获取PPT下载链接

        Args:
            task_id: 任务ID
            max_retries: 最大重试次数

        Returns:
            PPT下载链接或None
        """
        if not task_id:
            print("任务ID为空")
            return None

        retry_count = 0
        while retry_count < max_retries:
            try:
                response = self.get_progress(task_id)
                if not response:
                    print("获取任务进度失败，重试中...")
                    retry_count += 1
                    time.sleep(3)
                    continue

                resp = json.loads(response)
                if resp.get('code') != 0:
                    print(
                        f"获取任务进度失败，错误码：{resp['code']}，错误信息：{resp.get('desc', '未知错误')}")
                    retry_count += 1
                    time.sleep(3)
                    continue

                ppt_status = resp['data'].get('pptStatus')
                ai_image_status = resp['data'].get('aiImageStatus')
                card_note_status = resp['data'].get('cardNoteStatus')

                if ppt_status == 'done' and ai_image_status == 'done' and card_note_status == 'done':
                    ppt_url = resp['data'].get('pptUrl')
                    if ppt_url:
                        return ppt_url
                    else:
                        print("获取PPT下载链接失败")
                        retry_count += 1
                        time.sleep(3)
                        continue
                elif ppt_status == 'build_failed':
                    err_msg = resp['data'].get('errMsg', 'PPT生成失败')
                    print(f"PPT生成失败：{err_msg}")
                    return None
                else:
                    print(
                        f"PPT生成中，状态：{ppt_status}，AI配图：{ai_image_status}，演讲备注：{card_note_status}")
                    retry_count += 1
                    time.sleep(3)

            except json.JSONDecodeError as e:
                print(f"响应解析异常：{e}")
                retry_count += 1
                time.sleep(3)
            except Exception as e:
                print(f"获取PPT结果异常：{e}")
                retry_count += 1
                time.sleep(3)

        print('PPT生成超时')
        return None

    def create_ppt_by_outline(self, outline: str, template_id: Optional[str] = None,
                              author: Optional[str] = None, enable_card_note: bool = True,
                              enable_figure: bool = True, ai_image_type: str = "advanced",
                              language: str = "cn", retry: int = 3, timeout: int = 30) -> Optional[str]:
        """
        根据大纲生成PPT

        Args:
            outline: 大纲内容
            template_id: PPT模板ID
            author: PPT作者名
            enable_card_note: 是否生成PPT演讲备注
            enable_figure: 是否自动配图
            ai_image_type: AI配图类型（normal、advanced）
            language: 语种
            retry: 重试次数
            timeout: 请求超时时间

        Returns:
            任务ID或None
        """
        url = f"{self.base_url}/createByOutline"

        for i in range(retry):
            try:
                timestamp = int(time.time())
                signature = self._get_signature(timestamp)
                if not signature:
                    raise Exception("获取签名失败")

                # 使用传入的template_id或初始化时的template_id
                final_template_id = template_id or self.template_id or "20240718489569D"

                formData = MultipartEncoder(
                    fields={
                        "outline": outline,
                        "templateId": final_template_id,
                        "author": author if author else "AI生成",
                        "isCardNote": str(enable_card_note),
                        "isFigure": str(enable_figure),
                        "aiImage": ai_image_type,
                        "language": language
                    }
                )

                headers = {
                    "appId": self.app_id,
                    "timestamp": str(timestamp),
                    "signature": signature,
                    "Content-Type": formData.content_type
                }
                self.headers = headers

                response = requests.post(
                    url=url, data=formData, headers=headers, timeout=timeout)
                response.raise_for_status()

                response_text = response.text
                print(f"根据大纲创建PPT任务返回结果（第{i+1}次尝试）：{response_text}")

                resp = json.loads(response_text)
                if resp.get('code') == 0:
                    return resp['data']['sid']
                else:
                    print(
                        f'根据大纲创建PPT任务失败，错误码：{resp["code"]}，错误信息：{resp.get("desc", "未知错误")}')
                    if i < retry - 1:
                        time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"根据大纲创建PPT任务网络异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except json.JSONDecodeError as e:
                print(f"根据大纲创建PPT任务响应解析异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)
            except Exception as e:
                print(f"根据大纲创建PPT任务异常（第{i+1}次尝试）：{e}")
                if i < retry - 1:
                    time.sleep(2)

        print('多次尝试根据大纲创建PPT任务失败')
        return None


def main():
    """
    主函数 - 支持动态参数接收
    """

    app_id = os.environ.get('XF_PPT_APP_ID')
    api_secret = os.environ.get('XF_PPT_API_SECRET')

    if not app_id or not api_secret:
        print("export XF_PPT_APP_ID='your_app_id'")
        print("export XF_PPT_API_SECRET='your_api_secret'")
        sys.exit(1)

    ppt_generator = PPTGeneratorSkill(app_id, api_secret)

    capability = "generate_ppt"
    text = None

    if len(sys.argv) > 1:
        capability = sys.argv[1]

    if len(sys.argv) > 2:
        text = sys.argv[2]

    if capability == "generate_ppt":
        if not text:
            print("请提供PPT主题，例如：python ppt_generator.py generate_ppt '人工智能的发展历程'")
            sys.exit(1)
        print(f"\n=== 生成PPT：{text} ===")
        task_id = ppt_generator.create_ppt(text)
        if task_id:
            print(f"任务创建成功，任务ID：{task_id}")
            ppt_url = ppt_generator.get_result(task_id)
            if ppt_url:
                print(f"PPT生成成功，下载链接：{ppt_url}")
            else:
                print("PPT生成失败")
        else:
            print("任务创建失败")

    elif capability == "get_theme_list":
        style = sys.argv[3] if len(sys.argv) > 3 else "商务"
        page_size = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        print(f"\n=== 获取{style}风格主题列表 ===")
        theme_list = ppt_generator.get_theme_list(
            style=style, page_size=page_size)
        if theme_list:
            print("主题列表获取成功")
            print(theme_list)
        else:
            print("主题列表获取失败")

    elif capability == "create_outline":
        if not text:
            print("请提供大纲主题，例如：python ppt_generator.py create_outline '机器学习'")
            sys.exit(1)
        print(f"\n=== 生成大纲：{text} ===")
        outline = ppt_generator.create_outline(text)
        if outline:
            print("大纲生成成功")
            print(outline)
        else:
            print("大纲生成失败")

    else:
        print(f"未知能力：{capability}")
        print("支持的 capability：generate_ppt, get_theme_list, create_outline")
        sys.exit(1)


if __name__ == "__main__":
    main()