---
name: wechat-sender
version: 1.0.0
description: 微信消息自动发送。使用 peekaboo 工具操作窗口，结合 Agent-Eye 获取实时屏幕截图进行视觉理解。触发条件：用户提到"发微信"、"给xxx发消息"、"微信自动发送"等。
---

# WeChat Sender

## 准备工作

### 1. 依赖项目

**Agent-Eye** - 屏幕捕获服务
- 仓库：https://github.com/noir-hedgehog/Agent-eye
- 功能：实时屏幕截图、100px 网格叠加、鼠标坐标显示
- 启动方式：
  ```bash
  # 服务端
  eye-server --port 8080 --region 0,0,1200,900
  
  # Python Agent（需要配置 image key）
  cd crates/eye
  python -c "
  from agent import Agent
  agent = Agent(server_url='http://localhost:8080', interval=1.5, grid_size=100, show_mouse=True, region='0,0,1200,900')
  agent.run()
  "
  ```

### 2. 启动检查清单

- [ ] 确认微信已登录且保持后台运行
- [ ] 启动 Agent-Eye 服务端：`eye-server --port 8080`
- [ ] 启动 Python Agent（无需额外配置）
- [ ] 验证截图功能：`curl http://localhost:8080/snapshot.png -o test.png`
- [ ] 验证图像理解：使用 OpenClaw 内置的 image tool 分析截图

### 3. 图像理解说明

图像理解功能由 OpenClaw 内置的 `image` 工具提供，无需额外配置 Agent-Eye。Agent-Eye 负责捕获屏幕截图，`image` 工具负责理解图像内容。

微信消息自动发送技能。可以灵活组合以下能力，但执行前需要先思考流程（checklist）。

## 原子能力

| 能力 | 命令 | 说明 |
|------|------|------|
| 聚焦窗口 | `peekaboo window focus --app "微信"` | 聚焦微信窗口（某些app有防录屏限制，需要先聚焦） |
| 调整窗口 | `peekaboo window set-bounds --app "微信" --x 0 --y 0 --width 1200 --height 900` | 调整窗口位置和大小，避免防录屏限制 |
| 截图 | The-Eye: `curl http://localhost:8080/snapshot.png` 或 `/usr/sbin/screencapture -R0,0,1200,900` | 建议用 The-Eye 获取实时截图 |
| 图像理解 | `image` tool | 分析截图内容，查找联系人位置 |
| 切换联系人 | `peekaboo hotkey --keys "shift,down" --app "微信"` | 模拟 shift+↓ 切换选中联系人 |
| 粘贴文字 | `peekaboo paste --text "{message}" --app "微信"` | 复制文字到剪贴板并粘贴 |
| 发送消息 | `peekaboo hotkey --keys "cmd,return" --app "微信"` | 模拟 cmd+return 发送消息 |
| **搜索联系人** | `peekaboo hotkey --keys "cmd,f" --app "微信"` | **推荐！** 激活搜索框，比滑动列表快 |

## 视觉上下文说明

**使用 The-Eye 截图时：**
- 100px 网格：帮助定位界面元素的精确坐标。每个格子是 100x100 像素
- 鼠标准星坐标 (x, y)：当前鼠标位置，十字准星+坐标标签
- 截图分辨率：默认捕获整个屏幕，可在 The-Eye 启动时用 `--region` 参数指定区域

**图像理解时的参考信息：**
- 网格坐标可以帮助定位按钮、联系人等元素的具体位置
- 鼠标坐标指示当前关注的区域
- 微信界面特征：左侧联系人列表、右侧聊天窗口、底部输入框

## 微信 UI 探索发现

### 左侧边栏图标（从到到下）
1. 个人头像
2. 聊天（消息）- 绿色选中
3. 通讯录 - 小人头图标
4. 收藏 - 立方体图标
5. 朋友圈 - 圆环快门图标
6. 视频号 - 漏斗图标
7. 搜一搜/看一看 - 地球仪图标
8. 小程序 - 层级点图标
9. 手机连接 - 手机图标
10. 更多（设置）- 三横线图标

### 推荐联系人查找方式
**方式1：搜索（推荐）**
1. `peekaboo hotkey --keys "cmd,f" --app "微信"` 激活搜索框
2. `peekaboo paste --text "联系人名字" --app "微信"` 输入搜索词
3. 点击搜索结果进入聊天

**方式2：滑动列表**
- 使用 `shift+up/down` 切换联系人
- 适合联系人顺序已知的情况

## 执行流程（Checklist 思考模式）

**在执行每个操作前，先思考：**
1. 当前状态是什么？
2. 下一步需要做什么？
3. 需要什么工具/能力？
4. 可能的风险是什么？

### 推荐流程

```
1. [ ] 聚焦微信窗口 + 调整大小
     → peekaboo window focus --app "微信"
     → peekaboo window set-bounds --app "微信" --x 0 --y 0 --width 1200 --height 900

2. [ ] 选择找联系人方式
     → 搜索（推荐）：Cmd+F → 输入名字 → 点击结果
     → 滑动列表：shift+up/down

3. [ ] 获取截图（优先用 The-Eye）
     → curl http://localhost:8080/snapshot.png -o /tmp/wechat.png
     
4. [ ] 分析截图（视觉理解）
     → 使用 image tool，询问：
       - 当前选中的联系人是谁？
       - 目标联系人在列表第几个？
       - 界面是否有异常？

5. [ ] 发送消息
     → peekaboo paste --text "消息内容" --app "微信"
     → peekaboo hotkey --keys "cmd,return" --app "微信"

6. [ ] 确认发送成功
     → 截图 + image tool 确认消息气泡出现
```

## 灵活运用原则

- **搜索是最高效的**：用 Cmd+F 搜索，比滑动列表快很多
- **不必完全按顺序**：如果已经知道联系人名字，直接搜索
- **选择合适的截图方式**：
  - The-Eye 实时流：适合需要鼠标坐标的场景
  - 直接截图：适合只需要静态界面的场景
- **遇到问题灵活处理**：
  - 如果搜索没结果，尝试滑动列表
  - 如果切换失败，可以重新截图确认状态
  - 如果发送失败，尝试重新聚焦窗口

## 示例

发送"最近怎么样"给"宝宝星"：

**方式1：搜索（推荐）**
1. 聚焦 + 调整窗口
2. Cmd+F 激活搜索
3. paste "宝宝星"
4. 点击搜索结果
5. paste 消息 + Cmd+Return
6. 确认

**方式2：滑动列表**
1. 聚焦 + 调整窗口
2. 截图确认位置
3. shift+down × 7
4. paste 消息 + Cmd+Return
5. 确认

## 注意事项

- 某些 app（微信、企业微信等）有防录屏限制，聚焦窗口+调整大小可以绕过
- 窗口调整到 1200x900 后，截图只需截取该区域
- The-Eye 服务需要先启动：`eye-server --port 8080` + `eye agent start`
- 每次按键操作间隔 0.3 秒更稳定
- 遇到错误可以尝试重新聚焦窗口，不要盲目重试
