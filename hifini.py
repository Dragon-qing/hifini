# @author Dragon_qing
# encoding utf-8
import time

import requests
import urllib.request
import random
from lxml import etree


class Hifini(object):
    SIGN_IN_URL = "https://www.hifini.com/sg_sign.htm"
    TEST_URL = "http://httpbin.org/get"
    ip_list = []

    def __init__(self):
        self.ip_list = self.get_ip()
        print(self.ip_list, len(self.ip_list))

    def get_ip(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }
        response1 = requests.get('http://www.66ip.cn/areaindex_17/1.html', headers=headers)
        response2 = requests.get('http://www.ip3366.net', headers=headers)
        response3 = requests.get('https://ip.jiangxianli.com/?page=1', headers=headers)
        # response4 = requests.get('https://www.kuaidaili.com/free/', headers=headers)
        # 制作ip池
        ips = []
        if response1.ok or response2.ok or response3.ok:
            temp = []
            if response1.ok:
                html = etree.HTML(response1.content)
                temp_iplist = html.xpath(
                    '//div[@id = "footer"]/div/table/tr[position()>1]/td[position()>0 and position()<=2]/text()')
                for i in range(len(temp_iplist) // 2):
                    temp.append(temp_iplist[2 * i] + ':' + temp_iplist[2 * i + 1])

            if response2.ok:
                html = etree.HTML(response2.content)
                temp_iplist = html.xpath('//div[@id="list"]/table/tbody/tr/td[position()<3]/text()')
                for i in range(len(temp_iplist) // 2):
                    temp.append(temp_iplist[2 * i] + ':' + temp_iplist[2 * i + 1])

            if response3.ok:
                html = etree.HTML(response3.content)
                temp_iplist = html.xpath('//head/link[contains(@href, ":")]/@href')
                for ip in temp_iplist:
                    temp.append(str(ip).lstrip('//'))

            # if response4.ok:
            #    html = etree.HTML(response4.content)
            #    temp_iplist = html.xpath(
            #        '//div[@id="list"]/table/tbody/tr/td[@data-title="IP" or @data-title="PORT"]/text()')
            #    for i in range(len(temp_iplist) // 2):
            #        temp.append(temp_iplist[2 * i] + ':' + temp_iplist[2 * i + 1])

            ips.extend(temp.copy())
            # 测试每个ip是否可用
            for ip in ips:
                try:
                    proxy_host1 = 'http://' + ip
                    proxy_temp = {'http': proxy_host1}
                    urllib.request.urlopen("https://www.hifini.com", proxies=proxy_temp).read()
                    ip = proxy_host1
                except Exception as e:
                    ips.remove(ip)
                    continue
        else:
            print("代理获取失败！！！")
        return ips

    def get_randomip(self):
        ip = random.choice(self.ip_list)
        proxy_host1 = 'http://' + ip
        proxy_temp = {'http': proxy_host1}
        return proxy_temp

    def sign_hifini(self):
        temp_cookies = "bbs_sid=71ftqg13r0sohr9fv5np2gqebp; bbs_token=ndlS5_2FcRTPDeck3X9n2n3s8Lni3nGYzQjgKsWXlGNvfb6UanY6jKY9mSD3dK7Pm9ViYlAlKYT2H7zXG774Tq9Y6_2F4eDgFg4z; cookie_test=6FfHkUz_2Bt_2B5YUPLTWr7zaI_2BryDg4S5nKf7fEGdY6KR3en225; Hm_lvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1652013429,1652265506,1652359257,1652406736; Hm_lpvt_4ab5ca5f7f036f4a4747f1836fffe6f2=1652406736"
        headers = {
            "origin": "https://www.hifini.com",
            "referer": "https://www.hifini.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "accept": "text/plain, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        cookies = {cookie.split("=")[0]: cookie.split("=")[-1] for cookie in temp_cookies.split("; ")};
        for i in range(1):
            try:
                response = requests.post(url=self.SIGN_IN_URL, headers=headers, cookies=cookies,  verify=False)
                print(response.json()["message"])
            except Exception as e:
                print(e)
                time.sleep(0.3*random.random())

        # with open("hifini.html", "wb") as f:
        #     f.write(response.content)


if __name__ == "__main__":
    hifini = Hifini()
    hifini.sign_hifini()



