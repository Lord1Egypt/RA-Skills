"""
Tariff Search Library - TurtleClassify RESTful API Client for Tariff Classification

This library provides functions to query tariff classification and HS code information
through the TurtleClassify RESTful API (https://www.accio.com/api/turtle/classify).
It supports single and batch product classification.
"""

import json
import sys
import time
import random
from typing import List, Dict, Any, Tuple, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os

# Auto-add skills directory to Python path if not already present
_SKILLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SKILLS_DIR not in sys.path:
    sys.path.insert(0, _SKILLS_DIR)


class TariffSearch:
    DEFAULT_BASE_URL = 'https://www.accio.com'
    MAX_BATCH_SIZE = 50
    MAX_TOTAL_PRODUCTS = 100

    def __init__(self, base_url: str = '', timeout: int = 300):
        self.base_url = base_url if base_url else self.DEFAULT_BASE_URL
        self.timeout = timeout

    def search_tariff(self, products: List[Dict[str, Any]], return_type: str = 'list') -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        start_time = time.time()
        validated_products = []
        for idx, product in enumerate(products):
            is_valid, error_msg = self._validate_product(product)
            if not is_valid:
                if return_type == 'detail':
                    return {'success': False, 'error': f"Error in product {idx + 1}: {error_msg}", 'results': []}
                else:
                    print(f"[WARNING] Product {idx + 1} validation failed: {error_msg}")
            validated_products.append(product)
        try:
            results = self._process_products(validated_products)
            processing_time = time.time() - start_time
            if return_type == 'detail':
                response = results[0] if len(results) == 1 else {'data': results}
                formatted_output = self._format_output(response)
                return {
                    'success': True,
                    'results': results,
                    'formatted_output': formatted_output,
                    'raw_response': response,
                    'processing_time': processing_time,
                    'products_count': len(validated_products),
                    'base_url': self.base_url,
                }
            else:
                flattened_results = []
                for idx, result in enumerate(results):
                    product = validated_products[idx] if idx < len(validated_products) else {}
                    if not result or 'data' not in result:
                        flattened_results.append({
                            'hsCode': '',
                            'tariffRate': 0,
                            'tariffFormula': '',
                            'tariffCalculateType': '',
                            'originCountryCode': product.get('originCountryCode', ''),
                            'destinationCountryCode': product.get('destinationCountryCode', ''),
                            'productName': product.get('productName', ''),
                            'calculationDetails': {},
                        })
                    else:
                        flattened_results.append(self._extract_flattened_result(result['data'], product))
                return flattened_results
        except Exception as e:
            import traceback
            err = traceback.format_exc()
            if return_type == 'detail':
                return {'success': False, 'error': str(e), 'error_trace': err, 'results': []}
            else:
                print(f"[ERROR] {e}")
                return []

    # ... (additional helper methods unchanged from original) ...

    def _validate_product(self, product: Dict[str, Any]) -> Tuple[bool, str]:
        required = {'originCountryCode': 'Origin country code', 'destinationCountryCode': 'Destination country code', 'productName': 'Product name'}
        for f, n in required.items():
            if f not in product or not product[f]:
                return False, f"Missing required field: {n} ({f})"
        digit = product.get('digit')
        if digit is not None and (not isinstance(digit, int) or digit not in (8, 10)):
            return False, f"digit must be 8 or 10, got {digit}"
        if 'source' not in product or not product['source']:
            product['source'] = 'alibaba'
        return True, ''

    def _call_restful_api(self, product: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"{self.base_url.rstrip('/')}/api/turtle/classify"
        payload = {
            'source': product.get('source', 'alibaba'),
            'originCountryCode': product.get('originCountryCode', 'CN'),
            'destinationCountryCode': product.get('destinationCountryCode', 'US'),
            'productName': product.get('productName', ''),
        }
        for key in ['digit', 'productId', 'productSource', 'productCategoryId', 'productCategoryName', 'productProperties', 'productKeywords', 'channel']:
            if key in product and product[key]:
                payload[key] = product[key]
        try:
            r = requests.post(endpoint, json=payload, timeout=self.timeout)
            r.raise_for_status()
            res = r.json()
            if not res.get('success'):
                return {}
            data_field = res.get('data', '')
            if isinstance(data_field, str):
                inner = json.loads(data_field)
            else:
                inner = data_field
            if inner.get('success'):
                return {'data': inner.get('data', {}), 'raw_inner_response': inner}
            return {}
        except Exception as e:
            print(f"[ERROR] API call failed: {e}")
            return {}

    # Remaining methods (_extract_flattened_result, _process_batch, _process_products, etc.) would be copied from the original script.

# End of file
