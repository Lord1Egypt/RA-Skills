#!/usr/bin/env python3
"""初始化科幻小说项目的目录结构。"""

import sys
import os

def init_project(name: str):
    base = f"/home/claude/{name}"
    os.makedirs(f"{base}/chapters", exist_ok=True)

    files = {
        "settings.md": f"# {name} — 世界设定\n\n<!-- 在第1阶段填写 -->\n\n## 基本信息\n- 时代: \n- 舞台: \n- 技术水平: \n\n## 核心技术 / 新奇元素\n\n## 社会结构\n\n## 历史\n\n## 日常生活\n\n## 术语表\n",
        "plot.md": f"# {name} — 情节\n\n<!-- 在第2阶段填写 -->\n\n## 一句话梗概\n\n## 主题\n\n## 章节结构\n\n## 伏笔管理表\n\n| ID | 伏笔 | 埋入章节 | 回收章节 | 回收方式 |\n|----|------|--------|--------|----------|\n",
        "characters.md": f"# {name} — 角色设定\n\n<!-- 在第3阶段填写 -->\n",
        "notes.md": f"# {name} — 备忘录·创意\n\n",
    }

    for filename, content in files.items():
        path = os.path.join(base, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    print(f"✅ 项目 '{name}' 初始化完成: {base}")
    print(f"   - settings.md")
    print(f"   - plot.md")
    print(f"   - characters.md")
    print(f"   - chapters/")
    print(f"   - notes.md")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 init_project.py <project_name>")
        sys.exit(1)
    init_project(sys.argv[1])