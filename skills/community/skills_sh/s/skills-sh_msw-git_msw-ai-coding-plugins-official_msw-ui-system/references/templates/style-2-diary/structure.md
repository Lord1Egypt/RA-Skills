# Style 2 (Diary) — UI Structure

Format: `Name | Alignment | (x, y) | WxH | [Components] | (state)`

```
============================================================
  HUDGroup.ui  (12 entities)
============================================================
HUDGroup | GroupOrder=3 | StretchAll | 1920x1080 | [UIGroupComponent]
  BroadCastUI | Left | (1002, 343) | 981x136
    Panel | Center | (-72, 76) | 889x135
  PlrprofileUI | Left | (260, 421) | 439x194 | [Button]
    Profilepanel | StretchAll | (0, 2) | 439x190

============================================================
  PopupGroup.ui  (85 entities)
============================================================
PopupGroup | GroupOrder=4 | StretchAll | 1920x1080 | [UIGroupComponent]
  BasicPopup | Center | (-35, -10) | 745x684 | (disabled)
    Btn_No | BottomCenter | (150, 97) | 208x89 | [Button, TextComponent] | "Cancel"
    Btn_Ok | BottomCenter | (-150, 97) | 208x89 | [Button, TextComponent] | "OK"
    Img_Bg_1 | Center | (-1, 69) | 683x504
    Img_Clip_1 | TopCenter | (0, 4) | 89x105
  BasicPopup2 | Center | (-5, -29) | 1300x964 | (disabled)
    CloseButton | TopRight | (-65, -68) | 88x92 | [Button]
    Img_Acc_1_1_1 | Center | (-176, 265) | 73x34
    Img_Bg_Left | Right | (-1048, -63) | 434x782
    Img_Bg_Right | Center | (216, -63) | 792x782
    Left_SlotPanel | Center | (-402, -61) | 356x734
    SlotScroll | Center | (-402, -61) | 356x722 | [ScrollLayout]
    TitleText | HStretchTop | (-0, -66) | 1300x135 | [TextComponent] | "Title Title Title"
  GameResultPanel | Center | (-15, -32) | 1300x964 | (disabled)
    Btn_Ok_1 | BottomCenter | (0, 117) | 208x89 | [Button, TextComponent] | "OK"
    Img_Acc_1_1 | TopCenter | (0, -270) | 1180x6
    Img_Acc_2 | TopCenter | 89x105
    Img_Line_1_1_1 | StretchAll | (-3, -1) | 1240x889
    IndexPanel | StretchAll | (0, 4) | 1174x625
    MyResultPanel | BottomCenter | (2, 240) | 1154x109
    Time | BottomRight | (-328, 85) | 599x146 | [TextComponent]
    TitlePanel | TopCenter | (0, -100) | 328x98
  InventoryUI | Center | (-15, -32) | 1300x963 | (disabled)
    Bg_Right | Center | (243, -61) | 758x775
    CloseButton | TopRight | (-61, -68) | 88x92 | [Button]
    FilterPanel | Center | (369, 176) | 990x102 | [ScrollLayout]
    Img_Line | StretchAll | (0, -65) | 1288x799
    Item_Info | Center | (-386, 41) | 457x554
    MainPanel | Center | (239, -154) | 749x578 | [ScrollLayout]
    TitlePanel | HStretchCenter | (0, 412) | 1300x100
    UserGoldPanel | Center | (437, 280) | 316x56
    VolumePanel | Center | (-14, 279) | 173x56
  UIChat | TopLeft | (369, -252) | 698x439 | [ChatComponent] | (disabled)

============================================================
  Popupbutton.ui  (9 entities)
============================================================
Popupbutton | GroupOrder=2 | StretchAll | 1920x1080 | [UIGroupComponent]
  1 | Left | (108, 231) | 129x98 | [Button, script.Popupbutton]
    UIText | Left | (64, 3) | 100x100 | [TextComponent] | "Popup 1"
  2 | Left | (110, 125) | 129x98 | [Button, script.Popupbutton]
    UIText | Left | (64, 3) | 100x100 | [TextComponent] | "Popup 2"
  3 | Left | (109, 17) | 129x98 | [Button, script.Popupbutton]
    UIText | Left | (64, 3) | 100x100 | [TextComponent] | "Popup 3"
  4 | Left | (111, -91) | 129x98 | [Button, script.Popupbutton]
    UIText | Left | (64, 3) | 100x100 | [TextComponent] | "Popup 4"

============================================================
  ToastGroup.ui  (1 entities)
============================================================
ToastGroup | GroupOrder=1 | StretchAll | 1920x1080 | [UIGroupComponent] | (disabled)

============================================================
  TrashBin.ui  (1 entities)
============================================================
TrashBin | GroupOrder=0 | hidden | StretchAll | 1920x1080 | [UIGroupComponent]
```
