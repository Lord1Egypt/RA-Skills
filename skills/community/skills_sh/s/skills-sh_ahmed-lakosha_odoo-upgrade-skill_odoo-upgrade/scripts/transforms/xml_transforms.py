#!/usr/bin/env python3
"""XML transformation functions for Odoo version upgrades."""

import re
from pathlib import Path
from typing import List, Tuple

from ..utils import iter_project_files, read_file_safe, write_file_safe


class XmlTransforms:
    """Consolidated XML transformations for Odoo upgrades."""

    def __init__(self, project_path: str | Path, target_version: int = 19):
        self.project_path = Path(project_path)
        self.target_version = target_version
        self.files_modified: list[Path] = []

    def _apply_to_xml_files(self, transform_fn, description: str) -> int:
        """Apply a transform function to all XML files. Returns count of modified files."""
        count = 0
        for xml_file in iter_project_files(self.project_path, ('.xml',)):
            content = read_file_safe(xml_file)
            if content is None:
                continue
            try:
                new_content = transform_fn(content)
                if new_content != content:
                    if write_file_safe(xml_file, new_content):
                        self.files_modified.append(xml_file)
                        count += 1
            except Exception as e:
                print(f"  Error in {description} for {xml_file.name}: {e}")
        return count

    # --- Odoo 19 XML Transforms ---

    def fix_tree_to_list(self) -> int:
        """Convert <tree> tags to <list> and update related references."""
        def transform(content: str) -> str:
            content = re.sub(r'<tree(\s+[^>]*)?>', r'<list\1>', content)
            content = content.replace('</tree>', '</list>')
            # view_mode in XML fields
            content = re.sub(r'(<field name="view_mode">)tree(</field>)', r'\1list\2', content)
            content = re.sub(r'(<field name="view_mode">)tree,', r'\1list,', content)
            content = re.sub(r',tree([,<])', r',list\1', content)
            # view_mode in Python dict literals embedded in XML
            content = re.sub(r"'view_mode':\s*'tree'", r"'view_mode': 'list'", content)
            # XPath expressions
            content = re.sub(r'(xpath[^>]*expr=")//tree', r'\1//list', content)
            content = re.sub(r"(xpath[^>]*expr=')//tree", r"\1//list", content)
            # Remove edit="1" (deprecated in Odoo 19)
            content = re.sub(r'\s+edit=["\']1["\']', '', content)
            return content
        return self._apply_to_xml_files(transform, "tree-to-list")

    def fix_search_view_groups(self) -> int:
        """Remove <group> tags from search views (invalid in Odoo 19)."""
        def transform(content: str) -> str:
            if '<search' not in content:
                return content
            pattern = r'(<search[^>]*>)(.*?)(</search>)'

            def remove_groups(match):
                start, body, end = match.group(1), match.group(2), match.group(3)
                body = re.sub(r'<group[^>]*>', '', body)
                body = body.replace('</group>', '')
                if 'group_by' in body and '<separator/>' not in body:
                    body = re.sub(
                        r'(\s*)(<filter[^>]*group_by[^>]*>)',
                        r'\1<separator/>\1\2', body, count=1
                    )
                return start + body + end

            content = re.sub(pattern, remove_groups, content, flags=re.DOTALL)
            content = re.sub(r'(<group[^>]*)\s+expand=["\'][01]["\']', r'\1', content)
            content = re.sub(r"(<group[^>]*)\s+expand='[01]'", r'\1', content)
            return content
        return self._apply_to_xml_files(transform, "search-groups")

    def fix_kanban_templates(self) -> int:
        """Rename kanban-box to card and remove crm_kanban js_class."""
        def transform(content: str) -> str:
            content = content.replace('t-name="kanban-box"', 't-name="card"')
            content = re.sub(r'\s+js_class=["\']crm_kanban["\']', '', content)
            return content
        return self._apply_to_xml_files(transform, "kanban-templates")

    def fix_cron_numbercall(self) -> int:
        """Remove numbercall field from cron definitions (removed in Odoo 19)."""
        def transform(content: str) -> str:
            content = re.sub(
                r'\s*<field\s+name="numbercall"[^>]*>.*?</field>',
                '', content, flags=re.DOTALL
            )
            content = re.sub(r'\s*<field\s+name="numbercall"[^/]*?/>', '', content)
            return content
        return self._apply_to_xml_files(transform, "cron-numbercall")

    def fix_active_id(self) -> int:
        """Replace active_id with id in context expressions."""
        def transform(content: str) -> str:
            return re.sub(
                r"context=['\"]([^'\"]*?)active_id([^'\"]*?)['\"]",
                r"context='\1id\2'", content
            )
        return self._apply_to_xml_files(transform, "active-id")

    def fix_snippet_options(self) -> int:
        """Comment out website.snippet_options inheritance (removed in Odoo 19)."""
        def transform(content: str) -> str:
            if 'inherit_id="website.snippet_options"' not in content:
                return content
            pattern = r'(<template[^>]*inherit_id="website\.snippet_options"[^>]*>.*?</template>)'
            def comment_template(match):
                tmpl = match.group(1).replace('--', '- -')
                return f'<!-- website.snippet_options removed in Odoo 19\n  {tmpl}\n  -->'
            return re.sub(pattern, comment_template, content, flags=re.DOTALL)
        return self._apply_to_xml_files(transform, "snippet-options")

    def fix_xml_comments(self) -> int:
        """Fix malformed XML comments (nested starts/ends, double hyphens)."""
        def transform(content: str) -> str:
            while re.search(r'<!--[^>]*<!--', content):
                content = re.sub(r'<!--([^>]*)<!--', r'<!-- \1', content)
            while re.search(r'-->[^<]*-->', content):
                content = re.sub(r'-->([^<]*)-->', r'\1 -->', content)
            def fix_hyphens(m):
                inner = m.group(0)[4:-3]
                inner = re.sub(r'--+', '- -', inner)
                return f'<!--{inner}-->'
            content = re.sub(r'<!--.*?-->', fix_hyphens, content, flags=re.DOTALL)
            return content
        return self._apply_to_xml_files(transform, "xml-comments")

    # --- Odoo 18+ XML Transforms ---

    def fix_attrs_to_inline(self) -> int:
        """Convert attrs={'invisible':[...]} to inline invisible='...' expressions."""
        import json as _json

        def _domain_to_expr(domain_str: str) -> str:
            m = re.match(
                r"""\[\s*\(\s*['"](\w+)['"]\s*,\s*['"]([!=<>]{1,2})['"]\s*,\s*['"]?([^'"\)\]]+)['"]?\s*\)\s*\]""",
                domain_str.strip(),
            )
            if m:
                field, op, value = m.group(1), m.group(2), m.group(3).strip()
                if not re.match(r'^-?\d+(\.\d+)?$', value) and value not in ('True', 'False', 'None'):
                    value = f"'{value}'"
                return f"{field} {op} {value}"
            return domain_str

        def _convert_attrs(match):
            original = match.group(0)
            attrs_content = match.group(1)
            try:
                normalised = attrs_content.replace("'", '"')
                attrs_dict = _json.loads(normalised)
            except Exception:
                return original
            parts = []
            for attr in ('invisible', 'required', 'readonly', 'column_invisible'):
                if attr in attrs_dict:
                    expr = _domain_to_expr(str(attrs_dict[attr]).replace('"', "'"))
                    parts.append(f'{attr}="{expr}"')
            return ' '.join(parts) if parts else original

        attrs_re = re.compile(r"""attrs\s*=\s*["']\{([^}]+)\}["']""", re.DOTALL)

        def transform(content: str) -> str:
            return attrs_re.sub(_convert_attrs, content)
        return self._apply_to_xml_files(transform, "attrs-to-inline")

    def apply_all(self) -> dict[str, int]:
        """Apply all applicable XML transformations based on target version."""
        results = {}

        # Always safe
        results['xml_comments'] = self.fix_xml_comments()

        # Odoo 18+ transforms
        if self.target_version >= 18:
            results['attrs_to_inline'] = self.fix_attrs_to_inline()

        # Odoo 19+ transforms
        if self.target_version >= 19:
            results['tree_to_list'] = self.fix_tree_to_list()
            results['search_groups'] = self.fix_search_view_groups()
            results['kanban_templates'] = self.fix_kanban_templates()
            results['cron_numbercall'] = self.fix_cron_numbercall()
            results['active_id'] = self.fix_active_id()
            results['snippet_options'] = self.fix_snippet_options()

        return results

    def apply_all_odoo19(self) -> dict[str, int]:
        """Deprecated: use apply_all() instead."""
        return self.apply_all()
