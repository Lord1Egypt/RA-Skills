#!/usr/bin/env python3
"""
Compensation Transaction Pattern - Complete Examples
"""

import asyncio
from typing import Dict, Any, List, Callable
from datetime import datetime


class CompensationAction:
    """Compensation Action"""
    def __init__(self, name: str, action: Callable, params: Dict, 
                 rollback: Callable = None):
        self.name = name
        self.action = action
        self.params = params
        self.rollback = rollback
        self.executed = False
        self.result = None


class CompensationChain:
    """
    Compensation Transaction Chain
    
    Features:
    - Execute multiple actions sequentially
    - Auto-rollback executed actions on failure
    - Support action result passing
    """
    
    def __init__(self, name: str = "compensation_chain"):
        self.name = name
        self.actions: List[CompensationAction] = []
        self.executed_actions: List[CompensationAction] = []
        self.failed_action: CompensationAction = None
        self.error: Exception = None
    
    def add_action(self, name: str, action: Callable, params: Dict = None,
                   rollback: Callable = None):
        """Add compensation action"""
        self.actions.append(CompensationAction(
            name=name,
            action=action,
            params=params or {},
            rollback=rollback
        ))
        return self  # Support chaining
    
    async def execute(self) -> Dict[str, Any]:
        """
        Execute compensation transaction chain
        
        Returns:
            Execution result statistics
        """
        print(f"🔄 Starting compensation chain: {self.name}")
        print(f"   Total {len(self.actions)} actions")
        
        try:
            for i, action in enumerate(self.actions, 1):
                print(f"\n  [{i}/{len(self.actions)}] Executing: {action.name}")
                
                # Execute action
                action.result = await action.action(**action.params)
                action.executed = True
                self.executed_actions.append(action)
                
                print(f"      ✅ Success: {action.result}")
            
            print(f"\n✅ Compensation chain completed: {self.name}")
            return {
                'success': True,
                'executed_count': len(self.executed_actions),
                'results': [a.result for a in self.executed_actions]
            }
            
        except Exception as e:
            print(f"\n❌ Action failed: {e}")
            self.error = e
            self.failed_action = self.executed_actions[-1] if self.executed_actions else None
            
            # Rollback executed actions
            await self._rollback()
            
            raise CompensationError(f"Compensation failed: {e}")
    
    async def _rollback(self):
        """Rollback executed actions"""
        if not self.executed_actions:
            return
        
        print(f"\n🔄 Starting rollback ({len(self.executed_actions)} actions)...")
        
        for action in reversed(self.executed_actions):
            if action.rollback:
                try:
                    print(f"  ↩️  Rolling back: {action.name}")
                    await action.rollback(**action.params)
                    print(f"      ✅ Rollback successful")
                except Exception as e:
                    print(f"      ⚠️ Rollback failed: {e}")
            else:
                print(f"  ↩️  {action.name} (no rollback)")
    
    def get_execution_log(self) -> List[Dict]:
        """Get execution log"""
        return [
            {
                'name': a.name,
                'executed': a.executed,
                'result': a.result
            }
            for a in self.actions
        ]


class CompensationError(Exception):
    """Compensation Transaction Exception"""
    pass


# ==================== Concrete Scenario Examples ====================

class EmailService:
    """Email Service Simulation"""
    
    def __init__(self, fail_rate: float = 0.0):
        self.fail_rate = fail_rate
        self.sent_emails = []
    
    async def send(self, to: str, subject: str, body: str) -> str:
        """Send email"""
        import random
        if random.random() < self.fail_rate:
            raise Exception("SMTP server unavailable")
        
        email_id = f"email_{len(self.sent_emails)}"
        self.sent_emails.append({
            'id': email_id,
            'to': to,
            'subject': subject
        })
        return email_id
    
    async def recall(self, email_id: str):
        """Recall email"""
        self.sent_emails = [e for e in self.sent_emails if e['id'] != email_id]
        return True


class NotificationService:
    """Notification Service Simulation"""
    
    def __init__(self):
        self.notifications = []
    
    async def send_sms(self, phone: str, message: str) -> str:
        """Send SMS"""
        notif_id = f"sms_{len(self.notifications)}"
        self.notifications.append({
            'id': notif_id,
            'type': 'sms',
            'phone': phone,
            'message': message
        })
        return notif_id
    
    async def delete_notification(self, notif_id: str):
        """Delete notification"""
        self.notifications = [n for n in self.notifications if n['id'] != notif_id]
        return True


class LoggerService:
    """Logger Service"""
    
    def __init__(self):
        self.logs = []
    
    async def log_failure(self, error: str, context: Dict) -> str:
        """Log failure"""
        log_id = f"log_{len(self.logs)}"
        self.logs.append({
            'id': log_id,
            'timestamp': datetime.now().isoformat(),
            'error': error,
            'context': context
        })
        return log_id
    
    async def delete_log(self, log_id: str):
        """Delete log"""
        self.logs = [l for l in self.logs if l['id'] != log_id]
        return True


# ==================== Complete Examples ====================

async def email_with_compensation_example():
    """
    Example: Compensation handling after email sending failure
    """
    print("=" * 60)
    print("Scenario: Compensation after email sending failure")
    print("=" * 60)
    print()
    
    # Initialize services
    email_service = EmailService(fail_rate=0.5)  # 50% failure rate for testing
    notification_service = NotificationService()
    logger_service = LoggerService()
    
    # Email data
    email_data = {
        'to': 'user@example.com',
        'subject': 'Important Notification',
        'body': 'This is an important email...',
        'phone': '13800138000'  # Backup phone number
    }
    
    try:
        # Try to send email
        print("📧 Trying to send email...")
        email_id = await email_service.send(
            email_data['to'],
            email_data['subject'],
            email_data['body']
        )
        print(f"✅ Email sent successfully: {email_id}")
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        print("\n🔄 Starting compensation transaction...\n")
        
        # Create compensation chain
        chain = CompensationChain("email_failure_compensation")
        
        # 1. Log failure
        log_id = None
        async def log_failure_action(error, email):
            nonlocal log_id
            log_id = await logger_service.log_failure(
                str(error),
                {'email': email, 'time': datetime.now().isoformat()}
            )
            return log_id
        
        chain.add_action(
            name="Log failure",
            action=log_failure_action,
            params={'error': e, 'email': email_data},
            rollback=lambda log_id: logger_service.delete_log(log_id)
        )
        
        # 2. Send SMS notification
        sms_id = None
        async def send_sms_notification(phone, subject):
            nonlocal sms_id
            sms_id = await notification_service.send_sms(
                phone,
                f"Email sending failed, subject: {subject}"
            )
            return sms_id
        
        chain.add_action(
            name="Send SMS notification",
            action=send_sms_notification,
            params={'phone': email_data['phone'], 'subject': email_data['subject']},
            rollback=lambda: notification_service.delete_notification(sms_id)
        )
        
        # 3. Queue for retry
        retry_queued = False
        async def queue_for_retry(email):
            nonlocal retry_queued
            # Simulate queueing
            retry_queued = True
            return f"queued_{email['to']}"
        
        chain.add_action(
            name="Queue for retry",
            action=queue_for_retry,
            params={'email': email_data}
            # No rollback
        )
        
        # Execute compensation
        try:
            result = await chain.execute()
            print(f"\n✅ Compensation executed successfully")
            print(f"   Actions executed: {result['executed_count']}")
            print(f"   Results: {result['results']}")
        except CompensationError as ce:
            print(f"\n❌ Compensation failed: {ce}")
    
    # Print final status
    print("\n" + "=" * 60)
    print("Final Status:")
    print(f"  Emails sent: {len(email_service.sent_emails)}")
    print(f"  Notifications: {len(notification_service.notifications)}")
    print(f"  Log entries: {len(logger_service.logs)}")
    for log in logger_service.logs:
        print(f"    - {log['timestamp']}: {log['error']}")


async def order_processing_example():
    """
    Example: Order processing compensation
    """
    print("\n" + "=" * 60)
    print("Scenario: Order processing failure compensation")
    print("=" * 60)
    print()
    
    # Simulate database
    database = {
        'orders': [],
        'inventory': {'product_1': 100},
        'payments': []
    }
    
    async def create_order(user_id: str, product_id: str, quantity: int):
        """Create order"""
        order_id = f"order_{len(database['orders'])}"
        database['orders'].append({
            'id': order_id,
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'status': 'created'
        })
        return order_id
    
    async def cancel_order(order_id: str):
        """Cancel order"""
        database['orders'] = [o for o in database['orders'] if o['id'] != order_id]
        return True
    
    async def deduct_inventory(product_id: str, quantity: int):
        """Deduct inventory"""
        if database['inventory'][product_id] < quantity:
            raise Exception("Insufficient inventory")
        database['inventory'][product_id] -= quantity
        return f"deduct_{product_id}_{quantity}"
    
    async def restore_inventory(product_id: str, quantity: int):
        """Restore inventory"""
        database['inventory'][product_id] += quantity
        return True
    
    async def process_payment(order_id: str, amount: float):
        """Process payment"""
        # Simulate payment failure
        raise Exception("Payment gateway timeout")
    
    # Execute order processing
    chain = CompensationChain("order_processing")
    
    order_id = None
    deduct_id = None
    
    chain.add_action(
        name="Create order",
        action=lambda user_id, product_id, quantity: create_order(user_id, product_id, quantity),
        params={'user_id': 'user_123', 'product_id': 'product_1', 'quantity': 2},
        rollback=lambda: cancel_order(order_id) if order_id else None
    )
    
    chain.add_action(
        name="Deduct inventory",
        action=lambda product_id, quantity: deduct_inventory(product_id, quantity),
        params={'product_id': 'product_1', 'quantity': 2},
        rollback=lambda: restore_inventory('product_1', 2)
    )
    
    chain.add_action(
        name="Process payment",
        action=lambda order_id, amount: process_payment(order_id, amount),
        params={'order_id': 'order_placeholder', 'amount': 199.99}
    )
    
    try:
        await chain.execute()
    except CompensationError as e:
        print(f"Order processing failed: {e}")
    
    print(f"\nFinal database state:")
    print(f"  Orders: {database['orders']}")
    print(f"  Inventory: {database['inventory']}")


# ==================== Main Program ====================

async def main():
    """Run all examples"""
    await email_with_compensation_example()
    await order_processing_example()


if __name__ == '__main__':
    asyncio.run(main())
