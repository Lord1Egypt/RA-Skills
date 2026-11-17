import os
import sys

# 把 scripts/ 加入路径，使 `import route` 等可用
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
