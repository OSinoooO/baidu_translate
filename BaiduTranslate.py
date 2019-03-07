import json
import re
import execjs
import requests


class BaiduTranslate(object):
    """百度翻译接口爬虫"""
    def __init__(self, fanyi_str):
        self.fanyi_str = fanyi_str
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        self.langdetect_url = 'https://fanyi.baidu.com/langdetect'
        self.fanyi_url = 'https://fanyi.baidu.com/v2transapi'
        self.index_url = 'https://fanyi.baidu.com/'
        self.headers = {
            'UserAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            # 百度翻译接口有cookie验证，请求时务必带上cookie，否则报997错误
            'Cookie': 'BAIDUID=B1653FC46A963D20B84AE051A895E186:FG=1; locale=zh; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1551591801; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1551591801; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1551593472; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1551593472',
            'Host': 'fanyi.baidu.com',
            'Origin': 'https: // fanyi.baidu.com',
        }

    def get_str_type(self):
        """获得被翻译的文字类型"""
        data = {
            'query': self.fanyi_str
        }
        response = requests.post(self.langdetect_url, data=data, headers=self.headers)
        str_type = json.loads(response.content.decode())['lan']
        return str_type

    def get_result_type(self, str_type):
        """判断翻译的文字类型"""
        # 中译英
        if str_type == 'zh':
            result_type = 'en'
        # 外译中
        else:
            result_type = 'zh'
        return result_type

    def get_sign(self):
        """js解密sign参数"""
        with open('BaiduFanyi.js') as f:
            js = f.read()
        sign = execjs.compile(js).call('a', self.fanyi_str)
        return sign

    def get_result(self, str_type, result_type):
        """获取翻译内容"""
        index_resp = requests.get(self.index_url, headers=self.headers).content.decode()
        token = re.search(r"token:.*?'(.*?)'", index_resp, re.S).group(1)
        data = {
            'query': self.fanyi_str,
            'from': str_type,
            'to': result_type,
            'token': token,
            'sign': self.get_sign()
        }
        session = requests.Session()
        response = session.post(self.fanyi_url, headers=self.headers, data=data)
        trans_result = json.loads(response.content.decode())['trans_result']['data'][0]['dst']
        print('=' * 50)
        print('翻译结果：')
        print(trans_result)
        return trans_result

    def run(self):
        # 获得被翻译的文字类型
        str_type = self.get_str_type()

        # 判断翻译的文字类型
        result_type = self.get_result_type(str_type)

        # 获取翻译内容
        trans_result = self.get_result(str_type, result_type)
        return trans_result


if __name__ == '__main__':
    print("input 'q' to quit!")
    while True:
        orgin_str = input('输入翻译内容：\n')
        if orgin_str in ['q', 'Q']:
            print('程序退出')
            break
        fanyi = BaiduTranslate(orgin_str)
        fanyi.run()
        print('*' * 50)
