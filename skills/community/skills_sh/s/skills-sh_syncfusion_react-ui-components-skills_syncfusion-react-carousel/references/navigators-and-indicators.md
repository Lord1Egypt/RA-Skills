# Navigators and Indicators

## Table of Contents
- [Navigators Overview](#navigators-overview)
- [Navigator Button Visibility Modes](#navigator-button-visibility-modes)
- [Custom Navigator Templates](#custom-navigator-templates)
- [Indicators Overview](#indicators-overview)
- [Indicator Types](#indicator-types)
- [Indicator Templates](#indicator-templates)
- [Play Button Control](#play-button-control)

## Navigators Overview

The navigators are previous and next buttons that allow users to manually transition between slides. Control their visibility and appearance using the `buttonsVisibility` property and template customization.

## Navigator Button Visibility Modes

The `buttonsVisibility` property controls when the previous/next buttons appear:

### Mode 1: Always Hidden

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective, CarouselButtonVisibility } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  const showButtons: CarouselButtonVisibility = "Hidden";

  return (
    <div className='control-container'>
      <CarouselComponent buttonsVisibility={showButtons}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

### Mode 2: Always Visible

```tsx
const showButtons: CarouselButtonVisibility = "Visible";

return (
  <CarouselComponent buttonsVisibility={showButtons}>
    {/* items */}
  </CarouselComponent>
);
```

Buttons remain visible at all times, allowing continuous manual navigation.

### Mode 3: Visible on Hover

```tsx
const showButtons: CarouselButtonVisibility = "VisibleOnHover";

return (
  <CarouselComponent buttonsVisibility={showButtons}>
    {/* items */}
  </CarouselComponent>
);
```

Buttons only appear when the user hovers over the carousel, reducing visual clutter on desktop while keeping navigation available on mobile (pseudo-hover).

## Custom Navigator Templates

Customize the appearance of previous and next buttons using the `previousButtonTemplate` and `nextButtonTemplate` props:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from "@syncfusion/ej2-react-buttons";
import * as React from "react";

const App = () => {
  const previousButtonTemplate = (props: any): JSX.Element => {
    return (
      <ButtonComponent 
        className="e-btn" 
        cssClass="e-flat e-round" 
        iconCss="e-icons e-chevron-left-double" 
      />
    );
  }

  const nextButtonTemplate = (props: any): JSX.Element => {
    return (
      <ButtonComponent 
        className="e-btn" 
        cssClass="e-flat e-round" 
        iconCss="e-icons e-chevron-right-double" 
      />
    );
  }

  return (
    <div className='control-container'>
      <CarouselComponent 
        previousButtonTemplate={previousButtonTemplate} 
        nextButtonTemplate={nextButtonTemplate}
      >
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

**Available icons:** Use Syncfusion icon classes like `e-chevron-left`, `e-arrow-left`, `e-chevron-right`, `e-arrow-right`, or any custom SVG.

## Indicators Overview

Indicators show the current slide position and allow click-to-navigate to specific slides. Control indicators with `showIndicators` property (default: `true`).

### Show or Hide Indicators

```tsx
<CarouselComponent showIndicators={true}>
  <CarouselItemsDirective>
    {/* items */}
  </CarouselItemsDirective>
</CarouselComponent>
```

Set `showIndicators={false}` to hide indicators completely.

## Indicator Types

Choose from four indicator types using the `indicatorsType` property:

### Type 1: Default Indicator

A set of dots representing each slide:

```tsx
<CarouselComponent indicatorsType="Default">
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1</h3>' />
    <CarouselItemDirective template='<h3>Slide 2</h3>' />
    <CarouselItemDirective template='<h3>Slide 3</h3>' />
    <CarouselItemDirective template='<h3>Slide 4</h3>' />
    <CarouselItemDirective template='<h3>Slide 5</h3>' />
  </CarouselItemsDirective>
</CarouselComponent>
```

### Type 2: Dynamic Indicator

Dynamically styled dots that visually respond to slide position:

```tsx
<CarouselComponent indicatorsType="Dynamic">
  <CarouselItemsDirective>
    {/* items */}
  </CarouselItemsDirective>
</CarouselComponent>
```

### Type 3: Fraction Indicator

Displays current slide and total count as a fraction (e.g., "2/5"):

```tsx
<CarouselComponent indicatorsType="Fraction">
  <CarouselItemsDirective>
    {/* items */}
  </CarouselItemsDirective>
</CarouselComponent>
```

### Type 4: Progress Indicator

Shows a progress bar representing completion through slides:

```tsx
<CarouselComponent indicatorsType="Progress">
  <CarouselItemsDirective>
    {/* items */}
  </CarouselItemsDirective>
</CarouselComponent>
```

## Indicator Templates

### Custom Indicator Template

Customize indicator appearance using the `indicatorsTemplate` prop:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { useMemo } from "react";
import * as React from "react";

const App = () => {
  const indicatorTemplate = useMemo(() => {
    return (props: any) => <div className="indicator" indicator-index={props.index}></div>;
  }, []);

  return (
    <div className='control-container'>
      <CarouselComponent indicatorsTemplate={indicatorTemplate}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

**Template Props:**
- `props.index` - Zero-based slide index

### Indicator Template with Preview Images

Show thumbnail previews in indicators:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { useState } from "react";
import * as React from "react";

const App = () => {
  const [slides] = useState(["Slide 1", "Slide 2", "Slide 3", "Slide 4", "Slide 5"]);

  const getContent = (index: number) => {
    return slides[index];
  }

  const indicatorTemplate = (props: any): JSX.Element => {
    return (
      <div className="indicator" indicator-index={props.index}>
        <div className="preview-content">{getContent(props.index)}</div>
      </div>
    );
  }

  return (
    <div className="control-container">
      <CarouselComponent indicatorsTemplate={indicatorTemplate}>
        <CarouselItemsDirective>
          <CarouselItemDirective template="<div class='slide-content'>Slide 1</div>" />
          <CarouselItemDirective template="<div class='slide-content'>Slide 2</div>" />
          <CarouselItemDirective template="<div class='slide-content'>Slide 3</div>" />
          <CarouselItemDirective template="<div class='slide-content'>Slide 4</div>" />
          <CarouselItemDirective template="<div class='slide-content'>Slide 5</div>" />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

## Play Button Control

### Show or Hide Play Button

The `showPlayButton` property adds a play/pause button to control auto-play:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent showPlayButton={true}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

**Note:** Requires `buttonsVisibility` to be set (at least "Visible" or "VisibleOnHover").

### Custom Play Button Template

Customize the play/pause button:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from "@syncfusion/ej2-react-buttons";
import { useState } from "react";
import * as React from "react";

const App = () => {
  const [buttonContent, setButtonContent] = useState<string>('Pause');
  const [autoPlay, setAutoPlay] = useState<boolean>(true);

  const btnClick = () => {
    if (autoPlay) {
      setButtonContent('Play');
      setAutoPlay(false);
    } else {
      setButtonContent('Pause');
      setAutoPlay(true);
    }
  }

  const playButtonTemplate = (props: any): JSX.Element => {
    return (
      <ButtonComponent 
        className="e-btn" 
        cssClass="e-info playBtn" 
        content={buttonContent} 
        onClick={btnClick} 
      />
    );
  }

  return (
    <div className='control-container'>
      <CarouselComponent 
        showPlayButton={true} 
        playButtonTemplate={playButtonTemplate} 
        autoPlay={autoPlay}
      >
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

## Best Practices

- **Desktop:** Use "VisibleOnHover" to keep interface clean while providing navigation
- **Mobile:** Use "Visible" since hover doesn't work on touch devices
- **Accessibility:** Always include either indicators or play button for non-disabled users
- **Customization:** Templates allow complete UI control while maintaining functionality
