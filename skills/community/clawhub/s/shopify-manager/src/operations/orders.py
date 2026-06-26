"""Order operations."""

from typing import Dict, List, Optional
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class OrderOperations:
    """Order management operations."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    def list_orders(self, status: str = 'any', limit: int = 20, **filters) -> List[Dict]:
        """List orders with filters."""
        orders = self.client.get_orders(status=status, limit=limit, **filters)
        return orders
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order by ID."""
        try:
            order_id_int = int(order_id)
            return self.client.get_order(order_id_int)
        except ValueError:
            raise ValueError(f"Invalid order ID: {order_id}")
    
    def fulfill_order(self, order_id: str, tracking_number: Optional[str] = None,
                     tracking_company: Optional[str] = None, 
                     location_id: Optional[int] = None,
                     force: bool = False) -> Dict:
        """Fulfill an order."""
        order = self.get_order(order_id)
        if not order:
            raise ValueError(f"Order not found: {order_id}")
        
        order_id_int = order['id']
        
        # Check if already fulfilled
        if order.get('fulfillment_status') == 'fulfilled':
            return {'error': 'Order is already fulfilled'}
        
        # Build fulfillment data
        fulfillment_data = {
            'location_id': location_id,
            'tracking_number': tracking_number,
            'tracking_company': tracking_company,
        }
        
        # Remove None values
        fulfillment_data = {k: v for k, v in fulfillment_data.items() if v is not None}
        
        # Get default location if not specified
        if not location_id:
            locations = self.client.get_locations()
            if locations:
                fulfillment_data['location_id'] = locations[0]['id']
        
        # Line items to fulfill
        line_items = [{'id': item['id']} for item in order.get('line_items', [])]
        fulfillment_data['line_items'] = line_items
        
        # Validate
        is_valid, error = self.safety.validate_operation('order_fulfill', {
            'order_id': order_id_int,
            **fulfillment_data
        })
        if not is_valid:
            raise ValueError(error)
        
        # Preview
        changes = [{
            'action': f"Fulfill order #{order.get('name', order_id)}",
            'details': {
                'customer': order.get('customer', {}).get('email', 'Guest'),
                'items': len(line_items),
                'tracking': tracking_number or 'None',
            }
        }]
        self.safety.preview_changes("Order Fulfillment", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'order_id': order_id_int, 'fulfillment_data': fulfillment_data}
        
        # Create fulfillment
        fulfillment = self.client.fulfill_order(order_id_int, fulfillment_data)
        
        # Audit log
        self.audit.log_change('order', order_id_int, 'fulfill', order, {**order, 'fulfillment_status': 'fulfilled'})
        
        return fulfillment
    
    def refund_order(self, order_id: str, amount: Optional[float] = None,
                    reason: str = "", refund_line_items: Optional[List] = None,
                    force: bool = False) -> Dict:
        """Process refund for an order."""
        order = self.get_order(order_id)
        if not order:
            raise ValueError(f"Order not found: {order_id}")
        
        order_id_int = order['id']
        
        # Validate
        is_valid, error = self.safety.validate_operation('order_refund', {
            'order_id': order_id_int,
            'amount': amount,
        })
        if not is_valid:
            raise ValueError(error)
        
        # Require confirmation for refunds
        refund_amount = amount or order.get('total_price', '0')
        if self.safety.requires_confirmation('refunds'):
            if not self.safety.request_confirmation(
                'Process Refund',
                f"Refund {refund_amount} for order #{order.get('name')}? Reason: {reason or 'Not specified'}",
                force=force
            ):
                return {'cancelled': True}
        
        # Build refund data
        if not refund_line_items:
            # Refund all line items
            refund_line_items = [
                {'line_item_id': item['id'], 'quantity': item['quantity']}
                for item in order.get('line_items', [])
            ]
        
        refund_data = {
            'note': reason,
            'refund_line_items': refund_line_items,
        }
        
        # Calculate refund if amount specified
        if amount:
            refund_data['transactions'] = [{
                'parent_id': order.get('transactions', [{}])[0].get('id'),
                'amount': amount,
                'kind': 'refund',
                'gateway': order.get('gateway', ''),
            }]
        
        # Preview
        changes = [{
            'action': f"Refund order #{order.get('name')}",
            'before': f"Total: {order.get('total_price')}",
            'after': f"Refund: {refund_amount}",
            'warning': 'This will process a financial transaction.',
        }]
        self.safety.preview_changes("Order Refund", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'order_id': order_id_int, 'refund_data': refund_data}
        
        # Process refund
        refund = self.client.create_refund(order_id_int, refund_data)
        
        # Audit log
        self.audit.log_change('order', order_id_int, 'refund', order, {**order, 'refund_processed': True})
        
        return refund
    
    def format_order_list(self, orders: List[Dict]) -> str:
        """Format order list for display."""
        if not orders:
            return "No orders found."
        
        lines = [f"{'Order':<10} {'Date':<12} {'Customer':<25} {'Total':<10} {'Status':<12} {'Fulfillment':<12}"]
        lines.append("-" * 81)
        
        for o in orders:
            name = o.get('name', 'N/A')
            date = o.get('created_at', '')[:10]
            customer = o.get('customer', {}).get('email', 'Guest')[:23]
            total = o.get('total_price', 'N/A')
            status = o.get('financial_status', 'unknown')
            fulfillment = o.get('fulfillment_status') or 'unfulfilled'
            
            lines.append(f"{name:<10} {date:<12} {customer:<25} {total:<10} {status:<12} {fulfillment:<12}")
        
        return "\n".join(lines)
