import requests,re,os
from requests import RequestException

import random

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua

headers={ 
    'User-Agent':get_ua(),
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Host':'bookset.me',
    'Referer':'https://bookset.me/4989.html',
    'Cookie':'_ga=GA1.2.532825224.1538916786; _gid=GA1.2.215581363.1538916786; \
     Hm_lvt_867e9077558c759606bf5c053a75de22=1538983452,1538983474,1538983479,\
     1538983498; Hm_lpvt_867e9077558c759606bf5c053a75de22=1538986754'
}

def get_one_page(url):    # 获取一个页面    
    try:        
        response = requests.get(url,headers=headers)        
        if response.status_code == 200:            
            return response.text        
        return None    
    except RequestException:        
        return None

def pares_html(html):
    parrten = re.compile('<br /><a href="(.*?)" target="_blank" rel="nofollow" >(.*?)</a>',re.S)
    items=re.findall(parrten,html)
    for item in items:
        yield{
            'url':item[0],
            'filname':re.sub('&#\d+;','',item[1]).replace(' ','')
        }

def save_file(url,filename):
        
    floder = filename.split('.')[0]
    if not os.path.isdir(floder):
        os.makedirs(floder)
    data = requests.get(url,headers=headers)
    with open(floder+'/'+filename,'wb') as f:
        f.write(data.content)
        print(filename +'保存完毕')
    with open('urls.txt','w') as f:
        f.write(url)
        f.close()   
        print(url+'已下载') 

def urlcheck(url):
    with open('urls.txt','r') as f:
        for i in f:
            print(i)
            if url == i:
                return False #存在url返回假
            return True 

if __name__ =="__main__":
    html = get_one_page("https://bookset.me/4983.html") #解析页面
    for item in pares_html(html):#得到元组
        save_file(item['url'],item['filname'])
        

        
    