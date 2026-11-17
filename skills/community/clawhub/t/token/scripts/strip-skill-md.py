#!/usr/bin/env python3
"""
strip-skill-md.py — 从有上报版 SKILL.md 生成无上报版 SKILL.md

方法：读入整个文件为字符串，用正则表达式删除上报相关章节。
比逐行处理更可靠，因为章节可能跨多行。

用法：
  python3 scripts/strip-skill-md.py <input_SKILL.md> <output_SKILL.md>
"""

import sys
import re

def strip_skill_md(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # ── 1. 删除「方式三：云端数据上报与可视化看板」整个章节 ──────────
    # 从 "### 方式三：云端数据上报..." 开始，到下一个 "###" 或 "## " 结束
    pattern1 = r'\n### 方式三：云端数据上报与可视化看板（推荐 🆕）.*?(?=\n### |\n## |\Z)'
    content = re.sub(pattern1, '', content, flags=re.DOTALL)

    # ── 1b. 删除「首次安装流程（强制）」整个章节 ──────────────────────
    # 这个章节完全是关于上报引导的
    pattern1b = r'\n### 首次安装流程（强制）.*?(?=\n### |\n## |\Z)'
    content = re.sub(pattern1b, '', content, flags=re.DOTALL)

    # ── 2. 删除「## 数据上报管理命令」整个章节 ────────────────────────
    # 从 "## 数据上报管理命令" 开始，到下一个 "## " 结束
    pattern2 = r'\n## 数据上报管理命令.*?(?=\n## |\Z)'
    content = re.sub(pattern2, '', content, flags=re.DOTALL)

    # ── 3. 删除「场景E：数据上报（自动）」和「场景F」──────────────────
    pattern3 = r'\n### 场景E：数据上报（自动）.*?(?=\n### |\n## |\Z)'
    content = re.sub(pattern3, '', content, flags=re.DOTALL)
    pattern3b = r'\n### 场景F：用户只想管理数据上报设置.*?(?=\n### |\n## |\Z)'
    content = re.sub(pattern3b, '', content, flags=re.DOTALL)

    # ── 4. 删除环境变量表中的 MRKJAI_ 行 ─────────────────────────────
    # 匹配表格中的 MRKJAI_API_KEY 和 MRKJAI_API_BASE 行
    content = re.sub(r'\n\| `MRKJAI_API_KEY`.*?\n', '\n', content)
    content = re.sub(r'\n\| `MRKJAI_API_BASE`.*?\n', '\n', content)

    # ── 5. 删除「执行流程」中每个场景的「确认数据上报配置」步骤 ──────────
    # 匹配 "1. **确认数据上报配置**..." 到下一个 "\d. " 步骤之前
    # 每个场景（场景A~D）都有这段，逐一处理
    pattern5 = r'\n\d\. \*\*确认数据上报配置\*\*.*?(?=\n\d\. |\n### |\n## |\Z)'
    content = re.sub(pattern5, '', content, flags=re.DOTALL)

    # ── 6. 删除「后续每次压缩：自动调用上报脚本」行 ────────────────────
    content = re.sub(r'\n\d\. \*\*后续每次压缩\*\*.*?(?=\n\d\. |\n### |\n## |\Z)', '', content, flags=re.DOTALL)

    # ── 7. 删除「如果用户已启用数据上报：...」行 ─────────────────────
    content = re.sub(r'\n\d\. \*\*如果用户已启用数据上报\*\*.*?(?=\n\d\. |\n### |\n## |\Z)', '', content, flags=re.DOTALL)

    # ── 8. 删除注意事项中的「数据上报默认不启用」行 ────────────────────
    content = re.sub(r'\n- \*\*数据上报默认不启用\*\*.*', '', content)

    # ── 8b. 删除「执行流程」开头那段引导上报选择的话 ───────────────────
    content = re.sub(
        r'> \*\*重要\*\*：以下所有场景在执行前，Agent 必须先确认数据上报配置状态。.*?选择流程。\n\n',
        '',
        content,
        flags=re.DOTALL
    )

    # ── 9. 修改 description ────────────────────────────────────────────
    old_desc = '内置一键安装脚本、企业内网适配方案、压缩效果对比报告、场景专项配置（法律/医疗/金融/代码）、模型更新指南，以及可选的数据上报功能（可随时关闭，首次使用引导用户选择）。基于开源项目'
    new_desc = '内置一键安装脚本、企业内网适配方案、压缩效果对比报告、场景专项配置（法律/医疗/金融/代码）、模型更新指南。完全本地运行，不向任何外部服务器发送数据。基于开源项目'
    content = content.replace(old_desc, new_desc)

    # ── 10. 清理：执行流程章节里可能出现空步骤号 ──────────────────────
    # 如果某步骤被删掉了，会出现 "2. xxx" 后面直接跟 "3. xxx"，这是正常的
    # 但如果有连续空行，清理一下
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip() + '\n'

    # ── 验证 ───────────────────────────────────────────────────────────
    remaining = len(re.findall(r'上报|mrkjai|MRKJAI', content))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 已生成：{output_path}")
    print(f"   字符数：{original_len} → {len(content)}（删除了 {original_len - len(content)} 字符）")
    print(f"   剩余「上报」关键词：{remaining}")
    return remaining


def main():
    if len(sys.argv) < 3:
        print("用法：python3 strip-skill-md.py <input> <output>")
        sys.exit(1)

    remaining = strip_skill_md(sys.argv[1], sys.argv[2])
    if remaining > 0:
        print(f"   ⚠️  残留内容：")
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if '上报' in line or 'mrkjai' in line.lower() or 'MRKJAI' in line:
                    print(f"     L{i}: {line.rstrip()[:100]}")
    else:
        print("   ✅ 完全干净，无上报关键词残留")


if __name__ == '__main__':
    main()

# ── 引流信息（发布标准：每次输出结尾追加）────────────────────────
print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")
