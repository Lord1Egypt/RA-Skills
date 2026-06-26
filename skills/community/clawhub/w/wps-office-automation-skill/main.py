"""
WPS Office Automation Skill主入口
实现自然语言指令到具体操作的智能路由和执行
"""

import base64
import logging
import re
from typing import Dict, Any, Optional
from enum import Enum

from pydantic import BaseModel, Field

from modules.document import (
    DocumentProcessor,
    DocumentType,
    PolishStyle,
    OfficialDocumentRequest,
    PolishRequest,
)
from modules.spreadsheet import (
    SpreadsheetProcessor,
    ChartType,
    AnalysisType,
    DataCleaningRequest,
    AnalysisRequest,
    ChartGenerationRequest,
)
from modules.presentation import (
    PresentationProcessor,
    TemplateStyle,
    OutlineRequest,
    LayoutRequest,
)
from modules.pdf import (
    PDFProcessor,
    ConversionFormat,
    ExtractionType,
    ConversionRequest,
    ExtractionRequest,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(str, Enum):
    """操作类型"""
    GENERATE_DOCUMENT = "generate_document"
    POLISH_DOCUMENT = "polish_document"
    REVIEW_CONTRACT = "review_contract"
    CLEAN_DATA = "clean_data"
    ANALYZE_DATA = "analyze_data"
    GENERATE_CHART = "generate_chart"
    GENERATE_PPT_OUTLINE = "generate_ppt_outline"
    CREATE_PRESENTATION = "create_presentation"
    CONVERT_PDF = "convert_pdf"
    EXTRACT_PDF = "extract_pdf"
    MERGE_PDF = "merge_pdf"
    SPLIT_PDF = "split_pdf"


class SkillRequest(BaseModel):
    """Skill请求"""
    action: str = Field(..., description="操作指令")
    params: Dict[str, Any] = Field(default_factory=dict, description="参数")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")


class SkillResponse(BaseModel):
    """Skill响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    file_data: Optional[str] = Field(None, description="文件数据（Base64编码）")
    file_name: Optional[str] = Field(None, description="文件名")


class IntentParser:
    """意图解析器"""
    
    DOCUMENT_PATTERNS = {
        ActionType.GENERATE_DOCUMENT: [
            r"生成.*公文",
            r"创建.*通知",
            r"写.*报告",
            r"制作.*会议纪要",
        ],
        ActionType.POLISH_DOCUMENT: [
            r"润色.*文档",
            r"优化.*文字",
            r"修改.*风格",
            r"正式化.*内容",
        ],
        ActionType.REVIEW_CONTRACT: [
            r"审查.*合同",
            r"检查.*条款",
            r"分析.*协议",
        ],
    }
    
    SPREADSHEET_PATTERNS = {
        ActionType.CLEAN_DATA: [
            r"清洗.*数据",
            r"处理.*异常值",
            r"去重.*表格",
        ],
        ActionType.ANALYZE_DATA: [
            r"分析.*表格",
            r"统计.*数据",
            r"计算.*总和",
            r"求.*平均值",
        ],
        ActionType.GENERATE_CHART: [
            r"生成.*图表",
            r"创建.*柱状图",
            r"制作.*折线图",
            r"画.*饼图",
        ],
    }
    
    PRESENTATION_PATTERNS = {
        ActionType.GENERATE_PPT_OUTLINE: [
            r"生成.*PPT.*大纲",
            r"创建.*演示.*大纲",
            r"制作.*幻灯片.*大纲",
        ],
        ActionType.CREATE_PRESENTATION: [
            r"创建.*PPT",
            r"制作.*演示文稿",
            r"生成.*幻灯片",
        ],
    }
    
    PDF_PATTERNS = {
        ActionType.CONVERT_PDF: [
            r"PDF.*转.*Word",
            r"PDF.*转.*Excel",
            r"转换.*PDF",
        ],
        ActionType.EXTRACT_PDF: [
            r"提取.*PDF.*内容",
            r"读取.*PDF.*文本",
            r"解析.*PDF",
        ],
        ActionType.MERGE_PDF: [
            r"合并.*PDF",
            r"拼接.*PDF",
        ],
        ActionType.SPLIT_PDF: [
            r"拆分.*PDF",
            r"分割.*PDF",
        ],
    }
    
    @classmethod
    def parse(cls, instruction: str) -> Optional[str]:
        """
        解析用户指令，识别操作类型
        
        Args:
            instruction: 用户指令
            
        Returns:
            操作类型
        """
        all_patterns = {}
        all_patterns.update(cls.DOCUMENT_PATTERNS)
        all_patterns.update(cls.SPREADSHEET_PATTERNS)
        all_patterns.update(cls.PRESENTATION_PATTERNS)
        all_patterns.update(cls.PDF_PATTERNS)
        
        for action_type, patterns in all_patterns.items():
            for pattern in patterns:
                if re.search(pattern, instruction):
                    return action_type.value
        
        return None


class WPSOfficeAutomationSkill:
    """WPS Office自动化Skill"""
    
    def __init__(self):
        self.doc_processor: Optional[DocumentProcessor] = None
        self.sheet_processor: Optional[SpreadsheetProcessor] = None
        self.ppt_processor: Optional[PresentationProcessor] = None
        self.pdf_processor: Optional[PDFProcessor] = None
        
    async def initialize(self):
        """初始化"""
        logger.info("初始化WPS Office Automation Skill（本地模式）")
        
        self.doc_processor = DocumentProcessor()
        self.sheet_processor = SpreadsheetProcessor()
        self.ppt_processor = PresentationProcessor()
        self.pdf_processor = PDFProcessor()
        
        logger.info("WPS Office Automation Skill初始化成功")
            
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行Skill
        
        Args:
            params: 执行参数，包含action和具体参数
            
        Returns:
            执行结果
        """
        await self.initialize()
        
        action = params.get("action", "")
        
        action_type = IntentParser.parse(action)
        
        if not action_type:
            action_type = params.get("action_type")
            
        if not action_type:
            return SkillResponse(
                success=False,
                message="无法识别操作指令，请提供更明确的指令",
            ).model_dump()
            
        try:
            if action_type == ActionType.GENERATE_DOCUMENT.value:
                return await self._handle_generate_document(params)
            elif action_type == ActionType.POLISH_DOCUMENT.value:
                return await self._handle_polish_document(params)
            elif action_type == ActionType.REVIEW_CONTRACT.value:
                return await self._handle_review_contract(params)
            elif action_type == ActionType.CLEAN_DATA.value:
                return await self._handle_clean_data(params)
            elif action_type == ActionType.ANALYZE_DATA.value:
                return await self._handle_analyze_data(params)
            elif action_type == ActionType.GENERATE_CHART.value:
                return await self._handle_generate_chart(params)
            elif action_type == ActionType.GENERATE_PPT_OUTLINE.value:
                return await self._handle_generate_ppt_outline(params)
            elif action_type == ActionType.CREATE_PRESENTATION.value:
                return await self._handle_create_presentation(params)
            elif action_type == ActionType.CONVERT_PDF.value:
                return await self._handle_convert_pdf(params)
            elif action_type == ActionType.EXTRACT_PDF.value:
                return await self._handle_extract_pdf(params)
            elif action_type == ActionType.MERGE_PDF.value:
                return await self._handle_merge_pdf(params)
            elif action_type == ActionType.SPLIT_PDF.value:
                return await self._handle_split_pdf(params)
            else:
                return SkillResponse(
                    success=False,
                    message=f"不支持的操作类型: {action_type}",
                ).model_dump()
                
        except Exception as e:
            logger.error(f"执行失败: {str(e)}", exc_info=True)
            return SkillResponse(
                success=False,
                message=f"执行失败: {str(e)}",
            ).model_dump()
    
    async def _handle_generate_document(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理文档生成"""
        doc_type_str = params.get("doc_type", "notice")
        doc_type = DocumentType(doc_type_str)
        
        request = OfficialDocumentRequest(
            doc_type=doc_type,
            title=params.get("title", "未命名文档"),
            subject=params.get("subject", ""),
            recipient=params.get("recipient", ""),
            sender=params.get("sender", ""),
            date=params.get("date", ""),
            keywords=params.get("keywords", []),
            content=params.get("content", ""),
        )
        
        doc_bytes = await self.doc_processor.generate_official_document(request)
        
        return SkillResponse(
            success=True,
            message="文档生成成功",
            file_data=base64.b64encode(doc_bytes).decode('utf-8'),
            file_name=f"{request.title}.docx",
        ).model_dump()
    
    async def _handle_polish_document(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理文档润色"""
        style_str = params.get("style", "formal")
        style = PolishStyle(style_str)
        
        request = PolishRequest(
            content=params.get("content", ""),
            style=style,
        )
        
        result = await self.doc_processor.polish_document(request)
        
        return SkillResponse(
            success=True,
            message="文档润色成功",
            data={
                "polished_content": result["polished_content"],
                "original_content": result["original_content"],
            }
        ).model_dump()
    
    async def _handle_review_contract(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理合同审查"""
        content = params.get("content", "")
        
        result = await self.doc_processor.review_contract(content)
        
        return SkillResponse(
            success=True,
            message="合同审查完成",
            data=result.model_dump(),
        ).model_dump()
    
    async def _handle_clean_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理数据清洗"""
        data = params.get("data")
        if isinstance(data, str):
            data = base64.b64decode(data)
        
        request = DataCleaningRequest(
            data=data,
            remove_duplicates=params.get("remove_duplicates", True),
            handle_missing=params.get("handle_missing", "mean"),
            remove_outliers=params.get("remove_outliers", True),
            outlier_method=params.get("outlier_method", "iqr"),
        )
        
        result = await self.sheet_processor.clean_data(request)
        
        return SkillResponse(
            success=True,
            message="数据清洗完成",
            file_data=base64.b64encode(result["file_bytes"]).decode('utf-8'),
            file_name="cleaned_data.xlsx",
            data={
                "original_rows": result["original_rows"],
                "cleaned_rows": result["cleaned_rows"],
                "removed_duplicates": result["removed_duplicates"],
                "handled_missing": result["handled_missing"],
            }
        ).model_dump()
    
    async def _handle_analyze_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理数据分析"""
        data = params.get("data")
        if isinstance(data, str):
            data = base64.b64decode(data)
        
        analysis_type_str = params.get("analysis_type", "sum")
        analysis_type = AnalysisType(analysis_type_str)
        
        request = AnalysisRequest(
            data=data,
            analysis_type=analysis_type,
            columns=params.get("columns", []),
            group_by=params.get("group_by"),
        )
        
        result = await self.sheet_processor.analyze_data(request)
        
        return SkillResponse(
            success=True,
            message="数据分析完成",
            data=result,
        ).model_dump()
    
    async def _handle_generate_chart(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理图表生成"""
        data = params.get("data")
        if isinstance(data, str):
            data = base64.b64decode(data)
        
        chart_type_str = params.get("chart_type", "bar")
        chart_type = ChartType(chart_type_str)
        
        request = ChartGenerationRequest(
            data=data,
            chart_type=chart_type,
            x_column=params.get("x_column", ""),
            y_columns=params.get("y_columns", []),
            title=params.get("title", "图表"),
        )
        
        chart_bytes = await self.sheet_processor.generate_chart(request)
        
        return SkillResponse(
            success=True,
            message="图表生成成功",
            file_data=base64.b64encode(chart_bytes).decode('utf-8'),
            file_name=f"{request.title}.xlsx",
        ).model_dump()
    
    async def _handle_generate_ppt_outline(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理PPT大纲生成"""
        request = OutlineRequest(
            topic=params.get("topic", ""),
            slide_count=params.get("slide_count", 10),
            target_audience=params.get("target_audience", ""),
            key_points=params.get("key_points", []),
        )
        
        outline = await self.ppt_processor.generate_outline(request)
        
        return SkillResponse(
            success=True,
            message="PPT大纲生成成功",
            data={"slides": outline.slides},
        ).model_dump()
    
    async def _handle_create_presentation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理演示文稿创建"""
        outline_data = params.get("outline", {})
        
        from modules.presentation import PresentationOutline, SlideOutline
        
        outline = PresentationOutline(
            title=outline_data.get("title", "未命名演示"),
            slides=[
                SlideOutline(**slide) for slide in outline_data.get("slides", [])
            ]
        )
        
        style_str = params.get("style", "business")
        style = TemplateStyle(style_str)
        
        request = LayoutRequest(
            outline=outline,
            style=style,
        )
        
        ppt_bytes = await self.ppt_processor.create_presentation(request)
        
        return SkillResponse(
            success=True,
            message="演示文稿创建成功",
            file_data=base64.b64encode(ppt_bytes).decode('utf-8'),
            file_name=f"{outline.title}.pptx",
        ).model_dump()
    
    async def _handle_convert_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理PDF转换"""
        pdf_data = base64.b64decode(params.get("file_data", ""))
        
        target_format_str = params.get("target_format", "word")
        target_format = ConversionFormat(target_format_str)
        
        request = ConversionRequest(
            pdf_data=pdf_data,
            target_format=target_format,
            preserve_formatting=params.get("preserve_formatting", True),
        )
        
        converted_bytes = await self.pdf_processor.convert_pdf(request)
        
        return SkillResponse(
            success=True,
            message="PDF转换成功",
            file_data=base64.b64encode(converted_bytes).decode('utf-8'),
            file_name=f"converted.{target_format_str}",
        ).model_dump()
    
    async def _handle_extract_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理PDF内容提取"""
        pdf_data = base64.b64decode(params.get("file_data", ""))
        
        extraction_type_str = params.get("extraction_type", "text")
        extraction_type = ExtractionType(extraction_type_str)
        
        request = ExtractionRequest(
            pdf_data=pdf_data,
            extraction_type=extraction_type,
        )
        
        result = await self.pdf_processor.extract_content(request)
        
        return SkillResponse(
            success=True,
            message="PDF内容提取成功",
            data=result,
        ).model_dump()
    
    async def _handle_merge_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理PDF合并"""
        pdf_files = [
            base64.b64decode(file_data)
            for file_data in params.get("files", [])
        ]
        
        from modules.pdf import MergeRequest
        request = MergeRequest(pdf_files=pdf_files)
        
        merged_bytes = await self.pdf_processor.merge_pdfs(request)
        
        return SkillResponse(
            success=True,
            message="PDF合并成功",
            file_data=base64.b64encode(merged_bytes).decode('utf-8'),
            file_name="merged.pdf",
        ).model_dump()
        
    async def _handle_split_pdf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理PDF拆分"""
        pdf_data = base64.b64decode(params.get("file_data", ""))
        
        from modules.pdf import SplitRequest
        request = SplitRequest(
            pdf_data=pdf_data,
            split_mode=params.get("split_mode", "page"),
            page_ranges=params.get("page_ranges", []),
        )
        
        split_files = await self.pdf_processor.split_pdf(request)
        
        return SkillResponse(
            success=True,
            message="PDF拆分成功",
            data={
                "files": [
                    base64.b64encode(file_bytes).decode('utf-8')
                    for file_bytes in split_files
                ]
            },
        ).model_dump()


async def execute(params: dict) -> dict:
    """
    Skill执行入口
    
    Args:
        params: 执行参数
        
    Returns:
        执行结果
    """
    skill = WPSOfficeAutomationSkill()
    return await skill.execute(params)
