# Scrcpy Control Commands Reference

This document provides a comprehensive reference for scrcpy control commands.

## Control Message Types

| Type | Code | Description |
|------|------|-------------|
| INJECT_KEYCODE | 0 | Inject a key event |
| INJECT_TEXT | 1 | Inject text input |
| INJECT_TOUCH_EVENT | 2 | Inject touch event |
| INJECT_SCROLL_EVENT | 3 | Inject scroll event |
| BACK_OR_SCREEN_ON | 4 | Back key or power on |
| EXPAND_NOTIFICATION_PANEL | 5 | Expand notifications |
| EXPAND_SETTINGS_PANEL | 6 | Expand quick settings |
| COLLAPSE_PANELS | 7 | Collapse all panels |
| GET_CLIPBOARD | 8 | Get clipboard content |
| SET_CLIPBOARD | 9 | Set clipboard content |
| SET_DISPLAY_POWER | 10 | Control display power |
| ROTATE_DEVICE | 11 | Rotate device screen |
| UHID_CREATE | 12 | Create UHID device |
| UHID_INPUT | 13 | Send UHID input |
| UHID_DESTROY | 14 | Destroy UHID device |
| OPEN_HARD_KEYBOARD_SETTINGS | 15 | Open keyboard settings |
| START_APP | 16 | Start application |
| RESET_VIDEO | 17 | Reset video capture |

## Key Codes Reference

Common Android KeyEvent codes:

| Key | Code |
|-----|------|
| HOME | 3 |
| BACK | 4 |
| CALL | 5 |
| END_CALL | 6 |
| VOLUME_UP | 24 |
| VOLUME_DOWN | 25 |
| POWER | 26 |
| CAMERA | 27 |
| MENU | 82 |
| ENTER | 66 |
| TAB | 61 |
| DEL (Backspace) | 67 |
| FORWARD_DEL | 112 |
| ESCAPE | 111 |
| SPACE | 62 |
| DPAD_UP | 19 |
| DPAD_DOWN | 20 |
| DPAD_LEFT | 21 |
| DPAD_RIGHT | 22 |
| DPAD_CENTER | 23 |
| APP_SWITCH | 187 |
| NOTIFICATION | 83 |

## Touch Event Actions

| Action | Code |
|--------|------|
| ACTION_DOWN | 0 |
| ACTION_UP | 1 |
| ACTION_MOVE | 2 |
| ACTION_CANCEL | 3 |
| ACTION_POINTER_DOWN | 5 |
| ACTION_POINTER_UP | 6 |
| ACTION_HOVER_MOVE | 7 |

## Meta Key States

| Meta | Code |
|------|------|
| META_NONE | 0 |
| META_ALT_ON | 2 |
| META_ALT_LEFT_ON | 16 |
| META_ALT_RIGHT_ON | 32 |
| META_SHIFT_ON | 1 |
| META_SHIFT_LEFT_ON | 64 |
| META_SHIFT_RIGHT_ON | 128 |
| META_CTRL_ON | 4096 |
| META_CTRL_LEFT_ON | 8192 |
| META_CTRL_RIGHT_ON | 16384 |
| META_META_ON | 65536 |

## Message Formats

### INJECT_KEYCODE
```
[1 byte: type][1 byte: action][4 bytes: keycode][4 bytes: repeat][4 bytes: metastate]
```

### INJECT_TEXT
```
[1 byte: type][4 bytes: length][N bytes: text]
```

### INJECT_TOUCH_EVENT
```
[1 byte: type][1 byte: action][8 bytes: pointer_id][4 bytes: x][4 bytes: y]
[4 bytes: screen_width][4 bytes: screen_height][4 bytes: pressure]
[4 bytes: action_button][4 bytes: buttons]
```

### INJECT_SCROLL_EVENT
```
[1 byte: type][4 bytes: x][4 bytes: y][4 bytes: screen_width][4 bytes: screen_height]
[4 bytes: hscroll][4 bytes: vscroll][4 bytes: buttons]
```

### SET_CLIPBOARD
```
[1 byte: type][8 bytes: sequence][1 byte: paste][4 bytes: length][N bytes: text]
```

### START_APP
```
[1 byte: type][4 bytes: length][N bytes: name]
```
