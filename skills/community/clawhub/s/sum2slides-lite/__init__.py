"""
OpenClaw PPT制作Skill
支持多PPT软件和多通信平台的PPT自动化生成工具
"""

__version__ = "1.0.0"
__author__ = "OpenClaw Team"
__description__ = "自动化PPT生成和分享工具"

# 导出核心功能
from core.base_generator import (
    BasePPTGenerator,
    PPTStructure,
    SlideContent,
    PPTSoftware,
    PPTTemplate,
    GeneratorFactory
)

from core.pptx_generator import PPTXGenerator
from core.content_planner import ContentPlanner

# 导出平台功能
from platforms.base_platform import (
    BasePlatform,
    PlatformConfig,
    PlatformType,
    UploadResult,
    MessageResult,
    PlatformFactory
)

from platforms.feishu.feishu_platform import FeishuPlatform

# 导出配置管理
from config.settings import (
    ConfigManager,
    GlobalSettings,
    PlatformSettings,
    GeneratorSettings,
    get_config_manager
)

# 导出工具函数
from utils.logger import setup_logger
from utils.error_handler import handle_error, retry_with_backoff
from utils.file_utils import validate_file, create_temp_file, cleanup_temp_files

# 快捷函数
def create_ppt(title: str, content: list, software: str = "powerpoint", 
              template: str = "business") -> str:
    """
    快捷函数：创建PPT
    
    Args:
        title: PPT标题
        content: 内容列表
        software: PPT软件类型
        template: 模板类型
        
    Returns:
        生成的PPT文件路径
    """
    from core.base_generator import PPTSoftware, PPTTemplate
    
    # 创建生成器
    software_type = PPTSoftware(software)
    template_type = PPTTemplate(template)
    generator = GeneratorFactory.create_generator(software_type, template_type)
    
    # 创建结构
    structure = PPTStructure(
        title=title,
        slides=[
            SlideContent(title=f"第{i+1}页", content=[item])
            for i, item in enumerate(content)
        ]
    )
    
    # 生成PPT
    return generator.generate_from_structure(structure)


def upload_ppt(ppt_file: str, platform: str = "feishu", 
              config: dict = None) -> dict:
    """
    快捷函数：上传PPT到指定平台
    
    Args:
        ppt_file: PPT文件路径
        platform: 平台类型
        config: 平台配置
        
    Returns:
        上传结果
    """
    from platforms.base_platform import PlatformType, PlatformConfig, PlatformFactory
    
    # 获取配置
    if config is None:
        config_manager = get_config_manager()
        platform_config = config_manager.get_platform_config(platform)
        config_dict = platform_config
    else:
        config_dict = config
    
    # 创建平台配置
    platform_type = PlatformType(platform)
    platform_config = PlatformConfig(
        platform_type=platform_type,
        **config_dict
    )
    
    # 创建平台实例
    platform_instance = PlatformFactory.create_platform(platform_type, platform_config)
    
    # 上传文件
    return platform_instance.upload_and_share(ppt_file)


def create_and_upload(title: str, content: list, platform: str = "feishu",
                     software: str = "powerpoint", template: str = "business") -> dict:
    """
    快捷函数：创建并上传PPT
    
    Args:
        title: PPT标题
        content: 内容列表
        platform: 目标平台
        software: PPT软件类型
        template: 模板类型
        
    Returns:
        完整的结果字典
    """
    try:
        # 1. 创建PPT
        print(f"📝 创建PPT: {title}")
        ppt_file = create_ppt(title, content, software, template)
        
        if not ppt_file:
            return {"success": False, "error": "PPT创建失败"}
        
        print(f"✅ PPT创建成功: {ppt_file}")
        
        # 2. 上传到平台
        print(f"📤 上传到{platform}...")
        upload_result = upload_ppt(ppt_file, platform)
        
        if upload_result.get('success'):
            print(f"✅ 上传成功!")
            print(f"🔗 访问链接: {upload_result.get('file_url')}")
            
            return {
                "success": True,
                "ppt_file": ppt_file,
                "upload_result": upload_result,
                "file_url": upload_result.get('file_url')
            }
        else:
            print(f"❌ 上传失败: {upload_result.get('error', '未知错误')}")
            return {
                "success": False,
                "error": upload_result.get('error'),
                "ppt_file": ppt_file
            }
            
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


# 主工作流类
class PPTWorkflow:
    """PPT制作工作流"""
    
    def __init__(self, config_file: str = None):
        """
        初始化工作流
        
        Args:
            config_file: 配置文件路径
        """
        self.config_manager = get_config_manager(config_file)
        self.logger = setup_logger()
        
        # 设置默认值
        self.default_software = self.config_manager.generator_settings.default_generator
        self.default_platform = self.config_manager.platform_settings.default_platform
        self.default_template = self.config_manager.generator_settings.powerpoint_template
        
    def run(self, user_input: str, platform: str = None, 
           software: str = None, template: str = None) -> dict:
        """
        运行完整工作流
        
        Args:
            user_input: 用户需求描述
            platform: 目标平台
            software: PPT软件类型
            template: 模板类型
            
        Returns:
            完整的工作流结果
        """
        # 使用默认值或参数值
        platform = platform or self.default_platform
        software = software or self.default_software
        template = template or self.default_template
        
        self.logger.info(f"🚀 开始PPT制作工作流")
        self.logger.info(f"   用户需求: {user_input}")
        self.logger.info(f"   目标平台: {platform}")
        self.logger.info(f"   PPT软件: {software}")
        self.logger.info(f"   模板类型: {template}")
        
        try:
            # 1. 内容规划
            planner = ContentPlanner()
            structure = planner.plan_from_input(user_input)
            
            # 2. 创建PPT
            generator = GeneratorFactory.create_generator(
                PPTSoftware(software),
                PPTTemplate(template)
            )
            ppt_file = generator.generate_from_structure(structure)
            
            # 3. 上传到平台
            upload_result = upload_ppt(ppt_file, platform)
            
            if upload_result.get('success'):
                result = {
                    "success": True,
                    "user_input": user_input,
                    "structure": structure,
                    "ppt_file": ppt_file,
                    "upload_result": upload_result,
                    "file_url": upload_result.get('file_url')
                }
                
                self.logger.info("🎉 工作流执行成功!")
                return result
            else:
                self.logger.error(f"❌ 上传失败: {upload_result.get('error')}")
                return {
                    "success": False,
                    "error": upload_result.get('error'),
                    "user_input": user_input,
                    "ppt_file": ppt_file
                }
                
        except Exception as e:
            self.logger.error(f"❌ 工作流执行异常: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return {
                "success": False,
                "error": str(e),
                "user_input": user_input
            }


# 导出主工作流
__all__ = [
    # 核心功能
    'BasePPTGenerator',
    'PPTStructure',
    'SlideContent',
    'PPTSoftware',
    'PPTTemplate',
    'GeneratorFactory',
    'PPTXGenerator',
    'ContentPlanner',
    
    # 平台功能
    'BasePlatform',
    'PlatformConfig',
    'PlatformType',
    'UploadResult',
    'MessageResult',
    'PlatformFactory',
    'FeishuPlatform',
    
    # 配置管理
    'ConfigManager',
    'get_config_manager',
    
    # 工具函数
    'setup_logger',
    'handle_error',
    'retry_with_backoff',
    
    # 快捷函数
    'create_ppt',
    'upload_ppt',
    'create_and_upload',
    
    # 主工作流
    'PPTWorkflow',
    
    # 元数据
    '__version__',
    '__author__',
    '__description__'
]