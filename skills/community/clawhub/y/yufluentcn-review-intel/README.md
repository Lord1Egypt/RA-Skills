# yufluentcn-review-intel

买家评论情感与主题分析（JSON 洞察），经 Harness `review_analyze` 云端执行。

## 评论输入格式（摘要）

- **多条**：每条之间 **单独一行** `---`（推荐上下空一行）  
- **单条**：直接粘贴，无需分隔符  
- **文件**：`--reviews reviews.txt`（UTF-8）  

详见 [SKILL.md](./SKILL.md)。

## 调用

```powershell
cd skills\yufluentcn-review-intel
pip install -r requirements.txt
$env:TOKENAPI_KEY = "tk-你的密钥"

python scripts\run.py --reviews reviews.txt --product "蓝牙耳机" --platform amazon --lang zh -o out.json
```

## 打包
# 在仓库根目录执行

# 0.（建议）先把 _shared 同步进各技能 scripts/
.\scripts\sync-skill-shared.ps1

# 1. 一键打全包 → dist/skills/<slug>-<version>.zip
.\scripts\package-all-skills.ps1

# 或只打某一个
.\scripts\package-skill.ps1 yufluentcn-chat-assist


- 卖家指南：[docs/技能-评论分析客户指南.md](../../docs/技能-评论分析客户指南.md)  
- API：`POST /v1/skills/review-intel/run`
