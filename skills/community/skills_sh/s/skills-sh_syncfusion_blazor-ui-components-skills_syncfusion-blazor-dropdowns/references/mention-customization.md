# Customization in Blazor Mention Component

## Table of Contents
- [Overview](#overview)
- [Mention Character](#mention-character)
- [Mention Display](#mention-display)
- [Space Requirements](#space-requirements)
- [Popup Dimensions](#popup-dimensions)
- [Complete Customization Example](#complete-customization-example)

---

## Overview

The Mention component provides several properties to customize behavior and appearance:
- **MentionChar:** Trigger character (default: @)
- **ShowMentionChar:** Display character in selected mention
- **SuffixText:** Text appended after mention
- **RequireLeadingSpace:** Space requirement before trigger
- **PopupHeight/Width:** Suggestion list dimensions

These properties let you adapt the component to your use case and design.

---

## Mention Character

### Change Trigger Character

By default, `@` triggers the mention. Change it for different use cases:

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           MentionChar="@MentionCharHash">
    <TargetComponent>
        <div id="hashMention" contenteditable="true" placeholder="Type # to mention..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharHash = '#';
    
    List<PersonData> TeamMembers = new()
    {
        new() { Name = "Alice" },
        new() { Name = "Bob" }
    };
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Result:** Type `#Alice` instead of `@Alice`

### Use Cases for Different Trigger Characters

| Character | Use Case | Example |
|-----------|----------|---------|
| `@` | User mentions | "I agree with @Alice" |
| `#` | Hashtags/topics | "This is #urgent" |
| `+` | Priorities | "Priority +high" |
| `:` | Emojis/codes | "Great work :tada:" |
| `&` | Teams/groups | "Notify &engineering-team" |

### Multiple Mention Components with Different Triggers

```razor
<!-- Users with @ -->
<SfMention TItem="PersonData" DataSource="@Users" MentionChar="@MentionCharAt">
    <TargetComponent>
        <div id="users" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

<!-- Topics with # -->
<SfMention TItem="TopicData" DataSource="@Topics" MentionChar="@MentionCharHash">
    <TargetComponent>
        <div id="users" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="TopicName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    private char MentionCharHash = '#';
    
    List<PersonData> Users = new();
    List<TopicData> Topics = new();
    
    public class PersonData { public string Name { get; set; } }
    public class TopicData { public string TopicName { get; set; } }
}
```

**Result:** Same target supports both @mentions and #hashtags

---

## Mention Display

### ShowMentionChar Property

Controls whether the trigger character appears in the selected mention:

#### Hide Mention Character (Default)

```razor
<SfMention TItem="PersonData" 
           DataSource="@Employees"
           MentionChar="@MentionCharAt"
           ShowMentionChar="false">
    <TargetComponent>
        <div id="hideMention" contenteditable="true" placeholder="Type @..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    
    List<PersonData> Employees = new()
    {
        new() { Name = "Alice Johnson" },
        new() { Name = "Bob Smith" }
    };
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Result:** Select "Alice Johnson" → Text shows "Alice Johnson" (no @)

#### Show Mention Character

```razor
<SfMention TItem="PersonData" 
           DataSource="@Employees"
           MentionChar="@MentionCharAt"
           ShowMentionChar="true">
    <TargetComponent>
        <div id="showMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
}
```

**Result:** Select "Alice Johnson" → Text shows "@Alice Johnson"

**Use Case:** When you need to visually distinguish mentions from regular text

---

## Space Requirements

### RequireLeadingSpace Property

Controls whether a space must precede the mention character:

#### Leading Space Required

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           MentionChar="@MentionCharAt"
           RequireLeadingSpace="true">
    <TargetComponent>
        <div id="spaceRequired" contenteditable="true" placeholder="Type SPACE then @..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    
    List<PersonData> TeamMembers = new();
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Behavior:**
- Type `@Alice` at line start → No suggestions
- Type ` @Alice` (with space) → Shows suggestions ✓
- Type `email@company.com` → No suggestions triggered (no space before @)

**Use Case:** Prevent email addresses from triggering mentions

#### Leading Space Not Required (Default)

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           MentionChar="@MentionCharAt"
           RequireLeadingSpace="false">
    <TargetComponent>
        <div id="noSpaceRequired" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
}
```

**Behavior:**
- Type `@Alice` anywhere → Shows suggestions ✓
- Type at start of line → Shows suggestions ✓
- Type `test@Alice` → Shows suggestions (may not be desired)

**Use Case:** Simple comment systems, clear mention intent

---

## Popup Dimensions

### PopupHeight Property

Controls suggestion list height:

```razor
<SfMention TItem="PersonData" 
           DataSource="@LargeDataset"
           MentionChar="@MentionCharAt"
           PopupHeight="250px">
    <TargetComponent>
        <div id="compactPopup" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    
    List<PersonData> LargeDataset = new(); // 100+ items
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Options:**
- `250px` → Compact, shows ~5-8 items
- `300px` → Default, shows ~8-10 items
- `400px` → Tall, shows ~12-15 items
- `100%` → Full height (use with caution)

**Use Case:** Adapt to screen size or number of items

### PopupWidth Property

Controls suggestion list width:

```razor
<SfMention TItem="PersonData" 
           DataSource="@ComplexData"
           MentionChar="@MentionCharAt"
           PopupWidth="350px">
    <TargetComponent>
        <div id="widePopup" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="DisplayText"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    
    List<PersonData> ComplexData = new();
    
    public class PersonData
    {
        public string DisplayText { get; set; } // "Name - Department - Email"
    }
}
```

**Options:**
- `auto` → Matches target width (default)
- `250px` → Fixed narrow width
- `100%` → Full target width
- `500px` → Custom width

**Use Case:** Wide templates with multiple columns of data

### Responsive Dimensions

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           MentionChar="@MentionCharAt"
           PopupHeight="@GetPopupHeight()"
           PopupWidth="@GetPopupWidth()">
    <TargetComponent>
        <div id="responsive" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    
    private string GetPopupHeight()
    {
        // Adjust based on screen size
        return System.Environment.OSVersion.Platform == PlatformID.MacOSX ? "200px" : "300px";
    }

    private string GetPopupWidth()
    {
        return "auto";
    }

    List<PersonData> TeamMembers = new();
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

---

## Suffix Text

### SuffixText Property

Appends text after selected mention:

#### Add Space After Mention

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           SuffixText=" ">
    <TargetComponent>
        <div id="spaceSuffix" contenteditable="true" placeholder="Mention someone..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> TeamMembers = new()
    {
        new() { Name = "Alice" },
        new() { Name = "Bob" }
    };
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**Result:** Select "Alice" → Text: "Alice " (space appended)

#### Add Newline After Mention

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           SuffixText="\n">
    <TargetComponent>
        <textarea id="newlineSuffix" placeholder="Mention someone..."></textarea>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>
```

**Result:** Select "Alice" → Cursor moves to next line after mention

#### Custom Suffix

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           SuffixText=", ">
    <TargetComponent>
        <div id="customSuffix" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>
```

**Result:** Select "Alice", then "Bob" → "Alice, Bob, " (comma-separated)

---

## Complete Customization Example

### Comment System with All Customizations

```razor
<SfMention TItem="UserData" 
           DataSource="@TeamUsers"
           MentionChar="@MentionCharAt"
           ShowMentionChar="false"
           SuffixText=" "
           RequireLeadingSpace="false"
           FilterType="FilterType.StartsWith"
           MinLength="2"
           PopupHeight="300px"
           PopupWidth="350px"
           SuggestionCount="15"
           OnActionComplete="OnDataLoaded">
    <TargetComponent>
        <div id="comment" 
             contenteditable="true" 
             placeholder="Type @ to mention a team member..."
             style="border: 1px solid #ddd; padding: 12px; border-radius: 4px; min-height: 100px; background: white;">
        </div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="FullName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    private char MentionCharAt = '@';
    
    public class UserData
    {
        public int UserId { get; set; }
        public string FullName { get; set; }
        public string Email { get; set; }
    }

    List<UserData> TeamUsers = new()
    {
        new() { UserId = 1, FullName = "Alice Johnson", Email = "alice@company.com" },
        new() { UserId = 2, FullName = "Bob Smith", Email = "bob@company.com" },
        new() { UserId = 3, FullName = "Carol White", Email = "carol@company.com" }
    };

    void OnDataLoaded(ActionCompleteEventArgs<UserData> args)
    {
        Console.WriteLine($"Suggestion list loaded with {args.Result.Count()} items");
    }
}
```

**Features:**
- `@` triggers mentions, minimal keystroke
- No leading space required (user-friendly)
- Space appended after mention (natural typing)
- First-letter search (StartsWith)
- Minimum 2 characters before suggestions
- 350px wide popup (visible for complex data)
- Shows max 15 suggestions (performance)

---

## Configuration Quick Reference

| Property | Default | Example | Purpose |
|----------|---------|---------|---------|
| MentionChar | @ | # | Trigger character |
| ShowMentionChar | false | true | Display trigger in mention |
| SuffixText | - | " " | Text after mention |
| RequireLeadingSpace | false | true | Space before trigger |
| PopupHeight | 300px | 250px | Dropdown height |
| PopupWidth | auto | 350px | Dropdown width |
| FilterType | Contains | StartsWith | Search strategy |
| MinLength | 0 | 2 | Minimum search chars |
| SuggestionCount | 25 | 15 | Max results shown |

---

## Next Steps

- **Add templates:** See [Templates](../templates.md) for advanced display
- **Explore filtering:** Check [Filtering & Search](../filtering-and-search.md) for more control
- **Bind data:** Review [Working with Data](../working-with-data.md) for data sources
