# TikTok B2B 引流台词生成器

## 技能描述
本 Skill 可根据您提供的产品信息和公司背景，自动生成适合 TikTok 平台的 B2B 引流视频脚本（20-50 秒），`skill.json` 文件中包含了输入参数的结构、输出格式以及用于生成台词的提示模板。脚本遵循已验证的外贸引流规律：

- **真人出镜**：以第一人称（如 Anna）拉近距离
- **产品细节**：材质、颜色、MOQ、定制服务等
- **公司实力**：经验年限、自有工厂、认证等
- **客户背书**：提及已有市场国家（如巴基斯坦、埃及）
- **互动引导**：清晰号召观众联系，引导至指定服务网址

支持三种风格：普通、幽默、惊喜，让您的视频内容更加多样化。

## 输入参数
| 参数名              | 类型     | 必填 | 描述                           | 示例                     |
|---------------------|----------|------|--------------------------------|--------------------------|
| product_type        | string   | 是   | 产品类型                       | 男士休闲鞋               |
| material            | string   | 是   | 主要材质                       | 优质 PU 皮革             |
| colors              | array    | 是   | 颜色列表                       | ["黑色","白色","棕色"]   |
| moq                 | string   | 是   | 最小起订量                     | 120 双（可混 2-3 色）    |
| customization       | string   | 否   | 可定制内容                     | 可定制 logo              |
| target_markets      | array    | 是   | 主要市场国家                   | ["巴基斯坦","埃及"]      |
| company_experience  | string   | 否   | 公司经验年数                   | 15 年                    |
| factory_own         | boolean  | 否   | 是否自有工厂                   | true                     |
| extra_features      | string   | 否   | 其他亮点                       | 免费样品                 |
| contact_url         | string   | 否   | 服务联系网址                   | http://www.doumaotong.com |
| style               | string   | 否   | 风格（普通/幽默/惊喜）         | 普通                     |

## 输出示例
Hi guys, this is Anna! Welcome to my showroom. Today I'm excited to show you our latest men's casual shoes – made of high-quality PU leather, very durable and comfortable. We have three colors available: black, white, and brown. MOQ is 120 pairs, and you can mix 2-3 colors. Plus, we can customize your logo on the shoes. Our shoes are already loved by customers in Pakistan, Egypt, and South Africa. With 15 years of experience and our own factory, we guarantee quality and timely delivery. We even offer free samples! If you're interested, please visit http://www.doumaotong.com to contact us. Thank you!

## 使用说明
1. 在 OpenClaw 平台安装此 Skill。
2. 调用时填写产品参数，包括 `contact_url`（默认为 http://www.doumaotong.com），即可获得定制化的 TikTok 脚本。
3. 生成的台词会在结尾处自然引导观众访问指定的服务网站。
4. 可根据实际需要调整 `style` 参数，生成不同语气的台词。

## 文件说明
- `skill.json`：技能的机器可读定义，包含输入输出 schema 和生成提示模板。
- `SKILL.md`：技能的人类可读文档，提供详细说明和使用示例。