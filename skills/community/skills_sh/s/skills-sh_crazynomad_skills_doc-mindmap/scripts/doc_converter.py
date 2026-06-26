#!/usr/bin/env python3
"""
Doc Converter - 批量文档转 Markdown 工具

使用 markitdown 将办公文档（PDF、PPT、Word、Excel 等）批量转换为 Markdown，
通过本地 Ollama 模型生成摘要，生成 CSV 索引供 Claude 后续思维导图分类。
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# 支持的文件格式
SUPPORTED_EXTENSIONS = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".csv", ".html", ".htm", ".epub",
    ".json", ".xml",
}

# 扫描时排除的目录
EXCLUDED_DIRS = {
    ".git", ".svn", ".hg",
    ".cache", ".npm", ".yarn", ".pnpm",
    ".venv", "venv", "env", ".env",
    "__pycache__", ".pytest_cache",
    "node_modules", "vendor", "packages",
    "Library", ".Trash",
    ".idea", ".vscode", ".vs",
    "build", "dist", "target", "out",
    ".summaries",
}


@dataclass
class DocInfo:
    """文档信息"""
    original_path: str
    file_type: str
    file_size: int
    file_size_human: str = ""
    md5: str = ""
    is_duplicate: bool = False
    duplicate_of: str = ""
    markdown_path: str = ""
    conversion_status: str = "pending"
    error_message: str = ""
    converted_at: str = ""


@dataclass
class ConvertReport:
    """转换报告"""
    scan_time: str
    source_paths: list = field(default_factory=list)
    documents: list = field(default_factory=list)
    total_files: int = 0
    total_size_bytes: int = 0
    total_size_human: str = ""
    converted_count: int = 0
    failed_count: int = 0
    summaries_dir: str = ""


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def check_markitdown() -> bool:
    """检查 markitdown 是否已安装"""
    try:
        import markitdown  # noqa: F401
        return True
    except ImportError:
        return False


# Ollama 配置
OLLAMA_API_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"

SUMMARY_SYSTEM_PROMPT = "你是文档摘要助手。直接输出摘要内容，不要任何思考过程，不要输出多余的解释。"

SUMMARY_USER_PROMPT = """请为以下文档内容生成一份简明的中文摘要，格式要求：

1. 一句话概括核心内容
2. 3-5 个要点（每个要点一句话）
3. 3-5 个关键词

文档名: {filename}
文档类型: {filetype}

文档内容:
{content}

请严格按以下 Markdown 格式输出，不要输出其他内容：

**核心内容**: （一句话概括）

## 要点

- 要点 1
- 要点 2
- 要点 3

## 关键词

`关键词1` `关键词2` `关键词3`"""

# 摘要时截取的最大字符数，避免超出模型上下文
MAX_CONTENT_CHARS = 8000

CLASSIFY_SYSTEM_PROMPT = "你是文档分类助手。严格按要求的 JSON 格式输出，不要任何思考过程和多余文字。"

CLASSIFY_USER_PROMPT = """请为以下文档摘要进行三维度分类，并建议一个更清晰的文件名。

文档名: {filename}
摘要内容:
{brief}

请完成：
1. 按主题: 文档核心主题（2-6个字，如：AI技术、数据治理、运维方案、营销策略）
2. 按用途: 工作场景用途（2-6个字，如：培训材料、客户交付方案、售前方案、市场营销、内部参考）
3. 按客户: 所属客户或适用对象（2-6个字，如：沃尔沃、一汽集团、通用方案、内部使用）
4. 建议文件名: 根据文档内容建议一个简洁、有意义的中文文件名（不含扩展名，10-25个字符）
   - 格式参考: "沃尔沃DMS三年运维优化方案"、"AI驱动产品管理培训指南"
   - 如果原始文件名已经足够清晰，可以保留原名

严格按以下 JSON 格式输出，不要输出其他内容：
{{"topic": "主题分类", "usage": "用途分类", "client": "客户分类", "suggested_name": "建议文件名"}}"""


def check_ollama(model: str = DEFAULT_MODEL) -> tuple[bool, str]:
    """检查 Ollama 服务和模型是否可用"""
    import requests
    try:
        resp = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
        if resp.status_code != 200:
            return False, "Ollama 服务未响应"
        models = [m["name"] for m in resp.json().get("models", [])]
        # 检查模型是否存在（支持 "qwen3:4b" 匹配 "qwen3:4b" 或 "qwen3:4b-xxx"）
        base_name = model.split(":")[0] if ":" in model else model
        found = any(model in m or base_name in m for m in models)
        if not found:
            return False, f"模型 {model} 未安装，请运行: ollama pull {model}"
        return True, ""
    except requests.ConnectionError:
        return False, "Ollama 未启动，请运行: ollama serve"
    except Exception as e:
        return False, f"Ollama 检查失败: {e}"


def ollama_summarize(content: str, filename: str, filetype: str,
                     model: str = DEFAULT_MODEL) -> str:
    """使用 Ollama 本地模型生成摘要（通过 chat API 避免 thinking 模式干扰）"""
    import requests
    # 截取内容避免超出模型上下文
    truncated = content[:MAX_CONTENT_CHARS]
    if len(content) > MAX_CONTENT_CHARS:
        truncated += f"\n\n... (内容已截取前 {MAX_CONTENT_CHARS} 字符，原文共 {len(content)} 字符)"

    user_prompt = SUMMARY_USER_PROMPT.format(
        filename=filename,
        filetype=filetype,
        content=truncated,
    )

    resp = requests.post(
        f"{OLLAMA_API_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 1024},
        },
        timeout=120,
    )
    resp.raise_for_status()
    msg = resp.json().get("message", {})
    content = msg.get("content", "").strip()
    # Qwen3 等 thinking 模型可能把内容放在 thinking 字段
    if not content and msg.get("thinking"):
        content = msg["thinking"].strip()
    return content


def ollama_classify(brief: str, filename: str,
                    model: str = DEFAULT_MODEL) -> dict:
    """使用 Ollama 对文档进行三维度分类，返回 {topic, usage, client}"""
    import requests

    user_prompt = CLASSIFY_USER_PROMPT.format(filename=filename, brief=brief)

    resp = requests.post(
        f"{OLLAMA_API_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": CLASSIFY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 256},
        },
        timeout=60,
    )
    resp.raise_for_status()
    msg = resp.json().get("message", {})
    content = msg.get("content", "").strip()
    if not content and msg.get("thinking"):
        content = msg["thinking"].strip()

    # 从返回内容中提取 JSON
    try:
        # 处理可能包含 ```json 代码块的情况
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content.strip())
    except (json.JSONDecodeError, IndexError):
        return {"topic": "未分类", "usage": "未分类", "client": "未分类",
                "suggested_name": ""}


class DocConverter:
    """文档批量转换器"""

    def __init__(self, paths: list[str]):
        self.paths = [os.path.expanduser(p) for p in paths]
        self.documents: list[DocInfo] = []

    def _should_exclude(self, path: Path) -> bool:
        """检查是否应该排除该路径"""
        for part in path.parts:
            if part in EXCLUDED_DIRS:
                return True
        return False

    def _get_summaries_dir(self) -> str:
        """获取 .summaries 输出目录（基于第一个路径）"""
        first = Path(self.paths[0])
        if first.is_file():
            base = first.parent
        else:
            base = first
        return str(base / ".summaries")

    def scan(self) -> list[DocInfo]:
        """扫描所有路径，收集支持的文档"""
        self.documents = []

        for path_str in self.paths:
            path = Path(path_str)

            if not path.exists():
                print(f"  ⚠️  路径不存在: {path_str}")
                continue

            if path.is_file():
                self._add_file(path)
            elif path.is_dir():
                self._scan_dir(path)

        # 按文件大小降序排序
        self.documents.sort(key=lambda d: d.file_size, reverse=True)
        self._detect_duplicates()
        return self.documents

    def _scan_dir(self, directory: Path):
        """递归扫描目录"""
        try:
            for item in sorted(directory.iterdir()):
                if item.is_dir():
                    if item.name.startswith(".") or item.name in EXCLUDED_DIRS:
                        continue
                    self._scan_dir(item)
                elif item.is_file():
                    self._add_file(item)
        except PermissionError:
            print(f"  ⚠️  无权限访问: {directory}")

    def _add_file(self, path: Path):
        """添加单个文件"""
        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            return

        try:
            size = path.stat().st_size
        except OSError:
            return

        doc = DocInfo(
            original_path=str(path),
            file_type=ext,
            file_size=size,
            file_size_human=format_size(size),
            md5=self._file_md5(path),
        )
        self.documents.append(doc)

    @staticmethod
    def _file_md5(path: Path) -> str:
        """计算文件 MD5"""
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _detect_duplicates(self):
        """通过 MD5 检测重复文件"""
        seen: dict[str, str] = {}  # md5 -> first file path
        for doc in self.documents:
            if doc.md5 in seen:
                doc.is_duplicate = True
                doc.duplicate_of = seen[doc.md5]
            else:
                seen[doc.md5] = doc.original_path

    def preview(self, use_json: bool = False) -> ConvertReport:
        """预览模式：列出将要转换的文档"""
        if not self.documents:
            self.scan()

        report = ConvertReport(
            scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source_paths=self.paths,
            documents=self.documents,
            total_files=len(self.documents),
            total_size_bytes=sum(d.file_size for d in self.documents),
            summaries_dir=self._get_summaries_dir(),
        )
        report.total_size_human = format_size(report.total_size_bytes)

        # 重复文件统计
        duplicates = [d for d in self.documents if d.is_duplicate]

        if use_json:
            print(json.dumps({
                "scan_time": report.scan_time,
                "source_paths": report.source_paths,
                "total_files": report.total_files,
                "total_size": report.total_size_human,
                "duplicates": len(duplicates),
                "summaries_dir": report.summaries_dir,
                "documents": [
                    {
                        "path": d.original_path,
                        "type": d.file_type,
                        "size": d.file_size_human,
                        "size_bytes": d.file_size,
                        "md5": d.md5,
                        "is_duplicate": d.is_duplicate,
                        "duplicate_of": d.duplicate_of,
                    }
                    for d in self.documents
                ],
            }, indent=2, ensure_ascii=False))
        else:
            print(f"📂 扫描路径: {', '.join(self.paths)}")
            print(f"📊 找到 {report.total_files} 个文档, 共 {report.total_size_human}")
            print(f"📁 输出目录: {report.summaries_dir}")
            print("")

            # 按文件类型分组统计
            by_type: dict[str, list[DocInfo]] = {}
            for doc in self.documents:
                by_type.setdefault(doc.file_type, []).append(doc)

            type_icons = {
                ".pdf": "📄", ".pptx": "📊", ".docx": "📝",
                ".xlsx": "📈", ".xls": "📈", ".csv": "📈",
                ".html": "🌐", ".htm": "🌐", ".epub": "📚",
                ".json": "📋", ".xml": "📋",
            }

            for ext, docs in sorted(by_type.items(), key=lambda x: -len(x[1])):
                icon = type_icons.get(ext, "📄")
                total_size = sum(d.file_size for d in docs)
                print(f"  {icon} {ext}: {len(docs)} 个, {format_size(total_size)}")

            if self.documents:
                print("")
                print("📋 文件列表:")
                for i, doc in enumerate(self.documents, 1):
                    icon = type_icons.get(doc.file_type, "📄")
                    name = Path(doc.original_path).name
                    dup_tag = " ⚠️ 重复" if doc.is_duplicate else ""
                    print(f"  {i:3d}. {icon} {name} ({doc.file_size_human}){dup_tag}")

            # 展示重复文件详情
            if duplicates:
                dup_size = sum(d.file_size for d in duplicates)
                print("")
                print(f"⚠️  发现 {len(duplicates)} 个重复文件 (MD5 相同)，"
                      f"可释放 {format_size(dup_size)}:")
                for doc in duplicates:
                    dup_name = Path(doc.original_path).name
                    orig_name = Path(doc.duplicate_of).name
                    print(f"  - {dup_name} == {orig_name}  [{doc.md5[:8]}...]")
                print("")
                print("💡 建议删除重复文件，可运行:")
                for doc in duplicates:
                    print(f'  rm "{doc.original_path}"')

        return report

    def convert(self, use_json: bool = False) -> ConvertReport:
        """执行转换"""
        if not self.documents:
            self.scan()

        if not self.documents:
            print("ℹ️  没有可转换的文档")
            return ConvertReport(
                scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                source_paths=self.paths,
            )

        # 检查 markitdown
        if not check_markitdown():
            print("❌ markitdown 未安装")
            print("   请运行: pip install 'markitdown[all]'")
            sys.exit(1)

        from markitdown import MarkItDown

        md_converter = MarkItDown()

        # 创建输出目录
        summaries_dir = self._get_summaries_dir()
        converted_dir = os.path.join(summaries_dir, "converted")
        briefs_dir = os.path.join(summaries_dir, "briefs")
        os.makedirs(converted_dir, exist_ok=True)
        os.makedirs(briefs_dir, exist_ok=True)

        report = ConvertReport(
            scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source_paths=self.paths,
            documents=self.documents,
            total_files=len(self.documents),
            total_size_bytes=sum(d.file_size for d in self.documents),
            summaries_dir=summaries_dir,
        )
        report.total_size_human = format_size(report.total_size_bytes)

        if not use_json:
            print(f"🔄 开始转换 {report.total_files} 个文档...")
            print(f"📁 输出目录: {summaries_dir}")
            print("")

        for i, doc in enumerate(self.documents, 1):
            name = Path(doc.original_path).stem
            ext = doc.file_type
            md_filename = f"{name}{ext}.md"
            md_path = os.path.join(converted_dir, md_filename)

            if not use_json:
                print(f"  [{i}/{report.total_files}] 转换: {Path(doc.original_path).name}...", end=" ")

            # 跳过重复文件
            if doc.is_duplicate:
                doc.conversion_status = "skipped_duplicate"
                if not use_json:
                    print(f"⏭️  重复 (同 {Path(doc.duplicate_of).name})")
                continue

            try:
                result = md_converter.convert(doc.original_path)
                content = result.text_content if result.text_content else ""

                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(f"# {name}\n\n")
                    f.write(f"> 原始文件: {doc.original_path}\n")
                    f.write(f"> 文件类型: {ext} | 大小: {doc.file_size_human}\n")
                    f.write(f"> 转换时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")
                    f.write(content)

                doc.markdown_path = md_path
                doc.conversion_status = "success"
                doc.converted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                report.converted_count += 1

                if not use_json:
                    print("✅")

            except Exception as e:
                doc.conversion_status = "failed"
                doc.error_message = str(e)
                report.failed_count += 1

                if not use_json:
                    print(f"❌ {e}")

        # 生成 CSV 索引
        csv_path = os.path.join(summaries_dir, "index.csv")
        self._write_csv(csv_path)

        if use_json:
            print(json.dumps({
                "scan_time": report.scan_time,
                "source_paths": report.source_paths,
                "total_files": report.total_files,
                "total_size": report.total_size_human,
                "converted": report.converted_count,
                "failed": report.failed_count,
                "summaries_dir": summaries_dir,
                "index_csv": csv_path,
                "documents": [
                    {
                        "original_path": d.original_path,
                        "markdown_path": d.markdown_path,
                        "file_type": d.file_type,
                        "size": d.file_size_human,
                        "status": d.conversion_status,
                        "error": d.error_message,
                    }
                    for d in self.documents
                ],
            }, indent=2, ensure_ascii=False))
        else:
            print("")
            print(f"✅ 转换完成: {report.converted_count} 成功, {report.failed_count} 失败")
            print(f"📄 CSV 索引: {csv_path}")
            print(f"📁 Markdown 文件: {converted_dir}")
            print(f"📁 摘要目录（待 Claude 生成）: {briefs_dir}")

        return report

    def summarize(self, model: str = DEFAULT_MODEL,
                  use_json: bool = False) -> dict:
        """使用 Ollama 为已转换的 Markdown 文件生成摘要"""
        summaries_dir = self._get_summaries_dir()
        converted_dir = os.path.join(summaries_dir, "converted")
        briefs_dir = os.path.join(summaries_dir, "briefs")
        os.makedirs(briefs_dir, exist_ok=True)

        # 收集已转换的 md 文件
        if not os.path.isdir(converted_dir):
            msg = f"转换目录不存在: {converted_dir}，请先运行 --convert"
            if use_json:
                print(json.dumps({"error": msg}, ensure_ascii=False))
            else:
                print(f"❌ {msg}")
            return {"error": msg}

        md_files = sorted(Path(converted_dir).glob("*.md"))
        if not md_files:
            msg = "没有找到已转换的 Markdown 文件"
            if use_json:
                print(json.dumps({"error": msg}, ensure_ascii=False))
            else:
                print(f"ℹ️  {msg}")
            return {"error": msg}

        if not use_json:
            print(f"🤖 使用模型 {model} 生成摘要...")
            print(f"📁 摘要输出: {briefs_dir}")
            print(f"📄 待处理: {len(md_files)} 个文件")
            print("")

        results = []
        success_count = 0
        fail_count = 0

        for i, md_file in enumerate(md_files, 1):
            name = md_file.stem  # e.g. "report.pdf"
            brief_path = os.path.join(briefs_dir, f"{name}.brief.md")

            if not use_json:
                print(f"  [{i}/{len(md_files)}] 摘要: {md_file.name}...", end=" ",
                      flush=True)

            try:
                content = md_file.read_text(encoding="utf-8")
                # 跳过空内容
                if len(content.strip()) < 50:
                    if not use_json:
                        print("⏭️  内容过少，跳过")
                    results.append({"file": md_file.name, "status": "skipped",
                                    "reason": "内容过少"})
                    continue

                # 提取文件类型（从文件名如 report.pdf.md 中取 .pdf）
                parts = name.rsplit(".", 1)
                filetype = f".{parts[-1]}" if len(parts) > 1 else ""

                summary = ollama_summarize(content, name, filetype, model)

                # 写入摘要文件
                with open(brief_path, "w", encoding="utf-8") as f:
                    f.write(f"# {name} 摘要\n\n")
                    f.write(f"**文件类型**: {filetype} | ")
                    f.write(f"**模型**: {model}\n\n")
                    f.write(summary)
                    f.write("\n")

                success_count += 1
                results.append({"file": md_file.name, "status": "success",
                                "brief_path": brief_path})

                if not use_json:
                    print("✅")

            except Exception as e:
                fail_count += 1
                results.append({"file": md_file.name, "status": "failed",
                                "error": str(e)})
                if not use_json:
                    print(f"❌ {e}")

        summary_result = {
            "model": model,
            "total": len(md_files),
            "success": success_count,
            "failed": fail_count,
            "briefs_dir": briefs_dir,
            "results": results,
        }

        if use_json:
            print(json.dumps(summary_result, indent=2, ensure_ascii=False))
        else:
            print("")
            print(f"✅ 摘要完成: {success_count} 成功, {fail_count} 失败")
            print(f"📁 摘要文件: {briefs_dir}")

        return summary_result

    def organize(self, model: str = DEFAULT_MODEL,
                 use_json: bool = False, rename: bool = False) -> dict:
        """读取摘要，用 Ollama 分类，通过软链接生成三套目录结构"""
        summaries_dir = self._get_summaries_dir()
        briefs_dir = os.path.join(summaries_dir, "briefs")
        schemes_dir = os.path.join(summaries_dir, "schemes")

        if not os.path.isdir(briefs_dir):
            msg = f"摘要目录不存在: {briefs_dir}，请先运行 --summarize"
            if use_json:
                print(json.dumps({"error": msg}, ensure_ascii=False))
            else:
                print(f"❌ {msg}")
            return {"error": msg}

        brief_files = sorted(Path(briefs_dir).glob("*.brief.md"))
        if not brief_files:
            msg = "没有找到摘要文件"
            if use_json:
                print(json.dumps({"error": msg}, ensure_ascii=False))
            else:
                print(f"ℹ️  {msg}")
            return {"error": msg}

        # 收集原始文件路径映射（brief stem 如 "DMS.pptx" -> 原始路径）
        if not self.documents:
            self.scan()
        orig_map: dict[str, str] = {}
        for doc in self.documents:
            # brief 文件名格式: {stem}{ext}.brief.md，stem 对应 {name}{ext}
            key = Path(doc.original_path).stem + doc.file_type
            orig_map[key] = doc.original_path

        if not use_json:
            print(f"🗂️  使用模型 {model} 进行三维度分类...")
            print(f"📁 分类输出: {schemes_dir}")
            print(f"📄 待分类: {len(brief_files)} 个文件")
            print("")

        # 分类结果: [{filename, original_path, topic, usage, client}, ...]
        classifications = []

        for i, bf in enumerate(brief_files, 1):
            # brief stem: "DMS.pptx"  (从 "DMS.pptx.brief.md" 去掉 ".brief")
            doc_key = bf.stem.replace(".brief", "")
            orig_path = orig_map.get(doc_key, "")

            if not use_json:
                print(f"  [{i}/{len(brief_files)}] 分类: {doc_key}...",
                      end=" ", flush=True)

            try:
                brief_content = bf.read_text(encoding="utf-8")
                cats = ollama_classify(brief_content, doc_key, model)
                cats["filename"] = doc_key
                cats["original_path"] = orig_path
                classifications.append(cats)

                if not use_json:
                    suggested = cats.get("suggested_name", "")
                    print(f"✅ 主题:{cats.get('topic','')} | "
                          f"用途:{cats.get('usage','')} | "
                          f"客户:{cats.get('client','')}")
                    if suggested:
                        print(f"          📝 建议文件名: {suggested}")
            except Exception as e:
                classifications.append({
                    "filename": doc_key, "original_path": orig_path,
                    "topic": "未分类", "usage": "未分类", "client": "未分类",
                    "suggested_name": "",
                })
                if not use_json:
                    print(f"❌ {e}")

        # 创建三套软链接目录
        scheme_names = {
            "by-topic": "topic",
            "by-usage": "usage",
            "by-client": "client",
        }
        scheme_labels = {
            "by-topic": "按主题",
            "by-usage": "按用途",
            "by-client": "按客户",
        }

        # 清理旧的 schemes 目录
        import shutil
        if os.path.exists(schemes_dir):
            shutil.rmtree(schemes_dir)

        link_count = 0
        for scheme_dir, cat_key in scheme_names.items():
            for item in classifications:
                if not item["original_path"]:
                    continue
                category = item.get(cat_key, "未分类")
                cat_dir = os.path.join(schemes_dir, scheme_dir, category)
                os.makedirs(cat_dir, exist_ok=True)

                src = os.path.abspath(item["original_path"])
                # 使用建议文件名或原始文件名
                orig_name = Path(src).name
                if rename and item.get("suggested_name"):
                    ext = Path(src).suffix
                    link_name = item["suggested_name"] + ext
                else:
                    link_name = orig_name
                dst = os.path.join(cat_dir, link_name)
                if not os.path.exists(dst):
                    os.symlink(src, dst)
                    link_count += 1

        if not use_json:
            print("")
            rename_tag = "（使用建议文件名）" if rename else ""
            print(f"✅ 分类完成，共创建 {link_count} 个软链接{rename_tag}")
            print(f"📁 分类目录: {schemes_dir}")
            print("")
            for scheme_dir, cat_key in scheme_names.items():
                label = scheme_labels[scheme_dir]
                scheme_path = os.path.join(schemes_dir, scheme_dir)
                if os.path.isdir(scheme_path):
                    cats = sorted(os.listdir(scheme_path))
                    print(f"  🗂️  {label} ({scheme_dir}/)")
                    for cat in cats:
                        cat_path = os.path.join(scheme_path, cat)
                        count = len(os.listdir(cat_path))
                        print(f"      📁 {cat}/ ({count} 个)")
                    print("")
        else:
            print(json.dumps({
                "model": model,
                "schemes_dir": schemes_dir,
                "total_links": link_count,
                "classifications": classifications,
            }, indent=2, ensure_ascii=False))

        return {
            "schemes_dir": schemes_dir,
            "total_links": link_count,
            "classifications": classifications,
        }

    def _write_csv(self, csv_path: str):
        """写入 CSV 索引"""
        fieldnames = [
            "original_path", "markdown_path", "file_type",
            "file_size", "md5", "is_duplicate", "duplicate_of",
            "conversion_status", "error_message", "converted_at",
        ]

        with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for doc in self.documents:
                writer.writerow({
                    "original_path": doc.original_path,
                    "markdown_path": doc.markdown_path,
                    "file_type": doc.file_type,
                    "file_size": doc.file_size,
                    "md5": doc.md5,
                    "is_duplicate": doc.is_duplicate,
                    "duplicate_of": doc.duplicate_of,
                    "conversion_status": doc.conversion_status,
                    "error_message": doc.error_message,
                    "converted_at": doc.converted_at,
                })


def main():
    parser = argparse.ArgumentParser(
        description="Doc Converter - 批量文档转 Markdown 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s ~/Documents/reports --preview              # 预览文档列表
  %(prog)s ~/Documents/reports --convert --confirm     # 执行转换
  %(prog)s ~/Documents/reports --summarize             # 用 Ollama 生成摘要
  %(prog)s ~/Documents/reports --organize              # 三维度分类 + 软链接
  %(prog)s ~/Documents/reports --organize --rename     # 分类 + 优化文件名
  %(prog)s ~/Documents/reports --summarize --model qwen3:8b  # 指定模型
  %(prog)s file1.pdf file2.pptx --convert --confirm    # 转换指定文件
  %(prog)s ~/Documents --preview --json                # JSON 格式预览

支持格式: .pdf, .pptx, .docx, .xlsx, .xls, .csv, .html, .epub, .json, .xml
        """
    )

    parser.add_argument("paths", nargs="+", help="文件或目录路径")
    parser.add_argument("--preview", action="store_true", help="预览模式，列出文档")
    parser.add_argument("--convert", action="store_true", help="执行转换")
    parser.add_argument("--summarize", action="store_true",
                        help="使用 Ollama 本地模型生成摘要（需先 --convert）")
    parser.add_argument("--organize", action="store_true",
                        help="三维度分类并生成软链接目录（需先 --summarize）")
    parser.add_argument("--rename", action="store_true",
                        help="软链接使用 AI 建议的优化文件名（配合 --organize）")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Ollama 模型名称（默认: {DEFAULT_MODEL}）")
    parser.add_argument("--confirm", action="store_true", help="确认执行（安全机制）")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if not args.preview and not args.convert and not args.summarize and not args.organize:
        parser.print_help()
        return

    converter = DocConverter(args.paths)

    if args.preview:
        converter.preview(use_json=args.json)
        return

    if args.convert:
        if not args.confirm:
            print("❌ 转换需要 --confirm 参数确认")
            print("   请先使用 --preview 预览，确认后添加 --confirm 执行转换")
            return

        # 先检查 markitdown
        if not check_markitdown():
            print("❌ markitdown 未安装")
            print("   请运行: pip install 'markitdown[all]'")
            sys.exit(1)

        converter.convert(use_json=args.json)

    if args.summarize:
        # 检查 Ollama
        ok, err = check_ollama(args.model)
        if not ok:
            print(f"❌ {err}")
            sys.exit(1)

        converter.summarize(model=args.model, use_json=args.json)

    if args.organize:
        # 检查 Ollama
        ok, err = check_ollama(args.model)
        if not ok:
            print(f"❌ {err}")
            sys.exit(1)

        converter.organize(model=args.model, use_json=args.json,
                           rename=args.rename)


if __name__ == "__main__":
    main()
