#!/usr/bin/env node
/**
 * Quick Music — 轻量快捷找歌
 * 用法: node quick-music.js "关键词" [--page 1] [--limit 10] [--play N]
 */

import { parseArgs } from "node:util";

const SEARCH_API = "https://kw-api.cenguigui.cn/";
const PLAY_API = "https://api.xcvts.cn/api/music/migu";

const HEADERS = {
  accept: "*/*",
  "accept-language": "zh-CN,zh;q=0.9",
  "cache-control": "no-cache",
  pragma: "no-cache",
  "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": '"macOS"',
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "cross-site",
  "user-agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
};

async function searchSongs(name, page = 1, limit = 10) {
  const url = `${SEARCH_API}?name=${encodeURIComponent(name)}&page=${page}&limit=${limit}`;
  const res = await fetch(url, { headers: HEADERS });
  if (!res.ok) throw new Error(`搜索失败: ${res.status} ${res.statusText}`);
  return res.json();
}

async function getPlayUrl(keyword, index = 1, num = 10) {
  const url = `${PLAY_API}?gm=${encodeURIComponent(keyword)}&n=${index}&num=${num}&type=json`;
  const res = await fetch(url, { headers: HEADERS });
  if (!res.ok) throw new Error(`获取播放链接失败: ${res.status} ${res.statusText}`);
  return res.json();
}

function printSongList(data) {
  const songs = data?.data || data?.songs || data;
  if (!Array.isArray(songs) || songs.length === 0) {
    console.log("未找到相关歌曲");
    return [];
  }

  console.log("\n🎵 搜索结果:\n");
  console.log("序号  歌名                          歌手");
  console.log("----  ----------------------------  --------------------");

  songs.forEach((song, i) => {
    const name = (song.name || song.song || song.title || "未知").padEnd(28);
    const artist = song.artist || song.singer || song.author || "未知";
    console.log(`${String(i + 1).padStart(4)}  ${name}  ${artist}`);
  });

  console.log(`\n共 ${songs.length} 首，使用 --play N 获取播放链接\n`);
  return songs;
}

async function main() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      page:  { type: "string", short: "p", default: "1" },
      limit: { type: "string", short: "l", default: "10" },
      play:  { type: "string", short: "n" },
    },
  });

  const keyword = positionals[0];
  if (!keyword) {
    console.error("用法: node music-search.js \"歌名或歌手\" [--page 1] [--limit 10] [--play N]");
    process.exit(1);
  }

  const page = parseInt(values.page, 10);
  const limit = parseInt(values.limit, 10);

  try {
    if (values.play) {
      // 直接获取播放链接
      const index = parseInt(values.play, 10);
      console.log(`\n🔍 正在获取「${keyword}」第 ${index} 首的播放链接...\n`);
      const data = await getPlayUrl(keyword, index, limit);

      const playUrl = data?.music_url || data?.url || data?.data?.music_url || data?.data?.url;
      const title = data?.title || data?.data?.title || data?.song || "";
      const artist = data?.singer || data?.artist || data?.data?.singer || "";
      const cover = data?.cover || data?.data?.cover || "";
      const lrc = data?.lrc_url || data?.data?.lrc_url || "";
      const link = data?.link || data?.data?.link || "";

      if (playUrl) {
        console.log(`🎶 ${title} - ${artist}`);
        console.log(`🔗 播放链接: ${playUrl}`);
        if (link) console.log(`🌐 详情页: ${link}`);
        if (cover) console.log(`🖼️  封面: ${cover}`);
        if (lrc) console.log(`📝 歌词: ${lrc}`);
        console.log();
      } else {
        console.log("未找到播放链接，返回数据:");
        console.log(JSON.stringify(data, null, 2));
      }
    } else {
      // 搜索歌曲列表
      console.log(`\n🔍 正在搜索「${keyword}」(第 ${page} 页, 每页 ${limit} 首)...`);
      const data = await searchSongs(keyword, page, limit);
      printSongList(data);
    }
  } catch (e) {
    console.error(`❌ ${e.message}`);
    process.exit(1);
  }
}

main();
