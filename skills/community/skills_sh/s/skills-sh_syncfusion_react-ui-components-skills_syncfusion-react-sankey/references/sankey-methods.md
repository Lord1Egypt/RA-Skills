````markdown
# Sankey Methods Reference

See the component methods in the main API: [SankeyComponent API - Methods](https://ej2.syncfusion.com/react/documentation/api/sankey/index-default#methods)

Common instance methods (summaries):

- `export(type: string, fileName?: string, orientation?: object)` — Export the chart to supported formats (`'png'`, `'jpeg'`, `'svg'`, `'pdf'`).
- `print(id?: string)` — Print the chart or a specific element by id.
- `getModuleName()` — Returns internal module name for the component.
- `destroy()` — Destroys the component instance and cleans up event listeners and DOM modifications.

## Example

```tsx
import React, { useRef } from 'react';

function ExportableSankey() {
  const sankeyRef = useRef(null);

  const handleExport = () => {
    sankeyRef.current?.export('PNG', 'sankey-export');
  };

  const handlePrint = () => {
    sankeyRef.current?.print();
  };

  return (
    <div>
      <button onClick={handleExport}>Export</button>
      <button onClick={handlePrint}>Print</button>
      <SankeyComponent ref={sankeyRef} width="90%" height="420px">
        {/* nodes & links */}
      </SankeyComponent>
    </div>
  );
}

export default ExportableSankey;
```

````