import os
import pandas as pd
import re

df = pd.read_csv(r'pill.csv')



##### 기본 정리 #####

#불필요한 행 삭제
df.drop(columns=['Unnamed: 0', 'itemSeq', 'itemImage', 'openDe', 'updateDe'], inplace=True)

# 데이터에 오류가 있는 행 삭제
df.dropna(subset=['efcyQesitm'], inplace=True)
df.reset_index(drop=True, inplace=True)

# 주의사항 한 행으로 병합
cols = ['atpnWarnQesitm', 'atpnQesitm', 'intrcQesitm']

df = df.fillna('')
df['warn']=df[cols].apply(lambda row:''.join(row.values.astype(str)), axis=1)
df.drop(columns=cols, inplace=True)



##### 약 이름 정리 #####

pills = df['itemName'].values.tolist()
change = {'mg': ['밀리그람', '밀리그램'], 'IU':['아이유'], '뒤까지싹다지우기':['수출명'], '뒤만지우기':['캡슐/정[***/**** IU/mg]', 'mg', '']}
elems = ['이부프로펜', '나프록센', '나프록센나트륨', '덱시부프로펜', '아세트아미노펜', '소브레롤', '아세틸시스테인', '히알루론산나트륨', '카페인무수물', '염화나트륨']

final = []

for item in pills:
    # 수출명 삭제
    tmp = re.sub('수출명.+', '', item)
    # 단위 표기 통일
    tmp = re.sub('밀리그람|밀리그램', 'mg', tmp)
    tmp = re.sub('밀리리터', 'ml', tmp)
    tmp = re.sub('아이유', 'IU', tmp)
    # 불필요 성분명 삭제
    for elem in elems:
        if elem in tmp:
            rule = elem + '$'
            tmp = re.sub(rule, '', tmp)
    # 약 이름 뒤에 붙는 불필요 수식어(성분명 등) 일괄 삭제
    tmp = re.sub(r'((캡슐|정|액|시럽)[0-9]*(mg|IU)).+', r'\1', tmp)
    tmp = re.sub(r'([^^](캡슐|정|액|시럽))[^0-9].+', r'\1', tmp)

    final.append(tmp)

df['itemName'] = final



##### 본문 내용 편집 #####

strCol = ['efcyQesitm', 'useMethodQesitm', 'seQesitm', 'depositMethodQesitm', 'warn']
size = len(df)

for i in range(size):
    for col in strCol:
        text = df[col][i]
        text = re.sub(r'니다([^\.]|$)', r'니다. \1', text)
        text = re.sub(r'시오([^\.]|$)', r'시오. \1', text)
        text = text.strip()
        df[col][i] = text



df.to_csv(r'pill_processed.csv', index=False)