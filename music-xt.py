#-*- coding:utf-8 -*-
# author:**ZLH**
# editor:XTPEEPS.cn.
# datetime:2019/8/27 16:47
# Update: 
#   2019.08.28 fix n个bugs； 
#           fix当请求下载地址出现null时报错问题，并尝试获取mv逻辑；
#           所有类型现在可以根据实际情况显示，如果类型未获取地址不会显示其对应选择项；
#           增加自定义目录，并且如果目录不存在则新增功能。 by. XT.
#   2019.08.29 add 判断下载链接可用性，现在只有能够访问的下载链接可以提供选择下载;
#           fix bugs. by xt.
import requests
import json
import os
import stat


headers = {
'Host': 'c.y.qq.com',
'Referer': 'http://c.y.qq.com/',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
}
jsons=[]


def douqq_post(mid):
    """
    返回歌曲下载url
    :param mid:歌曲mid
    :return: 字典
    """
    # print("[debug]prepare download music.")
    post_url = 'http://www.douqq.com/qqmusic/qqapi.php'
    data = {'mid': mid}
    # print("[debug]get mid from qq.com:"+mid)
    res = requests.post(post_url, data=data)
    get_json = json.loads(res.text)
    # print("[debug]get_json"+get_json)
    # print("[debug]type of get_json"+str(type(get_json)))
    # print("[debug]eval(get_json):"+str(json.loads(get_json)))
    # return eval(get_json) # 当get_json存在null时会报错null，改成load.json
    return json.loads(get_json)
def test_songurl(url):
    """
    测试下载song下载链接可用性
    """
    try:
        song_api=requests.get(url,timeout=3)
        song_respon = song_api.status_code
        # print(song_respon, end=" ")
        return song_respon
    except Exception as e:
        return 0
    
    
def download_file(src, file_path):
    """
    歌曲下载
    :param src: 下载链接
    :param file_path: 存储路径
    :return: 文件路径
    """
    r = requests.get(src, stream=True)
    f = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    return file_path
def choice_download(dic):
    # print('')
    # print(dic)
    print("[-]判断连接可用性")
    if ((dic["m4a"]==None or str(dic["m4a"])=="" or str(dic["m4a"])==None) and (str(dic["mp3_l"])==None or str(dic["mp3_l"])=="" or dic["mp3_l"]=="") and (str(dic["mp3_h"])==None or str(dic["mp3_h"])=="" or dic["mp3_h"]=="") and (str(dic["ape"])==None or str(dic["ape"])=="" or dic["ape"]=="") and (str(dic["flac"])==None or str(dic["flac"])=="" or dic["flac"]=="")):
        print("[!]未获取到歌曲下载地址，可能由于歌曲需要购买无法获取")
        if str(dic["mv"])!=None and str(dic["mv"])!="" and dic["mv"]!="" and str(dic["mv"])!="暂无MV":
            if test_songurl(dic["mv"])==200:
                print('[+]mv ( 只提供手动下载地址 ) ：'+str(dic["mv"]))
        return None,None
    print("[-]判断歌曲连接可用性")
    if dic["m4a"]!=None and str(dic["m4a"])!="" and str(dic["m4a"])!=None :
        if test_songurl(dic["m4a"])==200:
            print('1. m4a格式 '+str(dic["m4a"]))
            # print("[debug]m4a get:"+str(dic["m4a"]))
    if str(dic["mp3_l"])!=None and str(dic["mp3_l"])!="" and dic["mp3_l"]!="":
        if test_songurl(dic["mp3_l"])==200:
            print('2. mp3普通品质 '+str(dic["mp3_l"]))
            # print("[debug]mp3_l get:"+str(dic["mp3_l"]))
    if str(dic["mp3_h"])!=None and str(dic["mp3_h"])!="" and dic["mp3_h"]!="":
        if test_songurl(dic["mp3_h"])==200:
            print('3. mp3高品质 '+str(dic["mp3_h"]))
            # print("[debug]mp3_h get:"+str(dic["mp3_h"]))
    if str(dic["ape"])!=None and str(dic["ape"])!="" and dic["ape"]!="":
        if test_songurl(dic["ape"])==200:
            print('4. ape高品无损'+str(dic["ape"]))
            # print("[debug]ape get:"+str(dic["ape"]))
    if str(dic["flac"])!=None and str(dic["flac"])!="" and dic["flac"]!="":
        if test_songurl(dic["flac"])==200:
            print('5. flac无损音频'+str(dic["flac"]))
            # print("[debug]flac get:"+str(dic["flac"]))
    print("[-]判断mv地址可用性")
    if str(dic["mv"])!=None and str(dic["mv"])!="" and dic["mv"]!="" and str(dic["mv"])!="暂无MV":
        if test_songurl(dic["mv"])==200:
            print('[+]mv ( 只提供手动下载地址 ) ：'+str(dic["mv"]))
    select = int(input("请输入您的选择:"))
    src = ''
    postfix = ''
    if select == 1:
        src = dic['m4a']
        postfix = '.m4a'
    if select == 2:
        src = dic['mp3_l']
        postfix = '.mp3'
    if select == 3:
        src = dic['mp3_h']
        postfix = '.mp3'
    if select == 4:
        src = dic['ape']
        postfix = '.ape'
    if select == 5:
        src = dic['flac']
        postfix = '.flac'
    return postfix, src.replace('\/\/', '//').replace('\/', '/')
def find_song(word):
    global song_name_download
    """
    查找歌曲
    :param word: 歌曲名
    :return: 返回歌曲mid
    """
    get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='+word
    try:
        res1 = requests.get(get_url, headers=headers)
        # print("[debug]requests search: "+str(res1))
        get_json = json.loads(res1.text.strip('callback()[]'))
        # print("[debug]get_json: "+str(get_json))
        # print("[debug]type of get_json"+str(type(get_json)))
        jsons = get_json['data']['song']['list']
        # print("[debug]finding songs.")
        # print("[debug]finding: "+word)
        # print("[debug]get result:"+str(jsons))
        
        songmid = []
        media_mid = []
        song_singer = []
        song_names=[]
        i = 1
        for song in jsons:
                # print(i, ':' + song['songname'], '---', song['singer'][0]['name'], song['songmid'], song['media_mid'])
                print(i, ':' + song['songname'], '---', song['singer'][0]['name'])
                songmid.append(song['songmid']) 
                media_mid.append(song['media_mid'])
                song_singer.append(song['singer'][0]['name'])
                song_names.append(song['songname'])
                i = i + 1
        select = int(input("请输入您的选择:")) - 1
        song_name_download=song_names[select]
        print(song_name_download)
        # # test start
        # print("[debug]get ele from api: ")
        # print("songname:"+str(song_names))
        # print("media_mid:"+str(media_mid))
        # print("song_singer:"+str(song_singer))
        # # test stop
        return songmid[select], song_singer[select]
    except Exception as e:
        print(f'歌曲查找有误：{e}')
        return None
if __name__ == '__main__':
    # songname = '叹云兮'
    # global song_name_download
    song_name_download=""
    get_save_path = input('Give a localpath to save music, default(E:\\music):')
    if get_save_path =="":
        save_path = "E:\\music"
    else:
        save_path=get_save_path
    # print(save_path)
    if not os.path.exists(save_path):
        print("[debug]path: "+save_path+" didn't exists, will create it.")
        os.system(r"md {}".format(save_path))
        print("[debug]md "+save_path+ " success")
    if not save_path.startswith('\\'):
        save_path=save_path+"\\"
        print(save_path)
    # dic=""
    while True:
        songname = input("Please input the music name:")
        song_mid, singer = find_song(songname)
        try:
            dic = douqq_post(song_mid)
            # print("[debug]type of dic: "+str(type(dic)))
            # print(dic)
        except Exception as e:
            print("[debug]type of dic: "+str(type(dic)))
            # print(dic)
            print("[Error]main/dic error: "+str(e))
            print("[debug]song_mid: "+song_mid)
        # {
        # "mid":"004FjJo32TISsY",
        # "m4a":"http:\/\/dl.stream.qqmusic.qq.com\/C400004FjJo32TISsY.m4a?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=38",
        # "mp3_l":"http:\/\/dl.stream.qqmusic.qq.com\/M500004FjJo32TISsY.mp3?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "mp3_h":media_mid"http:\/\/dl.stream.qqmusic.qq.com\/M800004FjJo32TISsY.mp3?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "ape":"http:\/\/dl.stream.qqmusic.qq.com\/A000004FjJo32TISsY.ape?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "flac":"http:\/\/dl.stream.qqmusic.qq.com\/F000004FjJo32TISsY.flac?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "pic":"https:\/\/y.gtimg.cn\/music\/photo_new\/T002R300x300M000003NZyTh4eMMsp.jpg?max_age=2592000"
        # }
        # print('mid:'+dic['mid'])
        postfix, url = choice_download(dic)
        # print("[debug]postfix: "+postfix+" url: "+url)
        if postfix==None:
            con = input('Continue or not: y/n')
            if con == 'n':
                break
        else:
            # print("[debug]get "+save_path + song_name_download + ' - ' + singer + postfix)
            file_local=download_file(url, save_path + song_name_download + ' - ' + singer + postfix)
            print("[+]success saved to: "+file_local)
            con = input('Continue or not: y/n')
            if con == 'n':
                break