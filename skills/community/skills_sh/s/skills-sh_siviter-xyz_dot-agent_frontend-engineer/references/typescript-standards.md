# TypeScript Standards

## Standards

- Strict mode, no `any` type
- Explicit return types on functions
- Type imports: `import type { User } from '~types/user'`
- Component prop interfaces with JSDoc

## Example

```typescript
import type { User } from '~types/user';

interface MyComponentProps {
    /** User ID to display */
    userId: number;
    /** Optional callback */
    onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ userId, onAction }) => {
    // Implementation
};
```
