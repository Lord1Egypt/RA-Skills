# Accessibility and Localization

## Table of Contents

- [Accessibility and Localization](#accessibility-and-localization)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Keyboard Navigation](#keyboard-navigation)
  - [ARIA Attributes](#aria-attributes)
  - [Screen Reader Support](#screen-reader-support)
  - [Focus Management](#focus-management)
  - [Localization Setup](#localization-setup)
    - [Installing CLDR Data](#installing-cldr-data)
    - [Loading Culture-Specific Data](#loading-culture-specific-data)
    - [Setting the Locale](#setting-the-locale)
  - [RTL Support](#rtl-support)
  - [Date/Time Format Localization](#datetime-format-localization)
    - [Date Format](#date-format)
    - [Time Format](#time-format)
    - [First Day of Week](#first-day-of-week)
  - [Custom Locale Strings](#custom-locale-strings)
    - [Available Locale Keys](#available-locale-keys)
    - [Loading Custom Locale Strings](#loading-custom-locale-strings)

## Overview

The Syncfusion React Scheduler is designed with comprehensive accessibility and localization features to ensure usability for all users across different regions and abilities. The component follows WAI-ARIA specifications and supports internationalization (i18n) for global applications.

**Accessibility Features:**
- WAI-ARIA compliant with appropriate roles, states, and properties
- Full keyboard navigation support
- Screen reader compatibility with announcements for user actions
- Focus management for interactive elements
- WCAG 2.2 and Section 508 compliance

**Localization Features:**
- Support for multiple cultures and languages
- Date and time format customization
- RTL (Right-to-Left) layout support
- Customizable locale strings for UI text
- Unicode CLDR-based globalization

The Scheduler requires an ARIA-compliant browser and a running screen reader for optimal accessibility support.

## Keyboard Navigation

The Scheduler provides comprehensive keyboard navigation support through the `allowKeyboardInteraction` property, which is enabled by default (`true`). All Scheduler actions can be controlled via keyboard shortcuts.

**Essential Keyboard Shortcuts:**

| Keys | Description |
|------|-------------|
| <kbd>Alt</kbd> + <kbd>j</kbd> | Focuses the Scheduler element (provided from application end) |
| <kbd>Tab</kbd> | Moves focus to the first/active item on header bar, then to event elements |
| <kbd>Shift</kbd> + <kbd>Tab</kbd> | Reverse tab navigation - focuses elements in backward direction |
| <kbd>Enter</kbd> | Opens quick info popup on selected cells or events |
| <kbd>Escape</kbd> | Closes any open popup or dialog |
| <kbd>Space</kbd> or <kbd>Enter</kbd> | Activates the currently focused item |

**Navigation Shortcuts:**

| Keys | Description |
|------|-------------|
| <kbd>Arrow</kbd> Keys | Navigate to adjacent cells (left, right, up, down) |
| <kbd>Shift</kbd> + <kbd>Arrow</kbd> | Select multiple cells in any direction |
| <kbd>Ctrl</kbd> + <kbd>Left Arrow</kbd> | Navigate to previous date period |
| <kbd>Ctrl</kbd> + <kbd>Right Arrow</kbd> | Navigate to next date period |
| <kbd>Left</kbd>/<kbd>Right Arrow</kbd> | Navigate between header bar items when focused |
| <kbd>Page Up</kbd> & <kbd>Page Down</kbd> | Scroll through work cells area |
| <kbd>Home</kbd> | Move selection to the first cell of Scheduler |

**View and Action Shortcuts:**

| Keys | Description |
|------|-------------|
| <kbd>Alt</kbd> + <kbd>Number</kbd> (1-6) | Switch between Scheduler views |
| <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>Y</kbd> | Navigate to today's date |
| <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>N</kbd> | Open editor window for new event |
| <kbd>Delete</kbd> | Delete one or more selected events |
| <kbd>Ctrl</kbd> + <kbd>Click</kbd> | Select multiple events |

**Implementation Example:**

```typescript
import { ScheduleComponent, Inject, Day, Week, Month } from '@syncfusion/ej2-react-schedule';

function App() {
  return (
    <ScheduleComponent
      allowKeyboardInteraction={true} // Default is true
      selectedDate={new Date()}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
}
```

## ARIA Attributes

The Scheduler implements proper ARIA attributes to ensure semantic meaning and accessibility for assistive technologies. The parent element is assigned a `role="main"` to denote it as the main content component.

**ARIA Attributes Implementation:**

| Attribute | Element | Description |
|-----------|---------|-------------|
| `role="main"` | Scheduler parent | Identifies the Scheduler as the main and unique content of the document |
| `role="button"` | Appointment elements | Denotes appointments as clickable interactive elements |
| `aria-label` | Scheduler parent | Contains the current date; updates dynamically on navigation |
| `aria-label` | Navigation buttons | Describes the purpose of previous/next navigation buttons |
| `aria-label` | Date range display | Describes the date range shown in the header bar |
| `aria-label` | Appointment elements | Provides descriptive information about events |
| `aria-labelledby` | Editor dialog | Indicates dialog title to assistive technologies |
| `aria-describedby` | Editor dialog | Provides dialog content description to assistive technologies |
| `aria-disabled` | Appointment elements | Indicates disabled state of appointments in the Scheduler |

**Dynamic ARIA Updates:**
- The `aria-label` on the Scheduler parent element updates automatically whenever users navigate to different dates
- Navigation actions and date changes are announced to screen readers in real-time
- Interactive elements receive appropriate ARIA states based on user interactions

**Example Structure:**

```html
<!-- Scheduler with ARIA attributes -->
<div role="main" aria-label="Scheduler, March 23, 2026" class="e-schedule">
  <div class="e-toolbar">
    <button aria-label="Previous date navigation">Previous</button>
    <div aria-label="March 23 - 29, 2026">March 23 - 29, 2026</div>
    <button aria-label="Next date navigation">Next</button>
  </div>
  <div class="e-content">
    <div role="button" aria-label="Meeting with team at 10:00 AM">
      Meeting with team
    </div>
  </div>
</div>
```

## Screen Reader Support

The Scheduler provides comprehensive screen reader support with real-time announcements for all user interactions and navigation actions. This ensures users with visual impairments can effectively use all Scheduler features.

**Announced Actions:**
- Date navigation and current date display
- View changes (Day, Week, Month, etc.)
- Appointment creation, editing, and deletion
- Cell selection and navigation
- Popup dialogs and quick info displays
- Error messages and validation feedback

**Screen Reader Requirements:**
- ARIA-compliant browser (Chrome, Firefox, Edge, Safari)
- Active screen reader software (JAWS, NVDA, VoiceOver, TalkBack)

**Best Practices for Screen Reader Support:**

1. **Meaningful Event Titles**: Always provide descriptive titles for appointments
   ```typescript
   const events = [{
     Subject: 'Team Meeting - Q1 Planning', // Descriptive title
     StartTime: new Date(2026, 2, 24, 10, 0),
     EndTime: new Date(2026, 2, 24, 11, 0)
   }];
   ```

2. **Accessible Editor Templates**: When using custom editor templates, include appropriate labels
   ```typescript
   function editorTemplate(props) {
     return (
       <div>
         <label htmlFor="event-title">Event Title</label>
         <input id="event-title" aria-label="Event title" />
       </div>
     );
   }
   ```

3. **Status Announcements**: Use the Scheduler's built-in announcements for operations
   ```typescript
   // Scheduler automatically announces:
   // "Event created successfully"
   // "Event updated"
   // "Event deleted"
   ```

**Testing Screen Reader Support:**
- Test with multiple screen readers (JAWS, NVDA on Windows; VoiceOver on macOS/iOS)
- Verify all interactive elements are announced correctly
- Ensure navigation actions provide adequate feedback
- Test form validation and error message announcements

## Focus Management

The Scheduler implements robust focus management to ensure keyboard users can navigate efficiently and maintain awareness of their current position within the component.

**Focus Behavior:**

1. **Initial Focus**
   - Use <kbd>Alt</kbd> + <kbd>j</kbd> to set initial focus on the Scheduler (application-provided)
   - Focus moves to the first interactive element in the header bar

2. **Focus Order**
   ```
   Header Bar → Previous Button → Date Display → Next Button → 
   View Buttons → Event Elements → Work Cells
   ```

3. **Focus Indicators**
   - Visible focus outline on all interactive elements
   - Clear visual distinction for focused cells and appointments
   - Focus persists during keyboard navigation

4. **Focus Trapping in Dialogs**
   - Quick info popup and editor dialogs trap focus
   - <kbd>Tab</kbd> cycles through dialog elements
   - <kbd>Escape</kbd> returns focus to the triggering element

**Focus Management Example:**

```typescript
import { ScheduleComponent, Inject, Day, Week } from '@syncfusion/ej2-react-schedule';
import { useEffect, useRef } from 'react';

function App() {
  const scheduleRef = useRef(null);

  useEffect(() => {
    // Programmatically set focus to Scheduler
    if (scheduleRef.current) {
      scheduleRef.current.element.focus();
    }
  }, []);

  return (
    <ScheduleComponent
      ref={scheduleRef}
      selectedDate={new Date()}
      allowKeyboardInteraction={true}
    >
      <Inject services={[Day, Week]} />
    </ScheduleComponent>
  );
}
```

**Focus Styling Customization:**

```css
/* Customize focus indicator */
.e-schedule .e-work-cells:focus,
.e-schedule .e-appointment:focus {
  outline: 2px solid #0078d4;
  outline-offset: 2px;
}

/* Ensure sufficient color contrast for focus */
.e-schedule .e-selected-cell {
  border: 2px solid #000;
  background-color: #e3f2fd;
}
```

## Localization Setup

The Scheduler supports comprehensive internationalization (i18n) through the Syncfusion Internationalization library, enabling date/time formatting and parsing based on official Unicode CLDR data.

### Installing CLDR Data

Install the CLDR data package via npm:

```bash
npm install @syncfusion/ej2-cldr-data --save
```

The culture-specific JSON data will be available at:
```
node_modules/@syncfusion/ej2-cldr-data/
```

### Loading Culture-Specific Data

Import and load the required culture data files using the `loadCldr` method:

**Required CLDR Files:**
1. `numberingSystems.json` - Number system definitions
2. `ca-gregorian.json` - Calendar and date patterns
3. `numbers.json` - Number formatting rules
4. `timeZoneNames.json` - Time zone information

**Example: French (Switzerland) Locale**

```typescript
import { loadCldr } from '@syncfusion/ej2-base';
import frNumberData from '@syncfusion/ej2-cldr-data/main/fr-CH/numbers.json';
import frTimeZoneData from '@syncfusion/ej2-cldr-data/main/fr-CH/timeZoneNames.json';
import frGregorian from '@syncfusion/ej2-cldr-data/main/fr-CH/ca-gregorian.json';
import frNumberingSystem from '@syncfusion/ej2-cldr-data/supplemental/numberingSystems.json';

// Load CLDR data before creating Scheduler
loadCldr(frNumberData, frTimeZoneData, frGregorian, frNumberingSystem);
```

### Setting the Locale

Configure the Scheduler to use the loaded locale using the `locale` property:

```typescript
import React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { loadCldr } from '@syncfusion/ej2-base';
import { scheduleData } from './datasource';

// Import and load CLDR data
import frNumberData from '@syncfusion/ej2-cldr-data/main/fr-CH/numbers.json';
import frTimeZoneData from '@syncfusion/ej2-cldr-data/main/fr-CH/timeZoneNames.json';
import frGregorian from '@syncfusion/ej2-cldr-data/main/fr-CH/ca-gregorian.json';
import frNumberingSystem from '@syncfusion/ej2-cldr-data/supplemental/numberingSystems.json';

loadCldr(frNumberData, frTimeZoneData, frGregorian, frNumberingSystem);

function App() {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent
      height='550px'
      selectedDate={new Date(2018, 1, 15)}
      locale='fr-CH' // Set French (Switzerland) locale
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, Month]} />
    </ScheduleComponent>
  );
}

export default App;
```

**Multiple Locale Support:**

```typescript
// Load multiple locales for language switching
import deNumberData from '@syncfusion/ej2-cldr-data/main/de/numbers.json';
import deTimeZoneData from '@syncfusion/ej2-cldr-data/main/de/timeZoneNames.json';
import deGregorian from '@syncfusion/ej2-cldr-data/main/de/ca-gregorian.json';

import esNumberData from '@syncfusion/ej2-cldr-data/main/es/numbers.json';
import esTimeZoneData from '@syncfusion/ej2-cldr-data/main/es/timeZoneNames.json';
import esGregorian from '@syncfusion/ej2-cldr-data/main/es/ca-gregorian.json';

// Load all locales
loadCldr(
  frNumberData, frTimeZoneData, frGregorian,
  deNumberData, deTimeZoneData, deGregorian,
  esNumberData, esTimeZoneData, esGregorian,
  frNumberingSystem
);

// Switch locale dynamically
<ScheduleComponent locale={selectedLocale} ... />
```

## RTL Support

The Scheduler supports Right-to-Left (RTL) layouts for languages like Arabic, Hebrew, and Persian using the `enableRtl` property.

**Enabling RTL Mode:**

```typescript
import React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { scheduleData } from './datasource';

function App() {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent
      height='550px'
      selectedDate={new Date(2018, 1, 15)}
      enableRtl={true} // Enable RTL layout
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek]} />
    </ScheduleComponent>
  );
}

export default App;
```

**RTL with Arabic Locale:**

```typescript
import { loadCldr, L10n } from '@syncfusion/ej2-base';
import arNumberData from '@syncfusion/ej2-cldr-data/main/ar/numbers.json';
import arTimeZoneData from '@syncfusion/ej2-cldr-data/main/ar/timeZoneNames.json';
import arGregorian from '@syncfusion/ej2-cldr-data/main/ar/ca-gregorian.json';
import numberingSystem from '@syncfusion/ej2-cldr-data/supplemental/numberingSystems.json';

// Load Arabic CLDR data
loadCldr(arNumberData, arTimeZoneData, arGregorian, numberingSystem);

// Load Arabic locale strings
L10n.load({
  'ar': {
    'schedule': {
      'day': 'يوم',
      'week': 'أسبوع',
      'month': 'شهر',
      'today': 'اليوم',
      // ... more translations
    }
  }
});

function App() {
  return (
    <ScheduleComponent
      locale='ar'
      enableRtl={true}
      selectedDate={new Date()}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
}
```

**RTL Layout Effects:**
- Navigation buttons flip position (Previous on right, Next on left)
- Header bar elements align to the right
- Time axis displays from right to left
- Event elements flow from right to left
- Popup dialogs and editor windows respect RTL layout

## Date/Time Format Localization

The Scheduler provides flexible date and time format customization to match regional preferences and standards.

### Date Format

Customize the date display format using the `dateFormat` property. The Scheduler supports all valid date format patterns.

**Default Behavior:**
- Default format: `MM/dd/yyyy` (based on `en-US` locale)
- Format automatically adjusts based on the `locale` property if `dateFormat` is not specified

**Custom Date Format Example:**

```typescript
import { ScheduleComponent, Inject, Day, Week, Month } from '@syncfusion/ej2-react-schedule';

function App() {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent
      height='550px'
      selectedDate={new Date(2018, 1, 15)}
      dateFormat="yyyy/MM/dd" // Custom format: 2018/02/15
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
}
```

**Common Date Format Patterns:**

| Format Pattern | Example Output | Description |
|----------------|----------------|-------------|
| `MM/dd/yyyy` | 03/23/2026 | US format (default) |
| `dd/MM/yyyy` | 23/03/2026 | European format |
| `yyyy-MM-dd` | 2026-03-23 | ISO format |
| `yyyy/MM/dd` | 2026/03/23 | Japanese format |
| `dd.MM.yyyy` | 23.03.2026 | German format |
| `MMMM dd, yyyy` | March 23, 2026 | Long format |

### Time Format

Customize time display using the `timeFormat` property. The default time format is determined by the locale (12-hour for `en-US`, 24-hour for most other locales).

**24-Hour Format Example:**

```typescript
function App() {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent
      height='550px'
      selectedDate={new Date(2018, 1, 15)}
      timeFormat="HH:mm" // 24-hour format: 14:30
      eventSettings={eventSettings}
    >
      <Inject services={[Day, Week, Month]} />
    </ScheduleComponent>
  );
}
```

**Common Time Format Patterns:**

| Format Pattern | Example Output | Description |
|----------------|----------------|-------------|
| `h:mm a` | 2:30 PM | 12-hour with AM/PM (default for en-US) |
| `hh:mm a` | 02:30 PM | 12-hour with leading zero |
| `HH:mm` | 14:30 | 24-hour format |
| `HH:mm:ss` | 14:30:45 | 24-hour with seconds |

> **Note:** The `timeFormat` property only accepts valid time format patterns. Invalid patterns will be ignored.

### First Day of Week

Set the first day of the week using the `firstDayOfWeek` property to match regional calendar conventions.

**Day Numbering:**
- 0 = Sunday
- 1 = Monday
- 2 = Tuesday
- 3 = Wednesday
- 4 = Thursday
- 5 = Friday
- 6 = Saturday

**Example: Week Starting on Wednesday**

```typescript
function App() {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent
      height='550px'
      selectedDate={new Date(2018, 1, 15)}
      firstDayOfWeek={3} // Start week on Wednesday
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Week, WorkWeek, Month]} />
    </ScheduleComponent>
  );
}
```

**Regional First Day Conventions:**

| Region | First Day | Value |
|--------|-----------|-------|
| United States, Canada | Sunday | 0 |
| Most of Europe, China, Australia | Monday | 1 |
| Middle East (some countries) | Saturday | 6 |

## Custom Locale Strings

The Scheduler allows customization of all static text through the L10n (Localization) library. This enables complete translation of the UI for any language.

### Available Locale Keys

The Scheduler uses two main locale namespaces: `schedule` and `recurrenceeditor`.

**Schedule Locale Keys:**

```typescript
{
  "schedule": {
    // View names
    "day": "Day",
    "week": "Week",
    "workWeek": "Work Week",
    "month": "Month",
    "year": "Year",
    "agenda": "Agenda",
    "weekAgenda": "Week Agenda",
    "workWeekAgenda": "Work Week Agenda",
    "monthAgenda": "Month Agenda",
    
    // Timeline views
    "timelineDay": "Timeline Day",
    "timelineWeek": "Timeline Week",
    "timelineWorkWeek": "Timeline Work Week",
    "timelineMonth": "Timeline Month",
    "timelineYear": "Timeline Year",
    
    // Navigation
    "today": "Today",
    "previous": "Previous",
    "next": "Next",
    
    // Event messages
    "noEvents": "No events",
    "emptyContainer": "There are no events scheduled on this day.",
    
    // Event fields
    "allDay": "All day",
    "start": "Start",
    "end": "End",
    "subject": "Subject",
    "title": "Title",
    "location": "Location",
    "description": "Description",
    "timezone": "Timezone",
    "startTimezone": "Start Timezone",
    "endTimezone": "End Timezone",
    "repeat": "Repeat",
    
    // Actions
    "more": "more",
    "moreEvents": "More Events",
    "moreDetails": "More Details",
    "close": "Close",
    "cancel": "Cancel",
    "save": "Save",
    "delete": "Delete",
    "edit": "Edit",
    "createEvent": "Create",
    "newEvent": "New Event",
    "addTitle": "Add title",
    "noTitle": "(No Title)",
    
    // Dialog titles
    "deleteEvent": "Delete Event",
    "deleteMultipleEvent": "Delete Multiple Events",
    "deleteSeries": "Delete Series",
    "editEvent": "Edit Event",
    "editSeries": "Edit Series",
    "editFollowingEvent": "Following Events",
    "editTitle": "Edit Event",
    "deleteTitle": "Delete Event",
    
    // Button labels
    "saveButton": "Save",
    "cancelButton": "Cancel",
    "deleteButton": "Delete",
    "ok": "Ok",
    "yes": "Yes",
    "no": "No",
    
    // Recurrence
    "recurrence": "Recurrence",
    "editRecurrence": "Edit Recurrence",
    "repeats": "Repeats",
    "occurrence": "Occurrence",
    "series": "Series",
    
    // Messages and alerts
    "alert": "Alert",
    "selectedItems": "Items selected",
    "editContent": "Do you want to edit only this event or entire series?",
    "deleteRecurrenceContent": "Do you want to delete only this event or entire series?",
    "deleteContent": "Are you sure you want to delete this event?",
    "deleteMultipleContent": "Are you sure you want to delete the selected events?",
    "wrongPattern": "The recurrence pattern is not valid.",
    "startEndError": "The selected end date occurs before the start date.",
    "invalidDateError": "The entered date value is invalid.",
    "blockAlert": "Events cannot be scheduled within the blocked time range.",
    "sameDayAlert": "Two occurrences of the same event cannot occur on the same day.",
    "occurenceAlert": "Cannot reschedule an occurrence of the recurring appointment if it skips over a later occurrence of the same appointment.",
    "createError": "The duration of the event must be shorter than how frequently it occurs. Shorten the duration, or change the recurrence pattern in the recurrence event editor.",
    "recurrenceDateValidation": "Some months have fewer than the selected date. For these months, the occurrence will fall on the last date of the month.",
    "seriesChangeAlert": "The changes made to specific instances of this series will be cancelled and those events will match the series again.",
    
    // Other
    "beginFrom": "Begin From",
    "endAt": "End At",
    "searchTimezone": "Search Timezone",
    "noRecords": "No records found",
    "of": "of",
    "expandAllDaySection": "Expand",
    "collapseAllDaySection": "Collapse"
  }
}
```

**Recurrence Editor Locale Keys:**

```typescript
{
  "recurrenceeditor": {
    "none": "None",
    "daily": "Daily",
    "weekly": "Weekly",
    "monthly": "Monthly",
    "month": "Month",
    "yearly": "Yearly",
    "never": "Never",
    "until": "Until",
    "count": "Count",
    "first": "First",
    "second": "Second",
    "third": "Third",
    "fourth": "Fourth",
    "last": "Last",
    "repeat": "Repeat",
    "repeatEvery": "Repeat Every",
    "on": "Repeat On",
    "end": "End",
    "onDay": "Day",
    "days": "Day(s)",
    "weeks": "Week(s)",
    "months": "Month(s)",
    "years": "Year(s)",
    "every": "every",
    "summaryTimes": "time(s)",
    "summaryOn": "on",
    "summaryUntil": "until",
    "summaryRepeat": "Repeats",
    "summaryDay": "day(s)",
    "summaryWeek": "week(s)",
    "summaryMonth": "month(s)",
    "summaryYear": "year(s)"
  }
}
```

### Loading Custom Locale Strings

Use the `L10n.load()` method to register custom locale strings before creating the Scheduler component.

**Example: French Locale Strings**

```typescript
import React from 'react';
import {
  ScheduleComponent, Day, Week, WorkWeek, Month, Inject,
  ViewsDirective, ViewDirective
} from '@syncfusion/ej2-react-schedule';
import { L10n, loadCldr } from '@syncfusion/ej2-base';
import { scheduleData } from './datasource';

// Import CLDR data
import frNumberData from '@syncfusion/ej2-cldr-data/main/fr-CH/numbers.json';
import frTimeZoneData from '@syncfusion/ej2-cldr-data/main/fr-CH/timeZoneNames.json';
import frGregorian from '@syncfusion/ej2-cldr-data/main/fr-CH/ca-gregorian.json';
import frNumberingSystem from '@syncfusion/ej2-cldr-data/supplemental/numberingSystems.json';

// Load CLDR data
loadCldr(frNumberData, frTimeZoneData, frGregorian, frNumberingSystem);

// Load French locale strings
L10n.load({
  'fr-CH': {
    'schedule': {
      'day': 'Jour',
      'week': 'Semaine',
      'workWeek': 'Semaine de travail',
      'month': 'Mois',
      'year': 'Année',
      'agenda': 'Ordre du jour',
      'today': "Aujourd'hui",
      'noEvents': 'Aucun événement',
      'emptyContainer': "Aucun événement n'est prévu pour ce jour.",
      'allDay': 'Toute la journée',
      'start': 'Début',
      'end': 'Fin',
      'more': 'plus',
      'close': 'Fermer',
      'cancel': 'Annuler',
      'noTitle': '(Sans titre)',
      'delete': 'Supprimer',
      'deleteEvent': "Supprimer l'événement",
      'deleteMultipleEvent': 'Supprimer plusieurs événements',
      'selectedItems': 'Éléments sélectionnés',
      'deleteSeries': 'Supprimer la série',
      'edit': 'Modifier',
      'editSeries': 'Modifier la série',
      'editEvent': "Modifier l'événement",
      'createEvent': 'Créer',
      'subject': 'Sujet',
      'addTitle': 'Ajouter un titre',
      'moreDetails': 'Plus de détails',
      'save': 'Enregistrer',
      'editContent': 'Voulez-vous modifier uniquement cet événement ou toute la série?',
      'deleteRecurrenceContent': 'Voulez-vous supprimer uniquement cet événement ou toute la série?',
      'deleteContent': 'Êtes-vous sûr de vouloir supprimer cet événement?',
      'deleteMultipleContent': 'Êtes-vous sûr de vouloir supprimer les événements sélectionnés?',
      'newEvent': 'Nouvel événement',
      'title': 'Titre',
      'location': 'Lieu',
      'description': 'Description',
      'timezone': 'Fuseau horaire',
      'startTimezone': 'Fuseau horaire de début',
      'endTimezone': 'Fuseau horaire de fin',
      'repeat': 'Répéter',
      'saveButton': 'Enregistrer',
      'cancelButton': 'Annuler',
      'deleteButton': 'Supprimer',
      'recurrence': 'Récurrence',
      'wrongPattern': "Le modèle de récurrence n'est pas valide.",
      'ok': 'Ok',
      'yes': 'Oui',
      'no': 'Non'
    },
    'recurrenceeditor': {
      'none': 'Aucun',
      'daily': 'Quotidien',
      'weekly': 'Hebdomadaire',
      'monthly': 'Mensuel',
      'yearly': 'Annuel',
      'never': 'Jamais',
      'until': "Jusqu'à",
      'count': 'Nombre',
      'first': 'Premier',
      'second': 'Deuxième',
      'third': 'Troisième',
      'fourth': 'Quatrième',
      'last': 'Dernier',
      'repeat': 'Répéter',
      'repeatEvery': 'Répéter tous les',
      'on': 'Répéter le',
      'end': 'Fin',
      'onDay': 'Jour',
      'days': 'Jour(s)',
      'weeks': 'Semaine(s)',
      'months': 'Mois',
      'years': 'Année(s)',
      'every': 'tous les',
      'summaryTimes': 'fois',
      'summaryOn': 'le',
      'summaryUntil': "jusqu'à",
      'summaryRepeat': 'Répète',
      'summaryDay': 'jour(s)',
      'summaryWeek': 'semaine(s)',
      'summaryMonth': 'mois',
      'summaryYear': 'année(s)'
    }
  }
});

function App() {
  const eventSettings = { dataSource: scheduleData };

  return (
    <ScheduleComponent
      height='550px'
      selectedDate={new Date(2018, 1, 15)}
      locale='fr-CH'
      eventSettings={eventSettings}
    >
      <ViewsDirective>
        <ViewDirective option='Day' />
        <ViewDirective option='Week' />
        <ViewDirective option='WorkWeek' />
        <ViewDirective option='Month' />
      </ViewsDirective>
      <Inject services={[Day, Week, WorkWeek, Month]} />
    </ScheduleComponent>
  );
}

export default App;
```

**Loading from External JSON File:**

```typescript
import { Ajax, L10n } from '@syncfusion/ej2-base';

// Load locale strings from external file
let localeTexts: string;
let ajax: Ajax = new Ajax('./locale.json', 'GET', false);
ajax.onSuccess = (value: string) => {
  localeTexts = value;
};
ajax.send();
L10n.load(JSON.parse(localeTexts));
```

**External JSON File Structure (locale.json):**

```json
{
  "fr-CH": {
    "schedule": {
      "day": "Jour",
      "week": "Semaine",
      ...
    },
    "recurrenceeditor": {
      "none": "Aucun",
      ...
    }
  },
  "de-DE": {
    "schedule": {
      "day": "Tag",
      "week": "Woche",
      ...
    }
  }
}
```

**Summary:**
This reference provides comprehensive guidance for implementing accessibility and localization features in the Syncfusion React Scheduler. By following these guidelines, you can create inclusive, globally-ready scheduling applications that meet WCAG 2.2 standards and support diverse user needs across different regions and abilities.
