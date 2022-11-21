import pandas as pd
import numpy as np

df = pd.read_csv('pill_db_after_preprocessing.csv')
df.drop(df.columns[[0, 1]], axis=1, inplace=True)
df.dropna(axis=0, inplace=True)

pill_list = df['ITEM_NAME'].values.tolist()

KEYWORDS = {0:['이름'],
            1:['회사'],
            2:['종류', '분류'],
            3:['보관']}

# 약 이름에 따라 알맞는 row index를 반환
def getRIndex(pill):
    return df.index[df['ITEM_NAME'] == pill][0]

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
    for item in pill_list:
        if item in text:
            cnt += 1
            pills.append(item)
    
    if cnt == 0:
        return -1
    if cnt == 1:
        return pills[0]
    return 0

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

text1 = '안녕하세요, 슬카인정의 보관은 어떻게 하나요?'
text2 = '슬카인정 보관방법'
text3 = '안녕하세요'
text4 = '슬카인정 보관방법 제조사'

print(respond(text1))
print(respond(text2))
print(respond(text3))
print(respond(text4))