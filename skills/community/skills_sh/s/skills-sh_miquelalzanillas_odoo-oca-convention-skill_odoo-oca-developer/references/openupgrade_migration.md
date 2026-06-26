# OpenUpgrade Migration Guide

## What is OpenUpgrade?

OpenUpgrade is a framework provided by OCA to migrate Odoo databases from one major version to another. It handles the necessary data transformations and adaptations required when upgrading between versions.

## Migration Workflow

### 1. Prepare Migration Scripts

Migration scripts should be placed in the module's `migrations/` directory:

```
module_name/
└── migrations/
    └── 17.0.1.0.0/
        ├── pre-migration.py
        ├── post-migration.py
        └── noupdate_changes.xml
```

### 2. Pre-Migration Script

Executed before the module is loaded:

```python
# migrations/17.0.1.0.0/pre-migration.py
from openupgradelib import openupgrade

@openupgrade.migrate()
def migrate(env, version):
    # Rename tables
    openupgrade.rename_tables(env.cr, [
        ('old_table_name', 'new_table_name'),
    ])
    
    # Rename columns
    openupgrade.rename_columns(env.cr, {
        'table_name': [
            ('old_column', 'new_column'),
        ],
    })
    
    # Rename fields
    openupgrade.rename_fields(env, [
        ('model.name', 'model_name', 'old_field', 'new_field'),
    ])
    
    # Rename models
    openupgrade.rename_models(env.cr, [
        ('old.model.name', 'new.model.name'),
    ])
    
    # Rename xmlids
    openupgrade.rename_xmlids(env.cr, [
        ('module_name.old_xmlid', 'module_name.new_xmlid'),
    ])
```

### 3. Post-Migration Script

Executed after the module is loaded:

```python
# migrations/17.0.1.0.0/post-migration.py
from openupgradelib import openupgrade

@openupgrade.migrate()
def migrate(env, version):
    # Update field values
    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name('old_field'),
        'new_field',
        [('old_value', 'new_value')],
        table='model_name',
    )
    
    # Fill computed fields
    env['model.name'].search([])._compute_field_name()
    
    # Update related records
    for record in env['model.name'].search([]):
        record.write({'field': 'value'})
```

### 4. XML Changes for Non-Updatable Data

```xml
<!-- migrations/17.0.1.0.0/noupdate_changes.xml -->
<odoo>
    <function model="ir.model.data" name="_update_xmlids">
        <value eval="[
            ('module_name.xmlid_name', {
                'field_name': 'new_value',
            }),
        ]"/>
    </function>
</odoo>
```

## Common Migration Tasks

### Renaming Fields
```python
openupgrade.rename_fields(env, [
    ('res.partner', 'res_partner', 'old_name', 'new_name'),
])
```

### Renaming Models
```python
openupgrade.rename_models(env.cr, [
    ('old.model', 'new.model'),
])
```

### Renaming Tables
```python
openupgrade.rename_tables(env.cr, [
    ('old_table', 'new_table'),
])
```

### Renaming Columns
```python
openupgrade.rename_columns(env.cr, {
    'table_name': [
        ('old_column', 'new_column'),
    ],
})
```

### Mapping Selection Values
```python
openupgrade.map_values(
    env.cr,
    openupgrade.get_legacy_name('state'),
    'state',
    [
        ('draft', 'pending'),
        ('confirm', 'confirmed'),
    ],
    table='sale_order',
)
```

### Moving Fields to Another Model
```python
# Pre-migration: Copy data to temporary column
openupgrade.copy_columns(env.cr, {
    'old_model': [
        ('field_name', None, None),
    ],
})

# Post-migration: Transfer data to new model
cr = env.cr
cr.execute("""
    UPDATE new_model nm
    SET field_name = om.{}
    FROM old_model om
    WHERE nm.old_model_id = om.id
""".format(openupgrade.get_legacy_name('field_name')))
```

### Deleting Obsolete Data
```python
openupgrade.delete_records_safely_by_xml_id(
    env, [
        'module_name.xmlid_to_delete',
    ]
)
```

### Updating Many2many Relations
```python
openupgrade.m2o_to_x2m(
    env.cr,
    env['new.model'],
    'old_model',
    'm2m_table_name',
    'new_model_id',
    'old_model_id',
)
```

## Analysis Files

OpenUpgrade generates analysis files to help identify changes:

### Generate Analysis
```bash
# In the source version
odoo-bin -d database --update=module_name --stop-after-init

# Generate comparison
python3 scripts/compare_analysis.py \
    --old-analysis=analysis/old_version \
    --new-analysis=analysis/new_version \
    --output=migrations/new_version
```

### Analysis File Format
```
---Fields in module.model_name---
module_name | model_name | field_name | type | relation | required | ...
```

## Migration Best Practices

### 1. Use OpenUpgrade Helper Functions
Always use openupgradelib functions instead of direct SQL:
```python
# Good
openupgrade.rename_columns(env.cr, {...})

# Bad - avoid
env.cr.execute("ALTER TABLE...")
```

### 2. Handle Missing Data Gracefully
```python
if openupgrade.column_exists(env.cr, 'table_name', 'old_column'):
    # Migrate data
    pass
```

### 3. Test Thoroughly
- Test migration on a copy of production database
- Verify all custom modules work after migration
- Check data integrity
- Test with and without demo data

### 4. Document Breaking Changes
In README.rst, add a migration note:
```rst
Migration from 16.0
~~~~~~~~~~~~~~~~~~~

* Field ``old_field`` has been renamed to ``new_field``
* Model ``old.model`` has been merged into ``new.model``
```

### 5. Maintain Backward Compatibility
```python
# Store legacy field name for later migration steps
openupgrade.rename_fields(env, [
    ('model.name', 'model_name', 'old_field', 'new_field'),
], no_deep=True)
```

## Common Patterns

### Pattern 1: Field Type Change
```python
# Pre-migration
openupgrade.rename_fields(env, [
    ('model.name', 'model_name', 'old_field', 'old_field_temp'),
])

# Post-migration
env['model.name'].search([]).write({
    'new_field': lambda r: convert_value(r.old_field_temp)
})
```

### Pattern 2: Split/Merge Models
```python
# Post-migration: Split model
for old_record in env['old.model'].search([]):
    env['new.model1'].create({...})
    env['new.model2'].create({...})
```

### Pattern 3: Update Computed/Related Fields
```python
# Post-migration
env['model.name'].search([])._compute_field_name()
```

## OpenUpgrade API Reference

### Core Functions

```python
# Column operations
openupgrade.rename_columns(cr, column_spec)
openupgrade.copy_columns(cr, column_spec)
openupgrade.column_exists(cr, table, column)

# Table operations
openupgrade.rename_tables(cr, table_spec)
openupgrade.table_exists(cr, table)

# Model/Field operations
openupgrade.rename_models(cr, model_spec)
openupgrade.rename_fields(env, field_spec)
openupgrade.rename_xmlids(cr, xmlid_spec)

# Data migration
openupgrade.map_values(cr, source_column, target_column, mapping, table=None)
openupgrade.delete_records_safely_by_xml_id(env, xml_ids)

# Utilities
openupgrade.get_legacy_name(name)
openupgrade.logged_query(cr, query, args=None)
```

## Resources

- OpenUpgrade Documentation: https://oca.github.io/OpenUpgrade/
- OpenUpgrade Repository: https://github.com/OCA/OpenUpgrade
- Analysis Files: Check existing migrations in OpenUpgrade repository
- Migration Scripts Examples: Browse `migrations/` folders in OCA modules
