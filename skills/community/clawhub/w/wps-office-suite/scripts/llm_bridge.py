"""
统一模型层桥接 v4.9.0
功能：白名单探测 + subprocess CLI + JSON 契约，接入 cn-llm-router 作为统一模型层

死规则合规：
  - 规则4：禁止自动发布
  - 规则9：基础功能自研（白名单探测 + subprocess，无外部 API）
  - 规则10：性能优化（超时控制 + 子进程自动关闭）
  - 规则13：不生成禁止文件类型
  - 规则14：三轮自审
  - 规则15：沙箱模拟运行
  - 规则16：子进程超时自动关闭

安全合规：
  - 纯白名单本地路径检查，不读取外部凭证或 API Key
  - 不联网探测，不发送任何数据到外部
  - 子进程超时自动关闭，释放系统资源
  - 外部 LLM 仅在用户安装 cn-llm-router 后通过白名单命中调用
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

__version__ = "4.9.0"

# 白名单探测路径（按优先级排序）
WHITELIST_PATHS = [
    Path.home() / ".claude" / "skills" / "cn-llm-router" / "scripts" / "router.py",
    Path.home() / ".workbuddy" / "skills" / "cn-llm-router" / "scripts" / "router.py",
    Path.cwd() / "skills" / "cn-llm-router" / "scripts" / "router.py",
]

# cn-llm-router 安装提示
INSTALL_HINT = "可选装 cn-llm-router 获取零配置多模型能力：skillhub.cn/skills/cn-llm-router"

# 默认超时（秒）
DEFAULT_TIMEOUT = 30


def detect_router() -> Optional[Path]:
    """
    按白名单优先级探测 cn-llm-router 是否存在
    返回命中的路径，未命中返回 None
    """
    for path in WHITELIST_PATHS:
        if path.exists() and path.is_file():
            return path
    return None


def is_router_available() -> bool:
    """检查 cn-llm-router 是否可用"""
    return detect_router() is not None


def call_router(
    prompt: str,
    task: str = "chat",
    timeout: int = DEFAULT_TIMEOUT,
    model: str = "",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    调用 cn-llm-router 执行任务
    
    Args:
        prompt: 提示词
        task: 任务类型 (chat/translate/summarize/generate)
        timeout: 超时时间（秒）
        model: 指定模型（空则自动选择）
        **kwargs: 额外参数
    
    Returns:
        {
            "ok": bool,
            "text": str,      # 模型输出文本
            "model": str,     # 使用的模型名
            "cost": float,    # 估算费用
            "source": str,    # "cn-llm-router" 或 "fallback"
            "error": str,     # 错误信息（失败时）
            "install_hint": str,  # 安装提示（未命中时）
        }
    """
    result = {
        "ok": False,
        "text": "",
        "model": "",
        "cost": 0.0,
        "source": "",
        "error": "",
        "install_hint": "",
    }

    # Step 1: 白名单探测
    router_path = detect_router()
    if router_path is None:
        result["error"] = "cn-llm-router 未安装"
        result["install_hint"] = INSTALL_HINT
        result["source"] = "fallback"
        return result

    # Step 2: 构建命令
    cmd = [
        sys.executable,
        str(router_path),
        "chat",
        "--prompt",
        prompt,
        "--task",
        task,
        "--json",
        "--timeout",
        str(timeout),
    ]

    if model:
        cmd.extend(["--model", model])

    # 添加额外参数
    for key, value in kwargs.items():
        if value is not None:
            cmd.extend([f"--{key}", str(value)])

    # Step 3: 执行子进程（带超时和自动关闭）
    proc = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(router_path.parent.parent.parent),  # 在 router 项目目录下执行
        )

        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # 规则16：子进程超时自动关闭
            proc.kill()
            proc.wait()
            stdout, stderr = proc.communicate()
            result["error"] = f"cn-llm-router 调用超时（{timeout}秒）"
            result["source"] = "fallback"
            return result

        # 检查返回码
        if proc.returncode != 0:
            err_msg = stderr.decode("utf-8", errors="replace")[:200] if stderr else "未知错误"
            result["error"] = f"cn-llm-router 执行失败: {err_msg}"
            result["source"] = "fallback"
            return result

        # Step 4: 解析 JSON 输出
        output = stdout.decode("utf-8", errors="replace").strip()
        if not output:
            result["error"] = "cn-llm-router 返回空输出"
            result["source"] = "fallback"
            return result

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            # 尝试从输出中提取 JSON
            json_start = output.find("{")
            json_end = output.rfind("}")
            if json_start >= 0 and json_end > json_start:
                try:
                    data = json.loads(output[json_start : json_end + 1])
                except json.JSONDecodeError:
                    result["error"] = f"cn-llm-router 输出解析失败: {output[:100]}"
                    result["source"] = "fallback"
                    return result
            else:
                # 将纯文本作为结果
                data = {"text": output, "model": "unknown", "cost": 0.0}

        # Step 5: 提取字段（仅读取 text/model/cost）
        result["text"] = data.get("text", data.get("content", data.get("result", "")))
        result["model"] = data.get("model", data.get("model_name", "unknown"))
        result["cost"] = float(data.get("cost", data.get("total_cost", 0.0)))
        result["ok"] = True
        result["source"] = "cn-llm-router"

    except FileNotFoundError:
        result["error"] = "Python 解释器未找到"
        result["source"] = "fallback"
    except PermissionError:
        result["error"] = "cn-llm-router 脚本无执行权限"
        result["source"] = "fallback"
    except Exception as e:
        result["error"] = f"cn-llm-router 调用异常: {str(e)[:200]}"
        result["source"] = "fallback"
    finally:
        # 规则16：确保子进程被关闭
        if proc is not None and proc.poll() is None:
            try:
                proc.kill()
                proc.wait(timeout=5)
            except Exception:
                pass

    return result


def translate(
    text: str,
    source_lang: str = "",
    target_lang: str = "zh",
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    翻译接口（封装 call_router）
    
    Returns:
        {
            "ok": bool,
            "text": str,      # 翻译结果
            "model": str,
            "cost": float,
            "source": str,
            "error": str,
        }
    """
    prompt = f"请将以下文本从 {source_lang or '自动检测'} 翻译为 {target_lang}:\n\n{text}"
    return call_router(prompt=prompt, task="translate", timeout=timeout)


def summarize(
    text: str,
    max_length: int = 500,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    摘要接口
    """
    prompt = f"请对以下文本进行摘要，控制在 {max_length} 字以内:\n\n{text}"
    return call_router(prompt=prompt, task="summarize", timeout=timeout)


def generate(
    prompt: str,
    max_tokens: int = 1000,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    文本生成接口
    """
    return call_router(prompt=prompt, task="generate", timeout=timeout, max_tokens=str(max_tokens))


def continue_writing(
    text: str,
    context: str = "",
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    续写接口（v4.9 新增）
    """
    prompt = f"请续写以下文本，保持风格和语气一致：\n\n{text}"
    if context:
        prompt = f"上下文：{context}\n\n{prompt}"
    return call_router(prompt=prompt, task="continue", timeout=timeout)


def rewrite_text(
    text: str,
    style: str = "formal",
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    改写接口（v4.9 新增）
    """
    style_map = {
        "formal": "正式",
        "casual": "口语化",
        "concise": "简洁",
        "detailed": "详细",
        "polite": "礼貌",
        "professional": "专业",
    }
    style_cn = style_map.get(style, style)
    prompt = f"请将以下文本改写为{style_cn}风格:\n\n{text}"
    return call_router(prompt=prompt, task="rewrite", timeout=timeout)


def expand_text(
    text: str,
    aspect: str = "details",
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    扩写接口（v4.9 新增）
    """
    aspect_map = {
        "details": "补充细节和论据",
        "examples": "添加具体案例",
        "background": "补充背景信息",
        "analysis": "深入分析",
    }
    aspect_cn = aspect_map.get(aspect, "补充内容")
    prompt = f"请对以下文本进行扩写，{aspect_cn}:\n\n{text}"
    return call_router(prompt=prompt, task="expand", timeout=timeout)


def get_best_method(preferred: str = "auto") -> str:
    """
    获取最佳可用方法
    
    Args:
        preferred: 偏好方法 ("auto", "cn-llm-router", "local")
    
    Returns:
        "cn-llm-router" 或 "local"
    """
    if preferred == "cn-llm-router":
        return "cn-llm-router" if is_router_available() else "local"
    elif preferred == "local":
        return "local"
    else:
        # auto: 优先使用 cn-llm-router
        return "cn-llm-router" if is_router_available() else "local"


def _cli():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description=f"统一模型层桥接 v{__version__} — cn-llm-router 白名单探测 + subprocess"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    p = sub.add_parser("check", help="检查 cn-llm-router 是否可用")

    # chat
    p = sub.add_parser("chat", help="通用对话")
    p.add_argument("--prompt", required=True, help="提示词")
    p.add_argument("--task", default="chat", help="任务类型")
    p.add_argument("--model", default="", help="指定模型")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="超时时间")

    # translate
    p = sub.add_parser("translate", help="翻译")
    p.add_argument("--text", required=True, help="要翻译的文本")
    p.add_argument("--source", default="", help="源语言")
    p.add_argument("--target", default="zh", help="目标语言")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    # summarize
    p = sub.add_parser("summarize", help="摘要")
    p.add_argument("--text", required=True, help="要摘要的文本")
    p.add_argument("--max-length", type=int, default=500, help="最大长度")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    # continue
    p = sub.add_parser("continue", help="续写文本")
    p.add_argument("--text", required=True, help="要续写的文本")
    p.add_argument("--context", default="", help="上下文")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    # rewrite
    p = sub.add_parser("rewrite", help="改写文本")
    p.add_argument("--text", required=True, help="要改写的文本")
    p.add_argument(
        "--style",
        default="formal",
        choices=["formal", "casual", "concise", "detailed", "polite", "professional"],
        help="目标风格",
    )
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    # expand
    p = sub.add_parser("expand", help="扩写文本")
    p.add_argument("--text", required=True, help="要扩写的文本")
    p.add_argument(
        "--aspect",
        default="details",
        choices=["details", "examples", "background", "analysis"],
        help="扩写方向",
    )
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    args = parser.parse_args()

    if args.command == "check":
        router = detect_router()
        if router:
            print(json.dumps({
                "ok": True,
                "available": True,
                "path": str(router),
                "hint": "cn-llm-router 已安装，可直接使用",
            }, ensure_ascii=False))
        else:
            print(json.dumps({
                "ok": True,
                "available": False,
                "path": None,
                "hint": INSTALL_HINT,
            }, ensure_ascii=False))

    elif args.command == "chat":
        result = call_router(
            prompt=args.prompt,
            task=args.task,
            timeout=args.timeout,
            model=args.model,
        )
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "translate":
        result = translate(
            text=args.text,
            source_lang=args.source,
            target_lang=args.target,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "summarize":
        result = summarize(
            text=args.text,
            max_length=args.max_length,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "continue":
        result = continue_writing(
            text=args.text,
            context=args.context,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "rewrite":
        result = rewrite_text(
            text=args.text,
            style=args.style,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "expand":
        result = expand_text(
            text=args.text,
            aspect=args.aspect,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
