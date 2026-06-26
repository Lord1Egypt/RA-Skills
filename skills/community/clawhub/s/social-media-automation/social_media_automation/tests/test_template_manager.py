"""
Tests for TemplateManager
"""

import pytest

from social_media_automation.core.template_manager import TemplateManager
from social_media_automation.storage.template_store import TemplateStore


@pytest.fixture
def template_store(tmp_path):
    """Create a temporary template store"""
    store = TemplateStore(str(tmp_path / "templates.db"))
    yield store
    # Cleanup is handled by tmp_path fixture


@pytest.fixture
def template_manager(template_store):
    """Create a TemplateManager instance"""
    return TemplateManager(template_store)


def test_create_template(template_manager):
    """Test creating a new template"""
    template_id = template_manager.create_template(
        name="test_template",
        content="Hello {{name}}",
        platform="x",
        variables=["name"],
    )

    assert template_id is not None
    assert template_id > 0


def test_get_template(template_manager):
    """Test getting a template by ID"""
    template_id = template_manager.create_template(
        name="test_template",
        content="Hello {{name}}",
        platform="x",
        variables=["name"],
    )

    template = template_manager.get_template(template_id)

    assert template is not None
    assert template["name"] == "test_template"
    assert template["content"] == "Hello {{name}}"
    assert template["platform"] == "x"
    assert "name" in template["variables"]


def test_get_template_by_name(template_manager):
    """Test getting a template by name"""
    template_manager.create_template(
        name="test_template",
        content="Hello {{name}}",
        platform="x",
        variables=["name"],
    )

    template = template_manager.get_template_by_name("test_template")

    assert template is not None
    assert template["name"] == "test_template"


def test_list_templates(template_manager):
    """Test listing templates"""
    template_manager.create_template(
        name="template1",
        content="Content 1",
        platform="x",
        variables=[],
    )
    template_manager.create_template(
        name="template2",
        content="Content 2",
        platform="x",
        variables=[],
    )

    templates = template_manager.list_templates()

    assert len(templates) == 2
    assert any(t["name"] == "template1" for t in templates)
    assert any(t["name"] == "template2" for t in templates)


def test_update_template(template_manager):
    """Test updating a template"""
    template_id = template_manager.create_template(
        name="test_template",
        content="Hello {{name}}",
        platform="x",
        variables=["name"],
    )

    success = template_manager.update_template(
        template_id,
        name="updated_template",
    )

    assert success is True

    template = template_manager.get_template(template_id)
    assert template["name"] == "updated_template"


def test_delete_template(template_manager):
    """Test deleting a template"""
    template_id = template_manager.create_template(
        name="test_template",
        content="Hello {{name}}",
        platform="x",
        variables=["name"],
    )

    success = template_manager.delete_template(template_id)

    assert success is True

    template = template_manager.get_template(template_id)
    assert template is None


def test_use_template(template_manager):
    """Test using a template with variables"""
    template_manager.create_template(
        name="greeting",
        content="Hello {{name}}, welcome to {{company}}!",
        platform="x",
        variables=["name", "company"],
    )

    content = template_manager.use_template(
        "greeting",
        {"name": "John", "company": "Acme"},
    )

    assert content == "Hello John, welcome to Acme!"


def test_use_template_missing_variables(template_manager):
    """Test using a template with missing variables"""
    template_manager.create_template(
        name="greeting",
        content="Hello {{name}}, welcome to {{company}}!",
        platform="x",
        variables=["name", "company"],
    )

    with pytest.raises(ValueError, match="Missing required variables"):
        template_manager.use_template(
            "greeting",
            {"name": "John"},  # Missing 'company'
        )


def test_use_template_not_found(template_manager):
    """Test using a non-existent template"""
    with pytest.raises(ValueError, match="Template not found"):
        template_manager.use_template(
            "nonexistent",
            {"name": "John"},
        )
