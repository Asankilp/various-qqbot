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
from bilibili_api import bangumi
ssl._create_default_https_context = ssl._create_unverified_context
@on_command('bangumi', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入搜索内容')
        return
    arg = urllib.parse.quote(arg)
    url = f'http://api.bilibili.com/x/web-interface/search/type?search_type=media_bangumi&keyword={arg}'
    json1 = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    title = json1["data"]["result"][0]["title"]
    title = title.replace("<em class=\"keyword\">", "")
    title = title.replace("</em>", "")
    org_title = json1["data"]["result"][0]["org_title"]
    cover = json1["data"]["result"][0]["cover"]
    url = json1["data"]["result"][0]["url"]
    media_id = json1["data"]["result"][0]["media_id"]
    season_id = json1["data"]["result"][0]["season_id"]
    await session.send(f"标题：{title}\n原标题：{org_title}\n播放URL：{url}\nmdid：{media_id}\nssid：{season_id}\n封面URL：{cover}")
    await session.send(f"[CQ:image,file={cover}]")
@on_command('meta', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入mdid')
        return
    resp = await bangumi.get_meta(arg)
    locale = resp["media"]["areas"][0]["name"]
    title = resp["media"]["title"]
    cover = resp["media"]["cover"]
    url = resp["media"]["share_url"]
    rating = resp["media"]["rating"]["score"]
    await session.send(f"标题：{title}\n地区：{locale}\n封面URL：{cover}\n播放URL：{url}\n评分：{rating}")
    await session.send(f"[CQ:image,file={cover}]")
@on_command('lcomment', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入mdid')
        return
    resp = await bangumi.get_long_comment_list(arg)
    for cmt in resp["list"]:
        content = cmt["content"]
        time = cmt["ctime"]
        name = cmt["author"]["uname"]
        mid = cmt["mid"]
        await session.send(f"{name}({mid})：{content}\n时间：{time}")  
@on_command('overview', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入ssid')
        return
    resp = await bangumi.get_overview(arg)
    jianjie = resp["evaluate"]
    jp_title = resp["jp_title"]
    await session.send(f"简介：{jianjie}\n日语标题：{jp_title}")
@on_command('bangumit', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send('请输入搜索内容')
        return
    arg = urllib.parse.quote(arg)
    url = f"https://api.qiu.moe/intl/gateway/v2/app/search/type?type=7&appkey=7d089525d3611b1c&build=1001310&mobi_app=bstar_a&platform=android&s_locale=zh_SG&c_locale=zh_SG&sim_code=52004&lang=hans&keyword={arg}"
    json1 = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    title = json1["data"]["items"][0]["title"]
    title = title.replace("<em class=\"keyword\">", "")
    title = title.replace("</em>", "")
    cover = json1["data"]["items"][0]["cover"]
    uri = json1["data"]["items"][0]["uri"]
    season_id = json1["data"]["items"][0]["season_id"]
    await session.send(f"标题：{title}\n播放URI：{uri}\nseason_id：{season_id}\n封面URL：{cover}")
    await session.send(f"[CQ:image,file={cover}]")