# 常见异常与处理方法 (TROUBLESHOOTING.md)

> **使用规则**：遇到异常时，主流程/子代理**必须先读取本文件**查找匹配的方案。
> 若本文件中无匹配方案，才自行分析处理。

---

## 1. 搜索代理配额耗尽
**现象**：搜索代理报"搜索配额不足"、"请提升配额"
**根因**：per-session 搜索配额主子代理共享硬限，多个代理并行时集体触顶
**方案**：
- 减少并发数至 `max(1, floor(剩余配额 / 72))`
- 优先用 WebFetch 抓取官方文档（不计入搜索配额）
- 剩余配额不足 72 时集中给 1 个代理

---

## 2. task-notification 元数据不实
**现象**：代理通知"搜索 85 次"，但实际文件仅 20 条来源
**根因**：task-notification 声明由代理自述，未经独立核验
**方案**：
- 仅以 `ls` + 文件大小 > 0 作为完成凭证
- 忽略所有元数据声明（"搜索 N 次"、"覆盖 M 个方向"等）
- 代理必须写入明确路径文件才算完成

---

## 3. `<code>` 标签导致字体异常
**现象**：全页等宽字体、正文颜色异常、块级标签样式泄漏
**根因**：`<code>` 开闭不匹配、`<code>` 内嵌套 `<p>`/`<table>` 等块级标签、`</code>` 写成 `</strong>`
**方案**：
- 运行 `python -X utf8 scripts/wordcount_check.py` 检查 `<code>` 完整性
- 问题消灭在草稿阶段，不要在 assemble 后才修

---

## 4. Windows 控制台 emoji 崩溃
**现象**：`UnicodeEncodeError: 'gbk' codec can't encode character '⚠'`
**根因**：Python 脚本含 emoji 输出（⚠️✅❌），Windows 默认 cp936 编码
**方案**：
- 所有 Python 脚本调用加 `-X utf8` 标志：`python -X utf8 scripts/xxx.py`
- 或设环境变量：`set PYTHONIOENCODING=utf-8`
- 已内置 `sys.stdout.reconfigure(encoding='utf-8')` 的脚本不需要

---

## 5. assemble.py 颜色归一误伤
**现象**：`.zh-answer__body code` 的 `background:#f8f8fa` 被替换成 `var(--zhihu-blue)`
**根因**：`is_blue()` 阈值 `b>0x80 and b>max(r,g)*0.8` 过宽，把浅蓝灰 #f8f8fa 也识别为蓝色系
**方案**：
- 阈值已收紧为 `b>0xC0 and b>max(r,g)*1.2`（v18）
- 如仍误伤，在对应 CSS 行加注释 `/* keep-hex */` 排除

---

## 6. autocheck 字典匹配失败
**现象**：autocheck 报"④ .zh-answer__body code 缺少 padding:3px 4px"
**根因**：CSS 压缩或格式化后 `padding:3px 4px` 可能变成 `padding:3px4px`（无空格）
**方案**：
- autocheck 已改用压缩格式匹配（v18），忽略空格差异

---

## 7. 子代理 Write/Bash 权限被拒
**现象**：agent 报 `Permission denied` 写入 `_draft_*.html`
**方案**：
- 检查 `.claude/settings.local.json` 的 `permissions.allow` 中是否包含 `Write(*:other/_draft_*.html)` 和 `Bash(python *:other/_draft_*.html *)`
- 确认 `additionalDirectories` 包含当前工作区路径

---

## 8. assemble.py 二次运行无效
**现象**：重跑 assemble.py 后页面无变化
**根因**：首次运行消费了 `<!-- ASSEMBLE -->` 标记
**方案**：
- 从 `./other/index_skeleton.html` 还原骨架
- 或在运行前手动恢复标记：`sed -i 's|</main>|\n  <!-- ASSEMBLE -->\n</main>|' index.html`

---

## 9. 头像图链全不可达
**现象**：curl 测试所有真实头像源都 timeout 或 403
**方案**：
- 降级到 DiceBear SVG 头像（已内置为默认策略）
- 标注"本轮头像因网络限制使用 DiceBear 替代"

---

## 10. 章节字数 agent 自述严重失真
**现象**：agent 自报 12,215 字，独立脚本实测仅 9,140 字（差 25%）
**根因**：agent 把 HTML 属性内中文或数字链接计入字数
**方案**：
- 每章写完后必须运行 **独立** 脚本 `python scripts/wordcount_check.py <文件路径>` 验收
- 结果 ≥11,000 且与 agent 自述差 ≤5%，否则扩写后重新验收

---

## 11. 来源池 token 浪费
**现象**：每个撰写 agent 收到完整 50+ URL 来源池，8 个 agent 重复消耗 ~16K token
**方案**：
- 完整来源池写入 `./research_result/source_pool.md`
- agent prompt 仅传 3-5 条专属 URL + 文件引用路径

---

## 12. scan_html.py 在 Windows 无响应
**现象**：双击或直接 `python scan_html.py` 无输出或闪退
**方案**：
- 必须加 `-X utf8`：`python -X utf8 scripts/scan_html.py`
- 或设 `PYTHONIOENCODING=utf-8`

---

## 13. 单文件打包时图片缺失
**现象**：`inline_images.py` 打印「缺失 M 张」，单文件里仍留着 `./images/xxx.png` 原路径
**根因**：`./images/` 下没有对应文件（curl 下载失败 / 文件名大小写或拼写与 HTML 引用不一致 / 扩展名被改名）
**方案**：
- 按「缺失清单」逐条核对 `./images/` 真实文件名，改 HTML 引用或补下载后重跑
- 只差 1-2 张且补不回来：可接受（其余已内嵌），但必须在交付通报里说明「N 张图片未能内嵌」
- 不要手工在单文件 HTML 里贴 base64——重跑脚本更可靠

---

## 14. 单文件 HTML 体积超 100 MiB
**现象**：base64 内嵌后文件 > 100 MiB，WorkBuddy 资料库提示体积超限
**根因**：图片总量大（高清截图/多张大图），base64 编码膨胀约 33%
**方案**：
- 交付本身不受影响，只是跳过资料库上传，如实告知用户
- 如需上传：先压缩 `./images/`（转 webp / 降分辨率 / 减质量）→ 重跑 `inline_images.py`
- 大版本（200%+）建议在阶段 4.5 就控制图片数量与单图体积

---

## 15. 删除 index.html 后又要改内容
**现象**：已交付单文件，发现要改文字或补章节，但 `index.html` 已删除
**方案**：
- 骨架在 `./other/index_skeleton.html`，章节草稿在 `./other/_draft_*.html`
- 恢复流程：`cp ./other/index_skeleton.html index.html` → 重跑 `assemble.py` → 重跑 `inline_images.py`
- **不要**直接在单文件 HTML 上编辑——满屏 base64 会干扰定位，且改动无法回流到草稿
