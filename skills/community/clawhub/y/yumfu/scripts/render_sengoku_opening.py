#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

WORLD_PATH = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds' / 'sengoku.json'
LOAD_GAME = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'load_game.py'


def load_world():
    return json.loads(WORLD_PATH.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Render the first playable opening scene for Sengoku Chaos')
    parser.add_argument('--user-id', required=True)
    args = parser.parse_args()

    proc = subprocess.run([
        'python3', str(LOAD_GAME), '--user-id', args.user_id, '--universe', 'sengoku', '--quiet'
    ], capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        sys.exit(proc.returncode)

    payload = json.loads(proc.stdout)
    save = payload.get('data') or {}
    world = load_world()
    character = save.get('character', {})
    quest = (save.get('quests') or [{}])[0]
    intel = quest.get('intel', {})
    role = character.get('role', '乱世之人')
    faction = character.get('house', '无主之势')
    name = character.get('name', '无名之辈')
    scenario = save.get('location', '乱世开局')
    hook = intel.get('scenario_hook', '今夜有事要发生。')

    npc_sets = {
        '京都夜火': ['戴斗笠的密探', '被火光照红脸的町奉行手下', '知道密信去向的花街女使'],
        '安土酒宴': ['笑得最慢的宿将', '给主人斟酒却不抬眼的侍女', '袖中藏信的年轻使番'],
        '大坂粮乱': ['掌仓老吏', '抢米的足轻', '借机抬价的商人'],
        '堺港火枪交易': ['南蛮火枪商', '压价的大名使者', '假装路过的忍者耳目'],
        '甲斐骑阵点兵': ['老骑将', '想夺你位置的同僚', '沉默记名的军法官'],
        '对马海书': ['持海书的译官', '不肯报真名的海商', '盯着码头不说话的朝鲜来客']
    }
    role_variants = {
        '足轻头': {
            '堺港火枪交易': ['看货的老足轻', '替主家压价的旗本', '假装搬货的浪人'],
            '安土酒宴': ['带疤的宿将', '斟酒却盯着佩刀的侍女', '奉命试你胆子的使番']
        },
        '火器技师': {
            '堺港火枪交易': ['懂枪管厚薄的南蛮火枪商', '只问火药不问价的大名使者', '记炮位尺寸的忍者耳目'],
            '对马海书': ['会看海图的译官', '带火药味的海商', '盯着码头火器箱的朝鲜来客']
        },
        '花魁/名妓势力主': {
            '京都夜火': ['借火乱传话的花街女使', '嘴太严的町奉行手下', '戴斗笠却认得你的人'],
            '安土酒宴': ['故意不看你的宿将', '给主人斟酒却在听话的侍女', '袖中藏信又藏情债的使番']
        },
        '忍者头领': {
            '京都夜火': ['踩点太熟的密探', '火起前就到位的官差', '知道逃路的女使'],
            '对马海书': ['不该懂密码的译官', '报假名的海商', '看潮汐不看人的来客']
        },
        '浪人头目': {
            '大坂粮乱': ['守仓的老吏', '等你出价的足轻', '拿米抬价的商人'],
            '甲斐骑阵点兵': ['看不起浪人的老骑将', '要你替死的同僚', '只记名字不记命的军法官']
        },
        '南蛮异乡客': {
            '堺港火枪交易': ['会说半吊子葡语的火枪商', '想压你价的大名使者', '装不懂南蛮话的耳目'],
            '对马海书': ['肯替你翻错字的译官', '不报真名的海商', '看你像货而不是人的朝鲜来客']
        },
        '海商头目': {
            '堺港火枪交易': ['压着账本不松手的海商掌柜', '想包圆军火的大名使者', '盯着码头税牌的黑市耳目'],
            '对马海书': ['懂哪条海路最值钱的译官', '借船不借名的海商', '来盯货也来盯人的朝鲜客商'],
            '大坂粮乱': ['囤米等涨价的船东代理', '急着抢粮的码头足轻', '想借乱封仓的商会代表']
        }
    }
    npcs = role_variants.get(role, {}).get(scenario) or npc_sets.get(scenario, ['沉默的看客', '藏刀的使者', '比你更先听到风声的人'])

    role_openers = {
        '足轻头': '你不是席上最尊贵的人，却可能是今夜第一个见血、也第一个立功的人。',
        '浪人头目': '你没正经俸禄，只有刀、脸和一群半饥半忠的手下。谁出得起价，你就替谁把局面切开。',
        '忍者头领': '别人看见的是火和酒，你看见的是谁在借火遮脸、借酒藏话。',
        '火器技师': '别人争的是面子，你争的是谁手里有枪、谁手里有药、谁会在第一响之前先死。',
        '花魁/名妓势力主': '别人以为你卖的是笑和眼波，只有你知道，真正值钱的是谁在你面前卸下戒心。',
        '南蛮异乡客': '别人看你像外人，可乱世里最不被本地规矩绑住的，往往最先闻到钱味和血味。',
        '海商头目': '别人争城，你先算船；别人争脸，你先算账。乱世里最先涨价的，往往不是刀，而是运刀的人。'
    }

    scenario_actions = {
        '京都夜火': [
            '先追那封失踪密信的最后去向',
            '先稳住被火惊散的人流和街口',
            '先找最先喊失火的人问话'
        ],
        '安土酒宴': [
            '先盯今晚笑得最慢的宿将',
            '先盯给主人斟酒却不抬眼的侍女',
            '先查谁把刀带进了不该带刀的席位'
        ],
        '大坂粮乱': [
            '先控制仓门和账册',
            '先压住带头抢粮的足轻',
            '先把抬价的商人单独拎出来'
        ],
        '堺港火枪交易': [
            '先接近南蛮火枪商，摸清真货和底价',
            '先盯住压价的大名使者，看他背后是哪家',
            '先试探那个假装路过的忍者耳目'
        ],
        '甲斐骑阵点兵': [
            '先看谁在点兵时故意报慢半拍',
            '先盯最想把你顶下去的同僚',
            '先去和掌军法的人搭上话'
        ],
        '对马海书': [
            '先拿到那封海书的第一眼内容',
            '先稳住持海书的译官',
            '先试探那个不肯报真名的海商'
        ]
    }
    role_actions = {
        '足轻头': {
            '安土酒宴': ['先看谁在席间敢把手按在刀柄上', '先向宿将敬酒试探他认不认你', '先逼使番当场把密令念出来'],
            '甲斐骑阵点兵': ['先看谁在点兵时故意慢半拍', '先当众压住最不服你的同僚', '先去和军法官对上口风']
        },
        '火器技师': {
            '堺港火枪交易': ['先验枪管和火药，查真货底价', '先盯压价使者，看他背后是哪家', '先试探那个假装路过却总看货箱的人'],
            '对马海书': ['先看海书里有没有火器或海路条款', '先稳住懂炮位的译官', '先套那个海商的军火来路']
        },
        '花魁/名妓势力主': {
            '京都夜火': ['先找知道密信去向的女使', '先稳住嘴最严的官差手下', '先让认得你的人欠你一句真话'],
            '安土酒宴': ['先用一句话试出谁最怕你听懂他的话', '先找侍女打听谁今晚会先死', '先借酒席让袖中藏信的人自己露怯']
        },
        '忍者头领': {
            '京都夜火': ['先查火起前谁就站在该站的位置', '先沿逃路追那封密信', '先把那名知道逃路的女使扣下来'],
            '对马海书': ['先试那译官懂不懂真正的暗码', '先查海商到底替谁递信', '先从来客的靴底和盐痕判断他哪边来的']
        },
        '浪人头目': {
            '大坂粮乱': ['先把最会起哄的足轻摁住', '先逼掌仓老吏开门验账', '先让商人知道抬价要见血'],
            '甲斐骑阵点兵': ['先挑最看不起你的同僚对上', '先盯老骑将到底要不要你卖命', '先看军法官认不认你的名字']
        },
        '南蛮异乡客': {
            '堺港火枪交易': ['先用南蛮话逼火枪商说真底价', '先看使者懂不懂枪只会不会压价', '先试探那耳目到底听不听得懂你说话'],
            '对马海书': ['先看海书里哪一句最像要开战', '先让译官替你错译一句试水', '先逼海商报出真正来路']
        },
        '海商头目': {
            '堺港火枪交易': ['先看账本和交货期，算谁最急着拿货', '先盯想包圆军火的使者，抬高他的价', '先试探黑市耳目是不是已经替别人留后门'],
            '对马海书': ['先看哪条海路最赚钱也最危险', '先稳住那个最懂货路的译官', '先逼海商说清谁在背后包船'],
            '大坂粮乱': ['先算谁在借粮价做局赚钱', '先盯商会代表准备封哪一仓', '先抢下最值钱的码头账目']
        }
    }
    actions = role_actions.get(role, {}).get(scenario) or scenario_actions.get(scenario, [
        f'先接近：{npcs[0]}', f'先盯住：{npcs[1]}', f'先试探：{npcs[2]}'
    ])

    text = (
        f"{hook}\n\n"
        f"你叫{name}，身份是【{role}】，目前站在【{faction}】这一边。"
        f"{role_openers.get(role, '你已经站进了这盘会吃人的局。')}\n\n"
        f"今夜真正值得你盯的人有三个：\n"
        + "\n".join(f"- {n}" for n in npcs) +
        f"\n\n这不是介绍世界观的时候，而是你得立刻决定第一步的时候。"
    )

    choices = [
        actions[0],
        actions[1],
        actions[2],
        '按你自己的路子先开口或先动手'
    ]

    print(json.dumps({
        'success': True,
        'text': text,
        'npcs': npcs,
        'choices': choices,
        'scene_title': scenario,
        'role_flavor': role_openers.get(role),
        'player_opening_message': text + '\n\n## 你先怎么入局？\nA. ' + choices[0] + '\nB. ' + choices[1] + '\nC. ' + choices[2] + '\nD. ' + choices[3],
        'image_prompt': f"Sengoku Chaos first playable scene, {scenario}, {hook}, protagonist {name}, role {role}, faction {faction}, three dangerous figures in one room, Japanese ukiyo-e woodblock print style, bold ink outlines, textured washi paper, flat layered colors, samurai intrigue, torchlight, lacquer armor, smoke and tension"
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
