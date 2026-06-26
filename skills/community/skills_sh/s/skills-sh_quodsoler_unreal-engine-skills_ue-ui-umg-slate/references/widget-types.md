# UMG Widget Type Reference

> Source: `Engine/Source/Runtime/UMG/Public/Components/`

---

## UButton

**Header:** `Components/Button.h`
**Base class:** `UContentWidget` (single child slot)
**Slate backing:** `SButton`

### Key Delegates (BlueprintAssignable)

| Delegate | Type | Description |
|---|---|---|
| `OnClicked` | `FOnButtonClickedEvent` | Mouse release after press (default DownAndUp) |
| `OnPressed` | `FOnButtonPressedEvent` | Mouse/key press begins |
| `OnReleased` | `FOnButtonReleasedEvent` | Mouse/key released |
| `OnHovered` | `FOnButtonHoverEvent` | Cursor enters bounds |
| `OnUnhovered` | `FOnButtonHoverEvent` | Cursor leaves bounds |

### Key Methods

```cpp
void SetStyle(const FButtonStyle& InStyle);
const FButtonStyle& GetStyle() const;
void SetColorAndOpacity(FLinearColor InColorAndOpacity);
FLinearColor GetColorAndOpacity() const;
void SetBackgroundColor(FLinearColor InBackgroundColor);
FLinearColor GetBackgroundColor() const;
bool IsPressed() const;
void SetClickMethod(EButtonClickMethod::Type InClickMethod);
void SetTouchMethod(EButtonTouchMethod::Type InTouchMethod);
void SetPressMethod(EButtonPressMethod::Type InPressMethod);
void SetAllowDragDrop(bool bInAllowDragDrop);
```

### Click Methods

| `EButtonClickMethod` | Behavior |
|---|---|
| `DownAndUp` | Default. Click fires on mouse up after mouse down. |
| `MouseDown` | Fires immediately on mouse down. |
| `MouseUp` | Fires on mouse up regardless of where mouse down was. |
| `PreciseClick` | Fires on mouse up only if cursor is still over the button. |

### UE5.2+ Deprecation Note

Direct property access (`WidgetStyle`, `ColorAndOpacity`, `BackgroundColor`, `ClickMethod`, `TouchMethod`, `PressMethod`, `IsFocusable`) is deprecated. Use the getter/setter methods above.

### BindWidget Example

```cpp
UPROPERTY(meta=(BindWidget))
TObjectPtr<UButton> ConfirmButton;

// In NativeConstruct:
ConfirmButton->OnClicked.AddDynamic(this, &UMyWidget::HandleConfirm);
ConfirmButton->SetColorAndOpacity(FLinearColor(0.2f, 0.8f, 0.2f, 1.f));
```

---

## UTextBlock

**Header:** `Components/TextBlock.h`
**Base class:** `UTextLayoutWidget`
**Slate backing:** `STextBlock`

### Key Properties (use setters in UE5.1+)

| Property | Type | Description |
|---|---|---|
| `Text` | `FText` | Displayed text |
| `Font` | `FSlateFontInfo` | Font, size, typeface |
| `ColorAndOpacity` | `FSlateColor` | Text color |
| `ShadowOffset` | `FVector2D` | Drop shadow offset |
| `ShadowColorAndOpacity` | `FLinearColor` | Drop shadow color |
| `MinDesiredWidth` | `float` | Minimum widget width |
| `TextTransformPolicy` | `ETextTransformPolicy` | None, ToLower, ToUpper |
| `TextOverflowPolicy` | `ETextOverflowPolicy` | Clip, Ellipsis, MultilineEllipsis |
| `bSimpleTextMode` | `bool` | Fast path for ASCII/numeric text |

### Key Methods

```cpp
FText GetText() const;
void SetText(FText InText);                                   // Wipes Blueprint binding!
void SetColorAndOpacity(FSlateColor InColorAndOpacity);
void SetOpacity(float InOpacity);
void SetShadowColorAndOpacity(FLinearColor InShadowColorAndOpacity);
void SetShadowOffset(FVector2D InShadowOffset);
void SetFont(FSlateFontInfo InFontInfo);
void SetStrikeBrush(FSlateBrush InStrikeBrush);
void SetMinDesiredWidth(float InMinDesiredWidth);
void SetAutoWrapText(bool InAutoTextWrap);
void SetTextTransformPolicy(ETextTransformPolicy InTransformPolicy);
void SetTextOverflowPolicy(ETextOverflowPolicy InOverflowPolicy);
void SetFontMaterial(UMaterialInterface* InMaterial);
void SetFontOutlineMaterial(UMaterialInterface* InMaterial);
UMaterialInstanceDynamic* GetDynamicFontMaterial();
UMaterialInstanceDynamic* GetDynamicOutlineMaterial();
```

### Common Patterns

```cpp
// Simple string (avoid — prefer FText for localization)
ScoreLabel->SetText(FText::FromString(TEXT("Score: 100")));

// Localized with format argument
ScoreLabel->SetText(FText::Format(
    NSLOCTEXT("HUD", "ScoreFmt", "Score: {0}"),
    FText::AsNumber(Score)));

// Number with grouping (e.g., "1,234,567")
ScoreLabel->SetText(FText::AsNumber(Score));

// Uppercase transform
ScoreLabel->SetTextTransformPolicy(ETextTransformPolicy::ToUpper);

// Ellipsis for overflow
ScoreLabel->SetTextOverflowPolicy(ETextOverflowPolicy::Ellipsis);

// Font from content
FSlateFontInfo FontInfo = FCoreStyle::GetDefaultFont();
FontInfo.Size = 32;
ScoreLabel->SetFont(FontInfo);
```

---

## UImage

**Header:** `Components/Image.h`
**Base class:** `UWidget` (no children)
**Slate backing:** `SImage`

### Key Properties

| Property | Type | Description |
|---|---|---|
| `Brush` | `FSlateBrush` | The image resource and drawing settings |
| `ColorAndOpacity` | `FLinearColor` | Tint applied to the image |
| `bFlipForRightToLeftFlowDirection` | `bool` | RTL localization support |

### Key Methods

```cpp
void SetColorAndOpacity(FLinearColor InColorAndOpacity);
void SetOpacity(float InOpacity);
void SetBrush(const FSlateBrush& InBrush);
const FSlateBrush& GetBrush() const;
void SetBrushFromAsset(USlateBrushAsset* Asset);
void SetBrushFromTexture(UTexture2D* Texture, bool bMatchSize = false);
void SetBrushFromTextureDynamic(UTexture2DDynamic* Texture, bool bMatchSize = false);
void SetBrushFromMaterial(UMaterialInterface* Material);
void SetBrushFromSoftTexture(TSoftObjectPtr<UTexture2D> SoftTexture, bool bMatchSize = false);
void SetBrushFromSoftMaterial(TSoftObjectPtr<UMaterialInterface> SoftMaterial);
void SetBrushFromAtlasInterface(TScriptInterface<ISlateTextureAtlasInterface> AtlasRegion, bool bMatchSize = false);
void SetDesiredSizeOverride(FVector2D DesiredSize);
void SetBrushTintColor(FSlateColor TintColor);
void SetBrushResourceObject(UObject* ResourceObject);
UMaterialInstanceDynamic* GetDynamicMaterial();
void SetFlipForRightToLeftFlowDirection(bool bFlip);
```

### Common Patterns

```cpp
// Static texture
AvatarImage->SetBrushFromTexture(LoadObject<UTexture2D>(nullptr, TEXT("/Game/UI/T_Avatar")));

// Material instance dynamic for animation or parameters
AvatarImage->SetBrushFromMaterial(AvatarMaterial);
UMaterialInstanceDynamic* MID = AvatarImage->GetDynamicMaterial();
MID->SetScalarParameterValue(TEXT("GlowIntensity"), 1.5f);
MID->SetVectorParameterValue(TEXT("Tint"), FLinearColor::Yellow);

// Async stream from soft pointer (no blocking load)
AvatarImage->SetBrushFromSoftTexture(SoftAvatarTexture, /*bMatchSize=*/true);

// Size override
AvatarImage->SetDesiredSizeOverride(FVector2D(64.f, 64.f));

// Tint without touching the brush
AvatarImage->SetColorAndOpacity(FLinearColor(1.f, 0.5f, 0.5f, 1.f));
```

---

## UProgressBar

**Header:** `Components/ProgressBar.h`
**Base class:** `UWidget` (no children)
**Slate backing:** `SProgressBar`

### Key Properties

| Property | Type | Description |
|---|---|---|
| `Percent` | `float` | Fill value 0.0–1.0 |
| `BarFillType` | `EProgressBarFillType` | LeftToRight, RightToLeft, FillFromCenter, etc. |
| `BarFillStyle` | `EProgressBarFillStyle` | Scale or Mask |
| `bIsMarquee` | `bool` | Indeterminate animation |
| `FillColorAndOpacity` | `FLinearColor` | Fill color |

### Key Methods

```cpp
float GetPercent() const;
void SetPercent(float InPercent);                  // Primary runtime update
void SetFillColorAndOpacity(FLinearColor InColor);
FLinearColor GetFillColorAndOpacity() const;
void SetIsMarquee(bool InbIsMarquee);
bool UseMarquee() const;
void SetBarFillType(EProgressBarFillType::Type InBarFillType);
void SetBarFillStyle(EProgressBarFillStyle::Type InBarFillStyle);
void SetBorderPadding(FVector2D InBorderPadding);
```

### Fill Types

| `EProgressBarFillType` | Description |
|---|---|
| `LeftToRight` | Default, fills left to right |
| `RightToLeft` | Fills right to left |
| `FillFromCenter` | Fills outward from center (vertical) |
| `FillFromCenterHorizontal` | Fills outward from center (horizontal) |
| `FillFromCenterVertical` | Fills up/down from vertical center |
| `TopToBottom` | Fills top to bottom |
| `BottomToTop` | Fills bottom to top |

### Common Patterns

```cpp
// Health bar
HealthBar->SetPercent(Health / MaxHealth);
HealthBar->SetFillColorAndOpacity(Health > MaxHealth * 0.3f
    ? FLinearColor(0.f, 0.8f, 0.f, 1.f)  // Green
    : FLinearColor(0.9f, 0.1f, 0.f, 1.f));// Red

// Loading spinner (marquee)
LoadingBar->SetIsMarquee(true);

// Experience bar filling right-to-left
XPBar->SetBarFillType(EProgressBarFillType::LeftToRight);
XPBar->SetPercent(XP / XPToNextLevel);
```

---

## UListView

**Header:** `Components/ListView.h`
**Base class:** `UListViewBase`, `ITypedUMGListView<UObject*>`
**Slate backing:** `SListView<UObject*>`

The list is virtualized: only visible entry widgets exist. Items are data objects; entry widgets are reused as the list scrolls.

### Key Delegates

| Delegate | Signature | Description |
|---|---|---|
| `BP_OnItemClicked` | `(UObject* Item)` | Item clicked |
| `BP_OnItemDoubleClicked` | `(UObject* Item)` | Item double-clicked |
| `BP_OnItemSelectionChanged` | `(UObject* Item, bool bIsSelected)` | Selection changed |
| `BP_OnEntryInitialized` | `(UObject* Item, UUserWidget* Widget)` | Entry widget assigned |
| `BP_OnItemScrolledIntoView` | `(UObject* Item, UUserWidget* Widget)` | Item scrolled visible |

### Key Methods

```cpp
// Add / remove items
void AddItem(UObject* Item);
void RemoveItem(UObject* Item);
void ClearListItems();
void SetListItems(const TArray<ItemObjectT, AllocatorType>& InListItems); // Template

// Query
const TArray<UObject*>& GetListItems() const;
UObject* GetItemAt(int32 Index) const;
int32 GetNumItems() const;
int32 GetIndexForItem(const UObject* Item) const;
bool IsRefreshPending() const;

// Selection (single-selection recommended for GetSelectedItem)
void SetSelectedItem(const UObject* Item);
void SetSelectedIndex(int32 Index);
UObject* GetSelectedItem() const;               // Template: GetSelectedItem<UMyData>()
bool BP_GetSelectedItems(TArray<UObject*>& Items) const;
int32 BP_GetNumItemsSelected() const;
void BP_ClearSelection();
void SetSelectionMode(TEnumAsByte<ESelectionMode::Type> SelectionMode);

// Navigation and scrolling
void ScrollIndexIntoView(int32 Index);
void NavigateToIndex(int32 Index);
void BP_ScrollItemIntoView(UObject* Item);
void BP_NavigateToItem(UObject* Item);
bool BP_IsItemVisible(UObject* Item) const;

// Entry widget retrieval (only valid when the entry is visible)
RowWidgetT* GetEntryWidgetFromItem(const UObject* Item) const; // Template
```

### IUserObjectListEntry (entry widget interface)

```cpp
// Entry widget header:
UCLASS()
class UMyEntryWidget : public UUserWidget, public IUserObjectListEntry
{
    GENERATED_BODY()
protected:
    // Implement this — called each time the entry is assigned a new item object
    virtual void NativeOnListItemObjectSet(UObject* ListItemObject) override;

    // IUserListEntry helpers (from parent interface):
    // bool IsItemSelected() const;
    // bool IsItemExpanded() const;  // TreeView only
};

// Access the assigned item from within the entry widget:
UMyData* Data = GetListItem<UMyData>();

// Static helpers (BlueprintCallable via UUserObjectListEntryLibrary):
// UObject* GetListItemObject(...)
// int32 GetListItemIndex(...)
// bool IsFirstWidget(...)
// bool IsLastWidget(...)
```

### UTileView

Works identically to `UListView` but arranges entries in a 2D grid. Entry height is set on the `UTileView`. Uses the same `IUserObjectListEntry` interface.

---

## UScrollBox

**Header:** `Components/ScrollBox.h`
**Base class:** `UPanelWidget` (multiple children)

```cpp
// Programmatic scroll
MyScrollBox->ScrollToStart();
MyScrollBox->ScrollToEnd();
MyScrollBox->ScrollWidgetIntoView(ChildWidget, /*bAnimateScroll=*/true);
MyScrollBox->SetScrollOffset(200.f);
float Offset = MyScrollBox->GetScrollOffset();
```

---

## UWidgetSwitcher

**Header:** `Components/WidgetSwitcher.h`

```cpp
// Only one child is visible at a time (zero-based index)
MySwitcher->SetActiveWidgetIndex(1);
MySwitcher->SetActiveWidget(MyChildWidget);
int32 Index = MySwitcher->GetActiveWidgetIndex();
UWidget* Active = MySwitcher->GetActiveWidget();
int32 Count = MySwitcher->GetNumWidgets();
```

---

## UCheckBox

```cpp
// State
bool bChecked = MyCheckBox->IsChecked();
MyCheckBox->SetIsChecked(true);
ECheckBoxState State = MyCheckBox->GetCheckedState();
// ECheckBoxState: Unchecked, Checked, Undetermined

// Delegate
MyCheckBox->OnCheckStateChanged.AddDynamic(this, &UMyWidget::HandleCheckChanged);
// Signature: void HandleCheckChanged(bool bIsChecked)
```

---

## UEditableTextBox

```cpp
FText Text = MyInput->GetText();
MyInput->SetText(FText::FromString(TEXT("Default")));
MyInput->SetHintText(NSLOCTEXT("UI", "SearchHint", "Search..."));
MyInput->SetIsReadOnly(true);
MyInput->SetIsPassword(true); // Mask characters

// Delegates
MyInput->OnTextChanged.AddDynamic(this, &UMyWidget::HandleTextChanged);
MyInput->OnTextCommitted.AddDynamic(this, &UMyWidget::HandleTextCommitted);
// Committed signature: void(const FText& Text, ETextCommit::Type CommitMethod)
// ETextCommit: OnEnter, OnUserMovedFocus, OnCleared, Default
```

---

## USlider

```cpp
float Value = MySlider->GetValue();       // 0.0 – 1.0
MySlider->SetValue(0.5f);
MySlider->SetMinValue(0.f);
MySlider->SetMaxValue(100.f);
MySlider->SetStepSize(1.f);
MySlider->SetOrientation(EOrientation::Orient_Horizontal);

MySlider->OnValueChanged.AddDynamic(this, &UMyWidget::HandleSliderChanged);
// Signature: void(float Value)
```

---

## UComboBoxString

```cpp
MyCombo->AddOption(TEXT("Option A"));
MyCombo->AddOption(TEXT("Option B"));
MyCombo->SetSelectedOption(TEXT("Option A"));
FString Selected = MyCombo->GetSelectedOption();
int32 Count = MyCombo->GetOptionCount();
MyCombo->ClearOptions();
MyCombo->RefreshOptions();

MyCombo->OnSelectionChanged.AddDynamic(this, &UMyWidget::HandleComboChanged);
// Signature: void(FString SelectedItem, ESelectInfo::Type SelectionType)
```

---

## Visibility Reference

| `ESlateVisibility` | Rendered | Takes Space | Receives Input |
|---|---|---|---|
| `Visible` | Yes | Yes | Yes |
| `Collapsed` | No | No | No |
| `Hidden` | No | Yes | No |
| `HitTestInvisible` | Yes | Yes | No (passes through) |
| `SelfHitTestInvisible` | Yes | Yes | Children only |

```cpp
Widget->SetVisibility(ESlateVisibility::Collapsed);
ESlateVisibility V = Widget->GetVisibility();
bool bVisible = V == ESlateVisibility::Visible;
```

---

## UWidget Base (All Widgets)

All UMG widgets inherit from `UWidget`:

```cpp
// Enable/disable (grays out and blocks input)
Widget->SetIsEnabled(false);
bool bEnabled = Widget->GetIsEnabled();

// Render opacity (does not affect layout or hit testing)
Widget->SetRenderOpacity(0.5f);
float Opacity = Widget->GetRenderOpacity();

// Transform (applied as render transform, not layout)
Widget->SetRenderTransformAngle(45.f);
Widget->SetRenderTranslation(FVector2D(10.f, 0.f));
Widget->SetRenderScale(FVector2D(1.2f, 1.2f));

// Tooltip
Widget->SetToolTipText(NSLOCTEXT("UI", "Tip", "Click to confirm"));

// Cursor
Widget->SetCursor(EMouseCursor::Hand);

// Focus
Widget->SetKeyboardFocus();
bool bHasFocus = Widget->HasKeyboardFocus();

// Slate widget access (for Slate-only APIs)
TSharedPtr<SWidget> SlateWidget = Widget->GetCachedWidget();
```
