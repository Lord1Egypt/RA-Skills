from __future__ import annotations
"""
format_converter.py - 文档格式转换模块

功能：
1. PDF 转 Word (.docx)
2. Word 转 PDF
3. Excel 转 PDF
4. 文本格式互转 (txt, md, rtf, csv)
5. 批量转换功能

使用：
    converter = FormatConverter()
    result = converter.convert("input.pdf", "output.docx")
    result = converter.convert("input.xlsx", "output.pdf")
"""

import os
import logging
import tempfile
from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ConversionStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"


class FileFormat(Enum):
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"
    PPT = "pptx"
    TXT = "txt"
    MD = "md"
    RTF = "rtf"
    CSV = "csv"
    HTML = "html"


@dataclass
class ConversionResult:
    success: bool
    status: ConversionStatus
    input_file: str
    output_file: str
    input_format: FileFormat
    output_format: FileFormat
    message: str = ""
    error: Optional[str] = None
    conversion_time: float = 0.0
    input_size: int = 0
    output_size: int = 0
    warnings: List[str] = field(default_factory=list)


class Converter(ABC):
    """转换器抽象基类"""

    @abstractmethod
    def can_convert(self, input_format: FileFormat, output_format: FileFormat) -> bool:
        """判断是否支持转换"""
        pass

    @abstractmethod
    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        """执行转换"""
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[tuple]:
        """获取支持的格式对"""
        pass


class PDFToWordConverter(Converter):
    """PDF 转 Word 转换器"""

    def can_convert(self, input_format: FileFormat, output_format: FileFormat) -> bool:
        return input_format == FileFormat.PDF and output_format == FileFormat.WORD

    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        import time
        start_time = time.time()

        try:
            from pdf2docx import Converter as Pdf2DocxConverter

            if not os.path.exists(input_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=FileFormat.PDF,
                    output_format=FileFormat.WORD,
                    error=f"输入文件不存在: {input_path}"
                )

            input_size = os.path.getsize(input_path)

            pdf_converter = Pdf2DocxConverter(input_path)
            pdf_converter.convert(output_path, start=0, end=None)
            pdf_converter.close()

            if not os.path.exists(output_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=FileFormat.PDF,
                    output_format=FileFormat.WORD,
                    error="转换失败，未生成输出文件"
                )

            conversion_time = time.time() - start_time
            output_size = os.path.getsize(output_path)

            return ConversionResult(
                success=True,
                status=ConversionStatus.SUCCESS,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.PDF,
                output_format=FileFormat.WORD,
                message=f"PDF 转 Word 成功",
                conversion_time=conversion_time,
                input_size=input_size,
                output_size=output_size
            )

        except ImportError:
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.PDF,
                output_format=FileFormat.WORD,
                error="缺少依赖: 请安装 pdf2docx (pip install pdf2docx)"
            )
        except Exception as e:
            logger.error(f"PDF 转 Word 失败: {e}")
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.PDF,
                output_format=FileFormat.WORD,
                error=str(e)
            )

    def get_supported_formats(self) -> List[tuple]:
        return [(FileFormat.PDF, FileFormat.WORD)]


class WordToPDFConverter(Converter):
    """Word 转 PDF 转换器"""

    def can_convert(self, input_format: FileFormat, output_format: FileFormat) -> bool:
        return input_format == FileFormat.WORD and output_format == FileFormat.PDF

    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        import time
        start_time = time.time()

        try:
            from docx2pdf import convert

            if not os.path.exists(input_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=FileFormat.WORD,
                    output_format=FileFormat.PDF,
                    error=f"输入文件不存在: {input_path}"
                )

            input_size = os.path.getsize(input_path)

            convert(input_path, output_path)

            if not os.path.exists(output_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=FileFormat.WORD,
                    output_format=FileFormat.PDF,
                    error="转换失败，未生成输出文件"
                )

            conversion_time = time.time() - start_time
            output_size = os.path.getsize(output_path)

            return ConversionResult(
                success=True,
                status=ConversionStatus.SUCCESS,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.WORD,
                output_format=FileFormat.PDF,
                message=f"Word 转 PDF 成功",
                conversion_time=conversion_time,
                input_size=input_size,
                output_size=output_size
            )

        except ImportError:
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.WORD,
                output_format=FileFormat.PDF,
                error="缺少依赖: 请安装 docx2pdf (pip install docx2pdf)"
            )
        except Exception as e:
            logger.error(f"Word 转 PDF 失败: {e}")
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.WORD,
                output_format=FileFormat.PDF,
                error=str(e)
            )

    def get_supported_formats(self) -> List[tuple]:
        return [(FileFormat.WORD, FileFormat.PDF)]


class ExcelToPDFConverter(Converter):
    """Excel 转 PDF 转换器"""

    def can_convert(self, input_format: FileFormat, output_format: FileFormat) -> bool:
        return input_format == FileFormat.EXCEL and output_format == FileFormat.PDF

    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        import time
        start_time = time.time()

        try:
            import win32com.client

            if not os.path.exists(input_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=FileFormat.EXCEL,
                    output_format=FileFormat.PDF,
                    error=f"输入文件不存在: {input_path}"
                )

            input_size = os.path.getsize(input_path)

            excel = win32com.client.Dispatch('Excel.Application')
            excel.Visible = False
            excel.DisplayAlerts = False

            try:
                workbook = excel.Workbooks.Open(os.path.abspath(input_path))
                workbook.ExportAsFixedFormat(
                    0,  # 0 = PDF format
                    os.path.abspath(output_path),
                    Quality=0,  # 0 = Standard, 1 = Minimum
                    IncludeDocProperties=True,
                    IgnorePrintAreas=False
                )
                workbook.Close(SaveChanges=False)
            finally:
                excel.Quit()

            if not os.path.exists(output_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=FileFormat.EXCEL,
                    output_format=FileFormat.PDF,
                    error="转换失败，未生成输出文件"
                )

            conversion_time = time.time() - start_time
            output_size = os.path.getsize(output_path)

            return ConversionResult(
                success=True,
                status=ConversionStatus.SUCCESS,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.EXCEL,
                output_format=FileFormat.PDF,
                message=f"Excel 转 PDF 成功",
                conversion_time=conversion_time,
                input_size=input_size,
                output_size=output_size
            )

        except ImportError:
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.EXCEL,
                output_format=FileFormat.PDF,
                error="缺少依赖: 请安装 pywin32 (pip install pywin32)"
            )
        except Exception as e:
            logger.error(f"Excel 转 PDF 失败: {e}")
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=FileFormat.EXCEL,
                output_format=FileFormat.PDF,
                error=str(e)
            )

    def get_supported_formats(self) -> List[tuple]:
        return [(FileFormat.EXCEL, FileFormat.PDF)]


class TextFormatConverter(Converter):
    """文本格式互转转换器"""

    SUPPORTED_FORMATS = {
        FileFormat.TXT, FileFormat.MD, FileFormat.RTF, FileFormat.CSV
    }

    def can_convert(self, input_format: FileFormat, output_format: FileFormat) -> bool:
        return input_format in self.SUPPORTED_FORMATS and output_format in self.SUPPORTED_FORMATS

    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        import time
        start_time = time.time()

        try:
            if not os.path.exists(input_path):
                return ConversionResult(
                    success=False,
                    status=ConversionStatus.FAILED,
                    input_file=input_path,
                    output_file=output_path,
                    input_format=self._get_format(input_path),
                    output_format=self._get_format(output_path),
                    error=f"输入文件不存在: {input_path}"
                )

            input_size = os.path.getsize(input_path)

            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if self._get_format(output_path) == FileFormat.RTF:
                content = self._txt_to_rtf(content)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            conversion_time = time.time() - start_time
            output_size = os.path.getsize(output_path)

            return ConversionResult(
                success=True,
                status=ConversionStatus.SUCCESS,
                input_file=input_path,
                output_file=output_path,
                input_format=self._get_format(input_path),
                output_format=self._get_format(output_path),
                message=f"文本格式转换成功",
                conversion_time=conversion_time,
                input_size=input_size,
                output_size=output_size
            )

        except Exception as e:
            logger.error(f"文本格式转换失败: {e}")
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=self._get_format(input_path),
                output_format=self._get_format(output_path),
                error=str(e)
            )

    def get_supported_formats(self) -> List[tuple]:
        formats = list(self.SUPPORTED_FORMATS)
        return [(f1, f2) for f1 in formats for f2 in formats if f1 != f2]

    def _get_format(self, file_path: str) -> FileFormat:
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        format_map = {
            'txt': FileFormat.TXT,
            'md': FileFormat.MD,
            'rtf': FileFormat.RTF,
            'csv': FileFormat.CSV
        }
        return format_map.get(ext, FileFormat.TXT)

    def _txt_to_rtf(self, text: str) -> str:
        """将纯文本转换为 RTF 格式"""
        rtf_header = r'{\rtf1\ansi\ansicpg1252\deff0\deflang1033{\fonttbl{\f0\fswiss\fprq2\fcharset0 Arial;}}\n'
        rtf_footer = r'\par}'
        
        lines = text.split('\n')
        rtf_lines = []
        for line in lines:
            rtf_line = line.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
            rtf_lines.append(rtf_line + '\\par')
        
        rtf_content = '\n'.join(rtf_lines)
        return rtf_header + rtf_content + rtf_footer


class FormatConverter:
    """
    格式转换主类

    支持的转换：
    - PDF ↔ Word
    - Word → PDF
    - Excel → PDF
    - 文本格式互转 (txt, md, rtf, csv)
    """

    def __init__(self):
        self.converters: List[Converter] = [
            PDFToWordConverter(),
            WordToPDFConverter(),
            ExcelToPDFConverter(),
            TextFormatConverter(),
        ]

        self._format_cache: Dict[str, FileFormat] = {}

    def get_file_format(self, file_path: str) -> FileFormat:
        """
        自动检测文件格式

        Args:
            file_path: 文件路径

        Returns:
            FileFormat: 检测到的格式
        """
        if file_path in self._format_cache:
            return self._format_cache[file_path]

        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        format_map = {
            'pdf': FileFormat.PDF,
            'docx': FileFormat.WORD,
            'doc': FileFormat.WORD,
            'xlsx': FileFormat.EXCEL,
            'xls': FileFormat.EXCEL,
            'pptx': FileFormat.PPT,
            'txt': FileFormat.TXT,
            'md': FileFormat.MD,
            'rtf': FileFormat.RTF,
            'csv': FileFormat.CSV,
            'html': FileFormat.HTML,
        }

        format = format_map.get(ext, FileFormat.TXT)
        self._format_cache[file_path] = format
        return format

    def is_supported(self, input_path: str, output_path: str) -> bool:
        """
        检查是否支持指定的格式转换

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径

        Returns:
            bool: 是否支持
        """
        input_format = self.get_file_format(input_path)
        output_format = self.get_file_format(output_path)

        for converter in self.converters:
            if converter.can_convert(input_format, output_format):
                return True
        return False

    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        """
        执行格式转换

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            **kwargs: 额外参数

        Returns:
            ConversionResult: 转换结果
        """
        input_format = self.get_file_format(input_path)
        output_format = self.get_file_format(output_path)

        if input_format == output_format:
            return ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=input_format,
                output_format=output_format,
                error="输入和输出格式相同，无需转换"
            )

        for converter in self.converters:
            if converter.can_convert(input_format, output_format):
                return converter.convert(input_path, output_path, **kwargs)

        return ConversionResult(
            success=False,
            status=ConversionStatus.FAILED,
            input_file=input_path,
            output_file=output_path,
            input_format=input_format,
            output_format=output_format,
            error=f"不支持的格式转换: {input_format.value} → {output_format.value}"
        )

    def batch_convert(self, files: List[tuple], **kwargs) -> List[ConversionResult]:
        """
        批量转换文件

        Args:
            files: 包含 (input_path, output_path) 的列表
            **kwargs: 额外参数

        Returns:
            List[ConversionResult]: 转换结果列表
        """
        results = []
        for input_path, output_path in files:
            result = self.convert(input_path, output_path, **kwargs)
            results.append(result)
        return results

    def get_supported_conversions(self) -> List[tuple]:
        """
        获取所有支持的格式转换

        Returns:
            List[tuple]: 支持的格式对列表
        """
        conversions = []
        for converter in self.converters:
            conversions.extend(converter.get_supported_formats())
        return conversions

    def get_supported_formats(self) -> List[FileFormat]:
        """
        获取所有支持的格式

        Returns:
            List[FileFormat]: 支持的格式列表
        """
        formats = set()
        for conversion in self.get_supported_conversions():
            formats.add(conversion[0])
            formats.add(conversion[1])
        return list(formats)

    def suggest_output_path(self, input_path: str, output_format: FileFormat) -> str:
        """
        根据输入路径和目标格式生成输出路径

        Args:
            input_path: 输入文件路径
            output_format: 目标格式

        Returns:
            str: 建议的输出路径
        """
        base_path = os.path.splitext(input_path)[0]
        return f"{base_path}.{output_format.value}"


class ConversionManager:
    """
    转换管理器

    功能：
    - 管理转换任务队列
    - 监控转换状态
    - 提供转换历史
    - 支持并发转换
    """

    def __init__(self):
        self.converter = FormatConverter()
        self.task_history: List[ConversionResult] = []
        self.active_tasks: Dict[str, ConversionResult] = {}

    def convert(self, input_path: str, output_path: str, **kwargs) -> ConversionResult:
        """
        执行转换并记录历史

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            **kwargs: 额外参数

        Returns:
            ConversionResult: 转换结果
        """
        task_id = f"{input_path}→{output_path}"
        
        self.active_tasks[task_id] = ConversionResult(
            success=False,
            status=ConversionStatus.IN_PROGRESS,
            input_file=input_path,
            output_file=output_path,
            input_format=self.converter.get_file_format(input_path),
            output_format=self.converter.get_file_format(output_path),
            message="转换中..."
        )

        try:
            result = self.converter.convert(input_path, output_path, **kwargs)
            self.task_history.append(result)
            self.active_tasks.pop(task_id, None)
            return result
        except Exception as e:
            result = ConversionResult(
                success=False,
                status=ConversionStatus.FAILED,
                input_file=input_path,
                output_file=output_path,
                input_format=self.converter.get_file_format(input_path),
                output_format=self.converter.get_file_format(output_path),
                error=str(e)
            )
            self.task_history.append(result)
            self.active_tasks.pop(task_id, None)
            return result

    def batch_convert(self, files: List[tuple], **kwargs) -> List[ConversionResult]:
        """
        批量转换并记录历史

        Args:
            files: 包含 (input_path, output_path) 的列表
            **kwargs: 额外参数

        Returns:
            List[ConversionResult]: 转换结果列表
        """
        results = self.converter.batch_convert(files, **kwargs)
        self.task_history.extend(results)
        return results

    def get_history(self, limit: int = 100) -> List[ConversionResult]:
        """
        获取转换历史

        Args:
            limit: 限制数量

        Returns:
            List[ConversionResult]: 历史记录
        """
        return self.task_history[-limit:]

    def get_active_tasks(self) -> Dict[str, ConversionResult]:
        """
        获取活跃的转换任务

        Returns:
            Dict[str, ConversionResult]: 活跃任务
        """
        return self.active_tasks

    def get_statistics(self) -> Dict:
        """
        获取转换统计信息

        Returns:
            Dict: 统计信息
        """
        total = len(self.task_history)
        success_count = sum(1 for r in self.task_history if r.success)
        failed_count = total - success_count
        
        format_stats = {}
        for result in self.task_history:
            key = f"{result.input_format.value}→{result.output_format.value}"
            format_stats[key] = format_stats.get(key, 0) + 1

        return {
            "total_tasks": total,
            "success_count": success_count,
            "failed_count": failed_count,
            "success_rate": success_count / max(total, 1),
            "format_stats": format_stats,
            "active_tasks": len(self.active_tasks)
        }

    def clear_history(self):
        """
        清空转换历史
        """
        self.task_history.clear()


if __name__ == "__main__":
    converter = FormatConverter()
    manager = ConversionManager()

    # 测试 PDF 转 Word
    # result = manager.convert("test.pdf", "test_output.docx")
    # print(f"PDF→Word: {result.success}, {result.message}")

    # 测试 Word 转 PDF
    # result = manager.convert("test.docx", "test_output.pdf")
    # print(f"Word→PDF: {result.success}, {result.message}")

    # 测试 Excel 转 PDF
    # result = manager.convert("test.xlsx", "test_output.pdf")
    # print(f"Excel→PDF: {result.success}, {result.message}")

    # 测试文本格式转换
    # result = manager.convert("test.txt", "test_output.md")
    # print(f"Text→MD: {result.success}, {result.message}")

    # 查看支持的转换
    supported = converter.get_supported_conversions()
    print("支持的格式转换:")
    for from_format, to_format in supported:
        print(f"  {from_format.value} → {to_format.value}")
