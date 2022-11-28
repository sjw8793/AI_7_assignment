import pandas as pd
import numpy as np



##### 데이터 불러오기 #####

df = pd.read_csv('pill_processed.csv')



##### Constant 선언 ######

PILLS = df['itemName'].values.tolist()

NORMAL = {'인사': ['안녕'],
          '감사': ['고마워', '감사', '고맙'],
          '도움': ['도움']}

KEYWORDS = {0:['회사', '제조사'],
            1:['이름', '제품명'],
            2:['효과', '효능', '약효'],
            3:['용법', '복용', '얼마나', '언제', '적정'],
            4:['부작용'],
            5:['보관'],
            6:['주의', '경고', '유의'],}



##### 초기 메시지 #####

def firstMessage():
    res = """안녕하세요? 약 도우미 챗봇입니다.
약의 보관법, 복용방법, 부작용 등 특정 약에 대해 궁금한 사항부터
특정 증상으로 아플 때 어떠한 약의 도움을 받을 수 있는지,
약에 관해 궁금한 사항은 무엇이든 물어봐 주세요.

예시 1) 약 "냠냠정"의 보관법이 궁금할 때: (약 이름, 궁금한 사항)
    => 냠냠정의 보관법은 뭐야?
    => 냠냠정 보관법
    => 냠냠정 어떻게 보관해야 해? 등
    
예시 2) 배 아플 때 어떤 약을 사야 하는지 궁금할 때: (증상)
    => 복통
    => 해열 되는 감기약 알려줘
    => 두통에 먹는 약 등"""
    
    return res



##### 유틸리티 함수 #####

# 약 이름에 따라 알맞는 row index를 반환
def getRIndex(pill):
    return df.index[df['itemName'] == pill][0]

# 제시된 키워드에 따라 알맞는 column index를 반환
def getCIndex(keyword):
    for k, v in KEYWORDS.items():
        if keyword in v:
            return k
    return -1

# 약 이름과 키워드에 따라 알맞는 data를 반환
def getData(pill, keyword):
    ridx = getRIndex(pill)
    cidx = getCIndex(keyword)
    return df.iat[ridx, cidx]

# 주어진 텍스트에서 조사를 제거한 단어들을 반환
def text2words(text):
    words = text.split()
    posts = ['은', '는', '랑', '이', '가', '을', '를', '의']
    
    for i in range(len(words)):
        for post in posts:
            words[i] = words[i].rstrip(post)
    
    return words



##### 키워드 추출 함수 #####

# 입력 텍스트에 응답 키워드가 들어있는지 확인하여 키워드를 반환
# Return -1 for 키워드 없음
# Return 0 for 키워드 다수
# Return 키워드 for 키워드 하나
def text2key(text):
    cnt = 0
    words = []
    for k, v in KEYWORDS.items():
        for keyword in v:
            if keyword in text:
                cnt += 1
                words.append(keyword)
                break
    
    if cnt == 0:
        return -1
    if cnt == 1:
        return words[0]
    return 0

# 입력 텍스트에 약 이름이 들어있는지 확인하여 약 이름을 반환
# Return -1 for 약 이름 없음
# Return 약 이름 리스트 for 약 이름 다수
# Return 약 이름 for 약 이름 하나
def text2pill(text):
    cnt = 0
    pills = []
    
    words = text2words(text)
    
    for item in words:
        for pill in PILLS:
            if item in pill:
                cnt += 1
                pills.append(pill)
    
    if cnt == 0:
        return -1
    if cnt == 1:
        return pills[0]
    return pills

# 입력 테스트에 인삿말 있는지 확인하여 인삿말 키워드를 반환
# Return -1 for 인삿말 없음
# Return 인삿말 키워드 for 인삿말 있음
def text2hi(text):
    for k, v in NORMAL.items():
        for item in v:
            if item in text:
                return k
    return -1



##### 키워드 반응 함수 #####

# 기본 인삿말에 맞는 응답을 반환
def hi(key):
    if (key == '인사'):
        res = '안녕하세요, 만나서 반갑습니다.'
    elif (key == '감사'):
        res = '이용해 주셔서 감사합니다.'
    elif (key == '도움'):
        res = firstMessage()
    else:
        '무슨 말인지 모르겠어요.'
    return res

# 제시된 증상에 맞는 약 이름 list를 반환
# Return -1 for 해당 약 없음
# Return 약 이름 list for 해당 약 있음
def whichPill(fac):
    pills = []
    cnt = 0
    for i in range(len(df)):
        efcy = df.iat[i, 2]
        if fac in efcy:
            pills.append(df.iat[i, 1])
            cnt += 1
    
    if cnt == 0:
        return -1
    return pills



##### main격 함수 #####

# 텍스트에서 증상을 발견하여 (증상 키워드, 해당 약) 반환
# Return -1 for 증상 감지되지 않음
# Return (증상 목록, 약 목록) for 증상 발견
def findCure(text):
    words = text2words(text)
    ills = []
    pill_list = []
    cnt = 0

    for word in words:
        word = word.rstrip('약')

        if(len(word) < 2):
            continue

        pills = whichPill(word)
        # 해당 단어가 유효한 증상이 아닌 경우 무시
        if (pills == -1):
            continue

        # 해당 단어가 유효한 증상인 경우 증상 목록에 추가
        ills.append(word)
        cnt += 1

        # 첫 증상인 경우 약 목록 초기화
        if not pill_list:
            pill_list = pills
        
        # 첫 증상이 아닌 경우, pill_list에 효과에 증상을 모두 포함하는 약만 남김
        if (cnt > 1):
            for pill in pill_list:
                if pill not in pills:
                    pill_list.remove(pill)
    
    if (cnt == 0):
        return -1

    return (ills, pill_list)

# ***** front에서는 이 함수만 호출하면 됨!!! *****
# 입력 텍스트를 인자로 넘겨주어야 함
# 사용자가 입력한 텍스트에 따라 알맞은 응답을 반환
def respond(text):
    keyword = text2key(text)
    pill = text2pill(text)

    res = """무슨 말인지 모르겠어요.
질문을 제대로 인식하지 못했거나, 데이터베이스에 물어보신 사항에 해당하는 정보가 없어요.
물어보시고자 하는 내용의 주요 단어를 띄어쓰기로 구분해 다시 질문해 보시겠어요?"""

    # 키워드가 여러 개인 경우
    if (keyword == 0):
        res = "한 번에 하나씩 질문해 주세요."
    
    # 사용자가 제시한 약 이름에 해당하는 약이 여러 개인 경우
    # ex) 이지엔 => 이지엔6, 이지엔6이브, 이지엔6스트롱 등
    elif (type(pill) is list) and (keyword != -1):
        pill_str = '[' + ', '.join(pill) + ']'
        res = "아래 약 목록 중 어느 약 말씀이신가요?\n" + pill_str

    # 사용자가 알맞은 약 이름과 키워드를 제시한 경우
    elif (type(pill) is str) and (keyword != -1):
        res = pill + "의 " + keyword + "(은)는: \n" + getData(pill, keyword)

    else:
        cure = findCure(text)
        key = text2hi(text)

        # 사용자가 증상에 맞는 약을 물어본 경우
        if not (cure == -1):
            istr = ', '.join(cure[0]) #증상
            pstr = ', '.join(cure[1]) #
            res = "증상 [" + istr + "]에 대한 약은 [" + pstr + "] 등이 있습니다."
        
        # 사용자가 인사한 경우
        elif not (key == -1):
            res = hi(key)
        
    return res