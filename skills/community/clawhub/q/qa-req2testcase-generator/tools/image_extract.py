#!/usr/bin/env python3
"""
T1-01：图片抽取模块 image_extract.py
从 docx 文件中抽取图片，建立章节映射，输出结构化 JSON。

功能：
- 双路径遍历：w:drawing（inline/anchor）+ w:object/v:imagedata（VML/OLE）
- 表格中图片检测（w:tc 中的 drawing/object）
- EMF 格式自动转 PNG
- 章节映射 + before_text/after_text/caption 提取
- 图片去重（同 MD5）
- 输出 JSON 严格对齐方案 §7

依赖：python-docx, lxml, Pillow（可选，EMF 转换）
"""

import json
import os
import sys
import time
import hashlib
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field, asdict

try:
    from docx import Document
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml.ns import qn
    from lxml import etree
except ImportError:
    print("❌ 依赖缺失，正在安装 python-docx lxml ...")
    os.system(f"{sys.executable} -m pip install python-docx lxml -q")
    from docx import Document
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml.ns import qn
    from lxml import etree


# ============================================================
# 命名空间定义
# ============================================================

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'v': 'urn:schemas-microsoft-com:vml',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'o': 'urn:schemas-microsoft-com:office:office',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


# ============================================================
# 数据结构（对齐方案 §7）
# ============================================================

@dataclass
class ExtractedImage:
    """单张图片抽取结果"""
    image_id: str                    # IMG-001 格式
    file_path: str                   # 图片保存路径
    filename: str                    # 原始文件名
    content_type: str                # MIME 类型
    size_bytes: int                  # 文件大小
    content_hash: str                # MD5 哈希
    embed_method: str                # inline / anchor / vml_ole / table_embedded / unreferenced
    section: str = ""                # 所属章节标题
    before_text: str = ""            # 图片前文本（≤200字）
    after_text: str = ""             # 图片后文本（≤200字）
    caption: str = ""                # 图注（如有）
    in_table: bool = False           # 是否在表格中
    table_row: int = -1              # 表格行号
    table_col: int = -1              # 表格列号
    reference_count: int = 1         # 引用次数（去重后）
    is_duplicate: bool = False       # 是否为重复图片
    duplicate_of: str = ""           # 重复的原始图片 ID
    emf_converted: bool = False      # 是否经过 EMF→PNG 转换
    extraction_status: str = "ok"    # ok / partial / failed / conversion_failed
    error_message: str = ""          # 错误信息


@dataclass
class ExtractionResult:
    """图片抽取总结果"""
    schema_version: str = "1.4.0"
    source_file: str = ""
    output_dir: str = ""
    total_images_in_rels: int = 0    # relationships 中的图片总数
    total_extracted: int = 0         # 成功抽取数
    unique_images: int = 0           # 去重后唯一图片数
    duplicate_count: int = 0         # 重复图片数
    emf_converted_count: int = 0     # EMF 转换数
    sections_found: List[str] = field(default_factory=list)
    images: List[dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    elapsed_seconds: float = 0.0


# ============================================================
# EMF 转换工具
# ============================================================

def convert_emf_to_png(emf_blob: bytes, output_path: str) -> bool:
    """
    将 EMF 格式图片转换为 PNG。
    优先使用 libreoffice，备选 Pillow。
    返回 True 表示转换成功。
    """
    # I-FIX-10: 改用 TemporaryDirectory 避免临时文件残留
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_emf = os.path.join(tmp_dir, 'input.emf')
        with open(tmp_emf, 'wb') as f:
            f.write(emf_blob)

        # 方式1：libreoffice 转换
        try:
            result = subprocess.run(
                ['libreoffice', '--headless', '--convert-to', 'png', tmp_emf, '--outdir', tmp_dir],
                capture_output=True, text=True, timeout=30
            )
            converted = os.path.join(tmp_dir, 'input.png')
            if os.path.exists(converted):
                import shutil
                shutil.copy2(converted, output_path)
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方式2：Pillow 尝试
        try:
            from PIL import Image
            img = Image.open(tmp_emf)
            img.save(output_path, 'PNG')
            return True
        except Exception:
            pass

        # 方式3：直接复制原始文件（降级）
        import shutil
        shutil.copy2(tmp_emf, output_path.replace('.png', '.emf'))
        return False


# ============================================================
# 核心抽取器
# ============================================================

class DocxImageExtractor:
    """
    docx 图片抽取器。
    双路径遍历 + 表格检测 + EMF 转换 + 章节映射 + 去重。
    """

    def __init__(self, docx_path: str, output_dir: str = None):
        """
        Args:
            docx_path: docx 文件路径
            output_dir: 图片输出目录，默认为 docx 同目录下的 assets/images/
        """
        self.docx_path = docx_path
        self.doc = Document(docx_path)
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(docx_path) or '.', 'assets', 'images'
        )
        os.makedirs(self.output_dir, exist_ok=True)

        self._images: List[ExtractedImage] = []
        self._found_rids: set = set()
        self._md5_map: Dict[str, str] = {}  # md5 → first image_id
        self._image_counter = 0

    def _next_image_id(self) -> str:
        """生成下一个图片 ID"""
        self._image_counter += 1
        return f"IMG-{self._image_counter:03d}"

    def _get_all_images_from_rels(self) -> Dict[str, dict]:
        """从 relationships 获取所有图片资源"""
        images = {}
        for rel in self.doc.part.rels.values():
            if "image" in rel.reltype:
                rId = rel.rId
                image_part = rel.target_part
                blob = image_part.blob
                md5 = hashlib.md5(blob).hexdigest()
                images[rId] = {
                    "rId": rId,
                    "filename": image_part.partname.split("/")[-1],
                    "content_type": image_part.content_type,
                    "size_bytes": len(blob),
                    "md5": md5,
                    "blob": blob,
                }
        return images

    def _save_image(self, img_info: dict, image_id: str) -> str:
        """
        保存图片到输出目录。EMF 自动转 PNG。
        I-FIX-14: EMF转换失败时重试1次（先libreoffice后PIL）。
        返回保存后的文件路径。
        """
        filename = img_info["filename"]
        content_type = img_info["content_type"]
        blob = img_info["blob"]
        is_emf = (content_type and 'emf' in content_type.lower()) or filename.lower().endswith('.emf')

        if is_emf:
            # EMF → PNG 转换（I-FIX-14: 内置重试逻辑已在 convert_emf_to_png 中实现）
            png_filename = f"{image_id}.png"
            png_path = os.path.join(self.output_dir, png_filename)
            success = convert_emf_to_png(blob, png_path)
            if success:
                return png_path
            else:
                # 转换失败，保存原始 EMF
                emf_path = os.path.join(self.output_dir, f"{image_id}.emf")
                with open(emf_path, 'wb') as f:
                    f.write(blob)
                return emf_path
        else:
            # 非 EMF，直接保存
            ext = os.path.splitext(filename)[1] or '.png'
            save_filename = f"{image_id}{ext}"
            save_path = os.path.join(self.output_dir, save_filename)
            with open(save_path, 'wb') as f:
                f.write(blob)
            return save_path

    def _get_current_heading(self, element) -> str:
        """
        从当前元素向前追溯最近的 Heading 段落。
        遍历 body 子元素，找到 element 之前最近的标题。
        """
        body = self.doc.element.body
        current_heading = ""
        for child in body:
            # 检查是否是标题段落
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag == "p":
                pPr = child.find(qn("w:pPr"))
                if pPr is not None:
                    pStyle = pPr.find(qn("w:pStyle"))
                    if pStyle is not None:
                        style_val = pStyle.get(qn("w:val"), "")
                        if "Heading" in style_val or "heading" in style_val or style_val.startswith("TOC"):
                            # 提取标题文本
                            texts = []
                            for t in child.iter(qn("w:t")):
                                if t.text:
                                    texts.append(t.text)
                            heading_text = "".join(texts).strip()
                            if heading_text:
                                current_heading = heading_text
            # 检查是否到达目标元素
            if child is element or self._element_contains(child, element):
                return current_heading
        return current_heading

    def _element_contains(self, parent, target) -> bool:
        """检查 parent 元素是否包含 target"""
        for desc in parent.iter():
            if desc is target:
                return True
        return False

    def _get_surrounding_text(self, para_element) -> Tuple[str, str, str]:
        """
        获取段落前后文本和图注。
        返回 (before_text, after_text, caption)
        """
        body = self.doc.element.body
        paragraphs = list(body.iter(qn("w:p")))

        para_idx = -1
        for i, p in enumerate(paragraphs):
            if p is para_element:
                para_idx = i
                break

        before_text = ""
        after_text = ""
        caption = ""

        # 前文：向前找最近的非空段落
        if para_idx > 0:
            for i in range(para_idx - 1, max(para_idx - 5, -1), -1):
                texts = []
                for t in paragraphs[i].iter(qn("w:t")):
                    if t.text:
                        texts.append(t.text)
                text = "".join(texts).strip()
                if text:
                    before_text = text[:200]
                    break

        # 后文 + 图注检测：向后找
        if para_idx >= 0 and para_idx < len(paragraphs) - 1:
            for i in range(para_idx + 1, min(para_idx + 5, len(paragraphs))):
                texts = []
                for t in paragraphs[i].iter(qn("w:t")):
                    if t.text:
                        texts.append(t.text)
                text = "".join(texts).strip()
                if text:
                    # 检测图注（以"图"开头，如"图3-2 xxx"）
                    if not caption and (text.startswith("图") or text.startswith("Figure")):
                        caption = text[:200]
                    elif not after_text:
                        after_text = text[:200]
                    if after_text and caption:
                        break

        return before_text, after_text, caption

    def _check_table_position(self, element) -> Tuple[bool, int, int]:
        """检查元素是否在表格中，返回 (in_table, row, col)"""
        for ancestor in element.iterancestors():
            tag = ancestor.tag.split("}")[-1] if "}" in ancestor.tag else ancestor.tag
            if tag == "tc":
                row_idx = -1
                col_idx = -1
                tr = ancestor.getparent()
                if tr is not None:
                    tbl = tr.getparent()
                    if tbl is not None:
                        rows = tbl.findall(qn("w:tr"))
                        for ri, r in enumerate(rows):
                            if r is tr:
                                row_idx = ri
                                cells = r.findall(qn("w:tc"))
                                for ci, c in enumerate(cells):
                                    if c is ancestor:
                                        col_idx = ci
                                        break
                                break
                return True, row_idx, col_idx
        return False, -1, -1

    def _determine_embed_method(self, drawing_element) -> str:
        """判断 drawing 元素的嵌入方式"""
        inline = drawing_element.find(qn("wp:inline"))
        anchor = drawing_element.find(qn("wp:anchor"))
        if inline is not None:
            return "inline"
        elif anchor is not None:
            return "anchor"
        return "inline"  # 默认 inline

    def _add_image(self, img_info: dict, embed_method: str,
                   para_element=None, in_table: bool = False,
                   table_row: int = -1, table_col: int = -1,
                   errors: list = None) -> Optional[ExtractedImage]:
        """
        添加一张图片到结果列表。处理去重和 EMF 转换。
        """
        md5 = img_info["md5"]
        content_type = img_info["content_type"]
        is_emf = (content_type and 'emf' in content_type.lower()) or \
                 img_info["filename"].lower().endswith('.emf')

        # 去重检查
        if md5 in self._md5_map:
            # 找到重复图片，增加引用计数
            original_id = self._md5_map[md5]
            for img in self._images:
                if img.image_id == original_id:
                    img.reference_count += 1
                    break

            # 创建重复记录（标记为 duplicate）
            image_id = self._next_image_id()
            dup_img = ExtractedImage(
                image_id=image_id,
                file_path="",
                filename=img_info["filename"],
                content_type=content_type,
                size_bytes=img_info["size_bytes"],
                content_hash=md5,
                embed_method=embed_method,
                in_table=in_table,
                table_row=table_row,
                table_col=table_col,
                is_duplicate=True,
                duplicate_of=original_id,
            )
            # 章节映射
            if para_element is not None:
                dup_img.section = self._get_current_heading(para_element)
                dup_img.before_text, dup_img.after_text, dup_img.caption = \
                    self._get_surrounding_text(para_element)

            self._images.append(dup_img)
            return dup_img

        # 非重复图片，保存并记录
        image_id = self._next_image_id()
        self._md5_map[md5] = image_id

        # 保存图片文件
        file_path = self._save_image(img_info, image_id)
        emf_converted = is_emf and file_path.endswith('.png')

        extracted = ExtractedImage(
            image_id=image_id,
            file_path=file_path,
            filename=img_info["filename"],
            content_type=content_type,
            size_bytes=img_info["size_bytes"],
            content_hash=md5,
            embed_method=embed_method,
            in_table=in_table,
            table_row=table_row,
            table_col=table_col,
            emf_converted=emf_converted,
        )

        # EMF 转换失败检测
        if is_emf and not emf_converted:
            extracted.extraction_status = "conversion_failed"
            extracted.error_message = "EMF 转 PNG 失败，保留原始 EMF 文件"
            if errors is not None:
                errors.append(f"EMF 转换失败: {img_info['filename']}")

        # 章节映射和上下文
        if para_element is not None:
            extracted.section = self._get_current_heading(para_element)
            extracted.before_text, extracted.after_text, extracted.caption = \
                self._get_surrounding_text(para_element)

        self._images.append(extracted)
        return extracted

    def extract(self) -> ExtractionResult:
        """
        执行完整图片抽取流程。
        返回 ExtractionResult 对象。
        """
        start_time = time.time()
        result = ExtractionResult(
            source_file=self.docx_path,
            output_dir=self.output_dir,
        )

        # Step 1: 获取所有图片资源
        all_images = self._get_all_images_from_rels()
        result.total_images_in_rels = len(all_images)

        if not all_images:
            result.errors.append("文档中没有找到图片资源")
            result.elapsed_seconds = time.time() - start_time
            return result

        # Step 2: 收集所有章节标题
        for para in self.doc.paragraphs:
            if para.style and para.style.name and "Heading" in para.style.name:
                if para.text.strip():
                    result.sections_found.append(para.text.strip())

        # Step 3: 遍历 body 子元素（段落 + 表格），双路径抽取
        body = self.doc.element.body
        for child in body:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

            if tag == "p":
                # 段落中的图片
                self._extract_from_paragraph(child, all_images, result.errors)

            elif tag == "tbl":
                # 表格中的图片
                self._extract_from_table(child, all_images, result.errors)

        # Step 4: 检查遗漏（relationships 中有但未被引用的图片）
        missed_rids = set(all_images.keys()) - self._found_rids
        for rId in missed_rids:
            img_info = all_images[rId]
            image_id = self._next_image_id()

            # 去重检查
            md5 = img_info["md5"]
            if md5 in self._md5_map:
                # 已有相同内容的图片，跳过
                continue

            self._md5_map[md5] = image_id
            file_path = self._save_image(img_info, image_id)
            is_emf = img_info["content_type"] and 'emf' in img_info["content_type"].lower()

            extracted = ExtractedImage(
                image_id=image_id,
                file_path=file_path,
                filename=img_info["filename"],
                content_type=img_info["content_type"],
                size_bytes=img_info["size_bytes"],
                content_hash=md5,
                embed_method="unreferenced",
                section="(未找到引用位置)",
                extraction_status="partial",
                error_message="图片存在于 relationships 但未在正文中找到引用",
                emf_converted=is_emf and file_path.endswith('.png'),
            )
            self._images.append(extracted)
            result.errors.append(
                f"⚠️ 图片 rId={rId} ({img_info['filename']}) 未在正文中找到引用"
            )

        # Step 5: 汇总统计
        unique_images = [img for img in self._images if not img.is_duplicate]
        duplicates = [img for img in self._images if img.is_duplicate]
        emf_converted = [img for img in self._images if img.emf_converted]

        result.total_extracted = len([
            img for img in self._images
            if img.extraction_status in ("ok", "conversion_failed")
            and not img.is_duplicate
        ])
        result.unique_images = len(unique_images)
        result.duplicate_count = len(duplicates)
        result.emf_converted_count = len(emf_converted)
        result.images = [asdict(img) for img in self._images]
        result.elapsed_seconds = time.time() - start_time

        return result

    def _extract_from_paragraph(self, para_element, all_images: dict, errors: list):
        """从段落中抽取图片（方式A: w:drawing + 方式B: w:object/v:imagedata）"""

        # === 方式A：w:drawing（inline / anchor）===
        for drawing in para_element.iter(qn("w:drawing")):
            blip = drawing.find(".//" + qn("a:blip"))
            if blip is None:
                continue

            rId = blip.get(qn("r:embed"))
            if rId is None:
                continue

            if rId not in all_images:
                errors.append(f"rId={rId} 在 relationships 中未找到")
                continue

            self._found_rids.add(rId)
            img_info = all_images[rId]
            embed_method = self._determine_embed_method(drawing)

            # 检查是否在表格中
            in_table, row, col = self._check_table_position(para_element)
            if in_table:
                embed_method = "table_embedded"

            self._add_image(
                img_info, embed_method,
                para_element=para_element,
                in_table=in_table, table_row=row, table_col=col,
                errors=errors
            )

        # === 方式B：w:object + v:imagedata（VML/OLE）===
        for obj in para_element.iter(qn("w:object")):
            for imagedata in obj.iter('{urn:schemas-microsoft-com:vml}imagedata'):
                rid = imagedata.get(
                    '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
                )
                if not rid or rid not in all_images:
                    if rid:
                        errors.append(f"VML rId={rid} 在 relationships 中未找到")
                    continue

                self._found_rids.add(rid)
                img_info = all_images[rid]

                in_table, row, col = self._check_table_position(para_element)
                embed_method = "table_embedded" if in_table else "vml_ole"

                self._add_image(
                    img_info, embed_method,
                    para_element=para_element,
                    in_table=in_table, table_row=row, table_col=col,
                    errors=errors
                )

    def _extract_from_table(self, tbl_element, all_images: dict, errors: list):
        """从表格中补充抽取遗漏的图片"""
        rows = tbl_element.findall(qn("w:tr"))
        for ri, row in enumerate(rows):
            cells = row.findall(qn("w:tc"))
            for ci, cell in enumerate(cells):
                for para in cell.iter(qn("w:p")):
                    # 方式A：w:drawing
                    for drawing in para.iter(qn("w:drawing")):
                        blip = drawing.find(".//" + qn("a:blip"))
                        if blip is None:
                            continue
                        rId = blip.get(qn("r:embed"))
                        if rId and rId in all_images and rId not in self._found_rids:
                            self._found_rids.add(rId)
                            self._add_image(
                                all_images[rId], "table_embedded",
                                para_element=para,
                                in_table=True, table_row=ri, table_col=ci,
                                errors=errors
                            )

                    # 方式B：w:object + v:imagedata
                    for obj in para.iter(qn("w:object")):
                        for imagedata in obj.iter('{urn:schemas-microsoft-com:vml}imagedata'):
                            rid = imagedata.get(
                                '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
                            )
                            if rid and rid in all_images and rid not in self._found_rids:
                                self._found_rids.add(rid)
                                self._add_image(
                                    all_images[rid], "table_embedded",
                                    para_element=para,
                                    in_table=True, table_row=ri, table_col=ci,
                                    errors=errors
                                )


# ============================================================
# 公共接口
# ============================================================

def extract_images(docx_path: str, output_dir: str = None) -> dict:
    """
    从 docx 文件抽取图片的公共接口。

    Args:
        docx_path: docx 文件路径
        output_dir: 图片输出目录（可选）

    Returns:
        ExtractionResult 的字典形式
    """
    if not os.path.exists(docx_path):
        return asdict(ExtractionResult(
            source_file=docx_path,
            errors=[f"文件不存在: {docx_path}"]
        ))

    try:
        extractor = DocxImageExtractor(docx_path, output_dir)
        result = extractor.extract()
        return asdict(result)
    except Exception as e:
        return asdict(ExtractionResult(
            source_file=docx_path,
            errors=[f"抽取异常: {str(e)}"]
        ))


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="docx 图片抽取工具")
    parser.add_argument("docx_path", help="docx 文件路径")
    parser.add_argument("--output-dir", "-o", help="图片输出目录")
    parser.add_argument("--json-output", "-j", help="JSON 结果输出路径")
    args = parser.parse_args()

    result = extract_images(args.docx_path, args.output_dir)

    # 输出 JSON
    json_output = args.json_output or os.path.join(
        os.path.dirname(args.docx_path) or '.', 'image_extract_result.json'
    )
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 打印摘要
    print(f"📊 图片抽取完成:")
    print(f"  文档: {result['source_file']}")
    print(f"  图片总数: {result['total_images_in_rels']}")
    print(f"  成功抽取: {result['total_extracted']}")
    print(f"  唯一图片: {result['unique_images']}")
    print(f"  重复图片: {result['duplicate_count']}")
    print(f"  EMF 转换: {result['emf_converted_count']}")
    print(f"  耗时: {result['elapsed_seconds']:.3f}s")
    print(f"  结果: {json_output}")
