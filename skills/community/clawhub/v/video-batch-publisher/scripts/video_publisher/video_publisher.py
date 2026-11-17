import pandas as pd
import os
import sys
import argparse
import logging
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from core.log_manager import setup_logger, PublisherLogger
logger = setup_logger("VideoPublisher", "video_publish")

from core.config_manager import (
    load_global_config,
    get_browser_config,
    ensure_output_directories,
    config_manager
)
from core.excel_handler import ExcelHandler
from core.constants import (
    STATUS_PENDING, COL_NAME, COL_PUBLISH_DATE, PUBLISH_TIME_FORMAT
)
from browser import (
    init_browser,
    get_page,
    get_platform_page,
    close_browser,
    create_douyin_publisher,
    create_bilibili_publisher,
    create_kuaishou_publisher,
    create_weixin_publisher,
    create_xiaohongshu_publisher
)

PUBLISHER_MAP = {
    "抖音": create_douyin_publisher,
    "视频号": create_weixin_publisher,
    "快手": create_kuaishou_publisher,
    "B站": create_bilibili_publisher,
    "小红书": create_xiaohongshu_publisher
}

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="短视频批量发布工具")
    parser.add_argument('--content-type', type=str, default='idiom', help='内容类型')
    parser.add_argument('--excel-path', type=str, required=True, help='Excel文件路径')
    parser.add_argument('--input-dir', type=str, required=True, help='输入目录')
    parser.add_argument('--platforms', type=str, required=True, help='发布平台列表，逗号分隔')
    parser.add_argument('--publish-data', type=str, default=None, help='用户编辑的发布数据JSON文件路径')
    
    return parser.parse_args()

def get_publish_strategy(publish_date_str, time_format=PUBLISH_TIME_FORMAT):
    """判断发布策略：立即发布/定时发布
    
    外部只做基础的时间格式化：
    - 如果只有年月日，补充默认时间 20:00
    - 统一返回 yyyy-MM-dd HH:mm 格式的时间字符串
    各平台内部根据自己的需求再做解析处理
    
    支持多种日期格式：
    - 2026-07-02 18:00
    - 2026/7/2 18:00
    - 2026/7/2
    - 2026-07-02
    """
    try:
        if not publish_date_str or publish_date_str.strip() in ['', 'nan', 'None']:
            return {"type": "immediate", "time": None}
        
        publish_date_str = str(publish_date_str).strip()
        
        # 如果只有年月日，补充默认时间 20:00
        if len(publish_date_str.split()) == 1:
            publish_date_str += " 20:00"
        
        # 解析时间，确保格式正确
        time_parts = publish_date_str.split()
        if len(time_parts) == 2:
            date_part = time_parts[0]
            time_part = time_parts[1]
            
            # 处理日期部分：支持 / 和 - 分隔符
            if '/' in date_part:
                date_part = date_part.replace('/', '-')
            
            # 处理单数字月份和日期
            date_components = date_part.split('-')
            if len(date_components) == 3:
                year, month, day = date_components
                month = month.zfill(2)
                day = day.zfill(2)
                date_part = f"{year}-{month}-{day}"
            
            # 处理时间部分：去除秒（如果有）
            if len(time_part.split(':')) == 3:
                time_part = ':'.join(time_part.split(':')[:2])
            
            publish_date_str = f"{date_part} {time_part}"
        
        # 验证时间是否合法
        from datetime import datetime
        publish_time = datetime.strptime(publish_date_str, "%Y-%m-%d %H:%M")
        now = datetime.now()
        
        if publish_time > now:
            return {
                "type": "schedule",
                "time": publish_date_str  # 统一格式：yyyy-MM-dd HH:mm
            }
        else:
            return {"type": "immediate", "time": None}
    
    except Exception as e:
        logger.error(f"解析发布时间失败：{str(e)}")
        return {"type": "immediate", "time": None}

import re

# 需要去除的特殊字符列表（这些字符在文件名中通常不存在）
# 注意：Unicode中有多个类似的"点"字符，包括：
# · (U+00B7) 间隔号/Middle Dot
# · (U+2027) 中间点/Interpunct  
# · (U+002E) 句点/Period
# 这里使用通配符匹配所有可能的点字符和其他特殊字符
REMOVE_CHARS_REGEX = re.compile(r'[\u00B7\u2027\u002E·、，。！？：；""''""《》（）【】<>「」『』〔〕—…～·]')

def find_local_media(row, input_dir, content_type):
    """匹配本地视频和封面文件（支持序号+名称模糊匹配）
    
    特殊字符处理：使用正则表达式去除标题中的特殊字符，
    因为实际文件名中可能没有这些字符。
    
    需要去除的特殊字符包括：
    - 标点符号：，。！？：；""''《》（）【】
    - 特殊符号：··、—…～
    - 其他符号：「」『』〔〕<>
    """
    try:
        name = str(row[COL_NAME]).strip()
        sn = str(row.get('序号', '')).strip()
        
        # 使用正则表达式去除所有特殊字符
        clean_name = REMOVE_CHARS_REGEX.sub('', name)
        
        possible_video_names = []
        possible_video_names.append(f"{name}.mp4")
        possible_video_names.append(f"{clean_name}.mp4")
        
        if sn:
            possible_video_names.append(f"{sn}{name}.mp4")
            possible_video_names.append(f"{sn}{clean_name}.mp4")
            possible_video_names.append(f"{int(sn):03d}{name}.mp4")
            possible_video_names.append(f"{int(sn):03d}{clean_name}.mp4")
            possible_video_names.append(f"{int(sn):04d}{name}.mp4")
            possible_video_names.append(f"{int(sn):04d}{clean_name}.mp4")
            possible_video_names.append(f"{sn} {name}.mp4")
            possible_video_names.append(f"{sn} {clean_name}.mp4")
        
        video_path = ""
        for video_name in possible_video_names:
            candidate_path = os.path.join(input_dir, video_name)
            if os.path.exists(candidate_path):
                video_path = candidate_path
                break
        
        if not video_path:
            for filename in os.listdir(input_dir):
                if filename.endswith('.mp4'):
                    # 对文件名也进行特殊字符清理，确保匹配更准确
                    clean_filename = REMOVE_CHARS_REGEX.sub('', filename)
                    base_name = os.path.splitext(filename)[0]
                    clean_base_name = os.path.splitext(clean_filename)[0]
                    
                    if (name in filename or clean_name in filename or
                        name in clean_filename or clean_name in clean_filename or
                        base_name in name or clean_base_name in name):
                        video_path = os.path.join(input_dir, filename)
                        logger.info(f"模糊匹配视频文件：{filename}")
                        break
        
        if not video_path:
            raise FileNotFoundError(f"视频文件不存在，尝试过的模式：{possible_video_names}")
        
        actual_name = os.path.splitext(os.path.basename(video_path))[0]
        cover_dir = os.path.join(input_dir, actual_name)
        
        cover_horizontal = ""
        cover_vertical = ""
        missing_covers = []
        
        cover_config = config_manager.get_type_covers(content_type)
        cover_horizontal_name = cover_config.get("horizontal", "")
        cover_vertical_name = cover_config.get("vertical", "")
        
        if cover_horizontal_name:
            cover_horizontal = os.path.join(cover_dir, cover_horizontal_name)
        if cover_vertical_name:
            cover_vertical = os.path.join(cover_dir, cover_vertical_name)
        
        if not os.path.exists(cover_dir) and name != actual_name:
            alt_cover_dir = os.path.join(input_dir, name)
            if os.path.exists(alt_cover_dir):
                cover_dir = alt_cover_dir
                if cover_horizontal_name:
                    cover_horizontal = os.path.join(cover_dir, cover_horizontal_name)
                if cover_vertical_name:
                    cover_vertical = os.path.join(cover_dir, cover_vertical_name)
        
        if cover_horizontal_name and not os.path.exists(cover_horizontal):
            missing_covers.append(f"横屏封面 {cover_horizontal}")
        if cover_vertical_name and not os.path.exists(cover_vertical):
            missing_covers.append(f"竖屏封面 {cover_vertical}")
        
        media_info = {
            "video_path": video_path,
            "cover_horizontal": cover_horizontal if os.path.exists(cover_horizontal) else "",
            "cover_vertical": cover_vertical if os.path.exists(cover_vertical) else "",
            "name": name,
            "actual_name": actual_name,
            "missing_covers": missing_covers,
            "cover_dir": cover_dir,
            "content_type": content_type
        }
        
        if missing_covers:
            logger.warning(f"封面文件缺失：{name} - {', '.join(missing_covers)}")
        
        logger.info(f"文件匹配成功：{video_path}")
        return media_info
    
    except Exception as e:
        logger.error(f"文件匹配失败：{str(e)}")
        raise

def get_platform_cover(media_info, platform, content_type):
    """根据平台和内容类型获取封面路径"""
    cover_config = config_manager.get_type_covers(content_type)
    has_horizontal = "horizontal" in cover_config
    has_vertical = "vertical" in cover_config
    
    if platform == "抖音":
        result = {}
        if has_horizontal:
            result["horizontal"] = media_info.get("cover_horizontal", "")
        if has_vertical:
            result["vertical"] = media_info.get("cover_vertical", "")
        return result
    else:
        if has_horizontal:
            return {"horizontal": media_info.get("cover_horizontal", "")}
        elif has_vertical:
            return {"vertical": media_info.get("cover_vertical", "")}
        return {}

def create_publisher_for_platform(platform, browser_config, force_new=False):
    """为指定平台创建发布器（复用已有页面）
    
    Args:
        platform: 平台名称
        browser_config: 浏览器配置
        force_new: 是否强制重新创建页面（用于批量发布时清理上一次发布后的页面状态）
    
    Returns:
        Publisher: 发布器实例
    """
    try:
        if platform not in PUBLISHER_MAP:
            logger.error(f"不支持的平台：{platform}")
            return None
        
        page = get_platform_page(platform, force_new=force_new)
        create_publisher = PUBLISHER_MAP[platform]
        return create_publisher(page, browser_config)
    
    except Exception as e:
        logger.error(f"创建{platform}发布器失败：{str(e)}")
        return None

def check_platform_login_status(platform):
    """检查平台登录状态（不切换到前台，避免频繁切换tab）"""
    from browser.browser_singleton import BrowserSingleton
    
    try:
        browser = BrowserSingleton()
        return browser.is_login_state_valid(platform, bring_to_front=False)
    except Exception as e:
        logger.warning(f"检查{platform}登录状态失败：{str(e)}")
        return True

def publish_to_platform(media_info, platform, content, publish_strategy, browser_config):
    """发布到指定平台（使用平台独立的标签页）- 原有串行方式，兼容旧调用
    
    每个平台使用独立的浏览器标签页，互不干扰，登录状态保持。
    发布前自动检测当前页面，如果不是发布页则自动导航过去。
    """
    try:
        publisher = create_publisher_for_platform(platform, browser_config)
        if not publisher:
            return False, "创建发布器失败"
        
        return publisher.publish(media_info, content, publish_strategy)
    
    except Exception as e:
        logger.error(f"{platform}发布失败：{str(e)}")
        return False, str(e)

def main():
    """主发布流程"""
    # 收集发布结果
    publish_results = []
    
    try:
        args = parse_args()
        excel_path = args.excel_path
        input_dir = args.input_dir
        content_type = args.content_type
        target_platforms = [p.strip() for p in args.platforms.split(',')]
        publish_data_path = args.publish_data
        
        logger.info(f"=== 开始发布任务 ===")
        logger.info(f"内容类型: {content_type}")
        logger.info(f"Excel路径: {excel_path}")
        logger.info(f"输入目录: {input_dir}")
        logger.info(f"目标平台: {target_platforms}")
        
        load_global_config()
        browser_config = get_browser_config()
        browser_config["logger"] = logger
        ensure_output_directories()
        
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel文件不存在：{excel_path}")
        
        publish_items = None
        publish_mode = "publish"
        if publish_data_path and os.path.exists(publish_data_path):
            import json
            with open(publish_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                publish_items = data.get('publish_items', [])
                publish_mode = data.get('publish_mode', 'publish')
            logger.info(f"加载用户编辑的发布数据：{len(publish_items)} 条")
            logger.info(f"发布模式: {'正式发布' if publish_mode == 'publish' else '存草稿'}")
        
        init_browser(browser_config)
        logger.info("浏览器初始化完成")
        
        handler = ExcelHandler(excel_path)
        handler.read_excel()
        
        if publish_items:
            pending_data = publish_items
        else:
            pending_df = handler.get_pending_rows(target_platforms)
            pending_data = []
            for _, row in pending_df.iterrows():
                name_value = row.get(COL_NAME)
                publish_date_value = row.get(COL_PUBLISH_DATE)
                
                pending_platforms = []
                for p in target_platforms:
                    if p in row:
                        p_value = row[p]
                        if p_value == STATUS_PENDING or pd.isna(p_value):
                            pending_platforms.append(p)
                
                pending_data.append({
                    'index': int(row.name),
                    'sn': str(row.get('序号', '')).strip(),
                    'name': str(name_value).strip() if pd.notna(name_value) else "",
                    'publish_date': str(publish_date_value).strip() if pd.notna(publish_date_value) else "",
                    'video_path': "",
                    'platforms': pending_platforms,
                    'cover_vertical': "",
                    'cover_horizontal': ""
                })
        
        logger.info(f"共读取到 {len(pending_data)} 条待发布视频数据")
        
        # 调试：打印所有待发布视频
        #for i, item in enumerate(pending_data):
        #    logger.info(f"待发布视频 {i+1}: name={item.get('name')}, platforms={item.get('platforms')}")
        
        if len(pending_data) == 0:
            logger.info("没有待发布的视频")
            close_browser()
            return
        
        platform_videos = {}
        for platform in target_platforms:
            platform_videos[platform] = []
        
        for item in pending_data:
            original_index = item['index']
            name = item['name']
            
            media_info = {
                'video_path': item.get('video_path', ''),
                'cover_vertical': item.get('cover_vertical', ''),
                'cover_horizontal': item.get('cover_horizontal', ''),
                'name': name,
                'actual_name': name,
                'missing_covers': [],
                'cover_dir': '',
                'content_type': content_type
            }
            
            if not media_info['video_path']:
                row_data = {
                    '序号': item.get('sn', ''),
                    COL_NAME: name
                }
                media_info = find_local_media(row_data, input_dir, content_type)
                media_info['content_type'] = content_type
            
            parsed_date = handler.parse_publish_date(original_index)
            publish_date_str = parsed_date.get('datetime', item.get('publish_date', ""))
            publish_strategy = get_publish_strategy(publish_date_str)
            publish_strategy['mode'] = publish_mode
            
            to_publish = item.get('platforms', [])
            if not to_publish:
                row = handler.df.loc[original_index]
                to_publish = []
                for p in target_platforms:
                    if p in row:
                        p_value = row[p]
                        if p_value == STATUS_PENDING or pd.isna(p_value):
                            to_publish.append(p)
            else:
                to_publish = [p for p in to_publish if p in target_platforms]
            
            for platform in to_publish:
                title_desc = handler.get_title_description(original_index, platform)
                platform_videos[platform].append({
                    'original_index': original_index,
                    'name': name,
                    'sn': item.get('sn', ''),
                    'media_info': media_info,
                    'publish_strategy': publish_strategy,
                    'content': title_desc
                })
        
        for platform in target_platforms:
            videos = platform_videos.get(platform, [])
            if not videos:
                continue
            
            logger.info(f"\n{'='*50}")
            logger.info(f"=== 开始发布 {platform} 平台 ===")
            logger.info(f"待发布视频数量: {len(videos)}")
            logger.info(f"{'='*50}")
            
            login_valid = check_platform_login_status(platform)
            if not login_valid:
                logger.warning(f"{platform} 未登录，请在浏览器中完成登录...")
                get_platform_page(platform)
                
                while not check_platform_login_status(platform):
                    logger.info(f"等待 {platform} 登录（3秒后重试）")
                    import time
                    time.sleep(3)
                
                logger.info(f"{platform} 登录成功")
            
            publisher = create_publisher_for_platform(platform, browser_config)
            if not publisher:
                logger.error(f"创建 {platform} 发布器失败")
                for video in videos:
                    publish_results.append({
                        'video_name': video['name'],
                        'platform': platform,
                        'status': '失败',
                        'message': '创建发布器失败',
                        'cover_status': 'N/A',
                        'submit_mode': publish_mode,
                        'publish_time': video['publish_strategy'].get('time') or '立即'
                    })
                continue
            
            for video_idx, video in enumerate(videos):
                original_index = video['original_index']
                name = video['name']
                media_info = video['media_info']
                publish_strategy = video['publish_strategy']
                content = video['content']
                
                logger.info(f"\n--- {platform} 第{video_idx + 1}/{len(videos)}个视频: {name} ---")
                logger.info(f"原始索引: {original_index}, 序号: {video['sn']}")
                
                try:
                    if media_info.get('missing_covers'):
                        missing_note = "; ".join(media_info['missing_covers'])
                        logger.warning(f"第{original_index + 1}行 封面状态 → 封面缺失: {missing_note}")
                    
                    if not media_info.get('video_path') or not os.path.exists(media_info['video_path']):
                        logger.error(f"视频文件不存在: {media_info.get('video_path')}")
                        publish_results.append({
                            'video_name': name,
                            'platform': platform,
                            'status': '失败',
                            'message': '视频文件不存在',
                            'cover_status': 'N/A',
                            'submit_mode': publish_mode,
                            'publish_time': publish_strategy.get('time') or '立即'
                        })
                        continue
                    
                    cover_path = get_platform_cover(media_info, platform, content_type)
                    media_info['publish_cover'] = cover_path
                    
                    logger.info(f"\n阶段1: 启动视频上传")
                    success = publisher.start_video_upload(media_info['video_path'])
                    if not success:
                        logger.warning(f"{platform} 视频上传启动失败")
                        publish_results.append({
                            'video_name': name,
                            'platform': platform,
                            'status': '失败',
                            'message': '视频上传启动失败',
                            'cover_status': 'N/A',
                            'submit_mode': publish_mode,
                            'publish_time': publish_strategy.get('time') or '立即'
                        })
                        continue
                    logger.info(f"{platform} 视频上传已启动")
                    
                    logger.info(f"\n阶段2: 填写内容")
                    success = publisher.fill_content_only(media_info, content, publish_strategy)
                    if not success:
                        logger.warning(f"{platform} 内容填写失败")
                    
                    logger.info(f"\n阶段3: 完成发布")
                    success, message = publisher.complete_publish(media_info, content, publish_strategy)
                    
                    logger.info(f"第{original_index + 1}行 {platform} → {'成功' if success else '失败'}{f' - {message}' if message else ''}")
                    if success:
                        logger.info(f"第{original_index + 1}行 发布日期 → {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                    
                    cover_status = '成功' if media_info.get('cover_horizontal') or media_info.get('cover_vertical') else '缺失'
                    publish_results.append({
                        'video_name': name,
                        'platform': platform,
                        'status': '成功' if success else '失败',
                        'message': message,
                        'cover_status': cover_status,
                        'submit_mode': publish_mode,
                        'publish_time': publish_strategy.get('time') or '立即'
                    })
                    
                except Exception as e:
                    logger.error(f"处理视频 {name} 失败：{str(e)}")
                    publish_results.append({
                        'video_name': name,
                        'platform': platform,
                        'status': '失败',
                        'message': str(e),
                        'cover_status': 'N/A',
                        'submit_mode': publish_mode,
                        'publish_time': publish_strategy.get('time') or '立即'
                    })
                    continue
            
            logger.info(f"\n=== {platform} 平台发布完成 ===")
        
        logger.info("\n===== 发布流程全部完成 =====")
        
        # 记录发布结果日志
        if publish_results:
            platform_str = "_".join(target_platforms)[:20]
            publisher_logger = PublisherLogger(platform=platform_str, content_type=content_type)
            
            success_count = sum(1 for r in publish_results if r['status'] == '成功')
            fail_count = sum(1 for r in publish_results if r['status'] == '失败')
            failed_videos = [r['video_name'] for r in publish_results if r['status'] == '失败']
            
            for result in publish_results:
                if result['status'] == '成功':
                    publisher_logger.log_publish_success(
                        result['video_name'], 
                        submit_mode='正式发布' if result['submit_mode'] == 'publish' else '存草稿',
                        schedule_time=result.get('publish_time', '立即'),
                        cover_status=result.get('cover_status', '成功')
                    )
                else:
                    publisher_logger.log_publish_failure(
                        result['video_name'],
                        result['message'],
                        submit_mode='正式发布' if result['submit_mode'] == 'publish' else '存草稿',
                        schedule_time=result.get('publish_time', '立即'),
                        cover_status=result.get('cover_status', 'N/A')
                    )
            
            # 批量日志统计
            publisher_logger.log_batch_summary(
                total_count=len(publish_results),
                success_count=success_count,
                fail_count=fail_count,
                failed_videos=failed_videos
            )
            
            logger.info(f"发布结果日志已保存到: {publisher_logger.get_log_file_path()}")
        
        # 输出结果到JSON文件供GUI展示
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        result_file = os.path.join(output_dir, f"publish_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        import json
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump({
                'results': publish_results,
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_count': len(publish_results),
                'success_count': sum(1 for r in publish_results if r['status'] == '成功'),
                'fail_count': sum(1 for r in publish_results if r['status'] == '失败')
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"发布结果已保存到: {result_file}")
        
    except Exception as e:
        logger.error(f"主流程失败：{str(e)}")
        raise
    
    finally:
        # 关闭浏览器（如配置 debug_keep_browser=true 则不关闭，由配置控制）
        try:
            close_browser()
            logger.info("=" * 60)
            logger.info("所有任务执行完毕，浏览器已关闭")
            logger.info("=" * 60)
        except Exception as e:
            logger.warning(f"关闭浏览器失败: {str(e)}")

if __name__ == "__main__":
    main()