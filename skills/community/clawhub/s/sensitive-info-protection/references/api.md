# API Documentation

## Class: SensitiveDetector

### Constructor

```python
SensitiveDetector()
```

Creates a new detector instance with default rules loaded automatically.

### Methods

#### `scan(content: str) -> ScanResult`
Scan the given content for sensitive information.

**Parameters:**
- `content`: The text content to scan

**Returns:** `ScanResult` object containing detection results

---

#### `add_rule(rule: DetectionRule) -> None`
Add a new detection rule to the detector. Automatically recompiles and re-sorts rules by priority.

**Parameters:**
- `rule`: `DetectionRule` object to add

---

#### `remove_rule(rule_name: str) -> bool`
Remove a rule by name.

**Parameters:**
- `rule_name`: Name of the rule to remove

**Returns:** `True` if rule was removed, `False` if not found

---

#### `enable_rule(rule_name: str) -> bool`
Enable a previously disabled rule.

**Parameters:**
- `rule_name`: Name of the rule to enable

**Returns:** `True` if rule was found and enabled, `False` if not found

---

#### `disable_rule(rule_name: str) -> bool`
Disable a rule by name (keeps it in the list but doesn't scan with it).

**Parameters:**
- `rule_name`: Name of the rule to disable

**Returns:** `True` if rule was found and disabled, `False` if not found

---

#### `load_config(config_path: str) -> None`
Load additional rules from a JSON configuration file.

**Parameters:**
- `config_path`: Path to JSON configuration file

**Raises:** `ValueError` if file format is not supported

---

#### `desensitize(content: str, replacement: str = "***") -> str`
Replace all detected sensitive information with replacement text.

**Parameters:**
- `content`: Original text content
- `replacement`: Text to replace sensitive content with (default: `"***"`)

**Returns:** Desensitized text string

---

#### `print_results(result: ScanResult) -> None`
Print detection results in the standard markdown format.

**Parameters:**
- `result`: `ScanResult` from `scan()`

---

## Class: DetectionRule

Represents a single detection rule.

```python
DetectionRule(
    name: str,
    pattern: str,
    sensitivity: str = "medium",
    description: str = "",
    enabled: bool = True,
    priority: int = 0
)
```

**Methods:**
- `compile() -> None`: Compile the regex pattern (called automatically)
- `match(text: str) -> List[re.Match]`: Find all matches in text

## Class: DetectionResult

Represents a single detection match.

**Attributes:**
- `rule`: The `DetectionRule` that matched
- `match`: The regex `Match` object
- `start`: Start position in text
- `end`: End position in text
- `text`: The matched text

**Methods:**
- `to_dict() -> dict`: Convert to dictionary

## Class: ScanResult

Represents the complete scan result for a text.

**Attributes:**
- `content`: The original scanned content
- `detections`: List of `DetectionResult` objects
- `has_sensitive`: `True` if any sensitive information was found

**Methods:**
- `add_detection(detection: DetectionResult) -> None`: Add a detection
- `sort_by_priority() -> None`: Sort detections by priority/sensitivity
- `to_markdown() -> str`: Format as markdown for display
