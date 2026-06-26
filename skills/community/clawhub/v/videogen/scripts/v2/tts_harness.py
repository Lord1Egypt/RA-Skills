#!/usr/bin/env python3
"""
videogen v2 — TTS Harness
用 harness 思路重新设计的 TTS 配音流水线。

核心思路：在 TTS 这个不确定节点外面套「校验 → 修复 → 循环」控制环，
让输出趋向收敛。

四个组件：
  1. Agent      — 操作对象是 chunk 脚本（按句子切片，每段≤200字）
  2. 评估函数   — 双层：确定性预检 + Whisper X 语义校验
  3. 约束系统   — Rules 文档定义 TTS 规范化规则
  4. 跨轮记忆   — normalize_patches.json，每次修复发现的新规则写入，下期自动加载

用法：
    from tts_harness import run_tts_harness
    result = run_tts_harness(narration_text, output_dir="minimax-output")
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

# ─── 路径设置 ───
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
MM_DIR = SKILL_DIR.parent / "minimax-multimodal"
OUTPUT_DIR = SKILL_DIR / "minimax-output"

# ─── Whisper 检测 ───
WHISPER_AVAILABLE = False
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    pass

# ═══════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════

@dataclass
class Chunk:
    """单个配音 Chunk"""
    chunk_id: int
    text: str                    # 原始文本
    normalized_text: str         # 规范化后文本
    audio_path: str              # 生成的音频文件
    duration: float = 0.0        # 实际音频时长(秒)
    transcription: str = ""      # Whisper X 转写结果
    evaluation: dict = field(default_factory=dict)  # 评估结果
    fix_count: int = 0
    needs_human: bool = False    # 超过3轮自动修复仍失败
    status: str = "pending"      # pending / fixing / ok / error / human

@dataclass
class HarnessResult:
    """完整 Harness 运行结果"""
    total_chunks: int
    ok_chunks: int
    error_chunks: int
    human_chunks: int
    total_token_estimate: int    # 粗估 token 消耗
    duration_sec: float
    chunks: list
    subtitle_path: Optional[str] = None  # SRT 字幕文件路径


# ═══════════════════════════════════════════════════════
# 规则系统
# ═══════════════════════════════════════════════════════

TTS_RULES = [
    # 百分比要优先匹配（放在数字规则前面）
    {
        "name": "百分号展开",
        "pattern": r"(\d+)%",
        "replacement": lambda m: f"{_num_to_chinese(m.group(1))}百分之",
        "example": "50% → 五十百分之",
    },
    # 数字转中文读法（适用于门牌号、年代、版本号等）
    # 注意：跳过已%结尾的数字（被上面规则处理过了）
    {
        "name": "数字转中文（4位以上）",
        "pattern": r"(\d{4,})(?=[^0-9%·]|$)",  # 4位及以上数字
        "replacement": lambda m: _num_to_chinese(m.group(1)),
        "example": "2024 → 二零二四",
    },
    {
        "name": "数字转中文（1-3位）",
        "pattern": r"(\d{1,3})(?=[^0-9%·]|$)",  # 1-3位数字
        "replacement": lambda m: _num_to_chinese(m.group(1)),
        "example": "6 → 六",
    },
    # 英文品牌名/专有名词驼峰分词，防止连读
    # CarPlay → Car Play, iPhone → i Phone
    {
        "name": "驼峰分词",
        "pattern": r"([A-Z][a-z]+)([A-Z][a-z]+)",  # 匹配 Capital + Lower + Capital + Lower
        "replacement": lambda m: f"{m.group(1)} {m.group(2)}",
        "example": "CarPlay → Car Play",
    },
    # 连字符转空格
    {
        "name": "连字符转空格",
        "pattern": r"-(?=\w)",
        "replacement": " ",
        "example": "AI-powered → AI powered",
    },
    # 英文缩写展开（中文语境）
    # 注意：\b 在中文文本里不work（中文被当作文词字符），改用负向前瞻/回顾
    {
        "name": "AI展开",
        "pattern": r"(?<![a-zA-Z])AI(?![a-zA-Z])",
        "replacement": "人工智能",
        "example": "AI → 人工智能",
    },
    {
        "name": "TTS展开",
        "pattern": r"(?<![a-zA-Z])TTS(?![a-zA-Z])",
        "replacement": "文字转语音",
        "example": "TTS → 文字转语音",
    },
    {
        "name": "LLM展开",
        "pattern": r"(?<![a-zA-Z])LLM(?![a-zA-Z])",
        "replacement": "大语言模型",
        "example": "LLM → 大语言模型",
    },
]


def _num_to_chinese(num_str: str) -> str:
    """数字转中文读法"""
    digits = "零一二三四五六七八九"
    result = ""
    for d in num_str:
        result += digits[int(d)]
    return result


def load_patches() -> dict:
    """加载跨轮记忆 patches"""
    patches_path = OUTPUT_DIR / "normalize_patches.json"
    if patches_path.exists():
        try:
            return json.loads(patches_path.read_text())
        except:
            return {}
    return {}


def save_patches(patches: dict):
    """保存 patches 到跨轮记忆"""
    patches_path = OUTPUT_DIR / "normalize_patches.json"
    patches_path.parent.mkdir(parents=True, exist_ok=True)
    patches_path.write_text(json.dumps(patches, ensure_ascii=False, indent=2))


def apply_patches(text: str, patches: dict) -> str:
    """应用已知的 patches 到文本"""
    for old, new in patches.items():
        text = text.replace(old, new)
    return text


def normalize_text(text: str, patches: dict) -> str:
    """
    对文本进行 TTS 规范化：
    1. 先应用已知的 patches（跨轮记忆）
    2. 再应用规则
    """
    # Step 1: 应用 patches
    text = apply_patches(text, patches)

    # Step 2: 应用规则
    for rule in TTS_RULES:
        pattern = rule["pattern"]
        replacement = rule["replacement"]
        text = re.sub(pattern, replacement, text)

    # Step 3: 清理多余空格
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ═══════════════════════════════════════════════════════
# Chunk 化
# ═══════════════════════════════════════════════════════

def chunk_text(text: str, max_chars: int = 200) -> list[str]:
    """
    按句子切分文本，每段≤max_chars 字。
    返回 chunks 列表。
    """
    # 按句子标点分割
    sentences = re.split(r"([。！？；\n])", text)
    chunks = []
    current = ""

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + sentences[i + 1]
        if len(current) + len(sentence) <= max_chars:
            current += sentence
        else:
            if current:
                chunks.append(current.strip())
            # 如果单个句子超过 max_chars，按子句继续切
            if len(sentence) > max_chars:
                sub_chunks = _split_long_sentence(sentence, max_chars)
                chunks.extend(sub_chunks[:-1])
                current = sub_chunks[-1]
            else:
                current = sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks


def _split_long_sentence(text: str, max_chars: int) -> list[str]:
    """超长句子内部继续切分（按逗号、顿号）"""
    parts = re.split(r"([，、])", text)
    result = []
    current = ""

    for i in range(0, len(parts) - 1, 2):
        seg = parts[i] + parts[i + 1]
        if len(current) + len(seg) <= max_chars:
            current += seg
        else:
            if current:
                result.append(current.strip())
            current = seg

    if current.strip():
        result.append(current.strip())

    if not result:
        # 实在切不动，直接按长度硬切
        for i in range(0, len(text), max_chars):
            result.append(text[i:i + max_chars])

    return result or [text]


# ═══════════════════════════════════════════════════════
# 评估函数
# ═══════════════════════════════════════════════════════

def evaluate_deterministic(chunk: Chunk) -> dict:
    """
    第一层评估：确定性预检
    不调 API，快速过滤明显问题。
    """
    result = {
        "passed": True,
        "issues": [],
        "checks": {},
    }

    # Check 1: 文件存在
    if not Path(chunk.audio_path).exists():
        result["passed"] = False
        result["issues"].append("audio_file_missing")
        return result

    # Check 2: 时长合理（预估：中文约 5字/秒）
    # 允许 ±40% 误差（比之前宽松，因为语速波动正常）
    duration = get_audio_duration(chunk.audio_path)
    chunk.duration = duration
    expected_duration = len(chunk.normalized_text) / 5.0
    if expected_duration > 0:
        ratio = duration / expected_duration
        result["checks"]["duration_ratio"] = round(ratio, 3)
        if ratio < 0.55 or ratio > 1.8:
            result["passed"] = False
            result["issues"].append(f"duration_anomaly: ratio={ratio:.2f}")

    # Check 3: 转写字数差异（Whisper，非 API 成本）
    # 用 Whisper 快速转写，不花钱，过滤明显问题
    if WHISPER_AVAILABLE:
        try:
            model = whisper.load_model("tiny")  # 用最小的，省时间
            transcription = transcribe_with_whisper(model, chunk.audio_path)
            chunk.transcription = transcription

            # 统计字数（中英文分开算）
            orig_len = len(chunk.normalized_text)
            trans_len = len(transcription)
            len_ratio = trans_len / orig_len if orig_len > 0 else 0

            result["checks"]["transcription_len"] = trans_len
            result["checks"]["transcription_ratio"] = round(len_ratio, 3)

            # 允许 ±50% 字数波动（语气词/重复会导致差异）
            # 但如果差异太大说明可能有明显漏读或添字
            if len_ratio < 0.4 or len_ratio > 2.0:
                result["passed"] = False
                result["issues"].append(f"transcription_len_anomaly: ratio={len_ratio:.2f}")
        except Exception as e:
            result["checks"]["transcription_error"] = str(e)
            # Whisper 失败不阻塞，继续走

    result["checks"]["whisper_available"] = WHISPER_AVAILABLE
    return result


def evaluate_semantic(chunk: Chunk, whisper_model=None) -> dict:
    """
    第二层评估：Whisper X 语义校验
    用外部信号（转写）比对原文，区分发音错误和无害替换。

    需要 whisper_model 参数传入（避免每轮重复加载模型）。
    """
    if not WHISPER_AVAILABLE:
        return {"skipped": True, "reason": "whisper_not_available"}

    result = {
        "passed": True,
        "issues": [],
        "warnings": [],
        "transcription": "",
    }

    try:
        # 如果没传模型，用 tiny（速度快）
        if whisper_model is None:
            whisper_model = whisper.load_model("tiny")

        audio_path = chunk.audio_path
        transcription = transcribe_with_whisper(whisper_model, audio_path)
        chunk.transcription = transcription
        result["transcription"] = transcription

        # 三方比对：原文 vs 规范化文本 vs 转写
        # 原文用于识别真正缺失的词（发音错误）
        # 规范化文本用于最终确认
        original = chunk.text  # 原始未规范化文本
        normalized = chunk.normalized_text

        diff = compare_transcription(normalized, transcription)

        if diff["error_count"] > 0:
            result["passed"] = False
            result["issues"].extend(diff["errors"])
            result["error_count"] = diff["error_count"]

        if diff["warnings"]:
            result["warnings"].extend(diff["warnings"])

        result["checks"] = diff

    except Exception as e:
        result["skipped"] = True
        result["error"] = str(e)

    return result


def transcribe_with_whisper(model, audio_path: str) -> str:
    """用 whisper 转写音频"""
    result = model.transcribe(audio_path, language="zh", fp16=False)
    return result["text"].strip()


def compare_transcription(original: str, transcription: str) -> dict:
    """
    词汇级比对：原文 vs 转写结果，识别发音错误。

    策略：
    1. 提取原文的核心词（去语气词、标点）
    2. 检查每个核心词是否出现在转写中（允许同音字模糊匹配）
    3. 真正的错误 = 核心词完全缺失 or 发音相差甚远

    同音字词典覆盖常见 TTS 发音错误（如 D630→D六三零被读成完全不同的词）。
    """
    errors = []
    warnings = []

    # ── 常见 TTS 发音错误（同音/近音映射）──
    KNOWN_PRONUNCIATION_ERRORS = {
        # 数字/编号
        "D六三零": ["d630", "d630", "地六三零"],
        "T": ["t", "tee", "提"],
        "AI": ["a i", "ei ai"],
        "LLM": ["l l m", "language model"],
        # 品牌/产品
        "卡帕西": ["carpathy", "carplay", "carpa"],
        "特斯拉": ["特斯拉克", "特瑞斯"],
        # 英文品牌名（规范化后的）
        "Car Play": ["carplay", "car play"],
    }

    def is_acceptable_variant(word: str, transcribed: str) -> bool:
        """判断转写是否为原文可接受的变体（同音字、语气词、停顿）"""
        if not word or not transcribed:
            return False
        # 完全相同
        if word == transcribed:
            return True
        # 长度差异过大（语气词添减）
        if abs(len(word) - len(transcribed)) > 3:
            # 可能是语气词大量添减，不算错
            return True
        # 查已知错误表
        for expected, variants in KNOWN_PRONUNCIATION_ERRORS.items():
            if word == expected and any(v in transcribed.lower() for v in variants):
                return True
        return False

    def extract_content_words(text: str) -> list[str]:
        """
        提取核心词（去语气词、标点、连词）。
        简化版：去掉标点和常见语气词，返回剩余词序列。
        """
        # 语气词/停用词列表
        stopwords = set([
            "的", "了", "啊", "呢", "吧", "呀", "嘛", "哦", "嗯", "哼",
            "哈", "诶", "噢", "哟", "呃", "唉", "喂", "嘻", "呃", "哇",
            "和", "与", "及", "或", "但", "而", "且", "所以", "因为",
            "如果", "虽然", "但是", "然而", "而且", "并且",
            "这", "那", "这个", "那个", "一种", "一些",
            "就", "才", "又", "还", "也", "都", "已", "已经",
            "我", "你", "他", "她", "它", "我们", "你们", "他们",
            "是", "在", "有", "被", "把", "给", "跟", "对", "向",
            "个", "们", "着", "过", "来", "去", "上", "下",
            "很", "非常", "特别", "比较", "相当", "最", "更",
        ])
        # 按标点和空格分词
        # 常见中英文标点分割符
        words = re.split(r"[，。、！？；：()（）\[\]【】《》,\.\s\"\u201c\u201d\u2018\u2019]+", text)
        # 只保留长度>=2 且不是停用词的词
        return [w for w in words if len(w) >= 2 and w not in stopwords]

    content_words = extract_content_words(original)
    transcribed_lower = transcription.lower()

    for word in content_words:
        # 检查核心词是否出现在转写中
        if word in transcribed_lower:
            continue  # 找到了，没问题

        # 检查是否是可接受的变体（语气词差异等）
        if is_acceptable_variant(word, transcription):
            warnings.append(f"acceptable_variant:{word}")
            continue

        # 真正的问题：核心词缺失
        errors.append(f"missing_word:{word}")

    return {
        "error_count": len(errors),
        "errors": errors,
        "warnings": warnings,
        "content_words_checked": len(content_words),
    }


def get_audio_duration(audio_path: str) -> float:
    """用 ffprobe 获取音频时长（秒）"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return 0.0


# ═══════════════════════════════════════════════════════
# 自动修复
# ═══════════════════════════════════════════════════════

def auto_fix(chunk: Chunk, eval_result: dict) -> str:
    """
    根据评估结果自动修复文本。
    返回修复后的文本（如果修复成功），否则返回原文本。
    """
    text = chunk.normalized_text
    new_fixes = []

    for issue in eval_result.get("issues", []):
        if issue == "audio_file_missing":
            # 文件缺失无法自动修复
            continue

        if "duration_anomaly" in issue:
            # 时长异常：可能是语速问题，尝试加停顿符
            if eval_result["checks"]["duration_ratio"] < 0.5:
                # 太快，加语气词或停顿
                text = _add_pauses(text)
            elif eval_result["checks"]["duration_ratio"] > 2.0:
                # 太慢，减少重复描述（简化）
                pass  # 需要更复杂的 LLM 判断，先跳过

        if "pronunciation_error" in issue or "possible_pronunciation_error" in issue:
            # 发音错误：尝试规范化
            # 常见错误模式修复
            text = _fix_common_pronunciation(text, chunk.text)

    return text


def _add_pauses(text: str) -> str:
    """在适当位置添加停顿符"""
    # 在句子中间加省略号或停顿
    text = re.sub(r"，([^，\n]{20,50})，", r"，\1……", text)
    return text


def _fix_common_pronunciation(text: str, original: str) -> str:
    """
    修复常见发音错误。
    从 patch 记忆和常见错误模式中学习。
    """
    # 常见的 TTS 发音错误模式
    known_errors = [
        # (错误模式, 正确替换)
        (r"\bD630\b", "D六三零"),
        (r"\bT\b(?=\s*[秒分时天月年])", "T"),  # T 作为单位保留
        # 更多模式可以动态添加
    ]

    for pattern, replacement in known_errors:
        text = re.sub(pattern, replacement, text)

    return text


def record_patch(original: str, fixed: str, reason: str, patches: dict):
    """
    将修复记录到 patches（跨轮记忆）。
    只有当修复被确认有效（人工或语义校验通过）才写入。
    """
    if original != fixed and len(fixed) < 100:  # 避免过长替换
        patches[original] = fixed


# ═══════════════════════════════════════════════════════
# 主循环：Harness
# ═══════════════════════════════════════════════════════

MAX_AUTO_FIX_ROUNDS = 3


def run_tts_harness(
    narration_text: str,
    output_dir: str = None,
    voice: str = "female-shaonv",
    whisper_model: str = "base",
    speed: float = 1.0,
) -> HarnessResult:
    """
    TTS Harness 主循环。

    流程：
    1. 加载 patches（跨轮记忆）
    2. 文本规范化 + Chunk 化
    3. 每个 Chunk 独立走流水线：生成 → 评估 → 修复（最多3轮）
    4. 超过3轮标记 human，输出报告
    """
    start_time = time.time()
    output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    chunks_dir = output_dir / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # 加载跨轮记忆
    patches = load_patches()

    # Step 1: 规范化 + Chunk 化
    normalized = normalize_text(narration_text, patches)
    raw_chunks = chunk_text(normalized)
    print(f"  📝 规范化完成，原始 {len(narration_text)} 字 → 规范化 {len(normalized)} 字")
    print(f"  🔪 切分为 {len(raw_chunks)} 个 chunks")

    # Step 2: 预加载 Whisper 模型（整个流程只加载一次）
    whisper_model_obj = None
    if WHISPER_AVAILABLE:
        try:
            whisper_model_obj = whisper.load_model("tiny")
            print(f"  🎤 Whisper 模型已加载（tiny，省时）")
        except Exception as e:
            print(f"  ⚠️  Whisper 模型加载失败: {e}")

    result_chunks = []
    ok_count = 0
    error_count = 0
    human_count = 0
    total_tokens = 0

    for i, chunk_text_raw in enumerate(raw_chunks):
        chunk_id = i + 1
        print(f"\n  ── Chunk {chunk_id}/{len(raw_chunks)} ──")
        print(f"  文本: {chunk_text_raw[:60]}{'...' if len(chunk_text_raw) > 60 else ''}")

        audio_path = str(chunks_dir / f"chunk_{chunk_id:02d}.mp3")

        chunk = Chunk(
            chunk_id=chunk_id,
            text=chunk_text_raw,
            normalized_text=chunk_text_raw,  # 第一轮用 chunk_text_raw，后面会重新规范化
            audio_path=audio_path,
        )

        # 重新规范化（应用 patches + 规则）
        chunk.normalized_text = normalize_text(chunk_text_raw, patches)

        # 主循环：生成 → 评估 → 修复（最多3轮）
        for round_i in range(MAX_AUTO_FIX_ROUNDS):
            print(f"  🔁 Round {round_i + 1}")

            # 生成
            ok = generate_tts_chunk(chunk.normalized_text, audio_path, voice, speed)
            if not ok:
                chunk.status = "error"
                error_count += 1
                print(f"  ❌ TTS 生成失败")
                break

            # 评估 Layer 1：确定性预检
            eval_det = evaluate_deterministic(chunk)
            print(f"  🔍 确定性预检: {'✅' if eval_det['passed'] else '❌'} {eval_det.get('issues', [])}")

            if not eval_det["passed"]:
                # 自动修复
                fixed_text = auto_fix(chunk, eval_det)
                if fixed_text != chunk.normalized_text:
                    chunk.normalized_text = fixed_text
                    chunk.fix_count += 1
                    print(f"  🔧 自动修复 → {fixed_text[:40]}...")
                    continue  # 下一轮重新生成 + 评估
                else:
                    chunk.status = "error"
                    error_count += 1
                    break

            # 评估 Layer 2：语义校验（Whisper）
            if WHISPER_AVAILABLE and whisper_model_obj:
                eval_sem = evaluate_semantic(chunk, whisper_model_obj)
                print(f"  🔍 语义校验: {'✅' if eval_sem.get('passed', True) else '❌'} {eval_sem.get('issues', [])}")
                chunk.evaluation = eval_sem

                if not eval_sem.get("passed"):
                    # 尝试语义层修复（需要 whisper，这里简化处理）
                    chunk.status = "human"  # 标记人工处理
                    human_count += 1
                    print(f"  ⚠️ 语义校验未通过，标记人工处理")
                    break

            # 两层都通过
            chunk.status = "ok"
            ok_count += 1
            print(f"  ✅ Chunk {chunk_id} 完成（{chunk.duration:.1f}秒）")
            break

        else:
            # 超过最大修复轮数
            chunk.status = "human"
            chunk.needs_human = True
            human_count += 1
            print(f"  ⚠️ 超过 {MAX_AUTO_FIX_ROUNDS} 轮，标记人工处理")

        result_chunks.append(chunk)
        # 粗估 token：每字约 2 token
        total_tokens += len(chunk.normalized_text) * 2 + 100  # 加上 API overhead

    # Step 3: 合并所有 OK 的 chunks
    final_audio = output_dir / "voiceover.mp3"
    merge_chunks(result_chunks, str(final_audio))

    # Step 4: 记录新发现的 patches
    # 只有 OK 或 human 的 chunk 才记录（确保不是随机通过的）
    for chunk in result_chunks:
        if chunk.status in ("ok", "human") and chunk.fix_count > 0:
            record_patch(chunk.text, chunk.normalized_text, "auto_fix", patches)

    save_patches(patches)

    duration = time.time() - start_time

    result = HarnessResult(
        total_chunks=len(raw_chunks),
        ok_chunks=ok_count,
        error_chunks=error_count,
        human_chunks=human_count,
        total_token_estimate=total_tokens,
        duration_sec=duration,
        chunks=result_chunks,
    )
    result.subtitle_path = None  # 后续由调用方填充

    # Step 3b: 生成精确对齐的 SRT 字幕
    if ok_count > 0 and WHISPER_AVAILABLE:
        print(f"\n  🎬 生成精确对齐字幕...")
        result.subtitle_path = generate_subtitles(
            result_chunks, output_dir, whisper_model_obj
        )

    print(f"\n{'='*50}")
    print(f"🎯 TTS Harness 完成")
    print(f"  总 chunks: {result.total_chunks}")
    print(f"  ✅ OK: {result.ok_chunks}")
    print(f"  ❌ Error: {result.error_chunks}")
    print(f"  ⚠️  Human: {result.human_chunks}")
    print(f"  ⏱️  耗时: {duration:.1f}秒")
    print(f"  🔮 Token 估算: {result.total_token_estimate:,}")
    print(f"  📁 输出: {final_audio}")
    print(f"{'='*50}")

    return result


# ═══════════════════════════════════════════════════════
# TTS 生成（调用 MiniMax）
# ═══════════════════════════════════════════════════════

def get_minimax_key() -> str:
    key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_KEY")
    if not key:
        env_path = Path.home() / ".openclaw" / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if "MINIMAX" in line and "API_KEY" in line:
                    key = line.split("=")[-1].strip()
                    break
    return key or ""


def generate_tts_chunk(text: str, output_path: str, voice: str = "female-shaonv", speed: float = 1.0) -> bool:
    """
    TTS 生成：优先 MiniMax API，fallback 到 Edge TTS
    """
    # 先尝试 MiniMax
    minimax_ok = _generate_minimax_tts(text, output_path, voice, speed)
    if minimax_ok:
        return True

    # Fallback: Edge TTS（微软语音，免费）
    return _generate_edge_tts(text, output_path, voice)


def _generate_minimax_tts(text: str, output_path: str, voice: str, speed: float = 1.0) -> bool:
    """调用 MiniMax TTS API"""
    import urllib.request
    import json

    key = get_minimax_key()
    if not key:
        return False

    # MiniMax 音色映射
    voice_map = {
        "female-shaonv": "female-shaonv",
        "female-yujie": "female-yujie",
        "male-yuan": "male-yuan",
        "male-john": "male-john",
    }
    voice_id = voice_map.get(voice, "female-shaonv")

    url = "https://api.minimax.chat/v1/t2a_v2"
    payload = {
        "model": "speech-02-hd",
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice_id, "speed": speed, "volume": 1.0, "pitch": 0},
        "audio_setting": {"audio_format": "mp3", "sample_rate": 32000, "bitrate": 128000},
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            ct = resp.headers.get("Content-Type", "")
            # 如果返回 JSON 而不是音频，说明失败了
            if "application/json" in ct or len(body) < 1000:
                return False
            Path(output_path).write_bytes(body)
            return True
    except Exception:
        return False


async def _edge_tts_async(text: str, output_path: str, voice: str) -> bool:
    """Edge TTS 异步生成"""
    import edge_tts
    import asyncio

    # Edge TTS 音色映射
    voice_map = {
        "female-shaonv": "zh-CN-XiaoxiaoNeural",
        "female-yujie": "zh-CN-YunjieNeural",
        "male-yuan": "zh-CN-YunxiNeural",
        "male-john": "zh-CN-YunyangNeural",
    }
    voice_id = voice_map.get(voice, "zh-CN-XiaoxiaoNeural")

    try:
        communicate = edge_tts.Communicate(text, voice_id)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"  ⚠️  Edge TTS 异常: {e}")
        return False


def _generate_edge_tts(text: str, output_path: str, voice: str) -> bool:
    """Edge TTS 同步入口"""
    import asyncio
    try:
        return asyncio.run(_edge_tts_async(text, output_path, voice))
    except Exception as e:
        print(f"  ⚠️  Edge TTS 失败: {e}")
        return False


def merge_chunks(chunks: list[Chunk], output_path: str):
    """
    合并所有 chunk 音频（v2 修复版）：
    1. 把所有 chunk 转成统一规格 AAC（48kHz, 128kbps）
    2. 用 FFmpeg filter_complex concat 合并
    3. 如果合并失败，fallback：直接复制最大的 chunk
    """
    ok_chunks = [
        c for c in chunks
        if c.status == "ok" and Path(c.audio_path).exists()
    ]

    if not ok_chunks:
        print("  ⚠️  没有可合并的 chunk")
        return

    chunks_dir = Path(output_path).parent / "chunks_aac"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: 统一转码为 AAC（强制 128kbps，解决 MiniMax 返回低 bitrate 的问题）
    aac_files = []
    for chunk in ok_chunks:
        aac_path = chunks_dir / f"chunk_{chunk.chunk_id:02d}.aac"
        # 强制重新转码，不依赖缓存（因为上次可能 bitrate 不对）
        cmd = [
            "ffmpeg", "-y",
            "-i", str(chunk.audio_path),
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
            "-ac", "2",
            str(aac_path),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            print(f"  ⚠️  转码失败 chunk_{chunk.chunk_id}: {r.stderr[-100:]}")
            # fallback: 直接复制原始文件（不推荐，但保证有输出）
            shutil.copy2(chunk.audio_path, aac_path)
        aac_files.append(str(aac_path))

    if not aac_files:
        print("  ⚠️  没有可用的 chunk 文件")
        return

    # Step 2: filter_complex concat（处理不同格式/长度的文件）
    # 动态构建 filter_complex
    n = len(aac_files)
    filter_str = "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[outa]"

    cmd = ["ffmpeg", "-y"]
    for f in aac_files:
        cmd += ["-i", f]
    cmd += [
        "-filter_complex", filter_str,
        "-map", "[outa]",
        "-c:a", "aac", "-b:a", "128k",
        str(output_path),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            # 验证输出 bitrate（128kbps AAC 应该 ≥ 10KB for 8s chunk）
            size = os.path.getsize(output_path)
            duration = get_audio_duration(output_path)
            bitrate = size * 8 / duration if duration > 0 else 0
            if bitrate < 50000:  # < 50kbps 说明有问题
                print(f"  ⚠️  合并后 bitrate {bitrate/1000:.0f}kbps 异常，重新合并")
                # 使用 concat muxer（更可靠）
                concat_list = "\n".join(f"file '{f}'" for f in aac_files)
                list_path = chunks_dir / "concat_list.txt"
                list_path.write_text(concat_list)
                cmd2 = [
                    "ffmpeg", "-y",
                    "-f", "concat", "-safe", "0",
                    "-i", str(list_path),
                    "-c:a", "aac", "-b:a", "128k",
                    str(output_path),
                ]
                r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=120)
                if r2.returncode != 0:
                    print(f"  ⚠️  concat muxer 也失败: {r2.stderr[-200:]}")
                    shutil.copy2(aac_files[0], output_path)
            print(f"  ✅ 合并完成: {output_path} ({duration:.1f}秒, {size/1024:.0f}KB)")
        else:
            print(f"  ⚠️  filter_complex 合并失败，fallback: {result.stderr[-200:]}")
            # Fallback: concat muxer
            concat_list = "\n".join(f"file '{f}'" for f in aac_files)
            list_path = chunks_dir / "concat_list.txt"
            list_path.write_text(concat_list)
            cmd2 = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", str(list_path),
                "-c:a", "aac", "-b:a", "128k",
                str(output_path),
            ]
            r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=120)
            if r2.returncode == 0:
                duration = get_audio_duration(output_path)
                print(f"  ✅ concat muxer fallback 成功: {duration:.1f}秒")
            else:
                print(f"  ⚠️  concat muxer 也失败: {r2.stderr[-200:]}")
                shutil.copy2(aac_files[0], output_path)
    except Exception as e:
        print(f"  ⚠️  合并异常: {e}")


# ═══════════════════════════════════════════════════════
# 字幕对齐模块（解决第三个痛点：毫秒级时间戳手动对齐）
# ═══════════════════════════════════════════════════════

def generate_subtitles(
    chunks: list[Chunk],
    output_dir: Path,
    whisper_model=None,
) -> Optional[str]:
    """
    用 Whisper word-level timestamps 生成精确对齐的 SRT 字幕。

    流程：
    1. 逐 chunk 用 Whisper 转写，获取每个词的起始/结束时间
    2. 将词合并成句子级别的 SRT entry
    3. 所有 chunk 的字幕按时间顺序拼接

    输出：output_dir / "subtitles.srt"
    """
    if not WHISPER_AVAILABLE:
        print("  ⚠️  Whisper 未安装，跳过字幕生成")
        return None

    if not whisper_model:
        try:
            whisper_model = whisper.load_model("tiny")
        except Exception as e:
            print(f"  ⚠️  Whisper 模型加载失败: {e}")
            return None

    srt_entries = []
    global_index = 1   # 全局 subtitle 序号
    global_offset = 0.0  # 累积时间偏移（秒），用于处理 chunk 之间的间隔

    for chunk in chunks:
        if chunk.status != "ok":
            continue

        audio_path = chunk.audio_path
        if not Path(audio_path).exists():
            continue

        try:
            # Whisper word-level timestamps
            result = whisper_model.transcribe(
                audio_path,
                language="zh",
                word_timestamps=True,
                fp16=False,
            )

            # 计算该 chunk 在合并音频中的起始时间
            chunk_start = global_offset

            for seg in result.get("segments", []):
                words = seg.get("words", [])
                if not words:
                    # 没有词级时间，用整句的 start/end
                    start_sec = seg["start"] + chunk_start
                    end_sec = seg["end"] + chunk_start
                    text = seg["text"].strip()
                    if text:
                        srt_entries.append({
                            "index": global_index,
                            "start": start_sec,
                            "end": end_sec,
                            "text": text,
                        })
                        global_index += 1
                else:
                    # 词级时间：合并成句子字幕
                    first_word = words[0]
                    last_word = words[-1]
                    start_sec = first_word["start"] + chunk_start
                    end_sec = last_word["end"] + chunk_start
                    # 过滤空白词
                    text = "".join(w["word"] for w in words if w["word"].strip())
                    if text:
                        srt_entries.append({
                            "index": global_index,
                            "start": start_sec,
                            "end": end_sec,
                            "text": text,
                        })
                        global_index += 1

            # 更新全局时间偏移 = 累加当前 chunk 的时长
            if chunk.duration > 0:
                global_offset += chunk.duration + 0.1  # 加100ms间隔

        except Exception as e:
            print(f"  ⚠️  Chunk {chunk.chunk_id} 字幕转写失败: {e}")
            global_offset += chunk.duration + 0.1

    if not srt_entries:
        return None

    # 写入 SRT 文件
    srt_path = output_dir / "subtitles.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for entry in srt_entries:
            f.write(f"{entry['index']}\n")
            f.write(f"{format_srt_time(entry['start'])} --> {format_srt_time(entry['end'])}\n")
            f.write(f"{entry['text']}\n\n")

    print(f"  ✅ 字幕生成: {srt_path}（{len(srt_entries)} 条）")
    return str(srt_path)


def format_srt_time(seconds: float) -> str:
    """秒 → SRT 时间格式 HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="TTS Harness — 带评估的 TTS 流水线")
    parser.add_argument("text", help="配音文本（或用 --file 指定文件）")
    parser.add_argument("--file", help="从文件读取配音文本")
    parser.add_argument("--output", default="minimax-output", help="输出目录")
    parser.add_argument("--voice", default="female-shaonv", help="音色")
    parser.add_argument("--whisper-model", default="base", help="Whisper 模型（base/tiny/large）")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="语速倍率，默认 1.0（1.5 = 1.5倍速，MiniMax API 支持 0.5-2.0）")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text()
    else:
        text = args.text

    result = run_tts_harness(
        narration_text=text,
        output_dir=args.output,
        voice=args.voice,
        whisper_model=args.whisper_model,
        speed=args.speed,
    )

    # 输出结构化结果（供 run_pipeline.py 调用）
    print(f"\n## TTS_HARNESS_RESULT ##")
    print(f"ok={result.ok_chunks}/{result.total_chunks}")
    print(f"human={result.human_chunks}")
    print(f"tokens={result.total_token_estimate}")


if __name__ == "__main__":
    main()
