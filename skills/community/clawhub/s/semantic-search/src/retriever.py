import asyncio
import pandas as pd
from typing import Optional, List, Dict, Callable
import sys
import os

# Add project root to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.vector.vector_db import FlightDataBase
from utils.logger import logger

class VannaRetriever:
    """
    A retriever tool inspired by Vanna AI that fetches relevant SQL examples 
    or context based on the user query.
    
    It assumes a vector database table containing pairs of questions and SQL queries.
    """
    
    def __init__(self, client: FlightDataBase, table_name: str = "sql_examples", top_k: int = 3):
        """
        Initialize the Vanna-like retriever.
        
        Args:
            client: FlightDataBase instance for vector search
            table_name: Name of the table containing (question, sql, question_embedding)
            top_k: Number of examples to retrieve
        """
        self.client = client
        self.table_name = table_name
        self.top_k = top_k
        self._ensure_table_exists()
        
    def _ensure_table_exists(self):
        """Ensure the vector table exists, create if not."""
        if not self.client.check_table_exist(self.table_name):
            schema = {
                "resource_id": "INT32",
                "question": "VARCHAR",
                "sql": "VARCHAR",
                "question_embedding": "VECTOR(1024)"
            }
            logger.info(f"VannaRetriever: Table {self.table_name} not found, creating...")
            self.client.create_vector_view(self.table_name, schema)
        
    def retrieve(self, query: str) -> str:
        """
        Retrieve relevant context for the given query.
        Returns a formatted string of examples/context.
        """
        try:
            # Run async search in a sync context
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Define fields mapping: text_field -> embedding_field
            # This assumes the table has 'question' and 'question_embedding' columns
            fields = {"question": "question_embedding"}
            
            logger.info(f"VannaRetriever: Searching table '{self.table_name}' for query: {query}")
            
            # Execute vector search
            # vector_search_multi_fields returns a DataFrame
            df_result = loop.run_until_complete(
                self.client.vector_search_multi_fields(
                    query=query,
                    fields=fields,
                    top_k=self.top_k,
                    table_name=self.table_name
                )
            )
            
            if df_result.empty:
                logger.info("VannaRetriever: No results found.")
                return ""
                
            # Format the results
            # Expected columns: 'question', 'sql' (plus others)
            context_parts = []
            for _, row in df_result.iterrows():
                q = row.get('question', '')
                s = row.get('sql', '')
                
                # If 'sql' column is missing, try to use 'content' or just return available info
                if not s and 'content' in row:
                    s = row['content']
                    
                if q or s:
                    context_parts.append(f"Q: {q}\nSQL: {s}")
            
            result_str = "\n".join(context_parts)
            logger.info(f"VannaRetriever: Found {len(context_parts)} examples.")
            return result_str
            
        except Exception as e:
            logger.warning(f"VannaRetriever failed: {e}")
            # Fail gracefully by returning empty string so the agent can continue without context
            return ""

    def __call__(self, query: str) -> str:
        """Allow the instance to be called like a function"""
        return self.retrieve(query)

    def add_example(self, question: str, sql: str) -> bool:
        """
        Add a new example (question, sql) to the vector database.
        """
        try:
            # Prepare data for insertion
            # We need to match the structure expected by insert_data
            # insert_data expects metadatas=[{"question":..., "sql":...}] and embed_fields=["question"]
            
            metadata = [{
                "question": question,
                "sql": sql,
                "resource_id": 0  # Placeholder or generate unique ID
            }]
            
            # Use async loop to call insert_data
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            loop.run_until_complete(
                self.client.insert_data(
                    table_name=self.table_name,
                    embed_fields=["question"],
                    metadatas=metadata
                )
            )
            logger.info(f"VannaRetriever: Added example: {question}")
            return True
            
        except Exception as e:
            logger.error(f"VannaRetriever: Failed to add example: {e}")
            return False
