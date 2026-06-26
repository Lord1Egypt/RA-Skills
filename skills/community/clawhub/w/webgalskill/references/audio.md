# 音频

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 播放BGM | `bgm:文件名.mp3;` | 播放背景音乐 |
| BGM淡入 | `bgm:文件名.mp3 -enter=毫秒;` | 淡入播放 |
| 停止BGM | `bgm:none -enter=毫秒;` | BGM淡出 |
| 语音 | `对话 -V文件名.ogg;` | 播放语音 |
| 效果音 | `playEffect:文件名.mp3;` | 播放效果音 |
| 效果音循环 | `playEffect:文件名.mp3 -id=xxx;` | 循环播放效果音 |
| 停止循环效果音 | `playEffect:none -id=xxx;` | 停止循环 |
| 解锁BGM | `unlockBgm:文件名.mp3 -name=名称;` | 解锁BGM鉴赏 |

## 资源文件位置

- BGM：`bgm/` 文件夹
- 语音/效果音：`vocal/` 文件夹

## 背景音乐（BGM）

```ws
bgm:夏影.mp3;
```

| 参数 | 必填 | 说明 |
| :--- | :--- | :--- |
| `-volume` | 否 | 音量 0-100，默认 100 |
| `-enter` | 否 | 淡入时间（毫秒），默认 0 |

**示例：**

```ws
bgm:夏影.mp3 -volume=30;    // 30%音量播放
bgm:夏影.mp3 -enter=3000;   // 3秒淡入播放
```

**淡出停止：**

```ws
bgm:none -enter=3000; // 3秒淡出后停止
```

## 语音

在对话后添加 `-V文件名` 参数：

```ws
比企谷八幡:刚到而已 -V3.ogg;
```

连续对话时语音语法相同：

```ws
雪之下雪乃:你到得真早 -V1.ogg;
对不起，等很久了吗？ -V2.ogg;
```

可附加 `-volume` 调整音量：

```ws
比企谷八幡:刚到而已 -V3.ogg -volume=30;
```

## 效果音

```ws
playEffect:xxx.mp3;
playEffect:xxx.mp3 -volume=30; // 30%音量播放
```

### 效果音循环

使用 `-id` 启用循环，通过 `none` 停止：

```ws
playEffect:xxx.mp3 -id=loopSound;    // 开始循环
playEffect:none -id=loopSound;       // 停止循环
```

## 解锁BGM鉴赏

```ws
unlockBgm:s_Title.mp3 -name=Smiling-Swinging!!!;
```

| 参数 | 必填 | 说明 |
| :--- | :--- | :--- |
| `-name` | 是 | BGM鉴赏中显示的名称 |
