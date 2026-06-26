# Automation Test Patterns

Reference for common Unreal Engine automation test setups, latent command patterns, and scenario recipes. All patterns use the real API from `Misc/AutomationTest.h`.

---

## Test Module Setup

### Build Rules

```csharp
// MyGameTests.Build.cs
public class MyGameTests : ModuleRules
{
    public MyGameTests(ReadOnlyTargetRules Target) : base(Target)
    {
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "AutomationController",
            "MyGame",           // the module being tested
        });

        // Include editor-only dependencies when running in Editor context
        if (Target.bBuildEditor)
        {
            PrivateDependencyModuleNames.Add("UnrealEd");
        }
    }
}
```

### Target File Inclusion

```csharp
// MyGameEditor.Target.cs  (editor target — tests run here)
ExtraModuleNames.Add("MyGameTests");

// MyGame.Target.cs  (game target — tests excluded unless bWithAutomationTests)
if (bWithAutomationTests)
{
    ExtraModuleNames.Add("MyGameTests");
}
```

### Naming Convention

```
MyGame.Category.SubCategory.TestName

Examples:
  MyGame.Inventory.AddItem
  MyGame.Inventory.RemoveItem
  MyGame.Inventory.Overflow
  MyGame.Pathfinding.SimpleGrid
  MyGame.Pathfinding.ObstacleDense
  MyGame.Assets.PrimaryWeaponLoad
```

The dot-separated path creates a tree in the Session Frontend Automation tab.

---

## Pattern: Pure Logic Test (No World)

For testing stateless utility functions and pure C++ classes.

```cpp
#include "Misc/AutomationTest.h"
#include "MyMath.h"   // the unit under test

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FMyMathLerpTest,
    "MyGame.Math.LerpClamped",
    EAutomationTestFlags::EditorContext |
    EAutomationTestFlags::SmokeFilter)   // SmokeFilter = fast, runs every check-in

bool FMyMathLerpTest::RunTest(const FString& Parameters)
{
    TestEqual(TEXT("Lerp at 0"),   MyMath::LerpClamped(0.f, 10.f, 0.f), 0.f,  0.001f);
    TestEqual(TEXT("Lerp at 1"),   MyMath::LerpClamped(0.f, 10.f, 1.f), 10.f, 0.001f);
    TestEqual(TEXT("Lerp at 0.5"), MyMath::LerpClamped(0.f, 10.f, 0.5f), 5.f, 0.001f);
    // Clamped: alpha outside [0,1] saturates
    TestEqual(TEXT("Lerp above 1"), MyMath::LerpClamped(0.f, 10.f, 2.f), 10.f, 0.001f);
    TestEqual(TEXT("Lerp below 0"), MyMath::LerpClamped(0.f, 10.f, -1.f), 0.f, 0.001f);
    return true;
}
```

---

## Pattern: UObject Test (Requires GC)

For testing `UObject`-derived classes. `NewObject<>` requires a valid outer.

```cpp
#include "Misc/AutomationTest.h"
#include "Engine/Engine.h"
#include "Inventory/InventoryComponent.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FInventoryComponentTest,
    "MyGame.Inventory.AddRemove",
    EAutomationTestFlags::EditorContext |
    EAutomationTestFlags::ProductFilter)

bool FInventoryComponentTest::RunTest(const FString& Parameters)
{
    // Use GetTransientPackage() as outer for test UObjects
    UInventoryComponent* Inv = NewObject<UInventoryComponent>(GetTransientPackage());
    if (!TestNotNull(TEXT("Inventory created"), Inv)) { return false; }

    Inv->AddItem(FName("Sword"), 3);
    TestEqual(TEXT("Count after add"), Inv->GetCount(FName("Sword")), 3);

    Inv->RemoveItem(FName("Sword"), 1);
    TestEqual(TEXT("Count after remove"), Inv->GetCount(FName("Sword")), 2);

    Inv->RemoveItem(FName("Sword"), 99);  // over-remove
    TestEqual(TEXT("Count clamped at 0"), Inv->GetCount(FName("Sword")), 0);

    // TestValid works on TWeakObjectPtr and IsValid()-capable types
    TWeakObjectPtr<UInventoryComponent> WeakInv(Inv);
    TestValid(TEXT("Weak ref valid"), WeakInv);

    return true;
}
```

---

## Pattern: Parameterized Test Over Asset Paths

```cpp
IMPLEMENT_COMPLEX_AUTOMATION_TEST(
    FDataAssetValidation,
    "MyGame.Assets.DataAssetValidation",
    EAutomationTestFlags::EditorContext |
    EAutomationTestFlags::ProductFilter)

void FDataAssetValidation::GetTests(TArray<FString>& OutBeautifiedNames,
                                     TArray<FString>& OutTestCommands) const
{
    // Enumerate assets at editor time
    FAssetRegistryModule& AR = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
    TArray<FAssetData> Assets;
    AR.Get().GetAssetsByClass(UMyItemData::StaticClass()->GetClassPathName(), Assets);

    for (const FAssetData& Asset : Assets)
    {
        OutBeautifiedNames.Add(Asset.AssetName.ToString());
        OutTestCommands.Add(Asset.GetObjectPathString());
    }
}

bool FDataAssetValidation::RunTest(const FString& Parameters)
{
    // Parameters = the object path string from OutTestCommands
    UMyItemData* ItemData = LoadObject<UMyItemData>(nullptr, *Parameters);
    UE_RETURN_ON_ERROR(ItemData != nullptr,
        FString::Printf(TEXT("Failed to load %s"), *Parameters));

    TestFalse(TEXT("DisplayName not empty"),
              ItemData->DisplayName.IsEmpty());
    TestTrue(TEXT("MaxStack > 0"),
             ItemData->MaxStack > 0);
    TestNotNull(TEXT("Icon set"), ItemData->Icon.LoadSynchronous());

    return true;
}
```

---

## Pattern: Expected Error / Negative Test

Use `AddExpectedMessage` to suppress and verify expected error log output.

```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FInventoryOverflowNegativeTest,
    "MyGame.Inventory.OverflowRejectsItem",
    EAutomationTestFlags::EditorContext |
    EAutomationTestFlags::ProductFilter |
    EAutomationTestFlags::NegativeFilter)

bool FInventoryOverflowNegativeTest::RunTest(const FString& Parameters)
{
    // Tell the framework to expect (and suppress) this warning
    AddExpectedMessage(TEXT("Inventory is full"),
                       ELogVerbosity::Warning,
                       EAutomationExpectedMessageFlags::Contains);

    UInventoryComponent* Inv = NewObject<UInventoryComponent>(GetTransientPackage());
    Inv->SetMaxSlots(1);
    Inv->AddItem(FName("Sword"), 1);   // fills the slot

    // This should log "Inventory is full" and return false
    bool bAdded = Inv->AddItem(FName("Shield"), 1);
    TestFalse(TEXT("Second item rejected"), bAdded);

    return true;
}
```

---

## Pattern: Latent Command — Wait for Delegate

```cpp
#include "Misc/AutomationTest.h"

// Command that waits until a shared bool flag is set
DEFINE_LATENT_AUTOMATION_COMMAND_ONE_PARAMETER(
    FWaitForBoolCommand, TSharedPtr<bool>, bDone);

bool FWaitForBoolCommand::Update()
{
    return bDone.IsValid() && *bDone;
}

// Command with timeout
DEFINE_LATENT_AUTOMATION_COMMAND_TWO_PARAMETER(
    FWaitForBoolOrTimeoutCommand, TSharedPtr<bool>, bDone, float, Timeout);

bool FWaitForBoolOrTimeoutCommand::Update()
{
    if (bDone.IsValid() && *bDone) { return true; }
    if (GetCurrentRunTime() > Timeout)
    {
        // Logging in a latent command does NOT add a test error automatically
        // Store the test ref if you need to call AddError
        return true;  // done (timed out)
    }
    return false;
}

// Usage inside a test
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FAsyncOperationTest,
    "MyGame.Async.SubsystemReady",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FAsyncOperationTest::RunTest(const FString& Parameters)
{
    TSharedPtr<bool> bReady = MakeShared<bool>(false);

    // Kick off async work, flip bReady when done
    UMySubsystem* Sub = GEngine->GetEngineSubsystem<UMySubsystem>();
    if (!TestNotNull(TEXT("Subsystem"), Sub)) { return false; }

    Sub->InitAsync([bReady]() { *bReady = true; });

    // Wait up to 5 seconds
    ADD_LATENT_AUTOMATION_COMMAND(FWaitForBoolOrTimeoutCommand(bReady, 5.0f));

    // Latent commands run after RunTest returns; assertions here run immediately
    // For post-async assertions, use a custom latent command that captures the test ptr
    return true;
}
```

---

## Pattern: Latent Command — Validate After Async

To make assertions after async work, capture the test reference in the latent command.

```cpp
class FValidateAfterAsyncCommand : public IAutomationLatentCommand
{
public:
    FValidateAfterAsyncCommand(FAutomationTestBase* InTest,
                                TSharedPtr<bool> InbDone,
                                TSharedPtr<int32> InResult)
        : Test(InTest), bDone(InbDone), Result(InResult) {}

    virtual bool Update() override
    {
        if (!bDone.IsValid() || !*bDone) { return false; }
        Test->TestEqual(TEXT("Async result"), *Result, 42);
        return true;
    }

private:
    FAutomationTestBase* Test;
    TSharedPtr<bool> bDone;
    TSharedPtr<int32> Result;
};

// In RunTest:
bool FMyAsyncCalcTest::RunTest(const FString& Parameters)
{
    auto bDone   = MakeShared<bool>(false);
    auto Result  = MakeShared<int32>(0);

    UMyCalc::RunAsync([bDone, Result](int32 Val)
    {
        *Result = Val;
        *bDone  = true;
    });

    ADD_LATENT_AUTOMATION_COMMAND(FValidateAfterAsyncCommand(this, bDone, Result));
    return true;
}
```

---

## Running Tests

### Session Frontend (Editor)

1. Open **Window > Session Frontend > Automation**.
2. Connect to the local session.
3. Filter by name or flags; check boxes and click **Start Tests**.

### Command Line (Unattended)

```bash
# Run all tests matching a name filter, exit when done
UnrealEditor-Cmd MyGame -ExecCmds="Automation RunTests MyGame.Inventory" \
    -unattended -nopause -testexit="Automation Test Queue Empty" \
    -log -abslog=TestOutput.log

# Run smoke tests only
UnrealEditor-Cmd MyGame \
    -ExecCmds="Automation RunFilter Smoke" \
    -unattended -nopause -testexit="Automation Test Queue Empty"
```

### Programmatic (C++ / Python)

```python
# Inside Editor Python (via Editor Python Plugin)
import unreal
subsystem = unreal.get_editor_subsystem(unreal.AutomationControllerManager)
# Use Automation Controller API to queue and run tests
```

---

## Context Stack for Test Grouping

Use `PushContext` / `PopContext` to annotate which sub-step caused a failure.

```cpp
bool FMyComplexTest::RunTest(const FString& Parameters)
{
    ExecutionInfo.PushContext(TEXT("Phase 1: Setup"));
    // ... setup assertions
    ExecutionInfo.PopContext();

    ExecutionInfo.PushContext(TEXT("Phase 2: Execute"));
    // ... execute assertions
    ExecutionInfo.PopContext();

    return true;
}
```

Errors recorded while a context is active will include the context string in the failure report.

---

## Test Telemetry

Report numeric measurements alongside test results (captured by automation infrastructure):

```cpp
bool FMyPerfTest::RunTest(const FString& Parameters)
{
    double StartTime = FPlatformTime::Seconds();
    // ... operation
    double Duration = FPlatformTime::Seconds() - StartTime;

    // Reports DataPoint="SpawnTime", Measurement=Duration to telemetry
    // ExecutionInfo.TelemetryStorage = TEXT("MyGamePerf");
    // ExecutionInfo.TelemetryItems.Emplace(TEXT("SpawnTime"), Duration, TEXT("ms"));
    FAutomationTestFramework::Get().AddAnalyticsItemToCurrentTest(
        FString::Printf(TEXT("SpawnTime=%.2fms"), Duration * 1000.0));

    return true;
}
```
