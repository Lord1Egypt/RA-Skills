# 小红书自动互动技能

## 描述
小红书自动互动技能，提供智能搜索、浏览、点赞、收藏功能。这是一个改进版，包含历史记录避免重复操作、扩展搜索关键词、智能错误处理等功能。

## 功能
1. **智能搜索**：从15个新加坡私立大学相关关键词中随机选择进行搜索
2. **浏览推荐**：浏览小红书推荐内容
3. **智能点赞**：避免重复点赞已互动过的笔记
4. **智能收藏**：避免重复收藏已互动过的笔记
5. **历史记录**：记录所有操作，避免重复执行
6. **错误处理**：智能识别已点赞/已收藏状态，避免重复尝试

## 前提条件
1. 小红书MCP服务已启动并运行在 `localhost:18060`
2. 小红书账号已登录
3. 已安装必要的工具：`curl`, `jq`

## 安装与配置

### 1. 复制脚本到工作空间（推荐使用改进版）
```bash
# 复制改进版脚本
cp scripts/xhs_interaction_improved.sh ~/.openclaw/workspace/
chmod +x ~/.openclaw/workspace/xhs_interaction_improved.sh

# 或者复制简化版（基础功能）
cp scripts/xhs_interaction_simple_fixed.sh ~/.openclaw/workspace/
chmod +x ~/.openclaw/workspace/xhs_interaction_simple_fixed.sh
```

### 2. 配置cron任务
```bash
# 编辑crontab
crontab -e

# 添加以下行（示例：每天12:31、14:31、16:31、18:31、20:31执行）
31 12,14,16,18,20 * * * /home/chan/.openclaw/workspace/xhs_interaction_improved.sh
```

### 3. 手动测试
```bash
cd ~/.openclaw/workspace
./xhs_interaction_improved.sh
```

## 脚本说明

### 改进版脚本特点
- **避免重复操作**：使用历史记录文件跟踪已互动笔记
- **扩展关键词**：15个新加坡私立大学相关关键词，每次随机选择
- **智能状态判断**：识别"已点赞"、"已收藏"等状态
- **详细统计**：提供完整的执行统计和日志
- **笔记链接**：输出点赞的笔记链接，方便查看

### 主要参数
- `MCP_URL`: MCP服务地址（默认：`http://localhost:18060/mcp`）
- `LOG_FILE`: 日志文件路径
- `HISTORY_FILE`: 历史记录文件路径
- `KEYWORDS`: 搜索关键词数组（15个新加坡留学相关关键词）
- `MAX_ATTEMPTS`: 最大尝试处理数（默认：10）

### 执行流程
1. 初始化MCP会话
2. 检查登录状态
3. 从关键词数组中随机选择一个关键词
4. 搜索相关内容
5. 浏览推荐内容
6. 加载历史记录
7. 智能互动处理（避免重复操作）
8. 输出详细执行统计和笔记链接

## 故障排除

### 常见问题
1. **MCP服务未启动**
   ```bash
   # 检查MCP服务状态
   curl http://localhost:18060/mcp
   ```

2. **登录状态异常**
   - 检查小红书APP是否已登录
   - 重启MCP服务

3. **点赞/收藏失败**
   - 可能是平台限制或网络超时
   - 脚本会自动记录失败状态，避免重复尝试
   - 可调整`MAX_ATTEMPTS`减少处理数量

4. **历史记录问题**
   - 历史记录文件：`~/.openclaw/workspace/xhs_interaction_history.txt`
   - 格式：`LIKE:feed_id:timestamp` 或 `FAVORITE:feed_id:timestamp`
   - 如需重置，可删除该文件

### 日志查看
```bash
# 查看实时日志
tail -f ~/.openclaw/workspace/xhs_interaction_improved.log

# 查看执行统计
grep -E "📊|执行统计|成功点赞数|成功收藏数" ~/.openclaw/workspace/xhs_interaction_improved.log

# 查看历史记录
cat ~/.openclaw/workspace/xhs_interaction_history.txt | head -20
```

## 更新记录
- **2026-04-04**: 创建改进版，添加历史记录、扩展关键词、智能错误处理
- **2026-04-04**: 创建简化修复版，移除评论功能，专注点赞和收藏

## 注意事项
1. 避免过于频繁执行，以免触发平台限制
2. 定期检查日志和历史记录，确保功能正常
3. 如遇平台限制，可调整执行频率或减少处理数量
4. 历史记录文件会持续增长，可定期清理旧记录

## 搜索关键词列表
脚本包含以下15个新加坡私立大学相关关键词：
1. 新加坡留学
2. 新加坡私立大学
3. 新加坡管理学院
4. 新加坡楷博高等教育学院
5. 新加坡PSB学院
6. 新加坡东亚管理学院
7. 新加坡留学咨询
8. 新加坡本科留学
9. 新加坡硕士留学
10. 新加坡留学费用
11. 新加坡留学申请
12. 新加坡留学条件
13. 新加坡留学签证
14. 新加坡留学优势
15. 新加坡留学就业