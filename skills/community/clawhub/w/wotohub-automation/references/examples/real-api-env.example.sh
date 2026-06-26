#!/usr/bin/env bash
# Fill only the missing token / campaign values, then:
# source references/examples/real-api-env.example.sh
#
# Safety note:
# - This file is a fixture template, not a production-ready env file.
# - Review every ID before use.
# - Do not copy sample/test IDs into production blindly.

export WOTOHUB_API_KEY='REPLACE_WITH_REAL_API_KEY'
export WOTOHUB_INVALID_API_KEY='REPLACE_WITH_INVALID_API_KEY'
export WOTOHUB_CAMPAIGN_ID='REPLACE_WITH_REAL_CAMPAIGN_ID'
export WOTOHUB_SENDER_NAME='Validation Sender'

export WOTOHUB_CONTACTED_BLOGGER_ID_1='6749527274875618310tt6fd6'
export WOTOHUB_CONTACTED_BLOGGER_ID_2='6766236235897914374tt6652'
export WOTOHUB_CONTACTED_BLOGGER_IDS='6749527274875618310tt6fd6,6766236235897914374tt6652'

export WOTOHUB_LOW_RISK_REPLY_ID='17876114'
export WOTOHUB_LOW_RISK_CHAT_ID='chat_69c4d882e4b04e1c55593d39'
export WOTOHUB_LOW_RISK_BLOGGER_ID='6766236235897914374tt6652'

export WOTOHUB_HIGH_RISK_REPLY_ID='17884930'
export WOTOHUB_HIGH_RISK_CHAT_ID='chat_69c5e3cbe4b04e1c555efab2'
export WOTOHUB_HIGH_RISK_BLOGGER_ID='6749527274875618310tt6fd6'
