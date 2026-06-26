# Workspace浏览器3.0 配置文件

# 服务器配置
PORT = 5001
HOST = '0.0.0.0'
DEBUG = False

# 应用配置
WORKSPACE_ROOT = '/root/.openclaw/workspace'  # workspace根目录

# AI解释配置
AI_MODEL = 'deepseek/deepseek-reasoner'  # 使用的AI模型
AI_TIMEOUT = 90  # AI解释超时时间（秒）
AI_MAX_RETRIES = 3  # AI解释重试次数

# 搜索配置
SEARCH_MAX_RESULTS = 200  # 最大搜索结果数
SEARCH_TIMEOUT = 10  # 搜索超时时间（秒）

# 文件树配置
MAX_DIRECT_ITEMS = 100  # 直接显示的最大项目数
MAX_TOTAL_ITEMS = 1000  # 总项目数限制
MAX_FILE_SIZE = 10 * 1024 * 1024  # 最大文件大小（10MB）
ALLOWED_EXTENSIONS = ['.py', '.js', '.html', '.css', '.md', '.txt', '.json', '.yml', '.yaml', '.xml']  # 允许的文件扩展名

# 数据库配置
import os
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explanations.db')  # 数据库文件完整路径
DB_BACKUP_DAYS = 7  # 备份保留天数

# 代码解释配置
MAX_FILE_SIZE_FOR_EXPLANATION = 100 * 1024  # 最大解释文件大小（100KB）
EXPLANATION_TIMEOUT = 90  # 解释生成超时时间（秒）
EXPLANATION_MAX_LENGTH = 5000  # 解释最大长度
EXPLANATION_CACHE_DURATION = 7 * 24 * 60 * 60  # 解释缓存持续时间（7天，秒）

# 安全配置
ALLOWED_PATHS = ['/root/.openclaw/workspace']  # 允许访问的路径
BLOCKED_EXTENSIONS = ['.exe', '.dll', '.so', '.sh', '.bat', '.cmd']  # 阻止的文件扩展名

# AI配置
AI_MAX_TOKENS = 4000
AI_TEMPERATURE = 0.7
AI_SYSTEM_MESSAGE = "你是一个代码解释助手，请用中文简要解释代码的核心功能、实现逻辑和算法。"
EXPLANATION_PROMPT_TEMPLATE = "请简要解释以下{language}代码的核心功能、实现逻辑和算法：\n\n{code}"

# DeepSeek API配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = ""  # 需要用户自己配置

# 显示配置
MAX_DISPLAY_ITEMS = 50

# 语言映射
LANGUAGE_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.html': 'HTML',
    '.css': 'CSS',
    '.md': 'Markdown',
    '.txt': 'Text',
    '.json': 'JSON',
    '.yml': 'YAML',
    '.yaml': 'YAML',
    '.xml': 'XML',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.go': 'Go',
    '.rs': 'Rust',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.ts': 'TypeScript',
    '.sql': 'SQL'
}