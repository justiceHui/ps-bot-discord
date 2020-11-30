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


# end

def tokenize(cmd_string):
    arr = cmd_string.split()
    ret = {'prefix': arr[0][0], 'op': arr[0][1:], 'paramCount': 0, 'paramAll': ''}
    for i in range(len(arr)):
        if i == 0:
            continue
        ret['paramAll'] += arr[i] + ' '
        ret['param' + str(i)] = arr[i]
        ret['paramCount'] += 1
    return ret


def get_command_result(cmd_string):
    cmd = tokenize(cmd_string)
    if cmd['prefix'] != '/':
        return None
    if cmd['op'] == 'cf' and cmd['paramCount'] == 0:
        return get_codeforces_round()
    if cmd['op'] == 'cf' and cmd['paramCount'] == 1:
        return get_codeforces_user(cmd['param1'])
    if cmd['op'] == 'rp' and cmd['paramCount'] > 0:
        return get_boj_random_problem(cmd['paramAll'].replace('/', ''))
    if cmd['op'] == 'sp' and cmd['paramCount'] > 0:
        return get_boj_search_problem(cmd['paramAll'].replace('/', ''))
    if cmd['op'] == 'solved' and cmd['paramCount'] == 1:
        return get_boj_user(cmd['param1'])
    if cmd['op'] == 'ptag' and cmd['paramCount'] == 1:
        return get_boj_problem_tier(cmd['param1'])
    return None


client = discord.Client()


@client.event
async def on_ready():
    print(f'logged in as {client.user.name}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Problem Solving'))


@client.event
async def on_message(message):
    msg = message.content

    res = get_command_result(msg)
    if res is not None:
        await message.channel.send(res)


client.run(json.load(open('./secret.json'))['login_token'])
