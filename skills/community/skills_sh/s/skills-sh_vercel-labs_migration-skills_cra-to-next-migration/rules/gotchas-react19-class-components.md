---
title: Fix React 19 Class Component this Binding
impact: CRITICAL
impactDescription: this is undefined in setState callbacks
tags: gotchas, react19, class-components, this-binding
---

## Fix React 19 Class Component this Binding

React 19 changes how `this` is bound in certain callback contexts, causing `this` to be `undefined` in Promise `.then()` handlers, `setState` callbacks, and nested callbacks within class components.

**CRITICAL:** Even arrow functions can lose `this` context in nested callbacks like `setState` callbacks and array methods. The `const self = this` pattern is the most reliable solution.

**Error message:**

```
TypeError: Cannot read properties of undefined (reading 'setState')
TypeError: Cannot read properties of undefined (reading 'props')
```

**Problematic pattern:**

```tsx
class MyComponent extends React.Component {
  handleSubmit = () => {
    fetchData()
      .then(function(response) {
        // ERROR in React 19: 'this' is undefined here
        this.setState({ data: response })
      })
  }

  loadData() {
    this.setState({ loading: true }, function() {
      // ERROR in React 19: 'this' is undefined in setState callback
      this.fetchMore()
    })
  }
}
```

**Even arrow functions can fail in nested callbacks:**

```tsx
class App extends React.Component {
  // This is an arrow function property, but 'this' is still lost in the callback!
  private onImageAction = async () => {
    this.setState(
      { pendingImageElementId: imageElement.id },
      () => {
        this.insertImageElement(...); // ERROR: 'this' is undefined even in arrow callback!
      },
    );
  };

  handleItems = () => {
    items
      .filter((item) => this.isValid(item)) // ERROR: 'this' may be undefined
      .map((item) => this.transform(item)); // ERROR: 'this' may be undefined
  }
}
```

**Solution 1: Use `const self = this` pattern (RECOMMENDED)**

This is the most reliable solution and works in all callback contexts:

```tsx
class MyComponent extends React.Component {
  handleSubmit = () => {
    const self = this // Capture this reference

    fetchData()
      .then(function(response) {
        self.setState({ data: response }) // Use self instead of this
      })
  }

  loadData() {
    const self = this

    this.setState({ loading: true }, function() {
      self.fetchMore()
    })
  }

  // For nested callbacks, use self throughout
  private onImageAction = async () => {
    const self = this

    self.setState(
      { pendingImageElementId: imageElement.id },
      () => {
        self.insertImageElement(...); // Works correctly with self
      },
    );
  };

  handleItems = () => {
    const self = this

    items
      .filter((item) => self.isValid(item))
      .map((item) => self.transform(item));
  }
}
```

**Solution 2: Use arrow functions (works for simple cases only)**

Arrow functions work for converting `function` keywords but may NOT work in nested callbacks:

```tsx
class MyComponent extends React.Component {
  handleSubmit = () => {
    fetchData()
      .then((response) => {
        // Arrow function preserves 'this' from enclosing scope in simple cases
        this.setState({ data: response })
      })
  }

  loadData() {
    this.setState({ loading: true }, () => {
      // May work, but not guaranteed in all contexts
      this.fetchMore()
    })
  }
}
```

**WARNING:** Arrow functions do NOT reliably preserve `this` in:
- `setState` callbacks (even when the outer function is an arrow function)
- Array method callbacks (`.filter()`, `.map()`, `.forEach()`, `.reduce()`)
- Promise executor callbacks
- Nested callback chains

If you encounter `this` issues with arrow functions, use `const self = this` instead.

**Solution 3: Convert to functional components (Recommended)**

```tsx
function MyComponent() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    const response = await fetchData()
    setData(response)
  }

  const loadData = () => {
    setLoading(true)
    // No callback needed - use useEffect for side effects
  }

  return <div>...</div>
}
```

**Search patterns for affected code:**

```bash
# Find Promise .then() with function keyword in class components
grep -r "\.then(function" --include="*.tsx" --include="*.ts"

# Find setState with callback function
grep -r "setState.*function(" --include="*.tsx" --include="*.ts"

# Find class components
grep -r "extends React.Component\|extends Component" --include="*.tsx" --include="*.ts"
```

**Migration checklist:**

1. Search for all class components in the codebase
2. Check each for Promise `.then()` handlers using `function` keyword
3. Check for `setState` with callback functions (even arrow functions!)
4. Check for array method chains (`.filter()`, `.map()`, etc.) that use `this`
5. Apply `const self = this` pattern as the primary fix
6. Consider converting heavily-affected components to functional components

**Why this happens:**

React 19 optimizes the rendering pipeline and changes internal binding behaviors. Traditional `function` declarations lose their `this` context in async boundaries, while arrow functions capture `this` lexically from their enclosing scope.
