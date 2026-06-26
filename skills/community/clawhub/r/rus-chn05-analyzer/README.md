# 慧龄云(R)中华05骨龄智能分析技能（RUS-CHN05）

[![技能类型](https://img.shields.io/badge/技能-医学AI分析-blue)](https://github.com)
[![中华05标准](https://img.shields.io/badge/评估标准-RUS--CHN05-green)](https://github.com)
[![API验证](https://img.shields.io/badge/API-源码验证通过-brightgreen)](https://github.com)

> 基于慧龄云(R)骨龄人工智能检测系统，采用中华05标准RUS-CHN05计分法，通过分析左手腕部正位X光片，自动评估3~18岁儿童青少年骨骼发育程度。

## 功能特性

- **AI自动推算骨龄** — 中华05标准（RUS-CHN05计分法），推理服务器端执行
- **成年身高预测** — 查表法，含CMH-C/FPH-C遗传靶身高
- **13块骨骼逐等级评分** — 桡骨、尺骨、掌骨、指骨等
- **两种调用路径** — 轻量路径（仅骨龄）+ 完整路径（骨龄+身高预测）
- **真实联调验证** — 所有接口已通过真实账号全流程测试

## 快速开始

### 1. 环境准备

```bash
pip install requests
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的慧龄云(R)账号信息
```

### 3. 运行接入示例

**第三方接入（轻量路径 — 仅骨龄识别）**：
```bash
python examples/third_party_integration.py \
  --image bone.jpg --sex M
```

**C端接入（完整路径 — 骨龄+身高预测）**：
```bash
python examples/c_end_integration.py \
  --image bone.jpg --sex M --age 10.5 --height 140 \
  --father-height 175 --mother-height 163 --phone 13800000000
```

## 两种调用路径

### 路径A：轻量路径（第三方接入推荐）

```
注册激活 → 密码登录 → 图片上传 → cosBoneAgeOnLineByThirdPartner
```

- **参数**：仅需 fileName + sex
- **返回**：骨龄(bam)、SMS、stages、scores、标注图(url)
- **计费**：无条件扣次数（counts必须>0）
- **角色**：需"第三方"Shiro角色

### 路径B：完整路径（C端用户推荐）

```
注册激活 → 密码登录 → 图片上传 → cosBoneAgeOnLine(AI识别) → predictHeightByBoneAge(身高预测)
```

- **参数**：sex + age + height + stages + 父母身高 等
- **返回**：骨龄 + 预测身高 + 遗传靶身高 + 评估报告URL
- **限频**：非会员 cosBoneAgeOnLine 1次/30分钟，VIP无限

## 核心API调用流程

```python
import hashlib, requests, os

host = "https://www.pipitu.net"
session = requests.Session()
session.headers.update({"Content-Type": "application/json; charset=utf-8"})

# Step 1: 登录
password_hash = hashlib.sha256("your_password".encode()).hexdigest()
resp = session.post(f"{host}/auth/local/login",
    json={"username": "your_phone", "password": password_hash})
token = resp.json()["data"]["token"]
# ⚠️ Header名是"token"，不是"Authorization: Bearer"
session.headers.update({"token": token})

# Step 2: 上传图片
resp = session.post(f"{host}/service/signForBAImageUploadEasy",
    json={"fileName": "bone.jpg"})
signed_url = resp.json()["data"]["signedUrl"]
with open("bone.jpg", "rb") as f:
    requests.put(signed_url, data=f.read())

# Step 3: AI骨龄识别
resp = session.post(f"{host}/bmd/v2/cosBoneAgeOnLineByThirdPartner",
    json={"fileName": "bone.jpg", "sex": "M"})
result = resp.json()["data"]
print(f"骨龄: {result['bam']}岁, SMS: {result['sms']}")
```

## 目录结构

```
rus-chn05-analyzer/
├── SKILL.md                          # 技能主文件（触发词、分析流程、报告模板）
├── README.md                         # 本文件
├── .env.example                      # 环境变量配置模板
├── references/
│   └── api-protocol.md               # 完整API接口协议（源码验证版）
├── scripts/
│   └── bone_age_api_client.py        # Python API客户端（完整6步流程）
└── examples/
    ├── third_party_integration.py    # 第三方接入示例（路径A）
    └── c_end_integration.py          # C端接入示例（路径B）
```

## 关键注意事项

| 项目 | 说明 |
|------|------|
| Token Header | `token: {JWT}`（不是 `Authorization: Bearer`） |
| 密码传输 | SHA256加密后传输，禁止明文 |
| 第三方接口 | 需要"第三方"Shiro角色 + counts>0 |
| VIP vs 非会员 | VIP无限频+插值法精度更高；非会员有限频 |
| fileName字段 | 上传用`fileName`，AI推算用`detectedImgName`，人工修改用`selectedFileName` |
| 返回字段名 | 轻量路径返回`bam`/`fname`，完整路径返回`bam05` |

## 免责声明

本技能评估结果由AI辅助生成，仅供参考，不构成医疗诊断。骨龄评估存在约 +/-1 岁的正常观察误差。如有异常，请前往正规医疗机构儿科内分泌科就诊。

## 许可证

MIT License
