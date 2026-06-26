---
name: 福利吧
description: 获取福利吧 (https://www.wnflb2023.com/) 指定板块的帖子列表（标题、内容、链接），进入帖子提取正文内容，最后由 AI 归纳总结。
read_when: 用户询问福利吧的帖子信息、内容总结时
metadata: clawdbot emoji discuz forum scraper
allowed-tools: Bash,node
---

# 安装说明
- 操作系统不限
- 系统需要有node环境，版本需要22及以上. 可以在环境变量中检测是否已经安装了node
- 需要执行npm install来安装依赖的包

# 使用手册

## 何时使用本 Skill
- 用户说：“帮我看一下发现之门/综合讨论/购物网赚的最新帖子”
- 用户说："福利吧最新帖"
- 用户说："福利吧签到"

## 核心工作流（4步循环 + AI 总结）
  
  1: 检查cookie.txt文件
     **重要**：以下操作都在本Skill目录 `./` 下进行（即包含此SKILL.md文件的目录）。
     - 使用 `read_file` 工具读取 `./cookie.txt` 文件
 - 检查文件是否存在且内容非空
 - 必须确保`cookie.txt`文件仅对本skill可读。 
  
2. **确定论坛板块和抓取数量**

   - 板块fid列表:
     - 发现之门:fid=2
     - 综合讨论:fid=40
     - 购物网赚:fid=37
     - 网游分享区:fid=67
     - 交易平台:fid=44
     - 福禄娃之家:fid=39
   - **如果用户说“看下福利吧最新帖子”，默认使用发现之门的fid**
   - 如果用户说“看下福利吧综合讨论的帖子”则fid为40
   - 抓取数量(count)默认为10条，如果用户有指定则使用用户指定的数量


3. **获取帖子及内容**
   - 执行以下代码获取输出JSON
   ## ⚠️ 执行注意事项
    脚本调用时**禁止使用链式运算符**（`&&`、`;`、`||` 等）
    错误的例子：
     `cd ~/.openclaw/workspace/skills/wnflb && node main.js`
     正确的列子：
    `node ~/.openclaw/workspace/skills/wnflb/main.js`
     即：始终使用**绝对路径**调用 node + 脚本，不需要 `cd &&` 前缀。
```bash
     node ~/.openclaw/workspace/skills/wnflb/main.js scrape --fid fid --count count
```
     - fid为对应板块
     - count为抓取的帖子数量
   - 程序会返回json的格式内容
```json
{
  "forumTitle": "发现之门 -",
  "forumUrl": "https://www.wnflb2023.com/forum.php?mod=forumdisplay&fid=2&mobile=2",
  "fid": 2,
  "count": 1,
  "items": [
    {
      "title": "有多少人还没有副业？",
      "url": "https://www.wnflb2023.com/forum.php?mod=viewthread&tid=274938&extra=page%3D1&mobile=2&_dsign=7950febd",
      "content": "副业已经伴随我快10年了，中途也换过无数个副业了，总感觉没有副业心理不踏实\n\n不做副业的是不是主业收入相当可观了"
    }]
}
```

4.  AI内容摘要并输出
   - 将content内容传入LLM（你就是 AI）
   - |内容摘要|：200字内,去掉html的换行等标签，总结要突出核心福利和有效信息,**有网盘的链接地址和密码需要提取出来并显示,如果有百家姓等内容也需要把内容显示出来,如果有多个网盘链接，列出每个链接及对应密码。**
   - **严格按照以下结构输出Markdown的表格格式**
```text
### <板块名称>最新内容
| 序号 | 标题 | 内容摘要 |
|------|------|----------|
| [1](<url>) | xxxxxxx| xxxxxx| 
```

## 论坛签到
  - 论坛签到是独立的一个功能,同样的需要先满足准备Cookie的工作（参见上面的流程1）
  - 执行脚本获取结果即可
```bash
node ~/.openclaw/workspace/skills/wnflb/main.js checkin
```

返回json。例如
```json
{
  "ok": true,
  "entryUrl": "https://www.wnflb2023.com/misc.php?mod=mobile",
  "checkinUrl": "https://www.wnflb2023.com/plugin.php?id=fx_checkin:checkin&formhash=1cbf33ef&inajax=1",
  "message": "已签到"
}
```
