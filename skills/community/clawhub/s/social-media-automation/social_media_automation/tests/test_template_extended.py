"""
Additional unit tests for core modules
"""

import pytest
from datetime import datetime

from social_media_automation.core.template_manager import TemplateManager
from social_media_automation.storage.template_store import TemplateStore


@pytest.fixture
def template_store(tmp_path):
    """Create a temporary template store"""
    store = TemplateStore(str(tmp_path / "templates.db"))
    yield store


@pytest.fixture
def template_manager(template_store):
    """Create a TemplateManager instance"""
    return TemplateManager(template_store)


def test_template_apply_with_empty_variables(template_manager):
    """Test applying template with no variables"""
    template_manager.create_template(
        name="no_vars",
        content="Hello world!",
        platform="x",
        variables=[],
    )

    content = template_manager.use_template("no_vars", {})

    assert content == "Hello world!"


def test_template_apply_with_extra_variables(template_manager):
    """Test applying template with extra variables"""
    template_manager.create_template(
        name="greeting",
        content="Hello {{name}}!",
        platform="x",
        variables=["name"],
    )

    # Extra variables should be ignored
    content = template_manager.use_template(
        "greeting",
        {"name": "John", "extra": "ignored"},
    )

    assert content == "Hello John!"


def test_template_apply_with_duplicate_variables(template_manager):
    """Test applying template with duplicate variable values"""
    template_manager.create_template(
        name="duplicate",
        content="{{a}} {{b}}",
        platform="x",
        variables=["a", "b"],
    )

    content = template_manager.use_template("duplicate", {"a": "1", "b": "2"})

    assert content == "1 2"
