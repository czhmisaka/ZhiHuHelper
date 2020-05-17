from zhihuHelper import zhihuHelper as zh

a = zh()
a.path = input(">")
a.getByQID(input('问题id>'))