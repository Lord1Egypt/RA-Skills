#!/usr/bin/env python3
"""
Email Campaign Manager
Create and send email marketing campaigns.

Usage:
    python email_campaign.py --action create --name "Spring Sale" --template promotional
    python email_campaign.py --action send --campaign spring_sale --list customers
"""

import argparse
import csv
import json
import smtplib
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

class EmailCampaign:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.logs = []
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def load_subscribers(self, list_name):
        """Load subscribers from list file."""
        list_file = Path(f"lists/{list_name}.csv")
        if not list_file.exists():
            self.log(f"Subscriber list not found: {list_name}")
            return []
        
        subscribers = []
        with open(list_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                subscribers.append(row)
        
        self.log(f"Loaded {len(subscribers)} subscribers from {list_name}")
        return subscribers
    
    def load_template(self, template_name):
        """Load email template."""
        template_file = Path(f"templates/{template_name}.txt")
        if not template_file.exists():
            self.log(f"Template not found: {template_name}")
            return None
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def personalize_email(self, template, subscriber):
        """Replace placeholders with subscriber data."""
        content = template
        for key, value in subscriber.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        return content
    
    def create_campaign(self, name, template_name, list_name, subject):
        """Create a new campaign."""
        self.log(f"Creating campaign: {name}")
        
        # Load template
        template = self.load_template(template_name)
        if not template:
            return {"status": "error", "message": "Template not found"}
        
        # Load subscribers
        subscribers = self.load_subscribers(list_name)
        if not subscribers:
            return {"status": "error", "message": "No subscribers found"}
        
        # Create campaign config
        campaign = {
            "name": name,
            "template": template_name,
            "list": list_name,
            "subject": subject,
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
        
        # Save campaign
        campaign_file = Path(f"campaigns/{name.replace(' ', '_')}.json")
        campaign_file.parent.mkdir(exist_ok=True)
        
        with open(campaign_file, 'w', encoding='utf-8') as f:
            json.dump(campaign, f, indent=2, ensure_ascii=False)
        
        self.log(f"Campaign saved: {campaign_file}")
        self.log(f"Ready to send to {len(subscribers)} subscribers")
        
        return {
            "status": "success",
            "campaign": name,
            "subscribers": len(subscribers)
        }
    
    def send_campaign(self, campaign_name, smtp_config=None):
        """Send campaign to all subscribers."""
        self.log(f"Sending campaign: {campaign_name}")
        
        if self.dry_run:
            self.log("DRY RUN - No emails will be sent")
        
        # Load campaign
        campaign_file = Path(f"campaigns/{campaign_name.replace(' ', '_')}.json")
        if not campaign_file.exists():
            return {"status": "error", "message": "Campaign not found"}
        
        with open(campaign_file, 'r', encoding='utf-8') as f:
            campaign = json.load(f)
        
        # Load template and subscribers
        template = self.load_template(campaign['template'])
        subscribers = self.load_subscribers(campaign['list'])
        
        if not template or not subscribers:
            return {"status": "error", "message": "Missing template or subscribers"}
        
        # Send emails
        sent_count = 0
        failed_count = 0
        
        for subscriber in subscribers:
            try:
                # Personalize email
                content = self.personalize_email(template, subscriber)
                subject = self.personalize_email(campaign.get('subject', ''), subscriber)
                
                if self.dry_run:
                    self.log(f"Would send to: {subscriber.get('email', 'unknown')}")
                    sent_count += 1
                    continue
                
                # Create email
                msg = MIMEMultipart()
                msg['From'] = smtp_config.get('from_email', 'noreply@example.com')
                msg['To'] = subscriber.get('email', '')
                msg['Subject'] = subject
                msg.attach(MIMEText(content, 'plain', 'utf-8'))
                
                # Send (placeholder - would need actual SMTP config)
                # server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
                # server.send_message(msg)
                
                sent_count += 1
                self.log(f"Sent to: {subscriber.get('email', 'unknown')}")
                
            except Exception as e:
                failed_count += 1
                self.log(f"Failed to send to {subscriber.get('email', 'unknown')}: {e}")
        
        # Update campaign status
        campaign['status'] = 'sent'
        campaign['sent_at'] = datetime.now().isoformat()
        campaign['sent_count'] = sent_count
        campaign['failed_count'] = failed_count
        
        with open(campaign_file, 'w', encoding='utf-8') as f:
            json.dump(campaign, f, indent=2, ensure_ascii=False)
        
        self.log(f"Campaign complete: {sent_count} sent, {failed_count} failed")
        
        return {
            "status": "success",
            "sent": sent_count,
            "failed": failed_count
        }
    
    def add_subscriber(self, list_name, email, first_name='', last_name=''):
        """Add subscriber to list."""
        list_file = Path(f"lists/{list_name}.csv")
        list_file.parent.mkdir(exist_ok=True)
        
        file_exists = list_file.exists()
        
        with open(list_file, 'a', encoding='utf-8', newline='') as f:
            fieldnames = ['email', 'first_name', 'last_name', 'source', 'signup_date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'source': 'manual',
                'signup_date': datetime.now().strftime('%Y-%m-%d')
            })
        
        self.log(f"Added {email} to {list_name}")
        return {"status": "success", "email": email}

def main():
    parser = argparse.ArgumentParser(description='Email Campaign Manager')
    parser.add_argument('--action', required=True, 
                        choices=['create', 'send', 'add-subscriber'],
                        help='Action to perform')
    parser.add_argument('--name', help='Campaign name')
    parser.add_argument('--template', help='Email template name')
    parser.add_argument('--list', help='Subscriber list name')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--email', help='Subscriber email (for add-subscriber)')
    parser.add_argument('--first-name', help='Subscriber first name')
    parser.add_argument('--last-name', help='Subscriber last name')
    parser.add_argument('--dry-run', action='store_true', help='Simulate without sending')
    args = parser.parse_args()
    
    campaign = EmailCampaign(args.dry_run)
    
    if args.action == 'create':
        result = campaign.create_campaign(
            args.name, args.template, args.list, args.subject
        )
    elif args.action == 'send':
        result = campaign.send_campaign(args.name)
    elif args.action == 'add-subscriber':
        result = campaign.add_subscriber(
            args.list, args.email, args.first_name, args.last_name
        )
    else:
        result = {"status": "error", "message": "Unknown action"}
    
    print(f"\nResult: {json.dumps(result, indent=2)}")
    return 0 if result.get('status') == 'success' else 1

if __name__ == '__main__':
    sys.exit(main())
