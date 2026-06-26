#!/usr/bin/env python3
"""
WiseAnalyze CLI - Medical Checkup Report Analysis (powered by WiseDiag)

Provides separate sub-commands for each step of the async analysis workflow.
The AI Agent calls each step independently and handles polling logic itself.

Sub-commands:
    submit  - Submit local files or a PDF URL for analysis, returns taskId
    start   - Start interpretation for a given taskId
    query   - Query task status and progress for a given taskId
    save    - Save the finished result to disk

Usage:
    export WISEDIAG_API_KEY=your_api_key
    python3 wise_analyze.py submit -f "/path/to/report.pdf"
    python3 wise_analyze.py submit -u "https://example.com/report.pdf"
    python3 wise_analyze.py start  -t "task-id-here"
    python3 wise_analyze.py query  -t "task-id-here"
    python3 wise_analyze.py save   -t "task-id-here"

Get API key: https://console.wisediag.com/apiKeyManage
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

import requests


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SERVICE_URL = "https://openapi.wisediag.com"
MAX_RETRIES         = 3
RETRY_DELAY         = 5
REQUEST_TIMEOUT     = 30
UPLOAD_TIMEOUT      = 120
MAX_PAGES           = 50
SUPPORTED_FORMATS   = (".pdf",)
MAX_FILE_SIZE_MB    = 50


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    key = os.environ.get("WISEDIAG_API_KEY", "")
    if not key:
        print("""
[!] Error: WISEDIAG_API_KEY is not set.

    export WISEDIAG_API_KEY=your_api_key

Get a key at: https://s.wisediag.com/xsu9x0jq
""")
        raise SystemExit(1)
    return key


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {_get_api_key()}",
        "Content-Type":  "application/json",
    }


def _post_json(endpoint: str, payload: dict,
               max_retries: int = MAX_RETRIES) -> dict | None:
    """POST JSON with automatic retry. Returns parsed JSON or None."""
    headers = _headers()
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[*] Requesting API... (attempt {attempt}/{max_retries})")
            resp = requests.post(
                endpoint, json=payload, headers=headers,
                timeout=REQUEST_TIMEOUT,
            )

            if resp.status_code == 401:
                print("[!] Authentication failed. Check your API key.")
                return None

            if resp.status_code == 200:
                try:
                    data = resp.json()
                except ValueError:
                    last_error = f"Invalid JSON in 200 response: {resp.text[:200]}"
                    continue
                if data.get("success"):
                    return data
                err_code = data.get("errCode", "")
                err_msg  = data.get("errMessage", "")
                if err_code == "50301":
                    print(f"[!] PDF exceeds page limit ({MAX_PAGES} pages max).")
                    return None
                if str(err_code) == "400":
                    print(f"[!] Bad request: {err_msg}")
                    return None
                last_error = f"API error {err_code}: {err_msg}"
            else:
                body = resp.text[:300]
                try:
                    err_data = resp.json()
                    err_code = str(err_data.get("errCode", ""))
                    if err_code in ("404", "400", "403"):
                        print(f"[!] Server error (non-retryable): {err_data.get('errMessage', body)}")
                        return None
                except Exception:
                    pass
                last_error = f"HTTP {resp.status_code}: {body}"

        except requests.Timeout:
            last_error = f"Timed out after {REQUEST_TIMEOUT}s"
        except requests.ConnectionError:
            last_error = "Connection refused"
        except Exception as e:
            last_error = str(e)

        if attempt < max_retries:
            print(f"[!] Attempt {attempt}/{max_retries} failed: {last_error}")
            print(f"    Retrying in {RETRY_DELAY}s ...")
            time.sleep(RETRY_DELAY)
        else:
            print(f"[!] All {max_retries} attempts failed. Last error: {last_error}")

    return None


def _post_multipart(endpoint: str, request_data: dict, file_paths: list[str],
                    max_retries: int = MAX_RETRIES) -> dict | None:
    """POST multipart/form-data with file uploads. Returns parsed JSON or None."""
    headers = {"Authorization": f"Bearer {_get_api_key()}"}
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[*] Uploading files... (attempt {attempt}/{max_retries})")

            files_list = []
            opened_files = []
            for fp in file_paths:
                f = open(fp, "rb")
                opened_files.append(f)
                files_list.append(("files", (os.path.basename(fp), f)))

            request_part = (
                "request",
                (None, json.dumps(request_data), "application/json"),
            )

            try:
                resp = requests.post(
                    endpoint,
                    headers=headers,
                    files=[request_part] + files_list,
                    timeout=UPLOAD_TIMEOUT,
                )
            finally:
                for f in opened_files:
                    f.close()

            if resp.status_code == 401:
                print("[!] Authentication failed. Check your API key.")
                return None

            if resp.status_code == 200:
                try:
                    data = resp.json()
                except ValueError:
                    last_error = f"Invalid JSON in 200 response: {resp.text[:200]}"
                    continue
                if data.get("success"):
                    return data
                err_code = data.get("errCode", "")
                err_msg = data.get("errMessage", "")
                if err_code == "50301":
                    print(f"[!] PDF exceeds page limit ({MAX_PAGES} pages max).")
                    return None
                if str(err_code) == "400":
                    print(f"[!] Bad request: {err_msg}")
                    return None
                last_error = f"API error {err_code}: {err_msg}"
            else:
                body = resp.text[:300]
                try:
                    err_data = resp.json()
                    err_code = str(err_data.get("errCode", ""))
                    if err_code in ("404", "400", "403"):
                        print(f"[!] Server error (non-retryable): {err_data.get('errMessage', body)}")
                        return None
                except Exception:
                    pass
                last_error = f"HTTP {resp.status_code}: {body}"

        except requests.Timeout:
            last_error = f"Timed out after {UPLOAD_TIMEOUT}s"
        except requests.ConnectionError:
            last_error = "Connection refused"
        except FileNotFoundError as e:
            print(f"[!] File not found: {e}")
            return None
        except Exception as e:
            last_error = str(e)

        if attempt < max_retries:
            print(f"[!] Attempt {attempt}/{max_retries} failed: {last_error}")
            print(f"    Retrying in {RETRY_DELAY}s ...")
            time.sleep(RETRY_DELAY)
        else:
            print(f"[!] All {max_retries} attempts failed. Last error: {last_error}")

    return None


def _default_output_dir() -> Path:
    return Path.cwd()


# ---------------------------------------------------------------------------
# Result formatting
# ---------------------------------------------------------------------------

def _format_result_markdown(result: dict, completed_at: str = "") -> str:
    """Convert the structured analysis result into readable Markdown."""
    lines = ["# 体检报告分析\n"]
    if completed_at:
        lines.append(f"**分析完成时间：** {completed_at}\n")

    summary = result.get("summaryOfSelfReportedHealthStatus", "")
    if summary:
        lines.append("## 自述健康概况\n")
        lines.append(summary + "\n")

    health_review = result.get("healthReview") or {}

    review_desc = health_review.get("description", "")
    if review_desc:
        lines.append("## 健康综述\n")
        lines.append(review_desc)
        lines.append("")

    abnormal_items = health_review.get("abnormalItems") or []
    if abnormal_items:
        lines.append("## 异常项目概览\n")
        for item in abnormal_items:
            name = item.get("name", "")
            abnormal = item.get("abnormal", "")
            lines.append(f"- **{name}**：{abnormal}")
        lines.append("")

    advantages = result.get("healthAdvantages")
    if advantages:
        lines.append("## 健康优势\n")
        if isinstance(advantages, list):
            for adv in advantages:
                lines.append(f"- {adv}")
        else:
            lines.append(str(advantages))
        lines.append("")

    consults = result.get("healthConsults") or []
    if consults:
        lines.append("## 详细解读\n")
        for i, c in enumerate(consults, 1):
            name = c.get("abnormalName", "Unknown")
            lines.append(f"### {i}. {name}\n")

            highlight = c.get("abnormalHighlight") or {}
            indicators = highlight.get("anomalousIndicators", "")
            if indicators:
                lines.append(f"**异常指标：** {indicators}\n")

            locality = c.get("abnormalLocality", "")
            science = c.get("abnormalScience") or {}
            cd = science.get("clinicalDefinition", "")
            cs = science.get("clinicalSignificance", "")
            cc = science.get("clinicalCognition", "")

            science_parts = []
            if locality:
                science_parts.append(locality)
            if cd:
                science_parts.append(cd)
            if cs:
                science_parts.append(cs)
            if cc:
                science_parts.append(cc)
            if science_parts:
                lines.append(f"**科普解读：** {' '.join(science_parts)}\n")

            impacts = c.get("abnormalHealthImpacts", "")
            if impacts:
                lines.append(f"**健康影响：** {impacts}\n")

            advice = c.get("abnormalLifeAndOtherEx", "")
            if advice:
                lines.append(f"**建议：** {advice}\n")

    lifestyle = result.get("lifestyleImpact") or []
    if lifestyle:
        lines.append("## 生活方式建议\n")
        for item in lifestyle:
            lines.append(f"### {item.get('key', '')}\n")
            lines.append(f"{item.get('val', '')}\n")

    recommendations = result.get("personalizedRecommendations") or []
    if recommendations:
        lines.append("## 个性化建议\n")
        for item in recommendations:
            lines.append(f"### {item.get('key', '')}\n")
            lines.append(f"{item.get('val', '')}\n")

    review = result.get("regularReview") or []
    if review:
        lines.append("## 复查计划\n")
        for item in review:
            lines.append(f"### {item.get('key', '')}\n")
            lines.append(f"{item.get('val', '')}\n")

    refs = result.get("references") or []
    if refs:
        lines.append("## 参考文献\n")
        seen_titles = set()
        count = 0
        for ref in refs:
            title = ref.get("title", "")
            link = ref.get("link", "")
            if title in seen_titles:
                continue
            seen_titles.add(title)
            count += 1
            if count > 5:
                break
            if link:
                lines.append(f"{count}. [{title}]({link})")
            else:
                lines.append(f"{count}. {title}")
        lines.append("")

    lines.append("---\n")
    lines.append("> ⚠️ 本报告由 AI 生成，仅供参考，不构成医疗诊断或治疗建议。如有健康问题请咨询专业医生。\n")

    return "\n".join(lines)


# ===========================================================================
# Sub-command: submit
# ===========================================================================

def cmd_submit(args):
    """Submit local files or a PDF URL for analysis. Prints taskId on success."""
    has_url = bool(args.url)
    has_files = bool(args.files)

    if not has_url and not has_files:
        print("[!] Error: must provide --url or --file (mutually exclusive).")
        return 1

    if has_url and has_files:
        print("[!] Error: --url and --file are mutually exclusive. Use one or the other.")
        return 1

    if has_files:
        for fp in args.files:
            if not os.path.isfile(fp):
                print(f"[!] File not found: {fp}")
                return 1
            ext = os.path.splitext(fp)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                print(f"[!] Unsupported file format: {ext} (file: {fp})")
                print(f"    Supported: {', '.join(SUPPORTED_FORMATS)}")
                return 1
            size_mb = os.path.getsize(fp) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                print(f"[!] File too large: {fp} ({size_mb:.1f} MB, max {MAX_FILE_SIZE_MB} MB)")
                return 1

    if has_files:
        request_data: dict = {"url": "", "member_id": args.member_id or ""}
        if args.questionnaire:
            request_data["questionnaire"] = 1
        print(f"[*] Uploading local files for analysis:")
        for fp in args.files:
            print(f"    - {fp}")
        resp = _post_multipart(
            f"{DEFAULT_SERVICE_URL}/api/report/upload",
            request_data, args.files,
        )
    else:
        print(f"[*] Submitting PDF for analysis: {args.url}")
        payload: dict = {"url": args.url}
        if args.questionnaire:
            payload["questionnaire"] = args.questionnaire
        if args.member_id:
            payload["memberId"] = args.member_id
        resp = _post_json(f"{DEFAULT_SERVICE_URL}/api/report/upload", payload)

    if resp is None:
        print("[!] Failed to submit task.")
        return 1

    task_id = resp.get("data", {}).get("taskId", "")
    if not task_id:
        print("[!] No taskId returned.")
        return 1

    print(f"[+] Task submitted successfully.")
    print(f"TASK_ID={task_id}")
    return 0


# ===========================================================================
# Sub-command: start
# ===========================================================================

def cmd_start(args):
    """Start interpretation for a given taskId."""
    print(f"[*] Starting interpretation for task: {args.task_id}")
    resp = _post_json(
        f"{DEFAULT_SERVICE_URL}/api/report/startInterpret",
        {"taskId": args.task_id},
    )
    if resp is None:
        print("[!] Failed to start interpretation.")
        return 1

    print("[+] Interpretation started successfully.")
    print(f"TASK_ID={args.task_id}")
    return 0


# ===========================================================================
# Sub-command: query
# ===========================================================================

def cmd_query(args):
    """Query task status. Prints status, progress, and result if finished."""
    resp = _post_json(
        f"{DEFAULT_SERVICE_URL}/api/report/query",
        {"taskId": args.task_id},
    )
    if resp is None:
        print("[!] Failed to query task.")
        return 1

    data   = resp.get("data", {})
    status = data.get("status", "unknown")
    pct    = data.get("process", 0)
    ctime  = data.get("processingCompletionTime", "")

    print(f"STATUS={status}")
    print(f"PROGRESS={pct}")

    if status == "finish":
        if ctime:
            print(f"COMPLETED_AT={ctime}")
        result = data.get("result") or {}
        if result:
            print(f"HAS_RESULT=true")
            print(f"HAS_ABNORMAL={str(result.get('hasAbnormalValues', False)).lower()}")
        else:
            print(f"HAS_RESULT=false")
    elif status == "failed":
        print("[!] Task failed on server side.")
        return 1

    return 0


# ===========================================================================
# Sub-command: save
# ===========================================================================

def cmd_save(args):
    """Query the finished result and save to disk as .md."""
    resp = _post_json(
        f"{DEFAULT_SERVICE_URL}/api/report/query",
        {"taskId": args.task_id},
    )
    if resp is None:
        print("[!] Failed to query task.")
        return 1

    data   = resp.get("data", {})
    status = data.get("status", "")

    if status != "finish":
        print(f"[!] Task is not finished yet. Current status: {status}")
        return 1

    result = data.get("result") or {}
    if not result:
        print("[!] Task finished but no result data returned.")
        return 1

    if args.output:
        out_dir = Path(args.output)
    else:
        out_dir = _default_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_stem = args.name if args.name else args.task_id
    stem = Path(raw_stem).name.replace("..", "")
    if not stem:
        stem = args.task_id
    ctime = data.get("processingCompletionTime", "")

    md_content = _format_result_markdown(result, completed_at=ctime)
    md_path = out_dir / f"{stem}.md"
    if md_path.exists():
        counter = 1
        while (out_dir / f"{stem}_{counter}.md").exists():
            counter += 1
        md_path = out_dir / f"{stem}_{counter}.md"
        print(f"[!] Name conflict, saving as: {md_path.name}")
    md_path.write_text(md_content, encoding="utf-8")
    print(f"[+] Report saved: {md_path}")
    print(f"REPORT_PATH={md_path}")

    return 0


# ===========================================================================
# CLI entry point
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="WiseAnalyze CLI — Medical Checkup Report Analysis (powered by WiseDiag)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sub-commands:
  submit  Submit a PDF URL, get taskId
  start   Start interpretation for a taskId
  query   Check task status and progress
  save    Save finished result to disk (.md)

Examples:
  python3 wise_analyze.py submit -u "https://example.com/report.pdf"
  python3 wise_analyze.py start  -t "c1ecce57-4c9b-4f87-ba94-b81f8404c503"
  python3 wise_analyze.py query  -t "c1ecce57-4c9b-4f87-ba94-b81f8404c503"
  python3 wise_analyze.py save   -t "c1ecce57-4c9b-4f87-ba94-b81f8404c503" -n "张三体检报告"
        """,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- submit ---
    p_submit = subparsers.add_parser("submit", help="Submit PDF URL or local files for analysis")
    p_submit.add_argument(
        "-u", "--url", default=None, metavar="URL",
        help="Publicly accessible URL of the PDF checkup report",
    )
    p_submit.add_argument(
        "-f", "--file", action="append", dest="files", metavar="PATH",
        help="Local file path to upload (PDF/image, repeat for multiple files)",
    )
    p_submit.add_argument(
        "-q", "--questionnaire", default=None, metavar="TEXT",
        help="Health questionnaire text (symptoms, family history, etc.)",
    )
    p_submit.add_argument(
        "-m", "--member-id", default=None, metavar="ID",
        help="Health profile member ID",
    )

    # --- start ---
    p_start = subparsers.add_parser("start", help="Start interpretation")
    p_start.add_argument(
        "-t", "--task-id", required=True, metavar="ID",
        help="Task ID from submit step",
    )

    # --- query ---
    p_query = subparsers.add_parser("query", help="Query task status")
    p_query.add_argument(
        "-t", "--task-id", required=True, metavar="ID",
        help="Task ID to query",
    )

    # --- save ---
    p_save = subparsers.add_parser("save", help="Save finished result to disk")
    p_save.add_argument(
        "-t", "--task-id", required=True, metavar="ID",
        help="Task ID to save",
    )
    p_save.add_argument(
        "-n", "--name", default=None,
        help="Output filename stem (default: taskId)",
    )
    p_save.add_argument(
        "-o", "--output", default=None,
        help="Output directory (default: current working directory)",
    )

    args = parser.parse_args()

    handlers = {
        "submit": cmd_submit,
        "start":  cmd_start,
        "query":  cmd_query,
        "save":   cmd_save,
    }
    sys.exit(handlers[args.command](args))


if __name__ == "__main__":
    main()
