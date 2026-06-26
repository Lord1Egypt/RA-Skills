# Detail Customization Patterns

Reference for common `IDetailCustomization` and `IPropertyTypeCustomization` patterns with Slate widget examples. All patterns are based on the real UE source interfaces in `Engine/Source/Editor/PropertyEditor/Public/`.

---

## IDetailLayoutBuilder Key Methods

From `DetailLayoutBuilder.h` (`IDetailLayoutBuilder`):

```cpp
// Edit or create a category
IDetailCategoryBuilder& EditCategory(
    FName CategoryName,
    const FText& NewLocalizedDisplayName = FText::GetEmpty(),
    ECategoryPriority::Type CategoryType = ECategoryPriority::Default);

// Hide an entire category
void HideCategory(FName CategoryName);

// Get a property handle by member name — use GET_MEMBER_NAME_CHECKED for safety
TSharedRef<IPropertyHandle> GetProperty(
    const FName PropertyPath,
    const UStruct* ClassOutermost = nullptr,
    FName InstanceName = NAME_None) const;

// Hide a specific property
void HideProperty(const TSharedPtr<IPropertyHandle> PropertyHandle);

// Get the objects currently being customized
void GetObjectsBeingCustomized(TArray<TWeakObjectPtr<UObject>>& OutObjects) const;

// Force rebuild of the entire detail layout
void ForceRefreshDetails();

// Add a property to its auto-detected category (preserves original category)
IDetailPropertyRow& AddPropertyToCategory(TSharedPtr<IPropertyHandle> InPropertyHandle);
```

---

## Category Priority Reference

`ECategoryPriority` controls sort order in the details panel (lower value = higher position):

| Enum Value | Sort Position |
|---|---|
| `Variable` | Highest (top) |
| `Transform` | Near top |
| `Important` | High |
| `TypeSpecific` | Middle |
| `Default` | Standard |
| `Uncommon` | Bottom |

```cpp
IDetailCategoryBuilder& CoreCat =
    DetailBuilder.EditCategory("Core", FText::GetEmpty(), ECategoryPriority::Important);
IDetailCategoryBuilder& AdvancedCat =
    DetailBuilder.EditCategory("Advanced", FText::GetEmpty(), ECategoryPriority::Uncommon);
```

---

## IDetailPropertyRow — Fluent Modifier API

From `IDetailPropertyRow.h`. Methods return `IDetailPropertyRow&` for chaining:

```cpp
IDetailCategoryBuilder& Category = DetailBuilder.EditCategory("Settings");
IDetailPropertyRow& Row = Category.AddProperty(
    DetailBuilder.GetProperty(GET_MEMBER_NAME_CHECKED(UMyClass, MyFloat)));

Row.DisplayName(FText::FromString("Speed"))
   .ToolTip(FText::FromString("Movement speed in cm/s"))
   .ShowPropertyButtons(false)  // hide reset-to-default arrow
   .EditCondition(
       TAttribute<bool>::Create([this]() { return bIsEnabled; }),
       FOnBooleanValueChanged::CreateLambda([this](bool bNewValue)
       {
           bIsEnabled = bNewValue;
       })
   )
   .IsEnabled(TAttribute<bool>::Create([]() { return true; }))
   .Visibility(TAttribute<EVisibility>::Create([]()
   {
       return EVisibility::Visible;
   }));
```

---

## Custom Widget Row Patterns

### Full Custom Widget Row

```cpp
Category.AddCustomRow(FText::FromString("SearchFilter"))
[
    SNew(SHorizontalBox)
    + SHorizontalBox::Slot()
    .FillWidth(1.f)
    .VAlign(VAlign_Center)
    [
        SNew(STextBlock)
        .Text(FText::FromString("Custom Label"))
        .Font(IDetailLayoutBuilder::GetDetailFont())
    ]
    + SHorizontalBox::Slot()
    .AutoWidth()
    .Padding(FMargin(4.f, 0.f))
    [
        SNew(SButton)
        .Text(FText::FromString("Action"))
        .OnClicked(FOnClicked::CreateLambda([]()
        {
            return FReply::Handled();
        }))
    ]
];
```

### NameContent / ValueContent Split Row

The detail panel uses a two-column layout. Use `NameContent()` and `ValueContent()` to align with standard property rows:

```cpp
Category.AddCustomRow(FText::FromString("MyCustomProp"))
.NameContent()
[
    SNew(STextBlock)
    .Text(FText::FromString("Custom Property"))
    .Font(IDetailLayoutBuilder::GetDetailFont())
]
.ValueContent()
.MinDesiredWidth(125.f)
.MaxDesiredWidth(400.f)
[
    SNew(SEditableTextBox)
    .Text_Lambda([]() { return FText::FromString("value"); })
    .OnTextCommitted_Lambda([](const FText& NewText, ETextCommit::Type CommitType)
    {
        // handle commit
    })
];
```

### Override Default Property Widget While Keeping Children

```cpp
TSharedRef<IPropertyHandle> Handle =
    DetailBuilder.GetProperty(GET_MEMBER_NAME_CHECKED(UMyClass, MyProp));
IDetailPropertyRow& Row = Category.AddProperty(Handle);
TSharedPtr<SWidget> DefaultNameWidget;
TSharedPtr<SWidget> DefaultValueWidget;
Row.GetDefaultWidgets(DefaultNameWidget, DefaultValueWidget);

Row.CustomWidget(/*bShowChildren=*/true)
.NameContent()
[
    DefaultNameWidget.ToSharedRef()
]
.ValueContent()
[
    SNew(SHorizontalBox)
    + SHorizontalBox::Slot().FillWidth(1.f)
    [
        DefaultValueWidget.ToSharedRef()
    ]
    + SHorizontalBox::Slot().AutoWidth().Padding(4.f, 0.f)
    [
        SNew(SButton)
        .Text(FText::FromString("..."))
    ]
];
```

---

## IPropertyTypeCustomization — Struct Header Patterns

From `IPropertyTypeCustomization.h`. `CustomizeHeader` sets up the collapsed/inline row; `CustomizeChildren` sets up the expanded rows.

### Compact Inline Display

Show all struct fields inline in the header, no expansion needed:

```cpp
void FMyVectorCustomization::CustomizeHeader(
    TSharedRef<IPropertyHandle> PropertyHandle,
    FDetailWidgetRow& HeaderRow,
    IPropertyTypeCustomizationUtils& CustomizationUtils)
{
    // Get child handles for X, Y, Z
    TSharedPtr<IPropertyHandle> XHandle = PropertyHandle->GetChildHandle(
        GET_MEMBER_NAME_CHECKED(FMyVector, X));
    TSharedPtr<IPropertyHandle> YHandle = PropertyHandle->GetChildHandle(
        GET_MEMBER_NAME_CHECKED(FMyVector, Y));

    HeaderRow
    .NameContent()
    [
        PropertyHandle->CreatePropertyNameWidget()
    ]
    .ValueContent()
    .MinDesiredWidth(200.f)
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().Padding(2.f)
        [
            XHandle->CreatePropertyValueWidget()
        ]
        + SHorizontalBox::Slot().Padding(2.f)
        [
            YHandle->CreatePropertyValueWidget()
        ]
    ];
}

void FMyVectorCustomization::CustomizeChildren(
    TSharedRef<IPropertyHandle> PropertyHandle,
    IDetailChildrenBuilder& ChildBuilder,
    IPropertyTypeCustomizationUtils& CustomizationUtils)
{
    // Leave empty to suppress expanded child rows
}
```

### Summary Text in Header, Children in Expansion

```cpp
void FMyRangeCustomization::CustomizeHeader(
    TSharedRef<IPropertyHandle> PropertyHandle,
    FDetailWidgetRow& HeaderRow,
    IPropertyTypeCustomizationUtils& CustomizationUtils)
{
    TSharedPtr<IPropertyHandle> MinHandle =
        PropertyHandle->GetChildHandle(GET_MEMBER_NAME_CHECKED(FMyRange, Min));
    TSharedPtr<IPropertyHandle> MaxHandle =
        PropertyHandle->GetChildHandle(GET_MEMBER_NAME_CHECKED(FMyRange, Max));

    HeaderRow
    .NameContent()
    [
        PropertyHandle->CreatePropertyNameWidget()
    ]
    .ValueContent()
    [
        SNew(STextBlock)
        .Text_Lambda([MinHandle, MaxHandle]()
        {
            float MinVal = 0.f, MaxVal = 0.f;
            MinHandle->GetValue(MinVal);
            MaxHandle->GetValue(MaxVal);
            return FText::Format(
                FText::FromString("[{0} .. {1}]"),
                FText::AsNumber(MinVal),
                FText::AsNumber(MaxVal));
        })
        .Font(IPropertyTypeCustomizationUtils::GetRegularFont())
    ];
}

void FMyRangeCustomization::CustomizeChildren(
    TSharedRef<IPropertyHandle> PropertyHandle,
    IDetailChildrenBuilder& ChildBuilder,
    IPropertyTypeCustomizationUtils& CustomizationUtils)
{
    uint32 NumChildren = 0;
    PropertyHandle->GetNumChildren(NumChildren);
    for (uint32 i = 0; i < NumChildren; ++i)
    {
        ChildBuilder.AddProperty(PropertyHandle->GetChildHandle(i).ToSharedRef());
    }
}
```

---

## IPropertyHandle — Reading and Writing Values

`IPropertyHandle` provides type-safe access to property values across one or more selected objects:

```cpp
TSharedRef<IPropertyHandle> Handle =
    DetailBuilder.GetProperty(GET_MEMBER_NAME_CHECKED(UMyClass, Speed));

// Read
float SpeedValue = 0.f;
FPropertyAccess::Result Result = Handle->GetValue(SpeedValue);
if (Result == FPropertyAccess::MultipleValues)
{
    // multiple objects with different values selected
}

// Write — automatically handles transactions and PostEditChange
Handle->SetValue(150.f);

// Get as display string
FString DisplayStr;
Handle->GetValueAsDisplayString(DisplayStr);

// Enumerate per-object values
Handle->EnumerateRawData([](void* RawData, const int32 DataIndex, const int32 NumDatas) -> bool
{
    float* SpeedPtr = static_cast<float*>(RawData);
    *SpeedPtr = 100.f;
    return true;  // continue iteration
});

// Notify post-change
Handle->NotifyPostChange(EPropertyChangeType::ValueSet);
```

---

## Fonts

Always use `IDetailLayoutBuilder` or `IPropertyTypeCustomizationUtils` static helpers for fonts to stay visually consistent with the details panel:

```cpp
FAppStyle::GetFontStyle(TEXT("PropertyWindow.NormalFont"))   // regular body
FAppStyle::GetFontStyle(TEXT("PropertyWindow.BoldFont"))     // bold label
FAppStyle::GetFontStyle(TEXT("PropertyWindow.ItalicFont"))   // italic/dimmed

// Shorthand statics:
IDetailLayoutBuilder::GetDetailFont()
IDetailLayoutBuilder::GetDetailFontBold()
IDetailLayoutBuilder::GetDetailFontItalic()
IPropertyTypeCustomizationUtils::GetRegularFont()
IPropertyTypeCustomizationUtils::GetBoldFont()
```

---

## Registration Reference

All registrations go in `StartupModule`; all unregistrations in `ShutdownModule`.

```cpp
// In StartupModule
FPropertyEditorModule& PropertyModule =
    FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");

// Class customization
PropertyModule.RegisterCustomClassLayout(
    UMyClass::StaticClass()->GetFName(),
    FOnGetDetailCustomizationInstance::CreateStatic(
        &FMyClassCustomization::MakeInstance));

// Struct / property type customization
PropertyModule.RegisterCustomPropertyTypeLayout(
    FMyStruct::StaticStruct()->GetFName(),
    FOnGetPropertyTypeCustomizationInstance::CreateStatic(
        &FMyStructCustomization::MakeInstance));

// Notify the editor that customizations changed
PropertyModule.NotifyCustomizationModuleChanged();

// In ShutdownModule
if (FModuleManager::Get().IsModuleLoaded("PropertyEditor"))
{
    FPropertyEditorModule& PM =
        FModuleManager::GetModuleChecked<FPropertyEditorModule>("PropertyEditor");
    PM.UnregisterCustomClassLayout(UMyClass::StaticClass()->GetFName());
    PM.UnregisterCustomPropertyTypeLayout(FMyStruct::StaticStruct()->GetFName());
}
```

---

## Instanced Property Type Layout (Scoped)

Register a property type customization for a specific details panel instance only, not globally. Useful when you want different presentation in different contexts:

```cpp
void FMyClassCustomization::CustomizeDetails(IDetailLayoutBuilder& DetailBuilder)
{
    // Register a type customization only within this details panel
    DetailBuilder.RegisterInstancedCustomPropertyTypeLayout(
        FMyStruct::StaticStruct()->GetFName(),
        FOnGetPropertyTypeCustomizationInstance::CreateStatic(
            &FMyStructInContextCustomization::MakeInstance));
}
```

---

## Common Patterns Checklist

- Use `GET_MEMBER_NAME_CHECKED(ClassName, MemberName)` — compile-time property name validation
- Always store `TWeakPtr<IDetailLayoutBuilder>` if calling `ForceRefreshDetails()` asynchronously
- For `SNew` lambdas that reference `DetailBuilder`, capture by `TWeakPtr` to avoid dangling references
- Use `IDetailCategoryBuilder::AddProperty` for standard rows, `AddCustomRow` for fully custom Slate rows
- `bShowChildren = true` in `CustomWidget()` to show child properties while overriding the parent row's display
- Call `PropertyModule.NotifyCustomizationModuleChanged()` after registrations so any open detail panels refresh
