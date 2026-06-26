# Build.cs Complete Field Reference

This reference covers every significant `ModuleRules` property used in Unreal Engine's C# build scripts. All fields are set inside the constructor of a class that derives from `ModuleRules`.

---

## Class Structure

```csharp
using UnrealBuildTool;
using System.IO;             // for Path.Combine
using System.Collections.Generic;

public class MyModule : ModuleRules
{
    public MyModule(ReadOnlyTargetRules Target) : base(Target)
    {
        // All fields are set here
    }
}
```

`ReadOnlyTargetRules Target` gives you read access to everything about the build target: platform, configuration, build type, editor flag, etc.

---

## Dependency Fields

### PublicDependencyModuleNames

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "Core",           // FString, TArray, TMap, logging
    "CoreUObject",    // UObject, UClass, reflection
    "Engine",         // AActor, UWorld, UGameInstance
    "InputCore",      // FKey, EKeys — needed when using Enhanced Input
});
```

Adds modules whose **public headers** are re-exported through your own public headers. Any module that depends on yours will also inherit these include paths transitively.

Use this when a type from the dependency appears in:
- A parameter or return type in your public header
- A base class of a type declared in your public header
- A field in a UPROPERTY in your public header

### PrivateDependencyModuleNames

```csharp
PrivateDependencyModuleNames.AddRange(new string[]
{
    "Slate",          // SWidget, SCompoundWidget
    "SlateCore",      // FSlateColor, FSlateBrush
    "RenderCore",     // FRenderCommandFence
    "RHI",            // FRHITexture, FRHICommandList
    "Json",           // FJsonObject, FJsonSerializer
    "HTTP",           // FHttpModule, IHttpRequest
});
```

Adds modules used only inside `Private/` implementation files. These are not inherited by downstream modules. Prefer private for anything you can — it minimizes transitive compilation overhead.

### DynamicallyLoadedModuleNames

```csharp
DynamicallyLoadedModuleNames.AddRange(new string[]
{
    "OnlineSubsystem",
    "OnlineSubsystemSteam",
});
```

Tells UBT the module may be loaded at runtime via `FModuleManager::LoadModule()`, but does not create a compile-time link dependency. Use this when you load plugins or platform-specific backends conditionally.

---

## Include Path Fields

### PublicIncludePaths

```csharp
// Expose subdirectories to downstream modules
PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public", "Interfaces"));
PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public", "Subsystems"));
```

UBT automatically adds `ModuleDirectory/Public` — only add this when you have headers in subdirectories that downstream modules need to include without a path prefix.

### PrivateIncludePaths

```csharp
// Only visible inside this module
PrivateIncludePaths.Add(Path.Combine(ModuleDirectory, "Private", "Helpers"));
PrivateIncludePaths.Add(Path.Combine(ModuleDirectory, "Private", "Internal"));
```

Only accessible to this module's own source files.

### PublicSystemIncludePaths

```csharp
// For third-party C headers — suppresses warnings
PublicSystemIncludePaths.Add(Path.Combine(ThirdPartyPath, "include"));
```

Treated as system include paths. Compiler warnings are suppressed for headers in these paths.

### PrivateIncludePathModuleNames

```csharp
// Access headers from another module's Public/ without creating a link dependency
PrivateIncludePathModuleNames.AddRange(new string[] { "AssetRegistry" });
```

Adds include paths from a module without linking against it. Use when you only need type-forward declarations or data structures, not exported symbols.

---

## PCH Fields

### PCHUsage

```csharp
// UE5 default — IWYU, each file includes what it uses
PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

// Legacy — shared PCH, all files implicitly get engine types
PCHUsage = PCHUsageMode.UseSharedPCHs;

// No precompiled headers at all
PCHUsage = PCHUsageMode.NoPCHs;

// Each module uses its own private PCH (slower build, maximum isolation)
PCHUsage = PCHUsageMode.NoSharedPCHs;
```

Always use `UseExplicitOrSharedPCHs` for new UE5 modules.

### PrivatePCHHeaderFile

```csharp
// When you want to define your own PCH header
PrivatePCHHeaderFile = "Private/MyModulePCH.h";
```

Specifies a custom PCH for this module. The referenced file is compiled as the PCH and prepended to all translation units in the module.

### bEnforceIWYU

```csharp
// Enforce Include What You Use — each file must include every header it directly uses
bEnforceIWYU = true;
```

When true, UBT checks that no source file relies on transitive includes. Strongly recommended for new modules; required when `PCHUsage = UseExplicitOrSharedPCHs`.

---

## Compiler and Linker Flags

### bEnableExceptions

```csharp
// Enable C++ exception handling (try/catch/throw)
// Default: false — most UE code uses ensure/check/UE_LOG instead
bEnableExceptions = true;
```

Only enable when integrating third-party code that throws exceptions. UE's own code does not use exceptions.

### bUseRTTI

```csharp
// Enable runtime type information (typeid, dynamic_cast)
// Default: false
bUseRTTI = true;
```

Only enable when third-party code requires it. UE uses its own reflection system instead.

### bUseAVX

```csharp
// Allow AVX instruction set on supported platforms
bUseAVX = true;
```

### OptimizeCode

```csharp
// Force optimization on or off regardless of build configuration
OptimizeCode = CodeOptimization.Always;   // even in Debug
OptimizeCode = CodeOptimization.Never;    // even in Shipping (debugging)
OptimizeCode = CodeOptimization.Default;  // follow build config (normal)
```

### bDisableStaticAnalysis

```csharp
// Disable static analysis for this module (use sparingly)
bDisableStaticAnalysis = true;
```

### CppStandard

```csharp
// Override C++ standard for this module
CppStandard = CppStandardVersion.Cpp20;
CppStandard = CppStandardVersion.Cpp17;   // UE default
```

---

## Third-Party Libraries

### AddEngineThirdPartyPrivateStaticDependencies

```csharp
// Link a third-party static library shipped with the engine
AddEngineThirdPartyPrivateStaticDependencies(Target,
    "zlib",
    "OpenSSL",
    "libcurl"
);
```

This is the preferred way to consume engine-bundled third-party libraries. UBT looks up the library definition in `Engine/Source/ThirdParty/`.

### PublicAdditionalLibraries / PublicDelayLoadDLLs

```csharp
// Link against an external static library
PublicAdditionalLibraries.Add(Path.Combine(ThirdPartyDir, "Win64", "MyLib.lib"));

// Delay-load a DLL (Windows only)
PublicDelayLoadDLLs.Add("MyLib.dll");
RuntimeDependencies.Add(Path.Combine(ThirdPartyDir, "Win64", "MyLib.dll"));
```

### RuntimeDependencies

```csharp
// Copy files to the output directory when packaging
RuntimeDependencies.Add("$(PluginDir)/Binaries/Win64/MyLib.dll");
RuntimeDependencies.Add(new RuntimeDependency(
    Path.Combine(PluginDirectory, "Content", "MyData.bin")));
```

---

## Platform-Conditional Patterns

```csharp
public MyModule(ReadOnlyTargetRules Target) : base(Target)
{
    PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

    PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine" });

    // Editor-only dependencies
    if (Target.bBuildEditor)
    {
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "UnrealEd",
            "EditorFramework",
        });
    }

    // Platform-specific libraries
    if (Target.Platform == UnrealTargetPlatform.Win64)
    {
        PublicAdditionalLibraries.Add(Path.Combine(ModuleDirectory, "lib", "Win64", "MyLib.lib"));
        PublicDelayLoadDLLs.Add("MyLib.dll");
    }
    else if (Target.Platform == UnrealTargetPlatform.Mac)
    {
        PublicAdditionalLibraries.Add(Path.Combine(ModuleDirectory, "lib", "Mac", "libMyLib.a"));
    }

    // Development-only code
    if (Target.Configuration != UnrealTargetConfiguration.Shipping)
    {
        PrivateDependencyModuleNames.Add("EngineSettings");
        PublicDefinitions.Add("ENABLE_MY_DEBUG_FEATURES=1");
    }
    else
    {
        PublicDefinitions.Add("ENABLE_MY_DEBUG_FEATURES=0");
    }
}
```

### Target.Platform Values

| Value | Platform |
|---|---|
| `UnrealTargetPlatform.Win64` | Windows 64-bit |
| `UnrealTargetPlatform.Mac` | macOS |
| `UnrealTargetPlatform.Linux` | Linux |
| `UnrealTargetPlatform.IOS` | iOS |
| `UnrealTargetPlatform.Android` | Android |

### Target.Configuration Values

| Value | Description |
|---|---|
| `UnrealTargetConfiguration.Debug` | Full debug, no optimization |
| `UnrealTargetConfiguration.DebugGame` | Debug game code, optimized engine |
| `UnrealTargetConfiguration.Development` | Standard development build |
| `UnrealTargetConfiguration.Test` | Like Shipping, with some stats |
| `UnrealTargetConfiguration.Shipping` | Final release, stripped |

---

## Preprocessor Definitions

```csharp
// Add a preprocessor definition to all compilation units in this module
PublicDefinitions.Add("MY_FEATURE_ENABLED=1");

// Private definitions only visible inside this module
PrivateDefinitions.Add("INTERNAL_BUILD_VERSION=42");
```

---

## TargetRules Reference (Target.cs)

```csharp
public class MyGameTarget : TargetRules
{
    public MyGameTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;

        // Use latest UBT build settings (sets sensible defaults)
        DefaultBuildSettings = BuildSettingsVersion.Latest;

        // Use latest include order (required for IWYU with UE5)
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;

        // Modules UBT must compile for this target
        ExtraModuleNames.AddRange(new string[]
        {
            "MyGame",
            "MyGameCore",
        });

        // Disable unity builds for faster incremental iteration (slower full builds)
        bUseUnityBuild = false;

        // Enable link time code generation in Shipping
        bAllowLTCG = Target.Configuration == UnrealTargetConfiguration.Shipping;
    }
}
```

### TargetType Values

| Value | Executable type |
|---|---|
| `TargetType.Game` | Game client, no editor tooling |
| `TargetType.Editor` | Editor build, all editor modules included |
| `TargetType.Client` | Client-only, server code excluded |
| `TargetType.Server` | Server-only, renderer excluded |
| `TargetType.Program` | Standalone program (not a game) |

---

## Common Engine Module Reference

These are the modules you most often add as dependencies:

| Module | Provides |
|---|---|
| `Core` | `FString`, `TArray`, `TMap`, `FName`, `FText`, `UE_LOG`, `check`, `ensure` |
| `CoreUObject` | `UObject`, `UClass`, UPROPERTY/UFUNCTION reflection |
| `Engine` | `AActor`, `UWorld`, `UGameInstance`, `UActorComponent` |
| `InputCore` | `FKey`, `EKeys` |
| `EnhancedInput` | `UInputAction`, `UInputMappingContext` |
| `GameplayTags` | `FGameplayTag`, `FGameplayTagContainer` |
| `Slate` | `SWidget`, `SCompoundWidget`, `SWindow` |
| `SlateCore` | `FSlateColor`, `FSlateBrush`, `FGeometry` |
| `UMG` | `UUserWidget`, `UButton`, `UTextBlock` |
| `RenderCore` | `FRenderCommandFence`, render thread utilities |
| `RHI` | `FRHITexture`, `FRHICommandList`, GPU resources |
| `Json` | `FJsonObject`, `FJsonSerializer` |
| `HTTP` | `FHttpModule`, `IHttpRequest` |
| `AssetRegistry` | `IAssetRegistry`, `FAssetData` |
| `UnrealEd` | Editor subsystems, `UEditorEngine` (editor-only) |
| `EditorFramework` | `IToolkit`, toolkit base (editor-only) |
| `PropertyEditor` | Details panel customization (editor-only) |
| `DeveloperSettings` | `UDeveloperSettings` config objects |
| `NetCore` | Networking primitives |
| `OnlineSubsystem` | `IOnlineSubsystem`, sessions, leaderboards |
| `AIModule` | `UAIController`, `UBehaviorTree` |
| `NavigationSystem` | `UNavigationSystemV1`, pathfinding |
| `PhysicsCore` | Physics engine abstractions |
| `Chaos` | Chaos physics (UE5+ default) |

---

## API Macro Generation Rules

UBT generates the export macro by:
1. Taking the module's directory name
2. Converting to uppercase
3. Appending `_API`

Examples:
- Module directory `MyPlugin` → `MYPLUGIN_API`
- Module directory `MyPlugin_Runtime` → `MYPLUGIN_RUNTIME_API`
- Module directory `Core` → `CORE_API`
- Module directory `Engine` → `ENGINE_API`

The macro expands to `__declspec(dllexport)` on Windows or `__attribute__((visibility("default")))` on Linux/Mac in DLL builds, and to nothing in monolithic builds.
