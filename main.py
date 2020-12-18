import discord
import requests
import json
from urllib import parse  # url encode

SERVER_URL = json.load(open('./secret.json'))['server_url']


# Codeforces
def get_codeforces_round():
    url = SERVER_URL + '/codeforces/round'
    return requests.get(url).text


def get_codeforces_user(handle):
    url = SERVER_URL + '/codeforces/user/' + handle
    return requests.get(url).text


# BOJ
def get_boj_user(handle):
    url = SERVER_URL + '/boj/user/' + handle
    return requests.get(url).text


def get_boj_random_problem(query):
    url = SERVER_URL + '/boj/random_problem/' + parse.quote(query)
    return requests.get(url).text


def get_boj_search_problem(query):
    url = SERVER_URL + '/boj/search_problem/' + parse.quote(query)
    return requests.get(url).text


def get_boj_problem_tier(prob):
    url = SERVER_URL + '/boj/tag/' + prob
    return requests.get(url).text

def get_boj_problem_name(prob):
    url = SERVER_URL + '/boj/problem_name/' + prob;
    return requests.get(url).text

# end

def tokenize(cmd_string):
    arr = cmd_string.split()
    if len(cmd_string) == 0:
        return None
    ret = {'prefix': arr[0][0], 'op': arr[0][1:], 'paramCount': 0, 'paramAll': ''}
    for i in range(len(arr)):
        if i == 0:
            continue
        ret['paramAll'] += arr[i] + ' '
        ret['param' + str(i)] = arr[i]
        ret['paramCount'] += 1
    return ret

def isProblemNumber(x):
    try:
        y = int(x)
    except ValueError:
        return False
    if y < 1000:
        return False
    return True

client = discord.Client()


@client.event
async def on_ready():
    print(f'logged in as {client.user.name}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Problem Solving'))


@client.event
async def on_message(message):
    res = None
    cmd_string = message.content
    cmd = tokenize(cmd_string)
    if cmd is None:
        return
    if cmd['prefix'] != '/':
        res = None
    elif cmd['op'] == 'cf' and cmd['paramCount'] == 0:
        res = get_codeforces_round()
    elif cmd['op'] == 'cf' and cmd['paramCount'] == 1:
        res = get_codeforces_user(cmd['param1'])
    elif cmd['op'] == 'rp' and cmd['paramCount'] > 0:
        res = get_boj_random_problem(cmd['paramAll'].replace('/', ''))
    elif cmd['op'] == 'sp' and cmd['paramCount'] > 0:
        res = get_boj_search_problem(cmd['paramAll'].replace('/', ''))
    elif cmd['op'] == 'solved' and cmd['paramCount'] == 1:
        res = get_boj_user(cmd['param1'])
    elif cmd['op'] == 'ptag' and cmd['paramCount'] == 1:
        res = get_boj_problem_tier(cmd['param1'])
    elif cmd['op'] == 'prob' and cmd['paramCount'] == 1 and isProblemNumber(cmd['param1']):
        title = get_boj_problem_name(cmd['param1'])
        embedVar = discord.Embed(title='🔍 `' + cmd_string + '`', description = '', color=0x42e0d1)
        embedVar.add_field(name='<:boj:789617690233929779> ' + title, value='https://www.acmicpc.net/problem/' + cmd['param1'], inline=True)
        res = None
        await message.channel.send(embed=embedVar)
    if res is not None:
        await message.channel.send(res)


client.run(json.load(open('./secret.json'))['login_token'])
