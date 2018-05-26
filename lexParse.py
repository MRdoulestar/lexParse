#编译原理课程实验——词法分析
#python3.6
#余星鑫

import re

#存储词法分析结果
token=[]

#定义正则匹配模式pattern
#标识符
diyList=r'''^[a-z|A-Z|_][\w|\d|_]*$'''

#数字常量
constList=r'''[\[|\({|=|\s]+([0-9]+\.*[0-9]*)[\]|\)|}|;]+'''

#字符串常量
strList=r'''["|']([^"]*)["|']'''

#边界符
boundList=r'''({|}|"|'|\(|\)|\[|\]|;|,)'''

#运算符
mathList=r'''(<<|>>|<>|<=|>=|==|=|<|>|\+|-|\*|/|\^)'''

#保留字
keepList=r'''\b(auto|int|long|short|float|double|char|unsigned|signed|break|continue|const|default|void|volatile|struct|union|auto|register|extern|static|sizeof|for|goto|do|while|if|else|switch|case|enum|typedef|return)'''

#便于错误处理，非法字符
allList=r'''\S+'''

#读取源代码文件
def getSrc(file):
    print("源代码：")
    with open(file) as code:
        for line in code:
            print(line,end="")
        print()

#读取Token词法分析结果
def getToken():
    print("提取结果:")
    for i in token:
        print(i)

#持久化Token
def saveToken(file):
    with open("output.txt","w") as f:
        for line in token:
            f.write(line[0]+' => '+line[1]+'\n')


#写入token
def reHandle(List,data,type):
    res=re.findall(List,data)
    if res:
        for word in res:
            # print("inhand:"+word)
            token.append([word,type])
            # data = data.replace(word,"")
        data=re.sub(List,' ',data)
        # data=data.replace(word,' ')
        # print("reHandle:"+data+str(len(data)))
        return [0,data]
    else:
        return [1,data]


#使用正则匹配进行词法分析
#逐行进行模式正则匹配结果处理
def setToken(file):
    with open(file) as code:
        #逐行正则匹配
        for data in code:
            #错误标记
            flag=0
            #数据进行去除前后tab和空格
            data=data.strip()
            # print(data)
            #进行正则匹配并处理
            #匹配保留字
            HandleR = reHandle(keepList,data,"保留字")
            flag += HandleR[0]
            data = HandleR[1]

            #匹配运算符
            HandleR = reHandle(mathList,data,"运算符")
            flag += HandleR[0]
            data = HandleR[1]

            #匹配常量
            HandleR = reHandle(constList,data,"数字常量")
            flag += HandleR[0]
            data = HandleR[1]

            HandleR = reHandle(strList,data,"字符串常量")
            flag += HandleR[0]
            data = HandleR[1]

            #匹配边界符号
            HandleR = reHandle(boundList,data,"边界符号")
            flag += HandleR[0]
            data = HandleR[1]

            #匹配所有剩余符号
            data = data.strip()
            res=re.findall(allList,data)
            if res:
                for word in res:
                    #进行7位截取
                    if len(word) > 7:
                        word = word[0:7]
                    #匹配合法标识符
                    sub_res=re.match(diyList,word)
                    if sub_res:
                        #写入表示符号到token
                        token.append([word,"标识符号"])
                    else:
                        #写入非法符号到token
                        token.append([word,"非法符号"])
                

if __name__ == "__main__":
    #源代码文件路径
    file="code2.txt"

    #打印源代码
    getSrc(file)

    #调用正则处理词法分析
    setToken(file)

    #打印词法分析结果
    getToken()

    #将此法分析结果写入文件
    saveToken("output.txt")

    