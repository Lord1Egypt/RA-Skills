# OCA Conventions and Guidelines

## Module Structure

### Naming Conventions
- Use singular form in module names (except when compound of module name or object that is already plural)
- For base modules: prefix with `base_` (e.g., `base_location_nuts`)
- For localization modules: prefix with `l10n_CC_` where CC is country code (e.g., `l10n_es_pos`)
- When extending an Odoo module: prefix with that module's name (e.g., `mail_forward`)
- When combining Odoo + OCA modules: Odoo's name goes first (e.g., `crm_partner_firstname`)

### Directory Structure

```
addons/<module_name>/
├── controllers/
│   ├── __init__.py
│   └── main.py
├── data/
│   └── <main_model>.xml
├── demo/
│   └── <model_name>_demo.xml
├── i18n/
│   ├── <language_code>.po
│   └── <module_name>.pot
├── migrations/
│   └── <version>/
│       ├── pre-migration.py
│       └── post-migration.py
├── models/
│   ├── __init__.py
│   ├── <main_model>.py
│   └── <inherited_model>.py
├── readme/
│   ├── CONTRIBUTORS.rst
│   ├── DESCRIPTION.rst
│   └── USAGE.rst
├── security/
│   ├── ir.model.access.csv
│   └── <main_model>_security.xml
├── static/
│   ├── src/
│   │   ├── js/
│   │   ├── css/
│   │   └── xml/
│   └── img/
├── tests/
│   ├── __init__.py
│   └── test_<feature>.py
├── views/
│   ├── <main_model>_views.xml
│   └── report_<qweb_report>.xml
├── wizards/
│   ├── __init__.py
│   ├── <wizard_model>.py
│   └── <wizard_model>_views.xml
├── README.rst (auto-generated)
├── __init__.py
├── __manifest__.py
├── exceptions.py (optional)
└── hooks.py (optional)
```

## __manifest__.py

### Required Keys
```python
{
    'name': 'Module Name',
    'version': '17.0.1.0.0',
    'category': 'Category',
    'license': 'AGPL-3',  # or LGPL-3
    'author': 'Company Name, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/<repo>',
    'depends': ['base'],
    'data': [],
    'installable': True,
}
```

### Version Numbering
Format: `{odoo_version}.x.y.z`
- x (Major): Breaking changes to data model or views (needs migration)
- y (Minor): New features, backward compatible (needs upgrade)
- z (Patch): Bug fixes (needs restart)

### External Dependencies
```python
{
    'external_dependencies': {
        'bin': ['external_binary'],
        'python': ['library_name'],
    },
}
```

## File Naming Conventions

- Models: `models/<model_name>.py`
- Data: `data/<model_name>_data.xml`
- Demo: `demo/<model_name>_demo.xml`
- Views: `views/<model_name>_views.xml`
- Templates: `templates/<model_name>_template.xml`
- Controllers: `controllers/main.py` (or split if multiple)
- Static files: `static/src/{js,css,xml}/<module_name>.{js,css,xml}`

## XML Conventions

### Format
- Indent with 4 spaces
- Place `id` before `model`
- For fields: `name` first, then value, then other attributes
- Don't prefix xmlid with module name
- Use `<odoo>` tag (not `<data>`)
- Use `<odoo noupdate='1'>` for non-updatable data

### Naming xml_id

**Data Records:**
```xml
<record id="<model_name>_<record_name>" model="...">
```

**Views:**
```xml
<record id="<model_name>_view_<view_type>" model="ir.ui.view">
```

**Actions:**
```xml
<record id="<model_name>_action" model="ir.actions.act_window">
```

**Groups:**
```xml
<record id="<model_name>_group_<group_name>" model="res.groups">
```

**Rules:**
```xml
<record id="<model_name>_rule_<concerned_group>" model="ir.rule">
```

**Demo Records:**
Suffix with `_demo`:
```xml
<record id="<model_name>_<record_name>_demo" model="...">
```

### Inherited Views
```xml
<record id="original_id" model="ir.ui.view">
    <field name="inherit_id" ref="original_module.original_id"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='field_name']" position="after">
            <!-- Your content -->
        </xpath>
    </field>
</record>
```

## Python Conventions

### Imports Order
1. Standard library
2. Known third party
3. Odoo imports (`odoo`)
4. Odoo module imports (`odoo.addons`)
5. Local imports (relative)
6. Unknown third party

```python
import base64
import logging

import lxml

import odoo
from odoo import api, fields, models, _
from odoo.exceptions import UserError

from odoo.addons.website.models.website import slug

from . import utils
```

### External Dependencies
```python
try:
    import external_library
except ImportError:
    _logger.debug('Cannot import external_library')
```

### Model Structure
```python
class ModelName(models.Model):
    # Private attributes
    _name = 'model.name'
    _inherit = ['model.name', 'mail.thread']
    _description = 'Model Description'
    _order = 'name'
    
    # Fields
    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner')
    line_ids = fields.One2many('model.line', 'parent_id')
    
    # SQL Constraints
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique'),
    ]
    
    # Default methods
    def _default_name(self):
        return 'Default'
    
    # Compute methods
    @api.depends('line_ids')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.line_ids.mapped('amount'))
    
    # Constraints
    @api.constrains('name')
    def _check_name(self):
        if not self.name:
            raise UserError(_('Name is required'))
    
    # Onchange
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.email = self.partner_id.email
    
    # CRUD methods
    def create(self, vals):
        return super().create(vals)
    
    # Action methods
    def action_validate(self):
        self.ensure_one()
        self.state = 'done'
    
    # Business methods
    def custom_method(self):
        pass
```

### Method Naming Patterns
- Compute: `_compute_<field_name>`
- Inverse: `_inverse_<field_name>`
- Search: `_search_<field_name>`
- Default: `_default_<field_name>`
- Onchange: `_onchange_<field_name>`
- Constraint: `_check_<constraint_name>`
- Action: `action_<action_name>`

### Field Naming
- Many2one: suffix with `_id` (e.g., `partner_id`)
- One2many/Many2many: suffix with `_ids` (e.g., `line_ids`)
- Use lowercase with underscores (snake_case)

## Installation Hooks

Place in `hooks.py`:
```python
def pre_init_hook(cr):
    """Hook before module installation"""
    pass

def post_init_hook(cr, registry):
    """Hook after module installation"""
    pass

def uninstall_hook(cr, registry):
    """Hook before module uninstallation"""
    pass

def post_load():
    """Hook after loading (for monkey patches)"""
    pass
```

Reference in `__manifest__.py`:
```python
{
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'post_load': 'post_load',
}
```

Import in `__init__.py`:
```python
from .hooks import pre_init_hook, post_init_hook, uninstall_hook, post_load
```

## Git Commit Messages

Format:
```
[TAG] module_name: short summary (max 50 chars)

Detailed explanation of the changes. Multiple lines allowed.
Each line max 80 characters.
```

Tags:
- `[ADD]` - New module or feature
- `[FIX]` - Bug fix
- `[REF]` - Refactoring
- `[REM]` - Removal
- `[IMP]` - Improvement
- `[MIG]` - Migration to new version
- `[I18N]` - Translation
- `[REL]` - Release

## Tests

- Place in `tests/` directory
- Name files `test_<feature>.py`
- Inherit from `TransactionCase` or `SavepointCase`
- Use `@tagged('post_install', '-at_install')` for tests that need demo data
- Test with minimal permissions using `@users()` decorator

```python
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestModule(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner'
        })
    
    def test_feature(self):
        self.assertEqual(self.partner.name, 'Test Partner')
```
