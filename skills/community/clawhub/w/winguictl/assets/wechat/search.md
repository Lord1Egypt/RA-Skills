# 搜索操作

微信顶部搜索框可用于搜索联系人、群聊、聊天记录、收藏内容等。

---

## 搜索框特征

| 属性 | 值 |
|------|-----|
| control_type | Edit |
| class | mmui::XValidatorTextEdit" |

---

## 基本使用流程

### 步骤1：确保微信主界面在前台

详见 [窗口定位与微信主界面操作](./window.md)

### 步骤2：定位并激活搜索框

#### 定位搜索框

##### 方式A：通过 class 查找（推荐）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --class XValidatorTextEdit
```

##### 方式B：通过 snapshot 查找

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
```

找到 `control_type="Edit"` 的搜索输入框，记录其 `relative_rect` 和 `runtime_id`。

#### 激活搜索框

使用 `--element-id` 点击搜索框中心，无需手动计算坐标。

##### 通过 runtime_id 点击

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <search_edit_runtime_id>
```

### 步骤3：输入搜索关键词

`uia-control set-text` 可以直接设置文本，无需提前清空。设置文本后要点击搜索框以激活搜索结果列表。

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <search_edit_runtime_id> set-text "联系人备注名"
```

### 步骤4：等待搜索结果

#### 等待一段时间

```powershell
python scripts\winguictl.py wait sleep 1000
```

#### 或等待搜索结果出现

```powershell
python scripts\winguictl.py wait uia --window-id <wx_window_id> --text "好友备注名" --control-type ListItem --timeout 3
```

### 步骤5：点击搜索结果

一定要用`action click`点击，`uia-control invoke` 对微信控件无效。

#### 方式A：通过 element-id 点击（推荐）

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "好友备注名" --control-type ListItem
```

使用返回的 `element_id` 点击。

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <result_element_id>
```

#### 方式B：通过坐标点击

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --relative-x <result_x> --relative-y <result_y>
```

---

## 搜索结果类型

搜索结果可能包含以下类型：

| 类型 | 说明 |
|------|------|
| 联系人 | 单个好友 |
| 群聊 | 群组 |
| 聊天记录 | 历史消息 |
| 收藏 | 收藏的内容 |
| 公众号 | 关注的公众号 |

---

## 清空搜索框

### 方式A：使用 set-text 设置空字符串

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <search_edit_runtime_id> set-text ""
```

### 方式B：点击搜索框后使用快捷键清空

```powershell
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <search_element_id>
python scripts\winguictl.py action --window-id <wx_window_id> hotkey --keys "{CTRL}" "{A}"
python scripts\winguictl.py action --window-id <wx_window_id> press-key --key "{DELETE}"
```

---

## 常见用例

### 搜索并打开好友聊天窗口

#### 步骤1：聚焦微信窗口

```powershell
python scripts\winguictl.py window --window-id <wx_window_id> focus
```

#### 步骤2：定位搜索框

```powershell
python scripts\winguictl.py find --window-id <wx_window_id> uia --class XValidatorTextEdit
```

假设 `runtime_id` 为 `42-4399352-4--123456`。

#### 步骤3：输入好友名称

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id "42-4399352-4--123456" set-text "好友备注名"
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <search_element_id>
```

#### 步骤4：等待并点击搜索结果

```powershell
python scripts\winguictl.py wait uia --window-id <wx_window_id> --text "好友备注名" --control-type ListItem --timeout 3
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "好友备注名" --control-type ListItem
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <result_element_id>
```

### 搜索聊天记录

#### 步骤1：输入搜索关键词

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <search_edit_runtime_id> set-text "关键词"
```

#### 步骤2：等待搜索结果

```powershell
python scripts\winguictl.py wait sleep 1000
```

#### 步骤3：查找聊天记录类型的结果

```powershell
python scripts\winguictl.py snapshot --window-id <wx_window_id> uia
```

在结果中查找包含 "聊天记录" 标签的 `ListItem`。

### 搜索群聊

#### 步骤1：输入群名称

```powershell
python scripts\winguictl.py uia-control --window-id <wx_window_id> --element-id <search_edit_runtime_id> set-text "群名称"
```

#### 步骤2：等待并点击群聊结果

```powershell
python scripts\winguictl.py wait uia --window-id <wx_window_id> --text "群名称" --control-type ListItem --timeout 3
python scripts\winguictl.py find --window-id <wx_window_id> uia --text "群名称" --control-type ListItem
python scripts\winguictl.py action --window-id <wx_window_id> click --element-id <result_element_id>
```

---

## 多语言支持

搜索框的 automation_id 在不同语言版本中保持一致，但搜索结果中的标签文字会因语言不同而变化：

| 中文 | English | 繁體中文 |
|------|---------|----------|
| 联系人 | Contacts | 聯絡人 |
| 群聊 | Group Chats | 群聊 |
| 聊天记录 | Chat History | 聊天記錄 |
| 收藏 | Favorites | 收藏 |
| 公众号 | Official Accounts | 公眾號 |
