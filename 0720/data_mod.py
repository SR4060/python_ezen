import pandas as pd
import os
from glob import glob

def read_df(_path, _encoding="utf-8"):
    # 해당 파일과 확장자 분리
    # head: csv/2021/202101_exepense_list
    # tail: .csv
    head, tail = os.path.splitext(_path)
    if tail == ".csv":
        df=pd.read_csv(_path, encoding=_encoding)
    elif tail == ".tsv":
        df=pd.read_csv(_path, encoding=_encoding, seq="\t")
    elif tail == ".json":
        df=pd.read_json(_path, encoding=_encoding)
    elif tail in [".xlsx", "xls"]:
        df=pd.read_excel(_path, encoding=_encoding)
    elif tail == ".xml":
        df=pd.read_xml(_path, encoding=_encoding)
    else:
        df=pd.DataFrame()
    return df
    
def data_load_add(_patn, _end="csv"):
    file_list=os.listdir(_path)
    _path+="/"

    list_filter=[
        i for i in file_list if i.endswith(_end)
    ]
    result=pd.DataFrame()
    for i in list_filter:
        try:
            df=read_df(_path+i)
        except:
            try:
                df=read_df(_path+i, "CP949")
            except:
                df=read_df(_path+i, "EUC-KR")
        result=pd.concat([result, df])
    return result

def data_load(_path):
    # 입력받은 경로를 기준으로 파일의 목록을 로드
    # glob
    file_list=glob(_path+"/*.*")
    result=dict()
    for i in file_list:
        forder, name=os.path.split(i)
        head, tail=os.path.splitext(name)
        try:
            df=read_df(i)
        except:
            try:
                df=read_df(i, "CP949")
            except:
                df=read_df(i, "EUC-KR")
        # 로드한 데이터프렘의 길이가 0인 경우: 전역변수 생성x
        # 전역변수에 head 값을 사용한다.
        # 모듈을 이용해서 전역 변수 생성 불가능
        # 하나의 변수에 여러개의 데이터프레임을 저장
        # 딕셔너리 데이터를 이용하여 key에는 파일의 이름
        # values에는 데이터프레임 대입
        # 딕셔너리를 return
        print(len(df))
        if len(df) !=0:
            # globals()[head]=df.copy()
            result[head]=df.copy()
            print(f"{head} key 생성")
            print(result.keys())
        else:
            print(f"{head} 파일은 데이터 파일이 아닙니다.")
    return result