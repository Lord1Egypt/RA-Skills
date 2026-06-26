---
title: Prefer mutate() Over mutateAsync()
impact: HIGH
impactDescription: better error handling
tags: mutation, mutate, async, error
---

## Prefer mutate() Over mutateAsync()

Use `mutate()` with callbacks for most cases. Only use `mutateAsync()` for sequential operations.

**Incorrect (unhandled promise rejection):**

```typescript
const { mutateAsync } = useMutation({...});

// Easy to forget try/catch
const handleSave = () => {
  mutateAsync(data); // Unhandled rejection if error!
};
```

**Correct (mutate with callbacks):**

```typescript
const { mutate } = useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});

mutate(todoData, {
  onSuccess: () => toast.success('Saved!'),
  onError: (error) => toast.error(error.message),
});
```

**Use mutateAsync only for sequential mutations:**

```typescript
async function handleComplexSave() {
  try {
    const user = await createUserMutation.mutateAsync(userData);
    await createProfileMutation.mutateAsync({
      userId: user.id,
      ...profileData,
    });
    toast.success('User and profile created!');
  } catch (error) {
    toast.error('Failed to create user');
  }
}
```
