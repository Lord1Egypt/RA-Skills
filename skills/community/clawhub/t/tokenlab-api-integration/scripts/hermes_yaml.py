"""Insert one Hermes provider using YAML source marks; never serialize existing settings."""

import copy
import json

from setup_files import SetupError


def insert_provider(content: bytes | None, container: str, name: str, provider: dict) -> bytes:
    # Use the parser already installed by the pinned official Hermes distribution.
    # Import lazily so restoration continues to work after Hermes is uninstalled.
    try:
        import yaml
    except ImportError:
        raise SetupError("PyYAML is unavailable. Run with your installed Hermes Python or use --hermes-python; no packages were installed.") from None
    if yaml.__version__ != "6.0.3":
        raise SetupError("Use the PyYAML 6.0.3 environment supplied by Hermes 0.21.3; no packages were installed.")

    class UniqueLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            keys = set()
            for key, _ in node.value:
                # Merge keys can hide a collision and change an alias consumer.
                if key.tag != "tag:yaml.org,2002:str" or key.value in keys:
                    raise ValueError("Ambiguous YAML mapping")
                keys.add(key.value)
            return super().construct_mapping(node, deep=deep)

    try:
        text = (content or b"").decode("utf-8")
        document = yaml.load(text, Loader=UniqueLoader)
        root = yaml.compose(text, Loader=UniqueLoader)
        if root is None:
            document = {}
        if not isinstance(document, dict):
            raise ValueError("Expected a mapping")
        selected = document.get("model", {})
        if isinstance(selected, dict) and selected.get("provider") in {name, f"custom:{name}"}:
            raise SetupError("The existing default already refers to that Hermes provider; choose another name.")
        existing = document.get(container, {})
        if not isinstance(existing, dict):
            raise ValueError("Expected providers mapping")
        if name in existing:
            raise SetupError("That Hermes provider already exists outside this helper. Choose another provider name.")
        target = root
        addition = {container: {name: provider}}
        if container in document:
            target = next(value for key, value in root.value if key.value == container)
            addition = {name: provider}
        newline = "\r\n" if "\r\n" in text else "\n"
        if target is not None and target.flow_style:
            # Flow mappings use JSON-compatible member syntax. Keep all old bytes.
            offset = target.end_mark.index - 1
            if text[offset] != "}":
                raise ValueError("Unexpected flow mapping")
            fragment = (", " if target.value else "") + json.dumps(addition, ensure_ascii=False)[1:-1]
        else:
            offset = target.end_mark.index if target is not None else len(text)
            indent = target.start_mark.column if target is not None else 0
            # Existing mapping ends at the next sibling token; insert before its
            # indentation, including when it is the root document-end marker.
            line_start = text.rfind("\n", 0, offset) + 1
            if not text[line_start:offset].strip():
                offset = line_start
            prefix = " " * indent
            if container in document:
                lines = [prefix + json.dumps(name) + ":"]
                lines += [prefix + "  " + json.dumps(key) + ": " + json.dumps(value)
                          for key, value in provider.items()]
            else:
                lines = [prefix + container + ":", prefix + "  " + json.dumps(name) + ":"]
                lines += [prefix + "    " + json.dumps(key) + ": " + json.dumps(value)
                          for key, value in provider.items()]
            fragment = (newline if offset and text[offset - 1] not in "\r\n\ufeff" else "") + newline.join(lines) + newline
        result = text[:offset] + fragment + text[offset:]
        loaded = yaml.load(result, Loader=UniqueLoader)
        expected = copy.deepcopy(document)
        # Replace just this mapping in the expected value. Shared YAML aliases
        # elsewhere must not gain a provider as a side effect of insertion.
        expected[container] = {**copy.deepcopy(existing), name: provider}
        if loaded != expected:
            raise ValueError("Insertion changed other settings")
        return result.encode("utf-8")
    except SetupError:
        raise
    except (yaml.YAMLError, ValueError, TypeError, UnicodeDecodeError, RecursionError, AttributeError, StopIteration):
        raise SetupError("Hermes configuration is not an unambiguous supported YAML mapping; use the manual guide. Existing values were not printed or changed.") from None
