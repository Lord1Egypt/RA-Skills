# Common UI Plugin — Setup and Patterns

> Source: `Engine/Plugins/Runtime/CommonUI/Source/CommonUI/Public/`

Common UI is Epic's cross-platform UI framework built on top of UMG. It handles input method detection (gamepad vs. mouse vs. touch), input routing through an activation tree, and provides base classes for platform-agnostic buttons and screens.

---

## Plugin Setup

### 1. Enable the Plugin

In `<ProjectName>.uproject`:

```json
{
  "Plugins": [
    { "Name": "CommonUI", "Enabled": true },
    { "Name": "CommonInput", "Enabled": true }
  ]
}
```

### 2. Build.cs Dependencies

```csharp
// <ProjectName>.Build.cs
PrivateDependencyModuleNames.AddRange(new string[]
{
    "CommonUI",
    "CommonInput",
});
```

### 3. Configure the Game Viewport Client

Common UI requires a custom viewport client to detect input method changes.

**Project Settings → Maps & Modes → Game Viewport Client Class** → set to `CommonGameViewportClient`.

Or in `DefaultEngine.ini`:

```ini
[/Script/Engine.Engine]
GameViewportClientClassName=/Script/CommonUI.CommonGameViewportClient
```

`UCommonGameViewportClient` detects whether the most recent input was from a gamepad, mouse, or touch, and broadcasts this change via `UCommonInputSubsystem`. All `UCommonButtonBase` and `UCommonActivatableWidget` instances respond to this automatically.

### 4. Configure Common Input Settings

In **Project Settings → Common Input Settings**:

- **Default Joystick Name**: Gamepad action icon set to display
- **Input Data**: Map platform + input type combinations to icon data tables
- **Platform Input**: Define which input types each target platform supports

Or via `DefaultInput.ini`:

```ini
[/Script/CommonInput.CommonInputSettings]
InputData=/Game/UI/CommonInputData.CommonInputData
bEnableInputMethodTrigger=True
```

---

## Core Classes

### UCommonActivatableWidget

The foundation of Common UI's screen management. A widget that can be activated (brought to focus) and deactivated without being created or destroyed.

**Header:** `CommonActivatableWidget.h`
**Base class:** `UCommonUserWidget` → `UUserWidget`

```cpp
// Activation state
bool IsActivated() const;
void ActivateWidget();
void DeactivateWidget();

// Delegates (non-dynamic multicast)
FSimpleMulticastDelegate& OnActivated() const;
FSimpleMulticastDelegate& OnDeactivated() const;

// Focus
UWidget* GetDesiredFocusTarget() const;
void ClearFocusRestorationTarget();
void RequestRefreshFocus();
```

**Key UPROPERTY settings (configure in Blueprint defaults or C++ constructor):**

```cpp
// Auto-activate when constructed (false by default)
UPROPERTY(EditAnywhere, Category = Activation)
bool bAutoActivate = false;

// Acts as a modal — blocks input routing to all ancestors
UPROPERTY(EditAnywhere, Category = Activation)
bool bIsModal = false;

// Receives "Back" action and deactivates on it
UPROPERTY(EditAnywhere, Category = Back)
bool bIsBackHandler = false;

// Restore focus to the previously-focused widget when re-activating
UPROPERTY(EditAnywhere, Category = Activation)
bool bAutoRestoreFocus = false;

// Set visibility automatically on activation/deactivation
UPROPERTY(EditAnywhere, Category = Activation)
bool bSetVisibilityOnActivated = false;
UPROPERTY(EditAnywhere, Category = Activation)
ESlateVisibility ActivatedVisibility = ESlateVisibility::SelfHitTestInvisible;
UPROPERTY(EditAnywhere, Category = Activation)
bool bSetVisibilityOnDeactivated = false;
UPROPERTY(EditAnywhere, Category = Activation)
ESlateVisibility DeactivatedVisibility = ESlateVisibility::Collapsed;
```

**Subclassing pattern:**

```cpp
// MyMenuScreen.h
#pragma once
#include "CommonActivatableWidget.h"
#include "MyMenuScreen.generated.h"

UCLASS()
class MYGAME_API UMyMenuScreen : public UCommonActivatableWidget
{
    GENERATED_BODY()

protected:
    virtual void NativeOnActivated() override;
    virtual void NativeOnDeactivated() override;
    virtual UWidget* NativeGetDesiredFocusTarget() const override;
    virtual TOptional<FUIInputConfig> GetDesiredInputConfig() const override;

    UPROPERTY(meta=(BindWidget)) TObjectPtr<UCommonButtonBase> CloseButton;
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UCommonButtonBase> ConfirmButton;
};
```

```cpp
// MyMenuScreen.cpp
void UMyMenuScreen::NativeOnActivated()
{
    Super::NativeOnActivated();
    CloseButton->OnClicked().AddUObject(this, &UMyMenuScreen::DeactivateWidget);
    ConfirmButton->OnClicked().AddUObject(this, &UMyMenuScreen::HandleConfirm);
}

void UMyMenuScreen::NativeOnDeactivated()
{
    CloseButton->OnClicked().RemoveAll(this);
    ConfirmButton->OnClicked().RemoveAll(this);
    Super::NativeOnDeactivated();
}

UWidget* UMyMenuScreen::NativeGetDesiredFocusTarget() const
{
    // The first focusable button receives focus when this screen activates
    return ConfirmButton;
}

TOptional<FUIInputConfig> UMyMenuScreen::GetDesiredInputConfig() const
{
    // ECommonInputMode::Menu — enables gamepad menu navigation, hides cursor on gamepad
    return FUIInputConfig(ECommonInputMode::Menu, EMouseCaptureMode::NoCapture);
}
```

---

### UCommonActivatableWidgetStack

**Header:** `Widgets/CommonActivatableWidgetContainer.h`
**Base class:** `UCommonActivatableWidgetContainerBase`

The correct class for screen layer stacks. Shows only the topmost widget; deactivating the top widget reveals the previous one. Use this for game layer, menu layer, and modal layer containers — do NOT use `UCommonActivatableWidgetSwitcher` here, which inherits from `UCommonAnimatedSwitcher`/`UWidgetSwitcher` and is a different (index-based switcher) widget that does not have `AddWidget()`.

```cpp
// In a root HUD widget:
UPROPERTY(meta=(BindWidget))
TObjectPtr<UCommonActivatableWidgetStack> MenuLayer;

// Push a new screen onto the stack:
void UMyHUDWidget::ShowOptionsScreen()
{
    UMyOptionsScreen* Screen = Cast<UMyOptionsScreen>(
        MenuLayer->AddWidget(UMyOptionsScreen::StaticClass()));
    // AddWidget creates and activates the widget internally
}

// Go back (deactivate top widget — stack re-activates the previous one):
void UMyHUDWidget::GoBack()
{
    if (UCommonActivatableWidget* Active = MenuLayer->GetActiveWidget())
    {
        Active->DeactivateWidget();
    }
}
```

**Important:** `UCommonActivatableWidgetStack::AddWidget(TSubclassOf<UCommonActivatableWidget>)` creates the widget and pushes it. It returns `UCommonActivatableWidget*` (cast to your type). Deactivating the top widget automatically re-activates the widget beneath it.

---

### UCommonButtonBase

**Header:** `CommonButtonBase.h`
**Base class:** `UCommonUserWidget`

A replacement for `UButton` that is aware of the current input method (mouse, gamepad, touch) and can display platform-appropriate icons (e.g., "A button" on Xbox, "Cross" on PlayStation).

```cpp
// OnClicked returns FCommonButtonEvent (DECLARE_EVENT-based) — NOT a DYNAMIC delegate
// Use AddUObject or AddWeakLambda instead of AddDynamic
FCommonButtonEvent& OnClicked();

// Example binding in NativeOnActivated (remove in NativeOnDeactivated)
MyButton->OnClicked().AddUObject(this, &UMyScreen::HandleButtonClicked);
MyButton->OnClicked().RemoveAll(this);

// Enable/disable
MyButton->SetIsEnabled(false);

// Selected state (toggle-style buttons)
MyButton->SetIsSelected(true);
bool bSelected = MyButton->GetSelected();

// Hovering
MyButton->SetIsInteractionEnabled(true);
```

**Styling:** `UCommonButtonBase` uses a `UCommonButtonStyle` data asset instead of `FButtonStyle`. Configure this in the widget Blueprint.

---

### UCommonUIActionRouter

**Header:** Not typically subclassed — managed by the Common UI subsystem.

The action router manages which activatable widget receives input actions (confirm, cancel/back, etc.) based on the current activation tree. When `UCommonActivatableWidget::ActivateWidget()` is called, the widget registers as a node in the action routing tree. Input actions are routed to the leaf-most active node first.

**You rarely interact with `UCommonUIActionRouter` directly.** Instead, configure per-widget behavior via:
- `bIsBackHandler` on `UCommonActivatableWidget`
- `GetDesiredInputConfig()` override
- `InputMapping` (Enhanced Input context) on `UCommonActivatableWidget`

---

### UCommonInputSubsystem

Provides runtime information about the current input method and allows observing changes.

```cpp
// Get the subsystem
UCommonInputSubsystem* InputSubsystem = UCommonInputSubsystem::Get(GetOwningLocalPlayer());

// Query current input type
ECommonInputType CurrentType = InputSubsystem->GetCurrentInputType();
// ECommonInputType: None, MouseAndKeyboard, Gamepad, Touch

// Is gamepad active?
bool bGamepad = CurrentType == ECommonInputType::Gamepad;

// Observe input type changes
InputSubsystem->OnInputMethodChangedNative.AddUObject(
    this, &UMyWidget::HandleInputMethodChanged);

UFUNCTION()
void UMyWidget::HandleInputMethodChanged(ECommonInputType NewInputType)
{
    // Update cursor visibility, icon display, etc.
    bool bShowMouse = NewInputType == ECommonInputType::MouseAndKeyboard
                   || NewInputType == ECommonInputType::Touch;
    GetOwningPlayer()->SetShowMouseCursor(bShowMouse);
}
```

---

## Input Configuration

### FUIInputConfig

Returned from `UCommonActivatableWidget::GetDesiredInputConfig()` to define how input is handled while this widget is the active leaf.

```cpp
// Menu mode: gamepad navigates widgets, no mouse capture
return FUIInputConfig(ECommonInputMode::Menu, EMouseCaptureMode::NoCapture);

// Game mode: game receives all input
return FUIInputConfig(ECommonInputMode::Game, EMouseCaptureMode::CapturePermanently);

// All mode: both game and UI receive input (e.g., for HUD with tooltips)
return FUIInputConfig(ECommonInputMode::All, EMouseCaptureMode::NoCapture);
```

| `ECommonInputMode` | Description |
|---|---|
| `Menu` | Game input suspended. UI navigation active. |
| `Game` | Game receives input. UI does not route actions. |
| `All` | Both game and UI receive input simultaneously. |

### Enhanced Input Integration

`UCommonActivatableWidget` supports an `InputMapping` property for adding an `UInputMappingContext` while the widget is active:

```cpp
// Set in the widget's Blueprint defaults or C++ constructor:
UPROPERTY(EditAnywhere, Category="Input")
TObjectPtr<UInputMappingContext> InputMapping;

UPROPERTY(EditAnywhere, Category="Input")
int32 InputMappingPriority = 0;
```

The mapping context is added when `ActivateWidget()` is called and removed when `DeactivateWidget()` is called via `ActivateMappingContext()` / `DeactivateMappingContext()`.

---

## UI Layer Architecture Pattern

A typical Common UI hierarchy for a game with main menu, pause, and HUD:

```
AHUD or PlayerController
    └── URootUIWidget (UUserWidget, AddToViewport ZOrder=0)
            ├── UCommonActivatableWidgetStack "GameLayer"
            │       └── UMyHUDWidget (always active during gameplay)
            ├── UCommonActivatableWidgetStack "MenuLayer"
            │       ├── UMyMainMenuWidget
            │       ├── UMyOptionsScreen
            │       └── UMyPauseMenuWidget
            └── UCommonActivatableWidgetStack "ModalLayer"
                    └── UMyConfirmationDialog (modal, bIsModal=true)
```

**Implementation:**

```cpp
// URootUIWidget.h
UCLASS()
class MYGAME_API URootUIWidget : public UUserWidget
{
    GENERATED_BODY()

public:
    template<typename T>
    T* PushMenuWidget(TSubclassOf<T> WidgetClass)
    {
        return Cast<T>(MenuLayer->AddWidget(WidgetClass));
        // AddWidget creates, pushes, and activates the widget
    }

    void PopMenuWidget()
    {
        if (UCommonActivatableWidget* Active = MenuLayer->GetActiveWidget())
        {
            Active->DeactivateWidget();
        }
    }

protected:
    UPROPERTY(meta=(BindWidget))
    TObjectPtr<UCommonActivatableWidgetStack> GameLayer;

    UPROPERTY(meta=(BindWidget))
    TObjectPtr<UCommonActivatableWidgetStack> MenuLayer;

    UPROPERTY(meta=(BindWidget))
    TObjectPtr<UCommonActivatableWidgetStack> ModalLayer;
};
```

---

## Common UI Gamepad Navigation

Common UI provides automatic focus management for gamepad navigation. When a `UCommonActivatableWidget` activates:

1. `GetDesiredFocusTarget()` is called.
2. The returned widget receives Slate keyboard focus.
3. Directional pad / left stick navigates between focusable widgets automatically.
4. "Back" / B-button / Escape triggers the back action if `bIsBackHandler = true`.

**Focus target best practices:**

```cpp
UWidget* UMyMenuScreen::NativeGetDesiredFocusTarget() const
{
    // Return the first interactive widget in tab order
    // This is the widget that gets focus when the screen activates
    return FirstButton;
}
```

**Ensure your buttons are focusable:**

In `UCommonButtonBase` Blueprint defaults or via C++:
```cpp
// IsFocusable is true by default on UCommonButtonBase
// For standard UButton, explicitly set it:
MyButton->InitIsFocusable(true); // Call before Slate widget is constructed
```

---

## Common Mistakes

**Not removing the delegate binding when deactivated**
```cpp
// BAD: leaks bindings, fires after the screen is gone
void UMyScreen::NativeOnActivated() {
    MyButton->OnClicked().AddUObject(this, &UMyScreen::HandleClick);
    // Never removed!
}

// GOOD
void UMyScreen::NativeOnActivated() {
    MyButton->OnClicked().AddUObject(this, &UMyScreen::HandleClick);
}
void UMyScreen::NativeOnDeactivated() {
    MyButton->OnClicked().RemoveAll(this);
}
```

**Using AddDynamic with UCommonButtonBase::OnClicked()**
```cpp
// WRONG: OnClicked() returns FCommonButtonEvent, not a DYNAMIC delegate
MyButton->OnClicked().AddDynamic(this, &UMyScreen::HandleClick); // Compile error

// CORRECT
MyButton->OnClicked().AddUObject(this, &UMyScreen::HandleClick);
```

**Skipping the viewport client configuration**

Common UI's input method detection requires `UCommonGameViewportClient`. Without it, `UCommonInputSubsystem::GetCurrentInputType()` always returns `MouseAndKeyboard` on non-console platforms, and `UCommonButtonBase` icon display does not work.

**Mixing Common UI and raw SetInputMode calls**

Once Common UI is active, avoid calling `GetOwningPlayer()->SetInputMode(FInputModeUIOnly())`. Common UI manages input mode internally through `FUIInputConfig`. Direct calls bypass the activation tree and cause conflicts.

```cpp
// BAD with Common UI
GetOwningPlayer()->SetInputMode(FInputModeUIOnly());

// GOOD: return the config from the activatable widget
TOptional<FUIInputConfig> UMyScreen::GetDesiredInputConfig() const {
    return FUIInputConfig(ECommonInputMode::Menu, EMouseCaptureMode::NoCapture);
}
```

**Not calling Super in activation overrides**
```cpp
// REQUIRED — Super sets up internal state, delegates, and focus routing
void UMyScreen::NativeOnActivated() {
    Super::NativeOnActivated(); // Must be called
    // Your code
}
void UMyScreen::NativeOnDeactivated() {
    // Your cleanup
    Super::NativeOnDeactivated(); // Must be called
}
```

---

## Checklist: Adding a New Screen

1. Create a `UCommonActivatableWidget` subclass (C++ or BP).
2. In C++: override `NativeOnActivated`, `NativeOnDeactivated`, `NativeGetDesiredFocusTarget`, `GetDesiredInputConfig`.
3. In the UMG Blueprint: design the layout using `UCommonButtonBase` for all interactive buttons.
4. Set `bIsBackHandler = true` if this screen should close on Back/Escape/B-button.
5. Set `bAutoActivate = false` (default) unless you need activation on construction.
6. Push via the appropriate layer stack (game, menu, or modal).
7. Verify focus flows correctly on gamepad by testing `NativeGetDesiredFocusTarget`.
8. Verify `GetDesiredInputConfig` returns the correct `ECommonInputMode`.
