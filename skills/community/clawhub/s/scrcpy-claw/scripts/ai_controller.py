#!/usr/bin/env python3
"""
AI-Assisted Android Controller
Provides intelligent device control with screen analysis and decision-making.
"""

import os
import json
import time
import base64
import re
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import subprocess


# ==================== Screen Analysis ====================

class UIElementType(Enum):
    """UI element types."""
    BUTTON = "button"
    TEXT_FIELD = "text_field"
    TEXT = "text"
    IMAGE = "image"
    ICON = "icon"
    CHECKBOX = "checkbox"
    SWITCH = "switch"
    LIST_ITEM = "list_item"
    UNKNOWN = "unknown"


@dataclass
class UIElement:
    """UI element representation."""
    element_type: UIElementType
    x: int
    y: int
    width: int
    height: int
    text: str = ""
    content_description: str = ""
    resource_id: str = ""
    clickable: bool = False
    scrollable: bool = False
    enabled: bool = True
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get center coordinates."""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'type': self.element_type.value,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'text': self.text,
            'content_description': self.content_description,
            'resource_id': self.resource_id,
            'clickable': self.clickable,
            'scrollable': self.scrollable,
            'enabled': self.enabled
        }


class ScreenAnalyzer:
    """
    Analyze Android screen content using uiautomator dump.
    """
    
    def __init__(self, adb_path: str = "adb", device_id: Optional[str] = None):
        self.adb_path = adb_path
        self.device_id = device_id
        self.last_elements: List[UIElement] = []
        self.screen_width = 1080
        self.screen_height = 1920
    
    def _run_adb(self, args: List[str]) -> Tuple[int, str, str]:
        """Run ADB command."""
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(args)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    
    def dump_ui(self) -> List[UIElement]:
        """
        Dump current UI hierarchy.
        
        Returns:
            List of UI elements.
        """
        # Dump UI to device
        self._run_adb(["shell", "uiautomator", "dump", "/sdcard/ui_dump.xml"])
        # Pull to local
        local_path = os.path.join(os.getcwd(), "ui_dump.xml")
        self._run_adb(["pull", "/sdcard/ui_dump.xml", local_path])
        # Clean up
        self._run_adb(["shell", "rm", "/sdcard/ui_dump.xml"])
        
        # Parse XML
        elements = self._parse_ui_dump(local_path)
        self.last_elements = elements
        
        # Clean up local file
        if os.path.exists(local_path):
            os.remove(local_path)
        
        return elements
    
    def _parse_ui_dump(self, filepath: str) -> List[UIElement]:
        """Parse UI dump XML file."""
        import xml.etree.ElementTree as ET
        
        elements = []
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            for node in root.iter():
                bounds_str = node.get('bounds', '[0,0][0,0]')
                bounds = self._parse_bounds(bounds_str)
                
                if bounds[2] - bounds[0] < 5 or bounds[3] - bounds[1] < 5:
                    continue  # Skip very small elements
                
                element = UIElement(
                    element_type=self._determine_element_type(node),
                    x=bounds[0],
                    y=bounds[1],
                    width=bounds[2] - bounds[0],
                    height=bounds[3] - bounds[1],
                    text=node.get('text', ''),
                    content_description=node.get('content-desc', ''),
                    resource_id=node.get('resource-id', ''),
                    clickable=node.get('clickable', 'false') == 'true',
                    scrollable=node.get('scrollable', 'false') == 'true',
                    enabled=node.get('enabled', 'true') == 'true'
                )
                elements.append(element)
        except Exception as e:
            print(f"Error parsing UI dump: {e}")
        
        return elements
    
    def _parse_bounds(self, bounds_str: str) -> Tuple[int, int, int, int]:
        """Parse bounds string '[x1,y1][x2,y2]'."""
        match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
        if match:
            return tuple(int(x) for x in match.groups())
        return (0, 0, 0, 0)
    
    def _determine_element_type(self, node) -> UIElementType:
        """Determine UI element type from node attributes."""
        class_name = node.get('class', '').lower()
        clickable = node.get('clickable', 'false') == 'true'
        
        if 'button' in class_name:
            return UIElementType.BUTTON
        elif 'edittext' in class_name or 'edit' in class_name:
            return UIElementType.TEXT_FIELD
        elif 'checkbox' in class_name:
            return UIElementType.CHECKBOX
        elif 'switch' in class_name:
            return UIElementType.SWITCH
        elif 'imageview' in class_name or 'image' in class_name:
            return UIElementType.IMAGE
        elif 'imagebutton' in class_name:
            return UIElementType.BUTTON
        elif 'textview' in class_name:
            if clickable:
                return UIElementType.BUTTON
            return UIElementType.TEXT
        elif 'recyclerview' in class_name or 'listview' in class_name:
            return UIElementType.LIST_ITEM
        
        return UIElementType.UNKNOWN
    
    def find_element_by_text(self, text: str, exact: bool = False) -> List[UIElement]:
        """
        Find elements containing text.
        
        Args:
            text: Text to search for.
            exact: Whether to match exactly.
            
        Returns:
            List of matching elements.
        """
        elements = []
        for elem in self.last_elements:
            if exact:
                if elem.text == text or elem.content_description == text:
                    elements.append(elem)
            else:
                if text.lower() in elem.text.lower() or text.lower() in elem.content_description.lower():
                    elements.append(elem)
        return elements
    
    def find_element_by_id(self, resource_id: str) -> List[UIElement]:
        """Find elements by resource ID."""
        return [e for e in self.last_elements if resource_id in e.resource_id]
    
    def find_clickable_elements(self) -> List[UIElement]:
        """Find all clickable elements."""
        return [e for e in self.last_elements if e.clickable and e.enabled]
    
    def find_text_fields(self) -> List[UIElement]:
        """Find all text input fields."""
        return [e for e in self.last_elements 
                if e.element_type == UIElementType.TEXT_FIELD and e.enabled]


# ==================== AI Decision Engine ====================

@dataclass
class ActionResult:
    """Result of an action execution."""
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


class AIDecisionEngine:
    """
    AI-powered decision engine for device control.
    Analyzes screen state and determines appropriate actions.
    """
    
    def __init__(self, controller, analyzer: ScreenAnalyzer):
        """
        Initialize decision engine.
        
        Args:
            controller: Device controller (ADB or Scrcpy).
            analyzer: Screen analyzer.
        """
        self.controller = controller
        self.analyzer = analyzer
        self.action_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
    
    def analyze_and_suggest(self, goal: str) -> List[Dict[str, Any]]:
        """
        Analyze current screen and suggest actions to achieve goal.
        
        Args:
            goal: Description of what to achieve.
            
        Returns:
            List of suggested actions.
        """
        elements = self.analyzer.dump_ui()
        suggestions = []
        
        # Analyze goal and find relevant elements
        goal_lower = goal.lower()
        
        # Check for common patterns
        if 'open' in goal_lower or 'launch' in goal_lower:
            # Find app launcher or specific app
            suggestions.extend(self._suggest_open_action(goal_lower, elements))
        
        if 'click' in goal_lower or 'tap' in goal_lower or 'select' in goal_lower:
            suggestions.extend(self._suggest_click_action(goal_lower, elements))
        
        if 'type' in goal_lower or 'enter' in goal_lower or 'input' in goal_lower:
            suggestions.extend(self._suggest_type_action(goal_lower, elements))
        
        if 'scroll' in goal_lower:
            suggestions.extend(self._suggest_scroll_action(goal_lower))
        
        if 'search' in goal_lower:
            suggestions.extend(self._suggest_search_action(goal_lower, elements))
        
        return suggestions
    
    def _suggest_open_action(self, goal: str, elements: List[UIElement]) -> List[Dict]:
        """Suggest open/launch actions."""
        suggestions = []
        
        # Extract app name from goal
        for word in goal.split():
            if word not in ['open', 'launch', 'start', 'the', 'app', 'application']:
                # Search for elements with this text
                matching = self.analyzer.find_element_by_text(word)
                for elem in matching:
                    if elem.clickable:
                        suggestions.append({
                            'action': 'tap',
                            'target': elem.center,
                            'description': f"Tap on '{elem.text or elem.content_description}'",
                            'element': elem.to_dict()
                        })
        
        return suggestions
    
    def _suggest_click_action(self, goal: str, elements: List[UIElement]) -> List[Dict]:
        """Suggest click/tap actions."""
        suggestions = []
        
        # Extract target text
        words = goal.replace('click', '').replace('tap', '').replace('select', '').strip()
        
        matching = self.analyzer.find_element_by_text(words)
        for elem in matching[:5]:  # Top 5 matches
            if elem.clickable:
                suggestions.append({
                    'action': 'tap',
                    'target': elem.center,
                    'description': f"Tap on '{elem.text or elem.content_description}'",
                    'element': elem.to_dict()
                })
        
        return suggestions
    
    def _suggest_type_action(self, goal: str, elements: List[Dict]) -> List[Dict]:
        """Suggest type/input actions."""
        suggestions = []
        
        # Find text to input
        import re
        match = re.search(r'type\s+["\'](.+?)["\']', goal)
        if not match:
            match = re.search(r'enter\s+["\'](.+?)["\']', goal)
        if not match:
            match = re.search(r'input\s+["\'](.+?)["\']', goal)
        
        if match:
            text_to_type = match.group(1)
            text_fields = self.analyzer.find_text_fields()
            
            if text_fields:
                suggestions.append({
                    'action': 'tap',
                    'target': text_fields[0].center,
                    'description': f"Tap on text field to focus",
                    'element': text_fields[0].to_dict()
                })
                suggestions.append({
                    'action': 'input_text',
                    'text': text_to_type,
                    'description': f"Input text: {text_to_type}"
                })
        
        return suggestions
    
    def _suggest_scroll_action(self, goal: str) -> List[Dict]:
        """Suggest scroll actions."""
        suggestions = []
        
        if 'up' in goal:
            suggestions.append({
                'action': 'swipe',
                'direction': 'up',
                'description': "Scroll up"
            })
        elif 'down' in goal:
            suggestions.append({
                'action': 'swipe',
                'direction': 'down',
                'description': "Scroll down"
            })
        
        return suggestions
    
    def _suggest_search_action(self, goal: str, elements: List[UIElement]) -> List[Dict]:
        """Suggest search actions."""
        suggestions = []
        
        # Find search field
        search_fields = self.analyzer.find_element_by_text('search', exact=False)
        search_fields.extend(self.analyzer.find_element_by_id('search'))
        
        for elem in search_fields[:1]:  # First search field
            if elem.clickable or elem.element_type == UIElementType.TEXT_FIELD:
                suggestions.append({
                    'action': 'tap',
                    'target': elem.center,
                    'description': f"Tap on search field",
                    'element': elem.to_dict()
                })
        
        return suggestions
    
    def execute_suggestion(self, suggestion: Dict[str, Any]) -> ActionResult:
        """
        Execute a suggested action.
        
        Args:
            suggestion: Action suggestion dict.
            
        Returns:
            ActionResult with execution status.
        """
        action = suggestion.get('action')
        
        try:
            if action == 'tap':
                x, y = suggestion['target']
                success = self.controller.tap(x, y)
                return ActionResult(
                    success=success,
                    message=f"Tapped at ({x}, {y})",
                    data={'coordinates': (x, y)}
                )
            
            elif action == 'swipe':
                direction = suggestion.get('direction', 'up')
                success = self.controller.swipe_direction(direction)
                return ActionResult(
                    success=success,
                    message=f"Scrolled {direction}",
                    data={'direction': direction}
                )
            
            elif action == 'input_text':
                text = suggestion['text']
                success = self.controller.input_text(text)
                return ActionResult(
                    success=success,
                    message=f"Input text: {text}",
                    data={'text': text}
                )
            
            elif action == 'press_key':
                keycode = suggestion['keycode']
                success = self.controller.press_key(keycode)
                return ActionResult(
                    success=success,
                    message=f"Pressed key: {keycode}",
                    data={'keycode': keycode}
                )
            
            else:
                return ActionResult(
                    success=False,
                    message=f"Unknown action: {action}"
                )
        
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Error executing action: {str(e)}"
            )
    
    def run_automation(self, goal: str, max_steps: int = 10) -> List[ActionResult]:
        """
        Run automated sequence to achieve a goal.
        
        Args:
            goal: Goal description.
            max_steps: Maximum number of steps.
            
        Returns:
            List of action results.
        """
        results = []
        
        for step in range(max_steps):
            suggestions = self.analyze_and_suggest(goal)
            
            if not suggestions:
                results.append(ActionResult(
                    success=False,
                    message="No more suggestions available"
                ))
                break
            
            # Execute first suggestion
            result = self.execute_suggestion(suggestions[0])
            results.append(result)
            self.action_history.append({
                'step': step,
                'suggestion': suggestions[0],
                'result': result
            })
            
            if not result.success:
                break
            
            # Wait for screen to update
            time.sleep(1)
        
        return results


# ==================== Workflow Automation ====================

class Workflow:
    """
    Predefined workflow for common tasks.
    """
    
    def __init__(self, controller, analyzer: ScreenAnalyzer):
        self.controller = controller
        self.analyzer = analyzer
    
    def open_app_by_name(self, app_name: str) -> bool:
        """
        Open app by name.
        
        Args:
            app_name: App name or partial name.
            
        Returns:
            True if successful.
        """
        # Open app drawer
        self.controller.press_home()
        time.sleep(0.5)
        
        # Swipe up to open app drawer (on most launchers)
        self.controller.swipe_direction('up')
        time.sleep(0.5)
        
        # Search for app
        elements = self.analyzer.dump_ui()
        matching = self.analyzer.find_element_by_text(app_name)
        
        for elem in matching:
            if elem.clickable:
                x, y = elem.center
                self.controller.tap(x, y)
                return True
        
        return False
    
    def search_and_action(self, search_query: str, action: str = 'search') -> bool:
        """
        Perform search with query.
        
        Args:
            search_query: Search query.
            action: Action type ('search', 'open', etc.).
            
        Returns:
            True if successful.
        """
        # Find and tap search field
        elements = self.analyzer.dump_ui()
        search_fields = self.analyzer.find_element_by_text('search', exact=False)
        
        if not search_fields:
            # Try using Google Assistant
            self.controller.press_home()
            time.sleep(0.3)
            self.controller.press_key(187)  # APP_SWITCH - doesn't trigger assistant
            # Alternative: long press home
            return False
        
        search_elem = search_fields[0]
        self.controller.tap(*search_elem.center)
        time.sleep(0.3)
        
        # Type search query
        self.controller.input_text(search_query)
        time.sleep(0.2)
        
        # Press enter/search
        self.controller.press_enter()
        
        return True
    
    def fill_form(self, fields: Dict[str, str]) -> bool:
        """
        Fill form with field values.
        
        Args:
            fields: Dict mapping field labels to values.
            
        Returns:
            True if all fields filled successfully.
        """
        elements = self.analyzer.dump_ui()
        text_fields = self.analyzer.find_text_fields()
        
        success = True
        for label, value in fields.items():
            # Find field near this label
            label_elems = self.analyzer.find_element_by_text(label)
            
            if label_elems:
                # Find nearest text field
                label_elem = label_elems[0]
                nearest_field = None
                min_distance = float('inf')
                
                for field in text_fields:
                    distance = abs(field.y - label_elem.y) + abs(field.x - label_elem.x)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_field = field
                
                if nearest_field:
                    self.controller.tap(*nearest_field.center)
                    time.sleep(0.2)
                    self.controller.input_text(value)
                    time.sleep(0.1)
                    continue
            
            success = False
        
        return success
    
    def scroll_to_find(self, text: str, max_swipes: int = 10, direction: str = 'down') -> Optional[UIElement]:
        """
        Scroll until finding element with text.
        
        Args:
            text: Text to find.
            max_swipes: Maximum number of swipes.
            direction: Scroll direction.
            
        Returns:
            Found element or None.
        """
        for _ in range(max_swipes):
            elements = self.analyzer.dump_ui()
            matching = self.analyzer.find_element_by_text(text)
            
            if matching:
                return matching[0]
            
            self.controller.swipe_direction(direction)
            time.sleep(0.5)
        
        return None


# ==================== CLI Interface ====================

def main():
    """CLI interface for testing."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='AI-Assisted Android Controller')
    parser.add_argument('--device', '-d', help='Device serial number')
    parser.add_argument('--goal', '-g', help='Goal to achieve')
    parser.add_argument('--dump-ui', action='store_true', help='Dump current UI')
    parser.add_argument('--find', '-f', help='Find element by text')
    
    args = parser.parse_args()
    
    # Import controller
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from adb_controller import ADBController
    
    controller = ADBController(device_id=args.device)
    analyzer = ScreenAnalyzer(device_id=args.device)
    engine = AIDecisionEngine(controller, analyzer)
    
    if args.dump_ui:
        elements = analyzer.dump_ui()
        print(f"Found {len(elements)} UI elements:")
        for elem in elements[:20]:
            print(f"  - {elem.element_type.value}: '{elem.text}' at ({elem.x}, {elem.y})")
    
    if args.find:
        elements = analyzer.dump_ui()
        matching = analyzer.find_element_by_text(args.find)
        print(f"Found {len(matching)} matching elements:")
        for elem in matching:
            print(f"  - {elem.to_dict()}")
    
    if args.goal:
        print(f"Working on goal: {args.goal}")
        results = engine.run_automation(args.goal)
        for i, result in enumerate(results):
            print(f"Step {i+1}: {result.message} ({'success' if result.success else 'failed'})")


if __name__ == '__main__':
    main()
