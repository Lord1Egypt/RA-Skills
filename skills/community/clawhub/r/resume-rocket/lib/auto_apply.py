"""Pro 档：批量 JD 定制 + 自动投递（对接 boss-zhipin skill）"""
from __future__ import annotations
import time
import subprocess
from pathlib import Path
from datetime import datetime


def run_batch(jd_list: Path, resume_base: Path, daily_limit: int = 50) -> None:
    urls = [l.strip() for l in jd_list.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    print(f"[auto-apply] 读取 {len(urls)} 条 JD，日上限 {daily_limit}")

    report_dir = Path("./output") / f"batch-{datetime.now():%Y%m%d-%H%M%S}"
    report_dir.mkdir(parents=True, exist_ok=True)

    applied = 0
    for i, url in enumerate(urls, 1):
        if applied >= daily_limit:
            print(f"[auto-apply] 达到日上限 {daily_limit}，停止")
            break
        print(f"[auto-apply] ({i}/{len(urls)}) 处理: {url}")
        out = report_dir / f"{i:03d}"
        try:
            subprocess.run([
                "python", "main.py", "rewrite",
                "--resume", str(resume_base),
                "--jd", url,
                "--output", str(out),
                "--tier", "pro",
            ], check=True, cwd=Path(__file__).parent.parent)
            _dispatch_to_boss(out / "resume-optimized.docx", url)
            applied += 1
        except Exception as ex:
            print(f"[auto-apply] 失败: {ex}")
        time.sleep(20 + (i % 10) * 3)  # 随机间隔

    print(f"[auto-apply] ✅ 完成 {applied}/{len(urls)}，报告：{report_dir}")


def _dispatch_to_boss(resume_path: Path, jd_url: str) -> None:
    """调用 boss-zhipin skill 投递；实际对接在集成测试时完成。"""
    # TODO: 通过 openclaw skill run boss-zhipin --apply --jd-url ... --resume ...
    print(f"  → [stub] 将 {resume_path.name} 投递到 {jd_url}")
