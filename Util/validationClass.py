import json
import time

import requests


class Validation:

    def __init__(self):
        pass

    def judge_func(self, requests_obj):
        pass

    def validate(self, proxy):
        if isinstance(proxy, bytes):
            proxy = proxy.decode("utf8")
        try:
            request = requests.get('http://quan.suning.com/getSysTime.do',
                                   proxies={"http": "http://{proxy}".format(proxy=proxy)}, timeout=2, verify=False)
            return self.judge_func(request)
        except Exception as e:
            return False


class SuningTimeValidation(Validation):

    def judge_func(self, requests_obj):
        if requests_obj.status_code == 200:
            try:
                result = json.loads(requests_obj.text)['sysTime2']
                result_timestamp = time.mktime(time.strptime(result, "%Y-%m-%d %H:%M:%S"))
                return abs(time.time() - result_timestamp) < 600
            except Exception:
                return False
