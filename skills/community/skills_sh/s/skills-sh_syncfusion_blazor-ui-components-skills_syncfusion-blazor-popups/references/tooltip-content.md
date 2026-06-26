# Tooltip Content Management

## Table of Contents
- [Overview](#overview)
- [Simple Text Content](#simple-text-content)
- [Using Title Attribute](#using-title-attribute)
- [HTML Templates with ContentTemplate](#html-templates-with-contenttemplate)
- [Dynamic Content with RenderFragment](#dynamic-content-with-renderfragment)
- [Rendering HTML with MarkupString](#rendering-html-with-markupstring)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)

## Overview

The Blazor Tooltip component supports multiple content types, from simple text strings to complex HTML templates with interactive elements. Choose the appropriate content type based on your requirements:

- **Simple text**: Use `Content` property for basic messages
- **Title attribute**: Leverage existing HTML title attributes
- **ContentTemplate**: Create rich HTML layouts with formatting
- **RenderFragment**: Build dynamic, programmatic content
- **MarkupString**: Render HTML strings from variables or databases

## Simple Text Content

The simplest way to display tooltip content is using the `Content` property with a string value.

### Basic Example

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="Tooltip" Target="#btn" Content="@Content">
    <SfButton ID="btn" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Lets go green & Save Earth !!";
}
```

### When to Use

- **Quick hints**: Brief descriptions or labels
- **Status messages**: Simple notifications or confirmations
- **Icon labels**: Describing icon-only buttons
- **Single-line help**: Short contextual information

### Key Points

- Content is set via the `Content` property
- String value can be a variable or literal
- HTML tags in strings are rendered as plain text (escaped)
- Maximum recommended length: 1-2 sentences for readability

### Multiple Text Tooltips

```razor
<SfTooltip Target=".action-btn" Content="@GetTooltipContent">
    <div>
        <button class="action-btn" data-action="save">Save</button>
        <button class="action-btn" data-action="cancel">Cancel</button>
        <button class="action-btn" data-action="delete">Delete</button>
    </div>
</SfTooltip>

@code
{
    string GetTooltipContent = "Perform action";
}
```

## Using Class-Based Selectors for Multiple Elements

The Tooltip component works best with class or ID selectors to target specific elements and provide explicit content. While `title` attributes can remain on elements for semantic HTML and fallback behavior, they should NOT be used as selectors.

### Basic Implementation with Class Selector

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Popups

<SfTooltip ID="Tooltip" Target=".eco-btn" Content="Learn about environmental action">
    <div id="container">
        <SfButton ID="btn1" CssClass="eco-btn" Content="Button 1" title="Go green and save energy"></SfButton>
        <SfButton ID="btn2" CssClass="eco-btn" Content="Button 2" title="Plant trees to combat climate change"></SfButton>
        <button class="eco-btn" title="Recycle to reduce waste">Recycle Tips</button>
        <a href="#" class="eco-btn" title="Switch to renewable energy">Renewable Energy</a>
    </div>
</SfTooltip>
```

### How It Works

1. Add class names to target elements (e.g., `class="eco-btn"`)
2. Set `Target=".eco-btn"` - Selects all elements with the class (NOT using `[title]` as selector)
3. Set explicit `Content` property with tooltip text
4. Title attributes on elements provide semantic markup and fallback behavior
5. Works with any HTML element (buttons, links, spans, divs, etc.)

### When to Use

- **Multiple elements**: Same tooltip for many elements with a common class
- **Semantic markup**: Use meaningful class names and title attributes
- **Consistent behavior**: Uniform styling across similar elements
- **Easy maintenance**: Content is clearly defined in the component

### Mixed Elements Example

```razor
<SfTooltip Target=".toolbar-item" Content="Perform an action">
    <div class="toolbar">
        <button class="toolbar-item" title="Create new document">New</button>
        <button class="toolbar-item" title="Open existing file">Open</button>
        <button class="toolbar-item" title="Save current work">Save</button>
        <span class="toolbar-item status-icon" title="File is auto-saved">✓</span>
        <a href="#settings" class="toolbar-item" title="Configure application settings">Settings</a>
    </div>
</SfTooltip>
```

### Advantages

- Clear and explicit content definition via `Content` property
- Works reliably with Syncfusion Tooltip
- Title attributes remain for semantic HTML and browser fallback
- Easy to style and target specific elements with class/ID selectors
- Better maintainability with explicit selectors and content

## HTML Templates with ContentTemplate

For rich, formatted content, use the `ContentTemplate` property to define custom HTML layouts.

### Basic Template

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Popups

<SfTooltip CssClass="e-tooltip-css" OpensOn="Click" Target="#btn">
    <ContentTemplate>
        <div id='democontent' class='democontent'>
            <div class='info'>
                <h3 style='margin-top:10px'>Eastern Bluebird <hr style='margin-top:10px'></h3>
                <div style='margin-top: -10px'>
                    <div style='float:left;width:57%'>
                        The
                        <a href='https://en.wikipedia.org/wiki/Eastern_bluebird' target='_blank'>
                            Eastern Bluebird
                        </a> 
                        is easily found in open fields and sparse woodland areas, including along woodland edges.
                        These are <i>cavity-nesting birds</i> and a pair of eastern bluebirds will raise 
                        2-3 broods annually, with 2-8 light blue or whitish eggs per brood.
                    </div>
                    <div id='bird' style='float:right;width:42%'>
                        <img src='https://blazor.syncfusion.com/demos/_content/blazor_webapp_common_net8/images/tooltip/bird.png' 
                             width='125' height='125' alt='Bluebird' />
                    </div>
                </div>
                <div style='margin-top:160px'>
                    <hr>
                    <p style='margin-top:-11px'>
                        Eastern bluebirds can be very vocal in flocks. Their calls include a rapid, 
                        mid-tone chatter and several long dropping pitch calls.
                    </p>
                </div>
                <p>Source:<br />
                    <a href='https://en.wikipedia.org/wiki/Eastern_bluebird' target='_blank'>
                        https://en.wikipedia.org/wiki/Eastern_bluebird
                    </a>
                </p>
            </div>
        </div>
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="btn" CssClass="e-outline text" IsPrimary="true" Content="HTML Template"></SfButton>
    </ChildContent>
</SfTooltip>

<style>
    .e-tooltip-css {
        filter: drop-shadow(2px 5px 5px rgba(0, 0, 0, 0.25));
    }
    .democontent {
        border: 0.5px solid grey;
    }
    #bird {
        padding-top: 4px;
    }
    .info a {
        color: #2FA1E3;
    }
    .info {
        padding-left: 12px;
        padding-right: 5px;
    }
</style>
```

### When to Use

- **Rich information cards**: Product details, user profiles, statistics
- **Formatted content**: Headings, paragraphs, lists, images
- **Multi-section layouts**: Complex information with multiple parts
- **Branded styling**: Custom designs with specific layouts

### User Profile Example

```razor
<SfTooltip Target="#userAvatar" OpensOn="Click" IsSticky="true">
    <ContentTemplate>
        <div style="padding: 15px; min-width: 250px;">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <img src="/images/avatar.jpg" alt="Avatar" 
                     style="width: 50px; height: 50px; border-radius: 50%; margin-right: 15px;" />
                <div>
                    <h4 style="margin: 0;">John Doe</h4>
                    <p style="margin: 0; color: #666; font-size: 12px;">Senior Developer</p>
                </div>
            </div>
            <hr style="margin: 10px 0;" />
            <p style="margin: 5px 0;"><strong>Email:</strong> john.doe@example.com</p>
            <p style="margin: 5px 0;"><strong>Phone:</strong> (555) 123-4567</p>
            <p style="margin: 5px 0;"><strong>Department:</strong> Engineering</p>
            <div style="margin-top: 10px;">
                <button style="padding: 5px 10px; margin-right: 5px;">Message</button>
                <button style="padding: 5px 10px;">View Profile</button>
            </div>
        </div>
    </ContentTemplate>
    <ChildContent>
        <div id="userAvatar" style="cursor: pointer;">👤</div>
    </ChildContent>
</SfTooltip>
```

### Product Details Example

```razor
<SfTooltip Target=".product-item" OpensOn="Hover">
    <ContentTemplate>
        <div style="max-width: 300px; padding: 10px;">
            <img src="/images/product.jpg" alt="Product" style="width: 100%; border-radius: 4px;" />
            <h4 style="margin: 10px 0 5px 0;">Premium Wireless Headphones</h4>
            <p style="color: #666; font-size: 13px; margin: 5px 0;">
                High-quality audio with active noise cancellation and 30-hour battery life.
            </p>
            <div style="margin-top: 10px;">
                <span style="font-size: 18px; font-weight: bold; color: #2196F3;">$299.99</span>
                <span style="margin-left: 10px; text-decoration: line-through; color: #999;">$399.99</span>
            </div>
            <ul style="margin: 10px 0; padding-left: 20px; font-size: 12px;">
                <li>Active Noise Cancellation</li>
                <li>30-hour battery life</li>
                <li>Bluetooth 5.0</li>
                <li>Premium comfort design</li>
            </ul>
        </div>
    </ContentTemplate>
    <ChildContent>
        <div class="product-item">View Product</div>
    </ChildContent>
</SfTooltip>
```

### Key Points

- ContentTemplate supports any HTML markup
- Use ChildContent to wrap target elements
- Combine with `OpensOn="Click"` and `IsSticky="true"` for complex content
- Add custom CSS via CssClass property
- Images, links, and formatting all work

## Dynamic Content with RenderFragment

RenderFragment enables programmatic content generation with full access to component logic, state, and Blazor components.

### Basic RenderFragment

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Popups

<SfTooltip ID="tooltip" Target="#target">
    <ContentTemplate>
        <div>
            @(TooltipContent())
        </div>
    </ContentTemplate>
    <ChildContent>
        <div id='container'>
            <p>
                A green home is a type of house designed to be
                <a id="target">
                    <u>environmentally friendly</u>
                </a> 
                and sustainable. And also focuses on the efficient use of "energy, water, and building materials."
            </p>
        </div>
    </ChildContent>
</SfTooltip>

@code {
    private RenderFragment TooltipContent()
    {
        return @<div>
            <h3>Complex Tooltip Content</h3>
            <p>This is a paragraph inside the tooltip.</p>
            <ul>
                <li>List item 1</li>
                <li>List item 2</li>
                <li>List item 3</li>
            </ul>
            <button @onclick="@(() => Console.WriteLine("Button in Tooltip clicked!"))">
                Click me!
            </button>
            <SfButton ID="btn" IsPrimary="true" Content="Syncfusion Button"></SfButton>
        </div>;
    }
}
```

### When to Use

- **Dynamic content**: Content changes based on state or props
- **Interactive elements**: Buttons, inputs, or other interactive components
- **Conditional rendering**: Show/hide parts based on logic
- **Component composition**: Include other Blazor components
- **Event handling**: Respond to user interactions inside tooltip

### Interactive Dashboard Card

```razor
<SfTooltip ID="statsTooltip" Target="#statsButton" OpensOn="Click" IsSticky="true">
    <ContentTemplate>
        @GetStatsContent()
    </ContentTemplate>
    <ChildContent>
        <SfButton ID="statsButton" Content="View Stats" IconCss="e-icons e-chart"></SfButton>
    </ChildContent>
</SfTooltip>

@code {
    private int viewCount = 1234;
    private int likeCount = 567;
    
    private RenderFragment GetStatsContent() => @<div style="padding: 15px; min-width: 200px;">
        <h4 style="margin-top: 0;">Statistics</h4>
        <div style="margin: 10px 0;">
            <strong>Views:</strong> @viewCount
            <button @onclick="IncrementViews" style="margin-left: 10px;">+</button>
        </div>
        <div style="margin: 10px 0;">
            <strong>Likes:</strong> @likeCount
            <button @onclick="IncrementLikes" style="margin-left: 10px;">+</button>
        </div>
        <button @onclick="RefreshStats" style="margin-top: 10px; width: 100%;">
            Refresh
        </button>
    </div>;
    
    private void IncrementViews() => viewCount++;
    private void IncrementLikes() => likeCount++;
    private void RefreshStats()
    {
        // Fetch new data
        Console.WriteLine("Refreshing stats...");
    }
}
```

### Conditional Content

```razor
<SfTooltip Target="#statusIcon">
    <ContentTemplate>
        @GetStatusContent()
    </ContentTemplate>
    <ChildContent>
        <span id="statusIcon" class="status-icon">🔔</span>
    </ChildContent>
</SfTooltip>

@code {
    private bool isOnline = true;
    private int messageCount = 5;
    
    private RenderFragment GetStatusContent() => @<div style="padding: 10px;">
        @if (isOnline)
        {
            <p style="color: green; margin: 0;">● Online</p>
            @if (messageCount > 0)
            {
                <p style="margin: 5px 0;">You have @messageCount new messages</p>
            }
            else
            {
                <p style="margin: 5px 0;">No new messages</p>
            }
        }
        else
        {
            <p style="color: red; margin: 0;">● Offline</p>
            <p style="margin: 5px 0;">You appear offline to others</p>
        }
    </div>;
}
```

### Key Points

- RenderFragment allows full C# logic in content
- Can include event handlers (@onclick, @onchange, etc.)
- Can use component state and properties
- Supports conditional rendering with @if, @foreach, @switch
- Can nest other Blazor components (SfButton, etc.)
- Updates automatically when state changes

## Rendering HTML with MarkupString

Use `MarkupString` to render HTML stored as strings, typically from databases, APIs, or configuration files.

### Basic MarkupString

```razor
@using Syncfusion.Blazor.Popups

<SfTooltip ID="tooltip" Target="#target">
    <ContentTemplate>
        <div>
            @((MarkupString)Content)
        </div>
    </ContentTemplate>
    <ChildContent>
        <div id='container'>
            <p>
                A green home is a type of house designed to be
                <a id="target">
                    <u>environmentally friendly</u>
                </a> 
                and sustainable.
            </p>
        </div>
    </ChildContent>
</SfTooltip>

@code
{
    string Content = "<div><b>Environmentally friendly</b> or environment-friendly, (also referred to as eco-friendly, nature-friendly, and green) are marketing and sustainability terms referring to goods and services, laws, guidelines and policies that inflict reduced, minimal, or no harm upon ecosystems or the environment.</div>";
}
```

### When to Use

- **Database content**: HTML stored in database fields
- **API responses**: HTML received from external services
- **CMS integration**: Content from content management systems
- **Configuration files**: HTML templates from JSON/XML
- **Markdown conversion**: Rendered markdown-to-HTML output

### From Database Example

```razor
<SfTooltip Target=".help-icon" OpensOn="Click">
    <ContentTemplate>
        <div style="max-width: 300px;">
            @((MarkupString)helpContent)
        </div>
    </ContentTemplate>
    <ChildContent>
        <span class="help-icon">❓</span>
    </ChildContent>
</SfTooltip>

@code {
    private string helpContent = string.Empty;
    
    protected override async Task OnInitializedAsync()
    {
        // Fetch from database or API
        helpContent = await GetHelpContentFromDatabase();
    }
    
    private async Task<string> GetHelpContentFromDatabase()
    {
        // Simulate API call
        await Task.Delay(100);
        return @"
            <h4>How to Use This Feature</h4>
            <ol>
                <li>Click the <strong>Start</strong> button</li>
                <li>Select your options from the dropdown</li>
                <li>Click <strong>Apply</strong> to save changes</li>
            </ol>
            <p><em>Need more help? <a href='/support'>Contact Support</a></em></p>
        ";
    }
}
```

### Security Warning

⚠️ **Important**: MarkupString renders HTML without sanitization. Only use with trusted content to prevent XSS attacks.

**Safe:**
```csharp
// Content from your own database/CMS with validation
string safeContent = "<p>Safe content from trusted source</p>";
@((MarkupString)safeContent)
```

**Unsafe:**
```csharp
// Never do this with user-generated content
string userContent = Request.Query["content"]; // ❌ DANGEROUS
@((MarkupString)userContent) // ❌ XSS VULNERABILITY
```

### Sanitization Example

```csharp
// Use a library like HtmlSanitizer
using Ganss.XSS;

private string SanitizeHtml(string html)
{
    var sanitizer = new HtmlSanitizer();
    return sanitizer.Sanitize(html);
}

// In component
string userContent = GetUserContent();
string safeContent = SanitizeHtml(userContent);
@((MarkupString)safeContent)
```

## Best Practices

### Content Length

- **Brief tooltips**: 1-2 sentences (simple hover hints)
- **Medium content**: 2-4 sentences (descriptions with details)
- **Rich content**: Use templates with sections, combine with IsSticky="true"

### Performance

- Avoid heavy computations in RenderFragment for hover tooltips
- Cache dynamic content when possible
- Use simple text for frequently opened tooltips

### Accessibility

- Keep content concise and scannable
- Use semantic HTML in templates (headings, lists, etc.)
- Ensure good color contrast
- Avoid essential information in tooltips (should supplement, not replace)

### User Experience

- Match content complexity to trigger type:
  - Hover: Brief, glanceable content
  - Click: More detailed, interactive content
  - Focus: Form field help text

## Common Patterns

### Help Text Pattern

```razor
<SfTooltip Target=".help-icon" Content="@helpText">
    <input type="text" placeholder="Username" />
    <span class="help-icon">ⓘ</span>
</SfTooltip>

@code {
    string helpText = "Enter your email address or username";
}
```

### Status Indicator Pattern

```razor
<SfTooltip Target=".status-badge">
    <ContentTemplate>
        @GetStatusTooltip()
    </ContentTemplate>
    <ChildContent>
        <span class="status-badge" data-status="active">●</span>
    </ChildContent>
</SfTooltip>
```

### Rich Preview Pattern

```razor
<SfTooltip Target=".preview-link" OpensOn="Hover">
    <ContentTemplate>
        <div>@((MarkupString)previewHtml)</div>
    </ContentTemplate>
    <ChildContent>
        <a href="/article" class="preview-link">Read Article</a>
    </ChildContent>
</SfTooltip>
```

### Interactive Actions Pattern

```razor
<SfTooltip Target="#quickActions" OpensOn="Click" IsSticky="true">
    <ContentTemplate>
        @QuickActionsMenu()
    </ContentTemplate>
    <ChildContent>
        <button id="quickActions">Actions ▾</button>
    </ChildContent>
</SfTooltip>

@code {
    private RenderFragment QuickActionsMenu() => @<div>
        <button @onclick="HandleEdit">Edit</button>
        <button @onclick="HandleDelete">Delete</button>
        <button @onclick="HandleShare">Share</button>
    </div>;
}
```
