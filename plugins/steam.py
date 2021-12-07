import nonebot
from nonebot import on_command, CommandSession, permission as perm
import urllib
import urllib.parse
import urllib.request
import json
import sys
import os
import ssl
import re
import platform
import requests
from requests.sessions import Session, session
ssl._create_default_https_context = ssl._create_unverified_context
CONFIG = ["{\"request_cookies\":\"\",\"apikey\":\"\"}"]
#读取配置文件
if os.path.exists("steambot_config.json") == False:
    print("steambot_config.json not found. Creating...")
    with open("steambot_config.json", mode="w") as newconf:
        newconf.writelines(CONFIG)
try:
    with open("steambot_config.json", encoding="utf-8") as conf:
        a = json.load(conf)
        request_cookies = a['request_cookies']
        apikey = a['apikey']
except:
    print("Unable to read steambot_config.json.")
    pass
def get_app_info(appids):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
    add = urllib.request.Request(f"https://store.steampowered.com/api/appdetails/?appids={appids}",headers=headers)
    resp = json.loads(urllib.request.urlopen(url=add).read().decode('utf-8'))
    return resp
def get_user_info(steamid):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
    add = urllib.request.Request(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apikey}&steamids={steamid}",headers=headers)
    resp = json.loads(urllib.request.urlopen(url=add).read().decode('utf-8'))
    return resp
def get_owned_games(steamid):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
    add = urllib.request.Request(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apikey}&steamid={steamid}&include_appinfo=1&include_played_free_games=1",headers=headers)
    resp = json.loads(urllib.request.urlopen(url=add).read().decode('utf-8'))
    return resp
def get_dymanic_info(steamid):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Cookie': request_cookies}
    add = urllib.request.Request(f"https://store.steampowered.com/dynamicstore/userdata/?id={steamid}&cc=CN",headers=headers)
    resp = json.loads(urllib.request.urlopen(url=add).read().decode('utf-8'))
    return resp
def get_wishlist(steamid):
    headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'}
    add = urllib.request.Request(f"https://store.steampowered.com/wishlist/profiles/{steamid}/wishlistdata/?p=0&v=1",headers=headers)
    resp = json.loads(urllib.request.urlopen(url=add).read().decode('utf-8'))
    return resp
def lts(list):
    string = ""
    count = 1
    for i in list:
        
        if count == len(list):
            string += i
        else:
            string += i + ","
        count = count + 1
    return string
@on_command('appinfo', aliases=('app'), only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入appid')
        return
    resp = get_app_info(arg)
    try:
        resp1 = resp[str(arg)]['data']
        developers = resp1['developers']
        publishers = resp1['publishers']
        price = resp1['price_overview']["final_formatted"]
        await session.send(f"应用名称：{resp1['name']}\n应用类型：{resp1['type']}\n短简介：{resp1['short_description']}\n开发者：{lts(developers)}\n发行者：{lts(publishers)}\n价格：{price}\nURL：https://store.steampowered.com/app/{arg}")
        header_image_url = resp1["header_image"]
        header_image_url = header_image_url.replace("cdn.akamai.steamstatic.com","media.st.dl.pinyuncloud.com")
        await session.send(f"[CQ:image,file={header_image_url}]")
    except:
        await session.send('没有找到相关应用')
@on_command('owned', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入搜索内容')
        return
    try:
        resp = get_owned_games(arg)
    except:
        await session.send('发生错误')
        return
    if resp['response']['game_count'] == 0:
        await session.send('没有找到相关游戏')
        return
    appids = []
    games = []
    for i in resp['response']['games']:

        games.append(f"{i['name']}({i['appid']})")
    # for i in appids:
    #     try:
    #         resp = get_app_info(i)
    #     except:
    #         games.append(f"未知({i})")
    #     try:
    #         resp = resp[str(i)]['data']
    #         games.append(f"{resp['name']}({i})")
    #     except:
    #         pass
    username = get_user_info(arg)["response"]["players"][0]["personaname"]
    await session.send(f"用户{username}({arg})拥有的应用及游戏：{lts(games)}")
@on_command('wishlist', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入steamid')
        return
    try:
        resp = get_wishlist(arg)
    except:
        await session.send('发生错误')
        return
    games = []
    for i in resp.keys():
        string = ""
        string += f"{resp[i]['name']}({i})"
        games.append(string)
        #wishgames.append(resp[str(i)]["name"])
    username = get_user_info(arg)["response"]["players"][0]["personaname"]
    await session.send(f"用户{username}({arg})的愿望单：{lts(games)}")