# coding=utf-8
import urllib
import urllib2
import random
import json
import cookielib


class RegionController:
    def __init__(self):
        pass

    def get_top_region(self):
        url = 'http://demo.koalareading.com:8081/users/open/region/topRegions'
        response = urllib2.urlopen(url)
        return json.loads(response.read())

    def get_sub_region(self, parent_id):
        url = 'http://demo.koalareading.com:8081/users/open/region/{0}/subRegions'.format(parent_id)
        response = urllib2.urlopen(url)
        return json.loads(response.read())

    def get_school(self, addr_code):
        url = 'http://demo.koalareading.com:8081/users/open/school/region/list?addrCode={0}'.format(addr_code)
        response = urllib2.urlopen(url)
        return json.loads(response.read())


class AccountController:
    """
    处理所有需要登录完成的事情

    1.创建学校
    2.创建校长账号
    3.创建老师账号
    4.校长认证老师班级
    5.创建学生账号
    6.学生加入班级
    7.老师允许学生加入班级
    """
    header = {
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
    cookie = cookielib.CookieJar()

    def __init__(self):
        pass

    @staticmethod
    def rand_phone_number():
        phone_number = '13'
        for i in range(9):
            phone_number += str(random.randint(0, 9))
        return phone_number

    @staticmethod
    def rand_psd():
        psd = ''
        for i in range(6):
            psd += str(random.randint(0, 9))
        return psd

    def login(self, account, psd, u_type):
        url = 'http://demo.koalareading.com:8081/users/open/login'
        data = urllib.urlencode({
            "account": account,
            "password": psd,
            "userType": u_type
        })
        handler=urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener(handler)
        try:
            response = opener.open(url, data=data)
            print response.read()
        except urllib2.URLError, e:
            print e.read()

    def op_login(self):
        self.login('O1', 'koala2016', '5')

    def tel_auth(self, tel):
        url = 'http://demo.koalareading.com:8081/users/open/register/telAuthCode'
        data = urllib.urlencode({
                "tel": tel
            })
        response = urllib2.urlopen(url, data=data)
        auth_id = response.read()
        auth_code_url = 'http://demo.koalareading.com:8081/users/open/authCode/{}'.format(auth_id)
        response = urllib2.urlopen(auth_code_url)
        auth_code = json.loads(response.read())['authCode']
        return (auth_id, str(auth_code))

    def create_account(self, opt):
        if 'birthday' not in opt:
            opt['birthday'] = ''
        if 'gender' not in opt:
            opt['gender'] = 1

        url = 'http://demo.koalareading.com:8081/users/open/register'
        request = urllib2.Request(url, headers=self.header)
        opt['tel'] = self.rand_phone_number()
        auth_id, auth_code = self.tel_auth(opt['tel'])
        psd = self.rand_psd()
        opt['password'] = psd
        opt['telAuthId'] = int(auth_id)
        opt['telAuthCode'] = auth_code

        try:
            response = urllib2.urlopen(request, data=json.dumps(opt))
            response_data = json.loads(response.read())
            with open('account.csv', 'a+') as f_in:
                f_in.write('{},{}\n'.format(response_data['account'], psd))
            return response_data['account'], psd
        except urllib2.URLError, e:
            print e.read()

    def student_join_class(self, class_code):
        url = 'http://demo.koalareading.com:8081/users/web/join/studentJoinClass'
        data = urllib.urlencode({
            "joinCode": class_code
        })

        handler=urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener(handler)
        try:
            response = opener.open(url, data=data)
            print response.read()
        except urllib2.URLError, e:
            print e.read()

    def create_school(self, school_id):
        self.op_login()

    def create_school_master(self, school_id):
        self.op_login()
        url = 'http://demo.koalareading.com:8081/users/operation/join/school/{0}/joinCode'.format(school_id)
        print url
        handler = urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener(handler)
        try:
            request = urllib2.Request(url, headers=self.header)
            response = opener.open(request, data=urllib.urlencode({}))
            data = json.loads(response.read())
            print len(data)
            print data
            join_code = data['joinCode']
            return self.create_account({
                'birthday': '',
                'gender': 1,
                'name': '校长',
                'schoolId': school_id,
                'userType': 4,
                'schoolJoinCode': join_code
            })
        except urllib2.URLError, e:
            print e.read()

    def create_class(self, school_id, class_info):
        """
        先创建老师账号，然后用这个老师账号创建班级
        :param school_id:
        :param class_info: {grade: '', full_name: ''}
        :return:
        """
        account, psd = self.create_account({
            'userType': 3,
            'schoolId': school_id,
            'name': class_info['full_name']
        })
        print account, psd
        self.login(account, psd, 3)
        # 创建班级，并返回班级代码
        url = 'http://demo.koalareading.com:8081/users/web/class'
        handler = urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener(handler)
        opt = {
            "authStatus": "1",
            "createTime": 0,
            "grade": class_info['grade'],
            "id": 0,
            "name": class_info['full_name'],
            "schoolId": school_id,
            "status": "1"
        }
        try:
            # 创建班级
            request = urllib2.Request(url, headers=self.header)
            response = opener.open(request, data=json.dumps(opt))
            data = json.loads(response.read())
            class_id = data['id']
            print class_id

            # 获取班级joinCode
            url = 'http://demo.koalareading.com:8081/users/web/join/class/{0}/joinCode'.format(class_id)
            handler = urllib2.HTTPCookieProcessor(self.cookie)
            opener = urllib2.build_opener(handler)
            response = opener.open(url)
            data = json.loads(response.read())
            join_code = data[0]['joinCode']

            return {
                'account': account,
                'psd': psd,
                'join_code': join_code
            }

        except urllib2.URLError, e:
            print e.read()

    def create_student_from_file(self, school_id, join_code, file_path):
        accounts = []
        with open(file_path) as f_in:
            data = []
            for i in f_in.readlines():
                data = i.decode('utf-8').split('\r')

            # print data
            for i in data:

                l = i.split(',')
                name = l[4]

                gender = 1 if l[5] == '男' else 2

                l[7] = l[7] if l[7] else '1'
                l[8] = l[8] if l[8] else '1'
                birthday = '{}-{:0>2}-{:0>2}'.format(l[6], l[7], l[8])
                # birthday = l[6][:4] + '-' + l[6][4:6] + '-' + l[6][6:]
                # print birthday

                # break
                account, psd = self.create_account({
                        "birthday": birthday,
                        "gender": gender,
                        "name": name,
                        "schoolId": school_id,
                        "userType": "2"
                    })
                accounts.append((account, psd))

        # sign up backup account
        for i in range(10):
            account, psd = self.create_account({
                "birthday": '',
                "gender": '',
                "name": '',
                "schoolId": school_id,
                "userType": "2"
                })
            accounts.append((account, psd))

        # sign in
        for data in accounts:
            self.login(data[0], data[1], '2')
            self.student_join_class(join_code)
        # print accounts
        return accounts

    def teacher_allow_join(self):
        pass

if __name__ == '__main__':
    ac = AccountController()
    rc = RegionController()
    ac.create_school_master('173')
    # ac.create_account({
    #     "birthday": "2006-01-01",
    #     "gender": 1,
    #     "name": "string",
    #     "schoolId": "167",
    #     "userType": "2"
    # })
    # ac.login('S000047', '097288', '2')
    # ac.student_join_class()

    # # sign up
    # school_id = '128017'
    # count = 0
    # # with open('class52.csv') as f_in:
    # with open('class52.csv') as f_in:
    #     data = []
    #     for i in f_in.readlines():
    #         data = i.decode('utf-8').split('\r')
    #
    #     # print data
    #     for i in data:
    #
    #         l = i.split(',')
    #         name = l[4]
    #
    #         gender = l[5]
    #
    #         # l[7] = l[7] if l[7] else '1'
    #         # l[8] = l[8] if l[8] else '1'
    #         # birthday = '{}-{:0>2}-{:0>2}'.format(l[6], l[7], l[8])
    #         birthday = l[6][:4] + '-' + l[6][4:6] + '-' + l[6][6:]
    #         # print birthday
    #
    #         # break
    #         ac.create_account({
    #                 "birthday": birthday,
    #                 "gender": gender,
    #                 "name": name,
    #                 "schoolId": school_id,
    #                 "userType": "2"
    #             })
    #
    # # sign up backup account
    # for i in range(10):
    #     ac.create_account({
    #         "birthday": '',
    #         "gender": '',
    #         "name": '',
    #         "schoolId": school_id,
    #         "userType": "2"
    #         })
    #
    # # sign in
    # with open('account.csv') as f_in:
    #     for i in f_in.readlines():
    #         data = i.strip().split(',')
    #         ac.login(data[0], data[1], '2')
    #         # ac.student_join_class('0Q7V03')
    #         ac.student_join_class('S9K016')

    # rc.get_school('110101')
