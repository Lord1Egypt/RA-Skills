#!/usr/bin/env python3
"""
超脑首次安装脚本
确保AI每次会话都会想起使用超脑
"""

import os
import sys
from pathlib import Path

def install():
    """安装超脑启动提醒到用户工作空间"""
    
    workspace = Path.home() / '.openclaw' / 'workspace'
    tools_md = workspace / 'TOOLS.md'
    
    # 启动检查清单内容
    startup_checklist = """
## ⚠️ 会话启动检查清单（超脑）

**每次会话开始必须执行：**

```bash
python3 -c "
import sqlite3, os
user_id = os.environ.get('USER_ID', '')
conn = sqlite3.connect(Path.home() / '.openclaw' / 'super-brain.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM user_profile WHERE user_id = ?', [user_id])
profile = cursor.fetchone()
if profile:
    print(f'用户画像: {profile[\"communication_style\"]} / {profile[\"technical_level\"]}')
conn.close()
"
```

**不执行 = 超脑未激活**
"""
    
    # 如果TOOLS.md不存在，创建它
    if not tools_md.exists():
        tools_md.write_text(f"# TOOLS.md - 本地配置\n{startup_checklist}\n")
        print("✅ 已创建 TOOLS.md")
    else:
        # 如果已存在，检查是否已有超脑检查清单
        content = tools_md.read_text()
        if "超脑" not in content and "会话启动检查清单" not in content:
            # 添加到文件开头
            new_content = f"# TOOLS.md - 本地配置\n{startup_checklist}\n\n{content}"
            tools_md.write_text(new_content)
            print("✅ 已添加超脑启动检查清单到 TOOLS.md")
        else:
            print("ℹ️ TOOLS.md 已包含超脑配置")
    
    print("\n📋 安装完成！")
    print("   超脑会在每次会话开始时自动激活")
    print("   数据库: ~/.openclaw/super-brain.db")
    
    return 0

if __name__ == "__main__":
    sys.exit(install())
