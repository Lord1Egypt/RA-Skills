# Templates & Display in Blazor Mention Component

## Table of Contents
- [Overview](#overview)
- [Item Template](#item-template)
- [Display Template](#display-template)
- [No Records Template](#no-records-template)
- [Spinner Template](#spinner-template)
- [Template Context](#template-context)
- [Advanced Template Examples](#advanced-template-examples)

---

## Overview

Templates allow you to customize how mention items display and how selected mentions appear. The Mention component provides:
- **ItemTemplate:** Customize each suggestion item
- **DisplayTemplate:** Format selected mention display
- **NoRecordsTemplate:** Show when no matches found
- **SpinnerTemplate:** Show while loading data

All templates use `RenderFragment` with a `context` parameter for data access.

---

## Item Template

### Basic Item Template

Controls how each suggestion appears in the dropdown:

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true" placeholder="Type @..."></div>
    </TargetComponent>
    <ItemTemplate>
        <div style="padding: 8px;">
            <strong>@((context as PersonData).Name)</strong>
        </div>
    </ItemTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public string Name { get; set; }
        public string Email { get; set; }
    }

    List<PersonData> TeamMembers = new()
    {
        new() { Name = "Alice", Email = "alice@company.com" },
        new() { Name = "Bob", Email = "bob@company.com" }
    };
}
```

**Result:** Displays name in bold in suggestion list

### Multi-Column Item Template

```razor
<SfMention TItem="EmployeeData" DataSource="@Employees">
    <TargetComponent>
        <div id="empMention" contenteditable="true"></div>
    </TargetComponent>
    <ItemTemplate>
        <div style="display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #eee;">
            <div style="flex: 1;">
                <strong>@((context as EmployeeData).Name)</strong><br/>
                <small>@((context as EmployeeData).Email)</small>
            </div>
            <div style="flex: 0 0 auto; color: #666; font-size: 12px;">
                @((context as EmployeeData).Department)
            </div>
        </div>
    </ItemTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class EmployeeData
    {
        public string Name { get; set; }
        public string Email { get; set; }
        public string Department { get; set; }
    }

    List<EmployeeData> Employees = new()
    {
        new() { Name = "Alice Johnson", Email = "alice@company.com", Department = "Engineering" },
        new() { Name = "Bob Smith", Email = "bob@company.com", Department = "Sales" }
    };
}
```

**Result:** Shows Name (bold), Email (small), and Department (right-aligned)

### Item Template with Styling

```razor
<SfMention TItem="UserData" DataSource="@Users">
    <TargetComponent>
        <div id="styledMention" contenteditable="true"></div>
    </TargetComponent>
    <ItemTemplate>
        @{
            var user = context as UserData;
            var statusColor = user.Status == "Active" ? "green" : "gray";
        }
        <div style="padding: 8px; display: flex; align-items: center; gap: 8px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #007bff; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                @user.Name[0]
            </div>
            <div>
                <strong>@user.Name</strong>
                <div style="font-size: 12px; color: @statusColor;">● @user.Status</div>
            </div>
        </div>
    </ItemTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class UserData
    {
        public string Name { get; set; }
        public string Status { get; set; }
    }

    List<UserData> Users = new()
    {
        new() { Name = "Alice", Status = "Active" },
        new() { Name = "Bob", Status = "Offline" }
    };
}
```

**Result:** Shows user avatar (initial), name, and colored status indicator

---

## Display Template

### Basic Display Template

Controls how selected mention appears:

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true" placeholder="Type @..."></div>
    </TargetComponent>
    <DisplayTemplate>
        <span style="background: lightblue; padding: 2px 6px; border-radius: 3px;">
            @((context as PersonData).Name)
        </span>
    </DisplayTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }

    List<PersonData> TeamMembers = new();
}
```

**Result:** Selected mention displays with light blue background

### Display Template with Multiple Fields

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <DisplayTemplate>
        <span style="background: #007bff; color: white; padding: 3px 8px; border-radius: 4px; margin: 2px;">
            @((context as PersonData).Name) - @((context as PersonData).Department)
        </span>
    </DisplayTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public string Name { get; set; }
        public string Department { get; set; }
    }

    List<PersonData> TeamMembers = new()
    {
        new() { Name = "Alice", Department = "Engineering" },
        new() { Name = "Bob", Department = "Sales" }
    };
}
```

**Result:** Mention displays as "Alice - Engineering" in a blue pill

### Display Template with Icons

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <DisplayTemplate>
        <span style="display: inline-flex; align-items: center; gap: 4px; background: #e3f2fd; padding: 2px 8px; border-radius: 4px;">
            👤 <strong>@((context as PersonData).Name)</strong>
        </span>
    </DisplayTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>
```

**Result:** Shows 👤 icon + name for each mention

---

## No Records Template

### Show Message When No Matches

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <NoRecordsTemplate>
        <div style="padding: 16px; text-align: center; color: #999;">
            <p>😕 No members found</p>
            <small>Try searching with a different name</small>
        </div>
    </NoRecordsTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> TeamMembers = new();
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Result:** When no items match filter, shows "😕 No members found"

### No Records with Action

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <NoRecordsTemplate>
        <div style="padding: 16px; color: #666;">
            <p><strong>No results for your search</strong></p>
            <p><small>Showing all team members:</small></p>
            <ul style="margin: 8px 0; padding-left: 20px;">
                @foreach(var member in TeamMembers)
                {
                    <li>@member.Name</li>
                }
            </ul>
        </div>
    </NoRecordsTemplate>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }

    List<PersonData> TeamMembers = new()
    {
        new() { Name = "Alice" },
        new() { Name = "Bob" },
        new() { Name = "Carol" }
    };
}
```

**Result:** Shows all available team members when no matches found

---

## Spinner Template

### Custom Loading Spinner

```razor
<SfMention TItem="PersonData">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <SpinnerTemplate>
        <div style="padding: 16px; text-align: center;">
            <div style="display: inline-block; animation: spin 1s linear infinite; font-size: 20px;">
                ⏳
            </div>
            <p style="margin-top: 8px; color: #666;">Loading suggestions...</p>
        </div>
    </SpinnerTemplate>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" 
                       Adaptor="Adaptors.WebApiAdaptor">
        </SfDataManager>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

<style>
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Result:** Shows animated hourglass during data fetch

### Spinner with Progress Text

```razor
<SfMention TItem="PersonData">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <SpinnerTemplate>
        <div style="padding: 24px; text-align: center;">
            <div style="font-size: 14px; color: #666;">
                <div style="animation: pulse 1.5s ease-in-out infinite;">
                    ● ● ●
                </div>
                <p style="margin-top: 12px;">Fetching team members...</p>
            </div>
        </div>
    </SpinnerTemplate>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" 
                       Adaptor="Adaptors.WebApiAdaptor">
        </SfDataManager>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

<style>
    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
</style>
```

---

## Template Context

### Understanding Context Parameter

Templates receive data through `context` parameter. Access properties directly:

```razor
<ItemTemplate>
    @{
        var person = context as PersonData;
        var firstLetter = person.Name?[0].ToString().ToUpper() ?? "";
    }
    <div>
        <div style="width: 24px; height: 24px; background: #007bff; color: white; 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            @firstLetter
        </div>
        <span>@person.Name</span>
    </div>
</ItemTemplate>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

### Type-Safe Context

```razor
<ItemTemplate Context="person">
    @{
        var userData = (PersonData)person;
    }
    <div>@userData.Name</div>
</ItemTemplate>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

---

## Advanced Template Examples

### Complete Team Member Display

```razor
<SfMention TItem="TeamMemberData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true" placeholder="Type @ to mention..."></div>
    </TargetComponent>
    
    <ItemTemplate>
        @{
            var member = context as TeamMemberData;
            var roleColor = member.Role == "Lead" ? "#dc3545" : "#28a745";
        }
        <div style="padding: 10px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #f0f0f0;">
            <img src="@member.AvatarUrl" 
                 style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;" 
                 alt="@member.Name" />
            <div style="flex: 1;">
                <strong>@member.Name</strong>
                <div style="font-size: 12px; color: #666;">@member.Email</div>
            </div>
            <span style="background: @roleColor; color: white; font-size: 10px; padding: 2px 6px; border-radius: 3px;">
                @member.Role
            </span>
        </div>
    </ItemTemplate>

    <DisplayTemplate>
        <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 4px 10px; border-radius: 12px; 
                     display: inline-flex; align-items: center; gap: 6px; margin: 2px;">
            <img src="@((context as TeamMemberData).AvatarUrl)" 
                 style="width: 16px; height: 16px; border-radius: 50%; object-fit: cover;" />
            <strong>@((context as TeamMemberData).Name)</strong>
        </span>
    </DisplayTemplate>

    <NoRecordsTemplate>
        <div style="padding: 16px; text-align: center; color: #999;">
            <p>No team members found</p>
        </div>
    </NoRecordsTemplate>

    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class TeamMemberData
    {
        public string Name { get; set; }
        public string Email { get; set; }
        public string Role { get; set; }
        public string AvatarUrl { get; set; }
    }

    List<TeamMemberData> TeamMembers = new()
    {
        new() 
        { 
            Name = "Alice Johnson", 
            Email = "alice@company.com", 
            Role = "Lead",
            AvatarUrl = "YOUR_AVATAR_IMAGE_URL"
        },
        new() 
        { 
            Name = "Bob Smith", 
            Email = "bob@company.com", 
            Role = "Developer",
            AvatarUrl = "YOUR_AVATAR_IMAGE_URL"
        }
    };
}
```

**Result:** Professional team member display with avatars, roles, and formatted selected mentions

---

## Template Best Practices

### Do's ✅
- Keep ItemTemplate concise (< 100 lines)
- Use inline styles or CSS classes
- Cache computed values in @code blocks
- Null-check complex properties

### Don'ts ❌
- Avoid complex async operations in templates
- Don't use reflection for property access
- Avoid large images in ItemTemplate (performance)
- Don't hardcode colors (use theme variables)

---

## Next Steps

- **Refine filtering:** See [Filtering & Search](../filtering-and-search.md)
- **Explore customization:** Check [Customization](../customization.md)
- **Ensure accessibility:** Review [Accessibility](../accessibility.md)
