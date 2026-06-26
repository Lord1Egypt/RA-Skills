# Style 4 (Blue) — UI Structure

Format: `Name | Alignment | (x, y) | WxH | [Components] | (state)`

```
============================================================
  ButtonGroup.ui  (26 entities)
============================================================
ButtonGroup | GroupOrder=3 | StretchAll | 1952x1080 | [UIGroupComponent]
  Btn_Achievement | TopRight | (-30, -583) | 140x140 | [Button]
    Icon | Center | (0, 2) | 64x72
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Achievement"
  Btn_Attendance | TopRight | (-30, -432) | 140x140 | [Button]
    Icon | Center | (0, 5) | 64x68
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Attendance"
  Btn_Basic | TopRight | (-30, -130) | 140x140 | [Button]
    Icon | Center | (0, 3) | 80x80
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Basic Popup 1"
  Btn_GameResult | TopRight | (-30, -885) | 140x140 | [Button]
    Icon | Center | (0, 2) | 48x72
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Game Ranking"
  Btn_Inven | TopRight | (-30, -734) | 140x140 | [Button]
    Icon | Center | (0, 5) | 72x64
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Inventory"
  Btn_Shop | TopRight | (-330, -287) | 130x130 | [Button]
    Icon | Center | (0, 5) | 80x76
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Gacha Shop"
  Btn_ShopMenu | TopRight | (-30, -281) | 140x140 | [Button]
    Icon | Center | (0, 5) | 80x76
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Shop"
    UISprite | Left | (10, 0) | 68x68
  Btn_ShopResult | TopRight | (-190, -287) | 130x130 | [Button]
    Icon | Center | (0, 5) | 80x76
    Title | BottomCenter | (0, 10) | 170x43 | [TextComponent] | "Gacha Result"

============================================================
  DefaultGroup.ui  (7 entities)
============================================================
DefaultGroup | GroupOrder=1 | hidden | StretchAll | 1920x1080 | [UIGroupComponent]
  Button_Attack | BottomRight | (-175, 332) | 204x204 | [Button]
    UISprite | Center | (-2, -1) | 108x109
  Button_Jump | BottomRight | (-392, 194) | 204x204 | [Button]
    UISprite | Center | (-5, 1) | 153x134
  UIChat | TopLeft | (369, -252) | 698x439 | [ChatComponent]
  UIJoystick | BottomLeft | (310, 230) | 200x200 | [JoystickComponent]

============================================================
  HUDGroup.ui  (33 entities)
============================================================
HUDGroup | GroupOrder=0 | StretchAll | 1920x1080 | [UIGroupComponent]
  ButtonGroup | TopLeft | 400x200
    Btn_FreeZone | TopLeft | (197, -10) | 140x140
    Btn_Hall | TopLeft | (30, -10) | 140x140
  MatchingPanel | TopCenter | (0, -150) | 600x150
    MatchingBG | Center | 300x88
    MatchingPlayers | TopLeft | (60, -5) | 201x35 | [TextComponent] | "Matching Players: 10"
    StartButton | Right | (-18, 0) | 250x104 | [Button]
    UIText | Left | (60, 0) | 260x50 | [TextComponent] | "Game Map Name"
  PlayerInfo | TopCenter | (0, -25) | 900x100
    DiaInfoBG | TopRight | 300x100
    LevelInfoBG | TopLeft | 350x100
    MesoInfoBG | TopCenter | (20, 0) | 300x100

============================================================
  PopupGroup.ui  (644 entities)
============================================================
PopupGroup | GroupOrder=4 | StretchAll | 1920x1080 | [UIGroupComponent]
  AchievementPopup | StretchAll | 2520x1680 | (disabled)
    Panel | Center | (0, -30) | 1400x900
  BasicPopup | StretchAll | 2520x1680 | (disabled)
    Panel | Center | 850x540
  DailyRewardPopup | StretchAll | 2520x1680 | (disabled)
    Panel | Center | (0, -50) | 1500x900
  InventoryPopup | StretchAll | 2520x1680 | (disabled)
    Panel | Center | (0, -20) | 1550x881
  ResultPanel | Right | (-20, -35) | 725x900 | (disabled)
    Bg | BottomCenter | (0, 9) | 706x196
    MyInfo | TopCenter | (0, -780) | 676x130
    Ranking | TopCenter | (0, -364) | 675x679 | [ScrollLayout]
    ReturnToLobby | BottomCenter | (-155, 10) | 300x104 | [Button, TextComponent] | "Return to Lobby"
    SaveResult | BottomCenter | (155, 10) | 300x104 | [Button, TextComponent] | "Save Result"
  ShopPopup | StretchAll | 2520x1680 | (disabled)
    Panel | Center | (0, -50) | 900x850
  ShopResult | StretchAll | 2520x1680 | (disabled)
    Deco | Center | (0, 220) | 750x750 | [TweenCircularComponent]
    DecoDpt | Center | (0, 6) | 100x100
    PopupBtnOK | Center | (0, -280) | 300x104 | [Button, TextComponent] | "OK"
    PopupName | Center | (0, 200) | 916x176
    ResultEffect | Center | (0, -300) | 800x760 | (disabled)
    ResultItemBG | HStretchCenter | (0, -47) | 1680x460

============================================================
  ToastGroup.ui  (2 entities)
============================================================
ToastGroup | GroupOrder=2 | hidden | StretchAll | 1920x1080 | [UIGroupComponent]
  Toast_message | TopCenter | (0, -64) | 210x79 | [TextComponent] | "message"
```
