# bUnit Setup for Syncfusion Blazor Components

> **Applies to:** Syncfusion Blazor Components  
> **Framework:** .NET 8+ with Blazor  
> **Testing Frameworks:** xUnit & NUnit  
> **Reference:** [Official Syncfusion Documentation](https://blazor.syncfusion.com/documentation/common/how-to/configure-blazor-component-in-bunit-testing)


## Overview

bUnit is a testing library for Blazor components. This guide covers configuring Syncfusion Blazor components for unit testing using bUnit with both xUnit and NUnit test frameworks.


## Table of Contents

1. [Configure bUnit with xUnit Test Project](#configure-bunit-with-xunit-test-project)
2. [Configure bUnit with NUnit Test Project](#configure-bunit-with-nunit-test-project)
3. [Passing Parameters to Blazor Components](#passing-parameters-to-blazor-components)
4. [Common Setup Patterns](#common-setup-patterns)

---

## Configure bUnit with xUnit Test Project

### Create xUnit Test Project

1. Open Visual Studio 2022 and create a new **xUnit Test Project**
2. Specify the project name and click **Next**
3. Select the target framework and click **Create**
4. Right-click the project in Solution Explorer and select **Manage NuGet Packages**
5. Search for `bunit` and install both NuGet packages in the test project:
   - `bunit`

### Add Existing Blazor App and Configure it on xUnit Project

1. Right-click the solution and select **Add → Existing Project**
2. Browse and add your existing Blazor project
3. Right-click the xUnit project and select **Add → Project Reference**, then select the added project
4. Add a Syncfusion Button sample to your Blazor project (`~/Pages/Home.razor` or `~/Pages/Index.razor`):

```razor
@using Syncfusion.Blazor.Buttons

<SfButton @onclick="OnButtonClick">My Button</SfButton>

<span class="alert alert-info">Count: @clickCount</span>

@code {
    private int clickCount = 0;

    [Parameter]
    public int Step { get; set; } = 1;

    private void OnButtonClick()
    {
        clickCount += Step;
    }
}
```

5. Add the following bUnit test cases in `~/UnitTest1.cs` on the xUnit project:

> **Note:** Replace `{Your App namespace}` with your actual project namespace (e.g., `MyBlazorApp`).

```csharp
using Xunit;
using Bunit;
using {Your App namespace}.Pages;
using Syncfusion.Blazor;
using Syncfusion.Blazor.Buttons;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace BlazorXUnitTesting
{
    public class UnitTest1
    {
        [Fact]
        public void TestIndex()
        {
            using var testContext = new TestContext();

            // Add Syncfusion Blazor service.
            testContext.Services.AddSyncfusionBlazor()
                .Replace(ServiceDescriptor.Transient<IComponentActivator, SfComponentActivator>());
            testContext.Services.AddOptions();

            // Rendering application Home component (~/Pages/Home.razor).
            var indexComponent = testContext.RenderComponent<Home>();
            
            // Find Syncfusion Button component.
            var sfButton = indexComponent.FindComponent<SfButton>();
            
            // Find span element.
            var span = indexComponent.Find("span.alert.alert-info");

            // Assert
            // Testing span element markup.
            span.MarkupMatches("<span class=\"alert alert-info\">Count: 0</span>");

            // Click Syncfusion Button component.
            sfButton.Find(".e-btn").Click();

            // Testing span element markup again.
            span.MarkupMatches("<span class=\"alert alert-info\">Count: 1</span>");
        }
    }
}
```

6. Right-click the xUnit project and select **Run Tests**. The test cases run and report the results.

---

## Configure bUnit with NUnit Test Project

### Create NUnit Test Project

1. Open Visual Studio 2022 and create a new **NUnit 3 Test Project**
2. Specify the project name and click **Next**
3. Select the target framework and click **Create**
4. Right-click the project in Solution Explorer and select **Manage NuGet Packages**
5. Search for `bunit` and install both NuGet packages in the test project:
   - `bunit`

### Add Existing Blazor App and Configure it on NUnit Project

1. Right-click the solution and select **Add → Existing Project**
2. Browse and add your existing Blazor project
3. Right-click the NUnit project and select **Add → Project Reference**, then select the added project
4. Add a Syncfusion Button sample to your Blazor project (`~/Pages/Home.razor` or `~/Pages/Index.razor`):

```razor
@using Syncfusion.Blazor.Buttons

<SfButton @onclick="OnButtonClick">My Button</SfButton>

<span class="alert alert-info">Count: @clickCount</span>

@code {
    private int clickCount = 0;

    [Parameter]
    public int Step { get; set; } = 1;

    private void OnButtonClick()
    {
        clickCount += Step;
    }
}
```

5. Add the following bUnit test cases in `~/UnitTest1.cs` on the NUnit project:

> **Note:** Replace `{Your App namespace}` with your actual project namespace (e.g., `MyBlazorApp`).

```csharp
using Bunit;
using NUnit.Framework;
using {Your App namespace}.Pages;
using Syncfusion.Blazor;
using Syncfusion.Blazor.Buttons;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace BlazorNUnitTesting
{
    public class Tests
    {
        [Test]
        public void TestIndex()
        {
            // Arrange
            using var testContext = new Bunit.TestContext();

            // Add Syncfusion Blazor service.
            testContext.Services.AddSyncfusionBlazor()
                .Replace(ServiceDescriptor.Transient<IComponentActivator, SfComponentActivator>());
            testContext.Services.AddOptions();

            // Rendering application Home component (~/Pages/Home.razor).
            var indexComponent = testContext.RenderComponent<Home>();
            
            // Find Syncfusion Button component.
            var sfButton = indexComponent.FindComponent<SfButton>();
            
            // Find span element.
            var span = indexComponent.Find("span.alert.alert-info");

            // Assert
            // Testing span element markup.
            span.MarkupMatches("<span class=\"alert alert-info\">Count: 0</span>");

            // Click Syncfusion Button component.
            sfButton.Find(".e-btn").Click();

            // Testing span element markup again.
            span.MarkupMatches("<span class=\"alert alert-info\">Count: 1</span>");
        }
    }
}
```

6. Right-click the NUnit project and select **Run Tests**. The test cases run and report the results.

---

## Passing Parameters to Blazor Components

Set component parameters using the `SetParametersAndRender` method:

```csharp
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.DependencyInjection.Extensions;

[Fact]
public void TestParameter()
{
    using var testContext = new TestContext();

    // Add Syncfusion Blazor service.
    testContext.Services.AddSyncfusionBlazor()
        .Replace(ServiceDescriptor.Transient<IComponentActivator, SfComponentActivator>());
    testContext.Services.AddOptions();

    // Rendering application Home component (~/Pages/Home.razor).
    var indexComponent = testContext.RenderComponent<Home>();
    
    // Set Home component parameter Step value.
    indexComponent.SetParametersAndRender(parameters => parameters.Add(p => p.Step, 5));

    // Find Syncfusion Button component.
    var sfButton = indexComponent.FindComponent<SfButton>();
    
    // Find span element.
    var span = indexComponent.Find("span.alert.alert-info");

    // Assert
    // Testing span element markup initial state.
    span.MarkupMatches("<span class=\"alert alert-info\">Count: 0</span>");

    // Click Syncfusion Button component.
    sfButton.Find(".e-btn").Click();

    // Testing span element markup again.
    span.MarkupMatches("<span class=\"alert alert-info\">Count: 5</span>");
}
```
