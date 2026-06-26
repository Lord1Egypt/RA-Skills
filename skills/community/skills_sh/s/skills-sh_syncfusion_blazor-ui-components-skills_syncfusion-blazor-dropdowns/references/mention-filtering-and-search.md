# Filtering & Search in Blazor Mention Component

## Table of Contents
- [Overview](#overview)
- [Minimum Filter Characters](#minimum-filter-characters)
- [Filter Type Strategies](#filter-type-strategies)
- [Space Handling](#space-handling)
- [Result Limiting](#result-limiting)
- [Common Filtering Patterns](#common-filtering-patterns)

---

## Overview

The Mention component provides several properties to control how suggestion filtering works:
- **MinLength:** Minimum characters before suggestions appear
- **FilterType:** Search strategy (StartsWith, Contains, EndsWith)
- **AllowSpaces:** Whether spaces trigger filtering
- **SuggestionCount:** Maximum items displayed

These settings help reduce API calls, focus results, and improve user experience.

---

## Minimum Filter Characters

### Why Use MinLength?

Typing just `@a` returns many suggestions. Requiring 2-3 characters reduces results and API calls:

```razor
<SfMention TItem="PersonData" 
           DataSource="@Employees"
           MinLength="2">
    <TargetComponent>
        <div id="mention" contenteditable="true" placeholder="Type @ + 2 chars..."></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> Employees = new();
}
```

**Behavior:**
- Type `@a` → No suggestions (< 2 chars)
- Type `@al` → Shows "Alice", "Alexander" (≥ 2 chars)
- Type `@ali` → Shows only "Alice"

### Remote Data with MinLength

Especially important for large datasets or slow APIs:

```razor
<SfMention TItem="UserData" MinLength="3">
    <TargetComponent>
        <input id="remoteUser" type="text" placeholder="Type @ + 3 chars..." />
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT" 
                       Adaptor="Adaptors.WebApiAdaptor">
        </SfDataManager>
        <MentionFieldSettings Text="UserName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class UserData
    {
        public int UserId { get; set; }
        public string UserName { get; set; }
    }
}
```

**Result:** Only fetches from API after 3+ characters, reducing server load.

---

## Filter Type Strategies

The Mention component supports three filter strategies to find matching items:

### StartsWith (Prefix Matching)

Suggestions must start with the typed characters:

```razor
<SfMention TItem="PersonData" 
           DataSource="@Employees"
           FilterType="FilterType.StartsWith">
    <TargetComponent>
        <div id="prefixMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> Employees = new()
    {
        new() { Name = "Alice Johnson" },
        new() { Name = "Bob Smith" },
        new() { Name = "Carol Williams" }
    };
}
```

**Examples:**
- Type `@Al` → Shows "Alice Johnson" ✓
- Type `@Joh` → Shows nothing (doesn't start with "Joh") ✗
- Type `@Bob` → Shows "Bob Smith" ✓

**Use Case:** When you expect users to remember first name/character

### Contains (Substring Matching) - Default

Suggestions match anywhere in the text:

```razor
<SfMention TItem="PersonData" 
           DataSource="@Employees"
           FilterType="FilterType.Contains">
    <TargetComponent>
        <div id="containsMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> Employees = new()
    {
        new() { Name = "Alice Johnson" },
        new() { Name = "Bob Smith" },
        new() { Name = "Carol Williams" }
    };
}
```

**Examples:**
- Type `@Joh` → Shows "Alice Johnson" ✓
- Type `@mith` → Shows "Bob Smith" ✓
- Type `@lia` → Shows "Alice Johnson" ✓

**Use Case:** Most flexible, best for general search

### EndsWith (Suffix Matching)

Suggestions must end with the typed characters:

```razor
<SfMention TItem="PersonData" 
           DataSource="@Employees"
           FilterType="FilterType.EndsWith">
    <TargetComponent>
        <div id="endsMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> Employees = new()
    {
        new() { Name = "Alice Johnson" },
        new() { Name = "Bob Smith" },
        new() { Name = "Carol Williams" }
    };
}
```

**Examples:**
- Type `@son` → Shows "Alice Johnson" ✓
- Type `@ith` → Shows "Bob Smith" ✓
- Type `@ace` → Shows nothing ✗

**Use Case:** Less common, useful for finding by surname or domain

### Comparison Table

| Filter Type | Type `@Al` | Type `@mith` | Type `@son` | Best For |
|-------------|-----------|--------------|-----------|----------|
| StartsWith | "Alice Johnson" ✓ | Nothing ✗ | Nothing ✗ | First name search |
| Contains | "Alice Johnson" ✓ | "Bob Smith" ✓ | "Alice Johnson" ✓ | General search (default) |
| EndsWith | Nothing ✗ | "Bob Smith" ✓ | "Alice Johnson" ✓ | Last name/suffix search |

---

## Space Handling

### AllowSpaces Property

Controls whether spaces terminate or continue the mention search:

#### Spaces End Search (Default)

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           AllowSpaces="false">
    <TargetComponent>
        <div id="noSpace" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> TeamMembers = new()
    {
        new() { Name = "John Smith" },
        new() { Name = "Mary Johnson" }
    };
}
```

**Behavior:**
1. Type `@John` → Shows "John Smith"
2. Press **Space** → Mention closes, inserts "@John "
3. Typing more doesn't re-open suggestions

**Use Case:** Simple tagging, one mention per trigger

#### Spaces Continue Search

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           AllowSpaces="true">
    <TargetComponent>
        <div id="withSpace" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>
```

**Behavior:**
1. Type `@John Smith` → Filters while searching full name
2. Space included in search (finds "John Smith")
3. Suggestions update with each character, including spaces

**Use Case:** Full-name searching, multi-word matches

---

## Result Limiting

### SuggestionCount Property

Controls maximum items displayed in dropdown:

```razor
<SfMention TItem="PersonData" 
           DataSource="@AllPersons"
           SuggestionCount="10">
    <TargetComponent>
        <div id="limited" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> AllPersons = new(); // Thousands of items
}
```

**Default:** 25 items
**Common Values:**
- `5-10` → Quick browsing, small lists
- `25` → Default, balanced performance
- `50+` → Large lists, scrollable dropdown

**Benefit:** Better performance with large datasets by limiting DOM elements

---

## Common Filtering Patterns

### Pattern 1: Strict Email Search

For email mentions with exact domain:

```razor
<SfMention TItem="EmployeeData" 
           DataSource="@Employees"
           FilterType="FilterType.Contains"
           MinLength="2"
           SuggestionCount="15">
    <TargetComponent>
        <input id="email" type="text" placeholder="Type @ + email..." />
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Email"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class EmployeeData
    {
        public string Email { get; set; }
        public string FullName { get; set; }
    }

    List<EmployeeData> Employees = new()
    {
        new() { Email = "alice.johnson@company.com", FullName = "Alice Johnson" },
        new() { Email = "bob.smith@company.com", FullName = "Bob Smith" }
    };
}
```

**Result:** Type `@alice` → Shows only "alice.johnson@company.com"

### Pattern 2: Large Team with Performance Optimization

For organizations with 1000+ employees:

```razor
<SfMention TItem="UserData" 
           MinLength="3"
           FilterType="FilterType.StartsWith"
           SuggestionCount="10"
           AllowSpaces="false">
    <TargetComponent>
        <input id="largeTeam" type="text" placeholder="Type @ + 3 letters..." />
    </TargetComponent>
    <ChildContent>
        <SfDataManager Url="YOUR_API_ENDPOINT/employees" 
                       Adaptor="Adaptors.WebApiAdaptor"
                       Offline="true">
        </SfDataManager>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class UserData
    {
        public int UserId { get; set; }
        public string Name { get; set; }
    }
}
```

**Optimizations:**
- `MinLength="3"` → Requires 3 chars before API call
- `SuggestionCount="10"` → Limits to 10 results
- `Offline="true"` → Caches results locally
- `StartsWith` → Predictable, prefix-based search

### Pattern 3: Flexible Search with Spaces

For multi-word full names:

```razor
<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           FilterType="FilterType.Contains"
           MinLength="2"
           AllowSpaces="true"
           SuggestionCount="20">
    <TargetComponent>
        <textarea id="comments" placeholder="Type @ to mention someone..."></textarea>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="FullName"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public int Id { get; set; }
        public string FullName { get; set; }
        public string Department { get; set; }
    }

    List<PersonData> TeamMembers = new()
    {
        new() { Id = 1, FullName = "Alice Johnson", Department = "Engineering" },
        new() { Id = 2, FullName = "Mary Anne Smith", Department = "Marketing" }
    };
}
```

**Examples:**
- `@al` → Shows "Alice Johnson"
- `@mary an` → Shows "Mary Anne Smith" (allows space)
- `@john` → Shows "Alice Johnson" (contains match)

---

## Advanced Filtering Scenario

### Custom Pre-Filtering Before Binding

```razor
@code {
    private List<PersonData> FilteredPersons;
    
    protected override void OnInitialized()
    {
        // Filter data before binding (e.g., active users only)
        var allPersons = FetchAllPersons();
        FilteredPersons = allPersons
            .Where(p => p.IsActive && !string.IsNullOrEmpty(p.Name))
            .ToList();
    }

    private List<PersonData> FetchAllPersons()
    {
        return new()
        {
            new() { Name = "Alice", IsActive = true },
            new() { Name = "Bob", IsActive = false },
            new() { Name = "Carol", IsActive = true }
        };
    }

    public class PersonData
    {
        public string Name { get; set; }
        public bool IsActive { get; set; }
    }
}
```

---

## Next Steps

- **Add templates:** See [Templates](../templates.md) for custom display
- **Explore data:** Check [Working with Data](../working-with-data.md) for more binding options
- **Fine-tune:** Review [Customization](../customization.md) for mention character and suffix settings
