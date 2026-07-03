# 常见问题排查

## 1. ModuleNotFoundError: No module named 'openpyxl'

**现象**：运行 writer.py 报错 `ModuleNotFoundError`
**原因**：未安装 openpyxl 依赖
**解决**：
```bash
pip install openpyxl
```

## 2. JSON 解析错误

**现象**：报错 `json.decoder.JSONDecodeError`
**原因**：JSON 格式不正确（中英文引号混用、尾部多余逗号等）
**排查**：
```bash
python -c "import json; json.load(open('data.json'))"
```

## 3. KeyError: '用例编号'

**现象**：报错 `KeyError: '用例编号'`
**原因**：JSON 中字段名不匹配（使用英文或错误中文字段名）
**解决**：字段名必须为中文，参见 `references/templates.md`

## 4. Excel 文件损坏或无法打开

**现象**：生成的 Excel 文件提示损坏
**解决**：
```bash
# 检查输出目录
mkdir -p output
```

## 5. 中文乱码

**现象**：Excel 中中文显示为乱码
**原因**：文件编码问题
**解决**：读取 JSON 时指定 `encoding='utf-8'`

## 6. Python 版本过低

**现象**：语法错误或功能缺失
**解决**：升级 Python 至 3.8+

## 7. 输出路径不存在

**现象**：报错 `FileNotFoundError` 或 `PermissionError`
**解决**：使用绝对路径或先创建目录

## 8. 步骤内容缺失

**现象**：Excel 中操作步骤或预期结果为空
**原因**：JSON 步骤字段名不匹配
**注意**：步骤内部字段必须是 `步骤`、`操作`、`预期`

## 快速诊断

```bash
# 1. 检查 Python 版本
python --version

# 2. 检查 openpyxl
python -c "import openpyxl; print('OK')"

# 3. 验证 JSON 格式
python -c "import json; json.load(open('your_file.json')); print('JSON OK')"

# 4. 测试 writer.py
echo '{"测试用例":[{"用例编号":"TC-001","业务域":"测试","优先级":"P0","测试维度":"功能","设计方法":"场景法","测试场景":"测试","测试点":"测试","操作步骤":[{"步骤":1,"操作":"测试","预期":"测试"}],"测试数据":"测试","需求来源":"REQ-001"}]}' | python scripts/writer.py
```
