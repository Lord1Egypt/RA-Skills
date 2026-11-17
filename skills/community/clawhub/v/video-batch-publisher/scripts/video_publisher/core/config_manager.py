import yaml
import os
import logging

from core.constants import BROWSER_PROFILE_DIR

logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器 - 加载配置、解析路径、自动创建目录"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def load_global_config(self, config_path="config.yaml"):
        """加载全局配置文件"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
            # 兼容：content_types 支持 list 写法，统一转成以 key 为索引的 dict（保持对外 dict 视图）
            cts = self._config.get("content_types")
            if isinstance(cts, list):
                indexed = {}
                for item in cts:
                    k = item.get("key") or item.get("type_name") or item.get("display_name")
                    if not k:
                        raise ValueError("content_types 列表项缺少 key/type_name 字段")
                    indexed[k] = item
                self._config["content_types"] = indexed
            logger.info("配置文件加载成功")
            return self._config
        except Exception as e:
            logger.error(f"加载配置文件失败：{str(e)}")
            raise
    
    def get_all_content_types(self):
        """获取所有内容类型配置"""
        if not self._config:
            self.load_global_config()
        return self._config.get("content_types", {})
    
    def get_type_paths(self, content_type):
        """获取指定内容类型的路径配置"""
        types = self.get_all_content_types()
        if content_type not in types:
            raise ValueError(f"内容类型 '{content_type}' 不存在于配置中")
        
        config = types[content_type]
        return {
            "display_name": config.get("type_name", config.get("display_name", content_type)),
            "collection": config.get("collection", ""),
            "input_dir": self.standard_path(config["input_dir"]),
            "output_dir": self.standard_path(config["output_dir"]),
            "excel_file": self.standard_path(config["excel_file"])
        }
    
    def get_type_config(self, type_key):
        """获取某个类型的完整配置"""
        if not self._config:
            self.load_global_config()
        return self._config.get("content_types", {}).get(type_key, {})
    
    def get_type_display(self, type_key):
        """获取某个类型的显示名（优先 type_name，兼容旧 display_name）"""
        config = self.get_type_config(type_key)
        return config.get("type_name", config.get("display_name", type_key))
    
    def get_type_covers(self, type_key):
        """获取某个类型的封面配置"""
        config = self.get_type_config(type_key)
        return config.get("covers", {})

    def get_collection_for_type(self, type_key):
        """获取某个类型的合集名称（发布时归入合集；空字符串=不指定合集）"""
        config = self.get_type_config(type_key)
        return config.get("collection", "")

    def get_ai_label_for_type(self, type_key):
        """获取某个类型是否勾选「AI生成内容」声明（默认 False）"""
        config = self.get_type_config(type_key)
        return bool(config.get("ai_label", False))
    
    @property
    def type_keys(self):
        """所有内容类型 key 列表"""
        if not self._config:
            self.load_global_config()
        return list(self._config.get("content_types", {}).keys())
    
    @property
    def type_display(self):
        """显示名映射 {type_key: display_name}"""
        if not self._config:
            self.load_global_config()
        return {
            k: v.get("type_name", v.get("display_name", k))
            for k, v in self._config.get("content_types", {}).items()
        }
    
    @property
    def type_covers(self):
        """封面配置映射 {type_key: {horizontal/vertical: filename}}"""
        if not self._config:
            self.load_global_config()
        return {
            k: v.get("covers", {})
            for k, v in self._config.get("content_types", {}).items()
        }
    
    def get_system_config(self):
        """获取系统配置"""
        if not self._config:
            self.load_global_config()
        return self._config.get("system", {})
    
    def get_browser_config(self):
        """获取浏览器配置（默认使用 BROWSER_PROFILE_DIR 作为用户数据目录）"""
        system = self.get_system_config()
        browser_config = system.get("browser", {})
        
        # 设置默认的用户数据目录
        if "user_data_dir" not in browser_config:
            browser_config["user_data_dir"] = BROWSER_PROFILE_DIR
        
        return browser_config
    
    def get_publish_time_format(self):
        """获取发布时间格式"""
        system = self.get_system_config()
        return system.get("publish_time_format", "%Y-%m-%d %H:%M")
    
    def get_platform_default_status(self):
        """获取平台默认勾选状态"""
        if not self._config:
            self.load_global_config()
        return self._config.get("platforms", {})

    def get_excel_filter_config(self):
        """获取 Excel 待发布过滤配置（是否要求 draft_finished/video_finished 列标记完成、及其列名）"""
        if not self._config:
            self.load_global_config()
        return self._config.get("excel", {})
    
    def standard_path(self, path):
        """标准化路径 - 支持绝对路径和相对路径"""
        if not path:
            return path
        
        # 转换为绝对路径
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        
        # 统一使用系统分隔符
        path = os.path.normpath(path)
        return path
    
    def ensure_directory_exists(self, dir_path):
        """确保目录存在，不存在则创建"""
        if not dir_path:
            return
        
        dir_path = self.standard_path(dir_path)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logger.info(f"创建目录：{dir_path}")
            except Exception as e:
                logger.error(f"创建目录失败 {dir_path}：{str(e)}")
                raise
    
    def ensure_output_directories(self):
        """确保所有输出目录存在"""
        types = self.get_all_content_types()
        for content_type, config in types.items():
            output_dir = self.standard_path(config["output_dir"])
            self.ensure_directory_exists(output_dir)
        
        # 确保浏览器缓存目录存在
        browser_config = self.get_browser_config()
        user_data_dir = browser_config.get("user_data_dir")
        if user_data_dir:
            self.ensure_directory_exists(user_data_dir)
    
    def validate_excel_file(self, excel_path):
        """验证Excel文件是否存在"""
        excel_path = self.standard_path(excel_path)
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel文件不存在：{excel_path}")
        return excel_path

# 全局单例
config_manager = ConfigManager()

def load_global_config(config_path="config.yaml"):
    return config_manager.load_global_config(config_path)

def get_all_content_types():
    return config_manager.get_all_content_types()

def get_type_paths(content_type):
    return config_manager.get_type_paths(content_type)

def get_system_config():
    return config_manager.get_system_config()

def get_browser_config():
    return config_manager.get_browser_config()

def get_publish_time_format():
    return config_manager.get_publish_time_format()

def get_platform_default_status():
    return config_manager.get_platform_default_status()

def get_excel_filter_config():
    return config_manager.get_excel_filter_config()

def standard_path(path):
    return config_manager.standard_path(path)

def ensure_directory_exists(dir_path):
    return config_manager.ensure_directory_exists(dir_path)

def ensure_output_directories():
    return config_manager.ensure_output_directories()

def validate_excel_file(excel_path):
    return config_manager.validate_excel_file(excel_path)

# 新增：内容类型快捷方法
def get_type_config(type_key):
    return config_manager.get_type_config(type_key)

def get_type_display(type_key):
    return config_manager.get_type_display(type_key)

def get_type_covers(type_key):
    return config_manager.get_type_covers(type_key)

def get_ai_label_for_type(type_key):
    return config_manager.get_ai_label_for_type(type_key)

def get_all_type_keys():
    return config_manager.type_keys

def get_all_type_display():
    return config_manager.type_display

def get_all_type_covers():
    return config_manager.type_covers