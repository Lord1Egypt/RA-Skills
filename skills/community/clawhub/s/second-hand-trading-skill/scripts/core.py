import json
from typing import Optional
import requests
import os
from cryptography.fernet import Fernet
import base64
from memory_logger import MemoryLogger


class PlazaClientCore:
    """Core functionality for the Plaza client"""

    def __init__(self, api_base_url: str = "http://115.190.255.55:80/api/v1", config_file: str = None):
        """
        Initialize the Plaza client core.

        Args:
            api_base_url: Base URL for the AgentNego API
            config_file: Path to the encrypted configuration file for storing agent credentials. 
                        If not provided, defaults to agent_config.enc in the skill directory.
        """
        self.api_base_url = api_base_url.rstrip("/")
        
        # 确保配置文件路径是相对于技能目录的
        if config_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_file = os.path.join(current_dir, "agent_config.enc")
        else:
            self.config_file = config_file
            
        self.agent_id = None
        self.agent_token = None
        self.target_agent_ids = []
        self.relays = {}
        self._key = None
        self._fernet = None
        self.logger = MemoryLogger()  # 移到前面
        self._init_encryption()
        self._load_config()

    def _init_encryption(self):
        """Initialize encryption system automatically without user input."""
        # 确保加密密钥文件位于与配置文件相同的目录
        config_dir = os.path.dirname(self.config_file)
        key_file = os.path.join(config_dir, ".config_key")

        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                self._key = base64.urlsafe_b64decode(f.read())
        else:
            # Generate new key automatically
            self._key = Fernet.generate_key()

            # Save key file
            with open(key_file, "wb") as f:
                f.write(base64.urlsafe_b64encode(self._key))

            # Set restrictive permissions
            if os.name == 'posix':
                os.chmod(key_file, 0o600)

        self._fernet = Fernet(self._key)

    def _load_config(self):
        """Load and decrypt agent credentials from the configuration file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "rb") as f:
                    encrypted_data = f.read()

                decrypted_data = self._fernet.decrypt(encrypted_data)
                config = json.loads(decrypted_data)

                self.agent_id = config.get("agent_id")
                self.agent_token = config.get("agent_token")
                self.target_agent_ids = config.get("target_agent_ids", [])
                self.relays = config.get("relays", {})
                self.logger.log_event(self.agent_id, "load_config", 
                                     description=f"Loaded encrypted credentials from {self.config_file}",
                                     metadata={"filename": self.config_file})
            except Exception as e:
                self.logger.log_error(self.agent_id, "config_error", 
                                     error_message=f"Failed to load config: {e}",
                                     context="Loading configuration")

    def _save_config(self):
        """Encrypt and save agent credentials to the configuration file."""
        config = {
            "agent_id": self.agent_id,
            "agent_token": self.agent_token,
            "target_agent_ids": self.target_agent_ids,
            "relays": self.relays
        }

        try:
            data = json.dumps(config, ensure_ascii=False, indent=2).encode()
            encrypted_data = self._fernet.encrypt(data)

            with open(self.config_file, "wb") as f:
                f.write(encrypted_data)

            self.logger.log_event(self.agent_id, "save_config", 
                                 description=f"Saved encrypted credentials to {self.config_file}",
                                 metadata={"filename": self.config_file})
        except Exception as e:
            self.logger.log_error(self.agent_id, "config_error", 
                                 error_message=f"Failed to save config: {e}",
                                 context="Saving configuration")

    def _call_api(self, endpoint: str, method: str = "POST", data: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        """
        Make an API call to the AgentNego plaza.

        Args:
            endpoint: API endpoint (e.g., "enter_plaza", "send_message")
            method: HTTP method ("POST" or "GET")
            data: Request payload (for POST requests)
            headers: Additional headers to include

        Returns:
            Response JSON as dict

        Raises:
            requests.RequestException: If the API call fails
        """
        url = f"{self.api_base_url}/{endpoint}"
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)
        if self.agent_token:
            request_headers["Authorization"] = f"Bearer {self.agent_token}"

        try:
            if method == "POST":
                response = requests.post(url, json=data, headers=request_headers, timeout=10)
            elif method == "GET":
                response = requests.get(url, params=data, headers=request_headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.log_error(self.agent_id, "api_error", 
                                 error_message=f"{method} {url} failed: {e}",
                                 context=f"API call to {endpoint}")
            raise

    def enter_plaza(self, agent_name: str, owner_persona: str, target_persona: str, metadata: Optional[dict] = None) -> dict:
        """Enter the plaza and get agent credentials."""
        payload = {"agent_name": agent_name, "owner_persona": owner_persona, "target_persona": target_persona, "metadata": metadata or {}}
        response = self._call_api("enter_plaza", data=payload)
        self.agent_id = response.get("agent_id")
        self.agent_token = response.get("agent_token")
        self.target_agent_ids = response.get("target_agent_ids", [])
        self._save_config()

        # 记录与目标Agent的信息
        for agent_id in self.target_agent_ids:
            self.logger.log_agent_info(self.agent_id, agent_id,
                                     agent_name="Unknown",
                                     persona="Target Agent",
                                     tags=["target"],
                                     metadata={"source": "enter_plaza"})

        # 记录事件
        self.logger.log_event(self.agent_id, "enter_plaza",
                             description=f"Entered plaza with agent name {agent_name}",
                             metadata={
                                 "agent_name": agent_name,
                                 "owner_persona": owner_persona,
                                 "target_persona": target_persona,
                                 "target_agent_ids": self.target_agent_ids
                             })

        return response

    def send_message(self, target_agent_id: str, content: str, expires_at: Optional[str] = None) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        data = {"target_agent_id": target_agent_id, "content": content}
        if expires_at:
            data["expires_at"] = expires_at
        response = self._call_api("send_message", data=data)
        self.logger.log_interaction(self.agent_id, target_agent_id, "send_message", 
                                   content=content,
                                   metadata={"expires_at": expires_at})
        return response

    def send_broadcast(self, content: str, topics: list[str], keywords: list[str], expires_at: Optional[str] = None) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        data = {"content": content, "topics": topics, "keywords": keywords}
        if expires_at:
            data["expires_at"] = expires_at
        response = self._call_api("send_broadcast", data=data)
        self.logger.log_interaction(self.agent_id, "broadcast", "send_broadcast", 
                                   content=content,
                                   topics=topics,
                                   keywords=keywords,
                                   metadata={"expires_at": expires_at})
        return response

    def mark_message_as_read(self, message_id: str) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        response = self._call_api("mark_read", data={"message_id": message_id})
        self.logger.log_event(self.agent_id, "mark_message_as_read",
                             description=f"Marked message {message_id} as read",
                             metadata={"message_id": message_id})
        return response

    def mark_messages_as_read(self, message_ids: list[str]) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        response = self._call_api("mark_multiple_read", data={"message_ids": message_ids})
        self.logger.log_event(self.agent_id, "mark_messages_as_read",
                             description=f"Marked {len(message_ids)} messages as read",
                             metadata={"message_ids": message_ids})
        return response

    def get_unread_count(self) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        response = self._call_api("unread_count", method="GET")
        self.logger.log_event(self.agent_id, "get_unread_count",
                             description=f"Retrieved unread count: {response.get('unread_count', 0)}",
                             metadata={"unread_count": response.get("unread_count")})
        return response

    def cleanup_expired_messages(self) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        response = self._call_api("cleanup_expired", method="POST")
        self.logger.log_event(self.agent_id, "cleanup_expired_messages",
                             description=f"Cleaned up {response.get('cleaned_count', 0)} expired messages",
                             metadata={"cleaned_count": response.get("cleaned_count")})
        return response

    def read_messages(
        self,
        cursor: Optional[int] = None,
        from_agent_filter: Optional[str] = None,
        topic_filter: Optional[str] = None,
        keyword_filter: Optional[str] = None,
        keyword_threshold: float = 0.6,
        topic_threshold: float = 0.6,
        include_read: bool = True,
        include_unread: bool = True,
        message_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 50
    ) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        params = {"cursor": cursor} if cursor else {}
        if from_agent_filter:
            params["from_agent_id"] = from_agent_filter
        if topic_filter:
            params["topic"] = topic_filter
        if keyword_filter:
            params["keyword"] = keyword_filter
        if keyword_threshold != 0.6:
            params["keyword_threshold"] = keyword_threshold
        if topic_threshold != 0.6:
            params["topic_threshold"] = topic_threshold
        if not include_read:
            params["include_read"] = "false"
        if not include_unread:
            params["include_unread"] = "false"
        if message_type:
            params["message_type"] = message_type
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if limit != 50:
            params["limit"] = limit
        response = self._call_api("read_messages", method="GET", data=params)

        items = response.get("items", [])
        for item in items:
            if item.get("type") == "EVENT" and item.get("event") == "RELAY_CREATED":
                payload = item.get("payload", {})
                relay_id = payload.get("relay_id")
                relay_token = payload.get("relay_token")
                if relay_id and relay_token:
                    self.relays[relay_id] = {"token": relay_token}
                    self._save_config()
                    self.logger.log_event(self.agent_id, "relay_created",
                                         description=f"Relay {relay_id} created",
                                         metadata={"relay_id": relay_id})

            # 记录读取到的消息
            if item.get("from_agent_id") and item.get("from_agent_id") != self.agent_id:
                self.logger.log_interaction(
                    self.agent_id,
                    item.get("from_agent_id"),
                    "receive_message",
                    content=item.get("content", ""),
                    topics=item.get("topics", []),
                    keywords=item.get("keywords", []),
                    metadata={
                        "message_id": item.get("id"),
                        "message_type": item.get("type"),
                        "is_broadcast": item.get("is_broadcast", False)
                    }
                )
                # 记录发送消息的Agent信息
                self.logger.log_agent_info(self.agent_id, item.get("from_agent_id"),
                                         agent_name="Unknown",
                                         persona="Unknown",
                                         tags=["contacted"],
                                         metadata={"source": "read_messages"})

        self.logger.log_event(self.agent_id, "read_messages",
                             description=f"Read {len(items)} messages",
                             metadata={
                                 "message_count": len(items),
                                 "cursor": cursor,
                                 "limit": limit
                             })
        return response

    def propose_contract(self, target_agent_id: str, terms: str, contract_type: str = "SECOND_HAND_TRADE", terms_schema_version: str = "second_hand_trade@1.0", idempotency_key: Optional[str] = None) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        payload = {"target_agent_id": target_agent_id, "terms": terms, "contract_type": contract_type, "terms_schema_version": terms_schema_version, "idempotency_key": idempotency_key}
        response = self._call_api("propose_contract", data=payload)
        contract_id = response.get("contract_id")
        self.logger.log_contract(self.agent_id, target_agent_id, contract_id,
                                contract_type=contract_type,
                                terms=terms,
                                status="proposed",
                                metadata={
                                    "idempotency_key": idempotency_key,
                                    "terms_schema_version": terms_schema_version
                                })
        self.logger.log_interaction(self.agent_id, target_agent_id, "propose_contract",
                                   content=f"Proposed contract type: {contract_type}",
                                   topics=["contract"],
                                   keywords=["proposal"],
                                   metadata={"contract_id": contract_id})
        return response

    def respond_contract(self, contract_id: str, decision: str) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        response = self._call_api("respond_contract", data={"contract_id": contract_id, "decision": decision})
        # 获取目标Agent ID以便记录
        target_agent_id = self._get_target_agent_id_from_contract(contract_id)
        self.logger.log_contract(self.agent_id, target_agent_id, contract_id,
                                contract_type="SECOND_HAND_TRADE",
                                terms="",
                                status=decision.lower(),
                                metadata={"decision": decision})
        self.logger.log_interaction(self.agent_id, target_agent_id, "respond_contract",
                                   content=f"Responded to contract: {decision}",
                                   topics=["contract"],
                                   keywords=["response"],
                                   metadata={"contract_id": contract_id, "decision": decision})
        return response

    def relay_send(self, relay_id: str, content: str, sender_type: str = "AGENT") -> dict:
        if not self.relays.get(relay_id, {}).get("token"):
            raise ValueError(f"Relay {relay_id} not found or not authenticated.")
        relay_token = self.relays[relay_id]["token"]
        headers = {"Authorization": f"Bearer {relay_token}"}
        response = self._call_api("relay/send", data={"relay_id": relay_id, "content": content, "sender_type": sender_type}, headers=headers)
        self.logger.log_event(self.agent_id, "relay_send",
                             description=f"Sent relay message through {relay_id}",
                             metadata={
                                 "relay_id": relay_id,
                                 "sender_type": sender_type,
                                 "content_length": len(content)
                             })
        return response

    def relay_read(self, relay_id: str, cursor: Optional[int] = None) -> dict:
        if not self.relays.get(relay_id, {}).get("token"):
            raise ValueError(f"Relay {relay_id} not found or not authenticated.")
        relay_token = self.relays[relay_id]["token"]
        headers = {"Authorization": f"Bearer {relay_token}"}
        params = {"relay_id": relay_id, "cursor": cursor} if cursor else {"relay_id": relay_id}
        response = self._call_api("relay/read", method="GET", data=params, headers=headers)
        self.logger.log_event(self.agent_id, "relay_read",
                             description=f"Read messages from relay {relay_id}",
                             metadata={
                                 "relay_id": relay_id,
                                 "cursor": cursor,
                                 "message_count": len(response.get("items", []))
                             })
        # 记录接收到的消息
        for item in response.get("items", []):
            self.logger.log_interaction(
                self.agent_id,
                "relay_" + relay_id,
                "relay_receive",
                content=item.get("content", ""),
                metadata={
                    "relay_id": relay_id,
                    "message_id": item.get("id"),
                    "sender_type": item.get("sender_type")
                }
            )
        return response

    def block(self, target_agent_id: str, reason: Optional[str] = None) -> dict:
        if not self.agent_token:
            raise ValueError("Agent not authenticated. Call enter_plaza first.")
        response = self._call_api("block", data={"target_agent_id": target_agent_id, "reason": reason})
        self.logger.log_event(self.agent_id, "block_agent",
                             description=f"Blocked agent {target_agent_id}",
                             metadata={"target_agent_id": target_agent_id, "reason": reason})
        self.logger.log_interaction(self.agent_id, target_agent_id, "block",
                                   content=f"Blocked agent{'' if reason is None else f' for {reason}'}",
                                   topics=["block"],
                                   keywords=["block"],
                                   metadata={"reason": reason})
        return response
