"""HTTP API客户端封装模块

提供：
- 统一的HTTP请求接口（GET/POST）
- 自动重试（指数退避）
- 速率限制处理（429状态码）
- User-Agent标识
- CurseForge API Key支持
- 文件下载（支持大文件流式下载）
"""

import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union
from urllib.parse import urlencode

try:
    import requests
    from requests.exceptions import (
        RequestException,
        Timeout,
        ConnectionError as ReqConnectionError,
        HTTPError,
    )
except ImportError:
    raise ImportError(
        "缺少requests库，请运行: pip install requests\n"
        "或: pip install -r requirements.txt"
    )

from .logger import get_logger
import sys

# 项目根目录，用于sys.path设置
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config

logger = get_logger("api_client")


class APIClient:
    """通用HTTP API客户端"""

    def __init__(
        self,
        base_url: str = "",
        user_agent: str = None,
        api_key: str = None,
        api_key_header: str = "x-api-key",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        retry_backoff: float = 2.0,
    ):
        """初始化API客户端

        Args:
            base_url: API基础URL
            user_agent: User-Agent字符串
            api_key: API密钥（可选）
            api_key_header: API Key的HTTP头名称
            timeout: 请求超时（秒）
            max_retries: 最大重试次数
            retry_delay: 初始重试延迟（秒）
            retry_backoff: 重试延迟退避系数（每次乘以此系数）
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff

        # 默认请求头
        self.headers = {
            "User-Agent": user_agent or "MC-Skill-V1/1.0",
            "Accept": "application/json",
        }
        if api_key:
            self.headers[api_key_header] = api_key

        # 创建Session复用连接
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _build_url(self, endpoint: str) -> str:
        """构建完整URL"""
        endpoint = endpoint.lstrip("/")
        if self.base_url:
            return f"{self.base_url}/{endpoint}"
        return endpoint

    def _request_with_retry(
        self,
        method: str,
        url: str,
        params: Dict = None,
        data: Any = None,
        json_data: Any = None,
        headers: Dict = None,
        stream: bool = False,
    ) -> requests.Response:
        """带重试机制的请求

        Args:
            method: HTTP方法 GET/POST/PUT/DELETE
            url: 完整URL
            params: URL查询参数
            data: 表单数据
            json_data: JSON数据
            headers: 额外的请求头
            stream: 是否流式响应

        Returns:
            requests.Response对象

        Raises:
            RequestException: 所有重试失败后抛出
        """
        last_exception = None
        current_delay = self.retry_delay

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f"请求 {method} {url} (尝试 {attempt}/{self.max_retries})")
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=headers,
                    timeout=self.timeout,
                    stream=stream,
                )

                # 处理速率限制
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(
                        f"触发速率限制(429)，等待 {retry_after} 秒后重试 "
                        f"(尝试 {attempt}/{self.max_retries})"
                    )
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        continue
                    else:
                        response.raise_for_status()

                # 处理5xx服务器错误（可重试）
                if 500 <= response.status_code < 600:
                    if attempt < self.max_retries:
                        logger.warning(
                            f"服务器错误 {response.status_code}，"
                            f"{current_delay:.1f}秒后重试 "
                            f"(尝试 {attempt}/{self.max_retries})"
                        )
                        time.sleep(current_delay)
                        current_delay *= self.retry_backoff
                        continue

                # 处理4xx客户端错误（除429外不重试）
                if 400 <= response.status_code < 500:
                    # 429已上面处理
                    response.raise_for_status()

                return response

            except (Timeout, ReqConnectionError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    logger.warning(
                        f"网络异常: {type(e).__name__}: {e}，"
                        f"{current_delay:.1f}秒后重试 "
                        f"(尝试 {attempt}/{self.max_retries})"
                    )
                    time.sleep(current_delay)
                    current_delay *= self.retry_backoff
                else:
                    logger.error(f"网络异常，已达最大重试次数: {e}")
                    raise
            except HTTPError as e:
                last_exception = e
                logger.error(f"HTTP错误: {e}")
                raise
            except RequestException as e:
                last_exception = e
                logger.error(f"请求异常: {e}")
                raise

        if last_exception:
            raise last_exception

    def get(
        self,
        endpoint: str,
        params: Dict = None,
        headers: Dict = None,
        raw_url: bool = False,
    ) -> Dict[str, Any]:
        """发送GET请求并返回JSON

        Args:
            endpoint: API端点路径，或完整URL（raw_url=True时）
            params: 查询参数
            headers: 额外请求头
            raw_url: True表示endpoint是完整URL

        Returns:
            JSON反序列化后的字典
        """
        url = endpoint if raw_url else self._build_url(endpoint)
        response = self._request_with_retry("GET", url, params=params, headers=headers)
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {url} - {e}")
            raise

    def get_raw(
        self,
        endpoint: str,
        params: Dict = None,
        headers: Dict = None,
        raw_url: bool = False,
    ) -> requests.Response:
        """发送GET请求并返回原始Response

        Args:
            endpoint: API端点路径，或完整URL（raw_url=True时）
            params: 查询参数
            headers: 额外请求头
            raw_url: True表示endpoint是完整URL

        Returns:
            requests.Response对象
        """
        url = endpoint if raw_url else self._build_url(endpoint)
        return self._request_with_retry("GET", url, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        json_data: Any = None,
        data: Any = None,
        params: Dict = None,
        headers: Dict = None,
    ) -> Dict[str, Any]:
        """发送POST请求并返回JSON

        Args:
            endpoint: API端点路径
            json_data: JSON请求体
            data: 表单数据
            params: 查询参数
            headers: 额外请求头

        Returns:
            JSON反序列化后的字典
        """
        url = self._build_url(endpoint)
        response = self._request_with_retry(
            "POST", url, params=params, data=data, json_data=json_data, headers=headers
        )
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {url} - {e}")
            raise

    def download(
        self,
        url: str,
        dest_path: Union[str, Path],
        chunk_size: int = 8192,
        show_progress: bool = True,
    ) -> Path:
        """下载文件到指定路径

        Args:
            url: 文件下载URL
            dest_path: 本地保存路径
            chunk_size: 流式下载块大小
            show_progress: 是否在日志中显示进度

        Returns:
            下载文件的Path对象

        Raises:
            RequestException: 下载失败
        """
        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"开始下载: {url}")
        response = self._request_with_retry("GET", url, stream=True)
        response.raise_for_status()

        # 获取文件总大小（如果服务器返回了Content-Length）
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded = 0

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if show_progress and total_size > 0:
                        percent = (downloaded / total_size) * 100
                        # 每下载10%输出一次日志
                        last_percent = ((downloaded - len(chunk)) / total_size) * 100
                        if int(percent / 10) > int(last_percent / 10):
                            logger.debug(
                                f"下载进度: {percent:.1f}% "
                                f"({downloaded // 1024}KB / {total_size // 1024}KB)"
                            )

        logger.info(f"下载完成: {dest_path.name} ({dest_path.stat().st_size} bytes)")
        return dest_path

    def close(self):
        """关闭客户端，释放连接"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ModrinthClient(APIClient):
    """Modrinth API客户端"""

    def __init__(self):
        super().__init__(
            base_url=config.APIConfig.MODRINTH_BASE,
            user_agent=config.APIConfig.MODRINTH_USER_AGENT,
            timeout=30,
            max_retries=3,
        )

    def search(
        self,
        query: str,
        mc_version: str = None,
        loader: str = None,
        limit: int = 10,
    ) -> Dict:
        """搜索模组

        Args:
            query: 搜索关键词
            mc_version: MC版本过滤
            loader: 加载器过滤
            limit: 返回结果数

        Returns:
            搜索结果字典
        """
        # 构建facets
        facets = [["project_type:mod"]]
        if mc_version:
            facets.append([f"versions:{mc_version}"])
        if loader:
            facets.append([f"categories:{loader}"])

        params = {
            "query": query,
            "facets": json.dumps(facets),
            "limit": limit,
        }
        return self.get("search", params=params)

    def get_project(self, slug: str) -> Dict:
        """获取模组项目信息

        Args:
            slug: 模组slug

        Returns:
            项目信息字典
        """
        return self.get(f"project/{slug}")

    def get_versions(
        self, slug: str, mc_version: str = None, loader: str = None
    ) -> List[Dict]:
        """获取模组版本列表

        Args:
            slug: 模组slug
            mc_version: MC版本过滤
            loader: 加载器过滤

        Returns:
            版本列表
        """
        params = {}
        if mc_version:
            params["game_versions"] = json.dumps([mc_version])
        if loader:
            params["loaders"] = json.dumps([loader])

        return self.get(f"project/{slug}/version", params=params)

    def get_categories(self) -> List[Dict]:
        """获取Modrinth所有可用的模组分类

        Returns:
            分类列表
        """
        try:
            result = self.get("tag/category")
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"获取分类失败: {e}")
            return []

    def get_search_categories(self) -> List[str]:
        """获取用于搜索的分类名称列表

        Returns:
            分类名称列表
        """
        categories = self.get_categories()
        return [cat.get("category", "") for cat in categories if cat.get("category")]


class CurseForgeClient(APIClient):
    """CurseForge API客户端"""

    def __init__(self, api_key: str = None):
        api_key = api_key or config.APIConfig.get_curseforge_api_key()
        if not api_key:
            logger.warning(
                "CurseForge API Key未配置，请设置环境变量 CURSEFORGE_API_KEY。"
                "CurseForge相关功能将不可用。"
            )

        super().__init__(
            base_url=config.APIConfig.CURSEFORGE_BASE,
            user_agent="MC-Skill-V1/1.0",
            api_key=api_key,
            api_key_header="x-api-key",
            timeout=30,
            max_retries=3,
        )

    def is_available(self) -> bool:
        """检查CurseForge API是否可用（即是否配置了API Key）"""
        return bool(config.APIConfig.has_curseforge_key())

    def search(
        self,
        query: str,
        mc_version: str = None,
        mod_loader_type: int = None,
        page_size: int = 20,
    ) -> Dict:
        """搜索模组

        Args:
            query: 搜索关键词
            mc_version: MC版本过滤
            mod_loader_type: 加载器类型 (1=Forge, 4=NeoForge, 4=Fabric, 5=Quilt)
            page_size: 返回数量

        Returns:
            搜索结果字典
        """
        if not self.is_available():
            return {"data": []}

        params = {
            "gameId": config.APIConfig.CURSEFORGE_GAME_ID,
            "searchFilter": query,
            "classId": config.APIConfig.CURSEFORGE_CLASS_MOD,
            "pageSize": page_size,
        }
        if mc_version:
            params["gameVersion"] = mc_version
        if mod_loader_type:
            params["modLoaderType"] = mod_loader_type

        return self.get("mods/search", params=params)

    def get_files(
        self, mod_id: int, mc_version: str = None, mod_loader_type: int = None
    ) -> Dict:
        """获取模组文件列表

        Args:
            mod_id: 模组ID
            mc_version: MC版本过滤
            mod_loader_type: 加载器类型

        Returns:
            文件列表字典
        """
        if not self.is_available():
            return {"data": []}

        params = {}
        if mc_version:
            params["gameVersion"] = mc_version
        if mod_loader_type:
            params["modLoaderType"] = mod_loader_type

        return self.get(f"mods/{mod_id}/files", params=params)


# === 全局单例 ===
_modrinth_client: Optional[ModrinthClient] = None
_curseforge_client: Optional[CurseForgeClient] = None


def get_modrinth_client() -> ModrinthClient:
    """获取Modrinth客户端单例"""
    global _modrinth_client
    if _modrinth_client is None:
        _modrinth_client = ModrinthClient()
    return _modrinth_client


def get_curseforge_client() -> CurseForgeClient:
    """获取CurseForge客户端单例"""
    global _curseforge_client
    if _curseforge_client is None:
        _curseforge_client = CurseForgeClient()
    return _curseforge_client


# === 加载器类型映射 ===
# 参考 CurseForge API 文档：
#   1=Forge, 2=Cauldron, 3=LiteLoader, 4=Fabric, 5=Quilt, 6=NeoForge
LOADER_TO_CURSEFORGE = {
    "forge": 1,
    "neoforge": 6,
    "fabric": 4,
    "quilt": 5,
}
