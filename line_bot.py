#gitで変更を見るために、コメントを追加しています。年のために分も追加。
print("aaa")
#まずはインポート
import requests
from bs4 import BeautifulSoup
import re
import datetime
import pytz
import pandas as pd

dt_now = str(datetime.datetime.now().strftime('%Y%m%d-%H％M%S'))

df = pd.DataFrame(
    [[dt_now, "kinocode", "hello cron"]],
    columns=['datetime', 'name', 'greet'])

df.to_csv('/Users/iwasawayuusaku/Documents/cron/test_'+dt_now+'.csv')
#print(dt_now, "hello world from cron")

#現在時刻の取得
time = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
time = time.strftime('%Y年%m月%d日 %H時％M分%S秒')
#print(time + "にニュースを送信しました。")
#グループのトークン
token = '6mK2bxugXsgn0xodoKah7CbQnHErrSkzhGyv1Eh3QuH'
#notifyのwebAPIのurl.エンドポイントという.linenotifyのドキュメントの通知系にある
api_url = 'https://notify-api.line.me/api/notify'
send_contents = "pythonプログラムから送信"
"""
lineは辞書型で情報を送信するらしい。
トークンはAuthorizationをキーとして送る
送りたい内容はmessegeをキーとする
"""
token_dic = {'Authorization': 'Bearer' + ' ' + token}
"""
実際に送信してみる。送信する際は、リクエストのポストメソッドを使用する
requests.post(アクセスするAPIのURL,headers=認証情報, data=送りたい内容)
画像を送信してみる。pngかjpgしか送れないけど
"""
#requests.post(api_url, headers=token_dic, data=message_dic, files=image_dic)

#Yahooのニュースのトップページをゲットして、パース。
load_url = "https://news.yahoo.co.jp/categories/it"
request = requests.get(load_url)
soup = BeautifulSoup(request.text, "html.parser")

#トップページから、ピックアップのニュースのリンクを取得
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
#ぶん回してlinkだけをpick_up_linksに格納
pick_up_links = []
for elem in elems:
    pick_up_links.append(elem.attrs['href'])

#pickupのニュースのリンクをぶん回して、中に入る。それで、続きを読むのリンクの中にさらに入る
i = 1
for pick_up in pick_up_links:
    if i == 2:
        break
    request_pick = requests.get(pick_up)
    soup_pick = BeautifulSoup(request_pick.text, "html.parser")
    #続きを読むがあるpタグを取得→続きを読むのリンクを取得
    next_read = soup_pick.find("p", class_="sc-beKmYL kjhEJs")
    #続きを読むのリンクの中をさらにパース
    request_next_read = requests.get(next_read.contents[0].attrs['href'])
    soup_next_read = BeautifulSoup(request_next_read.text, "html.parser")
    #タイトルとリンクをlineで送信するコンテンツの変数に代入して、lineに送信。
    send_url = {'message': next_read.contents[0].attrs['href']}
    #requests.post(api_url, headers=token_dic, data=send_url)
    i += 1

#lineトークン(岩澤個人)
#nX9xw2YGp2TdEGA1Zq6g8CMHWCy0HJED4bHjzYhlFIX
#lineトークン（グループ木村くん）
#6mK2bxugXsgn0xodoKah7CbQnHErrSkzhGyv1Eh3QuH
