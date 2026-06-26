---
name: todo
description: A skill for managing todo lists, including creating, updating, deleting, and organizing tasks with priorities and deadlines.
license: MIT
author: eno
tags: productivity, task-management, todo, organization
price: 0
---

# Todo Management Skill

## Overview

This skill provides a comprehensive todo list management system. It helps users create, organize, and track tasks efficiently with support for priorities, deadlines, categories, and status tracking.

## Features

- **Create Tasks**: Add new todo items with title, description, priority, and due date.
- **Update Tasks**: Modify existing tasks including status, priority, and details.
- **Delete Tasks**: Remove completed or unnecessary tasks.
- **List Tasks**: View all tasks with filtering by status, priority, or category.
- **Prioritize**: Assign priority levels (high, medium, low) to tasks.
- **Categorize**: Organize tasks into custom categories or projects.
- **Due Dates**: Set and track deadlines for tasks.
- **Status Tracking**: Mark tasks as pending, in-progress, or completed.

## Usage

### Create a new task
```
Add a todo: "Finish project report" with high priority, due 2026-04-10
```

### List tasks
```
Show all my pending todos
List high priority tasks
```

### Update a task
```
Mark "Finish project report" as completed
Change priority of task #3 to medium
```

### Delete a task
```
Remove todo "Buy groceries"
```

## Task Schema

| Field       | Type     | Description                          |
|-------------|----------|--------------------------------------|
| id          | number   | Unique task identifier               |
| title       | string   | Task title                           |
| description | string   | Detailed task description            |
| priority    | string   | high / medium / low                  |
| status      | string   | pending / in-progress / completed    |
| category    | string   | Custom category or project name      |
| due_date    | string   | Deadline in YYYY-MM-DD format        |
| created_at  | string   | Creation timestamp                   |
| updated_at  | string   | Last update timestamp                |

---
