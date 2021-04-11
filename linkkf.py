import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
from tqdm import tqdm

print('----linkkf Downloader----')
print("2차가공,유료판매등의 행위를 금합니다.")
print("다운로드는 네트워크 상태에 따라 시간이 다소 소요 될수 있습니다.")
print("\n\n\n\n")
res = ("https://linkkf.app/")
ani = []
ani2 = []
#-------------------------------애니 기본 세팅
def search(find):
    finish = (res + find)
    return finish
arvg = search(input("애니이름:"))
anipage = requests.get(arvg)
soup = BeautifulSoup(anipage.content, "html.parser")
#-------------------------------애니 이름 검색
for n in soup.select("article > a"):
    ani.append(n.get("title"))

for m in soup.select("article > a"):
    ani2.append(m.get("href"))

ani2.reverse()
ani.reverse()

for number2,name2 in enumerate(ani2):
    aniarr = ('[{}] : {} '.format(number2+1,name2))
    #~화와 연결 시켜줘야 하는데 링크는 안보이게 함
for number,name in enumerate(ani):
    print('[{}] : {} '.format(number+1,name))
#-------------------------------애니 회차 입력
aa = int(input("입력(숫자만):"))
print(ani[aa-1])
viewAni = (ani2[aa-1])

anipage2 = requests.get(viewAni)
soup2 = BeautifulSoup(anipage2.content, "html.parser")
option = (soup2.find("option"))
#-------------------------------링크 리퍼러 요청
video_url = viewAni
referlink = (option.get("value"))
res2 = requests.get(referlink, headers={"Referer": video_url})
#-------------------------------옵션서버 영상 요청
res3 = BeautifulSoup(res2.content,"html.parser")
refer = res3.find("source") #리퍼로 보낼 m3u8사이트 src추출
src = (refer.get("src"))
print(src)
#-------------------------------m3u8 리퍼러 요청
res4 = requests.get(src, headers={"Referer": viewAni})#리스폰스 200
#res5 = BeautifulSoup(res4.content,"html.parser")#리스폰스 200 -> html형식
res5 = res4.text.split("\n")
anibogi = [] # 애니 ts담을 리스트
for anism in res5:
    if anism.startswith('index'):
        anibogi.append(anism)
for i in tqdm(anibogi):
    res = requests.get("/".join(src.split("/")[:-1])+"/"+i, headers={"Referer": viewAni})
    f = open("index"+i+".ts","wb")
    f.write(res.content)
    f.close


