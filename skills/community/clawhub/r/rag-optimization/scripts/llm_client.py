#!/usr/bin/env python3
"""
统一 LLM 客户端抽象层
=======================
封装所有 LLM 交互模式，解决各脚本中重复的脆弱数字解析、异常处理、
重试和缓存问题。

使用方式：
    # 方式 1：直接构造 OpenAI 兼容客户端
    from llm_client import LLMClient, OpenAILikeClient, EmbeddingClient

    llm = OpenAILikeClient(
        api_key="your-key",
        api_url="https://integrate.api.nvidia.com/v1/chat/completions",
        model="nvidia/nemotron-3-super-120b-a12b"
    )
    score = llm.score("请评估以下文本与问题的相关性（0-1分）：...")
    text  = llm.generate("请回答：...")
    data  = llm.extract_json("输出 JSON 格式：...")
    label = llm.classify("分类以下文本", options=["A", "B", "C"])

    # 方式 2：从 .env 自动加载 NVIDIA 配置（零配置）
    from llm_client import load_from_env
    llm = load_from_env()

    # 方式 3：作为基类，让各脚本的 llm_client 注入统一接口
    class MockLLM(LLMClient):
        def generate(self, prompt, **kwargs): return "mock answer"
        def score(self, prompt): return 0.75
        def classify(self, prompt, options): return options[0]
        def extract_json(self, prompt): return {}

降级行为：未配置 API 凭证时，所有方法返回安全默认值，不抛异常。
"""
import json
import os
import logging
import re
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 可选 .env 加载（H4：让 load_from_env() 名副其实）
# ============================================================
def load_dotenv_if_available() -> bool:
    """
    尝试加载 .env 文件；python-dotenv 未安装时静默跳过。

    全局唯一的 dotenv 入口——其它模块应调用本函数，不要各自 try/import，
    否则会出现"有的入口加载了、有的没加载"的不一致。

    注意：load_dotenv() 默认不覆盖已存在的环境变量，
    因此真实环境注入的凭证优先级高于 .env（符合直觉）。

    Returns:
        是否成功加载了 .env
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except ImportError:
        logger.debug("python-dotenv 未安装，跳过 .env 加载（依赖真实环境变量）")
        return False


# 模块导入即生效，使 `from llm_client import load_from_env` 这条
# SKILL.md 承诺的零配置路径真正能读到 .env
DOTENV_LOADED = load_dotenv_if_available()


# ============================================================
# 核心基类
# ============================================================

class LLMClient:
    """
    统一 LLM 客户端基类。

    所有 LLM 交互统一通过以下 4 个方法，内部封装：
    - 安全的数字解析（解决各脚本中重复的脆弱拼接）
    - 安全的 JSON 解析（处理 LLM 返回的多余文本）
    - 3 次自动重试 + 指数退避
    - LRU 缓存（可配置开关）
    - 无 LLM 时的安全降级
    """

    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1.0
    DEFAULT_CACHE_SIZE = 128

    def __init__(self,
                 cache_enabled: bool = True,
                 cache_size: int = DEFAULT_CACHE_SIZE,
                 max_retries: int = DEFAULT_MAX_RETRIES,
                 retry_delay: float = DEFAULT_RETRY_DELAY,
                 llm_client=None):
        """
        Args:
            cache_enabled: 是否启用 LRU 缓存
            cache_size: 缓存条目上限
            max_retries: 最大重试次数
            retry_delay: 首次重试延迟（秒，指数退避）
            llm_client: 底层 LLM 客户端（可选；未传时全部降级返回默认值）
        """
        self._llm = llm_client
        self._cache_enabled = cache_enabled
        self._cache_size = cache_size
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._cache: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # 4 个核心方法
    # ------------------------------------------------------------------

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        通用文本生成，返回纯文本。

        Args:
            prompt: 用户提示
            system_prompt: 系统提示（可选）
            **kwargs: 透传给底层 LLM 的参数（temperature, max_tokens 等）

        Returns:
            LLM 输出的纯文本；无 LLM 时返回 "LLM 未配置"
        """
        if not self._llm:
            return "LLM 未配置"

        cache_key = self._cache_key("generate", prompt, system_prompt)
        if self._cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]

        def _call():
            if hasattr(self._llm, 'invoke'):
                if system_prompt:
                    full_prompt = f"System: {system_prompt}\n\n{prompt}"
                else:
                    full_prompt = prompt
                response = self._llm.invoke(full_prompt, **kwargs)
            else:
                response = self._llm(prompt, **kwargs)
            return response.strip() if isinstance(response, str) else str(response)

        result = self._retry_with_backoff(_call, fallback="LLM 调用失败")
        if self._cache_enabled:
            self._put_cache(cache_key, result)
        return result

    def score(self, prompt: str, default: float = 0.5) -> float:
        """
        返回 0-1 评分，内部处理安全的数字解析。

        解决 Bug 2：旧的 `float(''.join(...))` 拼接模式在 LLM 返回
        多数字时抛 ValueError 或静默污染。此方法改用正则提取第一个
        合法小数，并支持百分比格式（如 "75%" → 0.75）。

        Args:
            prompt: 包含评分要求的 prompt
            default: 无 LLM 或解析失败时的默认值

        Returns:
            0-1 范围的浮点数
        """
        if not self._llm:
            return default

        cache_key = self._cache_key("score", prompt)
        if self._cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]

        def _call():
            if hasattr(self._llm, 'invoke'):
                response = self._llm.invoke(prompt)
            else:
                response = self._llm(prompt)
            return self._parse_score(response)

        result = self._retry_with_backoff(_call, fallback=default)
        if self._cache_enabled:
            self._put_cache(cache_key, result)
        return result

    def classify(self, prompt: str, options: List[str]) -> str:
        """
        多分类选择，返回匹配的选项字符串。

        Args:
            prompt: 包含分类要求的 prompt
            options: 候选标签列表

        Returns:
            匹配的选项字符串；无 LLM 时返回 "unknown"
        """
        if not self._llm:
            return "unknown"

        cache_key = self._cache_key("classify", prompt, str(options))
        if self._cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]

        # 追加选项到 prompt（如果 prompt 未包含）
        options_text = "\n".join(f"- {opt}" for opt in options)
        full_prompt = prompt
        if options_text not in prompt:
            full_prompt = f"{prompt}\n\n可选分类：\n{options_text}\n\n只返回分类标签本身，不要其他内容。"

        def _call():
            if hasattr(self._llm, 'invoke'):
                response = self._llm.invoke(full_prompt)
            else:
                response = self._llm(full_prompt)
            text = response.strip() if isinstance(response, str) else str(response)
            for opt in options:
                if opt.lower() in text.lower():
                    return opt
            return "unknown"

        result = self._retry_with_backoff(_call, fallback="unknown")
        if self._cache_enabled:
            self._put_cache(cache_key, result)
        return result

    def extract_json(self, prompt: str) -> Dict:
        """
        期望 JSON 输出，内部处理 LLM 返回的多余文本。

        从 LLM 输出中提取第一个合法 JSON 对象。

        Args:
            prompt: 包含 JSON 输出要求的 prompt

        Returns:
            解析后的字典；无 LLM 或解析失败时返回空字典
        """
        if not self._llm:
            return {}

        cache_key = self._cache_key("extract_json", prompt)
        if self._cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]

        def _call():
            if hasattr(self._llm, 'invoke'):
                response = self._llm.invoke(prompt)
            else:
                response = self._llm(prompt)
            return self._parse_json(response)

        result = self._retry_with_backoff(_call, fallback={})
        if self._cache_enabled:
            self._put_cache(cache_key, result)
        return result

    # ------------------------------------------------------------------
    # 内部工具方法
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_score(text: Any) -> float:
        """
        安全解析 LLM 返回的评分文本。R1 加固版。

        处理场景（按优先级）：
        1. "3/10" 或 "3 / 10" → 0.3（显式分母格式）
        2. "3 out of 10" 或 "3 out of 5" → 0.6
        3. "75%" → 0.75
        4. dict 响应 → 提取数值字段
        5. "0.75" / "75"（无上下文）→ 推测为评分
        6. 无法解析 → 抛 ValueError
        """
        if isinstance(text, (int, float)):
            return max(0.0, min(1.0, float(text)))
        if not isinstance(text, str):
            text = str(text)

        text_stripped = text.strip().lower()

        # R1-1: 显式分母 "X/10", "3/5", "8 out of 10"
        slash_match = re.search(r'(\d+\.?\d*)\s*/\s*(\d+\.?\d*)', text)
        if slash_match:
            numerator = float(slash_match.group(1))
            denominator = float(slash_match.group(2))
            if denominator > 0:
                return max(0.0, min(1.0, numerator / denominator))

        out_of_match = re.search(r'(\d+\.?\d*)\s*out\s*of\s*(\d+\.?\d*)', text_stripped)
        if out_of_match:
            numerator = float(out_of_match.group(1))
            denominator = float(out_of_match.group(2))
            if denominator > 0:
                return max(0.0, min(1.0, numerator / denominator))

        # R1-2: 百分比
        pct_match = re.search(r'(\d+\.?\d*)%', text)
        if pct_match:
            return max(0.0, min(1.0, float(pct_match.group(1)) / 100.0))

        # R1-3: 从 JSON 中提取 rating/score/value 字段
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            import json
            try:
                data = json.loads(json_match.group())
                for key in ('score', 'rating', 'value', 'relevance', 'confidence'):
                    if key in data and isinstance(data[key], (int, float)):
                        raw = float(data[key])
                        if raw > 1.0 and raw <= 100.0:
                            raw = raw / 100.0
                        return max(0.0, min(1.0, raw))
            except (json.JSONDecodeError, TypeError):
                pass

        # R1-4: 第一个合法数字
        num_match = re.search(r'(\d+\.?\d*)', text)
        if num_match:
            raw = float(num_match.group(1))
            # 如果 > 1 且 <= 100，推测为百分比
            if raw > 1.0 and raw <= 100.0:
                raw = raw / 100.0
            # 如果 > 100，很可能是错误输出（如 "9999"），返回 0
            if raw > 1.0:
                return 0.0
            return max(0.0, min(1.0, raw))

        raise ValueError(f"无法从文本中解析出数字: {text[:100]}")

    @staticmethod
    def _parse_json(text: Any) -> Dict:
        """
        从 LLM 输出中提取第一个合法 JSON 对象。

        处理场景：
        - 纯 JSON → 直接解析
        - 带说明文字 + JSON → 提取第一个 {...} 块
        - 多段 JSON → 取第一段
        - 无法解析 → 抛 ValueError 触发重试
        """
        if isinstance(text, dict):
            return text
        if not isinstance(text, str):
            text = str(text)

        # 尝试直接解析
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass

        # 提取 { ... } 块
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except (json.JSONDecodeError, ValueError):
                pass

        raise ValueError(f"无法从文本中解析出 JSON: {text[:100]}")

    def _retry_with_backoff(self, fn, fallback=None, max_retries=None) -> Any:
        """带指数退避的重试包装器。"""
        retries = max_retries if max_retries is not None else self._max_retries
        for attempt in range(retries + 1):
            try:
                return fn()
            except Exception as e:
                if attempt < retries:
                    delay = self._retry_delay * (2 ** attempt)
                    logger.warning(f"LLM 调用失败（第 {attempt+1}/{retries} 次重试），{delay:.1f}s 后重试: {e}")
                    time.sleep(delay)
                else:
                    logger.error(f"LLM 调用耗尽重试次数，返回降级值: {e}")
        return fallback

    @staticmethod
    def _cache_key(method: str, *args) -> str:
        """生成缓存键。"""
        return f"{method}:{hash(' '.join(str(a) for a in args))}"

    def _put_cache(self, key: str, value: Any) -> None:
        """写入 LRU 缓存（简单实现，超容时清理最老条目）。"""
        if len(self._cache) >= self._cache_size:
            # 简单 LRU：删除最早的条目
            oldest_key = next(iter(self._cache), None)
            if oldest_key:
                del self._cache[oldest_key]
        self._cache[key] = value


# ============================================================
# 实现：OpenAI 兼容 API 客户端
# ============================================================

class OpenAILikeClient(LLMClient):
    """
    兼容 OpenAI 协议的 LLM 客户端。

    支持豆包、NVIDIA、OpenAI 等所有使用 chat/completions 端点的服务商。

    使用环境变量注入（通过 .env 加载）：
        OPENAI_API_KEY / DOUBAO_API_KEY / NVIDIA_API_KEY
        OPENAI_API_URL / DOUBAO_API_URL / NVIDIA_API_URL
        OPENAI_MODEL / DOUBAO_MODEL
    """

    # R2: 熔断器默认值 —— SKILL.md「架构约束」承诺：连续 5 次失败后熔断，冷却 30 秒
    CIRCUIT_FAILURE_THRESHOLD = 5
    CIRCUIT_COOLDOWN_SECONDS = 30

    def __init__(self,
                 api_key: str = None,
                 api_url: str = None,
                 model: str = None,
                 max_retries: int = None,
                 retry_delay: float = None,
                 cache_enabled: bool = True,
                 circuit_failure_threshold: int = None,
                 circuit_cooldown_seconds: float = None):
        import os

        # ---- R2 熔断器状态初始化（H1）----
        # 必须在任何 generate() 调用之前完成；这些属性被 generate() 读取，
        # 缺失会导致 AttributeError 且在 try 块之外无法兜底。
        self._circuit_state = "closed"
        self._consecutive_failures = 0
        self._circuit_failure_threshold = (
            circuit_failure_threshold
            if circuit_failure_threshold is not None
            else self.CIRCUIT_FAILURE_THRESHOLD
        )
        self._circuit_cooldown_seconds = (
            circuit_cooldown_seconds
            if circuit_cooldown_seconds is not None
            else self.CIRCUIT_COOLDOWN_SECONDS
        )
        self._circuit_last_failure_time = 0.0

        # 环境变量覆盖（优先级：构造参数 > 环境变量）
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("DOUBAO_API_KEY") or os.getenv("NVIDIA_API_KEY")
        self.api_url = api_url or os.getenv("OPENAI_API_URL") or os.getenv("DOUBAO_API_URL") or os.getenv("NVIDIA_API_URL")
        self.model = model or os.getenv("OPENAI_MODEL") or os.getenv("DOUBAO_MODEL")

        if not self.api_key:
            logger.warning("OpenAILikeClient 未配置 API Key，将降级为 MockLLM")
            super().__init__(llm_client=None, cache_enabled=cache_enabled)
            return

        if not self.api_url:
            logger.warning("未配置 API URL，使用豆包默认端点")
            self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

        # 自动补全：如果 URL 不包含 /chat/completions，追加之
        if '/chat/completions' not in self.api_url:
            self.api_url = self.api_url.rstrip('/') + '/chat/completions'

        # 尝试使用平台 SDK 的 requests（与 evaluate.py 保持一致）
        self._requests = None
        try:
            from coze_workload_identity import requests
            self._requests = requests
        except ImportError:
            try:
                import requests
                self._requests = requests
            except ImportError:
                logger.warning("requests 库未安装，LLM 调用将失败")

        # H24：max_retries 此前收下后从未传给基类——self._max_retries 恒为
        # 基类默认值 3，构造参数是死的。retry_delay 同理（连参数位都没有）。
        # 现在两者都真正透传；None 时用基类默认，保持向后兼容。
        super().__init__(llm_client=self,
                         cache_enabled=cache_enabled,
                         max_retries=max_retries if max_retries is not None else self.DEFAULT_MAX_RETRIES,
                         retry_delay=retry_delay if retry_delay is not None else self.DEFAULT_RETRY_DELAY)

    def __call__(self, prompt: str, **kwargs) -> str:
        """可调用接口：兼容旧代码的 llm(prompt) 调用方式。"""
        return self.generate(prompt, **kwargs)

    def invoke(self, prompt: str, **kwargs) -> str:
        """兼容 LangChain 风格的 invoke 调用。"""
        return self.generate(prompt, **kwargs)

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        调用 OpenAI 兼容 API 生成文本。

        Override 基类方法，绕过自身的 cache/retry 包装（因为 __call__/invoke
        已在此层做处理），直接走 HTTP 调用。
        """
        if not self._requests or not self.api_key:
            return "LLM 未配置"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.pop("max_tokens", 1024),
            "temperature": kwargs.pop("temperature", 0.0),
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for attempt in range(self._max_retries + 1):
            try:
                # R2: 熔断器检查（放在 try 内，状态异常也能被下面的 except 兜底，
                # 不会像之前那样在 try 之外直接外泄 AttributeError）
                if self._circuit_state == "open":
                    if time.time() - self._circuit_last_failure_time >= self._circuit_cooldown_seconds:
                        logger.info("熔断器进入 half-open 状态，尝试恢复")
                        self._circuit_state = "half_open"
                    else:
                        logger.warning(f"熔断器 open，跳过调用（冷却剩余 {self._circuit_cooldown_seconds - (time.time() - self._circuit_last_failure_time):.0f}s）")
                        return "LLM 调用失败：熔断器 open"

                response = self._requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                if response.status_code >= 400:
                    raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")

                result = response.json()
                if "error" in result:
                    raise Exception(f"API error: {result['error']}")

                content = result['choices'][0]['message']['content']
                # R2: 成功调用，重置熔断器
                self._consecutive_failures = 0
                if self._circuit_state == "half_open":
                    self._circuit_state = "closed"
                    logger.info("熔断器恢复 closed 状态")
                return content.strip()
            except Exception as e:
                if attempt < self._max_retries:
                    delay = self._retry_delay * (2 ** attempt)
                    logger.warning(f"HTTP 调用失败（第 {attempt+1}/{self._max_retries} 次重试），{delay:.1f}s 后重试: {e}")
                    time.sleep(delay)
                else:
                    logger.error(f"HTTP 调用耗尽重试次数: {e}")
                # R2: 失败计数
                self._consecutive_failures += 1
                self._circuit_last_failure_time = time.time()
                if self._consecutive_failures >= self._circuit_failure_threshold:
                    logger.warning(f"熔断器触发 open 状态（连续失败 {self._consecutive_failures} 次）")
                    self._circuit_state = "open"
        return "LLM 调用失败"


# ============================================================
# 向量嵌入：维度单一来源 + 降级结果协议
# ============================================================

# H14: 维度映射收进单一来源，EmbeddingClient 与 NvidiaEmbeddingClient 共用，
# 避免两处 magic number 各写一套导致向量无法互相比较。
EMBEDDING_DIMS: Dict[str, int] = {
    "nvidia/nemotron-3-embed-1b": 2048,
    "nvidia/nv-embed-v1": 4096,
    "snowflake/arctic-embed-l": 1024,
    # sentence-transformers 常用模型
    "all-MiniLM-L6-v2": 384,
    "BAAI/bge-m3": 1024,
}
DEFAULT_EMBEDDING_DIM = 2048


def resolve_embedding_dim(model_name: str) -> int:
    """按模型名解析向量维度（全项目唯一入口）。未知模型回退到默认值。"""
    return EMBEDDING_DIMS.get(model_name, DEFAULT_EMBEDDING_DIM)


@dataclass
class EmbeddingResult:
    """
    encode() 的返回协议（H9）。

    降级为哈希向量时必须可被识别——否则调用方拿到一份"看起来正常"的向量，
    语义检索静默失效却无任何迹象。

    为保持向后兼容，本对象支持像 List[List[float]] 一样被
    len() / 索引 / 迭代（`encode([q])[0]` 这种既有写法继续可用）。
    """
    vectors: List[List[float]]
    is_degraded: bool = False
    degraded_indices: List[int] = field(default_factory=list)
    reason: str = ""

    def __len__(self) -> int:
        return len(self.vectors)

    def __iter__(self):
        return iter(self.vectors)

    def __getitem__(self, index):
        return self.vectors[index]

    @property
    def list(self) -> List[List[float]]:
        """显式取回裸向量列表。"""
        return self.vectors


class EmbeddingClient:
    """
    向量嵌入客户端。

    支持：
    - sentence-transformers 模型（需安装）
    - 零依赖的哈希向量（降级方案）
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._mode = "hash"  # hash / sentence-transformers

        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(model_name)
            self._mode = "sentence-transformers"
            logger.info(f"使用 SentenceTransformer 嵌入模型: {model_name}")
        except ImportError:
            logger.info("sentence-transformers 未安装，使用哈希向量降级方案")

    def encode(self, texts: List[str]) -> EmbeddingResult:
        """
        将文本列表编码为向量列表。

        Args:
            texts: 文本列表

        Returns:
            EmbeddingResult（可当作 List[List[float]] 直接使用）。
            降级为哈希向量时 is_degraded=True 并附带 reason。
        """
        dim = resolve_embedding_dim(self.model_name)

        if self._mode == "sentence-transformers":
            return EmbeddingResult(
                vectors=self._model.encode(texts).tolist(),
                is_degraded=False,
            )

        # R4: 哈希向量降级方案（有明确警告 + 可识别标记）
        logger.warning(
            f"EmbeddingClient 使用哈希向量降级（is_degraded=True）："
            f"语义检索将完全失效，结果不可靠。model={self.model_name}"
        )
        return EmbeddingResult(
            vectors=[self._hash_vector(t, dim) for t in texts],
            is_degraded=True,
            degraded_indices=list(range(len(texts))),
            reason="sentence-transformers 未安装，已降级为哈希向量",
        )

    @staticmethod
    def _hash_vector(text: str, dim: int = DEFAULT_EMBEDDING_DIM) -> List[float]:
        """
        将文本转换为伪向量（基于字符哈希）。
        仅用于无 embedding 模型时的降级方案，效果远不及真实向量模型。
        """
        import hashlib
        vector = [0.0] * dim
        for i, ch in enumerate(text):
            h = int(hashlib.md5(f"{ch}{i}".encode()).hexdigest(), 16)
            idx = h % dim
            vector[idx] += 0.1
        norm = sum(v * v for v in vector) ** 0.5
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector


# ============================================================
# NVIDIA 向量嵌入客户端
# ============================================================

class NvidiaEmbeddingClient:
    """
    通过 NVIDIA API 调用向量嵌入模型。

    支持模型（截至 2026-07）：
        - nvidia/nemotron-3-embed-1b（推荐，2048 维，快速）
        - nvidia/nv-embed-v1（4096 维）
        - snowflake/arctic-embed-l

    零依赖：不安装任何模型文件，纯 HTTP 调用。
    """

    def __init__(self, model_name: str = "nvidia/nemotron-3-embed-1b",
                 api_key: str = None,
                 api_url: str = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY") or os.getenv("NVIDIA_API_KEY")
        self.api_url = (api_url or os.getenv("NVIDIA_API_URL")
                        or "https://integrate.api.nvidia.com/v1/embeddings")

        if not self.api_key:
            logger.warning("NvidiaEmbeddingClient 未配置 API Key，将无法编码")
            self._ready = False
        else:
            self._ready = True
            logger.info(f"使用 NVIDIA 嵌入模型: {model_name}")

    def encode(self, texts: List[str]) -> EmbeddingResult:
        """
        将文本列表编码为向量列表。

        Args:
            texts: 文本列表

        Returns:
            EmbeddingResult（可当作 List[List[float]] 直接使用）。
            整体或部分降级为哈希向量时，is_degraded / degraded_indices 会标明。
        """
        dim = self._detect_dim()

        if not self._ready:
            # R4: 整体降级必须可被识别（H9）
            logger.warning(
                "NvidiaEmbeddingClient 降级为哈希向量（is_degraded=True）："
                "未配置 API Key，语义检索将完全失效，结果不可靠"
            )
            return EmbeddingResult(
                vectors=[self._hash_vector(t, dim) for t in texts],
                is_degraded=True,
                degraded_indices=list(range(len(texts))),
                reason="未配置 API Key，已整体降级为哈希向量",
            )

        # 批量编码（NVIDIA API 支持一次最多 100 条）
        vectors: List[List[float]] = []
        degraded: List[int] = []
        batch_size = 20  # 保守批次大小
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_vectors, batch_degraded = self._encode_batch(batch)
            vectors.extend(batch_vectors)
            # 批次内相对下标 → 全局下标
            degraded.extend(i + idx for idx in batch_degraded)

        if degraded:
            # 部分降级更危险：同一批结果里真向量与哈希向量混在一起，
            # 余弦相似度不可比，必须显式告警。
            logger.warning(
                f"NvidiaEmbeddingClient 部分降级（is_degraded=True）："
                f"{len(degraded)}/{len(texts)} 条编码失败并替换为哈希向量，"
                f"下标={degraded[:10]}{'...' if len(degraded) > 10 else ''}；"
                f"这些向量与真实向量不处于同一语义空间，检索结果不可靠"
            )

        return EmbeddingResult(
            vectors=vectors,
            is_degraded=bool(degraded),
            degraded_indices=degraded,
            reason=(f"{len(degraded)}/{len(texts)} 条编码失败并降级为哈希向量"
                    if degraded else ""),
        )

    def _encode_batch(self, texts: List[str]):
        """
        编码一批文本。

        Returns:
            (vectors, degraded_indices) —— degraded_indices 为本批次内的相对下标
        """
        dim = self._detect_dim()

        vectors = []
        degraded = []
        for idx, text in enumerate(texts):
            try:
                payload = {
                    "model": self.model_name,
                    "input": [text],
                    "encoding_format": "float",
                }
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                import urllib.request
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    self.api_url,
                    data=data,
                    headers=headers,
                    method='POST',
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    result = json.loads(resp.read().decode())
                    embedding = result['data'][0]['embedding']
                    vectors.append(embedding)
            except Exception as e:
                logger.warning(
                    f"向量编码失败，降级为哈希（is_degraded=True，批次内第 {idx} 条）: {e}"
                )
                vectors.append(self._hash_vector(text, dim))
                degraded.append(idx)

        return vectors, degraded

    def _detect_dim(self) -> int:
        """
        根据模型名称推断向量维度。

        H14: 统一走 resolve_embedding_dim()，与 EmbeddingClient 共用同一份映射，
        不再在本方法里维护一份副本。
        """
        return resolve_embedding_dim(self.model_name)

    @staticmethod
    def _hash_vector(text: str, dim: int) -> List[float]:
        """降级哈希向量"""
        import hashlib
        vector = [0.0] * dim
        for i, ch in enumerate(text):
            h = int(hashlib.md5(f"{ch}{i}".encode()).hexdigest(), 16)
            idx = h % dim
            vector[idx] += 0.1
        norm = sum(v * v for v in vector) ** 0.5
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector


# ============================================================
# LLM 包装器（H23：统一入口，防止重试放大）
# ============================================================
def wrap_llm(llm_client, **kwargs) -> Optional[LLMClient]:
    """
    把外部传入的 LLM 对象统一成 LLMClient 接口。

    关键（H23）：若传入对象**已经是 LLMClient 实例**（OpenAILikeClient 也是其子类），
    直接返回、不再套一层。否则会造成重试放大：

        外层 LLMClient._retry_with_backoff 重试 3 次
          × 内层 OpenAILikeClient.generate 重试 3 次 = 最多 9 次调用、
            退避 sleep 累计可达 21 秒

    各脚本的 `self.llm_client = LLMClient(llm_client=llm_client)` 一律改为调用本函数。

    Args:
        llm_client: LLMClient 实例 / 有 invoke() 的对象 / 可调用对象
        **kwargs: 透传给 LLMClient 构造（cache_enabled、max_retries 等）

    Returns:
        LLMClient；入参为 None 时返回 None
    """
    if llm_client is None:
        return None
    if isinstance(llm_client, LLMClient):
        return llm_client
    return LLMClient(llm_client=llm_client, **kwargs)


# ============================================================
# 零配置加载器
# ============================================================
def load_from_env(api_url_env: str = "DOUBAO_API_URL",
                  api_key_env: str = "DOUBAO_API_KEY",
                  model_env: str = "DOUBAO_MODEL",
                  fallback_url: str = "https://integrate.api.nvidia.com/v1/chat/completions",
                  fallback_model: str = "nvidia/nemotron-3-super-120b-a12b") -> Optional[OpenAILikeClient]:
    """
    从环境变量自动加载 LLM 配置，返回 OpenAILikeClient 实例。

    搜索顺序：
        1. DOUBAO_API_URL / DOUBAO_API_KEY / DOUBAO_MODEL（环境变量）
        2. NVIDIA_API_URL / NVIDIA_API_KEY（.env 桥接）
        3. 内置 NVIDIA 默认值（零配置）

    所有凭证缺失时返回 None（降级模式）。
    """
    api_url = os.getenv(api_url_env)
    api_key = os.getenv(api_key_env)
    model = os.getenv(model_env)

    # 尝试 NVIDIA_API_URL / NVIDIA_API_KEY（.env 桥接）
    if not api_url:
        api_url = os.getenv("NVIDIA_API_URL", fallback_url)
    if not api_key:
        api_key = os.getenv("NVIDIA_API_KEY")
    if not model:
        model = fallback_model

    # 自动补全 URL：如果未包含 /chat/completions，追加之
    if api_url and '/chat/completions' not in api_url:
        api_url = api_url.rstrip('/') + '/chat/completions'

    # 无 API key 时返回 None（降级）
    if not api_key:
        logger.info("未找到 API 凭证，LLMClient 将使用降级模式")
        return None

    logger.info(f"加载 LLM 配置: {model} @ {api_url}")
    return OpenAILikeClient(
        api_key=api_key,
        api_url=api_url,
        model=model,
    )


# ============================================================
# 向量嵌入零配置加载器
# ============================================================
def load_embedding_from_env(
    api_key_env: str = "DOUBAO_API_KEY",
    model_env: str = "EMBEDDING_MODEL",
    fallback_model: str = "nvidia/nemotron-3-embed-1b",
) -> Optional[NvidiaEmbeddingClient]:
    """
    从环境变量自动加载嵌入模型配置。

    搜索顺序：
        1. EMBEDDING_MODEL / DOUBAO_API_KEY（环境变量）
        2. NVIDIA_API_KEY（.env 桥接）

    返回 NvidiaEmbeddingClient 实例；无凭证时返回 None。
    """
    api_key = os.getenv(api_key_env)
    model = os.getenv(model_env)

    if not api_key:
        api_key = os.getenv("NVIDIA_API_KEY")
    if not model:
        model = fallback_model

    if not api_key:
        logger.info("未找到 API 凭证，嵌入模型将使用降级模式")
        return None

    return NvidiaEmbeddingClient(
        model_name=model,
        api_key=api_key,
    )
