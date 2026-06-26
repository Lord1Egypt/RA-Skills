"""MCP Server 主实现"""
import sys
import json
import base64
import re
import os
from pathlib import Path
from typing import Any, Dict, Optional

from config import Config, get_config
from wiz_open_api import WizOpenApi
from note_parser_factory import NoteParserFactory
from note import Note
from wiz_logging import get_logger

logger = get_logger()


class WizMCPServer:
    """为知笔记 MCP Server"""

    def __init__(self):
        self.config: Optional[Config] = None
        self.api: Optional[WizOpenApi] = None

    def initialize(self, config: Config):
        """初始化 Server"""
        self.config = config
        self.api = WizOpenApi(config)
        logger.info("WizMCP Server 初始化完成")

    def handle_request(self, request: dict) -> dict:
        """处理 JSON-RPC 请求"""
        method = request.get("method")
        request_id = request.get("id")

        if method == "initialize":
            return self._handle_initialize(request_id)
        elif method == "notifications/initialized":
            return self._handle_notifications_initialized(request_id)
        elif method == "tools/list":
            return self._handle_tools_list(request_id)
        elif method == "tools/call":
            return self._handle_tools_call(request_id, request.get("params", {}))
        else:
            return self._error_response(request_id, -32601, f"Method not found: {method}")

    def _handle_initialize(self, request_id: Any) -> dict:
        """处理 initialize 请求"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "wiz-mcp",
                    "version": "1.0.0"
                }
            }
        }

    def _handle_notifications_initialized(self, request_id: Any) -> dict:
        """处理 notifications/initialized 请求"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {}
        }

    def _handle_tools_list(self, request_id: Any) -> dict:
        """处理 tools/list 请求"""
        tools = [
            {
                "name": "wiz_list_notes",
                "description": "列出笔记元数据",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_version": {
                            "type": "integer",
                            "description": "起始版本号，默认0"
                        },
                        "count": {
                            "type": "integer",
                            "description": "返回数量，默认50，范围1-200",
                            "default": 50
                        }
                    }
                }
            },
            {
                "name": "wiz_search_notes",
                "description": "调用官方搜索接口搜索笔记",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词（必填）"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "wiz_get_note",
                "description": "读取笔记正文（支持下载图片/附件到本地）",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "doc_guid": {
                            "type": "string",
                            "description": "笔记GUID（必填）"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "html", "both"],
                            "description": "返回格式，默认markdown",
                            "default": "markdown"
                        },
                        "include_info": {
                            "type": "boolean",
                            "description": "是否包含笔记信息，默认true",
                            "default": True
                        },
                        "include_resources": {
                            "type": "boolean",
                            "description": "是否下载图片/附件到本地，默认true",
                            "default": True
                        },
                        "include_extracted_text": {
                            "type": "boolean",
                            "description": "是否抽取附件文本（OCR/解析），默认false",
                            "default": False
                        },
                        "max_extract_chars": {
                            "type": "integer",
                            "description": "抽取文本总长度上限，默认20000，0不限",
                            "default": 20000
                        },
                        "max_extract_chars_per_item": {
                            "type": "integer",
                            "description": "单文件抽取上限，默认5000，0不限",
                            "default": 5000
                        },
                        "ocr_lang": {
                            "type": "string",
                            "description": "OCR语言参数，默认chi_sim+eng",
                            "default": "chi_sim+eng"
                        }
                    },
                    "required": ["doc_guid"]
                }
            },
            {
                "name": "wiz_list_attachments",
                "description": "列出笔记附件",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "doc_guid": {
                            "type": "string",
                            "description": "笔记GUID（必填）"
                        },
                        "note_type": {
                            "type": "string",
                            "description": "笔记类型（可选，用于协作笔记回退）"
                        }
                    },
                    "required": ["doc_guid"]
                }
            },
            {
                "name": "wiz_download_attachment",
                "description": "下载附件",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "kind": {
                            "type": "string",
                            "enum": ["normal", "collaboration_resource"],
                            "description": "附件类型，默认normal",
                            "default": "normal"
                        },
                        "doc_guid": {
                            "type": "string",
                            "description": "笔记GUID（必填）"
                        },
                        "att_guid": {
                            "type": "string",
                            "description": "普通附件GUID"
                        },
                        "name": {
                            "type": "string",
                            "description": "附件名称（仅回显/清理换行）"
                        },
                        "src": {
                            "type": "string",
                            "description": "协作资源标识"
                        }
                    },
                    "required": ["doc_guid"]
                }
            },
            {
                "name": "wiz_create_note",
                "description": "创建笔记（支持从URL导入Markdown）",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "笔记标题"
                        },
                        "content": {
                            "type": "string",
                            "description": "笔记内容（Markdown格式）"
                        },
                        "url": {
                            "type": "string",
                            "description": "URL地址，将自动抓取并转换为Markdown"
                        },
                        "category": {
                            "type": "string",
                            "description": "分类路径，默认 /My Notes/",
                            "default": "/My Notes/"
                        },
                        "tags": {
                            "type": "string",
                            "description": "标签，逗号分隔"
                        }
                    }
                }
            }
        ]

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }

    def _handle_tools_call(self, request_id: Any, params: dict) -> dict:
        """处理 tools/call 请求"""
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})

        try:
            if tool_name == "wiz_list_notes":
                result = self._tool_wiz_list_notes(tool_args)
            elif tool_name == "wiz_search_notes":
                result = self._tool_wiz_search_notes(tool_args)
            elif tool_name == "wiz_get_note":
                result = self._tool_wiz_get_note(tool_args)
            elif tool_name == "wiz_list_attachments":
                result = self._tool_wiz_list_attachments(tool_args)
            elif tool_name == "wiz_download_attachment":
                result = self._tool_wiz_download_attachment(tool_args)
            elif tool_name == "wiz_create_note":
                result = self._tool_wiz_create_note(tool_args)
            else:
                return self._error_response(request_id, -32601, f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False)
                        }
                    ]
                }
            }

        except Exception as e:
            logger.error(f"工具执行失败: {tool_name}, error: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({"error": str(e)}, ensure_ascii=False)
                        }
                    ],
                    "isError": True
                }
            }

    def _tool_wiz_list_notes(self, args: dict) -> dict:
        """wiz_list_notes 工具"""
        start_version = args.get("start_version", 0)
        count = min(max(args.get("count", 50), 1), 200)

        result = self.api.get_note_list(start_version, count)

        # API 直接返回数组或 {notes: [...], next_version: n}
        if isinstance(result, list):
            notes = result
            next_version = None
        else:
            notes = result.get("notes", []) if isinstance(result, dict) else []
            next_version = result.get("next_version") if isinstance(result, dict) else None

        return {
            "notes": notes,
            "next_version": next_version
        }

    def _tool_wiz_search_notes(self, args: dict) -> dict:
        """wiz_search_notes 工具 - 调用官方搜索接口"""
        query = args.get("query", "")

        if not query:
            raise ValueError("query 是必填参数")

        matches = self.api.search_notes(query, with_abstract=True, with_favor=False)

        return {
            "matches": matches,
            "next_version": None
        }

    def _tool_wiz_get_note(self, args: dict) -> dict:
        """wiz_get_note 工具"""
        doc_guid = args.get("doc_guid")
        format_type = args.get("format", "markdown")
        include_info = args.get("include_info", True)
        include_resources = args.get("include_resources", True)
        include_extracted_text = args.get("include_extracted_text", False)
        max_extract_chars = args.get("max_extract_chars", 20000)
        max_extract_chars_per_item = args.get("max_extract_chars_per_item", 5000)
        ocr_lang = args.get("ocr_lang", "chi_sim+eng")

        if not doc_guid:
            raise ValueError("doc_guid 是必填参数")

        # 如果开启文本抽取，强制下载资源
        if include_extracted_text:
            include_resources = True

        # 先获取笔记详情判断类型
        detail = self.api.get_note_detail(doc_guid)
        info = detail.get("info", {})
        note_type = info.get("type", "")
        title = info.get("title", "无标题")

        result = {
            "doc_guid": doc_guid,
            "type": note_type
        }

        if include_info:
            result["info"] = info

        # 获取原始内容
        is_collab = Note.is_collaboration_note(note_type)

        if is_collab:
            # 协作笔记
            editor_token = self.api.get_collaboration_token(doc_guid)
            collab_json = self.api.get_collaboration_content(editor_token, doc_guid)

            origin_content = collab_json

            if format_type in ("markdown", "both"):
                from collaboration_note_parser import CollaborationNoteParser
                parser = CollaborationNoteParser()
                result["markdown"] = parser.parse_content(collab_json)

            if format_type == "html":
                # 协作笔记返回 JSON 原文
                result["html"] = collab_json
            elif format_type == "both":
                result["html"] = collab_json

            # 下载协作笔记的资源
            if include_resources:
                resources_info = self._download_collaboration_resources(doc_guid, title)
                result["resources"] = resources_info["resources"]
                result["markdown"] = self._replace_resource_paths(
                    result.get("markdown", ""),
                    resources_info["replace_map"]
                )
        else:
            # 普通笔记
            origin_content = self.api.get_note_content(doc_guid)

            if format_type in ("markdown", "both"):
                parser = NoteParserFactory.create_parser(note_type)
                result["markdown"] = parser.parse_content(origin_content)

            if format_type in ("html", "both"):
                result["html"] = origin_content

            # 下载普通笔记的资源
            if include_resources:
                resources_info = self._download_note_resources(doc_guid, title)
                result["resources"] = resources_info["resources"]
                result["markdown"] = self._replace_resource_paths(
                    result.get("markdown", ""),
                    resources_info["replace_map"]
                )

        # 文本抽取
        if include_extracted_text and result.get("resources"):
            extract_result = self._extract_artifacts_text(
                result.get("resources", []),
                max_extract_chars,
                max_extract_chars_per_item,
                ocr_lang
            )
            result["extracted"] = extract_result["extracted"]
            result["bundle_text"] = self._build_bundle_text(
                result.get("markdown", ""),
                extract_result["extracted"],
                max_extract_chars
            )

        return result

    def _download_note_resources(self, doc_guid: str, title: str) -> dict:
        """下载普通笔记的资源（图片/附件）"""
        resources = self.api.get_note_resources(doc_guid)

        output_dir = Path(__file__).parent.parent / "output" / "notes" / doc_guid
        downloaded_resources = []
        replace_map = {}

        # 先过滤资源，收集有效资源
        valid_resources = []
        for res in resources:
            name = res.get("name", "")
            url = res.get("url", "")
            res_type = res.get("type", "attachment")

            if not name or not url:
                continue

            # 过滤非必要资源：name 是纯 GUID 格式的不是有效文件
            import re
            if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', name, re.I):
                continue

            valid_resources.append(res)

        # 如果没有有效资源，直接返回
        if not valid_resources:
            return {
                "resources": [],
                "replace_map": {}
            }

        # 创建目录
        images_dir = output_dir / "images"
        attachments_dir = output_dir / "attachments"
        images_dir.mkdir(parents=True, exist_ok=True)
        attachments_dir.mkdir(parents=True, exist_ok=True)

        for res in valid_resources:
            name = res.get("name", "")
            url = res.get("url", "")

            try:
                # 判断是图片还是附件
                ext = name.lower().split('.')[-1] if '.' in name else ''
                image_exts = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']

                if ext in image_exts:
                    # 图片
                    save_dir = images_dir
                    save_path = save_dir / name
                    rel_path = f"output/notes/{doc_guid}/images/{name}"
                else:
                    # 附件
                    save_dir = attachments_dir
                    save_path = save_dir / name
                    rel_path = f"output/notes/{doc_guid}/attachments/{name}"

                # 下载并保存
                content = self.api.download_resource(url)
                with open(save_path, "wb") as f:
                    f.write(content)

                downloaded_resources.append({
                    "name": name,
                    "path": str(save_path),
                    "relative_path": rel_path,
                    "type": "image" if ext in image_exts else "attachment"
                })

                # 记录替换映射（原路径 -> 新路径）
                replace_map[name] = rel_path
                logger.info(f"下载资源: {name} -> {rel_path}")

            except Exception as e:
                logger.warning(f"下载资源失败: {name}, error: {e}")

        return {
            "resources": downloaded_resources,
            "replace_map": replace_map
        }

    def _download_collaboration_resources(self, doc_guid: str, title: str) -> dict:
        """下载协作笔记的资源（图片/drawio等）"""
        # 获取协作笔记的 JSON 内容，提取 embed 信息
        editor_token = self.api.get_collaboration_token(doc_guid)
        collab_json = self.api.get_collaboration_content(editor_token, doc_guid)

        import json
        try:
            data = json.loads(collab_json)
            blocks = data.get("data", {}).get("data", {}).get("blocks", [])
        except:
            blocks = []

        # 先收集有效资源
        valid_resources = []
        for block in blocks:
            if block.get("type") != "embed":
                continue

            embed_type = block.get("embedType", "")
            embed_data = block.get("embedData", {})

            if embed_type in ("image", "office", "drawio"):
                src = embed_data.get("src", "")
                file_name = embed_data.get("fileName", src)
                if src:
                    valid_resources.append({
                        "type": embed_type,
                        "src": src,
                        "file_name": file_name
                    })

        # 如果没有有效资源，直接返回
        if not valid_resources:
            return {
                "resources": [],
                "replace_map": {}
            }

        # 创建目录
        output_dir = Path(__file__).parent.parent / "output" / "notes" / doc_guid
        images_dir = output_dir / "images"
        attachments_dir = output_dir / "attachments"
        images_dir.mkdir(parents=True, exist_ok=True)
        attachments_dir.mkdir(parents=True, exist_ok=True)

        downloaded_resources = []
        replace_map = {}

        for res in valid_resources:
            embed_type = res["type"]
            src = res["src"]
            file_name = res["file_name"]

            try:
                if embed_type == "image":
                    content = self.api.get_collaboration_image(doc_guid, src)
                    save_path = images_dir / file_name

                    rel_path = f"output/notes/{doc_guid}/images/{file_name}"
                    downloaded_resources.append({
                        "name": file_name,
                        "path": str(save_path),
                        "relative_path": rel_path,
                        "type": "image"
                    })

                    replace_map[src] = rel_path
                    logger.info(f"下载协作图片: {file_name}")

                elif embed_type in ("office", "drawio"):
                    content = self.api.download_collaboration_resource(editor_token, doc_guid, src)
                    save_path = attachments_dir / file_name

                    rel_path = f"output/notes/{doc_guid}/attachments/{file_name}"
                    downloaded_resources.append({
                        "name": file_name,
                        "path": str(save_path),
                        "relative_path": rel_path,
                        "type": embed_type
                    })

                    replace_map[src] = rel_path
                    logger.info(f"下载协作附件: {file_name}")

                with open(save_path, "wb") as f:
                    f.write(content)

            except Exception as e:
                logger.warning(f"下载协作资源失败: {src}, error: {e}")

        return {
            "resources": downloaded_resources,
            "replace_map": replace_map
        }

        return {
            "resources": downloaded_resources,
            "replace_map": replace_map
        }

    def _replace_resource_paths(self, markdown: str, replace_map: dict) -> str:
        """替换 Markdown 中的资源路径"""
        if not replace_map:
            return markdown

        for old_path, new_path in replace_map.items():
            # 替换各种格式的引用
            # ![name](old_path) -> ![name](new_path)
            # [name](wiz-collab-attachment://old_path) -> [name](new_path)
            # ![name](wiz-collab-attachment://old_path) -> ![name](new_path)

            # 处理 wiz-collab-attachment:// 协议
            markdown = markdown.replace(f"](wiz-collab-attachment://{old_path})", f"]({new_path})")
            markdown = markdown.replace(f"]({old_path})", f"]({new_path})")

        return markdown

    def _clamp_int(self, value: int, max_val: int) -> int:
        """限制整数在合理范围"""
        if max_val <= 0:
            return value
        return min(value, max_val)

    def _extract_image_ocr(self, file_path: str, ocr_lang: str) -> str:
        """对图片做 OCR"""
        try:
            from PIL import Image
            import pytesseract
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img, lang=ocr_lang)
            return text.strip()
        except Exception as e:
            return f"[OCR error: {e}]"

    def _extract_pdf_text(self, file_path: str) -> str:
        """抽取 PDF 文本"""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            texts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
            return "\n".join(texts)
        except Exception as e:
            return f"[PDF error: {e}]"

    def _extract_docx_text(self, file_path: str) -> str:
        """抽取 DOCX 文本（不使用 python-docx）"""
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            with zipfile.ZipFile(file_path, 'r') as z:
                with z.open('word/document.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    texts = []
                    for t in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                        if t.text:
                            texts.append(t.text)
                    return ''.join(texts)
        except Exception as e:
            return f"[DOCX error: {e}]"

    def _extract_text_file(self, file_path: str) -> str:
        """读取文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f"[Text error: {e}]"

    def _extract_artifacts_text(self, resources: list, max_total: int, max_per_item: int, ocr_lang: str) -> dict:
        """抽取所有附件文本"""
        extracted_items = []
        total_chars = 0

        for res in resources:
            name = res.get("name", "")
            file_path = res.get("path", "")
            rel_path = res.get("relative_path", "")
            res_type = res.get("type", "attachment")

            method = ""
            text = ""
            error = None

            try:
                ext = name.lower().split('.')[-1] if '.' in name else ''

                # 图片 OCR
                if ext in ('png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tif', 'tiff'):
                    method = "ocr"
                    text = self._extract_image_ocr(file_path, ocr_lang)

                # PDF
                elif ext == 'pdf':
                    method = "pdf"
                    text = self._extract_pdf_text(file_path)

                # DOCX
                elif ext in ('docx', 'doc'):
                    method = "docx"
                    text = self._extract_docx_text(file_path)

                # 文本文件
                elif ext in ('txt', 'md', 'log', 'json', 'yaml', 'yml', 'csv', 'xml', 'html', 'py', 'js', 'java', 'c', 'cpp', 'h', 'sh', 'bat', 'ps1'):
                    method = "text"
                    text = self._extract_text_file(file_path)

                else:
                    method = ""

            except Exception as e:
                error = str(e)

            chars = len(text)
            # 限制单文件长度
            if max_per_item > 0 and chars > max_per_item:
                text = text[:max_per_item]
                chars = len(text)

            extracted_items.append({
                "name": name,
                "relative_path": rel_path,
                "type": res_type,
                "method": method,
                "extracted_chars": chars,
                "extracted_text": text,
                "error": error
            })

            total_chars += chars

        # 限制总长度
        if max_total > 0 and total_chars > max_total:
            # 从后往前截断
            remaining = max_total
            for item in reversed(extracted_items):
                if item["extracted_chars"] <= remaining:
                    remaining -= item["extracted_chars"]
                else:
                    item["extracted_text"] = item["extracted_text"][:remaining]
                    item["extracted_chars"] = remaining
                    remaining = 0
                    break
            total_chars = sum(item["extracted_chars"] for item in extracted_items)

        return {
            "extracted": {
                "total_chars": total_chars,
                "items": extracted_items
            }
        }

    def _build_bundle_text(self, markdown: str, extracted: dict, max_total: int) -> str:
        """构建 bundle_text"""
        parts = [markdown]

        for item in extracted.get("items", []):
            if item.get("extracted_text"):
                parts.append(f"\n\n--- {item['name']} ({item['method']}) ---\n")
                parts.append(item["extracted_text"])

        result = "".join(parts)

        if max_total > 0 and len(result) > max_total:
            result = result[:max_total]

        return result

    def _tool_wiz_list_attachments(self, args: dict) -> dict:
        """wiz_list_attachments 工具"""
        doc_guid = args.get("doc_guid")
        note_type = args.get("note_type", "")

        if not doc_guid:
            raise ValueError("doc_guid 是必填参数")

        result = {
            "doc_guid": doc_guid,
            "note_type": note_type
        }

        try:
            attachments = self.api.get_note_attachments(doc_guid)

            if attachments:
                result["attachments"] = attachments
            elif note_type == "collaboration" and not attachments:
                # 协作笔记回退解析
                collab_result = self._parse_collaboration_attachments(doc_guid)
                result["collaboration"] = collab_result
            elif not attachments:
                # 非协作笔记没有附件
                result["attachments"] = []

        except Exception as e:
            if note_type == "collaboration":
                # 协作笔记回退解析
                collab_result = self._parse_collaboration_attachments(doc_guid)
                result["collaboration"] = collab_result
            else:
                raise Exception(f"获取附件列表失败: {e}")

        return result

    def _parse_collaboration_attachments(self, doc_guid: str) -> dict:
        """解析协作笔记的附件"""
        editor_token = self.api.get_collaboration_token(doc_guid)
        collab_json = self.api.get_collaboration_content(editor_token, doc_guid)

        from collaboration_note_parser import CollaborationNoteParser
        parser = CollaborationNoteParser()
        markdown = parser.parse_content(collab_json)

        # 解析 embeds
        json_data = json.loads(collab_json)
        embeds = []
        blocks = json_data.get("data", {}).get("data", {}).get("blocks", [])
        for block in blocks:
            if block.get("type") == "embed":
                embed_type = block.get("embedType", "")
                embed_data = block.get("embedData", {})
                embeds.append({
                    "embedType": embed_type,
                    "src": embed_data.get("src", ""),
                    "fileName": embed_data.get("fileName", "")
                })

        # 从 markdown 中提取 wiz-collab-attachment:// 链接（排除图片）
        attachment_names = []
        pattern = r'\[([^\]]+)\]\(wiz-collab-attachment://([^)]+)\)'
        for match in re.finditer(pattern, markdown):
            src = match.group(2)
            if src not in attachment_names:
                attachment_names.append(src)

        return {
            "attachment_names": attachment_names,
            "embeds": embeds
        }

    def _tool_wiz_download_attachment(self, args: dict) -> dict:
        """wiz_download_attachment 工具"""
        kind = args.get("kind", "normal")
        doc_guid = args.get("doc_guid")
        att_guid = args.get("att_guid")
        name = args.get("name", "")
        src = args.get("src")

        if not doc_guid:
            raise ValueError("doc_guid 是必填参数")

        # 清理 name 中的换行
        if name:
            name = name.replace("\n", " ").replace("\r", "")

        result = {
            "doc_guid": doc_guid
        }

        if kind == "normal":
            if not att_guid:
                raise ValueError("kind=normal 时，att_guid 是必填参数")

            binary_content = self.api.download_attachment(doc_guid, att_guid)
            result["att_guid"] = att_guid
            result["name"] = name
            result["kind"] = "normal"

        else:
            # collaboration_resource
            if not src:
                raise ValueError("kind=collaboration_resource 时，src 是必填参数")

            editor_token = self.api.get_collaboration_token(doc_guid)
            binary_content = self.api.download_collaboration_resource(editor_token, doc_guid, src)
            result["src"] = src
            result["name"] = name
            result["kind"] = "collaboration_resource"

        # 保存到 output/attach 目录
        if name:
            save_dir = Path(__file__).parent.parent / "output" / "attach"
            save_dir.mkdir(parents=True, exist_ok=True)
            file_path = save_dir / name
            with open(file_path, "wb") as f:
                f.write(binary_content)
            result["saved_path"] = str(file_path)

        # 转换为 base64
        result["base64"] = base64.b64encode(binary_content).decode("utf-8")

        return result

    def _tool_wiz_create_note(self, args: dict) -> dict:
        """wiz_create_note 工具 - 创建笔记"""
        title = args.get("title", "")
        content = args.get("content", "")
        url = args.get("url", "")
        category = args.get("category", "/My Notes/")
        tags = args.get("tags", "")

        final_url = url

        # 如果提供了 URL，则抓取网页内容
        if url:
            import requests
            from bs4 import BeautifulSoup
            import html2text
            import re

            logger.info(f"正在抓取 URL: {url}")

            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }

            try:
                response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
                response.raise_for_status()

                # 校验 content-type
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type.lower():
                    # 检查响应体是否以 < 开头
                    if not response.text.strip().startswith('<'):
                        raise Exception(f"非 HTML 响应: content-type={content_type}")

                # 获取最终跳转 URL
                final_url = response.url

                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # 提取标题
                if soup.title:
                    title = soup.title.string.strip() if soup.title.string else ""

                # 主内容节点选择
                main_content = None

                # 优先 article, main 且文本长度 > 200
                for tag in ['article', 'main']:
                    elem = soup.find(tag)
                    if elem and len(elem.get_text(strip=True)) > 200:
                        main_content = elem
                        break

                # 根据 id/class 关键字选择
                if not main_content:
                    keywords = ['content', 'article', 'post', 'thread', 'main', 'body', 'entry', 'text']
                    for keyword in keywords:
                        elems = soup.find_all(id=re.compile(keyword, re.I))
                        for elem in elems:
                            text_len = len(elem.get_text(strip=True))
                            if text_len > 200:
                                main_content = elem
                                break
                        if main_content:
                            break

                        elems = soup.find_all(class_=re.compile(keyword, re.I))
                        for elem in elems:
                            text_len = len(elem.get_text(strip=True))
                            if text_len > 200:
                                main_content = elem
                                break
                        if main_content:
                            break

                # fallback 到 body
                if not main_content:
                    main_content = soup.body if soup.body else soup

                # 使用 html2text 转 Markdown
                h = html2text.HTML2Text()
                h.ignore_images = False
                h.ignore_links = False
                h.body_width = 0

                # 设置 baseurl 以处理相对链接
                parsed_url = requests.compat.urlparse(final_url)
                baseurl = f"{parsed_url.scheme}://{parsed_url.netloc}"
                h.baseurl = baseurl

                markdown_content = h.handle(str(main_content))

                # 清理标题非法字符，确保 .md 结尾
                if title:
                    title = re.sub(r'[\\/:*?"<>|]', '', title)
                    if not title.endswith('.md'):
                        title = title + '.md'
                else:
                    title = "无标题.md"

                # Markdown 顶部追加来源
                if final_url:
                    markdown_content = f"[来源]({final_url})\n\n{markdown_content}"

                content = markdown_content
                logger.info(f"成功抓取 URL，内容长度: {len(content)}")

            except Exception as e:
                raise Exception(f"抓取 URL 失败: {e}")

        if not content:
            raise Exception("content 或 url 是必填参数")

        # 清理标题非法字符，确保 .md 结尾
        if title:
            import re
            title = re.sub(r'[\\/:*?"<>|]', '', title)
            if not title.endswith('.md'):
                title = title + '.md'
        else:
            title = "无标题.md"

        # Markdown 存 <pre> 格式
        escaped_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html_body = f"<pre>{escaped_content}</pre>"

        # 构建为知笔记的 HTML 格式
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style id="wiz_custom_css">html, body {{font-size: 12pt;}}body {{font-family: Helvetica, "Hiragino Sans GB", "微软雅黑", "Microsoft YaHei UI", SimSun, SimHei, arial, sans-serif;line-height: 1.6;margin: 0 auto;padding: 20px 16px;padding: 1.25rem 1rem;}}h1, h2, h3, h4, h5, h6 {{margin:20px 0 10px;margin:1.25rem 0 0.625rem;padding: 0;font-weight: bold;}}h1 {{font-size:20pt;font-size:1.67rem;}}h2 {{font-size:18pt;font-size:1.5rem;}}h3 {{font-size:15pt;font-size:1.25rem;}}h4 {{font-size:14pt;font-size:1.17rem;}}h5 {{font-size:12pt;font-size:1rem;}}h6 {{font-size:12pt;font-size:1rem;color: #777777;margin: 1rem 0;}}div, p, ul, ol, dl, li {{margin:0;}}blockquote, table, pre, code {{margin:8px 0;}}ul, ol {{padding-left:32px;padding-left:2rem;}}blockquote {{padding:0 12px;}}blockquote > :first-child {{margin-top:0;}}blockquote > :last-child {{margin-bottom:0;}}img {{border:0;max-width:100%;height:auto !important;margin:2px 0;}}table {{border-collapse:collapse;border:1px solid #bbbbbb;}}td, th {{padding:4px 8px;border-collapse:collapse;border:1px solid #bbbbbb;height:28px;word-break:break-all;box-sizing: border-box;}}</style>
</head>
<body>
{html_body}
</body>
</html>"""

        # 创建笔记
        result_data = self.api.create_note(title, html, category, tags)

        # 拿到 docGuid 后再调用一次 save_note 确保落库一致
        doc_guid = result_data.get("result", {}).get("docGuid", "")
        if doc_guid:
            try:
                self.api.save_note(doc_guid, title, html, category)
            except Exception as e:
                logger.warning(f"save_note 确认失败: {e}")

        # 返回结果
        return {
            "title": title,
            "category": category,
            "tags": tags,
            "url": final_url if final_url != url else (url if url else None),
            "doc_guid": doc_guid,
            "message": "笔记创建成功"
        }

    def _error_response(self, request_id: Any, code: int, message: str) -> dict:
        """返回错误响应"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }


def main():
    """主入口"""
    try:
        config = get_config()
        server = WizMCPServer()
        server.initialize(config)

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = server.handle_request(request)
                print(json.dumps(response, ensure_ascii=False), file=sys.stdout)
                sys.stdout.flush()
            except json.JSONDecodeError:
                # 跳过非 JSON 行
                continue
            except Exception as e:
                logger.error(f"处理请求失败: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {e}"
                    }
                }
                print(json.dumps(error_response, ensure_ascii=False), file=sys.stdout)
                sys.stdout.flush()

    except Exception as e:
        logger.error(f"Server 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
