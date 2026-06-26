#!/usr/bin/env python3
"""
SnowVoice TTS Skill - CLI 调用封装
处理自然语言到 snowvoice 命令的转换
"""

import subprocess
import os
import sys
import json
import re
from pathlib import Path


# ============ 路径发现 ============

def find_snowvoice_root():
    """自动发现 SnowVoice 安装路径"""
    candidates = [
        Path.home() / ".snowvoice-studio",
        Path.home() / "Desktop" / "personal" / "tts",
    ]
    for path in candidates:
        if (path / ".venv" / "bin" / "python").exists() and (path / "main.py").exists():
            return path
    return None


SNOWVOICE_ROOT = find_snowvoice_root()


def get_venv_python():
    if SNOWVOICE_ROOT is None:
        return None
    p = SNOWVOICE_ROOT / ".venv" / "bin" / "python"
    return str(p) if p.exists() else None


# ============ 环境检查 ============

def check_environment():
    """检查 SnowVoice 环境是否就绪"""
    if SNOWVOICE_ROOT is None or get_venv_python() is None:
        return {
            "ready": False,
            "message": "SnowVoice 未安装。请先运行: python3 scripts/init.py setup"
        }

    models_dir = SNOWVOICE_ROOT / "models"
    required = ["Base-1.7B", "VoiceDesign-1.7B"]
    missing = [m for m in required if not (models_dir / m / "model.safetensors").exists()]

    if missing:
        return {
            "ready": False,
            "message": f"缺少模型: {', '.join(missing)}。请运行: python3 scripts/init.py download-model {missing[0]}"
        }

    return {"ready": True, "message": "环境就绪"}


# ============ CLI 执行 ============

def run_snowvoice(args):
    """运行 snowvoice CLI 命令"""
    python = get_venv_python()
    if not python:
        return -1, "", "SnowVoice 未安装"

    cmd = [python, "-m", "cli.app"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(SNOWVOICE_ROOT),
            timeout=300,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "执行超时（5分钟）"
    except Exception as e:
        return -1, "", str(e)


# ============ 音色映射 ============
# 从 personas.json 的实际 key 到中文名

PERSONA_MAP = {
    # 通用名 → persona key
    "顾栖月": "gu_qiyue",
    "宁观尘": "ning_guanchen",
    "慕夕歌": "mu_xige",
    "苏梦城": "su_mengcheng",
    "慕北歌": "mu_beige",
    "萧烬弦": "xiao_jinxian",
    "燕照绫": "yan_zhaoling",
    "欧阳狂徒": "ouyang_kuangtu",
    "旁白": "narrator",
    "月栖洲": "yue_qizhou",
    "初晴": "chu_qing",
    "狐妖": "hu_yao",
    "陆听潮": "lu_tingchao",
    "梦竹": "meng_zhu",
    "水烟": "shui_yan",
    "婉儿": "wan_er",
    "小墨": "xiao_mo",
    "谢无锋": "xie_wufeng",
    "叶沉舟": "ye_chenzhou",
    "影": "shadow",
    "清灵": "qing_ling",
    "小烛": "candy",
    "江湖老人": "jianghu_laoren",
    "周星驰": "zhou_xingchi",
    "搞笑男": "zhou_xingchi",
    "黑市": "heishi",
    # 小烛变体
    "小烛傲娇": "candy_cool",
    "小烛腹黑": "candy_mischievous",
    "小烛-傲娇大小姐": "小烛-傲娇大小姐",
    "小烛-腹黑小恶魔": "小烛-腹黑小恶魔",
    "小烛-柔糯软妹": "小烛-柔糯软妹",
    "小烛-元气小太阳": "小烛-元气小太阳",
    "小烛-温婉白月光": "小烛-温婉白月光",
    # AI 女友系列
    "星栀": "星栀-暧昧撩人",
    "初霁": "初霁-晨光安抚",
    "疏音": "疏音-清冷月色",
    "棠梨": "棠梨-温热奶感",
    "小晚": "小晚-温柔治愈",
    "夜棠": "夜棠-午夜耳语",
    "朝朝": "朝朝-元气阳光",
    # 王爷系列
    "王爷": "王爷-儒武沉稳",
    "王爷沉稳": "王爷-儒武沉稳",
    "王爷冷峻": "王爷-冷峻锋压",
    "王爷年轻": "王爷-年轻锐锋",
    "王爷武林": "王爷-武林高手-不老成",
    # 年轻和尚系列
    "和尚清朗": "年轻和尚-清朗",
    "和尚温和": "年轻和尚-温和",
    "和尚少年": "年轻和尚-少年感",
    # 小璃
    "小璃": "小璃-温婉闺秀",
    # 完整名（直接匹配）
    "星栀-暧昧撩人": "星栀-暧昧撩人",
    "初霁-晨光安抚": "初霁-晨光安抚",
    "疏音-清冷月色": "疏音-清冷月色",
    "棠梨-温热奶感": "棠梨-温热奶感",
    "小晚-温柔治愈": "小晚-温柔治愈",
    "夜棠-午夜耳语": "夜棠-午夜耳语",
    "朝朝-元气阳光": "朝朝-元气阳光",
    "王爷-儒武沉稳": "王爷-儒武沉稳",
    "王爷-冷峻锋压": "王爷-冷峻锋压",
    "王爷-年轻锐锋": "王爷-年轻锐锋",
    "王爷-武林高手-不老成": "王爷-武林高手-不老成",
    "年轻和尚-清朗": "年轻和尚-清朗",
    "年轻和尚-温和": "年轻和尚-温和",
    "年轻和尚-少年感": "年轻和尚-少年感",
    "小璃-温婉闺秀": "小璃-温婉闺秀",
}


def resolve_persona(name_hint):
    """将自然语言音色名称解析为 persona key"""
    name_hint = name_hint.strip()

    # 精确匹配
    if name_hint in PERSONA_MAP:
        return PERSONA_MAP[name_hint]

    # 模糊匹配：用中文关键词搜索
    for cn_name, key in PERSONA_MAP.items():
        if cn_name in name_hint or name_hint in cn_name:
            return key

    # 直接返回原始输入（可能是有效的 persona key）
    return name_hint


# ============ 核心功能 ============

def list_voices():
    """获取可用音色列表"""
    code, stdout, stderr = run_snowvoice(["voice", "list"])
    if code == 0:
        return stdout
    return f"获取音色列表失败: {stderr or stdout}"


def clone_voice(persona_key, text, tone=None, emotion=None, emotion_priority=False):
    """克隆声音生成语音"""
    env_check = check_environment()
    if not env_check["ready"]:
        return {"success": False, "message": env_check["message"]}

    args = ["clone", persona_key, text]
    if tone:
        args.extend(["--tone", tone])
    if emotion:
        args.extend(["--emotion", emotion])
    if emotion_priority:
        args.append("--emotion-priority")

    code, stdout, stderr = run_snowvoice(args)

    if code == 0:
        # 从输出提取文件路径
        actual_output = "unknown"
        path_match = re.search(r'输出 → (.+)', stdout)
        if path_match:
            rel_path = path_match.group(1).strip()
            actual_output = str(SNOWVOICE_ROOT / rel_path)
        else:
            path_match = re.search(r'最终成品[：:]\s*(.+)', stdout)
            if path_match:
                actual_output = path_match.group(1).strip()

        return {
            "success": True,
            "output_path": actual_output,
            "message": f"语音生成成功: {actual_output}"
        }
    else:
        return {
            "success": False,
            "message": f"生成失败: {stderr or stdout}"
        }


def design_voice(name, text, tone=None, emotion=None):
    """设计新音色"""
    env_check = check_environment()
    if not env_check["ready"]:
        return {"success": False, "message": env_check["message"]}

    args = ["design", name, text]
    if tone:
        args.extend(["--tone", tone])
    if emotion:
        args.extend(["--emotion", emotion])

    code, stdout, stderr = run_snowvoice(args)

    if code == 0:
        actual_output = "unknown"
        path_match = re.search(r'输出 → (.+)', stdout)
        if path_match:
            rel_path = path_match.group(1).strip()
            actual_output = str(SNOWVOICE_ROOT / rel_path)

        return {
            "success": True,
            "output_path": actual_output,
            "message": f"音色设计成功: {name}"
        }
    else:
        return {
            "success": False,
            "message": f"设计失败: {stderr or stdout}"
        }


# ============ 自然语言解析 ============

def parse_natural_language(query):
    """解析自然语言，提取 TTS 参数"""
    query = query.strip()

    # 模式1: 用[音色]说[内容] / 用[音色]的声音说[内容]
    match = re.search(r'用(.+?)的?声音?说(.+)', query)
    if match:
        persona_hint = match.group(1).strip()
        text = match.group(2).strip().strip('"\'""''')
        return {
            "action": "clone",
            "params": {"persona_key": resolve_persona(persona_hint), "text": text}
        }

    # 模式2: 让[音色]说[内容]
    match = re.search(r'让(.+?)说(.+)', query)
    if match:
        persona_hint = match.group(1).strip()
        text = match.group(2).strip().strip('"\'""''')
        return {
            "action": "clone",
            "params": {"persona_key": resolve_persona(persona_hint), "text": text}
        }

    # 模式3: 设计[音色名] [描述]
    match = re.search(r'设计.{0,4}?([\u4e00-\u9fff]+).{0,4}?音色|设计.{0,4}?一个.{0,6}?([\u4e00-\u9fff]+)', query)
    if match:
        voice_name = match.group(1) or match.group(2)
        return {
            "action": "design",
            "params": {"name": voice_name, "text": "这是一段用于音色建模的短句", "tone": voice_name}
        }

    # 模式4: 把/将[内容]转成语音
    if any(kw in query for kw in ["转成语音", "转为语音", "转语音", "合成语音", "生成语音"]):
        # 先去掉「把/将」，再按关键词切分
        cleaned = re.sub(r"^(把|将)", "", query)
        text = re.split(r"转成语音|转为语音|转语音|合成语音|生成语音", cleaned)[0].strip()
        text = text.strip()
        if not text:
            text = query
        return {
            "action": "clone",
            "params": {"persona_key": "gu_qiyue", "text": text}
        }

    # 模式5: 直接说[内容]
    if query.startswith("说"):
        return {
            "action": "clone",
            "params": {"persona_key": "gu_qiyue", "text": query[1:].strip()}
        }

    # 默认：把整句话当内容，用默认音色
    return {
        "action": "clone",
        "params": {"persona_key": "gu_qiyue", "text": query}
    }


# ============ CLI 入口 ============

def main():
    if len(sys.argv) < 2:
        print("Usage: python tts_skill.py <自然语言指令>")
        print('Example: python tts_skill.py "用顾栖月的声音说你好"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    parsed = parse_natural_language(query)

    if parsed["action"] == "clone":
        result = clone_voice(**parsed["params"])
    elif parsed["action"] == "design":
        result = design_voice(**parsed["params"])
    else:
        result = {"success": False, "message": "不支持的操作"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
