#!/usr/bin/env python3
"""
Inventory Manager - Check and sync stock levels across e-commerce stores

Usage:
    python inventory_manager.py --action check --stores taobao,douyin --output stock.csv
    python inventory_manager.py --action sync --source taobao --target douyin
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

class InventoryManager:
    def __init__(self):
        self.stores = {}
        self.logs = []
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def load_store_data(self, store_name):
        """Load inventory data for a store (simulated)."""
        # In production, this would call Taobao/Douyin API
        # For now, return sample data
        sample_data = {
            'taobao': [
                {'sku': 'SKU001', 'name': 'Product A', 'stock': 150, 'sold_today': 12},
                {'sku': 'SKU002', 'name': 'Product B', 'stock': 8, 'sold_today': 5},
                {'sku': 'SKU003', 'name': 'Product C', 'stock': 45, 'sold_today': 3},
            ],
            'douyin': [
                {'sku': 'SKU001', 'name': 'Product A', 'stock': 120, 'sold_today': 8},
                {'sku': 'SKU002', 'name': 'Product B', 'stock': 15, 'sold_today': 10},
                {'sku': 'SKU003', 'name': 'Product C', 'stock': 3, 'sold_today': 7},
            ]
        }
        return sample_data.get(store_name, [])
    
    def check_stock(self, stores, output_file):
        """Check stock levels across stores."""
        self.log(f"Checking stock for stores: {stores}")
        
        all_stock = []
        
        for store_name in stores:
            self.log(f"Loading data from {store_name}...")
            products = self.load_store_data(store_name)
            
            for product in products:
                product['store'] = store_name
                product['checked_at'] = datetime.now().isoformat()
                
                # Add stock status
                stock = product.get('stock', 0)
                if stock <= 5:
                    product['status'] = 'CRITICAL'
                elif stock <= 10:
                    product['status'] = 'LOW'
                elif stock <= 20:
                    product['status'] = 'MEDIUM'
                else:
                    product['status'] = 'GOOD'
                
                all_stock.append(product)
        
        # Save to file
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                fieldnames = ['store', 'sku', 'name', 'stock', 'sold_today', 'status', 'checked_at']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_stock)
            
            self.log(f"Stock report saved to: {output_path}")
        
        # Summary
        critical = len([p for p in all_stock if p['status'] == 'CRITICAL'])
        low = len([p for p in all_stock if p['status'] == 'LOW'])
        
        self.log(f"Summary: {critical} critical, {low} low stock items")
        
        return {
            'status': 'success',
            'total_products': len(all_stock),
            'critical': critical,
            'low': low
        }
    
    def sync_inventory(self, source, target, conflict_resolution='source_wins'):
        """Sync inventory from source to target store."""
        self.log(f"Syncing inventory: {source} -> {target}")
        self.log(f"Conflict resolution: {conflict_resolution}")
        
        source_data = self.load_store_data(source)
        target_data = self.load_store_data(target)
        
        # Create lookup by SKU
        target_lookup = {p['sku']: p for p in target_data}
        
        sync_results = []
        
        for source_product in source_data:
            sku = source_product['sku']
            source_stock = source_product['stock']
            
            if sku in target_lookup:
                target_stock = target_lookup[sku]['stock']
                
                # Apply conflict resolution
                if conflict_resolution == 'source_wins':
                    new_stock = source_stock
                elif conflict_resolution == 'target_wins':
                    new_stock = target_stock
                elif conflict_resolution == 'max':
                    new_stock = max(source_stock, target_stock)
                elif conflict_resolution == 'min':
                    new_stock = min(source_stock, target_stock)
                else:
                    new_stock = source_stock
                
                sync_results.append({
                    'sku': sku,
                    'source_stock': source_stock,
                    'target_stock': target_stock,
                    'new_stock': new_stock,
                    'action': 'updated'
                })
            else:
                # Product doesn't exist in target
                sync_results.append({
                    'sku': sku,
                    'source_stock': source_stock,
                    'target_stock': 0,
                    'new_stock': source_stock,
                    'action': 'created'
                })
        
        self.log(f"Sync complete: {len(sync_results)} products processed")
        
        for result in sync_results:
            self.log(f"  {result['sku']}: {result['action']} -> {result['new_stock']} units")
        
        return {
            'status': 'success',
            'synced': len(sync_results),
            'details': sync_results
        }
    
    def stock_alerts(self, threshold, notify_channels):
        """Check for low stock and send alerts."""
        self.log(f"Checking stock alerts (threshold: {threshold})")
        
        all_products = []
        for store in ['taobao', 'douyin']:
            all_products.extend(self.load_store_data(store))
        
        alerts = []
        for product in all_products:
            if product['stock'] <= threshold:
                alerts.append({
                    'sku': product['sku'],
                    'name': product['name'],
                    'store': product.get('store', 'unknown'),
                    'current_stock': product['stock'],
                    'threshold': threshold,
                    'severity': 'critical' if product['stock'] <= 5 else 'warning'
                })
        
        if alerts:
            self.log(f"⚠️ {len(alerts)} alerts triggered!")
            for alert in alerts:
                self.log(f"  {alert['severity'].upper()}: {alert['sku']} - {alert['name']} ({alert['current_stock']} units)")
            
            # In production, would send email/WeChat notifications here
            if 'email' in notify_channels:
                self.log("📧 Email alerts would be sent")
            if 'wechat' in notify_channels:
                self.log("💬 WeChat alerts would be sent")
        else:
            self.log("✅ All stock levels OK")
        
        return {
            'status': 'success',
            'alerts': len(alerts),
            'details': alerts
        }

def main():
    parser = argparse.ArgumentParser(description='Inventory Manager')
    parser.add_argument('--action', required=True,
                        choices=['check', 'sync', 'alerts'],
                        help='Action to perform')
    parser.add_argument('--stores', help='Comma-separated store names')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--source', help='Source store for sync')
    parser.add_argument('--target', help='Target store for sync')
    parser.add_argument('--threshold', type=int, default=10,
                        help='Low stock threshold')
    parser.add_argument('--notify', help='Notification channels (comma-separated)')
    parser.add_argument('--conflict-resolution', default='source_wins',
                        choices=['source_wins', 'target_wins', 'max', 'min'],
                        help='Conflict resolution strategy')
    args = parser.parse_args()
    
    manager = InventoryManager()
    
    if args.action == 'check':
        stores = args.stores.split(',') if args.stores else ['taobao', 'douyin']
        result = manager.check_stock(stores, args.output)
    
    elif args.action == 'sync':
        if not args.source or not args.target:
            print("Error: --source and --target required for sync")
            return 1
        result = manager.sync_inventory(args.source, args.target, args.conflict_resolution)
    
    elif args.action == 'alerts':
        notify = args.notify.split(',') if args.notify else ['email']
        result = manager.stock_alerts(args.threshold, notify)
    
    else:
        result = {'status': 'error', 'message': 'Unknown action'}
    
    print(f"\nResult: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return 0 if result.get('status') == 'success' else 1

if __name__ == '__main__':
    sys.exit(main())
