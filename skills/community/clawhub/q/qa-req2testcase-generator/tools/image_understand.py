#!/usr/bin/env python3
"""
T1-05：图片理解调度模块 image_understand.py
协调图片抽取、模型探测、视觉/OCR/纯文本三种模式的图片理解流程。

功能：
- 路径选择：vision → ocr → context_only
- 单图失败降级路径（§3.4.1）
- 视觉模式调用 PX_image_understand.md Prompt
- 图片价值分级（high/medium/low）
- 聚合输出对齐 §8.3 Schema
- 文档级 token 预算控制

依赖：image_extract.py, model_detect.py
"""

import json
import os
import re
import time
import tempfile
from typing import List, Dict, Optional, Callable, Any
from pathlib import Path
from difflib import SequenceMatcher


# ============================================================
# 常量
# ============================================================

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)
_PX_PROMPT_PATH = os.path.join(_SKILL_DIR, 'prompts', 'PX_image_understand.md')
_EXPERIENCE_POOL_PATH = os.path.join(
    _SKILL_DIR, 'knowledge', 'experience_pool.json'
)  # T3-04: 经验池路径

# 文档级 token 预算
MAX_HIGH_VALUE_DEEP_PARSE = 20   # 高价值图深解析上限
MAX_AGGREGATE_TOKENS = 8000      # 聚合输出总 token 上限

# 价值分级映射
VALUE_LEVEL_MAP = {
    "ui_mockup": "high",
    "flowchart": "high",
    "state_diagram": "high",
    "table_rule": "high",
    "annotated_screenshot": "high",
    "api_snapshot": "medium",
    "report_chart": "low",
    "unknown": "low",
}

# 处理状态枚举
STATUS_SUCCESS = "success"
STATUS_SUCCESS_DEGRADED = "success_degraded"
STATUS_SUCCESS_VISION_FAILED = "success_vision_failed"
STATUS_SUCCESS_OCR_FAILED = "success_ocr_failed"
STATUS_SKIPPED = "skipped"
STATUS_SKIPPED_LOW_VALUE = "skipped_low_value"
STATUS_SKIPPED_NO_VISION = "skipped_no_vision"
STATUS_SKIPPED_UNKNOWN = "skipped_unknown"
STATUS_FAILED = "failed"


# ============================================================
# 单图处理结果模板
# ============================================================

def _empty_image_result(image_id: str, section: str = "",
                        caption: str = "", before_text: str = "",
                        after_text: str = "") -> dict:
    """生成空的单图结果模板"""
    return {
        "schema_version": "1.4.0",
        "image_id": image_id,
        "file_path": "",
        "classification": {
            "type": "unknown",
            "value_level": "low",
            "confidence": 0.0,
            "classification_method": "none",
            "model_used": ""
        },
        "extraction_mode": "context_only",
        "processing_status": STATUS_SKIPPED,
        "token_cost": {"input_tokens": 0, "output_tokens": 0},
        "content_hash": "",
        "section": section,
        "summary": "",
        "extracted_rules": [],
        "derived_features": [],
        "derived_test_points": [],
        "derived_risks": [],
        "derived_questions": [],
        "type_specific": {},
        "text_image_conflicts": [],
        "quality_score": {
            "completeness": 0.0,
            "actionability": 0.0,
            "non_redundancy": 0.0
        },
        "degradation_notice": None,
        "before_text": before_text,
        "after_text": after_text,
        "caption": caption,
    }


# ============================================================
# Prompt 加载与构造
# ============================================================

def _load_px_prompt() -> str:
    """加载 PX_image_understand.md Prompt 模板"""
    if os.path.exists(_PX_PROMPT_PATH):
        with open(_PX_PROMPT_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def _build_vision_prompt(image_info: dict, px_prompt: str) -> str:
    """
    构造视觉模式的完整 Prompt。
    将图片上下文信息填入模板。
    """
    prompt = px_prompt
    # 替换占位符
    replacements = {
        "{image_id}": image_info.get("image_id", ""),
        "{section}": image_info.get("section", image_info.get("section_heading", "")),
        "{before_text}": image_info.get("before_text", ""),
        "{after_text}": image_info.get("after_text", ""),
        "{caption}": image_info.get("caption", ""),
    }
    for key, value in replacements.items():
        prompt = prompt.replace(key, str(value))
    return prompt


# ============================================================
# 核心调度器
# ============================================================

class ImageUnderstandingDispatcher:
    """
    图片理解调度器。
    根据模型能力选择处理模式，协调单图处理和聚合输出。
    """

    def __init__(self,
                 active_mode: str = "vision",
                 model_id: str = "",
                 model_capability: dict = None,
                 ocr_status: dict = None,
                 model_caller: Callable = None,
                 task_id: str = ""):
        """
        Args:
            active_mode: 处理模式 vision / ocr / context_only
            model_id: 模型标识
            model_capability: 模型能力探测结果
            ocr_status: OCR 可用性状态
            model_caller: 模型调用函数，签名 fn(prompt, image_path=None) -> str
            task_id: 任务 ID
        """
        self.active_mode = active_mode
        self.model_id = model_id
        self.model_capability = model_capability or {}
        self.ocr_status = ocr_status or {}
        self.model_caller = model_caller
        self.task_id = task_id
        self.px_prompt = _load_px_prompt()

        # 统计计数器
        self._vision_count = 0
        self._ocr_count = 0
        self._ocr_degraded_count = 0
        self._context_only_count = 0
        self._skipped_count = 0
        self._failed_count = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._high_value_parsed = 0

    def process_images(self, extracted_images: List[dict]) -> dict:
        """
        处理所有抽取的图片，返回聚合输出（§8.3 Schema）。

        Args:
            extracted_images: image_extract.py 输出的图片列表

        Returns:
            聚合输出 dict
        """
        image_results = []

        for img in extracted_images:
            # 跳过重复图片
            if img.get("is_duplicate", False):
                continue

            result = self._process_single_image(img)
            image_results.append(result)

        return self._build_aggregate_output(image_results)

    def _process_single_image(self, img: dict) -> dict:
        """
        处理单张图片，含降级路径。
        """
        image_id = img.get("image_id", "")
        file_path = img.get("file_path", "")
        section = img.get("section", img.get("section_heading", ""))
        caption = img.get("caption", "")
        before_text = img.get("before_text", "")
        after_text = img.get("after_text", "")
        content_hash = img.get("content_hash", img.get("md5", ""))

        # 基础结果
        result = _empty_image_result(image_id, section, caption, before_text, after_text)
        result["file_path"] = file_path
        result["content_hash"] = content_hash

        # EMF 转换失败的图片，降级为纯文本
        if img.get("extraction_status") == "conversion_failed":
            result["processing_status"] = STATUS_SKIPPED
            result["extraction_mode"] = "context_only"
            result["degradation_notice"] = "EMF 格式转换失败，图片内容未被解析。"
            self._context_only_count += 1
            return result

        # 根据模式处理
        if self.active_mode == "vision":
            return self._process_vision(result, img)
        elif self.active_mode == "ocr":
            return self._process_ocr(result, img)
        else:
            return self._process_context_only(result, img)

    def _process_vision(self, result: dict, img: dict) -> dict:
        """视觉模式处理单图"""
        image_id = result["image_id"]
        file_path = img.get("file_path", "")

        # 预分类（基于上下文快速判断价值等级）
        pre_value = self._pre_classify_value(img)

        # 低价值图跳过深度解析
        if pre_value == "low":
            result["classification"]["value_level"] = "low"
            result["processing_status"] = STATUS_SKIPPED_LOW_VALUE
            result["extraction_mode"] = "skipped"
            result["summary"] = f"低价值图片，跳过深度解析"
            self._skipped_count += 1
            return result

        # 文档级预算控制
        if self._high_value_parsed >= MAX_HIGH_VALUE_DEEP_PARSE:
            result["classification"]["value_level"] = pre_value
            result["processing_status"] = STATUS_SKIPPED
            result["extraction_mode"] = "skipped"
            result["summary"] = "超出文档级深解析预算，跳过"
            self._skipped_count += 1
            return result

        # 调用视觉模型
        if self.model_caller and file_path and os.path.exists(file_path):
            try:
                prompt = _build_vision_prompt(img, self.px_prompt)
                response = self.model_caller(prompt, file_path)

                # 解析模型返回的 JSON
                parsed = self._parse_model_response(response)
                if parsed:
                    # 合并模型输出到结果
                    result = self._merge_model_output(result, parsed)
                    result["extraction_mode"] = "vision"
                    result["processing_status"] = STATUS_SUCCESS
                    result["classification"]["classification_method"] = "vision"
                    result["classification"]["model_used"] = self.model_id
                    self._vision_count += 1
                    self._high_value_parsed += 1

                    # R2修复：unknown类型标记skipped_unknown
                    if result["classification"].get("type") == "unknown":
                        result["processing_status"] = STATUS_SKIPPED_UNKNOWN
                        result["extraction_mode"] = "skipped"
                        result["summary"] = "无法识别图片类型，跳过深度解析"
                        self._skipped_count += 1
                        return result

                    # 估算 token 消耗
                    input_tokens = len(prompt) // 4 + 1500  # 图片约 1500 tokens
                    output_tokens = len(response) // 4 if response else 0
                    result["token_cost"] = {
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens
                    }
                    self._total_input_tokens += input_tokens
                    self._total_output_tokens += output_tokens
                    return result
                else:
                    # 解析失败，降级
                    return self._fallback_to_ocr(result, img, "vision response parse failed")

            except Exception as e:
                # 视觉模式失败，降级到 OCR
                return self._fallback_to_ocr(result, img, str(e))
        else:
            # I-FIX-13: 无模型调用能力或文件不存在，补充切换OCR模式的提示
            return self._fallback_to_ocr(
                result, img,
                "当前模型不支持视觉能力，可切换到OCR模式提取图片文字信息"
            )

    def _process_ocr(self, result: dict, img: dict) -> dict:
        """I-FIX-01: OCR 模式处理单图，集成调用 image_ocr.py"""
        image_id = result["image_id"]
        file_path = img.get("file_path", "")
        before_text = img.get("before_text", "") or ""
        after_text = img.get("after_text", "") or ""
        caption = img.get("caption", "") or ""
        section = img.get("section", img.get("section_heading", "")) or ""

        # I-FIX-01: 集成调用 image_ocr.py 的 OCR 引擎
        try:
            from image_ocr import ocr_single_image, postprocess_ocr_text, detect_available_engine

            # 检测可用 OCR 引擎
            engine_info = detect_available_engine()
            if not engine_info.get("ocr_available"):
                # OCR 引擎不可用，降级为 context_only
                result["extraction_mode"] = "context_only"
                result["processing_status"] = STATUS_SKIPPED
                result["degradation_notice"] = (
                    "OCR 引擎不可用（未安装 Tesseract/PaddleOCR/EasyOCR），"
                    "已降级为纯文本模式。图片内容未被解析，测试用例可能遗漏图中信息。"
                )
                self._context_only_count += 1
                return result

            engine = engine_info["ocr_engine"]

            # 执行 OCR 识别
            ocr_result = ocr_single_image(
                image_path=file_path,
                image_id=image_id,
                engine=engine,
                before_text=before_text,
                after_text=after_text,
                caption=caption,
                apply_correction=True,
            )

            if ocr_result.status == "ok" and ocr_result.corrected_text:
                # OCR 成功，记录结果
                result["ocr_text"] = ocr_result.ocr_text
                result["corrected_text"] = ocr_result.corrected_text

                # 基于上下文推断图片类型（必须在首次引用前赋值，修复 NameError）
                inferred_type = self._infer_type_from_context(
                    caption, before_text, after_text, section
                )

                # R3修复：按类型区分 ocr vs ocr_degraded
                # table_rule/api_snapshot → ocr（核心价值场景）
                # 其他类型 → ocr_degraded（降级OCR）
                ocr_core_types = {"table_rule", "api_snapshot"}
                if inferred_type in ocr_core_types:
                    result["extraction_mode"] = "ocr"
                    result["processing_status"] = STATUS_SUCCESS
                else:
                    result["extraction_mode"] = "ocr_degraded"
                    result["processing_status"] = STATUS_SUCCESS_DEGRADED
                    self._ocr_degraded_count += 1

                # R3修复：classification_method应为 ocr/ocr_context 而非 context_inference
                result["classification"]["classification_method"] = (
                    "ocr" if inferred_type in ocr_core_types else "ocr_context"
                )

                result["classification"]["type"] = inferred_type
                result["classification"]["value_level"] = VALUE_LEVEL_MAP.get(
                    inferred_type, "low"
                )

                # OCR 模式置信度按类型设置
                ocr_confidence_map = {
                    "table_rule": 0.70, "api_snapshot": 0.65,
                    "ui_mockup": 0.50, "flowchart": 0.50,
                    "annotated_screenshot": 0.50,
                    "state_diagram": 0.40, "report_chart": 0.40,
                }
                result["classification"]["confidence"] = ocr_confidence_map.get(
                    inferred_type, 0.30
                )

                result["summary"] = f"[OCR模式] {ocr_result.corrected_text[:100]}"
                self._ocr_count += 1
                return result
            else:
                # OCR 失败，降级为 context_only
                result["extraction_mode"] = "context_only"
                result["processing_status"] = STATUS_SUCCESS_OCR_FAILED
                result["degradation_notice"] = (
                    f"OCR 识别失败（{ocr_result.error_message}），"
                    "已降级为纯文本模式。图片内容未被解析。"
                )
                self._ocr_degraded_count += 1
                self._context_only_count += 1
                return result

        except ImportError:
            # image_ocr.py 不可用，降级为 context_only
            result["extraction_mode"] = "context_only"
            result["processing_status"] = STATUS_SKIPPED
            result["degradation_notice"] = (
                "OCR 模块未找到（image_ocr.py），"
                "已降级为纯文本模式。图片内容未被解析。"
            )
            self._context_only_count += 1
            return result
        except Exception as e:
            # OCR 处理异常，降级为 context_only
            result["extraction_mode"] = "context_only"
            result["processing_status"] = STATUS_SUCCESS_OCR_FAILED
            result["degradation_notice"] = (
                f"OCR 处理异常（{str(e)}），"
                "已降级为纯文本模式。"
            )
            self._context_only_count += 1
            return result

    def _process_context_only(self, result: dict, img: dict) -> dict:
        """
        T3-01：纯文本模式（context_only）完整实现。
        跳过图片内容解析，仅记录元数据，将上下文组合为 P0 补充输入。

        处理逻辑：
        1. 记录元数据：image_id / section / caption / before_text / after_text
        2. caption + before_text + after_text 组合为 P0 补充输入
        3. extraction_mode 标记为 "context_only"
        4. 基于上下文推断图片类型（用于降级说明细化）
        5. 生成纯文本模式降级说明
        """
        image_id = result["image_id"]
        section = result.get("section", "")
        caption = img.get("caption", "") or ""
        before_text = img.get("before_text", "") or ""
        after_text = img.get("after_text", "") or ""

        # T3-01: 记录完整元数据
        result["extraction_mode"] = "context_only"
        result["processing_status"] = STATUS_SKIPPED_NO_VISION
        result["caption"] = caption
        result["before_text"] = before_text
        result["after_text"] = after_text
        result["section"] = section

        # T3-01: 基于上下文推断图片类型（辅助降级说明细化）
        inferred_type = self._infer_type_from_context(
            caption, before_text, after_text, section
        )
        result["classification"]["type"] = inferred_type
        result["classification"]["value_level"] = VALUE_LEVEL_MAP.get(
            inferred_type, "low"
        )
        result["classification"]["confidence"] = 0.0  # 纯文本模式无置信度
        result["classification"]["classification_method"] = "context_inference"

        # T3-01: 组合上下文作为 P0 补充输入
        context_supplement = self._build_context_supplement(
            image_id, section, caption, before_text, after_text
        )
        result["context_supplement"] = context_supplement

        # T3-01: 生成摘要（基于上下文）
        summary_parts = []
        if caption:
            summary_parts.append(f"图注：{caption}")
        if before_text:
            summary_parts.append(f"前文提及：{before_text[:80]}")
        if after_text:
            summary_parts.append(f"后文提及：{after_text[:80]}")
        result["summary"] = (
            "[纯文本模式] " + "；".join(summary_parts)
            if summary_parts
            else "[纯文本模式] 无可用上下文信息"
        )

        # T3-01: 生成纯文本模式降级说明（按推断类型细化）
        result["degradation_notice"] = self._build_context_only_degradation(
            inferred_type, image_id
        )

        # T3-01: 纯文本模式不生成 derived_*，避免噪声（对齐方案 §4.3）
        result["derived_features"] = []
        result["derived_test_points"] = []
        result["derived_risks"] = []
        result["derived_questions"] = []

        self._context_only_count += 1
        return result

    # T3-01: 上下文推断图片类型
    def _infer_type_from_context(self, caption: str, before_text: str,
                                  after_text: str, section: str) -> str:
        """
        T3-01：基于上下文关键词推断图片类型。
        用于纯文本模式下辅助降级说明细化。
        """
        context = (caption + " " + before_text + " " + after_text
                   + " " + section).lower()

        # T3-04: 先查经验池纠偏记录
        corrected = self._check_experience_pool_correction(context)
        if corrected:
            return corrected

        # 关键词匹配推断（对齐方案 §4.2 OCR 模式分类逻辑）
        type_keywords = {
            "flowchart": [
                "流程图", "泳道图", "流程示意", "审批流程", "业务流程",
                "flow", "swimlane", "流程"
            ],
            "ui_mockup": [
                "原型图", "界面稿", "页面设计", "截图", "页面", "界面",
                "mockup", "wireframe", "原型", "布局"
            ],
            "state_diagram": [
                "状态图", "时序图", "状态迁移", "状态机",
                "state", "sequence", "状态"
            ],
            "table_rule": [
                "字段表", "规则表", "矩阵", "字段", "规则",
                "table", "matrix", "枚举"
            ],
            "annotated_screenshot": [
                "批注", "标注", "标框", "annotated", "annotation"
            ],
            "api_snapshot": [
                "接口", "api", "请求", "响应", "url", "endpoint"
            ],
            "report_chart": [
                "图表", "统计", "趋势", "chart", "graph", "报表"
            ],
        }

        for img_type, keywords in type_keywords.items():
            for kw in keywords:
                if kw in context:
                    return img_type

        return "unknown"

    # T3-01: 组合上下文为 P0 补充输入
    def _build_context_supplement(self, image_id: str, section: str,
                                   caption: str, before_text: str,
                                   after_text: str) -> dict:
        """
        T3-01：将 caption + before_text + after_text 组合为 P0 补充输入。
        """
        supplement_parts = []
        if caption:
            supplement_parts.append(f"[图注] {caption}")
        if before_text:
            # 截取前 200 字，避免过长
            supplement_parts.append(f"[图前文] {before_text[:200]}")
        if after_text:
            supplement_parts.append(f"[图后文] {after_text[:200]}")

        return {
            "image_id": image_id,
            "section": section,
            "caption": caption,
            "before_text": before_text[:200] if before_text else "",
            "after_text": after_text[:200] if after_text else "",
            "combined_text": "\n".join(supplement_parts),
            "extraction_mode": "context_only",
        }

    # T3-01: 纯文本模式降级说明（按类型细化）
    def _build_context_only_degradation(self, inferred_type: str,
                                         image_id: str) -> str:
        """
        T3-01：生成纯文本模式的降级说明，按推断的图片类型细化提示。
        """
        base_notice = (
            "当前模型不支持图片理解，图片内容未被解析。"
        )

        # 按类型细化缺失信息提示
        type_hints = {
            "flowchart": "该图可能为流程图，流程分支、判断逻辑、回退路径等信息均未解析。",
            "ui_mockup": "该图可能为原型图，页面布局、控件属性、交互状态等信息均未解析。",
            "state_diagram": "该图可能为状态图，状态迁移条件、触发事件等信息均未解析。",
            "table_rule": "该图可能为规则表，字段定义、枚举值、校验规则等信息均未解析。",
            "annotated_screenshot": "该图可能为批注截图，批注内容、标框对象等信息均未解析。",
            "api_snapshot": "该图可能为接口截图，接口字段、参数定义等信息均未解析。",
            "report_chart": "该图可能为报告图表，数据趋势、统计信息等未解析。",
        }

        hint = type_hints.get(inferred_type, "图片内容信息均未解析。")

        return (
            f"{base_notice}{hint}"
            "测试用例可能遗漏图中信息，建议人工审阅需求文档中的图片。"
        )

    # T3-04: 经验池优先匹配（分类纠偏）
    def _check_experience_pool_correction(self, context: str) -> Optional[str]:
        """
        T3-04：分类前先查 experience_pool 中同上下文关键词的纠正记录。
        如果有历史纠正，优先使用纠正后的类型。
        匹配规则：context_keywords 与当前图片的 section/before_text 关键词重叠度 ≥ 0.6

        Args:
            context: 当前图片的上下文文本（小写）

        Returns:
            纠正后的类型字符串，或 None（无匹配）
        """
        if not os.path.exists(_EXPERIENCE_POOL_PATH):
            return None

        try:
            with open(_EXPERIENCE_POOL_PATH, 'r', encoding='utf-8') as f:
                pool = json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

        feedback_entries = pool.get("feedback_entries", [])
        if not feedback_entries:
            return None

        # 提取当前上下文的关键词集合（简单分词：按空格和标点分割，过滤短词）
        current_keywords = self._extract_keywords(context)
        if not current_keywords:
            return None

        best_match = None
        best_overlap = 0.0

        for entry in feedback_entries:
            # 只匹配 classification_error 类型的纠偏记录
            if entry.get("feedback_type") != "classification_error":
                continue

            entry_keywords = set(entry.get("context_keywords", []))
            if not entry_keywords:
                continue

            # 计算关键词重叠度
            overlap = self._keyword_overlap(current_keywords, entry_keywords)
            if overlap >= 0.6 and overlap > best_overlap:
                corrected_type = entry.get("corrected_type", "")
                if corrected_type:
                    best_overlap = overlap
                    best_match = corrected_type

        return best_match

    # T3-04: 关键词提取
    @staticmethod
    def _extract_keywords(text: str) -> set:
        """
        T3-04：从文本中提取关键词集合。
        简单分词：按空格和常见标点分割，过滤长度 < 2 的词。
        """
        if not text:
            return set()
        # 按非中文字母数字字符分割
        tokens = re.split(r'[\s,，。；;：:、/\\()（）\[\]【】{}"\']', text)
        # 过滤短词
        return {t.strip().lower() for t in tokens if len(t.strip()) >= 2}

    # T3-04: 关键词重叠度计算
    @staticmethod
    def _keyword_overlap(set_a: set, set_b: set) -> float:
        """
        T3-04：计算两个关键词集合的重叠度。
        重叠度 = 交集大小 / 较小集合大小
        """
        if not set_a or not set_b:
            return 0.0
        intersection = set_a & set_b
        min_size = min(len(set_a), len(set_b))
        return len(intersection) / min_size if min_size > 0 else 0.0

    def _fallback_to_ocr(self, result: dict, img: dict, reason: str) -> dict:
        """
        视觉模式失败后降级到 OCR。
        §3.4.1 单图失败降级路径。
        I-FIX-01补充：OCR可用时调用_process_ocr()复用OCR能力，不再直接跳context_only。
        """
        result["processing_status"] = STATUS_SUCCESS_VISION_FAILED

        # 检查 OCR 可用性
        if self.ocr_status and self.ocr_status.get("ocr_available"):
            # I-FIX-01: OCR 可用，调用 _process_ocr 复用 OCR 能力
            try:
                ocr_result = self._process_ocr(result, img)
                if ocr_result.get("processing_status") in ("success", "success_degraded"):
                    # OCR 成功，更新状态但保留视觉失败的标记
                    ocr_result["processing_status"] = STATUS_SUCCESS_VISION_FAILED
                    ocr_result["degradation_notice"] = (
                        f"视觉模式处理失败（{reason}），已降级到OCR模式提取。"
                    )
                    return ocr_result
            except Exception as e:
                # OCR 调用也失败，继续降级到纯文本
                reason = f"视觉失败+OCR异常({e})"

        # OCR 不可用或 OCR 也失败，降级为纯文本
        result["extraction_mode"] = "context_only"
        result["degradation_notice"] = (
            f"视觉模式处理失败（{reason}），OCR 不可用，"
            "已降级为纯文本模式。"
        )
        self._context_only_count += 1

        return result

    def _pre_classify_value(self, img: dict) -> str:
        """
        基于上下文快速预判图片价值等级。
        用于在调用模型前过滤低价值图。
        """
        caption = (img.get("caption", "") or "").lower()
        before_text = (img.get("before_text", "") or "").lower()
        after_text = (img.get("after_text", "") or "").lower()
        context = caption + before_text + after_text

        # 高价值关键词
        high_keywords = [
            "原型", "界面", "页面", "流程", "泳道", "状态", "时序",
            "字段", "规则", "矩阵", "截图", "标注", "批注",
            "mockup", "wireframe", "flow", "state", "diagram"
        ]
        for kw in high_keywords:
            if kw in context:
                return "high"

        # 中等价值关键词
        medium_keywords = ["接口", "api", "请求", "响应", "url"]
        for kw in medium_keywords:
            if kw in context:
                return "medium"

        # 低价值关键词
        low_keywords = ["图表", "统计", "趋势", "chart", "graph", "logo", "图标"]
        for kw in low_keywords:
            if kw in context:
                return "low"

        # 默认中等（交给模型判断）
        return "medium"

    def _parse_model_response(self, response: str) -> Optional[dict]:
        """解析模型返回的 JSON 响应"""
        if not response:
            return None

        # I-FIX-17: 删除函数内重复的 import re，已在文件顶部导入

        # 尝试直接解析
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # 尝试提取 ```json ... ``` 代码块
        match = re.search(r'```json\s*\n(.*?)\n\s*```', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试提取第一个 { ... } 块
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        return None

    def _merge_model_output(self, result: dict, parsed: dict) -> dict:
        """将模型输出合并到结果模板"""
        # 分类信息
        if "classification" in parsed:
            cls = parsed["classification"]
            result["classification"]["type"] = cls.get("type", "unknown")
            result["classification"]["confidence"] = cls.get("confidence", 0.0)
            # 根据类型设置价值等级
            img_type = result["classification"]["type"]
            result["classification"]["value_level"] = VALUE_LEVEL_MAP.get(img_type, "low")

        # 摘要
        result["summary"] = parsed.get("summary", "")

        # 提取结果（带上限控制）
        result["extracted_rules"] = (parsed.get("extracted_rules", []) or [])[:10]
        result["derived_features"] = (parsed.get("derived_features", []) or [])[:15]
        result["derived_test_points"] = (parsed.get("derived_test_points", []) or [])[:10]
        result["derived_risks"] = (parsed.get("derived_risks", []) or [])[:5]
        result["derived_questions"] = (parsed.get("derived_questions", []) or [])[:5]

        # 类型特定字段
        result["type_specific"] = parsed.get("type_specific", {})

        # 图文冲突
        result["text_image_conflicts"] = parsed.get("text_image_conflicts", [])

        # 质量评分
        if "quality_score" in parsed:
            result["quality_score"] = parsed["quality_score"]

        return result

    def _build_aggregate_output(self, image_results: List[dict]) -> dict:
        """
        构建聚合输出（§8.3 Schema）。
        """
        # 统计
        total = len(image_results)
        high_value = len([r for r in image_results
                         if r["classification"]["value_level"] == "high"])
        medium_value = len([r for r in image_results
                           if r["classification"]["value_level"] == "medium"])
        low_value = len([r for r in image_results
                        if r["classification"]["value_level"] == "low"])

        # 降级说明
        degradation_summary = self._build_degradation_summary(image_results)

        # 聚合 derived_* 数据
        aggregate = self._build_aggregate_derived(image_results)

        # 图文冲突汇总
        all_conflicts = []
        for r in image_results:
            all_conflicts.extend(r.get("text_image_conflicts", []))

        # 覆盖矩阵
        coverage_matrix = self._build_coverage_matrix(image_results)

        return {
            "schema_version": "1.4.0",
            "task_id": self.task_id,
            "model_capability": self.model_capability,
            "mode_summary": {
                "active_mode": self.active_mode,
                "vision_count": self._vision_count,
                "ocr_count": self._ocr_count,
                "ocr_degraded_count": self._ocr_degraded_count,
                "context_only_count": self._context_only_count,
                "skipped_count": self._skipped_count,
            },
            "processing_summary": {
                "total_images": total,
                "high_value": high_value,
                "medium_value": medium_value,
                "low_value": low_value,
                "skipped": self._skipped_count,
                "failed": self._failed_count,
                "total_input_tokens": self._total_input_tokens,
                "total_output_tokens": self._total_output_tokens,
            },
            "degradation_summary": degradation_summary,
            "aggregate": aggregate,
            "text_image_conflicts": all_conflicts,
            "coverage_matrix": coverage_matrix,
            "images": image_results,
        }

    def _build_degradation_summary(self, image_results: List[dict]) -> Optional[str]:
        """生成降级说明摘要"""
        if self.active_mode == "vision" and self._context_only_count == 0:
            return None

        if self.active_mode == "context_only":
            return (
                "当前模型不支持图片理解，图片内容未被解析。"
                "测试用例可能遗漏图中信息（页面布局、流程分支、字段定义等）。"
                "建议人工审阅需求文档中的所有图片，补充遗漏的测试场景。"
            )

        if self.active_mode == "ocr":
            # 统计各类型降级图片数
            type_counts = {}
            for r in image_results:
                if r.get("extraction_mode") in ("ocr_degraded", "context_only"):
                    img_type = r["classification"]["type"]
                    type_counts[img_type] = type_counts.get(img_type, 0) + 1

            if type_counts:
                parts = [f"{t}({c}张)" for t, c in type_counts.items()]
                return (
                    f"当前模型不支持图片理解，已使用 OCR 替代。"
                    f"{'、'.join(parts)}的信息可能不完整，建议人工审阅。"
                )

        # 视觉模式下部分图片降级
        if self._context_only_count > 0:
            return (
                f"视觉模式下有 {self._context_only_count} 张图片处理失败，"
                "已降级为纯文本模式。建议人工审阅这些图片。"
            )

        return None

    def _build_aggregate_derived(self, image_results: List[dict]) -> dict:
        """聚合所有图片的 derived_* 数据"""
        all_features = []
        all_test_points = []
        all_risks = []
        all_questions = []

        for r in image_results:
            if r["processing_status"] in (STATUS_SUCCESS, STATUS_SUCCESS_DEGRADED):
                all_features.extend(r.get("derived_features", []))
                all_test_points.extend(r.get("derived_test_points", []))
                all_risks.extend(r.get("derived_risks", []))
                all_questions.extend(r.get("derived_questions", []))

        return {
            "total_derived_features": len(all_features),
            "total_derived_test_points": len(all_test_points),
            "total_derived_risks": len(all_risks),
            "total_derived_questions": len(all_questions),
            "derived_features": all_features,
            "derived_test_points": all_test_points,
            "derived_risks": all_risks,
            "derived_questions": all_questions,
        }

    def _build_coverage_matrix(self, image_results: List[dict]) -> dict:
        """构建图片类型覆盖矩阵"""
        matrix = {}
        for r in image_results:
            img_type = r["classification"]["type"]
            if img_type not in matrix:
                matrix[img_type] = {
                    "count": 0,
                    "processed": 0,
                    "skipped": 0,
                    "failed": 0,
                }
            matrix[img_type]["count"] += 1
            status = r["processing_status"]
            if status in (STATUS_SUCCESS, STATUS_SUCCESS_DEGRADED):
                matrix[img_type]["processed"] += 1
            elif "skipped" in status:
                matrix[img_type]["skipped"] += 1
            else:
                matrix[img_type]["failed"] += 1
        return matrix


# ============================================================
# T3-04：分类纠偏反馈机制
# ============================================================

# T3-04: 支持的反馈类型
FEEDBACK_TYPES = {
    "classification_error",   # 分类纠偏
    "ocr_inaccuracy",         # OCR 不准确
    "context_insufficient",   # 上下文不足
    "extraction_missing",     # 提取遗漏
}


def record_classification_feedback(
    image_id: str,
    original_type: str,
    corrected_type: str,
    context_keywords: List[str],
    feedback_type: str = "classification_error",
    doc_file: str = "",
    original_output: dict = None,
) -> dict:
    """
    T3-04：记录分类纠偏反馈，写入 experience_pool.json。

    Args:
        image_id: 图片 ID
        original_type: 原始分类类型
        corrected_type: 纠正后的类型
        context_keywords: 上下文关键词列表（用于后续匹配）
        feedback_type: 反馈类型，默认 classification_error
        doc_file: 文档文件名（可选）
        original_output: 原始 PX 输出（可选）

    Returns:
        {
            "success": bool,
            "feedback_id": str,
            "message": str
        }
    """
    # 参数校验
    if feedback_type not in FEEDBACK_TYPES:
        return {
            "success": False,
            "feedback_id": "",
            "message": f"不支持的反馈类型: {feedback_type}，"
                       f"支持: {', '.join(FEEDBACK_TYPES)}"
        }

    if not image_id:
        return {
            "success": False,
            "feedback_id": "",
            "message": "image_id 不能为空"
        }

    # 读取经验池
    pool_path = _EXPERIENCE_POOL_PATH
    # I-FIX-16: 读取失败时自动回退到 .bak 文件
    bak_path = pool_path + ".bak"
    try:
        if os.path.exists(pool_path):
            with open(pool_path, 'r', encoding='utf-8') as f:
                pool = json.load(f)
        else:
            pool = {
                "version": "1.0.0",
                "updated": "",
                "feedback_entries": [],
                "correction_stats": {
                    "total_corrections": 0,
                    "by_type": {
                        "classification_error": 0,
                        "ocr_inaccuracy": 0,
                        "context_insufficient": 0,
                        "extraction_missing": 0,
                    }
                },
                "model_capability_adjustments": [],
                "last_review_date": None,
            }
    except json.JSONDecodeError:
        # I-FIX-16: JSON解析失败，尝试读取 .bak
        if os.path.exists(bak_path):
            try:
                with open(bak_path, 'r', encoding='utf-8') as f:
                    pool = json.load(f)
            except (json.JSONDecodeError, IOError):
                return {
                    "success": False,
                    "feedback_id": "",
                    "message": f"读取经验池失败：原文件和备份文件均损坏"
                }
        else:
            return {
                "success": False,
                "feedback_id": "",
                "message": f"读取经验池失败：JSON解析错误且无备份文件"
            }
    except IOError as e:
        return {
            "success": False,
            "feedback_id": "",
            "message": f"读取经验池失败: {e}"
        }

    # 生成反馈 ID
    from datetime import datetime
    now = datetime.now()
    existing_count = len(pool.get("feedback_entries", []))
    feedback_id = f"fb_{now.strftime('%Y%m%d')}_{existing_count + 1:03d}"

    # 构造反馈条目
    entry = {
        "id": feedback_id,
        "timestamp": now.isoformat(),
        "image_id": image_id,
        "doc_file": doc_file,
        "feedback_type": feedback_type,
        "original_type": original_type,
        "corrected_type": corrected_type,
        "context_keywords": [kw.lower() for kw in context_keywords if kw],
        "original_output": original_output or {},
        "user_correction": f"{original_type} -> {corrected_type}",
        "applied": True,  # 分类纠偏立即生效
        "applied_date": now.isoformat(),
    }

    # 追加到 feedback_entries
    if "feedback_entries" not in pool:
        pool["feedback_entries"] = []
    pool["feedback_entries"].append(entry)

    # 更新 correction_stats
    stats = pool.get("correction_stats", {})
    stats["total_corrections"] = stats.get("total_corrections", 0) + 1
    by_type = stats.get("by_type", {})
    by_type[feedback_type] = by_type.get(feedback_type, 0) + 1
    stats["by_type"] = by_type
    pool["correction_stats"] = stats

    # 更新时间戳
    pool["updated"] = now.strftime("%Y-%m-%d")

    # AB-05修复：原子写入经验池（tempfile + os.rename + 备份回退）
    try:
        os.makedirs(os.path.dirname(pool_path), exist_ok=True)
        # 备份旧文件
        bak_path = pool_path + ".bak"
        if os.path.exists(pool_path):
            try:
                import shutil
                shutil.copy2(pool_path, bak_path)
            except IOError:
                pass  # 备份失败不阻断写入
        # 原子写入：先写临时文件，再 rename
        dir_name = os.path.dirname(pool_path)
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', suffix='.json',
            dir=dir_name, delete=False
        ) as tmp_f:
            json.dump(pool, tmp_f, ensure_ascii=False, indent=2)
            tmp_path = tmp_f.name
        os.replace(tmp_path, pool_path)  # 原子操作
    except IOError as e:
        # 写入失败，尝试回退到备份
        if os.path.exists(bak_path):
            try:
                os.replace(bak_path, pool_path)
            except IOError:
                pass
        return {
            "success": False,
            "feedback_id": feedback_id,
            "message": f"写入经验池失败: {e}"
        }

    return {
        "success": True,
        "feedback_id": feedback_id,
        "message": f"反馈已记录，{feedback_type}: {original_type} -> {corrected_type}"
    }


# ============================================================
# 公共接口
# ============================================================

def understand_images(extraction_result: dict,
                      mode_config: dict,
                      model_caller: Callable = None,
                      task_id: str = "") -> dict:
    """
    图片理解的公共接口。

    Args:
        extraction_result: image_extract.py 的输出
        mode_config: determine_processing_mode() 的输出
        model_caller: 模型调用函数
        task_id: 任务 ID

    Returns:
        聚合输出 dict（§8.3 Schema）
    """
    active_mode = mode_config.get("active_mode", "context_only")
    model_capability = mode_config.get("model_capability", {})
    ocr_status = mode_config.get("ocr_status", {})
    model_id = model_capability.get("model_id", "")

    dispatcher = ImageUnderstandingDispatcher(
        active_mode=active_mode,
        model_id=model_id,
        model_capability=model_capability,
        ocr_status=ocr_status,
        model_caller=model_caller,
        task_id=task_id,
    )

    images = extraction_result.get("images", [])
    return dispatcher.process_images(images)


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="图片理解调度工具")
    parser.add_argument("extraction_json", help="image_extract.py 输出的 JSON 文件")
    # I-FIX-02: CLI入口限制模式，视觉模式需Agent在Python层面调用并传入model_caller
    parser.add_argument("--mode", default="context_only",
                        choices=["vision", "ocr", "context_only"],
                        help="处理模式（CLI仅支持ocr/context_only，vision需通过Python API调用并传入model_caller）")
    parser.add_argument("--model-id", default="", help="模型标识")
    parser.add_argument("--task-id", default="", help="任务 ID")
    parser.add_argument("--output", "-o", help="输出 JSON 路径")
    args = parser.parse_args()

    # I-FIX-02: CLI模式下vision会静默降级，给出明确提示
    if args.mode == "vision":
        print("⚠️ CLI模式下无法提供model_caller，视觉模式将自动降级为OCR/context_only。")
        print("   如需使用视觉模式，请在Python层面调用 understand_images() 并传入 model_caller。")

    # 加载抽取结果
    with open(args.extraction_json, 'r', encoding='utf-8') as f:
        extraction_result = json.load(f)

    # 构造模式配置
    mode_config = {
        "active_mode": args.mode,
        "model_capability": {"model_id": args.model_id},
        "ocr_status": None,
    }

    # 执行理解
    result = understand_images(
        extraction_result, mode_config,
        task_id=args.task_id
    )

    # 输出
    output_path = args.output or "px_understand_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"📊 图片理解完成:")
    print(f"  模式: {result['mode_summary']['active_mode']}")
    print(f"  总图片: {result['processing_summary']['total_images']}")
    print(f"  视觉处理: {result['mode_summary']['vision_count']}")
    print(f"  OCR 处理: {result['mode_summary']['ocr_count']}")
    print(f"  纯文本: {result['mode_summary']['context_only_count']}")
    print(f"  跳过: {result['mode_summary']['skipped_count']}")
    print(f"  结果: {output_path}")
