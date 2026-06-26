# Session note: template development must not modify PHP/controllers/config

## Context

The user corrected the run-0002 workflow after PHP/controller/config files were modified while developing a template. The user required all PHP/controller-related files to be restored and made a permanent rule: future template development must never modify PHP or controller files.

## Durable rule

For xz01 template development:

1. Do not modify PHP application code.
2. Do not modify controllers under `application/*/controller/`.
3. Do not modify models, services, route definitions, ThinkPHP config files, database config files, or other backend/runtime PHP files.
4. Template work is limited to theme-side files under `public/themes/<theme>/`, including HTML templates, CSS, JS, and theme assets.
5. If data cannot be rendered with existing backend methods/routes, the correct action is to report the limitation and adjust the theme to use existing template tags/data variables; do not patch PHP to make the template pass.
6. Any package produced after PHP/controller/config changes is not a valid template package until those backend changes are reverted and the template is revalidated using only theme-side changes.

## Practical gate

Before assigning dev work, main must explicitly state:

```text
Forbidden: application/**/*.php, config/**/*.php, route/**/*.php, thinkphp/**/*.php, any controller/model/config/backend PHP file.
Allowed: public/themes/default/** only, unless the user explicitly authorizes a non-template backend task.
```

Before packaging, test/rule must verify no PHP/controller/config files were modified for the template task.