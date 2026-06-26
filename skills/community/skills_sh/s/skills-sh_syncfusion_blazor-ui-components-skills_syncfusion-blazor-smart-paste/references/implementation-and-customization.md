# Syncfusion Blazor Smart Paste Button - Usage and Customization Guide

## Overview

This guide covers implementing the Smart Paste Button component, adding annotations, customizing appearance, integrating custom AI services, and troubleshooting. Ensure you've completed setup and configuration from **getting-started.md** and **ai-service-configuration.md**.

## Add Smart Paste Button Component

Add the Syncfusion Blazor Smart Paste Button component with form components in `~/Pages/Index.razor`:

```razor
@using Syncfusion.Blazor.DataForm
@using System.ComponentModel.DataAnnotations
@using Syncfusion.Blazor.SmartComponents

<SfDataForm ID="MyForm"
            Model="@EventRegistrationModel">
    <FormValidator>
        <DataAnnotationsValidator></DataAnnotationsValidator>
    </FormValidator>
    <FormItems>
        <FormItem Field="@nameof(EventRegistration.Name)" ID="firstname"></FormItem>
        <FormItem Field="@nameof(EventRegistration.Email)" ID="email"></FormItem>
        <FormItem Field="@nameof(EventRegistration.Phone)" ID="phonenumber"></FormItem>
        <FormItem Field="@nameof(EventRegistration.Address)" ID="address"></FormItem>
    </FormItems>
    <FormButtons>
        <SfSmartPasteButton IsPrimary="true" Content="Smart Paste" IconCss="e-icons e-paste">
        </SfSmartPasteButton>
    </FormButtons>
</SfDataForm>

<br>
<h4 style="text-align:center;">Sample content</h4>
<div>
    Hi, my name is Jane Smith. You can reach me at example@domain.com or call me at +1-555-987-6543. I live at 789 Pine Avenue, Suite 12, Los Angeles, CA 90001.
</div>

@code {
    private EventRegistration EventRegistrationModel = new EventRegistration();

    public class EventRegistration
    {
        [Required(ErrorMessage = "Please enter your name.")]
        [Display(Name = "Name")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Please enter your email address.")]
        [Display(Name = "Email ID")]
        public string Email { get; set; }

        [Required(ErrorMessage = "Please enter your mobile number.")]
        [Display(Name = "Phone Number")]
        public string Phone { get; set; }

        [Required(ErrorMessage = "Please enter your address.")]
        [Display(Name = "Address")]
        public string Address { get; set; }
    }
}
```

## Running the Application

To test the Smart Paste Button:

1. Press **Ctrl+F5** (Windows) or **⌘+F5** (macOS) to launch the application
2. Copy the **Sample Content** from the page
3. Click the **Smart Paste** button
4. Observe form fields automatically populated with the analyzed data

## Annotations and Custom Field Descriptions

### Using data-smartpaste-description Attribute

By default, the Smart Paste Button analyzes form fields like `<input>`, `<select>`, and `<textarea>` elements, generating descriptions based on associated `<label>`, `name` attribute, `id` attribute, or nearby text content.

For more control, override the default behavior by specifying custom descriptions using the `data-smartpaste-description` attribute:

```razor
@using Syncfusion.Blazor.DataForm
@using System.ComponentModel.DataAnnotations
@using Syncfusion.Blazor.SmartComponents
@using Syncfusion.Blazor.Inputs

<SfDataForm ID="MyForm"
            Model="@EventRegistrationModel">
    <FormValidator>
        <DataAnnotationsValidator></DataAnnotationsValidator>
    </FormValidator>
    <FormItems>
        <FormItem Field="@nameof(EventRegistration.Name)" ID="firstname"></FormItem>
        <FormItem Field="@nameof(EventRegistration.DateOfBirth)">
            <Template>
                <label class="e-form-label">Date of Birth</label>
                <SfTextBox HtmlAttributes="DateOfBirth"
                           ID="dateofbirth" />
            </Template>
        </FormItem>
        <FormItem Field="@nameof(EventRegistration.Email)" ID="email"></FormItem>
        <FormItem Field="@nameof(EventRegistration.Phone)" ID="phonenumber"></FormItem>
        <FormItem Field="@nameof(EventRegistration.Address)" ID="address"></FormItem>
    </FormItems>
    <FormButtons>
        <SfSmartPasteButton IsPrimary="true" Content="Smart Paste" IconCss="e-icons e-paste">
        </SfSmartPasteButton>
    </FormButtons>
</SfDataForm>

<br>
<h4 style="text-align:center;">Sample content</h4>
<div>
    Hi, my name is Jane Smith. You can reach me at example@domain.com or call me at +1-555-987-6543. I live at 789 Pine Avenue, Suite 12, Los Angeles, CA 90001. I was born on 15th March 1990.
</div>

@code {
    private EventRegistration EventRegistrationModel = new EventRegistration();

    Dictionary<string, object> DateOfBirth = new Dictionary<string, object>()
    {
        { "data-smartpaste-description", "Date must follow the format: DD-MM-YYYY" }
    };

    public class EventRegistration
    {
        [Required(ErrorMessage = "Please enter your name.")]
        [Display(Name = "Name")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Please enter your email address.")]
        [Display(Name = "Email ID")]
        public string Email { get; set; }

        [Required(ErrorMessage = "Please enter your mobile number.")]
        [Display(Name = "Phone Number")]
        public string Phone { get; set; }

        [Required(ErrorMessage = "Please enter your address.")]
        [Display(Name = "Address")]
        public string Address { get; set; }

        [Required(ErrorMessage = "Please enter your DOB.")]
        [Display(Name = "Date Of Birth")]
        public string DateOfBirth { get; set; }
    }
}
```

## Customization

### Types and Appearance

The Syncfusion Blazor Smart Paste Button fully inherits all properties, types, and styling options of the Syncfusion Blazor Button component.

You can leverage:
- **Types and Styles** - Refer to **Syncfusion Blazor Button Types and Styles**
- **Appearances** - Refer to **Syncfusion Blazor Button Appearances**

## Custom AI Service Integration

### IChatInferenceService Interface

Implement custom AI services using the `IChatInferenceService` interface:

```csharp
public interface IChatInferenceService
{
    Task<string> GenerateResponseAsync(ChatParameters options);
}
```

The `GenerateResponseAsync` method takes `ChatParameters` (containing clipboard data and form field metadata) and returns a string response for populating form fields.

### Sample Custom AI Service Implementation

Below is a mock AI service example:

```csharp
using Syncfusion.Blazor.AI;
using System.Threading.Tasks;

public class MockAIService : IChatInferenceService
{
    public Task<string> GenerateResponseAsync(ChatParameters options)
    {
        // Implement custom AI logic here
        // Return formatted response for form fields
    }
}
```

### Register Custom AI Service

Register the custom AI service in `~/Program.cs`:

```csharp
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using Syncfusion.Blazor;
using Syncfusion.Blazor.AI;
using Syncfusion.Blazor.SmartComponents;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddSyncfusionBlazor();
builder.Services.AddSyncfusionSmartComponents();
builder.Services.AddSingleton<IChatInferenceService, MockAIService>();

var app = builder.Build();
// ... rest of configuration
```

### Testing Custom AI Integration

1. Configure the Blazor Web App with Smart Paste Button and custom AI service
2. Add the implementation to your Razor files
3. Run the application (Ctrl+F5 or ⌘+F5)
4. Copy sample content and click Smart Paste button
5. Verify form fields populate correctly

### Examples of Implemented AI Services

The following AI services can be integrated using the `IChatInferenceService` interface:

| AI Service | Integration |
|-----------|-------------|
| Claude | Claude Integration |
| DeepSeek | DeepSeek Integration |
| Groq | Groq Integration |
| Gemini | Gemini Integration |

## Performance Considerations

For optimal performance with the Smart Paste Button:

- **Use Lightweight AI Models**: Choose models like `gpt-3.5-turbo` or `mistral:7b` for faster processing
- **Limit Form Complexity**: Reduce the number of form fields being analyzed to minimize AI parsing time, especially for large datasets
- **Cache AI Model Responses**: Implement caching where possible to minimize repeated API calls to the AI service
- **Monitor API Costs**: Be aware of usage patterns to manage costs with external AI APIs

## Troubleshooting Common Issues

### AI Service Configuration Errors

**Problem**: Smart Paste button not working with AI service  
**Solution**: 
- Verify the API key, endpoint, and model name in `Program.cs`
- Check for typos or incorrect values
- Ensure proper spacing and formatting

### Network Failures

**Problem**: Connection errors when using OpenAI or Azure OpenAI  
**Solution**:
- Ensure a stable internet connection
- For Ollama, confirm the local server is running at the specified endpoint (e.g., `http://localhost:11434`)
- Check firewall and proxy settings

### Form Not Populating

**Problem**: Data from clipboard not appearing in form fields  
**Solution**:
- Confirm that the copied text matches the form field structure
- Verify the AI model is correctly configured
- Check that form field IDs and labels are properly set
- Test the AI service independently to verify connectivity
- Review browser console for JavaScript errors

### Service Registration Errors

**Problem**: Dependency injection errors at startup  
**Solution**:
- Confirm `CustomAIService` is registered in `Program.cs` after `AddSyncfusionBlazor`
- Verify all required interfaces are properly implemented
- Check NuGet package versions match the dependencies

### Custom AI Service Issues

**Problem**: Custom AI integration not working  
**Solution**:
- Verify endpoint, model, and API key in configuration
- Ensure `GenerateResponseAsync` returns valid data
- Check the AI service's response format matches expected structure
- Test the API independently

