# Wiki2Doc 使用示例

本文档提供实际使用场景的示例。

## 场景一：快速生成测试用例（推荐）

**需求：** 从Wiki需求页面一键生成完整的测试用例Excel

**命令：**
```bash
/skill wiki2doc --auto http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
```

**执行过程：**
1. ✓ 提取Wiki内容生成Word文档
2. ✓ 分析需求检测问题
3. ✓ 自动生成测试用例
4. ✓ 转换为Excel格式

**输出文件：**
- `Pad端适配需求.docx` - 需求Word文档
- `Pad端适配需求_analysis_report.txt` - 需求分析报告
- `Pad端适配需求_testcases.md` - 测试用例Markdown
- `Pad端适配需求_testcases.xlsx` - 测试用例Excel（最终交付）

**耗时：** 约 1-2 分钟

---

## 场景二：仅提取Wiki内容

**需求：** 只需要将Wiki内容保存为Word文档

**命令：**
```bash
/skill wiki2doc http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
```

**输出文件：**
- `需求标题.docx` - 包含文本和图片的Word文档

**适用场景：**
- 需求归档
- 离线查看
- 内容审阅

---

## 场景三：批量处理多个Wiki页面

**需求：** 一次处理多个Wiki页面

**命令：**
```bash
/skill wiki2doc --batch "http://10.225.1.76:8090/page1,http://10.225.1.76:8090/page2,http://10.225.1.76:8090/page3"
```

**输出：**
每个页面生成独立的Word文档

**适用场景：**
- 批量归档
- 批量导出
- 批量备份

---

## 场景四：独立分析需求文档

**需求：** 已有Word文档，需要分析需求质量

**命令：**
```bash
python bin/analyze/analyze_requirements.py demand/需求文档.docx
```

**输出：**
- JSON格式报告（机器可读）
- TXT格式报告（人类可读）

**报告内容：**
```
【遗漏点】
1. 功能缺少测试 (严重程度: high)
   描述: 文档中描述了功能模块，但缺少相应的测试要点
   建议: 建议为每个功能模块添加具体的测试要点

【矛盾点】
1. 数值矛盾 (严重程度: high)
   描述: 关于菜单数量的描述存在不同数值: ['9', '10']
   建议: 请确认正确的数值

【不明确点】
1. 模糊描述 (严重程度: medium)
   描述: 使用模糊词汇'适当'，没有具体的参数范围
   建议: 建议将'适当'替换为具体的数值
```

**适用场景：**
- 需求评审前的预检查
- 需求质量改进
- 发现潜在问题

---

## 场景五：为现有文档生成测试用例

**需求：** 已有需求文档，需要生成测试用例

**命令：**
```bash
python bin/generate/generate_testcases.py demand/需求文档.docx
```

**输出：**
- Markdown格式测试用例
- JSON格式测试用例

**生成的测试类型：**
- 正向测试（功能验证）
- 边界值测试
- 错误推测测试
- 场景测试
- UI测试
- 兼容性测试
- 性能测试

**适用场景：**
- 快速生成测试用例框架
- 补充测试用例
- 测试设计参考

---

## 场景六：Markdown转Excel

**需求：** 已有Markdown格式的测试用例，需要转为Excel

**命令：**
```bash
python bin/convert/md2excel.py demand/测试用例.md
```

**输出：**
- 格式化的Excel文件

**Excel特点：**
- 专业表格样式
- 自动列宽调整
- 表头高亮显示
- 边框和对齐优化
- 自动换行

**适用场景：**
- 测试用例格式转换
- 导入测试管理系统
- 团队共享

---

## 场景七：完整工作流（分步执行）

**需求：** 想要控制每个步骤，逐步执行

**步骤1：提取Wiki**
```bash
/skill wiki2doc http://10.225.1.76:8090/pages/viewpage.action?pageId=12345678
```

**步骤2：分析需求**
```bash
python bin/analyze/analyze_requirements.py demand/需求文档.docx
```
→ 查看分析报告，改进需求文档

**步骤3：生成测试用例**
```bash
python bin/generate/generate_testcases.py demand/需求文档.docx
```
→ 审阅Markdown文件，补充用例

**步骤4：转换Excel**
```bash
python bin/convert/md2excel.py demand/测试用例.md
```
→ 得到最终Excel文件

**优点：**
- 每步可控
- 可中间检查
- 可手动修改

---

## 实际案例：Pad端适配需求

### 输入
Wiki页面：`http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052`

### 命令
```bash
/skill wiki2doc --auto http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052
```

### 执行日志
```
[2026-03-06 14:30:15] [INFO] 开始执行完整工作流...
[2026-03-06 14:30:15] [INFO] Wiki URL: http://10.225.1.76:8090/pages/viewpage.action?pageId=34556052

============================================================
步骤1: 从Wiki提取内容并生成Word文档
============================================================
[2026-03-06 14:30:15] [INFO] 执行命令: python bin/wiki2doc.py ...
成功加载文档: Pad端适配需求.docx
✓ 成功生成Word文档: demand/Pad端适配需求.docx

============================================================
步骤2: 分析需求文档
============================================================
[2026-03-06 14:30:45] [INFO] 执行命令: python bin/analyze/analyze_requirements.py ...
提取文本内容: 5234 字符
发现遗漏点: 3 个
发现矛盾点: 1 个
发现不明确点: 2 个
发现不完整点: 1 个
✓ 成功生成分析报告: demand/Pad端适配需求_analysis_report.txt

============================================================
步骤3: 生成测试用例
============================================================
[2026-03-06 14:31:00] [INFO] 执行命令: python bin/generate/generate_testcases.py ...
提取到 12 个功能特性
生成正向测试用例...
生成边界值测试用例...
生成异常测试用例...
生成场景测试用例...
生成UI测试用例...
生成兼容性测试用例...
生成性能测试用例...
总计生成测试用例: 35 个
✓ 成功生成测试用例Markdown: demand/Pad端适配需求_testcases.md

============================================================
步骤4: 转换为Excel格式
============================================================
[2026-03-06 14:31:15] [INFO] 执行命令: python bin/convert/md2excel.py ...
提取到 35 个测试用例
Excel文件已生成: demand/Pad端适配需求_testcases.xlsx
总计测试用例: 35 条
✓ 成功生成Excel文件: demand/Pad端适配需求_testcases.xlsx

============================================================
工作流执行完成！
============================================================
✓ Word文档: demand/Pad端适配需求.docx
✓ 分析报告: demand/Pad端适配需求_analysis_report.txt
✓ 测试用例MD: demand/Pad端适配需求_testcases.md
✓ 测试用例Excel: demand/Pad端适配需求_testcases.xlsx

所有文件保存在: C:\Users\yanghua1\.claude\skills\wiki2doc\demand
```

### 输出结果

**1. Word文档**
- 文件：`Pad端适配需求.docx`
- 内容：完整的Wiki内容，包含文本和图片
- 大小：约 2.3 MB

**2. 分析报告**
- 文件：`Pad端适配需求_analysis_report.txt`
- 发现问题：7个（3个遗漏点、1个矛盾点、2个不明确点、1个不完整点）
- 建议：针对每个问题的具体改进建议

**3. 测试用例Markdown**
- 文件：`Pad端适配需求_testcases.md`
- 用例数：35个
- 分类：8个模块

**4. 测试用例Excel**
- 文件：`Pad端适配需求_testcases.xlsx`
- 格式：专业表格样式
- 列：编号、模块、标题、前置条件、步骤、优先级、预期结果

### 总耗时
约 1分30秒

---

## 常见问题排查

### 问题1：提示"找不到元素"
**原因：** Wiki页面结构与预期不同

**解决：**
```bash
# 检查页面结构
python bin/wiki2doc.py --debug http://...
```

### 问题2：图片下载失败
**原因：** 图片权限或链接失效

**解决：** 跳过失败图片，不影响其他内容

### 问题3：生成的用例不够详细
**原因：** 需求文档内容较少

**解决：**
1. 完善需求文档
2. 手动补充测试用例
3. 调整生成策略

---

## 进阶技巧

### 技巧1：自定义配置

创建配置文件 `~/.wiki2doc/config.json`：
```json
{
  "confluence_url": "http://your-wiki.com",
  "username": "your-username",
  "password": "your-password",
  "output_dir": "/custom/output/path"
}
```

### 技巧2：批量脚本

创建批处理脚本 `batch_process.sh`：
```bash
#!/bin/bash
urls=(
  "http://10.225.1.76:8090/page1"
  "http://10.225.1.76:8090/page2"
  "http://10.225.1.76:8090/page3"
)

for url in "${urls[@]}"; do
  echo "Processing: $url"
  /skill wiki2doc --auto "$url"
  echo "---"
done
```

### 技巧3：自动化测试用例管理

将生成的Excel导入测试管理系统：
1. 导出Excel
2. 使用测试管理系统的导入功能
3. 映射字段对应关系
4. 批量导入

---

## 最佳实践建议

1. **需求质量保证**
   - 在生成测试用例前，先运行需求分析
   - 根据分析报告改进需求文档
   - 确保需求完整、清晰、无矛盾

2. **测试用例优化**
   - 自动生成后进行人工审核
   - 删除重复或冗余的用例
   - 补充业务特定的测试场景
   - 调整优先级

3. **团队协作**
   - 将生成的文档共享给团队
   - 定期更新测试用例
   - 建立评审机制

4. **版本管理**
   - 保存历史版本的测试用例
   - 记录变更历史
   - 追踪需求变更

---

**祝您使用愉快！**
