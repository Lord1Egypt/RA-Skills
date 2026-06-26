#!/bin/bash
# Example: Workflow menu with multiple options
# Demonstrates multi-row layout and emoji usage
#
# ⚠️ SECURITY WARNING:
# - Replace YOUR_CHAT_ID with your actual Telegram chat ID
# - Review this script before running
# - Only run in trusted environments
# - Requires openclaw CLI configured with Telegram bot token

TARGET="telegram:YOUR_CHAT_ID"  # ⚠️ REPLACE WITH YOUR CHAT ID

echo "Sending workflow menu..."

openclaw message send \
    --target "$TARGET" \
    --message "What would you like to do today?" \
    --buttons '[[{"text": "🎬 AI Search", "callback_data": "wf_ai_search"}, {"text": "📺 Follow List", "callback_data": "wf_follow_list"}], [{"text": "🔍 Free Search", "callback_data": "wf_free_search"}, {"text": "🎲 Random", "callback_data": "wf_random"}], [{"text": "📊 Metrics", "callback_data": "wf_metrics"}, {"text": "📅 Meetings", "callback_data": "wf_meetings"}]]'

echo ""
echo "This creates a 3x2 grid of workflow options"
echo ""
echo "Button callbacks to handle:"
echo "  - wf_ai_search: Trigger AI search workflow"
echo "  - wf_follow_list: Show followed channels"
echo "  - wf_free_search: Free-form search"
echo "  - wf_random: Random selection"
echo "  - wf_metrics: Show metrics dashboard"
echo "  - wf_meetings: Calendar view"
echo ""
echo "Best practice: Use descriptive callback_data (not btn1, btn2, etc.)"
