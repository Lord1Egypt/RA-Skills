# Populating Items and Selection

## Table of Contents
- [Item Binding with CarouselItem](#item-binding-with-carouselitem)
- [Data Source Binding](#data-source-binding)
- [Selection with Property](#selection-with-property)
- [Selection with Methods](#selection-with-methods)
- [Partial Visible Slides](#partial-visible-slides)

## Item Binding with CarouselItem

When rendering the Carousel with item binding, you can assign individual templates to each item or use a common template. Each item can also have its own transition interval.

### Basic Item Binding

Each `CarouselItemDirective` defines one slide. The `template` prop contains the HTML to render:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="cardinal" style="height:100%;width:100%;" /><figcaption class="img-caption">Cardinal</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="kingfisher" style="height:100%;width:100%;" /><figcaption class="img-caption">Kingfisher</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="keel-billed-toucan" style="height:100%;width:100%;" /><figcaption class="img-caption">Keel-billed-toucan</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="yellow-warbler" style="height:100%;width:100%;" /><figcaption class="img-caption">Yellow-warbler</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="bee-eater" style="height:100%;width:100%;" /><figcaption class="img-caption">Bee-eater</figcaption></figure>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

### Custom Intervals Per Item

Set different transition intervals for each item using the `interval` prop (milliseconds):

```tsx
<CarouselComponent>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1 - 3 seconds</h3>' interval={3000} />
    <CarouselItemDirective template='<h3>Slide 2 - 1 second</h3>' interval={1000} />
    <CarouselItemDirective template='<h3>Slide 3 - 2 seconds</h3>' interval={2000} />
    <CarouselItemDirective template='<h3>Slide 4 - 5 seconds</h3>' interval={5000} />
    <CarouselItemDirective template='<h3>Slide 5 - 6 seconds</h3>' interval={6000} />
  </CarouselItemsDirective>
</CarouselComponent>
```

**Note:** Custom intervals only work with CarouselItem binding, not with dataSource binding.

## Data Source Binding

When using data source binding, you define a common template applied to all items. This approach is ideal for:
- Large dynamic datasets
- Items fetched from APIs
- Templates based on data properties

### Using itemTemplate

```tsx
import { CarouselComponent } from "@syncfusion/ej2-react-navigations";
import { useMemo } from "react";
import * as React from "react";

const App = () => {
  const productItems = useMemo(() => [
    { ID: 1, Name: "Cardinal", imageName: 'cardinal' },
    { ID: 2, Name: "Kingfisher", imageName: 'hunei' },
    { ID: 3, Name: "Keel-billed-toucan", imageName: 'costa-rica' },
    { ID: 4, Name: "Yellow-warbler", imageName: 'kaohsiung' },
    { ID: 5, Name: "Bee-eater", imageName: 'bee-eater' }
  ], []);

  const itemTemplate = (props: any): JSX.Element => {
    return (
      <figure className="img-container">
        <img 
          src={":url" + props.imageName + ".png"} 
          alt={props.Name} 
          style={{ height: "100%", width: "100%" }} 
        />
        <figcaption className="img-caption">{props.Name}</figcaption>
      </figure>
    );
  }

  return (
    <div className='control-container'>
      <CarouselComponent dataSource={productItems} itemTemplate={itemTemplate} />
    </div>
  );
}

export default App;
```

### Fetching Data from API

```tsx
const [carouselData, setCarouselData] = React.useState([]);

React.useEffect(() => {
  fetch('url')
    .then(res => res.json())
    .then(data => setCarouselData(data))
    .catch(err => console.error('Failed to load carousel data:', err));
}, []);

const itemTemplate = (props: any): JSX.Element => {
  return <img src={props.imageUrl} alt={props.title} style={{ width: '100%', height: '100%' }} />;
}

return <CarouselComponent dataSource={carouselData} itemTemplate={itemTemplate} />;
```

## Selection with Property

### Set Initial Slide with selectedIndex

The `selectedIndex` property specifies which slide displays when the carousel initializes (0-indexed):

```tsx
<CarouselComponent selectedIndex={3}>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1</h3>' />
    <CarouselItemDirective template='<h3>Slide 2</h3>' />
    <CarouselItemDirective template='<h3>Slide 3</h3>' />
    <CarouselItemDirective template='<h3>Slide 4</h3>' />
    <CarouselItemDirective template='<h3>Slide 5</h3>' />
  </CarouselItemsDirective>
</CarouselComponent>
```

This renders with Slide 4 (index 3) displayed initially.

### Update Slide Programmatically

Change the selected slide after initial render using state:

```tsx
const [selectedIndex, setSelectedIndex] = React.useState(0);

const goToSlide = (index: number) => {
  setSelectedIndex(index);
}

return (
  <div>
    <CarouselComponent selectedIndex={selectedIndex}>
      {/* items */}
    </CarouselComponent>
    <button onClick={() => goToSlide(2)}>Go to Slide 3</button>
  </div>
);
```

## Selection with Methods

### Using prev() and next() Methods

Access the carousel instance via `useRef` to call navigation methods:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from "@syncfusion/ej2-react-buttons";
import { useRef } from "react";
import * as React from "react";

const App = () => {
  const carouselRef = useRef<CarouselComponent>(null);

  const prevBtnClick = (): void => {
    carouselRef.current?.prev();
  }

  const nextBtnClick = (): void => {
    carouselRef.current?.next();
  }

  return (
    <div>
      <div>
        <ButtonComponent className="e-btn" cssClass="e-info" onClick={prevBtnClick}>Previous</ButtonComponent>
        <ButtonComponent className="e-btn" cssClass="e-info" onClick={nextBtnClick}>Next</ButtonComponent>
      </div>
      <div className='control-container'>
        <CarouselComponent ref={carouselRef}>
          <CarouselItemsDirective>
            <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="cardinal" style="height:100%;width:100%;" /><figcaption class="img-caption">Cardinal</figcaption></figure>' />
            <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="kingfisher" style="height:100%;width:100%;" /><figcaption class="img-caption">Kingfisher</figcaption></figure>' />
            <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="keel-billed-toucan" style="height:100%;width:100%;" /><figcaption class="img-caption">Keel-billed-toucan</figcaption></figure>' />
            <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="yellow-warbler" style="height:100%;width:100%;" /><figcaption class="img-caption">Yellow-warbler</figcaption></figure>' />
            <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="bee-eater" style="height:100%;width:100%;" /><figcaption class="img-caption">Bee-eater</figcaption></figure>' />
          </CarouselItemsDirective>
        </CarouselComponent>
      </div>
    </div>
  );
}

export default App;
```

**Methods:**
- `prev()` - Navigate to previous slide
- `next()` - Navigate to next slide

## Partial Visible Slides

### Enable Adjacent Slide Previews

Show one complete slide plus partial views of previous and next slides using the `partialVisible` property:

```tsx
<CarouselComponent partialVisible={true}>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1</h3>' />
    <CarouselItemDirective template='<h3>Slide 2</h3>' />
    <CarouselItemDirective template='<h3>Slide 3</h3>' />
    <CarouselItemDirective template='<h3>Slide 4</h3>' />
    <CarouselItemDirective template='<h3>Slide 5</h3>' />
  </CarouselItemsDirective>
</CarouselComponent>
```

### Partial Visible Without Loop

When `loop={false}`, the carousel stops at the last slide without wrapping:

```tsx
<CarouselComponent partialVisible={true} loop={false}>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1</h3>' />
    <CarouselItemDirective template='<h3>Slide 2</h3>' />
    <CarouselItemDirective template='<h3>Slide 3</h3>' />
  </CarouselItemsDirective>
</CarouselComponent>
```

**Behavior:**
- With `loop={true}`: Last slide displays with previous slide as partial
- With `loop={false}`: Previous slide not shown at initial render

### Customizing Partial Slide Size

See [styling-and-appearance.md](./styling-and-appearance.md#customizing-partial-slides-size) for CSS customization of partial slide area.

## Edge Cases

**No items defined:**
- Carousel renders with empty container
- Navigator and indicator buttons still appear but are non-functional

**Single item:**
- Carousel displays the single item
- Navigation buttons and indicators appear but have no effect
- Loop has no visible impact

**Large datasets:**
- Consider using dataSource with itemTemplate for 50+ items
- Avoid rendering 100+ CarouselItemDirective elements in JSX
