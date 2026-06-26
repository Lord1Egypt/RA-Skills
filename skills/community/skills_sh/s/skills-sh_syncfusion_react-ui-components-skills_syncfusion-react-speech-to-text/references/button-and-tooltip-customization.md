# Button and Tooltip Customization

## Table of Contents
- [Customizing Button Content](#customizing-button-content)
- [Icon Customization](#icon-customization)
- [Icon Positioning](#icon-positioning)
- [Primary Button Styling](#primary-button-styling)
- [Controlling Tooltip Visibility](#controlling-tooltip-visibility)
- [Tooltip Configuration](#tooltip-configuration)
- [CSS Class Styling](#css-class-styling)
- [Complete Customization Examples](#complete-customization-examples)

## Customizing Button Content

You can customize the text displayed on the button in both listening and stopped states using the `buttonSettings` property.

### Setting Button Text

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function ButtonTextDemo() {
  const buttonSettings: ButtonSettingsModel = {
    content: 'Start Listening',      // Text when not listening
    stopContent: 'Stop Listening'    // Text when listening
  };

  return (
    <SpeechToTextComponent 
      buttonSettings={buttonSettings}
    />
  );
}

export default ButtonTextDemo;
```

### Minimal Button Text

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function MinimalButtonDemo() {
  const buttonSettings: ButtonSettingsModel = {
    content: 'Start',
    stopContent: 'Stop'
  };

  return (
    <SpeechToTextComponent 
      buttonSettings={buttonSettings}
    />
  );
}
```

## Icon Customization

Customize the appearance of button icons using CSS icon classes.

### Available Icon Classes

Syncfusion provides icon classes from the `e-icons` font:
- `e-icons e-play` - Play icon
- `e-icons e-pause` - Pause icon
- `e-icons e-stop` - Stop icon
- `e-icons e-mic` - Microphone icon
- `e-icons e-speaker` - Speaker icon
- `e-icons e-close` - Close icon
- Custom CSS class names for custom icons

### Setting Icons

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-icons/styles/material.css';

function IconDemo() {
  const buttonSettings: ButtonSettingsModel = {
    content: 'Record',
    stopContent: 'Stop',
    iconCss: 'e-icons e-play',           // Icon when not listening
    stopIconCss: 'e-icons e-pause'       // Icon when listening
  };

  return (
    <div>
      <SpeechToTextComponent 
        buttonSettings={buttonSettings}
      />
    </div>
  );
}

export default IconDemo;
```

### Using Different Icons

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function AlternateIconDemo() {
  const buttonSettings: ButtonSettingsModel = {
    iconCss: 'e-icons e-mic',           // Microphone icon
    stopIconCss: 'e-icons e-stop'       // Stop icon
  };

  return (
    <SpeechToTextComponent 
      buttonSettings={buttonSettings}
    />
  );
}
```

### Custom Icons

Add custom CSS for your own icons:

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function CustomIconDemo() {
  const buttonSettings: ButtonSettingsModel = {
    iconCss: 'custom-icon-start',
    stopIconCss: 'custom-icon-stop'
  };

  const customStyles = `
    .custom-icon-start::before {
      content: '🎤';
      margin-right: 8px;
    }
    .custom-icon-stop::before {
      content: '⏹️';
      margin-right: 8px;
    }
  `;

  return (
    <div>
      <style>{customStyles}</style>
      <SpeechToTextComponent 
        buttonSettings={buttonSettings}
      />
    </div>
  );
}

export default CustomIconDemo;
```

## Icon Positioning

Control where the icon appears relative to the button text.

### Icon Position Options

- `Left` - Icon on the left side of text (default)
- `Right` - Icon on the right side of text
- `Top` - Icon above the text
- `Bottom` - Icon below the text

### Positioning Examples

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function IconPositionDemo() {
  // Icon on the right
  const rightPosition: ButtonSettingsModel = {
    content: 'Start',
    stopContent: 'Stop',
    iconCss: 'e-icons e-play',
    stopIconCss: 'e-icons e-pause',
    iconPosition: 'Right'
  };

  // Icon on top
  const topPosition: ButtonSettingsModel = {
    content: 'Record',
    iconCss: 'e-icons e-mic',
    iconPosition: 'Top'
  };

  // Icon on bottom
  const bottomPosition: ButtonSettingsModel = {
    content: 'Listen',
    iconCss: 'e-icons e-speaker',
    iconPosition: 'Bottom'
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div>
        <p>Icon Right:</p>
        <SpeechToTextComponent buttonSettings={rightPosition} />
      </div>
      <div>
        <p>Icon Top:</p>
        <SpeechToTextComponent buttonSettings={topPosition} />
      </div>
      <div>
        <p>Icon Bottom:</p>
        <SpeechToTextComponent buttonSettings={bottomPosition} />
      </div>
    </div>
  );
}

export default IconPositionDemo;
```

## Primary Button Styling

The `isPrimary` property makes the button visually prominent with primary action styling.

### Primary Button

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function PrimaryButtonDemo() {
  const buttonSettings: ButtonSettingsModel = {
    content: 'Start Recording',
    stopContent: 'Stop Recording',
    isPrimary: true  // Makes button prominent
  };

  return (
    <SpeechToTextComponent 
      buttonSettings={buttonSettings}
    />
  );
}

export default PrimaryButtonDemo;
```

### Combining with Other Customizations

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function AdvancedButtonDemo() {
  const buttonSettings: ButtonSettingsModel = {
    content: 'Start',
    stopContent: 'Stop',
    iconCss: 'e-icons e-play',
    stopIconCss: 'e-icons e-stop',
    iconPosition: 'Right',
    isPrimary: true
  };

  return (
    <SpeechToTextComponent 
      buttonSettings={buttonSettings}
    />
  );
}

export default AdvancedButtonDemo;
```

## Controlling Tooltip Visibility

The `showTooltip` property (default: `true`) controls whether the tooltip is displayed at all when hovering over the SpeechToText button. Set it to `false` to completely hide the tooltip.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function NoTooltipDemo() {
  return (
    // Tooltip is hidden — no hover popup appears
    <SpeechToTextComponent showTooltip={false} />
  );
}

export default NoTooltipDemo;
```

### Conditionally Toggling Tooltip

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function ToggleTooltipDemo() {
  const [showTooltip, setShowTooltip] = useState(true);

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={showTooltip}
          onChange={e => setShowTooltip(e.target.checked)}
        />
        Show Tooltip
      </label>
      <SpeechToTextComponent showTooltip={showTooltip} />
    </div>
  );
}

export default ToggleTooltipDemo;
```

## Tooltip Configuration

Customize the tooltip that appears when hovering over the button using `tooltipSettings`.

### Basic Tooltip

```tsx
import { SpeechToTextComponent, TooltipSettingsModel } from '@syncfusion/ej2-react-inputs';

function TooltipDemo() {
  const tooltipSettings: TooltipSettingsModel = {
    content: 'Click to start speech recognition',
    stopContent: 'Click to stop recording'
  };

  return (
    <SpeechToTextComponent 
      tooltipSettings={tooltipSettings}
    />
  );
}

export default TooltipDemo;
```

### Tooltip Position

Control where the tooltip appears:

```tsx
import { SpeechToTextComponent, TooltipSettingsModel } from '@syncfusion/ej2-react-inputs';

function TooltipPositionDemo() {
  const tooltipSettings: TooltipSettingsModel = {
    position: 'TopCenter',           // TopCenter, TopLeft, TopRight
    content: 'Click to record',
    stopContent: 'Click to stop'
  };

  return (
    <SpeechToTextComponent 
      tooltipSettings={tooltipSettings}
    />
  );
}

export default TooltipPositionDemo;
```

### Tooltip Position Options

All valid `TooltipPosition` enum values:

| Value | Description |
|-------|-------------|
| `TopLeft` | Appears at the top-left corner of the button |
| `TopCenter` | Appears at the top-center of the button |
| `TopRight` | Appears at the top-right corner of the button |
| `BottomLeft` | Appears at the bottom-left corner of the button |
| `BottomCenter` | Appears at the bottom-center of the button |
| `BottomRight` | Appears at the bottom-right corner of the button |
| `LeftTop` | Appears at the left-top corner of the button |
| `LeftCenter` | Appears at the left-center of the button |
| `LeftBottom` | Appears at the left-bottom corner of the button |
| `RightTop` | Appears at the right-top corner of the button |
| `RightCenter` | Appears at the right-center of the button |
| `RightBottom` | Appears at the right-bottom corner of the button |

## CSS Class Styling

Apply predefined or custom CSS classes for styling.

### Predefined CSS Classes

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function PredefinedStylesDemo() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Primary button */}
      <SpeechToTextComponent cssClass="e-primary" />
      
      {/* Success button */}
      <SpeechToTextComponent cssClass="e-success" />
      
      {/* Info button */}
      <SpeechToTextComponent cssClass="e-info" />
      
      {/* Warning button */}
      <SpeechToTextComponent cssClass="e-warning" />
      
      {/* Danger button */}
      <SpeechToTextComponent cssClass="e-danger" />
      
      {/* Outline button */}
      <SpeechToTextComponent cssClass="e-outline" />
    </div>
  );
}

export default PredefinedStylesDemo;
```

### Custom CSS Classes

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function CustomStyleDemo() {
  const customStyles = `
    .custom-voice-btn.e-btn {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      border-radius: 25px;
      padding: 12px 30px;
      font-weight: bold;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .custom-voice-btn.e-btn:hover {
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
  `;

  return (
    <div>
      <style>{customStyles}</style>
      <SpeechToTextComponent cssClass="custom-voice-btn" />
    </div>
  );
}

export default CustomStyleDemo;
```

## Complete Customization Examples

### Example 1: Modern Voice Button

```tsx
import { SpeechToTextComponent, ButtonSettingsModel, TooltipSettingsModel } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function ModernVoiceButton() {
  const [isListening, setIsListening] = useState(false);

  const buttonSettings: ButtonSettingsModel = {
    content: 'Start',
    stopContent: 'Stop',
    iconCss: 'e-icons e-play',
    stopIconCss: 'e-icons e-stop',
    iconPosition: 'Right',
    isPrimary: true
  };

  const tooltipSettings: TooltipSettingsModel = {
    position: 'TopCenter',
    content: 'Click to start recording your voice',
    stopContent: 'Click to stop recording'
  };

  return (
    <div style={{ padding: '20px' }}>
      <SpeechToTextComponent
        buttonSettings={buttonSettings}
        tooltipSettings={tooltipSettings}
        cssClass="e-primary"
        onStart={() => setIsListening(true)}
        onStop={() => setIsListening(false)}
      />
      {isListening && <p style={{ color: 'red' }}>🎤 Recording...</p>}
    </div>
  );
}

export default ModernVoiceButton;
```

### Example 2: Minimalist Design

```tsx
import { SpeechToTextComponent, ButtonSettingsModel } from '@syncfusion/ej2-react-inputs';

function MinimalistDesign() {
  const buttonSettings: ButtonSettingsModel = {
    content: '',           // No text
    stopContent: '',
    iconCss: 'e-icons e-mic',
    stopIconCss: 'e-icons e-close',
    isPrimary: false
  };

  const customStyles = `
    .minimalist-btn.e-btn {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #f0f0f0;
      border: 2px solid #ddd;
    }
    
    .minimalist-btn.e-btn:hover {
      background-color: #e0e0e0;
    }
  `;

  return (
    <div>
      <style>{customStyles}</style>
      <SpeechToTextComponent 
        cssClass="minimalist-btn"
        buttonSettings={buttonSettings}
      />
    </div>
  );
}

export default MinimalistDesign;
```

### Example 3: Accessible Voice Input

```tsx
import { SpeechToTextComponent, ButtonSettingsModel, TooltipSettingsModel } from '@syncfusion/ej2-react-inputs';

function AccessibleVoiceInput() {
  const buttonSettings: ButtonSettingsModel = {
    content: 'Start Voice Input',
    stopContent: 'Stop Voice Input',
    iconCss: 'e-icons e-play',
    stopIconCss: 'e-icons e-pause',
    iconPosition: 'Left',
    isPrimary: true
  };

  const tooltipSettings: TooltipSettingsModel = {
    position: 'TopCenter',
    content: 'Press enter or click to activate voice input. Speak clearly into your microphone.',
    stopContent: 'Press enter or click to deactivate voice input.'
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <label htmlFor="voiceInput" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
        Voice Input Control
      </label>
      <SpeechToTextComponent
        id="voiceInput"
        buttonSettings={buttonSettings}
        tooltipSettings={tooltipSettings}
        cssClass="e-primary"
      />
      <p style={{ fontSize: '14px', color: '#666', marginTop: '10px' }}>
        Use this button to provide voice input. Speak naturally and pause between sentences.
      </p>
    </div>
  );
}

export default AccessibleVoiceInput;
```

## Troubleshooting

### Icons not showing
- Ensure `@syncfusion/ej2-icons/styles/material.css` is imported
- Verify icon class names are correct

### Tooltip not appearing
- Check that `tooltipSettings` is properly configured
- Ensure position property uses correct enum values

### Custom CSS not applying
- Verify CSS class name matches in component and styles
- Check CSS specificity - Syncfusion classes might override your styles
- Use `!important` if needed, or increase specificity with more selectors

