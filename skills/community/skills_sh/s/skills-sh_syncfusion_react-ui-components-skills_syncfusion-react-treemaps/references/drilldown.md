# Drill-Down and Navigation

## Table of Contents

- [Enabling Drill-Down](#enabling-drill-down)
  - [Basic Drill-Down Example](#basic-drill-down-example)
  - [How It Works](#how-it-works)
- [Multi-Level Hierarchies](#multi-level-hierarchies)
  - [Three-Level Organization](#three-level-organization)
  - [File System Hierarchy](#file-system-hierarchy)
- [Drill-Down Events](#drill-down-events)
  - [DrillStart Event (Before Drill-Down)](#drillstart-event-before-drill-down)
  - [DrillEnd Event (After Drill-Down)](#drillend-event-after-drill-down)
  - [Complete Event Handler Example](#complete-event-handler-example)
- [Navigation Patterns](#navigation-patterns)
  - [Pattern 1: Guided Drill-Down](#pattern-1-guided-drill-down)
  - [Pattern 2: Auto-Drill to Specific Level](#pattern-2-auto-drill-to-specific-level)
  - [Pattern 3: Tracking Drill Path](#pattern-3-tracking-drill-path)
- [Breadcrumb Navigation](#breadcrumb-navigation)
  - [Custom Breadcrumb Example](#custom-breadcrumb-example)
- [Advanced Drill-Down](#advanced-drill-down)
  - [Conditional Drill-Down Based on Selection](#conditional-drill-down-based-on-selection)
  - [Drill-Down with Dynamic Data Loading](#drill-down-with-dynamic-data-loading)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Enabling Drill-Down

Drill-down enables users to click on items to explore nested levels of hierarchical data.

### Basic Drill-Down Example

```jsx
import { TreeMapComponent, Inject } from '@syncfusion/ej2-react-treemap';
import { LevelsDirective, LevelDirective } from '@syncfusion/ej2-react-treemap';

const data = [
  { Country: 'USA', State: 'California', City: 'Los Angeles', Population: 3990456 },
  { Country: 'USA', State: 'California', City: 'San Francisco', Population: 884363 },
  { Country: 'USA', State: 'Texas', City: 'Houston', Population: 2320268 },
  { Country: 'USA', State: 'Texas', City: 'Dallas', Population: 1343573 },
  { Country: 'Canada', State: 'Ontario', City: 'Toronto', Population: 2930000 },
  { Country: 'Canada', State: 'British Columbia', City: 'Vancouver', Population: 640000 }
];

<TreeMapComponent
  enableDrillDown={true}  // Enable drill-down
  dataSource={data}
  weightValuePath="Population"
  leafItemSettings={{ labelPath: 'City' }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Country" />
    <LevelDirective groupPath="State" />
  </LevelsDirective>
</TreeMapComponent>
```

**Interaction:**
1. Initial view shows countries (USA, Canada)
2. Click a country → shows states within that country
3. Click a state → shows cities within that state

### How It Works

- **enableDrillDown={true}:** Activates click-to-drill behavior
- **Levels define hierarchy:** Each `<LevelDirective>` is a depth level
- **Clicking:** User clicks any item to drill into next level
- **Back button:** Header shows back option to return to previous level

## Multi-Level Hierarchies

Support any number of hierarchy levels for complex data exploration.

### Three-Level Organization

```jsx
const orgData = [
  { Company: 'Tech Corp', Division: 'Engineering', Department: 'Backend', Team: 'API Services', Members: 12 },
  { Company: 'Tech Corp', Division: 'Engineering', Department: 'Backend', Team: 'Database', Members: 8 },
  { Company: 'Tech Corp', Division: 'Engineering', Department: 'Frontend', Team: 'Web', Members: 10 },
  { Company: 'Tech Corp', Division: 'Sales', Department: 'Enterprise', Team: 'Team A', Members: 15 },
  { Company: 'Tech Corp', Division: 'Sales', Department: 'Enterprise', Team: 'Team B', Members: 12 }
];

<TreeMapComponent
  enableDrillDown={true}
  dataSource={orgData}
  weightValuePath="Members"
  leafItemSettings={{ labelPath: 'Team' }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Division" />
    <LevelDirective groupPath="Department" />
  </LevelsDirective>
</TreeMapComponent>
```

**Navigation Flow:**
- Level 0: Shows divisions (Engineering, Sales)
- Level 1: Shows departments within selected division
- Leaf level: Shows teams within selected department

### File System Hierarchy

```jsx
const fileSystemData = [
  { Drive: 'C:', Folder: 'Users', SubFolder: 'Documents', File: 'Resume.pdf', Size: 256 },
  { Drive: 'C:', Folder: 'Users', SubFolder: 'Documents', File: 'CoverLetter.docx', Size: 128 },
  { Drive: 'C:', Folder: 'Users', SubFolder: 'Downloads', File: 'Setup.exe', Size: 5120 },
  { Drive: 'D:', Folder: 'Projects', SubFolder: 'WebApp', File: 'App.jsx', Size: 64 },
  { Drive: 'D:', Folder: 'Media', SubFolder: 'Videos', File: 'Tutorial.mp4', Size: 512000 }
];

<TreeMapComponent
  enableDrillDown={true}
  dataSource={fileSystemData}
  weightValuePath="Size"
  leafItemSettings={{
    labelPath: 'File',
    labelFormat: '${File}\n${Size}KB'
  }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Drive" />
    <LevelDirective groupPath="Folder" />
    <LevelDirective groupPath="SubFolder" />
  </LevelsDirective>
</TreeMapComponent>
```

## Drill-Down Events

Handle drill-down interactions with events to customize behavior.

### DrillStart Event (Before Drill-Down)

```jsx
export function TreeMapWithEvents() {
  const handleDrillStart = (args) => {
    console.log('Drilling into:', args.rowIndex);
    // args.rowIndex: index of clicked item
    // Can prevent drill-down if needed: args.cancel = true
  };

  return (
    <TreeMapComponent
      enableDrillDown={true}
      dataSource={data}
      onDrillStart={handleDrillStart}
    >
      {/* Levels */}
    </TreeMapComponent>
  );
}
```

### DrillEnd Event (After Drill-Down)

```jsx
export function TreeMapDrillEnd() {
  const [currentLevel, setCurrentLevel] = React.useState('root');

  const handleDrillEnd = (args) => {
    console.log('Current level:', args.currentLevel);
    setCurrentLevel(args.currentLevel);
    // Update UI or trigger data loading
  };

  return (
    <div>
      <div>Current Level: {currentLevel}</div>
      <TreeMapComponent
        enableDrillDown={true}
        dataSource={data}
        onDrillEnd={handleDrillEnd}
      >
        {/* Levels */}
      </TreeMapComponent>
    </div>
  );
}
```

### Complete Event Handler Example

```jsx
export function TreeMapEventHandling() {
  const [itemCount, setItemCount] = React.useState(0);

  const handleDrillStart = (args) => {
    console.log('Starting drill-down');
  };

  const handleDrillEnd = (args) => {
    // Update UI based on new level
    const visibleItems = args.drillDownItems?.length || 0;
    setItemCount(visibleItems);
    console.log(`Drilled to level with ${visibleItems} items`);
  };

  return (
    <div>
      <div>Visible Items: {itemCount}</div>
      <TreeMapComponent
        enableDrillDown={true}
        dataSource={data}
        onDrillStart={handleDrillStart}
        onDrillEnd={handleDrillEnd}
      >
        {/* Levels */}
      </TreeMapComponent>
    </div>
  );
}
```

## Navigation Patterns

### Pattern 1: Guided Drill-Down

Only allow drilling into specific items:

```jsx
export function GuidedDrillDown() {
  const handleDrillStart = (args) => {
    // Only allow drilling if item meets criteria
    const item = args.item;
    if (item.Members === undefined) {
      args.cancel = true;  // Prevent drill-down
      alert('Cannot drill into leaf items');
    }
  };

  return (
    <TreeMapComponent
      enableDrillDown={true}
      dataSource={data}
      onDrillStart={handleDrillStart}
    >
      {/* Levels */}
    </TreeMapComponent>
  );
}
```

### Pattern 2: Auto-Drill to Specific Level

Automatically drill when clicking certain items:

```jsx
export function AutoDrill() {
  const treeMapRef = React.useRef(null);

  const handleDrillStart = (args) => {
    // Auto-drill if only one child exists
    if (args.drillDownItems?.length === 1) {
      setTimeout(() => {
        treeMapRef.current?.drillDown(args.item, 0);
      }, 0);
    }
  };

  return (
    <TreeMapComponent
      ref={treeMapRef}
      enableDrillDown={true}
      dataSource={data}
      onDrillStart={handleDrillStart}
    >
      {/* Levels */}
    </TreeMapComponent>
  );
}
```

### Pattern 3: Tracking Drill Path

Track user's navigation path:

```jsx
export function TrackDrillPath() {
  const [drillPath, setDrillPath] = React.useState(['Root']);

  const handleDrillEnd = (args) => {
    const pathItems = args.item ? [...drillPath, args.item.label] : ['Root'];
    setDrillPath(pathItems);
  };

  return (
    <div>
      <div>Path: {drillPath.join(' > ')}</div>
      <TreeMapComponent
        enableDrillDown={true}
        dataSource={data}
        onDrillEnd={handleDrillEnd}
      >
        {/* Levels */}
      </TreeMapComponent>
    </div>
  );
}
```

## Breadcrumb Navigation

Show breadcrumb for current drill location:

### Custom Breadcrumb Example

```jsx
export function TreeMapWithBreadcrumb() {
  const [breadcrumb, setBreadcrumb] = React.useState(['Root']);
  const treeMapRef = React.useRef(null);

  const handleDrillEnd = (args) => {
    const newPath = [...breadcrumb, args.item?.label || 'Item'];
    setBreadcrumb(newPath);
  };

  const handleBreadcrumbClick = (index) => {
    // Return to previous level
    const newBreadcrumb = breadcrumb.slice(0, index + 1);
    setBreadcrumb(newBreadcrumb);
    
    // Implement back navigation logic
    // treeMapRef.current?.goBack();
  };

  return (
    <div>
      <div style={{ padding: '10px', marginBottom: '10px' }}>
        {breadcrumb.map((item, index) => (
          <span key={index}>
            <a 
              href="#" 
              onClick={() => handleBreadcrumbClick(index)}
              style={{ cursor: 'pointer' }}
            >
              {item}
            </a>
            {index < breadcrumb.length - 1 && ' > '}
          </span>
        ))}
      </div>
      <TreeMapComponent
        ref={treeMapRef}
        enableDrillDown={true}
        dataSource={data}
        onDrillEnd={handleDrillEnd}
      >
        {/* Levels */}
      </TreeMapComponent>
    </div>
  );
}
```

## Advanced Drill-Down

### Conditional Drill-Down Based on Selection

```jsx
export function ConditionalDrillDown() {
  const [selectedCategory, setSelectedCategory] = React.useState(null);

  const handleItemClick = (args) => {
    setSelectedCategory(args.item?.label);
  };

  const handleDrillStart = (args) => {
    // Only allow drill-down for selected category
    if (selectedCategory && args.item?.label !== selectedCategory) {
      args.cancel = true;
    }
  };

  return (
    <TreeMapComponent
      enableDrillDown={true}
      dataSource={data}
      onItemClick={handleItemClick}
      onDrillStart={handleDrillStart}
    >
      {/* Levels */}
    </TreeMapComponent>
  );
}
```

### Drill-Down with Dynamic Data Loading

```jsx
export function DynamicDrillDown() {
  const [data, setData] = React.useState(initialData);

  const handleDrillStart = async (args) => {
    const selectedItem = args.item;
    
    // Load child data from API
    try {
      const response = await fetch(`/api/children/${selectedItem.id}`);
      const childData = await response.json();
      
      // Merge child data with existing data
      setData([...data, ...childData]);
    } catch (error) {
      console.error('Failed to load child data:', error);
      args.cancel = true;
    }
  };

  return (
    <TreeMapComponent
      enableDrillDown={true}
      dataSource={data}
      onDrillStart={handleDrillStart}
    >
      {/* Levels */}
    </TreeMapComponent>
  );
}
```

## Best Practices

1. **Clear hierarchy:** Use 2-4 levels for best user experience
2. **Meaningful labels:** Make drill paths understandable
3. **Visual feedback:** Show current location clearly
4. **Back option:** Always allow returning to previous level
5. **Data loading:** For large datasets, consider lazy loading on drill
6. **Mobile consideration:** Ensure drill-down works on touch devices

## Common Issues

**Issue:** Back button doesn't appear
- **Solution:** Ensure enableDrillDown={true} and hierarchy levels defined

**Issue:** Can't drill into certain items
- **Solution:** Check that onDrillStart doesn't cancel drill; verify data has children

**Issue:** Drill-down very slow
- **Solution:** Reduce data size, use pagination, or implement lazy loading

## Next Steps

- **Leaf Items:** See [leaf-items-and-labels.md](leaf-items-and-labels.md) for label formatting
- **Layouts:** See [layouts.md](layouts.md) to optimize hierarchy display
- **Color Mapping:** See [color-mapping.md](color-mapping.md) to distinguish levels
