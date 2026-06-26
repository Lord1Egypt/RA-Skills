"""
AI 去痕模块

去除 AI 写作痕迹，使文章更加自然人性化。

支持的 Provider:
- openai: OpenAI GPT 系列
- qwen: 通义千问 (阿里云 DashScope)
- doubao: 豆包 (字节跳动火山引擎)
- minimax: MiniMax
- moonshot: Moonshot (月之暗面)
- zhipu: 智谱 GLM
- hunyuan: 腾讯混元
- yi: 零一万物 Yi 系列
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import httpx


class Intensity(str, Enum):
    """处理强度"""

    LIGHT = "light"  # 轻度：保留大部分原文
    MEDIUM = "medium"  # 中度：适度调整
    HEAVY = "heavy"  # 重度：大幅改写


class Provider(str, Enum):
    """支持的 AI 提供商"""

    OPENAI = "openai"
    QWEN = "qwen"
    DOUBAO = "doubao"
    MINIMAX = "minimax"
    MOONSHOT = "moonshot"
    ZHIPU = "zhipu"
    HUNYUAN = "hunyuan"
    YI = "yi"
    CUSTOM = "custom"  # 自定义 provider


# Provider 配置映射
PROVIDER_CONFIG = {
    Provider.OPENAI: {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4",
    },
    Provider.QWEN: {
        "name": "通义千问",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
    },
    Provider.DOUBAO: {
        "name": "豆包",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "default_model": "doubao-pro-32k",
    },
    Provider.MINIMAX: {
        "name": "MiniMax",
        "base_url": "https://api.minimax.chat/v1",
        "default_model": "MiniMax-Text-01",
    },
    Provider.MOONSHOT: {
        "name": "Moonshot",
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
    },
    Provider.ZHIPU: {
        "name": "智谱 GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4-flash",
    },
    Provider.HUNYUAN: {
        "name": "腾讯混元",
        "base_url": "https://hunyuan.cloud.tencent.com/hunyuan-vision-api",
        "default_model": "hunyuan",
    },
    Provider.YI: {
        "name": "零一万物 Yi",
        "base_url": "https://api.lingyiwanwu.com/v1",
        "default_model": "yi-medium",
    },
}


@dataclass
class HumanizeResult:
    """去痕结果"""

    original: str
    humanized: str
    changes: list[str]


class Humanizer:
    """AI 去痕处理器"""

    SYSTEM_PROMPT = """你是一个专业的文本人性化专家。你的任务是重写 AI 生成的内容，使其更加自然、人性化。

AI 写作的常见特征包括：
1. 过于规整的句式结构
2. 频繁使用"首先"、"其次"、"最后"等过渡词
3. 缺乏个人观点和情感
4. 过度使用被动语态
5. 句子长度过于均匀
6. 缺少口语化表达
7. 过于完美的逻辑结构

人性化改写的策略：
1. 变化句式长度和结构
2. 添加个人观点和感受
3. 使用更口语化的表达
4. 加入适当的语气词
5. 打破过于规整的结构
6. 添加一些"不完美"但更真实的表达
7. 保留核心信息，调整表达方式

请根据指定的强度进行改写。"""

    INTENSITY_GUIDES = {
        "light": """轻度改写：保持原文大部分内容，只做轻微调整。
- 调整个别句式
- 添加少量口语化表达
- 保持原有结构不变""",
        "medium": """中度改写：适度调整，保留核心内容。
- 重新组织部分段落
- 添加个人观点
- 调整句式多样性
- 加入一些口语化表达""",
        "heavy": """重度改写：大幅调整，使文章焕然一新。
- 重新组织文章结构
- 大量使用口语化表达
- 添加个人经历和感受
- 打破原有的规整模式
- 让文章更有"人味" """,
    }

    def __init__(
        self,
        api_key: str,
        provider: str = "openai",
        base_url: str = "",
        model: str = "",
    ) -> None:
        self.api_key = api_key
        self.provider = Provider(provider) if isinstance(provider, str) else provider
        self._config = PROVIDER_CONFIG.get(self.provider, PROVIDER_CONFIG[Provider.OPENAI])
        self.base_url = base_url or self._config["base_url"]
        self.model = model or self._config["default_model"]
        self._client = httpx.AsyncClient(timeout=120.0)

    async def humanize(
        self,
        content: str,
        intensity: str = "medium",
        style_hint: Optional[str] = None,
    ) -> HumanizeResult:
        """
        对内容进行去痕处理

        Args:
            content: 原始内容
            intensity: 处理强度 (light/medium/heavy)
            style_hint: 风格提示

        Returns:
            HumanizeResult 包含处理结果
        """
        intensity_guide = self.INTENSITY_GUIDES.get(intensity, self.INTENSITY_GUIDES["medium"])

        prompt = f"""{self.SYSTEM_PROMPT}

改写强度：{intensity}
{intensity_guide}

{f"风格提示：{style_hint}" if style_hint else ""}

原文内容：
{content}

请对上述内容进行人性化改写，使其读起来更像是真人写的内容。
直接输出改写后的内容，使用 Markdown 格式。"""

        humanized = await self._call_ai(prompt)

        changes = await self._analyze_changes(content, humanized)

        return HumanizeResult(
            original=content,
            humanized=humanized,
            changes=changes,
        )

    async def _analyze_changes(self, original: str, humanized: str) -> list[str]:
        """分析改写的变化"""
        prompt = f"""对比原文和改写后的内容，列出主要的变化点。

原文：
{original[:1000]}

改写后：
{humanized[:1000]}

请用简洁的语言列出 3-5 个主要变化点，每点一句话。格式：
1. xxx
2. xxx
..."""

        try:
            result = await self._call_ai(prompt)
            changes = []
            for line in result.split("\n"):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith("-")):
                    change = line.lstrip("0123456789.-) ")
                    if change:
                        changes.append(change)
            return changes[:5]
        except Exception:
            return ["内容已人性化改写"]

    async def _call_ai(self, prompt: str) -> str:
        """调用 AI API"""
        return await self._call_openai_compatible(prompt)

    def _is_custom_config(self) -> bool:
        """检查是否使用了自定义配置"""
        default_config = PROVIDER_CONFIG.get(self.provider, PROVIDER_CONFIG[Provider.OPENAI])
        return (
            self.base_url != default_config["base_url"]
            or self.model != default_config["default_model"]
        )

    async def _call_openai_compatible(self, prompt: str) -> str:
        """调用 OpenAI 兼容格式的 API"""
        response = await self._client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.8,
            },
        )

        response.raise_for_status()
        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "output" in data:
            return data["output"]["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"Unexpected response format: {data}")

    async def close(self) -> None:
        """关闭客户端连接"""
        await self._client.aclose()


async def humanize_content(
    content: str,
    api_key: str,
    intensity: str = "medium",
    provider: str = "openai",
    base_url: str = "",
    model: str = "",
) -> HumanizeResult:
    """
    快捷函数：对内容进行去痕处理

    Args:
        content: 原始内容
        api_key: API 密钥
        intensity: 处理强度
        provider: AI 提供商 (openai/qwen/doubao/minimax/moonshot/zhipu/hunyuan/yi/custom)
        base_url: API 基础 URL (仅在 custom provider 时使用)
        model: 模型名称 (留空则使用 provider 默认模型)

    Returns:
        HumanizeResult
    """
    humanizer = Humanizer(
        api_key=api_key,
        provider=provider,
        base_url=base_url,
        model=model,
    )
    try:
        return await humanizer.humanize(content, intensity)
    finally:
        await humanizer.close()
