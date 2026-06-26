# Advanced Theming Features

## Table of Contents
- [Size Modes (Touch Support)](#size-modes-touch-support)
- [Styled-Components Integration](#styled-components-integration)
- [Theme Studio Customization](#theme-studio-customization)
- [Component-Specific Styling](#component-specific-styling)

## Size Modes (Touch Support)

Syncfusion React components provide two size modes to optimize UX across different devices and input methods:

- **Normal mode (default):** Standard control sizes optimized for mouse/keyboard input
- **Touch mode (bigger):** Enlarged controls with increased spacing for touch/mobile devices

### Global Size Mode

Enable touch mode for the entire application by adding the `e-bigger` class to `<body>`:

```html
<!-- index.html -->
<body class="e-bigger">
  <div id="root"></div>
</body>
```

**Effect:** All Syncfusion components increase in size with larger tap targets (44x44px minimum).

### Component-Specific Size Mode

Apply touch mode to individual components:

```jsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { GridComponent } from '@syncfusion/ej2-react-grids';

function App() {
  return (
    <div>
      {/* Regular size button */}
      <ButtonComponent>Normal Button</ButtonComponent>
      
      {/* Touch-optimized button via container class */}
      <div className="e-bigger">
        <ButtonComponent>Touch Button</ButtonComponent>
      </div>
      
      {/* Touch-optimized grid via cssClass prop */}
      <GridComponent cssClass="e-bigger" dataSource={data} />
    </div>
  );
}
```

### Runtime Size Mode Switching

Toggle size mode dynamically based on user preference or device detection:

```jsx
import { useState, useEffect } from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isTouchMode, setIsTouchMode] = useState(false);

  // Apply e-bigger class to body
  useEffect(() => {
    if (isTouchMode) {
      document.body.classList.add('e-bigger');
    } else {
      document.body.classList.remove('e-bigger');
    }
  }, [isTouchMode]);

  // Auto-detect touch device on mount
  useEffect(() => {
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    setIsTouchMode(isTouchDevice);
  }, []);

  return (
    <div>
      <h3>Size Mode: {isTouchMode ? 'Touch' : 'Normal'}</h3>
      <ButtonComponent onClick={() => setIsTouchMode(!isTouchMode)}>
        Toggle Size Mode
      </ButtonComponent>
      
      <div style={{ marginTop: '20px' }}>
        <ButtonComponent isPrimary={true}>Sample Button</ButtonComponent>
      </div>
    </div>
  );
}
```

## Styled-Components Integration

Syncfusion components support [styled-components](https://styled-components.com/) for CSS-in-JS styling.

### Basic Styled-Components Usage

Install styled-components from official packages.

Wrap Syncfusion components with `styled()`:

```jsx
import styled from 'styled-components';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import '@syncfusion/ej2-material3-theme/material3.css';

const StyledButton = styled(ButtonComponent)`
  &.e-btn {
    background: #75e1ef;
    color: #000000;
    border: none;
    border-radius: 20px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
    
    &:hover {
      background: #5ccde0;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(117, 225, 239, 0.4);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
`;

function App() {
  return (
    <div>
      <StyledButton>Custom Styled Button</StyledButton>
    </div>
  );
}
```

**⚠️ Important:** Always target Syncfusion component root classes (e.g., `.e-btn`, `.e-input`, `.e-grid`) for proper style application.

### Dynamic Styling with Props

Pass props to styled components for conditional styling:

```jsx
import styled, { css } from 'styled-components';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

const DynamicButton = styled(ButtonComponent)`
  &.e-btn {
    ${props => props.$variant === 'success' && css`
      background: #4caf50;
      color: white;
    `}
    
    ${props => props.$variant === 'warning' && css`
      background: #ff9800;
      color: white;
    `}
    
    ${props => props.$variant === 'error' && css`
      background: #f44336;
      color: white;
    `}
    
    ${props => props.disabled && css`
      background: #cccccc;
      color: #666666;
      cursor: not-allowed;
    `}
  }
`;

function App() {
  return (
    <div>
      <DynamicButton $variant="success">Success</DynamicButton>
      <DynamicButton $variant="warning">Warning</DynamicButton>
      <DynamicButton $variant="error">Error</DynamicButton>
      <DynamicButton disabled={true}>Disabled</DynamicButton>
    </div>
  );
}
```

**Note:** Use transient props (`$propName`) to prevent props from being passed to the DOM.

### Theme-Aware Styling

Integrate with styled-components ThemeProvider:

```jsx
import { ThemeProvider } from 'styled-components';
import styled from 'styled-components';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

const theme = {
  primary: '#6200ee',
  secondary: '#03dac6',
  error: '#b00020'
};

const ThemedButton = styled(ButtonComponent)`
  &.e-btn {
    background: ${props => props.theme.primary};
    color: white;
    
    &:hover {
      background: ${props => props.theme.secondary};
    }
  }
`;

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ThemedButton>Themed Button</ThemedButton>
    </ThemeProvider>
  );
}
```

## Theme Studio Customization

### Accessing Theme Studio

Visit [https://ej2.syncfusion.com/themestudio/?theme=tailwind3](https://ej2.syncfusion.com/themestudio/?theme=tailwind3)

**Available themes:**
- Material 3: `?theme=material3`
- Fluent 2: `?theme=fluent2`
- Bootstrap 5.3: `?theme=bootstrap5.3`
- Tailwind 3.4: `?theme=tailwind3`

### Customizing Theme Colors

Theme Studio exposes common theme variables for customization:

1. **Select base theme** (Material 3, Fluent 2, Bootstrap 5.3, Tailwind 3.4)
2. **Pick colors** using color pickers for primary, secondary, success, warning, error
3. **Preview changes** in real-time across multiple components
4. **Filter components** to generate CSS for specific components only (reduces bundle size)
5. **Download theme** as ZIP containing CSS, SCSS, and `settings.json`

### Using Downloaded Theme

```jsx
// Option 1: Direct CSS import
import './custom-theme/custom-material3.css';

// Option 2: HTML link tag
// <link href="./custom-theme/custom-material3.css" rel="stylesheet" />

import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return <ButtonComponent isPrimary={true}>Custom Theme Button</ButtonComponent>;
}
```

### Re-importing Settings

To modify an existing custom theme:

1. Click **Import** icon in Theme Studio
2. Upload previously downloaded `settings.json`
3. Modify colors as needed
4. Download updated theme

**Use case:** Update brand colors across application without recreating theme from scratch.

### Filtering Components

Reduce CSS bundle size by including only used components:

1. Click **Filter** icon in Theme Studio
2. Select components (e.g., Button, Grid, Dropdown)
3. Click **Apply**
4. Download filtered theme (smaller CSS file)

**Example:** If app only uses Button, Grid, and Calendar, filter to those components instead of downloading full theme CSS (~300KB+ reduction).

## Component-Specific Styling

### Button Customization

```css
/* index.css */
.e-btn {
  border-radius: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.e-btn.e-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.e-btn.e-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}
```