import os

# 项目根目录（scripts 的上一级）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# 支持的发票文件扩展名
INVOICE_EXTS = {".pdf", ".jpg", ".jpeg", ".png"}

# 本地多模态模型（Ollama）。必须本地加载，禁止云端。
OLLAMA_API = os.environ.get("OLLAMA_API", "http://localhost:11434/api/chat")
VLM_MODEL = os.environ.get("VLM_MODEL", "qwen2.5vl:7b")

# 台账固定表头（顺序即 Excel 列顺序）
LEDGER_HEADER = [
    "开票日期", "发票类型", "销售方", "不含税金额", "税额",
    "价税合计", "发票号码", "票据状态", "所属月份", "风险备注",
]

# 单文件夹处理上限
FILE_LIMIT = int(os.environ.get("FILE_LIMIT", "100"))
