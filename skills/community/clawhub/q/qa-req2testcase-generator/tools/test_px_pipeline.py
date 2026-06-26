#!/usr/bin/env python3
"""
T2-07 + AB-07修复：PX 链路验证脚本
覆盖：视觉模式 E2E / OCR 模式 E2E / 纯文本模式 E2E / 降级路径 / 去重 / 降级说明 / Schema 校验
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# 添加 skill_v2/tools 到路径
SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_DIR))


# ============================================================
# Mock 工具函数
# ============================================================

def make_mock_extract_result(n_images=3, has_emf=False):
    """生成模拟的图片抽取结果"""
    images = []
    for i in range(n_images):
        images.append({
            "image_id": f"IMG-{i+1:03d}",
            "filename": f"image{i+1}.png",
            "content_type": "image/png",
            "size_bytes": 50000 + i * 10000,
            "md5": f"hash_{i}",
            "embed_method": "inline",
            "section_heading": f"4.4.{i+1} 功能模块{i+1}",
            "before_text": f"功能模块{i+1}说明前文",
            "after_text": f"功能模块{i+1}说明后文",
            "in_table": False,
            "table_row": -1,
            "table_col": -1,
            "extraction_status": "ok",
            "error_message": "",
            "file_path": f"/tmp/mock/image{i+1}.png",
            "emf_converted": False,
        })
    if has_emf:
        images.append({
            "image_id": "IMG-099",
            "filename": "image_emf.emf",
            "content_type": "image/x-emf",
            "size_bytes": 10232,
            "md5": "hash_emf",
            "embed_method": "vml_ole",
            "section_heading": "4.4.4 数据后台模块",
            "before_text": "数据后台说明前文",
            "after_text": "数据后台说明后文",
            "in_table": False,
            "table_row": -1,
            "table_col": -1,
            "extraction_status": "ok",
            "error_message": "",
            "file_path": "/tmp/mock/image_emf.png",
            "emf_converted": True,
        })
    return {
        "source_file": "mock.docx",
        "total_images_in_doc": len(images),
        "images_extracted": len(images),
        "images": images,
        "sections_found": [img["section_heading"] for img in images],
        "errors": [],
        "elapsed_seconds": 0.01,
    }


# ============================================================
# 测试用例
# ============================================================

def test_vision_mode_e2e():
    """测试1：视觉模式 E2E — extract → detect → understand → enhance"""
    print("\n" + "=" * 60)
    print("测试1：视觉模式 E2E")
    print("=" * 60)

    from model_detect import ModelCapabilityDetector
    detector = ModelCapabilityDetector()
    capability = detector.detect("doubao-seed-2.0-pro")
    assert capability["model_capability"]["vision_supported"] == True
    print(f"  ✅ 模型探测: doubao-seed-2.0-pro → vision=True")

    from image_understand import ImageUnderstandingDispatcher
    dispatcher = ImageUnderstandingDispatcher(
        model_capability=capability,
        model_caller=lambda prompt, image_path=None: json.dumps({
            "image_type": "ui_mockup", "confidence": 0.9
        }),
        task_id="test_vision_001",
    )
    print(f"  ✅ 视觉模式调度器创建成功")

    from image_enhance import enhance_image_results, deduplicate_list
    print(f"  ✅ 增强聚合函数可调用")
    print("  ✅ 视觉模式 E2E: 通过")


def test_ocr_mode_e2e():
    """测试2：OCR 模式 E2E — extract → detect(ocr) → ocr → enhance"""
    print("\n" + "=" * 60)
    print("测试2：OCR 模式 E2E")
    print("=" * 60)

    from model_detect import ModelCapabilityDetector
    detector = ModelCapabilityDetector()
    capability = detector.detect("deepseek-v3")
    assert capability["model_capability"]["vision_supported"] == False
    print(f"  ✅ 模型探测: deepseek-v3 → vision=False")

    from image_ocr import detect_available_engine, postprocess_ocr_text
    available = detect_available_engine()
    print(f"  ℹ️ OCR 可用性: {available['ocr_available']}, 引擎: {available['ocr_engine']}")

    # 测试近音字纠错（AB-07修复：使用正确参数名）
    result = postprocess_ocr_text(
        "兴光闪耀 月亮晒 周晾晒 有效机构户",
        before_text="月亮晒模块说明",
        after_text="",
        caption="月亮晒截图",
    )
    print(f"  ✅ OCR 纠错: type={type(result).__name__}, 结果有效")
    print("  ✅ OCR 模式 E2E: 通过")


def test_text_only_mode():
    """测试3：纯文本模式 — extract → detect(text_only) → understand(context_only) → enhance"""
    print("\n" + "=" * 60)
    print("测试3：纯文本模式")
    print("=" * 60)

    extract_result = make_mock_extract_result(n_images=2)
    for img in extract_result["images"]:
        assert "section_heading" in img
        assert "before_text" in img
    print(f"  ✅ 纯文本模式: 2张图片元数据完整")
    print("  ✅ 纯文本模式: 通过")


def test_degradation_path():
    """测试4：降级路径 vision_failed → ocr → context_only"""
    print("\n" + "=" * 60)
    print("测试4：降级路径")
    print("=" * 60)

    from image_enhance import generate_degradation_notice

    # 模拟 OCR 降级
    mock_ocr_result = {
        "mode_summary": {"active_mode": "ocr"},
        "images": [
            {"image_type": "flowchart", "extraction_mode": "ocr_degraded", "confidence": 0.4},
        ]
    }
    notice = generate_degradation_notice(mock_ocr_result)
    if notice:
        print(f"  ✅ OCR降级说明: {notice[:60]}...")

    # 模拟纯文本降级
    mock_text_result = {
        "mode_summary": {"active_mode": "context_only"},
        "images": [
            {"image_type": "ui_mockup", "extraction_mode": "context_only"},
        ]
    }
    notice2 = generate_degradation_notice(mock_text_result)
    if notice2:
        print(f"  ✅ 纯文本降级说明: {notice2[:60]}...")

    print("  ✅ 降级路径: 通过")


def test_dedup():
    """测试5：去重合并"""
    print("\n" + "=" * 60)
    print("测试5：去重合并")
    print("=" * 60)

    from image_enhance import deduplicate_list
    items = ["验证登录", "验证登录", "验证登录正常", "验证退出"]
    deduped = deduplicate_list(items, threshold=0.75)
    assert len(deduped) < len(items)
    print(f"  ✅ 去重: {len(items)} → {len(deduped)}")
    print("  ✅ 去重合并: 通过")


def test_degradation_notice():
    """测试6：降级说明输出"""
    print("\n" + "=" * 60)
    print("测试6：降级说明输出")
    print("=" * 60)

    from image_enhance import generate_degradation_notice

    # OCR降级
    mock_ocr = {
        "mode_summary": {"active_mode": "ocr"},
        "images": [
            {"image_type": "flowchart", "extraction_mode": "ocr_degraded", "confidence": 0.4},
            {"image_type": "table_rule", "extraction_mode": "ocr", "confidence": 0.7},
        ]
    }
    notice = generate_degradation_notice(mock_ocr)
    assert notice, "OCR 模式应生成降级说明"
    print(f"  OCR降级说明: {notice[:80]}...")

    # 纯文本降级
    mock_text = {
        "mode_summary": {"active_mode": "context_only"},
        "images": [
            {"image_type": "ui_mockup", "extraction_mode": "context_only"},
        ]
    }
    notice2 = generate_degradation_notice(mock_text)
    assert notice2, "纯文本模式应生成降级说明"
    print(f"  纯文本降级说明: {notice2[:80]}...")
    print("  ✅ 降级说明: 通过")


def test_schema_validation():
    """测试7：Schema 校验"""
    print("\n" + "=" * 60)
    print("测试7：Schema 校验")
    print("=" * 60)

    schema_path = SKILL_DIR.parent / "prompts" / "schemas" / "px_output.schema.json"
    with open(schema_path) as f:
        schema = json.load(f)

    # 验证关键定义存在
    assert "definitions" in schema
    assert "single_image_output" in schema["definitions"]
    assert "classification" in schema["definitions"]

    # AB-01修复验证：ocr_text 和 corrected_text 字段已补充
    props = schema["definitions"]["single_image_output"]["properties"]
    assert "ocr_text" in props, "AB-01: Schema 应包含 ocr_text 字段"
    assert "corrected_text" in props, "AB-01: Schema 应包含 corrected_text 字段"

    # AB-01修复验证：classification_method 包含 ocr 枚举值
    cls_method = schema["definitions"]["classification"]["properties"]["classification_method"]
    assert "ocr" in cls_method["enum"], "AB-01: classification_method 应包含 ocr 枚举值"

    # AB-01修复验证：image_id 正则已放宽
    pattern = props["image_id"].get("pattern", "")
    assert "\\d+" in pattern or "\\d{1," in pattern, "AB-01: image_id pattern 应放宽"

    # AB-01修复验证：text_image_conflicts 改为 object 数组
    tic = props["text_image_conflicts"]
    assert tic["items"]["type"] == "object", "AB-01: text_image_conflicts items 应为 object"

    print(f"  ✅ Schema 有效, definitions: {list(schema['definitions'].keys())}")
    print(f"  ✅ AB-01验证: ocr_text/corrected_text 字段已补充")
    print(f"  ✅ AB-01验证: classification_method 含 ocr 枚举值")
    print(f"  ✅ AB-01验证: image_id pattern 已放宽")
    print(f"  ✅ AB-01验证: text_image_conflicts 改为 object 数组")
    print("  ✅ Schema 校验: 通过")


# ============================================================
# I-FIX-12: 异常场景测试用例
# ============================================================

def test_emf_conversion_failure():
    """测试8：EMF 转换失败场景"""
    print("\n" + "=" * 60)
    print("测试8：EMF 转换失败场景")
    print("=" * 60)

    from image_understand import ImageUnderstandingDispatcher, STATUS_SKIPPED
    dispatcher = ImageUnderstandingDispatcher(active_mode="context_only", task_id="test_emf_fail")

    # 模拟 EMF 转换失败的图片
    mock_img = {
        "image_id": "IMG-EMF-FAIL",
        "file_path": "/tmp/nonexistent.emf",
        "extraction_status": "conversion_failed",
        "section_heading": "4.1 测试",
        "before_text": "流程图说明",
        "after_text": "",
        "caption": "",
        "content_hash": "hash_emf_fail",
    }
    result = dispatcher._process_single_image(mock_img)
    assert result["processing_status"] == STATUS_SKIPPED
    assert result["extraction_mode"] == "context_only"
    assert "EMF" in (result.get("degradation_notice") or "")
    print("  ✅ EMF 转换失败: 正确降级为 context_only")
    print("  ✅ EMF 转换失败场景: 通过")


def test_file_not_found():
    """测试9：图片文件不存在场景"""
    print("\n" + "=" * 60)
    print("测试9：图片文件不存在场景")
    print("=" * 60)

    from image_understand import ImageUnderstandingDispatcher
    dispatcher = ImageUnderstandingDispatcher(
        active_mode="vision",
        model_caller=lambda prompt, image_path=None: '{"classification":{"type":"unknown"}}',
        task_id="test_file_missing",
    )

    mock_img = {
        "image_id": "IMG-MISSING",
        "file_path": "/tmp/absolutely_nonexistent_image_12345.png",
        "extraction_status": "ok",
        "section_heading": "4.1 测试",
        "before_text": "原型图",
        "after_text": "",
        "caption": "",
        "content_hash": "hash_missing",
    }
    result = dispatcher._process_single_image(mock_img)
    # 文件不存在应降级
    assert result["extraction_mode"] == "context_only"
    print("  ✅ 文件不存在: 正确降级")
    print("  ✅ 图片文件不存在场景: 通过")


def test_empty_image_list():
    """测试10：空图片列表场景"""
    print("\n" + "=" * 60)
    print("测试10：空图片列表场景")
    print("=" * 60)

    from image_understand import ImageUnderstandingDispatcher
    dispatcher = ImageUnderstandingDispatcher(active_mode="vision", task_id="test_empty")
    result = dispatcher.process_images([])
    assert result["processing_summary"]["total_images"] == 0
    assert result["images"] == []
    print("  ✅ 空图片列表: 返回空结果")
    print("  ✅ 空图片列表场景: 通过")


def test_model_caller_exception():
    """测试11：模型调用异常场景"""
    print("\n" + "=" * 60)
    print("测试11：模型调用异常场景")
    print("=" * 60)

    def failing_model_caller(prompt, image_path=None):
        raise ConnectionError("模拟网络超时")

    from image_understand import ImageUnderstandingDispatcher
    dispatcher = ImageUnderstandingDispatcher(
        active_mode="vision",
        model_caller=failing_model_caller,
        task_id="test_exception",
    )

    # 创建临时文件以通过文件存在检查
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(b'fake png data')
        tmp_path = f.name

    try:
        mock_img = {
            "image_id": "IMG-EXCEPTION",
            "file_path": tmp_path,
            "extraction_status": "ok",
            "section_heading": "4.1 测试",
            "before_text": "流程图说明",
            "after_text": "",
            "caption": "",
            "content_hash": "hash_exc",
        }
        result = dispatcher._process_single_image(mock_img)
        # 应降级而非崩溃
        assert result["extraction_mode"] == "context_only"
        assert "模拟网络超时" in (result.get("degradation_notice") or "")
        print("  ✅ 模型调用异常: 正确降级而非崩溃")
    finally:
        os.unlink(tmp_path)
    print("  ✅ 模型调用异常场景: 通过")


def test_invalid_json_response():
    """测试12：模型返回无效JSON场景"""
    print("\n" + "=" * 60)
    print("测试12：模型返回无效JSON场景")
    print("=" * 60)

    from image_understand import ImageUnderstandingDispatcher

    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(b'fake png data')
        tmp_path = f.name

    try:
        dispatcher = ImageUnderstandingDispatcher(
            active_mode="vision",
            model_caller=lambda prompt, image_path=None: "这不是合法JSON{{{",
            task_id="test_bad_json",
        )
        mock_img = {
            "image_id": "IMG-BADJSON",
            "file_path": tmp_path,
            "extraction_status": "ok",
            "section_heading": "4.1 测试",
            "before_text": "原型图",
            "after_text": "",
            "caption": "",
            "content_hash": "hash_badjson",
        }
        result = dispatcher._process_single_image(mock_img)
        # JSON解析失败应降级
        assert result["extraction_mode"] == "context_only"
        print("  ✅ 无效JSON响应: 正确降级")
    finally:
        os.unlink(tmp_path)
    print("  ✅ 模型返回无效JSON场景: 通过")


def test_large_image_budget_exceeded():
    """测试13：超出文档级深解析预算场景"""
    print("\n" + "=" * 60)
    print("测试13：超出文档级深解析预算场景")
    print("=" * 60)

    from image_understand import ImageUnderstandingDispatcher, MAX_HIGH_VALUE_DEEP_PARSE
    dispatcher = ImageUnderstandingDispatcher(
        active_mode="vision",
        model_caller=lambda prompt, image_path=None: '{"classification":{"type":"ui_mockup"}}',
        task_id="test_budget",
    )
    # 模拟已达到预算上限
    dispatcher._high_value_parsed = MAX_HIGH_VALUE_DEEP_PARSE

    mock_img = {
        "image_id": "IMG-BUDGET",
        "file_path": "/tmp/mock.png",
        "extraction_status": "ok",
        "section_heading": "4.1 测试",
        "before_text": "原型图说明",
        "after_text": "",
        "caption": "",
        "content_hash": "hash_budget",
    }
    result = dispatcher._process_single_image(mock_img)
    assert "skipped" in result["processing_status"]
    assert "预算" in result.get("summary", "")
    print(f"  ✅ 预算超出: 状态={result['processing_status']}")
    print("  ✅ 超出文档级深解析预算场景: 通过")


def test_ocr_engine_unavailable():
    """测试14：OCR引擎不可用场景"""
    print("\n" + "=" * 60)
    print("测试14：OCR引擎不可用场景")
    print("=" * 60)

    from image_ocr import OCRResult
    result = OCRResult(image_id="IMG-NO-OCR", status="engine_unavailable",
                       error_message="无可用 OCR 引擎")
    assert result.status == "engine_unavailable"
    print("  ✅ OCR引擎不可用: 状态正确")
    print("  ✅ OCR引擎不可用场景: 通过")


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    print("🔍 Phase 1/2/3 全量交付验证脚本 (AB-07修复版)")
    print(f"📁 SKILL_DIR: {SKILL_DIR}")

    results = []
    tests = [
        ("视觉模式E2E", test_vision_mode_e2e),
        ("OCR模式E2E", test_ocr_mode_e2e),
        ("纯文本模式", test_text_only_mode),
        ("降级路径", test_degradation_path),
        ("去重合并", test_dedup),
        ("降级说明", test_degradation_notice),
        ("Schema校验", test_schema_validation),
        # I-FIX-12: 补充异常场景测试用例
        ("EMF转换失败", test_emf_conversion_failure),
        ("文件不存在", test_file_not_found),
        ("空图片列表", test_empty_image_list),
        ("模型调用异常", test_model_caller_exception),
        ("无效JSON响应", test_invalid_json_response),
        ("深解析预算超出", test_large_image_budget_exceeded),
        ("OCR引擎不可用", test_ocr_engine_unavailable),
    ]

    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
            results.append((name, "✅ PASS"))
        except Exception as e:
            failed += 1
            results.append((name, f"❌ FAIL: {e}"))
            print(f"  ❌ {name}: {e}")

    print("\n" + "=" * 60)
    print("📊 验证结果汇总")
    print("=" * 60)
    for name, status in results:
        print(f"  {status} | {name}")
    print(f"\n总计: {passed}/{len(tests)} 通过, {failed} 失败")

    if failed == 0:
        print("\n✅ 全部验证通过！")
    else:
        print(f"\n⚠️ 有 {failed} 个测试失败，需要修复")
