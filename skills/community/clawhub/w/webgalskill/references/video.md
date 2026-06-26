# 视频

## 命令速查

| 命令 | 语法 | 说明 |
| :--- | :--- | :--- |
| 播放视频 | `playVideo:文件名.mp4;` | 播放视频 |
| 禁止跳过 | `playVideo:文件名.mp4 -skipOff;` | 禁止用户跳过 |

## 播放视频

将视频放入 `video/` 文件夹，使用 `playVideo` 播放：

```ws
playVideo:OP.mp4;
```

## 禁止跳过

使用 `-skipOff` 参数可阻止用户跳过视频：

```ws
playVideo:OP.mp4 -skipOff;
```
