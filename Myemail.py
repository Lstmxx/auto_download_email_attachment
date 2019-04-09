class MyEmail(object):
    def __init__(self):
        self.Subject = ''
        self.Sender = ''
        self.Recipient = ''
        self.html = ''
        self.file = []
        self.context = ''

    def showInfo(self,i):
        print("-"*8+str(i)+"-"*8)
        print("标题: %s" %self.Subject)
        print("发送者为: %s  %s" %(self.Sender[0],self.Sender[1]))
        print("接收文件位置:")
        print("html: %s" % self.html)
        print("邮件内容: %s"% self.context)
        print("附件:")
        for filepn in self.file:
            print(filepn)

    def clear(self):
        self.Subject = ''
        self.Sender = ''
        self.Recipient = ''
        self.html = ''
        self.file = []
        self.context = ''
