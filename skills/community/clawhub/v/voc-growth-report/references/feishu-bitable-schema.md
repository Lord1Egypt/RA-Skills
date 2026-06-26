# Feishu Bitable Comment Library Schema

Use this schema when the user wants to store social comments in Feishu for manual review or later analysis.

## 12-field minimal production schema

1. 平台  
   Type: single select or text
2. 帖子标题  
   Type: text
3. 帖子链接  
   Type: url
4. 评论内容  
   Type: long text
5. 评论用户  
   Type: text
6. 评论时间  
   Type: datetime
7. 情绪倾向  
   Type: single select  
   Options: 正向 / 中性 / 负向
8. 意图类型  
   Type: single select  
   Options: 咨询价格 / 咨询功能 / 咨询购买 / 使用反馈 / 吐槽抱怨 / 夸赞认可 / 对比竞品 / 无效灌水 / 其他
9. 商机等级  
   Type: single select  
   Options: 高 / 中 / 低 / 无
10. 是否需要回复  
   Type: single select  
   Options: 是 / 否
11. 跟进状态  
   Type: single select  
   Options: 待处理 / 已回复 / 已私信 / 已忽略 / 已归档
12. 备注  
   Type: long text

## Recommended views
- 全部评论
- 高商机评论
- 待回复评论
- 负面评论

## Simple operational rules
- 商机等级=高: clear buying/cooperation/contact intent
- 是否需要回复=是: explicit question, buying intent, negative complaint, or competitor mention
- 跟进状态 defaults to 待处理 for anything worth review
