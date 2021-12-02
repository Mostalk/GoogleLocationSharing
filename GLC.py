import json
import requests


class GLC:
    def __init__(self, cookie, url):
        self.url = url
        self.header = {"cookie": cookie}
        self.ulist = []
        self.data = []

    def req(self):
        r = requests.get(self.url, headers=self.header)
        self.data = json.loads(r.text.replace(")]}'", ""))[0]
        return r

    def get_user_list(self):
        r = self.req()
        for user in r:
            self.ulist.append(user[0][3])
        return self.ulist

    def get_user_loc(self, name):
        ulist = self.get_user_list()
        for user in ulist:
            if user[0][3] == name:
                return user[1][4]
