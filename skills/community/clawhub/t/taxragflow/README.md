# TAX Knowledge Skill

税务知识智能问答技能。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制配置模板：

```bash
cp .env.example .env
```

### 3. 测试运行

```bash
python query_tax.py "增值税税率是多少？"
```

## 使用方法

在 OpenClaw 中安装此 skill 后，当用户提出税务相关问题时会自动调用知识库查询。

**示例问题：**
- "最新的增值税优惠政策是什么？"
- "企业所得税的扣除标准有哪些？"
- "个人所得税专项附加扣除包括哪些？"

## 常见问题

**Q: 提示认证失败？**  
A: 检查 `.env` 文件中的 API Key 是否正确，确保没有多余空格。

**Q: 连接超时？**  
A: 确认 API URL 地址正确，且网络可以访问该地址。

## 联系方式

如有问题，请联系：zhao xin
