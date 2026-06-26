# Testing Syncfusion React Grids

## Table of Contents
- [Overview](#overview)
- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)
- [Snapshot Testing](#snapshot-testing)
- [Best Practices](#best-practices)

---

## Overview

Test grids to ensure:
- Correct data rendering
- Feature operations (sort, filter, edit)
- Event handling
- User interactions
- Integration with backend

This guide uses **Jest** and **React Testing Library**.

---

## Unit Testing

Test individual grid features in isolation.

```tsx
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import GridComponent from './GridComponent';

describe('Grid Component - Unit Tests', () => {
  
  // Mock data
  const mockData = [
    { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 },
    { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83 },
  ];

  test('renders grid container', () => {
    const { container } = render(<GridComponent dataSource={mockData} />);
    expect(container.querySelector('.e-grid')).toBeInTheDocument();
  });

  test('displays correct number of rows', async () => {
    const { container } = render(<GridComponent dataSource={mockData} allowPaging={false} />);
    
    await waitFor(() => {
      const rows = container.querySelectorAll('.e-row');
      expect(rows).toHaveLength(mockData.length);
    });
  });

  test('renders all columns', () => {
    const { container } = render(<GridComponent dataSource={mockData} />);
    
    const headers = container.querySelectorAll('.e-headercell');
    expect(headers.length).toBeGreaterThan(0);
  });

  test('displays column headers correctly', () => {
    const { container } = render(<GridComponent dataSource={mockData} />);
    
    const headerText = container.querySelector('.e-headercell')?.textContent;
    expect(headerText).toBeTruthy();
  });

  test('displays data in cells', () => {
    const { container } = render(<GridComponent dataSource={mockData} />);
    
    const cells = container.querySelectorAll('.e-rowcell');
    const firstCellText = cells[0]?.textContent;
    expect(firstCellText).toBe(mockData[0].OrderID.toString());
  });

  test('paging works correctly', async () => {
    const largeData = Array.from({ length: 50 }, (_, i) => ({
      OrderID: 10248 + i,
      CustomerID: `CUST${i}`,
      Freight: Math.random() * 100
    }));

    const { container } = render(
      <GridComponent
        dataSource={largeData}
        allowPaging={true}
        pageSettings={{ pageSize: 10 }}
      />
    );

    await waitFor(() => {
      const rows = container.querySelectorAll('.e-row');
      expect(rows.length).toBeLessThanOrEqual(10);
    });
  });

  test('sorting toggles correctly', async () => {
    const { container } = render(
      <GridComponent dataSource={mockData} allowSorting={true} />
    );

    const orderIdHeader = container.querySelector(
      '[data-field="OrderID"] .e-headercell'
    );

    fireEvent.click(orderIdHeader);

    await waitFor(() => {
      const sortIcon = orderIdHeader.querySelector('.e-sort-icon');
      expect(sortIcon).toHaveClass('e-ascending');
    });

    fireEvent.click(orderIdHeader);

    await waitFor(() => {
      const sortIcon = orderIdHeader.querySelector('.e-sort-icon');
      expect(sortIcon).toHaveClass('e-descending');
    });
  });

  test('filtering works correctly', async () => {
    const { container } = render(
      <GridComponent dataSource={mockData} allowFiltering={true} />
    );

    const filterInput = container.querySelector('.e-filterinput');
    fireEvent.change(filterInput, { target: { value: 'VINET' } });

    await waitFor(() => {
      const rows = container.querySelectorAll('.e-row');
      expect(rows.length).toBeLessThan(mockData.length);
    });
  });

  test('row selection works', async () => {
    const { container } = render(
      <GridComponent dataSource={mockData} allowSelection={true} />
    );

    const firstRow = container.querySelector('.e-row');
    fireEvent.click(firstRow);

    await waitFor(() => {
      expect(firstRow).toHaveClass('e-selectionbackground');
    });
  });

  test('edit mode activates', async () => {
    const { container } = render(
      <GridComponent
        dataSource={mockData}
        editSettings={{ mode: 'Inline', allowEditing: true }}
      />
    );

    const firstRow = container.querySelector('.e-row');
    fireEvent.doubleClick(firstRow);

    await waitFor(() => {
      const editForm = container.querySelector('.e-inline-edit');
      expect(editForm).toBeDefined();
    });
  });

  test('save button saves data', async () => {
    const mockSave = jest.fn();
    const { container } = render(
      <GridComponent
        dataSource={mockData}
        editSettings={{ mode: 'Inline' }}
        actionComplete={mockSave}
      />
    );

    // Start edit
    const firstRow = container.querySelector('.e-row');
    fireEvent.doubleClick(firstRow);

    // Find save button and click
    const saveBtn = container.querySelector('[aria-label="Save"]');
    fireEvent.click(saveBtn);

    await waitFor(() => {
      expect(mockSave).toHaveBeenCalled();
    });
  });

  test('delete record removes row', async () => {
    const { container } = render(
      <GridComponent
        dataSource={mockData}
        editSettings={{ allowDeleting: true }}
      />
    );

    const initialRows = container.querySelectorAll('.e-row').length;

    const deleteBtn = container.querySelector('[aria-label="Delete"]');
    fireEvent.click(deleteBtn);

    await waitFor(() => {
      const finalRows = container.querySelectorAll('.e-row').length;
      expect(finalRows).toBeLessThan(initialRows);
    });
  });

});
```

---

## Integration Testing

Test multiple features working together.

```tsx
describe('Grid Component - Integration Tests', () => {

  const largeDataset = Array.from({ length: 100 }, (_, i) => ({
    OrderID: 10248 + i,
    CustomerID: `CUST${i % 10}`,
    Freight: Math.random() * 1000,
    Status: i % 2 === 0 ? 'Completed' : 'Pending'
  }));

  test('pagination, sorting, and filtering work together', async () => {
    const { container } = render(
      <GridComponent
        dataSource={largeDataset}
        allowPaging={true}
        pageSettings={{ pageSize: 10 }}
        allowSorting={true}
        allowFiltering={true}
      />
    );

    // Apply filter
    const filterInput = container.querySelector('.e-filterinput');
    fireEvent.change(filterInput, { target: { value: 'CUST0' } });

    // Sort by Freight
    const freightHeader = container.querySelector('[data-field="Freight"] .e-headercell');
    fireEvent.click(freightHeader);

    // Navigate to page 2
    const nextPageBtn = container.querySelector('.e-nextpage');
    fireEvent.click(nextPageBtn);

    await waitFor(() => {
      const rows = container.querySelectorAll('.e-row');
      expect(rows.length).toBeGreaterThan(0);
    });
  });

  test('edit and save with validation', async () => {
    const onSave = jest.fn();
    const { container } = render(
      <GridComponent
        dataSource={largeDataset}
        editSettings={{
          mode: 'Dialog',
          allowEditing: true
        }}
        actionComplete={onSave}
      />
    );

    // Find and click row
    const editBtn = container.querySelector('[aria-label="Edit"]');
    fireEvent.click(editBtn);

    // Wait for dialog
    await waitFor(() => {
      const dialog = container.querySelector('.e-dialog');
      expect(dialog).toBeInTheDocument();
    });

    // Modify data
    const input = container.querySelector('.e-dialog input');
    fireEvent.change(input, { target: { value: 'UpdatedValue' } });

    // Save
    const saveBtn = container.querySelector('.e-dialog .e-primary');
    fireEvent.click(saveBtn);

    await waitFor(() => {
      expect(onSave).toHaveBeenCalledWith(
        expect.objectContaining({
          requestType: expect.stringMatching(/save|update/)
        })
      );
    });
  });

  test('complex filter with sort and edit', async () => {
    const { container } = render(
      <GridComponent
        dataSource={largeDataset}
        allowFiltering={true}
        allowSorting={true}
        editSettings={{ allowEditing: true }}
      />
    );

    // Filter for 'Completed' status
    const filterInput = container.querySelector('.e-filterinput');
    fireEvent.change(filterInput, { target: { value: 'Completed' } });

    // Sort by Freight descending
    const header = container.querySelector('[data-field="Freight"] .e-headercell');
    fireEvent.click(header);
    fireEvent.click(header); // Second click for descending

    // Edit first row
    const firstRow = container.querySelector('.e-row');
    fireEvent.doubleClick(firstRow);

    await waitFor(() => {
      const input = firstRow.querySelector('input');
      expect(input).toBeInTheDocument();
    });
  });

});
```

---

## Snapshot Testing

Test that grid structure doesn't change unexpectedly.

```tsx
test('grid renders with expected snapshot', () => {
  const { container } = render(<GridComponent dataSource={mockData} />);
  expect(container.firstChild).toMatchSnapshot();
});
```

---

## Best Practices

1. **Mock data**: Use consistent seed data for tests
   ```tsx
   const mockData = [ /* fixed data */ ];
   ```

2. **Test behaviors, not implementation**: Don't test internal class names
   ```tsx
   // ✅ GOOD
   expect(rows).toHaveLength(3);
   
   // ❌ BAD
   expect(container.querySelector('.e-row')).toBeDefined();
   ```

3. **Use `waitFor` for async operations**
   ```tsx
   await waitFor(() => {
     expect(element).toBeInTheDocument();
   });
   ```

4. **Test user interactions**, not APIs
   ```tsx
   // ✅ GOOD
   fireEvent.click(sortButton);
   expect(firstRow.textContent).toBe('Sorted value');
   
   // ❌ BAD (testing internal method)
   gridRef.current.sortColumn('Freight', 'Ascending');
   ```

5. **Test edge cases**
   ```tsx
   test('handles empty data', () => { /* ... */ });
   test('handles error response', () => { /* ... */ });
   test('handles very large dataset', () => { /* ... */ });
   ```

6. **Group related tests**
   ```tsx
   describe('Editing Feature', () => {
     test('edit starts on double-click', () => {});
     test('save persists changes', () => {});
     test('cancel discards changes', () => {});
   });
   ```

---
