#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voice_policy.py — TTS 多音色与情感策略（v2.8）

功能：
1. 加载 config/voices.yaml 音色库（pyyaml 可选，不可用时降级 JSON 或内置默认值）
2. 场景 → 预设音色映射（正式通知 / 客服安抚 / 营销外呼 3 套预设）
3. 情感 → 语速/语调动态调整（叠加在预设参数之上，自动限幅）
4. SSML 构建（句间停顿 + 数字日期自动加重）
5. 双链路合成调度：Edge TTS 主链路 → 火山 TTS 备用链路 → 文字降级
6. 音色列表命令（list）

降级策略（规则 9）：
- voices.yaml 缺失 / pyyaml 不可用 → 使用内置默认音色，功能不中断
- Edge TTS 不可用（edge_tts 包未安装）→ 自动切火山链路
- 火山 TTS 未配置 VOLC_TTS_KEY → 静默跳过，最终降级为文字回复
- 任何链路异常都不阻断外呼主流程

无 Key 原则（规则 16）：Edge TTS 免费无需 Key 为主链路；火山为可选增强。

依赖：纯 Python 标准库（edge_tts 为可选第三方包，仅主链路探测用）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-20)
"""

import os
import re
import json
import asyncio
import logging
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

# 尝试导入 pyyaml，不可用时降级为 json（与 intent_registry.py 同一约定）
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logger.warning("pyyaml 不可用，将使用 JSON 格式作为降级")

# ==========================================
# 配置
# ==========================================

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
VOICES_FILE_YAML = os.path.join(CONFIG_DIR, 'voices.yaml')
VOICES_FILE_JSON = os.path.join(CONFIG_DIR, 'voices.json')

# 参数限幅（防止叠加后越界，Edge/火山引擎安全范围）
RATE_LIMIT = 50      # ±50%
PITCH_LIMIT = 50     # ±50Hz

# 内置默认音色库（voices.yaml 缺失时的降级配置，保证开箱即用）
DEFAULT_VOICES: Dict[str, Any] = {
    "version": 1,
    "presets": {
        "formal_notice": {
            "display_name": "正式通知",
            "voice": "zh-CN-YunxiNeural",
            "rate": "-10%",
            "pitch": "+0Hz",
            "style": "formal",
            "description": "沉稳正式，适合系统通知、日程提醒、审批结果告知",
            "scenarios": ["ivr", "system_notice"],
        },
        "service_soothe": {
            "display_name": "客服安抚",
            "voice": "zh-CN-XiaoxiaoNeural",
            "rate": "-5%",
            "pitch": "+0Hz",
            "style": "gentle",
            "description": "温柔耐心，适合投诉安抚、故障解释、焦虑客户接听",
            "scenarios": ["inbound", "complaint"],
        },
        "marketing_outbound": {
            "display_name": "营销外呼",
            "voice": "zh-CN-YunjieNeural",
            "rate": "+5%",
            "pitch": "+2Hz",
            "style": "promo",
            "description": "热情活力，适合活动通知、产品推介、回访调查",
            "scenarios": ["outbound", "survey"],
        },
    },
    "scene_mapping": {
        "ivr": "formal_notice",
        "system_notice": "formal_notice",
        "inbound": "service_soothe",
        "complaint": "service_soothe",
        "outbound": "marketing_outbound",
        "survey": "marketing_outbound",
        "default": "formal_notice",
    },
    "emotion_adjust": {
        "angry": {"rate": "-15%", "pitch": "-5Hz"},
        "anxious": {"rate": "-10%", "pitch": "-2Hz"},
        "satisfied": {"rate": "+5%", "pitch": "+2Hz"},
        "confused": {"rate": "-10%", "pitch": "+0Hz"},
        "neutral": {"rate": "+0%", "pitch": "+0Hz"},
    },
    "ssml": {"enabled": True, "sentence_pause_ms": 300, "auto_emphasis": True},
    "links": {
        "primary": {"name": "edge", "display_name": "Edge TTS（主链路）"},
        "fallback": {"name": "volcengine", "display_name": "火山引擎 TTS（备用链路）", "env_key": "VOLC_TTS_KEY"},
    },
    "clone_voices": [],
}


# ==========================================
# 参数解析与格式化工具
# ==========================================

def _parse_percent(value: str) -> int:
    """解析 '-10%' / '+5%' / '0%' 为整数（不带 % 时按 0 处理）"""
    if not value:
        return 0
    m = re.match(r'^([+-]?\d+(?:\.\d+)?)%?$', str(value).strip())
    return int(round(float(m.group(1)))) if m else 0


def _parse_hz(value: str) -> int:
    """解析 '+2Hz' / '-5Hz' 为整数"""
    if not value:
        return 0
    m = re.match(r'^([+-]?\d+(?:\.\d+)?)\s*Hz$', str(value).strip(), re.IGNORECASE)
    return int(round(float(m.group(1)))) if m else 0


def _fmt_percent(num: int) -> str:
    return f"{'+' if num >= 0 else ''}{num}%"


def _fmt_hz(num: int) -> str:
    return f"{'+' if num >= 0 else ''}{num}Hz"


def _clamp(num: int, limit: int) -> int:
    return max(-limit, min(limit, num))


# ==========================================
# 音色策略引擎
# ==========================================

class VoicePolicy:
    """
    TTS 多音色与情感策略引擎

    使用方式：
        policy = VoicePolicy()
        params = policy.resolve_params(scene="outbound", emotion="angry", confidence=0.8)
        # params: {"preset": "marketing_outbound", "voice": "...", "rate": "-10%", "pitch": "-3Hz", ...}
        ssml = policy.build_ssml("您好，通知您...", params)
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._loaded = False

    # ---------- 配置加载 ----------

    def load(self) -> bool:
        """加载音色库配置（yaml → json → 内置默认值 三级降级）"""
        path = self.config_path
        if not path:
            if YAML_AVAILABLE and os.path.exists(VOICES_FILE_YAML):
                path = VOICES_FILE_YAML
            elif os.path.exists(VOICES_FILE_JSON):
                path = VOICES_FILE_JSON
            else:
                path = None

        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if path.endswith(('.yaml', '.yml')):
                        if YAML_AVAILABLE:
                            config = yaml.safe_load(f)
                        else:
                            logger.warning("pyyaml 不可用，尝试解析为 JSON")
                            config = json.load(f)
                    else:
                        config = json.load(f)
                if config and isinstance(config, dict) and config.get('presets'):
                    self.config = config
                    self._loaded = True
                    logger.info(f"音色库加载完成：{len(config.get('presets', {}))} 套预设（{os.path.basename(path)}）")
                    return True
                logger.warning("音色库配置格式错误（缺少 presets），使用内置默认值")
            except Exception as e:
                logger.warning(f"加载音色库失败: {e}，使用内置默认值")

        # 降级：内置默认值（规则 9）
        self.config = DEFAULT_VOICES
        self._loaded = True
        logger.info("使用内置默认音色库（3 套预设）")
        return True

    def _ensure_loaded(self):
        if not self._loaded:
            self.load()

    # ---------- 音色选择 ----------

    def select_preset(self, scene: str = "") -> Tuple[str, Dict[str, Any]]:
        """
        按场景选择预设音色

        Returns:
            (preset_name, preset_dict)
        """
        self._ensure_loaded()
        mapping = self.config.get('scene_mapping', {})
        presets = self.config.get('presets', {})
        name = mapping.get(scene) or mapping.get('default') or 'formal_notice'
        if name not in presets:
            name = 'formal_notice' if 'formal_notice' in presets else next(iter(presets), 'formal_notice')
        return name, presets.get(name, {})

    def adjust_for_emotion(self, emotion: str = "", confidence: float = 0.0) -> Dict[str, int]:
        """
        按情感计算参数调整量（百分点 / Hz）

        低置信度（< 0.5）时不调整，避免误判叠加。
        """
        self._ensure_loaded()
        if not emotion or confidence < 0.5:
            return {"rate": 0, "pitch": 0}
        adjust = self.config.get('emotion_adjust', {}).get(emotion, {})
        return {
            "rate": _parse_percent(adjust.get('rate', '0%')),
            "pitch": _parse_hz(adjust.get('pitch', '+0Hz')),
        }

    def resolve_params(self, scene: str = "", emotion: str = "",
                       confidence: float = 0.0, voice_override: str = "") -> Dict[str, Any]:
        """
        解析最终合成参数：预设 + 情感调整（叠加并限幅）

        Args:
            scene: 场景（ivr/inbound/outbound/complaint/survey/system_notice）
            emotion: 情感（angry/anxious/satisfied/confused/neutral）
            confidence: 情感置信度（< 0.5 不调整）
            voice_override: 指定音色（克隆音色等），优先级最高

        Returns:
            dict: {preset, display_name, voice, rate, pitch, style, emotion, scene}
        """
        preset_name, preset = self.select_preset(scene)
        base_rate = _parse_percent(preset.get('rate', '0%'))
        base_pitch = _parse_hz(preset.get('pitch', '+0Hz'))
        adj = self.adjust_for_emotion(emotion, confidence)

        return {
            "preset": preset_name,
            "display_name": preset.get('display_name', preset_name),
            "voice": voice_override or preset.get('voice', 'zh-CN-YunxiNeural'),
            "rate": _fmt_percent(_clamp(base_rate + adj["rate"], RATE_LIMIT)),
            "pitch": _fmt_hz(_clamp(base_pitch + adj["pitch"], PITCH_LIMIT)),
            "style": preset.get('style', ''),
            "scene": scene,
            "emotion": emotion or "neutral",
        }

    # ---------- SSML 构建 ----------

    def build_ssml(self, text: str, params: Dict[str, Any]) -> str:
        """
        构建 SSML（句间停顿 + 数字日期自动加重）

        Args:
            text: 待合成文本
            params: resolve_params 的输出

        Returns:
            SSML 字符串；ssml.enabled=false 时返回纯文本
        """
        self._ensure_loaded()
        ssml_cfg = self.config.get('ssml', {})
        if not ssml_cfg.get('enabled', True):
            return text

        pause_ms = int(ssml_cfg.get('sentence_pause_ms', 300))
        auto_emphasis = ssml_cfg.get('auto_emphasis', True)

        # 按句切分（保留标点），句间插入 break
        sentences = [s for s in re.split(r'(?<=[。！？；!?;])', text) if s.strip()]
        if not sentences:
            sentences = [text]

        parts = []
        for i, sent in enumerate(sentences):
            content = sent.strip()
            if auto_emphasis:
                # 数字/日期/时间自动加重（如 3点、15日、2026年、80%）
                content = re.sub(
                    r'(\d+\s*(?:点|时|分|日|号|月|年|%|％|元|万|亿|次|位|名|个|条|项|轮|天|周|小时|分钟|秒))',
                    r'<emphasis level="moderate">\1</emphasis>',
                    content,
                )
            parts.append(content)
            if i < len(sentences) - 1:
                parts.append(f'<break time="{pause_ms}ms"/>')

        body = ''.join(parts)
        # XML 转义（emphasis/break 标签之外的内容）
        def _escape(s: str) -> str:
            return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                     .replace('"', '&quot;'))

        # 先转义再还原我们自己的标签
        escaped = _escape(body)
        for tag in ('emphasis', 'break', '/emphasis'):
            escaped = escaped.replace(_escape(f'<{tag}'), f'<{tag}').replace(_escape('/>'), '/>')
        # emphasis 带属性，逐个还原
        escaped = re.sub(r'&lt;(emphasis level=&quot;moderate&quot;)&gt;', r'<\1>', escaped)
        # 还原属性引号（XML 文本节点中裸引号合法）
        escaped = escaped.replace('&quot;', '"')

        return (
            '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">'
            f'<voice name="{params.get("voice", "zh-CN-YunxiNeural")}">'
            f'<prosody rate="{params.get("rate", "+0%")}" pitch="{params.get("pitch", "+0Hz")}">'
            f'{escaped}'
            '</prosody></voice></speak>'
        )

    # ---------- 音色列表 ----------

    def list_voices(self) -> List[Dict[str, Any]]:
        """列出全部可用音色（预设 + 已登记克隆音色）"""
        self._ensure_loaded()
        result = []
        for name, preset in self.config.get('presets', {}).items():
            result.append({
                "id": name,
                "display_name": preset.get('display_name', name),
                "voice": preset.get('voice', ''),
                "rate": preset.get('rate', '+0%'),
                "pitch": preset.get('pitch', '+0Hz'),
                "description": preset.get('description', ''),
                "type": "preset",
            })
        for clone in self.config.get('clone_voices', []) or []:
            result.append({
                "id": clone.get('id', ''),
                "display_name": clone.get('display_name', ''),
                "voice": clone.get('voice', ''),
                "rate": clone.get('rate', '+0%'),
                "pitch": clone.get('pitch', '+0Hz'),
                "description": clone.get('description', ''),
                "type": "clone",
            })
        return result

    def format_voice_list(self) -> str:
        """格式化为中文文本（音色列表命令输出）"""
        voices = self.list_voices()
        lines = [f"可用音色共 {len(voices)} 套：", ""]
        for v in voices:
            tag = "克隆" if v["type"] == "clone" else "预设"
            lines.append(f"  [{tag}] {v['display_name']}（{v['id']}）")
            lines.append(f"        音色: {v['voice']}  语速: {v['rate']}  语调: {v['pitch']}")
            if v.get("description"):
                lines.append(f"        说明: {v['description']}")
        lines.append("")
        lines.append("提示：修改 config/voices.yaml 可自定义音色与场景映射。")
        return "\n".join(lines)


# ==========================================
# 双链路合成调度
# ==========================================

class EdgeTTSLink:
    """Edge TTS 主链路（免费无需 Key；edge_tts 包可用时启用）"""

    name = "edge"

    @staticmethod
    def probe() -> bool:
        """探测是否可用（edge_tts 包是否可导入）"""
        try:
            import edge_tts  # noqa: F401
            return True
        except ImportError:
            return False

    @staticmethod
    def synthesize(text: str, params: Dict[str, Any], output_path: str = "") -> Dict[str, Any]:
        """
        调用 Edge TTS 合成（异步包，用 asyncio.run 包装）

        Returns:
            {"ok": True, "link": "edge", "path": ...} 或 {"ok": False, "reason": ...}
        """
        try:
            import edge_tts
        except ImportError:
            return {"ok": False, "reason": "edge_tts 包未安装"}

        if not output_path:
            output_path = os.path.join(os.path.expanduser("~"), ".wecom_voice", "tts",
                                       f"tts_edge_{abs(hash(text)) % 10**8}.mp3")

        async def _run():
            communicate = edge_tts.Communicate(
                text,
                voice=params.get("voice", "zh-CN-YunxiNeural"),
                rate=params.get("rate", "+0%"),
                pitch=params.get("pitch", "+0Hz"),
            )
            await communicate.save(output_path)

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            asyncio.run(_run())
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return {"ok": True, "link": "edge", "path": output_path}
            return {"ok": False, "reason": "Edge TTS 输出文件为空"}
        except Exception as e:
            logger.warning(f"Edge TTS 合成失败: {e}")
            return {"ok": False, "reason": f"Edge TTS 合成失败: {e}"}


class VolcengineTTSLink:
    """火山引擎 TTS 备用链路（需配置 VOLC_TTS_KEY，未配置静默跳过）"""

    name = "volcengine"

    @staticmethod
    def probe() -> bool:
        """探测是否配置了 Key（规则 16：无 Key 不启用）"""
        return bool(os.environ.get("VOLC_TTS_KEY", ""))

    @staticmethod
    def synthesize(text: str, params: Dict[str, Any], output_path: str = "") -> Dict[str, Any]:
        """
        调用火山引擎 TTS（HTTPS API）

        未配置 Key 时返回不可用；任何网络/协议异常均降级，不抛出。
        """
        api_key = os.environ.get("VOLC_TTS_KEY", "")
        if not api_key:
            return {"ok": False, "reason": "未配置 VOLC_TTS_KEY"}

        try:
            from urllib.request import Request, urlopen
            import ssl

            payload = {
                "app": {"appid": os.environ.get("VOLC_TTS_APPID", ""), "token": api_key,
                        "cluster": os.environ.get("VOLC_TTS_CLUSTER", "volcano_tts")},
                "user": {"uid": "wecom_voice_agent"},
                "audio": {"voice_type": params.get("voice", "zh-CN-YunxiNeural"),
                          "encoding": "mp3", "rate": 24000},
                "request": {"reqid": f"req_{abs(hash(text)) % 10**10}",
                            "text": text, "operation": "query"},
            }
            if not output_path:
                output_path = os.path.join(os.path.expanduser("~"), ".wecom_voice", "tts",
                                           f"tts_volc_{abs(hash(text)) % 10**8}.mp3")
            req = Request(
                "https://openspeech.bytedance.com/api/v1/tts",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json",
                         "Authorization": f"bearer; {api_key}"},
            )
            ctx = ssl.create_default_context()
            with urlopen(req, timeout=10, context=ctx) as resp:
                body = resp.read()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(body)
            if os.path.getsize(output_path) > 0:
                return {"ok": True, "link": "volcengine", "path": output_path}
            return {"ok": False, "reason": "火山 TTS 返回内容为空"}
        except Exception as e:
            logger.warning(f"火山 TTS 合成失败: {e}")
            return {"ok": False, "reason": f"火山 TTS 合成失败: {e}"}


class VoiceSynthesizer:
    """
    双链路合成调度器：Edge 主链路 → 火山备用链路 → 文字降级

    使用方式：
        synth = VoiceSynthesizer()
        result = synth.synthesize("您好，通知您明天下午3点开会。", scene="ivr", emotion="neutral")
        # result: {"ok": True, "link": "edge", "path": ...}
        # 或     {"ok": False, "degraded": True, "text": ..., "message": "语音播报暂时不可用，已为您用文字显示。"}
    """

    DEGRADED_MESSAGE = "语音播报暂时不可用，已为您用文字显示。"

    def __init__(self, policy: Optional[VoicePolicy] = None):
        self.policy = policy or VoicePolicy()
        self.policy.load()
        self._links = [EdgeTTSLink, VolcengineTTSLink]

    def available_links(self) -> List[str]:
        """返回当前可用链路名列表"""
        return [link.name for link in self._links if link.probe()]

    def synthesize(self, text: str, scene: str = "", emotion: str = "",
                   confidence: float = 0.0, output_path: str = "") -> Dict[str, Any]:
        """
        合成语音：主链路失败自动切备用链路，全部不可用降级为文字（规则 9）

        Returns:
            {"ok": True, "link": ..., "path": ..., "params": ...}
            或 {"ok": False, "degraded": True, "text": ..., "message": ..., "params": ...}
        """
        params = self.policy.resolve_params(scene, emotion, confidence)

        for link in self._links:
            if not link.probe():
                logger.info(f"链路 {link.name} 不可用，跳过")
                continue
            result = link.synthesize(text, params, output_path)
            if result.get("ok"):
                result["params"] = params
                return result
            logger.info(f"链路 {link.name} 合成失败（{result.get('reason')}），尝试下一链路")

        # 全部不可用 → 文字降级（不报错、不阻断）
        return {
            "ok": False,
            "degraded": True,
            "text": text,
            "message": self.DEGRADED_MESSAGE,
            "params": params,
        }


# ==========================================
# 便捷函数
# ==========================================

_policy_instance: Optional[VoicePolicy] = None


def get_policy() -> VoicePolicy:
    """获取音色策略单例"""
    global _policy_instance
    if _policy_instance is None:
        _policy_instance = VoicePolicy()
        _policy_instance.load()
    return _policy_instance


def synthesize(text: str, scene: str = "", emotion: str = "",
               confidence: float = 0.0) -> Dict[str, Any]:
    """便捷函数：按场景+情感合成语音（双链路 + 降级）"""
    return VoiceSynthesizer(get_policy()).synthesize(text, scene, emotion, confidence)


# ==========================================
# 命令行入口
# ==========================================

def _print_encoding_safe(text: str):
    """GBK 终端安全输出（Windows 默认编码下中文不乱码）"""
    try:
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(text)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="TTS 多音色与情感策略（v2.8）")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="列出全部可用音色")

    p_synth = sub.add_parser("synth", help="按场景+情感解析合成参数")
    p_synth.add_argument("--text", required=True, help="待合成文本")
    p_synth.add_argument("--scene", default="", help="场景：ivr/inbound/outbound/complaint/survey/system_notice")
    p_synth.add_argument("--emotion", default="", help="情感：angry/anxious/satisfied/confused/neutral")
    p_synth.add_argument("--confidence", type=float, default=0.0, help="情感置信度")
    p_synth.add_argument("--ssml", action="store_true", help="输出 SSML 而不执行合成")

    p_test = sub.add_parser("selftest", help="运行自测")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    policy = get_policy()

    if args.command == "list":
        _print_encoding_safe(policy.format_voice_list())

    elif args.command == "synth":
        params = policy.resolve_params(args.scene, args.emotion, args.confidence)
        _print_encoding_safe(f"场景: {args.scene or '(默认)'}  情感: {args.emotion or '(无)'}")
        _print_encoding_safe(f"音色: {params['display_name']}（{params['voice']}）")
        _print_encoding_safe(f"语速: {params['rate']}  语调: {params['pitch']}")
        if args.ssml:
            _print_encoding_safe("\n" + policy.build_ssml(args.text, params))
        else:
            synth = VoiceSynthesizer(policy)
            links = synth.available_links()
            _print_encoding_safe(f"可用链路: {links if links else '无（将降级为文字）'}")
            result = synth.synthesize(args.text, args.scene, args.emotion, args.confidence)
            if result.get("ok"):
                _print_encoding_safe(f"合成成功（{result['link']}）: {result.get('path', '')}")
            else:
                _print_encoding_safe(f"降级为文字: {result.get('message', '')}")

    elif args.command == "selftest":
        run_self_test()

    else:
        parser.print_help()


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行音色策略自测"""
    _print_encoding_safe("=" * 60)
    _print_encoding_safe("voice_policy.py — 自测模式")
    _print_encoding_safe("=" * 60)

    policy = VoicePolicy()

    # 测试 1: 配置加载
    _print_encoding_safe("\n[测试 1] 配置加载")
    ok = policy.load()
    assert ok is True
    presets = policy.config.get("presets", {})
    assert len(presets) >= 3, "至少 3 套预设"
    _print_encoding_safe(f"  预设数量: {len(presets)} ✅")

    # 测试 2: 场景 → 预设映射
    _print_encoding_safe("\n[测试 2] 场景映射")
    for scene, expect in [("ivr", "formal_notice"), ("inbound", "service_soothe"),
                          ("outbound", "marketing_outbound"), ("complaint", "service_soothe"),
                          ("unknown_scene", "formal_notice")]:
        name, _ = policy.select_preset(scene)
        assert name == expect, f"{scene} 应映射 {expect}，实际 {name}"
        _print_encoding_safe(f"  {scene or '(空)'} → {name} ✅")

    # 测试 3: 情感参数叠加与限幅
    _print_encoding_safe("\n[测试 3] 情感参数调整")
    p = policy.resolve_params("outbound", "angry", 0.9)
    assert p["rate"] == "-10%", f"营销外呼+愤怒应为 -10%，实际 {p['rate']}"  # +5% + (-15%)
    assert p["pitch"] == "-3Hz", f"营销外呼+愤怒应为 -3Hz，实际 {p['pitch']}"  # +2Hz + (-5Hz)
    _print_encoding_safe(f"  营销外呼+愤怒: {p['rate']} {p['pitch']} ✅")
    p2 = policy.resolve_params("ivr", "anxious", 0.9)
    assert p2["rate"] == "-20%", f"正式通知+焦虑应为 -20%，实际 {p2['rate']}"  # -10% + (-10%)
    _print_encoding_safe(f"  正式通知+焦虑: {p2['rate']} ✅")
    p3 = policy.resolve_params("ivr", "angry", 0.3)  # 低置信度不调整
    assert p3["rate"] == "-10%", f"低置信度不应调整，实际 {p3['rate']}"
    _print_encoding_safe(f"  低置信度(0.3)不调整: {p3['rate']} ✅")

    # 测试 4: SSML 构建
    _print_encoding_safe("\n[测试 4] SSML 构建")
    params = policy.resolve_params("ivr")
    ssml = policy.build_ssml("您好，通知您明天下午3点开会。请准时参加。", params)
    assert "<speak" in ssml and "<prosody" in ssml and "<break" in ssml
    assert "<emphasis" in ssml, "数字日期应自动加重"
    assert 'level="moderate"' in ssml, "emphasis 属性引号应还原"
    assert "&amp;" not in ssml.replace("&amp;lt;", "").replace("&amp;gt;", "").replace("&amp;quot;", ""), "正文不应有未还原转义"
    _print_encoding_safe(f"  SSML 长度: {len(ssml)} 字符 ✅")

    # 测试 5: SSML 关闭时返回纯文本
    _print_encoding_safe("\n[测试 5] SSML 开关")
    policy.config["ssml"]["enabled"] = False
    plain = policy.build_ssml("测试文本。", params)
    assert plain == "测试文本。"
    policy.config["ssml"]["enabled"] = True
    _print_encoding_safe("  enabled=false 返回纯文本 ✅")

    # 测试 6: 音色列表
    _print_encoding_safe("\n[测试 6] 音色列表")
    voices = policy.list_voices()
    assert len(voices) >= 3
    listing = policy.format_voice_list()
    assert "可用音色" in listing
    _print_encoding_safe(f"  音色数量: {len(voices)} ✅")

    # 测试 7: 双链路降级（沙箱无 edge_tts / 无 Key → 降级为文字）
    _print_encoding_safe("\n[测试 7] 双链路降级")
    synth = VoiceSynthesizer(policy)
    links = synth.available_links()
    _print_encoding_safe(f"  当前可用链路: {links if links else '无'}")
    result = synth.synthesize("测试降级。", scene="ivr")
    if result.get("ok"):
        _print_encoding_safe(f"  链路可用，合成成功（{result['link']}）✅")
    else:
        assert result.get("degraded") is True
        assert result.get("text") == "测试降级。"
        assert result.get("message") == VoiceSynthesizer.DEGRADED_MESSAGE
        _print_encoding_safe("  无可用链路 → 降级为文字，不报错 ✅")

    # 测试 8: voice_override（克隆音色直通）
    _print_encoding_safe("\n[测试 8] 音色覆盖")
    p4 = policy.resolve_params("ivr", voice_override="clone_voice_001")
    assert p4["voice"] == "clone_voice_001"
    _print_encoding_safe(f"  override: {p4['voice']} ✅")

    _print_encoding_safe(f"\n{'='*60}")
    _print_encoding_safe("所有自测通过 ✓")
    _print_encoding_safe("=" * 60)


if __name__ == "__main__":
    main()
