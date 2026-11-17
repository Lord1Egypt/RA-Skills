# 示例说明

`examples/` 目录用于存放本 Skill 的输入示例和完整运行示例。

## 当前文件

- `sample_resume.json` —— 简历生成脚本 `scripts/generate_resume.py` 的输入格式示例。

## 使用方法

```bash
# 安装依赖
pip install python-docx

# 生成示例简历
python scripts/generate_resume.py examples/sample_resume.json 示例简历.docx
```

## 完整 Skill 使用流程示例

用户输入：

> 这是我的简历（粘贴/上传简历），我想申请字节跳动 AI 产品经理实习生，JD 如下：...

Skill 自动执行：

1. 生成 `outputs/岗位调研.md`
2. 用户确认调研方向后，生成 `outputs/改后简历.docx`
3. 用户确认简历定稿后，生成 `outputs/面试准备.md`
