"""
Design LLM v1.0 — 大模型驱动设计层
====================================
为 PSD 图层级引擎提供 AI 增强能力：配色生成、布局建议、文案撰写、设计评价。

支持的模型提供商:
  - OpenAI (gpt-4o, gpt-4o-mini)
  - Anthropic Claude (claude-3-5-sonnet)
  - 任何 OpenAI 兼容 API (Ollama, vLLM, DeepSeek 等)

配置方式（任选其一）:
  1. 环境变量:
     OPENAI_API_KEY / ANTHROPIC_API_KEY
     DESIGN_LLM_MODEL=gpt-4o          (可选，默认 gpt-4o-mini)
     DESIGN_LLM_BASE_URL=http://...    (可选，自定义 endpoint)

  2. 代码传参:
     from design_llm import DesignLLM
     llm = DesignLLM(provider="openai", api_key="sk-...", model="gpt-4o")

无 API key 时自动回退到规则引擎。
"""

import json
import os
import re
from typing import Optional

from console_utils import configure_stdio

configure_stdio()


class DesignLLM:
    """设计领域 LLM 适配器"""

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.provider = provider
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model or os.environ.get("DESIGN_LLM_MODEL", "gpt-4o-mini")
        self.base_url = base_url or os.environ.get("DESIGN_LLM_BASE_URL")
        self._available = bool(self.api_key)

    # ── 内部调用 ──

    def _call(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> Optional[str]:
        """调用 LLM，返回文本响应"""
        if not self._available:
            return None

        try:
            if self.provider == "openai" or self.base_url:
                from openai import OpenAI
                client_kwargs = {"api_key": self.api_key}
                if self.base_url:
                    client_kwargs["base_url"] = self.base_url
                client = OpenAI(**client_kwargs)
                resp = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=1024,
                )
                return resp.choices[0].message.content

            elif self.provider == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=self.api_key)
                resp = client.messages.create(
                    model=self.model or "claude-3-5-sonnet-20241022",
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=temperature,
                    max_tokens=1024,
                )
                return resp.content[0].text

        except Exception as e:
            print(f"  ⚠ LLM 调用失败: {e}，回退到规则引擎")
            return None

    def _call_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> Optional[dict]:
        """调用 LLM 并解析 JSON 响应"""
        text = self._call(system_prompt, user_prompt, temperature)
        if not text:
            return None
        # 提取 JSON 块
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return None

    # ── 设计能力 ──

    def generate_palette(self, description: str, count: int = 5) -> dict:
        """
        根据自然语言描述生成配色方案。
        
        例: "深蓝色科技感的企业年会门票"
            → {"bg": "#0A1628", "accent": "#00D4FF", "text": "#FFFFFF", ...}
        """
        if not self._available:
            return None

        system = """你是一位资深视觉设计师。根据用户的场景描述，生成一套专业的配色方案。
返回严格 JSON 格式:
{
  "name": "方案名称",
  "bg": "#背景色",
  "accent": "#强调色",
  "text": "#主文字色",
  "sub": "#辅助文字色",
  "reason": "设计理由(一句话)"
}
配色原则: 符合 WCAG AA 对比度标准，配色和谐，符合场景氛围。"""
        
        user = f"场景: {description}\n生成 {count} 套配色方案，每套包含 bg/accent/text/sub 四个颜色。"
        result = self._call_json(system, user, temperature=0.7)
        return result

    def generate_palettes(self, description: str, count: int = 3) -> list:
        """生成多套配色方案"""
        if not self._available:
            return []
        
        system = """你是资深视觉设计师。根据场景描述生成多套配色方案。
返回严格 JSON 数组格式: [{"name":"方案1","bg":"#...","accent":"#...","text":"#...","sub":"#...","reason":"理由"}, ...]
每个方案的 bg/accent/text/sub 必须符合 WCAG AA 标准。"""
        
        user = f"场景: {description}\n生成 {count} 套不同的配色方案。"
        text = self._call(system, user, temperature=0.9)
        if not text:
            return []
        match = re.search(r'\[[\s\S]*\]', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return []

    def suggest_layout(self, canvas_w: int, canvas_h: int,
                       elements: list, description: str = "") -> dict:
        """
        根据画布和元素列表，LLM 推荐布局参数。
        
        返回: {"elements": [{"role":"title","y_pct":0.08,"size_pct":0.055,"align":"center"}, ...], "reason":"..."}
        """
        if not self._available:
            return None

        system = """你是平面设计排版专家。根据画布尺寸和设计元素，推荐最优排版参数。
返回 JSON: {"elements":[{"role":"元素名","y_pct":0.xx,"size_pct":0.xxx,"align":"center|left|right"},...],"reason":"排版理由"}
y_pct=垂直位置百分比(0~1), size_pct=字号占画布高度百分比。"""
        
        user = f"画布: {canvas_w}×{canvas_h}px\n元素: {json.dumps(elements, ensure_ascii=False)}\n描述: {description}"
        result = self._call_json(system, user, temperature=0.4)
        return result

    def write_copy(self, template_type: str, context: dict) -> dict:
        """
        根据模板类型和上下文，撰写文案。
        
        例: template_type="ticket", context={"event":"春季运动会","date":"2026-06-01"}
            → {"title":"春季运动会入场券","subtitle":"SPRING GAMES 2026",...}
        """
        if not self._available:
            return None

        system = f"""你是专业文案撰写人。为"{template_type}"类设计撰写合适的文字内容。
返回 JSON，字段根据模板类型不同:
- ticket: {{"title":"标题","subtitle":"副标题(英文)","fields":[{{"label":"字段标签","placeholder":"占位符"}}]}}
- certificate: {{"title":"标题","body":"正文","fields":[...]}}
- badge: {{"org":"组织名","name_placeholder":"姓名占位符","role_placeholder":"职位占位符"}}
- invitation: {{"event":"活动名","host":"主办方","date_placeholder":"日期占位符","venue_placeholder":"地点占位符"}}
保持简洁、专业、符合场景。"""

        user = f"类型: {template_type}\n上下文: {json.dumps(context, ensure_ascii=False)}"
        result = self._call_json(system, user, temperature=0.8)
        return result

    def evaluate_design(self, description: str, palette: dict = None,
                        layout: dict = None) -> dict:
        """
        评价设计质量，给出改进建议。
        
        返回: {"score":85,"strengths":["..."],"weaknesses":["..."],"suggestions":["..."]}
        """
        if not self._available:
            return None

        system = """你是设计评审专家。评价设计方案的优劣，给出0-100分数和改进建议。
返回 JSON: {"score":85,"strengths":["优点1","优点2"],"weaknesses":["不足1"],"suggestions":["建议1","建议2"]}"""
        
        user = f"设计描述: {description}\n配色: {json.dumps(palette) if palette else '未指定'}\n布局: {json.dumps(layout) if layout else '未指定'}"
        result = self._call_json(system, user, temperature=0.5)
        return result

    def smart_palette_for_scene(self, scene: str, extra: str = "") -> list:
        """
        根据业务场景智能推荐配色。比内置规则更灵活。
        """
        if not self._available:
            return []
        
        system = """你是视觉设计专家。根据业务场景推荐3套专业配色。
返回 JSON 数组: [{"name":"方案名","bg":"#bg","accent":"#强调","text":"#文字","sub":"#辅助","contrast_ratio":12.5}, ...]
注意: contrast_ratio 是文字色与背景色的 WCAG 对比度估算值。"""
        
        user = f"场景: {scene}。{extra}"
        return self.generate_palettes(f"{scene} - {extra}", count=3) or []


# ═══════════════════════════════════════════════════════
# 模块级便捷函数
# ═══════════════════════════════════════════════════════

_llm_instance = None

def get_llm(**kwargs) -> DesignLLM:
    """获取共享 DesignLLM 实例"""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = DesignLLM(**kwargs)
    return _llm_instance

def generate_palette(description: str) -> Optional[dict]:
    return get_llm().generate_palette(description)

def suggest_layout(w: int, h: int, elements: list, desc: str = "") -> Optional[dict]:
    return get_llm().suggest_layout(w, h, elements, desc)

def write_copy(template_type: str, context: dict) -> Optional[dict]:
    return get_llm().write_copy(template_type, context)

def evaluate_design(desc: str, palette: dict = None, layout: dict = None) -> Optional[dict]:
    return get_llm().evaluate_design(desc, palette, layout)


# ═══════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    llm = DesignLLM()
    if llm._available:
        print(f"✅ LLM 已连接: {llm.model}")
        # 快速测试
        result = llm.generate_palette("科技感蓝色门票")
        if result:
            print(f"   配色方案: {json.dumps(result, ensure_ascii=False)}")
    else:
        print("⚠ LLM 未配置 (无 API key)，将使用规则引擎")
        print("   设置方法: set DESIGN_LLM_MODEL=gpt-4o")
        print("             set OPENAI_API_KEY=sk-...")
