#!/usr/bin/env python3
# UZI Investor Panel: 20 rules (Buffett ROE>15 +10, Lynch growth>20 +8, HK游资 vol>1.5 +5)
import sys, json
# Self-contained: mock ROE/growth/vol from stdin or hardcode for test
fund = {'roe': 22, 'revenue_growth': 13, 'volume_ratio': 1.0}
votes = []
if fund.get('roe', 0) > 15: votes.append('+10 Buffett ROE')
if fund.get('revenue_growth', 0) > 20: votes.append('+8 Lynch growth')
if fund.get('volume_ratio', 0) > 1.5: votes.append('+5 HK游资 vol')
avg = sum(int(x[1:]) for x in votes) / max(1, len(votes)) if votes else 0
print(json.dumps({'panel_avg': avg, 'votes': votes}))

ticker = sys.argv[1]
fund = get_fundamentals(ticker)

votes = []
if fund.get('roe', 0) > 15: votes.append('+10 Buffett ROE')
if fund.get('revenue_growth', 0) > 20: votes.append('+8 Lynch growth')
if fund.get('volume_ratio', 0) > 1.5: votes.append('+5 HK游资 vol')

avg = sum(map(lambda x: int(x[1:]), votes)) / max(1, len(votes)) if votes else 0
print(json.dumps({'ticker': ticker, 'panel_avg': avg, 'votes': votes}))
