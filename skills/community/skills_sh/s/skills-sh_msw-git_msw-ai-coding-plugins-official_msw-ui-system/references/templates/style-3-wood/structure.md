# Style 3 (Wood) — UI Structure

Format: `Name | Alignment | (x, y) | WxH | [Components] | (state)`

```
============================================================
  ButtonGroup.ui  (24 entities)
============================================================
ButtonGroup | GroupOrder=3 | StretchAll | 1920x1080 | [UIGroupComponent]
  Menu_Panel | TopLeft | (0, -540) | 363x850
    ScrollList | StretchAll | 315x805 | [ScrollLayout]

============================================================
  DefaultGroup.ui  (3 entities)
============================================================
DefaultGroup | GroupOrder=1 | hidden | StretchAll | 1920x1080 | [UIGroupComponent]
  UIChat | TopLeft | (369, -252) | 698x439 | [ChatComponent]
  UIJoystick | BottomLeft | (310, 230) | 200x200 | [JoystickComponent]

============================================================
  HUDGroup.ui  (45 entities)
============================================================
HUDGroup | GroupOrder=0 | StretchAll | 1920x1080 | [UIGroupComponent]
  Button_Attack | BottomRight | (-175, 332) | 204x204 | [Button]
    UISprite | Center | (0, 1) | 104x105
  Button_Jump | BottomRight | (-392, 194) | 204x204 | [Button]
    UISprite | Center | (0, 5) | 143x125
  Button_Menu | TopLeft | (10, -20) | 112x104 | [Button]
  HP | BottomCenter | (-205, 10) | 410x49 | [Button]
    Fill | Center | (-100, 0) | 304x51
    Num | Center | (48, 0) | 297x28 | [TextComponent] | "100/100"
    Outline | Center | 404x45
    Tiltle | Left | (0, -3) | 113x51 | [TextComponent] | "HP"
  InfiniteQuest | Right | (-30, 340) | 100x100
    Paper | Right | (-47, -1) | 410x124
    QuestGauge | Center | 100x100 | [Button]
  InfiniteQuest_Clear | Right | (-30, 215) | 100x100
    Paper | Right | (-47, -1) | 410x124
    QuestGauge | Center | 100x100 | [Button]
  MP | BottomCenter | (205, 10) | 410x49 | [Button]
    Fill | Center | (-100, 0) | 304x51
    Num | Center | (48, 0) | 297x28 | [TextComponent] | "100/100"
    Outline | Center | 404x45
    Tiltle | Left | (0, -3) | 113x51 | [TextComponent] | "MP"
  Money_1 | TopCenter | (-150, -30) | 250x64
    Icon | Left | (26, 0) | 65x62
    Num | Center | (25, -0) | 190x60 | [TextComponent] | "9,999,999"
  Money_2 | TopCenter | (120, -30) | 250x64
    Icon | Left | (32, 0) | 68x71
    Num | Center | (25, -0) | 190x60 | [TextComponent] | "9,999,999"

============================================================
  PopupGroup.ui  (435 entities)
============================================================
PopupGroup | GroupOrder=4 | StretchAll | 1920x1080 | [UIGroupComponent]
  AchievementPopup | StretchAll | (0, -0) | 2360x1520 | (disabled)
    Panel | Center | (0, -10) | 900x950
  BasicPopup | StretchAll | 2360x1520 | (disabled)
    Panel | Center | (0, 10) | 810x910
  DailyRewardPopup | StretchAll | (0, -0) | 2360x1520 | (disabled)
    Panel | Center | 1144x980
  InventoryPopup | StretchAll | 2360x1520 | (disabled)
    Panel | Center | (0, -10) | 1450x950
  ShopPopup | StretchAll | 2360x1520 | (disabled)
    Panel | Center | (0, -10) | 1450x950
  Shop_DetailInfoPopup | StretchAll | 2360x1520 | (disabled)
    DetailInfoPopup | StretchAll | 2360x1520
  TabPopup | StretchAll | (0, -0) | 2360x1520 | (disabled)
    Panel | Center | (0, 10) | 1250x910

============================================================
  ToastGroup.ui  (2 entities)
============================================================
ToastGroup | GroupOrder=2 | hidden | StretchAll | 1920x1080 | [UIGroupComponent] | (disabled)
  Toast_message | TopCenter | (0, -64) | 210x79 | [TextComponent] | "message"
```
