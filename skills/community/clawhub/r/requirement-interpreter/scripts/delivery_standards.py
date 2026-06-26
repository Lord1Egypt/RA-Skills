#!/usr/bin/env python3
"""
交付物标准化模块
定义各行业需求的标准化交付物清单
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class DeliveryCategory(str, Enum):
    """交付物大类"""
    CODE = "代码文件"
    DESIGN = "设计文件"
    DOCUMENT = "文档资料"
    ASSET = "资源素材"
    REPORT = "分析报告"
    VIDEO = "视频素材"
    AUDIO = "音频素材"
    DATA = "数据文件"


class FileFormat(str, Enum):
    """文件格式"""
    # 代码类
    HTML = "HTML"
    CSS = "CSS"
    JS = "JavaScript"
    TS = "TypeScript"
    PY = "Python"
    JSON = "JSON"
    YAML = "YAML"
    
    # 设计类
    FIGMA = "Figma"
    SKETCH = "Sketch"
    PSD = "PSD"
    AI = "AI"
    SVG = "SVG"
    PNG = "PNG"
    JPG = "JPG"
    PDF = "PDF"
    
    # 文档类
    DOCX = "Word"
    XLSX = "Excel"
    PPTX = "PPT"
    MD = "Markdown"
    TXT = "TXT"
    
    # 视频类
    MP4 = "MP4"
    MOV = "MOV"
    GIF = "GIF"
    
    # 音频类
    MP3 = "MP3"
    WAV = "WAV"
    
    # 数据类
    CSV = "CSV"
    SQL = "SQL"
    XML = "XML"


@dataclass
class DeliveryItem:
    """单个交付物项"""
    name: str                    # 交付物名称
    description: str             # 交付物描述
    category: DeliveryCategory   # 所属分类
    formats: List[FileFormat]    # 推荐格式
    priority: int = 1            # 优先级 (1-3)
    required: bool = True        # 是否必需
    notes: str = ""              # 备注说明
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "formats": [f.value for f in self.formats],
            "priority": self.priority,
            "required": self.required,
            "notes": self.notes
        }


@dataclass
class DeliveryStandard:
    """交付物标准模板"""
    id: str
    name: str
    requirement_type: str        # 匹配的需求类型
    description: str             # 标准说明
    items: List[DeliveryItem]    # 交付物清单
    usage_guide: str = ""        # 使用指南
    validation_checklist: List[str] = field(default_factory=list)  # 验收清单
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "requirement_type": self.requirement_type,
            "description": self.description,
            "items": [item.to_dict() for item in self.items],
            "usage_guide": self.usage_guide,
            "validation_checklist": self.validation_checklist
        }


class DeliveryStandards:
    """交付物标准库"""
    
    @staticmethod
    def get_all_standards() -> List[DeliveryStandard]:
        """获取所有交付物标准"""
        return [
            DeliveryStandards.web_design(),
            DeliveryStandards.mobile_app(),
            DeliveryStandards.ecommerce(),
            DeliveryStandards.marketing_poster(),
            DeliveryStandards.video_production(),
            DeliveryStandards.data_analysis(),
            DeliveryStandards.business_process(),
            DeliveryStandards.consulting(),
        ]
    
    @staticmethod
    def web_design() -> DeliveryStandard:
        """网站设计交付标准"""
        return DeliveryStandard(
            id="web_design",
            name="网站设计交付标准",
            requirement_type="技术开发/内容创作",
            description="网页设计和前端开发项目的标准化交付物",
            items=[
                DeliveryItem(
                    name="网页文件",
                    description="符合HTML5标准的网页文件",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.HTML, FileFormat.CSS, FileFormat.JS],
                    priority=1,
                    required=True,
                    notes="语义化HTML，响应式布局，SEO友好"
                ),
                DeliveryItem(
                    name="设计稿",
                    description="完整页面设计稿（分层）",
                    category=DeliveryCategory.DESIGN,
                    formats=[FileFormat.FIGMA, FileFormat.SKETCH, FileFormat.PSD],
                    priority=1,
                    required=True,
                    notes="包含各状态（默认、悬停、点击等）"
                ),
                DeliveryItem(
                    name="图标资源",
                    description="SVG/PNG格式图标",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.SVG, FileFormat.PNG],
                    priority=2,
                    required=True,
                    notes="提供多种尺寸，支持Retina屏幕"
                ),
                DeliveryItem(
                    name="图片素材",
                    description="页面使用的图片资源",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.JPG, FileFormat.SVG],
                    priority=2,
                    required=True,
                    notes="优化压缩，标注图片来源"
                ),
                DeliveryItem(
                    name="交互规范",
                    description="动效和交互说明文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.MD, FileFormat.PDF],
                    priority=2,
                    required=False,
                    notes="包含过渡时长、缓动函数等"
                ),
                DeliveryItem(
                    name="设计说明文档",
                    description="设计规范和组件说明",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.MD, FileFormat.PDF],
                    priority=3,
                    required=False,
                    notes="包含颜色、字体、间距等规范"
                ),
            ],
            usage_guide="1. 先完成设计稿确认 2. 开发实现并提供预览 3. 交付所有源文件和资源",
            validation_checklist=[
                "页面在不同设备上显示正常",
                "所有交互状态已实现",
                "图片已优化压缩",
                "代码符合W3C标准",
                "设计稿与实现一致"
            ]
        )
    
    @staticmethod
    def mobile_app() -> DeliveryStandard:
        """移动应用交付标准"""
        return DeliveryStandard(
            id="mobile_app",
            name="移动应用交付标准",
            requirement_type="技术开发",
            description="iOS/Android移动应用开发项目的标准化交付物",
            items=[
                DeliveryItem(
                    name="应用安装包",
                    description="可安装的应用包文件",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.YAML],  # APK/IPA
                    priority=1,
                    required=True,
                    notes="Android: APK, iOS: IPA"
                ),
                DeliveryItem(
                    name="设计稿",
                    description="完整UI设计稿（1x/2x/3x）",
                    category=DeliveryCategory.DESIGN,
                    formats=[FileFormat.FIGMA, FileFormat.SKETCH],
                    priority=1,
                    required=True,
                    notes="包含启动页、各页面、图标"
                ),
                DeliveryItem(
                    name="切图资源",
                    description="各分辨率的图片资源",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.JPG],
                    priority=1,
                    required=True,
                    notes="@1x/@2x/@3x标注清晰"
                ),
                DeliveryItem(
                    name="图标资源",
                    description="应用图标和功能图标",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.SVG],
                    priority=1,
                    required=True,
                    notes="多尺寸规格（1024x1024等）"
                ),
                DeliveryItem(
                    name="源码项目",
                    description="完整的项目源代码",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.PY, FileFormat.TS],  # Swift/Kotlin/Flutter
                    priority=1,
                    required=True,
                    notes="包含注释和文档"
                ),
                DeliveryItem(
                    name="接口文档",
                    description="API接口说明文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.MD, FileFormat.YAML],
                    priority=2,
                    required=True,
                    notes="包含请求/响应示例"
                ),
                DeliveryItem(
                    name="测试报告",
                    description="功能测试和兼容性测试报告",
                    category=DeliveryCategory.REPORT,
                    formats=[FileFormat.PDF, FileFormat.XLSX],
                    priority=2,
                    required=False,
                    notes="覆盖主流机型"
                ),
            ],
            usage_guide="1. 设计稿评审确认 2. 开发测试 3. 上架前准备完整资源包",
            validation_checklist=[
                "应用可正常安装运行",
                "各分辨率显示正确",
                "核心功能测试通过",
                "性能指标达标",
                "上架材料齐全"
            ]
        )
    
    @staticmethod
    def ecommerce() -> DeliveryStandard:
        """电商项目交付标准"""
        return DeliveryStandard(
            id="ecommerce",
            name="电商项目交付标准",
            requirement_type="技术开发",
            description="电商平台/商城系统开发的标准交付物",
            items=[
                DeliveryItem(
                    name="前端代码",
                    description="商城前端页面代码",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.HTML, FileFormat.CSS, FileFormat.JS, FileFormat.TS],
                    priority=1,
                    required=True,
                    notes="响应式设计，支持PC/移动端"
                ),
                DeliveryItem(
                    name="后端代码",
                    description="服务端API和业务逻辑代码",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.PY],  # Java/Node/Python
                    priority=1,
                    required=True,
                    notes="包含数据库操作代码"
                ),
                DeliveryItem(
                    name="数据库文件",
                    description="数据库结构和初始化脚本",
                    category=DeliveryCategory.DATA,
                    formats=[FileFormat.SQL, FileFormat.YAML],
                    priority=1,
                    required=True,
                    notes="包含表结构和索引"
                ),
                DeliveryItem(
                    name="UI设计稿",
                    description="商城整体UI设计",
                    category=DeliveryCategory.DESIGN,
                    formats=[FileFormat.FIGMA, FileFormat.SKETCH],
                    priority=1,
                    required=True,
                    notes="包含商品页、购物车、支付等"
                ),
                DeliveryItem(
                    name="接口文档",
                    description="API接口文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.MD, FileFormat.YAML],
                    priority=1,
                    required=True,
                    notes="Swagger/OpenAPI格式"
                ),
                DeliveryItem(
                    name="运营后台",
                    description="商家运营管理系统",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.HTML, FileFormat.PY],
                    priority=2,
                    required=True,
                    notes="商品管理、订单管理等"
                ),
                DeliveryItem(
                    name="部署文档",
                    description="服务器部署和环境配置文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.MD],
                    priority=2,
                    required=True,
                    notes="包含Docker/Nginx配置"
                ),
                DeliveryItem(
                    name="培训手册",
                    description="系统使用培训文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.PDF, FileFormat.DOCX],
                    priority=3,
                    required=False,
                    notes="操作指南和常见问题"
                ),
            ],
            usage_guide="1. 需求确认和原型设计 2. 系统开发和内部测试 3. 验收测试和部署上线",
            validation_checklist=[
                "商品展示和购买流程完整",
                "支付功能正常",
                "订单管理功能正常",
                "数据安全措施到位",
                "性能压测达标"
            ]
        )
    
    @staticmethod
    def marketing_poster() -> DeliveryStandard:
        """营销海报交付标准"""
        return DeliveryStandard(
            id="marketing_poster",
            name="营销海报交付标准",
            requirement_type="内容创作",
            description="营销海报/宣传图设计项目的标准化交付物",
            items=[
                DeliveryItem(
                    name="设计源文件",
                    description="可编辑的分层设计文件",
                    category=DeliveryCategory.DESIGN,
                    formats=[FileFormat.PSD, FileFormat.AI, FileFormat.FIGMA],
                    priority=1,
                    required=True,
                    notes="分层清晰，便于后续修改"
                ),
                DeliveryItem(
                    name="印刷文件",
                    description="印刷用的PDF文件（CMYK）",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PDF],
                    priority=1,
                    required=True,
                    notes="3mm出血，分辨率300dpi"
                ),
                DeliveryItem(
                    name="数字文件",
                    description="线上使用的图片文件",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.JPG],
                    priority=1,
                    required=True,
                    notes="提供多种尺寸规格"
                ),
                DeliveryItem(
                    name="矢量文件",
                    description="SVG矢量格式文件",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.SVG],
                    priority=2,
                    required=False,
                    notes="无限缩放，网页适用"
                ),
                DeliveryItem(
                    name="预览缩略图",
                    description="用于快速预览的小图",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.JPG],
                    priority=3,
                    required=False,
                    notes="宽800px以内"
                ),
            ],
            usage_guide="1. 确认设计需求和风格 2. 提供初稿确认 3. 修改定稿后交付各格式",
            validation_checklist=[
                "印刷文件尺寸和色彩模式正确",
                "数字文件清晰度足够",
                "文字可正常显示",
                "品牌元素使用正确",
                "各格式文件完整"
            ]
        )
    
    @staticmethod
    def video_production() -> DeliveryStandard:
        """视频制作交付标准"""
        return DeliveryStandard(
            id="video_production",
            name="视频制作交付标准",
            requirement_type="内容创作",
            description="视频/动画制作项目的标准化交付物",
            items=[
                DeliveryItem(
                    name="视频成片",
                    description="最终输出的视频文件",
                    category=DeliveryCategory.VIDEO,
                    formats=[FileFormat.MP4, FileFormat.MOV],
                    priority=1,
                    required=True,
                    notes="主流格式，支持多平台使用"
                ),
                DeliveryItem(
                    name="工程文件",
                    description="剪辑/特效源工程文件",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.YAML],  # PR/AE工程文件
                    priority=1,
                    required=True,
                    notes="便于后续修改"
                ),
                DeliveryItem(
                    name="分镜脚本",
                    description="视频分镜和脚本文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.PDF, FileFormat.DOCX],
                    priority=1,
                    required=True,
                    notes="包含画面描述和配音文稿"
                ),
                DeliveryItem(
                    name="封面图",
                    description="视频封面图文件",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.JPG],
                    priority=2,
                    required=True,
                    notes="多种尺寸规格"
                ),
                DeliveryItem(
                    name="缩略图/GIF",
                    description="用于预览的缩略图或GIF",
                    category=DeliveryCategory.VIDEO,
                    formats=[FileFormat.PNG, FileFormat.JPG, FileFormat.GIF],
                    priority=2,
                    required=False,
                    notes="便于社交媒体分享"
                ),
                DeliveryItem(
                    name="字幕文件",
                    description="字幕SRT/ASS文件",
                    category=DeliveryCategory.DATA,
                    formats=[FileFormat.YAML],  # SRT/ASS格式
                    priority=2,
                    required=False,
                    notes="支持多语言字幕"
                ),
                DeliveryItem(
                    name="配乐素材",
                    description="使用的背景音乐文件",
                    category=DeliveryCategory.AUDIO,
                    formats=[FileFormat.MP3, FileFormat.WAV],
                    priority=3,
                    required=False,
                    notes="标注音乐来源和版权"
                ),
            ],
            usage_guide="1. 确认创意方向和脚本 2. 分镜拍摄/素材准备 3. 剪辑制作 4. 审片修改 5. 成片交付",
            validation_checklist=[
                "视频画质和音频清晰度达标",
                "时长符合要求",
                "字幕和配音准确",
                "版权素材使用合规",
                "各平台格式适配"
            ]
        )
    
    @staticmethod
    def data_analysis() -> DeliveryStandard:
        """数据分析交付标准"""
        return DeliveryStandard(
            id="data_analysis",
            name="数据分析交付标准",
            requirement_type="数据分析",
            description="数据分析/报表项目的标准化交付物",
            items=[
                DeliveryItem(
                    name="分析报告",
                    description="完整的分析报告文档",
                    category=DeliveryCategory.REPORT,
                    formats=[FileFormat.PDF, FileFormat.PPTX],
                    priority=1,
                    required=True,
                    notes="包含结论和建议"
                ),
                DeliveryItem(
                    name="数据文件",
                    description="原始数据和清洗后的数据",
                    category=DeliveryCategory.DATA,
                    formats=[FileFormat.CSV, FileFormat.XLSX],
                    priority=1,
                    required=True,
                    notes="标注字段说明"
                ),
                DeliveryItem(
                    name="可视化图表",
                    description="数据可视化图表文件",
                    category=DeliveryCategory.ASSET,
                    formats=[FileFormat.PNG, FileFormat.JPG, FileFormat.SVG],
                    priority=1,
                    required=True,
                    notes="高清晰度，支持导出"
                ),
                DeliveryItem(
                    name="分析代码",
                    description="数据处理和分析代码",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.PY, FileFormat.JS],
                    priority=2,
                    required=False,
                    notes="包含注释说明"
                ),
                DeliveryItem(
                    name="仪表盘",
                    description="BI仪表盘或在线报表链接",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.YAML],  # Dashboard链接
                    priority=2,
                    required=False,
                    notes="可交互查看"
                ),
                DeliveryItem(
                    name="方法论文档",
                    description="分析方法和模型说明",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.MD, FileFormat.PDF],
                    priority=3,
                    required=False,
                    notes="技术细节说明"
                ),
            ],
            usage_guide="1. 数据采集和清洗 2. 分析建模 3. 可视化呈现 4. 撰写报告",
            validation_checklist=[
                "数据来源可追溯",
                "分析方法科学合理",
                "图表准确无误",
                "结论有数据支撑",
                "建议可操作性强"
            ]
        )
    
    @staticmethod
    def business_process() -> DeliveryStandard:
        """业务流程交付标准"""
        return DeliveryStandard(
            id="business_process",
            name="业务流程交付标准",
            requirement_type="业务流程",
            description="业务流程设计/自动化项目的标准化交付物",
            items=[
                DeliveryItem(
                    name="流程图",
                    description="业务流程图文件",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.PDF, FileFormat.FIGMA],
                    priority=1,
                    required=True,
                    notes="包含各环节和判定条件"
                ),
                DeliveryItem(
                    name="需求文档",
                    description="业务流程需求说明书",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.DOCX, FileFormat.MD],
                    priority=1,
                    required=True,
                    notes="明确输入输出和规则"
                ),
                DeliveryItem(
                    name="原型设计",
                    description="系统界面原型设计",
                    category=DeliveryCategory.DESIGN,
                    formats=[FileFormat.FIGMA, FileFormat.SKETCH],
                    priority=2,
                    required=False,
                    notes="包含各角色操作界面"
                ),
                DeliveryItem(
                    name="自动化脚本",
                    description="流程自动化脚本代码",
                    category=DeliveryCategory.CODE,
                    formats=[FileFormat.PY, FileFormat.YAML],
                    priority=2,
                    required=False,
                    notes="包含使用说明"
                ),
                DeliveryItem(
                    name="测试用例",
                    description="功能测试用例文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.XLSX, FileFormat.DOCX],
                    priority=2,
                    required=False,
                    notes="覆盖各流程分支"
                ),
                DeliveryItem(
                    name="培训材料",
                    description="用户操作培训文档",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.PDF, FileFormat.PPTX],
                    priority=3,
                    required=False,
                    notes="图文并茂的操作指南"
                ),
            ],
            usage_guide="1. 需求调研 2. 流程设计 3. 原型评审 4. 开发实施 5. 用户培训",
            validation_checklist=[
                "流程覆盖所有业务场景",
                "异常处理机制完善",
                "权限控制合理",
                "操作日志可追溯",
                "用户培训完成"
            ]
        )
    
    @staticmethod
    def consulting() -> DeliveryStandard:
        """咨询服务交付标准"""
        return DeliveryStandard(
            id="consulting",
            name="咨询服务交付标准",
            requirement_type="咨询服务",
            description="咨询方案/评估报告的标准交付物",
            items=[
                DeliveryItem(
                    name="咨询报告",
                    description="完整的咨询方案报告",
                    category=DeliveryCategory.REPORT,
                    formats=[FileFormat.PDF, FileFormat.PPTX],
                    priority=1,
                    required=True,
                    notes="结构完整，包含执行计划"
                ),
                DeliveryItem(
                    name="执行方案",
                    description="详细的落地执行方案",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.DOCX, FileFormat.PDF],
                    priority=1,
                    required=True,
                    notes="明确时间表和责任人"
                ),
                DeliveryItem(
                    name="评估报告",
                    description="现状评估和问题诊断报告",
                    category=DeliveryCategory.REPORT,
                    formats=[FileFormat.PDF, FileFormat.XLSX],
                    priority=2,
                    required=False,
                    notes="数据支撑，图表说明"
                ),
                DeliveryItem(
                    name="对比分析",
                    description="方案对比分析表格",
                    category=DeliveryCategory.DATA,
                    formats=[FileFormat.XLSX, FileFormat.PDF],
                    priority=2,
                    required=False,
                    notes="多维度评估"
                ),
                DeliveryItem(
                    name="预算清单",
                    description="项目预算明细表",
                    category=DeliveryCategory.DATA,
                    formats=[FileFormat.XLSX, FileFormat.PDF],
                    priority=2,
                    required=False,
                    notes="分项列示"
                ),
                DeliveryItem(
                    name="演示文稿",
                    description="汇报用的PPT演示文稿",
                    category=DeliveryCategory.DOCUMENT,
                    formats=[FileFormat.PPTX],
                    priority=3,
                    required=False,
                    notes="精炼核心观点"
                ),
            ],
            usage_guide="1. 调研诊断 2. 方案设计 3. 评审汇报 4. 细化执行",
            validation_checklist=[
                "问题分析准确到位",
                "方案逻辑清晰",
                "可行性经过论证",
                "预算合理有依据",
                "得到客户认可"
            ]
        )
    
    @staticmethod
    def get_standard_by_type(requirement_type: str, secondary_type: str = "", requirement_text: str = "") -> DeliveryStandard:
        """根据需求类型和二级类型获取对应的交付物标准"""
        standards = DeliveryStandards.get_all_standards()
        
        # 关键词到标准的映射（按优先级排序，电商最优先）
        keyword_mapping = [
            # 电商类（最优先）
            ("商城", "ecommerce"),
            ("电商", "ecommerce"),
            ("购物", "ecommerce"),
            ("支付", "ecommerce"),
            # 海报设计类
            ("海报", "marketing_poster"),
            ("宣传", "marketing_poster"),
            ("banner", "marketing_poster"),
            ("logo", "marketing_poster"),
            ("营销文案", "marketing_poster"),
            ("文案", "marketing_poster"),
            # 移动应用
            ("小程序", "mobile_app"),
            ("移动端", "mobile_app"),
            ("ios", "mobile_app"),
            ("android", "mobile_app"),
            ("app", "mobile_app"),
            # 数据分析
            ("分析", "data_analysis"),
            ("报表", "data_analysis"),
            ("统计", "data_analysis"),
            ("可视化", "data_analysis"),
            # 业务流程
            ("流程", "business_process"),
            ("审批", "business_process"),
            ("工作流", "business_process"),
            ("自动化", "business_process"),
            # 咨询（优先于Web）
            ("选型", "consulting"),
            ("技术选型", "consulting"),
            ("咨询", "consulting"),
            ("方案", "consulting"),
            ("评估", "consulting"),
            # 通用Web
            ("web", "web_design"),
            ("网站", "web_design"),
            ("网页", "web_design"),
            # 视频/动画
            ("视频", "video_production"),
            ("动画", "video_production"),
            # 图标
            ("图标", "marketing_poster"),
            # VI设计
            ("vi", "marketing_poster"),
            ("品牌设计", "marketing_poster"),
        ]
        
        def find_matching_standard(text: str) -> DeliveryStandard:
            """在文本中查找匹配的标准"""
            if not text:
                return None
            text_lower = text.lower()
            for keyword, standard_id in keyword_mapping:
                if keyword in text_lower:
                    for s in standards:
                        if s.id == standard_id:
                            return s
            return None
        
        # 优先根据需求文本匹配
        if requirement_text:
            matched = find_matching_standard(requirement_text)
            if matched:
                return matched
        
        # 然后根据二级类型匹配
        matched = find_matching_standard(secondary_type)
        if matched:
            return matched
        
        # 然后根据一级类型匹配
        type_mapping = {
            "技术开发": ["web_design", "mobile_app", "ecommerce"],
            "内容创作": ["marketing_poster", "web_design"],
            "数据分析": ["data_analysis"],
            "业务流程": ["business_process"],
            "问题解决": ["data_analysis", "consulting"],
            "咨询服务": ["consulting"],
        }
        
        for key, standard_ids in type_mapping.items():
            if key in requirement_type:
                for s in standards:
                    if s.id in standard_ids:
                        return s
        
        # 默认返回网站设计标准
        return standards[0]
    
    @staticmethod
    def generate_delivery_checklist(requirement_type: str, secondary_type: str = "", requirement_text: str = "") -> Dict[str, Any]:
        """生成针对特定需求的交付物清单"""
        standard = DeliveryStandards.get_standard_by_type(requirement_type, secondary_type, requirement_text)
        
        # 根据二级类型调整优先级
        items = standard.items.copy()
        
        # 生成简化的清单
        checklist = {
            "standard_name": standard.name,
            "required_items": [item.to_dict() for item in items if item.required],
            "optional_items": [item.to_dict() for item in items if not item.required],
            "validation_checklist": standard.validation_checklist,
            "usage_guide": standard.usage_guide
        }
        
        return checklist


def test_delivery_standards():
    """测试交付物标准"""
    print("🗂️ 交付物标准化模块测试")
    print("=" * 60)
    
    # 获取所有标准
    standards = DeliveryStandards.get_all_standards()
    print(f"共有 {len(standards)} 个交付物标准\n")
    
    # 测试电商标准
    ecommerce = DeliveryStandards.ecommerce()
    print(f"📦 {ecommerce.name}")
    print(f"描述: {ecommerce.description}")
    print(f"交付物数量: {len(ecommerce.items)}\n")
    
    for item in ecommerce.items:
        required_str = "✓" if item.required else "○"
        formats_str = ", ".join([f.value for f in item.formats])
        print(f"  [{required_str}] {item.name} ({formats_str})")
    
    print("\n" + "-" * 40)
    
    # 测试自动匹配
    print("\n🔍 类型自动匹配测试:")
    test_types = ["技术开发", "内容创作", "数据分析"]
    for t in test_types:
        matched = DeliveryStandards.get_standard_by_type(t)
        print(f"  {t} → {matched.name}")
    
    print("\n✅ 测试完成")


if __name__ == "__main__":
    test_delivery_standards()
