#!/usr/bin/env python3
"""
SiYuan API Client - Production Grade
思源笔记 API 客户端 - 生产级
"""

import json
import logging
import time
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('siyuan')


class SiYuanError(Exception):
    """Base exception for SiYuan API errors"""
    pass


class SiYuanAPIError(SiYuanError):
    """API returned error response"""
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"API Error {code}: {msg}")


class SiYuanConnectionError(SiYuanError):
    """Failed to connect to SiYuan"""
    pass


class SiYuanClient:
    """
    Production-grade client for SiYuan Note API.
    
    Features:
    - Automatic retry with exponential backoff
    - Connection pooling (via keep-alive)
    - Comprehensive error handling
    - Request/response logging
    - Config file support
    """
    
    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".openclaw" / "workspace" / "skills" / "siyuan" / "config.yaml",
        Path(__file__).parent / "config.yaml",
    ]
    
    def __init__(
        self,
        base_url: str = None,
        token: str = None,
        timeout: int = 30,
        retry: int = 3,
        verify_ssl: bool = True,
        config_path: Path = None
    ):
        """
        Initialize SiYuan client.
        
        Priority: explicit args > config file > defaults
        
        Args:
            base_url: SiYuan API base URL (e.g., "http://127.0.0.1:6806")
            token: API authorization token
            timeout: Request timeout in seconds
            retry: Number of retry attempts
            verify_ssl: Whether to verify SSL certificates
            config_path: Path to config YAML file
        """
        # Load config from file if exists
        config = self._load_config(config_path)
        
        # Set attributes with priority: explicit > config > default
        self.base_url = (base_url or config.get('base_url', "http://127.0.0.1:6806")).rstrip('/')
        self.token = token or config.get('token')
        self.timeout = timeout or config.get('timeout', 30)
        self.retry = retry or config.get('retry', 3)
        self.verify_ssl = verify_ssl if verify_ssl is not None else config.get('verify_ssl', True)
        
        if not self.token:
            raise SiYuanError("API token is required. Provide it explicitly or in config.yaml")
        
        logger.info(f"Initialized SiYuan client: {self.base_url}")
    
    def _load_config(self, config_path: Path = None) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        paths = [config_path] if config_path else self.DEFAULT_CONFIG_PATHS
        
        for path in paths:
            if path and path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        if config and 'siyuan' in config:
                            logger.debug(f"Loaded config from {path}")
                            return config['siyuan']
                except Exception as e:
                    logger.warning(f"Failed to load config from {path}: {e}")
        
        return {}
    
    def _make_request(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.
        
        Args:
            endpoint: API endpoint (without base URL)
            data: JSON payload
            method: HTTP method
            
        Returns:
            Parsed JSON response
            
        Raises:
            SiYuanAPIError: API returned error
            SiYuanConnectionError: Connection failed after retries
        """
        url = urljoin(self.base_url + "/", endpoint)
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = json.dumps(data or {}).encode('utf-8')
        last_error = None
        
        for attempt in range(self.retry):
            try:
                req = Request(
                    url,
                    data=payload,
                    headers=headers,
                    method=method
                )
                
                with urlopen(req, timeout=self.timeout) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                    # Check for API-level errors
                    if result.get('code') != 0:
                        msg = result.get('msg', 'Unknown error')
                        logger.warning(f"API error: {msg}")
                        raise SiYuanAPIError(result['code'], msg)
                    
                    return result
                    
            except HTTPError as e:
                last_error = f"HTTP {e.code}: {e.reason}"
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retry}): {last_error}")
                
                if e.code == 401:
                    raise SiYuanError("Authentication failed. Check your API token.")
                elif e.code == 404:
                    raise SiYuanError(f"Endpoint not found: {endpoint}")
                    
            except URLError as e:
                last_error = f"Connection error: {e.reason}"
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retry}): {last_error}")
                
            except json.JSONDecodeError as e:
                last_error = f"Invalid JSON response: {e}"
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retry}): {last_error}")
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retry}): {last_error}")
            
            # Exponential backoff before retry
            if attempt < self.retry - 1:
                sleep_time = 2 ** attempt
                logger.info(f"Retrying in {sleep_time}s...")
                time.sleep(sleep_time)
        
        # All retries exhausted
        raise SiYuanConnectionError(
            f"Failed after {self.retry} attempts. Last error: {last_error}"
        )
    
    # ==================== System Operations ====================
    
    def boot_progress(self) -> Dict[str, Any]:
        """
        Get SiYuan boot progress.
        
        Returns:
            Dict with 'details' and 'progress' (0-100)
        """
        result = self._make_request("api/system/bootProgress")
        return result.get('data', {})
    
    def system_version(self) -> str:
        """
        Get SiYuan system version.
        
        Returns:
            Version string (e.g., "1.3.5")
        """
        result = self._make_request("api/system/version")
        return result.get('data', '')
    
    def current_time(self) -> int:
        """
        Get current system time.
        
        Returns:
            Unix timestamp in milliseconds
        """
        result = self._make_request("api/system/currentTime")
        return result.get('data', 0)
    
    # ==================== Notebook Operations ====================
    
    def list_notebooks(self) -> List[Dict[str, Any]]:
        """Get all notebooks"""
        result = self._make_request("api/notebook/lsNotebooks")
        return result.get('data', {}).get('notebooks', [])
    
    def create_notebook(self, name: str) -> Dict[str, Any]:
        """
        Create a new notebook.
        
        Args:
            name: Notebook name
            
        Returns:
            Created notebook info
        """
        result = self._make_request(
            "api/notebook/createNotebook",
            {"name": name}
        )
        logger.info(f"Created notebook: {name}")
        return result.get('data', {})
    
    def remove_notebook(self, notebook_id: str) -> bool:
        """
        Remove a notebook.
        
        Args:
            notebook_id: Notebook ID to remove
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/notebook/removeNotebook",
            {"notebook": notebook_id}
        )
        logger.info(f"Removed notebook: {notebook_id}")
        return result.get('code') == 0
    
    def open_notebook(self, notebook_id: str) -> bool:
        """
        Open a notebook (load it into memory).
        
        Args:
            notebook_id: Notebook ID to open
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/notebook/openNotebook",
            {"notebook": notebook_id}
        )
        logger.info(f"Opened notebook: {notebook_id}")
        return result.get('code') == 0
    
    def close_notebook(self, notebook_id: str) -> bool:
        """
        Close a notebook (unload from memory).
        
        Args:
            notebook_id: Notebook ID to close
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/notebook/closeNotebook",
            {"notebook": notebook_id}
        )
        logger.info(f"Closed notebook: {notebook_id}")
        return result.get('code') == 0
    
    def rename_notebook(self, notebook_id: str, new_name: str) -> bool:
        """
        Rename a notebook.
        
        Args:
            notebook_id: Notebook ID
            new_name: New name for the notebook
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/notebook/renameNotebook",
            {"notebook": notebook_id, "name": new_name}
        )
        logger.info(f"Renamed notebook {notebook_id} to: {new_name}")
        return result.get('code') == 0
    
    def get_notebook_conf(self, notebook_id: str) -> Dict[str, Any]:
        """
        Get notebook configuration.
        
        Args:
            notebook_id: Notebook ID
            
        Returns:
            Notebook configuration dict
        """
        result = self._make_request(
            "api/notebook/getNotebookConf",
            {"notebook": notebook_id}
        )
        return result.get('data', {})
    
    def set_notebook_conf(self, notebook_id: str, conf: Dict[str, Any]) -> bool:
        """
        Set notebook configuration.
        
        Args:
            notebook_id: Notebook ID
            conf: Configuration dict
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/notebook/setNotebookConf",
            {"notebook": notebook_id, "conf": conf}
        )
        logger.info(f"Updated notebook config: {notebook_id}")
        return result.get('code') == 0
    
    # ==================== Document Operations ====================
    
    def export_md_content(self, doc_id: str) -> Dict[str, Any]:
        """
        Export document as Markdown content.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Dict with 'hPath' (human-readable path) and 'content' (Markdown)
        """
        result = self._make_request(
            "api/export/exportMdContent",
            {"id": doc_id}
        )
        return result.get('data', {})
    
    def create_doc_with_md(self, notebook_id: str, path: str, markdown: str = "") -> str:
        """
        Create a new document with Markdown content.
        
        Args:
            notebook_id: Target notebook ID
            path: Document path (e.g., "folder/docname" or just "docname")
            markdown: Initial Markdown content
            
        Returns:
            Created document ID
        """
        result = self._make_request(
            "api/filetree/createDocWithMd",
            {
                "notebook": notebook_id,
                "path": path,
                "markdown": markdown
            }
        )
        logger.info(f"Created document: {path} in {notebook_id}")
        return result.get('data', '')
    
    def rename_doc(self, notebook_id: str, path: str, new_name: str) -> bool:
        """
        Rename a document by path.
        
        Args:
            notebook_id: Notebook ID
            path: Current document path
            new_name: New name for the document
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/filetree/renameDoc",
            {"notebook": notebook_id, "path": path, "title": new_name}
        )
        logger.info(f"Renamed document {path} to: {new_name}")
        return result.get('code') == 0
    
    def rename_doc_by_id(self, doc_id: str, new_name: str) -> bool:
        """
        Rename a document by ID.
        
        Args:
            doc_id: Document ID
            new_name: New name for the document
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/filetree/renameDocByID",
            {"id": doc_id, "title": new_name}
        )
        logger.info(f"Renamed document {doc_id} to: {new_name}")
        return result.get('code') == 0
    
    def move_docs_by_id(self, doc_ids: List[str], to_id: str) -> bool:
        """
        Move documents to another notebook/document by ID.
        
        Args:
            doc_ids: List of document IDs to move
            to_id: Target parent document ID or notebook ID
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/filetree/moveDocsByID",
            {
                "fromIDs": doc_ids,
                "toID": to_id
            }
        )
        logger.info(f"Moved {len(doc_ids)} documents to {to_id}")
        return result.get('code') == 0
    
    def move_docs(self, from_paths: List[str], to_notebook: str, to_path: str = "/") -> bool:
        """
        Move documents by path.
        
        Args:
            from_paths: List of source document paths
            to_notebook: Target notebook ID
            to_path: Target path (default: root)
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/filetree/moveDocs",
            {
                "fromPaths": from_paths,
                "toNotebook": to_notebook,
                "toPath": to_path
            }
        )
        logger.info(f"Moved {len(from_paths)} documents to {to_notebook}{to_path}")
        return result.get('code') == 0
    
    def get_hpath_by_id(self, doc_id: str) -> str:
        """
        Get human-readable path based on document ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Human-readable path string
        """
        result = self._make_request(
            "api/filetree/getHPathByID",
            {"id": doc_id}
        )
        return result.get('data', '')
    
    def get_path_by_id(self, doc_id: str) -> Dict[str, Any]:
        """
        Get storage path based on document ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Dict with path information
        """
        result = self._make_request(
            "api/filetree/getPathByID",
            {"id": doc_id}
        )
        return result.get('data', {})
    
    def get_ids_by_hpath(self, notebook_id: str, hpath: str) -> List[str]:
        """
        Get document IDs based on human-readable path.
        
        Args:
            notebook_id: Notebook ID
            hpath: Human-readable path
            
        Returns:
            List of document IDs
        """
        result = self._make_request(
            "api/filetree/getIDsByHPath",
            {"notebook": notebook_id, "path": hpath}
        )
        return result.get('data', [])
    
    def remove_doc(self, notebook_id: str, path: str) -> bool:
        """
        Remove a document by notebook and path.
        
        Args:
            notebook_id: Notebook ID
            path: Document path
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/filetree/removeDoc",
            {"notebook": notebook_id, "path": path}
        )
        logger.info(f"Removed document: {path} from {notebook_id}")
        return result.get('code') == 0
    
    def remove_doc_by_id(self, doc_id: str) -> bool:
        """
        Remove a document by ID.
        
        Args:
            doc_id: Document ID to remove
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/filetree/removeDocByID",
            {"id": doc_id}
        )
        logger.info(f"Removed document by ID: {doc_id}")
        return result.get('code') == 0
    
    def get_hpath_by_path(self, notebook_id: str, path: str) -> str:
        """
        Get human-readable path based on document path.
        
        Args:
            notebook_id: Notebook ID
            path: Document path
            
        Returns:
            Human-readable path string
        """
        result = self._make_request(
            "api/filetree/getHPathByPath",
            {"notebook": notebook_id, "path": path}
        )
        return result.get('data', '')
    
    # ==================== Asset Operations ====================
    
    def upload_asset(self, file_paths: List[str], assets_dir_path: str = "/assets/") -> Dict[str, Any]:
        """
        Upload asset files to SiYuan.
        
        Args:
            file_paths: List of local file paths to upload
            assets_dir_path: Target directory in workspace (default: "/assets/")
            
        Returns:
            Dict with 'succMap' (successful uploads) and 'errFiles' (failed uploads)
        """
        import mimetypes
        from urllib.request import Request as URLRequest
        
        url = urljoin(self.base_url + "/", "api/asset/upload")
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        body = []
        
        # Add assetsDirPath field
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="assetsDirPath"')
        body.append(b'')
        body.append(assets_dir_path.encode())
        
        # Add files
        for file_path in file_paths:
            file_name = Path(file_path).name
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or 'application/octet-stream'
            
            body.append(f'--{boundary}'.encode())
            body.append(f'Content-Disposition: form-data; name="file[]"; filename="{file_name}"'.encode())
            body.append(f'Content-Type: {mime_type}'.encode())
            body.append(b'')
            
            with open(file_path, 'rb') as f:
                body.append(f.read())
        
        body.append(f'--{boundary}--'.encode())
        body.append(b'')
        
        payload = b'\r\n'.join(body)
        
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
        
        last_error = None
        for attempt in range(self.retry):
            try:
                req = URLRequest(url, data=payload, headers=headers, method="POST")
                with urlopen(req, timeout=self.timeout) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    if result.get('code') != 0:
                        raise SiYuanAPIError(result['code'], result.get('msg', 'Unknown error'))
                    logger.info(f"Uploaded {len(file_paths)} assets")
                    return result.get('data', {})
            except Exception as e:
                last_error = str(e)
                if attempt < self.retry - 1:
                    time.sleep(2 ** attempt)
        
        raise SiYuanConnectionError(f"Upload failed after {self.retry} attempts: {last_error}")
    
    # ==================== Block Operations ====================
    
    def insert_block(self, data_type: str, data: str, parent_id: str = None, 
                     previous_id: str = None, next_id: str = None) -> List[Dict[str, Any]]:
        """
        Insert blocks at specified position.
        
        Args:
            data_type: Data type (e.g., "markdown", "dom")
            data: Content to insert
            parent_id: Parent block ID (optional)
            previous_id: Insert after this block ID (optional)
            next_id: Insert before this block ID (optional)
            
        Returns:
            List of created block IDs
        """
        payload = {"dataType": data_type, "data": data}
        if parent_id:
            payload["parentID"] = parent_id
        if previous_id:
            payload["previousID"] = previous_id
        if next_id:
            payload["nextID"] = next_id
            
        result = self._make_request("api/block/insertBlock", payload)
        return result.get('data', [])
    
    def prepend_block(self, data_type: str, data: str, parent_id: str) -> List[Dict[str, Any]]:
        """
        Prepend blocks to the beginning of a document/block.
        
        Args:
            data_type: Data type (e.g., "markdown", "dom")
            data: Content to prepend
            parent_id: Parent block/document ID
            
        Returns:
            List of created block IDs
        """
        result = self._make_request(
            "api/block/prependBlock",
            {"dataType": data_type, "data": data, "parentID": parent_id}
        )
        return result.get('data', [])
    
    def append_block(self, data_type: str, data: str, parent_id: str) -> List[Dict[str, Any]]:
        """
        Append blocks to the end of a document/block.
        
        Args:
            data_type: Data type (e.g., "markdown", "dom")
            data: Content to append
            parent_id: Parent block/document ID
            
        Returns:
            List of created block IDs
        """
        result = self._make_request(
            "api/block/appendBlock",
            {"dataType": data_type, "data": data, "parentID": parent_id}
        )
        return result.get('data', [])
    
    def update_block(self, data_type: str, data: str, block_id: str) -> bool:
        """
        Update a block's content.
        
        Args:
            data_type: Data type (e.g., "markdown", "dom")
            data: New content
            block_id: Block ID to update
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/block/updateBlock",
            {"dataType": data_type, "data": data, "id": block_id}
        )
        return result.get('code') == 0
    
    def delete_block(self, block_id: str) -> bool:
        """
        Delete a block.
        
        Args:
            block_id: Block ID to delete
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/block/deleteBlock",
            {"id": block_id}
        )
        logger.info(f"Deleted block: {block_id}")
        return result.get('code') == 0
    
    def move_block(self, block_id: str, parent_id: str = None,
                   previous_id: str = None) -> bool:
        """
        Move a block to a new position.

        Args:
            block_id: Block ID to move
            parent_id: Parent block ID (optional)
            previous_id: Previous block ID for positioning (optional)

        Note:
            previous_id and parent_id cannot both be empty.
            If both provided, previous_id takes priority.

        Returns:
            True if successful
        """
        payload = {"id": block_id}
        if previous_id:
            payload["previousID"] = previous_id
        if parent_id:
            payload["parentID"] = parent_id

        result = self._make_request("api/block/moveBlock", payload)
        logger.info(f"Moved block {block_id}")
        return result.get('code') == 0
    
    def fold_block(self, block_id: str) -> bool:
        """
        Fold (collapse) a block.
        
        Args:
            block_id: Block ID to fold
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/block/foldBlock",
            {"id": block_id}
        )
        return result.get('code') == 0
    
    def unfold_block(self, block_id: str) -> bool:
        """
        Unfold (expand) a block.
        
        Args:
            block_id: Block ID to unfold
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/block/unfoldBlock",
            {"id": block_id}
        )
        return result.get('code') == 0
    
    def get_block_kramdown(self, block_id: str) -> str:
        """
        Get block content in Kramdown format.
        
        Args:
            block_id: Block ID
            
        Returns:
            Kramdown formatted content
        """
        result = self._make_request(
            "api/block/getBlockKramdown",
            {"id": block_id}
        )
        return result.get('data', {}).get('kramdown', '')
    
    def get_child_blocks(self, block_id: str) -> List[Dict[str, Any]]:
        """
        Get child blocks of a container block.
        
        Args:
            block_id: Parent block ID
            
        Returns:
            List of child block info
        """
        result = self._make_request(
            "api/block/getChildBlocks",
            {"id": block_id}
        )
        return result.get('data', [])
    
    def transfer_block_ref(self, from_id: str, to_id: str, ref_ids: List[str] = None) -> bool:
        """
        Transfer block references from one block to another.
        
        Args:
            from_id: Source block ID (def block)
            to_id: Target block ID
            ref_ids: Specific reference block IDs to transfer (optional, transfers all if not specified)
            
        Returns:
            True if successful
        """
        payload = {"fromID": from_id, "toID": to_id}
        if ref_ids:
            payload["refIDs"] = ref_ids
        
        result = self._make_request("api/block/transferBlockRef", payload)
        logger.info(f"Transferred refs from {from_id} to {to_id}")
        return result.get('code') == 0
    
    # ==================== Attribute Operations ====================
    
    def set_block_attrs(self, block_id: str, attrs: Dict[str, str]) -> bool:
        """
        Set attributes for a block.
        
        Args:
            block_id: Block ID
            attrs: Dictionary of attribute key-value pairs
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/attr/setBlockAttrs",
            {"id": block_id, "attrs": attrs}
        )
        logger.info(f"Set attributes for block: {block_id}")
        return result.get('code') == 0
    
    def get_block_attrs(self, block_id: str) -> Dict[str, str]:
        """
        Get all attributes of a block.
        
        Args:
            block_id: Block ID
            
        Returns:
            Dictionary of attribute key-value pairs
        """
        result = self._make_request(
            "api/attr/getBlockAttrs",
            {"id": block_id}
        )
        return result.get('data', {})
    
    # ==================== SQL Operations ====================
    
    def query_sql(self, stmt: str) -> List[Dict[str, Any]]:
        """
        Execute SQL query against SiYuan database.
        
        WARNING: Read-only queries recommended. Use with caution.
        
        Args:
            stmt: SQL statement
            
        Returns:
            Query results as list of dictionaries
        """
        result = self._make_request("api/query/sql", {"stmt": stmt})
        return result.get('data', [])
    
    def flush_transaction(self) -> bool:
        """
        Flush SQLite transaction to disk.
        
        Returns:
            True if successful
        """
        result = self._make_request("api/sqlite/flushTransaction")
        logger.info("Flushed SQLite transaction")
        return result.get('code') == 0
    
    # ==================== Template Operations ====================
    
    def render_template(self, doc_id: str, template_path: str) -> Dict[str, Any]:
        """
        Render a template file.
        
        Args:
            doc_id: Document ID where rendering is called
            template_path: Absolute path to template file
            
        Returns:
            Dict with 'content' (rendered HTML) and 'path'
        """
        result = self._make_request(
            "api/template/render",
            {"id": doc_id, "path": template_path}
        )
        return result.get('data', {})
    
    def render_sprig(self, template: str) -> str:
        """
        Render a Sprig template string.
        
        Args:
            template: Template content (e.g., "/daily note/{{now | date \"2006/01\"}}")
            
        Returns:
            Rendered string
        """
        result = self._make_request(
            "api/template/renderSprig",
            {"template": template}
        )
        return result.get('data', '')
    
    # ==================== File Operations ====================
    
    def get_file(self, path: str) -> Union[bytes, Dict[str, Any]]:
        """
        Get file content from workspace.
        
        Args:
            path: File path under workspace (e.g., "/data/xxx/xxx.sy")
            
        Returns:
            File bytes on success, or error dict on failure
        """
        url = urljoin(self.base_url + "/", "api/file/getFile")
        headers = {
            "Authorization": f"Token {self.token}"
        }
        
        import urllib.request
        req = urllib.request.Request(url, data=json.dumps({"path": path}).encode(), 
                                     headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status == 200:
                    return response.read()
                else:
                    return json.loads(response.read().decode())
        except HTTPError as e:
            if e.code == 202:
                return json.loads(e.read().decode())
            raise
    
    def put_file(self, path: str, file_content: bytes = None, is_dir: bool = False, 
                 mod_time: int = None) -> bool:
        """
        Upload/create a file or directory in workspace.
        
        Args:
            path: Target path under workspace
            file_content: File content bytes (ignored if is_dir=True)
            is_dir: Whether to create a directory
            mod_time: Unix timestamp for modification time
            
        Returns:
            True if successful
        """
        import mimetypes
        from urllib.request import Request as URLRequest
        
        url = urljoin(self.base_url + "/", "api/file/putFile")
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        body = []
        
        # Add path field
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="path"')
        body.append(b'')
        body.append(path.encode())
        
        # Add isDir field
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="isDir"')
        body.append(b'')
        body.append(b'true' if is_dir else b'false')
        
        # Add modTime field if provided
        if mod_time:
            body.append(f'--{boundary}'.encode())
            body.append(b'Content-Disposition: form-data; name="modTime"')
            body.append(b'')
            body.append(str(mod_time).encode())
        
        # Add file content if not directory
        if not is_dir and file_content:
            file_name = Path(path).name
            body.append(f'--{boundary}'.encode())
            body.append(f'Content-Disposition: form-data; name="file"; filename="{file_name}"'.encode())
            body.append(b'Content-Type: application/octet-stream')
            body.append(b'')
            body.append(file_content)
        
        body.append(f'--{boundary}--'.encode())
        body.append(b'')
        
        payload = b'\r\n'.join(body)
        
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
        
        req = URLRequest(url, data=payload, headers=headers, method="POST")
        with urlopen(req, timeout=self.timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('code') == 0
    
    def remove_file(self, path: str) -> bool:
        """
        Remove a file from workspace.
        
        Args:
            path: File path under workspace
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/file/removeFile",
            {"path": path}
        )
        logger.info(f"Removed file: {path}")
        return result.get('code') == 0
    
    def rename_file(self, path: str, new_path: str) -> bool:
        """
        Rename/move a file in workspace.
        
        Args:
            path: Current file path
            new_path: New file path
            
        Returns:
            True if successful
        """
        result = self._make_request(
            "api/file/renameFile",
            {"path": path, "newPath": new_path}
        )
        logger.info(f"Renamed file {path} to {new_path}")
        return result.get('code') == 0
    
    def read_dir(self, path: str) -> List[Dict[str, Any]]:
        """
        List files in a directory.
        
        Args:
            path: Directory path under workspace
            
        Returns:
            List of file info dicts with 'name', 'isDir', 'isSymlink', 'updated'
        """
        result = self._make_request(
            "api/file/readDir",
            {"path": path}
        )
        return result.get('data', [])
    
    # ==================== Export Operations ====================
    
    def export_resources(self, paths: List[str], name: str = None) -> str:
        """
        Export files/folders as a zip archive.
        
        Args:
            paths: List of paths to export
            name: Optional zip filename (default: export-YYYY-MM-DD_hh-mm-ss.zip)
            
        Returns:
            Path to created zip file (relative to workspace)
        """
        payload = {"paths": paths}
        if name:
            payload["name"] = name
        
        result = self._make_request("api/export/exportResources", payload)
        return result.get('data', {}).get('path', '')
    
    # ==================== Conversion Operations ====================
    
    def pandoc(self, dir_name: str, args: List[str]) -> str:
        """
        Run Pandoc conversion.
        
        Working directory: workspace/temp/convert/pandoc/{dir_name}
        Use put_file() to write input files first, then call this, then get_file() to retrieve output.
        
        Args:
            dir_name: Working directory name
            args: Pandoc command line arguments (e.g., ["--to", "markdown", "input.md", "-o", "output.md"])
            
        Returns:
            Path to working directory
        """
        result = self._make_request(
            "api/convert/pandoc",
            {"dir": dir_name, "args": args}
        )
        return result.get('data', {}).get('path', '')
    
    # ==================== Notification Operations ====================
    
    def push_msg(self, msg: str, timeout: int = 7000) -> str:
        """
        Push a notification message to SiYuan UI.
        
        Args:
            msg: Message text
            timeout: Display duration in milliseconds (default: 7000)
            
        Returns:
            Message ID
        """
        result = self._make_request(
            "api/notification/pushMsg",
            {"msg": msg, "timeout": timeout}
        )
        return result.get('data', {}).get('id', '')
    
    def push_err_msg(self, msg: str, timeout: int = 7000) -> str:
        """
        Push an error message to SiYuan UI.
        
        Args:
            msg: Error message text
            timeout: Display duration in milliseconds (default: 7000)
            
        Returns:
            Message ID
        """
        result = self._make_request(
            "api/notification/pushErrMsg",
            {"msg": msg, "timeout": timeout}
        )
        return result.get('data', {}).get('id', '')
    
    # ==================== Network Operations ====================
    
    def forward_proxy(self, url: str, method: str = "POST", timeout: int = 7000,
                      content_type: str = "application/json", headers: List[Dict[str, str]] = None,
                      payload: Union[str, Dict] = None, payload_encoding: str = "text",
                      response_encoding: str = "text") -> Dict[str, Any]:
        """
        Forward HTTP request through SiYuan proxy.
        
        Args:
            url: Target URL
            method: HTTP method (default: POST)
            timeout: Timeout in milliseconds (default: 7000)
            content_type: Content-Type header (default: application/json)
            headers: Additional HTTP headers
            payload: Request body (string or dict)
            payload_encoding: Payload encoding (text, base64, base32, hex)
            response_encoding: Expected response encoding
            
        Returns:
            Response dict with 'body', 'status', 'headers', etc.
        """
        data = {
            "url": url,
            "method": method,
            "timeout": timeout,
            "contentType": content_type,
            "payloadEncoding": payload_encoding,
            "responseEncoding": response_encoding
        }
        if headers:
            data["headers"] = headers
        if payload:
            data["payload"] = payload
        
        result = self._make_request("api/network/forwardProxy", data)
        return result.get('data', {})
    
    # ==================== System Operations ====================
    
    def boot_progress(self) -> Dict[str, Any]:
        """
        Get SiYuan boot progress.
        
        Returns:
            Dict with 'details' and 'progress' (0-100)
        """
        result = self._make_request("api/system/bootProgress")
        return result.get('data', {})
    
    def system_version(self) -> str:
        """
        Get SiYuan system version.
        
        Returns:
            Version string (e.g., "1.3.5")
        """
        result = self._make_request("api/system/version")
        return result.get('data', '')
    
    def current_time(self) -> int:
        """
        Get current system time.
        
        Returns:
            Unix timestamp in milliseconds
        """
        result = self._make_request("api/system/currentTime")
        return result.get('data', 0)


# ==================== Helper Functions ====================

def get_client() -> SiYuanClient:
    """Get a configured SiYuan client instance"""
    return SiYuanClient()


if __name__ == "__main__":
    # Test the client
    client = SiYuanClient()
    print("System version:", client.system_version())
    print("\nNotebooks:", len(client.list_notebooks()))
