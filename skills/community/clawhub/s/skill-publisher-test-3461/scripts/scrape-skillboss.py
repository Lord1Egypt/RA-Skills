#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
import re

async def main():
    print('🚀 启动浏览器...')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        print('📄 访问 SkillBoss.co/skills...')
        
        await page.goto('https://www.skillboss.co/skills', 
                       wait_until='networkidle', 
                       timeout=30000)
        
        print('⏳ 等待内容加载...')
        await page.wait_for_timeout(5000)
        
        # 滚动加载更多
        print('📜 滚动加载...')
        for i in range(5):
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await page.wait_for_timeout(2000)
            print(f'  第 {i+1}/5 次滚动')
        
        await page.screenshot(path='/tmp/skillboss-skills-page.png', full_page=True)
        
        print('')
        print('🔍 提取 skills...')
        
        # 获取所有链接
        links = await page.evaluate('''() => {
            const hrefs = [];
            document.querySelectorAll('a[href]').forEach(el => {
                hrefs.push(el.href);
            });
            return hrefs;
        }''')
        
        # 提取 skill IDs
        skill_ids = set()
        for link in links:
            match = re.search(r'/skills/([a-z0-9-]+)', link)
            if match:
                skill_id = match.group(1)
                # 过滤掉太短或明显不是 skill 的
                if len(skill_id) >= 3 and skill_id not in ['new', 'edit', 'create']:
                    skill_ids.add(skill_id)
        
        # 也从页面内容中搜索
        content = await page.content()
        content_matches = re.findall(r'href="/skills/([a-z0-9-]+)"', content)
        for skill_id in content_matches:
            if len(skill_id) >= 3:
                skill_ids.add(skill_id)
        
        skill_ids = sorted(skill_ids)
        
        if skill_ids:
            print(f'🎯 找到 {len(skill_ids)} 个 skills!')
            print('')
            
            for i, skill_id in enumerate(skill_ids[:30], 1):
                print(f'  {i:2d}. {skill_id}')
            
            if len(skill_ids) > 30:
                print(f'  ... 还有 {len(skill_ids) - 30} 个')
            
            # 保存
            with open('/tmp/skillboss-all-skills.txt', 'w') as f:
                f.write('\n'.join(skill_ids))
            
            print('')
            print(f'💾 全部 {len(skill_ids)} 个已保存到 /tmp/skillboss-all-skills.txt')
        else:
            print('⚠️  未找到 skills')
            print(f'  页面长度: {len(content)}')
            print(f'  链接数量: {len(links)}')
        
        await browser.close()
        print('')
        print('🏁 完成！')

if __name__ == '__main__':
    asyncio.run(main())
