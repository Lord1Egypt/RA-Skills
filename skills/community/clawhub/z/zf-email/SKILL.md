name: 邮件生成助手
description: 根据用户提供的要点，自动生成正式或友好的英文/中文邮件。
trigger: 用户说“写封邮件”、“生成邮件”或“帮我起草邮件”。
input:
  - 收件人 (string, required)
  - 主题 (string, optional)
  - 要点列表 (array, required)
  - 语气 (enum: 正式/友好, default: 正式)
steps:
  1. 解析用户给出的邮件要点。
  2. 根据语气选择模板（正式：Dear X, ...；友好：Hi X, ...）。
  3. 将要点组织成连贯段落，添加适当的开场和结尾。
  4. 输出完整邮件正文，并提示用户可修改。
  output: 纯文本格式的邮件内容，带标题和落款。
  example:
    user: 帮我写封正式邮件给 john@example.com，主题是项目进度汇报。要点：1. 已完成前端开发；2. 后端预计周五完成；3. 需要下周安排测试。
    assistant: 邮件正文...
