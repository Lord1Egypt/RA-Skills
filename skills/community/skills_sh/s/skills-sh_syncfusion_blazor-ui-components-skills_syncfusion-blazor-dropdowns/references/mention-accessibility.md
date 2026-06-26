# Accessibility in Blazor Mention Component

## Table of Contents
- [Compliance Standards](#compliance-standards)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Mobile Accessibility](#mobile-accessibility)
- [RTL Language Support](#rtl-language-support)
- [Best Practices](#best-practices)

---

## Compliance Standards

The Syncfusion Blazor Mention component meets international accessibility standards:

| Standard | Status | Details |
|----------|--------|---------|
| **WCAG 2.2** | AA Compliant | Level AA accessibility requirements met |
| **Section 508** | Compliant | US federal accessibility requirements |
| **WAI-ARIA** | Fully Supported | Web Accessibility Initiative - Accessible Rich Internet Applications |
| **ADA** | Compliant | Americans with Disabilities Act compliance |
| **Color Contrast** | PASS | Meets minimum color contrast ratios |
| **Keyboard Access** | Full | All functionality accessible via keyboard |
| **Screen Readers** | Supported | Compatible with Jaws, NVDA, VoiceOver |

---

## WAI-ARIA Attributes

### Supported ARIA Attributes

The Mention component automatically implements these ARIA attributes for assistive technology support:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-selected` | Indicates currently selected suggestion | Applied to focused list item |
| `aria-activedescendant` | Holds ID of focused descendant | Points to currently focused option |
| `aria-owns` | Indicates popup list owned by input | Associates input with suggestions list |
| `aria-label` | Descriptive label for screen readers | Auto-generated or custom |
| `aria-describedby` | Associates help text | Optional, for additional context |

### Example ARIA Implementation

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <!-- ARIA attributes automatically added by component -->
        <div id="mention" 
             contenteditable="true" 
             role="combobox"
             aria-label="Mention team member"
             aria-describedby="mention-help"
             aria-expanded="false"
             aria-autocomplete="list">
        </div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

<p id="mention-help" style="display: none;">Type @ to see team members</p>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }

    List<PersonData> TeamMembers = new();
}
```

### Screen Reader Announcements

The component announces:
- "Mention list expanded with 5 results"
- "Alice Johnson selected"
- "No results found"
- Navigation instructions (arrows, enter, escape)

---

## Keyboard Navigation

### Supported Keyboard Shortcuts

Complete keyboard support for all mention operations:

| Key | Windows/Linux | Mac | Function |
|-----|---------------|-----|----------|
| `@` or custom | Any | Any | Trigger suggestion list |
| **↓** (Down Arrow) | ↓ | ↓ | Focus next suggestion |
| **↑** (Up Arrow) | ↑ | ↑ | Focus previous suggestion |
| **Enter** | Enter | Return | Select focused suggestion |
| **Tab** | Tab | Tab | Insert mention or move to next element |
| **Escape** | Esc | Esc | Close suggestion list |
| **Home** | Home | Fn+← | Focus first suggestion |
| **End** | End | Fn+→ | Focus last suggestion |
| **Page Up** | PgUp | Fn+↑ | Scroll up in list |
| **Page Down** | PgDn | Fn+↓ | Scroll down in list |

### Keyboard Navigation Example

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" 
             contenteditable="true" 
             placeholder="Type @ then use arrow keys to navigate"
             role="combobox"
             aria-label="Mention team member">
        </div>
    </TargetComponent>
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

### Keyboard Navigation Workflow

1. **Type `@`** → Suggestion list opens
2. **Press ↓** → Focus moves to "Alice"
3. **Press ↓** → Focus moves to "Bob"
4. **Press Enter** → Inserts "Bob" and closes list
5. **Type ` @`** → Opens list again for another mention
6. **Press Escape** → Closes list without selection

---

## Screen Reader Support

### NVDA (Non-Visual Desktop Access) - Windows

```razor
<!-- When user types @, NVDA announces: -->
<!-- "Mention list, list 3 items" -->

<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<PersonData> TeamMembers = new()
    {
        new() { Name = "Alice" },
        new() { Name = "Bob" },
        new() { Name = "Carol" }
    };
    
    public class PersonData
    {
        public string Name { get; set; }
    }
}
```

**NVDA Announces:**
1. "Mention list, list with 3 items"
2. "Alice, 1 of 3" (on focus)
3. "Bob, 2 of 3" (after ↓)
4. "Alice selected" (after Enter)

### JAWS (Job Access With Speech) - Windows

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true" role="combobox"></div>
    </TargetComponent>
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

**JAWS Announces:**
- "Combobox collapsed"
- "Combobox expanded, 5 suggestions"
- "Suggestion one of five: Alice"
- "Selected Alice"

### VoiceOver - macOS/iOS

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="mention" contenteditable="true"></div>
    </TargetComponent>
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

**VoiceOver Announces:**
- "Editable text"
- "Mention suggestions, list with 5 items"
- "Alice" (with button role)
- "Selected Alice"

---

## Mobile Accessibility

### Touch Navigation

Mention component fully supports touch:
- **Tap** on suggestion → Selects item
- **Swipe** on list → Scrolls through suggestions
- **Long press** → Shows context menu (if available)

### Mobile Screen Reader Support

Works with mobile screen readers:
- **Android:** TalkBack
- **iOS:** VoiceOver
- **iPad:** VoiceOver

### Mobile Implementation

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <textarea id="mention" 
                  placeholder="Type @ to mention"
                  style="font-size: 16px; padding: 12px; width: 100%;">
        </textarea>
    </TargetComponent>
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

**Mobile Best Practices:**
- Font size ≥ 16px (prevents auto-zoom on iOS)
- Sufficient touch target size (44x44px minimum)
- Clear focus indicators
- Simple, responsive layout

---

## RTL Language Support

### Right-to-Left Language Implementation

The Mention component fully supports RTL languages (Arabic, Hebrew, Urdu, etc.):

```razor
<!-- HTML with dir="rtl" -->
<div dir="rtl" lang="ar">
    <SfMention TItem="PersonData" DataSource="@TeamMembers">
        <TargetComponent>
            <div id="mention" 
                 contenteditable="true" 
                 placeholder="اكتب @ لذكر شخص">
            </div>
        </TargetComponent>
        <ChildContent>
            <MentionFieldSettings Text="Name"></MentionFieldSettings>
        </ChildContent>
    </SfMention>
</div>

@code {
    public class PersonData
    {
        public string Name { get; set; }
    }

    List<PersonData> TeamMembers = new()
    {
        new() { Name = "علي" },      // Ali
        new() { Name = "فاطمة" },     // Fatima
        new() { Name = "محمد" }       // Mohammed
    };
}
```

**RTL Features:**
- Text direction automatically reversed
- Suggestions appear left side
- Arrow keys work correctly (← becomes next, → becomes previous)
- RTL text input fully supported

---

## Best Practices

### 1. Provide Clear Labels

```razor
<!-- ✅ Good: Clear, descriptive label -->
<label for="mention-input">Mention team member</label>
<div id="mention-input" contenteditable="true" role="combobox"></div>

<!-- ❌ Poor: No label -->
<div id="mention-input" contenteditable="true"></div>
```

### 2. Include Help Text

```razor
<!-- ✅ Good: Help text with aria-describedby -->
<div id="mention" 
     contenteditable="true"
     aria-describedby="mention-help"
     role="combobox">
</div>
<small id="mention-help">Type @ followed by 2+ characters to find team members</small>

<!-- ❌ Poor: No guidance -->
<div id="mention" contenteditable="true"></div>
```

### 3. Color Contrast

```razor
<!-- ✅ Good: Sufficient contrast -->
<div style="background: white; color: #333;">  <!-- 12.6:1 ratio -->
    Suggestion item
</div>

<!-- ❌ Poor: Insufficient contrast -->
<div style="background: white; color: #ccc;">  <!-- 1.4:1 ratio -->
    Suggestion item
</div>
```

### 4. Focus Indicators

```razor
<!-- ✅ Good: Visible focus indicator -->
<style>
    div[contenteditable]:focus {
        outline: 2px solid #4a90e2;
        outline-offset: 2px;
    }
</style>

<!-- ❌ Poor: No focus indicator -->
<style>
    div[contenteditable]:focus {
        outline: none;
    }
</style>
```

### 5. Error Messages

```razor
<!-- ✅ Good: Linked to input, descriptive -->
<div id="mention" 
     contenteditable="true"
     aria-describedby="mention-error"
     role="combobox">
</div>
<span id="mention-error" role="alert">
    No matching team members found. Try a different search.
</span>

<!-- ❌ Poor: Generic error -->
<p>No results</p>
```

### 6. Test with Real Assistive Technology

```
Testing Checklist:
□ NVDA (Windows)
□ JAWS (Windows)
□ VoiceOver (macOS/iOS)
□ TalkBack (Android)
□ Keyboard-only navigation
□ High contrast mode
□ Zoom at 200%
```

---

## Accessibility Testing

### Manual Testing Steps

1. **Keyboard Only:**
   - Navigate with Tab/Shift+Tab
   - Open list with @
   - Navigate with arrow keys
   - Select with Enter

2. **Screen Reader (NVDA):**
   - Launch NVDA
   - Navigate to Mention component
   - Verify announcements correct
   - Test all keyboard functions

3. **Color Contrast:**
   - Use WebAIM Color Contrast Checker
   - Verify all text meets AA standards
   - Test with Colorblind Simulator

4. **Responsive Design:**
   - Test at 100%, 150%, 200% zoom
   - Test on mobile devices
   - Verify touch targets (44x44px+)

### Automated Testing

```html
<!-- Use Axe DevTools extension -->
<!-- Install: https://www.deque.com/axe/devtools/ -->
<!-- Run scan → Verify 0 violations -->
```

---

## Common Accessibility Issues & Fixes

| Issue | Problem | Solution |
|-------|---------|----------|
| No keyboard access | Can't open list | Add trigger character support, ensure focus management |
| Missing labels | Screen reader confused | Use `aria-label` or linked `<label>` |
| Poor contrast | Hard to read | Ensure 4.5:1 ratio for text on background |
| No focus indicator | Hard to navigate | Add visible outline on focus |
| Mobile text too small | Auto-zoom triggers | Use 16px+ font size |
| RTL not supported | Arabic/Hebrew broken | Add `dir="rtl"` to container |

---

## Compliance Validation

### Browser DevTools Accessibility Inspector

```
Chrome/Edge:
1. Press F12 (Open DevTools)
2. Go to "Accessibility" tab
3. Check "Audit accessibility of this page"
4. Verify no issues found

Firefox:
1. Press F12
2. Go to "Inspector"
3. Click "Accessibility" tab
4. Review accessibility tree
```

---

## Next Steps

- **Customize appearance:** See [Customization](../customization.md)
- **Add templates:** Explore [Templates](../templates.md)
- **Implement filtering:** Check [Filtering & Search](../filtering-and-search.md)
- **Test your implementation** with your target audience and assistive technologies
