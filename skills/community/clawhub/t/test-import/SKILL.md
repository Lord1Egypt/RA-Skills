# ClawHub Publish

将本地 skill 发布到 ClawHub。

## 使用方法

```bash
python3 ~/.openclaw/workspace/skills/clawhub-publish/publish.py --slug <slug> --name "<名称>" --version <版本> --path <技能目录>
```

## 参数

- `--slug`: Skill slug (如 family-intent-recognition)
- `--name`: 显示名称 (如 家庭消费意图识别)
- `--version`: 版本号 (如 1.0.0)
- `--path`: 技能文件夹路径 (默认: 当前目录)
- `--changelog`: 更新日志 (可选)

## 示例

```bash
python3 ~/.openclaw/workspace/skills/clawhub-publish/publish.py \
  --slug family-intent-recognition \
  --name "家庭消费意图识别" \
  --version 1.0.0 \
  --path ~/.openclaw/workspace/skills/family-intent-recognition \
  --changelog "支持消费意图识别"
```

## Python 调用

```python
from publish import publish_skill

result = publish_skill(
    slug="family-intent-recognition",
    name="家庭消费意图识别", 
    version="1.0.0",
    skill_dir="/path/to/skill",
    changelog="更新说明"
)
print(result)
```
