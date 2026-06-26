#!/usr/bin/env python3
import asyncio
from techmanpy import connect_sct

async def stop_and_move():
    async with connect_sct(robot_ip='192.168.1.13', conn_timeout=10) as conn:
        print('[INFO] Stopping previous motion...')
        await conn.stop_motion()
        await asyncio.sleep(1)
        
        print('[INFO] Moving X -150mm...')
        await conn.move_to_relative_point_line([-150, 0, 0, 0, 0, 0], 0.2, 50)
        print('[OK] X -150mm command sent!')

asyncio.run(stop_and_move())
