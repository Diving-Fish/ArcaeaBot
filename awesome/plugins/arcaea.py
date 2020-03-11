from nonebot import on_command, CommandSession, helpers
import requests
import demjson
import random
import math
import time as _time
from awesome.plugins.arcaea_crawler import query as arc_query
from awesome.plugins.arcaea_crawler import best as arc_best

f = open('ds.txt', 'r', encoding='utf-8')
dss = f.readlines()
f.close()

help_text = '''欢迎使用Arcaea Bot。支持的命令如下：
.ds <曲名/等级> 查询定数
.arc <玩家名/好友码> 查询玩家的ptt、r10/b30和最近游玩的歌曲
.best <玩家名/好友码> <n> 查询玩家ptt前n的歌曲'''

@on_command('help', only_to_me=False)
async def help(session: CommandSession):
    await session.send(help_text)

@on_command('best', only_to_me=False)
async def lookup(session: CommandSession):
    await session.send("Looking up %s\nWarning: .best命令具有刷屏风险，请尽量私聊查询~" % session.state['id'])
    try:
    	s = arc_best(session.state['id'], session.state['num'])
    except Exception as e:
        s = ["An error occurred: " + repr(e)]
    for elem in s:
        await session.send(elem)


@lookup.args_parser
async def _(session: CommandSession):
    arr = session.current_arg_text.strip().split(' ')
    session.state['id'] = arr[0]
    try:
        session.state['num'] = int(arr[1])
    except Exception:
        session.state['num'] = 0


@on_command('arcaea', aliases=['arc'], only_to_me=False)
async def arcaea(session: CommandSession):
    await session.send("Querying %s" % session.state['id'])
    try:
        s = arc_query(session.state['id'])
    except Exception as e:
        s = "An error occurred: " + repr(e)
    await session.send(s)
        

@arcaea.args_parser
async def _(session: CommandSession):
    session.state['id'] = session.current_arg_text.strip()


@on_command('ds', only_to_me=False)
async def ds(session: CommandSession):
    result_str = ""
    num = 0
    for line in dss:
        if session.state['arg'].lower() in line.lower():
            num += 1
            result_str += line.replace('\t', '  ')
    await session.send("共找到%d条结果：\n" % num + result_str[:-1])


@ds.args_parser
async def _(session: CommandSession):
    session.state['arg'] = session.current_arg_text.strip()
