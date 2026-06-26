# Style 1 (Black) — UI Structure

Format: `Name | Alignment | (x, y) | WxH | [Components] | (state)`

```
============================================================
  ButtonGroup.ui  (13 entities)
============================================================
ButtonGroup | GroupOrder=3 | StretchAll | 1920x1080 | [UIGroupComponent]
  1 | Center | (-829, 196) | 235x88 | [Button, script.Popupbutton]
    UIText | Center | (-1, 7) | 100x100 | [TextComponent] | "Popup 1"
  2 | Center | (-829, 97) | 235x88 | [Button, script.Popupbutton]
    UIText | Center | (-1, 7) | 100x100 | [TextComponent] | "Popup 2"
  3 | Center | (-829, -4) | 235x88 | [Button, script.Popupbutton]
    UIText | Center | (-1, 7) | 100x100 | [TextComponent] | "Popup 3"
  4 | Center | (-829, -104) | 235x88 | [Button, script.Popupbutton]
    UIText | Center | (-1, 7) | 100x100 | [TextComponent] | "Popup 4"
  5 | Center | (-829, -201) | 235x88 | [Button, script.Popupbutton]
    UIText | Center | (-1, 7) | 100x100 | [TextComponent] | "Popup 5"
  6 | Center | (-829, -295) | 235x88 | [Button, script.Popupbutton]
    UIText | Center | (-1, 7) | 100x100 | [TextComponent] | "Popup 6"

============================================================
  DefaultGroup.ui  (3 entities)
============================================================
DefaultGroup | GroupOrder=1 | StretchAll | 1920x1080 | [UIGroupComponent] | (disabled)
  UIChat | TopLeft | (369, -252) | 698x439 | [ChatComponent]
  UIJoystick | BottomLeft | (310, 230) | 200x200 | [JoystickComponent]

============================================================
  HUDGroup.ui  (22 entities)
============================================================
HUDGroup | GroupOrder=0 | StretchAll | 1920x1080 | [UIGroupComponent]
  QuestHUD | TopCenter | (-486, -25) | 465x220 | [Button]
    QuestDescription | StretchAll | (1, -28) | 463x165 | [TextComponent] | "Defeat Orange Mushroom  0/10
Defeat Slime 0/10"
    Title | HStretchTop | 465x57 | [TextComponent] | "Main Quest"
    bg_title | HStretchTop | (-0, -0) | 465x55
  UIMatch | TopCenter | (90, -38) | 540x340
    Title | HStretchTop | 510x70 | [TextComponent] | "Mini Game Open!"
    img_pattern | StretchAll | 510x310
    matchBtn | HStretchBottom | (81, 38) | 300x70 | [Button]
    matchCancelBtn | HStretchBottom | (81, 38) | 300x70 | [Button]
    textMatchGame | HStretchTop | (0, -103) | 510x50 | [TextComponent] | "Mini Game Name"
    textMatchInfo | HStretchTop | (0, -148) | 510x50 | [TextComponent] | "Max Players: 1~10"
    textRecommendedLevel | HStretchTop | (0, -193) | 510x50 | [TextComponent] | "Recommended Level: LV 5 ↑"
    textWaitInfo | BottomLeft | (43, 43) | 157x61 | [TextComponent] | "0"
    timer | TopLeft | (31, -20) | 82x91

============================================================
  PopupGroup.ui  (131 entities)
============================================================
PopupGroup | GroupOrder=4 | StretchAll | 1920x1080 | [UIGroupComponent]
  AchieveUI | Center | (0, -0) | 1408x680 | (disabled)
    Panel_slot | StretchAll | (0, -35) | 1328x530 | [GridViewComponent]
    TitlePanel | HStretchTop | 1408x100
  BasicPopup | Center | (8, 5) | 981x508 | (disabled)
    PopupBtnCancel | Center | (206, -155) | 415x105 | [Button, TextComponent] | "Cancel"
    PopupBtnOK | Center | (-206, -155) | 415x105 | [Button, TextComponent] | "OK"
    PopupMessage | Center | (0, 80) | 780x260 | [TextComponent] | "Popup Message"
    deco_line | HStretchCenter | (0, -70) | 945x2
    img_deco | StretchAll | (0, -0) | 955x482
    img_pattern | StretchAll | 951x478
  InventoryUI | Center | (-32, -11) | 740x1046 | (disabled)
    BottomPanel | HStretchBottom | (0, 13) | 714x80
    CategoryPanel | HStretchTop | (0, -124) | 646x88 | [ScrollLayout]
    ContentPanel | StretchAll | (40, 93) | 660x718 | [ScrollLayout]
    TopPanel | HStretchTop | 732x97
  MonsterDexUI | Center | (0, -18) | 1455x1066 | (disabled)
    AchieveBG | HStretchBottom | (0, 60) | 1351x17
    CategoryPanel | TopLeft | (62, -124) | 602x86 | [ScrollLayout]
    MonsterDexBG | StretchAll | (0, 10) | 1455x1046
    Panel_info | TopRight | (-62, -124) | 700x829
    Panel_slot | StretchAll | (40, 103) | 615x728
    TitlePanel | HStretchTop | 1455x100
  QuestUI | Center | (0, -26) | 1376x954 | (disabled)
    LeftPanel | StretchAll | (-344, -38) | 623x811 | [ScrollLayout]
    QuestUITitle | HStretchTop | 1376x97
    RightPanel | VStretchRight | (-366, -48) | 706x831
  ShopUI | Center | (-14, 31) | 1600x800 | (disabled)
    CategoryPanel | VStretchLeft | (43, -115) | 200x642 | [ScrollLayout]
    ContentsPanel | StretchAll | (-43, -115) | 1277x642 | [ScrollLayout]
    TopPanel | HStretchTop | 1592x97

============================================================
  ToastGroup.ui  (2 entities)
============================================================
ToastGroup | GroupOrder=2 | hidden | StretchAll | 1920x1080 | [UIGroupComponent] | (disabled)
  Toast_message | TopCenter | (0, -64) | 210x79 | [TextComponent] | "message"
```
