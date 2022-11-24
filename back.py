import pandas as pd
import numpy as np



##### 데이터 전처리 #####

df = pd.read_csv('pill.csv')
df.drop(columns=['Unnamed: 0', 'itemSeq', 'itemImage', 'openDe', 'updateDe'], inplace=True)

df.dropna(subset=['efcyQesitm'], inplace=True)

cols = ['atpnWarnQesitm', 'atpnQesitm', 'intrcQesitm']

df = df.fillna(' ')
df['warn']=df[cols].apply(lambda row:' '.join(row.values.astype(str)), axis=1)
df.drop(columns=cols, inplace=True)



##### 약 이름, 키워드 규칙 #####

PILLS = df['itemName'].values.tolist()
KEYWORDS = {0:['회사', '제조사'],
            1:['이름', '제품명'],
            2:['효과', '효능', '약효'],
            3:['용법', '복용', '얼마나', '언제', '적정'],
            4:['부작용'],
            5:['보관'],
            6:['주의', '경고', '유의']}



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



##### 주요 기능 함수 #####

# 약 이름과 키워드에 따라 알맞는 data를 반환
def getData(pill, keyword):
    ridx = getRIndex(pill)
    cidx = getCIndex(keyword)
    return df.iat[ridx, cidx]

# 제시된 증상에 맞는 약 이름 list를 반환
def whichPill(fac):
    pills = []
    for i in range(len(df)):
        efcy = df.iat[i, 2]
        if fac in efcy:
            pills.append(df.iat[i, 1])
    return pills

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
# Return 0 for 약 이름 다수
# Return 약 이름 for 약 이름 하나
def text2pill(text):
    cnt = 0
    pills = []
    for item in PILLS:
        if item in text:
            cnt += 1
            pills.append(item)
    
    if cnt == 0:
        return -1
    if cnt == 1:
        return pills[0]
    return 0



##### main격 함수 #####

# front에서는 이 함수만 호출하면 됨
# 입력 텍스트에 따라 적절한 응답 텍스트를 반환
def respond(text):
    keyword = text2key(text)
    pill = text2pill(text)
    if (keyword == -1 or pill == -1):
        res = "무슨 말인지 모르겠어요."
        return res
    elif (keyword == 0 or pill == 0):
        res = "한 번에 하나씩 질문해 주세요."
        return res
    else:
        return getData(pill, keyword)



##### TEST CODE #####
    
text1 = '안녕하세요, 아네모정의 보관은 어떻게 하나요?'
text2 = '아네모정 보관방법'
text3 = '안녕하세요'
text4 = '아네모정 보관방법 제조사'

print(respond(text1))
print(respond(text2))
print(respond(text3))
print(respond(text4))
print(whichPill('편두통'))