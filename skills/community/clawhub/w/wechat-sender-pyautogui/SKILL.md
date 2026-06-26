# wechat-sender 技能

快捷键版微信发送工具，使用 PyAutoGUI 模拟键盘操作。

## 触发条件

- 用户说"发微信"、"微信发送"、"发消息给 XXX"
- 用户要求发送微信消息或文件

## 使用方法

```bash
# 发送消息
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py --contact "联系人" --message "消息内容"

# 发送文件
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py --contact "联系人" --file "文件路径"

# 仅输入不发送（让用户自己确认）
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py --contact "联系人" --message "消息" --no-send

# 选择第 N 个同名联系人
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py --contact "联系人" --message "消息" --index 2

# 临时指定快捷键（本次有效）
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py -c "张三" -m "你好" --hotkey "Ctrl+Shift+W"

# 保存快捷键配置（永久有效）
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py --config-hotkey "Ctrl+Alt+W"

# 查看当前快捷键配置
python D:\clawSpaces\skills\wechat-sender\wechat_sender.py --show-config
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--contact`, `-c` | 联系人名称（必填） |
| `--message`, `-m` | 消息内容 |
| `--file`, `-f` | 文件路径 |
| `--no-send` | 仅输入不发送，让用户自己确认 |
| `--index`, `-i` | 选择第 N 个联系人（默认 1） |
| `--hotkey`, `-k` | 临时指定微信打开快捷键（格式：Ctrl+Alt+W） |
| `--config-hotkey` | 保存微信快捷键到配置文件 |
| `--show-config` | 显示当前快捷键配置 |

## 快捷键配置

### 默认快捷键
- **`Ctrl+Alt+W`** - 打开微信（默认）

### 如果用户的微信快捷键不同

**方法 1：临时指定（本次有效）**
```bash
python wechat_sender.py -c "张三" -m "你好" --hotkey "Ctrl+Shift+W"
```

**方法 2：保存到配置文件（永久有效）**
```bash
# 保存快捷键
python wechat_sender.py --config-hotkey "Ctrl+Shift+W"

# 查看配置
python wechat_sender.py --show-config
```

配置文件位置：`wechat-sender/wechat_config.json`

### 支持的快捷键格式
- `Ctrl+Alt+W`
- `Ctrl+Shift+W`
- `Alt+F4`
- `Ctrl+W`
- 等等（支持 Ctrl/Alt/Shift/Win + 字母）

## 其他快捷键

- `Ctrl+F` - 搜索联系人（固定）
- `Enter` - 确认选择/发送消息（固定）

## 依赖

```bash
pip install pyautogui
```

## 安全设置

- `pyautogui.FAILSAFE = True` - 鼠标移到屏幕角落可中止操作
- `pyautogui.PAUSE = 0.3` - 每次操作间隔 0.3 秒

## 注意事项

1. 确保微信已安装
2. 如果微信快捷键不是默认的 Ctrl+Alt+W，请使用 `--config-hotkey` 配置
3. 操作过程中不要移动鼠标或键盘输入
4. 发送敏感消息前建议使用 `--no-send` 预览
5. 配置文件会自动创建在技能目录中

## 示例场景

### 场景 1：首次使用，快捷键是默认的
```bash
python wechat_sender.py -c "张三" -m "早上好！"
```

### 场景 2：微信快捷键是 Ctrl+Shift+W
```bash
# 第一次：配置快捷键
python wechat_sender.py --config-hotkey "Ctrl+Shift+W"

# 以后：直接使用
python wechat_sender.py -c "李四" -m "下午好！"
```

### 场景 3：临时使用不同的快捷键
```bash
# 某次临时使用不同的快捷键
python wechat_sender.py -c "王五" -m "你好" --hotkey "Alt+Shift+W"
```
