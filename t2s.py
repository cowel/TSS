import sys
import requests
import os
import random
import re
import time
import nltk
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
# nltk.download('punkt')      //download if nltk error


class text2voice:
    def get_free_proxies():
        url = "https://free-proxy-list.net/"
        # request and grab content
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        # to store proxies
        proxies = []
        for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxies.append(str(ip) + ":" + str(port))
            except IndexError:
                continue
        return proxies

    def zalo_api(payload, voidid, speed):
        # get proxies
        proxies = []
        proxies = text2voice.get_free_proxies()
        # url = "https://zalo.ai/api/demo/v1/tts/synthesize"
        url = "https://api.zalo.ai/v1/tts/synthesize"
        f = open("output.txt", "w")
        links = []
        source = "https://zalo.ai/"
        cookie=''
        for p in payload:
            time.sleep(2)
            session = requests.Session()
            proxy = random.choice(proxies)
            phttp = "http://" + proxy
            text = quote(str(p))
            response = session.get(source)
            cookie = response.cookies.get_dict()
            text.encode('utf-8')  # Totally fine.
            payload = "input="+text+"&speaker_id=" + \
                voidid+"&speed="+speed+"&dict_id=0"
            for k,v in cookie.items():
                cookie = k+'='+v
            headers = {
                "apikey":"egYEKV9t1hnOJF5MLavK6YEjJbqeUnjA",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8",
                "origin": "https://zalo.ai",
                "referer": "https://zalo.ai/experiments/text-to-audio-converter",
                "cookie": cookie,
                # "cookie": "zai_did=8k9uAj3FNiTevcSSryzXoYYo64l0pcN8AB0TI38m; _ga=GA1.2.306647033.1634021428; zpsid=eMKnVbo-PZEPI60H5S5lHez9Pn8VmNT7aq8hJ5MvGHg0MKn9KeKvKwbBILT8iZPpqrTVLYQd2NAsQqPYEU4IO_S3LdeO_WeqoJK4PHB3Q3V78sLa; zai_sid=deN0KVCzFc28XCTI-JqcOPIFYmopHH0yXvJi2RHvQ7MkXkaNhavdLTIQ_nR0MrXKiQRc8jyTGqNmplOw_W9R4ixuf2NqFpaHmEx59AqVQqYnvyqf; ozi=2000.SSZzejyD0jydXQcYsa00d3xBfxgO71AMSOUclD5I6v9tXQszqXuPbtN8fRZP7nUICJ8p.1; _zlang=vn; _gid=GA1.2.1396954612.1641556131; __zi=3000.SSZzejyD0jydXQcYsa00d3xBfxgP71AM8Tdbg8yDLybdsUFXomnGoctPgUVF3Ht2QDAewSe47yO.1; _gat_gtag_UA_158812682_2=1"
            }

            response = requests.request("POST", url, data=payload.encode(
                'utf-8'), headers=headers, proxies={'http': phttp})
            f.write(response.text+"\n")
            

        out = open('output.txt', 'r').read()

        links = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}.m3u8)', out)
        f.close()
        return links

    def split_text(payload):
        text = []
        long_sentence = []
        if len(payload) <= 200:
            text.append(payload)
            return text
        elif len(payload) > 200:
            sentences = nltk.sent_tokenize(payload)
            sub_para = ''

            for sen in sentences:
                if sub_para == '':
                    sub_para = sen

                elif sub_para != '':
                    if len(sub_para)+len(sen) <= 200 and sen != sentences[-1]:
                        sub_para = sub_para + " " + sen

                    elif len(sub_para)+len(sen) <= 200 and sen == sentences[-1]:
                        sub_para = sub_para + " " + sen
                        long_sentence.append(sub_para)

                    elif len(sub_para)+len(sen) > 200:
                        long_sentence.append(sub_para)
                        sub_para = ''
                        sub_para = sen

                    elif sen == sentences[-1]:
                        long_sentence.append(sub_para)

        return long_sentence

    def connect_audio(links):
        id = 1
        path = str(os.getcwd())
        full = path + '/tmp_audio/'
        command = 'cd '+full+' && rm -rf *'
        os.system(command)
        f = open('list_name.txt', 'w')
        for i in links:
            url = i
            des_fol = str(os.getcwd())+"/tmp_audio/"
            namefile = str(id)+".mp3"
            command = 'ffmpeg  -i '+url+' -ab 256k ' + des_fol + namefile + ' -y'
            id = id + 1
            os.system(command)
            f.write("file '"+full+namefile+"'\n")
        f.close()
        print("done")

    def get_links():
        out = open('output.txt', 'r').read()
        links = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}.m3u8)', out)
        return links

    def mer_audio(id):
        path_list = str(os.getcwd()) + "/list_name.txt"
        path = str(os.getcwd())+"/final_audio/"

        mp3_path = path+id+".mp3"
        command = 'ffmpeg -f concat -safe 0 -i ' + \
            path_list + ' -c copy '+mp3_path + ' -y'
        os.system(command)

        mp3_path = mp3_path.replace(os.getcwd(), '.')

        return mp3_path


class final_path_mp3():
    def get_path_mp3(id, payload, voiceid, speed):
        path = str(os.getcwd())+"/tmp_audio"
        if os.path.exists(path) == False:
            os.system("mkdir tmp_audio")
        path = str(os.getcwd()) + "/final_audio"
        if os.path.exists(path) == False:
            os.system("mkdir final_audio")
        data = text2voice.split_text(payload)
        text2voice.zalo_api(data, voiceid, speed)
        links = text2voice.get_links()
        text2voice.connect_audio(links)
        path = text2voice.mer_audio(id)
        return path


class file2payload(object):
    def read_file(path):
        with open(path, 'r') as data:
            payload = data.read()
        return payload


def main(path, voiceid='1'):
    payload = file2payload.read_file(path)
    path = final_path_mp3.get_path_mp3(
            id='void', payload=payload, voiceid=voiceid, speed="0.8")
    print(path)

    

if __name__ == "__main__":
    path = './data/page.txt'
    main(path)
    
