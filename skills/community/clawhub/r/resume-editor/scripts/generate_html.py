#!/usr/bin/env python3
"""
Generate styled HTML resume from JSON data.
Supports multiple themes and languages.
"""

import argparse
import html as html_escape
import json
import sys
from pathlib import Path

from resume_utils import (
    DEFAULT_THEME,
    SUPPORTED_LANGUAGES,
    list_available_themes,
    get_localized_text,
    normalize_resume_data,
    resolve_theme_assets,
    resolve_photo_src,
    validate_resume_data,
    ensure_string_list,
)


def escape_text(text):
    """Escape HTML special characters to prevent injection."""
    if text is None:
        return ""
    return html_escape.escape(str(text))


def load_template(theme_path):
    """Load HTML template file."""
    with open(theme_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_css(css_path):
    """Load CSS stylesheet."""
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()


def build_edit_script(resume_data, language):
    """Build inline JS/CSS for edit mode. Returns HTML string to inject before </body>."""
    labels = get_localized_text(language)
    json_snapshot = json.dumps(resume_data, ensure_ascii=False, indent=2)
    # Escape for safe embedding in HTML
    json_snapshot_escaped = json_snapshot.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')

    return f'''
<script type="application/json" id="resume-source-data">
{json_snapshot_escaped}
</script>
<style>
/* Edit button */
#resume-edit-btn {{
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 99999;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: rgba(30, 41, 59, 0.85);
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    opacity: 0.25;
    transition: opacity 0.2s, transform 0.15s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}}
#resume-edit-btn:hover {{
    opacity: 1;
    transform: scale(1.08);
}}
/* Toolbar */
#resume-edit-toolbar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100000;
    height: 48px;
    background: #1e293b;
    color: #f1f5f9;
    display: none;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}}
#resume-edit-toolbar.visible {{
    display: flex;
}}
#resume-edit-toolbar .toolbar-label {{
    font-weight: 600;
    letter-spacing: 0.02em;
}}
#resume-edit-toolbar .toolbar-actions {{
    display: flex;
    gap: 8px;
}}
#resume-edit-toolbar button {{
    padding: 6px 16px;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
}}
.toolbar-btn-copy {{
    background: #22c55e;
    color: #fff;
}}
.toolbar-btn-copy:hover {{
    background: #16a34a;
}}
.toolbar-btn-cancel {{
    background: #ef4444;
    color: #fff;
}}
.toolbar-btn-cancel:hover {{
    background: #dc2626;
}}
/* Toast notification */
#resume-edit-toast {{
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100001;
    background: #1e293b;
    color: #f1f5f9;
    padding: 10px 24px;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 14px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    display: none;
    opacity: 0;
    transition: opacity 0.25s;
}}
#resume-edit-toast.show {{
    display: block;
    opacity: 1;
}}
/* Editable state visual cues */
body.resume-editing {{
    padding-top: 48px !important;
}}
body.resume-editing [contenteditable="true"] {{
    outline: 1px dashed rgba(100, 116, 200, 0.45);
    outline-offset: 3px;
    border-radius: 2px;
    transition: outline-color 0.15s, background 0.15s;
}}
body.resume-editing [contenteditable="true"]:focus {{
    outline: 1px solid rgba(100, 116, 200, 0.7);
    background: rgba(66, 133, 244, 0.05);
}}
/* Dark background override (sidebar / gradient header) */
body.resume-editing .sidebar [contenteditable="true"],
body.resume-editing .resume-header [contenteditable="true"] {{
    outline-color: rgba(200, 200, 255, 0.4);
}}
body.resume-editing .sidebar [contenteditable="true"]:focus,
body.resume-editing .resume-header [contenteditable="true"]:focus {{
    outline-color: rgba(200, 200, 255, 0.7);
    background: rgba(255, 255, 255, 0.08);
}}
/* List add/remove buttons */
.edit-add-btn, .edit-remove-btn {{
    display: none;
}}
/* Section-level "Add entry" buttons (hidden outside edit mode) */
.edit-add-entry-btn {{
    display: none;
}}
body.resume-editing .edit-add-entry-btn {{
    display: inline-block;
    margin-top: 12px;
    padding: 6px 14px;
    border: 1px dashed rgba(100, 116, 200, 0.6);
    border-radius: 6px;
    background: rgba(100, 116, 200, 0.08);
    color: rgba(100, 116, 200, 1);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
}}
body.resume-editing .edit-add-entry-btn:hover {{
    background: rgba(100, 116, 200, 0.18);
}}
body.resume-editing .edit-add-btn {{
    display: inline-block;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1px dashed rgba(100, 116, 200, 0.5);
    background: transparent;
    color: rgba(100, 116, 200, 0.7);
    font-size: 14px;
    line-height: 1;
    cursor: pointer;
    margin-left: 4px;
    vertical-align: middle;
    transition: background 0.15s;
}}
body.resume-editing .edit-add-btn:hover {{
    background: rgba(100, 116, 200, 0.12);
}}
body.resume-editing li,
body.resume-editing .skill-item {{
    position: relative;
}}
body.resume-editing li .edit-remove-btn,
body.resume-editing .skill-item .edit-remove-btn {{
    display: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: none;
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    font-size: 12px;
    line-height: 1;
    cursor: pointer;
    transition: background 0.15s;
    vertical-align: middle;
    margin-left: 4px;
    padding: 0;
}}
/* li: overlay button absolutely positioned to the right */
body.resume-editing li .edit-remove-btn {{
    position: absolute;
    right: -4px;
    top: 50%;
    transform: translateY(-50%);
}}
body.resume-editing li:hover .edit-remove-btn,
body.resume-editing .skill-item:hover .edit-remove-btn,
body.resume-editing .skill-item:focus-within .edit-remove-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}
body.resume-editing li .edit-remove-btn:hover,
body.resume-editing .skill-item .edit-remove-btn:hover {{
    background: rgba(239, 68, 68, 0.3);
}}
/* Print: hide all edit UI */
@media print {{
    #resume-edit-btn,
    #resume-edit-toolbar,
    #resume-edit-toast,
    .edit-add-btn,
    .edit-remove-btn,
    .edit-add-entry-btn {{
        display: none !important;
    }}
    body.resume-editing {{
        padding-top: 0 !important;
    }}
    body.resume-editing [contenteditable] {{
        outline: none !important;
        background: transparent !important;
    }}
}}
</style>
<button id="resume-edit-btn" title="{escape_text(labels["edit_resume"])}">&#9998;</button>
<div id="resume-edit-toolbar">
    <span class="toolbar-label">{escape_text(labels["editing_resume"])}</span>
    <div class="toolbar-actions">
        <button class="toolbar-btn-copy" id="edit-copy-btn">{escape_text(labels["copy_json"])}</button>
        <button class="toolbar-btn-cancel" id="edit-cancel-btn">{escape_text(labels["done"])}</button>
    </div>
</div>
<div id="resume-edit-toast"></div>
<script>
(function() {{
    var btn = document.getElementById('resume-edit-btn');
    var toolbar = document.getElementById('resume-edit-toolbar');
    var copyBtn = document.getElementById('edit-copy-btn');
    var cancelBtn = document.getElementById('edit-cancel-btn');
    var toast = document.getElementById('resume-edit-toast');
    var isEditing = false;
    var originalHtml = null;

    var EDITABLE_SELECTORS = [
        '.resume-header .name',
        '.contact-email a',
        '.contact-phone',
        '.contact-location',
        '.contact-linkedin a',
        '.contact-github a',
        '[data-section="summary"] p',
        '.experience-item .company-name',
        '.experience-item .position',
        '.experience-item .period',
        '.experience-item .location',
        '.experience-item .experience-description',
        '.experience-item .achievements li',
        '.experience-item .responsibilities li',
        '.education-item .institution',
        '.education-item .degree',
        '.education-item .period',
        '.education-item .location',
        '.education-item .gpa',
        '.education-item .honors',
        '.project-item .project-name',
        '.project-item .role',
        '.project-item .period',
        '.project-item .technologies',
        '.project-item .project-description',
        '.project-item .achievements li',
        '.skill-category .category-title',
        '.skill-category .skill-item'
    ];

    var LIST_CONTAINERS = '.achievements, .responsibilities, .skill-list';

    function getOriginalData() {{
        var el = document.getElementById('resume-source-data');
        if (!el) return {{}};
        return JSON.parse(el.textContent);
    }}

    function showToast(msg, duration) {{
        toast.textContent = msg;
        toast.classList.add('show');
        toast.style.display = 'block';
        setTimeout(function() {{
            toast.classList.remove('show');
            setTimeout(function() {{ toast.style.display = 'none'; }}, 300);
        }}, duration || 2000);
    }}

    function toggleEditMode() {{
        if (!isEditing) {{
            enterEditMode();
        }} else {{
            exitEditMode(true);
        }}
    }}

    function enterEditMode() {{
        isEditing = true;
        document.body.classList.add('resume-editing');
        toolbar.classList.add('visible');
        btn.innerHTML = '&#10005;';
        btn.title = {json.dumps(labels["exit_edit_mode"], ensure_ascii=False)};

        EDITABLE_SELECTORS.forEach(function(sel) {{
            var els = document.querySelectorAll(sel);
            els.forEach(function(el) {{
                el.setAttribute('contenteditable', 'true');
            }});
        }});

        // Suppress link navigation during editing
        document.querySelectorAll('.contact-info a').forEach(function(a) {{
            a.addEventListener('click', preventNav);
        }});

        // Add list item management buttons
        addListButtons();
        addEntryButtons();
    }}

    function preventNav(e) {{
        if (isEditing) {{
            e.preventDefault();
            e.stopPropagation();
        }}
    }}

    function exitEditMode(save) {{
        if (!isEditing) return;
        isEditing = false;
        document.body.classList.remove('resume-editing');
        toolbar.classList.remove('visible');
        btn.innerHTML = '&#9998;';
        btn.title = {json.dumps(labels["edit_resume"], ensure_ascii=False)};

        EDITABLE_SELECTORS.forEach(function(sel) {{
            var els = document.querySelectorAll(sel);
            els.forEach(function(el) {{
                el.removeAttribute('contenteditable');
            }});
        }});

        // Restore link navigation
        document.querySelectorAll('.contact-info a').forEach(function(a) {{
            a.removeEventListener('click', preventNav);
        }});

        removeListButtons();
        removeEntryButtons();
    }}

    function makeEntryButton(label, sectionType) {{
        var btn = document.createElement('button');
        btn.className = 'edit-add-entry-btn';
        btn.setAttribute('data-edit-control', '');
        btn.setAttribute('data-section-type', sectionType);
        btn.textContent = '+ ' + label;
        btn.addEventListener('click', function() {{ appendBlankEntry(sectionType); }});
        return btn;
    }}

    function addEntryButtons() {{
        var sectionMap = [
            ['experience', {json.dumps(labels["add_experience"], ensure_ascii=False)}],
            ['education', {json.dumps(labels["add_education"], ensure_ascii=False)}],
            ['projects', {json.dumps(labels["add_project"], ensure_ascii=False)}],
        ];
        sectionMap.forEach(function(pair) {{
            var sectionEl = document.querySelector('[data-section="' + pair[0] + '"]');
            if (sectionEl) sectionEl.appendChild(makeEntryButton(pair[1], pair[0]));
        }});
    }}

    function removeEntryButtons() {{
        document.querySelectorAll('.edit-add-entry-btn').forEach(function(b) {{ b.remove(); }});
    }}

    function applyEditableToEntry(root) {{
        // Mark text fields editable and attach list buttons within a newly added entry
        var selectorsByType = {{
            experience: ['.company-name', '.position', '.period', '.location',
                         '.experience-description', '.achievements li', '.responsibilities li'],
            education: ['.institution', '.degree', '.period', '.location', '.gpa', '.honors'],
            projects: ['.project-name', '.role', '.period', '.technologies',
                       '.project-description', '.achievements li'],
        }};
        var selectors = selectorsByType[root.getAttribute('data-entry-type')] || [];
        selectors.forEach(function(sel) {{
            root.querySelectorAll(sel).forEach(function(el) {{
                el.setAttribute('contenteditable', 'true');
            }});
        }});
        root.querySelectorAll(LIST_CONTAINERS).forEach(function(container) {{
            var isSkillList = container.classList.contains('skill-list');
            var addBtn = document.createElement('button');
            addBtn.className = 'edit-add-btn';
            addBtn.setAttribute('data-edit-control', '');
            addBtn.textContent = '+';
            addBtn.title = {json.dumps(labels["add_item"], ensure_ascii=False)};
            addBtn.addEventListener('click', function() {{
                var item = document.createElement(isSkillList ? 'span' : 'li');
                if (isSkillList) item.className = 'skill-item';
                item.setAttribute('contenteditable', 'true');
                item.textContent = {json.dumps(labels["new_item"], ensure_ascii=False)};
                attachRemoveBtn(item);
                container.appendChild(item);
                item.focus();
            }});
            container.parentNode.insertBefore(addBtn, container.nextSibling);
            var itemSelector = isSkillList ? '.skill-item' : 'li';
            container.querySelectorAll(itemSelector).forEach(attachRemoveBtn);
        }});
    }}

    function appendBlankEntry(sectionType) {{
        var sectionEl = document.querySelector('[data-section="' + sectionType + '"]');
        if (!sectionEl) return;
        var node = document.createElement('div');
        // Template mirrors generate_html.py output structure
        if (sectionType === 'experience') {{
            node.innerHTML =
                '<div class="experience-item" data-entry-type="experience">' +
                '<div class="experience-header"><h3 class="company-name">Company</h3>' +
                '<div class="position-period"><span class="position">Position</span>' +
                '<span class="period"></span></div></div>' +
                '<p class="experience-description"></p>' +
                '<ul class="responsibilities"></ul><ul class="achievements"></ul></div>';
        }} else if (sectionType === 'education') {{
            node.innerHTML =
                '<div class="education-item" data-entry-type="education">' +
                '<div class="education-header"><h3 class="institution">Institution</h3>' +
                '<div class="degree-period"><span class="degree">Degree</span>' +
                '<span class="period"></span></div></div></div>';
        }} else if (sectionType === 'projects') {{
            node.innerHTML =
                '<div class="project-item" data-entry-type="projects">' +
                '<div class="project-header"><h3 class="project-name">Project</h3>' +
                '<span class="role"></span><span class="period"></span></div>' +
                '<p class="project-description"></p><ul class="achievements"></ul></div>';
        }}
        var entry = node.firstElementChild;
        // Insert before the "+ Add" button
        sectionEl.insertBefore(entry, sectionEl.querySelector('.edit-add-entry-btn'));
        applyEditableToEntry(entry);
        entry.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        var firstField = entry.querySelector('.company-name, .institution, .project-name');
        if (firstField) {{
            firstField.focus();
            var range = document.createRange();
            range.selectNodeContents(firstField);
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }}
    }}

    function addListButtons() {{
        document.querySelectorAll(LIST_CONTAINERS).forEach(function(container) {{
            container.style.position = 'relative';
            var isSkillList = container.classList.contains('skill-list');
            var addBtn = document.createElement('button');
            addBtn.className = 'edit-add-btn';
            addBtn.textContent = '+';
            addBtn.title = {json.dumps(labels["add_item"], ensure_ascii=False)};
            addBtn.addEventListener('click', function() {{
                var item = document.createElement(isSkillList ? 'span' : 'li');
                if (isSkillList) item.className = 'skill-item';
                item.setAttribute('contenteditable', 'true');
                item.textContent = {json.dumps(labels["new_item"], ensure_ascii=False)};
                attachRemoveBtn(item);
                container.appendChild(item);
                item.focus();
                var range = document.createRange();
                range.selectNodeContents(item);
                var sel = window.getSelection();
                sel.removeAllRanges();
                sel.addRange(range);
            }});
            container.parentNode.insertBefore(addBtn, container.nextSibling);

            var itemSelector = isSkillList ? '.skill-item' : 'li';
            container.querySelectorAll(itemSelector).forEach(attachRemoveBtn);
        }});
    }}

    function attachRemoveBtn(item) {{
        var rmBtn = document.createElement('button');
        rmBtn.className = 'edit-remove-btn';
        rmBtn.setAttribute('aria-hidden', 'true');
        rmBtn.setAttribute('data-edit-control', '');
        rmBtn.textContent = '\\u00d7';
        rmBtn.title = {json.dumps(labels["remove_item"], ensure_ascii=False)};
        rmBtn.addEventListener('click', function(e) {{
            e.stopPropagation();
            item.remove();
        }});
        item.appendChild(rmBtn);
    }}

    function textWithoutControls(el) {{
        var clone = el.cloneNode(true);
        clone.querySelectorAll('[data-edit-control]').forEach(function(n) {{ n.remove(); }});
        return clone.textContent.trim();
    }}

    function removeListButtons() {{
        document.querySelectorAll('.edit-add-btn').forEach(function(b) {{ b.remove(); }});
        document.querySelectorAll('.edit-remove-btn').forEach(function(b) {{ b.remove(); }});
    }}

    function extractToJson() {{
        var src = getOriginalData();
        var result = JSON.parse(JSON.stringify(src)); // deep clone

        // Personal
        var name = document.querySelector('.resume-header .name');
        if (name && result.personal) result.personal.name = name.textContent.trim();

        var emailLink = document.querySelector('.contact-email a');
        if (emailLink && result.personal) {{
            result.personal.email = emailLink.textContent.trim();
        }}

        var phone = document.querySelector('.contact-phone');
        if (phone && result.personal) result.personal.phone = phone.textContent.trim();

        var location = document.querySelector('.contact-location');
        if (location && result.personal) result.personal.location = location.textContent.trim();

        var linkedin = document.querySelector('.contact-linkedin a');
        if (linkedin && result.personal) result.personal.linkedin = linkedin.textContent.trim();

        var github = document.querySelector('.contact-github a');
        if (github && result.personal) result.personal.github = github.textContent.trim();

        // Summary
        var summaryP = document.querySelector('[data-section="summary"] p');
        if (summaryP) result.summary = summaryP.textContent.trim();

        // Experience
        if (result.experience) {{
            var expItems = document.querySelectorAll('.experience-item');
            for (var i = 0; i < expItems.length; i++) {{
                if (!result.experience[i]) result.experience[i] = {{}};
                var item = expItems[i];
                var el;

                el = item.querySelector('.company-name');
                if (el) result.experience[i].company = el.textContent.trim();

                el = item.querySelector('.position');
                if (el) result.experience[i].position = el.textContent.trim();

                el = item.querySelector('.period');
                if (el) result.experience[i].period = el.textContent.trim();

                el = item.querySelector('.location');
                if (el) result.experience[i].location = el.textContent.trim();

                el = item.querySelector('.experience-description');
                if (el) result.experience[i].description = el.textContent.trim();

                el = item.querySelector('.responsibilities');
                if (el) {{
                    result.experience[i].responsibilities = [];
                    el.querySelectorAll('li').forEach(function(li) {{
                        var t = textWithoutControls(li);
                        if (t) result.experience[i].responsibilities.push(t);
                    }});
                }}

                el = item.querySelector('.achievements');
                if (el) {{
                    result.experience[i].achievements = [];
                    el.querySelectorAll('li').forEach(function(li) {{
                        var t = textWithoutControls(li);
                        if (t) result.experience[i].achievements.push(t);
                    }});
                }}
            }}
        }}

        // Education
        if (result.education) {{
            var eduItems = document.querySelectorAll('.education-item');
            for (var i = 0; i < eduItems.length; i++) {{
                if (!result.education[i]) result.education[i] = {{}};
                var item = eduItems[i];
                var el;

                el = item.querySelector('.institution');
                if (el) result.education[i].institution = el.textContent.trim();

                el = item.querySelector('.degree');
                if (el) result.education[i].degree = el.textContent.trim();

                el = item.querySelector('.period');
                if (el) result.education[i].period = el.textContent.trim();

                el = item.querySelector('.location');
                if (el) result.education[i].location = el.textContent.trim();

                el = item.querySelector('.gpa');
                if (el) {{
                    var gpaText = el.textContent.trim();
                    result.education[i].gpa = gpaText.replace(/^GPA:\\s*/, '');
                }}

                el = item.querySelector('.honors');
                if (el) {{
                    var honorsText = el.textContent.trim();
                    var cleaned = honorsText.replace(/^[^:]+:\\s*/, '');
                    result.education[i].honors = cleaned.split(',').map(function(s) {{ return s.trim(); }}).filter(Boolean);
                }}
            }}
        }}

        // Projects
        if (result.projects) {{
            var projItems = document.querySelectorAll('.project-item');
            for (var i = 0; i < projItems.length; i++) {{
                if (!result.projects[i]) result.projects[i] = {{}};
                var item = projItems[i];
                var el;

                el = item.querySelector('.project-name');
                if (el) result.projects[i].name = el.textContent.trim();

                el = item.querySelector('.role');
                if (el) result.projects[i].role = el.textContent.trim();

                el = item.querySelector('.period');
                if (el) result.projects[i].period = el.textContent.trim();

                el = item.querySelector('.technologies');
                if (el) {{
                    var techText = el.textContent.trim();
                    var cleaned = techText.replace(/^[^:]+:\\s*/, '');
                    result.projects[i].technologies = cleaned.split(',').map(function(s) {{ return s.trim(); }}).filter(Boolean);
                }}

                el = item.querySelector('.project-description');
                if (el) result.projects[i].description = el.textContent.trim();

                el = item.querySelector('.achievements');
                if (el) {{
                    result.projects[i].achievements = [];
                    el.querySelectorAll('li').forEach(function(li) {{
                        var t = textWithoutControls(li);
                        if (t) result.projects[i].achievements.push(t);
                    }});
                }}
            }}
        }}

        // Skills — clear existing then rebuild from DOM to avoid stale keys
        if (result.skills) {{
            Object.keys(result.skills).forEach(function(k) {{ delete result.skills[k]; }});
            var newSkills = {{}};

            document.querySelectorAll('.skill-category').forEach(function(cat) {{
                var titleEl = cat.querySelector('.category-title');
                var listEl = cat.querySelector('.skill-list');
                if (!titleEl || !listEl) return;

                var title = titleEl.textContent.trim();
                // Stable key: prefer original data-key attribute, fall back to normalized title
                var dataKey = cat.getAttribute('data-key');
                var jsonKey = dataKey || title.toLowerCase().replace(/\\s+/g, '_');

                var skillEls = listEl.querySelectorAll('.skill-item');
                var skillsArr = [];
                skillEls.forEach(function(el) {{
                    var t = textWithoutControls(el);
                    if (t) skillsArr.push(t);
                }});
                if (skillsArr.length > 0) {{
                    newSkills[jsonKey] = skillsArr;
                }} else if (title) {{
                    // Preserve the (now empty) category so the user's edit isn't lost
                    newSkills[jsonKey] = [];
                }}
            }});
            result.skills = newSkills;
        }}

        return result;
    }}

    function copyJson() {{
        var data = extractToJson();
        var jsonStr = JSON.stringify(data, null, 2);

        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(jsonStr).then(function() {{
                showToast({json.dumps(labels["json_copied"], ensure_ascii=False)}, 2500);
            }}).catch(function() {{
                fallbackCopy(jsonStr);
            }});
        }} else {{
            fallbackCopy(jsonStr);
        }}
    }}

    function fallbackCopy(jsonStr) {{
        console.log('=== RESUME JSON ===');
        console.log(jsonStr);
        console.log('=== END RESUME JSON ===');
        showToast({json.dumps(labels["json_console"], ensure_ascii=False)}, 3500);
    }}

    btn.addEventListener('click', toggleEditMode);
    copyBtn.addEventListener('click', copyJson);
    cancelBtn.addEventListener('click', function() {{ exitEditMode(true); }});

    // Expose for programmatic extraction (e.g. Playwright) per SKILL.md
    window.extractToJson = extractToJson;
}})();
</script>
'''


def generate_resume_html(resume_data, theme="modern", language="en", editable=False, resume_json_path=None):
    """
    Generate HTML resume from JSON data with specified theme and language.
    """
    theme = theme or DEFAULT_THEME
    language = language if language in SUPPORTED_LANGUAGES else "en"

    theme_assets = resolve_theme_assets(theme, Path(__file__).parent.parent)
    template_path = theme_assets["template_path"]
    css_path = theme_assets["css_path"]

    template = load_template(template_path)
    css = load_css(css_path)

    # Build HTML content
    html_content = build_sections(resume_data, language, resume_json_path)

    # Build edit script payload if editable mode is enabled
    edit_payload = build_edit_script(resume_data, language) if editable else ""

    # Insert CSS, content, language, and edit script into template
    full_html = template.replace("{{CSS}}", css)
    full_html = full_html.replace("{{CONTENT}}", html_content)
    full_html = full_html.replace("{{LANG}}", language)
    full_html = full_html.replace("{{EDIT_SCRIPT}}", edit_payload)

    return full_html


def build_sections(resume_data, language, resume_json_path=None):
    """Build HTML sections from resume data."""
    sidebar_sections = []
    main_sections = []

    # Header (Personal Info) — always in sidebar
    sidebar_sections.append(build_header(resume_data.get("personal", {}), language, resume_json_path))

    # Summary
    if resume_data.get("summary"):
        main_sections.append(build_summary(resume_data["summary"], language))

    # Experience
    if resume_data.get("experience"):
        main_sections.append(build_experience(resume_data["experience"], language))

    # Education
    if resume_data.get("education"):
        main_sections.append(build_education(resume_data["education"], language))

    # Projects
    if resume_data.get("projects"):
        main_sections.append(build_projects(resume_data["projects"], language))

    # Skills — always in sidebar
    if resume_data.get("skills"):
        sidebar_sections.append(build_skills(resume_data["skills"], language))

    sidebar_html = '<aside class="sidebar">' + "\n".join(sidebar_sections) + '</aside>'
    main_html = '<main class="main-content">' + "\n".join(main_sections) + '</main>'

    return sidebar_html + "\n" + main_html


def build_header(personal, language, resume_json_path=None):
    """Build header section with personal info."""
    name = escape_text(personal.get("name", "Your Name"))
    email = escape_text(personal.get("email", ""))
    phone = escape_text(personal.get("phone", ""))
    location = escape_text(personal.get("location", ""))
    linkedin = escape_text(personal.get("linkedin", ""))
    github = escape_text(personal.get("github", ""))
    photo_src = resolve_photo_src(personal.get("photo", ""), resume_json_path)

    contact_items = []
    if email:
        contact_items.append(f'<span class="contact-item contact-email"><a href="mailto:{email}">{email}</a></span>')
    if phone:
        contact_items.append(f'<span class="contact-item contact-phone">{phone}</span>')
    if location:
        contact_items.append(f'<span class="contact-item contact-location">{location}</span>')
    if linkedin:
        contact_items.append(f'<span class="contact-item contact-linkedin"><a href="{linkedin}" target="_blank">LinkedIn</a></span>')
    if github:
        contact_items.append(f'<span class="contact-item contact-github"><a href="{github}" target="_blank">GitHub</a></span>')

    contact_html = "\n".join(contact_items) if contact_items else ""
    # Photo is opt-in per theme. Built-in themes hide .resume-photo via CSS;
    # a custom theme enables it by setting display: block (or similar).
    photo_html = f'<img class="resume-photo" src="{photo_src}" alt="">\n' if photo_src else ""

    return f"""
<header class="resume-header">
    {photo_html}<h1 class="name">{name}</h1>
    <div class="contact-info">{contact_html}</div>
</header>
"""


def build_summary(summary, language):
    """Build summary section."""
    labels = get_localized_text(language)
    title = labels["summary"]
    return f"""
<section class="resume-section" data-section="summary">
    <h2 class="section-title">{title}</h2>
    <p>{escape_text(summary)}</p>
</section>
"""


def build_experience(experience, language):
    """Build experience section."""
    labels = get_localized_text(language)
    title = labels["experience"]
    html = f'<section class="resume-section" data-section="experience"><h2 class="section-title">{title}</h2>'

    for exp in experience:
        company = escape_text(exp.get("company", "Company Name"))
        position = escape_text(exp.get("position", "Position"))
        period = escape_text(exp.get("period", ""))
        location = escape_text(exp.get("location", ""))
        description = escape_text(exp.get("description", ""))
        responsibilities = exp.get("responsibilities", [])
        achievements = exp.get("achievements", [])

        html += f"""
<div class="experience-item">
    <div class="experience-header">
        <h3 class="company-name">{company}</h3>
        <div class="position-period">
            <span class="position">{position}</span>
            <span class="period">{period}</span>
        </div>
    </div>
    {f'<div class="location">{location}</div>' if location else ''}
"""

        if description:
            html += f"<p class='experience-description'>{description}</p>"

        if responsibilities:
            html += "<ul class='responsibilities'>"
            for resp in responsibilities:
                html += f"<li>{escape_text(resp)}</li>"
            html += "</ul>"

        if achievements:
            html += "<ul class='achievements'>"
            for ach in achievements:
                html += f"<li>{escape_text(ach)}</li>"
            html += "</ul>"

        html += "</div>"

    html += "</section>"
    return html


def build_education(education, language):
    """Build education section."""
    labels = get_localized_text(language)
    title = labels["education"]
    html = f'<section class="resume-section" data-section="education"><h2 class="section-title">{title}</h2>'

    for edu in education:
        institution = escape_text(edu.get("institution", "Institution Name"))
        degree = escape_text(edu.get("degree", "Degree"))
        period = escape_text(edu.get("period", ""))
        location = escape_text(edu.get("location", ""))
        gpa = escape_text(edu.get("gpa", ""))
        honors = edu.get("honors", [])

        html += f"""
<div class="education-item">
    <div class="education-header">
        <h3 class="institution">{institution}</h3>
        <div class="degree-period">
            <span class="degree">{degree}</span>
            <span class="period">{period}</span>
        </div>
    </div>
    {f'<div class="location">{location}</div>' if location else ''}
    {f'<div class="gpa">{escape_text(labels["gpa"])}: {gpa}</div>' if gpa else ''}
"""

        if honors:
            html += f"<div class='honors'><strong>{escape_text(labels['honors'])}:</strong> " + ", ".join([escape_text(h) for h in honors]) + "</div>"

        html += "</div>"

    html += "</section>"
    return html


def build_projects(projects, language):
    """Build projects section."""
    labels = get_localized_text(language)
    title = labels["projects"]
    html = f'<section class="resume-section" data-section="projects"><h2 class="section-title">{title}</h2>'

    for proj in projects:
        name = escape_text(proj.get("name", "Project Name"))
        role = escape_text(proj.get("role", ""))
        period = escape_text(proj.get("period", ""))
        technologies = proj.get("technologies", [])
        description = escape_text(proj.get("description", ""))
        achievements = proj.get("achievements", [])

        html += f"""
<div class="project-item">
    <div class="project-header">
        <h3 class="project-name">{name}</h3>
        {f'<span class="role">{role}</span>' if role else ''}
        {f'<span class="period">{period}</span>' if period else ''}
    </div>
"""

        if technologies:
            escaped_techs = [escape_text(t) for t in technologies]
            html += f"<div class='technologies'><strong>{escape_text(labels['technologies'])}:</strong> {', '.join(escaped_techs)}</div>"

        if description:
            html += f"<p class='project-description'>{description}</p>"

        if achievements:
            html += "<ul class='achievements'>"
            for ach in achievements:
                html += f"<li>{escape_text(ach)}</li>"
            html += "</ul>"

        html += "</div>"

    html += "</section>"
    return html


def build_skills(skills, language):
    """Build skills section."""
    labels = get_localized_text(language)
    title = labels["skills"]
    html = f'<section class="resume-section" data-section="skills"><h2 class="section-title">{title}</h2>'

    for category, skill_list in skills.items():
        category_escaped = escape_text(category)
        category_key = escape_text(category)
        display_title = category_escaped.replace('_', ' ').title()
        items = ensure_string_list(skill_list)
        item_spans = "".join(
            f'<span class="skill-item">{escape_text(s)}</span>' for s in items
        )
        html += f"""
<div class="skill-category" data-key="{category_key}">
    <h3 class="category-title">{display_title}</h3>
    <div class="skill-list">{item_spans}</div>
</div>
"""

    html += "</section>"
    return html


def main():
    parser = argparse.ArgumentParser(description='Generate HTML resume from JSON data')
    parser.add_argument('resume_json', help='Path to resume JSON file')
    parser.add_argument('output_html', help='Path to output HTML file')
    parser.add_argument(
        '--theme',
        default=DEFAULT_THEME,
        help='Resume theme name, a user-themes/<name> custom theme, or a path to a custom theme directory',
    )
    parser.add_argument('--lang', default='en', choices=SUPPORTED_LANGUAGES,
                        help='Language (default: en)')
    parser.add_argument('--editable', action='store_true',
                        help='Add inline editing capabilities to the HTML output')

    args = parser.parse_args()

    # Load resume data with error handling
    try:
        with open(args.resume_json, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Resume file not found: {args.resume_json}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.resume_json}")
        print(f"Details: {e}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Failed to read file. Please ensure it's UTF-8 encoded: {args.resume_json}")
        sys.exit(1)

    resume_data = normalize_resume_data(resume_data)

    # Validate resume data
    validation_errors = validate_resume_data(resume_data)
    if validation_errors:
        print("Error: Resume data validation failed:")
        for error in validation_errors:
            print(f"  - {error}")
        sys.exit(1)

    # Generate HTML
    print(f"Generating HTML resume with theme '{args.theme}' in {args.lang}...")
    try:
        html = generate_resume_html(
            resume_data,
            theme=args.theme,
            language=args.lang,
            editable=args.editable,
            resume_json_path=args.resume_json,
        )
    except ValueError as e:
        print("Error: Invalid theme configuration")
        print(f"Details: {e}")
        print(f"Available themes: {', '.join(list_available_themes(Path(__file__).parent.parent))}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to generate HTML")
        print(f"Details: {e}")
        sys.exit(1)

    # Save to file with error handling
    try:
        with open(args.output_html, 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        print(f"Error: Failed to write output file: {args.output_html}")
        print(f"Details: {e}")
        sys.exit(1)

    print(f"Resume generated: {args.output_html}")
    print(f"Open in browser to view: file://{Path(args.output_html).absolute()}")


if __name__ == "__main__":
    main()
