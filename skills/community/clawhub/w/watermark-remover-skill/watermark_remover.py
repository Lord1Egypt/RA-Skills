#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布衣去水印 GUI 程序的自动化辅助工具。

工作模式（方案 B）：
  GUI 程序常驻运行 + 监控功能开启 → 把图片复制到"输入目录"后会被自动处理 → 结果写到"输出目录"。

本脚本不启动 GUI，只负责：
  1. 把图片送入输入目录（可选：用任务子目录隔离）
  2. 轮询输出目录，等待对应输出文件出现
  3. 收集结果路径返回
  4. 提供"前置自检"功能，验证 GUI 监控是否在工作

依赖：仅标准库。
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
import uuid
from pathlib import Path
from typing import Iterable


# ============================================================
# 配置加载
# ============================================================
DEFAULT_CONFIG_NAMES = ["config.json", "watermark_remover_config.json"]
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def find_config(explicit_path: str | None) -> Path:
    """按优先级查找配置文件：显式参数 > 环境变量 > 同目录 > 用户目录"""
    if explicit_path:
        p = Path(explicit_path).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"指定的配置文件不存在: {p}")
        return p

    env = os.environ.get("WATERMARK_REMOVER_CONFIG")
    if env:
        p = Path(env).expanduser().resolve()
        if p.exists():
            return p

    here = Path(__file__).resolve().parent
    for name in DEFAULT_CONFIG_NAMES:
        p = here / name
        if p.exists():
            return p

    home = Path.home() / ".watermark-remover" / "config.json"
    if home.exists():
        return home

    raise FileNotFoundError(
        "找不到配置文件。请按下列任一方式提供:\n"
        f"  1) 命令行参数 --config <路径>\n"
        f"  2) 环境变量 WATERMARK_REMOVER_CONFIG\n"
        f"  3) 与脚本同目录下放 config.json\n"
        f"  4) ~/.watermark-remover/config.json"
    )


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # 必填字段校验
    for key in ("input_dir", "output_dir"):
        if key not in cfg or not cfg[key]:
            raise ValueError(f"配置文件缺少必填字段: {key} （来自 {path}）")
    cfg["input_dir"] = str(Path(cfg["input_dir"]).expanduser().resolve())
    cfg["output_dir"] = str(Path(cfg["output_dir"]).expanduser().resolve())
    cfg.setdefault("undetected_dir", cfg["output_dir"] + "_未识别")
    cfg.setdefault("default_timeout_sec", 300)
    cfg.setdefault("poll_interval_sec", 1.0)
    return cfg


# ============================================================
# 核心逻辑
# ============================================================
class WatermarkRemoverClient:
    """封装与 GUI 监控的交互。"""

    def __init__(self, config: dict):
        self.input_dir = Path(config["input_dir"])
        self.output_dir = Path(config["output_dir"])
        self.undetected_dir = Path(config["undetected_dir"])
        self.default_timeout = float(config.get("default_timeout_sec", 300))
        self.poll_interval = float(config.get("poll_interval_sec", 1.0))

        if not self.input_dir.exists():
            raise FileNotFoundError(
                f"输入目录不存在: {self.input_dir}\n"
                f"请检查 GUI 程序中实际选定的'输入文件夹'是否与配置一致。"
            )
        if not self.output_dir.exists():
            # 输出目录通常会由 GUI 创建，这里允许不存在
            print(f"[警告] 输出目录暂不存在（GUI 处理后会自动创建）: {self.output_dir}", file=sys.stderr)

    # ---------- 提交文件 ----------
    def submit_files(
        self,
        sources: Iterable[str | Path],
        task_subdir: str | None = None,
        copy: bool = True,
    ) -> tuple[list[Path], str]:
        """
        把若干图片送入输入目录。

        :param sources: 源文件路径列表
        :param task_subdir: 任务子目录名（建议使用，避免与他人冲突）。None 时直接放在输入根目录
        :param copy: True=复制（默认，不影响原文件），False=移动
        :return: (送达后在输入目录中的文件路径列表, 实际使用的子目录名或'')
        """
        srcs: list[Path] = [Path(s).expanduser().resolve() for s in sources]
        for s in srcs:
            if not s.exists():
                raise FileNotFoundError(f"源文件不存在: {s}")
            if s.suffix.lower() not in SUPPORTED_FORMATS:
                raise ValueError(f"不支持的文件格式 {s.suffix}: {s}")

        # 任务隔离子目录
        if task_subdir is None:
            target_root = self.input_dir
            sub = ""
        else:
            sub = task_subdir
            target_root = self.input_dir / sub
            target_root.mkdir(parents=True, exist_ok=True)

        # 先用 .part 临时名写入，写完再 rename，避免 GUI 监控读到半截文件
        delivered: list[Path] = []
        for src in srcs:
            final_path = target_root / src.name
            tmp_path = final_path.with_suffix(final_path.suffix + ".part")
            try:
                if copy:
                    shutil.copy2(src, tmp_path)
                else:
                    shutil.move(str(src), str(tmp_path))
                tmp_path.rename(final_path)
            except Exception as e:
                # 失败时清理临时文件
                if tmp_path.exists():
                    try:
                        tmp_path.unlink()
                    except Exception:
                        pass
                raise RuntimeError(f"送入文件失败 {src}: {e}") from e
            delivered.append(final_path)

        return delivered, sub

    # ---------- 等待结果 ----------
    def wait_for_results(
        self,
        input_files: Iterable[Path],
        timeout_sec: float | None = None,
        verbose: bool = True,
    ) -> dict:
        """
        轮询等待这些输入文件被处理完成。

        判定方式：检查输出目录或"_未识别"目录中是否出现对应的相对路径文件。

        :return: {
            "completed": [{"input": str, "output": str, "category": "ok"|"undetected"}, ...],
            "pending":   [str, ...],   # 超时还没出现的
            "elapsed_sec": float
        }
        """
        timeout = float(timeout_sec) if timeout_sec is not None else self.default_timeout
        deadline = time.time() + timeout

        # 把每个输入文件映射成"它应该出现在哪两个位置中的一个"
        in_files = [Path(p).resolve() for p in input_files]
        expected: list[tuple[Path, Path, Path]] = []   # (input, expected_in_output, expected_in_undetected)
        for ip in in_files:
            try:
                rel = ip.relative_to(self.input_dir)
            except ValueError:
                # 不在输入目录下（理论上不应发生，因为 submit_files 后路径就是输入目录里的）
                rel = Path(ip.name)
            expected.append((ip, self.output_dir / rel, self.undetected_dir / rel))

        completed: list[dict] = []
        remaining = list(expected)

        while remaining and time.time() < deadline:
            still_pending: list[tuple[Path, Path, Path]] = []
            for input_p, ok_p, undet_p in remaining:
                if ok_p.exists() and self._is_file_stable(ok_p):
                    completed.append({"input": str(input_p), "output": str(ok_p), "category": "ok"})
                elif undet_p.exists() and self._is_file_stable(undet_p):
                    completed.append({"input": str(input_p), "output": str(undet_p), "category": "undetected"})
                else:
                    still_pending.append((input_p, ok_p, undet_p))

            if verbose and len(still_pending) != len(remaining):
                print(f"[进度] 已完成 {len(completed)}/{len(expected)}, 等待中 {len(still_pending)}")

            remaining = still_pending
            if remaining:
                time.sleep(self.poll_interval)

        elapsed = timeout - max(0, deadline - time.time())
        return {
            "completed": completed,
            "pending": [str(p[0]) for p in remaining],
            "elapsed_sec": round(elapsed, 2),
        }

    @staticmethod
    def _is_file_stable(p: Path) -> bool:
        """连续两次 stat 大小一致且 > 0 视为稳定（避免读到正在写入的半成品）"""
        try:
            s1 = p.stat().st_size
            if s1 == 0:
                return False
            time.sleep(0.15)
            s2 = p.stat().st_size
            return s1 == s2
        except Exception:
            return False

    # ---------- 一站式：提交并等待 ----------
    def process(
        self,
        sources: Iterable[str | Path],
        task_subdir: str | None = "auto",   # "auto" = 自动生成 UUID 子目录；None = 不用子目录；其他字符串 = 指定名字
        copy: bool = True,
        timeout_sec: float | None = None,
        verbose: bool = True,
    ) -> dict:
        """提交 + 等待结果，一步搞定。返回与 wait_for_results 相同的字典，外加 task_subdir。"""
        if task_subdir == "auto":
            task_subdir = f"agent_{uuid.uuid4().hex[:10]}"

        if verbose:
            count = len(list(sources)) if not isinstance(sources, (list, tuple)) else len(sources)
            print(f"[提交] 送入 {count} 个文件到 {self.input_dir / (task_subdir or '')}")

        delivered, sub = self.submit_files(sources, task_subdir=task_subdir, copy=copy)

        if verbose:
            print(f"[等待] 轮询输出目录, 超时 {timeout_sec or self.default_timeout}s")

        result = self.wait_for_results(delivered, timeout_sec=timeout_sec, verbose=verbose)
        result["task_subdir"] = sub
        return result

    # ---------- 自检：验证 GUI 监控是否在工作 ----------
    def health_check(self, sample_image: str | Path | None = None, timeout_sec: float = 60.0) -> dict:
        """
        发一张图试试，看 GUI 是不是真的在监控。

        :param sample_image: 测试用图片。不提供时只做静态检查（目录是否存在等）。
        :param timeout_sec: 等待结果的超时
        :return: {"ok": bool, "messages": [str, ...], "result": dict|None}
        """
        messages: list[str] = []
        ok = True

        # 静态检查
        if not self.input_dir.exists():
            ok = False
            messages.append(f"❌ 输入目录不存在: {self.input_dir}")
        else:
            messages.append(f"✅ 输入目录存在: {self.input_dir}")

        if not self.output_dir.exists():
            messages.append(f"⚠️  输出目录暂不存在（GUI 处理后会创建）: {self.output_dir}")
        else:
            messages.append(f"✅ 输出目录存在: {self.output_dir}")

        if sample_image is None:
            messages.append("（未提供测试图片，跳过实时连通性测试）")
            return {"ok": ok, "messages": messages, "result": None}

        # 实时测试
        sub = f"healthcheck_{uuid.uuid4().hex[:8]}"
        try:
            result = self.process(
                [sample_image],
                task_subdir=sub,
                timeout_sec=timeout_sec,
                verbose=False,
            )
            if result["completed"]:
                messages.append(f"✅ 测试成功，{result['elapsed_sec']}s 后收到结果。GUI 监控工作正常。")
            else:
                ok = False
                messages.append(
                    f"❌ 测试失败：{timeout_sec}s 内未收到处理结果。\n"
                    f"   常见原因：\n"
                    f"   1) GUI 程序未运行\n"
                    f"   2) GUI 中没开启「📡 监控目录」按钮（必须显示绿色'开启'状态）\n"
                    f"   3) GUI 选择的输入目录与本配置的 input_dir 不一致\n"
                    f"   4) 当前账号是免费会员，无监控权限"
                )
            return {"ok": ok, "messages": messages, "result": result}
        except Exception as e:
            return {"ok": False, "messages": messages + [f"❌ 测试过程中异常: {e}"], "result": None}


# ============================================================
# 命令行接口
# ============================================================
def cmd_check(args, client: WatermarkRemoverClient) -> int:
    res = client.health_check(sample_image=args.sample, timeout_sec=args.timeout)
    print("\n".join(res["messages"]))
    return 0 if res["ok"] else 1


def cmd_process(args, client: WatermarkRemoverClient) -> int:
    files: list[str] = []
    for item in args.files:
        p = Path(item).expanduser()
        if p.is_dir():
            files.extend(str(x) for x in p.rglob("*") if x.suffix.lower() in SUPPORTED_FORMATS)
        else:
            files.append(str(p))

    if not files:
        print("没有找到可处理的图片。", file=sys.stderr)
        return 2

    print(f"待处理 {len(files)} 个文件")
    sub = None if args.no_subdir else (args.subdir or "auto")

    try:
        result = client.process(
            files,
            task_subdir=sub,
            copy=not args.move,
            timeout_sec=args.timeout,
            verbose=True,
        )
    except FileNotFoundError as e:
        print(f"提交失败: {e}", file=sys.stderr)
        return 5
    except ValueError as e:
        print(f"参数错误: {e}", file=sys.stderr)
        return 5
    except Exception as e:
        print(f"提交过程出错: {e}", file=sys.stderr)
        return 5

    print("\n========== 处理完成 ==========")
    print(f"任务子目录: {result.get('task_subdir') or '(根目录)'}")
    print(f"完成: {len(result['completed'])} 个")
    print(f"未完成（超时）: {len(result['pending'])} 个")
    print(f"耗时: {result['elapsed_sec']}s")
    print()

    for item in result["completed"]:
        tag = "[OK]" if item["category"] == "ok" else "[未识别水印]"
        print(f"{tag} {item['input']}\n     -> {item['output']}")

    if result["pending"]:
        print("\n以下文件超时未完成：")
        for p in result["pending"]:
            print(f"  - {p}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n详细结果已写入: {args.json_out}")

    return 0 if not result["pending"] else 3   # 部分超时返回 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="watermark_remover",
        description="布衣去水印 GUI 自动化辅助工具（方案B：依赖 GUI 监控功能）",
    )
    parser.add_argument("--config", "-c", help="配置文件路径，不传时按默认顺序查找")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="自检：验证 GUI 监控是否工作")
    p_check.add_argument("--sample", help="测试用图片路径，不提供时只做静态检查")
    p_check.add_argument("--timeout", type=float, default=60.0, help="测试超时秒数, 默认 60s")
    p_check.set_defaults(func=cmd_check)

    p_proc = sub.add_parser("process", help="处理一批图片或一个目录")
    p_proc.add_argument("files", nargs="+", help="图片文件路径或目录")
    p_proc.add_argument("--subdir", help="任务子目录名, 缺省自动生成 UUID 子目录")
    p_proc.add_argument("--no-subdir", action="store_true", help="不使用任务子目录, 直接放入输入根目录")
    p_proc.add_argument("--move", action="store_true", help="移动而不是复制（会删除原文件）")
    p_proc.add_argument("--timeout", type=float, help="等待超时秒数, 缺省用配置文件中的 default_timeout_sec")
    p_proc.add_argument("--json-out", help="把结果以 JSON 形式写入指定文件")
    p_proc.set_defaults(func=cmd_process)

    args = parser.parse_args(argv)

    try:
        cfg_path = find_config(args.config)
        cfg = load_config(cfg_path)
        client = WatermarkRemoverClient(cfg)
    except Exception as e:
        print(f"初始化失败: {e}", file=sys.stderr)
        return 4

    return args.func(args, client)


if __name__ == "__main__":
    sys.exit(main())
