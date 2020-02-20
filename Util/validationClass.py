import json
import time

import requests


class Validation:

    def __init__(self):
        self._url = None

    def judge_func(self, requests_obj, proxy):
        pass

    def validate(self, proxy):
        if isinstance(proxy, bytes):
            proxy = proxy.decode("utf8")
        try:
            request = requests.get(self._url,
                                   proxies={"http": "http://{proxy}".format(proxy=proxy)}, timeout=3.14, verify=False)
            return self.judge_func(request, proxy)
        except Exception as e:
            return False


class SuningTimeValidation(Validation):

    def __init__(self):
        super().__init__()
        self._url = 'http://quan.suning.com/getSysTime.do'

    def judge_func(self, requests_obj, proxy):
        if requests_obj.status_code == 200:
            try:
                result = json.loads(requests_obj.text)['sysTime2']
                result_timestamp = time.mktime(time.strptime(result, "%Y-%m-%d %H:%M:%S"))
                return abs(time.time() - result_timestamp) < 600
            except Exception:
                return False


class IPAPIValidation(Validation):

    def __init__(self):
        super().__init__()
        self._url = 'http://ip-api.com/json/?fields=countryCode,query'

    def judge_func(self, requests_obj, proxy):
        if requests_obj.status_code == 200:
            try:
                result = json.loads(requests_obj.text)['query']
                # print(result)
                return result == proxy.split(':')[0]
            except Exception:
                return False
