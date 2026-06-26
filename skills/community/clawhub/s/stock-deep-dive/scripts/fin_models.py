#!/usr/bin/env python3
# UZI Fin Models: DCF WACC6.5% + Comps PE/PB
import sys
ticker = sys.argv[1]
# Mock DCF
fcf_growth = 0.15  # from fund
fcf = 10  # mock
wacc = 0.065
dcf_target = fcf * (1 + fcf_growth) / wacc * 0.5  # simplified
comps_pe = 25
print(f'{ticker} DCF ${dcf_target:.0f} | Comps PE {comps_pe}x')
