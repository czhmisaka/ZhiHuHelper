

class log():
    def __init__(self,Wtype='develop'):
        if Wtype == 'develop':
            self.warning = True
            self.error = True
            self.normal = True
        if Wtype == 'work':
            self.warning = False
            self.error = False
            self.normal = True
    def warn(self,s):
        if self.warning:
            print('【警告】 :'+str(s))
    def err(self,s):
        if self.error:
            print('【错误】 :'+str(s))
    def log(self,s):
        if self.normal:
            print('【普通提示】 :'+str(s))
            