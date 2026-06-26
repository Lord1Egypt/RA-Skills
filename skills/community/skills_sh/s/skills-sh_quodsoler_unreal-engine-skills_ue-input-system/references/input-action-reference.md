# Enhanced Input: Trigger and Modifier Reference

Complete reference for built-in `UInputTrigger` and `UInputModifier` classes.
All classes are in the `EnhancedInput` plugin module.
Source headers: `InputTriggers.h`, `InputModifiers.h`.

---

## UInputAction Properties

```cpp
class UInputAction : public UDataAsset
```

| Property | Type | Default | Description |
|---|---|---|---|
| `ValueType` | `EInputActionValueType` | `Boolean` | Shape of the value: `Boolean`, `Axis1D` (float), `Axis2D` (FVector2D), `Axis3D` (FVector) |
| `AccumulationBehavior` | `EInputActionAccumulationBehavior` | `TakeHighestAbsoluteValue` | How multiple mappings to the same action are combined |
| `bConsumeInput` | `bool` | `true` | If true, lower-priority Enhanced Input mappings to the same keys are blocked |
| `bConsumesActionAndAxisMappings` | `bool` | `false` | If true, legacy Action/Axis mappings to the same key are also blocked |
| `bReserveAllMappings` | `bool` | `false` | Mappings are not automatically overridden by higher-priority contexts |
| `bTriggerWhenPaused` | `bool` | `false` | Action fires even while game is paused |
| `Triggers` | `TArray<UInputTrigger*>` | empty | Action-level triggers; applied after per-mapping triggers |
| `Modifiers` | `TArray<UInputModifier*>` | empty | Action-level modifiers; applied after per-mapping modifiers |

### EInputActionAccumulationBehavior

| Value | Behavior |
|---|---|
| `TakeHighestAbsoluteValue` | The mapping with the highest absolute value wins. Pressing W (-0.3) and D (0.5) gives 0.5. |
| `Cumulative` | All mapping values are added. Pressing W (1.0) and S (-1.0) cancels to 0.0. Useful for WASD pairs. |

---

## FInputActionInstance (Runtime)

Available inside `FInputActionInstance` callbacks:

| Method | Returns | Description |
|---|---|---|
| `GetValue()` | `FInputActionValue` | Current value; zero when event is not `Triggered` |
| `GetTriggerEvent()` | `ETriggerEvent` | Current event state |
| `GetElapsedTime()` | `float` | Seconds since action began evaluating (Started + Ongoing + Triggered) |
| `GetTriggeredTime()` | `float` | Seconds the action has been in `Triggered` state only |
| `GetLastTriggeredWorldTime()` | `float` | World time of last trigger |
| `GetSourceAction()` | `const UInputAction*` | The originating action asset |

---

## ETriggerEvent

Bitmask enum. Represents state transitions observed in a single tick.

| Value | Bit | State Transition | Fires when |
|---|---|---|---|
| `None` | 0x00 | — | No significant transition, no active inputs |
| `Triggered` | 0x01 | None->Triggered, Ongoing->Triggered, Triggered->Triggered | Action is actively firing; also fires on the first triggered frame |
| `Started` | 0x02 | None->Ongoing, None->Triggered | First frame any input begins evaluation |
| `Ongoing` | 0x04 | Ongoing->Ongoing | Input is held and processing but trigger condition not yet met |
| `Canceled` | 0x08 | Ongoing->None | Evaluation began but was abandoned before triggering (e.g., held key released early) |
| `Completed` | 0x10 | Triggered->None | Trigger was active and has now ended |

`Completed` will not fire if any trigger on the same action reports `Ongoing` that frame.

---

## Trigger Classes

### ETriggerState (Internal)

Triggers return one of three states:

| State | Meaning |
|---|---|
| `None` | No conditions met |
| `Ongoing` | Conditions partially met; continue evaluating |
| `Triggered` | All conditions met; fire the action |

### ETriggerType (Multi-Trigger Evaluation)

| Type | Rule |
|---|---|
| `Explicit` | At least one Explicit trigger must be in Triggered state |
| `Implicit` | All Implicit triggers must be in Triggered state |
| `Blocker` | If blocking, prevents all other triggers from firing |

---

### UInputTriggerDown

```
DisplayName: "Down"
Class: UInputTriggerDown : public UInputTrigger
TriggerType: Explicit
SupportedEvents: Instant
```

**Behavior:** Fires `Triggered` every frame input magnitude exceeds `ActuationThreshold`.
This is the implicit default when an action has no triggers assigned.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude to consider the input actuated |

**Use for:** Continuous actions where you want firing as long as a key is held (before adding a proper trigger).

---

### UInputTriggerPressed

```
DisplayName: "Pressed"
Class: UInputTriggerPressed : public UInputTrigger
TriggerType: Explicit
SupportedEvents: Instant
```

**Behavior:** Fires `Triggered` exactly once on the first frame input exceeds `ActuationThreshold`.
Holding the input does not fire again. Re-press is required for another trigger.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude |

**Use for:** Discrete press-once actions: jump initiation, weapon fire on semi-auto, menu confirm.

---

### UInputTriggerReleased

```
DisplayName: "Released"
Class: UInputTriggerReleased : public UInputTrigger
TriggerType: Explicit
SupportedEvents: Instant
```

**Behavior:** Returns `Ongoing` while input exceeds `ActuationThreshold`. Fires `Triggered`
once when input drops back below the threshold after having been actuated.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ActuationThreshold` | `float` | `0.5` | Threshold |

**Use for:** Release-on-let-go: throwing after wind-up on a dedicated action, "lift to release" grenades.

---

### UInputTriggerHold

```
DisplayName: "Hold"
Class: UInputTriggerHold : public UInputTriggerTimedBase
TriggerType: Explicit
SupportedEvents: Ongoing (Started, Ongoing, Triggered, Canceled)
```

**Behavior:** Returns `Ongoing` while input is held. After `HoldTimeThreshold` seconds,
fires `Triggered`. If `bIsOneShot=false`, continues firing `Triggered` every frame.
If input is released before the threshold, fires `Canceled`.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `HoldTimeThreshold` | `float` | `1.0` | Seconds of continuous hold required |
| `bIsOneShot` | `bool` | `false` | If true, fires `Triggered` only once then stops; if false, fires every frame after threshold |
| `bAffectedByTimeDilation` | `bool` | `false` | Use actor time dilation when accumulating hold duration |
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude |

**Use for:** Hold-to-interact prompts, charged attacks where you need the `Ongoing` callback
to show a progress bar. Combine with `GetElapsedTime()` in the `Ongoing` handler.

**Example — charge bar:**
```cpp
void AMyCharacter::UpdateChargeBar(const FInputActionInstance& Instance)
{
    // Instance.GetElapsedTime() grows while key is held
    const float Progress = FMath::Clamp(
        Instance.GetElapsedTime() / HoldTrigger->HoldTimeThreshold, 0.f, 1.f);
    ChargeBarWidget->SetPercent(Progress);
}
```

---

### UInputTriggerHoldAndRelease

```
DisplayName: "Hold And Release"
Class: UInputTriggerHoldAndRelease : public UInputTriggerTimedBase
TriggerType: Explicit
SupportedEvents: Ongoing
```

**Behavior:** Returns `Ongoing` while input is held. Fires `Triggered` only when input
is released after having been held for at least `HoldTimeThreshold` seconds.
If released before the threshold, does not trigger.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `HoldTimeThreshold` | `float` | `0.5` | Minimum hold duration before release triggers |
| `bAffectedByTimeDilation` | `bool` | `false` | Use actor time dilation |
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude |

**Use for:** "Pull back and release" bows, charged throws where the shot fires on release.
Different from `UInputTriggerHold` in that the payload fires on release, not during hold.

---

### UInputTriggerTap

```
DisplayName: "Tap"
Class: UInputTriggerTap : public UInputTriggerTimedBase
TriggerType: Explicit
SupportedEvents: Instant
```

**Behavior:** Fires `Triggered` if input is actuated then released within
`TapReleaseTimeThreshold` seconds. Returns `Ongoing` while held within the window.
If held past the threshold without release, the trigger does not fire.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `TapReleaseTimeThreshold` | `float` | `0.2` | Max seconds between press and release to count as a tap |
| `bAffectedByTimeDilation` | `bool` | `false` | Use actor time dilation |
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude |

**Use for:** Quick-dash on tap (vs hold for a sustained dash). Combine with a separate
`UInputTriggerHold` on a second binding of the same key to distinguish tap vs hold.

---

### UInputTriggerRepeatedTap

```
DisplayName: "Repeated Tap"
Class: UInputTriggerRepeatedTap : public UInputTriggerTimedBase
TriggerType: Explicit
SupportedEvents: Instant
```

**Behavior:** Fires `Triggered` when the input is tapped `NumberOfTapsWhichTriggerRepeat`
times in succession, with each individual tap completing within `TapReleaseTimeThreshold`
and each gap between taps within `RepeatDelay` seconds.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `NumberOfTapsWhichTriggerRepeat` | `int32` | `2` | Number of rapid taps required to trigger |
| `RepeatDelay` | `double` | `0.5` | Max seconds allowed between consecutive taps |
| `TapReleaseTimeThreshold` | `float` | `0.2` | Max hold duration per tap |
| `bAffectedByTimeDilation` | `bool` | `false` | Use actor time dilation |

**Use for:** Double-tap dodge roll (`NumberOfTapsWhichTriggerRepeat=2`), triple-tap finisher.

---

### UInputTriggerPulse

```
DisplayName: "Pulse"
Class: UInputTriggerPulse : public UInputTriggerTimedBase
TriggerType: Explicit
SupportedEvents: Ongoing
```

**Behavior:** While input is held, fires `Triggered` at regular `Interval` second intervals.
If `bTriggerOnStart=true`, also fires immediately on the first actuation frame.
Stops after `TriggerLimit` fires if `TriggerLimit > 0`.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `bTriggerOnStart` | `bool` | `true` | Fire on the first frame of actuation before the first interval elapses |
| `Interval` | `float` | `1.0` | Seconds between successive triggers |
| `TriggerLimit` | `int32` | `0` | Maximum number of fires; 0 = unlimited |
| `bAffectedByTimeDilation` | `bool` | `false` | Use actor time dilation |
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude |

**Use for:** Automatic weapon fire rate, repeated ability pulses while holding a key,
tick-based resource drain.

---

### UInputTriggerChordAction

```
DisplayName: "Chorded Action"
Class: UInputTriggerChordAction : public UInputTrigger
TriggerType: Implicit
SupportedEvents: Instant
NotInputConfigurable: true (not exposed in per-mapping settings)
```

**Behavior:** This action only fires when `ChordAction` is simultaneously in `Triggered`
state. Automatically creates a `UInputTriggerChordBlocker` on `ChordAction` to prevent
the chord key from also firing solo actions while the chord is active.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ChordAction` | `const UInputAction*` | `nullptr` | The action that must be active at the same time |
| `ActuationThreshold` | `float` | `0.5` | Minimum magnitude |

**Setup pattern — Shift+E for special interact:**

1. Create `IA_Sprint` (Bool) bound to Shift in the IMC
2. Create `IA_SpecialInteract` (Bool) bound to E in the IMC
3. On `IA_SpecialInteract`, add a `UInputTriggerChordAction` with `ChordAction = IA_Sprint`
4. Result: E fires `IA_Interact`; Shift+E fires `IA_SpecialInteract`; E while Shift is held does NOT fire `IA_Interact`

---

### UInputTriggerCombo (Beta)

```
DisplayName: "Combo (Beta)"
Class: UInputTriggerCombo : public UInputTrigger
TriggerType: Implicit
SupportedEvents: All
NotInputConfigurable: true
```

**Behavior:** Fires when all `ComboActions` are completed in order. Each step must be
completed within its `TimeToPressKey` window after the previous step. The trigger fires
for one frame then resets. Actions in `InputCancelActions` abort the combo if triggered.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ComboActions` | `TArray<FInputComboStepData>` | empty | Ordered sequence of steps |
| `InputCancelActions` | `TArray<FInputCancelAction>` | empty | Actions that abort the combo |

**FInputComboStepData fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `ComboStepAction` | `const UInputAction*` | `nullptr` | The action for this step |
| `ComboStepCompletionStates` | `uint8` (bitmask of `ETriggerEvent`) | `Triggered` | Which events count as completing this step |
| `TimeToPressKey` | `float` | `0.5` | Seconds after previous step within which this step must complete |

**Use for:** Fighting game input sequences (Down, Down-Right, Right + Attack = Hadouken),
multi-step ability combos.

---

## Modifier Classes

### UInputModifierDeadZone

```
DisplayName: "Dead Zone"
Class: UInputModifierDeadZone : public UInputModifier
```

**Behavior:** Input values with magnitude below `LowerThreshold` are zeroed out.
Values are remapped from `[LowerThreshold, UpperThreshold]` to `[0, 1]`.
Values above `UpperThreshold` are clamped to 1.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `LowerThreshold` | `float` | `0.2` | Below this, input is zero |
| `UpperThreshold` | `float` | `1.0` | Above this, input is clamped to 1 |
| `Type` | `EDeadZoneType` | `Radial` | `Axial`: per-axis (chamfered corners); `Radial`: circular smooth; `UnscaledRadial`: circular, no smoothing |

**EDeadZoneType:**

| Value | Description |
|---|---|
| `Axial` | Dead zone applied independently per axis. Matches UE4 legacy behavior. Results in chamfered corners on 2D sticks. |
| `Radial` | Dead zone applied to the combined magnitude. Gives smooth circular coverage. Recommended for most sticks. |
| `UnscaledRadial` | Radial dead zone without the value smoothing. Can feel "jumpy" at the threshold boundary. |

**Use for:** All gamepad analog stick mappings. Add per-stick-mapping in the IMC, not on the action asset.

---

### UInputModifierScalar

```
DisplayName: "Scalar"
Class: UInputModifierScalar : public UInputModifier
```

**Behavior:** Multiplies each axis component of the input by the corresponding component
of `Scalar`. Has no effect on Boolean value types.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `Scalar` | `FVector` | `(1, 1, 1)` | Per-axis multiplier |

**Use for:** Mouse sensitivity scaling (`Scalar=(0.4, 0.4, 1.0)`), axis inversion without
using `Negate` (set component to -1.0), adjusting controller stick sensitivity.

---

### UInputModifierScaleByDeltaTime

```
DisplayName: "Scale By Delta Time"
Class: UInputModifierScaleByDeltaTime : public UInputModifier
```

**Behavior:** Multiplies the input value by the current frame's DeltaTime.
No configurable properties.

**Use for:** Making input frame-rate independent when feeding raw values into physics
or math that expects a per-second rate. Not typically needed for movement (AddMovementInput
already accounts for DeltaTime internally).

---

### UInputModifierNegate

```
DisplayName: "Negate"
Class: UInputModifierNegate : public UInputModifier
```

**Behavior:** Inverts selected axes by multiplying by -1.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `bX` | `bool` | `true` | Invert X axis |
| `bY` | `bool` | `true` | Invert Y axis |
| `bZ` | `bool` | `true` | Invert Z axis |

**Use for:** Y-axis inversion for "inverted look" options, negating the S and A keys in
WASD-to-2D composition.

**Common setup — invert Y only:**
Set `bX=false`, `bY=true`, `bZ=false`.

---

### UInputModifierSwizzleAxis

```
DisplayName: "Swizzle Input Axis Values"
Class: UInputModifierSwizzleAxis : public UInputModifier
```

**Behavior:** Reorders the X, Y, Z components of the input value according to `Order`.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `Order` | `EInputAxisSwizzle` | `YXZ` | How to reorder axes |

**EInputAxisSwizzle:**

| Value | Result | Description |
|---|---|---|
| `YXZ` | Output=(Y,X,Z) | Swap X and Y. Maps a 1D W/S key into the Y component of an Axis2D action. |
| `ZYX` | Output=(Z,Y,X) | Swap X and Z |
| `XZY` | Output=(X,Z,Y) | Swap Y and Z |
| `YZX` | Output=(Y,Z,X) | Rotate all axes Y-first |
| `ZXY` | Output=(Z,X,Y) | Rotate all axes Z-first |

**Use for:** The canonical WASD-to-Axis2D mapping. W produces a 1D value of 1.0 on X.
Adding `SwizzleAxis(YXZ)` converts it to Y=1.0, which is forward in the Axis2D Move action.

---

### UInputModifierSmooth

```
DisplayName: "Smooth"
Class: UInputModifierSmooth : public UInputModifier
```

**Behavior:** Averages the input value over recent samples to reduce per-frame jitter.
Uses a rolling average with `TotalSampleTime` as the accumulation window
(default ~8.3ms, i.e., roughly one frame at 120fps). Resets when input returns to zero.

No configurable public properties (sample window is a compile-time constant).

**Use for:** Smoothing raw mouse delta input for look controls. Add alongside `Scalar`
on mouse look mappings.

---

### UInputModifierSmoothDelta

```
DisplayName: "Smooth Delta"
Class: UInputModifierSmoothDelta : public UInputModifier
```

**Behavior:** Produces a smoothed normalized delta between the current and previous frame's
input value, using one of many configurable interpolation methods.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `SmoothingMethod` | `ENormalizeInputSmoothingType` | `Lerp` | Interpolation algorithm |
| `Speed` | `float` | `0.5` | Speed or alpha for the interpolation. If 0, jumps immediately to target. |
| `EasingExponent` | `float` | `2.0` | Degree of the ease curve; only for `Interp_Ease_*` methods |

**ENormalizeInputSmoothingType options:**
`Lerp`, `Interp_To`, `Interp_Constant_To`, `Interp_Circular_In/Out/In_Out`,
`Interp_Ease_In/Out/In_Out`, `Interp_Expo_In/Out/In_Out`, `Interp_Sin_In/Out/In_Out`

**Use for:** Smooth acceleration/deceleration on stick or mouse input where you want
to author the feel curve precisely.

---

### UInputModifierResponseCurveExponential

```
DisplayName: "Response Curve - Exponential"
Class: UInputModifierResponseCurveExponential : public UInputModifier
```

**Behavior:** Applies `sign(x) * |x|^CurveExponent` per axis, creating a non-linear
response. Values below 1 create a "softer" near-center feel; values above 1 create a
"harder" aggressive feel.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `CurveExponent` | `FVector` | `(1, 1, 1)` | Exponent per axis. 1.0 = linear. 2.0 = squared. |

**Use for:** Analog stick look sensitivity curves — a squared or cubed response gives
fine control near center with fast movement at the edges.

---

### UInputModifierResponseCurveUser

```
DisplayName: "Response Curve - User Defined"
Class: UInputModifierResponseCurveUser : public UInputModifier
```

**Behavior:** Applies separate `UCurveFloat` assets per axis, evaluating each curve with
the current axis value as input. Gives full artist control over the response shape.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `ResponseX` | `UCurveFloat*` | `nullptr` | Curve for the X axis |
| `ResponseY` | `UCurveFloat*` | `nullptr` | Curve for the Y axis |
| `ResponseZ` | `UCurveFloat*` | `nullptr` | Curve for the Z axis |

**Use for:** Precise feel tuning with a visible curve asset. Preferred over
`ResponseCurveExponential` when the exact shape matters and needs iteration in the
Curve Editor.

---

### UInputModifierFOVScaling

```
DisplayName: "FOV Scaling"
Class: UInputModifierFOVScaling : public UInputModifier
```

**Behavior:** Scales the mouse look input value by the current camera FOV, maintaining
a consistent angular displacement per mouse unit regardless of zoom level.

**Properties:**

| Property | Type | Default | Description |
|---|---|---|---|
| `FOVScale` | `float` | `1.0` | Additional scalar applied on top of the FOV calculation |
| `FOVScalingType` | `EFOVScalingType` | `Standard` | `Standard` = correct; `UE4_BackCompat` = legacy incorrect calculation for migration |

**Use for:** Mouse look on any character with a zoom/aim-down-sights mechanic.
Without this, zoomed-in aim feels faster than unzoomed aim in terms of screen pixels.

---

### UInputModifierToWorldSpace

```
DisplayName: "To World Space"
Class: UInputModifierToWorldSpace : public UInputModifier
```

**Behavior:** Converts a 2D axis input into world space. The up/down axis maps to world
forward (X), and left/right maps to world right (Y). Allows the value to be passed
directly to `AddMovementInput` or similar world-space functions without manual conversion.

No configurable properties.

**Use for:** Simplifying movement handler code when you want to receive a world-space
direction directly from the callback rather than rotating by the actor's facing.

---

## Modifier Execution Order

Modifiers are applied in this sequence:

1. Per-mapping modifiers (defined on each `FEnhancedActionKeyMapping` in the IMC)
2. Action-level modifiers (defined on the `UInputAction` asset `Modifiers` array)

Within each group, modifiers execute in array order. The output of modifier N is the
input to modifier N+1.

**Typical keyboard+mouse stack for a look action:**
```
Mapping modifiers: [Scalar(0.4, 0.4, 1.0), Smooth, FOVScaling]
Action modifiers:  [] (none needed at action level)
```

**Typical gamepad stick move action:**
```
Mapping modifiers: [DeadZone(Radial, 0.2, 1.0), SwizzleAxis(YXZ)]  // for W/S keys
Mapping modifiers: [DeadZone(Radial, 0.2, 1.0)]                     // for D/A keys
Action modifiers:  []
```

---

## Custom Trigger Interface

Override in a `UInputTrigger` subclass:

| Virtual Method | Signature | Description |
|---|---|---|
| `UpdateState_Implementation` | `ETriggerState(const UEnhancedPlayerInput*, FInputActionValue, float DeltaTime)` | Core per-tick evaluation; return None/Ongoing/Triggered |
| `GetTriggerType_Implementation` | `ETriggerType()` | Return Explicit, Implicit, or Blocker |
| `GetSupportedTriggerEvents` | `ETriggerEventsSupported()` | Declare which ETriggerEvent types this trigger can produce |
| `IsBlocking` | `bool(ETriggerState)` | Return true to block all other triggers (used by ChordBlocker) |
| `GetDebugState` | `FString()` | Text shown in `ShowDebug EnhancedInput` HUD |

`UInputTrigger::IsActuated(const FInputActionValue&)` helper:
Returns `true` if `Value.GetMagnitudeSq() >= ActuationThreshold * ActuationThreshold`.

`UInputTriggerTimedBase` base class provides:
- `HeldDuration` — accumulated time while actuated
- `CalculateHeldDuration(PlayerInput, DeltaTime)` — increments with optional time dilation
- Automatically transitions to `Ongoing` on first actuation

---

## Custom Modifier Interface

Override in a `UInputModifier` subclass:

| Virtual Method | Signature | Description |
|---|---|---|
| `ModifyRaw_Implementation` | `FInputActionValue(const UEnhancedPlayerInput*, FInputActionValue CurrentValue, float DeltaTime)` | Transform and return the modified value |
| `GetVisualizationColor_Implementation` | `FLinearColor(FInputActionValue Sample, FInputActionValue Final)` | Color used in debug visualization overlays |

The returned `FInputActionValue` will be cast back to the action's `ValueType` before
further processing, so you can return any type internally.

---

## UInputMappingContext Properties

```cpp
class UInputMappingContext : public UDataAsset
```

| Property / Method | Type | Description |
|---|---|---|
| `DefaultKeyMappings.Mappings` | `TArray<FEnhancedActionKeyMapping>` | Default key-to-action bindings (deprecated in 5.7 — use `GetMappings()` accessor) |
| `MappingProfileOverrides` | `TMap<FString, FInputMappingContextMappingData>` | Per-profile key overrides (for rebinding profiles) |
| `RegistrationTrackingMode` | `EMappingContextRegistrationTrackingMode` | `Untracked` or `CountRegistrations` |
| `InputModeFilterOptions` | `EMappingContextInputModeFilterOptions` | `UseProjectDefaultQuery`, `UseCustomQuery`, `DoNotFilter` |
| `GetMappings()` | `const TArray<FEnhancedActionKeyMapping>&` | Accessor for default mappings |
| `MapKey(Action, Key)` | `FEnhancedActionKeyMapping&` | Editor-time: add a key binding |
| `UnmapKey(Action, Key)` | `void` | Editor-time: remove a key binding |
| `HasMappingForInputAction(Action)` | `bool` | Returns true if action appears in this IMC |

### EMappingContextRegistrationTrackingMode

| Value | Behavior |
|---|---|
| `Untracked` | First `RemoveMappingContext` call removes the IMC regardless of how many times it was added |
| `CountRegistrations` | IMC stays active until `RemoveMappingContext` is called the same number of times as `AddMappingContext`. Useful when multiple subsystems share an IMC. |

---

## UEnhancedInputLocalPlayerSubsystem API

```cpp
// Add a context (BeginPlay or on mode change)
Subsystem->AddMappingContext(IMC, Priority, Options);

// Remove a context (on mode change, unpossess)
Subsystem->RemoveMappingContext(IMC, Options);

// Remove all contexts
Subsystem->ClearAllMappings();

// Check if a context is currently active
Subsystem->HasMappingContext(IMC);

// Query current value of an action without a binding
Subsystem->GetPlayerInput()->GetActionValue(InputAction);
```

**FModifyContextOptions:**

| Field | Type | Default | Description |
|---|---|---|---|
| `bIgnoreAllPressedKeysUntilRelease` | `bool` | `true` | Prevents "stuck key" ghost inputs when switching contexts while a key is held |
| `bForceImmediately` | `bool` | `false` | Rebuild mapping caches immediately rather than deferring to end of frame |
| `bNotifyUserSettings` | `bool` | `false` | Notify `UEnhancedInputUserSettings` of the change (for rebinding UI) |
