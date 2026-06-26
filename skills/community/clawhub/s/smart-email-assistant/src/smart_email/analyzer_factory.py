"""
Analyzer 工厂模块 - 根据配置创建对应的 Analyzer 实例
"""
from typing import Optional

from .ai_analyzer import AIAnalyzer
from .anthropic_analyzer import AnthropicAnalyzer
from .subagent_analyzer import SubagentAnalyzer


class BaseAnalyzer:
    """
    Analyzer 基类接口

    所有 Analyzer 必须实现以下接口：
    - analyze_email(email_data: Dict) -> Tuple[bool, str, str]
    - analyze_emails_batch(emails: List[Dict], callback=None) -> List[Dict]
    """

    def analyze_email(self, email_data):
        """分析单封邮件，Returns: (is_urgent: bool, reason: str, summary: str)"""
        raise NotImplementedError

    def analyze_emails_batch(self, emails, callback=None):
        """批量分析"""
        raise NotImplementedError


def create_analyzer(provider: str = "openai",
                    api_key: str = None,
                    base_url: str = None,
                    model: str = None,
                    max_concurrent: int = 5,
                    multimodal_analysis: bool = False,
                    retry_count: int = 3,
                    retry_base_delay: float = 1.0,
                    timeout: int = None) -> BaseAnalyzer:
    """
    根据配置创建对应的 Analyzer 实例

    Args:
        provider: 分析方式
            - "openai": 使用 OpenAI 兼容 API (AIAnalyzer)
            - "anthropic": 使用 Anthropic API (AnthropicAnalyzer)
            - "subagent": 使用 OpenClaw Subagent (SubagentAnalyzer)
        api_key: API Key（OpenAI 和 Anthropic 使用）
        base_url: API Base URL（OpenAI 和 Anthropic 使用）
        model: 模型名称
        max_concurrent: 最大并发数
        multimodal_analysis: 是否启用多模态分析
        retry_count: 重试次数
        retry_base_delay: 重试基础延迟
        timeout: Subagent 超时时间（秒），默认从 SMART_EMAIL_SUBAGENT_TIMEOUT 读取

    Returns:
        Analyzer 实例
    """
    provider = provider.lower().strip()

    if provider == "openai":
        if not api_key:
            raise ValueError("❌ 未配置 API Key，请检查环境变量")
        if not model:
            raise ValueError("❌ 未配置模型名称，请设置 SMART_EMAIL_OPENAI_MODEL")
        return AIAnalyzer(
            api_key=api_key,
            base_url=base_url or "",
            model=model,
            max_concurrent=max_concurrent,
            multimodal_analysis=multimodal_analysis,
            retry_count=retry_count,
            retry_base_delay=retry_base_delay
        )

    elif provider == "anthropic":
        if not api_key:
            raise ValueError("❌ 未配置 API Key，请检查环境变量")
        if not model:
            raise ValueError("❌ 未配置模型名称，请设置 SMART_EMAIL_ANTHROPIC_MODEL")
        return AnthropicAnalyzer(
            api_key=api_key,
            model=model,
            base_url=base_url or "",
            max_concurrent=max_concurrent,
            multimodal_analysis=multimodal_analysis,
            retry_count=retry_count,
            retry_base_delay=retry_base_delay
        )

    elif provider == "subagent":
        return SubagentAnalyzer(
            max_concurrent=max_concurrent,
            retry_count=retry_count,
            retry_base_delay=retry_base_delay,
            timeout=timeout
        )

    else:
        raise ValueError(f"Unknown analyzer provider: {provider}")


def create_analyzer_from_config(config) -> Optional[BaseAnalyzer]:
    """
    从 Config 对象创建 Analyzer 实例

    Args:
        config: Config 实例

    Returns:
        Analyzer 实例，如果未配置则返回 None
    """
    import os

    # 获取 LLM Provider
    provider = os.getenv("SMART_EMAIL_LLM_PROVIDER", "openai").lower().strip()

    # 获取并发配置
    max_concurrent_str = os.getenv("SMART_EMAIL_MAX_CONCURRENT")
    try:
        max_concurrent = int(max_concurrent_str) if max_concurrent_str else 5
    except ValueError:
        max_concurrent = 5

    # 获取多模态分析开关
    multimodal_env = os.getenv("SMART_EMAIL_MULTIMODAL_ANALYSIS")
    if multimodal_env is None:
        multimodal_analysis = config.get("ai.multimodal_analysis", False)
    else:
        multimodal_analysis = multimodal_env.lower() in ('true', '1', 'yes', 'on')

    # 获取重试配置
    retry_count_str = os.getenv("SMART_EMAIL_LLM_RETRY_COUNT")
    try:
        retry_count = int(retry_count_str) if retry_count_str else 3
    except ValueError:
        retry_count = 3

    retry_base_delay_str = os.getenv("SMART_EMAIL_LLM_RETRY_BASE_DELAY")
    try:
        retry_base_delay = float(retry_base_delay_str) if retry_base_delay_str else 1.0
    except ValueError:
        retry_base_delay = 1.0

    if provider == "openai":
        # OpenAI 配置
        openai_api_key = os.getenv("SMART_EMAIL_OPENAI_API_KEY")

        if not openai_api_key:
            print("⚠️ 未配置 SMART_EMAIL_OPENAI_API_KEY，使用 OpenAI provider 需要配置此环境变量")
            return None

        openai_base_url = os.getenv("SMART_EMAIL_OPENAI_API_URL", "")
        openai_model = os.getenv("SMART_EMAIL_OPENAI_MODEL")

        return create_analyzer(
            provider="openai",
            api_key=openai_api_key,
            base_url=openai_base_url or "",
            model=openai_model,
            max_concurrent=max_concurrent,
            multimodal_analysis=multimodal_analysis,
            retry_count=retry_count,
            retry_base_delay=retry_base_delay
        )

    elif provider == "anthropic":
        # Anthropic 配置
        api_key = os.getenv("SMART_EMAIL_ANTHROPIC_API_KEY")

        if not api_key:
            print("⚠️ 未配置 SMART_EMAIL_ANTHROPIC_API_KEY，使用 Anthropic provider 需要配置此环境变量")
            return None

        base_url = os.getenv("SMART_EMAIL_ANTHROPIC_API_URL", "")
        model = os.getenv("SMART_EMAIL_ANTHROPIC_MODEL")

        # 获取 Anthropic 专用并发配置
        subagent_concurrency_str = os.getenv("SMART_EMAIL_SUBAGENT_CONCURRENCY")
        if subagent_concurrency_str:
            try:
                max_concurrent = int(subagent_concurrency_str)
            except ValueError:
                pass

        return create_analyzer(
            provider="anthropic",
            api_key=api_key,
            base_url=base_url,
            model=model,
            max_concurrent=max_concurrent,
            multimodal_analysis=multimodal_analysis,
            retry_count=retry_count,
            retry_base_delay=retry_base_delay
        )

    elif provider == "subagent":
        # Subagent 配置
        concurrency_str = os.getenv("SMART_EMAIL_SUBAGENT_CONCURRENCY")
        if concurrency_str:
            try:
                max_concurrent = int(concurrency_str)
            except ValueError:
                pass

        # 读取 Subagent 超时配置
        timeout_str = os.getenv("SMART_EMAIL_SUBAGENT_TIMEOUT")
        timeout = None
        if timeout_str:
            try:
                timeout = int(timeout_str)
            except ValueError:
                pass

        return create_analyzer(
            provider="subagent",
            max_concurrent=max_concurrent,
            retry_count=retry_count,
            retry_base_delay=retry_base_delay,
            timeout=timeout
        )

    else:
        print(f"⚠️ 未知的 LLM Provider: {provider}，使用默认 OpenAI")
        return None
